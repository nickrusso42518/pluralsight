#/bin/bash
# Small script to avoid typing these long commands

# Build tree for IETF basic interfaces
pyang --format tree --path ../../yang_big \
  --output data_ref/ietf_intf.txt \
  ../../yang_big/standard/ietf/RFC/ietf-interfaces.yang

# Build tree for IETF interface IP-specific components
pyang --format tree --path ../../yang_big \
  --output data_ref/ietf_ip.txt \
  ../../yang_big/standard/ietf/RFC/ietf-ip.yang
