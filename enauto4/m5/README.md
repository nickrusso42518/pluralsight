# Monitoring and Troubleshooting the SD-WAN Fabric
This directory contains the files needed to collect information from
a variety of different APIs. Most of these scripts are short and simple.

Relevant files:
  * `get_system_stats.py`: Collect the CPU and memory statistics using
    a custom query defined in `sys_stat_query.json`.
  * `get_dashboard_info.py`: Collect miscellaneous facts from the dashboard
    API, such as alarm status, certificate summary, and control status.
  * `get_certs.py`: Perform a back of the controller certificates, plus the
    root CA certificate, into the `backup_certs/` directory.
  * `get_rtm_info.py`: Collect miscellaneous facts from the real-time
    monitoring API, tunnel statistics and control connections.
  * `run_security_audit.py`: Creates a new user with permissions to view
    the audit log, then collects the log entries into CSV format.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
