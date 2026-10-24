"""Publication evidence must stay bound to the actual task and source."""
import copy
import unittest

from english_task_review import task_fingerprint, reconcile
from english_review_gate import check_visual


class EnglishTaskEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.record = {'id': 'english-2013-hl-p2',
                       'questionPaper': {'sha256': 'paper', 'pages': 2},
                       'markingScheme': {'sha256': 'scheme'}}
        self.task = {'id': 'english-2013-hl-p2-unseen-q1-a', 'paper': 2,
                     'questionText': 'Explain how this emotion is conveyed.',
                     'questionRef': 'Unseen Q1(a)', 'totalMarks': 10,
                     'topicId': 'english-8-0',
                     'sourceMaterial': {'pages': [2], 'title': 'The poem'}}
        self.entry = {'taskSha256': task_fingerprint(self.task), 'paperSha256': 'paper',
                      'schemeSha256': 'scheme', 'totalMarks': 10, 'schemePages': [3],
                      'criteria': {'mode': 'holistic'}, 'reason': 'Task and scheme checked.'}
        self.ledger = {'tasks': {self.task['id']: self.entry}}

    def test_source_context_and_tariff_changes_invalidate_review(self):
        self.assertEqual(reconcile([self.task], [self.record], self.ledger), [])
        for update in ({'totalMarks': 20}, {'parentQuestionText': 'A required shared stem'},
                       {'additionalSourceMaterials': [{'pages': [20], 'sourceYear': 2021}]},
                       {'sourceMaterial': {'pages': [1], 'title': 'Another poem'}}):
            with self.subTest(update=update), self.assertRaisesRegex(ValueError, 'Stale scheme task'):
                reconcile([{**self.task, **update}], [self.record], self.ledger)

    def test_orphaned_and_invented_allocations_fail(self):
        with self.assertRaisesRegex(ValueError, 'Orphaned'):
            reconcile([], [self.record], self.ledger)
        broken = copy.deepcopy(self.ledger)
        broken['tasks'][self.task['id']]['criteria']['allocation'] = {'P': 10}
        with self.assertRaisesRegex(ValueError, 'cannot invent'):
            reconcile([self.task], [self.record], broken)

    def test_missing_review_is_reported(self):
        self.assertEqual(reconcile([self.task], [self.record], {'tasks': {}}), [self.task['id']])

    def test_independent_visual_count_and_every_page_are_required(self):
        entry = {'paperId': self.record['id'], 'paperSha256': 'paper', 'schemeSha256': 'scheme',
                 'visualSweepComplete': True, 'paperPagesInspected': [1, 2],
                 'independentPaperTally': {'baseTasks': 1, 'finiteRoutes': 1, 'basis': 'Visual tally'},
                 'allTaskBoundariesSchemeChecked': True, 'allFiniteRoutesReconciled': True}
        self.assertEqual(check_visual([self.record], [self.task], [self.task], {'papers': [entry]}), [])
        entry['openFindings'] = ['Required poem reader unresolved']
        self.assertEqual(check_visual([self.record], [self.task], [self.task], {'papers': [entry]}),
                         [self.record['id'] + ': Required poem reader unresolved'])
        entry['openFindings'] = []
        entry['paperPagesInspected'] = [1]
        with self.assertRaisesRegex(ValueError, 'omits/repeats'):
            check_visual([self.record], [self.task], [self.task], {'papers': [entry]})
        entry['paperPagesInspected'] = [1, 2]
        entry['independentPaperTally']['finiteRoutes'] = 2
        with self.assertRaisesRegex(ValueError, 'tally differs'):
            check_visual([self.record], [self.task], [self.task], {'papers': [entry]})


if __name__ == '__main__':
    unittest.main()
