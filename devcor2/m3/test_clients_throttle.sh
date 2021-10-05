#/bin/bash
# Tiny script that passes in known-good demo MACs for testing.
# Script should fail because throttling is enabled.

python get_client_detail_throttle.py \
  00:00:2A:01:00:01 \
  bogus_mac \
  00:00:2A:01:00:02 \
  00:00:2A:01:00:03 \
  00:00:2A:01:00:2A \
  00:00:2A:01:00:22 \
  00:00:2A:01:00:46 \
  00:00:2A:01:00:49
