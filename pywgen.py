"""generate pronounceable passwords"""

import argparse
import pkg_resources
import secrets
import string
from typing import List, Optional


def has_capitals(values: List[str]) -> bool:
    return any(v.isupper() for v in values)


def has_numerals(values: List[str]) -> bool:
    return any(v.isdigit() for v in values)


def generate_password(
    length: int, numerals: Optional[bool] = None, capitalize: Optional[bool] = None
) -> str:
    """Return one password of specified `length` possibly excluding/including
    character types matching keyword arguments.

    `numerals` (resp. `capitalize`) control whether produced password must
    (True value), may (None value) or must not (False value) contain numerals
    (resp. capital letters).
    """
    if capitalize is False:
        chars = string.ascii_lowercase
    else:
        chars = string.ascii_letters
    if numerals is not False:
        chars += string.digits
    while True:
        elements = [secrets.choice(chars) for _ in range(length)]
        if (not capitalize or (capitalize and has_capitals(elements))) and (
            not numerals or (numerals and has_numerals(elements))
        ):
            return "".join(elements)


def get_parser() -> argparse.ArgumentParser:
    prog = "pywgen"
    parser = argparse.ArgumentParser(prog, description=__doc__)
    dist = pkg_resources.get_distribution(prog)
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {dist.version}"
    )
    numerals_group = parser.add_mutually_exclusive_group()
    numerals_group.add_argument(
        "-0",
        "--no-numerals",
        help="don't include numbers in the generated password",
        action="store_false",
        dest="numerals",
        default=None,
    )
    numerals_group.add_argument(
        "-n",
        "--numerals",
        help="include at least one number in the generated password",
        action="store_true",
        dest="numerals",
        default=None,
    )
    capitalize_group = parser.add_mutually_exclusive_group()
    capitalize_group.add_argument(
        "-A",
        "--no-capitalize",
        help="don't include capital letters in the generated password",
        action="store_false",
        dest="capitalize",
        default=None,
    )
    capitalize_group.add_argument(
        "-c",
        "--capitalize",
        help="include at least one capital letter in the generated password",
        action="store_true",
        dest="capitalize",
        default=None,
    )
    return parser


def main() -> None:
    parser = get_parser()
    parser.parse_args()


if __name__ == "__main__":
    main()
