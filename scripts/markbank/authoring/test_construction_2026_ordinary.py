import copy
import json
import unittest

import construction_2026_ordinary as m


def card(d, key):
    return next(t['card'] for t in d['tasks'] if t['card']['id'] == m.PREFIX + key)


def binding(d, key):
    return next(b for b in d['bindings'] if b['cardId'] == m.PREFIX + key)


def drop(d, key):
    d['tasks'] = [t for t in d['tasks'] if t['card']['id'] != m.PREFIX + key]
    d['bindings'] = [b for b in d['bindings'] if b['cardId'] != m.PREFIX + key]
    d['addedIds'] = [i for i in d['addedIds'] if i != m.PREFIX + key]



def term_card(d):
    t = copy.deepcopy(next(t for t in d['tasks'] if t['card']['id'] == m.PREFIX + 'q8'))
    t['card']['id'] = m.PREFIX + 'q8-triple-glazing'
    return t


class SourceGuard(unittest.TestCase):
    def test_source_and_images(self):
        self.assertEqual(m.validate(json.loads(m.REVIEW.read_text()))['tasks'], 32)

    def test_rejects_lost_marks_wording_routes_or_topics(self):
        original = json.loads(m.REVIEW.read_text())
        cases = {
            'drawing allowance moved out of part (a)': lambda d: card(d, 'q1-a')['rows'].pop(),
            'invented question bonus': lambda d: card(d, 'q5-complete').update(questionBonus=dict(card(d, 'q5-a')['rows'][2], id='bonus')),
            'choice split into a per-term card': lambda d: d['tasks'].append(term_card(d)),
            'printed term list trimmed': lambda d: card(d, 'q8').update(questionText=card(d, 'q8')['questionText'].replace('; smart meter', '')),
            'term option dropped': lambda d: card(d, 'q8')['rows'][0]['group']['options'].pop(),
            'wrong claim limit': lambda d: card(d, 'q8')['rows'][0]['group'].update(claimMax=4),
            'lost required situation': lambda d: card(d, 'q6-a')['taskGroups'].pop(),
            'invented question wording': lambda d: card(d, 'q7-c').update(questionText='Discuss two reasons why gardens should face north.'),
            'paraphrased stem': lambda d: card(d, 'q5-a').update(stem='A door in a 300 mm wall with a 50 mm cavity.'),
            'marking row not in scheme': lambda d: card(d, 'q9-c')['rows'][0].update(verbatim='Teak is the only acceptable cladding'),
            'invented mark band': lambda d: card(d, 'q5-a')['rows'][2].update(permittedMarks=list(range(9))),
            'changed tariff': lambda d: card(d, 'q6-b')['rows'][0].update(marks=6, permittedMarks=list(range(7))),
            'missing Atlas association': lambda d: binding(d, 'q1-a')['atlasTopicIds'].pop(),
            'missing term topic': lambda d: binding(d, 'q8')['canonicalTopicIds'].pop(),
            'undeclared taxonomy gap': lambda d: binding(d, 'q9-a')['canonicalTopicIds'].append('cons-10-4'),
            'broken composite topic union': lambda d: binding(d, 'q9-complete')['atlasTopicIds'].pop(),
            'unreviewed source crop': lambda d: d['questionFigures'][3].update(visuallyInspected=False),
            'cut off drawing': lambda d: d['questionFigures'][9].update(rect=[50, 138, 545, 300]),
            'solution shown before reveal': lambda d: card(d, 'q3-a').update(questionFigureKey=m.FP + 'q3-system'),
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
