# Module 4 - Updating CI Tests and Integrating Static Code Analysis
This module adds testing for the database and SSL upgrades
from the previous module. It also adds static code analysis
using the Python `bandit` package.

## Additional scripts
In addition to `make_cert.sh`, there a few other scripts worth mentioning:
  * `quick.sh`: This runs a quick regression test of the entire CI
    test pipeline without CD. It is handy for local testing before `git push`
    to ensure the application is generally functional.
  * `wait_for_https.sh`: Waits for the application to respond to HTTPS
    requests. The database takes time to start up, so the script should hang
    until HTTPS is responding to ensure the system tests that follow do
    not fail (false negatives). This takes one argument which specifies
    the number of seconds to wait. The value 60 appears to work well.
