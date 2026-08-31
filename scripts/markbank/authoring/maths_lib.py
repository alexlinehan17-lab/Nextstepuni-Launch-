#!/usr/bin/env python3
"""Authoring for Mathematics.

A card is one part of one paper:

  question   the paper's own wording, read span-aware so exponents survive
             (mathtext.clean_like) -- "4x^3 - 12x^2", not "4x3 - 12x2"
  rows       the Marking Notes: the numbered steps where the scheme gives them,
             otherwise its Low/Mid/High Partial Credit descriptors
  tariff     the partial-credit ladder, "Scale 15D (0, 4, 7, 10, 15)"

The ladder maps exactly onto perOptionSteps, which is what the first n options
claimed are worth: the increments of (0, 4, 7, 10, 15) are 4, 3, 3, 5, so one
step earns 4, two earn 7, three earn 10 and all four earn 15. Nothing is
derived -- every number is printed on the page.

The model solution is NOT text. Extraction scrambles it, so it belongs on the
card as a cropped image; see maths_figures.py.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathtext                                              # noqa: E402
import maths_scheme                                          # noqa: E402
import paper as PP                                           # noqa: E402
from markbank_authoring import anyN, make_audit, make_card, make_emit  # noqa: E402

SUBJECT = 'maths'
_card = make_card(SUBJECT, default_section='B')
MAX_OPTIONS_SHOWN = 14
audit = make_audit(MAX_OPTIONS_SHOWN)
emit = make_emit(audit)
COMPONENT = {1: '100', 2: '200'}

# The running header runs on into a part's text where the question ends near
# the foot of a page: "... (2x+ 5√x-7 ) Leaving Certificate 2025 5 Mathematics,
# Paper 1". It is not part of the question and looks like a mistake on a card.
FURNITURE_TAIL = re.compile(
    r'\s*(Leaving Certificate\s+\d{4}|Mathematics,?\s*Paper|Page\s+\d+\s+of)'
    r'[\s\S]*$', re.I)

CONTENT_FREE = re.compile(r'^(work of merit|any valid|as above|see above|'
                          r'accept any|other relevant)\W*$', re.I)

# Primary-paper corrections for asks whose two-dimensional typesetting defeats
# the generic text extractor. The source remains the SEC paper; these strings
# are verified transcriptions and keep future regeneration from restoring the
# broken, interleaved readings currently visible on the affected cards.
VERIFIED_QUESTION_TEXT = {
    (2025, 'hl', 1, 10, 'e', 'i'):
        'H(n) is the total number of dots in Pattern n of the sequence, for '
        'n ∈ ℕ. (i) Write down the value of H(1). When n is a natural number, '
        'H(n + 1) can always be found from H(n), using the formula '
        'H(n + 1) = H(n) + 2n + 3. (ii) Using this fact, prove by induction '
        'that H(n) = (n + 1)² for all n ∈ ℕ.',
    (2025, 'hl', 2, 8, 'a', 'i'):
        '(i) Use the theorem of Pythagoras to show that |OB| = 3√2 m, and '
        'hence find |OP|, the vertical height of the pyramid. Give |OP| in '
        'surd form.',
    (2025, 'hl', 2, 8, 'a', 'ii'):
        '(ii) On the triangular face PAB, the size of ∠PAB is 74·2°, correct '
        'to 1 decimal place. Using this, or otherwise, work out the total area '
        'of the four triangular faces of the roof. Give your answer correct '
        'to the nearest m².',
    (2025, 'hl', 2, 8, 'a', 'iii'):
        '(iii) The diagram below shows part of a scaled diagram of the net of '
        'this pyramid. The diagram shows the square base and two of the '
        'triangular sides. Construct the rest of the scaled diagram of the '
        'net of the pyramid. Show all construction lines clearly.',
    (2025, 'hl', 2, 10, 'e', None):
        '(e) For one of the questions on the test, students are given a mark '
        'of 0, 1, 2, or 3. The proportion receiving each mark is 0·19, p, 2r, '
        'and r, respectively, where p, r ∈ ℝ and p, r ≥ 0. A student is '
        'picked at random. The expected value of their mark will depend on p '
        'and r. Find the largest value that the expected value could be.',
}


class Refused(Exception):
    pass


def _squash(t):
    return re.sub(r'[^a-z0-9]+', '', (t or '').lower())


SOLUTION_LABEL = 'Model solution'
# Part labels, rung markers and bare mark totals are not working.
SOLUTION_FURNITURE = re.compile(
    r'^(?:\(?[a-h]\)|\(?(?:i{1,3}|iv|vi{0,3})\)|\[?\d{1,3}\]?|OR'
    r'|Model Solution.*|Q\d+)$', re.I)


class Author:
    LEVELS = {'hl': 'higher', 'ol': 'ordinary'}

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.deck_level = self.LEVELS[level]
        self.S = maths_scheme.Scheme(year, level)
        self.P = {n: PP.Paper(SUBJECT, year, level, component=c)
                  for n, c in COMPONENT.items()}
        self.cards = []
        self._used = set()
        self._flat = None

    def topic_evidence(self, key):
        """The text a topic classifier may read for this unit.

        The paper's own wording first. Where that names nothing a keyword can
        file -- "Find the length of the runway. Give your answer in km." --
        the SCHEME still states the method it is marking, and the method is
        the topic: 2021 OL Paper 2 Q9 files as Trigonometry only because its
        (b)(i) solution reads "x/(sin 47) = 260/(sin 36)". Reading the scheme
        for this is not reading it for an ANSWER; it decides which shelf the
        card sits on, nothing a student is shown.
        """
        try:
            scheme = ' '.join(self.S.notes(key)) + ' ' + ' '.join(self.S.solution(key))
        except Exception:                                    # noqa: BLE001
            scheme = ''
        return scheme

    def question(self, key):
        """The paper's wording for this unit.

        A unit may be marked at a coarser grain than the paper sets it -- the
        scheme prices Q2(b) once where the paper asks (b)(i), (b)(ii) and
        (b)(iii) -- so where the exact part is not in the paper, the parts
        underneath it are joined. That is still the paper's own words.
        """
        paper, q, letter, roman = key[0], key[1], key[2], key[3]
        verified = VERIFIED_QUESTION_TEXT.get(
            (self.year, self.level, paper, q, letter, roman))
        if verified:
            return verified
        P = self.P[paper]
        exact = [k for k in P.parts
                 if k[0] == q and k[1] == letter and k[2] == roman]
        if not exact and roman is None:
            exact = [k for k in P.parts if k[0] == q and k[1] == letter]
        # The scheme sometimes prices a whole question as one unit -- 2021 OL
        # Paper 1 Q2 is marked once where the paper sets (a) and (b) -- and the
        # paper has no part with no letter to match, so the lookup found
        # nothing and the part was filed as having no question text at all.
        if not exact and letter is None:
            exact = [k for k in P.parts if k[0] == q]
        if not exact:
            return ''
        exact.sort(key=lambda k: (k[1] or '', k[2] or ''))
        joined = ' '.join((P.text(*k) or '').strip() for k in exact)
        # A part whose first line ends in a full stop stops collecting, so an
        # ask set on the next line lands in the letter's stem instead: 2022 HL
        # Paper 1 Q2(a) reads "g(x) = 2x^2 + 5x + 6, where x in R." with "Find
        # the integral of g(x) dx" underneath, and the part alone is not a
        # question. Pulled in only when the part cannot stand on its own, and
        # only for a lettered part -- a roman's stem holds its SIBLINGS' asks,
        # and Q3(a)'s stem is the wording of Q3(a)(iii).
        cleaned = mathtext.clean_like(P.files, joined)
        if roman is None and len(_squash(joined)) < 25:
            extra = (P.stem(q, letter) or '').strip()
            if extra:
                # Cleaned SEPARATELY and then joined. clean_like finds a
                # fragment in the document and hands back the span-aware
                # reading of it, so a string glued together from two places
                # matches nothing and falls back to the unrepaired text --
                # which is how "2x^2 + 5x + 6" came back as "2x2+ 5x+ 6".
                cleaned = f'{cleaned} {mathtext.clean_like(P.files, extra)}'.strip()
        return cleaned

    # A scheme unit keyed by a marker the PAPER does not print. 2021 HL P2's
    # scheme labels the Q2(c)(i) work (|AC|, D, the translation) as a bare
    # "(i)", and the card shipped citing "Q2(i)" — an address no paper page
    # answers to. The citation is corrected here; the card id is NOT (ids
    # never rename once shipped).
    RECITE = {
        (2021, 'hl'): {(2, 2, None, 'i'): (2, 2, 'c', 'i')},
    }

    def ref(self, key):
        key = self.RECITE.get((self.year, self.level), {}).get(tuple(key[:4]), key)
        paper, q, letter, roman = key[0], key[1], key[2], key[3]
        tail = f'Q{q}'
        if letter:
            # One scale, several LETTERS: the scheme heads a unit "(a), (b)"
            # and marks both together, the letter twin of the roman span
            # below. 2022 OL Paper 1 Q1 does this; citing only (a) left (b)
            # reading as uncovered when the card already answers it.
            lspan = self.S.letter_spans.get(tuple(key[:4])) \
                if hasattr(self.S, 'letter_spans') else None
            if lspan and len(lspan) > 1 and not roman:
                tail += f'({lspan[0]})–({lspan[-1]})' if len(lspan) > 2 \
                    else f'({lspan[0]}), ({lspan[1]})'
            else:
                tail += f'({letter})'
        if roman:
            # One scale, several parts: the scheme heads a unit "(a) (i) & (ii)"
            # and marks both together, so the card answers both and must say so.
            # Citing only the first left the rest looking uncovered.
            span = self.S.spans.get(tuple(key[:4])) if hasattr(self.S, 'spans') else None
            if span and len(span) > 1:
                tail += f'({span[0]})–({span[-1]})' if len(span) > 2 \
                    else f'({span[0]}), ({span[1]})'
            else:
                tail += f'({roman})'
        return f'{self.year} {self.level.upper()} Paper {paper} {tail}'

    def _flat_scheme(self):
        """The whole scheme as one squashed string, for a traceability check.

        The build refuses a card whose marking point it cannot find in the
        scheme, and squashing to letters and digits is exactly the comparison
        it makes. Making the same check here lets the author react to a failure
        instead of emitting a card the build will silently drop.
        """
        if self._flat is None:
            said = []
            for i in range(len(self.S.doc)):
                left, right = mathtext.placed(self.S.doc[i])
                said.extend(t for _, t in left)
                said.extend(t for _, t in right)
            self._flat = _squash(' '.join(said))
        return self._flat

    def _traceable(self, rows):
        flat = self._flat_scheme()
        return all(_squash(t) in flat for _, t in rows)

    def _solution_rows(self, key):
        """The scheme's printed worked solution, read as marking points.

        Where the Marking Notes column is empty the scheme has still printed
        the answer -- in the Model Solution column beside it, which is the SEC's
        own text and is what the ladder is marked against. 2021 HL Paper 1
        Q4(b)(i) prices five marks on a (0, 2, 5) scale and states nothing in
        the notes, while the solution column reads "Tn = p + (n-1)(7)" and
        "Tn = p + 7n-7". Refusing those parts threw away a printed answer; 84
        parts of the ten papers are marked that way.
        """
        out = []
        for text in self.S.solution(key):
            text = text.strip()
            if not text or SOLUTION_FURNITURE.match(text):
                continue
            # Not the squashed-length test the prose subjects use. Squashing
            # keeps only letters and digits, and a line of algebra is mostly
            # neither: "Tn = p + (n-1)(7)" squashes to six characters and was
            # dropped as too thin, which is why this fallback first returned
            # nothing at all. Length of the line as printed, plus something to
            # read in it.
            if len(text) < 4 or not re.search(r'[A-Za-z0-9]', text):
                continue
            out.append((SOLUTION_LABEL, text))
        return out

    def stem_for(self, key):
        """The paper's setup for this part — the context the ask leans on.

        "Find the probability that there is exactly one left footed player on
        the team" is unanswerable without the stem that says 15% of the
        population is left footed and the team has 11 players. The stem lives
        on the question, sometimes on the letter; both are the paper's own
        words. Cleaned piece by piece (clean_like matches one fragment at a
        time) and deduplicated against the part's own text, since a short part
        already pulls its letter stem into the question."""
        paper, q, letter, roman = key[0], key[1], key[2], key[3]
        P = self.P[paper]
        pieces = []
        for src in ((q, None), (q, letter) if letter else None):
            if not src:
                continue
            raw = (P.stem(*src) or '').strip()
            raw = re.sub(r'^\(\d{1,3}\s*marks?\)\s*', '', raw)
            if len(_squash(raw)) >= 15:
                pieces.append(mathtext.clean_like(P.files, raw))
        text = ' '.join(dict.fromkeys(pieces))
        return text if len(_squash(text)) >= 15 else ''

    def card(self, key, *, cid, topic, concept, notes='', stem='', figure_key=''):
        if cid in self._used:
            raise Refused(f'{cid}: already emitted')
        qtext = FURNITURE_TAIL.sub('', self.question(key)).strip(' .;,')
        if not stem:
            stem = self.stem_for(key)
            # A stem the question already contains (the short-part rule pulls
            # it in) would print twice.
            if stem and _squash(stem) in _squash(qtext):
                stem = ''
        # Squashing keeps only letters and digits, and a Maths question is
        # mostly neither: "Show that z - iz = 8 - 4i." measures fourteen and is
        # a whole question. Judged on either measure, not on the squash alone.
        if len(_squash(qtext)) < 12 and len(qtext) < 24:
            raise Refused(f'{self.ref(key)}: no question text in the paper')
        total, ladder = self.S.tariff(key)
        if not total or not ladder or len(ladder) < 2:
            raise Refused(f'{self.ref(key)}: the scheme prints no ladder for this part')
        # The fraction splice can echo a stacked token the scheme prints once
        # — "Writes 1/√n 1/√n" — when the same bar serves two printed rows.
        # Collapsed here because a student reads this text; the collapsed form
        # still traces (the fold holds the doubled spelling, and a substring
        # only matches more).
        dedupe = lambda t: re.sub(r'(\S{1,14}/\S{1,14}) \1(?=\s|$)', r'\1', t)
        rows = [(lab, dedupe(txt)) for lab, txt in self.S.answer_rows(key)
                if txt and not CONTENT_FREE.match(txt) and len(_squash(txt)) > 6]
        # A marking point set as two-dimensional mathematics does not survive
        # being read line by line: "cos C = (28^2 + 4^2 - 30^2) / (2(28)(4))"
        # comes back as "cosC = 282 + 42-302 or equivalent 2(28)(4)", which is
        # not what the scheme says and would not be readable if it were. The
        # build drops those on provenance -- 85 of them -- so notice here and
        # use the solution column instead, which the same scheme prints in one
        # line at a time.
        if rows and not self._traceable(rows):
            spelled = self._solution_rows(key)
            if spelled and self._traceable(spelled):
                rows = spelled
        if not rows:
            rows = self._solution_rows(key)
        if not rows:
            raise Refused(f'{self.ref(key)}: the marking notes state nothing liftable')
        if len(rows) > MAX_OPTIONS_SHOWN:
            raise Refused(f'{self.ref(key)}: {len(rows)} rows, past the '
                          f'{MAX_OPTIONS_SHOWN} a row may show')
        # The ladder's rungs are cumulative; perOptionSteps wants the increments.
        rungs = [v for v in ladder if v]
        steps = [rungs[0]] + [b - a for a, b in zip(rungs, rungs[1:])]
        if sum(steps) != total or any(s < 0 for s in steps):
            raise Refused(f'{self.ref(key)}: ladder {ladder} does not make {total}')
        claim = min(len(rows), len(steps))
        steps = steps[:claim]
        if sum(steps) != total:
            # Fewer marking points than rungs: give the last row the remainder,
            # which is what the scale does -- the top rung is full credit.
            steps[-1] += total - sum(steps)
        # The option is the scheme's own text and nothing else. Joining the
        # rung's heading to it -- "Low Partial Credit — Finds one relevant
        # probability" -- is a string the scheme never printed, and the
        # provenance gate is right to refuse it. The headings go in the note,
        # in order, so a student still knows which rung is which.
        options = [txt for _, txt in rows]
        if all(lab == SOLUTION_LABEL for lab, _ in rows):
            rung_note = (" These are the lines of the scheme's own printed "
                         'solution, in the order it sets them out.')
        else:
            rung_note = ' Marked in order: ' + '; '.join(lab for lab, _ in rows) + '.'
        # Enumerate only as many rungs as the card actually SHOWS. The ladder
        # can have more rungs than the scheme names bands for, and printing
        # "three parts for 10" beside two options told the student a third
        # option existed and they had missed it.
        shown = ladder[:claim + 1]
        note = ('The scheme marks this on a sliding scale: '
                + ', '.join(f'{n} for {v}' for n, v in
                            zip(('nothing', 'one part', 'two parts', 'three parts',
                                 'four parts', 'five parts'), shown)) + '.')
        if len(shown) < len(ladder):
            note += f' The full scale runs to {ladder[-1]}.'
        # "Full Credit -1" is a deduction the examiner applies, not a rung to
        # claim, so it belongs in the note and never in the options. The same
        # goes for the part's marking instructions -- the scheme's own "Note:"
        # lines, which were being appended to whichever bullet they followed.
        def _sentence(t):
            t = t.strip()
            return t if t.endswith(('.', ':', '?')) else t + '.'
        for lab, bullets in self.S.deductions(key):
            note += ' ' + _sentence(f'{lab}: ' + '; '.join(bullets))
        for aside in self.S.part_notes(key):
            # A note is worth having only if it is readable. Some carry a glyph
            # the font subset never mapped -- "(2233.3\u1236 m\u00b2)" -- and the build
            # rightly refuses the whole card for it. Drop the note, keep the card.
            if any(0x0530 <= ord(ch) <= 0x1FFF for ch in aside):
                continue
            note += ' ' + _sentence(aside if aside.lower().startswith('note') else f'Note: {aside}')
        row = anyN(f'{cid}-r1', options[0], total, claim, steps[0], options,
                   note + rung_note,
                   steps=steps if len(set(steps)) > 1 else None)
        self.cards.append(_card(
            cid, self.year, self.deck_level, topic, concept, self.ref(key), qtext,
            f'Scale ({", ".join(str(v) for v in ladder)})', total, [row], notes,
            stem=stem, tariff_kind='fixed', figure_key=figure_key))
        self._used.add(cid)
        return self.cards[-1]

    def emit(self):
        emit(self.cards)


if __name__ == '__main__':
    A = Author(int(sys.argv[1]), sys.argv[2])
    ok = bad = 0
    for key in A.S.parts():
        try:
            c = A.card(key, cid=f'probe-{key}', topic='t', concept='c')
            ok += 1
            if ok <= 4:
                g = c['rows'][0]['group']
                print(f'{c["questionRef"]:<28} {c["totalMarks"]:>3}m  '
                      f'{g["claimMax"]}x steps={g.get("perOptionSteps")}')
                print(f'    Q: {c["questionText"][:78]}')
                for o in g['options'][:3]:
                    print(f'    - {o[:74]}')
        except Refused as e:
            bad += 1
            if bad <= 4:
                print(f'  REFUSED {str(e)[:88]}')
    print(f'\n{ok} cardable, {bad} refused of {len(A.S.parts())}')
