"""Source-gate regressions for Japanese printed nested listening references."""
import unittest

from ja_review_refs import bind_japanese_ref, reviewed_japanese_refs
from reconcile import match_leaves, parse_ref


class PrintedJapaneseReferences(unittest.TestCase):
    def test_nested_tasks_cover_only_their_independently_censused_leaf(self):
        bindings = reviewed_japanese_refs()
        self.assertEqual(len(bindings), 12)
        self.assertEqual(sum(binding['q'] is None for binding in bindings.values()), 2)
        for cid, binding in bindings.items():
            with self.subTest(card=cid):
                section, q = binding['section'], binding['q']
                letter, roman = binding['path']
                other_letter = 'b' if letter == 'a' else 'a'
                leaves = [(section, q, letter, roman), (section, q, other_letter, roman),
                          (section, q, None, roman), (section, (q or 0) + 1, letter, roman)]
                generic = parse_ref(binding['literal'])
                self.assertNotEqual(generic['paths'], [(letter, roman)])
                bound = bind_japanese_ref(cid, binding['literal'], generic, bindings)
                self.assertEqual(match_leaves(bound, leaves, True), [leaves[0]])
                for changed in [binding['literal'].replace(f'({roman})({letter})', f'({letter})({roman})'),
                                binding['literal'].replace(f'({letter})', f'({other_letter})'),
                                binding['literal'].replace(str(binding['year']), str(binding['year'] + 1)),
                                binding['literal'] + ' — unrelated suffix']:
                    self.assertIsNone(bind_japanese_ref(cid, changed, parse_ref(changed), bindings))

    def test_unbound_generic_references_remain_identical(self):
        bindings = reviewed_japanese_refs()
        for cid, literal in [('ja-2024-hl-lb-1', '2024 HL Section LB Q1'),
                             ('ja-2025-hl-ld-2-a-i', '2025 HL Section LD Q2(a)(i)'),
                             ('maths-example', '2024 HL Paper 1 Q3(a)(i)'),
                             ('he-example', '2024 HL Section 2 Q3(ii)(a)')]:
            parsed = parse_ref(literal)
            self.assertIs(bind_japanese_ref(cid, literal, parsed, bindings), parsed)


if __name__ == '__main__':
    unittest.main()
