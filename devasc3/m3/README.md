# Module 3 - Deploying Common Network Services
This module contains the packet captures (`.pcapng`) files used in the
course. Feel free to browse or dig deeper to better understand these
IP services. You can download Wireshark at `https://www.wireshark.org`
which is freeware.

## Lab topology
Please reference the Module 2 course files to access the network topology.
Although the course did not feature a live demonstration of these IP services,
all of them are configured in the demo topology. The demo was omitted because
this is too technically deep for a beginner-level software-oriented course.

### DHCP
The DHCP server is running on R1 and serves VLAN 10, which has H1 and H2 on
it. These hosts get their IP configuration, DNS servers, and domain name
from the IOS-hosted DHCP server.

### DNS
The INTERNET router is a DNS server while H1 and H2 are DNS clients. The DNS
server has an IPv4 "A" record for L1.globomantics.com, which is the
internal load balancer.

Both H1 and H2 have an alias named `lbtest`. If you type `lbtest`, it will
perform an HTTP GET to L1.globomantics.com This will download the
configuration of a specific web server. There are 3 web servers behind the
load balancer, and using a "destination" NAT technique, the load balancer
forwards these requests to each web server in a round-robin fashion.

### NAT
F1 is both a firewall and a NAT device. It uses NAT overloading to translate all
internal 10.0.0.0/8 addressing to the outside IP address of 203.0.113.3. You can
also explore the firewall rules on F1 which inspects TCP, UDP, and
ICMP (for ping traffic).

### SNMP
The SNMP management station is an external virtual machine as this cannot be
simulated on Cisco IOS. The network devices are SNMP servers and will respond
to SNMP polls. I used CentOS 7 and tied it into my simulator.

I installed the required SNMP packages using this command:
`$ sudo yum install net-snmp net-snmp-utils`

Using the `snmpwalk` command, you can query devices for bits of information.
SNMP is not terribly intuitive, but you can view specific values this way.
Below are some examples that I used to generate SNMP poll traffic.

```
$ snmpwalk -v3 -l noauth -u SNMPUSER 10.1.30.1 sysName.0
$ snmpwalk -v3 -l noauth -u SNMPUSER 10.1.30.1 sysContact.0
```

### NTP
The INTERNET router is also an NTP server. For simplicity, all network devices
in the Globomantics network pull time from it. An alternative design could
reconfigure the switches to pull time from their local routers as well.