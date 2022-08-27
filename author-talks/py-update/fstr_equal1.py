#!/usr/bin/env
# Boilerplate needed to print variable names

def factorial(n):
    total = 0
    for i in range(n):
        print(f"i={i}, total={total}")
        total *= i + 1
        print(f"i={i}, total={total}")
    return total

print(factorial(3))
print(factorial(5))
