#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using Nornir to introduce orchestration and
concurrency, as well as inventory management.
"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result


def main():
    """
    Execution begins here.
    """

    # Initialize nornir and invoke the grouped task.
    nornir = InitNornir()

    # Use NAPALM logic to invoke the "get_facts" getter
    # Below is the documentation page used in the demo:
    # https://nornir.readthedocs.io/en/stable/plugins/tasks/networking.html
    result = nornir.run(task=napalm_get, getters=["get_facts"])

    # Use Nornir-supplied function to pretty-print the result
    # to see a recap of all actions taken.
    print_result(result)


if __name__ == "__main__":
    main()
