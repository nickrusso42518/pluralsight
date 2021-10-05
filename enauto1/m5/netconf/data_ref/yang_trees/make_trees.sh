#!/bin/bash
# Small script to avoid typing these long commands

# Build the Cisco Native model tree
pyang --format tree --path yang/vendor/cisco/xe/16121 \
   yang/vendor/cisco/xe/16121/Cisco-IOS-XE-native.yang \
   --output native.txt

# Build the Cisco OSPF model tree
pyang --format tree --path yang/vendor/cisco/xe/16121 \
   yang/vendor/cisco/xe/16121/Cisco-IOS-XE-ospf.yang \
   --output ospf.txt

# Build the Cisco crypto model tree
pyang --format tree --path yang/vendor/cisco/xe/16121 \
   yang/vendor/cisco/xe/16121/Cisco-IOS-XE-crypto.yang \
   --output crypto.txt
