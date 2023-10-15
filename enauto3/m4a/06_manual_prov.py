#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Remind the user to manually provision devices to their site.
"""

steps = """
Manual steps:
  1. Log into DNAC via web GUI
  2. Navigate to menu option Provision > Inventory
  3. Navigate to site tree Maryland > secretlab
  4. Select all devices
  5. Navigate to Actions > Provision > Provision Device
  6. Don't make changes. Just click Next > Next > Deploy > Apply
"""
print(steps)
