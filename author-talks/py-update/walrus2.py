#!/usr/bin/env python
# Python 3.8: Walrus operation

with open("sample.txt") as handle:
    while data := handle.read(64):
        print(data)
