# Cisco DevNet yangexplorer
This legacy tool will likely not be used much in the future, but it is still
powerful for basic NETCONF/YANG exploration.

## Installation
Use this command to run the setup script. You may need to run this command
as `root` using `sudo`.

`./start_yangexplorer.sh`

## Basic exploration
1. From main page, click "Login" using guest/guest
2. `ietf-interfaces` appears as the sample model available
3. Expand to show subfolders to interfaces/interface for config
4. `interface` is a list, `name` is the key, click it
5. Observe attributes on the right
6. Click green leaf `description` (not mandatory)
7. Click red leaf `type` (mandatory)
8. Config/oper button allows for RW or RO, safety feature

## Loading additional models
1. In the middle panel, choose the "Manage Models" tab at the top
2. Click "Add" at the bottom to browse from your local machine.
   You can `git clone` the YANG models repo to grab everything
3. Click "Browse"
4. Choose `yang/vendor/cisco/xe/16111/Cisco-IOS-XE-cdp-oper.yang`
5. Click "Upload"
6. Navigate to `Cisco-IOS-XE-cdp-oper.yang`
7. Once uploaded, click the checkbox for that model, then click "Subscribe"
8. Expand the new `Cisco-IOS-XE-cdp-oper` model in the explorer
9. Navigate into `cdp-neighbor-details/cdp-neighbor-detail`
10. Explore the `device-name` item; note the xpath filter

## Using NETCONF tools
1. Click "Oper" radio button in the bottom left
2. Expand the new `Cisco-IOS-XE-cdp-oper` model in the explorer
3. Navigate into `cdp-neighbor-details/cdp-neighbor-detail`
4. At the `cdp-neighbor-detail` directory, set "Values" to `<get>`
5. On the middle panel, click "RPC" to get the NETCONF RPC in XML format.
6. If we fill in the connectivity settings, we can interactively issue this RPC
  * Platform: `csr`
  * Host: `192.168.2.191`
  * Port: `830` (default)
  * Username: `cisco`
  * Password: `cisco`
7. Click "Run" and observe the result: all the CDP neighbor details
8. Remove `<get>` from the directory level, and add it to `device-name` and `capability`
9. Click "Run" and observe the result: only the device names and capabilities
