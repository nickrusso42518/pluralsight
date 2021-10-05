# Building and Applying vSmart Device Templates
This directory contains the files needed to create a new vSmart device
template and apply it to all vSmarts. This is a required step before
application routing policies can be applied to the fabric.

Relevant files:
  * `build_vsmart_template.py`: Creates a new vSmart device template using the
    factory default vSmart feature templates, then applies it to all vSmarts.

Note that if you are using this script for a production deployment, **DO NOT**
blindly use the factory default templates. I'm using them here just to
illustrate ease of configuration from a programmability perspective. Be sure
to create custom feature templates for your environment and add them to the
device template before attaching it.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
