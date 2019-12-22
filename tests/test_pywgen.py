import io
import os.path
import re
import string
from unittest.mock import patch

import pytest

from pywgen import (
    check_password,
    generate_password,
    generate_pronounceable_password,
    get_parser,
    has_capitals,
    has_numerals,
    has_symbols,
    is_interactive,
    main,
    pronounceable_choice,
    write_columns,
)
from pywgen.phonemes import (
    NUMERAL_PHONEMES,
    Phoneme,
    PHONEMES,
    PHONEMES_WITH_CAPITALS,
    PUNCTUATION_PHONEMES,
)


def datapath(*p):
    return os.path.join(os.path.dirname(__file__), "data", *p)


def test_phonemes():
    assert Phoneme.VOWEL & Phoneme.VOWEL
    assert Phoneme.CONSONANT & Phoneme.CONSONANT
    assert not (Phoneme.VOWEL & Phoneme.CONSONANT)
    # 0 does not combine with any others
    assert not any(Phoneme(0) & p for p in Phoneme)


def test_phonemes_contains_all_letters():
    letters = set(string.ascii_lowercase)
    phonemes_letters = set(s for s, _ in PHONEMES)
    assert not letters - phonemes_letters


@pytest.mark.parametrize(["value", "result"], [("Ab6", True), ("123rt", False)])
def test_has_capitals(value, result):
    values = list(value)
    assert has_capitals(values) == result


@pytest.mark.parametrize(["value", "result"], [("e73", True), ("azerty", False)])
def test_has_numerals(value, result):
    values = list(value)
    assert has_numerals(values) == result


@pytest.mark.parametrize(["value", "result"], [("b!z6", True), ("4gt", False)])
def test_has_symbols(value, result):
    values = list(value)
    assert has_symbols(values) == result


@pytest.mark.parametrize(
    ["value", "capitalize", "numerals", "symbols", "expected"],
    [
        ("abc", True, None, None, False),
        ("A!2", True, None, None, True),
        ("A!2", False, None, None, False),
        ("abc", None, True, None, False),
        ("A!2", None, True, None, True),
        ("A!2", None, False, None, False),
        ("abc", None, None, True, False),
        ("A!2", None, None, True, True),
        ("A!2", None, None, False, False),
    ],
)
def test_check_password(value, capitalize, numerals, symbols, expected):
    assert check_password(value, capitalize, numerals, symbols) == expected


@pytest.mark.parametrize(
    ["length", "options", "pattern"],
    [
        (8, {}, r"[a-zA-Z0-9]{8}"),
        (2, {"numerals": False}, r"[a-zA-Z]{2}"),
        (10, {"numerals": True}, r"[0-9]+[a-zA-Z]+|[a-zA-Z]+[0-9]+"),
        (7, {"capitalize": None}, r"[A-Za-z0-9]{7}"),
        (5, {"capitalize": False}, r"[a-z0-9]{5}"),
        (10, {"capitalize": True}, r"[A-Z]+[a-z0-9]+|[a-z0-9]+[A-Z]+"),
        (5, {"symbols": True}, r".*[^A-Za-z0-9]+.*"),
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
    ["phonemes", "expected"],
    [
        ([("a", Phoneme.VOWEL), ("e", Phoneme.VOWEL), ("x", Phoneme.CONSONANT)], "ax",),
        ([("b", Phoneme.CONSONANT), ("a", Phoneme.VOWEL)], "ba"),
        (
            [("au", Phoneme.VOWEL), ("e", Phoneme.VOWEL), ("x", Phoneme.CONSONANT)],
            "aux",
        ),
    ],
)
def test_pronounceable_choice(phonemes, expected):
    with patch("secrets.choice", new=next):
        gen = pronounceable_choice(iter(phonemes))
        choice = ""
        while len(choice) < len(expected):
            choice += next(gen)
    assert choice == expected


@pytest.mark.parametrize(
    ["options", "choice", "phonemes", "expected"],
    [
        (
            {"capitalize": None, "numerals": None, "symbols": True},
            ["a", "B", "3", "de", "!"],
            PHONEMES_WITH_CAPITALS + NUMERAL_PHONEMES + PUNCTUATION_PHONEMES,
            "aB3!",
        ),
        (
            {"capitalize": False, "numerals": True, "symbols": False},
            ["a", "b", "!", "de", "T", "f", "7", "u", "z", "#"],
            PHONEMES + NUMERAL_PHONEMES,
            "f7uz",
        ),
        (
            {"capitalize": False, "numerals": None, "symbols": True},
            ["a", "b", "!", "de", "f", "7", "?", "x", "y"],
            PHONEMES + NUMERAL_PHONEMES + PUNCTUATION_PHONEMES,
            "ab!f",
        ),
        (
            {"capitalize": True, "numerals": True, "symbols": True},
            ["a", "b", "!", "de", "f", "7", "?", "x", "yz", "AB", "C"],
            PHONEMES_WITH_CAPITALS + NUMERAL_PHONEMES + PUNCTUATION_PHONEMES,
            "7?xC",
        ),
    ],
)
def test_generate_pronounceable_password(options, choice, phonemes, expected):
    with patch("pywgen.pronounceable_choice", return_value=iter(choice)) as patched:
        pw = generate_pronounceable_password(4, **options)
    patched.assert_called_once_with(phonemes)
    assert pw == expected


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
                "secure": False,
                "symbols": False,
            },
        ),
        (
            "7 --symbols",
            {
                "pw_length": 7,
                "num_pw": 1,
                "numerals": None,
                "capitalize": None,
                "columns": False,
                "secure": False,
                "symbols": True,
            },
        ),
        (
            "2 9 -y -s",
            {
                "pw_length": 2,
                "num_pw": 9,
                "numerals": None,
                "capitalize": None,
                "columns": False,
                "secure": True,
                "symbols": True,
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
                "secure": False,
                "symbols": False,
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
                "secure": False,
                "symbols": False,
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
                "secure": False,
                "symbols": False,
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

    with capsys.disabled():
        parser = get_parser()
        args = parser.parse_args(["-1", "8", "3"])
    assert args.num_pw == 3
    assert args.columns is False


@pytest.mark.parametrize("argv", [["-Ac"], ["-n", "-0"]])
def test_parser_exclusive_options(argv):
    parser = get_parser()
    with pytest.raises(SystemExit, match="2"):
        parser.parse_args(argv)


def test_main(capsys):
    with patch("pywgen.generate_pronounceable_password", return_value="xyz") as patched:
        main([])
    patched.assert_called_once_with(8, capitalize=None, numerals=None, symbols=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "xyz"


def test_main_columns(capsys):
    with patch("pywgen.generate_password", return_value="abc") as patched:
        main(["-C", "3", "40", "-y", "-s"])
    patched.assert_called_with(3, capitalize=None, numerals=None, symbols=True)
    assert patched.call_count == 40
    captured = capsys.readouterr()
    with open(datapath("abc40.txt")) as f:
        expected = f.read()
    assert captured.err == ""
    assert captured.out == expected
