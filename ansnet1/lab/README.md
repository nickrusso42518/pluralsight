# Lab builder
Simple Ansible project to rapidly build the Globomantics network. The
entire process should take 5 to 10 minutes.

## Abstract
This auxiliary project is used to quickly configure the basic MPLS network
using the absolute minimally complex code. You may use this to help with
initial setup once your three routers have management IP addresses and
functional SSH access.

This playbook is *not* an example of well-designed infrastructure as code
because it is designed for lab setup only. Also note that the reason
my `configs/` are using GRE tunnels is because I recorded this course
using AWS routers. AWS does not allow IP multicast (OSPF/LDP hellos) or
non-IP traffic (MPLS-encapsulated packets) to traverse its network fabric.

Be sure you have Python 3.6 or newer along with pip installed.

## Pre-installation
Follow these steps to ensure your environment is properly configured
before building the lab. I'm using `Cisco IOS-XE 16.09.02` for this course.
There are many ways to set up the environment so I try to be descriptive
rather than prescriptive.

  1. Create (3) routers set up with management IP addresses.
     I suggest naming them `R1`, `R2`, and `R3` to match the course names.
     I used IP addresses `10.125.0.61`, `10.125.0.62`, and `10.125.0.63` for
     the three routers in sequence. If you change this, be sure to manually
     update the `configs/` files.
  2. Ensure you have DNS or `/etc/hosts` entries for these
     hostnames, allowing Ansible to connect. Alternatively, you could
     define the host variable `ansible_host: x.x.x.x` to assign an
     IP address, but I don't recommend this approach.
  3. Bootstrap the router with this snippet (copy/paste). You *only* need
     to do this step if SSH has not been configured and a username does
     not exist. If you can already access the routers, skip this step.
     On a new router, you'll likely have to use the console or telnet.
     ```
     configure terminal
     username ansible privilege 15 password ansible
     ip ssh version 2
     crypto key generate rsa modulus 2048
     line vty 0 4
      login local
      transport input ssh
     end
     write memory
     ```
  4. SSH into each router and store the SSH public keys in the
     `~/.ssh/known_hosts` file. You could use `ssh-keyscan` but
     I recommend logging to ensure your prompt is `#` as
     opposed to `>`. Once you can log into all routers as
     `ansible`, you may continue.

## Installation
Follow these steps to quickly build the lab environment for this course.
Note that some modules and excursion may deviate from this precise
setup. The course expects you to have basic networking and
Ansible skills to make adjustments as you see fit.

  1. The `requirements.txt` file contains the Python packages used
     in this course. Use `make setup` to quickly install them.
  2. Perform a quick syntax check and execute the lab builder by
     typing `make`. This also checks IP connectivity by sending ICMP
     echo-requests across the MPLS network to guarantee the correct
     VPN topologies were built.
  3. Optionally log into the routers to poke around. You can also
     run `make` again just to send pings without making router
     updates once the lab is built.
