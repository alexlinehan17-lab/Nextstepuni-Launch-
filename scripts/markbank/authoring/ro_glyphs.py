#!/usr/bin/env python3
"""Repair the Romanian 2013 and 2015 scheme .md and paper text from glyph ids.

Those four PDFs set Times New Roman (regular, bold, italic) with no ToUnicode
map, so the text layer reports stand-ins ("܊", "܈", "Ġ", "а", "Ю"...) for
ă ş ţ ș ț and friends. The repo's glyph table (glyph_ids.json) does not know
these glyphs, so the entries are DERIVED here, never typed: for every
(font family, glyph id) the four documents need, every other scheme and paper
under examiner-reports/ that draws the same glyph with a working map votes
for its character. An entry is taken only with at least three sightings and
95 % agreement; anything else is left unresolved, and the repair then refuses
the whole file rather than guess.

    python3 scripts/markbank/authoring/ro_glyphs.py derive          # print the derived entries
    python3 scripts/markbank/authoring/ro_glyphs.py scheme 2013 [--check]
    python3 scripts/markbank/authoring/ro_glyphs.py paper 2013      # print the paper's map

The scheme .md is changed only at its mangled characters (repair_scheme_glyphs
does the same with the shared table). The paper's map is written to
glyphmap-romanian-<year>-paper.json, which sl_lib applies to that paper's text.
"""
import collections
import glob
import json
import os
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(HERE, '..'))
from glyph_ids import MANGLED, load_table, family, page_glyphs  # noqa: E402

YEARS = (2013, 2015)
# Romanian's own letters (lt_glyphs.ALPHABETS['romanian'] and capitals): real
# characters, though they sit in the block glyph_ids.MANGLED scans, so a
# sighting of one counts as clean.
ROMANIAN = set('ăâîşșţțĂÂÎŞȘŢȚ')
MIN_SIGHTINGS, MIN_SHARE = 3, 0.95


def _pdfs(year):
    base = os.path.join(ROOT, 'examiner-reports', 'romanian')
    return {'scheme': os.path.join(base, 'schemes', f'{year}-hl.pdf'),
            'paper': os.path.join(base, 'papers', f'{year}-hl-paper.pdf')}


def needed():
    out = set()
    for year in YEARS:
        for path in _pdfs(year).values():
            with pymupdf.open(path) as doc:
                for page in doc:
                    for span in page.get_texttrace():
                        for ch in span['chars']:
                            if ch[0] == 0xFFFD:
                                out.add((family(span['font']), ch[1]))
    return out


def derive():
    want = needed()
    votes = collections.defaultdict(collections.Counter)
    skip = {os.path.realpath(p) for y in YEARS for p in _pdfs(y).values()}
    for path in sorted(glob.glob(os.path.join(ROOT, 'examiner-reports', '*', 'schemes', '*.pdf'))
                       + glob.glob(os.path.join(ROOT, 'examiner-reports', '*', 'papers', '*.pdf'))):
        if os.path.realpath(path) in skip:
            continue
        try:
            doc = pymupdf.open(path)
        except Exception:
            continue
        with doc:
            for page in doc:
                for span in page.get_texttrace():
                    fam = family(span['font'])
                    for ch in span['chars']:
                        if (fam, ch[1]) in want and ch[0] not in (0xFFFD,) and ch[0] > 0x1F \
                                and (chr(ch[0]) in ROMANIAN or not MANGLED.match(chr(ch[0]))):
                            votes[(fam, ch[1])][chr(ch[0])] += 1
    table, left = {}, {}
    for key in sorted(want):
        v = votes.get(key)
        if not v:
            left[key] = 'no clean sighting'
            continue
        ch, n = v.most_common(1)[0]
        total = sum(v.values())
        if n >= MIN_SIGHTINGS and n / total >= MIN_SHARE:
            table[f'{key[0]}|{key[1]}'] = ch
        else:
            left[key] = dict(v)
    return table, left


# Two glyphs whose only clean sightings are themselves outside Romanian's
# alphabet, settled by cropping them and looking (memory markbank-glyph-repair):
# Times New Roman Bold 1211 is a with breve and dot below (the 2012-2020 rule
# line "Toate rặspunsurile ...", rendered at 300 dpi, 2016 p2); 1276 is A with
# a caron, read U+01CD in the 2010-2012, 2014 and 2016 schemes and drawn with a
# pointed caron in their heading "LIMBA ROMÂNǍ" (2014 p3, 300 dpi).
RENDERED = {'TimesNewRoman|1211': '\u1eb7', 'TimesNewRoman|1276': '\u01cd'}


# Latin-1 letters Romanian does not use, which these documents' regular-weight
# Times New Roman reports for its own letters ("úi" for şi, "aúa" for aşa):
# suspect wherever the font is not bold (the bold "Coimisiún na Scrúduithe
# Stáit" on each cover is Irish and genuine).
SUSPECT = set('úá')


def document_map(doc, table):
    """glyph_ids.document_map, also reading SUSPECT letters in regular fonts:
    every candidate character is read by its drawing origin's (family, glyph
    id); within one document a code point must resolve one way."""
    seen, unresolved = {}, set()
    for page in doc:
        origin = page_glyphs(page)
        for blk in page.get_text('rawdict')['blocks']:
            for line in blk.get('lines', []):
                for sp in line.get('spans', []):
                    bold = 'Bold' in sp.get('font', '')
                    for ch in sp['chars']:
                        c = ch['c']
                        if not (MANGLED.match(c) and c not in ROMANIAN) and not (c in SUSPECT and not bold):
                            continue
                        hit = origin.get((round(ch['origin'][0], 2), round(ch['origin'][1], 2)))
                        text = table['gid'].get(f'{hit[0]}|{hit[1]}') if hit else None
                        if text is None or text == c:
                            unresolved.add(c)
                        else:
                            seen.setdefault(c, set()).add(text)
    ambiguous = {c for c, v in seen.items() if len(v) > 1}
    return {c: next(iter(v)) for c, v in seen.items() if len(v) == 1}, unresolved, ambiguous


def full_table():
    base = load_table()
    derived, _left = derive()
    derived = {**derived, **RENDERED}
    gid = dict(base['gid'])
    for k, v in derived.items():
        gid.setdefault(k, v)
    return {**base, 'gid': gid}


def main():
    cmd = sys.argv[1]
    if cmd == 'derive':
        table, left = derive()
        for k, v in sorted(table.items()):
            print(f'{k} -> {v!r}')
        for k, v in sorted(left.items()):
            print(f'UNSETTLED {k}: {v}')
        return 0
    year = int(sys.argv[2])
    table = full_table()
    pdf = _pdfs(year)[cmd]
    with pymupdf.open(pdf) as doc:
        dmap, unresolved, ambiguous = document_map(doc, table)
    if cmd == 'paper':
        out = os.path.join(HERE, f'glyphmap-romanian-{year}-paper.json')
        print({f'U+{ord(k):04X}': v for k, v in sorted(dmap.items())}, 'unresolved', unresolved, 'ambiguous', ambiguous)
        if not ambiguous:
            with open(out, 'w', encoding='utf-8') as fh:
                json.dump(dict(sorted(dmap.items())), fh, ensure_ascii=False, indent=1)
                fh.write('\n')
        return 1 if ambiguous else 0
    md = os.path.join(ROOT, 'examiner-reports', 'romanian', 'schemes', f'{year}-hl.md')
    text = open(md, encoding='utf-8').read()
    real = ROMANIAN | set(RENDERED.values())
    present = ({c for c in MANGLED.findall(text) if c not in real}
               | (SUSPECT & set(text.partition('## Page 2')[2]))
               | {c for c in text if 0x0700 <= ord(c) <= 0x074F or 0x0400 <= ord(c) <= 0x04FF})
    refused = sorted(c for c in present if c not in dmap or c in ambiguous)
    if refused:
        print(f'{md}: refused, unresolved: ' + ' '.join(f'U+{ord(c):04X}' for c in refused))
        return 1
    suspect = {c: dmap.pop(c) for c in list(dmap) if c in SUSPECT}
    fixed = ''.join(dmap.get(c, c) for c in text)
    changes = {f'U+{ord(c):04X}->{dmap[c]}': text.count(c) for c in sorted(present) if c in dmap}
    # A SUSPECT letter is repaired only below the cover (page 1 prints the
    # genuine Irish "Coimisiún na Scrúduithe Stáit" in bold), and only where the
    # .md holds exactly as many as the PDF draws in regular weight.
    head, sep, body = fixed.partition('## Page 2')
    with pymupdf.open(pdf) as doc:
        regular = collections.Counter(ch['c'] for page in doc for blk in page.get_text('rawdict')['blocks']
                                      for line in blk.get('lines', []) for sp in line.get('spans', [])
                                      if 'Bold' not in sp.get('font', '') for ch in sp['chars'] if ch['c'] in SUSPECT)
    for c, good in suspect.items():
        if body.count(c) == 0:
            continue                                  # repaired already
        if body.count(c) != regular[c]:
            print(f'{md}: refused, {c!r} {body.count(c)} in the .md body, {regular[c]} regular in the PDF')
            return 1
        changes[f'U+{ord(c):04X}->{good}'] = body.count(c)
        body = body.replace(c, good)
    fixed = head + sep + body
    if '--check' not in sys.argv:
        with open(md, 'w', encoding='utf-8') as fh:
            fh.write(fixed)
    print(f'{md}: {sum(changes.values())} glyphs repaired {changes}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
