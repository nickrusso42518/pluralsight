import json
import sys


with open("symbols.json", "r") as handle:
    try:
        SYMBOLS = json.load(handle)
    except json.JSONDecodeError as exc:
        print(exc)


def main(names):
    """
    Convert each name in the list of supplied names from text
    into braille, displayed to the screen.
    """

    # Iterate over the names, ensuring they contain only alphabetic characters
    # If not, silently ignore the name and process the rest
    for name in names:
        if not name.isalpha():
            continue

        # Define an empty braille string iterate over the chars in each name
        braille = ""
        for char in name:

            # Uppercase characters must be preceded by a special symbol
            if char.isupper():
                braille += SYMBOLS["UPPER"]

            # Lookup the character in the symbol map and append to string
            braille += SYMBOLS[char.lower()]

        # Display the original text name and its corresponding braille
        print(f"{name}={braille}")
        print(json.dumps({name: braille}, indent=2))


if __name__ == "__main__":
    # If the CLI argument vector (argv) contains less than 2 entries,
    # this means no user-specified arguments exist. Supply the ficticious
    # company name instead
    if len(sys.argv) < 2:
        main(["Wired", "Brain", "Coffee"])

    # User-specified arguments exist; pass those in directory
    else:
        main(sys.argv[1:])
