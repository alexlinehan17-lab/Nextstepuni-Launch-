"""Regressions for same-year main/deferred SEC sources and inline asks."""
import copy
from pathlib import Path
from types import SimpleNamespace
import unittest

import phys_review_2022_hl_deferred as ledger
import phys_review_2023_hl_deferred as ledger23
import phys_review as review
import phys_sources as sources
from paper_census import census_merged, census_physics_deferred, leaves_of

ROOT = Path(__file__).resolve().parents[3]


class PhysicsDeferredTest(unittest.TestCase):
    def test_same_basename_resolves_to_deferred_archives_only(self):
        for kind, folder in [('paper', 'deferredexams'), ('scheme', 'deferredmarkingschemes')]:
            self.assertEqual(Path(sources.source_path(ROOT, ledger, kind)).resolve(),
                             (ROOT / 'paper-trail-corpus' / folder / '2022' / 'LC021ALP000EV.pdf').resolve())
            self.assertEqual(sources.indexed_fileid(ledger, kind), 'LC021ALP000EV-deferred.pdf')

    def test_main_pdf_with_matching_year_and_basename_is_rejected(self):
        for kind, folder in [('paper', 'exampapers'), ('scheme', 'markingschemes')]:
            wrong = SimpleNamespace(SITTING='deferred', YEAR=2022, LEVEL='hl',
                                    SOURCES=copy.deepcopy(ledger.SOURCES))
            wrong.SOURCES[kind]['path'] = f'paper-trail-corpus/{folder}/2022/LC021ALP000EV.pdf'
            with self.assertRaisesRegex(ValueError, 'outside its SEC archive'):
                sources.source_path(ROOT, wrong, kind)

    def test_level_mismatch_is_rejected_even_in_correct_archive(self):
        wrong = SimpleNamespace(SITTING='deferred', YEAR=2022, LEVEL='ol', SOURCES=ledger.SOURCES)
        with self.assertRaisesRegex(ValueError, 'wrong level or edition'):
            sources.source_path(ROOT, wrong, 'paper')

    def test_rewriting_main_or_deferred_never_owns_the_other_sitting(self):
        main = SimpleNamespace(SITTING='main')
        for family in ['phys', 'physics']:
            for actual in ['main', 'deferred']:
                identifier = f'{family}-2022-hl-' + ('deferred-' if actual == 'deferred' else '') + 'q1-i'
                self.assertEqual(sources.owns(identifier, main, 2022, 'hl', family), actual == 'main')
                self.assertEqual(sources.owns(identifier, ledger, 2022, 'hl', family), actual == 'deferred')

    def test_original_pdf_keeps_every_independently_numbered_inline_ask(self):
        parts, _, _ = census_merged('physics', 2022, 'hl',
                                   files=[sources.source_path(ROOT, ledger, 'paper')])
        leaves = set(leaves_of(parts))
        self.assertEqual(len(leaves), 130)
        expected = [(4,None,'iii'), (4,None,'iv'), (7,None,'i'), (7,None,'ii'),
                    (10,'b','iv'), (10,'b','v'), (11,None,'i'), (11,None,'ii'),
                    (12,'b','vi'), (12,'b','vii'), (14,'a','iv'), (14,'a','v'),
                    *[(14,'c',r) for r in ['iii','iv','vi','vii','viii','ix']]]
        for key in expected:
            self.assertIn(key, leaves)

    def test_deferred_continuity_checks_run_without_main_sitting_waivers(self):
        paper = next(p for p in census_physics_deferred() if p['year'] == 2022)
        self.assertEqual(paper['leafCount'], 130)
        self.assertEqual(paper['paper'], 'Deferred')
        self.assertEqual(paper['flags'], [])


class Physics2023DeferredTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.cards, cls.tasks, cls.checks = review.build(ledger23, 2023, 'hl')
        cls.by_id = {c['id']: c for c in cls.cards}

    def mutated_ledger(self):
        return SimpleNamespace(**{k: copy.deepcopy(v) for k, v in vars(ledger23).items() if k.isupper()})

    def test_nested_hadron_parts_do_not_steal_the_electronics_option(self):
        parts, texts, _ = census_merged('physics', 2023, 'hl',
                                       files=[sources.source_path(ROOT, ledger23, 'paper')])
        for roman in ['vi', 'vii', 'viii', 'ix']:
            self.assertIn((12, 'a', roman), leaves_of(parts))
        self.assertIn('What charge does this kaon have?', texts[(12, 'a', 'vii')])
        self.assertIn('tangential velocity', texts[(12, 'a', 'viii')])
        self.assertNotIn('tangential velocity', texts[(12, 'b', 'viii')])
        self.assertIn('NOT gate', texts[(12, 'b', 'viii')])

    def test_shared_electronics_tariffs_stay_unpriced_and_cover_disjoint_parts(self):
        tasks = [t for t in self.tasks if t.get('sharedParts')]
        self.assertEqual([t['total'] for t in tasks], [12, 16, 15, 13])
        self.assertEqual([r for t in tasks for r in t['sharedParts']['romans']],
                         ['i','ii','iii','iv','v','vi','vii','viii','ix'])
        for t in tasks:
            card = self.by_id[t['id']]
            self.assertEqual(card['tariffModel'], {'kind':'questionTotal'})
            self.assertTrue(all(r['marks'] is None for r in card['rows']))
            self.assertEqual(t['cells']['sum'], card['totalMarks'])

    def test_shared_group_cannot_claim_a_sibling_or_skip_a_printed_part(self):
        for romans, message in [(['i'], 'has no task'), (['i','ii','iii'], 'groups overlap')]:
            bad = self.mutated_ledger()
            bad.WHOLE_GROUPS['q12b-i-ii']['romans'] = romans
            with self.assertRaisesRegex(review.Refusal, message):
                review.build(bad, 2023, 'hl')

    def test_supplementary_equation_does_not_hide_its_question_or_stem(self):
        card = self.by_id['phys-2023-hl-deferred-q11-iv']
        self.assertFalse(card['questionFigureIncludesPrompt'])
        self.assertIn('fusion reactions', card['stem'])
        self.assertIn('Calculate the energy', card['questionText'])
        bad = self.mutated_ledger()
        next(t for t in bad.TASKS if t['key']=='q11iv')['qfig_prompt'] = True
        with self.assertRaisesRegex(review.Refusal, 'does not print the ask'):
            review.build(bad, 2023, 'hl')

    def test_internal_slashes_do_not_create_spurious_answer_slots(self):
        for key, intact in [('q3-vi','measure to/from centre of the lens'),
                            ('q5-vi','reverse the diode/battery connections')]:
            row = self.by_id['phys-2023-hl-deferred-'+key]['rows'][0]
            self.assertEqual(row['group']['claimMax'], 2)
            self.assertEqual(len(row['group']['options']), 3)
            self.assertIn(intact, row['group']['options'])


if __name__ == '__main__':
    unittest.main()
