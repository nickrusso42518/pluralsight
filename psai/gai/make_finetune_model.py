#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Generates/synthesizes training data for a fine-tune
model which is specifically designed for config conversion.
"""

import json
import time
from pathlib import Path
from utils import _make_intf_map
from openai import OpenAI


def main():
    """
    Execution starts here.
    """

    # Define supported platforms
    supported_platforms = [
        "arista_eos",
        "cisco_iosxe",
        "cisco_iosxr",
        "cisco_nxos",
        "juniper_junos",
    ]

    # Initialize empty dict to map OS types to their example configs
    examples = {}
    in_dir = "gai/inputs"
    for plat in supported_platforms:
        with open(f"{in_dir}/example_{plat}.txt", "r") as handle:
            examples[plat] = handle.read()

    # Open the platform map and training prompt template
    with open(f"{in_dir}/platforms.json", "r") as handle:
        platforms = json.load(handle)

    with open(f"{in_dir}/prompt_train.txt", "r") as handle:
        prompt = handle.read()

    # Render the prompt template by providing the required inputs
    context = (
        "You are a senior network engineer with extensive experience in"
        " planning, implementing, and validating network migrations."
    )

    # Initialize empty list to store JSON message dicts as strings
    jsonl_msgs = []

    # Loop over examples in nested form, ignorning self-to-self conversions
    for src_os, src_example in examples.items():
        for dst_os, dst_example in examples.items():
            if src_os == dst_os:
                continue

            # Assemble the prompt using substitution
            question = prompt.format(
                src_type=platforms[src_os]["type"],
                dst_type=platforms[dst_os]["type"],
                config_text=src_example,
                intf_map=_make_intf_map(platforms[src_os], platforms[dst_os]),
                include="\n".join(platforms[dst_os]["include"]),
            )
            messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": question},
                {"role": "assistant", "content": f"```\n{dst_example}\n```"},
            ]
            jsonl_msgs.append(json.dumps({"messages": messages}))

    # Ensure we had the expected number of JSONL items (n * n-1)
    num_plats = len(supported_platforms)
    assert len(jsonl_msgs) == num_plats * (num_plats - 1)

    # Write JSONL data to disk as "plain text" ... not using json.dump()
    trng_file = f"{in_dir}/finetune_trng_data.jsonl"
    with open(trng_file, "w") as handle:
        handle.write("\n".join(jsonl_msgs) + "\n")

    # Create the OpenAI client and upload the training data file
    client = OpenAI()
    upload_file = client.files.create(
        file=Path(trng_file),
        purpose="fine-tune",
    )

    # Create (and start) a fine-tuning job based on that file
    create_ft_job = client.fine_tuning.jobs.create(
        model="gpt-3.5-turbo",
        training_file=upload_file.id,
    )

    # Wait until fine-tuning job is done; success or failure. Options:
    # validating_files, queued, running, succeeded, failed, cancelled
    while True:
        # It's a slow process; wait a bit, then ask for status
        time.sleep(30)
        get_ft_job = client.fine_tuning.jobs.retrieve(
            fine_tuning_job_id=create_ft_job.id,
        )
        print(f"Fine-tune job status: {get_ft_job.status}")

        # If succeeded, stop looping. If failed/cancelled, raise error
        if get_ft_job.status == "succeeded":
            break
        if get_ft_job.status in ["failed", "cancelled"]:
            raise IOError("Fine tune job failed")

    # Save fine-tune model ID (console and disk) so future scripts can use it
    print(f"Fine-tune model ID: {get_ft_job.fine_tuned_model}")
    with open(f"{in_dir}/finetune_model_id.txt", "w") as handle:
        handle.write(get_ft_job.fine_tuned_model)


if __name__ == "__main__":
    main()
