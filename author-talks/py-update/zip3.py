colors = ["green", "blue", "red", "orange"]
elems = ["earth", "water", "fire"]

if len(colors) != len(elems):
    raise ValueError("lists are unequal length")

for color, elem in zip(colors, elems):
    print(color, elem)
