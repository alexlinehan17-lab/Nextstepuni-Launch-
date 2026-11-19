#!/usr/bin/env python3
"""Exam identities for English's deferred Paper 2 options (single texts, prescribed poets and poems).

A deferred paper sets the year's prescribed texts and poets under its own
letters and numbers, so each option is identified from the deferred paper
itself: the heading June's reader finds on the page (`observedHeading`), the
poet's name printed with a Higher prescribed question (`promptHeading`), and
for an Ordinary poem its title and the byline printed under it. The topic is
the one June's identities already give the same text or poet; a text or poet
June never set is refused rather than guessed. Writes the deferred entries of
english-exam-identities.json (June's are untouched).

    python3 scripts/markbank/authoring/english_deferred_identities.py [--check]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import fitz

from english_cards import comparable
from english_complete import ROOT, inventory

sys.path.insert(0, str(ROOT / 'scripts/paper-trail'))
import english_p2_complete as p2  # noqa: E402
import english_p2_ol as p2ol  # noqa: E402

PATH = ROOT / 'scripts/markbank/authored/english-exam-identities.json'


def curriculum_names():
    text = (ROOT / 'curriculum.ts').read_text()
    return {m.group(1): m.group(2) for m in re.finditer(r'"id": "(english-1[12]-\d+)",\s*"name": "([^"]+)"', text)}


def same(a, b):
    """Printed and curriculum spellings of one name: case, full stops, accents and apostrophes aside."""
    def key(value):
        return re.sub(r'[^a-z]', '', comparable(value.replace('.', ' ')))
    return key(a) == key(b)


def build():
    payload = json.loads(PATH.read_text())
    june = {k: v for k, v in payload['identities'].items() if '-deferred-' not in k}
    names = curriculum_names()
    texts = {}
    for key, value in june.items():
        if '-single-' in key:
            texts.setdefault(comparable(value['title']), value)
    poets = {name: node for node, name in names.items() if node.startswith('english-11-')}
    out, errors = {}, []
    for record in inventory()['papers']:
        if record.get('sitting') != 'deferred' or record['paper'] != 2:
            continue
        try:
            out.update(identities_for(record, texts, poets, names))
        except ValueError as error:
            # A paper whose options are not all identified keeps no deferred identity at all.
            errors.append(str(error))
    payload['identities'] = {**june, **dict(sorted(out.items()))}
    return payload, errors


def identities_for(record, texts, poets, names):
    out = {}
    if True:
        doc = fitz.open(ROOT / record['questionPaper']['path'])
        higher = record['level'] == 'higher'
        blocks = (p2.collect_single_text_cards(doc) + p2.collect_comparative_cards(doc) + p2.collect_poetry_cards(doc)) \
            if higher else p2ol.collect_cards(doc, record['year'])
        for block in blocks:
            base = {'observedHeading': block.label, 'paperPage': block.p_page + 1,
                    'source': record['questionPaper']['path'], 'sourceSha256': record['questionPaper']['sha256']}
            if block.kind == 'single':
                letter = re.search(r'Single Text ([A-I])', block.label).group(1).lower()
                key = f"{record['id']}-single-{letter}"
                if key in out:
                    continue
                title = block.label.split(' · ')[1]
                known = texts.get(comparable(title.replace('’ S', '’s')))
                if not known:
                    raise ValueError(f'{key}: no June identity for the single text {title!r}')
                out[key] = {'topicId': known['topicId'], 'title': known['title'],
                            'canonicalLabel': known['canonicalLabel'], **base}
            elif block.kind == 'prescribed' and higher:
                number = block.label.rsplit('Q', 1)[1]
                key = f"{record['id']}-prescribed-{number}"
                lines = [line for line in p2.lines_of(doc[block.p_page]) if block.p_y - 0.002 <= line.y < block.p_y + 0.03]
                printed = next(line.text for line in lines if not re.fullmatch(r'[1-5]\.', line.text))
                node = next((n for name, n in poets.items() if same(name, printed)), None)
                if not node:
                    raise ValueError(f'{key}: no curriculum poet for the printed heading {printed!r}')
                out[key] = {'topicId': node, 'title': names[node], 'canonicalLabel': names[node], **base,
                            'promptHeading': printed}
            elif block.kind == 'prescribed':
                letter = re.search(r'Poetry ([A-F])', block.label).group(1).lower()
                key = f"{record['id']}-prescribed-{letter}"
                text = doc[block.p_page].get_text()
                byline = next((name for name in poets.values() if same_in(name, text)), None)
                if not byline:
                    raise ValueError(f'{key}: no curriculum poet printed under {block.label!r} on PDF{block.p_page + 1}')
                node = next(n for n, name in names.items() if name == byline)
                out[key] = {'topicId': node, 'title': block.label.split(' · ')[1], 'canonicalLabel': byline, **base,
                            'sourcePages': [block.p_page + 1]}
    return out


def same_in(name, text):
    """A curriculum poet printed as a byline line on the page (spelling variants as `same`)."""
    return any(same(name, line.strip()) for line in text.splitlines() if line.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    payload, errors = build()
    for error in errors:
        print('REFUSED ' + error)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if PATH.read_text() != rendered:
            raise SystemExit('English deferred identities are stale; run english_deferred_identities.py')
    else:
        PATH.write_text(rendered)
    print(sum('-deferred-' in k for k in payload['identities']), 'deferred identities')


if __name__ == '__main__':
    main()
