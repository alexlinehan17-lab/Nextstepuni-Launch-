#!/usr/bin/env python3
"""Repair ONE glyph-mangled Polish scheme .md from the corpus-derived map.

    python3 scripts/markbank/authoring/pl_glyphs.py 2015 hl [--check]

The 2015 Higher scheme's subset font reports its Polish letters as other code
points ("czĊĞci" for "części": ę -> Ċ, ś -> Ğ, ł -> á, ć -> ü, ż -> Ī, ń -> Ĕ,
ź -> Ĩ). Those stand inside Latin Extended-A, which build-deck's glyph gate
accepts as real Polish, so nothing downstream would catch them.

The map is lt_glyphs.derive('polish'): every mangled character settled by the
WORDS the clean Polish schemes and papers print (three votes, clear margin), or
by a glyph cropped from the page and looked at (lt_glyphs.VERIFIED). Nothing is
hand-mapped. Only the characters this file holds are applied, character by
character, so its lines stay where they are; a mangled character the map does
not settle is refused and the file is left as it was. The per-file map is
recorded beside the subject maps as glyphmap-polish-<year>-<level>.json.

No other Polish scheme is touched: real "á" and "ü" in a quoted name elsewhere
must stay what they are.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import lt_glyphs  # noqa: E402


def main():
    year, level = sys.argv[1], sys.argv[2]
    md = os.path.join(ROOT, 'examiner-reports', 'polish', 'schemes', f'{year}-{level}.md')
    text = open(md, encoding='utf-8').read()
    real = lt_glyphs.LATIN1_REAL - lt_glyphs.LATIN1_MANGLED['polish']
    present = lt_glyphs.mangled_chars(text, lt_glyphs.ALPHABETS['polish'], real)
    if not present:
        print(f'{md}: clean')
        return 0
    table, _left = lt_glyphs.derive('polish', verbose=False)
    refused = sorted(c for c in present if c not in table)
    if refused:
        print(f'{md}: refused, unsettled: ' + ' '.join(f'U+{ord(c):04X}' for c in refused),
              file=sys.stderr)
        return 1
    used = {c: table[c] for c in sorted(present)}
    fixed = ''.join(used.get(c, c) for c in text)
    counts = {f'{c} U+{ord(c):04X} -> {used[c]}': text.count(c) for c in used}
    print(f'{md}: {sum(text.count(c) for c in used)} glyphs repaired {counts}')
    if '--check' not in sys.argv:
        with open(md, 'w', encoding='utf-8') as fh:
            fh.write(fixed)
        path = os.path.join(HERE, f'glyphmap-polish-{year}-{level}.json')
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(used, fh, ensure_ascii=False, indent=0, sort_keys=True)
            fh.write('\n')
        print(f'wrote {path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
