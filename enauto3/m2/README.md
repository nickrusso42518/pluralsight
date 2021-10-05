# Getting Started with DNA Center Device Management
This directory contains the files needed to build new sites and
perform network discoveries in DNA center.

Relevant files:
  * `site_data/`: Directory that contains input data for area, building, and
    floor in order to build a new site. Also contains information to add a
    dummy device to be assigned to the new site.
  * `build_sites.py`: Loads in the site data to provision new sites and
    assigns a dummy device.
  * `discoveries.json`: List of dictionaries which specifies a discovery that
    should be executed.
  * `run_discoveries.py`: Uses the `discoveries.json` file to iteratively run
    each discovery.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls. There are subdirectories for `site`, `discovery`, and `generic`
JSON responses.
