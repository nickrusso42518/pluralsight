#!/usr/bin/env python
# Python 3.7 Simple Type Hinting

class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, new_age: int) -> None:
        if new_age < 0:
            raise ValueError(f"invalid new_age: {new_age}")
        self._age = new_age

if __name__ == "__main__":
    p1 = Person("nick", 35)
    print(p1.name, p1.age)

    p2 = Person("sophie", 13)
    print(p2.name, p2.age)
