# Provisioning and Managing Networks using Common Automation Tools
2 hours, covers network automation fundamentals, builds on DEVASC

## m2: Getting Started with Device Provisioning Techniques
1. Course Prerequisites and Business Scenario
2. Utilizing iPXE for Network Device Booting
3. Utilizing ZTP for Initial Device Configuration
4. Scaling and Centralizing Day 0 Operations with Cisco PnP
5. iPXE, ZTP, or PnP; Which is Right for Our Scenario?
6. Demo: Writing the ZTP Python Script
7. Demo: Implementing the ZTP Required Services in Cisco IOS-XE
8. Demo: Standing up new Branch Sites with ZTP
9. Module Summary and Homework Challenge
  - if you have hardware, try iPXE

## m3: Utilizing Netmiko to Automate Cisco Enterprise Devices (25m)
1. Understanding the Fundamental Network Automation Concepts
2. Demo: Collecting the Initial WAN Health with Netmiko
3. Demo: Configuring Routing Enhancements via Static Files
4. Assembling Flexible Configuration Templates with Jinja2
5. Demo: Configuring Routing Enhancements via Jinja2 Templates
6. Module Summary and Homework Challenge
  - try using netmiko on other enterprise devices, like ASA and NX-OS

## m4: Integrating Ansible Playbooks into Network Operations (15m)
1. Introducing Ansible for Network Automation
2. Demo: Ansible Installation and Auxiliary File Creation
3. Demo: Collecting Device State with Ansible
4. Demo: Configuring and Verifying Routing Enhancements with Ansible
5. Module Summary and Homework Challenge
  - combine ansible and netconf

## m5: Migrating from CLI-driven to Model-driven Programmability (20m)
1. Network-driven Programmability and YANG Refresher
2. Demo: Exploring YANG models with Cisco DevNet's yangexplorer
3. Demo: Exploring YANG models with Advanced NETCONF Explorer (anx)
4. Planning Your Migration and Avoiding Common Mistakes
5. Demo: Migrating the Network to NETCONF Management using Python ncclient
6. Module Summary and Homework Challenge
  - add the baseline ZTP config to NETCONF to make config more declarative

## m6: Monitoring Networks using Model-driven Telemetry (MDT) (30m)
1. Introducing the Telegraf, Influxdb, and Grafana (TIG) Stack
2. Demo: Building and Deploying the TIG Stack
3. Demo: Exploring Operational State YANG Models
4. Demo: Configuring gRPC Dial-out Connections On Cisco IOS-XE
5. Demo: Creating New Dashboard Visualizations in Grafana
6. Course Summary and Homework Challenge
  - add a new subscription and visualization for OSPF data
