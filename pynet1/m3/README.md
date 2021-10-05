# SSH-based Infrastructure as Code
Netmiko was written by Kirk Byers and was designed to capture
the idiosyncracies of SSH-based network management. Similar to
paramiko, it interacts with devices on a basic level, sending
commands and reading output. It helps clean up output and abstracts
the low-level commands like `recv` out of the process.

> Netmiko official docs: https://netmiko.readthedocs.io/en/stable/

Netmiko has very wide support for network devices and should be used
before paramiko when trying to communicate with a device for the first
time. I recommend using paramiko as a fall back.
