#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect the connected computers using the Cisco AMP API.
"""

from cisco_amp import CiscoAMP


def main():
    """
    Execution starts here.
    """

    # Instantiate a new AMP object from env vars and get event list
    amp = CiscoAMP.build_from_env_vars()
    params = {
        "limit": 20,
        # Other useful query params to zero in one computers/events, etc.
        # "connector_guid": "82403470-8d83-426c-8984-3f0679f1cb7f",
        # "event_type": 553648168,
    }
    events = amp.req("events", params=params)

    # Create the column names for the CSV file
    text = "date,id,type,hostname,severity,disposition,file_name,sha256\n"
    outfile = "recent_threats.csv"

    # For each event, ensure it is related to a computer (not general events)
    for event in events["data"]:
        if "computer" not in event:
            continue

        # Append the date, event ID, type, and hostname to the string,
        # separated by commas. Sometimes the event name has commas in
        # it, so those need to be manually removed
        text += f"{event['date']},{event['event_type_id']},"
        text += f"{event['event_type'].replace(',', '')},"
        text += f"{event['computer']['hostname']},"

        # If the event has a "severity" and a "file" key, dig deeper
        if "severity" in event and "file" in event:

            # Add the severity, disposition, file name, and SHA256 hash
            mfile = event["file"]
            text += f"{event['severity']},{mfile['disposition']},"
            text += f"{mfile.get('file_name', 'N/A')},"
            text += f"{mfile['identity']['sha256']}\n"

        # The event is missing "severity" or "file"; pad with commas to align
        else:
            text += ",,,\n"

    # Write the text to the outfile and print useful command to read it
    with open(outfile, "w") as handle:
        handle.write(text)
    print(f"Use 'column -s, -t {outfile} | less -S' to view from shell")


if __name__ == "__main__":
    main()
