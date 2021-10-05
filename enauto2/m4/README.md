# Designing and Deploying Wireless Captive Portals
This directory contains the files needed to enable portals in Meraki,
as well as create your own custom portals.

The `setup/build_apache_excap.sh` script can be run on a fresh Ubuntu
machine to build a Meraki-styled stock example of an excap.

Relevant files:
  * `add_portals.json`: Hierarchical dictionary which maps SSIDs to new portals
    to add and configure. 
  * `build_portals.py`: This modifies the SSID and splash settings to enable
    captive portals, external or otherwise, on a per SSID basis.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
