"""Exact Russian-only coverage for source-reviewed shared mark boundaries.

Runtime card counts remain real card counts. These references expand only the
coverage lookup, retaining each original leaf in the independent denominator.
The mandatory original-source gate pins the small manifest to PDF hashes and
all original prompts; no generic parent-question coverage is inferred here.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / 'scripts/markbank/authoring/russian-joint-tasks.json'


def validate_joint_task(source, card, registry=None):
    registry = registry if registry is not None else json.loads(MANIFEST.read_text())
    matches = [task for task in registry['tasks'] if task['id'] == source['id']]
    declares = 'coveredQuestionRefs' in source or 'atlasQuestions' in source
    if not matches and not declares:
        return None
    assert len(matches) == 1, ('Unknown/duplicate Russian joint task', source['id'])
    expected = matches[0]
    assert card['subjectId'] == 'russian', source['id']
    assert card.get('section') == expected['section'], source['id']
    for key in ('id', 'year', 'level', 'questionRef'):
        assert source[key] == card[key] == expected[key], (source['id'], key)
    for key in ('component', 'paperFileid', 'schemeFileid', 'paperPages', 'schemePages'):
        assert source[key] == expected[key], (source['id'], key)
    assert source.get('questionPages') == expected['paperPages'], source['id']
    assert card.get('sourceMaterial', {}).get('pages') == expected['paperPages'], source['id']
    questions = [{key: value for key, value in q.items() if key != 'leafKey'} for q in expected['questions']]
    refs = [q['questionRef'] for q in questions]
    assert source.get('coveredQuestionRefs') == refs, source['id']
    assert source.get('atlasQuestions') == questions, source['id']
    assert len(set(refs)) == len(refs) == len({q['n'] for q in questions}), source['id']
    compact = lambda text: ' '.join(text.split())
    for q in questions:
        assert isinstance(q.get('n'), str) and q['n'].strip() == q['n'] and q['n'], 'Missing Russian joint question identity'
        assert isinstance(q.get('questionRef'), str) and q['questionRef'].strip(), q['n']
        for key, allowed in [('questionPages', expected['paperPages']), ('schemePages', expected['schemePages'])]:
            pages = q.get(key)
            assert isinstance(pages, list) and pages and len(set(pages)) == len(pages), (q['n'], key)
            assert all(type(page) is int and page > 0 and page in allowed for page in pages), (q['n'], key)
        assert compact(q['questionText']) and compact(q['questionText']) in compact(card['questionText']), q['questionRef']
    if any('topicId' in q or 'additionalTopicIds' in q for q in questions):
        union=set()
        for q in questions:
            assert isinstance(q.get('topicId'),str) and q['topicId'].strip(), q['questionRef']
            assert isinstance(q.get('additionalTopicIds'),list) and len(q['additionalTopicIds'])<=1, q['questionRef']
            ids=[q['topicId'],*q['additionalTopicIds']]
            assert all(isinstance(value,str) and value.strip()==value and value for value in ids), q['questionRef']
            assert len(set(ids))==len(ids), q['questionRef']
            union.update(ids)
        ids=[card['topicId'],*card.get('additionalTopicIds',[])]
        assert len(set(ids))==len(ids) and set(ids)==union, 'Incomplete Russian joint-card topic coverage'
    return expected


def reviewed_joint_coverage(shipped, census_index, root=ROOT):
    """Validate generated source metadata before granting exact leaf coverage."""
    records = json.loads((root / 'scripts/markbank/authoring/russian-reviewed-sources.json').read_text())
    cards = json.loads((root / 'components/MarkBank/cards/russian/reviewed.json').read_text())
    registry = json.loads((root / 'scripts/markbank/authoring/russian-joint-tasks.json').read_text())
    known = {task['id'] for task in registry['tasks']}
    card_by_id = {card['id']: card for card in cards}
    shipped_by_id = dict(shipped)
    result = {}
    for source in records:
        if source['id'] not in known and not any(key in source for key in ('coveredQuestionRefs', 'atlasQuestions')):
            continue
        assert source['id'] not in result, ('Duplicate Russian joint source', source['id'])
        card = card_by_id[source['id']]
        expected = validate_joint_task(source, card, registry)
        assert shipped_by_id.get(card['id']) == card['questionRef'], card['id']
        level = 'hl' if expected['level'] == 'higher' else 'ol'
        candidates = [leaves for (year, candidate_level, paper), leaves in census_index.items()
                      if year == expected['year'] and candidate_level == level and paper is None]
        assert len(candidates) == 1, ('Russian joint census missing', card['id'])
        for q in expected['questions']:
            assert tuple(q['leafKey']) in candidates[0], ('Unknown Russian census key', q['questionRef'])
        result[card['id']] = source['coveredQuestionRefs']
    assert (known & set(shipped_by_id)) == set(result), 'Missing Russian joint source metadata'
    return result
