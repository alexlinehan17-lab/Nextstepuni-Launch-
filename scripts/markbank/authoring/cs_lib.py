#!/usr/bin/env python3
"""Authoring for Construction Studies. Refuses rather than guesses.

A card here is one GROUP of a part: the scheme answers "draw a vertical section
through the external wall" with named sub-lists, and each is its own question a
student can be asked and its own tariff. See cs_scheme.py for why the group is
the unit.

The tariff is never invented. It comes from one of two places the scheme
actually prints, and if neither is there the part is left uncarded:

  * a group tariff — "5 x 4 marks" over "Foundation + Solid ground floor";
  * a part total plus an "any two" in the question — "(12 marks)" over three
    named options, which is 2 x 6, and the scheme prints the 6 as well so the
    derivation is checked rather than assumed.

Guessing a tariff has been the recurring error of this whole project, five times
over. There is no argument to this module that lets a caller supply one.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cs_scheme as CS                                       # noqa: E402
import paper as PP                                           # noqa: E402
from markbank_authoring import anyN, make_audit, make_card, make_emit  # noqa: E402

SUBJECT = 'construction-studies'
_card = make_card(SUBJECT, default_section='B')
audit = make_audit(40)
emit = make_emit(audit)

ANY_N = re.compile(r'\bany\s+(one|two|three|four|five|six)\b', re.I)
N_WORD = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}
TOTAL = re.compile(r'\(\s*(\d{1,3})\s*marks?\s*\)', re.I)
# A "point" that names nothing. The build refuses these anyway; catching them
# here says which scheme line is at fault instead of which card.
CONTENT_FREE = re.compile(
    r'^(any other relevant|any other valid|etc\.?|as above|any valid|'
    r'any correct|other relevant points?|alternative\b.{0,20})$', re.I)


class Refused(Exception):
    pass


def _squash(t):
    return re.sub(r'[^a-z0-9]+', '', (t or '').lower())


class Author:
    def __init__(self, year, level):
        self.year, self.level = year, level
        self.S = CS.Scheme(year, level)
        self.P = PP.Paper(SUBJECT, year, level)
        self.cards = []
        self._used = set()

    # ---- the paper side -------------------------------------------------
    def _paper_key(self, q, letter):
        for k in self.P.parts:
            if k[0] == q and k[1] == letter:
                return k
        return None

    def question(self, q, letter):
        k = self._paper_key(q, letter)
        return (self.P.text(*k) or '').strip() if k else ''

    def ref(self, q, letter):
        k = self._paper_key(q, letter)
        return self.P.ref(k) if k else f'{self.year} {self.level.upper()} Q{q}({letter})'

    # ---- the tariff -----------------------------------------------------
    def tariff(self, q, letter, name, n_items):
        """(claim, per) from what the scheme prints, or Refused."""
        for gname, t, _ in self.S.groups(q, letter):
            if t and (name is None or _squash(gname or '') == _squash(name)):
                return t
        block = ' '.join(self.S.marks.get((q, letter), []))
        # The commonest form by far, and the one groups() cannot reach: the
        # mark table prints "6 x 5 marks" as a line of its own, above rows that
        # carry no bullet character, so there is no group structure to hang it
        # on. Read straight off the part's mark block instead.
        #
        # Where the part prints SEVERAL group tariffs they belong to named
        # groups and groups() has already matched them by name; falling through
        # to here would take the first one for every group, so only an
        # unambiguous single tariff is used.
        direct = CS.GROUP_TARIFF.findall(block)
        if len(direct) == 1:
            return (int(direct[0][0]), int(direct[0][1]))
        tot = TOTAL.search(block)
        anyn = ANY_N.search(block) or ANY_N.search(self.question(q, letter))
        if tot and anyn:
            total, claim = int(tot.group(1)), N_WORD[anyn.group(1).lower()]
            if claim and total % claim == 0:
                per = total // claim
                # The scheme prints the per-option value too; require it to
                # agree rather than trusting the division on its own.
                if re.search(rf'\b{per}\b', block):
                    return (claim, per)
                raise Refused(f'Q{q}({letter}): {total}/{claim} = {per}, but the scheme '
                              f'never prints {per} — not carding a derived tariff')
        raise Refused(f'Q{q}({letter}) [{name}]: the scheme prints no tariff for this '
                      f'group; leave it uncarded rather than estimate one')

    # ---- the card -------------------------------------------------------
    def card(self, q, letter, name, *, cid, topic, concept, qtext, note='', notes='',
             stem='', claim=None):
        if cid in self._used:
            raise Refused(f'{cid}: already emitted')
        gs = [g for g in self.S.groups(q, letter, 'indicative')
              if name is None or _squash(g[0] or '') == _squash(name)]
        if not gs:
            have = [g[0] for g in self.S.groups(q, letter, 'indicative')]
            raise Refused(f'Q{q}({letter}): no group {name!r} in the scheme; it has {have}')
        _, _, items = gs[0]
        options = []
        for it in items:
            it = it.strip(' .;')
            if not it or CONTENT_FREE.match(it):
                continue
            if _squash(it) not in self.raw:
                raise Refused(f'Q{q}({letter}) [{name}]: {it[:60]!r} is not in the '
                              f'scheme text — the extraction changed it')
            options.append(it)
        if len(options) < 2:
            raise Refused(f'Q{q}({letter}) [{name}]: {len(options)} usable option(s)')
        n, per = self.tariff(q, letter, name, len(options))
        if claim is not None:
            n = claim
        if n > len(options):
            raise Refused(f'Q{q}({letter}) [{name}]: tariff claims {n} of only '
                          f'{len(options)} printed options')
        if not qtext:
            raise Refused(f'Q{q}({letter}): no question text')
        total = n * per
        row = anyN(f'{cid}-r1', options[0], total, n, per, options, note)
        self.cards.append(_card(
            cid, self.year, self.level, topic, concept, self.ref(q, letter),
            qtext, f'{n} x {per}', total, [row], notes, stem=stem,
            tariff_kind='bestNofParts'))
        self._used.add(cid)
        return self.cards[-1]

    @property
    def raw(self):
        if not hasattr(self, '_raw'):
            path = os.path.join(CS.SCHEMES, f'{self.year}-{self.level}.md')
            self._raw = _squash(open(path, errors='ignore').read())
        return self._raw

    def emit(self):
        emit(self.cards)


if __name__ == '__main__':
    # Probe: what could be carded, and what the scheme refuses to price.
    year, level = int(sys.argv[1]), sys.argv[2]
    A = Author(year, level)
    ok = refused = 0
    for (q, letter) in A.S.parts():
        for name, _, items in A.S.groups(q, letter, 'indicative'):
            if len(items) < 2:
                continue
            try:
                n, per = A.tariff(q, letter, name, len(items))
                print(f'  OK   Q{q}({letter}) [{(name or "-")[:44]:<44}] {n} x {per}'
                      f'  {len(items)} options')
                ok += 1
            except Refused as e:
                print(f'  --   {str(e)[:118]}')
                refused += 1
    print(f'\n{year} {level.upper()}: {ok} priceable, {refused} not priced by the scheme')
