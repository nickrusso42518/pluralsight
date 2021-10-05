#!/bin/bash
# Initial setup on a fresh CentOS 7 box, not relevant to TIG tasks
sudo yum update yum -y
sudo yum update -y
sudo yum install git tree vim -y
sudo hostname tig
echo "color desert" > ~/.vimrc
echo "set number" >> ~/.vimrc
echo 'alias ls="ls --color=none"' >> ~/.bashrc
source ~/.bashrc
