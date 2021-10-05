#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Submits the file specified in the CLI argument as a sample for
Cisco ThreatGrid analysis.
"""

import json
import os
import sys
import time
from cisco_tg import CiscoTG


# Specify constants specific to your environment/desires
CALLBACK_URL = "https://webhook.site/0b43c29f-8e0c-4ae4-9b3f-9f1df76dcaf8"
OUTDIR = "sample_details"


def main(filename):
    """
    Execution starts here.
    """

    # Create a new CiscoTG object and specify optional sample parameters
    tg = CiscoTG.build_from_env_vars()
    body = {
        "callback_url": CALLBACK_URL,
        "private": True,
        "sample_filename": "windows_calc",
    }

    # Open the file in binary format then include in POST request
    # Note the body is NOT JSON, but is www form data (use "data")
    with open(filename, "rb") as handle:
        sample = tg.req(
            "samples", method="post", files={"sample": handle}, data=body
        )

    # Store the sample ID and state for use later
    sample_id = sample["data"]["id"]
    sample_state = sample["data"]["state"]

    # While the state is not successful, keep checking every 30 seconds
    while sample_state != "succ":
        time.sleep(30)

        # Update the sample response
        sample = tg.req(f"samples/{sample_id}")
        sample_state = sample["data"]["state"]
        print(f"Sample {sample_id} in state {sample_state}")

    # Processing complete; create output directory for JSON files
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

    # These are the resources to query for a given sample (there are more)
    resources = [
        "summary",
        "threat",
        "analysis/metadata",
        "analysis/artifacts",
        "analysis/processes",
        "analysis/network_streams",
        "analysis/annotations",
        "analysis/iocs",
    ]

    # Loop over resources, issuing a GET request for each one
    for resource in resources:
        details = tg.req(f"samples/{sample_id}/{resource}")

        # Determine the full output file name, replace slash with underscore
        outfile = f"{OUTDIR}/{resource.replace('/', '_')}.json"

        # Store the output to disk
        with open(outfile, "w") as handle:
            json.dump(details, handle, indent=2)

        # Print status message to indicate success
        print(f"Saved sample details from {resource} to {outfile}")


if __name__ == "__main__":

    # User must supply a CLI argument of the file to submit for a sample
    if len(sys.argv) < 2:
        print("usage: python submit_sample.py <path_to_file>")
        sys.exit(1)

    # Ensure the file exists before continuing
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"File '{input_file}' does not exist")
        sys.exit(2)

    # Pass the filename into main() for submission. Example:
    #  /Users/nicholasrusso/calc.exe
    main(input_file)
