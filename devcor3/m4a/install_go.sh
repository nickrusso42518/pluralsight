#!/bin/bash

apt-get update
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
tar -xvf go1.21.0.linux-amd64.tar.gz
mv go /usr/local
