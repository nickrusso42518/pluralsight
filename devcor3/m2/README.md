# Module 2 - Utilizing RESTCONF to Manage Device Configuration
This directory contains several Python scripts to collect,
add, and delete IETF-modeled static routes from the Cisco IOS-XE
"latest code" always-on sandbox.

## Python scripts
There are 3 main scripts:

  * `get_routes.py`: Collects the IETF static routes from the device
    and writes the output to stdout in a human-readable format.
  * `add_routes.py`: Adds the interfaces in the `config_state.yml`
    file. This is a bulk operation.
  * `delete_routes.py`: Iteratively deletes all interfaces in
    the `config_state.yml` file one by one.

## Auxiliary files
There are several other files that play a role in this demo:

  * `config_state.yml`: Contains the YANG-modeled data encoded as YAML
    of the routes that should be added or deleted, depending on which
    script is executed.
  * `make_trees.sh`: Not directly related to Python, this is a Bash script
    that uses `pyang` to build text tree representations of the IETF
    routing and IPv4 unicast routing YANG models, which are needed for
    this demo.

## Reference files
The `data_ref/` directory contains several files that are useful to
reference for learning:

  * `ietf_routing.txt`: The `pyang` tree representation of the IETF routing
     YANG model.
  * `ietf_v4ur.txt`: The `pyang` tree representation of the IETF IPv4
     unicast routing YANG model.
  * `get_rtes_resp.json`: Output from the "get" script for the
     router targeted by the script (currently IOS-XE "latest").
  * `add_rtes_duplicate.json`: Output from the "add" script
     when an addition fails due to an object already existing.
