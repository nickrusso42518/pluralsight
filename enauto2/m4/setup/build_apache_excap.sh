#!/bin/bash
# On an Ubuntu machine, run this script as root to setup a simple excap

# Install Apache2 web service (basic web server) and git
apt install apache2 git -y

# Download the Meraki sample click-through excap code
git clone https://github.com/meraki/js-splash.git

# Move the excap sample code to the proper directory
mv js-splash/public/* /var/www/html/

# Restart Apache2 so the new files are processed
service apache2 restart
