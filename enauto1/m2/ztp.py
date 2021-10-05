#!/usr/bin/python

"""
Author: Nick Russo
Purpose: Simple bootstrap ZTP script to enable remote access to
a device using SSH.
"""

import cli

# Use "show version" to extract the device serial number, which is
# guaranteed to be unique. Capture the last string from the line
# which is always the serial number. The output looks like this:
#   'Processor board ID 9BZ0FXAYK7X'
print "\n* Capture device serial number"
sn_text = cli.execute("show version | include ^Processor")
sn = sn_text.split(" ")[-1]

# Define serial to IP address 2-tuple matching, which provides the
# unique tunnel and loopback IPs for each device.
ipaddr_map = {
    "92Z8YAWE1YO": ("10.0.0.2", "172.16.100.2"),
    "9G7LDZKE6F4": ("10.0.0.3", "172.16.100.3")
}

# Check the dictionary for a serial number and unpack the addresses
lb0_ip, tun100_ip = ipaddr_map[sn]
print "\n* sn {0} -> lb0: {1}, tun100: {2}".format(sn, lb0_ip, tun100_ip)

# Define the config commands necessary for day 0 setup. In summary:
#  1. Configure a unique hostname
#  2. Configure SSH with crypto keys
#  3. Create a basic username and VTY access methods
#  4. Configure loopback
#  5. Configure DMVPN spoke tunnel with OSPF/CDP
config_cmds = [
    "hostname ZTP-{}".format(sn),
    "ip ssh version 2",
    "ip ssh logging events",
    "crypto key generate rsa modulus 2048",
    "username cisco privilege 15 secret cisco",
    "enable secret cisco",
    "netconf-yang",
    "cdp run",
    "line vty 0 4",
    "login local",
    "transport input ssh",
    "interface Loopback0",
    "ip address {} 255.255.255.255".format(lb0_ip),
    "ip ospf 1 area 0",
    "interface Tunnel100",
    "description DMVPN SPOKE TUNNEL",
    "ip address {} 255.255.255.0".format(tun100_ip),
    "cdp enable",
    "ip nhrp network-id 100",
    "ip nhrp nhs dynamic nbma connect.njrusmc.net multicast",
    "ip ospf network point-to-multipoint",
    "ip ospf 1 area 0",
    "tunnel source GigabitEthernet1",
    "tunnel mode gre multipoint"
]

print "\n* Performing ZTP configuration"
cli.configurep(config_cmds)

# Ensure each feature was configured successfully by running some
# "show" commands and displaying the output on the screen.
print "\n* Performing ZTP verification"
show_cmds = [
    "show ip ssh",
    "show ip interface brief",
    "show dhcp lease",
    "show ip ospf interface brief"
]

for show_cmd in show_cmds:
    print "\n* Running command '{}'".format(show_cmd)
    cli.executep(show_cmd)
