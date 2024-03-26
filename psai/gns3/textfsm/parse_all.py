# /usr/bin/env python

"""
Author: Nick Russo
Purpose: Test textfsm parsing using Network To Code (NTC) templates
and custom templates on various Cisco and Juniper "show" outputs.
See https://github.com/networktocode/ntc-templates for more templates.
"""

from csv import DictWriter
import json
import os
from ntc_templates.parse import parse_output
import textfsm


def to_json_file(out_dir, prefix, records):
    """
    Write the records to the output file named <prefix>.json on disk. The
    resulting JSON structure is always a single-depth list of dictionaries.
    """
    with open(f"{out_dir}/{prefix}.json", "w") as handle:
        json.dump(records, handle, indent=2)


def to_csv_file(out_dir, prefix, records):
    """
    Write the records to the output file named <prefix>.json on disk. The
    resulting JSON structure is always a single-depth list of dictionaries.
    """
    with open(f"{out_dir}/{prefix}.csv", "w") as handle:
        dict_writer = DictWriter(handle, records[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(records)


def parse_custom(prefix, data):
    """
    Given a file prefix and plain-text input data, load a custom
    textfsm template and attempt to parse records from the data.
    Returns the list of records in matrix form.
    """

    # Open the textfsm template, initialize the FSM, and parse the records
    tmpl_dir = "gns3/textfsm/templates"
    with open(f"{tmpl_dir}/{prefix}.textfsm", "r") as handle:
        fsm = textfsm.TextFSM(handle)
        records = fsm.ParseText(data.strip())

    # Ensure that the number of column headers equals the number
    # of fields in each record, or else tabular format is ruined
    assert all(len(fsm.header) == len(record) for record in records)
    return (fsm, records)


def main():
    """
    Execution starts here.
    """

    # Create the outputs/ directory if it doesn't exist
    out_dir = "gns3/textfsm/outputs"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

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
        new_records = []
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

            # Basic reference so generic write operation can succeed
            new_records = records

        except Exception as exc:
            # Don't have a template, try a custom one
            if "No template found" in str(exc):
                fsm, records = parse_custom(input_file[:dot_index], data)

                # Convert integer values in the matrix, ignore failures
                for record in records:
                    for i in range(len(record)):
                        try:
                            record[i] = int(record[i])
                        except ValueError:
                            pass

                    # Add a new dict to the list with the headers (keys) and values
                    new_records.append(dict(zip(fsm.header, record)))

            # Some other error occurred; re-raise
            else:
                raise

        finally:
            # Whether NTC or custom template, new_records should be a
            # list of dictionaries with at least one element
            assert isinstance(new_records, list)
            assert len(new_records) > 0
            assert all(isinstance(d, dict) for d in new_records)

        # Print the output using a variety of outputs
        for output_function in [to_csv_file, to_json_file]:
            output_function(out_dir, input_file[:dot_index], new_records)


if __name__ == "__main__":
    main()
