# pywgen - generate pronounceable passwords

pywgen is a Python program to generate passwords which are designed to be
easily memorized by humans, while being as secure as possible.

pywgen is a clone of [pwgen](https://github.com/tytso/pwgen) implementing most
of its features with the exception of options to exclude certain characters
(--ambiguous, --remove-chars and --no-vowels).

## Installing

The program requires Python 3.6 or higher. From the source code or
distribution, the program can be installed as follows:

    python3 -m pip install .

There are no external dependency, only the Python standard library is needed.

## Using

Running `pywgen` from a terminal produces a screen full of passwords. See
`pywgen --help` for usage details.

## Running tests

Tests can be run using [tox](https://tox.readthedocs.io/) by simply executing
the `tox` command in a terminal. Alternatively, the test suite can be run
using [pytest](https://docs.pytest.org/).
