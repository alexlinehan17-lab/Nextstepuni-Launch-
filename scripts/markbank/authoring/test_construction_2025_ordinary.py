import copy
import json
import unittest

import construction_2025_ordinary as m


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
    t['card']['id'] = m.PREFIX + 'q8-raft-foundation'
    return t


class SourceGuard(unittest.TestCase):
    def test_source_and_images(self):
        self.assertEqual(m.validate(json.loads(m.REVIEW.read_text()))['tasks'], 35)

    def test_rejects_lost_marks_wording_routes_topics_or_corrections(self):
        original = json.loads(m.REVIEW.read_text())
        cases = {
            'choice split into a per-term card': lambda d: d['tasks'].append(term_card(d)),
            'printed term list trimmed': lambda d: card(d, 'q8').update(questionText=card(d, 'q8')['questionText'].replace('; baluster', '')),
            'term option dropped': lambda d: card(d, 'q8')['rows'][0]['group']['options'].pop(),
            'wrong claim limit': lambda d: card(d, 'q8')['rows'][0]['group'].update(claimMax=4),
            'required PPE item dropped': lambda d: card(d, 'q6-a')['taskGroups'].pop(),
            'invented question wording': lambda d: card(d, 'q9-c').update(questionText='Explain why gardens are always worth more.'),
            'paraphrased stem': lambda d: card(d, 'q5-a').update(stem='A stairs with a 200 mm rise.'),
            'marking row not in scheme': lambda d: card(d, 'q4-b')['rows'][0].update(verbatim='Any sensible site layout'),
            'changed tariff': lambda d: card(d, 'q2-b')['rows'][1].update(marks=6, permittedMarks=list(range(7))),
            'dropped drawing allowance': lambda d: card(d, 'q1-a')['rows'].pop(),
            'invented mark band': lambda d: card(d, 'q3-a')['rows'][1].update(permittedMarks=list(range(6))),
            'partial credit for an all-or-nothing row': lambda d: card(d, 'q1-b')['rows'][0].update(permittedMarks=list(range(5))),
            'unmarked site selection': lambda d: card(d, 'q4-a')['rows'].pop(0),
            'missing Atlas association': lambda d: binding(d, 'q8')['atlasTopicIds'].pop(),
            'undeclared taxonomy gap': lambda d: d['taxonomyGaps'].pop(),
            'broken composite topic union': lambda d: binding(d, 'q6-complete')['atlasTopicIds'].pop(),
            'unreviewed source crop': lambda d: d['questionFigures'][10].update(visuallyInspected=False),
            'cut off drawing': lambda d: d['questionFigures'][10].update(rect=[80, 108, 480, 300]),
            'solution shown before reveal': lambda d: card(d, 'q3-a').update(questionFigureKey=m.FP + 'q3-system'),
            'unclassified choice': lambda d: d['selectionLedger'].update(unclassified=1),
            'uncertain source': lambda d: d['sourceHashes'].update({m.P: 'changed'}),
            'correction loses its concept ID': lambda d: card(d, 'q7-b').update(conceptId='office-layout'),
            'correction not hash-linked': lambda d: d['corrections'][0].update(priorSha256='0' * 64),
            'legacy card replaced without a record': lambda d: d['corrections'].pop(),
            'legacy card counted as an addition': lambda d: d['addedIds'].append(m.PREFIX + 'q6-a'),
        }
        for label, change in cases.items():
            with self.subTest(label=label):
                d = copy.deepcopy(original)
                change(d)
                with self.assertRaises(AssertionError):
                    m.validate(d, images=False)


if __name__ == '__main__':
    unittest.main()
