from pathlib import Path
from setuptools import find_packages, setup

setup(
    name="remarkov",
    version="0.2.4",
    description="Generate text from text using Markov chains.",
    author="lausek",
    author_email="input@lausek.eu",
    url="https://github.com/lausek/remarkov",
    packages=find_packages(),
    entry_points={"console_scripts": ["remarkov=remarkov.cli:main"]},
    long_description=open(Path(__file__).parent / "README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords=[
        "markov",
        "cli",
    ],
)
