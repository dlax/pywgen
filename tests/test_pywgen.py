import re
from unittest.mock import patch

from pywgen import generate_password


def test_generate_password_produces_expected_characters():
    pw = generate_password(8)
    assert re.match(r"[a-zA-Z0-9]{8}", pw)


def test_generate_password_calls_secrets_choice():
    with patch("secrets.choice", return_value="a") as patched:
        pw = generate_password(2)
    assert patched.call_count == 2
    assert pw == "aa"
