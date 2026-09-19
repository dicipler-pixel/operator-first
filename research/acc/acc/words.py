"""Exact word and presentation arithmetic for Andrews-Curtis search.

Letters are signed integers: 1 = x, -1 = x^-1, 2 = y, -2 = y^-1, and so on
for higher-rank (Stable AC) generators.  A word is a tuple of letters.  A
presentation is a tuple of words, one per relator.

Nothing here prunes or scores.  This module is an exact checker only.
"""

from __future__ import annotations

from typing import Iterable, Sequence, Tuple

Word = Tuple[int, ...]
Presentation = Tuple[Word, ...]

LETTER_TO_CODE = {"x": 1, "X": -1, "y": 2, "Y": -2}
CODE_TO_LETTER = {1: "x", -1: "X", 2: "y", -2: "Y"}
DIGIT_TO_CODE = {"0": 1, "1": 2, "2": -1, "3": -2}
CODE_TO_DIGIT = {1: "0", 2: "1", -1: "2", -2: "3"}


def parse_word(text: str) -> Word:
    """Parse a word in either the letter encoding or the digit encoding.

    Letter encoding: x, y are generators; X, Y are their inverses.
    Digit encoding: 0=x, 1=y, 2=x^-1, 3=y^-1.
    Rank > 2 uses the explicit ``g<k>`` / ``G<k>`` form, space separated.
    """
    text = text.strip()
    if not text:
        return ()
    if text[0] in "gG" and any(ch.isdigit() for ch in text):
        out = []
        for token in text.split():
            sign = 1 if token[0] == "g" else -1
            out.append(sign * int(token[1:]))
        return tuple(out)
    if all(ch in LETTER_TO_CODE for ch in text):
        return tuple(LETTER_TO_CODE[ch] for ch in text)
    if all(ch in DIGIT_TO_CODE for ch in text):
        return tuple(DIGIT_TO_CODE[ch] for ch in text)
    raise ValueError(f"unrecognised word encoding: {text!r}")


def format_word(word: Sequence[int], style: str = "letter") -> str:
    if style == "letter":
        if all(abs(c) <= 2 for c in word):
            return "".join(CODE_TO_LETTER[c] for c in word)
        style = "generator"
    if style == "digit":
        return "".join(CODE_TO_DIGIT[c] for c in word)
    return " ".join(("g" if c > 0 else "G") + str(abs(c)) for c in word)


def parse_presentation(text: str) -> Presentation:
    """Parse ``r1 / r2`` (the handoff's notation) into a presentation."""
    parts = [p for p in text.replace(",", "/").split("/")]
    return tuple(parse_word(p) for p in parts if p.strip())


def format_presentation(pres: Presentation, style: str = "letter") -> str:
    return " / ".join(format_word(w, style) for w in pres)


def free_reduce(word: Iterable[int]) -> Word:
    """Cancel adjacent inverse pairs.  This is the exact state normal form."""
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def cyclic_reduce(word: Word) -> Word:
    """Free-reduce, then strip cancelling first/last letters."""
    word = free_reduce(word)
    lo, hi = 0, len(word)
    while hi - lo >= 2 and word[lo] == -word[hi - 1]:
        lo += 1
        hi -= 1
    return word[lo:hi]


def inverse(word: Word) -> Word:
    return tuple(-c for c in reversed(word))


def rotations(word: Word) -> list[Word]:
    n = len(word)
    if n == 0:
        return [()]
    return [word[i:] + word[:i] for i in range(n)]


def total_length(pres: Presentation) -> int:
    return sum(len(w) for w in pres)


def relator_lengths(pres: Presentation) -> Tuple[int, ...]:
    return tuple(len(w) for w in pres)


def cyclic_canonical(word: Word) -> Word:
    """Least representative of a relator under rotation and inversion."""
    core = cyclic_reduce(word)
    if not core:
        return ()
    candidates = rotations(core) + rotations(inverse(core))
    return min(candidates)


def normalize_ordinary(pres: Presentation) -> Presentation:
    """The handoff's 'ordinary cyclic/inversion-normalized representative'.

    Quotients by: cyclic rotation of each relator, inversion of each relator,
    and reordering of the relators.  Used only for counting and contracting
    boundaries -- never as the state key of an exact search.
    """
    return tuple(sorted(cyclic_canonical(w) for w in pres))


def exponent_sums(pres: Presentation, rank: int = 2) -> Tuple[Tuple[int, ...], ...]:
    rows = []
    for word in pres:
        row = [0] * rank
        for letter in word:
            idx = abs(letter) - 1
            if idx < rank:
                row[idx] += 1 if letter > 0 else -1
        rows.append(tuple(row))
    return tuple(rows)


def abelianized_determinant(pres: Presentation) -> int:
    """det of the 2x2 exponent-sum matrix.  An AC invariant: stays +-1."""
    if len(pres) != 2:
        raise ValueError("determinant is defined here for rank-2 presentations")
    (a, b), (c, d) = exponent_sums(pres, rank=2)
    return a * d - b * c


def encode_state(pres: Presentation) -> bytes:
    """Compact exact key.  Distinct presentations get distinct keys."""
    parts = []
    for word in pres:
        parts.append(bytes((c + 128) & 0xFF for c in word))
    return b"\x00".join(parts)


def decode_state(key: bytes) -> Presentation:
    out = []
    for chunk in key.split(b"\x00"):
        out.append(tuple((b - 128) if b >= 128 else (b + 128) - 256 for b in chunk))
    return tuple(out)
