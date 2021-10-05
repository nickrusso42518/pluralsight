# Initial CRM App from Previous Courses
This simple Flask app was the focus of the previous DEVASC-oriented courses.
It serves as a simple containerized app for IOS-XE app hosting.

## Container details
This directory contains the Docker data files used in the demos.
The `Dockerfile` describes the image itself, and `docker-compose.yml`
is a simple automation tool for building multiple docker containers.

## App hosting details
This section explains the details behind the app hosting demo.

The configuration snippet below was used in the demo. This creates a new
application with an ID of `crm`. It will process untagged (no VLAN) traffic
on it's first network interface and be assigned IP address `10.10.20.101/24`.
The `run-opts` string ensures the container is restarted if it fails and also
publishes TCP 5000 externally, which maps to the exposed container port.
The VLAN 4000 interface adds an additional IP to test layer-2 connectivity
from the container to the switch

```
interface Vlan4000
 ip address 10.10.20.99 255.255.255.0
 no shutdown
!
app-hosting appid crm
 app-vnic AppGigEthernet vlan-access
  vlan 4000 guest-interface 0
   guest-ipaddress 10.10.20.101 netmask 255.255.255.0
 app-default-gateway 10.10.20.254 guest-interface 0
 app-resource docker
  run-opts "--restart=unless-stopped -p 5000:5000/tcp"
```

These three commands, issued in sequence, will perform the necessary setup
steps. These should be issued *after* the `app-hosting`configuration is done.

```
app-hosting install appid crm package usbflash1:crm.tar
app-hosting activate appid crm
app-hosting start appid crm
```

These three commands, issued in sequence, will perform the necessary teardown
steps.

```
app-hosting stop appid crm
app-hosting deactivate appid crm
app-hosting uninstall appid crm
```

You can use `show app-hosting list` along the way to check progress in
between each command, if desired.
