import copy
import json
import unittest

import construction_2025_higher as m


def card(d, key):
    return next(t['card'] for t in d['tasks'] if t['card']['id'] == m.PREFIX + key)


def binding(d, key):
    return next(b for b in d['bindings'] if b['cardId'] == m.PREFIX + key)


def drop(d, key):
    d['tasks'] = [t for t in d['tasks'] if t['card']['id'] != m.PREFIX + key]
    d['bindings'] = [b for b in d['bindings'] if b['cardId'] != m.PREFIX + key]
    d['addedIds'] = [i for i in d['addedIds'] if i != m.PREFIX + key]



def item_card(d, key, new_key):
    t = copy.deepcopy(next(t for t in d['tasks'] if t['card']['id'] == m.PREFIX + key))
    t['card']['id'] = m.PREFIX + new_key
    return t


class SourceGuard(unittest.TestCase):
    def test_source_and_images(self):
        self.assertEqual(m.validate(json.loads(m.REVIEW.read_text()))['tasks'], 49)

    def test_rejects_lost_marks_wording_routes_topics_or_corrections(self):
        original = json.loads(m.REVIEW.read_text())
        passive = card(original, 'q10-a-building-form')
        cases = {
            'choice split into a per-location card': lambda d: d['tasks'].append(item_card(d, 'q8-b', 'q8-b-door-head')),
            'consolidated item card reintroduced': lambda d: d['tasks'].append(item_card(d, 'q2-a-safety-training', 'q2-a-health-and-safety-officer')),
            'option dropped from a choice': lambda d: card(d, 'q2-a-safety-training')['rows'][0]['group']['options'].pop(),
            'wrong claim limit': lambda d: card(d, 'q10-a-building-form')['rows'][0]['group'].update(claimMax=3),
            'printed list trimmed': lambda d: card(d, 'q10-a-building-form').update(questionText=card(d, 'q10-a-building-form')['questionText'].replace('; space heating energy demand', '')),
            'consolidation not hash-linked': lambda d: d['consolidatedLegacy'][0].update(preCorrectionSha256='0' * 64),
            'consolidated card aliased to the wrong card': lambda d: d['consolidatedLegacy'][2].update(aliasOf=m.PREFIX + 'q10-b'),
            'alternative combined with Passive House': lambda d: card(d, 'q10-alt-complete')['taskGroups'].append(dict(sourceCardId=passive['id'], label='a', marks=10, rowIds=[])),
            'invented location label': lambda d: card(d, 'q8-b')['rows'][0]['group']['options'].__setitem__(2, 'Chimney junction'),
            'invented activity label': lambda d: card(d, 'q2-c-deep-trench').update(questionText=card(d, 'q2-c-deep-trench')['questionText'].replace('working in a deep trench', 'working on a flat roof')),
            'lost part in the complete question': lambda d: card(d, 'q8-complete')['taskGroups'].pop(1),
            'invented question wording': lambda d: card(d, 'q6-c').update(questionText='Explain why local materials are always cheaper.'),
            'paraphrased stem': lambda d: card(d, 'q7-a').update(stem='A chimney with a 45° roof pitch.'),
            'marking row not in scheme': lambda d: card(d, 'q9-a')['rows'][0].update(verbatim='Any sensible circuit'),
            'changed tariff': lambda d: card(d, 'q7-a')['rows'][1].update(marks=8, permittedMarks=list(range(9))),
            'dropped drawing allowance': lambda d: card(d, 'q1-a')['rows'].pop(),
            'invented mark band': lambda d: card(d, 'q1-a')['rows'][3].update(permittedMarks=list(range(9))),
            'wrong worked answer': lambda d: card(d, 'q5-b')['rows'][4].update(contextNote='Cost = €67.34 per year.'),
            'missing Atlas association': lambda d: binding(d, 'q8-b')['atlasTopicIds'].pop(),
            'canonical node outside the crosswalk': lambda d: binding(d, 'q2-b-deep-trench')['canonicalTopicIds'].append('cons-1-7'),
            'broken composite topic union': lambda d: binding(d, 'q8-complete')['atlasTopicIds'].pop(),
            'choice card q8-b loses its composite solution figure': lambda d: card(d, 'q8-b').pop('figureKey'),
            'composite q8-locations loses an item panel': lambda d: next(f for f in d['questionFigures'] if f['key'] == m.FP + 'q8-locations')['panels'].pop(),
            'choice card q10-a-building-form loses its composite solution figure': lambda d: card(d, 'q10-a-building-form').pop('figureKey'),
            'composite q10-items loses an item panel': lambda d: next(f for f in d['questionFigures'] if f['key'] == m.FP + 'q10-items')['panels'].pop(),
            'unreviewed source crop': lambda d: d['questionFigures'][1].update(visuallyInspected=False),
            'cut off drawing': lambda d: d['questionFigures'][1].update(rect=[48, 46, 568, 400]),
            'solution shown before reveal': lambda d: card(d, 'q5-a').update(questionFigureKey=m.FP + 'q5-calculation'),
            'unclassified choice': lambda d: d['selectionLedger'].update(unclassified=1),
            'uncertain source': lambda d: d['sourceHashes'].update({m.P: 'changed'}),
            'correction loses its concept ID': lambda d: card(d, 'q10-b').update(conceptId='orientation'),
            'correction not hash-linked': lambda d: d['corrections'][0].update(priorSha256='0' * 64),
            'legacy card replaced without a record': lambda d: d['corrections'].pop(),
            'legacy card counted as an addition': lambda d: d['addedIds'].append(m.PREFIX + 'q9-a'),
        }
        for label, change in cases.items():
            with self.subTest(label=label):
                d = copy.deepcopy(original)
                change(d)
                with self.assertRaises(AssertionError):
                    m.validate(d, images=False)


if __name__ == '__main__':
    unittest.main()
