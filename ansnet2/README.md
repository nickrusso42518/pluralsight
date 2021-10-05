# New Ansible course
Duration: 3 hours
Difficulty: Intermediate

# Module 1 - Intro

# Module 2 - Multi-vendor Automation and Security Techniques (35m)
6-8 minute business context + Ansible refresher/expectations.
Specifically mention narrow/deep vs. broad/shallow along with
some "weird" approaches to design, task/play inclusion, and var mgmt.
IOS/EOS/NXOS together in simulation using `cli_command` and `cli_config`
for VLAN management (refresher from previous course).
Introduce ansible-vault, show string-level encryption for secrets.
Discuss (no demo): firewalling, placement, TACACS/RBAC, etc.
Demonstrate ssh pubkey, use "--limit" to demonstrate vault and pubkey.

# Module 3 - Configuration Management and Validation with NAPALM (35m)
Collect VLANs (v1 and v2) and perform validation. Use
file-level encryption with static file. Explain Python filters and
review source code. Briefly review NX-API and EOS postman collections.
Include file-level encryption with basic VPF.

# Module 4 - Building and Referencing a Single Source of Truth (SSoT) with NetBox (40m)
Create NetBox representation of network (subset). Use NetBox as SoT for NAPALM
get VLANs (refactored). files contained in `netbox`. Use
string-level encryption for secrets. Mention and briefly explore postman collection.

# Module 5 - Creating a Hybrid Cloud via IPsec VPN to Palo Alto Firewall in AWS (40m)
Provide brief cloud overview usin AWS specifics. Review detailed diagram.
Explain initial setup with keypair and IAM user premade. Discuss `cloud` files.
Use file-level encryption for secrets + shell script. Includes teardown playbook.

# Module 6 - Simplifying Hybrid Cloud Connectivity using AWS SaaS Solutions (30m)
Provide SaaS overview and review updated (simplified diagram).
Discuss `vpn` files and explain real-life customer use case.
Use file-level encryption for secrets + shell script. Wrap up with high-level
cost comparison between solutions.

```
Collection             Version
---------------------- -------
amazon.aws             1.4.0
ansible.netcommon      1.5.0
arista.eos             1.3.0
cisco.ios              1.3.0
cisco.nxos             1.4.0
community.aws          1.3.0
community.general      2.0.0
netbox.netbox          2.0.0
paloaltonetworks.panos 2.5.0
```
