import re
from unittest.mock import patch

import pytest

from pywgen import generate_password, get_parser, has_capitals, has_numerals


@pytest.mark.parametrize(["value", "result"], [("Ab6", True), ("123rt", False)])
def test_has_capitals(value, result):
    values = list(value)
    assert has_capitals(values) == result


@pytest.mark.parametrize(["value", "result"], [("e73", True), ("azerty", False)])
def test_has_numerals(value, result):
    values = list(value)
    assert has_numerals(values) == result


@pytest.mark.parametrize(
    ["length", "options", "pattern"],
    [
        (8, {}, r"[a-zA-Z0-9]{8}"),
        (2, {"numerals": False}, r"[a-zA-Z]{2}"),
        (10, {"numerals": True}, r"[0-9]+[a-zA-Z]+|[a-zA-Z]+[0-9]+"),
        (7, {"capitalize": None}, r"[A-Za-z0-9]{7}"),
        (5, {"capitalize": False}, r"[a-z0-9]{5}"),
        (10, {"capitalize": True}, r"[A-Z]+[a-z0-9]+|[a-z0-9]+[A-Z]+"),
    ],
)
def test_generate_password_produces_expected_characters(length, options, pattern):
    pw = generate_password(length, **options)
    assert re.match(pattern, pw)


def test_generate_password_calls_secrets_choice():
    with patch("secrets.choice", return_value="a") as patched:
        pw = generate_password(2)
    assert patched.call_count == 2
    assert pw == "aa"


@pytest.mark.parametrize(
    ["argv", "expected"],
    [
        ("", {"numerals": None, "capitalize": None}),
        ("-n", {"numerals": True, "capitalize": None}),
        ("-0 -A", {"numerals": False, "capitalize": False}),
        ("-c", {"numerals": None, "capitalize": True}),
    ],
)
def test_parser(argv, expected):
    parser = get_parser()
    args = parser.parse_args(argv.split())
    assert vars(args) == expected


@pytest.mark.parametrize("argv", [["-Ac"], ["-n", "-0"]])
def test_parser_exclusive_options(argv):
    parser = get_parser()
    with pytest.raises(SystemExit, match="2"):
        parser.parse_args(argv)
