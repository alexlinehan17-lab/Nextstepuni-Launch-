#!/usr/bin/env python3
"""Verify direct original-image readings for the 2010 Ordinary CFF scheme.

The PDF's text trace identifies missing ToUnicode entries by font/GID even
where ordinary extraction substitutes misleading non-Japanese code points.
Every nonblank repair is an independently read original glyph crop, bound to
the exact original SHA256, font, GID and origin. No approximate outlines,
Unicode offsets, language-based substitutions or external font are used.
Blank spaces are proven by the original CFF program. PyMuPDF/stdlib only.
"""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path

import fitz
from ja_glyph_derive_2014 import cff_blank_program

ROOT = Path(__file__).resolve().parents[3]
SOURCE = 'examiner-reports/japanese/schemes/2010-ol.pdf'
PIN = '096c546ef66b119647c04d4e401ad0845819859fba602e9e2ca8d237a14ac080'
PROOF = Path(__file__).parent / 'reviews/japanese-2010-ol-glyph-proof.json'
OUTPUT = Path(__file__).with_name('glyphmap-japanese-2010-ol.json')
ALIASES = {'MSMincho': 'M', 'MS-PMincho': 'P', 'MS-Gothic': 'G', 'SimSun': 'S', 'TimesNewRomanPSMT': 'T'}


def contact_sheet(doc, items):
    with fitz.open() as sheet:
        page = sheet.new_page(width=520, height=75 * math.ceil(len(items) / 8))
        for index, item in enumerate(items):
            x, y = (index % 8) * 65, (index // 8) * 75
            page.insert_text((x + 3, y + 9), f'{ALIASES[item["font"]]} {item["gid"]} p{item["page"]} *', fontsize=7)
            cropped = doc[item['page'] - 1].get_pixmap(matrix=fitz.Matrix(8, 8), clip=fitz.Rect(item['crop'])).tobytes('png')
            page.insert_image(fitz.Rect(x + 4, y + 12, x + 61, y + 69), stream=cropped, keep_proportion=True)
        return page.get_pixmap(matrix=fitz.Matrix(2, 2)).tobytes('png')


def derive():
    original = ROOT / SOURCE
    assert hashlib.sha256(original.read_bytes()).hexdigest() == PIN
    proof = json.loads(PROOF.read_text())
    assert proof['source'] == SOURCE and proof['sha256'] == PIN
    proof_digest = hashlib.sha256(PROOF.read_bytes()).hexdigest()
    by_key = {(item['font'], item['gid']): item for item in proof['glyphs']}
    assert len(by_key) == len(proof['glyphs']) == 154
    with fitz.open(original) as doc:
        locations = collections.defaultdict(list)
        for page in doc:
            for span in page.get_texttrace():
                for uni, gid, origin, _bbox in span['chars']:
                    if uni == 65533:
                        locations[(span['font'], gid)].append({'page': page.number + 1, 'origin': [round(value, 3) for value in origin]})
        covered = []
        for sheet in proof['sheets']:
            keys = [tuple(key) for key in sheet['glyphKeys']]
            assert all(key in by_key for key in keys)
            covered.extend(keys)
            assert hashlib.sha256((ROOT / sheet['path']).read_bytes()).hexdigest() == sheet['sha256']
            rendered = contact_sheet(doc, [by_key[key] for key in keys])
            assert hashlib.sha256(rendered).hexdigest() == sheet['sha256'], 'Proof sheet differs from its original PDF crops'
        assert len(covered) == len(set(covered)) and set(covered) == set(by_key)
        entries = {}
        for key, item in by_key.items():
            assert len(item['text']) == 1 and item['text'] != '\ufffd'
            assert {'page': item['page'], 'origin': item['origin']} in locations[key]
            rendered = doc[item['page'] - 1].get_pixmap(matrix=fitz.Matrix(8, 8), clip=fitz.Rect(item['crop'])).tobytes('png')
            assert hashlib.sha256(rendered).hexdigest() == item['imageSha256'], key
            assert item['contactSheet'] in {sheet['path'] for sheet in proof['sheets']}
            entries[key] = {'text': item['text'], 'outlines': [], 'evidence': [{
                'visualProof': str(PROOF.relative_to(ROOT)), 'sha256': proof_digest,
                'page': item['page'], 'origin': item['origin'], 'imageSha256': item['imageSha256'],
                'fontSha256': proof['fonts'][item['font']]['sha256']}]}
        fonts = {}
        for page in doc:
            for info in page.get_fonts(full=True):
                if info[1] != 'cid':
                    continue
                name = info[3].split('+')[-1].removesuffix('-Identity-H')
                data = doc.extract_font(info[0])[3]
                assert name not in fonts or fonts[name] == data
                fonts[name] = data
        assert set(fonts) == set(proof['fonts'])
        for name, data in fonts.items():
            assert hashlib.sha256(data).hexdigest() == proof['fonts'][name]['sha256']
            assert len(data) == proof['fonts'][name]['bytes']
        for item in proof['blankGlyphs']:
            key = (item['font'], item['gid'])
            assert key not in entries and key in locations
            data = fonts[item['font']]
            assert hashlib.sha256(data).hexdigest() == item['fontSha256']
            program = cff_blank_program(data, item['gid'])
            entries[key] = {'text': ' ', 'outlines': [], 'evidence': [{
                'method': 'original-CFF-optional-width-and-endchar-only',
                'fontSha256': item['fontSha256'], 'charstringHex': program}]}
        assert len(entries) == 156 and set(entries) == set(locations), 'Missing or unreviewed original glyph identity'
    repairs = {}
    for (font, gid), entry in sorted(entries.items()):
        repairs.setdefault(font, {})[str(gid)] = entry
    return {'source': SOURCE, 'sha256': PIN,
            'outlineMethod': 'original-image-glyph-crops-and-proven-zero-ink-spaces',
            'repairs': repairs, 'unresolvedImageOnly': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.write:
        OUTPUT.write_text(rendered)
    else:
        assert OUTPUT.read_text() == rendered, 'Regenerated 2010 glyph proof differs'
    print('154 original-image readings +2 proven blank glyphs; all156 missing identities recovered')
