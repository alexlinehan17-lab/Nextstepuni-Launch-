"""Reconciliation must expose a lost split even when its parent still ships."""
import unittest
from unittest.mock import patch

from applied_census import census_applied_maths
from reconcile import reconcile_applied, shipped_cards


class AppliedReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.census = census_applied_maths(verify_sources=False)
        cls.cards = shipped_cards('applied-maths')

    def test_reviewed_inventory_reconciles_all_editions(self):
        result = reconcile_applied(self.census)
        self.assertEqual((result['cards'], result['leaves'], result['covered']), (1486, 1486, 1486))
        self.assertEqual((result['sourceEditions'], result['sourceTaskLinks'], result['nativeSchemes']), (66, 2972, 65))
        self.assertEqual((result['open'], result['orphans'], result['staleExclusions']), (0, [], []))

    def test_parent_citation_cannot_cover_a_missing_diagram(self):
        missing = 'am-2025-hl-5-a-i-y'
        changed = [(cid, '2025 HL Q5(a)(i)' if cid == 'am-2025-hl-5-a-i-x' else ref)
                   for cid, ref in self.cards if cid != missing]
        with patch('reconcile.shipped_cards', return_value=changed):
            result = reconcile_applied(self.census)
        self.assertEqual(result['open'], 2)
        self.assertEqual(len(result['orphans']), 1)

    def test_same_count_duplicate_does_not_hide_a_missing_task(self):
        changed = self.cards[:-1] + [self.cards[0]]
        with patch('reconcile.shipped_cards', return_value=changed):
            result = reconcile_applied(self.census)
        self.assertEqual(result['cards'], 1486)
        self.assertEqual(result['open'], 1)
        self.assertEqual(len(result['orphans']), 1)


if __name__ == '__main__':
    unittest.main()
