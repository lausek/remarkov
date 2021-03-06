#!/usr/bin/python3

"""
A tool for scraping Wikipedia posts. This prints the extracted text to stdout.
"""

from collections import namedtuple

REMOVE_CLASSES = [
    "reference",
    "references",
    "noprint",
    "internal",
]

PageLoadResult = namedtuple(
    "PageLoadResult",
    [
        "text",
        "related_pages",
    ],
)


def info(msg: str) -> str:
    import sys

    print(msg, file=sys.stderr)


def is_related_page(anchor) -> bool:
    if anchor.get("href", None) is None:
        return False

    return anchor.get("href").startswith("/wiki/")


def anchors_to_page_names(anchors) -> list:
    page_names = set()

    for anchor in anchors:
        # remove relative wiki link.
        page_name = anchor.get("href")[len("/wiki/") :]
        # if there is a selector on the url -> remove it as well.
        page_name, *_ = page_name.split("#")

        page_names.add(page_name)

    return list(page_names)


def load_page(name: str, language: str = "en") -> PageLoadResult:
    import requests
    from bs4 import BeautifulSoup

    API = f"http://{language}.wikipedia.org/w/api.php"

    params = {
        "action": "parse",
        "page": name,
        "prop": "text",
        "formatversion": 2,
        "format": "json",
    }

    response = requests.get(API, params)

    if response.status_code != 200:
        return None

    response_body = response.json()

    if "error" in response_body:
        return None

    text = response_body["parse"]["text"]
    page = BeautifulSoup(text, "html.parser")

    for nav_frame in page.find_all(class_="NavFrame"):
        nav_frame.decompose()

    related_pages = filter(is_related_page, page.find_all("a"))
    related_pages = anchors_to_page_names(related_pages)

    paragraphs = page.find_all("p")

    # remove some unwanted html elements.
    for paragraph in paragraphs:
        remove_elements = paragraph.find_all("span")

        # remove html elements that we do not want in our output. references, etc.
        for cls in REMOVE_CLASSES:
            remove_elements.extend(paragraph.find_all(class_=cls))

        for tag in remove_elements:
            tag.decompose()

    # extract text from paragraphs and concatenate.
    text = " ".join(map(lambda p: p.get_text(), paragraphs))

    return PageLoadResult(text=text, related_pages=related_pages)


def build_argument_parser():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "pages",
        nargs="+",
        default=[],
        help="list of pages to scrape",
    )
    parser.add_argument(
        "--limit", type=int, default=5, help="maximum amount of fetched pages"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="language identifier: en, de, ru, etc.",
    )
    parser.add_argument(
        "--tee",
        action="store_true",
        default=False,
        help="sends the scraped text to stdout and stderr",
    )

    return parser


def scrape_queue(initial_pages: list, limit: int, language: str, tee: bool):
    import random
    import time

    page_name_scrape_queue = [*initial_pages]
    page_name_scraped = []
    scraped_pages = 0

    while scraped_pages < limit:
        try:
            page_name = page_name_scrape_queue.pop(0)
        except IndexError:
            # no more pages to scrape.
            break

        if ":" in page_name:
            info(f"{page_name} is Wikipedia stuff. Skipping.")
            continue

        if page_name in page_name_scraped:
            info(f"{page_name} was already scraped. Skipping.")
            continue

        info(f"Loading page {page_name} ...")
        page = load_page(page_name, language=language)

        # page loading failed. just try the next one.
        if page is None:
            info(f"Loading page {page_name} failed. Skipping.")
            continue

        print(page.text)

        if tee:
            info(page.text)

        # push some mentioned pages into the scrape queue.
        page_name_scrape_queue.extend(page.related_pages[:4])
        page_name_scraped.append(page_name)
        scraped_pages += 1

        # sleep a little.
        sleep_time = random.randint(0, 2)
        info(f"Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    page_name_scrape_queue = [*args.pages]
    scrape_queue(
        page_name_scrape_queue, limit=args.limit, language=args.language, tee=args.tee
    )


if __name__ == "__main__":
    main()
