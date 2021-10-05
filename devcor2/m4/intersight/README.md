# Cisco Intersight
This directory contains files to interact with the Intersight API. This
sandbox requires a sizable amount of administrative setup which is
detailed in the course.

Detailed sandbox instructions can be found here:
`https://devnetsandbox.cisco.com/sandbox-instructions/Intersight/Setup.html`

Intersight API documentation and reference can be found here:
`https://intersight.com/apidocs/introduction/overview/`

## Getting Started
To use the `get_components.py` script, you must export two environment
variables first:

  * `INTERSIGHT_KEY`: This is the API key you generated from the
    Intersight dashboard and contains hexademical digits and
    forward slashes.
  * `INTERSIGHT_SECRET_FILE`: This specifies a path to the file
    containing the RSA private key, also supplied by the Intersight
    dashboard. Ensure this file is *never* shared.

You can copy, edit, and paste these shell commands to get started:
```
export INTERSIGHT_KEY=abcdef0123456789/defabc0987654321
export INTERSIGHT_SECRET_FILE=private_key.txt
```

## Error Messages
Failing to specify any of the environment variables will lead
to the following errors.
```
$ python get_components.py    
Specify key: 'export INTERSIGHT_KEY=<key_string>'

$ python get_components.py 
Specify path: 'export INTERSIGHT_SECRET_FILE=<path>'
```

Also, if Intersight cannot find any data from a specific API request,
this prints the following message (one for each failed request).
Sometimes this occurs when a specific UCS manager has not been
properly claimed/registered to Intersight.

```
$ python get_components.py 
No results from network/Elements; is your UCS Manager claimed?
No results from compute/PhysicalSummaries; is your UCS Manager claimed?
```

## Reference Files
There are two reference files in `data_ref/`:
  `get_network.json`: Example JSON dump of the `network/Elements` resource.
  `get_server.json`: Example JSON dump of the 
  `compute/PhysicalSummaries` resource.

## Credits
The `intersight_auth.py` script was downloaded from this repository without
edits: `https://github.com/movinalot/intersight-rest-api`. This provides an
authentication plugin for `requests` which allows for RSA-based HTTP
request signing in a simplified manner.
