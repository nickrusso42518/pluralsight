#/bin/bash
# Small script to avoid typing these long commands

# Build tree for Cisco-modeled CPU operational stats
pyang --format tree --path ../yang_big \
  --output data_ref/xe16111_mem.txt \
  ../yang_big/vendor/cisco/xe/16111/Cisco-IOS-XE-memory-oper.yang

# Build tree for Cisco-modeled memory operational stats
pyang --format tree --path ../yang_big \
  --output data_ref/xe16111_cpu.txt \
  ../yang_big/vendor/cisco/xe/16111/Cisco-IOS-XE-process-cpu-oper.yang
