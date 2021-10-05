# Cisco UCS Manager Service Profile Provisioning
This directory contains code to provision new service profiles
from existing service profile templates (created through GUI).
Each service profile represents a physical server as a logical
abstraction and can be associated to a physical server or
a server pool.

## Python code
The `make_service_profiles.py` script contains the logic needed to do two
main actions:

  1. Log into the UCS Manager in the sandbox over HTTP using DevNet
     credentials. Note that the Sandbox UCS Managers are emulated and
     HTTPS does not work well, so I suggest using HTTP.
  2. Issue an API call to create a batch of service profiles from a
     service profile template.

Note that this API is *not* RESTful. All requests used in this
demo are HTTP POST requests. Individual resources are not modeled into
unique and accessible URLs, unlike REST-based APIs.

## Reference Files
The `data_ref/` directory contains files that help reveal the structured
data received from UCS Manager. These can help you traverse the
data structures as you explore the code. The files ending in `.json` are
the JSON equivalents of their similarly-named XML counterparts.
  * `login_resp.xml`: The UCS Manager response from the `aaaLogin` API call.
    Contains a `cookie` which can be used for subsequent API calls.
  * `sp_resp.xml`: The UCS Manager response from the `lsInstantiateNTemplate`
    API call. It contains a list of newly-added service profiles along with
    data about those profiles, such as `dn`.

## Creating a Service Profile Template
At the time of this writing, there does not appear to be an obvious way
to create these templates using the API. Advanced techniques do exist, and
custom libraries have been developed to do it, but these are outside the scope
of this course. Instead, follow these high-level steps in the UCS Manager GUI.

### Pool-related prep work
  1. Click on "LAN", then scroll down in the menu to "Pools"
  2. Click on "MAC Pools" then "MAC Pool default"
  3. Click "Create a Block of MAC Addresses". Adjust the size to 100.
  4. CLick "OK" and ensure there are 100 available MACs in the pool.
  5. Click on "Servers", then scroll down in the menu to "Pools"
  6. Click on "UUID Suffix Pools" then "Pool default"
  7. Click "Create a Block of UUID Suffixes". Adjust the size to 100.
  8. Click "OK" and ensure there are 100 UUIDs in the pool.
  9. (Optional) Click on "Server Pools" then "Server Pool default"
  10. (Optional) Staying under "Servers", scroll down in the menu to "Pools"
  11. (Optional) Click "Add Servers", highlight 4 servers, then click ">>"
      to add them into the default server pool on the right.
  12. (Optional) Click "OK" and ensure there are 4 servers in the pool.

### Building the service profile template
  1. Staying under "Servers", scroll up to "Service Profile Templates".
  2. Right-click "root" then "Create Service Profile Template"
  3. Name the template "globotemplate"
  4. UUID assignment should already be set to use the default pool.
  5. (Optional) Navigate through the other menus to customize the template.

At this point, the Python script should run without errors.
