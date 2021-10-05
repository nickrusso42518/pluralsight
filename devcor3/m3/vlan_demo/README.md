# Managing IOS-XE VLANs with Ansible + RESTCONF
This directory contains several Ansible playbooks to collect,
add, and delete Cisco-modeled interfaces from Cisco IOS-XE
switches running in the DevNet always-on sandboxes.

## Playbooks
There are 3 main playbooks:

  * `get_vlans.yml`: Collects the Cisco-modeled VLANs from each device
    in the `restconf_switches` group and writes the output as JSON
    into a file named `data_ref/<hostname>_restconf_vlans.json`.
    This uses HTTP GET behind the scenes, and if you are using
    the DevNet sandbox, there is only one Catalyst 9300 switch.
  * `add_vlans.yml`: Adds the VLANs in the `new_vlans`
    variable to the switches using HTTP POST behind the scenes.
    This is a bulk operation.
  * `delete_vlans.yml`: Iteratively deletes all VLANs in
    the `new_interfaces` variable one by one. This uses an
    Ansible `loop` and uses HTTP DELETE behind the scenes.

## Other information
These playbooks have an identical look and feel as the ones
described in the `intf_demo/` directory. Please check that
directory for details about the auxiliary files.
