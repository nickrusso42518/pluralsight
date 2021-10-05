# Building and Applying vSmart Device Templates
This directory contains the files needed to create a new vSmart routing
policy. This is used to control traffic flow and is the main capability
of any SD-WAN solution.

Relevant files:
  * `build_vsmart_policy.py`: Creates a new vSmart routing policy using
    custom parameters to ensure voice traffic prefers MPLS over Internet
    (when compliant with SLA performance). The policy is then applied
    to all vSmarts.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
