#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Gets Umbrella Reporting site activity for a site specified
via CLI argument.
"""

import sys
from cisco_umbrella_reporting import CiscoUmbrellaReporting


def main(site_url):
    """
    Execution starts here.
    """

    # Instantiate a new Umbrella Reporting object from env vars
    umb_rep = CiscoUmbrellaReporting.build_from_env_vars()

    # Given a URL to check, collect the activity from that URL
    data = umb_rep.req(f"destinations/{site_url}/activity")

    # Create the column names for the CSV file
    text = "date,device_id,device_type,device_name,site,action,categories\n"
    outfile = f"site_activity_{site_url.replace('.', '_')}.csv"

    # Iterate over all requests logged by Umbrella Reporting
    for item in data["requests"]:

        # Append the key data items to the text string. Categories are
        # joined from a list of strings into a single space-delineated string
        text += f"{item['datetime']},{item['originId']},{item['originType']},"
        text += f"{item['originLabel']},{item['destination']},"
        text += f"{item['actionTaken']},{' '.join(item['categories'])}\n"

    # Write the text to the outfile and print useful command to read it
    with open(outfile, "w") as handle:
        handle.write(text)
    print(f"Use 'column -s, -t {outfile} | less -S' to view from shell")


if __name__ == "__main__":
    # User must supply a CLI argument of the SHA256 hash for the
    # application to blacklist. If not, print error message and exit
    # with error code
    if len(sys.argv) < 2:
        print("usage: python get_site_activity.py <site_to_check>")
        sys.exit(1)

    # Extract the CLI argument (website name) and pass into main()
    # Example: www.internetbadguys.com
    main(sys.argv[1])
