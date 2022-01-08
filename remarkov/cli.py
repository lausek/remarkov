#!/usr/bin/python3

import sys

from remarkov.remarkov import ReMarkov


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
        "--original-caps",
        action="store_true",
        default=False,
        help="Keep capitalization of the source text.",
    )

    return parser


def add_text_from_file(remarkov: ReMarkov, file_name: str):
    with open(file_name, "r") as fin:
        remarkov.add_text(fin.read())


def add_stdin_text(remarkov: ReMarkov):
    remarkov.add_text(sys.stdin.read())


def run_generation():
    parser = build_argument_parser()
    args = parser.parse_args()

    if args.original_caps:
        remarkov = ReMarkov(order=args.order, before_insert=None)
    else:
        remarkov = ReMarkov(order=args.order)

    if args.files:
        for file_name in args.files:
            add_text_from_file(remarkov, file_name)
    else:
        add_stdin_text(remarkov)

    print(" ".join(remarkov.generate_text(args.words)))


def main():
    try:
        run_generation()
    except Exception as e:
        print(f"ERROR: {e}")
