#!/usr/bin/env python3
"""Authoring for Construction Studies. Refuses rather than guesses.

A card here is one PART of a question, carrying one row per group the scheme
names under it. Not one card per group: a group-level card would need a
group-level question and the paper prints no such sentence, and question text is
lifted or it is not written. See cs_scheme.py for how the groups are read.

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
from markbank_authoring import anyN, make_audit, make_card, make_emit, point  # noqa: E402

SUBJECT = 'construction-studies'
_card = make_card(SUBJECT, default_section='B')
# The deck's own display cap; mirrors MAX_LONG_OPTION_ROWS in optionCap.mjs.
MAX_OPTIONS_SHOWN = 14
audit = make_audit(MAX_OPTIONS_SHOWN)
emit = make_emit(audit)

ANY_N = re.compile(r'\bany\s+(one|two|three|four|five|six)\b', re.I)
N_WORD = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}
TOTAL = re.compile(r'\(\s*(\d{1,3})\s*marks?\s*\)', re.I)
# Every printed total for a part: the bracketed one and the Sub-total row.
PART_TOTAL = re.compile(r'\((\d{1,3})\s*marks?\)|sub-?\s*total\s+(\d{1,3})', re.I)
# "Scale - 4 marks Drafting - 4 marks", "+ 4 marks (3 for drawing, 1 for
# annotation)" — priced, but not a named answer, so a card may leave it out.
DRAW_ALLOWANCE = re.compile(r'(?:scale|drafting|drawing|annotation)\s*[-–]?\s*(\d{1,3})\s*marks?', re.I)
# The presentation band, priced as a descending run under its own heading:
#   Quality of sketch (excellent, good, fair)
#   6 4 2
# Its top value is what a full answer earns, and like the scale and drafting
# marks it is awarded for presentation rather than for a named answer.
BAND = re.compile(r'(?:quality of \w+|excellent,? ?good,? ?fair)[^\d]{0,40}?(\d{1,3})(?:\s+\d{1,3})+', re.I)
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
    LEVELS = {'hl': 'higher', 'ol': 'ordinary'}

    def __init__(self, year, level):
        self.year, self.level = year, level
        # The deck names levels in full, and the build resolves a card's scheme
        # file from it: "hl" was read as not-"higher", so every Higher card was
        # checked against the ORDINARY scheme and its marking points reported
        # untraceable. They traced perfectly against the right file.
        self.deck_level = self.LEVELS[level]
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
        """"2021 HL Q1(a)" — the citation form every other subject uses.

        paper.ref() returns only the part path. Without the year and level on
        the front, every paper's Q1(a) is the same string, and the build's
        one-card-per-question rule then drops all but the first: three papers
        came out as seventeen cards instead of thirty-four.
        """
        k = self._paper_key(q, letter)
        tail = self.P.ref(k) if k else f'Q{q}({letter})'
        return f'{self.year} {self.level.upper()} {tail}'

    # ---- the tariff -----------------------------------------------------
    def tariff(self, q, letter, name, n_items, index=None):
        """(claim, per) from what the scheme prints, or Refused.

        Groups are paired between the two halves BY ORDER, not by name. The
        halves name the same group differently -- the 2025 Higher scheme calls
        one "Foundation and solid concrete ground floor - typical detailing"
        where it prints the content and "Foundation + Solid ground floor" where
        it prints the marks -- so matching on the name refused every grouped
        drawing question in the paper, which is the best content the subject
        has. The order is the same in both halves because both are generated
        from the same list.
        """
        block_lines = self.S.marks.get((q, letter), [])
        block = ' '.join(block_lines)
        tariffs = [(int(a), int(b)) for a, b in CS.GROUP_TARIFF.findall(block)]
        if index is not None and index < len(tariffs):
            return tariffs[index]
        for gname, t, _ in self.S.groups(q, letter):
            if t and (name is None or _squash(gname or '') == _squash(name)):
                return t
        # A group whose mark rows are each priced the same: the scheme sets
        # "Guideline 1 (3 for note, 3 for sketch) 6 / Guideline 2 ... 6" under
        # each task, which is two claimable answers at 6 rather than a total.
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
        # The scheme's commonest way of pricing a menu: rows that NAME nothing.
        # "Advantage 1  5 / Advantage 2  5" is two interchangeable answers at
        # five, and the content is in the indicative half. This is not an
        # inference -- the count and the mark are both printed -- and it is what
        # most of Ordinary Level looks like.
        # Deliberately NOT filtered by _is_unstateable. Dropping the drawing and
        # notes rows here unlocks a handful of parts and costs more than it
        # wins: the readings that survive shift the option lists past the
        # display cap, and same-mark readings that were right stop resolving.
        # Measured at 168 carded against 173 without it. The allowance belongs
        # in _check_total, where it can only widen what is accepted.
        rows = self.S.mark_rows(q, letter)
        scaffold = [(lab, mk) for lab, mk in rows if CS.SCAFFOLD_ROW.match(lab)]
        printed = {int(a or b) for a, b in PART_TOTAL.findall(block)}

        # Two readings of the same block, and the printed total decides between
        # them. "Suitable finish 4 / Reason 1 4 / Reason 2 4 / Sub-total 12" is
        # THREE answers at four, not the two the scaffold rows alone suggest --
        # taking the scaffold reading gave a card worth 8 on a 12-mark question.
        # Where no total is printed the scaffold reading is the safer of the two,
        # because a named row may be a heading rather than an answer.
        cand = []
        if len(scaffold) >= 2 and len({mk for _, mk in scaffold}) == 1:
            cand.append((len(scaffold), scaffold[0][1]))
        if len(rows) >= 2 and len({mk for _, mk in rows}) == 1:
            cand.append((len(rows), rows[0][1]))
        for n, per in cand:
            if printed and n * per in printed:
                return (n, per)
        if cand:
            return cand[0]

        # N identically-named slots against a printed total. "Three functional
        # requirements of an external wall (18 marks)" over "Functional
        # Requirement 1/2/3" is three answers at six, and both the three and the
        # eighteen are printed -- the six is arithmetic on them, not a guess.
        # The division must be exact; where it is not, the scheme has not said
        # how the marks fall and the part is left.
        slots = CS.slot_labels(block_lines)
        if tot and len(slots) >= 2 and len(set(slots)) == 1:
            total = int(tot.group(1))
            if total % len(slots) == 0:
                return (len(slots), total // len(slots))

        # A part with exactly ONE priced row prices one answer. "Advantage 6 /
        # Sub-total 6" and "Safety precaution note & sketch (8 + 5 marks) 13"
        # are both a single answer worth what the row says, and the candidates
        # for it are in the indicative half. The scaffold path above needs two
        # rows to see a pattern and so could not read either.
        if len(rows) == 1:
            return (1, rows[0][1])

        # Last resort, and the only inferred form: every priced row in the part
        # carries the same mark, so the count and that mark are the tariff. It
        # must reconcile with the printed total, otherwise it is a guess.
        marks = [mk for _, mk in rows]
        if len(marks) >= 2 and len(set(marks)) == 1 and index is None:
            n, per = len(marks), marks[0]
            if tot is None or n * per == int(tot.group(1)):
                return (n, per)
        raise Refused(f'Q{q}({letter}) [{name}]: the scheme prints no tariff for this '
                      f'group; leave it uncarded rather than estimate one')

    def _choice_and_reasons(self, q, letter, qtext, cid, topic, concept, notes, stem):
        """A card for "specify a suitable X, and give two reasons for it".

        The scheme prices these as "Suitable material 4 / Reason 1 4 / Reason 2
        4", every row at the same mark, and answers them with a two-column
        table. Read flat, only the one named row survives and the card came out
        worth 4 on a 12-mark question; read as columns, it is the choice and the
        reasons, which is what the question asks for.
        """
        rows = self.S.mark_rows(q, letter)
        if len(rows) < 2:
            return None
        reasons = [r for r in rows if re.match(r'reasons?\b', r[0], re.I)]
        choice = [r for r in rows if not CS.SCAFFOLD_ROW.match(r[0])]
        # The choice is not always priced the same as its reasons: 2021 Ordinary
        # Q2(c) pays 6 for the floor type and 4 for each reason. The reasons
        # must agree with each other, and nothing else may be priced here.
        if (not reasons or len(choice) != 1
                or len({mk for _, mk in reasons}) != 1
                or len(reasons) + 1 != len(rows)):
            return None
        per, pick = reasons[0][1], choice[0][1]
        page = self.S.pages.get((q, letter))
        left, right = CS.paired_table(self.year, self.level, page, letter)
        if len(left) < 2 or len(right) < 2:
            return None

        def clean(col):
            out = []
            for t in col:
                t = t.strip(' .;')
                if (not t or CONTENT_FREE.match(t) or len(t) < 3
                        or re.fullmatch(r'reasons?', t, re.I)
                        or _squash(t)[:24] in _squash(qtext)
                        or _squash(t) not in self.raw):
                    continue
                out.append(t)
            return out

        opts_l, opts_r = clean(left), clean(right)
        if len(opts_l) < 2 or len(opts_r) < 2:
            return None
        # The reasons column pools every material's reasons, so it can run past
        # what the deck will show. Trimming it is not an option -- the SEC
        # printed the list whole -- so the part is left rather than shown a
        # menu that is missing five of its answers.
        if len(opts_l) > MAX_OPTIONS_SHOWN or len(opts_r) > MAX_OPTIONS_SHOWN:
            raise Refused(f'Q{q}({letter}): the reasons column has {len(opts_r)} '
                          f'options, past the {MAX_OPTIONS_SHOWN} a row may show')
        total = pick + len(reasons) * per
        gap_note = self._check_total(q, letter, total, qtext)
        if gap_note:
            notes = (notes + ' ' if notes else '') + gap_note
        card_rows = [
            anyN(f'{cid}-r1', choice[0][0], pick, 1, pick, opts_l, choice[0][0]),
            anyN(f'{cid}-r2', 'Reasons for the choice', len(reasons) * per,
                 len(reasons), per, opts_r, 'Any valid reason for the choice'),
        ]
        self.cards.append(_card(
            cid, self.year, self.deck_level, topic, concept, self.ref(q, letter),
            qtext, f'1 x {pick} + {len(reasons)} x {per}', total, card_rows, notes,
            stem=stem, tariff_kind='fixed'))
        self._used.add(cid)
        return self.cards[-1]

    # A priced row that awards no NAMEABLE answer: the drawing itself, the
    # notes/sketch split, the presentation band, or a row that simply restates
    # the task. A card cannot carry these -- there is nothing to lift -- so the
    # marks they hold are a legitimate shortfall against the part's total.
    # Anchored to the WHOLE label. As a prefix it swallowed "Note for separate
    # living space", which is a named answer worth five marks, and the part
    # then priced as one answer worth fifteen.
    UNSTATEABLE = re.compile(
        r'^(sketch(es)?|drawing|notes?|notes?\s*[/&]\s*(discussion|sketch(es)?)'
        r'|discussion|presentation|layout|quality of \w+.*)$', re.I)

    def _is_unstateable(self, lab, qtext):
        """Does this priced row award anything a card could carry?

        Three ways it does not: the label is a bare "Sketch" or "Notes"; it is
        content-free; or it restates the task. The restatement is matched on
        OVERLAP, not on a prefix -- "Proposed design layout sketch for extension
        to include separate living space" is the question said back with one
        word inserted, which a prefix test misses and a ratio does not.
        """
        if CONTENT_FREE.match(lab) or self.UNSTATEABLE.match(lab):
            return True
        a, b = _squash(lab), _squash(qtext)
        if len(a) < 16 or not b:
            return False
        # COVERAGE of the label, not similarity of the two strings. A ratio
        # compares lengths as well as content, so a 30-character row label
        # scored 0.39 against a 110-character question it is almost entirely
        # contained in. What matters is whether the row says anything the
        # question does not: "Design layout for home office space" against
        # "show a proposed design layout for the office space" says nothing.
        import difflib
        m = difflib.SequenceMatcher(None, a, b).get_matching_blocks()
        return sum(bl.size for bl in m) / len(a) >= 0.8

    def _unstateable(self, q, letter, qtext):
        return sum(mk for lab, mk in self.S.mark_rows(q, letter)
                   if self._is_unstateable(lab, qtext))

    def _check_total(self, q, letter, total, qtext='', used=None):
        """Returns a note where a NAMED shortfall is allowed, else None."""
        """The card's marks must be the question's marks.

        Where the scheme prints a total for this part, the rows have to make it
        -- otherwise the card tells a student a 30-mark question is worth 12,
        which is worse than no card. The one allowed shortfall is the drawing
        and scale allowance, which the scheme prices separately and is not a
        named answer.

        Called from EVERY path that emits. It began life inline in the menu path
        and the single-answer path added later returned before reaching it, so
        nine cards shipped with a total their own scheme block never prints.
        """
        block = ' '.join(self.S.marks.get((q, letter), []))
        printed = {int(a or b) for a, b in PART_TOTAL.findall(block)}
        if not printed or total in printed:
            return None
        allowance = sum(int(x) for x in DRAW_ALLOWANCE.findall(block))
        allowance += sum(int(x) for x in BAND.findall(block))
        # NOT _unstateable() over every row: that counted the rows the card
        # itself used. 2025 Higher Q10(c) is priced "Notes 3 / Notes 3" and the
        # card is those two rows, so allowing them again as an allowance made a
        # 6-mark card pass silently as a 12-mark part. The rows the card did not
        # take are handled below, where they produce a note the student sees.
        if any(total + allowance == p for p in printed):
            return None
        # The shortfall is only acceptable if it can be NAMED. Where the rows
        # the card does not carry account for it exactly, the card ships with a
        # note saying so, because a student needs to know a 12-mark card sits
        # inside a 30-mark question. Where the arithmetic does not close, the
        # part is left: an unexplained shortfall is a misread tariff.
        # The gap is whatever the card did NOT take. `used` says how many rows
        # of what value the card's own tariff accounts for; removing exactly
        # those leaves the rows nobody is being asked to state -- the drawing,
        # and a "Justification" the scheme gives no content for. Deciding this
        # by inspecting each label instead was wrong in both directions: the
        # card's own "Design Consideration 1/2/3" rows read as unstateable
        # because the question names them, while "Justification" did not.
        rest = list(self.S.mark_rows(q, letter))
        for claim, per in (used or []):
            for _ in range(claim):
                hit = next((i for i, (_, mk) in enumerate(rest) if mk == per), None)
                if hit is None:
                    break
                rest.pop(hit)
        named = rest
        gap = min(p for p in printed if p > total) - total if any(p > total for p in printed) else -1
        if gap > 0 and sum(mk for _, mk in named) == gap:
            what = '; '.join(f'{lab} ({mk})' for lab, mk in named)
            return (f'The scheme awards {total + gap} marks for this part. The '
                    f'{total} on this card are the marks it states answers for; '
                    f'the other {gap} go to {what} — the drawing itself and '
                    f'anything the scheme prices without saying what earns it.')
        raise Refused(f'Q{q}({letter}): rows make {total} but the scheme prints '
                      f'{sorted(printed)} for this part — not carding a partial tariff')

    # ---- the card -------------------------------------------------------
    def card(self, q, letter, *, cid, topic, concept, note='', notes='', stem='',
             only=None, split=True):
        """One card per PART, with one row per group the scheme names.

        NOT one card per group. A group-level card would need a group-level
        question -- "name five details of the foundation" -- and no such
        sentence exists in the paper. Question text is lifted or it is not
        written, so the card asks the part exactly as the paper sets it and
        carries the scheme's own groups as separate rows. That is also how the
        SEC marks it: Q1(a) of the 2021 Higher paper is three lists priced
        4 x 4 each, not one list of twelve.
        """
        self._forced = self._forced_each = None
        if cid in self._used:
            raise Refused(f'{cid}: already emitted')
        qtext = self.question(q, letter)
        if not qtext:
            raise Refused(f'Q{q}({letter}): no question text in the paper')
        pair = self._choice_and_reasons(q, letter, qtext, cid, topic, concept,
                                        notes, stem)
        if pair is not None:
            return pair
        gs = self.S.groups(q, letter, 'indicative')
        # The two halves do not always agree on how many groups a part has, and
        # the mark half is sometimes the one that got it right: 2021 Higher
        # Q7(a) is "Chimney stack 4 x 5" and "Roofing 4 x 5" there, while the
        # indicative half welded the two column headings into one line and
        # returned a single group of sixteen -- too long for the deck to show,
        # and wrong about the question, which prices the two halves separately.
        mk_groups = [g for g in self.S.groups(q, letter) if g[1] and len(g[2]) >= 2]
        if len(mk_groups) > len([g for g in gs if len(g[2]) >= 2]):
            gs = mk_groups
        if not [g for g in gs if len(g[2]) >= 2]:
            # The indicative half groups nothing for this part, but the MARK
            # table often names the answer itself: the U-value questions list
            # every element of the wall at three marks each, and the vertical
            # sections of the Ordinary papers list the section's details there
            # rather than opposite. 46 parts have no usable indicative group and
            # most of them are these.
            named = []
            for lab, mk in self.S.mark_rows(q, letter):
                if CS.SCAFFOLD_ROW.match(lab) or len(lab) < 4:
                    continue
                named.append((lab, mk))
            if len(named) >= 2 and len({mk for _, mk in named}) == 1:
                seen, opts = set(), []
                for lab, _ in named:
                    k = _squash(lab)
                    if k and k not in seen:
                        seen.add(k)
                        opts.append(lab)
                if len(opts) >= 2:
                    gs = [(None, None, opts)]
            if not [g for g in gs if len(g[2]) >= 2]:
                # The mark column is printed on alternate lines in the Ordinary
                # vertical sections, so only four of thirteen details carry a
                # number and mark_rows() sees a quarter of the answer. Where the
                # block states its tariff outright -- "Any 7 x 5 marks" -- the
                # options are every detail line, priced by that.
                blk = ' '.join(self.S.marks.get((q, letter), []))
                if len(CS.GROUP_TARIFF.findall(blk)) == 1:
                    items = [it for it in self.S.mark_items(q, letter, qtext)
                             if not CONTENT_FREE.match(it) and len(it) > 4]
                    seen, opts = set(), []
                    for it in items:
                        k = _squash(it)
                        if k and k not in seen and k in self.raw:
                            seen.add(k)
                            opts.append(it)
                    if len(opts) >= 2:
                        gs = [(None, None, opts)]
        multi = len(CS.GROUP_TARIFF.findall(
            ' '.join(self.S.marks.get((q, letter), [])))) > 1
        # One tariff over several groups prices the PART, not each group:
        # "Two features that could be added to reduce its energy use (4 x 5
        # marks)" sits over five candidate features. Charging every group 4 x 5
        # multiplies the question's marks by five, and the guard below caught it
        # as a tariff claiming more options than the group prints. Merge instead,
        # so the tariff applies to exactly the list the scheme priced.
        # How the part's tariff lands on its groups. Decided by comparing what
        # the scheme lets a student CLAIM against how many groups it names:
        #
        #   claim == groups   -> answer each one   -> fixed, a row per group
        #   claim %  groups==0-> k answers in each -> fixed, a row per group
        #   claim <  groups   -> choose among them -> best-of over group NAMES
        #
        # The last is the one that matters most. "The importance of any two in
        # maintaining a positive health and safety culture (12 marks)" over
        # three named options is two of three at six, not two of the twenty-six
        # bullets underneath them -- which is both a menu the deck will not show
        # and a misreading of the question.
        block = ' '.join(self.S.marks.get((q, letter), []))
        named_groups = [g for g in gs if g[0]]
        # Not when `multi`: that means the mark table prints a tariff PER GROUP
        # already, and dividing one of them by the group count priced 2021
        # Higher Q7(a) at 2 x 5 per group where the scheme plainly gives each
        # group its own 4 x 5.
        if len(gs) > 1 and len(named_groups) == len(gs) and not multi:
            try:
                n, per = self.tariff(q, letter, None, len(gs), None)
            except Refused:
                n = per = None
            if n:
                if n % len(gs) == 0:
                    self._forced_each = (n // len(gs), per)
                elif ANY_N.search(qtext) or ANY_N.search(block):
                    # "any two of the following" over three named groups is two
                    # of THREE, whatever the tariff's own multiplier says: the
                    # 4 in "(4 x 5 marks)" counts answers, not groups, and
                    # reading it as the claim merged all three groups into a
                    # 29-option menu the deck will not show.
                    k = N_WORD[(ANY_N.search(qtext) or ANY_N.search(block)).group(1).lower()]
                    tot_ = n * per
                    if 0 < k < len(gs) and tot_ % k == 0:
                        gs = [(None, None, [g[0] for g in gs])]
                        multi = False
                        self._forced = (k, tot_ // k)
                elif n < len(gs):
                    gs = [(None, None, [g[0] for g in gs])]
                    multi = False
                    self._forced = (n, per)
        if self._forced is None and self._forced_each is None and not multi and len(gs) > 1:
            merged = [it for _, _, items in gs for it in items]
            names = [n for n, _, _ in gs if n]
            gs = [(None, None, merged)]
            stem = stem or ('The scheme groups its answer under: ' + '; '.join(names)
                            if names else stem)
        rows, parts_note, row_names = [], [], []
        for gi, (name, _, items) in enumerate(gs):
            if only is not None and gi not in only:
                continue
            options = []
            for it in items:
                it = it.strip(' .;')
                if not it or CONTENT_FREE.match(it):
                    continue
                if _squash(it) not in self.raw:
                    raise Refused(f'Q{q}({letter}) [{name}]: {it[:60]!r} is not in '
                                  f'the scheme text — the extraction changed it')
                options.append(it)
            if len(options) < 2:
                continue
            if getattr(self, '_forced_each', None):
                n, per = self._forced_each
            elif getattr(self, '_forced', None):
                n, per = self._forced
            else:
                n, per = self.tariff(q, letter, name, len(options),
                                     gi if multi else None)
            if n > len(options) and len(gs) == 1:
                # The mark table is the fuller list for this part -- see
                # cs_scheme.mark_items. Only tried where the part has a single
                # group, because with several the two halves are not the same
                # list and swapping one for the other would mix them.
                alt = [it.strip(' .;') for it in self.S.mark_items(q, letter)
                       if it.strip() and not CONTENT_FREE.match(it.strip(' .;'))]
                alt = [it for it in alt if _squash(it) in self.raw]
                if len(alt) >= n:
                    options = alt
            if n > len(options):
                raise Refused(f'Q{q}({letter}) [{name}]: tariff claims {n} of only '
                              f'{len(options)} printed options')
            if len(options) > MAX_OPTIONS_SHOWN:
                # The deck will not show more than this many options in a row,
                # and a card offering thirty-seven is not a card. It happens
                # where one part-level tariff sits over several groups and they
                # are merged; the honest answer is to leave the part than to
                # truncate a menu the SEC printed whole.
                raise Refused(f'Q{q}({letter}) [{name}]: {len(options)} options, past '
                              f'the {MAX_OPTIONS_SHOWN} a row may show')
            label = (name or qtext)[:120]
            rows.append(anyN(f'{cid}-r{len(rows) + 1}', label, n * per, n, per,
                             options, name or ''))
            row_names.append(name)
            parts_note.append(f'{n} x {per}')
        if len(rows) == 1 and rows[0].get('group', {}).get('claimMax') == 1 \
                and len(rows[0]['group']['options']) > 6:
            # A menu of one from twenty is not a menu. Where the scheme prices a
            # single named answer, that answer is the card -- 2021 Ordinary
            # Q1(b) is "Eaves gutter/ downpipe" for three marks, and the twenty
            # options came from the previous part's specification list.
            lone = [(lab, mk) for lab, mk in self.S.mark_rows(q, letter)
                    if not CS.SCAFFOLD_ROW.match(lab) and len(lab) > 8
                    and not CONTENT_FREE.match(lab)]
            if len(lone) == 1 and _squash(lone[0][0]) in self.raw:
                rows = []

        if not rows:
            # A part whose scheme names ONE thing is still a card -- it is just
            # not a menu. "Show the typical design detailing to prevent water
            # entering at the window cill" is answered "Throating / drip / DPC"
            # for four marks, and that is as liftable as any list.
            single = [(lab, mk) for lab, mk in self.S.mark_rows(q, letter)
                      if not CS.SCAFFOLD_ROW.match(lab) and len(lab) > 8
                      and not CONTENT_FREE.match(lab)]
            if len(single) == 1 and _squash(single[0][0]) in self.raw:
                lab, mk = single[0]
                gap_note = self._check_total(q, letter, mk, qtext)
                if gap_note:
                    notes = (notes + ' ' if notes else '') + gap_note
                self.cards.append(_card(
                    cid, self.year, self.deck_level, topic, concept,
                    self.ref(q, letter), qtext, f'{mk}', mk,
                    [point(f'{cid}-r1', lab, mk, '')], notes, stem=stem,
                    tariff_kind='fixed'))
                self._used.add(cid)
                return self.cards[-1]
            raise Refused(f'Q{q}({letter}): no priced group with usable options')
        total = sum(r['marks'] for r in rows)
        used = [(r['group']['claimMax'], r['group']['perOption'])
                for r in rows if r.get('group')]
        gap_note = self._check_total(q, letter, total, qtext, used)
        if gap_note:
            notes = (notes + ' ' if notes else '') + gap_note
        # One card per row, where the PAPER's own sentence enumerates the rows.
        # The narrowed question is that sentence with the other items deleted --
        # never rewritten -- and narrow() returns nothing unless the result is a
        # strict subsequence of what the SEC printed. All rows must narrow or
        # none do: a half-split part would ask two of its items and silently
        # drop the third. The marks still reconcile, because the split cards'
        # totals are the row totals that were just checked against the part's.
        if split and len(rows) > 1 and all(row_names):
            narrowed = {nm: narrow(qtext, row_names, nm) for nm in row_names}
            if all(narrowed.values()) and len(set(narrowed.values())) == len(rows):
                for row, nm in zip(rows, row_names):
                    slug = re.sub(r'[^a-z0-9]+', '-', nm.lower()).strip('-')[:44]
                    sub = f'{cid}-{slug}'
                    if sub in self._used:
                        continue
                    g = row['group']
                    self.cards.append(_card(
                        sub, self.year, self.deck_level, topic, f'{concept}-{slug}',
                        # The item goes on the CITATION, the way Economics
                        # cites "2022 OL Q15(a)(iii) — social benefit". Both
                        # halves of a split cite the same part, and the build
                        # keeps one card per citation, so without this the
                        # second half of every split was dropped as a duplicate.
                        f'{self.ref(q, letter)} — {nm}', narrowed[nm],
                        f"{g['claimMax']} x {g['perOption']}", row['marks'],
                        [dict(row, id=f'{sub}-r1')], notes, stem=stem,
                        tariff_kind='bestNofParts'))
                    self._used.add(sub)
                return self.cards[-1]

        kind = 'bestNofParts' if len(rows) == 1 else 'fixed'
        self.cards.append(_card(
            cid, self.year, self.deck_level, topic, concept, self.ref(q, letter),
            qtext, ' + '.join(parts_note), total, rows, notes, stem=stem,
            tariff_kind=kind))
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
        gs = A.S.groups(q, letter, 'indicative')
        multi = len([t for t in CS.GROUP_TARIFF.findall(
            ' '.join(A.S.marks.get((q, letter), [])))]) > 1
        for gi, (name, _, items) in enumerate(gs):
            if len(items) < 2:
                continue
            try:
                n, per = A.tariff(q, letter, name, len(items), gi if multi else None)
                print(f'  OK   Q{q}({letter}) [{(name or "-")[:44]:<44}] {n} x {per}'
                      f'  {len(items)} options')
                ok += 1
            except Refused as e:
                print(f'  --   {str(e)[:118]}')
                refused += 1
    print(f'\n{year} {level.upper()}: {ok} priceable, {refused} not priced by the scheme')


# ---------------------------------------------------------------- splitting --
# A multi-row card can become one card per row, but ONLY where the paper's own
# sentence enumerates the items. The narrowed question is then built by DELETING
# the other items from that sentence -- never by rewriting it, reordering it or
# supplying a word of our own -- so the result is literally a subsequence of
# what the SEC printed. narrow() proves that before it returns.
#
# Where the scheme's groups are its own invention rather than the paper's list
# ("Foundation, external wall and level entrance" against a question that says
# "the door, the external wall and the ground floor"), or where the question
# points at another part instead of listing anything ("each risk identified at
# 2(b) above"), there is nothing to narrow and the card stays whole.

def _index_map(text):
    """(squashed text, index of each squashed char in the original)."""
    keep, idx = [], []
    for i, ch in enumerate(text):
        c = re.sub(r'[^a-z0-9]', '', ch.lower())
        if c:
            keep.append(c)
            idx.append(i)
    return ''.join(keep), idx


def locate(text, item):
    """(start, end) of `item` inside `text`, ignoring case and punctuation."""
    hay, idx = _index_map(text)
    needle, _ = _index_map(item)
    if len(needle) < 4:
        return None
    at = hay.find(needle)
    if at < 0:
        return None
    return idx[at], idx[at + len(needle) - 1] + 1


QUANT = re.compile(r'(?:\b(?:one|two|three|four|five|six|\d{1,2})\s*)$', re.I)


def _span(question, item):
    """The item's span, widened to what belongs with it and nothing more.

    Widened FORWARD over a closing bracket the squashed match cannot see --
    "personal protective equipment (PPE)" ends at the second E, and leaving the
    ")" behind put a stray bracket in the question. Widened BACKWARD over the
    quantifier and the separator that introduce it, so deleting one member of
    "two advantages and two disadvantages" does not stnad a "two" or an "and".

    Returns None where the item is not separable -- where what precedes it is
    ordinary prose rather than a bullet, a comma, "and", or the colon that opens
    the list. An item embedded mid-clause cannot be removed without rewriting
    the sentence, and rewriting is the one thing that is not allowed here.
    """
    found = locate(question, item)
    if found is None:
        return None
    lo, hi = found
    while hi < len(question) and question[hi] in ')]':
        hi += 1
    cut = False
    while True:
        before = question[:lo]
        stripped = before.rstrip(' \t')
        if stripped.endswith(('•', '·')):
            lo = len(stripped) - 1
            cut = True
            break
        if stripped.lower().endswith(' and'):
            lo = len(stripped) - 4
            cut = True
            break
        if stripped.endswith(','):
            lo = len(stripped) - 1
            cut = True
            break
        m = QUANT.search(before)
        if m and not cut:
            lo = m.start()
            continue                      # then look again for the separator
        break
    if not cut:
        # Nothing separable in front. The first member of a pair carries its
        # separator BEHIND it instead -- "two advantages and two disadvantages"
        # -- so the "and" is taken with it. Only tried once a quantifier has
        # been consumed, which is what marks this as a list member rather than
        # a phrase that happens to appear mid-sentence.
        after = question[hi:]
        m = re.match(r'\s+(and|,)\s', after, re.I)
        if m and QUANT.search(question[:found[0]]):
            return lo, hi + m.end() - 1
        return None
    return lo, hi


def narrow(question, items, keep):
    """The paper's sentence with every item but `keep` deleted.

    Returns None unless the result is a strict subsequence of the original --
    that is the whole safety property. If a cleanup ever introduced so much as a
    letter that the SEC did not print, this returns nothing and the caller keeps
    the undivided card.
    """
    spans = []
    for it in items:
        if it == keep:
            continue
        sp = _span(question, it)
        if sp is None:
            return None
        spans.append(sp)
    if not spans:
        return None
    out, last = [], 0
    for lo, hi in sorted(spans):
        if lo < last:
            return None                       # overlapping items: not separable
        out.append(question[last:lo])
        last = hi
    out.append(question[last:])
    text = re.sub(r'\s+', ' ', ''.join(out)).strip()
    text = re.sub(r'\s+([.,;:])', r'\1', text)
    text = re.sub(r'[:•]\s*([.,;])', r'\1', text).strip(' •·-–,')
    if not text.endswith('.'):
        text = text.rstrip(':;, ') + '.'
    # The guarantee: every character of the result, in order, came from the
    # original. Whitespace and the one closing full stop are exempt.
    a, _ = _index_map(text)
    b, _ = _index_map(question)
    i = 0
    for ch in a:
        i = b.find(ch, i)
        if i < 0:
            return None
        i += 1
    if locate(text, keep) is None:
        return None
    return text
