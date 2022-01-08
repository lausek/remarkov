# MarkovAuthor

Generate Text From Text.

``` bash
pip3 install markov-author
```

## Example

``` bash
./tools/scrape-wiki.py --pages Computer_programming | python3 -m markov-author --
```

## Development

Make sure you run pytest as module. This will add the current directory to the import path:

``` bash
python3 -m pytest
```