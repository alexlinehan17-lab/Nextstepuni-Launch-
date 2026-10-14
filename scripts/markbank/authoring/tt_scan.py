"""Which glyph is behind U+01A9 and U+01AB, and where is it read wrongly? Ligature proof 1 of 3.

    python3 scripts/markbank/authoring/tt_scan.py tmp/tt_scan.json    # from the repo root

Reads every English paper and scheme PDF in paper-trail-corpus/ and records,
for the two private code points the shared glyph map repaired (U+01A9 "Ʃ" and
U+01AB "ƫ"), the font family and glyph id each sighting is drawn with and the
character that follows it. It also counts where Calibri glyph 425 or 427
carries a lossy ToUnicode entry ("t" for 425, "t"/"tt" for 427), the source of
misreads such as "batle".

What it proved (2026-10-12, 4,284 PDFs): all 1,221 U+01A9 sightings are
Calibri gid 425 and all 364 U+01AB sightings are Calibri gid 427, so each
code point stands for one glyph and the map can be corrected per code point.
Calibri 425 is read as a bare "t" 280 times in 9 documents.
"""
import sys, glob, collections, re, json
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # scripts/markbank, for glyph_ids
import pymupdf
from glyph_ids import family
files = sorted(glob.glob('paper-trail-corpus/markingschemes/*/*EV.pdf') + glob.glob('paper-trail-corpus/exampapers/*/*EV.pdf'))
cp = collections.defaultdict(collections.Counter)        # char -> Counter((fam,gid))
nextch = collections.defaultdict(collections.Counter)    # char -> Counter(next char)
lossy = collections.defaultdict(collections.Counter)     # (fam,gid) -> Counter(doc) where reading is 't' / 'tt' for 425/427
words = collections.defaultdict(set)
for n, f in enumerate(files):
    try: doc = pymupdf.open(f)
    except Exception: continue
    name = f.split('corpus/')[1]
    for page in doc:
        try:
            origin = {}
            tt = page.get_texttrace()
        except Exception:
            continue
        for sp in tt:
            fam = family(sp.get('font', ''))
            chars = sp['chars']; i = 0
            while i < len(chars):
                u, gid, org = chars[i][0], chars[i][1], chars[i][2]
                text = chr(u) if u >= 0 else ''
                j = i + 1
                while j < len(chars) and chars[j][1] == -1 and abs(chars[j][2][0]-org[0]) < 0.01 and abs(chars[j][2][1]-org[1]) < 0.01:
                    text += chr(chars[j][0]) if chars[j][0] >= 0 else ''; j += 1
                if gid >= 0:
                    origin[(round(org[0], 2), round(org[1], 2))] = (fam, gid)
                    if fam == 'Calibri' and ((gid == 425 and text == 't') or (gid == 427 and text in ('tt', 't'))):
                        lossy[(fam, gid, text)][name] += 1
                i = j
        for blk in page.get_text('rawdict')['blocks']:
            for line in blk.get('lines', []):
                for sp in line.get('spans', []):
                    cs = sp['chars']
                    for k, ch in enumerate(cs):
                        if ch['c'] in ('Ʃ', 'ƫ'):
                            key = origin.get((round(ch['origin'][0], 2), round(ch['origin'][1], 2)))
                            cp[ch['c']][key] += 1
                            nx = cs[k + 1]['c'] if k + 1 < len(cs) else ' '
                            nextch[ch['c']][nx] += 1
    doc.close()
out = dict(codepoints={c: {str(k): v for k, v in cnt.items()} for c, cnt in cp.items()},
           next={c: dict(cnt.most_common(15)) for c, cnt in nextch.items()},
           lossy={f'{k[0]}|{k[1]}|{k[2]}': dict(v) for k, v in lossy.items()}, files=len(files))
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('done', len(files))
