import copy
import json
import unittest

import construction_2023_higher as m


def card(d, key):
    return next(t['card'] for t in d['tasks'] if t['card']['id'] == m.PREFIX + key)


def binding(d, key):
    return next(b for b in d['bindings'] if b['cardId'] == m.PREFIX + key)


def item_card(d, key, new_key):
    t = copy.deepcopy(next(t for t in d['tasks'] if t['card']['id'] == m.PREFIX + key))
    t['card']['id'] = m.PREFIX + new_key
    return t


def figure(d, key):
    return next(f for f in d['questionFigures'] if f['key'] == m.FP + key)


class SourceGuard(unittest.TestCase):
    def test_source_and_images(self):
        self.assertEqual(m.validate(json.loads(m.REVIEW.read_text()))['tasks'], 50)

    def test_rejects_lost_marks_wording_routes_topics_or_corrections(self):
        original = json.loads(m.REVIEW.read_text())
        passive = card(original, 'q10-a')
        cases = {
            'choice split into a per-item card': lambda d: d['tasks'].append(item_card(d, 'q10-a', 'q10-a-solar-shading')),
            'vernacular choice split into a per-item card': lambda d: d['tasks'].append(item_card(d, 'q4-b', 'q4-b-craft-skills')),
            'option dropped from a choice': lambda d: card(d, 'q4-b')['rows'][0]['group']['options'].pop(),
            'wrong claim limit': lambda d: card(d, 'q10-a')['rows'][0]['group'].update(claimMax=3),
            'printed list trimmed': lambda d: card(d, 'q4-b').update(questionText=card(d, 'q4-b')['questionText'].replace('; craft skills', '')),
            'choice card loses its composite solution figure': lambda d: card(d, 'q10-a').pop('figureKey'),
            'choice item loses its drawings': lambda d: figure(d, 'q10-features')['panels'].pop(),
            'complete route loses a choice item panel': lambda d: figure(d, 'q4-scheme')['panels'].pop(),
            'alternative combined with Passive House': lambda d: card(d, 'q10-alt-complete')['taskGroups'].append(dict(sourceCardId=passive['id'], label='a', marks=20, rowIds=[])),
            'invented item label': lambda d: card(d, 'q2-a-training').update(questionText=card(d, 'q2-a-training')['questionText'].replace('— Training', '— Induction')),
            'item named without its scheme heading': lambda d: card(d, 'q2-b-site-access').update(questionText=card(d, 'q2-b-site-access')['questionText'].split(' — ')[0]),
            'lost part in the complete question': lambda d: card(d, 'q8-complete')['taskGroups'].pop(1),
            'lost item in a composed part': lambda d: card(d, 'q2-a')['taskGroups'].pop(),
            'invented question wording': lambda d: card(d, 'q6-c').update(questionText='Explain why energy efficient homes are always cheaper.'),
            'paraphrased stem': lambda d: card(d, 'q7-a').update(stem='A sheeted door in a cavity wall with a 1:5 section.'),
            'marking row not in scheme': lambda d: card(d, 'q3-b')['rows'][0].update(verbatim='Any sensible layout'),
            'changed tariff': lambda d: card(d, 'q8-b')['rows'][1].update(marks=6, permittedMarks=list(range(7))),
            'dropped drafting allowance': lambda d: card(d, 'q1-a')['rows'].pop(),
            'invented mark band': lambda d: card(d, 'q7-a')['rows'][3].update(permittedMarks=[0, 4, 6, 8]),
            'resistance steps loosened': lambda d: card(d, 'q5-a')['rows'][0].update(permittedMarks=list(range(25))),
            'wrong worked answer': lambda d: card(d, 'q5-b')['rows'][4].update(contextNote='Annual cost = €44.60.'),
            'wrong window area': lambda d: card(d, 'q9-b')['rows'][4].update(contextNote='Window area = 4.73 m².'),
            'missing Atlas association': lambda d: binding(d, 'q10-a')['atlasTopicIds'].pop(),
            'canonical node outside the crosswalk': lambda d: binding(d, 'q10-c')['canonicalTopicIds'].append('cons-1-4'),
            'broken composite topic union': lambda d: binding(d, 'q6-complete')['atlasTopicIds'].pop(),
            'unreviewed source crop': lambda d: d['questionFigures'][1].update(visuallyInspected=False),
            'cut off drawing': lambda d: figure(d, 'q1-section').update(rect=[51, 51, 550, 400]),
            'solution shown before reveal': lambda d: card(d, 'q5-a').update(questionFigureKey=m.FP + 'q5-calculation'),
            'unclassified choice': lambda d: d['selectionLedger'].update(unclassified=1),
            'choice dropped from the ledger': lambda d: d['selectionLedger']['finiteQuestionChoices'].pop('4b'),
            'uncertain source': lambda d: d['sourceHashes'].update({m.P: 'changed'}),
            'correction loses its concept ID': lambda d: card(d, 'q8-a').update(conceptId='wastewater-requirements'),
            'correction not hash-linked': lambda d: d['corrections'][0].update(priorSha256='0' * 64),
            'legacy card replaced without a record': lambda d: d['corrections'].pop(),
            'legacy card counted as an addition': lambda d: d['addedIds'].append(m.PREFIX + 'q9-c-advantages'),
        }
        for label, change in cases.items():
            with self.subTest(label=label):
                d = copy.deepcopy(original)
                change(d)
                with self.assertRaises(AssertionError):
                    m.validate(d, images=False)


if __name__ == '__main__':
    unittest.main()
