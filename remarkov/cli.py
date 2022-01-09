#!/usr/bin/python3

import sys

from typing import Optional, TextIO

from remarkov.remarkov import ReMarkov, token_to_lowercase


def create_build_parser(subcommands):
    parser = subcommands.add_parser(
        "build",
        help="build a markov chain from input text and output the model as json",
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=[],
        help="specifies input files for building the model.",
    )
    parser.add_argument(
        "--order", type=int, default=1, help="changes the order of the Markov chain."
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        default=False,
        help="translate all text to lowercase increasing the probability of word linkage.",
    )
    parser.add_argument(
        "--compress",
        action="store_true",
        default=False,
        help="disable newlines in the generated representation.",
    )


def create_generate_parser(subcommands):
    parser = subcommands.add_parser(
        "generate", help="generate text from a markov chain"
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=[],
        help="specifies input files for building the model.",
    )
    parser.add_argument(
        "--order", type=int, default=1, help="changes the order of the Markov chain."
    )
    parser.add_argument(
        "--words", type=int, default=32, help="amount of words to generate."
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        default=False,
        help="translate all text to lowercase increasing the probability of word linkage.",
    )


def create_parser():
    import argparse

    parser = argparse.ArgumentParser()

    subcommands = parser.add_subparsers(title="commands", dest="cmd", required=True)

    create_build_parser(subcommands)
    create_generate_parser(subcommands)

    return parser


def add_text_from_file(remarkov: ReMarkov, file_name: str):
    with open(file_name, "r") as fin:
        remarkov.add_text(fin.read())


def run_command(args=None, stream: Optional[TextIO] = None) -> str:
    parser = create_parser()
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

    if args.cmd == "build":
        return remarkov.to_json(compress=args.compress)
    elif args.cmd == "generate":
        return remarkov.generate(args.words).text()
    else:
        raise NotImplementedError()


def main():
    try:
        output = run_command()
        print(output)
    except Exception as e:
        print(f"ERROR: {e}")
