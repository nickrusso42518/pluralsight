#/bin/bash
# Small script to avoid typing these long commands

# Build tree for Cisco-modeled VLAN-specific components
pyang --format tree --path ../../yang_big --lax-quote-checks \
  --output data_ref/xe16121_vlan.txt \
  ../../yang_big/vendor/cisco/xe/16121/Cisco-IOS-XE-vlan.yang
