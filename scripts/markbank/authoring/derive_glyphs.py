#!/usr/bin/env python3
"""Derive the mangled-glyph repair map from the scheme PDFs themselves.

Word embeds its fonts as subsets whose ToUnicode CMap is wrong: "tan" comes
out of the text layer as Oriya, "Certificate" as "CerƟficate", and an exponent
as a Tamil letter. Hand-mapping the glyphs one at a time was how this started
and it does not converge -- there were 147 distinct ones across ten Maths
schemes alone, and a wrong guess silently changes what a marking point says.

The glyph id is trustworthy where the ToUnicode is not. PyMuPDF exposes it
through get_texttrace(), and a glyph id means the same character everywhere in
the same font. So: join each drawn glyph to its id by drawing origin, learn
id -> character from every PDF where the ToUnicode happens to be correct, and
apply what was learned to the PDFs where it is not. The map is derived from the
corpus rather than guessed, and re-running this script re-derives it.

    python3 scripts/markbank/authoring/derive_glyphs.py [--write]
"""
import collections
import glob
import json
import os
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'glyphmap.json')

# Greek is really Greek in these schemes; everything else in the range is a
# subset font's private muddle.
def mangled(u):
    return 0x0100 < u < 0x2000 and not (0x0370 <= u < 0x0400)


# Ligatures and PUA marks, which are one glyph standing for more than one
# character -- so they cannot come out of a glyph-id table keyed by character.
LIGATURE = {
    'Ɵ': 'ti', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl',
    'ƫ': 'tt', 'ƞ': 'tf', '\u02da': '\u00b0',   # "pu[tt]ing", "ou[tf]lows", 25[deg]C
    '\uf0ae': '\u2192',   # Symbol font: code point 0xAE is its rightwards arrow
    # Symbol and Wingdings characters, which a PDF stores at 0xF000 + the code
    # point. Each was settled by cropping the glyph out of the page and looking
    # at it rather than by trusting an encoding chart:
    '\uf071': '\u03b8',   # SymbolMT 0x71 -- "values of temperature [theta]"
    '\uf044': '\u0394',   # SymbolMT 0x44 -- "[Delta]H = 206" beside a reaction
    '\uf06c': '\u2022',   # Wingdings 0x6c -- the bullet on "using a scalpel"
    '\uf050': '\u2713',   # Wingdings 2 0x50 -- a tick
    '\uf067': '\u2192',   # Wingdings 3 0x67 -- "6O2 -> 6CO2 + 6H2O"
    '\uf081': '\u2460',   # Wingdings 0x81 -- a circled 1
    '\u0424': '\u03a6',   # renders as Phi: "[Phi] = 4.33 x 10^-19 (J)"
    '\u0278': '\u03c6',   # the same letter lowercase, in the same schemes
    '': ' ', '': '•', '': '•', '': '✓',
    '': '•', '': '-', '': '=',
}


# Glyphs whose id never appears with a sane ToUnicode anywhere in the corpus,
# identified instead by the ids either side of them -- a subset font keeps the
# original font's glyph order, so a glyph's neighbours place it. The evidence
# for each is the neighbour list, recorded here so the call can be re-checked.
NEIGHBOUR = {
    '\u0d6c': '(',   # gid 3436, between 3435='(' and 3439=')': a size variant
    '\u0d70': ')',   # gid 3440, and it closes 3436 in "cos(t + 2npi) + isin(2pi
    '\u0bec': '\U0001d466',  # gid 3052, follows 3051='x': the y of dy/dx
    '\u0da7': '\u221a',  # gid 3495, beside 3493='v': a taller radical
    '\u0db1': '\u222b',  # gid 3505, beside 3493='v' and 3533='S': the integral
    '\u1246': '(',   # gid 4678, in the 4672='(' 4673=')' bracket run
    '\u1247': ')',   # gid 4679, same run
    '\u1242': '[',   # gid 4674, follows 4673=')' -- "75[" ... "+ 5x + C]"
    '\u1243': ']',   # gid 4675 in the same run, closes it
    '\u0c0f': '\U0001d703',  # gid 3087, four before 3091='m' in the Greek run: theta
    '\u014c': 'ft',  # Calibri gid 332, between 327='fl' and 336='g': "aOer"
}


def scan(files):
    """(font, gid) -> Counter(character), and the mangled sightings."""
    seen = collections.defaultdict(collections.Counter)
    bad = collections.Counter()
    for f in files:
        doc = pymupdf.open(f)
        for pno in range(len(doc)):
            origin = {}
            for sp in doc[pno].get_texttrace():
                font = sp.get('font')
                for ch in sp['chars']:
                    origin[(round(ch[2][0], 2), round(ch[2][1], 2))] = (font, ch[1])
            for blk in doc[pno].get_text('rawdict')['blocks']:
                for line in blk.get('lines', []):
                    for sp in line.get('spans', []):
                        for ch in sp['chars']:
                            key = (round(ch['origin'][0], 2), round(ch['origin'][1], 2))
                            if key not in origin:
                                continue
                            font, gid = origin[key]
                            u = ord(ch['c'])
                            if mangled(u):
                                bad[(font, gid, u)] += 1
                            elif u > 32:
                                seen[(font, gid)][ch['c']] += 1
        doc.close()
    return seen, bad


def interpolate(seen):
    """Fill gaps in a glyph-id run whose ends are known and consecutive.

    A subset font lays its glyphs out in the original font's order, so ids
    2868..2877 being '0'..'9' is not a coincidence -- an unseen id inside a
    known arithmetic run is the character the run's step predicts. Only runs
    that already agree on their step are extended, so this adds the '9' nobody
    happened to print and nothing else.
    """
    known = {}
    for (font, gid), counts in seen.items():
        c = max(counts, key=counts.get)
        if len(c) == 1:
            known.setdefault(font, {})[gid] = c
    added = 0
    for font, table in known.items():
        gids = sorted(table)
        for a, b in zip(gids, gids[1:]):
            step = ord(table[b]) - ord(table[a])
            if b - a < 2 or b - a > 6 or step != b - a:
                continue
            for g in range(a + 1, b):
                if g not in table:
                    seen[(font, g)][chr(ord(table[a]) + g - a)] += 1
                    added += 1
    return added


def main():
    files = sorted(glob.glob('examiner-reports/*/schemes/*.pdf'))
    if not files:
        sys.exit('no scheme PDFs found -- run from the repo root')
    seen, bad = scan(files)
    added = interpolate(seen)

    table, conflict = {}, collections.defaultdict(set)
    for (font, gid, u), n in bad.most_common():
        counts = seen.get((font, gid))
        if not counts:
            continue
        real = max(counts, key=counts.get)
        # Agreement, not volume. A glyph id is one character in one font, so a
        # single clean sighting settles it -- demanding three threw away the x
        # of dy/dx, read correctly exactly once in a hundred schemes. What is
        # not evidence is an id that disagrees with itself, which is how a
        # mis-joined bracket got read as an italic n.
        if counts[real] * 10 < sum(counts.values()) * 9:
            continue
        conflict[chr(u)].add(real)
        table.setdefault(chr(u), real)

    # A mangled codepoint that means two different characters cannot be
    # repaired from the character alone, so drop it rather than guess.
    dropped = sorted(k for k, v in conflict.items() if len(v) > 1)
    for k in dropped:
        table.pop(k, None)
    table.update(NEIGHBOUR)
    table.update(LIGATURE)

    total = sum(bad.values())
    fixed = sum(n for (f, g, u), n in bad.items()
                if chr(u) in table)
    print(f'{len(files)} scheme PDFs')
    print(f'interpolated {added} glyph ids inside known runs')
    print(f'{len(table)} map entries; dropped {len(dropped)} ambiguous {dropped}')
    print(f'mangled instances {total}, repaired {fixed} ({100 * fixed // max(total, 1)}%)')
    if '--write' in sys.argv:
        with open(OUT, 'w', encoding='utf-8') as fh:
            json.dump(table, fh, ensure_ascii=False, indent=0, sort_keys=True)
        print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
