"""Recover only the hash-pinned 2017 written PDF's missing ToUnicode glyphs.

The repair table is derived from identical embedded TrueType glyph outlines in
original PDFs, with source paths/hashes retained, never from a manually guessed character mapping.
Known characters and every other PDF are unchanged. Missing derivation fails.
"""
import hashlib
import json
from functools import lru_cache
from pathlib import Path

MANIFEST = Path(__file__).with_name('glyphmap-japanese-2017.json')


@lru_cache(maxsize=1)
def manifest():
    return json.loads(MANIFEST.read_text())


@lru_cache(maxsize=64)
def document_repairs(name, modified, size):
    data = manifest()
    digest = hashlib.sha256(Path(name).read_bytes()).hexdigest()
    return data if digest == data['sha256'] else None


def repaired_rawdict(page, raw):
    name = page.parent.name
    if not name:
        return raw
    path = Path(name)
    if not path.is_file():
        return raw
    stat = path.stat()
    repairs = document_repairs(str(path.resolve()), stat.st_mtime_ns, stat.st_size)
    if repairs is None:
        return raw
    unresolved = {(item['font'], item['gid']) for item in repairs['unresolvedImageOnly']}
    replacement = {}
    blank_keys = set()
    for span in page.get_texttrace():
        for uni, gid, origin, _bbox in span['chars']:
            if uni != 65533:
                continue
            entry = repairs['repairs'].get(span['font'], {}).get(str(gid))
            assert entry is not None or (span['font'], gid) in unresolved, f'Unreviewed glyph: {name} p{page.number + 1} {span["font"]} gid{gid}'
            text = entry['text'] if entry else '\ufffd'
            key = (span['font'], tuple(round(value, 3) for value in origin))
            assert key not in replacement or replacement[key] == text, key
            replacement[key] = text
            if entry and not entry["outlines"] and text == " ":
                blank_keys.add(key)
    found = set()
    for block in raw['blocks']:
        if block['type'] != 0:
            continue
        for line in block['lines']:
            for span in line['spans']:
                for char in span['chars']:
                    key = (span['font'], tuple(round(value, 3) for value in char['origin']))
                    if key in replacement:
                        char['c'] = replacement[key]
                        found.add(key)
    # The trace includes an overlapping zero-ink word space after one answer
    # underline that rawdict collapses. Every drawn glyph must still match its
    # exact origin; only proven blank outlines may have no separate raw char.
    assert set(replacement) - found <= blank_keys, f'Glyph origin did not match raw text: {name} p{page.number + 1}'
    return raw
