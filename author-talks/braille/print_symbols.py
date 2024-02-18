#!/usr/bin/env python

import json

# Open JSON mapping file for reading
with open("symbols.json", "r") as handle:
    data = json.load(handle)

# Print 8 symbols per row
for i, (k, v) in enumerate(data.items()):
    if i % 8 == 0:
        print()
    num = ord(v) - 10240
    print(f"{k}={v}/{num:02x}  ", end="")
print()
