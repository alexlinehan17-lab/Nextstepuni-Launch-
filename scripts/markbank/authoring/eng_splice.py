#!/usr/bin/env python3
"""Put ONE sitting's freshly authored cards into the authored file.

    python3 scripts/markbank/authoring/eng_splice.py 2025 hl 2025 ol

Five agents own two sittings each and share eng_all.py, so a wholesale
regeneration would rewrite every sitting from whichever agent ran it last.
This replaces only the sittings named, leaves every other card byte-identical,
and keeps the file in the order eng_all emits.
"""
import json
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'engineering.json')
LONG = {'hl': 'higher', 'ol': 'ordinary'}


def main(argv):
    want = {(int(argv[i]), LONG[argv[i + 1]]) for i in range(0, len(argv), 2)}
    fresh = json.loads(subprocess.run(
        [sys.executable, os.path.join(DIR, 'eng_all.py')],
        capture_output=True, text=True, check=True).stdout)
    existing = json.load(open(AUTHORED, encoding='utf-8'))
    kept = [c for c in existing if (c['year'], c['level']) not in want]
    mine = [c for c in fresh if (c['year'], c['level']) in want]
    out = sorted(kept + mine,
                 key=lambda c: (c['year'], c['level'] != 'higher', c['id']))
    json.dump(out, open(AUTHORED, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'{len(existing)} -> {len(out)} cards; '
          f'{len(mine)} for {sorted(want)}, {len(kept)} untouched')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
