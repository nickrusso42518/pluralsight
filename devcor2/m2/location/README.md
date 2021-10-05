# Meraki Location Scanning API
This directory contains scripts to simulate the Meraki location API.
At the time of this writing, the Cisco DevNet sandboxes for Meraki do
not have any wireless clients available for testing. This makes a full
test of the location API impossible.

## Testing the Location API
In the course, we used two key scripts:

  * `https_server.py`: This script is the Python receiver which would
    be used both for simulation testing and for integration with a real
    Meraki deployment. This script uses some parts of the logic from
    this repo: `https://github.com/dexterlabora/cmxreceiver-python`,
    except has been optimized and simplified for our use case.
  * `send_data.py`: This script issues HTTP POST requests to act
    like the Meraki system by spoofing location data. The `data.json`
    file contains sample data entries based on the structure here:
    `https://documenter.getpostman.com/view/897512/71FUpux?version=latest`.
    The Postman collection here can be used as an interactive alternative
    to this Python script.

## HTTPS Server Setup
As of August 2019, Meraki no longer supports HTTP targets for its location
API. All targets must be HTTPS using real certificates that Meraki trusts,
which means no self-signed or otherwise untrustworthy certificates.
The simplest solution is create a small HTTPS server follow the process
outlined in the course, but here are the summarized steps:

  1. Install Apache using `yum install httpd` or `sudo apt install apache2`,
     depending on Linux distribution.
  2. Install `certbot` using the script `certbot/setup.sh` and
     corresponding instructions. This will automatically register you
     for a Let's Encrypt (`https://letsencrypt.org/`) certificate. You
     will need your own personal domain for this. This also handles
     updating permissions so Python/Flask can access the cert/key.
  3. Install pip with `sudo apt-get install python3-pip` on the
     HTTPS server along with the server requirements (see below).
  4. Start the HTTPS server using `python3 https_server.py`
  5. From your client workstation, run `send_data.py` and you should see
     a JSON dump printed to the web server's terminal.

## Python packages
Assuming you have Python 3.6 or newer along with `pip` installed on
both the HTTPS server and the Meraki simulation client, use
these requirements files to install packages. If you are not
using `virtualenv`, you may need to use `pip3` versus `pip`.

  * `server_reqts.txt`: Install on the HTTP server
  * `client_reqts.txt`: Install on Meraki simulation client
