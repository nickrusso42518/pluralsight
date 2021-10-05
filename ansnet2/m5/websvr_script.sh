#!/bin/bash
# Image ID: ami-0fa59001d65100e7f (Apache on Centos 7.6)
# Local eth0 IP: 10.0.2.78 in server subnet
# Create route to Globomantics network via PAN FW server interface
ip route add 192.168.0.0/16 via 10.0.2.77 dev eth0
