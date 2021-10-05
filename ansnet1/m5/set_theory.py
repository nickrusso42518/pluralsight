#!/usr/bin/env python

# Route-targets in our "intended state"
want = {
    '65000:1',
    '65000:2',
    '65000:3',
    '65000:4',
    '65000:5'
}

# Route-targets in our "current state"
have = {
    '65000:1',
    '65000:3',
    '65000:5',
    '65000:7',
    '65000:9'
}

# Print out set information
print("Want:   ", want)
print("Have:   ", have)
print("Add:    ", want - have)
print("Delete: ", have - want)
