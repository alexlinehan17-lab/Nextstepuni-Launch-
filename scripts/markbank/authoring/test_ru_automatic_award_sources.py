"""Mandatory original-page gate for the 2010 award to every candidate."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
import fitz
from ru_verify_review import verify_automatic_award_sources

ROOT = Path(__file__).resolve().parents[3]
ORIGINAL_SHA256 = '15607f22c24d4502dee8d28cd319711c880d27d06eac33b1da96fa6554a0672c'


class AutomaticAwardOriginals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / 'examiner-reports/russian/schemes/2010-hl.pdf'
        assert hashlib.sha256(cls.path.read_bytes()).hexdigest() == ORIGINAL_SHA256
        cls.card = json.loads((ROOT / 'test/fixtures/russian2010UniversalAward.json').read_text())

    def test_exact_universal_award_occurs_on_original_physical_page_five(self):
        with fitz.open(self.path) as document:
            verify_automatic_award_sources(document, self.card)
            text = document[4].get_text(sort=True)
            self.assertIn('Give an example of a plural noun in the dative case:', text)
            self.assertIn('award 2 marks to all (there is no noun in the dative case)', text)

    def test_wrong_page_empty_and_invented_awards_fail(self):
        with fitz.open(self.path) as document:
            for update in [{'schemePages': [1]}, {'schemePages': []}, {'schemePages': [0]},
                           {'sourceText': 'Always award twelve marks to all candidates.'}, {'sourceText': ' '}]:
                card = copy.deepcopy(self.card)
                card['rubric']['criteria'][3]['automaticAward'].update(update)
                with self.assertRaises(AssertionError):
                    verify_automatic_award_sources(document, card)

    def test_manual_zero_conditions_deductions_and_language_adjustments_fail(self):
        with fitz.open(self.path) as document:
            for update in [{'permittedMarks': [0, 2]}, {'maxMarks': 4}, {'limits': []}, {'bands': []}, {'kind': 'deduction'}]:
                card = copy.deepcopy(self.card)
                card['rubric']['criteria'][3].update(update)
                with self.assertRaises(AssertionError):
                    verify_automatic_award_sources(document, card)
            card = copy.deepcopy(self.card)
            card['answerLanguageRule'] = {'otherLanguageMultiplier': 0}
            with self.assertRaises(AssertionError):
                verify_automatic_award_sources(document, card)


if __name__ == '__main__':
    unittest.main()
