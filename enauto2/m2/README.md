# Building and Updating Meraki Networks
This directory contains the scripts, input files, and reference outputs
for building/managing networks.

Relevant files:
  * `add_networks.json`: Contains a list of dictionaries with the networks to
    add to Meraki. In this example, includes a wireless and camera network.
  * `build_network.py`: Script that consumes `add_networks.json` to create
    and configure these networks in Meraki.

**Note:** Check the `data_ref/` directory for JSON outputs from API calls,
separated into `devnet` and `home` network directories.
