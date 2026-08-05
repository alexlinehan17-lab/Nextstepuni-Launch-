"""
Mark Bank — text repairs shared by every SEC PDF reader here.

Kept in its own module because the scripts that need it are named with hyphens
and cannot import one another. A second copy of this map would drift, and the
damage it undoes is invisible in a diff: "reacƟon" reads as "reaction" to a
human skimming, so a corrupted string survives review and lands in a card.
"""

# Some SEC PDFs embed a subsetted font whose LIGATURE glyphs carry no sensible
# Unicode mapping, so an extractor faithfully reports the wrong codepoint. The
# 2024 Chemistry Ordinary scheme came out with 213 instances of "Ɵ" standing for
# "ti" — "unsaturaƟon", "addiƟon reacƟon", "separaƟon" — plus 73 f-ligatures.
LIGATURES = {
    "Ɵ": "ti",   # Ɵ  LATIN CAPITAL LETTER O WITH MIDDLE TILDE
    "Ŧ": "ti",   # Ŧ
    "Ʃ": "tt",   # Ʃ  LATIN CAPITAL LETTER ESH — "leƩers", "ploƩed", "BeƩer"
    "ﬀ": "ff",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
    "ﬅ": "st",
    "ﬆ": "st",
    # Symbol-font glyphs in the private-use area, read from where they appear:
    # U+F0B7 opens every bullet in "How to use the marking scheme", and U+F0FC is
    # the tick the scheme's own Annotation table glosses as "a correct response".
    "": "•",
    "": "✓",
}


def unligature(text: str) -> str:
    """Restore ligature glyphs that the PDF's font encoding mangled."""
    for bad, good in LIGATURES.items():
        text = text.replace(bad, good)
    return text
