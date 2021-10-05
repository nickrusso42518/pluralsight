# Adding MySQL Support
This directory contains the source code to add MySQL support
to the CRM app.

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
