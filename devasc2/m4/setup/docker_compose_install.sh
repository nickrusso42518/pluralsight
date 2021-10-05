#!/bin/bash

# Guide: https://docs.docker.com/compose/install/
# Replace version "1.24.1" if you need something else
# On my system:
#  uname -s: Linux
#  uname -m: x86_64
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
mv /usr/local/bin/docker-compose /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose
docker-compose --version
