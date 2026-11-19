"""Mandatory 2017 Higher original-PDF authoring gate, separate from runtime CI.

Run: python3 scripts/markbank/authoring/test_ru_2017_hl_sources.py
Requires the pinned original written/aural papers and marking scheme.
"""
import copy
import json
import unittest
from pathlib import Path

from ru_review_2017_hl import build
from ru_review_census import reviewed_keys
from ru_verify_review import verify

ROOT = Path(__file__).resolve().parents[3]


class Russian2017OriginalSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = build()

    def test_all_published_cards_match_the_original_source_authoring(self):
        published = json.loads((ROOT / 'scripts/markbank/authored/russian-reviewed.json').read_text())
        sitting = [card for card in published if card['year'] == 2017 and card['level'] == 'higher']
        self.assertEqual(sorted(self.cards, key=lambda card: card['id']), sorted(sitting, key=lambda card: card['id']))
        verify(self.cards)

    def test_independent_original_census_is_complete(self):
        self.assertEqual(len(reviewed_keys(2017, 'hl')), 39)

    def test_invented_or_wrong_page_alternative_rule_is_rejected(self):
        original = next(card for card in self.cards if card['id'] == 'ru-2017-hl-c2-4')
        for change in ({'sourceText': 'Invented mutually exclusive route rule'}, {'schemePages': [6]}):
            with self.subTest(change=change):
                card = copy.deepcopy(original)
                card['rubric']['alternativeSets'][0].update(change)
                with self.assertRaises(AssertionError):
                    verify([card])


if __name__ == '__main__':
    unittest.main()
