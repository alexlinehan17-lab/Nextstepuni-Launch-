#!/usr/bin/env python3
"""Verify original-image readings for the hash-pinned 2014 Ordinary scheme.

Its CID/CFF Mincho font has no ToUnicode. No named identical CFF outlines were
available in the original corpus. Each recovered character is therefore a
direct visual reading of an original-page crop, bound to the exact trace
font, glyph ID, origin and crop digest. Zero-ink spaces are separately proven
from embedded TrueType outlines or a CFF charstring containing only an
optional width and endchar. There is no approximate outline matching or
character-ID arithmetic. This source-archive gate needs only PyMuPDF/stdlib.
"""
import argparse
import collections
import hashlib
import json
import math
import struct
from pathlib import Path

import fitz
from ara_glyphs import font_hashes

ROOT = Path(__file__).resolve().parents[3]
SOURCE = 'examiner-reports/japanese/schemes/2014-ol.pdf'
PIN = '69355ed48177aeaec82eb22b281381acfe9cea433c3a39a8791b88c662472f9f'
PROOF = Path(__file__).parent / 'reviews/japanese-2014-ol-glyph-proof.json'
OUTPUT = Path(__file__).with_name('glyphmap-japanese-2014-ol.json')


def contact_sheet(doc, items):
    """Recreate the exact proof sheet from its bound original PDF crops."""
    with fitz.open() as sheet:
        page = sheet.new_page(width=520, height=75 * math.ceil(len(items) / 8))
        for i, item in enumerate(items):
            x, y = (i % 8) * 65, (i // 8) * 75
            page.insert_text((x + 3, y + 9), f'{item["gid"]} p{item["page"]} *', fontsize=7)
            image = doc[item['page'] - 1].get_pixmap(matrix=fitz.Matrix(8, 8), clip=fitz.Rect(item['crop'])).tobytes('png')
            page.insert_image(fitz.Rect(x + 4, y + 12, x + 61, y + 69), stream=image, keep_proportion=True)
        return page.get_pixmap(matrix=fitz.Matrix(2, 2)).tobytes('png')


def cff_index(data, pos):
    count = struct.unpack_from('>H', data, pos)[0]
    if not count:
        return [], pos + 2
    size = data[pos + 2]
    assert 1 <= size <= 4
    start = pos + 3
    offsets = [int.from_bytes(data[start + i * size:start + (i + 1) * size], 'big') for i in range(count + 1)]
    assert offsets[0] == 1 and offsets == sorted(offsets)
    start += size * (count + 1)
    return [data[start + offsets[i] - 1:start + offsets[i + 1] - 1] for i in range(count)], start + offsets[-1] - 1


def cff_number(data, pos):
    byte = data[pos]
    if 32 <= byte <= 246:
        return byte - 139, pos + 1
    if 247 <= byte <= 250:
        return (byte - 247) * 256 + data[pos + 1] + 108, pos + 2
    if 251 <= byte <= 254:
        return -(byte - 251) * 256 - data[pos + 1] - 108, pos + 2
    if byte in [28, 29]:
        size = 2 if byte == 28 else 4
        return int.from_bytes(data[pos + 1:pos + 1 + size], 'big', signed=True), pos + 1 + size
    if byte == 30:
        # Real operands do not address the two tables needed here.
        pos += 1
        while data[pos] & 15 != 15 and data[pos] >> 4 != 15:
            pos += 1
        return None, pos + 1
    raise AssertionError(('Unexpected CFF number', byte))


def cff_blank_program(data, cid):
    assert data[0] == 1
    _names, end = cff_index(data, data[2])
    dictionaries, _end = cff_index(data, end)
    assert len(dictionaries) == 1
    dictionary, values, stack, pos = dictionaries[0], {}, [], 0
    while pos < len(dictionary):
        byte = dictionary[pos]
        if byte <= 21:
            operator = (12, dictionary[pos + 1]) if byte == 12 else byte
            pos += 2 if byte == 12 else 1
            values[operator], stack = stack, []
        else:
            value, pos = cff_number(dictionary, pos)
            stack.append(value)
    charstrings, _end = cff_index(data, values[17][0])
    pos = values[15][0]
    assert pos > 2, 'CID font must have an explicit charset'
    format_ = data[pos]
    pos += 1
    charset = [0]
    if format_ == 0:
        charset += list(struct.unpack_from('>' + 'H' * (len(charstrings) - 1), data, pos))
    else:
        assert format_ in [1, 2]
        while len(charset) < len(charstrings):
            first = struct.unpack_from('>H', data, pos)[0]
            count = data[pos + 2] if format_ == 1 else struct.unpack_from('>H', data, pos + 2)[0]
            pos += 3 if format_ == 1 else 4
            charset += list(range(first, first + count + 1))
    assert len(charset) == len(charstrings)
    program = charstrings[charset.index(cid)]
    pos, operands = 0, 0
    while pos < len(program):
        if program[pos] == 14:
            # Four/five endchar operands are seac, which can paint an accent.
            assert pos == len(program) - 1 and operands <= 1
            return program.hex()
        assert program[pos] == 28 or program[pos] >= 32
        if program[pos] == 255:
            pos += 5
        else:
            _value, pos = cff_number(program, pos)
        operands += 1
    raise AssertionError('Blank CFF glyph has no endchar')


def derive():
    original = ROOT / SOURCE
    assert hashlib.sha256(original.read_bytes()).hexdigest() == PIN
    proof = json.loads(PROOF.read_text())
    assert proof['source'] == SOURCE and proof['sha256'] == PIN
    proof_digest = hashlib.sha256(PROOF.read_bytes()).hexdigest()
    for sheet in proof['sheets']:
        assert hashlib.sha256((ROOT / sheet['path']).read_bytes()).hexdigest() == sheet['sha256']
    with fitz.open(original) as doc:
        by_id = {item['gid']: item for item in proof['glyphs']}
        for sheet in proof['sheets']:
            assert set(sheet['gids']) <= set(by_id)
            rendered = contact_sheet(doc, [by_id[gid] for gid in sheet['gids']])
            assert hashlib.sha256(rendered).hexdigest() == sheet['sha256'], 'Proof contact sheet differs from its original PDF crops'
        locations = collections.defaultdict(list)
        for page in doc:
            for span in page.get_texttrace():
                for uni, gid, origin, _bbox in span['chars']:
                    if uni == 65533:
                        locations[(span['font'], gid)].append({'page': page.number + 1, 'origin': [round(value, 3) for value in origin]})
        entries = {}
        for item in proof['glyphs']:
            key = (item['font'], item['gid'])
            assert key not in entries and len(item['text']) == 1 and item['text'] != '\ufffd'
            assert {'page': item['page'], 'origin': item['origin']} in locations[key]
            rendered = doc[item['page'] - 1].get_pixmap(matrix=fitz.Matrix(8, 8), clip=fitz.Rect(item['crop'])).tobytes('png')
            assert hashlib.sha256(rendered).hexdigest() == item['imageSha256'], key
            assert item['contactSheet'] in {sheet['path'] for sheet in proof['sheets']}
            entries[key] = {'text': item['text'], 'outlines': [], 'evidence': [{
                'visualProof': str(PROOF.relative_to(ROOT)), 'sha256': proof_digest,
                'page': item['page'], 'origin': item['origin'], 'imageSha256': item['imageSha256']}]}
        fonts = {}
        for page in doc:
            for info in page.get_fonts(full=True):
                name = info[3].split('+')[-1].removesuffix('-Identity-H')
                if name in fonts:
                    continue
                fonts[name] = (info[1], doc.extract_font(info[0])[3])
        for name in ['Calibri', 'MSMincho']:
            kind, data = fonts[name]
            evidence = {'fontSha256': hashlib.sha256(data).hexdigest()}
            if kind == 'ttf':
                _hashes, blanks = font_hashes(data)
                assert 3 in blanks
                evidence['method'] = 'empty-original-TrueType-glyf'
            else:
                evidence['method'] = 'original-CFF-optional-width-and-endchar-only'
                evidence['charstringHex'] = cff_blank_program(data, 3)
            entries[(name, 3)] = {'text': ' ', 'outlines': [], 'evidence': [evidence]}
    repairs, missing = {}, []
    for (font, gid), places in sorted(locations.items()):
        if (font, gid) in entries:
            repairs.setdefault(font, {})[str(gid)] = entries[(font, gid)]
        else:
            assert all(place['page'] >= 11 for place in places), ('Required glyph not visually read', font, gid, places)
            missing.append({'font': font, 'gid': gid, 'occurrences': len(places), 'outlines': [], 'locations': places,
                            'presentation': 'Original transcript PDF image only; forbidden in published text'})
    return {'source': SOURCE, 'sha256': PIN, 'outlineMethod': 'original-image-glyph-crops-and-proven-zero-ink-spaces',
            'repairs': repairs, 'unresolvedImageOnly': missing}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.write:
        OUTPUT.write_text(rendered)
    else:
        assert OUTPUT.read_text() == rendered, 'Regenerated 2014 glyph proof differs'
    print(f'{sum(len(mapping) for mapping in result["repairs"].values())} source-proven glyph repairs; {len(result["unresolvedImageOnly"])} transcript-only survivors')
