# FTP scripts
Informal collection of FTP operations.

## System info
```
$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 18.04.2 LTS
Release:        18.04
Codename:       bionic
```

## Packages used
Relevants packages on the server and client.

### Server
```
$ dpkg-query --show tftpd xinetd vsftpd tcpdump
tcpdump 4.9.2-3
tftpd   0.17-18ubuntu3
vsftpd  3.0.3-9build1
xinetd  1:2.3.15.3-1
```

### Client
```
$ dpkg-query --show lftp tftp-hpa nmap tcpdump
lftp     4.8.1-1ubuntu0.1
nmap     7.60-1ubuntu5
tcpdump  4.9.2-3
tftp-hpa 5.2+20150808-1ubuntu3
```
