"""Regression checks for line-leading function notation in older Maths papers."""
import unittest

from paper import Paper, _split_own_line_markers
from paper_census import census_subject, census_merged, continuity_flags, leaves_of
from reconcile import parse_ref, reconcile_subject
from unittest.mock import patch


class MathsFunctionMarkersTest(unittest.TestCase):
    def test_2010_ordinary_project_paper2_keeps_window_and_both_routes_separate(self):
        parts, texts, _ = census_merged('maths', 2010, 'ol', '230')
        leaves = leaves_of(parts)
        self.assertEqual(len(leaves), 46)
        self.assertEqual([sum(k[0] == q for k in leaves)
                          for q in list(range(1, 9)) + ['9A', '9B']],
                         [6, 2, 3, 4, 5, 3, 6, 5, 7, 5])
        self.assertEqual({k for k in leaves if k[0] == 8},
                         {(8, part, None) for part in 'abcde'})
        self.assertIn('scaled drawing', texts[(8, 'e', None)])
        self.assertNotIn('sunshine', texts[(8, 'e', None)])
        self.assertIn('Tukey Quick Test', texts[('9A', 'c', None)])
        self.assertIn('median', texts[('9A', 'e', 'i')])
        self.assertIn('parallel', texts[('9B', 'a', 'iii')])
        self.assertFalse(any(f['type'].endswith('-gap')
                             for f in continuity_flags(parts, texts)))

    def test_2010_higher_project_paper2_keeps_both_routes_out_of_question_eight(self):
        parts, texts, _ = census_merged('maths', 2010, 'hl', '230')
        leaves = leaves_of(parts)
        self.assertEqual(len(leaves), 35)
        self.assertEqual([sum(k[0] == q for k in leaves)
                          for q in list(range(1, 9)) + ['9A', '9B']],
                         [4, 2, 2, 2, 3, 4, 7, 5, 3, 3])
        self.assertEqual({k for k in leaves if k[0] == 8},
                         {(8, part, None) for part in 'abcde'})
        self.assertIn('ship is moving', texts[(8, 'b', None)])
        self.assertIn('at least two', texts[('9A', 'b', None)])
        self.assertIn('three parallel lines', texts[('9B', 'a', None)])
        self.assertIn('total length of timber', texts[('9B', 'b', 'ii')])
        self.assertFalse(any(f['type'].endswith('-gap')
                             for f in continuity_flags(parts, texts)))

    def test_2010_higher_paper2_heads_following_formulas_and_rubric(self):
        parts, texts, _ = census_merged('maths', 2010, 'hl', '200')
        leaves = leaves_of(parts)
        self.assertEqual(len(leaves), 57)
        self.assertEqual([sum(k[0] == n for k in leaves) for n in range(1, 12)],
                         [4, 6, 5, 5, 5, 3, 6, 6, 5, 7, 5])
        for q, phrase in [(2, 'A, B and C'), (4, 'triangle PQR'),
                          (6, 'four red discs'), (8, 'integration by parts')]:
            self.assertIn(phrase, texts[(q, 'a', None)])
        self.assertNotIn((3, 'c', 'iii'), leaves)
        self.assertNotIn((7, 'c', 'iii'), leaves)
        self.assertFalse(any(f['type'] == 'question-gap' for f in continuity_flags(parts, texts)))

    def test_2011_higher_project_paper2_keeps_both_complete_proofs(self):
        parts, texts, _ = census_merged('maths', 2011, 'hl', '230')
        leaves = leaves_of(parts)
        self.assertEqual(len(leaves), 28)
        self.assertEqual({k for k in leaves if str(k[0]).startswith('6')}, {
            ('6A', None, None), ('6B', None, None)})
        self.assertIn('three parallel lines', texts[('6A', None, None)])
        self.assertIn('Prove', texts[('6B', None, None)])
        self.assertFalse(any(f['type'] == 'question-gap' for f in continuity_flags(parts, texts)))

    def test_2011_higher_project_jewellery_page_keeps_all_six_leaves(self):
        parts, texts, _ = census_merged('maths', 2011, 'hl', '130')
        leaves = leaves_of(parts)
        self.assertEqual([sum(k[0] == n for k in leaves) for n in range(1, 10)],
                         [3, 4, 2, 4, 6, 7, 7, 5, 4])
        self.assertIn('total value of the jeweller', texts[(5, 'a', None)])
        self.assertIn('21 grams of 15-carat gold', texts[(5, 'b', None)])
        self.assertIn('copper', texts[(5, 'c', 'i')])
        self.assertIn('monthly profit', texts[(5, 'd', 'ii')])
        self.assertIn('constant multiple', texts[(4, 'c', None)])
        self.assertFalse(any(k[0] == 55 for k in leaves))

    def test_2011_ordinary_legacy_paper2_restores_first_and_trailing_heads(self):
        parts, texts, _ = census_merged('maths', 2011, 'ol', '200')
        leaves = leaves_of(parts)
        self.assertEqual(len(leaves), 74)
        self.assertEqual([sum(k[0] == n for k in leaves) for n in range(1, 12)],
                         [6, 7, 8, 7, 6, 10, 7, 5, 8, 6, 4])
        self.assertIn('rectangle', texts[(1, 'a', 'i')])
        self.assertIn('2 : 1.', Paper('maths', 2011, 'ol', '200').text(9, 'c'))
        self.assertIn('expansion', texts[(10, 'a', 'i')])
        self.assertFalse(any(f['type'] == 'question-gap' for f in continuity_flags(parts, texts)))

    def test_2010_higher_legacy_paper1_standalone_first_head(self):
        parts, texts, _ = census_merged('maths', 2010, 'hl', '100')
        self.assertEqual({k for k in leaves_of(parts) if k[0] == 1}, {
            (1, 'a', None), (1, 'b', None), (1, 'c', 'i'), (1, 'c', 'ii'), (1, 'c', 'iii')})
        self.assertIn('real roots', texts[(1, 'b', None)])
        leaves = leaves_of(parts)
        self.assertEqual(len(leaves), 40)
        self.assertEqual([sum(k[0] == n for k in leaves) for n in range(1, 9)],
                         [5, 5, 5, 6, 4, 5, 5, 5])
        self.assertIn('recurring decimal', texts[(4, 'a', None)])
        self.assertNotIn('recurring decimal', texts[(3, 'c', 'ii')])
        self.assertNotIn((3, 'c', 'iii'), leaves)


    def test_2011_ordinary_ratio_does_not_skip_question_two(self):
        parts, texts, _ = census_merged('maths', 2011, 'ol', '000')
        leaves = leaves_of(parts)
        self.assertEqual(len(leaves), 49)
        self.assertEqual([sum(k[0] == q for k in leaves) for q in range(1, 9)],
                         [7, 7, 5, 7, 6, 6, 6, 5])
        self.assertIn('prize fund', texts[(1, 'a', 'i')])
        self.assertIn('cost a year ago', texts[(1, 'b', 'ii')])
        self.assertIn('3a(x + 5) = 114', texts[(2, 'a', None)])
        self.assertIn('Multiply', texts[(3, 'a', None)])
        paper = Paper('maths', 2011, 'ol', component='000')
        self.assertIn('4 : 3. Aoife gets €56.', paper.text(1, 'a'))
        self.assertFalse(any(f['type'].endswith('-gap')
                             for f in continuity_flags(parts, texts)))

    def test_zero_component_keeps_original_paper_filename(self):
        from maths_question_figures import Sitting
        sitting = Sitting(2011, 'ol', 0)
        try:
            self.assertTrue(sitting.path.endswith('/2011-ol-000-paper.pdf'))
            self.assertIn('PAPER 1', sitting.doc[0].get_text())
            self.assertEqual(sitting.doc.page_count, 8)
        finally:
            sitting.doc.close()

    def test_wrapped_ratio_keeps_the_part_after_its_last_operand(self):
        paper = Paper('maths', 2017, 'hl', component='200')
        self.assertIn('co-ordinates', paper.text(3, 'a'))
        self.assertIn('2 : 1.', paper.stem(3))

    def test_separately_marked_bullets_do_not_overwrite_question_images(self):
        from maths_question_figures import REF, fig_name
        names = [fig_name(*REF.match(f'2012 FL Paper 2 Q7(b)(ii)({n})').groups())
                 for n in (1, 2, 3)]
        self.assertEqual(names, ['maths-2012-FL-ask-p2-q7-b-ii-1',
                                 'maths-2012-FL-ask-p2-q7-b-ii-2',
                                 'maths-2012-FL-ask-p2-q7-b-ii-3'])
        self.assertEqual(fig_name(*REF.match('2012 FL Paper 2 Q7(b)(i)').groups()),
                         'maths-2012-FL-ask-p2-q7-b-i')

    def test_2012_phase3_ordinary_keeps_both_geometry_routes(self):
        parts, texts, _ = census_merged('maths', 2012, 'ol', '230')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', 'i'), ('6A', 'a', 'ii'), ('6A', 'b', None), ('6B', None, None)})
        self.assertIn('geometrical result', texts[('6A', 'a', 'i')])
        self.assertIn('tangent', texts[('6A', 'a', 'ii')])
        self.assertIn('circumcentre', texts[('6A', 'b', None)])
        self.assertIn('Prove', texts[('6B', None, None)])
        self.assertFalse(any(f['type'] == 'question-gap' for f in continuity_flags(parts, texts)))


    def test_2012_phase1_ordinary_keeps_both_geometry_routes(self):
        parts, texts, _ = census_merged('maths', 2012, 'ol', '200')
        self.assertEqual({k for k in parts if str(k[0]).startswith('5')}, {
            ('5A', 'a', 'i'), ('5A', 'a', 'ii'), ('5A', 'b', None), ('5B', None, None)})
        self.assertIn('geometrical result', texts[('5A', 'a', 'i')])
        self.assertIn('tangent', texts[('5A', 'a', 'ii')])
        self.assertIn('circumcentre', texts[('5A', 'b', None)])
        self.assertIn('Prove', texts[('5B', None, None)])
        self.assertFalse(any(f['type'] == 'question-gap' for f in continuity_flags(parts, texts)))

    def test_2012_phase1_higher_keeps_both_geometry_routes(self):
        parts, texts, _ = census_merged('maths', 2012, 'hl', '200')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', 'i'), ('6A', 'a', 'ii'), ('6A', 'b', None), ('6B', None, None)})
        self.assertIn('protractor', texts[('6A', 'a', 'i')])
        self.assertIn('15°', texts[('6A', 'a', 'ii')])
        self.assertIn('congruent', texts[('6A', 'b', None)])
        self.assertIn('incircle', texts[('6B', None, None)])
        self.assertFalse(any(f['type'] == 'question-gap' for f in continuity_flags(parts, texts)))

    def test_2012_phase3_higher_keeps_both_geometry_routes(self):
        parts, texts, _ = census_merged('maths', 2012, 'hl', '230')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', 'i'), ('6A', 'a', 'ii'), ('6A', 'b', None), ('6B', None, None)})
        self.assertIn('protractor', texts[('6A', 'a', 'i')])
        self.assertIn('15°', texts[('6A', 'a', 'ii')])
        self.assertIn('congruent', texts[('6A', 'b', None)])
        self.assertIn('incircle', texts[('6B', None, None)])
        self.assertFalse(any(f['type'] == 'question-gap' for f in continuity_flags(parts, texts)))

    def test_2013_phase2_ordinary_routes_and_letter_i_are_separate(self):
        parts, texts, _ = census_merged('maths', 2013, 'ol', '200')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', None), ('6A', 'b', None), ('6A', 'c', None), ('6B', None, None)})
        self.assertIn('axial symmetry', texts[('6A', 'b', None)])
        self.assertIn('Prove', texts[('6B', None, None)])
        self.assertNotIn((7, 'h', 'i'), parts)
        self.assertIn('scatter plot', texts[(7, 'i', None)])
        self.assertIn('ratio', texts[(7, 'h', None)])

    def test_2013_ordinary_routes_and_letter_i_are_separate(self):
        parts, texts, _ = census_merged('maths', 2013, 'ol', '230')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', None), ('6A', 'b', None), ('6A', 'c', None), ('6B', None, None)})
        self.assertIn('axial symmetry', texts[('6A', 'b', None)])
        self.assertIn('Prove', texts[('6B', None, None)])
        self.assertNotIn((7, 'h', 'i'), parts)
        self.assertIn('scatter plot', texts[(7, 'i', None)])
        self.assertIn('ratio', texts[(7, 'h', None)])

    def test_project_cards_do_not_cover_parallel_legacy_questions(self):
        census = census_subject('maths')
        cid = 'maths-2013-hl-p1-project-q1-a'
        with patch('reconcile.shipped_cards', return_value=[(cid, '2013 HL Paper 1 Q1(a) — Project Maths')]):
            result = reconcile_subject('maths', census)
        papers = {p['paper']: p for p in result['papers'] if p['year'] == 2013 and p['level'] == 'hl'}
        self.assertEqual(papers['130']['covered'], 1)
        self.assertEqual(papers['Paper 1']['covered'], 0)
        self.assertEqual(result['orphans'], [])

    def test_2014_project_maths_components_reconcile_as_numbered_papers(self):
        census = census_subject('maths')
        earlier = [p['paper'] for p in census['papers'] if p['year'] == 2013 and p['level'] == 'hl']
        self.assertEqual(set(earlier), {'Paper 1', 'Paper 2', '130', '230'})
        papers = [p for p in census['papers']
                  if p['year'] == 2014 and p['level'] == 'hl']
        self.assertEqual({p['paper'] for p in papers}, {'Paper 1', 'Paper 2'})
        paper_one = next(p for p in papers if p['paper'] == 'Paper 1')
        self.assertNotIn('error', paper_one)
        self.assertTrue(any(leaf['key'][0] == 9 for leaf in paper_one['leaves']))

    def test_2013_phase2_paper_two_keeps_both_geometry_routes(self):
        parts, texts, _ = census_merged('maths', 2013, 'hl', '200')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', None), ('6A', 'a', 'i'), ('6A', 'a', 'ii'), ('6A', 'a', 'iii'),
            ('6A', 'b', None), ('6A', 'c', None), ('6B', 'a', None), ('6B', 'b', None)})
        self.assertIn('orthocentre', texts[('6A', 'c', None)])
        self.assertIn('parallelogram', texts[('6B', 'b', None)])
        self.assertFalse(any(f['type'] == 'question-gap' for f in continuity_flags(parts, texts)))

    def test_2013_project_paper_two_keeps_both_geometry_routes(self):
        parts, texts, _ = census_merged('maths', 2013, 'hl', '230')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', None), ('6A', 'a', 'i'), ('6A', 'a', 'ii'), ('6A', 'a', 'iii'),
            ('6A', 'b', None), ('6A', 'c', None), ('6B', 'a', None), ('6B', 'b', None)})
        self.assertIn('orthocentre', texts[('6A', 'c', None)])
        self.assertIn('parallelogram', texts[('6B', 'b', None)])
        self.assertFalse(any(f['type'] == 'question-gap' for f in continuity_flags(parts, texts)))

    def test_2014_paper_two_alternatives_have_separate_paper_addresses(self):
        parts, texts, _ = census_merged('maths', 2014, 'hl', '230')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', None), ('6A', 'b', None),
            ('6B', 'a', None), ('6B', 'b', None), ('6B', 'c', None)})
        self.assertIn('similar', texts[('6A', 'a', None)])
        self.assertIn('construct', texts[('6A', 'b', None)])
        self.assertIn('Name two', texts[('6B', 'a', None)])
        self.assertIn('Prove', texts[('6B', 'b', None)])
        self.assertIn('Given', texts[('6B', 'c', None)])
        self.assertFalse(any(f['type'] == 'question-gap'
                             for f in continuity_flags(parts, texts)))
        a = parse_ref('2014 HL Paper 2 Q6A(a)')
        b = parse_ref('2014 HL Paper 2 Q6B(a)')
        self.assertEqual(a['q'], '6A')
        self.assertEqual(b['q'], '6B')
        self.assertEqual(a['paths'], [('a', None)])
        self.assertEqual(b['paths'], [('a', None)])

    def test_2011_ordinary_project_alternatives_retain_construction_axiom_and_proof(self):
        parts, texts, _ = census_merged('maths', 2011, 'ol', '230')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', None), ('6A', 'b', None), ('6B', None, None)})
        self.assertIn('centroid', texts[('6A', 'a', None)])
        self.assertIn('axiom', texts[('6A', 'b', None)])
        self.assertIn('DEFG', texts[('6B', None, None)])
        self.assertIn('cyclic', texts[('6B', None, None)])
        self.assertFalse(any(f['type'] == 'question-gap'
                             for f in continuity_flags(parts, texts)))

    def test_ordinary_alternative_keeps_the_unlettered_proof(self):
        parts, texts, _ = census_merged('maths', 2014, 'ol', '230')
        self.assertEqual({k for k in parts if str(k[0]).startswith('6')}, {
            ('6A', 'a', 'i'), ('6A', 'a', 'ii'), ('6A', 'b', None),
            ('6B', None, None)})
        self.assertIn('incircle', texts[('6A', 'a', 'i')])
        self.assertIn('radius', texts[('6A', 'a', 'ii')])
        self.assertIn('Prove', texts[('6B', None, None)])
        self.assertIn('tangent', texts[('6B', None, None)])
        self.assertFalse(any(f['type'] == 'question-gap'
                             for f in continuity_flags(parts, texts)))
        proof = parse_ref('2014 OL Paper 2 Q6B')
        self.assertEqual(proof['q'], '6B')
        self.assertEqual(proof['paths'], [(None, None)])

    def test_function_on_own_line_starts_a_maths_part(self):
        raw = '(b) List all the values.\n(c) g(x) is a function. Find g(x).'
        self.assertEqual(_split_own_line_markers(raw, maths=True), [
            '(b) List all the values.', '(c) g(x) is a function. Find g(x).'])
        self.assertEqual(len(_split_own_line_markers(raw)), 1)

    def test_inline_references_and_lowercase_prose_do_not_split(self):
        for raw in ['Use the answer to (c) g(x) above.',
                    'Explain how (i) health and wellbeing and\n(ii) responsible living influence choices.']:
            self.assertEqual(len(_split_own_line_markers(raw, maths=True)), 1)

    def test_2015_ordinary_paper_one_has_three_question_three_parts(self):
        paper = Paper('maths', 2015, 'ol', component='100')
        self.assertEqual({key for key in paper.parts if key[0] == 3},
                         {(3, 'a', None), (3, 'b', None), (3, 'c', None)})
        self.assertTrue(paper.parts[(3, 'c', None)][0].startswith('g(x) is a function'))
        self.assertNotIn('(c)', ' '.join(paper.parts[(3, 'b', None)]))


if __name__ == '__main__':
    unittest.main()
