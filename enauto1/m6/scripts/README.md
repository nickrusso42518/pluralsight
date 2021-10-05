# Managing Model-drien Telemetry (MDT) Subscriptions
This directory contains simple Python scripts to add/update
MDT subscriptions. All scripts rely on the `vars/mdt.yml` file
for their data. Some scripts use `jinja2` templates while others
use structured data techniques to build their payloads. All
templates are in the `templates/` directory.

All scripts take a variable number of CLI arguments representing
the hosts to configure with the generalized MDT subscriptions.

These scripts are included:

  * `cli_mdt.py`: Uses the `netmiko` package to configure MDT
    subscriptions using SSH/CLI.
  * `netconf_mdt.py`: Uses the `ncclient` package to configure MDT
    subscriptions using NETCONF `edit_config` RPC over SSH.
  * `restconf_mdt.py`:  Uses the `requests` package to configure MDT
    subscriptions using RESTCONF via HTTP PUT requests.

**Note:** Check the `data_ref/` directory for example body payloads.
