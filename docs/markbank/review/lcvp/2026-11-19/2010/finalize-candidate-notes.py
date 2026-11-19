"""Remove settled editorial notes from new LCVP source drafts only.

The frozen readings and source quotations are retained. This does not author
new answers, modify live cards, generate an app deck, or certify a release.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
OUT = HERE / 'final-note-cleanup'
OUT.mkdir(exist_ok=True)
assert not (OUT / 'proof.json').exists(), 'Already finalized; inspect before retrying'

def sha(b):
    return hashlib.sha256(b).hexdigest()

paths = {
    '2010': REVIEW / '2026-11-19-lcvp-2010-authoring/proposed-48-authored-cards.json',
    '2011': REVIEW / '2026-11-19-lcvp-2011-authoring/proposed-47-authored-cards.json',
    '2012': REVIEW / '2026-11-19-lcvp-2012-authoring/proposed-47-authored-cards.json',
    '2013': REVIEW / '2026-11-19-lcvp-2013-source-reading/proposed-authored-cards.json',
    '2022-deferred': REVIEW / '2026-11-19-lcvp-2022-deferred-authoring/proposed-48-after-third-reading.json',
    '2023-deferred': REVIEW / '2026-11-19-lcvp-2023-deferred-authoring/proposed-50-authored-cards.json',
}
rules = [
    ('; split form remains provisional.', '.'),
    ('Split form remains provisional. ', ''),
    ('Provisional split of the three printed1+1 allocations; generic-component consistency decision remains pending.',
     'The paper asks for three ways and then an explanation of each. The scheme gives 3 @ 2m (1+1), without naming the component weights.'),
    (' The proposed naming/explanation split remains provisional.', ''),
    ('; proposed split awaiting consistency adjudication.', '.'),
    ('Proposed name allocation from the printed 2@3m(1+2), awaiting consistency adjudication.',
     'Name allocation from the printed 2@3m(1+2).'),
    ('Proposed two marks for this category; third-reader validation required.', 'Two marks for this category.'),
    ('the whole six-mark ask is provisional pending third reading.', 'the whole ask carries six marks.'),
    ('Proposed positive-effect card, with all seven positive models.', 'Positive-effect question, with all seven positive models.'),
    ('Proposed negative-effect card, with all six negative models.', 'Negative-effect question, with all six negative models.'),
    (' Third-reader validation required.', ''),
    ('Provisional whole ask. Generic 3 x 2 (1+1) does not name separate identification/explanation awards. A third reader decides whether it must split.',
     'Three complete responses, each worth two marks (1+1). The scheme does not name separate identification/explanation awards.'),
    ('Provisional whole ask. Two responses, each with two indivisible two-mark components. No semantic allocation is invented; a third reader decides the split.',
     'Two responses, each with two indivisible two-mark components. The scheme does not name separate identification/description awards.'),
    ('Provisional whole ask: a third reader decides whether generic 1+1 permits separate naming/explanation cards.',
     'Four complete responses, each worth two marks (1+1). The scheme does not name separate identification/explanation awards.'),
    (' Hosted playback remains pending the audio-hosting lane while the SEC archive is blocked.', ''),
]

changes = []
staged = []
used = {old: 0 for old, _ in rules}
for sitting, path in paths.items():
    raw = path.read_bytes()
    before = json.loads(raw)
    after = copy.deepcopy(before)
    local = []
    for card in after:
        fields = [('rows/' + str(i) + '/contextNote', row, 'contextNote')
                  for i, row in enumerate(card.get('rows', [])) if 'contextNote' in row]
        if card.get('videoMaterial', {}).get('presentationNote'):
            fields.append(('videoMaterial/presentationNote', card['videoMaterial'], 'presentationNote'))
        for field, owner, key in fields:
            original = owner[key]
            for old, new in rules:
                used[old] += owner[key].count(old)
                owner[key] = owner[key].replace(old, new)
            if owner[key] != original:
                # The unchanged suffix includes all quoted source wording.
                for marker in ['Complete original', 'Complete printed', 'Printed support notes']:
                    if marker in original:
                        assert original.split(marker, 1)[1] == owner[key].split(marker, 1)[1]
                local.append(dict(id=card['id'], field=field, before=original, after=owner[key]))
    assert [c['id'] for c in before] == [c['id'] for c in after]
    # Strip only the explicitly recorded presentation fields; everything else
    # (including sources, questions, answers, controls, marks and IDs) must match.
    old_by_id = {c['id']: copy.deepcopy(c) for c in before}
    new_by_id = {c['id']: copy.deepcopy(c) for c in after}
    for change in local:
        for mapping in [old_by_id, new_by_id]:
            target = mapping[change['id']]
            steps = change['field'].split('/')
            for step in steps[:-1]:
                target = target[int(step)] if isinstance(target, list) else target[step]
            del target[steps[-1]]
    assert old_by_id == new_by_id
    result = (json.dumps(after, ensure_ascii=False, indent=2) + '\n').encode()
    staged.append((path, raw, result))
    changes.append(dict(sitting=sitting, path=str(path), beforeSha256=sha(raw), afterSha256=sha(result),
                        cards=len(after), changedCards=len({r['id'] for r in local}), changes=local))

assert all(used.values()), used
assert {x['sitting']: len(x['changes']) for x in changes} == {
    '2010': 7, '2011': 2, '2012': 1, '2013': 9,
    '2022-deferred': 6, '2023-deferred': 2,
}
for path, raw, result in staged:
    sitting = next(k for k, p in paths.items() if p == path)
    (OUT / (sitting + '-before.json')).write_bytes(raw)
    path.write_bytes(result)
proof = dict(recordedAt=datetime.now(timezone.utc).isoformat(),
    scope='Settled editorial notes removed from new source drafts; quoted source text and all assessment fields preserved.',
    basis=['Final third-reader decisions beside the original comparison packets',
           'Coordinator splitting rule: separately printed instructions or named items with separate marks split; compound instructions stay together',
           '2010 B2(ii), 2011 C2(d)(ii), 2012 C4(b): two separate printed instructions confirmed in source-parts.json'],
    limitations=['Audio hosting/search remains unresolved in the evidence; removing operational notes from student copy does not certify playback.',
                 'Final generation, source openings, canonical filings and production verification remain pending.'],
    files=changes)
(OUT / 'proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
print(json.dumps([{k:v for k,v in x.items() if k != 'changes'} for x in changes], indent=2))
