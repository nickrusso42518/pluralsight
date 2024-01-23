#!/bin/bash
# Small script to deploy k8s manifest files and quickly
# get the status of those objects to ensure they were deployed

# Apply changes to k8s based on declarative YAML files.
# This results in new objects being created the first time.
echo "Applying changes:"
kubectl apply -f k8s/manifest

# Print pods that should be starting up
echo "Pods seen:"
kubectl get pods

# Print services
echo "Services seen:"
kubectl get svc
