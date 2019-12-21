import re
from unittest.mock import patch

import pytest

from pywgen import generate_password


@pytest.mark.parametrize(
    ["length", "options", "pattern"],
    [(8, {}, r"[a-zA-Z0-9]{8}"), (2, {"numerals": False}, r"[a-zA-Z]{2}")],
)
def test_generate_password_produces_expected_characters(length, options, pattern):
    pw = generate_password(length, **options)
    assert re.match(pattern, pw)


def test_generate_password_calls_secrets_choice():
    with patch("secrets.choice", return_value="a") as patched:
        pw = generate_password(2)
    assert patched.call_count == 2
    assert pw == "aa"
