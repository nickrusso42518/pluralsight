#!/bin/bash
# Quick test script to run for local testing.
# Generally follows the Travis CI process stages.

# Optionally generate new certs
# ./make_cert.sh
pylint src/*.py
bandit src/*.py --skip B101
pytest src/test_unit.py
sudo docker-compose down --volumes
sudo docker-compose up --build --detach
./wait_for_https.sh 60
# pytest src/test_system.py
