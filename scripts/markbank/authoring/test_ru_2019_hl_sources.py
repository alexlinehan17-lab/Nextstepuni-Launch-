"""Mandatory pinned-original source, census and joint-question mapping gate; no corpus skips."""
import copy,hashlib,json,re,sys,unittest
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from reconcile import parse_ref
from ru_verify_review import verify,normal
from ru_joint_tasks import validate_joint_task
from ru_review_2019_hl import build,source_records,grammar_forms,raw_scheme_text,METADATA
from ru_review_census import reviewed_keys
MODULE={'build':build,'source_records':source_records,'grammar_forms':grammar_forms,'raw_scheme_text':raw_scheme_text,'METADATA':METADATA}

class Original2019HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards=MODULE['build']()
        cls.registry=json.loads((ROOT/'scripts/markbank/authoring/russian-joint-tasks.json').read_text())

    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2019-hl-'+suffix))

    def test_independent_original_census_retains44_asks_under24_tasks(self):
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
        self.assertEqual(actual,set(keys));self.assertEqual(actual,reviewed_keys(2019,'hl'));self.assertEqual(len(self.cards),24)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards),300)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['kind']=='rubric'),190)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['kind']=='question'),110)

    def test_joint_manifest_matches_all_original_questions_pages_and_hashes(self):
        docs,source=MODULE['source_records']()
        try:
            self.assertEqual([len(docs[k]) for k in ('paper','aural','scheme')],[16,8,24])
            for spec in [t for t in self.registry['tasks'] if t['year']==2019 and t['level']=='higher']:
                c=self.get(spec['id'].replace('ru-2019-hl-',''))
                generated={k:c[k] for k in ('id','year','level','questionRef')}|{'paperFileid':spec['paperFileid'],'schemeFileid':spec['schemeFileid'],**c['review']}
                validate_joint_task(generated,c,self.registry)
                self.assertEqual(spec['paperSha256'],MODULE['METADATA']['aural']['sha256'])
                self.assertEqual(spec['schemeSha256'],MODULE['METADATA']['scheme']['sha256'])
                self.assertEqual(spec['independentSittingAsks'],44)
                originals=[r for r in source['tasks'] if r['unit']==spec['section']]
                self.assertEqual(len(spec['questions']),len(originals))
                for q,r in zip(spec['questions'],originals):
                    self.assertEqual(q['questionText'],r['question']);self.assertEqual(q['questionPages'],r['questionPages'])
                    self.assertEqual(q['schemePages'],r['schemePages'])
                    self.assertEqual(q['leafKey'],[r['unit'],r['item'],None,r['roman']])
                    original=' '.join(docs['aural'][page-1].get_text(clip=fitz.Rect(295,30,580,793)) for page in q['questionPages'])
                    self.assertIn(normal(q['questionText']),normal(original))
                for change in [lambda s:s['atlasQuestions'][0].update(questionText='Invented extra source question'),lambda s:s['atlasQuestions'][0].update(questionPages=[99]),lambda s:s['atlasQuestions'][0].update(topicId='russian-unknown')]:
                    wrong=copy.deepcopy(generated);change(wrong)
                    with self.assertRaises(AssertionError):validate_joint_task(wrong,c,self.registry)
        finally:
            for d in docs.values():d.close()

    def test_listening_keeps_complete_unpriced_pools_and_every_known_partial_or_zero(self):
        docs,source=MODULE['source_records']()
        try:
            clauses=[];asks=0
            for section in range(1,5):
                c=self.get(f'l{section}');records=[r for r in source['tasks'] if r['unit']==f'L{section}']
                self.assertEqual(c['totalMarks'],20);self.assertEqual(c['tariffModel'],{'kind':'questionTotal'})
                self.assertTrue(all(row['marks'] is None for row in c['rows']));self.assertNotIn('answerLanguageRule',c)
                self.assertEqual(c['rows'][0]['verbatim'],source['listeningGuidance'])
                self.assertIn('Accept answers written in Russian',c['rows'][0]['verbatim'])
                self.assertEqual([row['verbatim'] for row in c['rows'][1:]],[r['publishedSourceBlock'] for r in records])
                asks+=len(records);clauses.extend(row['verbatim'] for row in c['rows'])
            self.assertEqual(asks,24)
            all_text=' '.join(clauses)
            for literal in ['Assign one mark: station','Award one mark: skating','Award one mark for a partial detail e.g. Dublin/Dundrum','Assign no marks: artists','Assign no marks: comedy']:
                self.assertIn(literal,all_text)
            self.assertIn('5(ii) twice',' '.join(row.get('contextNote','') for row in self.get('l1')['rows']))
            self.assertIn('Irish column prints 2(ii)',' '.join(row.get('contextNote','') for row in self.get('l4')['rows']))
        finally:
            for d in docs.values():d.close()

    def test_essay_preserves_unresolved_literal_deduction_and_every_choice(self):
        c=self.get('se');docs,source=MODULE['source_records']()
        try:
            record=next(r for r in source['tasks'] if r['unit']=='SE')
            self.assertEqual(c['totalMarks'],30);self.assertEqual(c['tariffModel'],{'kind':'questionTotal'})
            self.assertTrue(all(row['marks'] is None for row in c['rows']));self.assertNotIn('answerLanguageRule',c)
            self.assertEqual(normal(' '.join(r['verbatim'] for r in c['rows'])),normal(record['publishedSourceBlock']))
            for text in ['Sport in the Russian Federation','Education in the Russian Federation','The family in the Russian Federation','Religion in the Russian Federation','Housing in the Russian Federation']:
                self.assertIn(text,c['questionText'])
            self.assertIn('Deduct 1/2 marks',' '.join(r['verbatim'] for r in c['rows']))
            self.assertIn('Neither interpretation is selected',c['rows'][0]['contextNote'])
        finally:
            for d in docs.values():d.close()

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
