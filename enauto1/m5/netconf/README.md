# NETCONF-based Network Management with ncclient
This directory contains a handful of Python scripts:
  * `get_config.py`: Collects the current configuration of the elements
    relevant to the scenario using a subtree
    filter.
  * `edit_config.py`: Edits the configuration based on the `config_state.yml`
    which is similar to the Netmiko/Ansible variables.

The `hosts.yml` file contains an inventory identical to the one used in
Netmiko, which simplifies the migration.

**Note:** Check the `data_ref/` directory to see "before and after" versions
of the NETCONF configuration in the output JSON format and the raw XML format.
