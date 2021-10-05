# Integrating Ansible Playbooks into Network Operations
This directory contains a simple Ansible project to manage the WAN
devices using SSH, instead of Netmiko.

Playbooks:
  * `get_facts.yml`: Collects information from each device and writes the
    output to a host-specific file using `templates/ios_data.j2`.
  * `template_wan.yml`: Updates the device configuration based on the
    `idempotent.j2` or `not_idempotent.j2` templates in the `templates/`
    directory.

Auxiliary files:
  * `ansible.cfg`: Directory-specific Ansible config file
  * `group_vars`: Contains group variables for the `all`, `hubs`, and `spokes`
    groups, which can be consumed at the play or task level in the playbooks.
  * `hosts.yml`: The YAML-formatted Ansible inventory, identifying all hosts
    managed by Ansible and their group assignments.

**Note**: Check the `data_ref/` directory for example JSON structures,
rendered templates and more.
