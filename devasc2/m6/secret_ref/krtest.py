#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Illustrates the usage of keyring for storing
passwords using the OS key management system (varies by OS).
Be sure to "pip install keyring" first.
"""

import keyring

keyring.set_password("devopstest", "krtest", "d3v0p$")
secret = keyring.get_password("devopstest", "krtest")
print(type(secret), secret)
