import copy
import json
import unittest

import construction_2024_ordinary as m


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
        self.assertEqual(m.validate(json.loads(m.REVIEW.read_text()))['tasks'], 30)

    def test_rejects_lost_marks_wording_routes_topics_or_corrections(self):
        original = json.loads(m.REVIEW.read_text())
        cases = {
            'choice split into a per-term card': lambda d: d['tasks'].append(item_card(d, m.Q8, 'q8-None-plywood')),
            'term dropped from the choice': lambda d: card(d, m.Q8)['rows'][0]['group']['options'].pop(),
            'wrong claim limit': lambda d: card(d, m.Q8)['rows'][0]['group'].update(claimMax=4),
            'printed term list trimmed': lambda d: card(d, m.Q8).update(questionText=card(d, m.Q8)['questionText'].replace('; heat pump', '')),
            'choice card loses its composite solution figure': lambda d: card(d, m.Q8).pop('figureKey'),
            'composite loses a term page': lambda d: next(f for f in d['questionFigures'] if f['key'] == m.FP + 'q8-terms')['panels'].pop(),
            'consolidation not hash-linked': lambda d: d['consolidatedLegacy'][0].update(preCorrectionSha256='0' * 64),
            'consolidated card aliased to the wrong card': lambda d: d['consolidatedLegacy'][2].update(aliasOf=m.PREFIX + 'q9-c'),
            'withdrawal not recorded': lambda d: d['withdrawn'].pop(),
            'lost part in the complete question': lambda d: card(d, 'q7-complete')['taskGroups'].pop(1),
            'invented question wording': lambda d: card(d, 'q6-c').update(questionText='Explain why dumpers are always unsafe.'),
            'paraphrased stem': lambda d: card(d, 'q5-a').update(stem='A window in a cavity wall with a cill.'),
            'marking row not in scheme': lambda d: card(d, 'q4-b')['rows'][0].update(verbatim='Any sensible foundation'),
            'changed tariff': lambda d: card(d, 'q7-b')['rows'][0].update(marks=6, permittedMarks=list(range(7))),
            'dropped drawing allowance': lambda d: card(d, 'q1-a')['rows'].pop(),
            'invented mark band': lambda d: card(d, 'q5-a')['rows'][1].update(permittedMarks=list(range(7))),
            'missing Atlas association': lambda d: binding(d, m.Q8)['atlasTopicIds'].pop(),
            'undeclared taxonomy gap': lambda d: binding(d, 'q4-b')['canonicalTopicIds'].append('cons-2-5'),
            'broken composite topic union': lambda d: binding(d, 'q9-complete')['atlasTopicIds'].pop(),
            'unreviewed source crop': lambda d: d['questionFigures'][1].update(visuallyInspected=False),
            'cut off drawing': lambda d: next(f for f in d['questionFigures'] if f['key'] == m.FP + 'q5-section').update(rect=[51, 58, 531, 300]),
            'solution shown before reveal': lambda d: card(d, 'q3-a').update(questionFigureKey=m.FP + 'q3-system'),
            'unclassified choice': lambda d: d['selectionLedger'].update(unclassified=1),
            'uncertain source': lambda d: d['sourceHashes'].update({m.P: 'changed'}),
            'correction loses its concept ID': lambda d: card(d, 'q2-a').update(conceptId='ber'),
            'correction not hash-linked': lambda d: d['corrections'][0].update(priorSha256='0' * 64),
            'legacy card replaced without a record': lambda d: d['corrections'].pop(),
            'legacy card counted as an addition': lambda d: d['addedIds'].append(m.PREFIX + 'q9-c'),
        }
        for label, change in cases.items():
            with self.subTest(label=label):
                d = copy.deepcopy(original)
                change(d)
                with self.assertRaises(AssertionError):
                    m.validate(d, images=False)


if __name__ == '__main__':
    unittest.main()
