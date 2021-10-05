# Managing devices with APIs
This module has two subdirectories which contain the specific
code implementation for each API method:
  * `netconf/`: Network configuration protocol (RFC 6241 and RFC 6242)
  * `restconf/`: REST-based configuration protocol (RFC 8040) with Nornir
  * `nornir_netconf/`: New update combining NETCONF and Nornir

The following versions were used in this project.
  * `requests, version 2.21.0`
  * `ncclient, version 0.6.4`
  * `nornir, version 2.3.0`
  * `PyYAML, version 5.1`
