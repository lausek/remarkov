[![PyPI version](https://badge.fury.io/py/remarkov.svg)](https://badge.fury.io/py/remarkov)

# ReMarkov

Generate text from text using Markov chains.

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
# "This is a sample text and this is a sample text and this is a sample text and this is a sample and this is another."
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
pdoc remarkov
```

Publishing is done like this (don't forget to bump the version in `setup.py`):

``` bash
pip3 install twine # optional

python3 setup.py sdist bdist_wheel
twine check "dist/*"
twine upload "dist/*"
```