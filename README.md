# ReMarkov

Generate text from text using Markov chains.

``` bash
pip3 install remarkov
```

## Example

``` bash
./tools/scrape-wiki.py --pages Computer_programming | remarkov
```

## Development

Make sure you run pytest as module. This will add the current directory to the import path:

``` bash
python3 -m pytest
```