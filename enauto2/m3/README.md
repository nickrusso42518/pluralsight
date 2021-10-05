# Collecting Video Footage from Meraki MV Cameras
This directory contains many scripts to manage Meraki cameras:

  * `get_footage.py`: Gets a live video link for viewing, plus a point-in-time
    snapshot downloaded to `camera_snapshots/`.
  * `get_mvsense.py`: Uses the MV sense analytics engine to collect various
    pieces of data from the API.
  * `update_qr.py`: Loads the `qr_settings.json` then updates the camera quality
    and retention settings. This is a minor task but important to know.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
