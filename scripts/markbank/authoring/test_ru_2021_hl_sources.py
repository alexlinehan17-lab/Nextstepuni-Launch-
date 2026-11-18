"""Mandatory pinned-original Russian 2021 Higher evidence; no source skips."""
import copy,hashlib,json,re,sys,unittest
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from reconcile import parse_ref
from ru_verify_review import normal,verify
from ru_review_2021_hl import build,source_records,grammar_forms,raw_scheme_text,summary_tariff,METADATA
from ru_review_census import reviewed_keys
NS={name:globals()[name] for name in ('build','source_records','grammar_forms','raw_scheme_text','summary_tariff','METADATA')}
NS['squash']=lambda value:' '.join(value.split())

KEYS=[('C1',q,None,r) for q,rs in [(1,('i','ii')),(2,('i','ii')),(3,('i','ii','iii')),(4,('i','ii'))] for r in rs]
KEYS += [('LA1',None,None,None),('CA1',None,None,None)]
KEYS += [('C2',q,None,None) for q in range(1,5)]
KEYS += [('LA2',None,None,r) for r in ('i','ii')]
KEYS += [(u,q,None,None) for u,q in [('SD',3),('GR',1),('SE',2),('GW',3)]]
KEYS += [('L1',q,None,None) for q in range(1,5)]
KEYS += [('L2',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,'i'),(2,'ii'),(3,None),(4,None)]]
KEYS += [('L3',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,'i'),(3,'ii'),(4,None)]]
KEYS += [('L4',q,None,r) for q,r in [(1,'i'),(1,'ii'),(2,None),(3,None)]]
assert len(KEYS)==len(set(KEYS))==41

def bind_original_cards(cards,records,docs):
    assert len(cards)==len({c['id'] for c in cards})==41
    source={r['id']:r for r in records};assert set(source)=={c['id'] for c in cards}
    actual=set()
    for c in cards:
        r=source[c['id']];assert c['year']==2021 and c['level']=='higher'
        parsed=parse_ref(c['questionRef']);assert parsed
        actual.update((parsed['section'],parsed['q'],letter,roman) for letter,roman in parsed['paths'])
        assert c['totalMarks']==r['publishedTotal']
        assert c['review']['questionPages']==r['questionPages']
        assert c['review']['schemePages']==r['schemePages']
        assert c['questionText'].startswith(r['question'])
        d=docs[r['component']]
        raw=[' '.join(d[p-1].get_text(clip=clip,sort=sort) for p in r['questionPages']) for clip in (None,fitz.Rect(295,30,580,793)) for sort in (False,True)]
        assert any(normal(r['question']) in normal(text) for text in raw),r['id']
    assert actual==set(KEYS)

class Original2021HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards=NS['build']();cls.docs,cls.source=NS['source_records']()
    @classmethod
    def tearDownClass(cls):
        for doc in cls.docs.values():doc.close()
    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2021-hl-'+suffix))
    def test_original_hashes_and_independent41_ask_boundaries(self):
        hashes={'paper':'cc1ccca7e039ac3d38af858cdf842bd549c42183c392684f368e67cc952cca22','aural':'b635aff4288709c732cc1cdc18e891ab13517d8ee21643f8578ff363266b5bf4','scheme':'7339c36919457d79424b100fb782372daf99d8c790dbe26ca5d69900779d3b41'}
        self.assertEqual({k:v['sha256'] for k,v in NS['METADATA'].items()},hashes)
        self.assertEqual([len(self.docs[k]) for k in ('paper','aural','scheme')],[16,8,28])
        bind_original_cards(self.cards,self.source['tasks'],self.docs)
        self.assertEqual(set(KEYS),reviewed_keys(2021,'hl'))
        self.assertEqual(sum(c['totalMarks'] for c in self.cards),320)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['kind']=='rubric'),320)
        for mutated in ['question','year','page','ref','price','duplicate']:
            bad=copy.deepcopy(self.cards)
            if mutated=='question':bad[0]['questionText']='An invented question'
            if mutated=='year':bad[0]['year']=2020
            if mutated=='page':bad[0]['review']['questionPages']=[99]
            if mutated=='ref':bad[0]['questionRef']='2021 HL Section C1 Q99'
            if mutated=='price':bad[0]['totalMarks']+=1
            if mutated=='duplicate':bad[1]=copy.deepcopy(bad[0])
            with self.assertRaises(AssertionError):bind_original_cards(bad,self.source['tasks'],self.docs)
    def test_original_exam_choices_and_six_guided_options(self):
        paper=' '.join(self.docs['paper'][p-1].get_text() for p in (1,2,5,9,11,13))
        for phrase in ['170','Answer Question 1 (50 marks) or Question 2','Question 3 (20 marks)','Question 1.2 Language Awareness or Question 1.3','Q. 2.2(i) or 2.2(ii)']:
            self.assertIn(normal(phrase),normal(paper))
        card=self.get('gw')
        for phrase in ['concert or a music festival','cover letter','favourite book or film','amusing episode','living in a big city','choosing a career']:
            self.assertIn(normal(phrase),normal(card['questionText']))
        self.assertEqual(self.source['selectedWrittenTotal']+self.source['listeningTotal'],250)
    def test_all17_original_identities_are_explicit_corrections(self):
        legacy=json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())
        old={c['id']:c for c in legacy if c['year']==2021 and c['level']=='higher'}
        corrected={c['id']:c for c in self.cards if c['review'].get('correctsExisting')}
        self.assertEqual(set(old),set(corrected));self.assertEqual(len(old),17)
        for identifier,c in corrected.items():
            self.assertEqual(c['topicId'],old[identifier]['topicId'])
            self.assertEqual(c['conceptId'],old[identifier]['conceptId'])
        for n in range(1,5):
            self.assertEqual(old[f'ru-2021-hl-c2-{n}']['totalMarks'],8)
            self.assertEqual(corrected[f'ru-2021-hl-c2-{n}']['totalMarks'],10)
    def test_one_school_year_fact_preserves_both_printed_alternatives(self):
        raw=self.docs['paper'][1].get_text();self.assertEqual(raw.count('11-классницу'),1)
        scheme=self.docs['scheme'][3].get_text();card=self.get('c1-1-ii')
        group=next(g for g in card['rubric']['groups'] if g['id']=='school-year')
        self.assertEqual(group['answerCount'],1);self.assertEqual(card['rubric']['count'],2)
        self.assertEqual([r['marks'] for r in group['rows']],[2,2])
        for row in group['rows']:self.assertIn(normal(row['text']),normal(scheme))
        self.assertEqual(len(card['rubric']['groups']),3)
    def test_advantage_and_disadvantage_are_distinct_required_categories(self):
        card=self.get('c1-3-iii');paper=self.docs['paper'][3].get_text()
        self.assertIn(normal('Give one advantage and one disadvantage'),normal(paper))
        self.assertEqual([(g['id'],g['answerCount'],len(g['rows'])) for g in card['rubric']['groups']],[('advantage',1,2),('disadvantage',1,1)])
        self.assertEqual(card['totalMarks'],4)
    def test_music_all22_entries_but21_distinct_credits_and_all_topics(self):
        r=next(r for r in self.source['tasks'] if r['unit']=='CA1');card=self.get('ca1')
        self.assertEqual(len(r['publishedEntries']),22);self.assertEqual(r['publishedEntries'].count('синтезатор'),2)
        rows=[g['rows'][0] for g in card['rubric']['groups']]
        self.assertEqual(len(rows),21);self.assertEqual(len({row['text'] for row in rows}),21)
        self.assertEqual(card['rubric']['count'],10);self.assertTrue(all(row['marks']==1 for row in rows))
        self.assertIn('No mark for YouTube (In English or Russian)',card['rubric']['taskRequirements'][0])
        self.assertEqual(card['topicId'],'russian-2-0');self.assertEqual(card['additionalTopicIds'],['russian-1-1','russian-0-5'])
    def test_complete_summary_page_continuations_and_manual_partial_rule(self):
        for n in range(1,5):
            r=next(r for r in self.source['tasks'] if r['unit']=='C2' and r['item']==n);card=self.get(f'c2-{n}')
            for block in r['sourcePageBlocks']:self.assertIn(block,card['rubric']['taskRequirements'])
            self.assertEqual(normal(' '.join(r['sourcePageBlocks'])),normal(r['publishedSourceBlock']))
            rows=[g['rows'][0] for g in card['rubric']['groups']]
            self.assertEqual(len(rows),{1:13,2:11,3:15,4:13}[n])
            self.assertTrue(all(row['steps']==[0,1,2] and row['marks']==2 for row in rows))
            self.assertTrue(all('Secondary details' not in row['text'] for row in rows))
            self.assertEqual(card['rubric']['count'],4)
            self.assertIn('intelligible to a monolingual speaker of English',' '.join(card['rubric']['taskRequirements']))
            e=NS['summary_tariff'](self.docs['scheme'],n);self.assertEqual(e['text'],'10 marks')
        first=self.get('c2-1');limit=next(l for l in first['rubric']['criteria'][0]['limits'] if l['id']=='missing-certain-or-uncertain')
        self.assertEqual(limit['maxMarks'],1);self.assertIn('at least one uncertain and one certain aspect',' '.join(first['rubric']['taskRequirements']))
    def test_original50_40_paper_labels_and_irish_permission_stay_visible(self):
        paper=self.docs['paper'][5].get_text();self.assertIn('50 marks',paper);self.assertIn('40 marks',paper);self.assertIn('i nGaeilge',paper)
        for n in range(1,5):
            note=self.get(f'c2-{n}')['rubric']['markingGuideNote']
            self.assertIn('50 marks',note);self.assertIn('40 marks',note);self.assertIn('Irish is not a disallowed answer language',note)
    def test_summary_discretion_exception_binds_its_own_original_page(self):
        card=self.get('c2-1');rule=card['answerLanguageRule'];self.assertEqual(rule['otherLanguageMultiplier'],0)
        e=rule['manualCriterionExceptions'];self.assertEqual(e['criterionIds'],['summary-skills']);self.assertEqual(e['schemePages'],[7])
        self.assertIn(normal(e['sourceText']),normal(self.docs['scheme'][6].get_text()))
        for mutation in ['wrong-page','invented-rule']:
            bad=copy.deepcopy(card)
            if mutation=='wrong-page':bad['answerLanguageRule']['manualCriterionExceptions']['schemePages']=[3]
            else:bad['answerLanguageRule']['manualCriterionExceptions']['sourceText']='Invented discretionary credit rule'
            with self.assertRaises(AssertionError):verify([bad])
    def test_language_infinitive_clauses_and_original_numbering(self):
        card=self.get('la2-i');guide=' '.join(card['rubric']['taskRequirements'])
        self.assertIn('Irish, English or Russian',guide);self.assertIn('translate the phrases into English',guide);self.assertNotIn('answerLanguageRule',card)
        self.assertEqual(len(card['rubric']['groups']),5)
        page=self.docs['paper'][8].get_text();self.assertIn('C.2.2(i)',page);self.assertIn('Q.2.2(ii)',page)
        self.assertIn('repeating the first Irish label',self.get('la2-ii')['rubric']['markingGuideNote'])
    def test_fifteen_native_grammar_forms_for_thirteen_prompts(self):
        forms=NS['grammar_forms'](self.docs['scheme']);self.assertEqual(len(forms),15)
        page=self.docs['paper'][10].get_text();passage=page.split('В середине лета',1)[1]
        prompts=re.findall(r'\(([^)]+)\)',passage);self.assertEqual(len(prompts),13)
        self.assertIn('учебное заведение',prompts);self.assertIn('международная арена',prompts)
        card=self.get('gr');self.assertEqual([g['rows'][0]['text'] for g in card['rubric']['groups']],forms)
        self.assertEqual(forms[0],'увлекалась/увлекается');self.assertTrue(all(g['rows'][0]['marks']==2 for g in card['rubric']['groups']))
    def test_six_writing_choices_literal_overlap_and_explicit_deduction(self):
        card=self.get('gw');expression=card['rubric']['criteria'][1]
        lower=next(l for l in expression['limits'] if l['id']=='lower-a')
        self.assertEqual((lower['minMarks'],lower['maxMarks']),(7,12));self.assertNotIn('bands',lower)
        guide=' '.join(lower['guidance']);self.assertIn('9/10',guide);self.assertIn('9-11',guide);self.assertIn('11-12',guide)
        penalty=next(c for c in card['rubric']['criteria'] if c['id']=='soft-sign-penalty');self.assertEqual(penalty['permittedMarks'],[0,2])
    def test_essay_uses_printed_content_expression_grid_and_retains_every_original_page(self):
        card=self.get('se');record=next(r for r in self.source['tasks'] if r['unit']=='SE')
        self.assertEqual(card['totalMarks'],30);self.assertEqual(card['rubric']['system'],'language-writing')
        self.assertEqual(card['rubric']['taskRequirements'],record['sourcePageBlocks'])
        content,title,expression=card['rubric']['criteria']
        self.assertEqual((content['maxMarks'],expression['maxMarks']),(10,20))
        self.assertEqual(content['permittedMarks'],[0,2,4,6,8,10])
        self.assertEqual(title['permittedMarks'],[0,1]);self.assertEqual(title['deductFrom'],'content')
        self.assertEqual([b['marks'] for b in expression['bands']],[[18,19,20],[14,15,16,17],[10,11,12,13],[6,7,8,9],[1,2,3,4,5],[0]])
        lower_e=next(l for l in expression['limits'] if l['id']=='lower-e')
        lower_a=next(l for l in expression['limits'] if l['id']=='lower-a')
        self.assertEqual([b['marks'] for b in lower_e['bands']],[[12,13,14],[10,11],[7,8,9],[4,5,6],[1,2,3],[0]])
        self.assertEqual([b['marks'] for b in lower_a['bands']],[[13,14],[11,12],[9,10]])
        self.assertIn('Deduct 1/2 marks',' '.join(expression['guidance']))
        self.assertNotIn('soft-sign-penalty',[c['id'] for c in card['rubric']['criteria']])
        self.assertTrue(card['rubric']['markingGuideNote'].startswith('The scheme prints no answer for this part.'))
        self.assertEqual(card['review']['noPrintedAnswer']['schemePages'],[13,14,15])
        self.assertEqual(card['questionText'].count('•'),5);self.assertNotIn('answerLanguageRule',card)
    def test_twenty_listening_local_prices_and_named_partials(self):
        cards=[c for c in self.cards if c.get('audioMaterial')];self.assertEqual(len(cards),20);self.assertEqual(sum(c['totalMarks'] for c in cards),80)
        for card in cards:
            self.assertNotIn('answerLanguageRule',card);self.assertIn('Accept answers written in Russian',' '.join(card['rubric']['taskRequirements']))
        crew=self.get('l3-2');self.assertEqual(crew['totalMarks'],4);self.assertEqual(len(crew['rubric']['groups']),1);self.assertEqual(crew['rubric']['groups'][0]['rows'][0]['marks'],4)
        boat=self.get('l3-1-i');self.assertEqual([g['rows'][0]['marks'] for g in boat['rubric']['groups']],[2,2,1]);self.assertEqual(boat['rubric']['count'],1)
        education=self.get('l4-1-i');group=next(g for g in education['rubric']['groups'] if any(r['id']=='economics-only' for r in g['rows']))
        self.assertEqual([r['marks'] for r in group['rows']],[2,1]);self.assertEqual(group['answerCount'],1)
        for suffix,phrase in [('l2-2-i','training twice a week + on Tuesdays and Thursdays'),('l4-3','Don’t focus on one topic only + try different things'),('l4-3','Try to improve the picture + photo and video content')]:
            self.assertTrue(any(phrase in r['text'] and r['marks']==2 for g in self.get(suffix)['rubric']['groups'] for r in g['rows']))
    def test_full_raw_pages_and_separate_mechanical_rendering(self):
        text=NS['raw_scheme_text']();self.assertEqual(text,(ROOT/'examiner-reports/russian/schemes/2021-hl.md').read_text())
        for p,page in enumerate(self.docs['scheme'],1):
            raw=page.get_text();self.assertIn(f'## Page {p}\n\n'+raw,text)
            self.assertIn(f'### Joined original page {p}\n\n'+NS['squash'](raw),text)
    def test_all_original_claims_and_fresh_derivation_equal_saved_proposal(self):
        verify(self.cards);self.assertEqual(self.cards,[c for c in json.loads((ROOT/'scripts/markbank/authored/russian-reviewed.json').read_text()) if c['year']==2021 and c['level']=='higher'])
        bad=self.get('l3-2');bad['rubric']['groups'][0]['rows'][0]['text']='An invented accepted answer'
        with self.assertRaises(AssertionError):verify([bad])

if __name__=='__main__':unittest.main(verbosity=2)
