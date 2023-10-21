#!/bin/bash
# Follow instructions from here, except don't use "tee" as it writes binary
# data to the shell, ruining everything. Just redirect instead.
# https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

apt-get update
apt-get install -y gnupg software-properties-common curl wget

wget -O- https://apt.releases.hashicorp.com/gpg | \
  gpg --dearmor \
  > /usr/share/keyrings/hashicorp-archive-keyring.gpg

gpg --no-default-keyring \
  --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
  --fingerprint

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
  https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
  > /etc/apt/sources.list.d/hashicorp.list

apt update
apt-get install terraform -y
terraform -version
