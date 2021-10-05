# RESTCONF on IOS-XE
This repository provides an example of using RESTCONF via
Nornir (Python `requests` behind the scenes) to update
VRF configurations on IOS-XE. IOS-XR supports RESTCONF but requires
a special package and, in my experience, is not commonly used
today compared to NETCONF.

The `hosts.yaml` file identifies the two routers in scope (both
are IOS-XE here) along with their VRF definitions. The `groups.yaml`
specifies common IOS-XE connection parameters. These are automatically
imported by Nornir upon initialization.

The Python code uses standard Nornir task execution, relying on the
`http_method` built-in method. Experienced Python developers could
bypass this wrapper and use `requests` directly as well. The tasks are:
  * Retrieve configuration via HTTP GET
  * Update configuration via HTTP PUT
  * Save configuration via HTTP POST
