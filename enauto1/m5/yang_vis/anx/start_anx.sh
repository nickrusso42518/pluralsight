#!/bin/bash
# Bash script to clone the ANX repo and start the container

# Clone the anx repo and change into the directory
git clone https://github.com/cisco-ie/anx
cd anx

# Use the supplied docker-compose file to start the container
docker-compose up --detach

# Make sure the container starts
docker container ls
