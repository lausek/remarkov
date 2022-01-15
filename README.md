[![PyPI version](https://badge.fury.io/py/remarkov.svg)](https://badge.fury.io/py/remarkov)

<img align="left" src="https://raw.githubusercontent.com/lausek/remarkov/gh-pages/public/logo192.png" height="120px" />

**ReMarkov** is a Python library for generating text from preexisting samples using [Markov chains](https://en.wikipedia.org/wiki/Markov_chain).
You can use it to customize all sorts of writing from birthday messages, horoscopes, Wikipedia articles, or the utterances of your game's NPCs.
Everything works without an omnipotent *"AI"* - it is dead-simple code and therefore fast.

Feel free to contribute!

<br clear="both" />

## Installation

``` bash
pip3 install remarkov
```

## Example

Scrape the Wikipedia page for "Computer Programming" and generate a new text from it:

``` bash
./tools/scrape-wiki.py Computer_programming | remarkov build | remarkov generate
```

You can also use `remarkov` programmatically:

``` bash
from remarkov import create_model

model = create_model()
model.add_text("This is a sample text and this is another.")

print(model.generate().text())
# "This is a sample text and this is a sample text and this is a sample text ..."
```

## Development

Make sure you run pytest as module. This will add the current directory to the import path:

``` bash
python3 -m pytest
```

This project uses [black](https://github.com/psf/black) for source code formatting:

``` bash
black .
```

Generate documentation for the project (this uses the original pdoc at [pdoc.dev](https://pdoc.dev)):

``` bash
git checkout gh-pages
pdoc -t pdoc/template -o public/docs <path_to_remarkov_module>
```

Run type checks using [mypy](https://github.com/python/mypy):

``` bash
mypy -p remarkov
```

Publishing is done like this (don't forget to bump the version in `setup.py`):

``` bash
pip3 install twine # optional

git tag -a <version>
git push --tags

python3 setup.py sdist bdist_wheel
twine check "dist/*"
twine upload "dist/*"
```
