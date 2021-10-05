#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Develop product model ID parsers for IOS-XE and IOS-XR.
These are focused on just the model ID and not general information.
"""

import re


def parse_model_ios(text):
    """
    Parses the model ID from the IOS "show version" command.
    If not match is found, None is returned. Sample:
    cisco CSR1000V (VXE) processor (revision VXE) with 31K/32K memory.
    """
    model_regex = re.compile(r"cisco\s+(?P<model>\S+)\s+\(\S+\)\s+processor\s+")

    # Attempt to match the regex against the specific input.
    model_match = model_regex.search(text)
    if model_match:
        return model_match.group("model")

    # No match was found
    return None


def parse_model_iosxr(text):
    """
    Parses the model ID from the IOS-XR "show diag 0/0" command.
    If not match is found, None is returned. Sample:
    PID                  : R-IOSXRV9000-RP-C
    """
    model_regex = re.compile(r"\s+PID\s+:[ \t]+(?P<model>\S+)")

    # Attempt to match the regex against the specific input.
    model_match = model_regex.search(text)
    if model_match:
        return model_match.group("model")

    # No match was found
    return None
