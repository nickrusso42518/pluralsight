# Nornir for task orchestration
Nornir was created by David Barroso. It is a flexible and
powerful orchestration engine similar to Ansible in concept but
quite different in its operation. It supports a variety of connection
plugins and this repository explores using Netmiko and NAPALM.

> Nornir official docs: https://nornir.readthedocs.io/en/stable/

Nornir helps consolidate and sequence the tasks to execute but
leverages existing libraries to do so. The Nornir runbook
operates similarly to the NAPALM example in the previous module
by collecting facts from devices and applying necessary VRF changes
based on the current state of devices. Inventory management and overall
code complexity is much reduced, which is a big advantage of Nornir.

The `hosts.yaml` file identifies the hosts and their specific VRF data.
The `groups.yaml` file defines groups, often on a per-OS or per-role basis,
which group-specific parameters. Because Netmiko and NAPALM already know how
to talk to many devices, Nornir just relies on them for connectivity.
