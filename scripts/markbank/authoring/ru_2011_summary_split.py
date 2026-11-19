"""Apply Alex's approved R7 split to the source-derived 2011 summary task."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = 'scripts/markbank/authoring/reviews/russian-r7-split-20261119'


def split_approved_summaries(cards):
    folder = ROOT / REVIEW
    approval = json.loads((folder / '2011-hl-approval.json').read_text())
    proposal_bytes = (folder / '2011-hl-proposal.json').read_bytes()
    assert hashlib.sha256(proposal_bytes).hexdigest() == approval['proposalSha256']
    proposal = json.loads(proposal_bytes)
    original = next(c for c in cards if c['id'] == 'ru-2011-hl-c2')
    assert original == proposal['originalCard'], 'Source-derived summary changed since approval'
    expected = {c['id']: c for c in proposal['proposedCards']}
    questions = original['review']['atlasQuestions']
    instruction = original['questionText'].split('\n\n', 1)[0]
    replacements = []
    for index, question in enumerate(questions, 1):
        card = copy.deepcopy(original)
        card['id'] = original['id'] if index == 1 else f'ru-2011-hl-c2-{index}'
        agreed = expected[card['id']]
        card['conceptId'] = agreed['conceptId']
        card['questionRef'] = question['questionRef']
        card['questionText'] = instruction + '\n\n' + question['questionText']
        card['totalMarks'] = agreed['totalMarks']
        card['sourceMaterial']['pages'] = question['questionPages']
        card['review']['paperPages'] = question['questionPages']
        card['review']['questionPages'] = question['questionPages']
        card['review']['reviewedAt'] = '2026-11-19'
        card['review']['splitApproval'] = REVIEW + '/2011-hl-approval.json'
        if index == 1:
            # Keep the existing card identity on the existing first Atlas ask.
            # This exact one-to-one binding uses the established manifest format.
            card['review']['coveredQuestionRefs'] = [question['questionRef']]
            card['review']['atlasQuestions'] = [question]
        else:
            card['review'].pop('coveredQuestionRefs')
            card['review'].pop('atlasQuestions')
        group = card['rubric']['groups'][0]
        group['id'] = f'section-{index}'
        group['label'] = f'Section {index}'
        group['criteria'] = [c for c in group['criteria'] if c['id'].startswith(f'section-{index}-')]
        assert len(group['criteria']) == 2
        assert [c['maxMarks'] for c in group['criteria']] == [10, 2]
        card['rubric'].pop('allocationCap')
        card['rubric']['markingGuideNote'] = agreed['rubric']['markingGuideNote']
        card['rubric']['markingGuideNote'] += ' Assess content manually against the complete printed pool and its conditions; the numerical controls do not count or classify individual details.'
        card['rubric']['markingGuideNote'] += ' Assess language manually' + original['rubric']['markingGuideNote'].split(' Assess language manually', 1)[1]
        replacements.append(card)
    assert sum(c['totalMarks'] for c in replacements) == 48
    result = []
    for card in cards:
        result.extend(replacements if card['id'] == original['id'] else [card])
    assert len(result) == 39 and len({c['id'] for c in result}) == 39
    assert sum(c['totalMarks'] for c in result) == 303
    return result
