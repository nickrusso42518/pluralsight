# Module 5 - Modernizing Network Management using NETCONF
This directory contains NETCONF examples using Python's `ncclient`
library. The `config_state.yml` file represents the infrastructure
as code declarative state that can be used to determine how
the switchports in scope should be configured.

## Scripts
The `make_trees.sh` script leverages `pyang` to build tree representations
of the YANG models relevant for the module.

## Data References
The `data_ref/` directory contains the following reference data:
  * Raw XML RPC-reply payload from `get-config`
  * Parsed JSON RPC-reply payload from `get-config`
  * `pyang` text tree representation of the relevant
    OpenConfig models used in this module
