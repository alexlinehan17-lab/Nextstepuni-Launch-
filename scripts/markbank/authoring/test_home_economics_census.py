"""Source-backed Home Economics census corrections; no card-count shortcut."""
import hashlib
import json
from pathlib import Path
import unittest

import fitz

from paper_census import census_sections

ROOT = Path(__file__).resolve().parents[3]


class HomeEconomicsNestedDevicesTest(unittest.TestCase):
    def test_device_labels_do_not_move_the_following_safety_ask(self):
        paper = ROOT / 'examiner-reports/home-economics/papers/2022-ol-039-paper.pdf'
        self.assertEqual(hashlib.sha256(paper.read_bytes()).hexdigest(),
                         '6fd83dce9dc39044b6284a9f16814c05c31b0dd9b6ed11c7b311e25ffc42b608')
        _, texts, _ = census_sections('home-economics', 2022, 'ol')
        devices = texts[('C', 1, 'c', 'i')]
        self.assertIn('(a) miniature circuit breakers', devices)
        self.assertIn('(b) earth wire', devices)
        safety = texts[('C', 1, 'c', 'ii')]
        self.assertIn('Outline four guidelines', safety)
        self.assertIn('(20 marks)', safety)
        lighting = texts[('C', 1, 'a', 'ii')]
        self.assertIn('planning a lighting system', lighting)
        self.assertNotIn('safe use of electricity', lighting)
        self.assertNotIn('circuit breakers', texts[('C', 1, 'a', None)])


class HomeEconomicsRecoveredSourcesTest(unittest.TestCase):
    def test_remaining_section_b_reproduces_complete_source_guidance(self):
        from he_review_2023_hl_section_b_rest import build
        fixes = build()
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        self.assertEqual(len(fixes), 10)
        for key, correction in fixes.items():
            self.assertEqual(saved[key], correction)

    def test_nutrition_review_regenerates_from_the_pinned_sources(self):
        from he_review_2023_hl_section_b_q1 import build
        fixes = build()
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        self.assertEqual(len(fixes), 3)
        for key, correction in fixes.items():
            self.assertEqual(saved[key], correction)

    def test_section_a_repairs_regenerate_and_keep_the_full_mark_tariffs(self):
        from he_review_2023_hl_section_a import build
        fixes, added = build()
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        self.assertEqual(len(fixes), 14)
        for key, correction in fixes.items():
            self.assertEqual(saved[key], correction)
        self.assertEqual([c['totalMarks'] for c in added], [2, 4])

    def test_recovered_cards_regenerate_from_the_pinned_sources(self):
        from he_review_2023_hl import build
        authored = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
        recovered = build()
        self.assertEqual(len(recovered), 3)
        for card in recovered:
            self.assertEqual(authored[card['id']], card)
        self.assertEqual([c['totalMarks'] for c in recovered], [18, 26, 6])

    def test_section_c_crops_include_the_final_printed_marks(self):
        source = fitz.open(ROOT / 'examiner-reports/home-economics/papers/2023-hl-039-paper.pdf')
        anchors = json.loads((ROOT / 'scripts/paper-trail/answers/2023/LC098ALP039EV.pdf.json').read_text())
        for question in anchors['q'][5:]:
            page = source[question['pP'] - 1]
            marks = [line['bbox'] for block in page.get_text('dict')['blocks'] if 'lines' in block
                     for line in block['lines'] if 'marks)' in ''.join(span['text'] for span in line['spans'])]
            self.assertTrue(marks)
            self.assertLess(max(rect[3] for rect in marks), question['endY'] * page.rect.height)
            self.assertEqual(question['endP'], question['pP'])


if __name__ == '__main__':
    unittest.main()
