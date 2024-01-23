# CRM App with CI/CD and Kubernetes
This directory contains a sizable project that builds on the
prerequisite courses by introducing a number of advanced techniques:
  - Python static code analysis using `bandit`
  - SSL certificates to enable HTTPS transport
  - Cross-site request forgery (CSRF) enhancements
  - Publication of custom-build Docker images to Dockerhub
  - Continuous Deployment (CD) to AWS Elastic Kubernetes Service (EKS)

## Source code
All source code, including tests, are including in the `src/` directory.
The key files in that directory are described below.
  * `database.py`: Defines the `Database` class which provides a simple
    interface to the SQL database included with the app. This can be a
    remote database (such as `mysql`) or an in-memory local database
    for testing (such as `sqlite`).
  * `start.py`: The main Flask application.
  * `test_system.py`: The system tests for this project. This requires
    that the application is already deployed on the localhost, often
    using `docker-compose`.
  * `test_unit.py`: The unit tests for this project.

## Database design
The database schema is as follows. These fields correspond to
the important pieces of data related to any CRM account.
```
+------------------------------+--------------+-------------+
| acctid (str15) (primary key) | paid (float) | due (float) |
+------------------------------+--------------+-------------+
```

For security and ease of use, an Object-Relational Mapper (ORM) framework
named `sqlalchemy` is used. This helps prevent SQL injection attacks because
user input is never directly transformed into raw SQL queries. Instead,
programmers interact with the database using Python objects and their
supported methods.

The Flask `src/start.py` file creates the database, which loads in the
seed accounts from `src/data/initial.json` in the `Database` constructor.

## Containers
This project uses two main containers:
  * `web`: This is the Flask app which is neatly packaged into a container
    using the custom `Dockerfile`.
  * `db`: This is the `mysql` container which is a standard, unmodified
    container from Dockerhub.

The `docker-compose.yml` file creates both containers at once which is useful
for testing. This technique was explained in previous courses.

## SSL Certificates
This project uses self-signed certificates to keep things simple. The
`make_cert.sh` script creates a new `ssl/` directory, then creates a new
certificate (`cert.pem`) and private key (`key.pem`) in that directory.
The Flask app (`src/start.py`) automatically loads these files at runtime
to provide HTTPS support. The `Dockerfile` copies the `ssl/` directory,
along with the `src/` directory, into the container for portability.
This is *not* a secure technique but does sufficiently demonstrate SSL
certificate usage.

## Kubernetes (k8s)
The `k8s/` folder contains all k8s-related files. This includes
several Bash scripts:
  * `push_to_dockerhub.sh`: After building the custom Flask image from
    the `Dockerfile`, this script logs into Dockerhub to push (upload)
    the new image. The environment variables `$DOCKER_PASSWORD` and
    `$DOCKER_USERNAME` must be defined before running this script.
  * `install_k8s_pkgs.sh`: Interacting with AWS EKS is complex and requires
    many packages. This script handles the installation and setup of
    those packages, as well as the initial communication to AWS EKS. This
    script uses the cluster name of `globo_cluster`, so be sure to edit this
    if you are using another cluster name. You should also have `awscli`
    pre-configured, or use the following environment variables:
      * `AWS_DEFAULT_REGION`
      * `AWS_ACCESS_KEY_ID`
      * `AWS_SECRET_ACCESS_KEY`
  * `deploy_k8s.sh`: Applies the k8s manifest files stored in `k8s/manifest`:
      * `flask_pod.yml`: Creates a pod for the flask (web) container.
      * `flask_svc.yml`: Creates a service "web" for the flask container.
      * `mysql_pod.yml`: Creates a pod for the mysql (db) container.
      * `mysql_svc.yml`: Creates a service "db" for the mysql container.

## Other scripts
In addition to `make_cert.sh`, there a few other scripts worth mentioning:
  * `quick.sh`: This runs a quick regression test of the entire CI
    test pipeline without CD. It is handy for local testing before `git push`
    to ensure the application is generally functional.
  * `wait_for_https.sh`: Waits for the application to respond to HTTPS
    requests. The database takes time to start up, so the script should hang
    until HTTPS is responding to ensure the system tests that follow do
    not fail (false negatives). This takes one argument which specifies
    the number of seconds to wait. The value 60 appears to work well.
