"""Mandatory regression for original answer previously lost by clipping."""
import hashlib
import unittest
from pathlib import Path
import fitz

class OriginalAnswerFour(unittest.TestCase):
    def test_ir1_v_original_answer_and_footer_are_separate(self):
        path=Path(__file__).resolve().parents[3]/'examiner-reports/russian/schemes/2016-ol.pdf'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),'4242b1be879b2ff9973f75aabf3135478afe1e59b098d2c694ff581d1ce84616')
        with fitz.open(path) as doc:
            page=doc[2]
            question='How many days a week do students attend classes?'
            clipped=page.get_text(clip=fitz.Rect(20,30,580,793),sort=False)
            self.assertEqual(clipped.split(question)[1].strip(),'4')
            bottom=[w for w in page.get_text('words') if w[1]>770]
            answer=next(w for w in bottom if w[4]=='4')
            footer=next(w for w in bottom if w[4]=='1')
            self.assertLess(answer[3],793)
            self.assertGreater(footer[1],793)
            # Older775 boundary does not contain the whole answer glyph.
            # PyMuPDF versions can retain overlapping glyphs, so do not
            # claim that this boundary invariably omits its extracted text.
            self.assertGreater(answer[3],775)

import copy,json,re
from ru_review_2016_ol import build
from ru_review_census import reviewed_keys
from ru_verify_review import verify
from reconcile import parse_ref

class Original2016OrdinarySources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cards=build()
    def test_all_originals_and_independent_census(self):
        verify(self.cards);keys=set()
        for card in self.cards:
            ref=parse_ref(card['questionRef']);self.assertIsNotNone(ref)
            keys.update((ref['section'],ref['q'],letter,roman) for letter,roman in ref['paths'])
        self.assertEqual(keys,reviewed_keys(2016,'ol'));self.assertEqual(len(keys),73)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards),320)
    def test_published_sitting_equals_original_derivation(self):
        root=Path(__file__).resolve().parents[3]
        authored=json.loads((root/'scripts/markbank/authored/russian-reviewed.json').read_text())
        published=[c for c in authored if c['year']==2016 and c['level']=='ordinary']
        self.assertEqual({c['id']:c for c in published},{c['id']:c for c in self.cards})
    def test_invented_handwriting_rule_rejected(self):
        c=copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2016-ol-la1'))
        c['rubric']['criteria'][-1]['limits'][0]['guidance']=['Invented rule: give two joining marks per phrase.']
        with self.assertRaises(AssertionError):verify([c])
    def test_actual_ten_dialogue_gaps_and_already_supplied_question(self):
        path=Path(__file__).resolve().parents[3]/'examiner-reports/russian/papers/2016-ol-000-paper.pdf'
        with fitz.open(path) as doc:
            pages=[doc[p-1].get_text() for p in (9,10)]
            self.assertEqual([len(re.findall(r'[.\u2026]{3,}',t)) for t in pages],[4,6])
            self.assertIn('4. Вопрос:  И тебе нравится с ними работать?',pages[0])
        c=next(c for c in self.cards if c['id']=='ru-2016-ol-sd')
        self.assertEqual(len(c['rows']),10);self.assertTrue(all(r['marks'] is None for r in c['rows']))
        self.assertEqual(c['tariffModel'],{'kind':'questionTotal'})

if __name__=='__main__':unittest.main()
