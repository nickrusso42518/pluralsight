#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Simple, semi-interactive script to experiment with xpath.
Should be run as "python -i ixpath.py <inputfile.xml>"
"""

from lxml import etree
import sys

def strip_ns(root):
    """
    Remove all XML namespaces from the document, making it easier to
    issue xpath queries. Credit to Jeremy Schulman.
    """
    for elem in root.getiterator():
        elem.tag = etree.QName(elem).localname
    etree.cleanup_namespaces(root)
    return root

def s(root):
    """
    Print the string representation of an element. If it's a list,
    iteratively print all elements.
    """

    if isinstance(root, list):
        for elem in root:
            print(etree.tostring(elem, encoding="unicode"))
    else:
        print(etree.tostring(root, encoding="unicode"))


# Load in the CLI-specified XML file, recovering from any errors if possible
et = etree.parse(sys.argv[1], parser=etree.XMLParser(recover=True))

# String namespaces
et = strip_ns(et)

# Globally accessible delegated function to make xpath queries easier
x = et.xpath

print("xpath query: x(str) // to string: s(elem)")
