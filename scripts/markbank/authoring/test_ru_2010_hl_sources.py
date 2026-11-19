"""Mandatory original-PDF, glyph, census and negative source gate for 2010 Higher."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import fitz
import ru_2010_hl_fonts as fonts
from reconcile import parse_ref
from ru_review_2010_hl import build,source_records
from ru_review_census import reviewed_keys
from ru_verify_review import verify,normal,verify_automatic_award_sources

ROOT=Path(__file__).resolve().parents[3]


class Original2010HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards=build();cls.docs,cls.source=source_records()

    @classmethod
    def tearDownClass(cls):
        for document in cls.docs.values():document.close()

    def get(self,suffix):return copy.deepcopy(next(c for c in self.cards if c['id']=='ru-2010-hl-'+suffix))

    def test_all_38_independently_reviewed_asks_have_original_source_claims(self):
        verify(self.cards);keys=set()
        for card in self.cards:
            ref=parse_ref(card['questionRef']);self.assertIsNotNone(ref)
            keys.update((ref['section'],ref['q'],letter,roman) for letter,roman in ref['paths'])
        self.assertEqual(keys,reviewed_keys(2010,'hl'));self.assertEqual(len(keys),38)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards if c['id']!='ru-2010-hl-l1-1-i'),296)
        self.assertEqual(self.source['sourceLeafTotalIncludesDerivedMissingAnswerMarks'],4)

    def test_published_records_equal_original_derivation(self):
        cards=json.loads((ROOT/'scripts/markbank/authored/russian-reviewed.json').read_text())
        published={c['id']:c for c in cards if c['year']==2010 and c['level']=='higher'}
        self.assertEqual(published,{c['id']:c for c in self.cards})

    def test_all_missing_glyphs_are_original_id_bound_and_visually_reviewed(self):
        self.assertEqual([len(f['glyphs']) for f in fonts.REVIEW['fonts']],[49,31,35])
        for relative,key in [('papers/2010-hl-000-paper.pdf','paperSha256'),('schemes/2010-hl.pdf','schemeSha256')]:
            self.assertEqual(hashlib.sha256((ROOT/'examiner-reports/russian'/relative).read_bytes()).hexdigest(),fonts.REVIEW[key])
        self.assertNotIn('\ufffd',''.join(p.get_text() for p in self.docs['scheme']))
        for path in fonts.REVIEW['comparisonImages']:self.assertTrue((ROOT/path).is_file())
        self.assertIn('Exact geometry equality is not claimed',fonts.REVIEW['assessment'])

    def test_invented_glyph_mapping_fails_before_repair(self):
        review=copy.deepcopy(fonts.REVIEW);review['fonts'][0]['glyphs'][0]['unicode']=ord('Z')
        with patch.object(fonts,'REVIEW',review):
            with self.assertRaises(AssertionError):fonts.open_repaired_scheme()

    def test_full_award_survives_and_only_exact_footer_blocks_are_removed(self):
        document=self.docs['scheme'];phrase='award 2 marks to all (there is no noun in the dative case)'
        self.assertIn(phrase,normal_text:= ' '.join(document[4].get_text().split()))
        self.assertNotIn(phrase,' '.join(document[4].get_text(clip=fitz.Rect(20,30,580,793)).split()))
        self.assertIn(phrase,' '.join(fonts.scheme_page(document,5).split()))
        self.assertIn('Include:',document[12].get_text(clip=fitz.Rect(20,30,580,793)))
        for page in range(3,20):
            text=fonts.scheme_page(document,page)
            self.assertNotIn(normal(fonts.REVIEW['footerBlocks'][str(page)]['text']),normal(text))
        self.assertIn('case)',normal_text)

    def test_unverified_footer_rectangle_is_rejected(self):
        review=copy.deepcopy(fonts.REVIEW);review['footerBlocks']['5']['bbox'][0]+=1
        with patch.object(fonts,'REVIEW',review):
            with self.assertRaises(AssertionError):fonts.scheme_page(self.docs['scheme'],5)

    def test_all_six_prompts_original_story_and_specific_language_allowance_survive(self):
        c=self.get('la1');record=next(r for r in self.source['tasks'] if r['unit']=='LA1')
        self.assertEqual(len(record['printedPrompts']),6)
        self.assertEqual(c['sourceMaterial']['pages'],[2,5])
        for prompt in record['printedPrompts']:
            self.assertIn(normal(prompt),normal(c['questionText']))
            self.assertIn(normal(prompt),normal(self.docs['paper'][4].get_text()))
        criteria=c['rubric']['criteria'];self.assertEqual([x['permittedMarks'] for x in criteria],[[0,2],[0,2],[0,2],[2],[0,2],[0,2]])
        self.assertEqual(criteria[3]['id'],'section2-dative-plural')
        self.assertNotIn('answerLanguageRule',c)
        self.assertIn('translated and supplied in English OR', ' '.join(c['rubric']['taskRequirements']))
        verify_automatic_award_sources(self.docs['scheme'],c)
        c['rubric']['criteria'][3]['automaticAward']['schemePages']=[6]
        with self.assertRaises(AssertionError):verify_automatic_award_sources(self.docs['scheme'],c)

    def test_infinitive_question_contains_worked_example_and_five_actual_prompts(self):
        c=self.get('la2-1');record=next(r for r in self.source['tasks'] if r['unit']=='LA2' and r['item']==1)
        self.assertEqual(c['questionText'],record['question'])
        self.assertIn('Sampla/Example: получила получить',c['questionText'])
        self.assertEqual(record['printedVerbs'],['имеют','выбрались','поняла','создалось','стали'])
        for fragment in record['questionFragments']:self.assertIn(normal(fragment),normal(self.docs['paper'][8].get_text()))
        self.assertEqual([g['label'] for g in c['rubric']['groups']],record['printedVerbs'])
        self.assertEqual([g['rows'][0]['text'] for g in c['rubric']['groups']],['иметь','выбраться','понять','создаться','стать'])
        altered=copy.deepcopy(c);altered['questionText']=altered['questionText'].replace('выбрались','')
        self.assertNotEqual(altered['questionText'],record['question'])

    def verify_missing_city(self,c):
        record=next(r for r in self.source['tasks'] if r.get('missingAcceptedAnswerSource'))
        self.assertEqual(c['questionText'],record['question']);self.assertEqual(c['questionRef'],'2010 HL Section L1 Q1(i)')
        self.assertEqual(c['totalMarks'],4);self.assertEqual(record['derivedTotalBasis']['detailCount'],2)
        self.assertEqual(record['derivedTotalBasis']['marksPerDetail'],2)
        self.assertEqual(c['tariffModel'],{'kind':'questionTotal'});self.assertEqual(len(c['rows']),1)
        self.assertEqual(c['rows'][0]['verbatim'],self.source['listeningGuidance']);self.assertIsNone(c['rows'][0]['marks'])
        self.assertIn('derived',c['rows'][0]['contextNote']);self.assertIn('not a separately printed task total',c['rows'][0]['contextNote'])
        self.assertNotIn('answerLanguageRule',c)
        all_text=' '.join(p.get_text() for p in self.docs['scheme'])
        self.assertEqual(all_text.count('Yaroslavl'),1)
        self.assertIn(normal(record['question']),normal(self.docs['aural'][1].get_text()))

    def test_missing_city_is_confidence_only_with_original_audio_and_derived_total(self):
        c=self.get('l1-1-i');self.verify_missing_city(c);self.assertIsNotNone(c['audioMaterial'])

    def test_borrowed_city_answer_or_invented_numeric_row_is_rejected(self):
        for update in [{'verbatim':'The city has one thousand years of history.'},{'marks':4}]:
            c=self.get('l1-1-i');c['rows'][0].update(update)
            with self.assertRaises(AssertionError):self.verify_missing_city(c)

    def test_summary_exception_requires_its_own_original_page(self):
        c=self.get('c2-1');exception=c['answerLanguageRule']['manualCriterionExceptions']
        self.assertEqual(exception['schemePages'],[7]);self.assertIn('Russian-language words',exception['sourceText'])
        exception['schemePages']=[3]
        with self.assertRaises(AssertionError):verify([c])

    def test_invented_grammar_partial_or_swimming_rule_is_rejected(self):
        for suffix,claim in [('gr','Award one mark for incorrect capitalisation.'),('la2-2','Award one mark for sailing and boating vocabulary.')]:
            c=self.get(suffix);c['rubric']['taskRequirements'].append(claim)
            with self.assertRaises(AssertionError):verify([c])


if __name__=='__main__':unittest.main()
