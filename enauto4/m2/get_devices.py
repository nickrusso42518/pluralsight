#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Consume the custom CiscoSDWAN mini-SDK and
and test its Inventory API methods.
"""

from cisco_sdwan import CiscoSDWAN


def main():
    """
    Execution begins here.
    """

    # Create SD-WAN object to DevNet sandbox host
    sdwan = CiscoSDWAN.get_instance_reserved()

    # Create list of functions (not calling them)
    api_calls = [
        sdwan.get_all_devices,
        sdwan.get_device_vedges,
        sdwan.get_device_controllers,
    ]

    # Run the device inventory API calls
    CiscoSDWAN.run_api_calls(api_calls)


if __name__ == "__main__":
    main()
