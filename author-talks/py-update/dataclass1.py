#!/usr/bin/env python
# Boilerplate without Data Classes

class Person:
    def __init__(self, name, age):
       self.name = name
       self.age = age

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age})"

p1 = Person(name="nick", age=35)
p2 = Person(name="carla", age=37)

print(p1); print(p2)
print(f"Same? {p1 == p2}")
