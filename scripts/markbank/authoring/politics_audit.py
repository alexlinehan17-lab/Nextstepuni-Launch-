"""Fail-closed source, selection and visually reviewed boundary checks.

The raw selection ledger covers every PDF page, independently of the task
extractor. It is pinned after the visual sweep, never rewritten by author.py.
The handwritten printed-boundary census is an additional extraction guard;
reviewedTaskCounts records the separate scheme/route census.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import fitz
from politics_corpus import ROOT, clean
from politics_reviewed import REVIEWED

LEDGER = ROOT / 'scripts/markbank/authored/politics-selection-review.json'
SIGNAL = re.compile(r'\b(?:choos\w*|chosen|choices?|either|or|any|one of|two of|three of|five of|select\w*|following|answer\s+(?:one|two|three|ten|fifteen|\d+))\b|☐|□', re.I)

# Visual inventory of printed answer-bearing labels (blank roman answer lines
# at 2019 OL 2(e) are one question, not five independently priced tasks).
PRINTED = {
 (2018,'higher'): ('l', {'b':2,'i':2,'k':2}, {'2':'f'}, '3 4(a) 4(b) 5(a) 5(b) 6'),
 (2018,'ordinary'): ('t', {'b':2,'e':2,'o':2}, {'2':'f','3':'e','4':'b'}, '5 6 7 8 9 10'),
 (2019,'higher'): ('l', {}, {'2':'g'}, '3(a) 3(b) 4 5 6(a) 6(b)'),
 (2019,'ordinary'): ('u', {'u':3}, {'2':'e','3':'e','4':'c'}, '5 6 7 8 9 10'),
 (2020,'higher'): ('l', {}, {'2':'g'}, '3(a) 3(b) 4 5 6(a) 6(b)'),
 (2021,'higher'): ('o', {}, {'2':'g'}, '3 4(a) 4(b) 5 6 7'),
 (2021,'ordinary'): ('t', {'q':3}, {'2':'e','3':'e','4':'d'}, '5 6 7 8 9 10'),
 (2022,'higher'): ('o', {}, {'2':'g'}, '3(a) 3(b) 4 5 6 7'),
 (2022,'ordinary'): ('t', {'d':3}, {'2':'e','3':'e','4':'d'}, '5 6 7 8 9 10'),
 (2023,'higher'): ('o', {}, {'2':'g'}, '3 4(a) 4(b) 5 6 7'),
 (2023,'ordinary'): ('t', {'h':3}, {'2':'e','3':'e','4':'d'}, '5 6 7 8 9 10'),
 (2024,'higher'): ('o', {}, {'2':'g'}, '3(a) 3(b) 4 5 6 7'),
 (2024,'ordinary'): ('t', {'d':3}, {'2':'e','3':'e','4':'d'}, '5 6 7 8 9 10'),
 (2025,'higher'): ('o', {}, {'2':'g'}, '3(a) 3(b) 4 5 6 7'),
 (2025,'ordinary'): ('t', {'d':3}, {'2':'e','3':'e','4':'d'}, '5 6 7 8 9 10'),
 (2026,'higher'): ('o', {}, {'2':'g'}, '3(a) 3(b) 4 5 6 7'),
 (2026,'ordinary'): ('t', {'d':3}, {'2':'e','3':'e','4':'d'}, '5 6 7 8 9 10'),
}

def printed_keys(identity):
    end, romans, data, essays = PRINTED[identity]
    result = []
    for letter in map(chr, range(ord('a'), ord(end)+1)):
        if letter in romans:
            result += [f'1({letter})({r})' for r in ['i','ii','iii'][:romans[letter]]]
        else:
            result.append(f'1({letter})')
    for q, last in data.items():
        result += [f'{q}({c})' for c in map(chr, range(ord('a'),ord(last)+1))]
    return result + essays.split()


def raw_selection_pages(sources):
    result = []
    for src in sources:
        for number, page in enumerate(fitz.open(ROOT / src['papers']['path']), 1):
            raw = clean(page.get_text())
            signals = [{'signal': m.group(), 'context': raw[max(0,m.start()-90):m.end()+130]}
                       for m in SIGNAL.finditer(raw)]
            if signals:
                result.append({'year': src['year'], 'level': src['level'], 'page': number,
                               'sha256': hashlib.sha256(raw.encode()).hexdigest(), 'signals': signals})
    return result


def verify(drafts):
    sources = [d['source'] for d in drafts]
    assert set(PRINTED) == {(s['year'],s['level']) for s in sources}, 'Indexed corpus changed'
    reviewed = json.loads(LEDGER.read_text())['pages']
    actual = raw_selection_pages(sources)
    expected = [{k:r[k] for k in ('year','level','page','sha256','signals')} for r in reviewed]
    assert actual == expected, 'Unclassified or stale raw-paper selection directive; review the PDF and ledger'
    assert all(r['reason'].strip() and r['disposition'] in ['administration','source-content','reviewed-tasks'] for r in reviewed)
    for draft in drafts:
        src = draft['source']; identity = (src['year'],src['level'])
        for kind in ['papers','schemes']:
            assert hashlib.sha256((ROOT/src[kind]['path']).read_bytes()).hexdigest() == src[kind]['sha256'], 'Source changed'
        keys = []
        for u in draft['paper']['units']:
            if identity == (2019,'ordinary') and u['key'].startswith('2(e)'):
                if '2(e)' not in keys: keys.append('2(e)')
            elif not u.get('contextOnly'): keys.append(u['key'])
        assert keys == printed_keys(identity), (identity, 'Printed task boundary missing/extra')
        # Closed source pools remain tied to their actual printed labels.
        if identity == (2023,'ordinary'):
            from politics_reviewed import CAUSES_2023_OL
            page = clean(fitz.open(ROOT/src['papers']['path'])[10].get_text())
            for _, label in CAUSES_2023_OL:
                assert clean(label).lower() in page.lower(), ('Changed poverty-cause pool', label)
        if identity == (2025,'ordinary'):
            page = clean(fitz.open(ROOT/src['papers']['path'])[10].get_text())
            assert all(c in page for c in ['Haiti','South Sudan','Sudan'])
    return len(actual), sum(len(p['signals']) for p in actual)
