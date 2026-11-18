"""Mandatory pinned-original and joint-question coverage gate; no CI skips."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import fitz

from reconcile import parse_ref, reconcile_subject
from ru_joint_tasks import validate_joint_task, reviewed_joint_coverage
from ru_review_2011_hl import build, source_records, METADATA, grammar_forms
from ru_review_census import reviewed_keys
from ru_verify_review import verify, normal

ROOT = Path(__file__).resolve().parents[3]


def generated_source(card):
    return {key: card[key] for key in ('id', 'year', 'level', 'questionRef')} | {
        'paperFileid': 'LC099ALP000EV.pdf', 'schemeFileid': 'LC099ALP000EV.pdf', **card['review']}


class Original2011HigherSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = build()
        cls.registry = json.loads((ROOT / 'scripts/markbank/authoring/russian-joint-tasks.json').read_text())

    def get(self, suffix):
        return copy.deepcopy(next(c for c in self.cards if c['id'] == 'ru-2011-hl-' + suffix))

    def test_all_39_original_asks_keep_their_denominator_with_36_real_tasks(self):
        verify(self.cards)
        keys = set()
        for c in self.cards:
            for refstr in c['review'].get('coveredQuestionRefs', [c['questionRef']]):
                ref = parse_ref(refstr)
                self.assertIsNotNone(ref)
                keys.update((ref['section'], ref['q'], letter, roman) for letter, roman in ref['paths'])
        census = reviewed_keys(2011, 'hl')
        self.assertEqual(len(census), 39)
        self.assertEqual(keys, census)
        self.assertEqual(len(self.cards), 36)
        self.assertEqual(sum(c['totalMarks'] for c in self.cards), 300)

    def test_published_records_equal_original_derivation(self):
        authored = json.loads((ROOT / 'scripts/markbank/authored/russian-reviewed.json').read_text())
        published = [c for c in authored if c['year'] == 2011 and c['level'] == 'higher']
        self.assertEqual({c['id']: c for c in published}, {c['id']: c for c in self.cards})

    def test_joint_manifest_pins_all_four_original_prompts_and_pdf_hashes(self):
        docs, source = source_records()
        try:
            spec = self.registry['tasks'][0]
            self.assertEqual(spec['paperSha256'], METADATA['paper']['sha256'])
            self.assertEqual(spec['schemeSha256'], METADATA['scheme']['sha256'])
            self.assertEqual(spec['independentSittingAsks'], 39)
            originals = [r for r in source['tasks'] if r['unit'] == 'C2']
            self.assertEqual(len(originals), 4)
            for number, (q, original) in enumerate(zip(spec['questions'], originals), 1):
                self.assertEqual(q['questionText'], original['question'])
                self.assertEqual(q['questionPages'], [number + 5])
                self.assertEqual(q['schemePages'], [8, 9])
                self.assertEqual(q['leafKey'], ['C2', number, None, None])
                # The original p7 repeats coincident text-layer glyphs across
                # spans. Verify the literal source characters by geometry,
                # retaining one identical glyph at the same physical location.
                chars = []
                for block in docs['paper'][number + 4].get_text('rawdict', clip=fitz.Rect(295,30,580,793))['blocks']:
                    for line in block.get('lines', []):
                        for span in line.get('spans', []):
                            for char in span['chars']:
                                if not any(char['c'] == old['c'] and max(abs(a-b) for a,b in zip(char['bbox'], old['bbox'])) < .2 for old in chars):
                                    chars.append(char)
                lines = {}
                for char in chars:
                    key = round(char['origin'][1], 1)
                    lines.setdefault(key, []).append(char)
                visible = '\n'.join(''.join(c['c'] for c in sorted(line, key=lambda c:c['origin'][0])) for _, line in sorted(lines.items()))
                self.assertIn(normal(q['questionText']), normal(visible))
        finally:
            for d in docs.values(): d.close()

    def test_collective_45_and_paper_40_remain_literal_without_section_tariffs(self):
        docs, source = source_records()
        try:
            self.assertIn(normal('Summary writing 45 marks'), normal(docs['scheme'][7].get_text()))
            self.assertIn(normal('40 marks'), normal(docs['paper'][5].get_text()))
            c = self.get('c2')
            self.assertEqual(c['totalMarks'], 45)
            self.assertEqual(c['rubric']['allocationCap']['schemePages'], [8])
            self.assertEqual([k['maxMarks'] for k in c['rubric']['groups'][0]['criteria']], [10,2,10,2,10,2,10,2])
            c['rubric']['allocationCap']['schemePages'] = [9]
            with self.assertRaises(AssertionError): verify([c])
        finally:
            for d in docs.values(): d.close()

    def test_manual_language_retains_general_rule_and_specific_discretion_exception(self):
        c = self.get('c2')
        self.assertNotIn('answerLanguageRule', c)
        self.assertEqual(c['review']['guidancePages'], [3])
        for criterion in c['rubric']['groups'][0]['criteria']:
            guide = ' '.join(criterion['guidance'])
            self.assertIn('award NO marks', guide)
            self.assertIn('Discretionary marks may be awarded', guide)
            self.assertIn(normal('Russian-language words in their answers'), normal(guide))
        self.assertTrue(self.get('c1-1-i')['answerLanguageRule'])
        c['rubric']['groups'][0]['criteria'][1]['guidance'] = ['Always remove discretion if any Russian word is present.']
        with self.assertRaises(AssertionError): verify([c])

    def test_page_boundary_slices_recombine_without_changing_printed_headings(self):
        docs, source = source_records()
        try:
            original = next(r for r in source['tasks'] if r['unit']=='C2' and r['item']==2)
            criterion = next(k for k in self.get('c2')['rubric']['groups'][0]['criteria'] if k['id']=='section-2-content')
            self.assertIn(normal(original['publishedSourceBlock']), normal(' '.join(criterion['guidance'])))
            guide = ' '.join(self.get('gw')['rubric']['taskRequirements'])
            self.assertIn('1. FACEBOOK', guide)
            self.assertNotIn('1. NARRATIVE', guide)
            self.assertIn('3. INTERVIEW', guide)
            self.assertIn('4. DISCUSSION', guide)
        finally:
            for d in docs.values(): d.close()

    def test_joint_identity_rejects_missing_duplicate_unknown_or_mismatched_evidence(self):
        c = self.get('c2'); source = generated_source(c)
        self.assertIsNotNone(validate_joint_task(source, c, self.registry))
        mutations = [
            lambda s:s['coveredQuestionRefs'].pop(),
            lambda s:s['coveredQuestionRefs'].__setitem__(1, s['coveredQuestionRefs'][0]),
            lambda s:s['coveredQuestionRefs'].__setitem__(0, '2011 HL Section C2 Q5'),
            lambda s:s.__setitem__('year', 2012),
            lambda s:s.__setitem__('level', 'ordinary'),
            lambda s:s['atlasQuestions'][0].__setitem__('n', 'invented-summary'),
            lambda s:s['atlasQuestions'][0].__setitem__('questionText', ''),
            lambda s:s['atlasQuestions'][0].__setitem__('questionPages', [7]),
            lambda s:s['atlasQuestions'][0].__setitem__('schemePages', [10]),
            lambda s:s.pop('atlasQuestions'),
        ]
        for mutate in mutations:
            wrong = copy.deepcopy(source); mutate(wrong)
            with self.subTest(source=wrong), self.assertRaises(AssertionError):
                validate_joint_task(wrong, c, self.registry)
        wrong = copy.deepcopy(c); wrong['section'] = 'C1'
        with self.assertRaises(AssertionError): validate_joint_task(source, wrong, self.registry)
        wrong = copy.deepcopy(c); wrong['questionText'] = wrong['questionText'].split('Section 4')[0]
        with self.assertRaises(AssertionError): validate_joint_task(source, wrong, self.registry)
        wrong = copy.deepcopy(source); wrong['id'] = 'ru-2011-hl-invented'
        with self.assertRaises(AssertionError): validate_joint_task(wrong, c, self.registry)

    def test_coverage_checks_independent_census_and_does_not_inflate_cards(self):
        c = self.get('c2'); source = generated_source(c)
        census = {(2011,'hl',None): reviewed_keys(2011,'hl')}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            def write(relative, value):
                p = root / relative; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(value))
            write('scripts/markbank/authoring/russian-reviewed-sources.json', [source])
            write('scripts/markbank/authoring/russian-joint-tasks.json', self.registry)
            write('components/MarkBank/cards/russian/reviewed.json', [c])
            actual = reviewed_joint_coverage([(c['id'],c['questionRef'])], census, root)
            self.assertEqual(actual, {c['id']: source['coveredQuestionRefs']})
            wrong = copy.deepcopy(census); wrong[(2011,'hl',None)].remove(('C2',4,None,None))
            with self.assertRaises(AssertionError): reviewed_joint_coverage([(c['id'],c['questionRef'])], wrong, root)
            write('scripts/markbank/authoring/russian-reviewed-sources.json', [])
            with self.assertRaises(AssertionError): reviewed_joint_coverage([(c['id'],c['questionRef'])], census, root)
        leaves = [{'key': ['C2', n, None, None]} for n in range(1,5)]
        fixture = {'mode':'sections','papers':[{'year':2011,'level':'hl','leaves':leaves,'flags':[]}]}
        with patch('reconcile.shipped_cards', return_value=[(c['id'],c['questionRef'])]), patch('reconcile.load_exclusions', return_value=[]), patch('ru_joint_tasks.reviewed_joint_coverage', return_value={c['id']:source['coveredQuestionRefs']}):
            ledger = reconcile_subject('russian', fixture)
            self.assertEqual((ledger['cards'],ledger['leaves'],ledger['covered']), (1,4,4))
            self.assertEqual(ledger['orphans'], [])

    def test_non_russian_reconciliation_does_not_use_joint_metadata(self):
        fixture = {'mode':'sections','papers':[{'year':2011,'level':'hl','leaves':[{'key':['C2',1,None,None]},{'key':['C2',2,None,None]}],'flags':[]}]}
        with patch('reconcile.shipped_cards', return_value=[('ordinary-subject-card','2011 HL Section C2 Q1')]), patch('reconcile.load_exclusions', return_value=[]), patch('ru_joint_tasks.reviewed_joint_coverage') as joint:
            ledger = reconcile_subject('french', fixture)
            self.assertEqual((ledger['cards'],ledger['leaves'],ledger['covered'],ledger['open']), (1,2,1,1))
            joint.assert_not_called()

    def test_full_matching_partials_and_grammar_variants_are_original(self):
        docs, source = source_records()
        try:
            self.assertEqual(grammar_forms(docs)[6], ('вуз', 'вуза/ВУЗа'))
            self.assertIn('Upper Case or Lower Case are used inappropriately', ' '.join(self.get('gr')['rubric']['taskRequirements']))
            rows = self.get('sd')['rubric']['groups']
            self.assertEqual([r['text'] for r in rows[0]['rows']], ['6','5','8'])
            self.assertEqual([r['text'] for r in rows[-1]['rows']], ['5','2'])
        finally:
            for d in docs.values(): d.close()

if __name__ == '__main__': unittest.main()
