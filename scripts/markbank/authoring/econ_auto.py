"""Author an Economics paper against the extracted parts rather than raw text.

A card is four lines here instead of twelve, because the tariff, the response
headings and the option text all come from `econ_parts`, which reads them off
the scheme. What is left for a person is the half a machine cannot do: which
topic the part belongs to, how the question should read, and whether the part is
a menu at all.

    P = Paper(2021, 'higher')
    P.menu('positive impacts and two negative',
           'econ-2021-hl-q12-a-ii', 'economics-4-1', 'impacts-of-globalisation',
           'Outline two positive impacts of globalisation.',
           'A positive impact — any two',
           drop=('Suggested responses', 'Negative impacts'))
    P.emit()

`find()` refuses a key that matches no part or more than one, so a card can
never be built against a part other than the one intended — the same reasoning
as block()'s ambiguous-anchor guard.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, card, emit  # noqa: E402
from econ_parts import parts  # noqa: E402


class Paper:
    def __init__(self, year, level):
        self.year, self.level = year, level
        self.parts = parts(year, level)
        self.cards = []

    def find(self, key):
        hits = [p for p in self.parts if key in p['question']]
        if not hits:
            raise ValueError(f'{self.year} {self.level}: no part matching {key!r}')
        if len(hits) > 1:
            raise ValueError(
                f'{self.year} {self.level}: {len(hits)} parts match {key!r} — lengthen it:\n' +
                '\n'.join('    ' + h['question'][:90] for h in hits))
        return hits[0]

    def menu(self, key, cid, topic, concept, qtext, verbatim, note='',
             *, ref=None, drop=(), stop=None, claim=None, per=None, steps=None,
             notes='', stem='', cap=14):
        """One card from one part.

        `drop` removes an option containing any of these strings — the scheme's
        own scaffolding ("Suggested responses:") and, where one part answers two
        opposite questions, the half this card is not about. `stop` ends the list
        at the first option containing it, for the same reason.
        """
        p = self.find(key)
        opts = [o for o in p['options'] if o and not any(d in o for d in drop)]
        if stop:
            for i, o in enumerate(opts):
                if stop in o:
                    opts = opts[:i]
                    break
        opts = opts[:cap]
        n = claim if claim is not None else p['claim']
        m = per if per is not None else p['per']
        st = steps if steps is not None else p['steps']
        if n is None or m is None:
            raise ValueError(f'{cid}: no menu tariff on this part ({p["cells"]}) — pass claim/per')
        if len(opts) < n:
            raise ValueError(f'{cid}: {len(opts)} option(s) for a claim of {n}')
        total = sum(st[:n]) if st else n * m
        self.cards.append(card(
            cid, self.year, self.level, topic, concept,
            ref or self._ref(cid), qtext,
            '+'.join(f'1 @ {x}' for x in st) if st else f'{n} @ {m}', total,
            [anyN('r-1', verbatim, None if st else total, n, m, opts, note, steps=st)],
            notes, stem=stem, tariff_kind='fixed' if st else 'bestNofParts'))
        return self.cards[-1]

    def _ref(self, cid):
        """`econ-2021-hl-q12-a-ii` -> `2021 HL Q12(a)(ii)`."""
        bits = cid.split('-')
        q = bits[3][1:]
        parts_ = bits[4:]
        return (f'{self.year} {"HL" if self.level == "higher" else "OL"} '
                f'Q{q}' + ''.join(f'({x})' for x in parts_))

    def emit(self):
        emit(self.cards)
