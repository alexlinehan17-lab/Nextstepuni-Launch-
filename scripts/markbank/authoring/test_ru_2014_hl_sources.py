"""Mandatory original-PDF gate; runtime tests remain portable."""
import copy
import json
import unittest
from pathlib import Path
from reconcile import parse_ref
from ru_review_2014_hl import build,source_records,grammar_forms
from ru_review_census import reviewed_keys
from ru_verify_review import verify,normal


class Original2014HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cards=build()

    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2014-hl-'+suffix))

    def test_originals_and_independent_forty_task_census(self):
        verify(self.cards);keys=set()
        for c in self.cards:
            ref=parse_ref(c['questionRef']);self.assertIsNotNone(ref)
            keys.update((ref['section'],ref['q'],letter,roman) for letter,roman in ref['paths'])
        self.assertEqual(keys,reviewed_keys(2014,'hl'));self.assertEqual(len(keys),40)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards),300)

    def test_published_sitting_equals_original_derivation(self):
        root=Path(__file__).resolve().parents[3]
        authored=json.loads((root/'scripts/markbank/authored/russian-reviewed.json').read_text())
        published=[c for c in authored if c['year']==2014 and c['level']=='higher']
        self.assertEqual({c['id']:c for c in published},{c['id']:c for c in self.cards})

    def test_translation_rule_requires_its_own_page(self):
        c=self.get('la1');c['rubric']['alternativeSets'][0]['schemePages']=[4]
        with self.assertRaises(AssertionError):verify([c])

    def test_invented_translation_partial_is_rejected(self):
        c=self.get('la1');c['rubric']['groups'][1]['criteria'][0]['guidance']=['Award one mark for translating half a phrase.']
        with self.assertRaises(AssertionError):verify([c])

    def test_neighbours_allocation_requires_its_original_page(self):
        c=self.get('c1-3-i');c['rubric']['allocationCap']['schemePages']=[8]
        with self.assertRaises(AssertionError):verify([c])

    def test_cultural_rate_uses_general_q1_page_and_original_irish_allowance(self):
        c=self.get('ca1');verify([c]);self.assertEqual(c['review']['schemePages'],[5]);self.assertEqual(c['review']['guidancePages'],[4])
        docs,source=source_records()
        try:self.assertIn(normal('Freagair i nGaeilge nó i Rúisis'),normal(docs['paper'][4].get_text()))
        finally:
            for d in docs.values():d.close()
        c['review']['guidancePages']=[]
        with self.assertRaises(AssertionError):verify([c])

    def test_concert_partial_remains_in_exact_printed_question_position(self):
        docs,source=source_records()
        try:
            text=normal(docs['scheme'][14].get_text())
            band=text.index(normal('3.i. Give two details about the band.'))
            partial=text.index(normal('Assign one mark for each of: concert + May + 8:00'))
            event=text.index(normal('3.ii. Give two details about the upcoming event in Vologda.'))
            self.assertLess(band,partial);self.assertLess(partial,event)
            self.assertIn('concert + May + 8:00',' '.join(self.get('l1-3-i')['rubric']['taskRequirements']))
            self.assertNotIn('concert + May + 8:00',' '.join(self.get('l1-3-ii')['rubric']['taskRequirements']))
        finally:
            for d in docs.values():d.close()

    def test_all_fifteen_original_grammar_gaps_bind_to_nearest_fixed_words(self):
        docs,source=source_records()
        try:self.assertEqual(len(grammar_forms(docs)),15)
        finally:
            for d in docs.values():d.close()


if __name__=='__main__':unittest.main()
