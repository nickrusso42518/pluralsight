# Module 3 - Visualizing Network Threats with Cisco Stealthwatch
This directory contains code for the Cisco Stealthwatch Enterprise and
Cloud APIs. The documentation links are below:

```
https://developer.cisco.com/docs/stealthwatch/enterprise
https://developer.cisco.com/docs/stealthwatch/cloud
```

Export the following environment variables before using the `swc` scripts
to avoid any authentication problems with Stealthwatch Cloud.
```
export SWC_ACCOUNT=<your Stealthwatch Cloud URL identifier>
export SWC_EMAIL=<your Stealthwatch Cloud registered email>
export SWC_API_KEY=<your Stealthwatch Cloud hexadecimal API key>
```

__Note:__ When using the `send_netflow_v5.py` script, you may need to
provide the ability to create raw sockets for non-root users. Use
the `sudo setcap cap_net_raw=eip /usr/local/bin/python3.7` command,
specifying your specific Python binary, to accomplish this. Alternatively,
you could run the script as root, but that complicates the venv design.

The `data_ref/` directory contains example JSON responses from the
various API calls used in the course, as well as sample logs/artifacts.
