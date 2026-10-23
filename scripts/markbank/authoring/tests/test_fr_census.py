"""A scheme text companion must not turn an unsupported layout into zero asks."""
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paper_census import census_lang
from fr_scheme import FrScheme
from fr_paper import FrPaper
from fr_pdf_words import fragmented_words
from fr_legacy_reading import normalize_ordinary, apply_reviewed_blocks


class FrenchCensusLayoutTest(unittest.TestCase):
    def test_overlapping_tiles_remove_repeated_glyphs_without_collapsing_double_letters(self):
        def glyph(char, x):
            return {'c': char, 'origin': (x, 10), 'bbox': (x, 0, x + 5, 12)}
        # The N at x15 repeats across tiles. The N at x20 is a real second N.
        first = [glyph(c, i * 5) for i, c in enumerate('ROIN')]
        second = [glyph(c, 15 + i * 5) for i, c in enumerate('NN I')]
        page = SimpleNamespace(get_text=lambda _: {'blocks': [{'lines': [
            {'spans': [{'chars': first}]}, {'spans': [{'chars': second}]},
        ]}]})
        self.assertEqual([word[4] for word in fragmented_words(page)], ['ROINN', 'I'])

    def test_short_french_question_keeps_its_reference_across_the_column_bound(self):
        rows = [(0, [(40, 'L', 'SECTION I: COMPRÉHENSION ÉCRITE')]),
                (1, [(40, 'L', 'Q.4')]),
                (1, [(40, 'L', '2.'), (70, 'L', 'Comment sont ses résultats ?'), (305, 'R', '(Section 1)')]),
                (1, [(240, 'L', 'Lch. 8 de 16 / Page 8 of 16')])]
        with patch.object(FrPaper, '_written_path', return_value='paper.pdf'), \
             patch.object(FrPaper, '_aural_path', return_value=None), \
             patch.object(FrPaper, '_width', return_value=595), \
             patch('fr_paper._rows', return_value=rows):
            paper = FrPaper(2012, 'ol')
        self.assertEqual(paper.candidates(4, 2, None)[0].text, 'Comment sont ses résultats ? (Section 1)')

    def aural(self, lines):
        paper = FrPaper.__new__(FrPaper)
        paper.aural_path = 'listening.pdf'
        rows = [(1, [(320, 'R', line)]) for line in lines]
        with patch('fr_paper._rows', return_value=rows):
            return paper.aural_asks()

    def test_roman_listening_sections_keep_response_slots_and_choices_inside_the_ask(self):
        asks = self.aural([
            'SECTION II', '1. Name two activities.', '(a)', '(b)',
            '2. (i) What does she do?', '(ii) Why?',
            'SECTION IV', '1. Choose one answer.', '(a) First', '(b) Second', '(c) Third', '(d) Fourth',
            'SECTION V', '1. What happened?', 'END', '2. Copyright material',
        ])
        self.assertEqual([(s, q, part) for s, q, part, _ in asks], [
            ('II', 1, None), ('II', 2, 'i'), ('II', 2, 'ii'), ('IV', 1, None), ('V', 1, None),
        ])
        self.assertIn('(a) (b)', asks[0][3])
        self.assertIn('(d) Fourth', asks[3][3])

    def test_modern_listening_lettered_parts_remain_independent(self):
        asks = self.aural(['SECTION A', '1. (a) Who?', '(b) Where?', 'SECTION E', '1. What?'])
        self.assertEqual([(s, q, part) for s, q, part, _ in asks], [
            ('A', 1, 'a'), ('A', 1, 'b'), ('E', 1, None),
        ])

    def test_census_keeps_the_printed_roman_section_reference(self):
        scheme = SimpleNamespace(rc_totals={1: 5, 2: 5}, reading=lambda: [
            SimpleNamespace(rc=rc, item=1, letter=None, letter_to=None, cue='Printed task') for rc in [1, 2]
        ])
        paper = SimpleNamespace(path='written.pdf', aural_path='aural.pdf',
            find=lambda *args: ('Printed task', 1, 1.0), section_b_asks=lambda: [],
            aural_asks=lambda: [('II', 2, 'i', 'Older ask'), ('A', 1, 'a', 'Modern ask')])
        with patch('fr_scheme.FrScheme', return_value=scheme), patch('fr_paper.FrPaper', return_value=paper):
            parts, *_ = census_lang('french', 2019, 'hl')
        self.assertIn(('II', 2, 'i', None), parts)
        self.assertIn(('LA', 1, 'a', None), parts)

    def census(self, headings, comprehensions):
        asks = [SimpleNamespace(rc=rc, item=1, letter=None, letter_to=None, cue='Printed task')
                for rc in comprehensions]
        scheme = SimpleNamespace(rc_totals=headings, reading=lambda: asks)
        paper = SimpleNamespace(
            path='written.pdf', aural_path=None,
            find=lambda *args: ('Printed task', 1, 1.0),
            section_b_asks=lambda: [], aural_asks=lambda: [],
        )
        with patch('fr_scheme.FrScheme', return_value=scheme), patch('fr_paper.FrPaper', return_value=paper):
            return census_lang('french', 2010, 'hl')

    def test_indented_scheme_keeps_its_priced_tasks(self):
        scheme = FrScheme(2020, 'hl', raw_text="""
            SECTION A COMPRÉHENSION ÉCRITE (10 marks)
            Q.1 (5 marks)
            1. (a) ........................ 5 Marks
            Où se passe la scène ?
            • Dans une maison .................... 5 Marks
            Q.2 (5 marks)
            1. (a) ........................ 5 Marks
            Quel jour est-ce ?
            • Dimanche .................... 5 Marks
            SECTION B PRODUCTION ÉCRITE
        """)
        self.assertEqual(scheme.rc_totals, {1: 5, 2: 5})
        self.assertEqual([(ask.rc, ask.total, ask.fault) for ask in scheme.reading()],
                         [(1, 5, None), (2, 5, None)])

    def test_legacy_ordinary_inherits_full_rate_without_promoting_partial_rungs(self):
        scheme = FrScheme(2019, 'ol', raw_text="""
            Section I (24 marks)
            Question 1 – 24 marks
            1.
            (a) - First ................................ 4 marks
            (b) - Second ............................... 4 marks
            (c) - Third ................................ 4 marks
            (d) - Fourth ............................... 4 marks
            2. (i) & (ii) Accept any two of the following: ........ 4+4 marks
            - Complete answer
            - Another complete answer
            \uf02a Partial answer ........................... 2 marks
            Section II (60 marks)
            Listening Comprehension (100 marks)
            Section I (16 marks)
            1. Someone
        """)
        match, pair = scheme.reading()
        self.assertEqual((match.letter, match.letter_to, match.total), ('a', 'd', 16))
        self.assertEqual((pair.total, pair.per, pair.count, pair.fault), (8, 4, 2, None))
        self.assertEqual([answer['marks'] for answer in pair.answers], [4, 4, 2])

    def test_roman_parts_keep_the_two_people_question_separate_from_two_required_reasons(self):
        scheme = FrScheme(2019, 'hl', raw_text="""
            SECTION I COMPRÉHENSION ÉCRITE
            Q.2 (15 marks)
            3.(ii) ...................... 5 Marks
            Donnez deux raisons pour son départ.
            Two of:
            • Une raison ................ 5 Marks
            • Une autre raison .......... 5 Marks
            4. .......................... 5 Marks
            Que font les deux hommes ?
            • Ils partent ............... 5 Marks
            SECTION II PRODUCTION ÉCRITE
        """)
        pair, people = scheme.reading()
        self.assertEqual(pair.letter, 'ii')
        self.assertIn('demands more than one answer', pair.fault)
        self.assertIsNone(people.fault)

    def test_reviewed_country_split_preserves_shared_rungs_and_the_next_page_boundary(self):
        body = ['- Japan qualities 4 marks', '- France qualities 4 marks', '* 2 qualities 2 marks', '* 1 quality 1 mark']
        split = {'A3-Q5': {
            'reason': 'Separate country responses are separately priced.',
            'sourceLines': body,
            'parts': [{'letter': 'i', 'answerLine': 0}, {'letter': 'ii', 'answerLine': 1}],
            'sharedRungs': [2, 3],
        }}
        lines = ['Section I (40 marks)', 'Question 3 – 40 marks', '## Page 8',
                 '5. ' + body[0], *body[1:], '6', '## Page 9', '6. - Next answer 4 marks', 'Section II (60 marks)']
        normalized = normalize_ordinary(lines, split)
        self.assertIn('5.(i) ........ 4 Marks', normalized)
        self.assertIn('5.(ii) ........ 4 Marks', normalized)
        self.assertEqual(normalized.count('– 2 qualities 2 marks'), 2)
        self.assertEqual(normalized.count('– 1 quality 1 mark'), 2)
        self.assertLess(normalized.index('## Page 9'), normalized.index('6. ........ 4 Marks'))
        changed = [line.replace('France qualities', 'Changed answer') for line in lines]
        with self.assertRaises(AssertionError):
            normalize_ordinary(changed, split)

    def test_unassigned_instrument_pair_keeps_both_four_mark_answers_and_partials(self):
        body = ['(i) - Violin 4 marks', '* du violon 3 marks', '(ii) - Flute 4 marks', '* de la flute 3 marks']
        combined = {'A3-Q1': {'sourceLines': body, 'marks': [4, 4], 'reason': 'Two unnamed answer slots, one distinct pair.'}}
        source = ['Section I (40 marks)', 'Question 3 – 40 marks', '1. ' + body[0], *body[1:], 'Section II (60 marks)']
        normalized = normalize_ordinary(source, combined_parts=combined)
        self.assertIn('1. ........ 4+4 Marks', normalized)
        self.assertIn('• Violin 4 marks', normalized)
        self.assertIn('• Flute 4 marks', normalized)
        self.assertIn('– du violon 3 marks', normalized)
        changed = [line.replace('Flute 4', 'Flute 3') for line in source]
        with self.assertRaises(AssertionError):
            normalize_ordinary(changed, combined_parts=combined)

    def test_shared_tariff_span_rejects_changed_source_and_retains_both_question_keys(self):
        source = ['Question 1 – 40 marks', 'Shared section 8 marks', '2. - First answer', '3. - Second answer']
        replacement = ['Question 1 – 40 marks', '2. ........ 8 marks', 'Question 2:', '- First answer', 'Question 3:', '- Second answer']
        blocks = [{'address': 'A1', 'sourceLines': source, 'replacementLines': replacement, 'reason': 'Published seven plus one joint tariff.'}]
        output = normalize_ordinary(apply_reviewed_blocks(['## Page 4', *source, '## Page 5'], blocks))
        self.assertIn('Question 2:', output)
        self.assertIn('Question 3:', output)
        self.assertEqual(output[0], '## Page 4')
        self.assertEqual(output[-1], '## Page 5')
        with self.assertRaises(AssertionError):
            apply_reviewed_blocks([line.replace('Second answer', 'Changed answer') for line in source], blocks)

    def test_reviewed_x_bullet_encoding_does_not_promote_partial_answers(self):
        scheme = FrScheme(2014, 'hl', raw_text='''
            Section I COMPRÉHENSION ÉCRITE
            Q.1 (5 marks)
            1.(i) ........ 5 Marks
            Quel temps fait-il ?
            x Il pleut ........ 5 Marks
            - Pluie ........ 4 Marks
            Section II PRODUCTION ÉCRITE
        ''')
        ask = scheme.reading()[0]
        self.assertIsNone(ask.fault)
        self.assertEqual((ask.total, ask.per), (5, 5))
        self.assertEqual([(answer['text'], answer['marks']) for answer in ask.answers], [('Il pleut', 5), ('Pluie', 4)])

    def test_unrecognized_roman_scheme_is_not_an_empty_success(self):
        with self.assertRaisesRegex(ValueError, 'unsupported or incomplete reading-scheme layout'):
            self.census({}, [])

    def test_missing_comprehension_is_not_a_partial_success(self):
        with self.assertRaisesRegex(ValueError, 'priced tasks \\[1\\]'):
            self.census({1: 60, 2: 60}, [1])

    def test_recognized_comprehensions_still_reach_the_paper_census(self):
        parts, texts, *_ = self.census({1: 60, 2: 60}, [1, 2])
        self.assertEqual(parts, {('A1', 1, None, None), ('A2', 1, None, None)})
        self.assertEqual(set(texts.values()), {'Printed task'})


if __name__ == '__main__':
    unittest.main()
