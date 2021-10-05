# Module 6 - Deploying RESTCONF for Lightweight Network Management
This directory contains HTTP GET and HTTP POST RESTCONF examples to
collect and update DHCP pool configurations on Cisco IOS-XE, respectively.
This uses the popular Python `requests` library seen in previous courses.

## Scripts
The `make_trees.sh` script leverages `pyang` to build tree representations
of the YANG models relevant for the module.

## Demo prep
For this demo, the following DHCP pool is already configured on
the sandbox, which can be added using the `add_pools.py` script or
manually via CLI. See `data_ref/initial_state.yml` for details.

```
ip dhcp pool GLOBOMANTICS_VLAN10
 network 192.0.2.0 255.255.255.0
 default-router 192.0.2.254
 dns-server 8.8.8.8 8.8.4.4
 domain-name globomantics.com
```

## Data References
The `data_ref/` directory contains the following reference data:
  * Quick start initialization state file to add the first
    DHCP pool for the demo (copy into `config_state.yml`)
  * Parsed JSON HTTP response bodies from various requests
  * `pyang` text tree representation of the relevant
    Cisco "native" models used in this module
