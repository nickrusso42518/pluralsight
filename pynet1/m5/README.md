# Using NAPALM to simplify parsing and updating
NAPALM was written by David Barroso and is used as an
abstraction tool to simply device management. Unlike Netmiko,
NAPALM comes with pre-made "getters" which can collect basic
data from devices and return their data in JSON format. This
allows us to eliminate one of our custom parsers from the
previous module.

> NAPALM official docs: https://napalm.readthedocs.io/en/stable/

NAPALM can also replace configurations and merge in config changes.
When combined with our set theory logic, this approach is useful
for updating configurations and providing a "diff".

This project also introduces the concept of "set theory" used to
determine what configuration to add and what to remove. When not
replacing configurations wholesale, this method is important to
achieve idempotent operations.
