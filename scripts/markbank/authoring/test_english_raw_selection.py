"""A missing card must not make a source-paper choice disappear from the gate."""
from copy import deepcopy
import unittest

from english_choices import fingerprint, review
from english_raw_selection import hits_for_rows, reconcile, suggested_tasks


class RawPaperSelectionTest(unittest.TestCase):
    def setUp(self):
        self.paper = 'english-2026-ol-p1'
        self.records = [{'id': self.paper, 'questionPaper': {'sha256': 'source-hash'}}]
        self.hits = hits_for_rows(self.paper, 7, [
            {'text': 'Choose two of the four images below.', 'x': .1, 'y': .4},
            {'text': 'Explain both choices.', 'x': .1, 'y': .45},
        ])
        self.task = {'id': self.paper + '-t3-a-ii', 'questionText': self.hits[0]['text'],
                     'rawQuestionText': self.hits[0]['text'],
                     'paperRegion': [{'p': 7, 'r': [0, .3, 1, .6]}]}
        self.decision = {'kind': 'open', 'reason': 'Fixture only.',
                         'questionSha256': fingerprint(self.task['questionText'])}

    def ledger(self, kind='tasks'):
        hit = self.hits[0]
        entry = {key: hit[key] for key in ('textSha256', 'contextSha256')}
        entry.update({'kind': kind, 'reason': 'Exact directive covered by the reviewed image task.'})
        if kind == 'tasks':
            entry.update({'taskIds': [self.task['id']],
                          'taskSha256': {self.task['id']: fingerprint(self.task['questionText'])}})
        return {'sources': {self.paper: 'source-hash'}, 'decisions': {hit['id']: entry}}

    def test_raw_hit_survives_when_card_parser_drops_the_whole_task(self):
        self.assertEqual(suggested_tasks(self.hits[0], []), [])
        missing, pending = reconcile(self.hits, self.records, {}, [], {})
        self.assertEqual(missing, [self.hits[0]['id']])
        self.assertEqual(pending, [])
        with self.assertRaisesRegex(ValueError, 'absent/wrong-paper'):
            reconcile(self.hits, self.records, self.ledger(), [], {})

    def test_numbered_pool_without_choose_still_requires_review(self):
        wording = 'Discuss this view with reference to two of the above characters.'
        hits = hits_for_rows('english-2015-hl-p2', 3, [
            {'text': wording, 'x': .1, 'y': .4}])
        self.assertEqual(len(hits), 1)
        task = {**self.task, 'questionText': wording, 'rawQuestionText': wording}
        routes, pending = review([task], {})
        self.assertEqual((routes, pending), ([], [task['id']]))
        for number in ('three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', '2'):
            self.assertEqual(len(hits_for_rows(self.paper, 1, [
                {'text': f'Refer to {number} of these examples.', 'x': .1, 'y': .2}])), 1)

    def test_covered_raw_line_still_requires_task_level_choice_review(self):
        self.assertEqual(suggested_tasks(self.hits[0], [self.task]), [self.task['id']])
        missing, pending = reconcile(self.hits, self.records, self.ledger(), [self.task], {})
        self.assertEqual(missing, [])
        self.assertEqual(pending, [self.task['id']])
        self.assertEqual(reconcile(self.hits, self.records, self.ledger(), [self.task],
                                  {self.task['id']: self.decision}), ([], []))

    def test_source_context_and_task_changes_invalidate_review(self):
        ledger = self.ledger()
        ledger['sources'][self.paper] = 'changed'
        with self.assertRaisesRegex(ValueError, 'stale source'):
            reconcile(self.hits, self.records, ledger, [self.task], {})
        changed = deepcopy(self.hits)
        changed[0]['contextSha256'] = 'different-context'
        with self.assertRaisesRegex(ValueError, 'wording/context changed'):
            reconcile(changed, self.records, self.ledger(), [self.task], {})
        changed_task = {**self.task, 'questionText': 'Choose one image.'}
        with self.assertRaisesRegex(ValueError, 'task wording changed'):
            reconcile(self.hits, self.records, self.ledger(), [changed_task], {})

    def test_orphaned_decisions_and_unexplained_exclusions_fail(self):
        with self.assertRaisesRegex(ValueError, 'no longer match'):
            reconcile([], self.records, self.ledger(), [], {})
        ledger = self.ledger('source-prose')
        ledger['decisions'][self.hits[0]['id']]['reason'] = ''
        with self.assertRaisesRegex(ValueError, 'no written reason'):
            reconcile(self.hits, self.records, ledger, [], {})


if __name__ == '__main__':
    unittest.main()
