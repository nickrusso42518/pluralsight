#!/bin/bash
# Script to use curl in a bash loop to check if the app is up. Without
# this script, the system tests would run immediately after the containers
# are started, which doesn't work with our new (slow) database. Pass in one
# CLI argument to represent the number of seconds to wait.

echo -n "Waiting for HTTPS/5000 on app "
i=0

# So long as curl to HTTPS/5000 keeps failing and we haven't tried X times
while ! curl --output /dev/null --silent --head --fail --insecure \
  https://localhost:5000 && [ $i -lt $1 ]; do
    # Wait 1 second, print a period (no newline) to measure progress
    sleep 1
    echo -n "."
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
