#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: The pytest functions for ensuring platform model ID parsers
for IOS-XE and IOS-XR are functional. Run with "-s" to see outputs.
"""

from parse_model_m4 import parse_model_ios, parse_model_iosxr


def test_parse_model_ios():
    """
    Defines unit tests for the Cisco IOS XE model string.
    """

    # Positive test case; provide valid output that should parse correctly
    model_output = """
        cisco CSR1000V (VXE) processor (revision VXE) with 31K/32K memory.
        Processor board ID 9TH4AXITD7I
        1 Gigabit Ethernet interface
        32768K bytes of non-volatile configuration memory.
    """
    print(model_output)

    # Perform parsing, print structured data, and validate
    model_data = parse_model_ios(model_output)
    print(model_data)
    assert model_data == "CSR1000V"

    # Negative test case; provide invalid output that should not parse
    model_output = """
        cisco (VXE) processor (revision VXE) with 31K/32K memory.
        Processor board ID 9TH4AXITD7I
        1 Gigabit Ethernet interface
        32768K bytes of non-volatile configuration memory.
    """
    print(model_output)

    # Perform parsing, print structured data, and validate
    model_data = parse_model_ios(model_output)
    print(model_data)
    assert model_data is None


def test_parse_model_iosxr():
    """
    Defines unit tests for the Cisco IOS XR model string.
    """

    # Create and display some test data
    model_output_list = [
        """
        0/RP0-Fake-IDPROM - Cisco XRv9K Centralized ...
         Info:
            PID                      : R-IOSXRV9000-RP-C
            Version Identifier       : V01
            UDI Description          : Cisco XRv9K Centralized ...
            CLEI Code                : N/A
        """,
        """
        0/RP0-Fake-IDPROM - Cisco XRv9K Centralized ...
         Info:
            PID                      :
            Version Identifier       : V01
            UDI Description          : Cisco XRv9K Centralized ...
            CLEI Code                : N/A
        """,
    ]
    model_answer_list = ["R-IOSXRV9000-RP-C", None]
    for model_output, model_answer in zip(model_output_list, model_answer_list):
        print(model_output)

        # Perform parsing, print structured data, and validate
        model_data = parse_model_iosxr(model_output)
        print(model_data)
        assert model_data == model_answer
