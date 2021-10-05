#!/bin/bash
# Shell script to simplify long Ansible command
echo "Set password using the env var below"
echo "export SSHPASS=<password>"
sshpass -e ansible-playbook get_vlans_v3.yml \
  --inventory netbox_inv.yml \
  --extra-vars '{"strict_mode": true}' \
  --user admin --ask-pass
