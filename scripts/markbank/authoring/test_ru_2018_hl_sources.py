"""Mandatory pinned-original tests; no corpus-dependent runtime test skips."""
import copy,hashlib,json,re,unittest
import fitz
from pathlib import Path
from reconcile import parse_ref
from ru_review_2018_hl import build,source_records,grammar_forms
from ru_review_census import reviewed_keys
from ru_verify_review import verify,normal

class Original2018HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cards=build()

    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2018-hl-'+suffix))

    def test_raw_scheme_artifact_preserves_every_original_page(self):
        root=Path(__file__).resolve().parents[3]
        actual=(root/'examiner-reports/russian/schemes/2018-hl.md').read_text()
        original=root/'examiner-reports/russian/schemes/2018-hl.pdf'
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),'3a850731dfc2acd40b0df080a8910776105b541dee97dadaa94c353331a5360a')
        with fitz.open(original) as document:pages=[page.get_text() for page in document]
        self.assertEqual(len(pages),20)
        raw,joined=actual.split('\n# Original pages with line wraps joined\n\n')
        self.assertEqual(raw,'\n\n'.join(f'## Page {n+1}\n\n'+text for n,text in enumerate(pages))+'\n')
        self.assertEqual(joined,'\n\n'.join(f'### Joined original page {n+1}\n\n'+re.sub(r'\s+',' ',text).strip() for n,text in enumerate(pages))+'\n')
        self.assertEqual(actual.count('## Page '),20)
        self.assertEqual(actual.count('### Joined original page '),20)
        self.assertIn('between 9 and 14 (9-11; 12-14; 15-16)',' '.join(actual.split()))

    def test_every_original_ask_retains_its_own_identity(self):
        verify(self.cards);keys=set()
        for c in self.cards:
            ref=parse_ref(c['questionRef']);self.assertIsNotNone(ref)
            keys.update((ref['section'],ref['q'],letter,roman) for letter,roman in ref['paths'])
        self.assertEqual(keys,reviewed_keys(2018,'hl'));self.assertEqual(len(keys),39)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards),300)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['section']!='SE'),270)
        self.assertEqual(sum(c['review']['component']=='A00' for c in self.cards),20)

    def test_published_cards_equal_original_derivation(self):
        root=Path(__file__).resolve().parents[3]
        cards=json.loads((root/'scripts/markbank/authored/russian-reviewed.json').read_text())
        self.assertEqual({c['id']:c for c in cards if c['year']==2018 and c['level']=='higher'},
                         {c['id']:c for c in self.cards})

    def verify_essay(self,card):
        docs,source=source_records()
        try:
            r=next(r for r in source['tasks'] if r['unit']=='SE')
            self.assertEqual(card['rubric']['system'],'language-writing');self.assertEqual(card['totalMarks'],30)
            self.assertNotIn('tariffModel',card);self.assertNotIn('rows',card)
            self.assertEqual(card['answerLanguageRule']['otherLanguageMultiplier'],0)
            self.assertEqual(card['review']['schemePages'],[10,11]);self.assertEqual(card['review']['questionPages'],[13])
            blocks=card['rubric']['taskRequirements'];self.assertEqual(len(blocks),2)
            self.assertEqual(normal(' '.join(blocks)),normal(r['publishedSourceBlock']))
            self.assertIn('between 9 and 14 (9-11; 12-14; 15-16)',blocks[0])
            self.assertIn('lower A 15-16',blocks[1])
            self.assertIn('no single Lower A ceiling is imposed',card['rubric']['markingGuideNote'])
            criteria={c['id']:c for c in card['rubric']['criteria']}
            self.assertEqual(criteria['content']['maxMarks'],10)
            self.assertEqual(criteria['expression']['maxMarks'],20)
            self.assertEqual(criteria['content']['permittedMarks'],[0,2,4,6,8,10])
            self.assertEqual(criteria['soft-sign-penalty']['permittedMarks'],[0,1,2])
            self.assertEqual(criteria['title-penalty']['permittedMarks'],[0,1])
            self.assertFalse(any(l['id']=='lower-a' for l in criteria['expression']['limits']))
            self.assertEqual([b['marks'] for b in criteria['expression']['bands']],[[18,19,20],[14,15,16,17],[10,11,12,13],[6,7,8,9],[1,2,3,4,5],[0]])
            self.assertIn(normal(card['questionText']),normal(docs['paper'][12].get_text()))
            for phrase in ['Russian music and/or musicians','Russian literature','Housing in the Russian Federation','Irish‐Russian links','Cities in the Russian Federation']:
                self.assertIn(phrase,card['questionText'])
            for phrase in ['maximum of two content marks','deduct ONE penalty mark','less than 25 words','(– 1 OR – 2)','no marks for language']:
                self.assertIn(phrase,blocks[0])
        finally:
            for d in docs.values():d.close()

    def test_conflicting_whole_choice_preserves_every_instruction(self):
        card=self.get('se');self.verify_essay(card);verify([card])

    def test_missing_choice_range_grid_or_invented_price_fails(self):
        changes=[lambda c:c['rubric']['criteria'][0].update(maxMarks=12),
                 lambda c:c['rubric']['taskRequirements'].pop(),
                 lambda c:c['rubric']['taskRequirements'].__setitem__(0,c['rubric']['taskRequirements'][0].replace('15-16','13-14')),
                 lambda c:c.update(questionText=c['questionText'].replace('Russian literature','')),
                 lambda c:c['rubric']['criteria'][2]['limits'].append({'id':'lower-a','maxMarks':14}),
                 lambda c:c['review'].update(schemePages=[11])]
        for change in changes:
            c=self.get('se');change(c)
            with self.assertRaises(AssertionError):self.verify_essay(c)

    def test_both_writing_tasks_have_the_fixed_no_answer_line_and_fresh_sec_evidence(self):
        root=Path(__file__).resolve().parents[3]
        evidence=json.loads((root/'scripts/markbank/authoring/reviews/russian-2018-hl-sec-20261118/archive-recheck.json').read_text())
        self.assertTrue(evidence['exactMatch']);self.assertEqual(evidence['sha256'],'3a850731dfc2acd40b0df080a8910776105b541dee97dadaa94c353331a5360a')
        self.assertEqual({c['id'] for c in evidence['cardsWithNoPrintedAnswer']},{'ru-2018-hl-se','ru-2018-hl-gw'})
        for suffix in ['se','gw']:
            c=self.get(suffix)
            self.assertIn('The scheme prints no answer for this part.',c['rubric']['markingGuideNote'])
            self.assertEqual(c['review']['noPrintedAnswer']['fixedLine'],'The scheme prints no answer for this part.')

    def test_summary_discretion_exception_is_bound_to_physical_page_six(self):
        for n in range(1,5):
            c=self.get(f'c2-{n}');exception=c['answerLanguageRule']['manualCriterionExceptions']
            self.assertEqual(exception['criterionIds'],['summary-skills']);self.assertEqual(exception['schemePages'],[6])
            self.assertIn('as opposed to content marks',exception['sourceText']);self.assertIn('Russian-language words',exception['sourceText'])
            self.assertTrue(all(g['criteria'][0]['permittedMarks']==[0,2] for g in c['rubric']['groups']))
            verify([c]);exception['schemePages']=[7]
            with self.assertRaises(AssertionError):verify([c])

    def test_summary_page_continuation_and_literal_website_difference_are_preserved(self):
        docs,source=source_records()
        try:
            c=self.get('c2-2');r=next(r for r in source['tasks'] if r['id']==c['id'])
            self.assertEqual(normal(' '.join(c['rubric']['taskRequirements'][1:])),normal(r['publishedSourceBlock']))
            self.assertTrue(c['rubric']['taskRequirements'][1].strip().endswith('he sings for'))
            self.assertTrue(c['rubric']['taskRequirements'][2].startswith('people who understand/ listen'))
            self.assertNotIn('for 5 people',' '.join(c['rubric']['taskRequirements']))
            self.assertIn('www.scherbackov.ru',docs['paper'][7].get_text())
            self.assertIn('www.scherbakov.ru',docs['scheme'][6].get_text())
            self.assertIn('www.scherbackov.ru',self.get('c2-4')['rubric']['markingGuideNote'])
            self.assertIn('www.scherbakov.ru',self.get('c2-4')['rubric']['markingGuideNote'])
            self.assertIn('Do not give 2 bonus marks',self.get('c2-4')['rubric']['criteria'][0]['limits'][1]['guidance'][0])
        finally:
            for d in docs.values():d.close()

    def test_all_source_language_pools_and_two_form_phrase_survive(self):
        docs,source=source_records()
        try:
            la1=self.get('la1');self.assertEqual(len(la1['rubric']['groups']),9);self.assertEqual(la1['rubric']['count'],5)
            self.assertIn('no marks: пойди, пойдти',la1['rubric']['groups'][4]['rows'][0]['text'])
            words=[g['rows'][0]['text'] for g in self.get('la2')['rubric']['groups']]
            self.assertEqual(len(words),29);self.assertEqual(words[7:9],['записать','звезда'])
            self.assertEqual(words.count('петь/спеть (спою)'),1);self.assertNotIn('певец',words)
            forms=grammar_forms(docs['scheme']);self.assertEqual(len(forms),15)
            self.assertEqual(forms[5:7],['школьных','занятий'])
            self.assertEqual(forms,[g['rows'][0]['text'] for g in self.get('gr')['rubric']['groups']])
            self.assertIn('Latin letters are treated as errors',' '.join(self.get('gr')['rubric']['taskRequirements']))
        finally:
            for d in docs.values():d.close()

    def test_writing_ranges_and_year_specific_deduction_come_from_original_tables(self):
        c=self.get('gw');expression=c['rubric']['criteria'][1]
        self.assertEqual(expression['limits'][1]['minMarks'],7);self.assertEqual(expression['limits'][1]['maxMarks'],12)
        self.assertEqual([b['marks'] for b in expression['limits'][1]['bands']],[[11,12],[9,10],[7,8]])
        self.assertEqual(c['rubric']['criteria'][-1]['permittedMarks'],[0,1,2])
        self.assertIn('at least ONE detail',c['rubric']['criteria'][0]['guidance'][0])
        self.assertIn('military or civilian national service',c['questionText']);verify([c])
        expression['limits'][1]['guidance']=['Award twelve marks automatically when Lower A is selected.']
        with self.assertRaises(AssertionError):verify([c])

    def test_listening_half_details_remain_one_two_mark_response_with_no_invented_atoms(self):
        c=self.get('l4-1-ii');guide=' '.join(c['rubric']['taskRequirements'])
        self.assertIn('half the details from one of the segments',guide)
        self.assertIn('husband and she going round Dublin',guide);self.assertIn('no marks for museums',guide)
        self.assertEqual(c['rubric']['count'],2)
        self.assertTrue(all(g['criteria'][0]['permittedMarks']==[0,2] for g in c['rubric']['groups']))
        self.assertNotIn('answerLanguageRule',c);self.assertIn('Accept answers written in Russian',guide)

if __name__=='__main__':unittest.main()
