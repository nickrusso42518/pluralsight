#!/bin/bash
# Small script to avoid typing these long commands

# Build tree for OC interfaces
pyang --format tree --path yang_oc \
  yang_oc/release/models/interfaces/openconfig-interfaces.yang \
  > data_ref/oc_intf.txt

# Build tree for OC Ethernet interface specifics
pyang --format tree --path yang_oc \
  yang_oc/release/models/interfaces/openconfig-if-ethernet.yang \
  > data_ref/oc_eth.txt

# Build tree for OC VLAN specifics
pyang --format tree --path yang_oc \
  yang_oc/release/models/vlan/openconfig-vlan.yang \
  > data_ref/oc_vlan.txt
