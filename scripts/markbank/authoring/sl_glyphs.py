#!/usr/bin/env python3
"""Repair small-language scheme .md and paper text from glyph ids.

Some PDFs set a font with no ToUnicode map, so the text layer reports
stand-ins for the language's letters:
- Romanian 2013 and 2015 (scheme and paper): Times New Roman (regular, bold,
  italic) reports "܊", "܈", "Ġ", "а", "Ю"... for ă ş ţ ș ț and friends.
- Bulgarian 2015 (scheme): a Type0 Times New Roman with no ToUnicode map, so
  every Cyrillic letter reaches the .md as its glyph id read as a code point
  ("ɨɬɝɨɜɨɪɢ" for "отговори"; the census excluded Q2-Q5 for it).
The repo's glyph table (glyph_ids.json) does not know these glyphs, so the
entries are DERIVED here, never typed: for every (font family, glyph id) the
documents need, every other scheme and paper under examiner-reports/ that draws
the same glyph with a working map votes for its character. An entry is taken
only with at least three sightings and 95 % agreement; anything else is left
unresolved, and the repair then refuses the whole file rather than guess.

    python3 scripts/markbank/authoring/sl_glyphs.py <subject> derive          # print the derived entries
    python3 scripts/markbank/authoring/sl_glyphs.py <subject> scheme <year> [--check]
    python3 scripts/markbank/authoring/sl_glyphs.py <subject> paper <year>    # write the paper's map

The scheme .md is changed only at its mangled characters (repair_scheme_glyphs
does the same with the shared table). The paper's map is written to
glyphmap-<subject>-<year>-paper.json, which sl_lib applies to that paper's text.
(Was ro_glyphs.py, Romanian only; its Romanian results are unchanged.)
"""
import collections
import glob
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(HERE, '..'))
from glyph_ids import MANGLED, load_table, family, page_glyphs  # noqa: E402

# A language's own letters: real characters, though they sit in the block
# glyph_ids.MANGLED scans, so a sighting of one counts as clean.
# Romanian: lt_glyphs.ALPHABETS['romanian'] and capitals. Bulgarian: the
# Cyrillic alphabet it prints (ѝ included).
ROMANIAN = set('ăâîşșţțĂÂÎŞȘŢȚ')
CZECH = set('áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ')
CROATIAN = set('čćđšžČĆĐŠŽ')
# Greek and Coptic (U+0370-03FF) and Greek Extended (U+1F00-1FFF), as build-deck's REAL class
GREEK = {chr(c) for c in list(range(0x370, 0x400)) + list(range(0x1F00, 0x2000))}
BULGARIAN = set('абвгдежзийклмнопрстуфхцчшщъьюяѝАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯЍ')
MIN_SIGHTINGS, MIN_SHARE = 3, 0.95


def _pdfs(subject, year):
    base = os.path.join(ROOT, 'examiner-reports', subject)
    return {'scheme': os.path.join(base, 'schemes', f'{year}-hl.pdf'),
            'paper': os.path.join(base, 'papers', f'{year}-hl-paper.pdf')}


def needed(subject):
    cfg = SUBJECTS[subject]
    out = set()
    for year, kinds in cfg['docs'].items():
        for path in (_pdfs(subject, year)[k] for k in kinds):
            with pymupdf.open(path) as doc:
                for page in doc:
                    for span in page.get_texttrace():
                        for ch in span['chars']:
                            if ch[0] == 0xFFFD:
                                out.add((family(span['font']), ch[1]))
    return out


def derive(subject):
    cfg = SUBJECTS[subject]
    want = needed(subject)
    votes = collections.defaultdict(collections.Counter)
    skip = {os.path.realpath(_pdfs(subject, y)[k]) for y, kinds in cfg['docs'].items() for k in kinds}
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
                                and (chr(ch[0]) in cfg['alphabet'] or not MANGLED.match(chr(ch[0]))):
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


# Per subject: the documents to repair ({year: kinds}), the letters that are
# real, glyphs settled by render, letters suspect in regular weight, and the
# stand-in blocks a scheme .md is also scanned for.
SUBJECTS = {
    'romanian': {'docs': {2013: ('scheme', 'paper'), 2015: ('scheme', 'paper')}, 'alphabet': ROMANIAN,
                 'rendered': RENDERED, 'suspect': SUSPECT,
                 'standin': lambda c: 0x0700 <= ord(c) <= 0x074F or 0x0400 <= ord(c) <= 0x04FF},
    # Times New Roman 630 has one clean sighting in the corpus ("ь"), short of
    # three: settled by cropping it at 400 dpi and looking (2015 scheme p4,
    # italic, "актьори").
    # Czech 2015 (scheme): a Type0 Times New Roman draws some letters with no
    # Unicode; rawdict reports their glyph ids, which collide with real Czech
    # letters ("VysvČtlete" for "Vysvětlete", "ýást" for "Část"), so the .md is
    # repaired by POSITION (positional()), never by character.
    'czech': {'docs': {2015: ('scheme',)}, 'alphabet': CZECH, 'rendered': {}, 'suspect': set(),
              'standin': lambda c: False, 'positional': True},
    # Croatian 2015 (scheme): Georgia and Times New Roman Type0 fonts draw
    # č ć đ Č Đ with no Unicode; rawdict reports their ids as þ ü ÿ ý Ĉ. By
    # position, as Czech.
    # Two Georgia glyphs settled by cropping at 400 dpi (p3): 264 is Đ (the bold
    # heading "VOĐA IZ ŠKOLE"; no clean sighting), 253 is Č ("Čudio se"; two
    # clean sightings, short of three).
    'croatian': {'docs': {2015: ('scheme',)}, 'alphabet': CROATIAN,
                 'rendered': {'Georgia|264': '\u0110', 'Georgia|253': '\u010c'}, 'suspect': set(),
                 'standin': lambda c: False, 'positional': True},
    # Modern Greek 2015 (scheme): Times New Roman and Calibri Type0 fonts with no
    # Unicode for any Greek letter ("ǺǹĬȂȅȁȅīǿȀǼȈ" for its heading). By position.
    # Eight Times New Roman capitals with fewer than three clean sightings, each
    # settled by cropping its own box at 400 dpi in its word (p3-p4): 299 Γ
    # ("ΒΑΘΜΟΛΟΓΙΚΕΣ"), 300 Θ, 498 Έ ("Ένα"), 506 Β, 513 Λ, 516 Ξ ("ΕΝΔΕΙΞΕΙΣ"),
    # 518 Π ("Πες"), 522 Υ ("Υπάρχουν").
    'modern-greek': {'docs': {2015: ('scheme',)}, 'alphabet': GREEK,
                     'rendered': {'TimesNewRoman|299': '\u0393', 'TimesNewRoman|300': '\u0398',
                                  'TimesNewRoman|498': '\u0388', 'TimesNewRoman|506': '\u0392',
                                  'TimesNewRoman|513': '\u039b', 'TimesNewRoman|516': '\u039e',
                                  'TimesNewRoman|518': '\u03a0', 'TimesNewRoman|522': '\u03a5'}, 'suspect': set(),
                     'standin': lambda c: False, 'positional': True},
    'bulgarian': {'docs': {2015: ('scheme',)}, 'alphabet': BULGARIAN,
                  'rendered': {'TimesNewRoman|630': '\u044c'}, 'suspect': set(),
                  'standin': lambda c: False},
}


def document_map(doc, table, alphabet=ROMANIAN, suspect=SUSPECT):
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
                        if not (MANGLED.match(c) and c not in alphabet) and not (c in suspect and not bold):
                            continue
                        hit = origin.get((round(ch['origin'][0], 2), round(ch['origin'][1], 2)))
                        text = table['gid'].get(f'{hit[0]}|{hit[1]}') if hit else None
                        if text is None or text == c:
                            unresolved.add(c)
                        else:
                            seen.setdefault(c, set()).add(text)
    ambiguous = {c for c, v in seen.items() if len(v) > 1}
    return {c: next(iter(v)) for c, v in seen.items() if len(v) == 1}, unresolved, ambiguous


def full_table(subject):
    base = load_table()
    derived, _left = derive(subject)
    derived = {**derived, **SUBJECTS[subject]['rendered']}
    gid = dict(base['gid'])
    for k, v in derived.items():
        gid.setdefault(k, v)
    return {**base, 'gid': gid}


def positional(subject, year, check):
    """Repair a scheme .md glyph by glyph: each page's non-space characters are
    aligned with the PDF's own glyph stream (rawdict order; the .md moves the
    page number and some cells), and only a position where the PDF draws an
    UNNAMED glyph (trace U+FFFD) is changed, to the table's reading of that
    glyph's (family, id). A position the .md already reads as the table does
    (the extractor's own repair) is left; one it reads otherwise is refused.
    Run it ONCE, on the .md as extracted: on a file it has already repaired the
    alignment no longer pairs the stand-ins and it reports them unaligned (take
    the unrepaired file from git to re-derive)."""
    import difflib
    from glyph_ids import page_glyphs, page_unnamed
    table = full_table(subject)
    md = os.path.join(ROOT, 'examiner-reports', subject, 'schemes', f'{year}-hl.md')
    text = open(md, encoding='utf-8').read()
    marks = [(m.start(), int(m.group(1))) for m in re.finditer(r'^## Page (\d+)', text, re.M)]
    bounds = {pn: (st, marks[i + 1][0] if i + 1 < len(marks) else len(text)) for i, (st, pn) in enumerate(marks)}
    edits, unresolved, conflicts, missing, absent = {}, collections.Counter(), [], 0, 0
    with pymupdf.open(_pdfs(subject, year)['scheme']) as doc:
        for pn, page in enumerate(doc, 1):
            origin, unnamed = page_glyphs(page), page_unnamed(page)
            raw = []
            for blk in page.get_text('rawdict')['blocks']:
                for line in blk.get('lines', []):
                    for sp in line['spans']:
                        for ch in sp['chars']:
                            if ch['c'].isspace():
                                continue
                            key = (round(ch['origin'][0], 2), round(ch['origin'][1], 2))
                            want = None
                            if key in unnamed:
                                hit = origin.get(key)
                                want = (table.get('cid', {}).get(f'{hit[0]}|{hit[1]}') or table['gid'].get(f'{hit[0]}|{hit[1]}')) if hit else None
                                if want is None:
                                    unresolved[f'{hit[0]}|{hit[1]}' if hit else '?'] += 1
                            raw.append((ch['c'], want))
            st, en = bounds.get(pn, (0, 0))
            pos = [i for i in range(st, en) if not text[i].isspace()]
            mdc = [text[i] for i in pos]
            # the .md's own page marker line is not on the page
            head = len(re.sub(r'\s+', '', f'## Page {pn}'))
            pos, mdc = pos[head:], mdc[head:]
            sm = difflib.SequenceMatcher(None, [c for c, _w in raw], mdc, autojunk=False)
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op == 'equal':
                    for k in range(i2 - i1):
                        c, want = raw[i1 + k]
                        if want is not None and want != c:
                            edits[pos[j1 + k]] = want
                elif op == 'delete':
                    # glyphs the .md does not hold at all (Czech 2015's cover
                    # word): nothing there to repair
                    absent += sum(1 for _c, w in raw[i1:i2] if w is not None)
                else:
                    for k in range(i1, i2):
                        c, want = raw[k]
                        if want is None:
                            continue
                        j = j1 + (k - i1)
                        if j < j2 and mdc[j] == want:
                            continue                            # repaired already
                        if op == 'replace' and j < j2 and i2 - i1 == j2 - j1:
                            conflicts.append((pn, c, want, mdc[j]))
                        else:
                            missing += 1
    if unresolved or conflicts or missing:
        print(f'{md}: refused; unresolved {dict(unresolved)}; conflicts {conflicts[:6]}; unaligned {missing}')
        return 1
    out = list(text)
    for i, want in edits.items():
        out[i] = want
    fixed = ''.join(out)
    changes = collections.Counter(f'{text[i]}->{w}' for i, w in edits.items())
    if not check:
        with open(md, 'w', encoding='utf-8') as fh:
            fh.write(fixed)
    print(f'{md}: {len(edits)} glyphs repaired by position {dict(changes)}; {absent} unnamed glyphs not in the .md')
    return 0


def main():
    subject, cmd = sys.argv[1], sys.argv[2]
    cfg = SUBJECTS[subject]
    if cmd == 'derive':
        table, left = derive(subject)
        for k, v in sorted(table.items()):
            print(f'{k} -> {v!r}')
        for k, v in sorted(left.items()):
            print(f'UNSETTLED {k}: {v}')
        return 0
    year = int(sys.argv[3])
    if cmd == 'scheme' and cfg.get('positional'):
        return positional(subject, year, '--check' in sys.argv)
    table = full_table(subject)
    pdf = _pdfs(subject, year)[cmd]
    with pymupdf.open(pdf) as doc:
        dmap, unresolved, ambiguous = document_map(doc, table, cfg['alphabet'], cfg['suspect'])
    if cmd == 'paper':
        out = os.path.join(HERE, f'glyphmap-{subject}-{year}-paper.json')
        print({f'U+{ord(k):04X}': v for k, v in sorted(dmap.items())}, 'unresolved', unresolved, 'ambiguous', ambiguous)
        if not ambiguous and dmap:
            with open(out, 'w', encoding='utf-8') as fh:
                json.dump(dict(sorted(dmap.items())), fh, ensure_ascii=False, indent=1)
                fh.write('\n')
        return 1 if ambiguous else 0
    md = os.path.join(ROOT, 'examiner-reports', subject, 'schemes', f'{year}-hl.md')
    text = open(md, encoding='utf-8').read()
    real = cfg['alphabet'] | set(cfg['rendered'].values())
    present = ({c for c in MANGLED.findall(text) if c not in real}
               | (cfg['suspect'] & set(text.partition('## Page 2')[2]))
               | {c for c in text if cfg['standin'](c)})
    refused = sorted(c for c in present if c not in dmap or c in ambiguous)
    if refused:
        print(f'{md}: refused, unresolved: ' + ' '.join(f'U+{ord(c):04X}' for c in refused))
        return 1
    suspect = {c: dmap.pop(c) for c in list(dmap) if c in cfg['suspect']}
    fixed = ''.join(dmap.get(c, c) for c in text)
    changes = {f'U+{ord(c):04X}->{dmap[c]}': text.count(c) for c in sorted(present) if c in dmap}
    # A SUSPECT letter is repaired only below the cover (page 1 prints the
    # genuine Irish "Coimisiún na Scrúduithe Stáit" in bold), and only where the
    # .md holds exactly as many as the PDF draws in regular weight.
    head, sep, body = fixed.partition('## Page 2')
    with pymupdf.open(pdf) as doc:
        regular = collections.Counter(ch['c'] for page in doc for blk in page.get_text('rawdict')['blocks']
                                      for line in blk.get('lines', []) for sp in line.get('spans', [])
                                      if 'Bold' not in sp.get('font', '') for ch in sp['chars'] if ch['c'] in cfg['suspect'])
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
