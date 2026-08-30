#!/usr/bin/env python3
"""Author every Computer Science part the scheme states and prices.

    python3 scripts/markbank/authoring/cs_all.py            # emit JSON
    python3 scripts/markbank/authoring/cs_all.py --report   # counts and refusals

Unlike the other subjects, this one is driven from the CENSUS rather than from
a hand-written work list: 484 asks is too many to enumerate by hand, and every
card here is the scheme's own text against the paper's own ask, so there is
nothing per-card to decide except the topic. What the census says the paper
prints is the list; what cs_scheme states and prices is what can be carded.

Three refusals, all of them the rules already in force:

  * the scheme states nothing at this key,
  * it prints no tariff that reads one way -- see cs_scheme.tariff(), which
    takes the part's own row, then the parent's printed split, then the
    paper's "All questions carry equal marks" rubric, and refuses beyond that,
  * the wording files under no syllabus topic. A wrong shelf sends a student
    to revise the wrong thing; a gap only asks a person to look.

The lead-in "Any response that captures the essence of any of the following:"
is dropped where the scheme prints it. It introduces the marking points and is
not one of them, and a card that opened with it would be quoting the
examiner's instruction to the examiner.
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

import paper as PP                                          # noqa: E402
import reconcile as R                                       # noqa: E402
from paper_census import census_subject                     # noqa: E402
from lib import Author, Refused                             # noqa: E402
from cs_topics import topic_for, concept_for                 # noqa: E402
import cardlint                                             # noqa: E402
import cs_question_figures as CSF                           # noqa: E402

# The examiner's instruction ABOUT the marking points, not one of them.
LEAD_IN = re.compile(r'^(any response that captures|any \w+ of the following|'
                     r'accept any|examples? of|the following are|'
                     r'any \d+ (?:from|of)|marks? awarded for)', re.I)
# Two copies of one maths digit, which is what the text layer returns for a
# scheme set in CambriaMath. The value cannot be recovered from the text: the
# same font mis-maps some digits, so the pair is not necessarily the digit.
DOUBLED_MATHS_DIGIT = re.compile(r'([\U0001D7CE-\U0001D7FF])\1')
# How much of the answer earns what, rather than what the answer is. The
# scheme prints these beside the marking points and they are not among them.
CREDIT_RULE = re.compile(
    r'^(each|every|first|half|some|fully|partially)\b[^.]*\b'
    r'(correct|valid|relevant|response|item|rows?|columns?|pass|'
    r'steps?|solution|conversion|attempt)\b'
    # "Any correct step", "Small calculation error" -- the same thing said the
    # other way round. Partial credit, not an answer.
    r'|^any (correct|valid) (step|response|attempt|conversion|answer|part)'
    r'|^(small|minor|major)\b[^.]*\berrors?\b', re.I)
MAX_ROWS = 12


# An "ask" that is a row of a printed table, a code fragment or a serial-number
# column the paper reader lifted as prose: "GA5 AOK1", "X234 Y56", "8XT A43Y".
# It has no verb and no sentence, and filing it under a topic would be filing
# noise. Refused with its own reason so the count is not read as a gap in the
# topic rules.
NOT_AN_ASK = re.compile(r'^(?=.*[A-Z0-9])(?:[A-Z0-9][A-Za-z0-9]*\s*){1,6}$')


def looks_like_an_ask(text):
    t = ' '.join((text or '').split())
    if not t or NOT_AN_ASK.match(t):
        return False
    return len(re.findall(r'[a-z]{3,}', t)) >= 2


def points_at_printed_matter(joined):
    """Card lint's own two gates, applied before the card is written.

    FIG_REF catches "shown in Figure 3" and "the following code"; NAMES_LETTERS
    catches a question that names a lettered part ("the symbol labelled A")
    without using a figure word at all, which is the case that reaches the deck
    looking answerable and is not.
    """
    return bool(
        (cardlint.FIG_REF.search(joined)
         and not cardlint.SELF_WORK.search(joined)
         and not cardlint.NO_DEPENDENCY.search(joined))
        or cardlint.NAMES_LETTERS.search(joined))


def cardable(points):
    """(index, text) for each marking point a card may claim.

    INDICES, not just text. lib.card builds its own candidate list from the
    scheme and `use` selects into THAT, so returning a filtered copy meant the
    filtering never reached the card: nineteen cards carried a row this
    function had already rejected, one of them opening with "Any response that
    captures the essence of any of the following:" -- the examiner's
    instruction to the examiner.

    Two things are dropped and both are the examiner talking to the examiner:
    the lead-in that introduces the marking points, and the CREDIT RULE that
    says how much of the answer earns what -- "Each correct item", "Half
    correct conversion of (a)", "First full correct response". Those say how
    well, never what, which is the same line cs_scheme.bands() draws.

    A row that is all digits and punctuation is KEPT. It was dropped as table
    noise, and it is the answer at least as often: the scheme states "1111"
    for the largest binary number in a nibble, "7 3" and "6 8" for what a
    program prints, and a trace table's rows for a question that asks for a
    trace table. Dropping them left 2024 OL Q2 claiming six marks for "Half
    correct conversion of (a)", which is not an answer at all.
    """
    out = []
    for i, p in enumerate(points):
        t = ' '.join(p.split())
        if not t or LEAD_IN.match(t) or CREDIT_RULE.match(t):
            continue
        # A doubled maths digit has lost its value. The scheme sets maths in
        # CambriaMath, the text layer returns every glyph twice, and the same
        # font mis-maps some digits: 2021 HL Q2 prints "2^4 = 16" and comes
        # back as 2,2,4,4,=,1,1,1,1, so collapsing the pairs would state
        # "2^4 = 11". The point is dropped and the card keeps its others,
        # rather than the whole card being lost to one unreadable line.
        if DOUBLED_MATHS_DIGIT.search(t):
            continue
        out.append((i, t))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--all', action='store_true',
                    help='list every refusal, not the first three of each')
    args = ap.parse_args()

    # {(year, LEVEL, q): figure key} for the code this question prints, from
    # the figures already bound. A card whose ask points at a listing can only
    # ship if it CARRIES that listing, so the crop decides whether the card
    # exists at all rather than being decoration on one that already did.
    figs = {}
    manifest = os.path.join(ROOT, 'components/MarkBank/figures.json')
    if os.path.exists(manifest):
        for key, meta in json.load(open(manifest)).items():
            if not key.startswith('computer-science-'):
                continue
            # One key per question, whatever its suffix. cs_question_figures
            # publishes a single crop for each question -- the listing, the
            # diagram, or the two joined -- because a card cites a PART and
            # the part cannot be matched to one band on the page. Matching
            # "code0" alone missed every question whose printed matter is a
            # table rather than a program.
            m = re.match(r'computer-science-(\d{4})-(HL|OL)-paper-q(\d+)-\w+$', key)
            if m:
                figs[(int(m.group(1)), m.group(2), int(m.group(3)))] = key

    # The program lines each question's crop carries, so the card's question
    # text can be the ask without the listing run into it.
    listings = {}

    def listing_for(year, level, q):
        key = (year, level.lower(), q)
        if key not in listings:
            # The lines the BOUND crop carries, not every band the question
            # prints. A listing the card does not show is still the only place
            # the student can read it, so taking it out of the question text
            # would leave "Explain what the following code does:" with nothing
            # to explain.
            try:
                chosen = CSF.question_figure(year, level.lower(), q)
            except Exception:                                # noqa: BLE001
                chosen = None
            listings[key] = (chosen[4], chosen[5]) if chosen else ([], [])
        return listings[key]

    idx = R.leaf_index(census_subject('computer-science'))
    cards, refused = [], collections.Counter()
    examples = collections.defaultdict(list)

    for (year, level, _), leaves in sorted(idx.items()):
        A = Author('computer-science', year, level)
        table = A._source('table')
        unpriced = collections.defaultdict(list)
        for leaf in sorted(leaves):
            section, q, letter, roman = leaf[0], leaf[1], leaf[2], leaf[3]
            ref = (f'{year} {level.upper()} Q{q}'
                   + (f'({letter})' if letter else '')
                   + (f'({roman})' if roman else ''))
            try:
                ask = A.paper.text(q, letter, roman) or ''
            except Exception:                                # noqa: BLE001
                ask = ''
            keep = cardable(table.points(q, letter, roman))
            rows = [t for _, t in keep]
            tariff = table.tariff(q, letter, roman)
            topic, _ = topic_for(ask + ' ' + ' '.join(rows))

            def note(reason):
                refused[reason] += 1
                examples[reason].append(f'{ref}: {" ".join(ask.split())[:70]}')

            if not ask.strip():
                note('the paper reader recovers no ask')
                continue
            if not looks_like_an_ask(ask):
                note('the ask is a table row or code fragment, not a question')
                continue
            if not rows:
                # Held for the whole-question pass, not refused: the scheme
                # often states a roman's answer inside its LETTER's block or
                # under the question itself -- 2021 HL Q2(b) prints "(i) 2^4 =
                # 16 unique pieces of information" as one of (b)'s points, and
                # 2025 OL Q8 prints both romans' answers under Q8. A card
                # citing the question covers everything beneath it.
                unpriced[(section, q)].append(leaf)
                continue
            if not tariff:
                # Held for the whole-question pass below rather than refused
                # outright: the QUESTION is priced even where its parts are
                # not, and a card citing the question covers everything
                # beneath it -- reconcile's own rule for a shallower ref.
                unpriced[(section, q)].append(leaf)
                continue
            if not topic:
                note('files under no syllabus topic')
                continue
            # The same rule card lint applies to the shipped deck, applied
            # here so the card is never written rather than written and
            # flagged. Computer Science trips it more than any other subject:
            # its questions print PROGRAMS, and the text layer gives them back
            # as "1 def gcd(a, b): 2 while a != b: 3 if a > b:" -- a listing
            # with its line numbers run into the code. That belongs in a crop,
            # which is a figure pass this subject has not had.
            # Card lint reads the STEM as well as the question text, and the
            # stem is where a shared "such as that shown in Figure 3" lives.
            stem = ''
            try:
                stem = A.paper.stem(q, letter) or A.paper.stem(q) or ''
            except Exception:                                # noqa: BLE001
                pass
            joined = ' '.join(f'{stem} {ask}'.split())
            figure = figs.get((year, level.upper(), q))
            if points_at_printed_matter(joined) and not figure:
                note('points at printed matter the card cannot carry')
                continue
            # A card that NAMES a lettered part needs the letters decoded as
            # well as shown, which is what card lint asks for and what this
            # author cannot supply: the meaning of the letter is usually the
            # answer. Refusing here rather than letting the deck build drop it
            # keeps the authored file and the shipped deck the same thing.
            if cardlint.NAMES_LETTERS.search(joined):
                note('names a lettered part this author cannot decode')
                continue
            if len(keep) > MAX_ROWS:
                keep, rows = keep[:MAX_ROWS], rows[:MAX_ROWS]
            # One mark per point where the tariff divides, else the whole
            # tariff on a single claim. Never a guessed split.
            if len(keep) == 1 or tariff % len(keep):
                use, marks = [keep[0][0]], [tariff]
            else:
                use = [i for i, _ in keep]
                marks = [tariff // len(keep)] * len(keep)
            cid = (f'cs-{year}-{level}-q{q}'
                   + (f'-{letter}' if letter else '')
                   + (f'-{roman}' if roman else ''))
            try:
                A.card(q, letter, roman, topic=topic,
                       concept=concept_for(ask), source='table',
                       use=use, marks=marks, tariff='fixed', card_id=cid,
                       figure=figure,
                       listing=listing_for(year, level, q)[0] if figure else (),
                       printed=listing_for(year, level, q)[1] if figure else (),
                       # A stem that reads as a heap of short tokens IS the
                       # printed table, lifted by the text layer. The crop
                       # carries it properly, so the card drops the text
                       # version rather than showing a student both.
                       stem=not (figure and cardlint.label_junk(stem)))
            except Refused as exc:
                note(str(exc).split(':', 1)[-1].strip()[:60])
        # ── whole-question pass ───────────────────────────────────────────
        # Section A prices the question and states the answer under its parts,
        # and the marks are not split across them. Splitting 5 over two parts
        # is a guess; citing the question is not, and the card then holds what
        # both parts hold. The rows are ONE alt group carrying the question's
        # whole tariff, because claiming a per-part division the scheme never
        # printed is the thing being avoided.
        for (section, q), held in sorted(unpriced.items()):
            tariff = table.tariff(q)
            keep = cardable(table.points(q))
            # Each row here stands on its own rather than being an
            # alternative to the one above it, so a point that does not trace
            # back to the scheme is DROPPED rather than failing the card. That
            # is what the alternatives path already did; when every point
            # became its own row, seven cards died for one untraceable point
            # among several good ones.
            traces, _bad = table.verify([t for _, t in keep])
            traces = set(traces)
            keep = [(i, t) for i, t in keep if t in traces]
            rows = [t for _, t in keep]
            # The same join A.card will make. paper.text() on a question that
            # states nothing of its own returns empty, so checking it here
            # rejected every one of these before the card was even attempted.
            try:
                ask = A.paper.text(q, None, None) or ''
                if len(' '.join(ask.split())) < 40:
                    kids = sorted((k for k in A.paper.parts if k[0] == q
                                   and (k[1] is not None or k[2] is not None)),
                                  key=lambda k: (k[1] or '', k[2] or ''))
                    tail = ' '.join(f'({k[2] or k[1]}) '
                                    f'{(A.paper.text(*k) or "").strip()}'
                                    for k in kids)
                    ask = f'{ask.rstrip()} {tail}'.strip()
            except Exception:                                # noqa: BLE001
                ask = ''
            ref = f'{year} {level.upper()} Q{q}'
            if not (tariff and rows and ask.strip()):
                for _ in held:
                    refused['no tariff that reads one way'] += 1
                continue
            topic, _ = topic_for(ask + ' ' + ' '.join(rows))
            if not topic:
                for _ in held:
                    refused['files under no syllabus topic'] += 1
                continue
            stem = ''
            try:
                stem = A.paper.stem(q) or ''
            except Exception:                                # noqa: BLE001
                pass
            joined = ' '.join(f'{stem} {ask}'.split())
            figure = figs.get((year, level.upper(), q))
            if points_at_printed_matter(joined) and not figure:
                for _ in held:
                    refused['points at printed matter the card cannot carry'] += 1
                continue
            if cardlint.NAMES_LETTERS.search(joined):
                for _ in held:
                    refused['names a lettered part this author cannot decode'] += 1
                continue
            try:
                # ONE ROW PER POINT, and no per-row value. The pass used to
                # make a single alt row carrying the question's whole tariff,
                # which reads as "five marks for any one of these" -- false
                # wherever the question's parts ask different things. 2022 OL
                # Q5 offered "3" (the index part (a) asks for) as an
                # alternative to three limitations of linear search, which is
                # what (b) asks for. The scheme prices the QUESTION and states
                # these points under it; it never says how the marks divide,
                # and the card now says exactly that much.
                A.card(q, None, None, topic=topic, concept=concept_for(ask),
                       source='table', use=[i for i, _ in keep[:MAX_ROWS]],
                       total=tariff, tariff='questionTotal',
                       card_id=f'cs-{year}-{level}-q{q}', figure=figure,
                       listing=listing_for(year, level, q)[0] if figure else (),
                       printed=listing_for(year, level, q)[1] if figure else (),
                       checked='The question states nothing of its own: the '
                               'paper prints the ask only under its parts, and '
                               'the card carries them joined in the paper\'s '
                               'own order, each behind its own marker. That is '
                               'what the paper prints and what this card '
                               'answers, since it cites the question rather '
                               'than either part.')
            except Refused as exc:
                for _ in held:
                    refused[str(exc).split(':', 1)[-1].strip()[:60]] += 1
        cards.extend(A.cards)

    if args.report:
        print(f'{len(cards)} card(s) from {sum(len(v) for v in idx.values())} asks')
        limit = 60 if args.all else 3
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:limit]:
                print(f'             {e}')
        return 0
    print(json.dumps(cards, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
