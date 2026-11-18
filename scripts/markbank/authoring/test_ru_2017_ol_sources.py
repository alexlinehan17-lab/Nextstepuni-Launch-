"""Bind all2017 Ordinary cards to originals and the explicitly approved listening allocation."""
import copy,json,re,sys,unittest
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from ru_review_2017_ol import build_written,source_records,raw_scheme_text
from ru_review_census import reviewed_keys
from ru_verify_review import normal,verify
from reconcile import parse_ref

def bind(cards,source,docs):
    written={r['id']:r for r in source['tasks'] if r['component']=='paper'}
    assert len(cards)==33 and {c['id'] for c in cards}==set(written)
    actual=set()
    for c in cards:
        r=written[c['id']]
        assert c['year']==2017 and c['level']=='ordinary'
        assert c['questionText'].startswith(r['question'])
        assert c['totalMarks']==r['publishedTotal']
        assert c['review']['questionPages']==r['questionPages']
        assert c['review']['schemePages']==r['schemePages']
        raw=[' '.join(docs['paper'][p-1].get_text(clip=clip) for p in r['questionPages']) for clip in (None,fitz.Rect(295,30,580,793))]
        assert any(normal(r['question']) in normal(text) for text in raw),c['id']
        ref=parse_ref(c['questionRef']);assert ref
        actual.update((ref['section'],ref['q'],letter,roman) for letter,roman in ref['paths'])
    assert actual=={k for k in reviewed_keys(2017,'ol') if k[0] not in ('L1','L2','L3','L4')}

class Original2017OrdinarySources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards=build_written();cls.docs,cls.source=source_records()
    @classmethod
    def tearDownClass(cls):
        for doc in cls.docs.values():doc.close()
    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2017-ol-'+suffix))
    def test_independent_paper_census_and_binding_reject_wrong_asks(self):
        proof=json.loads((ROOT/'scripts/markbank/authoring/reviews/russian-2017-ol-sec-20261118/printed-census.json').read_text())
        expected={(('SA' if a['unit']=='CA' else a['unit']),a['printedQuestion'],None,a['roman']) for a in proof['sourceAddresses']}
        self.assertEqual(len(expected),51);self.assertEqual(expected,reviewed_keys(2017,'ol'))
        self.assertEqual([len(self.docs[k]) for k in ('paper','aural','scheme')],[20,8,16])
        bind(self.cards,self.source,self.docs)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards),220)
        for mutation in ('question','year','page','ref','marks','duplicate'):
            bad=copy.deepcopy(self.cards)
            if mutation=='question':bad[0]['questionText']='Invented question'
            if mutation=='year':bad[0]['year']=2018
            if mutation=='page':bad[0]['review']['questionPages']=[99]
            if mutation=='ref':bad[0]['questionRef']='2017 OL Section IR1 Q99'
            if mutation=='marks':bad[0]['totalMarks']+=1
            if mutation=='duplicate':bad[1]=copy.deepcopy(bad[0])
            with self.assertRaises(AssertionError):bind(bad,self.source,self.docs)
    def test_all_claims_are_literal_and_wrong_answer_is_rejected(self):
        verify(self.cards)
        bad=self.get('ir1-i');bad['rubric']['groups'][0]['rows'][0]['text']='An invented accepted answer'
        with self.assertRaises(AssertionError):verify([bad])
    def test_both_printed_true_false_options_and_all_submission_formats(self):
        self.assertEqual(self.get('ir2-ii')['review']['questionOptions'],['True','False'])
        self.assertTrue(self.get('ir2-ii')['questionText'].endswith('True / False'))
        self.assertEqual([g['rows'][0]['text'] for g in self.get('ir2-v')['rubric']['groups']],['text/written','2 pages','A4','font: TimesNewRoman','font size: 12 point','photo','format: Jpeg','resolution: minimum 1500 pixels'])
    def test_all_climate_options_and_optional_date_are_preserved(self):
        card=self.get('ir1-vii');groups=card['rubric']['groups']
        self.assertEqual(len(groups),15);self.assertEqual(sum(len(g['rows']) for g in groups),18)
        self.assertEqual([r['text'] for g in groups for r in g['rows'] if r['id']=='named-partial'],['little sun','snow','wintery'])
        self.assertIn('if not rewarded in ii',' '.join(r['text'] for g in groups for r in g['rows']))
        dates=self.get('ir2-vi');self.assertEqual(dates['totalMarks'],2)
        self.assertEqual(dates['rubric']['groups'][0]['rows'][0]['text'],'(1) October 2017 + (1) April 2018')
    def test_original_language_answers_and_ten_matching_numbers(self):
        self.assertEqual([g['rows'][0]['marks'] for g in self.get('la2')['rubric']['groups']],[1]*6)
        matches=self.get('mm-1')['rubric']['groups']
        self.assertEqual([int(g['rows'][0]['text'].split(' — ')[0]) for g in matches],[10,3,2,4,5,6,1,9,8,7])
        self.assertEqual([g['rows'][0]['marks'] for g in matches],[4]*10)
        self.assertEqual([g['rows'][0]['text'] for g in self.get('sd')['rubric']['groups']],['Чем','Как','Что','Какие','кем','Чем','Что','Когда','Где','какое'])
    def test_no_answer_lines_have_fresh_archive_evidence_and_printed_marks(self):
        evidence=json.loads((ROOT/'scripts/markbank/authoring/reviews/russian-2017-ol-sec-20261118/archive-recheck.json').read_text())
        self.assertEqual({r['id'] for r in evidence['cardsWithNoPrintedAnswer']},{'ru-2017-ol-'+s for s in ('la1','sa','ew')})
        for suffix,total in [('la1',6),('sa',30),('ew',30)]:
            c=self.get(suffix);self.assertEqual(c['totalMarks'],total)
            self.assertTrue(c['rubric']['markingGuideNote'].startswith('The scheme prints no answer for this part.'))
        guide=self.get('la1')['rubric']['criteria'][0]['guidance'][0]
        for text in ['Deduct ½ mark','Do not penalise repeat errors','Round up to the nearest full number']:
            self.assertIn(text,guide)
    def test_all_written_choices_and_complete_original_bands(self):
        short=self.get('sa');extended=self.get('ew')
        for phrase in ['The media','Housing','The Russian regions','Shopping','Animals']:
            self.assertIn(phrase,short['questionText'])
        for phrase in ['My home county','Letter','How I spend my Sundays','whether you have a pet','what is your favourite place? Why?']:
            self.assertIn(phrase,extended['questionText'])
        self.assertIn('up to a maximum of 6 marks',short['rubric']['criteria'][0]['guidance'][0])
        self.assertEqual([b['marks'] for b in extended['rubric']['criteria'][1]['bands']],[[12],[10,11],[7,8,9],[4,5,6],[1,2,3],[0]])
        self.assertEqual([b['marks'] for b in extended['rubric']['criteria'][2]['bands']],[[6],[4,5],[2,3],[1],[0]])
        self.assertEqual(len(extended['rubric']['taskRequirements']),2)
    def test_printed_source_does_not_mislabel_the_approved_inference_as_a_printed_award(self):
        listening=[r for r in self.source['tasks'] if r['component']=='aural']
        self.assertEqual(len(listening),18);self.assertTrue(all(r['publishedTotal'] is None for r in listening))
        self.assertFalse(any(c.get('audioMaterial') for c in self.cards))
        self.assertIn('Award two marks for each correct/relevant point',self.source['listeningGuidance'])
    def test_raw_scheme_preserves_every_original_page(self):
        raw=raw_scheme_text()
        for n,page in enumerate(self.docs['scheme'],1):self.assertIn(f'## Page {n}\n\n'+page.get_text(),raw)

class Approved2017OrdinaryListeningSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from ru_review_2017_ol import build
        cls.cards=build();cls.listening=[c for c in cls.cards if c.get('audioMaterial')]
        cls.docs,cls.source=source_records()
    @classmethod
    def tearDownClass(cls):
        for doc in cls.docs.values():doc.close()
    def test_all51_printed_asks_and_source_addresses(self):
        self.assertEqual(len(self.cards),51);self.assertEqual(sum(c['totalMarks'] for c in self.cards),320)
        self.assertEqual(len(self.listening),18)
        actual=set()
        for c in self.cards:
            ref=parse_ref(c['questionRef']);self.assertIsNotNone(ref)
            actual.update((ref['section'],ref['q'],letter,roman) for letter,roman in ref['paths'])
        self.assertEqual(actual,reviewed_keys(2017,'ol'))
        records={r['id']:r for r in self.source['tasks'] if r['component']=='aural'}
        for c in self.listening:
            r=records[c['id']];self.assertEqual(c['questionText'],r['question'])
            self.assertEqual(c['review']['questionPages'],r['questionPages'])
            self.assertEqual(c['review']['schemePages'],r['schemePages'])
            raw=' '.join(self.docs['aural'][p-1].get_text(clip=fitz.Rect(295,30,580,793)) for p in r['questionPages'])
            self.assertIn(normal(c['questionText']),normal(raw))
        verify(self.cards)
    def test_inferred_marks_require_exact_approval_and_all_section_totals_reconcile(self):
        from ru_review_2017_ol import approved_listening
        for section in ('L1','L2','L3','L4'):
            self.assertEqual(sum(c['totalMarks'] for c in self.listening if c['section']==section),25)
        for c in self.listening:
            self.assertIn('five is not a printed per-detail award',c['rubric']['markingGuideNote'])
            self.assertIn('Award two marks',c['rubric']['markingGuideNote'])
            self.assertEqual(c['review']['sourceConflict']['approvedInferredMarksPerDetail'],5)
            self.assertEqual(c['totalMarks'],c['rubric']['count']*5)
        bad=copy.deepcopy(self.source);bad['listeningGuidance']=bad['listeningGuidance'].replace('Award two marks','Award three marks')
        with self.assertRaises(AssertionError):approved_listening(bad)
    def test_all_six_explicit_three_mark_alternatives_are_preserved(self):
        partials=[(c['id'],r['text'],r['marks']) for c in self.listening for g in c['rubric']['groups'] for r in g['rows'] if r['marks']==3]
        self.assertEqual(partials,[('ru-2017-ol-l1-3-i','34 (people)',3),('ru-2017-ol-l1-4','winner',3),('ru-2017-ol-l1-4','Azerbaijan',3),('ru-2017-ol-l2-2','kids up to the age of …',3),('ru-2017-ol-l2-3-ii','friendship',3),('ru-2017-ol-l4-3','Facebook',3)])
        allrows=[r for c in self.listening for g in c['rubric']['groups'] for r in g['rows']]
        self.assertEqual(len(allrows),108)
        self.assertTrue(all(r['marks'] in (3,5) for r in allrows))
        bad=copy.deepcopy(self.listening[0]);bad['rubric']['groups'][0]['rows'][0]['text']='Invented studio answer'
        with self.assertRaises(AssertionError):verify([bad])
    def test_each_listening_card_has_the_verified2017_official_recording(self):
        for c in self.listening:
            self.assertEqual(c['audioMaterial']['secFileid'],'LC099ZLP017EV.mp3')
            self.assertEqual(c['audioMaterial']['canonicalUrl'],'https://www.examinations.ie/archive/exampapers/2017/LC099ZLP017EV.mp3')
            self.assertEqual(c['sourceMaterial']['kind'],'source-question')
            self.assertEqual(c['review']['component'],'A00')
            self.assertEqual(c['additionalTopicIds'],['russian-1-0'])

if __name__=='__main__':unittest.main(verbosity=2)
