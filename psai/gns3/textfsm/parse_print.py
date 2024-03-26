# /usr/bin/env python

"""
Author: Nick Russo
Purpose: Test textfsm parsing using Network To Code (NTC) templates
as an introductory example. Writes output to console for quick checking.
See https://github.com/networktocode/ntc-templates for more templates.
"""

import json
import os
from ntc_templates.parse import parse_output


def main():
    """
    Execution starts here.
    """

    # For each desired output in the global list
    in_dir = "gns3/textfsm/inputs"
    for input_file in os.listdir(in_dir):
        # Load the input data from plain-text file
        print(f"\nProcessing input: {input_file}")
        with open(f"{in_dir}/{input_file}", "r") as handle:
            data = handle.read()

        # Extract the platform name and command from the filename for NTC
        show_index, dot_index = input_file.find("show"), input_file.find(".")
        ntc_params = {
            "platform": input_file[: show_index - 1],
            "command": input_file[show_index:dot_index].replace("_", " "),
        }

        # Try to parse using an NTC template. It only raises a generic
        # "Exception", but we can catch it and check the message
        try:
            records = parse_output(data=data, **ntc_params)

            # Loop over each dict in list, then iterate over the keys.
            # Try to parse integers without creating a new dict, ignore failures
            for record in records:
                for key in record:
                    try:
                        record[key] = int(record[key])
                    except ValueError:
                        pass

            # Print the first 2 records to the terminal for a quick review
            print(json.dumps(records[:2], indent=2))

        except Exception as exc:
            # Don't have a template; print error but don't crash
            if "No template found" in str(exc):
                print(str(exc))

            # Some other error occurred; re-raise
            else:
                raise


if __name__ == "__main__":
    main()
