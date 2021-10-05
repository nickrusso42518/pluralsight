# Module 6 - Implementing Basic Web Application Security
This module adds cross site request forgery (CSRF) protection
into the CRM app using the `flask-WTF` package.

# Summary of updates
  * `src/start.py`: The flask app has CSRF protect enabled, so
    the app expects to receive CSRF tokens from clients.
  * `src/templates/index.html`: The `csrf_token` contains the
    CSRF token that clients use for the next request.
  * `src/old_test_system.py`: Old system tests from previous
    modules are retained here so you can run them and watch
    them fail.
