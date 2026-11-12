"""Mandatory original source gate, separate from portable runtime tests."""
import copy
import json
import unittest
from pathlib import Path
from reconcile import parse_ref
from ru_review_2012_hl import build,source_records,grammar_forms
from ru_review_census import reviewed_keys
from ru_verify_review import verify,normal

class Original2012HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cards=build()

    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2012-hl-'+suffix))

    def test_all_original_tasks_are_available_with_numeric_conflict_held(self):
        verify(self.cards);keys=set()
        for c in self.cards:
            ref=parse_ref(c['questionRef']);self.assertIsNotNone(ref)
            keys.update((ref['section'],ref['q'],letter,roman) for letter,roman in ref['paths'])
        census=reviewed_keys(2012,'hl');self.assertEqual(len(census),40)
        self.assertEqual(census,keys)
        self.assertEqual(len(keys),40);self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['id']!='ru-2012-hl-c1-2-ii'),296)

    def test_published_cards_equal_original_derivation(self):
        root=Path(__file__).resolve().parents[3]
        authored=json.loads((root/'scripts/markbank/authored/russian-reviewed.json').read_text())
        published=[c for c in authored if c['year']==2012 and c['level']=='higher']
        self.assertEqual({c['id']:c for c in published},{c['id']:c for c in self.cards})

    def test_reading_allocation_conflict_is_preserved_from_original(self):
        docs,source=source_records()
        try:
            r=next(r for r in source['tasks'] if r['id']=='ru-2012-hl-c1-2-ii')
            self.assertIn('two details',r['question'].lower());self.assertIn('2 x 2 = 6',r['publishedSourceBlock'])
            self.assertIn('COMPULSORY:',r['publishedSourceBlock'])
            self.assertTrue(any(c['id']==r['id'] for c in self.cards))
            self.assertIsNone(self.get('c1-2-ii')['rows'][0]['marks'])
        finally:
            for d in docs.values():d.close()

    def test_full_source_boundaries_reconcile_296_plus_held6_without_forcing_300(self):
        docs,source=source_records()
        try:
            self.assertEqual([r['publishedTotal'] for r in source['tasks'] if r['unit']=='C1'],[4,6,4,6,4,4,6,8])
            self.assertEqual(sum(r['publishedTotal'] for r in source['tasks']),302)
            self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['id']!='ru-2012-hl-c1-2-ii'),296)
            self.assertIn(normal('Q.1. Comprehension (50 marks) [40 + 10]'),normal(docs['scheme'][4].get_text()))
            self.assertIn(normal('40 marks'),normal(docs['paper'][2].get_text()))
            for suffix in ('c1-2-i','c2-2','ca1'):
                card=self.get(suffix);r=next(r for r in source['tasks'] if r['id']==card['id'])
                self.assertIn(normal(r['publishedSourceBlock']),normal(' '.join(card['rubric']['taskRequirements'])))
        finally:
            for d in docs.values():d.close()

    def test_derived_ceiling_quotes_actual_prohibition_on_its_original_page(self):
        c=self.get('c1-1-ii');limit=c['rubric']['allocationCap']['limits'][0]
        self.assertIn('cannot obtain full marks',limit['sourceText']);self.assertNotIn('5',limit['sourceText'])
        self.assertEqual(limit['maxMarks'],5);verify([c])
        limit['schemePages']=[6]
        with self.assertRaises(AssertionError):verify([c])

    def test_summary_routes_and_scoped_incomplete_rule_are_bound_to_original_page(self):
        c=self.get('c2-3');rule=c['rubric']['alternativeSets'][0]
        self.assertIn('general rubric was omitted',rule['sourceText']);self.assertEqual(rule['schemePages'],[9]);verify([c])
        rule['schemePages']=[10]
        with self.assertRaises(AssertionError):verify([c])
        c=self.get('c2-3');c['rubric']['groups'][0]['criteria'][-1]['limits'][0]['guidance']=['Award four discretionary marks if the exhibits category is missing.']
        with self.assertRaises(AssertionError):verify([c])

    def test_compensation_requires_literal_rule_on_its_own_page(self):
        c=self.get('l2-4');cap=c['rubric']['allocationCap']
        self.assertEqual(cap['sourceText'],'Assign 2 marks to venue; 2 marks to time; 2 marks to price. If a candidate scores 1 for a category, they can score 3 for another category.')
        self.assertEqual([g['id'] for g in c['rubric']['groups']],['venue','time','price']);verify([c])
        cap['schemePages']=[25]
        with self.assertRaises(AssertionError):verify([c])

    def test_full_grammar_alternatives_and_distinct_repeated_prompts_are_original(self):
        docs,source=source_records()
        try:
            pairs=grammar_forms(docs)
            self.assertEqual(pairs[1],('поздравлять','поздравил/ поздравлял / поздравляет'))
            self.assertEqual([pairs[n] for n in (3,10)],[('университет','университетом'),('университет','университет')])
            self.assertEqual(len(pairs),15)
        finally:
            for d in docs.values():d.close()

    def test_cultural_allowance_does_not_infer_named_pair(self):
        c=self.get('ca1');self.assertNotIn('answerLanguageRule',c)
        self.assertIn('Accept answers in both/either language',' '.join(c['rubric']['taskRequirements']))
        self.assertIn('English column asks for English',c['rubric']['markingGuideNote'])
        self.assertIn('Irish column asks for Irish',c['rubric']['markingGuideNote'])

    def test_final_matching_sentence_retains_full_original_continuation(self):
        c=self.get('sd');self.assertEqual(len(c['rubric']['groups']),10)
        self.assertIn(normal('полное отсутствие чопорности и снобизма'),normal(c['rubric']['groups'][-1]['label']))
        self.assertIn('Do not penalize for using the same number twice',' '.join(c['rubric']['taskRequirements']))

    def verify_conflict_original(self, card):
        docs, source = source_records()
        try:
            record = next(r for r in source['tasks'] if r['id'] == 'ru-2012-hl-c1-2-ii')
            self.assertEqual(card['questionText'], record['question'])
            self.assertIn(normal(card['questionText']), normal(docs['paper'][2].get_text()))
            self.assertIn('Give two details', record['question'])
            self.assertIn('2 x 2 = 6', record['publishedSourceBlock'])
            self.assertIn(normal(record['publishedSourceBlock']), normal(docs['scheme'][5].get_text()))
            self.assertEqual(card['totalMarks'], record['publishedTotal'])
            self.assertEqual(card['totalMarks'], 6)
            self.assertEqual(card['review']['questionPages'], [3])
            self.assertEqual(card['review']['paperPages'], [2,3,4])
            self.assertEqual(card['review']['schemePages'], [6])
            self.assertEqual(card['tariffModel'], {'kind':'questionTotal'})
            self.assertEqual(len(card['rows']), 1)
            self.assertIsNone(card['rows'][0]['marks'])
            self.assertEqual(card['rows'][0]['verbatim'], record['publishedSourceBlock'])
            for text in ['COMPULSORY:', 'assign two marks:', 'assign one mark:', 'no marks: bitter']:
                self.assertIn(text, card['rows'][0]['verbatim'])
            self.assertIn('not an agreed scoring maximum', card['rows'][0]['contextNote'])
            self.assertIn('Do not infer a third requested detail', card['rows'][0]['contextNote'])
            self.assertNotIn('answerLanguageRule', card)
        finally:
            for doc in docs.values(): doc.close()


    def test_conflict_is_complete_confidence_review_with_original_question_and_entire_guidance(self):
        card = self.get('c1-2-ii')
        self.verify_conflict_original(card)
        verify([card])


    def test_omitted_compulsory_partial_zero_or_invented_allocation_fails(self):
        changes = [
            lambda c: c['rows'][0].update(verbatim=c['rows'][0]['verbatim'].replace('COMPULSORY:', '')),
            lambda c: c['rows'][0].update(verbatim=c['rows'][0]['verbatim'].replace('assign one mark:', '')),
            lambda c: c['rows'][0].update(verbatim=c['rows'][0]['verbatim'].replace('no marks: bitter', '')),
            lambda c: c['rows'][0].update(marks=6),
            lambda c: c['review'].update(schemePages=[5]),
            lambda c: c.update(questionText=c['questionText'].replace('two details', 'three details')),
            lambda c: c.update(answerLanguageRule={'otherLanguageMultiplier':0}),
        ]
        for change in changes:
            card = self.get('c1-2-ii'); change(card)
            with self.assertRaises(AssertionError): self.verify_conflict_original(card)

if __name__=='__main__':unittest.main()
