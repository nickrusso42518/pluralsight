#!/usr/bin/env python
# Python 3.9 Dictionary merging

adults = {"nick": "dad", "carla": "mom"}
children = {"livvy": "sis1", "josie": "sis2", "nick": "jr"}

# Merge without assignment
print(adults | children)

# Merge with assignment (like .update() method)
adults |= children
print(adults)
