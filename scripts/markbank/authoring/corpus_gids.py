"""What do Calibri's ligature glyphs read as where the PDF is honest? Ligature proof 2 of 3.

    python3 scripts/markbank/authoring/corpus_gids.py tmp/corpus_gids.json    # from the repo root

Reads every marking-scheme PDF in paper-trail-corpus/ and, for Calibri glyph
ids in the ligature ranges (295-339, 405-431, 674 and 882), counts the text
each one is mapped to, with an example context for every alphabetic reading.
Where a document's ToUnicode is sane it names the glyph, so these readings
are the evidence for what the glyph draws.

What it proved (2026-10-12): Calibri gid 425 reads "tt" (109 sane
sightings) and gid 427 reads "tti" (43), so the glyph map's U+01A9 -> "t" and
U+01AB -> "tt" were each one letter short; the repair maps them to "tt" and
"tti". Every repaired word was then read from a crop of its PDF page.
"""
import glob, collections, re, pymupdf, json, sys
TARGET = set(range(295, 340)) | set(range(405, 432)) | {674, 882}
files = sorted(glob.glob('paper-trail-corpus/markingschemes/*/*.pdf'))
seen = collections.defaultdict(collections.Counter)
example = {}
for n, f in enumerate(files):
    try:
        doc = pymupdf.open(f)
    except Exception:
        continue
    for page in doc:
        for sp in page.get_texttrace():
            font = re.sub(r'^[A-Z]{6}\+', '', sp.get('font', ''))
            if not font.startswith('Calibri'):
                continue
            chars = sp['chars']; i = 0
            while i < len(chars):
                u, gid, org = chars[i][0], chars[i][1], chars[i][2]
                text = chr(u) if u >= 0 else ''
                j = i + 1
                while j < len(chars) and chars[j][1] == -1 and abs(chars[j][2][0]-org[0]) < 0.01 and abs(chars[j][2][1]-org[1]) < 0.01:
                    text += chr(chars[j][0]) if chars[j][0] >= 0 else ''; j += 1
                if gid in TARGET:
                    key = f'{font.split(",")[0].split("-")[0]}|{gid}'
                    seen[key][text] += 1
                    if text and all(c.isascii() and c.isalpha() for c in text) and (key, text) not in example:
                        ctx = ''.join(chr(c[0]) if c[0] >= 0 else '' for c in chars[max(0, i-8):j+8])
                        example[(key, text)] = f'{f.split("/")[-2]}/{f.split("/")[-1]} p{page.number+1}: {ctx}'
                i = j
    doc.close()
out = {k: dict(v.most_common(8)) for k, v in sorted(seen.items())}
json.dump(dict(seen=out, examples={f'{k}|{t}': v for (k, t), v in example.items()}), open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('done', len(files))
