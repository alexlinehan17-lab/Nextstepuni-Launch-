#!/usr/bin/env python3
"""Repair a subject's ligature misreadings in its scheme .md files and card sources.

A ligature glyph reaches the text layer misread: as a mangled code point
("seƫng"), which the shared character map then turned into the wrong letters
("settng"), or as fewer letters than it draws ("batle" for "battle"). For each
source PDF this reads every glyph the table knows to be a ligature by its font
and glyph id (scripts/markbank/glyph_ids.py) and turns each disagreement into a
whole-word repair for that document only. A misread form the same document also
prints correctly, or one that would repair two ways, is refused, never guessed.

  * examiner-reports/<subject>/schemes/<year>-<hl|ol>.md take their scheme PDF's
    repairs. Only the misread words change, so quotes do not shift.
  * scripts/markbank/authored/<subject>.json cards take the repairs of their
    year and level's scheme and papers. IDs and every other field are kept;
    author notes, which never ship, are left as written.

Every misread form found in the subject's papers and schemes is written to
authoring/ligature_words.json; the build refuses a card carrying one and the
deck test proves none ships.

    python3 scripts/markbank/authoring/repair_ligature_words.py <subject> [--write]
"""
import glob
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from glyph_ids import MANGLED, apply_words, document_map, document_words, load_table  # noqa: E402
from derive_glyph_ids import SUBJECT_CODES  # noqa: E402

WORDS_PATH = os.path.join(HERE, 'ligature_words.json')
LEVEL = {'hl': 'A', 'ol': 'G', 'higher': 'A', 'ordinary': 'G'}


def legacy_variants():
    """What earlier pipelines did to mangled glyphs, so their output is recognised.

    The shared character map as it stood before U+01A9 and U+01AB were corrected
    ("t" and "tt"), applied to every character it maps: "ﬁƫngs" reached the
    technology cards as "fittngs" through two of its entries at once.
    """
    with open(os.path.join(HERE, 'glyphmap.json'), encoding='utf-8') as fh:
        gm = json.load(fh)
    historic = dict(gm, **{'\u01a9': 't', '\u01ab': 'tt'})
    return (historic,)


def docs_for(code, year, level):
    lv = LEVEL[level]
    scheme = glob.glob(f'paper-trail-corpus/markingschemes/{year}/{code}{lv}LP000EV.pdf')
    papers = sorted(glob.glob(f'paper-trail-corpus/exampapers/{year}/{code}{lv}LP*EV.pdf'))
    return scheme, papers


_cache = {}


def doc_repairs(path, table, variants):
    if path not in _cache:
        doc = pymupdf.open(path)
        chars, _unresolved, ambiguous = document_map(doc, table)
        words, refused, clean = document_words(doc, table, variants)
        doc.close()
        # Characters too are repaired only where they stand for a ligature.
        _cache[path] = ({c: t for c, t in chars.items() if c not in ambiguous and len(t) > 1 and t.isalpha()},
                        words, refused, clean)
    return _cache[path]


def merged(paths, table, variants):
    chars, words, refused = {}, {}, set()
    for p in paths:
        c, w, r, _clean = doc_repairs(p, table, variants)
        for k, v in c.items():
            if chars.get(k, v) != v:
                refused.add(k)
            chars[k] = v
        for k, v in w.items():
            if words.get(k, v) != v:
                refused.add(k)
            words[k] = v
        refused |= r
    return ({k: v for k, v in chars.items() if k not in refused},
            {k: v for k, v in words.items() if k not in refused}, refused)


def fix_text(text, chars, words):
    text, counts = apply_words(text, words)
    if MANGLED.search(text):
        text = ''.join(chars.get(c, c) for c in text)
    return text, counts


def walk(node, fn, skip=('notes',)):
    if isinstance(node, dict):
        for k in list(node):
            if k in skip:
                continue
            v = node[k]
            if isinstance(v, str):
                node[k] = fn(v)
            else:
                walk(v, fn, skip)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if isinstance(v, str):
                node[i] = fn(v)
            else:
                walk(v, fn, skip)


def main():
    subject = sys.argv[1]
    write = '--write' in sys.argv
    # --code LCnnn audits a subject the derivation does not list yet.
    code = sys.argv[sys.argv.index('--code') + 1] if '--code' in sys.argv else SUBJECT_CODES[subject]
    table, variants = load_table(), legacy_variants()
    found = {}

    for md in sorted(glob.glob(f'examiner-reports/{subject}/schemes/*.md')):
        m = re.match(r'(\d{4})-(hl|ol)\.md$', os.path.basename(md))
        if not m:
            continue
        scheme, _ = docs_for(code, m.group(1), m.group(2))
        if not scheme:
            print(f'{md}: no scheme PDF')
            continue
        chars, words, refused = merged(scheme, table, variants)
        found.update(words)
        text = open(md, encoding='utf-8').read()
        fixed, counts = fix_text(text, chars, words)
        if fixed != text:
            print(f'{md}: {sum(counts.values())} words {counts}' + (f' refused {sorted(refused)[:6]}' if refused else ''))
            if write:
                open(md, 'w', encoding='utf-8').write(fixed)

    path = f'scripts/markbank/authored/{subject}.json'
    raw = open(path, encoding='utf-8').read()
    cards = json.loads(raw)
    items = cards if isinstance(cards, list) else cards.get('cards', [])
    pairs, total = {}, {}
    for card in items:
        year, level = card.get('year'), card.get('level')
        if not year or level not in LEVEL:
            continue
        scheme, papers = docs_for(code, year, level)
        chars, words, _ = merged(scheme + papers, table, variants)
        found.update(words)

        def fn(s, chars=chars, words=words):
            out, counts = fix_text(s, chars, words)
            if out != s:
                pairs[s] = out
                for w, n in counts.items():
                    total[w] = total.get(w, 0) + n
            return out
        walk(card, fn)
    if pairs:
        print(f'{path}: {len(pairs)} strings, words {total}')
    if write and pairs:
        # Replace each changed string in the file's own formatting rather than
        # re-serialising, so nothing but the misread words moves.
        for old, new in pairs.items():
            eo, en = json.dumps(old, ensure_ascii=False), json.dumps(new, ensure_ascii=False)
            assert eo in raw, old[:60]
            raw = raw.replace(eo, en)
        assert json.loads(raw) is not None
        open(path, 'w', encoding='utf-8').write(raw)

    # A misread form that ANY of the subject's papers or schemes prints as a
    # real word is not one the build may refuse ("tuta" is Italian for overalls
    # as well as the 2025 scheme's misreading of "tutta").
    every = sorted(glob.glob(f'paper-trail-corpus/markingschemes/*/{code}*LP*EV.pdf')
                   + glob.glob(f'paper-trail-corpus/exampapers/*/{code}*LP*EV.pdf'))
    real = set()
    for pdf in every:
        real |= doc_repairs(pdf, table, variants)[3]
    found = {w: r for w, r in found.items() if w not in real}
    if write:
        data = json.load(open(WORDS_PATH, encoding='utf-8')) if os.path.exists(WORDS_PATH) else {}
        data[subject] = dict(sorted(found.items()))
        with open(WORDS_PATH, 'w', encoding='utf-8') as fh:
            json.dump(dict(sorted(data.items())), fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    print(f'{subject}: {len(found)} misread forms')


if __name__ == '__main__':
    main()
