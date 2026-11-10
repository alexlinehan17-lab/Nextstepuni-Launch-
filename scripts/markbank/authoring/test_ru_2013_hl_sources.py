"""Mandatory original source gate; no conditional PDF imports in Vitest."""
import copy
import json
import re
import unittest
from pathlib import Path
import fitz
from reconcile import parse_ref
from ru_review_2013_hl import build,source_records,scheme_page,FOOTER_BLOCK_BOUNDS
from ru_review_census import reviewed_keys
from ru_verify_review import verify,normal


class Original2013HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cards=build()

    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2013-hl-'+suffix))

    def test_all_40_original_asks_are_covered_with_cultural_numeric_conflict_retained(self):
        verify(self.cards);keys=set()
        for c in self.cards:
            ref=parse_ref(c['questionRef']);self.assertIsNotNone(ref)
            keys.update((ref['section'],ref['q'],letter,roman) for letter,roman in ref['paths'])
        census=reviewed_keys(2013,'hl');self.assertEqual(len(census),40)
        self.assertEqual(census,keys)
        self.assertEqual(len(keys),40)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['section']!='CA1'),292)

    def test_published_supported_cards_equal_original_derivation(self):
        root=Path(__file__).resolve().parents[3]
        authored=json.loads((root/'scripts/markbank/authored/russian-reviewed.json').read_text())
        published=[c for c in authored if c['year']==2013 and c['level']=='higher']
        self.assertEqual({c['id']:c for c in published},{c['id']:c for c in self.cards})

    def test_last_no_full_credit_line_survives_and_exact_footer_does_not(self):
        docs,source=source_records()
        try:
            page=docs['scheme'][5];raw=page.get_text();clean=scheme_page(docs['scheme'],6)
            phrase='of famous people + she took photos of artists'
            self.assertIn(phrase,raw);self.assertIn(phrase,clean)
            self.assertNotIn(phrase,page.get_text(clip=fitz.Rect(20,30,580,775),sort=False))
            self.assertRegex(raw,r'^4\s');self.assertNotRegex(clean,r'(?m)^4\s*$')
            footers=[b for b in page.get_text('blocks',sort=False) if b[4].strip()=='4']
            self.assertEqual(len(footers),1);self.assertEqual(tuple(round(x,4) for x in footers[0][:4]),FOOTER_BLOCK_BOUNDS[6])
            required='Do not award full marks for the following details: she collected photographs of artists / of famous people + she took photos of artists'
            self.assertIn(normal(required),normal(' '.join(self.get('c2-2')['rubric']['taskRequirements'])))
        finally:
            for d in docs.values():d.close()

    def verify_cultural_original(self,card):
        docs,source=source_records()
        try:
            c=next(c for c in source['tasks'] if c['unit']=='CA1')
            self.assertEqual((c['paperTotal'],c['publishedTotal']),(8,4))
            self.assertIn(normal('Assign 1 mark for each relevant detail 2 х 2 = 4'),normal(c['publishedSourceBlock']))
            self.assertIn(normal('Freagair i nGaeilge nó i Rúisis'),normal(docs['paper'][4].get_text()))
            self.assertEqual(card['questionText'],c['question'])
            self.assertIn(normal(card['questionText']),normal(docs['paper'][4].get_text(clip=fitz.Rect(295,30,580,793))))
            self.assertEqual(card['review']['questionPages'],[5])
            self.assertEqual(card['review']['schemePages'],[5])
            self.assertEqual(card['totalMarks'],8)
            self.assertEqual(card['tariffModel'],{'kind':'questionTotal'})
            self.assertEqual(len(card['rows']),1)
            self.assertEqual(card['rows'][0]['verbatim'],c['publishedSourceBlock'])
            self.assertIsNone(card['rows'][0]['marks'])
            self.assertNotIn('answerLanguageRule',card)
            self.assertIn('not an agreed scoring maximum',card['rows'][0]['contextNote'])
        finally:
            for d in docs.values():d.close()

    def test_cultural_original_options_and_conflicting_totals_survive_as_unpriced_review(self):
        self.verify_cultural_original(self.get('ca1'))

    def test_cultural_omitted_option_invented_allocation_and_wrong_page_are_rejected(self):
        for mutation in [lambda c:c.update(questionText=c['questionText'].replace('Санкт-Петербург','')),
                         lambda c:c['rows'][0].update(marks=4),
                         lambda c:c['rows'][0].update(verbatim='Assign two marks for each relevant detail.'),
                         lambda c:c['review'].update(schemePages=[4]),
                         lambda c:c.update(answerLanguageRule={'otherLanguageMultiplier':0})]:
            card=self.get('ca1');mutation(card)
            with self.assertRaises(AssertionError):self.verify_cultural_original(card)

    def test_two_places_wording_and_explicit_two_mark_scale_are_both_original(self):
        docs,source=source_records()
        try:
            c=next(c for c in source['tasks'] if c['id']=='ru-2013-hl-c1-3-ii')
            self.assertIn('details about two places',c['question']);self.assertNotIn('two details',c['question'])
            self.assertIn('2 x 3 = 6',c['publishedSourceBlock']);self.assertIn('assign two marks:',c['publishedSourceBlock'])
        finally:
            for d in docs.values():d.close()

    def test_collection_quota_requires_its_own_source_page(self):
        c=self.get('c2-1');c['rubric']['allocationCap']['schemePages']=[7]
        with self.assertRaises(AssertionError):verify([c])

    def test_invented_parent_allocation_fails_source_gate(self):
        c=self.get('c2-2');c['rubric']['groups'][0]['criteria'][0]['guidance']=['Assign four marks only to details about the mother.']
        with self.assertRaises(AssertionError):verify([c])


if __name__=='__main__':unittest.main()
