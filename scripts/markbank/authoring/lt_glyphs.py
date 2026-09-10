#!/usr/bin/env python3
"""Derive the Baltic schemes' mangled-glyph repair map from the corpus itself.

    python3 scripts/markbank/authoring/lt_glyphs.py lithuanian [--write]

Why this exists beside derive_glyphs.py
---------------------------------------
`derive_glyphs.py` learns a glyph id's real character from a PDF where the same
FONT's ToUnicode happens to be right, and applies it where it is wrong. That
works across a corpus that shares fonts. It cannot reach these files: the 2015
Lithuanian scheme embeds a subset nothing else in the bank uses, so there is no
clean sighting of its glyph ids anywhere, and a run over the subject repaired
four per cent of what it found.

What IS available is the LANGUAGE. Twenty-two Lithuanian schemes and thirty-two
papers are set in the same vocabulary, and all but two of them are clean, so a
word from a mangled file can be checked against the words the clean files
print. The map is then derived by evidence rather than by hand: for each
mangled character, every Lithuanian letter is tried in its place and the one
that turns the most distinct mangled words into words the clean corpus prints
wins. "žodžiǐ" is not a word and "žodžių" is, in fifty other places, so ǐ is ų;
nothing about that is a guess about a font.

Two files need it and they are mangled differently:

    2011  paper and scheme       ţ  ->  ž           (one character)
    2015  scheme only            Ƴ  ->  į,  ǐ -> ų,  ơ -> ė,  Ċ -> ę,
                                 ǌ  ->  ū,  þ -> č,  and the rest below

and 2015 matters twice over, because the GLOBAL glyphmap.json — derived from
Maths and Chemistry — already maps 'ơ' to "l". Left to that map a Lithuanian
card would read "Baidykll, šmlkla" for "Baidyklė, šmėkla" and pass every gate,
because build-deck's own broken-glyph test only sees characters no map claims.
A subject map that is applied BEFORE anything reaches a card is what keeps that
from happening; `--write` puts it in glyphmap-<subject>.json, which lt_paper,
lt_scheme and extract-scheme.py all read.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

# The letters the three languages are actually set in. Everything else in the
# Latin Extended blocks is a subset font's muddle.
ALPHABETS = {
    'lithuanian': 'aąbcčdeęėfghiįyjklmnoprsštuųūvzž',
    'latvian': 'aābcčdeēfgģhiījkķlļmnņoprsštuūvzž',
    'czech': 'aábcčdďeéěfghiíjklmnňoóprřsštťuúůvyýzž',
}
KEEP = set('„“”‘’–—…€°·×•✓‐−’')


# Letters from the Latin-1 range that these documents really do print, in the
# foreign names and words they quote. Everything else in that range is the
# subset font again: the 2015 scheme sets "Plačiąja" as "Plaþiąja", and a
# window that started at U+0100 never saw it.
LATIN1_REAL = set('äöüåæøéèêëáàâíìîóòôúùûñçß'
                  'ÄÖÜÅÆØÉÈÊËÁÀÂÍÌÎÓÒÔÚÙÛÑÇ')


def mangled_chars(text, alphabet):
    out = set()
    for c in text:
        if 0x00C0 <= ord(c) <= 0x024F or 0x02B0 <= ord(c) <= 0x036F:
            if c.lower() not in alphabet and c not in KEEP \
                    and c not in LATIN1_REAL:
                out.add(c)
    return out


WORD = re.compile(r"[^\W\d_]+", re.UNICODE)

# Glyphs the word evidence cannot settle, cropped out of the page at 400dpi and
# LOOKED AT — derive_glyphs.py's rule, and the only way this bank is allowed to
# add a character the corpus does not vote for.
#
#   Ċ  U+010A  2015 Higher scheme, "reikšmĊ" — the crop shows an e with an
#              ogonek under it, so the word is "reikšmę" and Ċ is ę. Ten
#              sightings, all of them the accusative ending -ę.
#   Ţ  U+0162  2011 Higher scheme p4, "Ţmogus turi nuolat saugotis" — the crop
#              shows Ž with its caron, and the same line prints "žalingiems"
#              with the lowercase ţ this map already settles. Two sightings,
#              which is one under the three the vote demands.
#
# U+0336 is deliberately NOT here. It is the SEC's own annotation mark, printed
# once in the front-matter table that glosses it ("Question has not been
# answered"), and it is not a letter of anything — nothing downstream reads
# that table.
VERIFIED = {
    'lithuanian': {
        # Ċ U+010A — 2015 Higher scheme, "reikšmĊ". The crop shows an e with an
        # ogonek under it, so the word is "reikšmę". Ten sightings, all of them
        # the accusative ending -ę.
        '\u010a': 'ę',
        # Ţ U+0162 — 2011 Higher scheme p4, "Ţmogus turi nuolat saugotis". The
        # crop shows Ž with its caron, and the same line prints "žalingiems"
        # with the lowercase ţ this map already settles.
        '\u0162': 'Ž',
    },
    # Latvian's four survivors are settled by the WORD each stands in, which is
    # the same evidence the vote uses and simply has fewer than three examples
    # of. Each was read off the printed line rather than guessed:
    'latvian': {
        '\u01b7': 'ķ',   # "man šƷiet" -> "man šķiet"
        '\u01ae': 'Ī',   # "Ʈpaši" opening a sentence -> "Īpaši"
        '\u019c': 'Ē',   # "4. Ɯtika nespƝj" -> "4. Ētika nespēj"
        '\u01bb': 'Ņ',   # "ƻemot vƝrƗ visu" -> "Ņemot vērā visu"
    },
    'czech': {
        '\u0107': 'ď',   # "Teć už víme" -> "Teď už víme"
        '\u0122': 'ť',   # "šĢastný s málem" -> "šťastný s málem"
    },
}


def corpus(subject):
    files = sorted(glob.glob(os.path.join(
        ROOT, 'examiner-reports', subject, 'schemes', '*.pdf'))
        + glob.glob(os.path.join(
            ROOT, 'examiner-reports', subject, 'papers', '*.pdf')))
    for path in files:
        with pymupdf.open(path) as doc:
            yield path, '\n'.join(page.get_text() for page in doc)


def derive(subject, verbose=True):
    """{mangled character: the character the SEC printed}, from the corpus.

    The evidence is a WORD the clean files print and the mangled file does not.
    For every word carrying a mangled character, the clean vocabulary is
    searched for words of the same length that agree on every character the
    text layer got right; where all of those agree on the letter standing where
    the mangled one is, that letter is one vote. A character is settled at
    three votes with a clear margin over the runner-up, and left out otherwise.

    Voting per POSITION rather than per word is what makes the 2015 scheme
    readable at all: its words carry up to five mangled characters each
    ("žodžiǐ", "reikšmĊ", "medijǐ", "bǌti"), so no single substitution ever
    turns one into a word, and a whole-word test settled nothing. The unknown
    positions are wildcards and each one is read off the match.
    """
    alphabet = ALPHABETS[subject]
    clean = collections.Counter()
    dirty = collections.Counter()
    bad = collections.Counter()
    for _path, text in corpus(subject):
        hits = mangled_chars(text, alphabet)
        for word in WORD.findall(text):
            if len(word) < 3:
                continue
            if hits and mangled_chars(word, alphabet):
                dirty[word] += 1
            else:
                clean[word] += 1
        for c in text:
            if c in hits:
                bad[c] += 1
    by_len = collections.defaultdict(list)
    for word in clean:
        by_len[len(word)].append(word)
    if verbose:
        print(f'{len(clean)} clean word forms, {len(dirty)} words carrying a '
              f'mangled character, {len(bad)} distinct mangled characters')

    table = {}
    for _round in range(6):
        votes = collections.defaultdict(collections.Counter)
        for word in dirty:
            fixed = _apply(word, table)
            unknown = [i for i, c in enumerate(fixed)
                       if mangled_chars(c, alphabet)]
            if not unknown:
                continue
            low = fixed.lower()
            holes = set(unknown)
            matches = [w for w in by_len[len(fixed)]
                       if all(w[i].lower() == low[i]
                              for i in range(len(low)) if i not in holes)]
            if not matches:
                continue
            for i in unknown:
                letters = {w[i] for w in matches}
                if len(letters) == 1:
                    votes[fixed[i]][letters.pop()] += 1
        moved = False
        for ch, counts in votes.items():
            if ch in table:
                continue
            ranked = counts.most_common()
            best, n = ranked[0]
            runner = ranked[1][1] if len(ranked) > 1 else 0
            if n >= 3 and n > runner * 1.5:
                table[ch] = best
                moved = True
                if verbose:
                    print(f'  {ch!r} U+{ord(ch):04X} -> {best!r}  '
                          f'({n} votes, runner-up {runner})')
        if not moved:
            break
    table.update(VERIFIED.get(subject, {}))
    left = [(c, n) for c, n in bad.most_common() if c not in table]
    if verbose and left:
        print('unsettled:', ', '.join(f'{c!r} U+{ord(c):04X} x{n}'
                                      for c, n in left[:20]))
    return table, left


def _apply(text, table):
    return ''.join(table.get(c, c) for c in text)


def repair(text, table):
    return _apply(text, table)


def load(subject):
    path = os.path.join(HERE, f'glyphmap-{subject}.json')
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject', choices=sorted(ALPHABETS))
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    table, left = derive(args.subject)
    print(f'{len(table)} entry map, {len(left)} character(s) unsettled')
    if args.write:
        path = os.path.join(HERE, f'glyphmap-{args.subject}.json')
        existing = load(args.subject)
        existing.update(table)
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(existing, fh, ensure_ascii=False, indent=0, sort_keys=True)
            fh.write('\n')
        print(f'wrote {path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
