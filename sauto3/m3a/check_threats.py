#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Example showing how the inspect and enrich API operations can
surface, expose, and investigate threats.
"""

import os
from cisco_xdr import CiscoXDR


def main():
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
        enrich_actions = ["observe", "refer", "deliberate"]

        # Iteratively apply the aforementioned techniques
        for enrich_action in enrich_actions:
            print(f"{enrich_action}: {len(observables)} observables")

            # API is easy to use; many requests use the exact output
            # from the inspection process (list of observables)
            url = f"iroh-enrich/{enrich_action}/observables"
            enrich_data = xdr.req(url, method="post", jsonbody=observables)

if __name__ == "__main__":
    main()
