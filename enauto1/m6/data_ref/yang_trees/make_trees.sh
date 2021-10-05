#!/bin/bash
# Small script to avoid typing these long commands

# Build tree for Cisco-modeled CPU operational stats
pyang --format tree --path yang/vendor/cisco/xe/16121 \
  --output cpu_oper.txt \
  yang/vendor/cisco/xe/16121/Cisco-IOS-XE-process-cpu-oper.yang

# Build tree for Cisco-modeled memory operational stats
pyang --format tree --path yang/vendor/cisco/xe/16121 \
  --output mem_oper.txt \
  yang/vendor/cisco/xe/16121/Cisco-IOS-XE-memory-oper.yang

# Build tree for Cisco-modeled CDP operational stats
pyang --format tree --path yang/vendor/cisco/xe/16121 \
  --output cdp_oper.txt \
  yang/vendor/cisco/xe/16121/Cisco-IOS-XE-cdp-oper.yang

# Build tree for Cisco-modeled MDT configuration
pyang --format tree --path yang/vendor/cisco/xe/16121 \
  --output mdt_config.txt \
  yang/vendor/cisco/xe/16121/Cisco-IOS-XE-mdt-cfg.yang
