import copy
import json
import unittest

import construction_2026_higher as m


def card(d, key):
    return next(t['card'] for t in d['tasks'] if t['card']['id'] == m.PREFIX + key)


def binding(d, key):
    return next(b for b in d['bindings'] if b['cardId'] == m.PREFIX + key)


def drop(d, key):
    d['tasks'] = [t for t in d['tasks'] if t['card']['id'] != m.PREFIX + key]
    d['bindings'] = [b for b in d['bindings'] if b['cardId'] != m.PREFIX + key]
    d['addedIds'] = [i for i in d['addedIds'] if i != m.PREFIX + key]



def item_card(d, key, suffix):
    t = copy.deepcopy(next(t for t in d['tasks'] if t['card']['id'] == m.PREFIX + key))
    t['card']['id'] = m.PREFIX + f'{key}-{suffix}'
    return t


class SourceGuard(unittest.TestCase):
    def test_source_and_images(self):
        self.assertEqual(m.validate(json.loads(m.REVIEW.read_text()))['tasks'], 41)

    def test_rejects_lost_marks_wording_routes_or_topics(self):
        original = json.loads(m.REVIEW.read_text())
        enerphit = card(original, 'q10-a')
        cases = {
            'choice split into a per-area card': lambda d: d['tasks'].append(item_card(d, 'q4-a', 'stone-wall')),
            'choice split into a per-location card': lambda d: d['tasks'].append(item_card(d, 'q9-a', 'wall-roof')),
            'area option dropped': lambda d: card(d, 'q4-a')['rows'][0]['group']['options'].pop(),
            'wrong claim limit': lambda d: card(d, 'q9-a')['rows'][0]['group'].update(claimMax=2),
            'printed list trimmed': lambda d: card(d, 'q4-b').update(questionText=card(d, 'q4-b')['questionText'].replace('; respect for our built heritage', '')),
            'alternative combined with EnerPHit': lambda d: card(d, 'q10-alt-complete')['taskGroups'].append(dict(sourceCardId=enerphit['id'], label='a', marks=18, rowIds=[])),
            'invented location label': lambda d: card(d, 'q9-a')['rows'][0]['group']['options'].__setitem__(0, 'Chimney junction'),
            'lost part in the complete question': lambda d: card(d, 'q9-complete')['taskGroups'].pop(0),
            'invented question wording': lambda d: card(d, 'q6-c').update(questionText='Explain why natural houses are always healthier.'),
            'paraphrased stem': lambda d: card(d, 'q7-a').update(stem='A stairs with a 150 mm newel post.'),
            'marking row not in scheme': lambda d: card(d, 'q8-b')['rows'][0].update(verbatim='Any sensible pipe layout'),
            'changed tariff': lambda d: card(d, 'q7-a')['rows'][2].update(marks=10, permittedMarks=[0, 5, 10]),
            'invented mark band': lambda d: card(d, 'q1-a')['rows'][4].update(permittedMarks=list(range(9))),
            'wrong worked answer': lambda d: card(d, 'q5-b')['rows'][4].update(contextNote='Cost = €41.27 per year.'),
            'missing Atlas association': lambda d: binding(d, 'q9-a')['atlasTopicIds'].pop(),
            'canonical node outside the crosswalk': lambda d: binding(d, 'q2-c')['canonicalTopicIds'].append('cons-1-7'),
            'broken composite topic union': lambda d: binding(d, 'q4-complete')['atlasTopicIds'].pop(),
            'unreviewed source crop': lambda d: d['questionFigures'][1].update(visuallyInspected=False),
            'cut off drawing': lambda d: d['questionFigures'][1].update(rect=[48, 52, 568, 400]),
            'solution shown before reveal': lambda d: card(d, 'q5-a').update(questionFigureKey=m.FP + 'q5-calculation'),
            'unclassified choice': lambda d: d['selectionLedger'].update(unclassified=1),
            'uncertain source': lambda d: d['sourceHashes'].update({m.P: 'changed'}),
        }
        for label, change in cases.items():
            with self.subTest(label=label):
                d = copy.deepcopy(original)
                change(d)
                with self.assertRaises(AssertionError):
                    m.validate(d, images=False)


if __name__ == '__main__':
    unittest.main()
