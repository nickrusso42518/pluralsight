# Module 5 - Streaming Model-driven Telemetry using NETCONF
This directory contains files which enable model-driven telemetry (MDT)
on a Cisco IOS-XE router running in the DevNet sandbox. Note that
the sandbox credentials and hostname may change, so be sure to
check the DevNet documentation before blindly running the script.

## Getting Started
The `Dockerfile` and `docker-compose.yml` files are heavily commented, but
in summary, this project is based on the Elastic Stack. It builds on
an existing container which is documented here:
`https://elk-docker.readthedocs.io/`

Assuming you've already installed `docker` and `docker-compose`, 
use `sudo docker-compose up` to deploy the stack. You can use
the Bash scripts in `setup/` to assist with the Docker installation.
Those are the same scripts from a previous course. Next, run the
Python script using `python telemetry.py` to use dial-in
model-driven telemetry (MDT) to the target router. Be sure to
update the ELK DNS name or IP address to suit your environment.

## Making a Dashboard
Follow these steps to create the two dashboards used in the demo.
I encourage you to explore collecting other data as well.

### Initial setup
The Kibana component requires some initial setup:

  - Navigate to `http://(container-ip):5601`
  - Click "Add log data", then "Logstash logs"
  - Don't use `Filebeat`. Scroll down and click "Logstash logs dashboard"
  - If you haven't started the script, you will see a message
    claiming "Couldn't find any Elasticsearch data"
  - From the shell, run `python telemetry.py` to start the script
  - On Kibana, refresh by clicking "Check for new data"
  - This reveals an index like `%{[@metadata][beat]}-2019.09.15`
  - Create an "Index pattern" of `%{[@metadata][beat]}-*`
    to match measurements across multiple days (wildcard)
  - On the next screen, use "Time Filter" of `notificaton.eventTime` which
    is contained in the notification, and continue
  - Scroll down on index pattern page to ensure important metrics are
    of type `number` and not `string`. This is what the `postprocessor` does
    in `xmltodict.parse()` within `telemetry.py`.
  - Click "Discover" (compass icon) to see log examples. Perform a quick
    visual check of the data and make sure it is what you expect

### Adding a line graph
  - Click "Visualize" (line graph) and "Create new visualization"
  - Click "Line" and choose our `%{[@metadata][beat]}-*` index
  - Under the "Data" tab, and "Metrics" header, expand "Y-axis" and update:
    - Aggregation: Average
    - Field: `notification.push-update.datastore-contents-xml.cpu-usage.cpu-utilization.five-seconds`
    - Custom label: CPU 5-second (%) ... or some other label you prefer
  - Under "Buckets", click "Add", then "X-axis"
  - Expand "X-axis" and update:
    - Aggregation: Date Histogram
    - Field: `notification.eventTime`
    - Minimum interval: Manually type 10s to match the period, then press ENTER
  - Click the blue triangle "play" button to apply if the graph doesn't appear
  - Click "Save" at the top and provide a useful name, such as "cpu5seconds"

### Adding an area graph
  - Click "Visualize" (line graph) and "Create new visualization"
  - Click "Area" and choose our `%{[@metadata][beat]}-*` index
  - Expand Y-axis and choose (excluding `notification` headers for brevity):
    - Aggregation: Average
    - Field: `memory-statistic.free-memory`
    - Custom label: "Free Memory" (or something else you prefer)
  - Under "Buckets", click "Add", then "X-axis"
  - Expand "X-axis" and update:
    - Aggregation: Date Histogram
    - Field: `notification.eventTime`
    - Minimum interval: Manually type 10s to match the period, then press ENTER
  - Go to "Metrics & Axes" tab to rename the Y-axis title to "Memory (bytes)"
  - Optional: Repeat the previous steps to add a new Y-axis to add
    "stacking" to the area chart, such as total memory, etc.
  - Click the blue triangle "play" button to apply if the graph doesn't appear
  - Click "Save" at the top and provide a useful name, such as "memory"

### Build a dashboard
  - Click the Dashboard icon (icon has many rectangles)
  - Click "Create new dashboard", then "Add" to select visualizations
  - The two visualizations should be shown. Click each one to add them
  - Click "Save" and name the dashboard "metrics"

## Reference Files
The `data_ref/` directory contains files that help reveal the structured
data received from the NETCONF device. These can help you traverse the
data structures as you explore the code. The files ending in `.json` are
the JSON equivalents of their similarly-named XML counterparts.
  * `sub_good.xml`: The raw RPC reply from a successful
    `establish-subscription` RPC.
  * `sub_bad.xml`: The raw RPC reply from a failed
    `establish-subscription` RPC.
  * `notif_mem.xml`: The notification message for a specific MDT topic,
    and this example shows the `memory` statistics.

The directory also contains YANG tree models:
  * `xe16111_cpu.txt`: Generated by the Cisco native `process-cpu`
    operational data model.
  * `xe16111_mem.txt`: Generated by the Cisco native `memory`
    operational data model.

## CLI output
This section shows samples of CLI output.

### Python script
Assuming debugging outputs are off, the script displays the xpaths to which
the NETCONF client has subscribed along with their subscription IDs. Every
time a notification is received, a one-line summary is displayed.

```
$ python telemetry.py 
Subscribed to '/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds' via ID: 2147483689
Subscribed to '/memory-ios-xe-oper:memory-statistics/memory-statistic' via ID: 2147483690
Logged update from ID 2147483689 at 2019-09-15T11:26:38.70Z
Logged update from ID 2147483690 at 2019-09-15T11:26:38.93Z
Logged update from ID 2147483689 at 2019-09-15T11:26:48.70Z
Logged update from ID 2147483690 at 2019-09-15T11:26:48.93Z
```

### Device being monitored
The following `show` command will reveal active dial-in MDT subscriptions
on the router. The command only shows output when there are live sessions
(ie, after the telemetry script is running).

```
csr1000v-1#show telemetry ietf subscription all detail
Telemetry subscription detail:

  Subscription ID: 2147483689
  Type: Dynamic
  State: Valid
  Stream: yang-push
  Filter:
    Filter type: xpath
    XPath: /process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds
  Update policy:
    Update Trigger: periodic
    Period: 1000
  Encoding: encode-xml
  Source VRF:
  Source Address:
  Notes:

  Receivers:
    Address                Port     Protocol         Protocol Profile
    ---------------------------------------------------------------------
    xx.xxx.207.26          63694    netconf

  Subscription ID: 2147483690
  Type: Dynamic
  State: Valid
  Stream: yang-push
  Filter:
    Filter type: xpath
    XPath: /memory-ios-xe-oper:memory-statistics/memory-statistic
  Update policy:
    Update Trigger: periodic
    Period: 1000
  Encoding: encode-xml
  Source VRF:
  Source Address:
  Notes:

  Receivers:
    Address                Port     Protocol         Protocol Profile
    ---------------------------------------------------------------------
    xx.xxx.207.26          63694    netconf
```
