#!/bin/bash
# Simple script to create SSL certificate and private key non-interactively.
# The key.pem and cert.pem outputs are stored in the ssl/ directory.

mkdir -p ssl
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
    -subj "/C=US/ST=Maryland/L=Baltimore/O=Globomantics/CN=crm.njrusmc.net" \
    -keyout ssl/key.pem  -out ssl/cert.pem
