#!/usr/bin/env python3
"""Ancient Greek text: turning SPIonic back into polytonic Greek.

    python3 scripts/markbank/authoring/agr_text.py --audit
    python3 scripts/markbank/authoring/agr_text.py 2015 hl --pages 3

Why this file exists
--------------------
Every Ancient Greek paper and scheme from 2010 to 2022 sets its Greek in
**SPIonic**, a pre-Unicode 8-bit TrueType font, and embeds it with
`WinAnsiEncoding` and no ToUnicode CMap. So the PDF text layer hands back the
Latin-1 bytes rather than the Greek they draw:

    h]n de/ tij ... ce/noj w@n a)rxai=oj:      is    ἦν δέ τις ... ξένος ὢν ἀρχαῖος·

Counted: **0 Greek characters** come out of the text layer of any paper before
2023, against 4,327 out of the 2023 Higher paper, which the SEC finally set in
Unicode. Left alone, that costs the whole of Question 1 Section B (a
comprehension whose passage IS the ask) and every grammar and scansion part
that quotes the passage, in thirteen of the sixteen sittings the corpus holds
a marking scheme for.

How the map was settled — not by squinting at an encoding chart
---------------------------------------------------------------
`derive_glyphs.py` cannot help here: it learns a glyph id from a PDF where the
ToUnicode happens to be right, and there is no such PDF — SPIonic is wrong
everywhere it appears. So the map was built the way GLYPH REPAIR is supposed to
be built when derivation is impossible: the font was extracted out of the PDF,
every one of its glyphs rendered at 110pt over an alpha, and **looked at**.

That settles the letters and the single marks outright. It does NOT settle the
seven COMPOSITE marks — a breathing and an accent drawn as one glyph — because
smooth-plus-acute and rough-plus-acute differ only in which way a 2mm comma
curls. Each of those was instead pinned against a word the corpus actually
prints, where Greek's own orthography admits exactly one reading:

    1 !  smooth + acute      "1Adraston"    Ἄδραστον    (Euripides, Supplices)
    2 @  smooth + grave      "h2 me/nein"   ἢ μένειν    (ἤ always takes psili)
    3 #  rough  + acute      "3Ektora"      Ἕκτορα      (Ἕκτωρ always dasia)
    4 $  rough  + grave      "h4n e0pinoei="  ἣν ἐπινοεῖ  (relative ἥν, dasia)
    5 %  dieresis + acute    "Danai%dai"    Δαναΐδαι
    6    dieresis + grave    "Dii6 fi/le"   Διῒ φίλε
    ] }  smooth + circumflex "h]n", "w} fi/loi"   ἦν, ὦ φίλοι
    [ {  rough  + circumflex  (the pair ] } is smooth, so [ { is the other)

A mark sits AFTER its vowel for lower case and BEFORE it for capitals, which is
how SPIonic gets a breathing to the left of a capital: "3Ektora" is Ἕκτορα, not
Ε-then-a-loose-mark.

The gates
---------
`--audit` runs three checks over every decoded run in the corpus and refuses to
be trusted without them, because a wrong accent silently changes a word:

  1. **residue** — every byte the corpus prints in a SPIonic span is in the
     map. An unmapped byte is reported, never guessed at and never dropped.
  2. **grave position** — in Greek a grave accent occurs only on the LAST
     syllable of a word. If acute and grave were swapped anywhere in the map
     this count would explode; it is the one check that distinguishes them
     without reading the glyph.
  3. **breathing position** — a breathing occurs on a word's first vowel (or
     on the second of an initial diphthong) and nowhere else. A composite mark
     read as the wrong kind of thing shows up here.

Every decoded character is normalised to NFC, so a card carries precomposed
polytonic Greek (ἦν, one code point per letter) rather than a base plus
combining marks that a phone may render as a tower.
"""
import argparse
import collections
import glob
import os
import re
import sys
import unicodedata

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

FONT = 'SPIonic'

# Letters. Read off the rendered glyph sheet; the lower-case run is the plain
# Greek keyboard order and the capitals follow it exactly (c/C = xi, q/Q =
# theta, u/U = upsilon, w/W = omega, y/Y = psi).
LETTERS = {
    'a': 'α', 'b': 'β', 'c': 'ξ', 'd': 'δ', 'e': 'ε', 'f': 'φ', 'g': 'γ',
    'h': 'η', 'i': 'ι', 'j': 'ς', 'k': 'κ', 'l': 'λ', 'm': 'μ', 'n': 'ν',
    'o': 'ο', 'p': 'π', 'q': 'θ', 'r': 'ρ', 's': 'σ', 't': 'τ', 'u': 'υ',
    # 'v' is a variant nu the SEC's typist reaches for by accident: the corpus
    # prints it twice, in "pa/vtej" (πάντες) and "a1nqrwpov" (ἄνθρωπον), and
    # both read as nu and neither reads as anything else.
    'v': 'ν',
    'w': 'ω', 'x': 'χ', 'y': 'ψ', 'z': 'ζ',
    'A': 'Α', 'B': 'Β', 'C': 'Ξ', 'D': 'Δ', 'E': 'Ε', 'F': 'Φ', 'G': 'Γ',
    'H': 'Η', 'I': 'Ι', 'K': 'Κ', 'L': 'Λ', 'M': 'Μ', 'N': 'Ν', 'O': 'Ο',
    'P': 'Π', 'Q': 'Θ', 'R': 'Ρ', 'S': 'Σ', 'T': 'Τ', 'U': 'Υ', 'W': 'Ω',
    'X': 'Χ', 'Z': 'Ζ',
}

SMOOTH, ROUGH = '̓', '̔'
ACUTE, GRAVE, CIRC = '́', '̀', '͂'
DIAER, IOTA = '̈', 'ͅ'

# A mark, and the combining characters it stands for, in the order Unicode
# wants them: breathing/dieresis first, then the accent, then iota subscript.
MARKS = {
    ')': (SMOOTH,), '0': (SMOOTH,),
    '(': (ROUGH,), '9': (ROUGH,),
    '/': (ACUTE,), '&': (ACUTE,),
    '\\': (GRAVE,), '_': (GRAVE,),
    '=': (CIRC,), '~': (CIRC,),
    '+': (DIAER,),
    '|': (IOTA,),
    '!': (SMOOTH, ACUTE), '1': (SMOOTH, ACUTE),
    '@': (SMOOTH, GRAVE), '2': (SMOOTH, GRAVE),
    '#': (ROUGH, ACUTE), '3': (ROUGH, ACUTE),
    '$': (ROUGH, GRAVE), '4': (ROUGH, GRAVE),
    '%': (DIAER, ACUTE), '5': (DIAER, ACUTE),
    '6': (DIAER, GRAVE),
    ']': (SMOOTH, CIRC), '}': (SMOOTH, CIRC),
    '[': (ROUGH, CIRC), '{': (ROUGH, CIRC),
}

# Punctuation, which SPIonic leaves where ASCII put it except for the two Greek
# ones: ';' is the Greek question mark and ':' the ano teleia.
PUNCT = {
    ' ': ' ', ',': ',', '.': '.', '-': '-',
    ';': ';',           # U+037E GREEK QUESTION MARK
    ':': '·',      # ano teleia
    "'": '’', '\x1f': '’',   # elision
    '’': '’', '‘': '’', '\t': ' ',
}

VOWELS = 'αεηιουωΑΕΗΙΟΥΩ'
BREATHINGS = (SMOOTH, ROUGH)


def decode(s):
    """One SPIonic run -> polytonic Greek, NFC-normalised.

    A mark binds to the letter BEFORE it, except before a capital, where
    SPIonic puts the mark first so it can be drawn to the capital's left.
    """
    out = []
    pending = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in MARKS:
            nxt = s[i + 1] if i + 1 < len(s) else ''
            if nxt in LETTERS and nxt.isupper():
                pending.extend(MARKS[ch])
            elif out and out[-1][0] in VOWELS or (out and out[-1][0] == 'ρ'):
                out[-1] = out[-1] + ''.join(MARKS[ch])
            else:
                # A breathing standing on its own: poetic elision writes
                # "’camarta/nein" for ᾿ξαμαρτάνειν. Keep the mark, spacing.
                out.append(_spacing(MARKS[ch]))
        elif ch in LETTERS:
            out.append(LETTERS[ch] + ''.join(pending))
            pending = []
        elif ch in PUNCT:
            out.append(PUNCT[ch])
        else:
            out.append(ch)
        i += 1
    return unicodedata.normalize('NFC', ''.join(_order(t) for t in out))


def _order(tok):
    """base + marks, with the marks in canonical order."""
    if len(tok) < 2:
        return tok
    base, marks = tok[0], tok[1:]
    rank = {SMOOTH: 0, ROUGH: 0, DIAER: 0, ACUTE: 1, GRAVE: 1, CIRC: 1,
            IOTA: 2}
    return base + ''.join(sorted(marks, key=lambda m: rank.get(m, 3)))


_SPACING = {(SMOOTH,): '᾿', (ROUGH,): '῾', (ACUTE,): '´',
            (GRAVE,): '`', (CIRC,): '῀'}


def _spacing(marks):
    return _SPACING.get(tuple(marks), ''.join(marks))


def runs(page):
    """Every SPIonic span on the page, decoded, keyed by its line."""
    out = []
    for block in page.get_text('dict')['blocks']:
        if block.get('type'):
            continue
        for line in block['lines']:
            for span in line['spans']:
                if FONT in span['font']:
                    out.append((span['bbox'], span['text']))
    return out


def page_text(page):
    """The page's text with every SPIonic span decoded in place.

    pymupdf's plain get_text() has already thrown the font away, so the page is
    rebuilt span by span: a run in SPIonic is decoded, everything else is left
    exactly as the extractor gave it.
    """
    lines = []
    for block in sorted(page.get_text('dict')['blocks'],
                        key=lambda b: (round(b['bbox'][1]), b['bbox'][0])):
        if block.get('type'):
            continue
        for line in block['lines']:
            parts = []
            for span in line['spans']:
                t = span['text']
                parts.append(decode(t) if FONT in span['font'] else t)
            lines.append(''.join(parts))
    return '\n'.join(lines)


def has_spionic(doc):
    return any(FONT in f[3] for page in doc for f in page.get_fonts(full=True))


# ---------------------------------------------------------------- the gates

WORD = re.compile(r'[Ͱ-Ͽἀ-῿]+')


def _syllables(word):
    """Vowel groups, left to right. A diphthong counts once."""
    d = unicodedata.normalize('NFD', word)
    out, i = [], 0
    base = [c for c in d if not unicodedata.combining(c)]
    del base
    while i < len(d):
        if d[i] in VOWELS:
            j = i + 1
            while j < len(d) and unicodedata.combining(d[j]):
                j += 1
            # a following vowel with no mark of its own may be a diphthong
            if j < len(d) and d[j] in 'ιυΙΥ':
                k = j + 1
                while k < len(d) and unicodedata.combining(d[k]):
                    k += 1
                j = k
            out.append(d[i:j])
            i = j
        else:
            i += 1
    return out


def audit(paths=None):
    """residue, grave position, breathing position — over the whole corpus."""
    paths = paths or sorted(glob.glob(
        os.path.join(ROOT, 'examiner-reports', 'ancient-greek', '*', '*.pdf')))
    residue = collections.Counter()
    words = 0
    bad_grave, bad_breath = [], []
    for path in paths:
        doc = pymupdf.open(path)
        for page in doc:
            for _bbox, raw in runs(page):
                for ch in raw:
                    if ch not in LETTERS and ch not in MARKS \
                            and ch not in PUNCT:
                        residue[ch] += 1
                for word in WORD.findall(decode(raw)):
                    words += 1
                    syls = _syllables(word)
                    for n, syl in enumerate(syls):
                        d = unicodedata.normalize('NFD', syl)
                        if GRAVE in d and n != len(syls) - 1:
                            bad_grave.append((os.path.basename(path), word))
                        if any(b in d for b in BREATHINGS) and n != 0:
                            bad_breath.append((os.path.basename(path), word))
        doc.close()
    return {'words': words, 'residue': residue,
            'graveOffFinal': bad_grave, 'breathingOffFirst': bad_breath}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--pages', type=int, default=0)
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()
    if args.audit:
        r = audit()
        print(f"{r['words']} Greek words decoded")
        print(f"  residue        : {sum(r['residue'].values())} "
              f"({', '.join(repr(c) for c in r['residue']) or 'none'})")
        for name, rows in (('grave off final syllable', r['graveOffFinal']),
                           ('breathing off first vowel',
                            r['breathingOffFirst'])):
            print(f'  {name:<24}: {len(rows)}'
                  f" ({100 * len(rows) / max(r['words'], 1):.2f}%)")
            for f, w in rows[:6]:
                print(f'      {f} {w}')
        return 0 if not r['residue'] else 1
    doc = pymupdf.open(os.path.join(
        ROOT, 'examiner-reports', 'ancient-greek', 'papers',
        f'{args.year}-{args.level}-paper.pdf'))
    for n, page in enumerate(doc, 1):
        if args.pages and n != args.pages:
            continue
        print(f'--- page {n} ---')
        print(page_text(page))
    return 0


if __name__ == '__main__':
    sys.exit(main())
