"""Regression checks for reviewed pools that the legacy English deck omitted."""
import json
from pathlib import Path
import unittest
from english_choices import expand, fingerprint, review, route_variants

ROOT = Path(__file__).resolve().parents[3]
DECISIONS = json.loads((ROOT / 'scripts/markbank/authored/english-selection-review.json').read_text())['decisions']

ADVICE_QUESTION = (
    'Based on your reading of the above written list, what two pieces of advice do you consider most valuable? '
    'Explain why you consider them to be the most valuable. What one piece of advice do you consider to be the '
    'least valuable? Explain why you consider it the least valuable.'
)


def fixture(id, question):
    return {'id': id, 'questionText': question, 'rawQuestionText': question,
            'questionRef': '2026 OL Paper 1 Text 3 A(i)', 'totalMarks': 15,
            'sourceMaterial': {'pages': [6, 7]}, 'schemePage': 11}


class EnglishChoiceRoutesTest(unittest.TestCase):
    def test_two_best_and_one_different_worst_is_360_not_120(self):
        id = 'english-2026-ol-p1-t3-a-i'
        task = fixture(id, ADVICE_QUESTION)
        card, = expand(task, DECISIONS[id])
        self.assertEqual(card['id'], id)
        self.assertEqual(card['printedChoice']['choices'], 360)
        routes = route_variants(task, DECISIONS[id], 'printedChoices')
        self.assertEqual(len(routes), 360)
        self.assertEqual(len({route['id'] for route in routes}), 360)
        self.assertIn(id + '-route-most-1-2--least-3', {route['id'] for route in routes})
        self.assertNotIn(id + '-route-most-1-2--least-1', {route['id'] for route in routes})
        for route in routes:
            selection = route['choiceRoute']['selections']
            self.assertEqual(len(selection['most']), 2)
            self.assertEqual(len(selection['least']), 1)
            self.assertFalse(set(selection['most']) & set(selection['least']))
            self.assertEqual(route['totalMarks'], 15)
            self.assertEqual(route['schemePage'], 11)
            self.assertEqual(route['sourceMaterial']['pages'], [6, 7])
            self.assertTrue(route['questionText'].startswith(ADVICE_QUESTION))
        self.assertEqual(task['questionText'], ADVICE_QUESTION)

    def test_actual_2025_twelve_quote_source_is_not_cut_to_ten(self):
        id = 'english-2025-ol-p1-t3-a-i'
        question = ('Based on your reading of TEXT 3, which three quotations, out of the ten, do you think have '
                    'the most important things to say about love? In each case, explain your answer with reference '
                    'to your chosen quotations.')
        self.assertEqual(expand(fixture(id, question), DECISIONS[id])[0]['printedChoice']['choices'], 220)
        routes = route_variants(fixture(id, question), DECISIONS[id], 'printedChoices')
        self.assertEqual(len(routes), 220)
        self.assertIn(id + '-route-selection-10-11-12', {route['id'] for route in routes})
        self.assertTrue(all(route['totalMarks'] == 15 for route in routes))

    def test_word_cloud_has_ten_distinct_three_word_combinations(self):
        id = 'english-2012-ol-p1-t3-a-i'
        question = ('Based on your reading of the above passage, choose three words from Image 1, each of which '
                    'you think describes a different aspect of the company, Google, or of its founders. '
                    'Explain each of your choices with evidence from the passage.')
        routes = route_variants(fixture(id, question), DECISIONS[id], 'printedChoices')
        self.assertEqual(len(routes), 10)
        self.assertEqual({tuple(route['choiceRoute']['selections']['selection']) for route in routes}, {
            ('1', '2', '3'), ('1', '2', '4'), ('1', '2', '5'), ('1', '3', '4'), ('1', '3', '5'),
            ('1', '4', '5'), ('2', '3', '4'), ('2', '3', '5'), ('2', '4', '5'), ('3', '4', '5'),
        })

    def test_rejects_stale_or_unclassified_and_orphaned_decisions(self):
        id = 'english-2026-ol-p1-t3-a-i'
        with self.assertRaisesRegex(ValueError, 'wording changed'):
            expand(fixture(id, ADVICE_QUESTION + ' Changed.'), DECISIONS[id])
        routes, missing = review([fixture(id, ADVICE_QUESTION)], {})
        self.assertEqual(routes, [])
        self.assertEqual(missing, [id])
        with self.assertRaisesRegex(ValueError, 'no longer have a task'):
            review([], {id: DECISIONS[id]})

    def test_flexible_number_of_words_remains_one_response(self):
        id = 'english-2025-ol-p1-t1-a-ii'
        question = ('Which of the following word or words would you use to describe the language used in this '
                    'article? • Humorous • Descriptive • Moving Give reasons for your answer, referring to the article.')
        task = fixture(id, question)
        self.assertEqual(DECISIONS[id]['kind'], 'flexible')
        self.assertEqual(expand(task, DECISIONS[id]), [task])


if __name__ == '__main__':
    unittest.main()
