# Getting Started with Cisco SD-WAN Programmability
This directory contains the files needed to build the SD-WAN mini-SDK
and test it with a simple inventory API call.

Relevant files:
  * `cisco_sdwan.py`: This SDK will grow over time, but it starts here.
  * `get_devices.py`: Collects the output from several device-related API
    calls and stores the output in `data_ref/`.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
