# pywgen - generate pronounceable passwords

pywgen is a Python program to generate passwords which are designed to be
easily memorized by humans, while being as secure as possible.

pywgen is a clone of [pwgen](https://github.com/tytso/pwgen) implementing most
of its features with the exception of options to exclude certain characters
(--ambiguous, --remove-chars and --no-vowels).

## Running tests

Tests can be run using [tox](https://tox.readthedocs.io/) by simply executing
the `tox` in a terminal. Alternatively, the test suite can be run using
[pytest](https://docs.pytest.org/).
