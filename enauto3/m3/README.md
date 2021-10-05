# Managing Device Configurations Using DNA Center Templates
This directory contains the files needed to update device
configs using VTL templates. Use this Docker container to learn VTL
offline (without DNA center): `https://github.com/nickrusso42518/vtlcli-docker`

Relevant files:
  * `templates/`: Collection of JSON files to be iteratively loaded and
    built into templates within DNA center.
  * `build_templates.py`: Uses the JSON files in `templates/` to build new
    templates, render them, then apply them to a sandbox device (optional).

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
