"""Original-archive checks for the source-specific six-question 2010 checksum.

Run alongside ja_review_verify.py; ordinary unit tests use committed census
evidence and do not require the ignored SEC archive.
"""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from ja_review_census import reviewed_census

REVIEWS = Path(__file__).with_name('reviews')


class JapaneseReviewedCensus(unittest.TestCase):
    def test_2010_higher_six_questions_have_their_original_allocations(self):
        review = reviewed_census(2010, 'hl')
        self.assertEqual(len(review['tasks']), 66)
        self.assertEqual(review['checksums'], {
            'reading': 100, 'grammar': 20, 'writing': 100,
            'listening': 80, 'total': 300,
        })
        self.assertEqual([task['marks'] for task in review['tasks'] if task['key'][0] in ['5', '6']], [40, 60])
        self.assertEqual({task['key'][0][0] for task in review['tasks'] if task['component'] == 'paper'}, set('123456'))

    def test_missing_sixth_question_and_inherited_five_question_totals_fail(self):
        original = json.loads((REVIEWS / 'japanese-2010-hl-census.json').read_text())
        missing = copy.deepcopy(original)
        missing['tasks'] = [task for task in missing['tasks'] if task['key'][0] != '6']
        inherited = copy.deepcopy(original)
        inherited['checksums'] = {'reading': 100, 'writing': 60, 'listening': 80, 'total': 300}
        wrong_boundary = copy.deepcopy(original)
        next(task for task in wrong_boundary['tasks'] if task['key'][0] == '6')['key'][0] = '4C'
        for changed in [missing, inherited, wrong_boundary]:
            with self.subTest(checksums=changed['checksums']), patch('ja_review_census.json.loads', return_value=changed):
                with self.assertRaisesRegex(AssertionError, 'printed totals do not reconcile'):
                    reviewed_census(2010, 'hl')

    def test_original_hash_and_complete_physical_page_sweep_remain_mandatory(self):
        original = json.loads((REVIEWS / 'japanese-2010-hl-census.json').read_text())
        changed_source = copy.deepcopy(original)
        changed_source['sources'][0]['sha256'] = 'changed'
        missing_page = copy.deepcopy(original)
        del missing_page['pageRoles']['scheme']['15']
        for changed, message in [(changed_source, 'source changed'), (missing_page, 'source page not reviewed')]:
            with self.subTest(message=message), patch('ja_review_census.json.loads', return_value=changed):
                with self.assertRaisesRegex(AssertionError, message):
                    reviewed_census(2010, 'hl')

    def test_prior_higher_and_ordinary_checksum_contracts_are_unchanged(self):
        for year, level, expected in [
            (2011, 'hl', {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}),
            (2011, 'ol', {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}),
            (2026, 'hl', {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}),
        ]:
            with self.subTest(year=year, level=level):
                self.assertEqual(reviewed_census(year, level)['checksums'], expected)


if __name__ == '__main__':
    unittest.main()
