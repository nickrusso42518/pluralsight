#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Illustrates the usage of environment variables for passing
secrets into the program, then prints the variable's value. Be sure
to run "export SECRET=<password>" first.
"""

import os

secret = os.environ["SECRET"]
print(type(secret), secret)
