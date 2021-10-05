# Getting Started with Device Provisioning Techniques
This directory contains a sample zero touch provisioning ZTP project using
Cisco IOS-XE on CSR1000v routers. If you want to use it, be sure to
make the following changes.

1. Use `hub_base.txt` to derive your DHCP, TFTP, and DNS configurations.
   Make changes specified to your environment.
2. Change the `ipaddr_map` in `ztp.py` based on the serial numbers of the
   devices you want to provision. The two-tuple value includes the
   desired Loopback0 and Tunnel100 IP addresses, respectively.
3. Review the configuration lines to update the DMVPN NBMA address and
   other minor settings specific to your environment.

**Note:** You can use `tclsh` to enter the TCL shell, then
`puts [open "bootflash:ztp.py" w+] {` followed by
pasting the `ztp.py` script into the hub router's shell. Then use `}`
to close the operation followed by `tclquit`.
