#!/usr/bin/env python3
"""After english_publish.py: serve each published English deferred paper as June's papers are served.

For every deferred paper english_publish.py published: the index entry carries
"answers": 1 (paperTrailData.ts), the reviewed answer map is hosted byte-identically
in public/paper-answers and listed in HOSTED_ANSWER_OVERRIDES, the scheme's text is
extracted for the deck's scheme check (examiner-reports/english/schemes/<y>-<lv>-deferred.md),
and the deck size manifest counts the new cards. Idempotent; --check reports what it would change.

    python3 scripts/markbank/authoring/english_deferred_finish.py [--check]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys

from english_complete import ROOT

CARDS = ROOT / 'components/MarkBank/cards/english'


def published_deferred():
    papers = []
    for level in ('higher', 'ordinary'):
        manifest = json.loads((CARDS / f'published-{level}.json').read_text())
        papers += [p for p in manifest['papers'] if '-deferred-' in p['paperId']]
    return papers


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    from english_complete import inventory
    records = {r['id']: r for r in inventory()['papers']}
    todo = []
    index = (ROOT / 'paperTrailData.ts').read_text()
    resolve = (ROOT / 'components/PaperTrail/vaultResolve.ts').read_text()
    for paper in published_deferred():
        record = records[paper['paperId']]
        year, fileid = record['year'], record['paperFileid']
        # 1. index flag on the deferred entry's paper item
        item = re.compile(r'(\{"label": "Deferred · Paper (?:One|Two)", "doc": \{"f": "%s", "b": \d+\}, "sitting": "deferred", '
                          r'"scheme": \{"f": "[^"]+", "b": \d+\})(\})' % re.escape(fileid))
        entry_re = re.compile(r'\{"year": %d, "level": "%s", "lang": "ev", "sitting": "deferred", "papers": \[.*?\]\}'
                              % (year, record['level']))
        entries = [m for m in entry_re.finditer(index) if f'"{fileid}"' in m.group(0)]
        if len(entries) != 1:
            raise SystemExit(f'{fileid} {year}: {len(entries)} deferred index entries')
        whole = entries[0].group(0)
        if '"answers": 1' not in item.sub(r'\1\2', whole) or not re.search(
                r'"f": "%s", "b": \d+\}, "sitting": "deferred", "scheme": \{"f": "[^"]+", "b": \d+\}, "answers": 1\}'
                % re.escape(fileid), whole):
            new = item.sub(r'\1, "answers": 1\2', whole)
            if new == whole:
                raise SystemExit(f'{fileid} {year}: index item not found')
            index = index.replace(whole, new)
            todo.append(f'index answers flag {year} {fileid}')
        # 2. hosted override
        key = f"  'english|{year}|{fileid}',\n"
        if key not in resolve:
            anchor = "  // English deferred sittings, published paper by paper (english_publish.py): reviewed deferred answer maps.\n"
            if anchor not in resolve:
                raise SystemExit('HOSTED_ANSWER_OVERRIDES anchor missing')
            block_end = resolve.index(anchor) + len(anchor)
            while resolve[block_end:].startswith("  'english|") and '-deferred' in resolve[block_end:resolve.index('\n', block_end)]:
                block_end = resolve.index('\n', block_end) + 1
            resolve = resolve[:block_end] + key + resolve[block_end:]
            todo.append(f'hosted override {year} {fileid}')
        # 3. hosted copy
        src = ROOT / 'scripts/paper-trail/answers' / str(year) / f'{fileid}.json'
        dst = ROOT / 'public/paper-answers' / str(year) / f'{fileid}.json'
        if not dst.exists() or dst.read_bytes() != src.read_bytes():
            todo.append(f'hosted copy {dst.relative_to(ROOT)}')
            if not args.check:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
        # 4. scheme text for the deck's scheme check
        md = ROOT / 'examiner-reports/english/schemes' / f"{year}-{'hl' if record['level'] == 'higher' else 'ol'}-deferred.md"
        if not md.exists():
            todo.append(f'scheme text {md.relative_to(ROOT)}')
            if not args.check:
                subprocess.run([sys.executable, str(ROOT / 'scripts/markbank/extract-scheme.py'),
                                str(ROOT / record['markingScheme']['path']), '-o', str(md)], check=True)
    # 5. deck sizes
    sizes_path = ROOT / 'components/MarkBank/cards/sizes.json'
    sizes = json.loads(sizes_path.read_text())
    authored = json.loads((CARDS / 'authored.json').read_text())
    want = {}
    for level in ('higher', 'ordinary'):
        manifest = json.loads((CARDS / f'published-{level}.json').read_text())
        bridged = set(manifest['bridgedLegacyIds'])
        legacy = [c for c in authored['cards'] if c['level'] == level and c['id'] not in bridged]
        want[level] = len(legacy) + manifest['cardCount']
    if sizes['english'] != want:
        todo.append(f'deck sizes {want}')
        sizes['english'] = want
    if not args.check:
        (ROOT / 'paperTrailData.ts').write_text(index)
        (ROOT / 'components/PaperTrail/vaultResolve.ts').write_text(resolve)
        sizes_path.write_text(json.dumps(sizes, indent=1) + '\n')
    for line in todo:
        print(('stale: ' if args.check else 'done: ') + line)
    return 1 if (todo and args.check) else 0


if __name__ == '__main__':
    sys.exit(main())
