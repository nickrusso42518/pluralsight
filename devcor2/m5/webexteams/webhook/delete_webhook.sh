#!/bin/bash
# Simple bash script to remove an existing webhook by ID
# Ensure WT_API_TOKEN is defined and the first CLI argument
# is the webhook ID to be deleted.

echo "Deleting webhook with ID"
echo "$1"
curl -X DELETE \
  -H "Authorization: Bearer $WT_API_TOKEN" \
  https://api.ciscospark.com/v1/webhooks/"$1"
