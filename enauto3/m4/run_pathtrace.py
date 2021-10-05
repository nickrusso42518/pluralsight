#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the path trace tool on
Cisco DNA center via API calls.
"""

from dnac_requester import DNACRequester


def main():
    """
    Execution begins here.
    """

    # Create a DNARequester object with our sandbox parameters
    dnac = DNACRequester(
        host="10.10.20.85", username="admin", password="Cisco1234!", verify=False
    )

    # Define the parameters of the path trace. This just traces from leaf1
    # to leaf2 in the DevNet reservable sandbox (these IPs may change)
    body = {
        "sourceIP": "10.10.20.81",
        "destIP": "10.10.20.82",
        "inclusions": ["INTERFACE-STATS", "DEVICE-STATS", "QOS-STATS"],
        "controlPath": False,
        "periodicRefresh": False,
    }

    # Issue the HTTP POST request to begin the path trace
    path = dnac.req(
        "dna/intent/api/v1/flow-analysis", method="post", jsonbody=body
    )

    # Optionally print out the JSON dump of the path response
    # print(json.dumps(path.json(), indent=2))

    # Path traces are async tasks; wait for the trace to complete
    path_data = path.json()["response"]
    task_resp = dnac.wait_for_task(path_data["taskId"])
    if task_resp.json()["response"]["progress"] != path_data["flowAnalysisId"]:
        raise ValueError("Unexpected error; task progress doesn't match flow id")

    # Collect the path trace results (aka, the flow analysis results) by ID
    flow_resp = dnac.req(
        f"dna/intent/api/v1/flow-analysis/{path_data['flowAnalysisId']}"
    )

    # Optionally print out the JSON dump of the flow analysis
    # print(json.dumps(flow_resp.json(), indent=2))

    # Print a human readable summary of the hops in the path between
    # the two IP addresses specified (see data_ref/ for screenshot from GUI)
    flow_data = flow_resp.json()["response"]
    print(
        f"Path trace {flow_data['request']['sourceIP']} -> "
        f"{flow_data['request']['destIP']}"
    )
    for i, hop in enumerate(flow_data["networkElementsInfo"]):
        print(f"Hop {i+1}: {hop['name']}")


if __name__ == "__main__":
    main()
