#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect and display the SWC alerts.
"""

import json
import os
from cisco_sw_cloud import CiscoSWCloud


# Specify output directory for resulting flow files
OUTDIR = "swc_flows"


def main():
    """
    Execution starts here.
    """

    # Create new SWC object from environment variables
    swc = CiscoSWCloud.build_from_env_vars()

    # Load in the query param dicts from JSON file
    with open("flow_query_params.json", "r") as handle:
        flow_queries = json.load(handle)

    # Data loading complete; create output directory for JSON files
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

    # Iterate over each set of query params
    for name, params in flow_queries.items():

        # Collect the flows for a given set of query params
        flows = swc.req("snapshots/session-data/", params=params)

        # Write the flow data to disk
        outfile = f"{OUTDIR}/flow_{name.replace(' ', '_')}.json"
        with open(outfile, "w") as handle:
            json.dump(flows["objects"], handle, indent=2)

        # Print status message to indicate success
        print(f"Wrote flow '{name}' to {outfile}")

if __name__ == "__main__":
    main()
