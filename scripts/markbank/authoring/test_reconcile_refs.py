"""Coverage must retain every named part without borrowing adjacent tasks."""
import json
from pathlib import Path
import unittest

from reconcile import parse_ref


class CompoundReferencesTest(unittest.TestCase):
    def test_repeated_question_numbers_and_cross_letter_groups(self):
        cases = [
            ('Q5(b)(i),Q5(b)(ii)', [('b', 'i'), ('b', 'ii')]),
            ('Q9(a), Q9(b)', [('a', None), ('b', None)]),
            ('Q8(b)(i),Q8(b)(ii),Q8(b)(iii)', [('b', 'i'), ('b', 'ii'), ('b', 'iii')]),
            ('Q10(b)(i),Q10(b)(ii),Q10(c)(i),Q10(c)(ii)',
             [('b', 'i'), ('b', 'ii'), ('c', 'i'), ('c', 'ii')]),
            ('Q6A(a), Q6A(b)', [('a', None), ('b', None)]),
            ('Q4(ii), Q4(iii)', [(None, 'ii'), (None, 'iii')]),
            ('Q5(b)(i) and Q5(b)(ii)', [('b', 'i'), ('b', 'ii')]),
        ]
        for ref, expected in cases:
            with self.subTest(ref=ref):
                self.assertEqual(parse_ref('2026 HL Paper 1 ' + ref)['paths'], expected)

    def test_different_questions_or_routes_fail_instead_of_false_coverage(self):
        for ref in ['Q5(b)(i),Q6(b)(ii)', 'Q6A(a),Q6B(b)',
                    'Q5(a),Q5-alt(b)', 'Q5-alt(a),Q5(b)',
                    'Q5(a)Q5(b)']:
            with self.subTest(ref=ref):
                self.assertIsNone(parse_ref('2026 HL Paper 1 ' + ref))

    def test_existing_shorthand_and_annotations_stay_precise(self):
        for ref, expected in [
            ('Q5(b)(i), (ii)', [('b', 'i'), ('b', 'ii')]),
            ('Q6(a)–(c)', [('a', None), ('b', None), ('c', None)]),
            ('Q8(b)(i) — explain Q9(a)', [('b', 'i')]),
        ]:
            with self.subTest(ref=ref):
                self.assertEqual(parse_ref('2026 HL Paper 1 ' + ref)['paths'], expected)

    def test_every_2026_group_matches_the_visually_reviewed_parts(self):
        root = Path(__file__).resolve().parents[3]
        cards = {c['id']: c for c in json.loads((root / 'scripts/markbank/authored/maths.json').read_text())}
        groups = 0
        for path in sorted((root / 'scripts/markbank/mathematics/reviews').glob('2026-*.json')):
            review = json.loads(path.read_text())
            if review['level'] == 'foundation':
                continue
            for card in review['cards']:
                if len(card['printedParts']) < 2:
                    continue
                expected = [parse_ref('2026 HL ' + part)['paths'][0] for part in card['printedParts']]
                with self.subTest(card=card['id']):
                    actual = parse_ref(cards[card['id']]['questionRef'])
                    self.assertEqual(actual['paths'], expected)
                groups += 1
        self.assertEqual(groups, 29)


if __name__ == '__main__':
    unittest.main()
