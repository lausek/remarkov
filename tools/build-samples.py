#!/usr/bin/python3

from typing import List


def info(msg: str) -> str:
    import sys

    print(msg, file=sys.stderr)


def build_argument_parser():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--url", type=str, help="URL to the zipped dataset")
    parser.add_argument("--path", type=str, help="Path to the zipped dataset")
    parser.add_argument(
        "--order", type=int, default=4, help="Generate one sample from 1 till `order`"
    )
    parser.add_argument(
        "--samples", type=int, default=4, help="Amount of samples per configuration"
    )

    return parser


def download_dataset(url: str) -> bytes:
    import requests

    return requests.get(url).content


def download_and_save_dataset(url: str) -> str:
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(delete=False) as fout:
        buffer = download_dataset(url)
        fout.write(buffer)

    return fout.name


def generate_samples(amount: int, order: int, text: str) -> List[str]:
    from remarkov import create_model

    model = create_model(order=order)
    model.add_text(text)

    return [model.generate_sentences().text() for _ in range(amount)]


def build_samples(path: str, max_order: int, samples_per_model: int) -> dict:
    from zipfile import ZipFile

    OUTPUT = {}

    with ZipFile(path) as dataset:
        for dataset_file in dataset.namelist():
            if not dataset_file.endswith(".txt"):
                continue

            # strip language
            dataset_file_name = dataset_file.split(".")[0][3:]
            showcase_sample_name = dataset_file_name.replace("-", " ").title().strip()
            showcase_sample_data = {
                "source": dataset_file,
                "samples": {},
            }

            with dataset.open(dataset_file) as fin:
                text = fin.read().decode("utf-8")

            for order in range(1, max_order + 1):
                info(
                    f"Generating {samples_per_model} samples using order {order} from {dataset_file}."
                )
                samples = generate_samples(samples_per_model, order, text)
                info(samples)

                showcase_sample_data["samples"][str(order)] = samples

            OUTPUT[showcase_sample_name] = showcase_sample_data
            info(f"Created showcase sample {showcase_sample_name}.")

    return OUTPUT


def display(obj: dict):
    from json import dumps

    print(dumps(obj, indent=4))


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    if not args.url and not args.path:
        info("Please specify either --url or --path.")
        exit()

    path = args.path if args.path else download_and_save_dataset(args.url)

    output = build_samples(
        path=path,
        max_order=args.order,
        samples_per_model=args.samples,
    )

    display(output)


if __name__ == "__main__":
    main()
