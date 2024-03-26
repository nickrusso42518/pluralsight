#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Defines helper functions used for both foundation
and fine-tuned model chat completions.
"""


def _make_intf_map(src_plat, dst_plat):
    """
    Given source and destination subdictionaries, map interfaces between
    the configuration styles. Returns a two-column CSV with one row for
    each source interface to be mapped.
    """

    # Be sure to only add source interfaces if the are unique. Example:
    # NX-OS/EOS only use "ethernet", so mapping from these types is difficult.
    text = ""
    src_seen = set()
    for speed, src_intf in src_plat["intf"].items():
        if src_intf not in src_seen:
            dst_intf = dst_plat["intf"].get(speed, f"src_{src_intf}")
            text += f"{src_intf},{dst_intf}\n"
            src_seen.add(src_intf)
    return text.strip()
