"""Mandatory Russian 2015 original-PDF/census gate, separate from Vitest."""
import copy
import json
import unittest
from pathlib import Path
from reconcile import parse_ref
from ru_review_2015_hl import build
from ru_review_census import reviewed_keys
from ru_verify_review import verify


class Original2015Sources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = build()

    def test_originals_and_44_leaf_census_for_43_priced_tasks(self):
        verify(self.cards)
        keys = set()
        for card in self.cards:
            ref = parse_ref(card['questionRef'])
            self.assertIsNotNone(ref)
            keys.update((ref['section'], ref['q'], letter, roman) for letter, roman in ref['paths'])
        self.assertEqual(keys, reviewed_keys(2015, 'hl'))
        self.assertEqual(len(keys), 44)
        self.assertEqual(len(self.cards), 43)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards), 300)

    def test_authored_sitting_equals_original_derived_cards(self):
        root = Path(__file__).resolve().parents[3]
        authored = json.loads((root/'scripts/markbank/authored/russian-reviewed.json').read_text())
        published = [c for c in authored if c['year']==2015 and c['level']=='higher']
        self.assertEqual({c['id']:c for c in published}, {c['id']:c for c in self.cards})

    def test_conditional_rule_must_use_its_own_original_page(self):
        c=copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2015-hl-l3-1'))
        c['rubric']['allocationCap']['limits'][0]['schemePages']=[15]
        with self.assertRaises(AssertionError):verify([c])

    def test_invented_conditional_rule_fails(self):
        c=copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2015-hl-l3-1'))
        c['rubric']['allocationCap']['limits'][0]['sourceText']='Invented rule: five marks for mentioning employment.'
        with self.assertRaises(AssertionError):verify([c])

    def test_overlapping_descriptor_grid_stays_literal(self):
        c=copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2015-hl-gw'))
        criterion=next(x for x in c['rubric']['criteria'] if x['id']=='expression')
        lower=next(x for x in criterion['limits'] if x['id']=='lower-a')
        self.assertEqual((lower['minMarks'],lower['maxMarks']), (7,12))
        self.assertNotIn('bands',lower)
        self.assertIn('9 -11',lower['guidance'][2])
        lower['guidance'][2]='Invented non-overlapping replacement descriptor for nine and ten.'
        with self.assertRaises(AssertionError):verify([c])


if __name__=='__main__':unittest.main()
