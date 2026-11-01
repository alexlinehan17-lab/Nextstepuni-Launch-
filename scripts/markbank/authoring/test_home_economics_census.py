"""Source-backed Home Economics census corrections; no card-count shortcut."""
import hashlib
import json
from pathlib import Path
import unittest

import fitz

from paper_census import census_sections

ROOT = Path(__file__).resolve().parents[3]


class HomeEconomicsNestedDevicesTest(unittest.TestCase):
    def test_2022_deferred_a_regenerates_and_preserves_the_longer_last_answer_row(self):
        from he_review_2022_hl_deferred import build, documents
        cards, _, _ = build(); self.assertEqual(len(cards), 19)
        authored = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
        for c in cards: self.assertEqual(authored[c['id']], c)
        docs = documents()
        questions = json.loads((ROOT / 'scripts/paper-trail/answers/2022/LC098ALP014EV-deferred.pdf.json').read_text())['q']
        self.assertEqual(len(questions), 14)
        q3 = next(q for q in questions if q['n'] == '3')
        page = docs['a'][q3['pP'] - 1]
        self.assertGreater(q3['endY'] * page.rect.height, 741.5)
        text = page.get_text(clip=fitz.Rect(0, q3['pY'][0] * page.rect.height, page.rect.width, q3['endY'] * page.rect.height))
        self.assertIn('(ii)', text)
        self.assertNotIn('Leaving Certificate Examination', text)
        for q in questions:
            r, = q['region']; page = docs['scheme'][r['p'] - 1]
            bounds = r['r']; text = page.get_text(clip=fitz.Rect(bounds[0]*page.rect.width,bounds[1]*page.rect.height,bounds[2]*page.rect.width,bounds[3]*page.rect.height))
            self.assertIn(q['n']+'.', text)

    def test_deferred_c_regenerates_with_final_prompts_and_complete_scheme_continuations(self):
        from he_review_2023_hl_deferred_c1 import build as build_c1
        from he_review_2023_hl_deferred_c_rest import build as build_rest, FIGURE, CROP_SHA256
        from he_review_2023_hl_deferred import documents
        cards = build_c1() + build_rest()
        self.assertEqual(len(cards), 26)
        authored = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
        for c in cards: self.assertEqual(authored[c['id']], c)
        self.assertEqual(hashlib.sha256((ROOT / f'public/exam-figures/home-economics/{FIGURE}.png').read_bytes()).hexdigest(), CROP_SHA256)
        q = json.loads((ROOT / 'scripts/paper-trail/answers/2023/LC098ALP039EV-deferred.pdf.json').read_text())['q'][5:]
        self.assertEqual([[r['p'] for r in x['region']] for x in q], [[18, 19, 20, 21], [22, 23, 24], [25, 26, 27], [28, 29, 30]])
        docs = documents()
        for question, last_marks, last_prompt in zip(q, [18, 6, 10, 15], ['reduce the energy', 'influencers', 'dual-earner', 'marriage relationship']):
            page = docs['bc'][question['pP'] - 1]
            text = page.get_text(clip=fitz.Rect(0, question['pY'][0] * page.rect.height, page.rect.width, question['endY'] * page.rect.height))
            self.assertIn(f'({last_marks} marks)', text)
            self.assertIn(last_prompt, text)
            self.assertNotIn('Leaving Certificate Examination', text)
            for r in question['region']:
                page = docs['scheme'][r['p'] - 1]
                self.assertGreaterEqual(r['r'][3] * page.rect.height, max(w[3] for w in page.get_text('words') if w[3] < 775))

    def test_deferred_b2_to_b5_regenerate_and_keep_every_final_prompt_and_source_page(self):
        from he_review_2023_hl_deferred_b_rest import build
        from he_review_2023_hl_deferred import documents
        cards = build(); self.assertEqual(len(cards), 12)
        authored = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
        for c in cards: self.assertEqual(authored[c['id']], c)
        q = json.loads((ROOT / 'scripts/paper-trail/answers/2023/LC098ALP039EV-deferred.pdf.json').read_text())['q'][:5]
        self.assertEqual([[r['p'] for r in x['region']] for x in q], [[8, 9], [10, 11], [12, 13, 14], [15, 16], [17]])
        docs = documents()
        for question, last_marks in zip(q, [20, 12, 8, 10, 10]):
            page = docs['bc'][question['pP'] - 1]
            text = page.get_text(clip=fitz.Rect(0, question['pY'][0] * page.rect.height, page.rect.width, question['endY'] * page.rect.height))
            self.assertIn(f'({last_marks} marks)', text)
        for question in q:
            for r in question['region']:
                page = docs['scheme'][r['p'] - 1]
                end = r['r'][3] * page.rect.height
                self.assertGreaterEqual(end, max(w[3] for w in page.get_text('words') if w[3] < 775))

    def test_deferred_b1_regenerates_with_the_last_environmental_prompt_in_its_anchor(self):
        from he_review_2023_hl_deferred_b1 import build
        from he_review_2023_hl_deferred import documents
        cards = build(); self.assertEqual(len(cards), 5)
        authored = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
        for c in cards: self.assertEqual(authored[c['id']], c)
        self.assertEqual([c['totalMarks'] for c in cards], [18, 12, 18, 12, 20])
        q = json.loads((ROOT / 'scripts/paper-trail/answers/2023/LC098ALP039EV-deferred.pdf.json').read_text())['q'][0]
        page = documents()['bc'][1]
        text = page.get_text(clip=fitz.Rect(0, q['pY'][0] * page.rect.height, page.rect.width, q['endY'] * page.rect.height))
        self.assertIn('(20 marks)', text)
        self.assertIn('purchasing foods', text)

    def test_deferred_census_reads_both_booklets_and_uncarded_year_independently(self):
        from paper_census import census_home_economics_deferred
        papers = census_home_economics_deferred()
        self.assertEqual([p['year'] for p in papers], [2022, 2023])
        for p in papers:
            self.assertEqual(p['paper'], 'Deferred')
            self.assertEqual({leaf['key'][0] for leaf in p['leaves']}, {'A', 'B', 'C'})
        deferred = next(p for p in papers if p['year'] == 2023)
        self.assertTrue(any('gel formation' in leaf['text'] for leaf in deferred['leaves']))
        self.assertTrue(any('water pollution' in leaf['text'] for leaf in deferred['leaves']))
        self.assertFalse(any('Basal Metabolic Rate' in leaf['text'] for leaf in deferred['leaves']))

    def test_deferred_section_a_regenerates_and_anchors_include_floating_answers(self):
        from he_review_2023_hl_deferred import build_a, documents, region_text
        docs = documents(); cards, paper, scheme = build_a(docs)
        self.assertEqual(len(cards), 15)
        authored = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
        for c in cards: self.assertEqual(authored[c['id']], c)
        self.assertIn('genetically modified foods', region_text(docs['scheme'], scheme[8]))
        self.assertIn('access to funds', region_text(docs['scheme'], scheme[10]))
        self.assertIn('Croí Cónaithe', region_text(docs['scheme'], scheme[12]))
        self.assertIn('Reduction measure', region_text(docs['a'], paper[14]))

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
    def test_ordinary_section_c_regenerates_every_reviewed_response(self):
        from he_review_2023_ol_section_c import build
        fixes = build()
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        self.assertEqual(len(fixes), 27)
        for key, correction in fixes.items(): self.assertEqual(saved[key], correction)

    def test_ordinary_section_b_regenerates_and_preserves_the_split_context(self):
        from he_review_2023_ol_section_b import build
        fixes, added = build()
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        authored = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
        self.assertEqual(len(fixes), 13)
        self.assertEqual(len(added), 1)
        for key, correction in fixes.items(): self.assertEqual(saved[key], correction)
        self.assertEqual(authored[added[0]['id']], added[0])
        self.assertEqual(added[0]['totalMarks'], 10)
        self.assertIn('teenagers and adults', added[0]['stem'])

    def test_ordinary_section_a_regenerates_with_independent_iron_source(self):
        from he_review_2023_ol_section_a import build
        fixes, added = build()
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        authored = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
        self.assertEqual(len(fixes), 11)
        self.assertEqual(len(added), 1)
        for key, correction in fixes.items(): self.assertEqual(saved[key], correction)
        self.assertEqual(authored[added[0]['id']], added[0])
        self.assertEqual(added[0]['totalMarks'], 2)

    def test_ordinary_recovery_regenerates_from_full_source_guidance(self):
        from he_review_2023_ol import build
        added, fixes = build()
        authored = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/home-economics.json').read_text())}
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        self.assertEqual(len(added), 4)
        self.assertEqual(len(fixes), 1)
        for c in added:
            self.assertEqual(authored[c['id']], c)
        for key, correction in fixes.items():
            self.assertEqual(saved[key], correction)

    def test_social_studies_and_core_source_reviews_regenerate(self):
        from he_review_2023_hl_elective3 import build as social
        from he_review_2023_hl_core import build as core
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        for build in [social, core]:
            fixes = build()
            self.assertEqual(len(fixes), 7)
            for key, correction in fixes.items():
                self.assertEqual(saved[key], correction)

    def test_elective_two_source_review_regenerates(self):
        from he_review_2023_hl_elective2 import build
        fixes = build()
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        self.assertEqual(len(fixes), 5)
        for key, correction in fixes.items():
            self.assertEqual(saved[key], correction)

    def test_elective_one_source_review_regenerates(self):
        from he_review_2023_hl_elective1 import build
        fixes = build()
        saved = json.loads((ROOT / 'scripts/markbank/card-corrections.json').read_text())['home-economics']
        self.assertEqual(len(fixes), 7)
        for key, correction in fixes.items():
            self.assertEqual(saved[key], correction)

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
        for level, code in [('hl', 'A'), ('ol', 'G')]:
            source = fitz.open(ROOT / f'examiner-reports/home-economics/papers/2023-{level}-039-paper.pdf')
            anchors = json.loads((ROOT / f'scripts/paper-trail/answers/2023/LC098{code}LP039EV.pdf.json').read_text())
            for question in anchors['q'][5:]:
                page = source[question['pP'] - 1]
                marks = [line['bbox'] for block in page.get_text('dict')['blocks'] if 'lines' in block
                         for line in block['lines'] if 'marks)' in ''.join(span['text'] for span in line['spans'])]
                self.assertTrue(marks)
                self.assertLess(max(rect[3] for rect in marks), question['endY'] * page.rect.height)
                self.assertEqual(question['endP'], question['pP'])


if __name__ == '__main__':
    unittest.main()
