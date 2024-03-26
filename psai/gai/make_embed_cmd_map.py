#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Get embeddings for Cisco and Juniper OSPF commands
and find relevance/similarities.
"""

import os
import json
import ast
from argparse import ArgumentParser
import pandas as pd
import backoff
import openai
from scipy import spatial


@backoff.on_exception(backoff.expo, openai.RateLimitError)
def _create_embeddings(client, **kwargs):
    """
    Decorated function that creates embeddings while obeying
    OpenAI's rate limits using an exponential backoff algorithm.
    This could be based on request or token quantities.
    """
    return client.embeddings.create(**kwargs)


def _get_relatedness(e1, e2):
    """
    Measure relatedness using cosine distance, which is recommended by
    OpenAI when using their embeddings. Subtract it from 1 so that
    numbers closer to 1 represent "more" related ("less" distance).
    """
    return 1 - spatial.distance.cosine(e1, e2)


def main(args):
    """
    Execution starts here.
    """

    # Initialize OpenAI client and other variables
    client = openai.OpenAI()
    in_dir = "gai/inputs"
    emb = {}

    # When loading from CSV, convert stringified list to a list. Example:
    # '[1, 2, 3]' into [1, 2, 3]
    converters = {"embedding": ast.literal_eval}

    # Process each key (platform) in the database
    for plat in [args.src_os, args.dst_os]:
        # Check to see if the embedding file already exists. If it does,
        # and we don't want to recreate, load in the existing data and
        # continue to the next loop element
        emb_file = f"{in_dir}/{plat}_emb.csv"
        if os.path.isfile(emb_file) and not args.recreate:
            print(f"Already have {plat} embeddings: {emb_file}")
            emb[plat] = pd.read_csv(emb_file, converters=converters)
            continue

        # Embedding CSV doesn't exist or user wants to recreate.
        # Read in the commands from each dump, converting them to
        # a set to guarantee uniqueness (and reduce cost). Strip
        # whitespace and ignore comments denoted by #
        print(f"Create new {plat} embeddings")
        with open(f"{in_dir}/{plat}_dump.txt", "r") as handle:
            cmds = list({c.strip() for c in handle if not c.startswith("#")})

        # Create embeddings and ensure equal lengths between
        # input text (commands) and embedding responses
        resp = _create_embeddings(client, model=args.model, input=cmds)
        assert len(cmds) == len(resp.data)

        # Create pandas dataframe (table) mapping the text inputs (commands)
        # to their just-created OpenAI embeddings. Use a small, anonymous
        # lambda function to extract the "embedding" object from each data
        # element in the API response
        emb[plat] = pd.DataFrame(
            {"text": cmds, "embedding": map(lambda emb: emb.embedding, resp.data)}
        )

        # Write the pandas dataframe to disk for use later
        emb[plat].to_csv(emb_file, index=False)
        print(f"Wrote {plat} embeddings to {emb_file}")

    # Uncomment to generate embeddings alone for testing
    # print(emb); return

    # Iterate over src/dst commands/embeddings to find the most related
    # (highest relatedness value) commands, mapping src:dst in the cmd_map.
    cmd_map = {}
    for sc, se in zip(emb[args.src_os].text, emb[args.src_os].embedding):
        for dc, de in zip(emb[args.dst_os].text, emb[args.dst_os].embedding):
            # Compute relatedness between embedding vectors, and store
            # the new value if it's better than what's already there
            rel_val = _get_relatedness(se, de)
            if not sc in cmd_map or rel_val > cmd_map[sc]["rel_val"]:
                cmd_map[sc] = {"dst_cmd": dc, "rel_val": rel_val}

    # Write command map to disk in JSON format. This allows easy "lookups"
    # which has high offline value as well when using "jq". Example:
    # jq '.["<interface> ip ospf cost"]' cisco_iosxe_2_juniper_junos.json
    cmd_map_file = f"{in_dir}/{args.src_os}_2_{args.dst_os}.json"
    with open(cmd_map_file, "w") as handle:
        json.dump(cmd_map, handle, indent=2)
    print(f"Wrote {args.src_os}->{args.dst_os} command map to {cmd_map_file}")


if __name__ == "__main__":
    # Define supported platforms
    supported_platforms = [
        "cisco_iosxe",
        "juniper_junos",
    ]

    # Define supported models
    supported_models = [
        "text-embedding-ada-002",
        "text-embedding-3-small",
        "text-embedding-3-large",
    ]

    # Create parser and add src/dst OS and config arguments
    parser = ArgumentParser()
    parser.add_argument(
        "--src_os",
        help="source/original platform OS",
        choices=supported_platforms,
        required=True,
    )
    parser.add_argument(
        "--dst_os",
        help="destination/target platform OS",
        choices=supported_platforms,
        required=True,
    )
    parser.add_argument(
        "--model",
        help="OpenAI embedding model to use",
        choices=supported_models,
    )
    parser.add_argument(
        "--recreate",
        help="Recreate and overwrite embeddings CSV",
        action="store_true",
    )

    # Alternative method to handle defaults; re-assign with desired value
    args = parser.parse_args()
    if not args.model:
        args.model = supported_models[0]

    # Call main() and pass in parsed arg object to access values
    main(args)
