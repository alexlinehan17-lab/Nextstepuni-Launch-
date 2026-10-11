import copy
import json
import unittest

import construction_2015_ordinary as m


def card(d, key):
    return next(t['card'] for t in d['tasks'] if t['card']['id'] == m.PREFIX + key)


def binding(d, key):
    return next(b for b in d['bindings'] if b['cardId'] == m.PREFIX + key)


def drop(d, key):
    d['tasks'] = [t for t in d['tasks'] if t['card']['id'] != m.PREFIX + key]
    d['bindings'] = [b for b in d['bindings'] if b['cardId'] != m.PREFIX + key]
    d['addedIds'] = [i for i in d['addedIds'] if i != m.PREFIX + key]


ROUTE = 'q8-complete-box-dovetail-joint--triple-glazing--solar-panel--cordless-drill--skirting-board'


class SourceGuard(unittest.TestCase):
    def test_source_and_images(self):
        self.assertEqual(m.validate(json.loads(m.REVIEW.read_text()))['tasks'], 176)

    def test_rejects_lost_marks_wording_routes_or_topics(self):
        original = json.loads(m.REVIEW.read_text())
        bonus = card(original, 'q5-complete')['questionBonus']
        cases = {
            'drawing allowance attached to a part': lambda d: card(d, 'q1-a').update(questionBonus=copy.deepcopy(bonus)),
            'drawing allowance counted as a row': lambda d: card(d, 'q5-b')['rows'].append(dict(copy.deepcopy(bonus), id='quality')),
            'drawing allowance doubled': lambda d: card(d, 'q5-complete')['questionBonus'].update(marks=16, permittedMarks=[0, 8, 12, 16]),
            'lost choose-five route': lambda d: drop(d, ROUTE),
            'route terms reordered': lambda d: card(d, ROUTE)['taskGroups'].reverse(),
            'lost required insulation system': lambda d: card(d, 'q2-a')['taskGroups'].pop(),
            'invented question wording': lambda d: card(d, 'q7-c').update(questionText='Discuss two reasons why rainwater is free to drink.'),
            'paraphrased stem': lambda d: card(d, 'q5-a').update(stem='A strip foundation and timber wall with a 75 mm cavity.'),
            'marking row not in scheme': lambda d: card(d, 'q9-c')['rows'][0].update(verbatim='Varnish is the only acceptable finish'),
            'invented mark band': lambda d: card(d, 'q3-a')['rows'][1].update(permittedMarks=list(range(9))),
            'changed tariff': lambda d: card(d, 'q6-c')['rows'][0].update(marks=12, permittedMarks=[0, 6, 12]),
            'missing Atlas association': lambda d: binding(d, 'q1-a')['atlasTopicIds'].pop(),
            'missing constituent topic': lambda d: binding(d, 'q6-a-ear')['canonicalTopicIds'].pop(),
            'undeclared taxonomy gap': lambda d: binding(d, 'q9-c')['canonicalTopicIds'].append('cons-10-4'),
            'broken composite topic union': lambda d: binding(d, ROUTE)['atlasTopicIds'].pop(),
            'unreviewed source crop': lambda d: d['questionFigures'][3].update(visuallyInspected=False),
            'cut off drawing': lambda d: d['questionFigures'][1].update(rect=[54, 54, 568, 400]),
            'solution shown before reveal': lambda d: card(d, 'q7-a').update(questionFigureKey=m.FP + 'q7-water-butt'),
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
