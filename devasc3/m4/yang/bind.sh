#!/bin/bash
# Quick and dirty command to generate Python bindings for our
# switch interface YANG model. Swap in your Python version as needed.

pyang --plugindir \
  "$VIRTUAL_ENV"/lib/python3.7/site-packages/pyangbind/plugin \
  --format pybind interfaces.yang > interfaces.py
