# Module 4 - Designing Application Deployments in Various Environments
This directory contains the Docker data files used in the demos.
The `Dockerfile` describes the image itself, and `docker-compose.yml`
is a simple automation tool for building multiple docker containers.
The CRM app from previous course is containerized as a single entity.
A more professional (read: advanced) strategy would be to break up
the model, view, and controller components into separate containers.

## Setup files
I used basic Bash scripts to expedite the installation of Docker as
such tasks are administrative in nature and not the focus of this course.
These files are contained in the `setup/` directory.
  * `centos7_docker_install.sh`: Installs Docker on CentOS 7. Run as `sudo`.
  * `docker_compose_install.sh`: Installs `docker-compose`. Run as `sudo`.

## Bash aliases for CentOS 7 installs

Although I did not use them in this course, these Bash aliases may
simplify using `docker` from the shell.

```
alias dc='sudo docker container'
alias di='sudo docker image'
alias db='sudo docker build'
alias comp='sudo docker-compose'
```
