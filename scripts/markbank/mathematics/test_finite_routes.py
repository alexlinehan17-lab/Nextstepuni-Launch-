"""One printed choice stays one complete task, with source and tariff guards."""
import copy,json,unittest
from pathlib import Path
from audit import SELECTION, logical_tasks, validate_review_sources, CHOICE_POLICY

class PrintedChoiceTest(unittest.TestCase):
    def review(self, name):
        return json.loads((Path(__file__).parent/'reviews'/name).read_text())

    def test_numbered_exam_instructions_are_scanned_without_numeric_answer_false_positives(self):
        for text in ['Attempt SIX QUESTIONS (50 marks each).', 'Answer six questions from this section.', 'Answer 2 of the 5 questions.']:
            self.assertIsNotNone(SELECTION.search(text), text)
        for text in ['Subtract 3 from your answer 20 − 3', 'Add 12 to your answer 30 + 12']:
            self.assertIsNone(SELECTION.search(text), text)

    def test_unclassified_raw_selection_blocks_publication(self):
        review=self.review('2012-higher-p1.json')
        self.assertEqual(validate_review_sources([review]),[])
        review['selectionDecisions']={}
        self.assertTrue(any('unclassified' in error for error in validate_review_sources([review])))

    def test_all_thirteen_choices_keep_their_printed_marks_and_original_sources(self):
        self.assertEqual(len(CHOICE_POLICY),13)
        for policy in CHOICE_POLICY:
            with self.subTest(card=policy['canonicalId']):
                review=self.review(policy['reviewFile'])
                tasks=logical_tasks(review)
                self.assertEqual(sum(c['totalMarks'] for c in tasks),sum(review['printedQuestionMarks'].values()))
                self.assertEqual(validate_review_sources([review]),[])
                choice=next(c for c in tasks if c['id']==policy['canonicalId'])
                self.assertNotIn('selectionVariant',choice)
                self.assertEqual(choice['selectionChoice']['pool'],policy['selectionChoice']['pool'])
                self.assertNotIn('For this practice',choice['questionText'])

    def test_missing_card_duplicate_card_and_resurrected_combination_are_rejected(self):
        for policy in CHOICE_POLICY:
            review=self.review(policy['reviewFile']);first=next(c for c in review['cards'] if c['id']==policy['canonicalId'])
            missing=copy.deepcopy(review);missing['cards']=[c for c in missing['cards'] if c['id']!=first['id']]
            with self.assertRaisesRegex(ValueError,'missing or expanded'):logical_tasks(missing)
            duplicate=copy.deepcopy(review);duplicate['cards'].append(copy.deepcopy(first))
            with self.assertRaisesRegex(ValueError,'duplicate'):logical_tasks(duplicate)
            resurrected=copy.deepcopy(review);resurrected['cards'].append(copy.deepcopy(policy['legacyCards'][1]))
            with self.assertRaisesRegex(ValueError,'expanded'):logical_tasks(resurrected)

    def test_tariff_options_directive_and_prompt_are_protected(self):
        policy=CHOICE_POLICY[0]
        for field in ['totalMarks','pool','sourceDirective','questionText']:
            review=self.review(policy['reviewFile']);card=next(c for c in review['cards'] if c['id']==policy['canonicalId'])
            if field=='totalMarks':card[field]+=5
            elif field=='pool':card['selectionChoice'][field]=card['selectionChoice'][field][:-1]
            elif field=='sourceDirective':card['selectionChoice'][field]='Choose an invented option'
            else:card[field]='Use only the first option.'
            with self.assertRaises(ValueError):logical_tasks(review)

if __name__=='__main__':unittest.main()
