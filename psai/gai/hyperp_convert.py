#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Convert network configuration using few-shot prompting
with hyperparameter adjustments.
"""

import json
import os
from argparse import ArgumentParser
from utils import _make_intf_map
from openai import OpenAI


def main(args):
    """
    Execution starts here.
    """

    # Open the platform map, prompt template, source config, and example files
    in_dir = "gai/inputs"
    with open(f"{in_dir}/platforms.json", "r") as handle:
        platforms = json.load(handle)

    with open(f"{in_dir}/prompt_fewshot.txt", "r") as handle:
        prompt = handle.read()

    with open(f"{in_dir}/example_{args.src_os}.txt", "r") as handle:
        src_example = handle.read()

    with open(f"{in_dir}/example_{args.dst_os}.txt", "r") as handle:
        dst_example = handle.read()

    with open(args.src_cfg, "r") as handle:
        config_text = handle.read()

    # Ensure the choices directory exists to store OpenAI answers
    out_dir = "gai/choices/hyperp"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Provide context for how the AI system should behave
    context = (
        "You are a senior network engineer with extensive experience in"
        " planning, implementing, and validating network migrations."
    )

    # Render the prompt template by providing the required inputs
    question = prompt.format(
        src_type=platforms[args.src_os]["type"],
        dst_type=platforms[args.dst_os]["type"],
        src_example=src_example,
        dst_example=dst_example,
        config_text=config_text,
        intf_map=_make_intf_map(platforms[args.src_os], platforms[args.dst_os]),
        include="\n".join(platforms[args.dst_os]["include"]),
    )
    # print(question); return

    # Create an API client and perform the config conversion. Reducing top_p
    # and temperature generates more deterministic, less creative responses.
    # presence_penalty applies a flat penalty for repetition, while
    # frequency_penalty becomes stricter as repetition increases.
    client = OpenAI()
    completion = client.chat.completions.create(
        model=args.model,
        n=args.num_choices,
        temperature=0.8,
        # top_p=0.3,
        presence_penalty=1,
        # frequency_penalty=0.5,
        max_tokens=1800,
        messages=[
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    # Write all answers to disk in proper directory after removing whitespace
    # and code-denoting backticks, but add a final newline.
    for i, choice in enumerate(completion.choices):
        with open(f"{out_dir}/{i}.txt", "w") as handle:
            handle.write(choice.message.content.strip().strip("```") + "\n")


if __name__ == "__main__":
    # Define supported platforms
    supported_platforms = [
        "arista_eos",
        "cisco_iosxe",
        "cisco_iosxr",
        "cisco_nxos",
        "juniper_junos",
    ]

    # Define supported models (change 3.5 to 35 when using MSFT Azure)
    supported_models = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo",
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
        "--src_cfg",
        help="source/original configuration file",
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
        help="OpenAI LLM to use",
        choices=supported_models,
    )
    parser.add_argument(
        "--num_choices",
        help="number of choices to generate (iterations)",
        type=int,
        default=1,
    )

    # Alternative method to handle defaults; re-assign with desired value
    args = parser.parse_args()
    if not args.model:
        args.model = supported_models[0]

    # Call main() and pass in parsed arg object to access values
    main(args)
