# Module 6: Understanding Web Application Threats and Mitigations
This directory contains the Globomantics CRM code except modified to
be far less secure. The web interface is now susceptible to injection
attacks. Enter code like `db.data["ACCT100"]["due"]=0` into the web
form to overwrite data entries and wreak havoc.

## Reference files
The `secret_ref/` directory contains the tiny scripts used in the slides
which illustrate simple options for handling passwords/secrets in Python
applications.
