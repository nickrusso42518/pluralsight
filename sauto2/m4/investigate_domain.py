#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Use the Umbrella Investigate API to examine a specific
site passed in via CLI argument.
"""

import os
import json
import sys
from cisco_umbrella_investigate import CiscoUmbrellaInvestigate

# Specify constants specific to your environment/desires
OUTDIR = "domain_details"


def main(site):
    """
    Execution starts here.
    """

    # Instantiate a new Umbrella Investigate object from env vars
    umb_inv = CiscoUmbrellaInvestigate.build_from_env_vars()
    print(f"Investigating site: {site}")

    # Create output directory for JSON files
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

    # Dictionary of questions to ask Umbrella Investigate regarding
    # a user-supplied site
    resources = {
        "categorization": f"domains/categorization/{site}?showLabels",
        "dnsdb": f"dnsdb/name/a/{site}.json",
        "co_occurrences": f"recommendations/name/{site}",
        "geo": f"security/name/{site}",
    }

    # Unpack the dictionary by iterating over the key and value together
    for name, resource in resources.items():

        # Collect the details for a given resource via HTTP GET
        details = umb_inv.req(resource)

        # Determine the full output file name; use simplified name
        outfile = f"{OUTDIR}/{name}.json"

        # Store the output to disk
        with open(outfile, "w") as handle:
            json.dump(details, handle, indent=2)

        # Print status message to indicate success
        print(f"Saved data from {resource} to {outfile}")


if __name__ == "__main__":
    # User must supply a CLI argument of the site for Umbrella
    # Investigate to dig into. If not, print error message and exit
    # with error code
    if len(sys.argv) < 2:
        print("usage: python investigate_domain.py <site_to_check>")
        sys.exit(1)

    # Extract the CLI argument (website name) and pass into main()
    # Example: www.internetbadguys.com
    main(sys.argv[1])
