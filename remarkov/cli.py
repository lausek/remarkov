#!/usr/bin/python3

import sys

from typing import Optional, TextIO

from remarkov.tokenizer import token_to_lowercase
from remarkov.model import DEFAULT_GENERATE_WORD_AMOUNT, Model
from remarkov import create_model, load_model, parse_model


def create_build_parser(subcommands):
    parser = subcommands.add_parser(
        "build",
        help="build a markov chain from input text and output the model as json",
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=[],
        help="specifies input files for building the model",
    )
    parser.add_argument(
        "--order", type=int, default=1, help="changes the order of the Markov chain"
    )
    parser.add_argument(
        "--ngrams", type=int, nargs="?", help="tokenizes the input text into n-grams"
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        default=False,
        help="translate all text to lowercase increasing the probability of word linkage",
    )
    parser.add_argument(
        "--compress",
        action="store_true",
        default=False,
        help="disable newlines in the generated representation",
    )


def create_generate_parser(subcommands):
    parser = subcommands.add_parser(
        "generate", help="generate text from a markov chain"
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="path to the model file",
    )
    parser.add_argument(
        "--words",
        type=int,
        default=DEFAULT_GENERATE_WORD_AMOUNT,
        help="amount of words to generate",
    )


def create_parser():
    import argparse

    parser = argparse.ArgumentParser()

    subcommands = parser.add_subparsers(title="commands", dest="cmd", required=True)

    create_build_parser(subcommands)
    create_generate_parser(subcommands)

    return parser


def add_text_from_file(remarkov: Model, file_name: str):
    with open(file_name, "r") as fin:
        remarkov.add_text(fin.read())


def run_build(args, stream: TextIO) -> str:
    from remarkov.tokenizer import create_ngram_tokenizer

    tokenizer = create_ngram_tokenizer(args.ngrams) if args.ngrams else None
    before_insert = token_to_lowercase if args.normalize else None
    model = create_model(
        order=args.order, tokenizer=tokenizer, before_insert=before_insert
    )

    if args.files:
        for file_name in args.files:
            add_text_from_file(model, file_name)
    else:
        model.add_text(stream.read())
    return model.to_json(compress=args.compress)


def run_generate(args, stream: TextIO) -> str:
    model = load_model(args.model) if args.model else parse_model(stream.read())
    return model.generate(args.words).text()


def run_command(args=None, stream: Optional[TextIO] = None) -> str:
    parser = create_parser()
    args = parser.parse_args(args)

    # if no stream was provided, fallback to stdin
    if not stream:
        stream = sys.stdin

    if args.cmd == "build":
        return run_build(args, stream)
    elif args.cmd == "generate":
        return run_generate(args, stream)
    else:
        raise NotImplementedError()


def main():
    try:
        output = run_command()
        print(output)
    except Exception as e:
        print(f"ERROR: {e}")
