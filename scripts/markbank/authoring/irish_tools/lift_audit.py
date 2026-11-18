#!/usr/bin/env python3
"""Lift, never write: fail if any committed Irish card carries Irish of ours: a guidance sentence that is not the SEC's,
a card-scope line in its question ("An rogha don chárta seo", "Don chárta seo", "Léigh an téacs ar leathanach"), or a
source note in Irish.

Every card file under components/MarkBank/cards/irish is read; each criterion's guidance is cut into fragments and
checked against that year's printed Irish papers and schemes (irish_lifted.written). Needs the local
paper-trail-corpus PDFs, like the rest of irish_tools. regenerate.sh --check runs it.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from irish_lifted import ROOT, written  # noqa: E402

problems = []
for path in sorted(glob.glob(os.path.join(ROOT, 'components', 'MarkBank', 'cards', 'irish', '*.json'))):
    for card in json.load(open(path, encoding='utf-8'))['cards']:
        problems += [f'{os.path.basename(path)} {card["id"]}: {fragment[:120]}' for fragment in written(card)]
        problems += [f'{os.path.basename(path)} {card["id"]}: {criterion["id"]} has no guidance'
                     for criterion in card['criteria'] if not criterion['guidance']]
if problems:
    print('\n'.join(problems[:50]))
    raise SystemExit(f'{len(problems)} fragments on Irish cards are not the SEC\'s words')
print('IRISH CARDS CARRY THE SEC\'S WORDS ONLY')
