#!/bin/bash
# Small script to avoid typing these long commands

pyang_xe_path="yang/vendor/cisco/xe/1741"
pyang_xr_path="yang/vendor/cisco/xr/612"

echo "Producing XE snmp containers"
pyang --format tree --path $pyang_xe_path \
  --output data_ref/xe_snmp_tree.txt \
  $pyang_xe_path/Cisco-IOS-XE-snmp.yang

echo "Producing XR snmp containers"
pyang --format tree --path $pyang_xr_path \
  --output data_ref/xr_snmp_tree.txt \
  $pyang_xr_path/Cisco-IOS-XR-snmp-agent-cfg.yang
