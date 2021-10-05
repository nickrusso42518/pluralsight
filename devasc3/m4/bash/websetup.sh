#!/bin/bash

echo "TASK 1: Update hostname based on CLI argument"
hostname "$1"

echo "TASK 2: Install httpd"
yum install -y httpd

echo "TASK 3: Update HTML h1 header (CLI arg)"
sed -i "s:<h1>.*</h1>:<h1>$1</h1>:g" \
  /usr/share/httpd/noindex/index.html

echo "TASK 4: Start httpd"
systemctl start httpd

echo "TASK 5: Add webadmin user"
useradd -m -s /bin/bash webadmin
echo webpass | passwd webadmin --stdin

echo "Done!"
