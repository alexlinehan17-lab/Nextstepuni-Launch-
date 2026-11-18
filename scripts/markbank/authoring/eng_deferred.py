"""The SEC's deferred Engineering sittings, authored as sittings of their own.

The archive holds two (paper_census.ENG_DEFERRED_PAPERS): the 2022 and 2023
Higher papers sat by candidates who could not sit in June, each with its own
scheme, filed under deferredexams/ and deferredmarkingschemes/ with June's
file id (LC027ALP000EV). Paper Trail indexes each as its own entry,
"LC027ALP000EV-deferred".

A deferred sitting is read and carded exactly as a June one, through the same
Author and the same gates, from files named for it:

    examiner-reports/engineering/papers/<year>-<level>-deferred-paper.pdf
    examiner-reports/engineering/schemes/<year>-<level>-deferred.pdf / .md

(the PDFs are local copies of the archive's, as June's are; the .md is the
extraction the provenance gate reads). The sitting's level token is
"<level>-deferred", so the paper reader, the scheme readers, eng_lift and
eng_crops find those files by the names they already build, and every id the
author makes reads "eng-<year>-<level>-deferred-...", the form History and
Economics use. Each card's citation ends " — Deferred sitting", which
reconcile pairs with the id and matches only against the census's 'Deferred'
paper (paper_census.census_engineering_deferred).
"""
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)

from lib import Author                                     # noqa: E402

SUFFIX = '-deferred'
CITATION = ' — Deferred sitting'


def is_deferred(level):
    return str(level).endswith(SUFFIX)


def base_level(level):
    return level[:-len(SUFFIX)] if is_deferred(level) else level


class DeferredAuthor(Author):
    """lib.Author over one deferred sitting's own paper and scheme."""

    def __init__(self, year, level):
        if not is_deferred(level):
            raise ValueError(f'{year} {level}: not a deferred sitting')
        super().__init__('engineering', year, level)
        base = base_level(level)
        self.long_level = 'higher' if base == 'hl' else 'ordinary'
        self._june_ref = f'{year} {base.upper()} '
        self._token_ref = f'{year} {level.upper()} '

    def _cite(self, card):
        # lib.part_ref spells the level token out ("2022 HL-DEFERRED Q1(a)");
        # the citation names the June level and says which sitting it is.
        ref = card['questionRef']
        if ref.startswith(self._token_ref):
            ref = self._june_ref + ref[len(self._token_ref):]
        if not ref.endswith(CITATION):
            ref += CITATION
        card['questionRef'] = ref
        return card

    def card(self, *args, **kwargs):
        made = super().card(*args, **kwargs)
        return self._cite(made) if made is not None else made
