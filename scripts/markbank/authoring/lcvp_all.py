#!/usr/bin/env python3
"""Author every LCVP part the scheme states and prices.

    python3 scripts/markbank/authoring/lcvp_all.py            # emit JSON
    python3 scripts/markbank/authoring/lcvp_all.py --report   # counts, refusals
    python3 scripts/markbank/authoring/lcvp_all.py --write    # authored/lcvp.json

Census-driven, like Engineering and Computer Science: the denominator is
paper_census.py's count of what the eight papers print, and every card is the
scheme's own text against the paper's own ask.

WHAT THE TARIFF NOTATION MEANS, and the deck convention each maps to. All of
it is the SEC's own arithmetic; none is inferred.

  "3 @ 2m (1 + 1)"   the candidate offers three answers from the scheme's list
  "3 x 2 marks"      and each is worth two, split one for the point and one
  "4 x 1 mark"       for developing it -> an anyN row whose group IS the list,
  "2@2 (1+1)"        claimMax three, perOption two, worth six.

  "3 marks (1+1+1)"  the same menu with the count spelled out in the bracket
  "2 + 2 marks"      or in the addition: three answers at one, two at two.

  "Three valid       the count in words beside a total that divides by it.
   answers 3 marks"  Only read where the division is exact.

  "Heading AGENDA    a component priced on its own beside a menu. Both are
   = 1 mark" +       rows, and the two must add to the marks the PAPER prints
  "5 valid agenda    for the part — which is the check that makes reading a
   items 5@1m"       compound tariff safe rather than a guess.

  "(0/2)"            all or nothing on each answer. It changes nothing about
                     the arithmetic, and rides on the card as a note.

THE TARIFF IS NEVER GUESSED. A card is written only when the scheme's own
arithmetic lands exactly on the marks the PAPER prints for that part; where
the paper prices a whole question rather than the part, the scheme's own
arithmetic stands alone and nothing is inferred from the difference.

REFUSALS, each a named bucket reported with a count and a real example.
"""
import argparse
import collections
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import lcvp_lib as L                                          # noqa: E402
from align import bag as A_BAG, score as A_SCORE               # noqa: E402
from lcvp_topics import concept_for, topic_for                # noqa: E402

OUT = os.path.join(ROOT, 'scripts/markbank/authored/lcvp.json')
# The build refuses a menu longer than this outright; see groupFault() in
# build-deck.mjs and MAX_LONG_OPTION_ROWS in optionCap.mjs.
HARD_OPTION_CAP = 16
# An option this long is a slice that ran past its answer; see
# MAX_OPTION_CHARS in markbank_authoring.py.
MAX_OPTION_CHARS = 700

GROUP_RE = re.compile(r'\b(\d{1,2})\s*[@x×]\s*(\d{1,2})\s*(?:m\b|marks?\b)?', re.I)
MARKS_RE = re.compile(r'\b(\d{1,3})\s*marks?\b', re.I)
# "3 marks (1+1+1)", "(2+2+1+1)": the SEC splitting one tariff into its pieces.
SPLIT_RE = re.compile(r'\((\s*\d{1,2}(?:\s*\+\s*\d{1,2})+\s*)\)')
# The same addition without brackets: "Two valid reasons 2 + 2 marks".
PLUS_RE = re.compile(r'\b(\d{1,2}(?:\s*\+\s*\d{1,2})+)\s*marks?\b', re.I)
COUNTS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
          'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}
COUNT_RE = re.compile(
    r'\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+'
    r'(?:valid\s+|relevant\s+|other\s+)*'
    r'(answers?|reasons?|points?|terms?|ways?|items?|methods?|steps?|'
    r'explanations?|characteristics?|challenges?|benefits?|advantages?|'
    r'sections?|headings?|factors?|sources?|agenda items?|qualities|skills)\b',
    re.I)

# Text the SEC prints inside a numbered list that is not one of its answers:
# an instruction to the examiner, or a closing "etc." standing alone.
NOT_A_POINT = re.compile(
    r'^(?:etc\.?|and so on|any other\b|accept\b|award\b|allow\b|note:'
    r'|no marks\b|max\b|total\b)\s*$', re.I)
# The count phrase itself — "Three valid answers", "Two terms explained".
# It prices the list; it is not one of the answers in it.
def _is_count_phrase(text):
    """'Three valid answers' prices the list; it is not one of the answers.

    Anchored on the SEC's own counting vocabulary rather than on a leading
    number: "2 / 3 / 4 years" is the stated answer to how long an
    apprenticeship runs, and a leading-digit rule threw it away.
    """
    text = text.strip()
    m = COUNT_RE.match(text)
    return bool(m) and len(text) <= 55
# "(0/2)" and its relatives price an answer all-or-nothing. It is a note to
# the examiner about the split, not part of the answer.
SPLIT_NOTE = re.compile(r'\(\s*\d+\s*/\s*\d+\s*\)')
# A tariff or a marks cell, wherever it lands. The SEC prints these INSIDE the
# run of prose it is pricing, so a stated answer has to be cut at them: joining
# across one would put "1 mark" in the middle of what a student reads, and the
# provenance gate could not trace the result either — the words either side of
# a removed token are no longer adjacent in the scheme.
TOKEN = re.compile(r'\(?\s*\d{1,2}\s*[@x×]\s*\d{1,2}\s*(?:m\b|marks?\b)?'
                   r'(?:\s*\((?:\d+\s*[+/]\s*)+\d+\))?\s*\)?'
                   r'|\(?\s*\d{1,3}\s*marks?\b\s*\)?'
                   r'|\(\s*\d+\s*/\s*\d+\s*\)', re.I)
# A heading-led answer: "Mentor: A mentor is a person who...". Where the SEC
# answers "explain three of the following terms" it prints one of these per
# term instead of numbering them, and the terms ARE the menu.
HEADED = re.compile(r'(?:^|(?<=[.\s]))([A-Z][^:.]{2,45}:)\s')


# --------------------------------------------------------------- tariffs ----

def menu_tariff(part):
    """(claim, per) for a part whose answers are ONE menu, or None.

    Every form here is printed arithmetic. Nothing is derived from a total
    divided by a count the SEC did not state.
    """
    groups = sorted(set(part.groups))
    if len(groups) == 1:
        return groups[0]
    if len(groups) > 1:
        return None
    for rx in (SPLIT_RE, PLUS_RE):
        m = rx.search(part.head) or rx.search(part.body)
        if not m:
            continue
        addends = [int(x) for x in re.split(r'\s*\+\s*', m.group(1).strip())]
        if len(addends) > 1 and len(set(addends)) == 1:
            return (len(addends), addends[0])
    count = COUNT_RE.search(part.head)
    total = MARKS_RE.search(GROUP_RE.sub(' ', part.head))
    if count and total:
        n, marks = COUNTS[count.group(1).lower()], int(total.group(1))
        if n and marks % n == 0:
            return (n, marks // n)
    # "2 marks (0/2)": the SEC's all-or-nothing cell. The bracket says each
    # answer scores the full two or nothing, and the part is worth two — so
    # ONE answer off the list is what it pays for. Read only where the two
    # numbers agree; the far commoner "2@2m (0/2)" is a group and is read as
    # one above.
    if total:
        marks = int(total.group(1))
        zero = re.search(r'\(\s*0\s*/\s*(\d{1,2})\s*\)', part.head)
        if zero and int(zero.group(1)) == marks:
            return (1, marks)
    return None


def compound_extra(part, menu_worth, target):
    """A component priced beside the menu, as (marks, its stated answer).

    2019 pays one mark for what a CV is used for and three for its headings;
    2024 pays one for the word AGENDA and five for the items under it. Read
    only when the two land EXACTLY on the marks the paper prints for the part
    — otherwise the split is a guess, and this bank has five of those in its
    history.
    """
    if target is None or menu_worth is None or target <= menu_worth:
        return None
    want = target - menu_worth
    head = part.head
    spans = [(m.start(), m.end(), int(m.group(1)))
             for m in MARKS_RE.finditer(head)
             if not any(g.start() <= m.start() < g.end()
                        for g in GROUP_RE.finditer(head))]
    # A second GROUP can price the extra just as a bare marks cell can: 2018
    # pays "2@ 2m (1+1)" for the list and "Two Career Paths-2 routes to same
    # profession 2@2m (1+1)" for the second half of the same ask.
    for m in GROUP_RE.finditer(head):
        if int(m.group(1)) * int(m.group(2)) == want:
            spans.append((m.start(), m.end(), want))
    spans.sort()
    for start, end, value in spans:
        if value != want:
            continue
        before = L.tidy(TOKEN.sub(' ', head[:start]).strip(' .;:,='))
        after = L.tidy(TOKEN.sub(' ', head[end:]).strip(' .;:,='))
        for text in (before, after):
            text = re.sub(r'^\(?[a-z]{1,4}\)\s*', '', text)
            # The last sentence, not the whole head: everything before a
            # component's price includes the ask itself, and the ask is not
            # the answer to it.
            text = L.tidy(re.split(r'(?<=[.?!])\s+', text)[-1])
            if 8 <= len(text) <= 200 and not _is_count_phrase(text):
                return want, text
    return None


# The tariff the SEC prints UNDER the list it prices, which the last answer in
# that list swallows: "3. Place Any 2 @ 1m", "9. Appoint the volunteer and
# assign roles. 4@1m each". Taken off the END only — a token removed from the
# middle would leave two halves that are no longer adjacent in the scheme, and
# the provenance gate reads adjacency.
TRAILING_TARIFF = re.compile(
    r'(?:\s*(?:\bAny\s+\w{1,6}\s+)?\d{1,2}\s*[@x×]\s*\d{1,2}\s*'
    r'(?:m\b|marks?\b)?(?:\s*\((?:\d+\s*[+/]\s*)+\d+\))?'
    r'(?:\s*each)?\s*\)*'
    r'|\s*\(?\s*\d{1,3}\s*marks?\b\s*\)?'
    r'|\s*\(\s*\d+\s*/\s*\d+\s*\)'
    r'|\s*\bRP\b)+\s*[.;:]?\s*$', re.I)


def clean_options(points, year):
    """The scheme's answers, minus what is not an answer, all still traceable."""
    out, untraceable = [], []
    for text in points:
        text = L.tidy(TRAILING_TARIFF.sub('', L.tidy(text)))
        text = L.tidy(text.rstrip(' .;'))
        text = L.tidy(SPLIT_NOTE.sub(' ', text))
        if not text or NOT_A_POINT.match(text) or len(text) < 3:
            continue
        if len(text) > MAX_OPTION_CHARS:
            untraceable.append(text)
            continue
        if not L.traces(year, text):
            untraceable.append(text)
            continue
        if text not in out:
            out.append(text)
    return out, untraceable


def prose_segments(part, qtext, year):
    """The stated answer of a part the SEC did not number, in its own pieces.

    Cut where the SEC's own tariff and marks cells fall, never across them, so
    every piece is contiguous in the scheme and traces there. The ask is
    located by the PAPER's wording, not by counting lines: 2020 prints the
    marks on the answer's line rather than the ask's, and a line rule dropped
    the first of its two stated answers.
    """
    body = L.tidy(part.body)
    tail = None
    for form in ask_forms(qtext):
        tail = L.slice_after(body, form)
        if tail is not None:
            break
    if tail is None and part.cue:
        tail = L.slice_after(body, part.cue)
    if tail is None:
        return []
    out = []
    for piece in TOKEN.split(tail):
        piece = L.tidy((piece or '').strip(' .;:,='))
        if len(piece) < 8 or NOT_A_POINT.match(piece) or _is_count_phrase(piece):
            continue
        if not L.traces(year, piece):
            continue
        if piece not in out:
            out.append(piece)
    return out


def ask_forms(qtext):
    """The ways the SEC may have restated one ask, longest evidence first.

    The paper prints its tariff and its own part markers inside the ask —
    "Explain three of the following terms. (6 marks) (i) mentor (ii) ..." —
    and the scheme restates only the sentence. Matching the whole thing first
    keeps the strongest evidence; the sentence is the fallback.
    """
    text = L.tidy(qtext or '')
    if not text:
        return []
    forms = [text]
    stripped = L.tidy(TOKEN.sub(' ', text))
    if stripped and stripped != text:
        forms.append(stripped)
    sentence = L.tidy(re.split(r'(?<=[.?!])\s+', stripped or text)[0])
    if len(sentence) >= 20 and sentence not in forms:
        forms.append(sentence)
    return forms


def sibling_menu(scheme, paper, year, part_index, used):
    """The definitions the SEC lists under "explain three of the following".

    2018, 2020 and 2021 all set that ask, and all three answer it by defining
    each term in turn. 2020 prints the terms inside one part; 2018 and 2021
    print each under its own roman marker, with the tariff on the parent or on
    the LAST of them. Those are one ask on the paper — the candidate picks
    three of four — so they are one card, at the question, whose options are
    the SEC's own definitions.
    """
    head = scheme.parts[part_index]
    # The shape this reads is one printed ask offering a CHOICE of terms —
    # "Explain three of the following terms" — answered term by term. Without
    # that anchor the same walk turned 2021's Section C Q2 lead-in and its two
    # cue shells into a two-mark menu whose "answers" were the asks.
    if not (re.search(r'of the following', head.cue or '', re.I) or head.groups):
        return None
    section, q = head.address[0], head.address[1]
    siblings = []
    for part in scheme.parts[part_index:]:
        if part.address[0] != section or part.address[1] != q:
            break
        if part.points or part.index in used:
            return None
        if part.address[3] is None and part is not head:
            break
        if part is not head:
            siblings.append(part)
    if len(siblings) < 2:
        return None
    tariffs = {t for p in [head] + siblings for t in set(p.groups)}
    if len(tariffs) != 1:
        return None
    claim, per = next(iter(tariffs))
    options = []
    for part in siblings:
        text = L.tidy(TOKEN.sub(' ', L.tidy(part.body)).strip(' .;:,'))
        if len(text) < 30 or _is_criterion(text) or not L.traces(year, text):
            return None
        options.append(text)
    if len(options) < claim:
        return None
    return claim, per, options, [head] + siblings


# What the examiner must SEE, rather than what the answer is: "Name of career",
# "Two reasons", "Any valid answer". contentFree.mjs refuses these as marking
# points, and a menu built out of them is worse still — it shows a student the
# marking criteria and calls them the answers.
CRITERION = re.compile(
    r'^(?:name|title|heading|any|valid|state|outline|describe|explain|list|'
    r'give|two|three|four|five|six|one|reason|source|method|suggestion|'
    r'answer|agenda|question|layout|sequence|summary|content)\b'
    r'[^.?!]*$', re.I)


def _is_criterion(text):
    return len(text) < 60 and bool(CRITERION.match(text.strip()))


# A tariff cell left inside what a student reads: "Type of Research 1m
# Explanation". It means the slice was cut in the wrong place — the SEC's
# marks column landed in the middle of it — and whatever is either side of the
# cell is not one answer. The provenance gate cannot object, because the text
# really is in the scheme, contiguously.
TARIFF_RESIDUE = re.compile(r'\b\d{1,2}\s*(?:m|marks?)\b|\d\s*[@]\s*\d', re.I)


def _carries_tariff(text):
    return bool(TARIFF_RESIDUE.search(str(text)))


def headed_options(segments):
    """One segment of heading-led answers split into the answers it holds."""
    out = []
    for segment in segments:
        spans = list(HEADED.finditer(segment))
        if len(spans) < 2:
            out.append(segment)
            continue
        if spans[0].start() > 0:
            lead = L.tidy(segment[:spans[0].start()])
            if len(lead) >= 8:
                out.append(lead)
        for i, m in enumerate(spans):
            end = spans[i + 1].start() if i + 1 < len(spans) else len(segment)
            out.append(L.tidy(segment[m.start():end]))
    return [o for o in out if len(o) >= 8]


def notation_for(part):
    if part.notation:
        return part.notation
    m = SPLIT_RE.search(part.head) or PLUS_RE.search(part.head)
    return L.tidy(m.group(0)) if m else ''


def context_note(part, claim, per):
    """What the printed tariff says, in the tariff's own terms."""
    split = SPLIT_NOTE.search(part.head) or SPLIT_NOTE.search(part.body)
    inner = re.search(r'\((\s*\d+\s*(?:\+\s*\d+\s*)+)\)', part.notation or '')
    bits = [f'{claim} answer{"s" if claim > 1 else ""} at {per} '
            f'mark{"s" if per > 1 else ""} each']
    if inner:
        bits.append(f'each split {L.tidy(inner.group(1))}')
    if split:
        bits.append(f'{split.group(0)} — all or nothing on each answer')
    return '; '.join(bits) + '.'


def question_text(paper, key):
    """The ask, from the PAPER, with the tariff the paper prints taken off."""
    text = L.tidy(paper.text(key))
    return L.tidy(re.sub(r'\(?\s*\d{1,3}\s*marks?\s*\)?\s*$', '', text))


def stem_for(paper, key, theme):
    return theme if key[0] == 'A' else paper.stem(key)


def source_for(paper, year, key):
    """Section B's case study, bound as the official source page it is on.

    Every Section B ask is about a case study printed in the paper, and a card
    that shows the ask without it is unanswerable. The pages are read off the
    PDF, never typed.
    """
    if key[0] != 'B':
        return None
    pages = paper.case_study_pages()
    if not pages:
        return None
    return {
        'kind': 'source-text',
        'label': 'OFFICIAL SOURCE',
        'title': 'Section B case study',
        'pages': pages,
        'attribution': f'SEC Link Modules {year} Common Level examination '
                       f'paper — © State Examinations Commission.',
        'presentationNote': 'Read the case study exactly as it appeared in the '
                            'examination paper, then answer the question above.',
    }


def _row_label(part, qtext, claim):
    """A label for the menu, taken from the scheme's own words for it.

    Never the tariff: the build refuses a row whose marking point restates
    what it is worth, because the session never renders that field's arithmetic
    and twelve Business cards spent it saying so.
    """
    cue = L.tidy(re.sub(r'^\(?[a-z]{1,4}\)?\s*', '', part.cue or ''))
    cue = L.tidy(SPLIT_NOTE.sub(' ', cue))
    trimmed = L.tidy(re.sub(r'\b(?:valid|relevant)\b.*$', '', cue, flags=re.I))
    label = (trimmed or cue or L.tidy(qtext)).rstrip(' .:;?')
    # Where the scheme's heading for the list is just the ask restated, the
    # row would print the question back at the student above its own answers.
    if L.normalise(label)[:40] and L.normalise(label)[:40] in L.normalise(qtext):
        return f'Any {claim} of the answers the scheme states'
    if len(label) > 90:
        label = label[:87].rsplit(' ', 1)[0] + '…'
    return f'{label} — any {claim}'


def _notes(parts):
    printed = '; '.join(p.notation or notation_for(p) for p in parts
                        if p.notation or notation_for(p))
    if not printed:
        return ''
    return (f'The scheme prices this ask "{printed}". Its list is what the SEC '
            f'published and is not exhaustive — the scheme\'s own note says '
            f'variations and alternatives may also be acceptable.')


# ------------------------------------------------------------------ build ---

def build(year, refusals, held):
    paper, scheme, sparts, pairs, positional = L.pair(year)
    theme = paper.av_theme()
    by_key = collections.OrderedDict()

    # pairs/positional are keyed by position in the ANCHOR list; the windows
    # below are measured in scheme-part indices, a different numbering.
    anchor_of = {sparts[i].index: pairs[i][0] for i in pairs}
    used = {sparts[i].index for i in list(pairs) + list(positional)}

    # A question that names three things and prices them together — "Planning,
    # good managerial skills and product development ... Outline the importance
    # of each" — is answered as three numbered runs under one address. Only the
    # first pairs; the rest are its siblings and belong to the same card.
    at_address = collections.defaultdict(set)
    for index, key in anchor_of.items():
        at_address[scheme.parts[index].address].add(key)
    for part in scheme.parts:
        if part.index in anchor_of or not part.points:
            continue
        keys = at_address.get(part.address, set())
        if len(keys) != 1:
            continue                     # nothing to attach to, or ambiguous
        key = next(iter(keys))
        cue = part.cue or ''
        heading = '?' not in cue and len(cue) <= 70
        # Or the run repeats the ask the sibling was paired to: 2018 answers
        # "Explain the benefits ... How might poor industrial relations affect
        # the business?" as two lists under one ask, and the first run carries
        # the whole ask as its cue. What must NOT be merged is a run whose cue
        # is a DIFFERENT question — 2021 sets two asks of Section A Q.8 under
        # one head, and the paper prints them as two parts.
        echo = A_SCORE(A_BAG(cue), A_BAG(paper.text(key))) >= 0.4
        if not (heading or echo):
            continue
        anchor_of[part.index] = key
        used.add(part.index)

    for part in scheme.parts:
        if part.index not in anchor_of:
            continue
        key = anchor_of[part.index]
        tariff = menu_tariff(part)
        if tariff is None:
            refusals['the scheme prints no tariff that reads one way'].append(
                (year, part.address, L.ref(year, key),
                 f'{sorted(set(part.groups))} — {part.cue[:60]}'))
            continue
        claim, per = tariff
        options, untraceable = clean_options(part.points, year)
        if untraceable:
            refusals['a marking point does not trace to its own scheme'].append(
                (year, part.address, L.ref(year, key), untraceable[0][:70]))
            continue
        if 0 < len(options) < claim:
            # The SEC prices three explanations and prints one, closing the
            # list with "Etc." A menu that lets a student claim three from one
            # cannot be rendered, but the answer the scheme DID state is still
            # its answer for the marks it printed — so it ships as a stated
            # answer rather than as a menu.
            by_key.setdefault(key, []).append(
                ('prose', part, tariff, options))
            continue
        if not options:
            refusals['the scheme lists no answer the tariff can pay'].append(
                (year, part.address, L.ref(year, key),
                 f'0 answer(s) for {claim} claimable'))
            continue
        if len(options) > HARD_OPTION_CAP:
            held.append((year, part.address, L.ref(year, key),
                         f'{len(options)} options, past the {HARD_OPTION_CAP} '
                         f'the deck may show'))
            options = options[:HARD_OPTION_CAP]
        by_key.setdefault(key, []).append(('menu', part, claim, per, options))

    # ---- second pass: the answers the SEC did not number ------------------
    #
    # Everything between two anchors, in the scheme's own order, is a candidate
    # for the asks between the same two anchors in the paper. A candidate is
    # accepted only when the PAPER's ask can be found in it and something
    # follows — which is the difference between a stated answer and the SEC
    # restating the question.
    for part in scheme.parts:
        # No tariff required ON the head: 2018 prints "Explain three of the
        # following terms. 6 marks", then four definitions, and puts "3@2m
        # (0/2)" under the LAST of them. sibling_menu insists the run holds
        # exactly one tariff between them all, which is the real condition.
        if part.index in used or part.points or part.address[3] is not None:
            continue
        found = sibling_menu(scheme, paper, year, part.index, used)
        if not found:
            continue
        claim, per, options, parts = found
        key = (part.address[0], part.address[1], None, None)
        if key in by_key:
            continue
        for member in parts:
            used.add(member.index)
        by_key[key] = [('menu', part, claim, per, options[:HARD_OPTION_CAP])]

    anchors = sorted((k, i) for i, k in anchor_of.items())
    for key in paper.keys:
        if key in by_key:
            continue
        qtext = question_text(paper, key)
        if not qtext:
            continue
        lo = max([i for k, i in anchors if L.order_key(k) < L.order_key(key)],
                 default=-1)
        hi = min([i for k, i in anchors if L.order_key(k) > L.order_key(key)],
                 default=len(scheme.parts))
        window = [p for p in scheme.parts
                  if lo < p.index < hi and p.index not in used and not p.points]
        for part in window:
            segments = prose_segments(part, qtext, year)
            if not segments:
                continue
            if all(_is_criterion(seg) for seg in segments):
                # The scheme prints only what the examiner must see, because
                # the answer is the candidate's own — their career, their
                # school, the activity their class actually ran.
                refusals['the scheme states no answer — the answer is the '
                         'candidate\'s own'].append(
                    (year, key, L.ref(year, key), segments[0][:70]))
                used.add(part.index)
                break
            tariff = menu_tariff(part)
            headed = headed_options(segments) if tariff else segments
            if tariff and len(headed) >= tariff[0] > 0 and len(headed) > 1 \
                    and not any(_is_criterion(o) for o in headed):
                options, untraceable = clean_options(headed, year)
                if untraceable or len(options) < tariff[0]:
                    continue
                used.add(part.index)
                by_key[key] = [('menu', part, tariff[0], tariff[1],
                                options[:HARD_OPTION_CAP])]
                break
            used.add(part.index)
            by_key[key] = [('prose', part, tariff, segments)]
            break
        else:
            bucket = ('the scheme restates the ask here but states no answer'
                      if window else 'no part of the scheme answers this ask')
            refusals[bucket].append((year, key, L.ref(year, key), qtext[:70]))

    # ---- assemble ---------------------------------------------------------
    cards = []
    for key in sorted(by_key, key=L.order_key):
        entries = by_key[key]
        qtext = question_text(paper, key)
        if not qtext:
            qtext = L.tidy(paper.stem(key))
        if not qtext:
            refusals['the paper prints no text for the ask'].append(
                (year, key, L.ref(year, key), ''))
            continue
        printed = paper.part_marks(key)
        rows, total, parts_used = [], 0, []
        broken = None
        for n, entry in enumerate(entries, start=1):
            if entry[0] == 'menu':
                _tag, part, claim, per, options = entry
                worth = claim * per
                extra = (compound_extra(part, worth, printed)
                         if len(entries) == 1 else None)
                if extra:
                    marks, text = extra
                    if not L.traces(year, text):
                        broken = f'the component "{text[:40]}" does not trace'
                        break
                    rows.append({'id': f'r-{len(rows) + 1}', 'kind': 'point',
                                 'verbatim': text, 'marks': marks,
                                 'openList': True,
                                 'contextNote': f'{marks} mark'
                                                f'{"s" if marks > 1 else ""} '
                                                f'for this, priced on its own '
                                                f'beside the list below.'})
                    total += marks
                rows.append(L.anyN(f'r-{len(rows) + 1}',
                                   _row_label(part, qtext, claim), worth,
                                   claim, per, options,
                                   context_note(part, claim, per)))
                total += worth
                parts_used.append(part)
            else:
                _tag, part, tariff, segments = entry
                worth = (tariff[0] * tariff[1] if tariff else
                         (part.marks if part.marks is not None else printed))
                if worth is None:
                    broken = 'no tariff and no printed marks for a stated answer'
                    break
                rows.append({'id': f'r-{len(rows) + 1}',
                             'kind': 'alt' if len(segments) > 1 else 'point',
                             'verbatim': segments[0], 'marks': worth,
                             'openList': True,
                             'contextNote': _prose_note(part, tariff, worth)})
                if len(segments) > 1:
                    rows[-1]['accepts'] = segments[1:]
                total += worth
                parts_used.append(part)
        residue = next((str(r.get('verbatim')) for r in rows
                        if _carries_tariff(r.get('verbatim', ''))), None) \
            or next((o for r in rows
                     for o in r.get('group', {}).get('options', [])
                     if _carries_tariff(o)), None)
        if residue and not broken:
            broken = f'a marks cell survives inside "{residue[:50]}"'
        if broken:
            refusals['the scheme\'s arithmetic could not be read'].append(
                (year, key, L.ref(year, key), broken))
            continue
        if printed is not None and total != printed:
            refusals['the scheme\'s tariffs do not add to the marks the paper prints'
                     ].append((year, key, L.ref(year, key),
                               f'scheme pays {total}, the paper prints {printed}'))
            continue
        haystack = ' '.join(
            [qtext, stem_for(paper, key, theme)]
            + [str(r.get('verbatim', '')) for r in rows]
            + [o for r in rows for o in r.get('group', {}).get('options', [])])
        topic, _why = topic_for(haystack)
        if not topic:
            refusals['the wording files under no Link Modules unit'].append(
                (year, key, L.ref(year, key), qtext[:70]))
            continue
        single = len(rows) == 1 and rows[0]['kind'] == 'anyN'
        cards.append(L.card(
            L.card_id(year, key), year, key, topic, concept_for(qtext), qtext,
            ' + '.join(notation_for(p) or f'{total} marks' for p in parts_used),
            total, rows, notes=_notes(parts_used),
            stem=stem_for(paper, key, theme),
            tariff_kind='bestNofParts' if single else 'fixed',
            answer=rows[0]['group']['claimMax'] if single else None,
            of_parts=len(rows[0]['group']['options']) if single else None,
            per_part=rows[0]['group']['perOption'] if single else None,
            source_material=source_for(paper, year, key)))
    return cards


def _prose_note(part, tariff, worth):
    if tariff:
        return context_note(part, tariff[0], tariff[1])
    split = SPLIT_NOTE.search(part.body)
    note = f'{worth} mark{"s" if worth != 1 else ""} for this answer'
    if split:
        note += f'; {split.group(0)} — all or nothing'
    return note + '.'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--report', action='store_true')
    args = ap.parse_args()

    refusals = collections.defaultdict(list)
    held, cards = [], []
    for year in L.YEARS:
        cards.extend(build(year, refusals, held))

    seen, problems = {}, []
    for c in cards:
        if c['id'] in seen:
            problems.append(f"duplicate card id {c['id']}")
        seen[c['id']] = c
        problems.extend(L.audit_for(c['section'])([c]))
    if problems:
        for p in problems:
            print('REFUSING', p, file=sys.stderr)
        raise SystemExit('lcvp.json NOT written')

    if args.report:
        total = sum(len(v) for v in refusals.values())
        print(f'{len(cards)} cards, {total} refusal(s), {len(held)} trimmed')
        for bucket, rows in sorted(refusals.items(), key=lambda kv: -len(kv[1])):
            print(f'\n  {len(rows):3d}  {bucket}')
            for row in rows[:4]:
                print(f'         {row}')
        for row in held[:8]:
            print(f'  TRIMMED {row}')
        return

    if args.write:
        with open(OUT, 'w', encoding='utf-8') as fh:
            json.dump(cards, fh, ensure_ascii=False, indent=1)
        print(f'wrote {OUT} ({len(cards)} cards)', file=sys.stderr)
    else:
        json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
