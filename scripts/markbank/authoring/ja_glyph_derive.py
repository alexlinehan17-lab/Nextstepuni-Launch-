#!/usr/bin/env python3
"""Derive the exact 2017 Japanese font repair from original PDF font outlines.

The exact embedded-outline routine includes component offsets for composite
TrueType glyphs. A character is accepted only when every named matching
outline agrees. Blank glyphs must be proven to have no outline. No inference
from code-point arithmetic, words, or manually supplied character strings.
"""
import argparse
import collections
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import fitz
from ara_glyphs import doc_hashes

ROOT = Path(__file__).resolve().parents[3]
TARGET = 'examiner-reports/japanese/papers/2017-hl-000-paper.pdf'
PIN = 'e96083ac6d83286da7ad5e1172a3094819339d01cfe1acda36e4abeed1762a0e'
OUTPUT = Path(__file__).with_name('glyphmap-japanese-2017.json')


def derive():
    assert hashlib.sha256((ROOT / TARGET).read_bytes()).hexdigest() == PIN
    with fitz.open(ROOT / TARGET) as target:
        maps, blanks = doc_hashes(target)
        needed = collections.Counter()
        locations = collections.defaultdict(list)
        for page in target:
            for span in page.get_texttrace():
                for uni, gid, _origin, _bbox in span['chars']:
                    if uni == 65533:
                        needed[(span['font'], gid)] += 1
                        locations[(span['font'], gid)].append({'page': page.number + 1, 'origin': [round(v, 1) for v in _origin]})
    outlines = {outline for font, gid in needed for outline in maps.get(font, {}).get(gid, [])}
    sightings = collections.defaultdict(lambda: collections.defaultdict(list))
    paths = {}
    for path in sorted((Path(__file__).parent / 'reviews').glob('japanese-*.json')):
        if not re.fullmatch(r'japanese-\d{4}-(?:hl|ol)\.json', path.name) or int(path.name.split('-')[1]) < 2018:
            continue
        for source in json.loads(path.read_text())['sources']:
            paths[source['path']] = source['sha256']
    # Additional originals are font evidence only, not a claim of completed task review.
    for source in sorted((ROOT / 'examiner-reports/japanese').rglob('*.pdf')):
        rel = str(source.relative_to(ROOT))
        if rel != TARGET:
            paths.setdefault(rel, hashlib.sha256(source.read_bytes()).hexdigest())
    if OUTPUT.exists():
        pinned = json.loads(OUTPUT.read_text()).get('fontSources')
        if pinned:
            paths = pinned
    for source, digest in sorted(paths.items()):
        assert hashlib.sha256((ROOT / source).read_bytes()).hexdigest() == digest
        with fitz.open(ROOT / source) as doc:
            source_maps, _blank = doc_hashes(doc)
            relevant = {font: {gid: hashes for gid, hashes in byid.items() if any(h in outlines for h in hashes)} for font, byid in source_maps.items()}
            for page in doc:
                for span in page.get_texttrace():
                    for uni, gid, _origin, _bbox in span['chars']:
                        char = chr(uni)
                        if uni == 65533 or unicodedata.category(char) in ('Cc', 'Cn', 'Co', 'Cs') or gid < 0:
                            continue
                        for outline in relevant.get(span['font'], {}).get(gid, []):
                            if outline in outlines and len(sightings[outline][char]) < 2:
                                sightings[outline][char].append({'path': source, 'sha256': digest, 'page': page.number + 1, 'font': span['font'], 'gid': gid})
    visual_path = Path(__file__).parent / 'reviews/japanese-2017-hl-glyph-proof.json'
    visual = json.loads(visual_path.read_text())
    assert visual['source'] == TARGET and visual['sha256'] == PIN
    assert hashlib.sha256((ROOT / visual['image']).read_bytes()).hexdigest() == visual['imageSha256']
    assert {'page': visual['page'], 'origin': visual['origin']} in locations[(visual['font'], visual['gid'])]
    with fitz.open(ROOT / TARGET) as doc:
        rendered = doc[visual['page'] - 1].get_pixmap(matrix=fitz.Matrix(4, 4), clip=fitz.Rect(visual['crop'])).tobytes('png')
        assert hashlib.sha256(rendered).hexdigest() == visual['imageSha256']
    repairs, missing = {}, []
    for (font, gid), count in sorted(needed.items()):
        hashes = maps.get(font, {}).get(gid, [])
        answers = {char for outline in hashes for char in sightings.get(outline, {})}
        if not hashes and gid in blanks.get(font, set()):
            char, proof = ' ', []
        elif len(answers) == 1:
            char = answers.pop()
            proof = [item for outline in hashes for item in sightings[outline].get(char, [])]
        elif (font, gid) == (visual['font'], visual['gid']):
            assert not answers
            char = visual['text']
            proof = [{'visualProof': str(visual_path.relative_to(ROOT)), 'sha256': hashlib.sha256(visual_path.read_bytes()).hexdigest()}]
        else:
            assert not answers, f'Conflicting exact glyph evidence: {font} {gid} {answers}'
            assert all(place['page'] in [1, 6, 10] for place in locations[(font, gid)]), (font, gid, locations[(font, gid)])
            missing.append({'font': font, 'gid': gid, 'occurrences': count, 'outlines': hashes, 'locations': locations[(font, gid)], 'presentation': 'Original PDF image only; forbidden in published text'})
            continue
        repairs.setdefault(font, {})[str(gid)] = {'text': char, 'outlines': hashes, 'evidence': proof}
    assert len(missing) == 19
    used_sources = {item['path']: item['sha256'] for mapping in repairs.values() for entry in mapping.values() for item in entry['evidence'] if 'path' in item}
    return {'source': TARGET, 'sha256': PIN, 'outlineMethod': 'exact-embedded-glyf-v1', 'fontSources': dict(sorted(used_sources.items())), 'repairs': repairs, 'unresolvedImageOnly': missing}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.write:
        OUTPUT.write_text(rendered)
    else:
        assert OUTPUT.read_text() == rendered, 'Regenerated glyph proof differs'
    print(f'{sum(len(mapping) for mapping in result["repairs"].values())} source-proven glyph repairs; {len(result["unresolvedImageOnly"])} passage/cover glyphs retained only in original images, forbidden in card text')
