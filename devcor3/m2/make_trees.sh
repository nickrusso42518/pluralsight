#/bin/bash
# Small script to avoid typing these long commands
# Clone this repo to access to latest YANG models:
# https://github.com/YangModels

# Build tree for Cisco XE 16.11.1 IETF routing base
pyang --format tree --path ../yang_big/vendor/cisco/xe/16111 \
  --output data_ref/ietf_routing.txt \
  ../yang_big/vendor/cisco/xe/16111/ietf-routing.yang

# Build tree for Cisco XE 16.11.1 IETF IPv4 unicast routing
pyang --format tree --path ../yang_big/vendor/cisco/xe/16111 --no-path-recurse \
  --output data_ref/ietf_v4ur.txt \
  ../yang_big/vendor/cisco/xe/16111/ietf-ipv4-unicast-routing.yang
