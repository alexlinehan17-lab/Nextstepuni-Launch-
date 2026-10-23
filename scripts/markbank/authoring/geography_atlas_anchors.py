#!/usr/bin/env python3
"""Hosted paper anchors for the 2010-2019 Geography single booklets.

Before 2020 one booklet printed Part One (Q1-12) and then Part Two, which
restarts at Q1 (Higher Level option essays run on to Q24). Two maps described
it with different numbering:

- the Paper Trail Viewer's answer sidecar (Storage; its repo copy is
  scripts/paper-trail/answers/<year>/<fileid>.json) anchors PART TWO as 1-12:
  the Viewer's chips, Full Loop stops and Topics tool use that numbering;
- the hosted paper anchors the Topic Atlas reads for these booklets
  (public/paper-anchors/, VAULT_PREFER_ANCHORS) anchored PART ONE as 1-12.

So one Atlas identity (single, n) named two printed questions. This script
rebuilds each booklet's hosted map as a section-restart paper, the existing
mechanism documented in test/vaultAnchors.test.ts ("retain their
already-shipped numeric identities and declare the physical permutation
separately with printOrder"):

- Part Two keeps n, with the Viewer sidecar's own page and band (and, Higher
  Level English, the reviewed option-essay regions Q13-24 from the repo copy),
  so opening the Viewer from the Atlas never moves a chip;
- Part One takes n = 1000 + its printed number, the label
  "Part One · Question N" ("Cuid a hAon · Ceist N" on an Irish booklet, as its
  pages print "Cuid a hAon" and its sidecar labels Part Two "Ceist N"), and the
  explicit paper region the Atlas showed for it before (frozen in
  scripts/paper-trail/geography-part-one-anchors.json);
- every anchor carries printOrder in print order (Part One first).

Irish (IV) booklets get the same mechanical re-keying (same printed numbering);
nothing in their content is re-reviewed.

    python3 scripts/markbank/authoring/geography_atlas_anchors.py           # check
    python3 scripts/markbank/authoring/geography_atlas_anchors.py --write
"""

from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
SIDECARS = os.path.join(ROOT, 'scripts', 'paper-trail', 'answers')
HOSTED = os.path.join(ROOT, 'public', 'paper-anchors')
PART_ONE = os.path.join(ROOT, 'scripts', 'paper-trail', 'geography-part-one-anchors.json')

YEARS = range(2010, 2020)
FILEIDS = ('LC005ALP000EV.pdf', 'LC005GLP000EV.pdf', 'LC005ALP000IV.pdf', 'LC005GLP000IV.pdf')
PART_ONE_OFFSET = 1000
# Paper-only anchors: the Atlas shows the crop and keeps the honest
# "open beside its marking scheme" answer path (vaultAnchors.test.ts).
CONF = 0.5
PART_TWO_FIELDS = ('n', 'pP', 'pY', 'label', 'paperRegion', 'endP', 'endY')
# The Viewer sidecar's last Part Two anchor carries no end, so its crop is its
# own page. Where that question runs on, its audited end (page, y) is added:
# 2017 Ordinary Q12B-C continue on page 27 down to the "[40m]" line (EV 0.3943,
# IV 0.4243 of the page). Every other booklet's last question ends on its own
# page (the pages after it are blank, the copyright page or, Irish Higher, the
# option essays, which carry their own anchors only in English).
PART_TWO_ENDS = {
    (2017, 'LC005GLP000EV.pdf', '12'): (27, 0.4043),
    (2017, 'LC005GLP000IV.pdf', '12'): (27, 0.4343),
}


def part_one_n(printed: str) -> str:
    return str(PART_ONE_OFFSET + int(printed))


def part_one_label(fileid: str, printed: str) -> str:
    return (f'Cuid a hAon · Ceist {printed}' if fileid.endswith('IV.pdf')
            else f'Part One · Question {printed}')


def build(year: int, fileid: str, part_one: dict) -> dict:
    with open(os.path.join(SIDECARS, str(year), f'{fileid}.json'), encoding='utf-8') as handle:
        sidecar = json.load(handle)
    first = [{
        'conf': CONF, 'mode': 'pagejump', 'n': part_one_n(q['n']),
        'label': part_one_label(fileid, q['n']), 'pP': q['pP'], 'pY': q['pY'],
        'paperRegion': q['paperRegion'], 'region': [{'p': 1}],
    } for q in part_one]
    second = []
    for q in sidecar['q']:
        anchor = {key: q[key] for key in PART_TWO_FIELDS if key in q}
        anchor.update({'conf': CONF, 'mode': 'pagejump', 'region': [{'p': 1}]})
        if (year, fileid, q['n']) in PART_TWO_ENDS:
            anchor['endP'], anchor['endY'] = PART_TWO_ENDS[(year, fileid, q['n'])]
        second.append(anchor)
    if [q['n'] for q in first] != [part_one_n(str(i)) for i in range(1, 13)]:
        raise AssertionError(f'{year}/{fileid}: Part One is not Q1-12')
    if [q['n'] for q in second] != [str(i) for i in range(1, len(second) + 1)]:
        raise AssertionError(f'{year}/{fileid}: Part Two is not a run from Q1')
    last_one = first[-1]['paperRegion'][-1]
    if (last_one['p'], last_one['r'][3]) > (second[0]['pP'], second[0]['pY'][0]):
        raise AssertionError(f'{year}/{fileid}: Part One runs into Part Two')
    q = first + second
    for rank, anchor in enumerate(q, start=1):
        anchor['printOrder'] = rank
    return {'band': [1, 1], 'component': '000', 'copyright': '© State Examinations Commission',
            'paperFileid': fileid, 'paperOnly': 1, 'q': q, 'schemeFileid': '', 'v': 1}


def outputs() -> dict[str, str]:
    with open(PART_ONE, encoding='utf-8') as handle:
        frozen = json.load(handle)['papers']
    out = {}
    for year in YEARS:
        for fileid in FILEIDS:
            data = build(year, fileid, frozen[f'{year}/{fileid}'])
            out[os.path.join(HOSTED, str(year), f'{fileid}.json')] = json.dumps(
                data, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return out


def main() -> int:
    write = '--write' in sys.argv
    stale = []
    for path, text in outputs().items():
        current = open(path, encoding='utf-8').read() if os.path.exists(path) else None
        if current == text:
            continue
        if write:
            with open(path, 'w', encoding='utf-8') as handle:
                handle.write(text)
        else:
            stale.append(os.path.relpath(path, ROOT))
    if stale:
        print('stale (run with --write): ' + ', '.join(stale), file=sys.stderr)
        return 1
    print(f'{len(YEARS) * len(FILEIDS)} Geography single-booklet anchor maps current.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
