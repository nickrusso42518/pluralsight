# Module 5 - Managing Distributed Cisco FTD Instances Using Cisco FMC
This directory contains code for module 5
which focuses on Cisco FMC automation using Python and `requests`.
The `data_ref/` directory contains sample output files for reference.
This project was tested and demonstrated using these versions:
  * FTD: 6.3
  * Python: 3.7.3
  * requests: 2.23.0

You can optionally export the following environment variables
if you want to use the `build_from_env_vars()` method:
  * `FMC_USERNAME`: Your personal username for FMC
  * `FMC_PASSWORD`: Your personal password for FMC
  * `FMC_HOST`: FMC IP/hostname (defaults to `fmcrestapisandbox.cisco.com`)

Edit, copy, and paste the commands below to speed things up:
```
export FMC_USERNAME=njrusmc
export FMC_PASSWORD=2NgD3Kwz
export FMC_HOST=<your FMC IP/hostname>
```
