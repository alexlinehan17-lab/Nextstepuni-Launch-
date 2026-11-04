"""Every French paper variant is carded or deferred with a reason, and stays so.

Recomputes the alignment from Paper Trail, the local sources, the shipped
decks, the Atlas tasks and the paper census, and fails on any drift from
french-variant-alignment.json.
"""
from pathlib import Path
import json
import sys
import unittest

AUTH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTH))
import fr_variant_alignment as alignment  # noqa: E402


class FrenchVariantAlignmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(alignment.LEDGER.read_text())
        cls.live = alignment.build()

    def test_ledger_matches_the_live_corpus(self):
        self.assertEqual(self.live, self.ledger)

    def test_every_variant_is_accounted_for(self):
        rows = self.ledger['variants']
        self.assertEqual(len(rows), 98)
        self.assertEqual(self.ledger['carded'] + self.ledger['deferred'], 98)
        for row in rows:
            if row['lang'] == 'ev':
                self.assertEqual(row['status'], 'carded', row)
                self.assertEqual(row['sittingCensus']['open'], 0, row)
                self.assertTrue(row['cards'] and row['atlasTasks'], row)
            else:
                self.assertEqual(row['status'], 'deferred', row)
                self.assertTrue(row['reason'].startswith('Irish-language (IV) edition.'), row)
                twin = next(r for r in rows if r['paper'] == row['englishCounterpart'])
                self.assertEqual(twin['status'], 'carded', row)


if __name__ == '__main__':
    unittest.main()
