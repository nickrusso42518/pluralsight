#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Tests Batfish on sample Cisco Live sessions focused
on the OSPF routing protocol using archived configurations.
"""

import json
import os
import pytest
from pybatfish.client import asserts
from pybatfish.client.session import Session
from pybatfish.datamodel.flow import HeaderConstraints, RoutingStepDetail


@pytest.fixture(scope="module")
def bf(snapshot_name):
    """
    Perform basic initialization per documentation and return "bf" dict
    so tests can interface with batfish. This includes the bf session
    plus the batfish answers to all required questions at once.
    This centralizes access to basic data for the tests and also
    stores it on disk for troubleshooting or access by another script.
    """

    # Initialize the BF session and snapshot from CLI argument
    snap_dir = f"bf/snapshots/{snapshot_name}"
    bf_session = Session(host="localhost")
    bf_session.set_network(snapshot_name)
    bf_session.init_snapshot(snap_dir, name=snapshot_name, overwrite=True)

    # Collect all of the answers needed about the topology
    bf = {
        "nodes": bf_session.q.nodeProperties().answer().frame(),
        "nbrs": bf_session.q.ospfEdges().answer().frame(),
        "intfs": bf_session.q.ospfInterfaceConfiguration().answer().frame(),
        "procs": bf_session.q.ospfProcessConfiguration().answer().frame(),
        "areas": bf_session.q.ospfAreaConfiguration().answer().frame(),
        "compat": bf_session.q.ospfSessionCompatibility().answer().frame(),
        "iprops": bf_session.q.interfaceProperties().answer().frame(),
        "rtes": bf_session.q.routes().answer().frame(),
    }

    # Ensure the state directory exists for BF answer/topology data
    out_dir = f"bf/state/{snapshot_name}"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Write each answer to disk in JSON format
    for name, df in bf.items():
        json_data = json.loads(df.to_json(orient="records"))
        with open(f"{out_dir}/{name}.json", "w") as handle:
            json.dump(json_data, handle, indent=2)

    # Merge dict into bf containing the raw BF session for customization
    return bf | {"bf": bf_session}


@pytest.fixture(scope="module")
def cle(bf):
    """
    Returns a string:bool mapping to determine whether a node can
    learn OSPF external routes or not. Routers that cannot are non-ABRs
    existing only within stub/NSSA areas. Short for "can learn externals".
    """

    # Map node name to true (has externals) or false (lacks externals)
    node_dict = {}

    # Process data tells us area assignments and ABR status
    for _, proc in bf["procs"].iterrows():
        # If node is an ABR, it can definitely learn external routes
        if proc["Area_Border_Router"]:
            node_dict[proc["Node"]] = True
            continue

        # Node is not an ABR. Need to examine individual area assignments,
        # assume can-learn-externals (cle) is False to begin
        cle = False

        # Area tells us area types (STUB, NSSA, NONE)
        for check in proc["Areas"]:
            for _, area in bf["areas"].iterrows():
                # If we found the matching node/area pair, check the area type.
                # If a non-ABR exists only in stub areas, it cannot learn
                # externals, but we must check *all* areas to be certain
                if proc["Node"] == area["Node"] and check == area["Area"]:
                    node_dict[proc["Node"]] = cle or area["Area_Type"] != "STUB"

    # Sanity check; ensure node counts are equal between data structures
    assert len(node_dict) == len(bf["procs"])
    return node_dict


def test_no_duplicate_router_ids(bf):
    """
    Use the built-in batfish function to ensure OSPF RIDs are unique.
    """
    asserts.assert_no_duplicate_router_ids(session=bf["bf"])


def test_no_incompatible_ospf_sessions(bf):
    """
    Use the built-in batfish function to ensure OSPF neighbors are compatible.
    """
    asserts.assert_no_incompatible_ospf_sessions(session=bf["bf"])


def test_no_forwarding_loops(bf):
    """
    Use the built-in batfish function to ensure there are no L3 loops.
    """
    asserts.assert_no_forwarding_loops(session=bf["bf"])


def test_compatible_neighbors_up(bf):
    """
    Ensure the number of compatible and established neighbors are the same.
    This is more of a sanity check and will seldom fail.
    """
    assert len(bf["compat"]) == len(bf["nbrs"])


def test_symmetric_costs(bf):
    """
    Since the target network uses equal costs on all ends of a link/segment,
    ensure that those costs are the same. This prevents asymmetric routing.
    """
    intfs = bf["intfs"]
    for _, nbr in bf["nbrs"].iterrows():
        li, ri = nbr["Interface"], nbr["Remote_Interface"]
        lc = intfs.loc[intfs["Interface"] == li, "OSPF_Cost"].values[0]
        rc = intfs.loc[intfs["Interface"] == ri, "OSPF_Cost"].values[0]
        assert lc == rc


def test_complementary_descriptions(bf):
    """
    Routers on P2P links should have descriptions ending with the peer's
    hostname, such as "TO R10" on R02's link towards R10.
    """
    iprops = bf["iprops"]
    nbrs = bf["nbrs"]
    p2ps = bf["intfs"].loc[
        bf["intfs"]["OSPF_Network_Type"] == "POINT_TO_POINT", "Interface"
    ]

    # Loop over P2P interface ... a Series, not a DataFrame, so no iterrows()
    for p2p in p2ps:
        desc = iprops.loc[iprops["Interface"] == p2p, "Description"].values[0]
        nbr = nbrs.loc[nbrs["Interface"] == p2p, "Remote_Interface"].values[0]
        assert desc == f"TO {nbr.hostname.upper()}"


def test_stubs_lack_externals(bf, cle):
    """
    Ensure stub nodes lack the external routes redistributed by R10.
    """
    rtes = bf["rtes"]
    for node in [k for k, v in cle.items() if not v]:
        oe2 = rtes.loc[(rtes["Protocol"] == "ospfE2") & (rtes["Node"] == node)]
        assert len(oe2) == 0


def test_stubs_have_default(bf, cle):
    """
    Ensure stub nodes have exactly one default route via R01.
    """
    rtes = bf["rtes"]
    for node in [k for k, v in cle.items() if not v]:
        defrte = rtes.loc[
            (rtes["Protocol"] == "ospfIA")
            & (rtes["Network"] == "0.0.0.0/0")
            & (rtes["Node"] == node),
            "Next_Hop_IP",
        ]
        assert len(defrte) == 1
        assert defrte.values[0].startswith("10.1.")
        assert defrte.values[0].endswith(".1")


def test_stubs_have_interareas(bf, cle):
    """
    Ensure stub nodes have at least one non-default inter-area route
    via R14. Also, these nodes must have an equal number of such routes.
    """
    rtes = bf["rtes"]
    other_set = set()
    for node in [k for k, v in cle.items() if not v]:
        others = rtes.loc[
            (rtes["Protocol"] == "ospfIA")
            & (rtes["Network"] != "0.0.0.0/0")
            & (rtes["Node"] == node),
            "Next_Hop_IP",
        ]
        assert len(others) > 0
        other_set.add(len(others))
        for other in others:
            assert other.startswith("10.")
            assert other.endswith(".14.14")

    # Ensure stub nodes all saw same number of routes
    assert len(other_set) == 1


def test_nonstubs_have_externals(bf, cle):
    """
    Ensure backbone/NSSA nodes have the external routes redistributed by R10.
    Note that the ASBR itself will not have these external routes, but should
    have corresponding connected routes instead.
    """

    # Gather all OE2 routes in the network
    rtes = bf["rtes"]
    all_oe2 = rtes.loc[(rtes["Protocol"] == "ospfE2")]

    for node in [k for k, v in cle.items() if v]:
        # Get the node-specific OE2 routes and ensure more than zero exist
        oe2 = all_oe2.loc[(rtes["Node"] == node)]
        try:
            assert len(oe2) > 0

        except AssertionError:
            # This code runs for the ASBRs. Check the node's connected routes, then
            # for each unique OE2 route (using a set), ensure there is
            # exactly one corresponding connected route
            conn = rtes.loc[
                (rtes["Protocol"] == "connected") & (rtes["Node"] == node)
            ]
            for unique_oe2 in set(all_oe2.Network.values):
                assert len(conn.loc[conn["Network"] == unique_oe2]) == 1


def _run_traceroute(bf, params):
    """
    Helper function to run a undirectional traceroute based on the params
    dict, including "src" and "dest" targets formatted as "node[intf]".
    Ensures ACCEPTED disposition and returns pandas dataframe.
    """

    # Define source/dest traceroute and run it
    headers = HeaderConstraints(dstIps=params["dest"])
    df = (
        bf.q.traceroute(startLocation=params["src"], headers=headers)
        .answer()
        .frame()
    )

    # Write traceroute to disk in JSON format
    out_dir = f"bf/state/{params['snap']}"
    json_data = json.loads(df.to_json(orient="records"))

    # Example filename format: "r13[Loopback0]_2_r10[Loopback1].json"
    name = f"{params['src']}_2_{params['dest']}"
    with open(f"{out_dir}/{name}.json", "w") as handle:
        json.dump(json_data, handle, indent=2)

    # Perform basic assertion that probes were accepted
    assert df.Traces[0][0].disposition == "ACCEPTED"
    return df


def test_traceroute_stub_to_nssa_interarea(bf, cle, snapshot_name):
    """
    Run unidirectional traceroute from stub nodes to an NSSA inter-area
    destination, which must follow longer matches via R14.
    """
    for node in [k for k, v in cle.items() if not v]:
        params = {
            "src": f"{node}[Loopback0]",
            "dest": "r10[Loopback0]",
            "snap": snapshot_name,
        }
        tracert = _run_traceroute(bf["bf"], params)

        # Loop over routing steps only
        for tstep in tracert.Traces[0][0][0].steps:
            if isinstance(tstep.detail, RoutingStepDetail):
                # Extract the first route and check prefix/next-hop
                route = tstep.detail.routes[0]
                assert route.network != "0.0.0.0/0"
                assert route.nextHop.ip.startswith("10.")
                assert route.nextHop.ip.endswith(".14.14")
                break


def test_traceroute_stub_to_nssa_external(bf, cle, snapshot_name):
    """
    Run unidirectional traceroute from stub nodes to an NSSA external
    destination, which must follow the default route via R01.
    """
    for node in [k for k, v in cle.items() if not v]:
        params = {
            "src": f"{node}[Loopback0]",
            "dest": "r10[Loopback1]",
            "snap": snapshot_name,
        }
        tracert = _run_traceroute(bf["bf"], params)

        # Loop over routing steps only
        for tstep in tracert.Traces[0][0][0].steps:
            if isinstance(tstep.detail, RoutingStepDetail):
                # Extract the first route and check prefix/next-hop
                route = tstep.detail.routes[0]
                assert route.network == "0.0.0.0/0"
                assert route.nextHop.ip.startswith("10.1.")
                assert route.nextHop.ip.endswith(".1")
                break


def test_generate_topology(bf, snapshot_name):
    """
    Collects the OSPF edges and writes them to disk in JSON format.
    It also reforms the topology to dynamically discover multi-access networks
    so that GNS3 can add an "etherswitch" to the topology.
    This can be consumed by the lab simulation topology builder script.
    """

    # Get the unidirectional OSPF neighbors (links) and load them as JSON data
    json_data = json.loads(bf["nbrs"].to_json(orient="records"))

    # Find links that have a duplicate "Interface" dict, indicating a
    # multi-access network. Use an anomymous lambda function to create a
    # hashable dict of each "Interface" within the json_data list.
    seen = set()
    dupes = []
    for intf in map(lambda d: frozenset(d["Interface"].items()), json_data):
        # If we haven't seen this hostname/interface pair, it's unique
        if not intf in seen:
            seen.add(intf)

        # We've seen it before, so it's a duplicate (ie, multi-access network)
        else:
            dupes.append(intf)

    # Extract the duplication hostnames via set comprehension
    remaining_hosts = {dict(dupe)["hostname"] for dupe in dupes}

    # Increment counter for the GNS3 "etherswitch" interface numbering
    # and initialize an empty list to track those "reverse" links
    sw_intf = 0
    sw_to_node_links = []

    # Check entire topology for those duplicate interfaces
    for link in json_data:
        if frozenset(link["Interface"].items()) in dupes:
            # If we haven't processed that duplicate, process the swap
            if link["Interface"]["hostname"] in remaining_hosts:
                # Overwrite the remote hostname and interface accordingly,
                # and remove the host from the set because it's just been processed
                link["Remote_Interface"]["hostname"] = "sw"
                link["Remote_Interface"]["interface"] = f"0/{sw_intf}"
                remaining_hosts.remove(link["Interface"]["hostname"])

                # Generate the "reverse" link from etherswitch to node
                sw_to_node_links.append(
                    {
                        "Interface": {
                            "hostname": "sw",
                            "interface": f"0/{sw_intf}",
                        },
                        "Remote_Interface": {
                            "hostname": link["Interface"]["hostname"],
                            "interface": link["Interface"]["interface"],
                        },
                    }
                )

                # Increment the switch interface counter
                sw_intf += 1

            # Host was already processed; mark duplicate element for removal
            else:
                link["remove"] = True

    # Rebuild the topology list by excluding items marked as "remove",
    # then extend the etherswitch "reverse" links to the end
    all_links = [link for link in json_data if not link.get("remove")]
    all_links.extend(sw_to_node_links)

    # Augment the topological links with node information
    topology = {"all_links": all_links, "nodes": {}}
    for _, node in bf["nodes"].iterrows():
        topology["nodes"][node["Node"]] = node["Configuration_Format"]

    # Add the Ethernet switch as a node, despite Batfish not seeing it
    if len(dupes) > 0:
        topology["nodes"]["sw"] = "nonbf-gns3-ethsw"

    # Write resulting topology to disk in pretty format
    out_dir = f"bf/state/{snapshot_name}"
    with open(f"{out_dir}/topology.json", "w") as handle:
        json.dump(topology, handle, indent=2)
