"""Mandatory pinned-original Russian 2020 Higher evidence; no source skips."""
import copy,hashlib,json,re,sys,unittest
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from reconcile import parse_ref
from ru_verify_review import normal,verify
from ru_joint_tasks import validate_joint_task
from ru_review_2020_hl import build,source_records,grammar_forms,raw_scheme_text,summary_tariff,METADATA
from ru_review_census import reviewed_keys
MODULE={name:globals()[name] for name in ('build','source_records','grammar_forms','raw_scheme_text','summary_tariff','METADATA')}



class Original2020HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards=MODULE['build']()
        cls.registry=json.loads((ROOT/'scripts/markbank/authoring/russian-joint-tasks.json').read_text())

    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2020-hl-'+suffix))

    def test_independent42_ask_census_under24_practice_tasks(self):
        keys=[('C1',q,None,r) for q,rs in [(1,('i','ii')),(2,('i','ii','iii')),(3,('i','ii')),(4,('i','ii'))] for r in rs]
        keys += [('LA1',q,None,None) for q in (1,2)]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]
        keys += [('LA2',None,None,None)]
        keys += [(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        assert len(keys)==20
        keys += [('L1',q,None,r) for q,r in [(1,None),(2,None),(3,None),(4,None),(5,'i'),(5,'ii')]]
        keys += [('L2',q,None,r) for q,r in [(1,'i'),(2,'i'),(2,'ii'),(3,None),(4,None),(5,None)]]
        keys += [('L3',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,'i'),(3,'ii')]]
        keys += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii')]]
        assert len(keys)==len(set(keys))==42
        expected=set(keys)
        self.assertEqual(expected,reviewed_keys(2020,'hl'))
        self.assertEqual(len(expected),42)
        actual=set()
        for card in self.cards:
            for ref in card['review'].get('coveredQuestionRefs',[card['questionRef']]):
                parsed=parse_ref(ref);self.assertIsNotNone(parsed)
                actual.update((parsed['section'],parsed['q'],letter,roman) for letter,roman in parsed['paths'])
        self.assertEqual(actual,expected);self.assertEqual(len(self.cards),24)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards),300)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['kind']=='rubric'),190)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['kind']=='question'),110)

    def test_joint_original_identities_pages_and_hashes_with_negative_claims(self):
        docs,source=MODULE['source_records']()
        try:
            self.assertEqual([len(docs[k]) for k in ('paper','aural','scheme')],[16,8,27])
            total=0
            for spec in [t for t in self.registry['tasks'] if t['year']==2020]:
                card=self.get(spec['id'].replace('ru-2020-hl-',''))
                record={k:card[k] for k in ('id','year','level','questionRef')}|{'paperFileid':spec['paperFileid'],'schemeFileid':spec['schemeFileid'],**card['review']}
                validate_joint_task(record,card,self.registry)
                self.assertEqual(spec['paperSha256'],MODULE['METADATA']['aural']['sha256'])
                self.assertEqual(spec['schemeSha256'],MODULE['METADATA']['scheme']['sha256'])
                self.assertEqual(spec['independentSittingAsks'],42)
                originals=[r for r in source['tasks'] if r['unit']==spec['section']]
                self.assertEqual(len(originals),len(spec['questions']));total+=len(originals)
                for question,original in zip(spec['questions'],originals):
                    self.assertEqual(question['questionText'],original['question'])
                    self.assertEqual(question['leafKey'],[original['unit'],original['item'],None,original['roman']])
                    self.assertEqual(question['questionPages'],original['questionPages'])
                    self.assertEqual(question['schemePages'],original['schemePages'])
                    raw=' '.join(docs['aural'][p-1].get_text(clip=fitz.Rect(295,30,580,793)) for p in question['questionPages'])
                    self.assertIn(normal(question['questionText']),normal(raw))
                for mutation in [lambda r:r['atlasQuestions'][0].update(questionText='Invented source question'),lambda r:r['atlasQuestions'][0].update(questionPages=[99]),lambda r:r['atlasQuestions'][0].update(topicId='russian-unknown')]:
                    wrong=copy.deepcopy(record);mutation(wrong)
                    with self.assertRaises(AssertionError):validate_joint_task(wrong,card,self.registry)
            self.assertEqual(total,22)
        finally:
            for doc in docs.values():doc.close()

    def test_listening_complete_pools_known_luggage_prices_and_pet_partials(self):
        docs,source=MODULE['source_records']()
        try:
            for section in range(1,5):
                card=self.get(f'l{section}');records=[r for r in source['tasks'] if r['unit']==f'L{section}']
                self.assertEqual(card['totalMarks'],20);self.assertEqual(card['tariffModel'],{'kind':'questionTotal'})
                self.assertTrue(all(row['marks'] is None for row in card['rows']))
                self.assertNotIn('answerLanguageRule',card)
                self.assertEqual(card['rows'][0]['verbatim'],source['listeningGuidance'])
                self.assertIn('Accept answers written in Russian',card['rows'][0]['verbatim'])
                self.assertIn('no penalty for excess material which does not invalidate the answer',card['rows'][0]['verbatim'])
                self.assertEqual([row['verbatim'] for row in card['rows'][1:]],[r['publishedSourceBlock'] for r in records])
            luggage=next(row for row in self.get('l1')['rows'] if row['id']=='l1-2')
            self.assertEqual(luggage['verbatim'],'• One suitcase (1 mark) and a bag/purse (1 mark)')
            self.assertIsNone(luggage['marks'])
            self.assertFalse(any(c['id']=='ru-2020-hl-l1-2' for c in self.cards))
            pets=next(row for row in self.get('l4')['rows'] if row['id']=='l4-3-ii')
            self.assertIn('Dog: 1 mark',pets['verbatim']);self.assertIn('Cat: 1 mark',pets['verbatim'])
        finally:
            for doc in docs.values():doc.close()

    def test_original_numbering_and_duration_discrepancies_remain_visible(self):
        docs,_=MODULE['source_records']()
        try:
            front=normal(docs['aural'][0].get_text());back=normal(docs['aural'][7].get_text())
            self.assertIn(normal('50 minutes'),front);self.assertIn(normal('40 minutes'),back)
            notes=' '.join(row.get('contextNote','') for row in self.get('l2')['rows'])
            self.assertIn('50 minutes',notes);self.assertIn('40 minutes',notes)
            self.assertIn('English booklet1(i), Irish and scheme1',notes)
            self.assertIn('Paper3, scheme3(i)',notes)
        finally:
            for doc in docs.values():doc.close()

    def test_essay_retains_all_five_choices_and_ambiguous_literal_deduction(self):
        card=self.get('se');docs,source=MODULE['source_records']()
        try:
            record=next(r for r in source['tasks'] if r['unit']=='SE')
            self.assertEqual(card['tariffModel'],{'kind':'questionTotal'});self.assertEqual(card['totalMarks'],30)
            self.assertTrue(all(row['marks'] is None for row in card['rows']))
            self.assertEqual(normal(' '.join(row['verbatim'] for row in card['rows'])),normal(record['publishedSourceBlock']))
            self.assertEqual([row['verbatim'] for row in card['rows']],record['sourcePageBlocks'])
            for physical,row in zip((12,13,14),card['rows']):
                self.assertIn(normal(row['verbatim']),normal(docs['scheme'][physical-1].get_text()))
            for text in ['education system in the Russian Federation','family in the Russian Federation','Places of historic and cultural interest','Music / musicians in the Russian Federation','Russian language in Ireland']:
                self.assertIn(normal(text),normal(card['questionText']))
            self.assertIn('Deduct 1/2 marks',' '.join(row['verbatim'] for row in card['rows']))
            self.assertIn('Neither interpretation is selected',card['rows'][0]['contextNote'])
        finally:
            for doc in docs.values():doc.close()

    def test_comprehension_pools_and_general_duplicate_guidance_are_literal(self):
        docs,source=MODULE['source_records']()
        try:
            guide=source['comprehensionGuidance']
            for text in ['sections not referred to','accept the one which gives the candidate the most marks','inferred but not stated','Award 2 marks per detail']:
                self.assertIn(text,guide)
            self.assertIn(normal(guide),normal(docs['scheme'][3].get_text()))
            for record in [r for r in source['tasks'] if r['unit']=='C1']:
                card=self.get(record['id'].replace('ru-2020-hl-',''))
                self.assertEqual([g['rows'][0]['text'] for g in card['rubric']['groups']],[part.strip() for part in record['publishedSourceBlock'].split('•')[1:]])
                self.assertTrue(all(g['rows'][0]['marks']==2 and 'steps' not in g['rows'][0] for g in card['rubric']['groups']))
        finally:
            for doc in docs.values():doc.close()

    def test_fifteen_grammar_forms_are_the_bold_underlined_original_words(self):
        docs,_=MODULE['source_records']()
        try:
            expected=['Мою','бабушку','многодетной','семье','лыжах','среднюю','Моего','дедушку','восьми','главным','помощником','дому','зимой /зимою','природе','края']
            self.assertEqual(MODULE['grammar_forms'](docs['scheme']),expected)
            self.assertEqual([g['rows'][0]['text'] for g in self.get('gr')['rubric']['groups']],expected)
            self.assertIn(normal('15 x 2 marks'),normal(docs['scheme'][10].get_text()))
            self.assertIn('eleven bracketed prompts',self.get('gr')['rubric']['markingGuideNote'])
            self.assertEqual(sum(g['rows'][0]['marks'] for g in self.get('gr')['rubric']['groups']),30)
        finally:
            for doc in docs.values():doc.close()

    def test_language_forms_and_case_permission_are_source_specific(self):
        infinitives=self.get('la1-1');travel=self.get('la1-2');cases=self.get('la2')
        self.assertEqual(len(infinitives['rubric']['groups']),5)
        self.assertIn('Do not change the aspect',infinitives['rubric']['taskRequirements'][0])
        self.assertEqual(len(travel['rubric']['groups']),18);self.assertEqual(travel['rubric']['count'],5)
        self.assertIn('Accept words in any form (case, number)',travel['rubric']['taskRequirements'][0])
        self.assertIn('Q.1.3',travel['rubric']['markingGuideNote']);self.assertIn('Q.2.2',travel['rubric']['markingGuideNote'])
        self.assertEqual(len(cases['rubric']['groups']),10);self.assertNotIn('answerLanguageRule',cases)
        self.assertIn('Irish, English or Russian',cases['rubric']['taskRequirements'][0])
        self.assertIn('translate the phrases into English',cases['rubric']['taskRequirements'][0])
        self.assertEqual(sum('предожный' in g['rows'][0]['text'] for g in cases['rubric']['groups']),2)

    def test_guided_writing_preserves_overlap_and_explicit_two_only_deduction(self):
        card=self.get('gw');expression=card['rubric']['criteria'][1]
        self.assertTrue(expression['bands']);self.assertTrue(expression['limits'][0]['bands'])
        accuracy=expression['limits'][1]
        self.assertEqual((accuracy['minMarks'],accuracy['maxMarks']),(7,12));self.assertNotIn('bands',accuracy)
        self.assertIn('9-11',' '.join(accuracy['guidance']));self.assertIn('11-12',' '.join(accuracy['guidance']))
        self.assertIn('9/10',' '.join(accuracy['guidance']))
        self.assertEqual(card['rubric']['criteria'][-1]['permittedMarks'],[0,2])
        for text in ['1. LETTER','2. NARRATIVE','3. DISCUSSION']:
            self.assertIn(text,card['questionText'])

    def test_each_summary_tariff_binds_to_its_own_original_numbered_region(self):
        path=ROOT/'examiner-reports/russian/schemes/2020-hl.pdf'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),MODULE['METADATA']['scheme']['sha256'])
        with fitz.open(path) as doc:
            evidence=[MODULE['summary_tariff'](doc,n) for n in range(1,5)]
            self.assertEqual([e['schemePage'] for e in evidence],[7,8,8,8])
            self.assertEqual([e['text'] for e in evidence],['10 marks']*4)
            for e in evidence:
                words=doc[e['schemePage']-1].get_text('words')
                tariff_words=[w[4] for box in e['tariffBoxes'] for w in words if list(w[:4])==box]
                self.assertEqual(tariff_words,['10','marks'])
                heading=[w[4] for w in words if list(w[:4])==e['headingBox']]
                self.assertEqual(heading,[f"{e['questionNumber']}."])
            # The fourth tariff is beside the first answer line, after Main points,
            # while the stream emits it before heading4. This must not price Q3.
            self.assertGreater(evidence[3]['tariffBoxes'][0][1],evidence[3]['headingBox'][3])
            self.assertLess(evidence[2]['tariffBoxes'][0][1],evidence[3]['headingBox'][1])
        with self.assertRaises(AssertionError):MODULE['summary_tariff'](doc,5)

    def test_summary_partial_language_exception_and_incomplete_cap_bind_own_page(self):
        for number in range(1,5):
            card=self.get(f'c2-{number}');exception=card['answerLanguageRule']['manualCriterionExceptions']
            self.assertEqual(exception['schemePages'],[7]);self.assertEqual(exception['criterionIds'],['summary-skills'])
            self.assertTrue(all(g['criteria'][0]['permittedMarks']==[0,1,2] for g in card['rubric']['groups']))
            self.assertIn('Single marks may be awarded for partial details',card['rubric']['taskRequirements'][0])
            self.assertEqual(card['rubric']['criteria'][0]['limits'][0]['maxMarks'],1)
            self.assertTrue(any('10 marks' in text for text in card['rubric']['taskRequirements'][1:]))
            exception['schemePages']=[8]
            with self.assertRaises(AssertionError):verify([card])

    def test_draft_exactly_equals_original_derivation_and_all_claims_verify(self):
        self.assertEqual([c for c in json.loads((ROOT/'scripts/markbank/authored/russian-reviewed.json').read_text()) if c['year']==2020 and c['level']=='higher'],self.cards)
        verify(self.cards)

    def test_raw_and_line_joined_artifacts_independently_equal_all27_original_pages(self):
        actual=(ROOT/'examiner-reports/russian/schemes/2020-hl.md').read_text();path=ROOT/'examiner-reports/russian/schemes/2020-hl.pdf'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),MODULE['METADATA']['scheme']['sha256'])
        with fitz.open(path) as doc:pages=[page.get_text() for page in doc]
        self.assertEqual(len(pages),27)
        raw,joined=actual.split('\n# Original pages with line wraps joined\n\n')
        self.assertEqual(raw,'\n\n'.join(f'## Page {i+1}\n\n'+text for i,text in enumerate(pages))+'\n')
        self.assertEqual(joined,'\n\n'.join(f'### Joined original page {i+1}\n\n'+re.sub(r'\s+',' ',text).strip() for i,text in enumerate(pages))+'\n')


if __name__=='__main__':unittest.main()
