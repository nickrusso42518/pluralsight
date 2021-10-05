# Troubleshooting Network Problems in DNA Center
This directory contains the files needed to run DNA center
command runner and path trace operations.

Relevant files:
  * `run_commands.py`: Runs a set of commands on the Catalyst 9300 switches
     in inventory, then saves their outputs to individual files in `outputs/`.
  * `run_pathtrace.py`: Runs a sample path trace between two leaf switches in
    the DevNet sandbox leaf/spine architecture. You can replace the IP addresses
    and other details to suit your environment.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
