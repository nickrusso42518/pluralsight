# Managing IOS-XE Interfaces with Ansible + RESTCONF
This directory contains several Ansible playbooks to collect,
add, and delete IETF-modeled interfaces from Cisco IOS-XE
routers running in the DevNet always-on sandboxes.

## Playbooks
There are 3 main playbooks:

  * `get_intfs.yml`: Collects the IETF interfaces from each device
    in the `restconf_routers` group and writes the output as JSON
    into a file named `data_ref/<hostname>_restconf_intfs.json`.
    This uses HTTP GET behind the scenes.
  * `add_intfs.yml`: Adds the interfaces in the `new_interfaces`
    variable to the routers using HTTP POST behind the scenes.
    This is a bulk operation.
  * `delete_intfs.yml`: Iteratively deletes all interfaces in
    the `new_interfaces` variable one by one. This uses an
    Ansible `loop` and uses HTTP DELETE behind the scenes.

## Auxiliary files
There are several other files that play a role in this demo:

  * `ansible.cfg`: The Ansible configuration file which sets basic
    parameters for the runtime environment.
  * `hosts.yml`: The Ansible inventory file containing the devices being
    managed by Ansible.
  * `group_vars/restconf_routers.yml`: A group-specific variables file
    for the `restconf_routers` group. It contains both connectivity
    and configuration parameters.
  * `make_trees.sh`: Not directly related to Ansible, this is a Bash script
    that uses `pyang` to build text tree representations of the IETF
    interfaces and IP YANG models, which are needed for this demo.

## Reference files
The `data_ref/` directory contains several files that are useful to
reference for learning:

  * `ietf_intf.txt`: The `pyang` tree representation of the IETF interfaces
     YANG model.
  * `ietf_ip.txt`: The `pyang` tree representation of the IETF IP
     YANG model.
  * `latest_restconf_intfs.json`: Output from the "get" script for the
     IOS-XE latest code sandbox router.
  * `stable_restconf_intfs.json`: Output from the "get" script for the
     IOS-XE stable code sandbox router.
  
## Issues
I opened this `resconf_config` module issue while building this demo:

`https://github.com/ansible/ansible/issues/61372`

This requires a small change to the source code as outlined in
the issue details. I expect this issue to be rapidly resolved, possibly
by the time you are reading this.

## Alternative approaches
The older `uri` module was originally designed to interact with
web servers and also works for RESTCONF as I demonstrate in my
"Automating Networks with Ansible the Right Way" course. The
`restconf_*` modules are newer and simpler, but may have issues.
Those familiar with `uri` may prefer to continue using it.
