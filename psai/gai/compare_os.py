#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic script to leverage the OpenAI Python package
and demonstrate how to make basic chat completions.
"""

from openai import OpenAI


def main():
    """
    Execution starts here.
    """

    # Provide context for how the AI system should behave
    context = (
        "You are a senior network engineer with extensive experience in"
        " planning, implementing, and validating network migrations."
    )

    question = (
        "In 3 sentences, compare and contrast the Cisco IOS-XE and"
        " Juniper JunOS network operating systems."
    )

    # Create an API client and ask the question
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4",
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

    # Print context, question, and answer
    print(f"Context/persona: {context}")
    print(f"Question: {question}")
    print(f"Answer: {completion.choices[0].message.content}")


if __name__ == "__main__":
    main()
