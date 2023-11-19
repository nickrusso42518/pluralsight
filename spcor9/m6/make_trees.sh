#!/bin/bash
# Small script to avoid typing these long commands

pyang_path="mdt/src/yang"

echo "Producing mdt container from NSO YANG"
pyang --format tree --path $pyang_path \
  --output data_ref/mdt_tree.txt \
  $pyang_path/mdt.yang
