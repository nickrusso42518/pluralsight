# Utilizing Netmiko to Automate Cisco Enterprise Devices
This repository contains several Netmiko examples for Cisco IOS-XE. Scripts:

  * `get_wan_health.py`: Collects information from all devices in the network,
    which may differ between hubs and spokes.
  * `update_wan.py`: Pushes a static snippet to all devices to
    update the WAN configuration.
  * `template_wan.py`: Uses jinja2 templates instead of a static snippet to
    update the WAN configuration on all devices.

Other components:
  * `vars/`: Contains variables for individual routers as well as all devices.
  * `hosts.yml`: Contains a simple list of dictionaries to enumerate all hosts
    being managed by Netmiko

**Note:** Check the `data_ref/` directory for example snippets, outputs, etc.
