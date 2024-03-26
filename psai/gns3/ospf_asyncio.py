#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Uses scrapli and asyncio to validate the live topology,
similar to Batfish, except using simulated devices and "show" commands.
"""

import asyncio
import logging
import json
import operator as op
import os
import sys
from scrapli import AsyncScrapli


async def main(snapshot_name):
    """
    Execution starts here (coroutine). Targets a specific Batfish
    snapshot, using those Scrapli parameters
    """

    # Ensure the logs directory exists for virtual topology test results
    out_dir = "gns3/logs"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Basic parameters common to all nodes in the topology
    base_params = {
        "host": "192.168.120.128",  # Targetting GNS3 VM, not laptop client
        "transport": "asynctelnet",  # or "asyncssh" if desired
        "auth_bypass": True,  # don't perform telnet authentication
        "comms_return_char": "\r\n",  # Cisco "Press RETURN to get started."
    }

    # Load device/console port mappings dynamically built from GNS3
    in_dir = "gns3/params"
    device_file = f"{in_dir}/{snapshot_name}.json"
    with open(device_file, "r") as handle:
        device_map = json.load(handle)

    # Instantiate coroutines into objects, assemble into list for
    # all devices. Regardless of OS, they can all run together
    coros = [
        globals()[params["platform"]](device, snapshot_name, base_params | params)
        for device, params in device_map.items()
    ]

    # Encapsulate all coro objects in a future, then await concurrent completion
    coro_future = asyncio.gather(*coros)
    await coro_future

    # We now have the future results. Print them (the prompts) to indicate
    # successful validation of those nodes
    print("Validated nodes:")
    for result in coro_future.result():
        print(result)


async def juniper_junos(hostname, snapshot_name, conn_params):
    """
    Coroutine to collect information from Juniper JunOS devices. The
    only assertions performed are procedural/technical sanity checks.
    """

    # Create a logger for this node in CSV format
    logger = setup_logger(f"gns3/logs/{hostname}_log.csv")

    # Update the dict to set custom open/close actions
    conn_params |= {"on_open": _open_junos, "on_close": _close_junos}

    # Open async connection to the node and auto-close when context ends
    async with AsyncScrapli(**conn_params) as conn:
        # Get the prompt and ensure the supplied hostname matches
        prompt = await conn.get_prompt()
        test(prompt.strip(), op.eq, "root>", logger)

        # Load the initial config (cannot be done via GNS3 API)
        filepath = f"bf/snapshots/{snapshot_name}/configs/{hostname.upper()}.txt"
        await conn.send_configs_from_file(filepath, stop_on_failed=True)

        # Prompt changes after hostname change. Example: root@R01>
        new_prompt = f"root@{hostname.upper()}>"

        # Commit and quit config mode, check for new prompt.
        await conn.send_and_read(
            channel_input="commit and-quit",
            expected_outputs=new_prompt,
            timeout_ops=180,
            read_duration=180,
        )
        await asyncio.sleep(60)

        # Test for the presence of the new prompt
        prompt = await conn.get_prompt()
        test(prompt.strip(), op.eq, new_prompt, logger)

        # Collect the OSPF neighbors, interfaces, and LSDB
        resps = await conn.send_commands(
            [
                "show ospf neighbor",
                "show ospf interface",
                "show ospf database",
            ]
        )

        # Use a dict since we need to conduct parsing using a mix of
        # built-in and custom templates. Templatize the path to reduce typing
        tmpl = "gns3/textfsm/templates/juniper_junos_show_ospf_{}.textfsm"
        data = {
            "nbrs": resps[0].textfsm_parse_output(),
            "intfs": resps[1].textfsm_parse_output(
                template=tmpl.format("interface")
            ),
            "lsas": resps[2].textfsm_parse_output(
                template=tmpl.format("database")
            ),
        }

        # Load in the OSPF interfaces from batfish, then create
        # a dict keyed by the unique interface name referencing the main dict.
        # Only include dicts that match this host for node-specific testing
        with open(f"bf/state/{snapshot_name}/intfs.json", "r") as handle:
            bf_intfs = {
                intf["Interface"]["interface"]: intf
                for intf in json.load(handle)
                if intf["Interface"]["hostname"].lower() == hostname
            }

        # Validate interfaces by checking for correct area, never having BDR,
        # and only having a DR with R2 on port 2
        for intf in data["intfs"]:
            test(
                int(intf["area"][-1]),
                op.eq,
                bf_intfs[intf["intf"]]["OSPF_Area_Name"],
                logger,
            )
            test(intf["bdr_id"], op.eq, "0.0.0.0", logger)
            if intf["intf"] == "em2.0":
                test(intf["dr_id"], op.eq, "10.0.0.2", logger)
            else:
                test(intf["dr_id"], op.eq, "0.0.0.0", logger)

        # Validate neighbors by checking for FULL state if priority is more
        # zero, or 2WAY otherwise (correct in our design, at least)
        for nbr in data["nbrs"]:
            state = "Full" if int(nbr["priority"]) > 0 else "2Way"
            test(nbr["state"], op.eq, state, logger)

        # Validate LSDB by ensuring there is exactly one Network LSA
        # originated by R2 (DR) on LAN segment
        lsa2_count = 0
        for lsa in data["lsas"]:
            if lsa["type"] == "Network":
                lsa2_count += 1
                test(lsa["lsa_id"], op.eq, "10.0.99.2", logger)

        test(lsa2_count, op.eq, 1, logger)

    # Coroutines can return data, too; just return the prompt
    return prompt


async def cisco_iosxe(hostname, snapshot_name, conn_params):
    """
    Coroutine to collect information from Cisco IOS-XE devices. The
    only assertions performed are procedural/technical sanity checks.
    """

    # Create a logger for this node in CSV format
    logger = setup_logger(f"gns3/logs/{hostname}_log.csv")

    # Update the dict to set a custom close
    # Scrapli is smart enough to send "enable" if needed on open
    conn_params["on_close"] = _close_iosxe

    # Open async connection to the node and auto-close when context ends
    async with AsyncScrapli(**conn_params) as conn:
        # Get the prompt and ensure the supplied hostname matches
        prompt = await conn.get_prompt()
        test(prompt.lower().strip(), op.eq, hostname + "#", logger)

        # NOT NEEDED FOR IOU, but you can perform IOS-XE initialization
        # for a specified snapshot here, if necessary. Example:
        # filepath = f"snapshots/{snapshot_name}/configs/{hostname.upper()}.txt"
        # await conn.send_configs_from_file(filepath, stop_on_failed=True)

        # Collect the OSPF neighbors, interfaces, and LSDB
        resps = await conn.send_commands(
            [
                "show ip ospf neighbor",
                "show ip ospf interface brief",
                "show ip ospf database",
            ]
        )

        # Create named indices to improve readability, then parse with textfsm
        nbrs, intfs, lsas = range(3)
        data = [resp.textfsm_parse_output() for resp in resps]

        # Load in the compatible OSPF neighbors from batfish, then create
        # a dict keyed by the unique interface name referencing the main dict.
        # Only include dicts that match this host for node-specific testing
        with open(f"bf/state/{snapshot_name}/compat.json", "r") as handle:
            compat = {
                nbr["Interface"]["interface"]: nbr
                for nbr in json.load(handle)
                if nbr["Interface"]["hostname"].lower() == hostname
            }

        # Loop over textfsm-parsed OSPF interfaces
        areas_seen = set()
        for intf in data[intfs]:
            # Convert Et to Ethernet for comparison
            long_intf = _expand_intf(intf["interface"])

            # Ensure the area and IP addresses match what batfish thinks.
            # Don't try this on loopbacks as they never have neighbors
            if not "Loopback" in long_intf:
                test(compat[long_intf]["IP"], op.eq, intf["ip_address"], logger)
                test(compat[long_intf]["Area"], op.eq, int(intf["area"]), logger)
                areas_seen.add(compat[long_intf]["Area"])

        # If this router is in area 0 ...
        if 0 in areas_seen and hostname.lower() != "r02":
            # It must have a FULL neighbor with R2, the LAN segment DR
            r02 = [n for n in data[nbrs] if n["neighbor_id"] == "10.0.0.2"][0]
            test(int(r02["priority"]), op.eq, 1, logger)
            test(r02["state"], op.eq, "FULL/DR", logger)
            test(r02["ip_address"], op.eq, "10.0.99.2", logger)

            # It must also have R2's network LSA
            lsa2 = [l for l in data[lsas] if l["link_id"] == "10.0.99.2"][0]
            test(lsa2["adv_router"], op.eq, "10.0.0.2", logger)

        # You get the idea ... challenge: add more tests!

    # Coroutines can return data, too; just return the prompt
    return prompt


def _expand_intf(short_intf):
    """
    Convert a short Cisco interface string (eg "Et0/0") into its
    full-length equivalent (eg "Ethernet0/0"). If there is no
    mapping, return the interface unchanged.
    """

    # Examine the first two characters of the short intf
    match short_intf[:2]:
        case "Lo":
            long_intf = "Loopback"
        case "Et":
            long_intf = "Ethernet"
        case "Fa":
            long_intf = "FastEthernet"
        case "Gi":
            long_intf = "GigabitEthernet"
        case "Se":
            long_intf = "Serial"
        case _:
            return short_intf

    # Prepend long intf string to the slot/port string
    return long_intf + short_intf[2:]


async def _open_junos(conn):
    """
    Perform initial console login and enter the CLI, then apply the standard
    terminal settings.
    """

    # Low-level interactions to enter the CLI
    login_interactions = [
        ("\n", "Amnesiac (ttyd0)\n\nlogin:"),
        ("root", "root@%"),
        ("cli", "root>"),
    ]

    # Standard Scrapli terminal settings; must repeat since we defined on_open
    setup_cmds = [
        "set cli screen-length 0",
        "set cli screen-width 511",
        "set cli complete-on-space off",
    ]

    # Perform the login interactions, being graceful on timeouts
    for cmd, resp in login_interactions:
        resp = await conn.send_and_read(
            channel_input=cmd,
            expected_outputs=[resp],
            read_duration=20,
            timeout_ops=20,
        )

    # Send terminal settings, don't care about result
    await conn.send_commands(setup_cmds)


async def _close_junos(conn):
    """
    First exit the CLI and wait for the FreeBSD shell, then
    close the channel normally.
    """
    for resp in ["root@%", "Amnesiac (ttyd0)\n\nlogin:"]:
        await conn.send_and_read(channel_input="exit", expected_outputs=[resp])
    conn.channel.transport.close()


async def _close_iosxe(conn):
    """
    Close the channel but don't send "exit"; behavior appears inconsistent
    on GNS3 terminal server. Just leave the console line open.
    """
    conn.channel.transport.close()


def setup_logger(log_file):
    """
    Given a log file name (path), this function returns a new logger
    object to write into the specified file. Also writes the column names
    of "time,value1,operator,value2,result" without any formatting.
    """

    handler = logging.FileHandler(log_file, mode="w")
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("time,value1,operator,value2,result")
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d,%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    return logger


def test(v1, oper, v2, logger=None):
    """
    Compare values v1 and v2 using the operator specified. Prints a
    message in the format "v1,oper,v2,result" separated by commas for
    easy logging via the specified logger, or to to stdout if
    no logger is specified.
    """
    sym = {
        "eq": "==",
        "ne": "!=",
        "gt": ">",
        "ge": ">=",
        "lt": "<",
        "le": "<=",
        "contains": "in",
    }
    name = oper.__name__
    display_method = logger.info if logger else print
    display_method(f"{v1},{sym.get(name, name)},{v2},{oper(v1, v2)}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
