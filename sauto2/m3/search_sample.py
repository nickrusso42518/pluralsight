#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Search for samples based on a variety of parameters.
"""

from cisco_tg import CiscoTG


# Identify a hash to search for (this is calc.exe)
SHA256 = "3091e2abfb55d05d6284b6c4b058b62c8c28afc1d883b699e9a2b5482ec6fd51"


def main():
    """
    Execution starts here.
    """

    # Create a new CiscoTG object and specify optional sample parameters
    tg = CiscoTG.build_from_env_vars()

    # Define a nested dictionary of searches demonstrating both
    # simple and advanced searchin techniques
    searches = {
        "At most 3 failed": {"state": "fail", "limit": 3},
        "SHA256 for calc.exe": {"advanced": True, "q": f"sha256:{SHA256}"},
    }

    # Unpack the dictionary by iterating over the keys and values in parallel
    for name, params in searches.items():

        # Print decorative message with the proper number of hyphens
        msg = f"Executing search: {name}"
        print(f"{len(msg) * '-'}\n{msg}\n")

        # Perform the search and store the results
        results = tg.req("search/submissions", params=params)

        # Iterate over the results within the items list
        for result in results["data"]["items"]:

            # Extract the sample ID, status, and submission time for display
            data = result["item"]
            print(f"Sample ID: {data['sample']}")
            print(f"Status: {data['status']}")
            print(f"Submission time: {data['submitted_at']}\n")


if __name__ == "__main__":
    main()
