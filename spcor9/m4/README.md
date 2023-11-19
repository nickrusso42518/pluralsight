# Deploying a Pre-made, Known-good Telemetry Stack
Reference information below. You can install docker and docker-compose
using scripts in the `setup/` directory. `data_ref/` includes importable
Grafana dashboards.

Grafana login
```
http://grafana_host:3000
admin/admin
```

Example SNMP interfaces
```
CSR03#show snmp mib ifmib ifindex | include 2[456]
GigabitEthernet2.3038: Ifindex = 25
GigabitEthernet2.3023: Ifindex = 26
GigabitEthernet2.3035: Ifindex = 24
```

Purge IS-IS LSPs with `test isis lsp purge`

SNMP OID reference:
```
ciiNotificationEntry.1 (1.3.6.1.4.1.9.10.118.1.10.1.1): sender system ID
ciiNotificationEntry.13 (1.3.6.1.4.1.9.10.118.1.10.1.13): level 1 or 2
ciiNotificationEntry.1 (1.3.6.1.4.1.9.10.118.1.3.2.1.2): affected interface
```
