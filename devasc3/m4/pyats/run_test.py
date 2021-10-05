#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Simple demonstration of Cisco pyATS and Genie frameworks
for reference.
"""

import json
from pyats import aetest
from genie.conf import Genie


class NetworkTestcase(aetest.Testcase):
    """
    Object-oriented programming (OOP) design used to inherit (subclass)
    from the main pyATS Testcase class, allowing us to define our own
    custom tests.
    """

    @aetest.setup
    def setup(self):
        """
        Runs before the tests begin.
        Connect to all devices in the tested at once.
        """

        self.parameters["testbed"].connect()

    @aetest.test
    def test_ospf_neighbors(self):
        """
        Test case asserts that all OSPF neighbors are up. Issues the
        'show ip ospf neighbor' command and parses the output into structured
        data for easy access/assertions. We could write more detailed test
        cases which validate individual neighbor parameters, but this example
        is designed to be minimal.
        """

        # Loop over each device and check OSPF neighbors
        for name, device in self.parameters["testbed"].devices.items():
            ospf_nbrs = device.parse("show ip ospf neighbor")
            ospf_nbrs_str = json.dumps(ospf_nbrs, indent=2)
            print(f"{name} OSPF neighbors:\n{ospf_nbrs_str}")

            # In a full-mesh triangle, each router should have 2 neighbors
            assert len(ospf_nbrs["interfaces"]) == 2


if __name__ == "__main__":
    # Genie is a superset of pyATS, so we can use Genie to initialize the
    # testbed. This gives us access to Genie parsers.
    testbed = Genie.init("testbed.yml")

    # We can run the pyATS test suite by passing in our testbed object.
    aetest.main(testbed=testbed)
