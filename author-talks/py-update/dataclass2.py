#!/usr/bin/env python
# Python 3.7 Data Classes

from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

p1 = Person(name="nick", age=35)
p2 = Person(name="carla", age=37)

print(p1)
print(p2)
print(f"Same? {p1 == p2}")
