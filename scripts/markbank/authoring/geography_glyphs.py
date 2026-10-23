#!/usr/bin/env python3
"""Derive Geography's symbol-font repair map from the glyph ids themselves.

Some SEC Geography schemes embed Wingdings with a broken ToUnicode map: the
2014 Higher and Ordinary schemes (and the 2016 Ordinary instructions page)
print every note bullet as "¾", and get_texttrace() reads the same glyph as
U+FFFD. The glyph id is reliable where the ToUnicode is not, and it means the
same character throughout a font, so the repair is learned, never typed: every
symbol-font glyph id in the June 2010+ English Geography papers and schemes is
read where its ToUnicode is sane, and an id is mapped only when every sane
reading agrees (a real Unicode reading is preferred to the font's private-use
code point, which names the same glyph). Only ids that some document fails to
decode are written out, each with the sightings that settled it.

    python3 scripts/markbank/authoring/geography_glyphs.py          # check
    python3 scripts/markbank/authoring/geography_glyphs.py --write
"""

from __future__ import annotations

import collections
import glob
import json
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(HERE, 'glyphmap-geography.json')
SYMBOL_FONTS = ('Wingdings', 'Symbol')
# Reviewed window only: June sittings from 2010 (the shared corpus also holds
# the 1995-2009 archive and, in their own folders, the deferred sittings).
YEARS = range(2010, 2027)


def family(font: str) -> str | None:
    name = font.split('+')[-1]
    return next((f for f in SYMBOL_FONTS if name.startswith(f)), None)


def undecoded(code: int) -> bool:
    return code == 0xFFFD or 0x0100 < code < 0x2000


def private(code: int) -> bool:
    return 0xE000 <= code <= 0xF8FF


def sources() -> list[str]:
    out = []
    for year in YEARS:
        for kind in ('exampapers', 'markingschemes'):
            out += sorted(glob.glob(os.path.join(
                ROOT, 'paper-trail-corpus', kind, str(year), 'LC005*EV.pdf')))
    return out


def derive() -> dict:
    seen: dict[tuple[str, int], collections.Counter] = collections.defaultdict(collections.Counter)
    broken: dict[tuple[str, int], set[str]] = collections.defaultdict(set)
    for path in sources():
        rel = os.path.relpath(path, ROOT)
        for page in fitz.open(path):
            for trace in page.get_texttrace():
                fam = family(trace['font'])
                if not fam:
                    continue
                for code, gid, _origin, _bbox in trace['chars']:
                    if undecoded(code):
                        broken[(fam, gid)].add(rel)
                    else:
                        seen[(fam, gid)][code] += 1
    out: dict[str, dict[str, dict]] = {}
    for (fam, gid), docs in sorted(broken.items()):
        readings = seen.get((fam, gid), collections.Counter())
        public = {code for code in readings if not private(code)}
        pua = {code for code in readings if private(code)}
        if len(public) > 1 or (not public and len(pua) != 1):
            raise SystemExit(f'{fam} glyph {gid}: readings disagree {sorted(map(hex, readings))}')
        if not readings:
            raise SystemExit(f'{fam} glyph {gid}: never read sanely; settle it by looking at it')
        char = chr(next(iter(public)) if public else next(iter(pua)))
        out.setdefault(fam, {})[str(gid)] = {
            'char': char,
            'sightings': {f'U+{code:04X}': n for code, n in sorted(readings.items())},
            'repairs': sorted(docs),
        }
    return out


def main() -> int:
    derived = derive()
    text = json.dumps(derived, ensure_ascii=False, indent=1) + '\n'
    if '--write' in sys.argv:
        with open(OUT, 'w', encoding='utf-8') as handle:
            handle.write(text)
        print(f'wrote {os.path.relpath(OUT, ROOT)}: '
              + ', '.join(f'{fam} {gid} -> {row["char"]}' for fam, ids in derived.items()
                          for gid, row in ids.items()))
        return 0
    current = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
    if current != text:
        print('glyphmap-geography.json is stale; re-derive with --write', file=sys.stderr)
        return 1
    print('glyphmap-geography.json is current.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
