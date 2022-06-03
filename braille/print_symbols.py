#!/usr/bin/env python

import json

# Open JSON mapping file for reading
with open("symbols.json", "r") as f:
    data = json.load(f)

# Print 13 symbols per row
for i, (k, v) in enumerate(data.items()):
    if i % 13 == 0:
        print()
    num = ord(v) - 10240
    print(f"{k}={v}/{num:02x} ", end="")
print()
