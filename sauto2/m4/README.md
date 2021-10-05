# Module 4 - Employing Cisco Umbrella to Protect Roaming Endpoints
This directory contains code for the Cisco Umbrella APIs. The following
APIs are in scope, along with their documentation links:
  * Reporting: `https://docs.umbrella.com/umbrella-api/docs/reporting_api_overview`
  * Enforcement: `https://docs.umbrella.com/enforcement-api/reference/#introduction`
  * Investigate: `https://docs.umbrella.com/investigate-api/docs/introduction-to-cisco-investigate`

Export the following environment variables before using the scripts in
this directory to avoid any authentication problems.
```
export UMB_REP_ORG_ID=<your umbrella organization ID>
export UMB_REP_API_KEY=<your umbrella reporting API key>
export UMB_REP_API_SECRET=<your umbrella reporting API secret>
export UMB_ENF_CUST_KEY=<your umbrella integration (enforcement) customer key>
export UMB_INV_API_KEY=<your umbrella investigate API key>
```

The `data_ref/` directory contains example JSON responses from the
various API calls used in the course, as well as sample logs/artifacts.
