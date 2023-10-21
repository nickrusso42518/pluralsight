#!/bin/bash
# Script to use curl in a bash loop to check if the RESTCONF is up. Without
# this script, the XE resources would run immediately after the instances
# are started, which doesn't work with a newly-deployed router. The first
# CLI argument represents the number of seconds to wait, and the second is
# the FQDN (IP or URL) of the managed XE node. The third and fourth are the
# HTTP basic auth username and password, respectively. Example:
# $ ./wait_for_rc.sh 30 54.242.210.158 ec2-user password123!
# Waiting for RESTCONF on 54.242.210.158 OK!

echo -n "Waiting for RESTCONF on $2"
i=0

# So long as curl to HTTPS/5000 keeps failing and we haven't tried X times
while ! curl --output /dev/null --silent --head --fail --insecure --user $3:$4\
  https://$2/restconf/ && [ $i -lt $1 ]; do
    # Wait 10 seconds then rerun the loop
    sleep 10
    i=$((i + 1))
done

# If we counted all the way to X, we failed, use non-zero rc
# Else, we didn't count to X, which means the loop exited early (success)
if [ $i -eq $1 ]; then
    echo "FAILED!"
    exit 1
else
    echo "OK!"
fi
