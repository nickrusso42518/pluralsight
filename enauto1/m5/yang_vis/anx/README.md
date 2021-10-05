# Advanced NETCONF Explorer (ANX)
An alternative to the legacy Cisco DevNet NETCONF explorer.
Be sure you have at least 2 CPU and 4 GB RAM free in your platform before
starting. Also ensure your target device already has `netconf-yang` enabled
as the tool **must** log into a device in order to be uesful.

## Installation
Use this command to run the setup script. You may need to run this command
as `root` using `sudo`.

`./start_anx.sh`

## Using the tool
1. Navigate to `http://<host>:9269` in a web browser (not HTTPS).
2. Provide a device IP/hostname followed by the username and password.
   At the time of this writing, does not support SSH public key authentication.
3. After logging in, ANX will download and parse all YANG models, which
   may take awhile.
4. Once complete, you can explore the YANG models in the left-hand panel,
   optionally viewing the YANG source code or downloading the models.
5. On the right, you can search for interesting text in each model. This
   will expand a traversable form. You can click on elements to highlight
   their attributes which appear on the left.
6. Once you highlight items, you can click "NETCONF Console" to interact
   with the device using various RPCs.
