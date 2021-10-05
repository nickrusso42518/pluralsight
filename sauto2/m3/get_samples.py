#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect ThreatGrid samples as a functionality test.
"""

from cisco_tg import CiscoTG


def main():
    """
    Execution starts here.
    """

    # Create a new CiscoTG object and collect up to N samples
    tg = CiscoTG.build_from_env_vars()
    samples = tg.req("samples", params={"limit": 3})

    # For each sample, print some basic information
    for sample in samples["data"]["items"]:
        print(f"Sample ID: {sample['id']}")
        print(f"State: {sample['state']}")
        print(f"Completed: {sample['completed_at']}\n")


if __name__ == "__main__":
    main()
