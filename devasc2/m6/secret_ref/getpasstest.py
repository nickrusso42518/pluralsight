#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Illustrates the usage of getpass for interactive
password collection, then prints the password.
"""

import getpass

secret = getpass.getpass()
print(type(secret), secret)
