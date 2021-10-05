#!/bin/bash

# Create network by creating one router and adding two more
ncs-netsim create-device cisco-ios router1
ncs-netsim add-device cisco-ios router2
ncs-netsim add-device cisco-ios router3

# Change into the netsim directory, start the netsim, and get basic info
cd netsim
ncs-netsim start
ncs-netsim is-alive
ncs-netsim list
