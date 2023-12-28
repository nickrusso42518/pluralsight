#!/bin/bash
# Small script to quickly generate RFC-8340 YANG tree (plaintext) and
# XML skeleton example payloads for IOS-XR native static routing, CPU
# utilization, and memory consumption YANG models.

# If you run this script in the YDK container, use this path (not recommended)
# pyang_path="/root/ydk-gen/gen-api/python/xr_staticroute-bundle/ydk/models/xr_staticroute/_yang"

# Otherwise, clone the "yang" repository alongside this script, or use a symlink
pyang_path="./yang/vendor/cisco/xr/732"

# For each desired format/file extension pair
for fmt in "tree txt" "sample-xml-skeleton xml"
do
  # Unpack tuple into $1 (format) and $2 (file extension)
  set -- $fmt

  # Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/
  #   address-family/vrfipv{0}/vrf-unicast/vrf-prefixes
  echo "Producing static routing $1 file"
  pyang --format $1 --path $pyang_path \
    --output data_ref/static.$2 \
    $pyang_path/Cisco-IOS-XR-ip-static-cfg.yang

  # Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization
  echo "Producing CPU utilization $1 file"
  pyang --format $1 --path $pyang_path \
    --output data_ref/cpu.$2 \
    $pyang_path/Cisco-IOS-XR-wdsysmon-fd-oper.yang

  # Cisco-IOS-XR-nto-misc-oper:memory-summary/nodes/node/summary
  echo "Producing memory usage $1 file"
  pyang --format $1 --path $pyang_path \
    --output data_ref/memory.$2 \
    $pyang_path/Cisco-IOS-XR-nto-misc-oper.yang
done
