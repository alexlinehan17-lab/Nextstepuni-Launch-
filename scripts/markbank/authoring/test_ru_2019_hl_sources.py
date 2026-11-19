"""Mandatory pinned-original source, census and joint-question mapping gate; no corpus skips."""
import copy,hashlib,json,re,sys,unittest
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from ru_live_listening_ids import live_id
from reconcile import parse_ref
from ru_verify_review import verify,normal
from ru_review_2019_hl import build,source_records,grammar_forms,raw_scheme_text,METADATA,allocation_approval
from ru_review_census import reviewed_keys
MODULE={'build':build,'source_records':source_records,'grammar_forms':grammar_forms,'raw_scheme_text':raw_scheme_text,'METADATA':METADATA}

class Original2019HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards=MODULE['build']()
        cls.registry=json.loads((ROOT/'scripts/markbank/authoring/russian-joint-tasks.json').read_text())

    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']==live_id('ru-2019-hl-'+suffix)))

    def test_independent_original_census_retains44_asks_as44_cards(self):
        # Literal census from the prior independent48-page visual sweep.
        keys=[('C1',q,None,r) for q,rs in [(1,(None,)),(2,('i','ii')),(3,('i','ii','iii','iv')),(4,(None,))] for r in rs]
        keys += [('C2',q,None,None) for q in (1,2,3,4)]+[(u,None,None,None) for u in ('LA1','CA1')]
        keys += [('LA2',q,None,None) for q in (1,2)]+[(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
        self.assertEqual(len(keys),20)
        keys += [('L1',q,None,r) for q,r in [(1,None),(2,'i'),(2,'ii'),(3,None),(4,None),(5,'i'),(5,'ii')]]
        keys += [('L2',q,None,r) for q,r in [(1,'i'),(2,'i'),(2,'ii'),(3,'i'),(3,'ii'),(4,None)]]
        keys += [('L3',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(3,None)]]
        keys += [('L4',q,None,r) for q in (1,2,3) for r in ('i','ii')]
        self.assertEqual(len(keys),44);self.assertEqual(len(set(keys)),44)
        actual=set()
        for c in self.cards:
            for ref in c['review'].get('coveredQuestionRefs',[c['questionRef']]):
                parsed=parse_ref(ref);self.assertIsNotNone(parsed)
                actual.update((parsed['section'],parsed['q'],letter,roman) for letter,roman in parsed['paths'])
        self.assertEqual(actual,set(keys));self.assertEqual(actual,reviewed_keys(2019,'hl'));self.assertEqual(len(self.cards),44)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards),300)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['kind']=='rubric'),300)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['kind']=='question'),0)

    def test_individual_listening_cards_match_every_original_question_and_approved_allocation(self):
        docs,source=MODULE['source_records']()
        try:
            self.assertEqual([len(docs[k]) for k in ('paper','aural','scheme')],[16,8,24])
            self.assertFalse([t for t in self.registry['tasks'] if t['year']==2019 and t['level']=='higher'])
            approved={live_id(r['id']):r for r in allocation_approval()['listening']['cards'] if r['year']==2019}
            originals=[r for r in source['tasks'] if r['component']=='aural']
            self.assertEqual(len(originals),24)
            for r in originals:
                c=self.get(r['id'].replace('ru-2019-hl-',''));a=approved[c['id']]
                self.assertEqual(c['questionText'],r['question']);self.assertEqual(c['totalMarks'],a['proposedMaximum'])
                self.assertEqual(c['review']['questionPages'],r['questionPages']);self.assertEqual(c['review']['schemePages'],r['schemePages'])
                self.assertNotIn('coveredQuestionRefs',c['review']);self.assertNotIn('answerLanguageRule',c)
                self.assertEqual(c['rubric']['taskRequirements'],[source['listeningGuidance'],r['publishedSourceBlock']])
                self.assertEqual(c['rubric']['count'],a['proposedDetails']);self.assertEqual(c['topicId'],r['topicId'])
                self.assertIn('not printed as a general per-detail award',c['rubric']['markingGuideNote'])
                original=' '.join(docs['aural'][page-1].get_text(clip=fitz.Rect(295,30,580,793)) for page in r['questionPages'])
                self.assertIn(normal(c['questionText']),normal(original))
            self.assertEqual(sum(c['totalMarks'] for c in self.cards if c.get('audioMaterial')),80)
        finally:
            for d in docs.values():d.close()

    def test_every_explicit_partial_and_zero_remains_in_its_own_answer(self):
        station=self.get('l1-5-i')['rubric']['groups'][0]
        self.assertEqual(station['answerCount'],1);self.assertEqual([(r['text'],r['marks']) for r in station['rows']],[('Train station',2),('station',1)])
        skating=self.get('l2-3-ii')['rubric']['groups'][0]
        self.assertEqual([(r['text'],r['marks']) for r in skating['rows']],[('Ice skating',2),('skating',1)])
        place=self.get('l3-1-i')['rubric']['groups'][0]
        self.assertEqual(place['rows'][-1]['text'],'Dublin/Dundrum');self.assertEqual(place['rows'][-1]['marks'],1)
        self.assertEqual(self.get('l3-1-i')['rubric']['groups'][1]['rows'][0]['steps'],[0,1,2])
        for suffix,literal in [('l3-1-ii','Assign no marks: artists'),('l3-2-i','Assign no marks: comedy')]:
            c=self.get(suffix);self.assertIn(literal,' '.join(c['rubric']['taskRequirements']))
            self.assertFalse(any(r['text'] in ('artists','comedy') for g in c['rubric']['groups'] for r in g['rows']))
        self.assertIn('5(ii) twice',self.get('l1-5-i')['rubric']['markingGuideNote'])
        self.assertIn('Irish column prints 2(ii)',self.get('l4-1-ii')['rubric']['markingGuideNote'])

    def test_essay_preserves_approved_one_or_two_deduction_and_every_choice(self):
        c=self.get('se');self.assertEqual(c['totalMarks'],30);self.assertEqual(c['rubric']['system'],'language-writing')
        self.assertEqual(c['rubric']['criteria'][-1]['permittedMarks'],[0,1,2])
        self.assertIn('Deduct 1/2 marks',c['rubric']['criteria'][-1]['guidance'][0])
        self.assertIn('one or two marks',c['rubric']['markingGuideNote'])
        self.assertEqual(c['review']['noPrintedAnswer']['fixedLine'],'The scheme prints no answer for this part.')
        for text in ['Sport in the Russian Federation','Education in the Russian Federation','The family in the Russian Federation','Religion in the Russian Federation','Housing in the Russian Federation']:self.assertIn(text,c['questionText'])
        expression=c['rubric']['criteria'][2]
        self.assertEqual([b['marks'] for b in expression['limits'][1]['bands']],[[13,14],[11,12],[9,10]])
        self.assertTrue(expression['limits'][0]['when']['any'][0]['ignoreDeductions'])
        self.assertEqual(c['answerLanguageRule']['otherLanguageMultiplier'],0)

    def test_comprehension_general_guidance_and_detail_specific_repeat_rule_are_complete(self):
        docs,source=MODULE['source_records']()
        try:
            guide=source['comprehensionGuidance']
            for phrase in ['sections not referred to in the question','accept the one which gives the candidate the most marks','inferred but not stated','award a mark for each concept','Award 2 marks per detail']:
                self.assertIn(phrase,guide)
            self.assertIn(normal(guide),normal(docs['scheme'][3].get_text()))
            c=self.get('c1-2-ii');groups=c['rubric']['groups'];self.assertEqual(len(groups),2)
            flags=[]
            for group in groups:
                criterion=group['criteria'][0];self.assertEqual(criterion['permittedMarks'],[0,2])
                limit=criterion['limits'][0];self.assertEqual(limit['maxMarks'],0)
                flags.append(limit['when']['any'][0]['flag'])
                self.assertIn('it cannot be awarded marks again',limit['guidance'][0])
            self.assertEqual(len(set(flags)),2)
        finally:
            for d in docs.values():d.close()

    def test_grammar_comes_from_both_original_red_colours_without_normalising_characters(self):
        docs,_=MODULE['source_records']()
        try:
            spans=[s for b in docs['scheme'][8].get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'] if s['color']]
            self.assertEqual({s['color'] for s in spans},{12582912,13506590})
            expected=['небольшом','пошла/шла','детствa','современную','музыку','училась','ходила','музыкальной','ей','закончила','прошлого','годa','химиком','школы','своей']
            self.assertEqual(MODULE['grammar_forms'](docs['scheme']),expected)
            self.assertEqual([g['rows'][0]['text'] for g in self.get('gr')['rubric']['groups']],expected)
            self.assertEqual(len(self.get('la2-1')['rubric']['groups']),5)
            self.assertEqual(self.get('la2-1')['rubric']['groups'][0]['rows'][0]['text'],'беспокоилась — беспокоиться')
        finally:
            for d in docs.values():d.close()

    def test_guided_writing_retains_overlapping_lower_a_as_literal_guidance(self):
        c=self.get('gw');expression=c['rubric']['criteria'][1]
        self.assertTrue(expression['bands']);self.assertTrue(expression['limits'][0]['bands'])
        accuracy=expression['limits'][1]
        self.assertEqual((accuracy['minMarks'],accuracy['maxMarks']),(7,12));self.assertNotIn('bands',accuracy)
        self.assertIn('9-11',' '.join(accuracy['guidance']));self.assertIn('11-12',' '.join(accuracy['guidance']))
        self.assertIn('9/10',' '.join(accuracy['guidance']))
        self.assertEqual(c['rubric']['criteria'][-1]['permittedMarks'],[0,2])
        self.assertIn('Deduct 2 marks',c['rubric']['criteria'][-1]['guidance'][0])

    def test_summary_partial_and_language_exception_remain_source_scoped(self):
        for n in range(1,5):
            c=self.get(f'c2-{n}');exception=c['answerLanguageRule']['manualCriterionExceptions']
            self.assertEqual(exception['schemePages'],[6]);self.assertEqual(exception['criterionIds'],['summary-skills'])
            self.assertTrue(all(g['criteria'][0]['permittedMarks']==[0,1,2] for g in c['rubric']['groups']))
            self.assertIn('Single marks may be awarded for partial details',c['rubric']['taskRequirements'][0])
            self.assertEqual(c['rubric']['criteria'][0]['limits'][0]['maxMarks'],1)
            exception['schemePages']=[7]
            with self.assertRaises(AssertionError):verify([c])

    def test_published_cards_equal_the_original_derivation(self):
        actual=json.loads((ROOT/'scripts/markbank/authored/russian-reviewed.json').read_text())
        self.assertEqual({c['id']:c for c in actual if c['year']==2019 and c['level']=='higher'}, {c['id']:c for c in self.cards})
        verify(self.cards)

    def test_raw_and_joined_artifacts_each_equal_every_original_page(self):
        actual=(ROOT/'examiner-reports/russian/schemes/2019-hl.md').read_text()
        p=ROOT/'examiner-reports/russian/schemes/2019-hl.pdf'
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),MODULE['METADATA']['scheme']['sha256'])
        with fitz.open(p) as d:pages=[page.get_text() for page in d]
        self.assertEqual(len(pages),24)
        raw,joined=actual.split('\n# Original pages with line wraps joined\n\n')
        self.assertEqual(raw,'\n\n'.join(f'## Page {i+1}\n\n'+text for i,text in enumerate(pages))+'\n')
        self.assertEqual(joined,'\n\n'.join(f'### Joined original page {i+1}\n\n'+re.sub(r'\s+',' ',text).strip() for i,text in enumerate(pages))+'\n')

if __name__=='__main__':unittest.main()
