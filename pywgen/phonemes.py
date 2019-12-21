import enum
from typing import Tuple


class Phoneme(enum.Flag):
    CONSONANT = enum.auto()
    VOWEL = enum.auto()


Phonemes = Tuple[Tuple[str, Phoneme], ...]


PHONEMES: Phonemes = (
    ("a", Phoneme.VOWEL),
    ("ae", Phoneme.VOWEL),
    ("ai", Phoneme.VOWEL),
    ("au", Phoneme.VOWEL),
    ("b", Phoneme.CONSONANT),
    ("c", Phoneme.CONSONANT),
    ("d", Phoneme.CONSONANT),
    ("e", Phoneme.VOWEL),
    ("ei", Phoneme.VOWEL),
    ("eu", Phoneme.VOWEL),
    ("f", Phoneme.CONSONANT),
    ("g", Phoneme.CONSONANT),
    ("h", Phoneme.CONSONANT),
    ("i", Phoneme.VOWEL),
    ("j", Phoneme.CONSONANT),
    ("k", Phoneme.CONSONANT),
    ("l", Phoneme.CONSONANT),
    ("m", Phoneme.CONSONANT),
    ("n", Phoneme.CONSONANT),
    ("o", Phoneme.VOWEL),
    ("oe", Phoneme.VOWEL),
    ("oi", Phoneme.VOWEL),
    ("p", Phoneme.CONSONANT),
    ("q", Phoneme.CONSONANT),
    ("r", Phoneme.CONSONANT),
    ("s", Phoneme.CONSONANT),
    ("t", Phoneme.CONSONANT),
    ("u", Phoneme.VOWEL),
    ("ui", Phoneme.VOWEL),
    ("v", Phoneme.CONSONANT),
    ("w", Phoneme.CONSONANT),
    ("x", Phoneme.CONSONANT),
    ("y", Phoneme.CONSONANT),
    ("z", Phoneme.CONSONANT),
)

PHONEMES_WITH_CAPITALS: Phonemes = PHONEMES + tuple(
    (ph.upper(), phtype) for ph, phtype in PHONEMES
)
