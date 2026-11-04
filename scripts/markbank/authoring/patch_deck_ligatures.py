#!/usr/bin/env python3
"""Repair ligature misreadings in a shipped deck that cannot be rebuilt locally.

    python3 scripts/markbank/authoring/patch_deck_ligatures.py <subject> --code LCnnn [--write]

Some decks are not reproducible from their authored source on this machine (a
local applied-maths build drops cards), and some of their cards exist only in
the built deck. For those, a misread word ("leters" for the printed
"letters") is repaired where it ships:

  * every printed-text string literal in components/MarkBank/cards/<subject>/
    {higher,ordinary}.ts that carries a misread form recorded in
    ligature_words.json is repaired in place; identifiers (id, conceptId,
    topicId and figure keys) are never touched;
  * each repair must be proven by the card's OWN sources: the misread form and
    its repair must come from the glyph ids of that year and level's paper or
    scheme (scripts/markbank/glyph_ids.py), or the card is refused;
  * a card that also has an authored source gets a card-corrections.json entry
    setting the repaired field, so a future build ships the same text. A card
    that exists only in the deck gets none: build-deck.mjs refuses a correction
    for a card its source does not have ("stale correction").
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
from glyph_ids import apply_words, load_table  # noqa: E402
from repair_ligature_words import WORDS_PATH, docs_for, legacy_variants, merged  # noqa: E402

CORRECTIONS = 'scripts/markbank/card-corrections.json'
IDENTIFIERS = {'id', 'conceptId', 'topicId', 'figureKey', 'questionFigureKey', 'labelKey', 'candId', 'src', 'sha256'}
FIELD = re.compile(r'(?P<key>\w+): (?P<lit>"(?:[^"\\]|\\.)*")')
CARD = re.compile(r'\bid: "(?P<id>[^"]+)"[^\n]*?\n?(?:[^\n]*\n){0,3}?')


def main():
    subject = sys.argv[1]
    code = sys.argv[sys.argv.index('--code') + 1]
    write = '--write' in sys.argv
    misread = json.load(open(WORDS_PATH, encoding='utf-8')).get(subject, {})
    if not misread:
        sys.exit(f'{subject}: no misread forms recorded; run repair_ligature_words.py first')
    table, variants = load_table(), legacy_variants()
    authored = {c['id']: c for c in json.load(open(f'scripts/markbank/authored/{subject}.json', encoding='utf-8'))}
    corrections = json.load(open(CORRECTIONS, encoding='utf-8'))
    patched = {}
    for level in ('higher', 'ordinary'):
        path = f'components/MarkBank/cards/{subject}/{level}.ts'
        if not os.path.exists(path):
            continue
        text = open(path, encoding='utf-8').read()
        # Card boundaries: each card object opens with its year and carries an id.
        starts = [m.start() for m in re.finditer(r'\n  \{\n', text)] + [len(text)]
        out, last = [], 0
        for a, b in zip(starts, starts[1:]):
            block = text[a:b]
            cid = re.search(r'\bid: "([^"]+)"', block)
            year = re.search(r'\byear: (\d{4})', block)
            if not cid or not year:
                continue
            cid, year = cid.group(1), int(year.group(1))
            hits = [w for w in misread if re.search(rf'(?<![\w]){re.escape(w)}(?![\w])', block)]
            if not hits:
                continue
            scheme, papers = docs_for(code, year, level)
            _, words, _ = merged(scheme + papers, table, variants)

            def fix(m, cid=cid, words=words):
                key, lit = m.group('key'), m.group('lit')
                if key in IDENTIFIERS:
                    return m.group(0)
                value = json.loads(lit)
                repaired, counts = apply_words(value, words)
                if repaired == value:
                    return m.group(0)
                patched.setdefault(cid, {})[key] = (value, repaired, counts)
                return f'{key}: {json.dumps(repaired, ensure_ascii=False)}'
            new_block = FIELD.sub(fix, block)
            left = [w for w in misread if re.search(rf'(?<![\w]){re.escape(w)}(?![\w])', FIELD.sub(
                lambda m: '' if m.group('key') in IDENTIFIERS else m.group(0), new_block))]
            assert not left, f'{cid}: {left} not proven by its own {year} {level} sources'
            out.append((a, b, new_block))
        for a, b, new_block in reversed(out):
            text = text[:a] + new_block + text[b:]
        if write and out:
            open(path, 'w', encoding='utf-8').write(text)
    for cid, fields in sorted(patched.items()):
        for key, (old, new, counts) in fields.items():
            print(f'{cid}.{key}: {counts}')
        if cid in authored:
            entry = corrections.setdefault(subject, {}).setdefault(cid, {'reason': '', 'set': {}})
            for key, (old, new, counts) in fields.items():
                source = authored[cid].get(key)
                repaired_source = apply_words(source, {w: r for w, r in misread.items()})[0] if isinstance(source, str) else None
                assert repaired_source == new, (cid, key, 'the shipped text no longer matches its authored source')
                entry['set'][key] = new
            entry['reason'] = ('A ligature glyph misread: the paper draws Calibri’s "tt" ligature (glyph 425), which the text '
                               'layer reported as U+01A9 and the old character map turned into one "t". Repaired by glyph id from '
                               'the card’s own paper (patch_deck_ligatures.py); nothing else in the text changes.')
            print(f'   card-corrections.json entry for {cid}')
        else:
            print(f'   {cid} has no authored source: patched in the deck only')
    if write:
        with open(CORRECTIONS, 'w', encoding='utf-8') as fh:
            json.dump(corrections, fh, ensure_ascii=False, indent=1)
            fh.write('\n')


if __name__ == '__main__':
    main()
