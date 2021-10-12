#!/bin/bash
# Loop over each BGP RR client
for ip in 10.0.0.6 10.0.0.8; do
  echo ""
  echo "BGP prefix data for $ip"

  # cbgpPeerAddrFamilyName
  snmpget -v 3 -u V3_USER -l authPriv \
    -a SHA -A authpass123 -x AES -X privpass123 \
    10.0.0.5 iso.3.6.1.4.1.9.9.187.1.2.3.1.3.$ip.1.128

  # cbgpPeerAcceptedPrefixes
  snmpget -v 3 -u V3_USER -l authPriv \
    -a SHA -A authpass123 -x AES -X privpass123 \
    10.0.0.5 iso.3.6.1.4.1.9.9.187.1.2.4.1.1.$ip.1.128
done
