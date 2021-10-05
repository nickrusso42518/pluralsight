# Module 5 - Introducing Application Programming Interfaces (API)
There are many different files in this directory.

## Postman Requests
This directory contains Postman DNAC collection as a JSON file.
This contains the two requests covered in the course. I tested it
on Postman version 7.3.4 and the collection uses scheme version 2.1.

To use it, click `Import` from the main Postman dashboard and select
the JSON file. After running the token request, be sure to copy/paste
the token text into the `X-Auth-Token` of the device collection
request by replacing `PASTE-TOKEN-HERE` with the token.

## Scripts for curl
I've also included two one-line bash scripts. One of them collects the
access token while the other collects list of devices using `curl`. Again,
be sure to replace `PASTE-TOKEN-HERE` with the proper token.

## HTTP Packet Capture
The `flask_http.pcapng` contains the Wireshark-collected packets seen in
the course. HTTP normally runs on port 80, not 5000, so you'll need to
decode these TCP 5000 ports as HTTP. This process may change between
versions of Wireshark, but in general:
  1. Right-click on any packet that uses TCP 5000
  2. Click `Decode As`
  3. Select `HTTP` (not `HTTP2`) from the drop-down menu
