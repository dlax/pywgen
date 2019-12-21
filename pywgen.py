"""generate pronounceable passwords"""

import argparse
import pkg_resources
import secrets
import string
from typing import List, Optional


def has_capitals(values: List[str]) -> bool:
    return any(v.isupper() for v in values)


def generate_password(
    length: int, numerals: bool = True, capitalize: Optional[bool] = None
) -> str:
    """Return one password of specified `length` possibly excluding/including
    character types matching keyword arguments.

    `capitalize` controls whether produced password must (True value), may
    (None value) or must not (False value) contain capital letters.
    """
    if capitalize is False:
        chars = string.ascii_lowercase
    else:
        chars = string.ascii_letters
    if numerals:
        chars += string.digits
    while True:
        elements = [secrets.choice(chars) for _ in range(length)]
        if not capitalize or (capitalize and has_capitals(elements)):
            return "".join(elements)


def get_parser() -> argparse.ArgumentParser:
    prog = "pywgen"
    parser = argparse.ArgumentParser(prog, description=__doc__)
    dist = pkg_resources.get_distribution(prog)
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {dist.version}"
    )
    return parser


def main() -> None:
    parser = get_parser()
    parser.parse_args()


if __name__ == "__main__":
    main()
