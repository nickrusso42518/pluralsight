#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using Nornir to introduce orchestration and
concurrency, as well as inventory management.
"""

import json
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.files import write_file
from nornir.plugins.functions.text import print_result


def write_facts(task):
    """
    This is a grouped task that runs once per host. This
    iteration happens inside nornir automatically. Anytime
    'task.run()' is invoked, a new result is automatically added to
    the MultiResult assembled on a per-host basis. If the grouped
    task returns anything, that object is stored in MultiResult[0]
    and all subsequent results are stored thereafter.
    """

    # TASK 1: Gather facts using NAPALM to get model ID
    task1_result = task.run(task=napalm_get, getters=["get_facts"])

    # TASK 2: Write this data to a JSON file for use later.
    # We don't care about the result in this function, but Nornir stores
    # it for us anyway behind the scenes
    task.run(
        task=write_file,
        content=json.dumps(task1_result[0].result["get_facts"], indent=2),
        filename=f"{task.host.name}_facts.json",
    )


def main():
    """
    Execution begins here.
    """

    # Initialize nornir and invoke the grouped task.
    nornir = InitNornir()
    result = nornir.run(task=write_facts)

    # Use Nornir-supplied function to pretty-print the result
    # to see a recap of all actions taken.
    print_result(result)


if __name__ == "__main__":
    main()
