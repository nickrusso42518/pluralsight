#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Example showing how the inspect and enrich API operations can
surface, expose, and investigate threats.
"""

import os
from cisco_xdr import CiscoXDR


def _process_refer(data):
    """
    Process the refer data, focusing on actions and URLs to check.
    """
    for item in data["data"]:
        print(f"Action: {item['description']}/URL: {item['url']}")


def _process_deliberate(data):
    """
    Process the deliberate data, focusing on verdicts/dispositions.
    """
    for item in data["data"]:
        if not "verdicts" in item["data"].keys():
            continue

        for doc in item["data"]["verdicts"]["docs"]:
            obs = doc["observable"]["value"]
            print(
                f"{obs}: {doc['disposition_name']}, verdict"
                f" valid until {doc['valid_time']['end_time']}"
            )


def _process_observe(data):
    """
    Process the observe (detailed) data, focusing on the judgement
    severity and confidence levels.
    """
    for item in data["data"]:
        if "judgements" in item["data"].keys():
            for doc in item["data"]["judgements"]["docs"]:
                obs = doc["observable"]["value"]
                print(f"{obs}: Sev {doc['severity']}/Conf {doc['confidence']}")
                print(f"  Judgement reason: {doc['reason']}")


def main():
    """
    Execution starts here.
    """

    # Create a new XDR instance with default (DevNet LL) parameters
    xdr = CiscoXDR.make_devnet_client()

    # Check for errors with enrichment modules, which can be slow
    # (they exist in DevNet, but shouldn't in a prod env)
    enrich_health = xdr.req("iroh-enrich/health", method="post")
    for error in enrich_health["errors"]:
        print(f"{error['module']} error: {error['message']}")

    # Iterate over all input files
    for input_file in os.listdir("inputs/"):
        with open(f"inputs/{input_file}", "r") as handle:
            data = handle.read()

        # Inspect the raw text for any observables
        print(f"\nInspect: {input_file}")
        observables = xdr.req(
            "iroh-inspect/inspect", method="post", jsonbody={"content": data}
        )

        # Enrich the observables using three different techniques
        enrich_actions = ["refer", "deliberate", "observe"]

        # Iteratively apply the aforementioned techniques
        for enrich_action in enrich_actions:
            print(f"\n{60 * '-'}\n{enrich_action.upper()}")

            # API is easy to use; many requests use the exact output
            # from the inspection process (list of observables)
            url = f"iroh-enrich/{enrich_action}/observables"
            enrich_data = xdr.req(url, method="post", jsonbody=observables)

            # Call the proper method, based on action name, to process result
            globals()[f"_process_{enrich_action}"](enrich_data)


if __name__ == "__main__":
    main()
