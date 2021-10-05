#!/bin/bash

# Copy/pasting the steps from docker's installation instructions
# for CentOS 7. Documentation reference below.
# https://docs.docker.com/install/linux/docker-ce/centos/
yum remove -y docker \
  docker-client \
  docker-client-latest \
  docker-common \
  docker-latest \
  docker-latest-logrotate \
  docker-logrotate \
  docker-engine

yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2

yum-config-manager \
  --add-repo \
  https://download.docker.com/linux/centos/docker-ce.repo

yum install -y docker-ce \
  docker-ce-cli \
  containerd.io

systemctl enable docker.service
systemctl start docker
docker --version
echo "Use 'sudo docker container run hello-world' to verify"
