"""generate pronounceable passwords"""

import argparse
import pkg_resources
import secrets
import string


def generate_password(length: int, numerals: bool = True) -> str:
    """Return one password of specified `length` possibly excluding/including
    character types matching keyword arguments.
    """
    chars = string.ascii_letters
    if numerals:
        chars += string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


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
