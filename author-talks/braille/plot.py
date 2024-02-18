#!/usr/bin/env python

"""
Plot Braille symbols on Cartesian coordinate system to
model the coffee sleeve design.
"""

import json
import sys
import matplotlib.pyplot as plt

# When converting unicode chars to ints, the bits we care about are offset
# by 10240 just given their position in the unicode plan. This must be
# subtracted before performing any bitwise logic. Same as 0x2800 in hex.
# >>> ord("\u2800") 10240
# >>> ord("\u283f") 10303
BRAILLE_UNICODE_OFFSET = 10240

# Define a constant dict to identify the coordinates of each Braille
# position in accordance with ISO/TR 11548-1
GRID = {
  1: (1, 3),
  2: (1, 2),
  3: (1, 1),
  4: (2, 3),
  5: (2, 2),
  6: (2, 1)
}

# For longer dicts, the data can be included in a JSON (or YAML or XML) file.
# Read in the contents of the file and convert to a Python dict for easy
# reference. Print an error message and raise error if decoding fails.
with open("symbols.json", "r") as handle:
    try:
        SYMBOLS = json.load(handle)
    except json.JSONDecodeError as exc:
        print("Could not load Braille symbols from symbols.json")
        raise


def main(name):
    """
    Main logic of the program. Consumes a text name for conversion to Braille
    and subsequent plotting on the graph.
    """

    # Convert the text name into Braille symbols
    braille = convert_name(name)
    print(header := f"{name}: {braille}")

    # Plot each symbol independently, counting each one to ensure
    # the x_offset continues to increment by 2 as the symbols are plotted
    for i, symbol in enumerate(braille):
        plot_symbol(symbol, i * 2)

    # Graph cleanup: specify a title, x/y axis limits, and scaling aspect
    plt.title(header)
    plt.xlim(0, 40)
    plt.ylim(0, 4)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()


def plot_symbol(symbol, x_offset):
    """
    Given a single Braille symbol and an x-axis offset, plot the dots to
    visually draw the symbol.
    """

    # Ensure the input symbol and x_offset are valid; else raise errors
    if len(symbol) != 1:
        raise ValueError(f"symbol must have length of 1: {symbol}")

    if not isinstance(x_offset, int) or x_offset < 0:
        raise ValueError(f"x_offset must be a positive integer: {x_offset}")

    # To make the plot easier to read for non-Braille readers, alternate
    # the symbol colors between red and blue. Index a two-char string
    # containing the color codes using a mix of modulus and floor division
    # to solve it WITHOUT needing to pass in another argument.
    # Results in alternating "ro" and "bo" strings for plotting.
    fmt = "rb"[(x_offset % 4) // 2] + "o"
    print(f"Symbol {symbol} using format {fmt}")

    # There are 6 bits in the Braille symbol; iterate over it and compute
    # the bit position using 2^i exponent logic (0, 1, 2, 4, 16, 32)
    for i in range(6):
        bit = 2 ** i

        # Test the ordinal value for the presence of a given bit. If set,
        # plot the appropriate dot on the graph by referencing the GRID
        # map, applying the x_offset, and specifying the format string.
        if (ord(symbol) - BRAILLE_UNICODE_OFFSET) & bit:
            dot = GRID[i + 1]
            plt.plot(dot[0] + x_offset, dot[1], fmt)
            print(f"  raises bit {i} ({bit:02}) for dot {dot}")

def convert_name(name):

    # Define an empty braille string iterate over the chars in each name
    braille = ""
    for char in name:

        # Uppercase characters must be preceded by a special symbol
        if char.isupper():
            braille += SYMBOLS["UPPER"]

        # Lookup the character in the symbol map and append to string
        braille += SYMBOLS[char.lower()]

    # String has been formed successfully; return it
    return braille


if __name__ == "__main__":
    # If the CLI argument vector (argv) contains less than 2 entries,
    # this means no user-specified arguments exist. Supply a sample instead
    if len(sys.argv) < 2:
        main("WB Coffee Co")

    # User-specified arguments exist; pass in the first one, ignore others
    else:
        main(sys.argv[1])
