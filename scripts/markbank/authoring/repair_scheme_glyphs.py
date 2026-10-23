#!/usr/bin/env python3
"""Repair the mangled glyphs in an existing scheme .md from its source PDF's glyph ids.

A scheme .md committed by an earlier extractor carries whatever code points the
PDF's broken ToUnicode map reported ("seƫng", "ouƞlows", "aŌer", private-use
ticks). Re-extracting would also re-flow the file, and a provenance-checked card
quotes the file as it stands -- so this changes ONLY the mangled characters.

For the source PDF, every mangled character is read by its font and glyph id
through scripts/markbank/glyph_ids.py; within one document a code point is one
glyph, so the result is a per-document character map. A character the table
cannot resolve, or that resolves two ways in this document, is refused: the
file is left unchanged and the command fails. Never hand-map.

    python3 scripts/markbank/authoring/repair_scheme_glyphs.py <scheme.md> <scheme.pdf> [--check]
"""
import os
import sys

import pymupdf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from glyph_ids import MANGLED, document_map, load_table  # noqa: E402


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    md, pdf = sys.argv[1], sys.argv[2]
    text = open(md, encoding='utf-8').read()
    present = set(MANGLED.findall(text))
    if not present:
        print(f'{md}: clean')
        return 0
    dmap, unresolved, ambiguous = document_map(pymupdf.open(pdf), load_table())
    refused = sorted(c for c in present if c not in dmap or c in ambiguous)
    if refused:
        print(f'{md}: refused, unresolved by glyph id: ' + ' '.join(f'U+{ord(c):04X}' for c in refused), file=sys.stderr)
        return 1
    fixed = ''.join(dmap.get(c, c) for c in text)
    changes = {f'U+{ord(c):04X}->{dmap[c]}': text.count(c) for c in sorted(present)}
    if '--check' not in sys.argv:
        with open(md, 'w', encoding='utf-8') as fh:
            fh.write(fixed)
    print(f'{md}: {sum(changes.values())} glyphs repaired {changes}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
