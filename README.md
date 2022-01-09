[![PyPI version](https://badge.fury.io/py/remarkov.svg)](https://badge.fury.io/py/remarkov)

# ReMarkov

Generate text from text using Markov chains.

``` bash
pip3 install remarkov
```

## Example

Scrape the Wikipedia page for "Computer Programming" and generate a new text from it:

``` bash
./tools/scrape-wiki.py --pages Computer_programming | remarkov
```

## Development

Make sure you run pytest as module. This will add the current directory to the import path:

``` bash
python3 -m pytest
```
