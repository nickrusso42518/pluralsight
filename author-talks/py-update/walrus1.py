#!/usr/bin/env python
# Need to read input first, then loop

with open("sample.txt") as handle:
    data = handle.read(64)
    while data:
        print(data)
        data = handle.read(64)
