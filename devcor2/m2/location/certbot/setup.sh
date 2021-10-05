#!/bin/bash
# Full certbot instruments for Ubuntu (bionic) found here:
# https://certbot.eff.org/lets-encrypt/ubuntubionic-apache

# Perform updates and package installations per certbox instructions
apt-get update -y
apt-get install software-properties-common -y
add-apt-repository universe -y
add-apt-repository ppa:certbot/certbot -y
apt-get update -y
apt-get install certbot python-certbot-apache -y

# Make sure certbot was installed
certbot --version

# Run certbot non-interatively to achieve SSL certs
certbot --apache --non-interactive --agree-tos \
  -m your@email.com \
  -d your.domain.com

# Print summary of certificates that we just created
certbot certificates

# Update permissions so Python/Flask (anyone) can access cert and key
chmod o+rx /etc/letsencrypt/live
chmod o+rx /etc/letsencrypt/archive
chmod -R o+r /etc/letsencrypt/archive
