"""Mandatory original-PDF gate; run separately from portable runtime tests.

Requires all three hash-pinned original PDFs. Missing originals fail this gate.
"""
import copy
import unittest
from ru_review_2016_hl import build
from ru_review_census import reviewed_keys
from ru_verify_review import verify
from reconcile import parse_ref


class Original2016Sources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = build()

    def test_all_original_sources_and_independent_census(self):
        verify(self.cards)
        keys = set()
        for card in self.cards:
            ref = parse_ref(card['questionRef'])
            self.assertIsNotNone(ref)
            keys.update((ref['section'], ref['q'], letter, roman) for letter, roman in ref['paths'])
        self.assertEqual(keys, reviewed_keys(2016, 'hl'))
        self.assertEqual(len(keys), 40)
        self.assertEqual(sum(card['totalMarks'] for card in self.cards), 300)

    def test_alternative_rule_must_use_declared_original_page(self):
        card = copy.deepcopy(next(c for c in self.cards if c['id'] == 'ru-2016-hl-l2-2'))
        card['rubric']['alternativeSets'][0]['schemePages'] = [15]
        with self.assertRaises(AssertionError):
            verify([card])

    def test_invented_grouped_detail_guidance_fails(self):
        card = copy.deepcopy(next(c for c in self.cards if c['id'] == 'ru-2016-hl-l1-2'))
        card['rubric']['groups'][1]['criteria'][0]['guidance'] = ['Invented source rule: all travel answers are mutually exclusive.']
        with self.assertRaises(AssertionError):
            verify([card])

    def test_single_smoking_event_is_bound_to_original_passage(self):
        card = next(c for c in self.cards if c['id'] == 'ru-2016-hl-c2-4')
        binding = card['review']['paperAnswerSources'][0]
        self.assertEqual(binding['text'], 'курили')
        self.assertEqual(binding['pages'], [7])
        broken = copy.deepcopy(card)
        broken['review']['paperAnswerSources'][0]['pages'] = [2]
        with self.assertRaises(AssertionError):
            verify([broken])


if __name__ == '__main__':
    unittest.main()
