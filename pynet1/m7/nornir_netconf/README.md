# NETCONF on IOS-XE and IOS-XR using Nornir
This directory is an update to the course that demonstrates the
newly-added NETCONF connection plugin on IOS-XE and IOS-XR. Behind
the scenes, it just wraps `ncclient`.

New files of interest:
  * `get_runbook.py`: Collects the VRF configurations from all devices
    and stores then as JSON files in the `outputs/` directory.
  * `edit_runbook.py`: Manages the network devices using IAC principles
    demonstrated in previous NETCONF examples, except with Nornir.
  * `nc_tasks.py`: Contains customer tasks that encapsulate common
    NETCONF RPCs. This makes Nornir feel more like Ansible for those
    who prefer it.
