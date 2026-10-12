import copy
import json
import unittest

import construction_2015_higher as m


def card(d, key):
    return next(t['card'] for t in d['tasks'] if t['card']['id'] == m.PREFIX + key)


def binding(d, key):
    return next(b for b in d['bindings'] if b['cardId'] == m.PREFIX + key)


def item_card(d, key, new_key):
    t = copy.deepcopy(next(t for t in d['tasks'] if t['card']['id'] == m.PREFIX + key))
    t['card']['id'] = m.PREFIX + new_key
    return t


class SourceGuard(unittest.TestCase):
    def test_source_and_images(self):
        self.assertEqual(m.validate(json.loads(m.REVIEW.read_text()))['tasks'], 48)

    def test_rejects_lost_marks_wording_routes_topics_or_corrections(self):
        original = json.loads(m.REVIEW.read_text())
        passive = card(original, 'q10-a')
        cases = {
            'choice split into a per-location card': lambda d: d['tasks'].append(item_card(d, 'q9-a', 'q9-a-eaves')),
            'choice split into a per-option route': lambda d: d['tasks'].append(item_card(d, 'q3-b', 'q3-b-A')),
            'option dropped from a choice': lambda d: card(d, 'q4-b')['rows'][0]['group']['options'].pop(),
            'wrong claim limit': lambda d: card(d, 'q9-a')['rows'][0]['group'].update(claimMax=4),
            'per-option marks changed': lambda d: card(d, 'q10-a')['rows'][0]['group'].update(perOption=8),
            'printed list trimmed': lambda d: card(d, 'q6-b').update(questionText=card(d, 'q6-b')['questionText'].replace('; low maintenance', '')),
            'invented location label': lambda d: card(d, 'q9-a')['rows'][0]['group']['options'].__setitem__(2, 'Head of window'),
            'invented option label': lambda d: card(d, 'q3-a-A').update(questionText=card(d, 'q3-a-A')['questionText'].replace('Option A', 'Option C')),
            'alternative combined with Passive House': lambda d: card(d, 'q10-alt-complete')['taskGroups'].append(dict(sourceCardId=passive['id'], label='a', marks=32, rowIds=[])),
            'lost part in the complete question': lambda d: card(d, 'q3-complete')['taskGroups'].pop(1),
            'invented question wording': lambda d: card(d, 'q6-c').update(questionText='Explain why NZEB houses are always cheaper to build.'),
            'paraphrased stem': lambda d: card(d, 'q7-a').update(stem='A cut roof at 45 degrees with an attic floor.'),
            'authored route commentary in the stem': lambda d: card(d, 'q4-a').update(stem='Part (a) selects any TWO of the three principles.'),
            'marking row not in scheme': lambda d: card(d, 'q3-b')['rows'][0].update(verbatim='Any attractive design'),
            'changed tariff': lambda d: card(d, 'q3-c')['rows'][1].update(marks=4, permittedMarks=list(range(5))),
            'dropped drawing allowance': lambda d: card(d, 'q1-a')['rows'].pop(),
            'invented mark band': lambda d: card(d, 'q1-a')['rows'][1].update(permittedMarks=list(range(9))),
            'wrong worked answer': lambda d: card(d, 'q5-b-existing')['rows'][4].update(contextNote='Cost = €76.34 per year.'),
            'missing Atlas association': lambda d: binding(d, 'q9-a')['atlasTopicIds'].pop(),
            'broken composite topic union': lambda d: binding(d, 'q4-complete')['atlasTopicIds'].pop(),
            'choice card q4-a loses its composite solution figure': lambda d: card(d, 'q4-a').pop('figureKey'),
            'composite q4-discussion loses an item panel': lambda d: next(f for f in d['questionFigures'] if f['key'] == m.FP + 'q4-discussion')['panels'].pop(),
            'choice card q4-complete loses its composite solution figure': lambda d: card(d, 'q4-complete').pop('figureKey'),
            'composite q4-scheme loses an item panel': lambda d: next(f for f in d['questionFigures'] if f['key'] == m.FP + 'q4-scheme')['panels'].pop(),
            'unreviewed source crop': lambda d: d['questionFigures'][1].update(visuallyInspected=False),
            'cut off drawing': lambda d: d['questionFigures'][1].update(rect=[60, 104, 558, 500]),
            'cut off panel': lambda d: next(f for f in d['questionFigures'] if f['key'].endswith('q9-scheme'))['panels'].pop(),
            'solution shown before reveal': lambda d: card(d, 'q5-a').update(questionFigureKey=m.FP + 'q5-window-head'),
            'unclassified choice': lambda d: d['selectionLedger'].update(unclassified=1),
            'uncertain source': lambda d: d['sourceHashes'].update({m.P: 'changed'}),
            'correction loses its concept ID': lambda d: card(d, 'q10-b').update(conceptId='thermal-mass'),
            'correction not hash-linked': lambda d: d['corrections'][0].update(priorSha256='0' * 64),
            'earlier card replaced without a record': lambda d: d['corrections'].pop(),
            'earlier card counted as an addition': lambda d: d['addedIds'].append(m.PREFIX + 'q9-b'),
            'withdrawal not recorded': lambda d: d['withdrawn'].pop(),
            'withdrawal not hash-linked': lambda d: d['withdrawn'][0].update(priorSha256='0' * 64),
        }
        for label, change in cases.items():
            with self.subTest(label=label):
                d = copy.deepcopy(original)
                change(d)
                with self.assertRaises(AssertionError):
                    m.validate(d, images=False)


if __name__ == '__main__':
    unittest.main()
