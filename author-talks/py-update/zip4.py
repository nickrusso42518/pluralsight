colors = ["green", "blue", "red", "orange"]
elems = ["earth", "water", "fire"]
for color, elem in zip(colors, elems, strict=True):
    print(color, elem)
