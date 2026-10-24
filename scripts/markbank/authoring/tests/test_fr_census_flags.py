"""Every French paper-census flag is reviewed, and its class still holds.

The ledger (french-census-flag-review.json) gives each flag a class, a
written reason and its evidence. A new, changed or vanished flag fails here
until it is reviewed; each class is re-checked mechanically, so a flag cannot
stay classified once the fact behind its class stops being true.
"""
from pathlib import Path
import ast
import json
import re
import sys
import unittest

import fitz

AUTH = Path(__file__).resolve().parents[1]
ROOT = AUTH.parents[2]
sys.path.insert(0, str(AUTH))
from paper_census import census_subject  # noqa: E402

ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']


class FrenchCensusFlagReviewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = json.loads((AUTH / 'french-census-flag-review.json').read_text())
        cls.census = census_subject('french')
        cls.reading = {(p['year'], p['level']): p
                       for p in json.loads((AUTH / 'french-reading-review.json').read_text())['papers']}

    def key(self, row):
        return (row['year'], row['level'], row['type'], row['where'], row['detail'])

    def test_every_flag_is_reviewed_and_nothing_else(self):
        live = [self.key(dict(year=p['year'], level=p['level'], **f))
                for p in self.census['papers'] for f in p.get('flags', [])]
        reviewed = [self.key(row) for row in self.review['flags']]
        self.assertEqual(sorted(live), sorted(reviewed))
        self.assertEqual(self.review['censusFlagCount'], len(live))
        self.assertEqual(self.review['genuineMisses'], 0)
        for row in self.review['flags']:
            self.assertIn(row['class'], self.review['classes'], row)
            self.assertTrue(self.review['classes'][row['class']].strip())

    def test_each_class_still_holds(self):
        leaves = {(p['year'], p['level']): {tuple(l['key']): l['text'] for l in p['leaves']}
                  for p in self.census['papers']}
        for row in self.review['flags']:
            paper = leaves[(row['year'], row['level'])]
            if row['class'] == 'roman-run-in-letter-slot':
                found = ast.literal_eval(row['detail'].split(': ', 1)[1])
                self.assertEqual(found, ROMANS[:len(found)], row)
                self.assertTrue(row['evidence']['coveringCards'], row)
            elif row['class'] == 'joint-tariff-pair':
                section = re.fullmatch(r"\('([A-Z0-9]+)',\)", row['where']).group(1)
                for n in row['evidence']['missingNumbers']:
                    text = paper[(section, n - 1, None, None)]
                    self.assertIn(f'Question {n - 1}:', text, row)
                    self.assertIn(f'Question {n}:', text, row)
                    group = self.reading[(row['year'], row['level'])]['paperQuestionGroups'][f'{section}-Q{n - 1}']
                    self.assertEqual(group['questions'], [n - 1, n], row)
            elif row['class'] == 'stem-of-priced-parts':
                self.assertTrue(row['evidence']['pricedLeaves'] and row['evidence']['coveringCards'], row)
                self.assertRegex(row['evidence']['note'], r'^Paper p\d+ ', row)
            elif row['class'] == 'reviewed-scoring-decision':
                decision = self.reading[(row['year'], row['level'])]['scoringDecisions'][row['evidence']['readingLedgerAddress']]
                self.assertEqual(decision['parserFault'], row['detail'], row)
            elif row['class'] == 'printed-total-differs':
                total = 0
                for component in ('000', 'A00'):
                    path = ROOT / f"examiner-reports/french/papers/{row['year']}-{row['level']}-{component}-paper.pdf"
                    with fitz.open(path) as doc:
                        total += int(re.search(r'(\d{2,3})\s*marks\b', doc[0].get_text(), re.I).group(1))
                self.assertIn(f'marks sum {total}', row['detail'], row)
                marks = row['evidence']['coverMarks']
                self.assertEqual(marks['writtenBooklet'] + marks['listeningBooklet'], total, row)
            else:
                self.fail(f'unknown class {row}')


if __name__ == '__main__':
    unittest.main()
