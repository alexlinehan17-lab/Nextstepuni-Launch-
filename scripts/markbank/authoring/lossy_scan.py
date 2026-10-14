"""Which glyphs does a subject's text layer read inconsistently? Ligature proof 3 of 3.

    python3 scripts/markbank/authoring/lossy_scan.py tmp/lossy.json LC020,LC033    # from the repo root

Reads the English paper and scheme PDFs for the given SEC subject codes and,
per font family and glyph id, tallies every reading the text layer gives.
A glyph with a multi-letter reading, or one read as a private-use or Latin
Extended code point, is listed with the documents behind each reading. A
ligature glyph read two ways (Calibri 425 as "tt" in one file and "t" in
another) is a lossy ToUnicode, and every word built on the short reading is
a misread to repair.

This is how the misread words were found subject by subject before the
repair, and how a subject is re-checked afterwards.
"""
import sys, glob, collections, re, json
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # scripts/markbank, for glyph_ids
import pymupdf
from glyph_ids import family
codes = sys.argv[2].split(',')
files = sorted(f for c in codes for f in glob.glob(f'paper-trail-corpus/markingschemes/*/{c}*EV.pdf') + glob.glob(f'paper-trail-corpus/exampapers/*/{c}*EV.pdf'))
readings = collections.defaultdict(collections.Counter)
docs = collections.defaultdict(set)
for f in files:
    try: doc = pymupdf.open(f)
    except Exception: continue
    for page in doc:
        for sp in page.get_texttrace():
            fam = family(sp.get('font', ''))
            chars = sp['chars']; i = 0
            while i < len(chars):
                u, gid, org = chars[i][0], chars[i][1], chars[i][2]
                text = chr(u) if u >= 0 else ''
                j = i + 1
                while j < len(chars) and chars[j][1] == -1 and abs(chars[j][2][0]-org[0]) < 0.01 and abs(chars[j][2][1]-org[1]) < 0.01:
                    text += chr(chars[j][0]) if chars[j][0] >= 0 else ''; j += 1
                if gid >= 0:
                    readings[(fam, gid)][text] += 1
                    docs[(fam, gid, text)].add(f.split('corpus/')[1])
                i = j
    doc.close()
out = []
for (fam, gid), c in readings.items():
    rs = [r for r in c if r]
    multi = [r for r in rs if len(r) > 1 and r.isalpha()]
    weird = [r for r in rs if any(ord(ch) > 0x2000 or 0x100 <= ord(ch) < 0x370 for ch in r)]
    if multi or weird:
        out.append(dict(font=fam, gid=gid, readings=dict(c.most_common(8)),
                        docs={r: sorted(docs[(fam, gid, r)])[:4] for r in c if r in multi + weird or len(c) > 1}))
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
for o in sorted(out, key=lambda o: (o['font'], o['gid'])):
    print(o['font'], o['gid'], o['readings'])
