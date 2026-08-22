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
from econ_refcheck import Paper as PaperText  # noqa: E402


class Paper:
    def __init__(self, year, level, section='B'):
        self.year, self.level = year, level
        self.section = section
        self.parts = parts(year, level, section)
        self.cards = []
        self._paper = None

    def cite(self, part):
        """The reference the QUESTION PAPER gives this part, or '' if unplaced.

        The scheme cannot be trusted for this. It is a table flattened into one
        line, so a question number printed at the foot of a page comes back as
        more parts of the question before it — which is how nineteen shipped
        Section B cards came to cite a question they were not from. The paper
        heads each question on its own line and every page after it belongs to
        that question, so the paper is where a citation should come from.

        Printed by worklist() for the author to copy into the script by hand.
        econ_refcheck.py then derives it again from the paper and compares, so a
        part read off the wrong line of the worklist is still caught.
        """
        if self._paper is None:
            self._paper = PaperText(self.year, 'hl' if self.level == 'higher' else 'ol')
        at = self._paper.locate(part['question'])
        if at < 0:
            return ''
        q = self._paper.question_at(at)
        lvl = 'HL' if self.level == 'higher' else 'OL'
        sect = ' Section A' if self.section == 'A' else ''
        return f'{self.year} {lvl}{sect} Q{q}{self._paper.path_at(q, at)}'

    def find(self, key):
        """The one part this key names, by its question or by one of its options.

        A part whose mark cell is printed halfway down its response list has no
        question left in the extractor's output — everything above the cell is
        read as the question, so the head is the bare "(b)" and the responses
        above it are gone. Those parts are still worth carding, so a key that
        matches no question is tried against the options, where the guard
        against an ambiguous key still applies.
        """
        hits = [p for p in self.parts if key in p['question']]
        if not hits:
            hits = [p for p in self.parts if any(key in o for o in p['options'])]
        if not hits:
            raise ValueError(f'{self.year} {self.level}: no part matching {key!r}')
        if len(hits) > 1:
            raise ValueError(
                f'{self.year} {self.level}: {len(hits)} parts match {key!r} — lengthen it:\n' +
                '\n'.join('    ' + h['question'][:90] for h in hits))
        return hits[0]

    def menu(self, key, cid, topic, concept, qtext, verbatim, note='',
             *, ref=None, drop=(), stop=None, after=None, claim=None, per=None, steps=None,
             notes='', stem='', cap=None, trim=None):
        """One card from one part.

        `drop` removes an option containing any of these strings — the scheme's
        own scaffolding ("Suggested responses:") and, where one part answers two
        opposite questions, the half this card is not about. `stop` ends the list
        at the first option containing it, for the same reason, and `after`
        begins it at the first option containing it — which is how the second
        half of a two-sided part is taken without naming every response in the
        first half.

        `trim` cuts each option at a string. Where the two halves of a two-sided
        part are headed rather than bulleted — "AGREE:" … "DISAGREE:" — the
        heading is not a response and so arrives glued to the end of the last
        response above it; trimming there keeps that response instead of losing
        it to `stop`. A trimmed option is still a contiguous run of the scheme,
        so it still traces.
        """
        p = self.find(key)
        opts = [o for o in p['options'] if o and not any(d in o for d in drop)]
        if trim:
            opts = [o.split(trim)[0].strip().rstrip('.,;:–-').strip() for o in opts]
            opts = [o for o in opts if len(o) >= 25]
        if after:
            for i, o in enumerate(opts):
                if after in o:
                    opts = opts[i:]
                    break
        if stop:
            for i, o in enumerate(opts):
                if stop in o:
                    opts = opts[:i]
                    break
        # Section A is short-answer, and its option cap is lower for that
        # reason — optionCapFor('A') is 8 where 'B' is 14.
        opts = opts[:cap if cap is not None else (8 if self.section == 'A' else 14)]
        # A descending tariff states its own claim: "the first 4, the second 3"
        # is two responses. Taking the claim from the part instead would read
        # the single cell the extractor found beside it and ask for one.
        n = claim if claim is not None else len(steps) if steps else p['claim']
        m = per if per is not None else p['per']
        st = steps if steps is not None else p['steps']
        # A part's descending tariff belongs to the part, not to a card that
        # takes half of it. Where one part answers two questions — a private
        # cost paid 8 and a social cost paid 4 — each card claims one response,
        # and carrying the part's two steps onto a claim of one is the tariff of
        # neither side.
        if steps is None and claim is not None and st and len(st) != claim:
            st = None
        # With a descending tariff the per-option rate is the first step, which
        # is what the shipped stepped cards carry: perOption 8, steps [8, 4].
        if st and m is None:
            m = st[0]
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
            notes, stem=stem, section=self.section,
            tariff_kind='fixed' if st else 'bestNofParts'))
        return self.cards[-1]

    def _ref(self, cid):
        """`econ-2021-hl-q12-a-ii` -> `2021 HL Q12(a)(ii)`.

        Section A repeats the numbers 1-10 that Section B does not use, so a
        Section A card marks itself `-sa-` and the reference says which section
        it came from — otherwise "2021 HL Q1(b)" is ambiguous across the paper.
        """
        bits = cid.split('-')
        i = 4 if bits[3] == 'sa' else 3
        q = bits[i][1:]
        parts_ = bits[i + 1:]
        return (f'{self.year} {"HL" if self.level == "higher" else "OL"}'
                f'{" Section A" if bits[3] == "sa" else ""} '
                f'Q{q}' + ''.join(f'({x})' for x in parts_))

    def worklist(self, min_options=3, width=34):
        """Every part with enough listed responses to be worth reading.

        Not filtered to parts whose tariff the extractor could read: Section A
        prints a bare question total — ⟨12⟩ — where Section B prints ⟨2 @ 6⟩, so
        insisting on a derived claim hides most of Section A. The tariff is
        printed instead, for the author to set from the paper.
        """
        for p in self.parts:
            if len(p['options']) < min_options:
                continue
            st = ('+'.join(map(str, p['steps'])) if p['steps']
                  else f"{p['claim']}@{p['per']}" if p['claim'] else '/'.join(p['cells'])[:12])
            print(f"{self.cite(p) or '(unplaced)':<28} [{st:<12}] {p['question'][:104]}")
            for o in p['options']:
                print(f'    · {o[:width * 3]}')
            print()

    def emit(self):
        emit(self.cards)
