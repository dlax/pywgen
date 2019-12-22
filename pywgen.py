"""generate pronounceable passwords

When standard output (stdout) is  not  a tty, pywgen will only generate one
password, as this tends to be much more convenient for shell scripts.
Otherwise, a screenfull of passwords is produced.
"""

import argparse
import pkg_resources
import secrets
import string
import sys
from typing import Iterable, List, Optional, TextIO


def has_capitals(values: List[str]) -> bool:
    return any(v.isupper() for v in values)


def has_numerals(values: List[str]) -> bool:
    return any(v.isdigit() for v in values)


def has_symbols(values: List[str]) -> bool:
    return any(v in string.punctuation for v in values)


def generate_password(
    length: int,
    numerals: Optional[bool] = None,
    capitalize: Optional[bool] = None,
    symbols: bool = False,
) -> str:
    """Return one password of specified `length` possibly excluding/including
    character types matching keyword arguments.

    `numerals` (resp. `capitalize`) control whether produced password must
    (True value), may (None value) or must not (False value) contain numerals
    (resp. capital letters).

    `symbols` controls whether the password must contain at least one special
    character.
    """
    if capitalize is False:
        chars = string.ascii_lowercase
    else:
        chars = string.ascii_letters
    if numerals is not False:
        chars += string.digits
    if symbols:
        chars += string.punctuation
    while True:
        elements = [secrets.choice(chars) for _ in range(length)]
        if (not capitalize or (capitalize and has_capitals(elements))) and (
            not numerals
            or (numerals and has_numerals(elements))
            and (not symbols or has_symbols(elements))
        ):
            return "".join(elements)


def write_columns(values: Iterable[str], output: TextIO, item_length: int) -> None:
    """Write `values` to `output` stream in columns."""
    values_per_line = max(80 // (item_length + 1), 1)
    line = []
    for i, value in enumerate(values, 1):
        line.append(value)
        if i % values_per_line == 0:
            output.write(" ".join(line) + "\n")
            line = []
    if line:
        output.write(" ".join(line) + "\n")


def is_interactive():
    return sys.stdout.isatty()


class NumPwAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            if not is_interactive():
                values = 1
            else:
                # 20 lines of 8 values
                values = 20 * 8
        setattr(namespace, self.dest, values)


def get_parser() -> argparse.ArgumentParser:
    prog = "pywgen"
    parser = argparse.ArgumentParser(
        prog, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    dist = pkg_resources.get_distribution(prog)
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {dist.version}"
    )
    parser.add_argument(
        "pw_length", help="password length", nargs="?", type=int, default=8
    )
    parser.add_argument(
        "num_pw",
        help="number of passwords to generate",
        nargs="?",
        type=int,
        action=NumPwAction,
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
    columns_group = parser.add_mutually_exclusive_group()
    columns_group.add_argument(
        "-C",
        help=(
            "print the generated password in columns;"
            " this is the default if standard output is a TTY device"
        ),
        action="store_true",
        dest="columns",
        default=is_interactive(),
    )
    columns_group.add_argument(
        "-1",
        help="print the generated passwords one per line",
        action="store_false",
        dest="columns",
        default=is_interactive(),
    )
    parser.add_argument(
        "-y",
        "--symbols",
        help="include at least one special character in the password",
        action="store_true",
        default=False,
    )
    return parser


def main(argv: List[str] = None) -> None:
    parser = get_parser()
    ns = parser.parse_args(argv)
    args = vars(ns)
    pw_length, num_pw = args.pop("pw_length"), args.pop("num_pw")
    columns = args.pop("columns")
    passwords = (generate_password(pw_length, **args) for _ in range(num_pw))
    if columns:
        write_columns(passwords, sys.stdout, pw_length)
    else:
        sys.stdout.write("\n".join(passwords))


if __name__ == "__main__":
    main()
