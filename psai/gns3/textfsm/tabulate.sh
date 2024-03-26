#!/bin/bash
# Quickly print the CSV files in tabular form

for file in gns3/textfsm/outputs/*.csv
do
  echo ""
  echo $file
  column -s, -t $file | head -n 3
done
