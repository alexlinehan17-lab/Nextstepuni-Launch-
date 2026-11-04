#!/usr/bin/env python3
"""Derive the glyph-id repair table (glyph_ids.json) from the subjects' PDFs.

The character a broken subset font reports is not evidence of anything: the
same code point means different glyphs in different PDFs (see
scripts/markbank/glyph_ids.py). This learns from the glyph id instead.

For every mangled character drawn in a listed subject's paper or scheme, join it to
its (font family, glyph id) by drawing origin. Where the SAME family and id is
drawn elsewhere with a sane ToUnicode -- including a multi-character ligature,
which MuPDF reports as the glyph followed by id -1 continuations at the same
origin -- that reading is the glyph, provided it is near-unanimous (AGREEMENT)
and the id is high enough not to be renumbered per subset (MIN_DERIVED_GID). An
id whose sane readings disagree is dropped, never voted on.

A sane ToUnicode is not always an honest one. Some text layers report Calibri's
"tt" ligature (gid 425) as a single "t" ("batle" for "battle"): that is a sane
character, so it can outvote the truth. The ligature ids are therefore SETTLED
below, and repair_ligature_words.py uses the glyph lengths the text trace
records to find every word such a layer shortened.

Two kinds of entry are not derivable that way and are SETTLED instead, each
by cropping the glyph out of the page it is drawn on and looking at it; the
page and the word it sits in are recorded so the call can be re-checked:

* Calibri ligatures that are never drawn with a sane ToUnicode anywhere in the
  corpus of these subjects.
* Symbol-font code points (Wingdings, Wingdings 2, Symbol). A simple font's
  private-use code point is 0xF000 + its own character code, which names the
  glyph; its subset glyph ids are renumbered per PDF, so they are keyed by code.

A glyph a CID font draws with NO Unicode (U+FFFD in the text trace) reaches
rawdict as its own glyph id -- a control character or a plain letter, which no
code-point gate can see (2017 HL scheme "/($9,1*" for "LEAVING", 2016 OL
"W\x04z\x1c" for "PAYE"). CID fonts keep the original font's glyph order, so
these are derived from the sane sightings of the same family and id in CID
fonts only, at any id: the renumbering that MIN_DERIVED_GID guards against
happens in simple-font subsets, which this evidence excludes. They are written
to byCidGlyphId, which only an unnamed CID glyph consults.

Whatever is still unresolved is printed. Nothing here guesses: the gates in
test/markBankSchemes.test.ts and test/businessGlyphs.test.ts refuse residue.

    python3 scripts/markbank/authoring/derive_glyph_ids.py [--subjects a,b] [--write]

The table is written from the Business corpus alone (its default); --subjects
scans other subjects listed in SUBJECT_CODES for evidence without writing their
real Greek and maths symbols into the Business repairs.
"""
import collections
import glob
import json
import os
import re
import sys

import pymupdf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from glyph_ids import MANGLED, TABLE_PATH, cid_fonts, family  # noqa: E402

PUA_SYMBOL = range(0xF000, 0xF100)

# Settled by cropping the glyph from the page and reading it in its word.
SETTLED_GID = [
    dict(font='Calibri', gid=425, text='tt', evidence='rendered "battle", "attacked", "battles", "settle", "little", "letters" (2023 OL Latin scheme pp. 3, 5, 7, 8), '
         '"written", "omitted", "attempt", "pipette", "bottom", "nettles", "settling" (2024 OL Chemistry scheme pp. 3, 7, 9), '
         '"attempted", "attendance", "letter", "attention", "matter", "pattern" (2025 OL Religious Education scheme pp. 6-32), '
         '"Cigarette butts", "bottle" (2023 HL Portuguese scheme p. 9), "plotted" (2025 HL Physics scheme p. 8), "battery", '
         '"attached", "shuttle", "bottles" (2019 Technology schemes) and "letters" (Business). Some text layers read this glyph as '
         '"t" ("batle", "litle", "ploted"), the rest as U+01A9: every one of 1,221 U+01A9 sightings in 4,284 English papers and '
         'schemes is this glyph id. A lossy ToUnicode, never a "t".'),
    dict(font='Calibri', gid=427, text='tti', evidence='2025 OL Business scheme pp. 14 and 19: "Sometimes by putting the complaint", '
         '"cutting down on communication"; 2026 OL Religious Education scheme p. 4 "by setting"; 2024 OL Religious Education '
         'scheme p. 7 "committing"; 2021 OL Technology paper p. 2 "light emitting diodes"; 2019 Technology schemes "fittings", '
         '"Cutting blade"; 2024 HL Engineering scheme "Thermosetting", "Scottish"; 2025 HL Italian scheme "Infatti", "settimana", '
         '"progetti". Every one of 364 U+01AB sightings in the English corpus is this glyph id; the shared character map turned it '
         'into "tt" and shipped "settng".'),
    dict(font='Calibri', gid=414, text='tf', evidence='2025 OL scheme p. 34: "it predicts inflows and outflows"; the text '
         'layer reads "ouƞlows".'),
    dict(font='Calibri', gid=332, text='ft', evidence='2025 OL paper p. 3 "the word TRUE or FALSE after each", p. 7 '
         '"A Bank Overdraft"; 2025 OL scheme p. 33 (bold) "Draft the Notice and Agenda"; the text layer reads "aŌer", "DraŌ".'),
    dict(font='Calibri', gid=674, text="'", evidence='2021 HL scheme p. 51: "Competitors \' see what competitor is doing"; '
         'drawn as a short raised tick, reported as U+0374. Never drawn with a sane ToUnicode in the Business corpus.'),
    dict(font='Calibri', gid=882, text='-', evidence='2012 HL Irish scheme p. 16: "Aschur ina aonaid - \u2019000", a hyphen. '
         'Its sane readings split between U+002D and U+2010, both the hyphen, so the id fails the agreement rule.'),
    dict(font='Calibri', gid=304, text='f\u00ed', evidence='2026 HL Irish ABQ booklet pp. 8-9: "fíonta", "Cóimheas fíorthástála"; '
         'drawn with a sane ToUnicode as "fí" 15 times elsewhere in the SEC scheme corpus.'),
]
# Glyphs a CID font draws with no Unicode whose id has no unanimous sane CID
# sighting, settled by crop. They join byCidGlyphId, never byGlyphId.
SETTLED_CID = [
    dict(font='Calibri', gid=3, text=' ', evidence='2016 OL scheme p. 4: "the candidate\u2019s answer in order to merit the assigned marks", '
         'drawn blank between the words and reported as U+0003. Its sane readings split between U+0020 and U+00A0, both a space, so the id '
         'fails the agreement rule.'),
    dict(font='MinionPro', gid=1, text=' ', evidence='2016 OL scheme pp. 17 and 20: a blank 2.7pt glyph at the end of "Shareholders only '
         'lose what they invest into the" and "sees an opportunity and uses his initiative to set up the", reported as U+0001; nothing is drawn.'),
    dict(font='Symbol', gid=120, text='\u2022', evidence='2016 OL scheme pp. 4, 10, 17 and 20: the round bullet before "The support notes '
         'presented are not exclusive", drawn by a CID Symbol font with no Unicode and reported as "x"; SymbolMT gid 120 is "\u2022".'),
]
SETTLED_CODE = [
    dict(font='Wingdings', code='F0FC', text='✓', evidence='2023 OL paper p. 7 and 2026 OL paper p. 4: "by placing a tick (✓) '
         'in the correct box"; the scheme annotation table glosses it as a correct response.'),
    dict(font='Wingdings', code='F08C', text='❶', evidence='2018 HL scheme p. 56: "25,450❶ x 0.40", "10,180❶": a black circled 1 keying a working.'),
    dict(font='Wingdings', code='F08D', text='❷', evidence='2018 HL scheme p. 56: "60,000❷ (2 marks)".'),
    dict(font='Wingdings', code='F08E', text='❸', evidence='2018 HL scheme p. 56: "6,910❸", "60.06❸".'),
    dict(font='Wingdings', code='F08F', text='❹', evidence='2021 HL scheme p. 52: "❹" beside the TC and BEP labels of the chart.'),
    dict(font='Wingdings', code='F0A7', text='▪', evidence='2012 HL scheme p. 28: the small square bullet before '
         '"Metro North and Metro West" and "The underground Dart".'),
    dict(font='Wingdings2', code='F075', text='❶', evidence='2022 HL scheme p. 15: "staff@superstore.ie ❶", "GDPR ❶".'),
    dict(font='Wingdings2', code='F076', text='❷', evidence='2022 HL scheme p. 20: "6280 ❷", "= €6280 ❷".'),
    dict(font='Wingdings2', code='F078', text='❹', evidence='2022 HL scheme p. 20: "9680 ❹", "3400 ❹".'),
    dict(font='Wingdings', code='F076', text='\u2756', evidence='2014 OL scheme p. 20: the four-diamond bullet before '
         '"Jordan\u2019s strength is his knowledge" and "Jordan is aware of his weakness".'),
    dict(font='Wingdings', code='F0E2', text='\u2193', evidence='2010 OL scheme p. 11: the downward arrow between the boxes of a process chart.'),
    dict(font='Wingdings', code='F046', text='\u261e', evidence='2010 HL paper p. 1 (and its Irish edition): the pointing hand '
         'before "Write your Examination Number here".'),
    dict(font='SymbolMT', code='F0B4', text='\u00d7', evidence='2012 OL scheme p. 10: "Gross Profit / Sales × 100/1 = 84,000/420,000 × 100/1 = 20%".'),
    dict(font='Symbol', code='F0B7', text='•', evidence='Opens every bullet in "How to use the marking scheme" '
         '(scripts/markbank/markbank_text.py); drawn as a round bullet.'),
    dict(font='SymbolMT', code='F0B7', text='•', evidence='The same Symbol bullet under its MT name; SymbolMT gid 120 '
         'is read as "•" 2,265 times where its ToUnicode is sane.'),
]


# The subjects whose papers and schemes the table is derived from, by SEC
# subject code. A subject joins when its text needs glyph-id repair.
SUBJECT_CODES = {
    'business': 'LC033', 'religious-education': 'LC223', 'technology': 'LC065',
    'latin': 'LC006', 'physics': 'LC021', 'chemistry': 'LC022', 'portuguese': 'LC018',
    'dutch': 'LC017', 'italian': 'LC013', 'engineering': 'LC027', 'polish': 'LC548',
}

# Derived entries need near-unanimous agreement and a high glyph id. Low ids are
# renumbered in some subsets: across these subjects Calibri gid 4 reads "A"
# 16,245 times but "o" 492 times, so a low id is never trusted from volume.
AGREEMENT = 0.99
MIN_DERIVED_GID = 200


def subject_pdfs(subjects=None):
    codes = [SUBJECT_CODES[s] for s in (subjects or SUBJECT_CODES)]
    return sorted(f for c in codes for f in glob.glob(f'paper-trail-corpus/markingschemes/*/{c}*.pdf')
                  + glob.glob(f'paper-trail-corpus/exampapers/*/{c}*.pdf'))


def scan(files):
    clean = collections.defaultdict(collections.Counter)   # (family, gid) -> Counter(text)
    clean_cid = collections.defaultdict(collections.Counter)  # the same, from CID fonts only
    mangled = collections.Counter()                         # (family, gid, char) -> sightings
    unnamed = collections.Counter()                         # (family, gid) -> CID sightings with no Unicode
    for f in files:
        doc = pymupdf.open(f)
        for page in doc:
            origin = {}
            cids = cid_fonts(page)
            for sp in page.get_texttrace():
                fam = family(sp.get('font', ''))
                cid = re.sub(r'^[A-Z]{6}\+', '', sp.get('font', '')) in cids
                chars = sp['chars']
                i = 0
                while i < len(chars):
                    u, gid, org = chars[i][0], chars[i][1], chars[i][2]
                    text = chr(u) if u >= 0 else ''
                    j = i + 1
                    while (j < len(chars) and chars[j][1] == -1 and abs(chars[j][2][0] - org[0]) < 0.01
                           and abs(chars[j][2][1] - org[1]) < 0.01):
                        text += chr(chars[j][0]) if chars[j][0] >= 0 else ''
                        j += 1
                    if gid >= 0:
                        origin[(round(org[0], 2), round(org[1], 2))] = (fam, gid)
                        if text.strip() and not MANGLED.search(text):
                            clean[(fam, gid)][text] += 1
                        # A CID sighting may be a space: unnamed spaces are repaired too.
                        if cid and text and not MANGLED.search(text) and all(ord(t) >= 32 for t in text):
                            clean_cid[(fam, gid)][text] += 1
                        if cid and text == '\ufffd':
                            unnamed[(fam, gid)] += 1
                    i = j
            for blk in page.get_text('rawdict')['blocks']:
                for line in blk.get('lines', []):
                    for sp in line.get('spans', []):
                        for ch in sp['chars']:
                            if MANGLED.match(ch['c']):
                                key = origin.get((round(ch['origin'][0], 2), round(ch['origin'][1], 2)))
                                if key:
                                    mangled[(key[0], key[1], ch['c'])] += 1
        doc.close()
    return clean, mangled, clean_cid, unnamed


def main():
    # The table is derived from the Business corpus, whose fonts it was built
    # for; --subjects a,b widens the scan to gather evidence for other subjects
    # without letting their real Greek and maths symbols vote on Business glyphs.
    chosen = ['business']
    if '--subjects' in sys.argv:
        chosen = sys.argv[sys.argv.index('--subjects') + 1].split(',')
    files = subject_pdfs(chosen)
    if not files:
        sys.exit('no subject PDFs found -- run from the repo root')
    clean, mangled, clean_cid, unnamed = scan(files)
    by_gid, dropped = {}, []
    for (fam, gid, ch), n in mangled.most_common():
        if ord(ch) in PUA_SYMBOL:
            continue
        counts = clean.get((fam, gid))
        if not counts or gid < MIN_DERIVED_GID:
            continue
        real = max(counts, key=counts.get)
        if counts[real] < sum(counts.values()) * AGREEMENT:
            dropped.append((fam, gid, dict(counts)))
            continue
        by_gid.setdefault(f'{fam}|{gid}', dict(font=fam, gid=gid, text=real,
                          evidence=f'derived: {counts[real]} sane sighting(s) of this glyph id'))
    # Glyphs a CID font draws with no Unicode, read from CID sightings only.
    settled = {f'{e["font"]}|{e["gid"]}' for e in SETTLED_GID + SETTLED_CID}
    by_cid = {}
    for (fam, gid), n in unnamed.most_common():
        key = f'{fam}|{gid}'
        counts = clean_cid.get((fam, gid))
        if key in by_gid or key in settled or not counts:
            continue
        real = max(counts, key=counts.get)
        if counts[real] < sum(counts.values()) * AGREEMENT:
            dropped.append((fam, gid, dict(counts)))
            continue
        by_cid[key] = dict(font=fam, gid=gid, text=real, evidence=f'derived: {counts[real]} sane sighting(s) of this glyph id in CID fonts')
    for e in SETTLED_CID:
        by_cid[f'{e["font"]}|{e["gid"]}'] = dict(e, evidence='settled by crop: ' + e['evidence'])
    for e in SETTLED_GID:
        key = f'{e["font"]}|{e["gid"]}'
        if key in by_gid:
            assert by_gid[key]['text'] == e['text'], (key, by_gid[key], e)
            continue
        by_gid[key] = dict(e, evidence='settled by crop: ' + e['evidence'])
    by_code = {f'{e["font"]}|{e["code"]}': dict(e, evidence='settled by crop: ' + e['evidence']) for e in SETTLED_CODE}

    residue = collections.Counter()
    for (fam, gid, ch), n in mangled.items():
        if f'{fam}|{gid}' in by_gid or f'{fam}|{ord(ch):04X}' in by_code:
            continue
        residue[(fam, gid, ch)] += n
    for (fam, gid), n in unnamed.items():
        if f'{fam}|{gid}' not in by_gid and f'{fam}|{gid}' not in by_cid:
            residue[(fam, gid, '\ufffd')] += n
    total = sum(mangled.values()) + sum(unnamed.values())
    print(f'{len(files)} subject PDFs; {total} mangled glyph sightings; '
          f'{len(by_gid)} glyph-id entries, {len(by_cid)} CID glyph-id entries, {len(by_code)} code-point entries; dropped {len(dropped)} self-disagreeing ids')
    print(f'unresolved: {sum(residue.values())} sightings of {len(residue)} glyphs')
    for (fam, gid, ch), n in residue.most_common(40):
        print(f'   {fam} gid {gid} U+{ord(ch):04X} x{n}')
    if '--write' in sys.argv:
        out = dict(note='Generated by scripts/markbank/authoring/derive_glyph_ids.py. Do not hand-edit; add a settled entry there.',
                   byGlyphId=sorted(by_gid.values(), key=lambda e: (e['font'], e['gid'])),
                   byCodePoint=sorted(by_code.values(), key=lambda e: (e['font'], e['code'])),
                   byCidGlyphId=sorted(by_cid.values(), key=lambda e: (e['font'], e['gid'])))
        TABLE_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(f'wrote {TABLE_PATH}')


if __name__ == '__main__':
    main()
