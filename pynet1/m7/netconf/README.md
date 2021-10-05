# NETCONF on IOS-XE and IOS-XR
This repository provides an example of using NETCONF via
Python's `ncclient` to update VRF configurations.

The `hosts.yml` file identifies the platform and host-specific parameters,
which differ widely between the two operating systems. The YAML files in
`vars/` contains the VRF definitions on each individual host. This usage
of YAML files is a quick-and-dirty remake of Ansible/Nornir inventory
management for the purpose of keeping the Python code simpler.

The Python code performs two main actions:
  * Collecting and pretty-printing the running configurations as XML
  * Updating VRF configurations based on host-specific variable files
