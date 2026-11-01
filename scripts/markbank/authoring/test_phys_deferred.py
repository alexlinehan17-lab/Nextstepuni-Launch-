"""Regressions for same-year main/deferred SEC sources and inline asks."""
import copy
from pathlib import Path
from types import SimpleNamespace
import unittest

import phys_review_2022_hl_deferred as ledger
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


if __name__ == '__main__':
    unittest.main()
