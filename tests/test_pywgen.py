import io
import os.path
import re
from unittest.mock import patch

import pytest

from pywgen import (
    generate_password,
    get_parser,
    has_capitals,
    has_numerals,
    is_interactive,
    main,
    write_columns,
)


def datapath(*p):
    return os.path.join(os.path.dirname(__file__), "data", *p)


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


@pytest.mark.parametrize("num", [40, 37])
def test_write_columns(num):
    output = io.StringIO()
    write_columns(["abc"] * num, output, 3)
    actual = output.getvalue()
    with open(datapath(f"abc{num}.txt")) as f:
        expected = f.read()
    assert actual == expected


def test_write_columns_long():
    # value is longer than line length
    output = io.StringIO()
    write_columns(["a" * 81] * 2, output, 81)
    actual = output.getvalue()
    assert actual == "\n".join("a" * 81 for _ in range(2)) + "\n"


def test_is_interactive(capsys):
    # stdout is captured, hence non-interactive mode
    assert is_interactive() is False
    with capsys.disabled():
        assert is_interactive() is True


@pytest.mark.parametrize(
    ["argv", "expected"],
    [
        (
            "",
            {
                "pw_length": 8,
                "num_pw": 1,
                "numerals": None,
                "capitalize": None,
                "columns": False,
            },
        ),
        (
            "7",
            {
                "pw_length": 7,
                "num_pw": 1,
                "numerals": None,
                "capitalize": None,
                "columns": False,
            },
        ),
        (
            "2 9",
            {
                "pw_length": 2,
                "num_pw": 9,
                "numerals": None,
                "capitalize": None,
                "columns": False,
            },
        ),
        (
            "-n",
            {
                "pw_length": 8,
                "num_pw": 1,
                "numerals": True,
                "capitalize": None,
                "columns": False,
            },
        ),
        (
            "-0 -A -C",
            {
                "pw_length": 8,
                "num_pw": 1,
                "numerals": False,
                "capitalize": False,
                "columns": True,
            },
        ),
        (
            "-c 12 -C",
            {
                "pw_length": 12,
                "num_pw": 1,
                "numerals": None,
                "capitalize": True,
                "columns": True,
            },
        ),
    ],
)
def test_parser(argv, expected):
    parser = get_parser()
    args = parser.parse_args(argv.split())
    assert vars(args) == expected


def test_parser_interactive_num_pw_columns(capsys):
    parser = get_parser()
    args = parser.parse_args(["-C"])
    assert args.num_pw == 1
    assert args.columns is True

    parser = get_parser()
    args = parser.parse_args(["4", "10"])
    assert args.num_pw == 10
    assert args.columns is False

    with capsys.disabled():
        parser = get_parser()
        args = parser.parse_args([])
    assert args.num_pw == 160
    assert args.columns is True


@pytest.mark.parametrize("argv", [["-Ac"], ["-n", "-0"]])
def test_parser_exclusive_options(argv):
    parser = get_parser()
    with pytest.raises(SystemExit, match="2"):
        parser.parse_args(argv)


def test_main(capsys):
    with patch("pywgen.generate_password", return_value="xyz") as patched:
        main([])
    patched.assert_called_once_with(8, capitalize=None, numerals=None)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "xyz"


def test_main_columns(capsys):
    with patch("pywgen.generate_password", return_value="abc") as patched:
        main(["-C", "3", "40"])
    patched.assert_called_with(3, capitalize=None, numerals=None)
    assert patched.call_count == 40
    captured = capsys.readouterr()
    with open(datapath("abc40.txt")) as f:
        expected = f.read()
    assert captured.err == ""
    assert captured.out == expected
