"""Apply the final C6(c) source split in a separate review candidate."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, '/Users/alexlinehan/Documents/Nextstepuni-LCVP-Release-20261119/scripts/markbank/authoring')
from lcvp_review_2026 import criterion, tidy

baseline = HERE / 'proposed-47-authored-cards.json'
assert hashlib.sha256(baseline.read_bytes()).hexdigest() == 'ec2f9b38d5d36e1b10d8af4fda05c335ecca69876ead3f3c5281f396ba673e03'
cards = json.loads(baseline.read_text())
before = deepcopy(cards)
source = json.loads((HERE / 'source-parts.json').read_text())
r = next(r for r in source['records'] if r['ref'] == 'C6(c)')
decpath = HERE.parent / '2026-11-19-lcvp-2022-deferred-independent/third-reader-decision.json'
dec = json.loads(decpath.read_text())
decision = next(d for d in dec['splitDifferences'] if d['id'] == 'C6(c)')
assert decision['decision']['cardMarks'] == [4, 4]
idx = next(i for i, c in enumerate(cards) if c['id'] == r['id'])
original = cards[idx]
prompts = ['State four sources of information used to investigate the position.', 'Outline how each source was relevant.']
assert ' '.join(prompts) == original['questionText'] == r['questionText']
split = []
for n, prompt in enumerate(prompts):
    c = deepcopy(original)
    c['questionText'] = prompt
    c['stem'] += ' ' + original['questionText']
    c['totalMarks'] = 4
    scope = 'sources' if n == 0 else 'relevance'
    c['questionRef'] = original['questionRef'].removesuffix(' — Deferred sitting') + ' — ' + scope + ' — Deferred sitting'
    note = ('Four distinct sources, one mark each. The relevance belongs to the linked question.' if n == 0 else
            'One mark for the relevance of each of the same four sources chosen in the linked question. Do not count naming the source again.')
    note += ' The paper prints two separate instructions. The scheme gives marks for four responses at 2 (1+1) each; the source/relevance division follows the coordinator’s third reading of both printed instructions. The scheme does not label the two components separately.'
    note += ' Complete original wording, models and allocation: ' + tidy(r['sourceSchemeBlock'])
    c['rows'] = [criterion(scope, prompt, 4, [0, 1], note)]
    for i, part in enumerate(c['rows'][0]['parts'], 1):
        part['verbatim'] = ('Source ' if n == 0 else 'Relevance of source ') + str(i)
    if n:
        c['id'] += '-2'
        c['conceptId'] += '-second-ask'
        c['rows'].append(deepcopy(original['rows'][-1]))
    split.append(c)
cards[idx:idx+1] = split
assert len(cards) == len({c['id'] for c in cards}) == 48
assert sum(c['totalMarks'] for c in cards) == 230
assert all(sum(row['marks'] for row in c['rows']) == c['totalMarks'] for c in cards)
assert all(c == next(x for x in cards if x['id'] == c['id']) for c in before if c['id'] != original['id'])
assert split[0]['id'] == original['id'] and split[0]['conceptId'] == original['conceptId']
assert all('The scheme prints no answer for this part.' != row['verbatim'] for row in split[0]['rows'])
out = HERE / 'proposed-48-after-third-reading.json'
out.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
proof = dict(recordedAt=datetime.now(timezone.utc).isoformat(), status='Review-only split applied; no production writes',
    baselineSha256=hashlib.sha256(baseline.read_bytes()).hexdigest(), payloadSha256=hashlib.sha256(out.read_bytes()).hexdigest(),
    decisionPath=str(decpath), decisionSha256=hashlib.sha256(decpath.read_bytes()).hexdigest(),
    cards=48, sourceParts=44, offeredMarks=230, examMaximum=130,
    unchangedOriginalCards=46, originalIdentityRetained=original['id'], newIdentity=split[1]['id'],
    sourceSelection=dict(fullPrompt=original['questionText'], selectedPrompts=prompts, paperPages=r['paperPages'], schemePages=r['schemePages']),
    changes='C6(c) becomes two four-mark asks; the scoped missing-relevance notice appears only on the second. Full original question and all six source models remain.',
    remaining=['Independent confirmation of the applied split', 'Final filings and provenance integration', 'Application/source/Atlas checks', 'Fresh archive recheck and official recording search'])
(HERE / 'third-reading-split-proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(proof, ensure_ascii=False))
