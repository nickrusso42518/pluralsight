#!/bin/bash
# Small script to avoid typing these long commands

pyang_path="yang/vendor/cisco/xe/1741"

echo "Producing flow containers to augment native"
pyang --format tree --path $pyang_path \
  --output data_ref/xe_flow_tree.txt \
  $pyang_path/Cisco-IOS-XE-flow.yang

echo "Producing interface containers from native"
pyang --format tree --path $pyang_path \
  --output data_ref/xe_native_subtree.txt \
  --tree-path /native/interface/GigabitEthernet \
  $pyang_path/Cisco-IOS-XE-native.yang
