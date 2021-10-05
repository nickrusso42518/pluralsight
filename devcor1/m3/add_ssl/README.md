# Adding SSL support
This directory contains the source code to add SSL support
to the CRM app.

## SSL Certificates
This project uses self-signed certificates to keep things simple. The
`make_cert.sh` script creates a new `ssl/` directory, then creates a new
certificate (`cert.pem`) and private key (`key.pem`) in that directory.
The Flask app (`src/start.py`) automatically loads these files at runtime
to provide HTTPS support. The `Dockerfile` copies the `ssl/` directory,
along with the `src/` directory, into the container for portability.
This is *not* a secure technique but does sufficiently demonstrate SSL
certificate usage.
