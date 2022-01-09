#!/usr/bin/python3

import sys

from typing import Optional, TextIO

from remarkov.remarkov import ReMarkov, token_to_lowercase


def build_argument_parser():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "files",
        nargs="*",
        default=[],
        help="Specifies the files to import for generation.",
    )
    parser.add_argument(
        "--order", type=int, default=1, help="Changes the order of the Markov chain."
    )
    parser.add_argument(
        "--words", type=int, default=32, help="Amount of words to generate."
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        default=False,
        help="Translate all text to lowercase increasing the probability of word linkage.",
    )

    return parser


def add_text_from_file(remarkov: ReMarkov, file_name: str):
    with open(file_name, "r") as fin:
        remarkov.add_text(fin.read())


def run_generation(args=None, stream: Optional[TextIO] = None) -> str:
    parser = build_argument_parser()
    args = parser.parse_args(args)

    before_insert = token_to_lowercase if args.normalize else None
    remarkov = ReMarkov(order=args.order, before_insert=before_insert)

    if args.files:
        for file_name in args.files:
            add_text_from_file(remarkov, file_name)
    else:
        if not stream:
            stream = sys.stdin

        remarkov.add_text(stream.read())

    return remarkov.generate(args.words).text()


def main():
    try:
        output = run_generation()
        print(output)
    except Exception as e:
        print(f"ERROR: {e}")
