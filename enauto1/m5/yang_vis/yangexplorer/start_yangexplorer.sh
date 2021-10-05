#!/bin/bash
# Installation script for the DevNet yangexplorer in Docker

# Pull the image from Dockerhub and run a new container
# The image is large (1.9GB) so be sure you have disk space
docker pull hellt/yangexplorer-docker
docker container run -p 8088:8088 -d hellt/yangexplorer-docker

# Make sure the container has started
docker container ls
