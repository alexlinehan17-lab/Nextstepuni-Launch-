import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

import fitz

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fr_selection import scan_paper, verify_paper


class SelectionReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'example.pdf'
        with fitz.open() as doc:
            page = doc.new_page()
            page.insert_text((40, 40), 'Choose three of the following five points.\nAnswer either task A or task B.')
            doc.save(self.path)
        self.rows = scan_paper(self.path)
        self.ledger = {'papers': {self.path.name: {
            'sha256': hashlib.sha256(self.path.read_bytes()).hexdigest(),
            'directives': [dict(row, policy='finite-pool', reason='Reviewed printed five-point pool.',
                                task='B2A', choose=3, poolSize=5, routes=10) for row in self.rows],
        }}}

    def test_detects_task_internal_selection(self):
        phrases = [row['phrase'].lower() for row in self.rows]
        self.assertIn('choose', phrases)
        self.assertIn('three of', phrases)
        self.assertIn('either', phrases)
        self.assertEqual(verify_paper(self.path, self.ledger), self.rows)

    def test_rejects_one_unclassified_directive(self):
        record = self.ledger['papers'][self.path.name]
        record['directives'].pop()
        with self.assertRaisesRegex(ValueError, 'Unclassified or stale'):
            verify_paper(self.path, self.ledger)

    def test_rejects_source_drift_and_text_drift(self):
        record = self.ledger['papers'][self.path.name]
        good = copy.deepcopy(record)
        record['sha256'] = 'old document'
        with self.assertRaisesRegex(ValueError, 'source changed'):
            verify_paper(self.path, self.ledger)
        self.ledger['papers'][self.path.name] = good
        good['directives'][0]['context'] = 'different instruction'
        with self.assertRaisesRegex(ValueError, 'text mismatch'):
            verify_paper(self.path, self.ledger)

    def test_rejects_wrong_combinatorics(self):
        self.ledger['papers'][self.path.name]['directives'][0]['routes'] = 5
        with self.assertRaisesRegex(ValueError, 'route count is wrong'):
            verify_paper(self.path, self.ledger)

    def test_page_review_cannot_authorize_a_whole_paper(self):
        record = self.ledger['papers'].pop(self.path.name)
        record['pages'] = [1]
        self.ledger['papers'][self.path.name + '#pages=1'] = record
        self.assertEqual(verify_paper(self.path, self.ledger, pages=[1]), self.rows)
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            verify_paper(self.path, self.ledger)


if __name__ == '__main__':
    unittest.main()
