from pathlib import Path
from setuptools import find_packages, setup

setup(
    name="remarkov",
    version="0.1.0",
    description="Generate text from text using Markov chains.",
    long_description=open(Path(__file__).parent / "README.md").read(),
    author="lausek",
    author_email="input@lausek.eu",
    url="https://github.com/lausek/remarkov",
    packages=find_packages(),
    entry_points={"console_scripts": ["remarkov=remarkov.cli:main"]},
)