#!/usr/bin/env python3
"""Author every Physical Education ask whose scheme STATES its answer.

    python3 scripts/markbank/authoring/pe_all.py --report   # counts, refusals
    python3 scripts/markbank/authoring/pe_all.py            # emit JSON
    python3 scripts/markbank/authoring/pe_all.py --write    # authored/physical-education.json

THE MEASUREMENT THIS SUBJECT TURNS ON.  Physical Education had never been
assessed by this bank.  Its written paper is one of three components — the
other two are a physical performance and a project, neither of which the corpus
holds — and the question that decides it is whether the written paper's scheme
prints ANSWERS or BANDS.

It prints both, and the split is countable.  Of the 824 parts the thirteen
schemes print, 187 state an answer a student could have written and 637 print a
band ladder and nothing else:

    STATED   "Barriers may include: -Facilities -Access -Finance -Influence of
              family -Peer Group"                       (2024 HL Q2(b))
    BAND     "Clear and accurate definition. 2 / Some accuracy in the
              definition. 1"                            (2024 HL Q2(a))

Both are priced; only the first is liftable.  A band ladder states nothing a
student could have written, so it is EXCLUDED with its own printed line as the
evidence — generated from this reader, never hand-typed — and the stated parts
are carded.  The share swings hard by sitting (56% of 2021 Higher, 4% of 2025
Higher), which is why the verdict had to be counted per sitting and not read
off one paper.

WHAT A TARIFF MAY COME FROM.  Only the scheme's own printed arithmetic:

  "6 (2 x 3 marks)"        a menu of answers, two claimable at three each
  "2 x 2 marks"            the same, written without the total
  "3 marks + 3 marks"      the same again, spelled out as a repeat
  "1 mark", "2 marks"      one stated answer at its own printed value

Nothing is derived by dividing a total by a count the SEC did not state.  A
part whose tariff cannot be read one way is REFUSED, and every refusal is a
named bucket reported with a count and a real example.

WHERE THIS STANDS, AND WHAT IS LEFT.  Nothing has been shipped from here yet
and NOTHING SHOULD BE until the ledger closes: the deck is not registered in
components/MarkBank/deck.ts, the subject is not in paper_census.SUBJECTS, and
no exclusions file has been written, so `reconcile.py --all` does not see it
and CI is untouched.  The state today, against a census denominator of 741
leaf asks over 13 papers:

    51   cards this reader will write
   477   band-only exclusions, each carrying the scheme's own printed line
   ~213  OPEN, in the buckets `--report` prints

The open set is READER FAULT, not content — the same shape Engineering's
41.6% has.  In descending size:

  149  a scheme part that pairs to no printed ask.  Three routes are tried
       already (wording, identical printed shape, printed order under equal
       counts); 149 of 824 parts still fail all three, and 24 of those carry
       content.  A fourth route — the paper's own printed question total
       against the scheme's — is the next thing to try.
   40  the scheme states an answer this reader cannot lift, mostly 2022,
       whose tables come back welded into single pymupdf blocks.
   40  the scheme prints no tariff that reads one way.  The commonest shape
       is a part priced in TWO pieces — "Identifies two key patterns 1 mark +
       1 mark" then "Brief description of each pattern 2 marks + 2 marks" —
       which is two rows of one card, not an ambiguity, and wants a compound
       reading rather than a refusal.
   14  the ask depends on a figure the card cannot show.  These are real and
       want crop-question-art.py, not a reader change.

Do the first three before writing anything: a deck of 51 cards on a 741-ask
paper is thinner than any subject in this bank, and the number that matters is
covered/N, never the card count.
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

import pe_lib as L                                              # noqa: E402
import pe_scheme as S                                           # noqa: E402
from pe_topics import concept_for, topic_for                    # noqa: E402
from markbank_authoring import anyN, make_audit, make_card, point  # noqa: E402

OUT = os.path.join(ROOT, 'scripts/markbank/authored/physical-education.json')
EXCLUSIONS = os.path.join(DIR, 'exclusions', 'physical-education.json')
# The build refuses a menu longer than this; see groupFault() in build-deck.mjs.
HARD_OPTION_CAP = 16
MAX_OPTION_CHARS = 700

card = make_card('physical-education', default_section='A')
audit = make_audit(HARD_OPTION_CAP)

# An ask the candidate cannot answer without the figure, case study or data
# table printed beside it.  Held rather than shipped blind: a card that quotes
# "Make two statements about doping in cycling based on information presented
# in Figure 12" without Figure 12 is unanswerable.
NEEDS_SOURCE = re.compile(
    r'\b(figure\s*\d|in the (?:figure|table|graph|case study|photograph)'
    r'|shown (?:above|below)|the (?:image|photograph|graph|diagram) above'
    r'|with reference to the case study|from the case study|in the box'
    r'|tick|✓|the data (?:above|below|shown)|the score ?sheet)\b', re.I)
# A card must not cite an ask whose stem lives in a neighbouring part —
# "one of the measures named by you in question 13" answers nothing alone.
BACK_REFERENCE = re.compile(
    r'\bidentified by you in\b|\bnamed by you in\b|\bchosen by you in\b'
    r'|\bin question \d', re.I)

# Options and points the SEC prints that are not answers.
NOT_A_POINT = re.compile(
    r'^(?:etc\.?|and so on|any other\b|accept\b|award\b|allow\b|note:'
    r'|no marks\b|max\b|total\b|marks?\b|description\b)\s*$', re.I)
TARIFF_RESIDUE = re.compile(r'\b\d{1,2}\s*(?:m|marks?)\b|\d\s*[x×@]\s*\d', re.I)
TRAILING_TARIFF = re.compile(
    r'(?:\s*\(?\s*\d{1,2}\s*[x×@]\s*\d{1,2}\s*(?:m\b|marks?\b)?\s*\)?'
    r'|\s*\(?\s*\d{1,3}\s*marks?\b\s*\)?'
    r'|\s*\d{1,2}\s*[-–]\s*\d{1,2}\s*m\b)+\s*[.;:]?\s*$', re.I)


def tidy(s):
    return ' '.join((s or '').split())


# --------------------------------------------------------------- tariffs ----

def menu_tariff(part):
    """(claim, per) for a part answered by ONE menu, or None.

    Every reading is the SEC's printed arithmetic. Where the part prints more
    than one distinct group the reading is ambiguous and the part is refused.
    """
    groups = sorted(set(part.tariffs))
    if len(groups) == 1:
        return groups[0]
    return None


def single_answer_tariff(part):
    """The price of a part the scheme answers ONCE, or None.

    2021 Higher answers "Explain the frontal plane of movement from a
    biomechanical perspective" with one sentence and prices it twice in the
    same table — "Frontal plane movement explained in detail accurately - 4 m"
    and "4 marks". One answer, one printed value, stated twice: that is the
    SEC's own price for it. Read ONLY where every marks value printed in the
    part agrees, because two different values mean the part is priced in
    pieces and choosing between them would be inventing one.
    """
    values = set()
    for row in part.rows:
        for m in re.finditer(r'(\d{1,2})\s*(?:marks?|m)\b', row, re.I):
            values.add(int(m.group(1)))
    if len(values) == 1:
        return next(iter(values))
    return None


def row_marks(row):
    """The marks the scheme prints at the END of one Description row, or None.

    Taken off the end only. A value in the middle of a row is part of the
    examiner's sentence ("2 mark + 2 marks for explanation"), and reading it as
    the row's price is how a tariff gets invented.
    """
    m = re.search(r'(\d{1,2})\s*marks?\s*$', row, re.I) or re.search(r'\s(\d{1,2})$', row)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------- options ---

def clean_options(part, year, level):
    """The scheme's stated answers, minus what is not one, all still traceable."""
    out, untraceable = [], []
    for text in part.answers:
        text = tidy(TRAILING_TARIFF.sub('', tidy(text))).rstrip(' .;,')
        if not text or NOT_A_POINT.match(text) or len(text) < 3:
            continue
        if TARIFF_RESIDUE.search(text) or len(text) > MAX_OPTION_CHARS:
            untraceable.append(text)
            continue
        if not L.traces(year, level, text):
            untraceable.append(text)
            continue
        if text not in out:
            out.append(text)
    # A single answer line holding the SEC's own list — "Facilities; Access;
    # Finance" or "Video analysis, coach feedback, checklist" — is that list,
    # not one answer. Split it only where the SEC's own separator is there and
    # the pieces are short enough to be items rather than sentences.
    if len(out) == 1 and re.search(r'[;,]', out[0]):
        pieces = [tidy(x).rstrip(' .;,') for x in re.split(r'\s*[;]\s*', out[0])]
        if len(pieces) == 1:
            pieces = [tidy(x).rstrip(' .;,') for x in re.split(r'\s*,\s*', out[0])]
        pieces = [p for p in pieces if 3 <= len(p) <= 90]
        if len(pieces) >= 2 and all(L.traces(year, level, p) for p in pieces):
            out = pieces
    return out[:HARD_OPTION_CAP], untraceable


def stated_points(part, year, level):
    """The answers stated INSIDE the Description rows, with their own marks."""
    out = []
    for row in part.rows:
        said = S.stated(row)
        if not said:
            continue
        said = tidy(TRAILING_TARIFF.sub('', said)).rstrip(' .;,')
        if not said or TARIFF_RESIDUE.search(said) or len(said) > MAX_OPTION_CHARS:
            continue
        if not L.traces(year, level, said):
            continue
        marks = row_marks(row)
        if marks is None:
            continue
        out.append((said, marks))
    return out


# ------------------------------------------------------------------ refs ----

def ref_for(year, level, key):
    q, letter, roman = key
    tail = (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
    return f'{year} {level.upper()} Q{q}{tail}'


def card_id(year, level, key):
    q, letter, roman = key
    return f'pe-{year}-{level}-q{q}' + (letter or '') + (roman or '')


NOTES = ('The list is what the SEC published and is not exhaustive — the '
         "scheme's own note says the suggestions and examples in it are not "
         'exhaustive and alternative valid answers are acceptable.')


# ----------------------------------------------------------------- build ----

def build(report=False):
    cards, refusals, excluded = [], collections.defaultdict(list), []
    covered = collections.Counter()

    for year, level in L.SITTINGS:
        paper, parts, pairs, unpaired, _why = L.pair(year, level)
        lvl = 'higher' if level == 'hl' else 'ordinary'
        for part, sc, why in unpaired:
            refusals['the scheme part cannot be paired to a printed ask'].append(
                (year, level, repr(part), why))

        for key, members in pairs.items():
            covered['asks paired'] += 1
            qtext = tidy(paper.text(*key) or '')
            ref = ref_for(year, level, key)

            # WHAT THE SCHEME SAYS IS ASKED FIRST. Every gate below refuses a
            # card for a reason about the PAPER, and applying them first put
            # asks in those buckets whose scheme prints nothing anyway —
            # 128 "no topic matches" that were band ladders. A refusal bucket
            # has to count what it says it counts.
            part = members[0]
            options, untraceable = clean_options(part, year, level)
            points = stated_points(part, year, level)
            if not options and not points:
                if untraceable:
                    refusals['a marking point does not trace to its own '
                             'scheme'].append((year, level, ref, untraceable[0][:70]))
                elif S.band_only(part):
                    excluded.append({
                        'ref': ref,
                        'reason': 'the scheme prices this ask by band descriptor '
                                  'and states no answer',
                        'evidence': _band_evidence(part),
                    })
                else:
                    refusals['the scheme states nothing this reader can '
                             'lift'].append((year, level, ref, (part.rows or [''])[0][:70]))
                continue

            covered['asks the scheme answers'] += 1
            if len(qtext) < 12:
                refusals['the paper prints no ask text under this key'].append(
                    (year, level, ref, qtext[:60]))
                continue
            if NEEDS_SOURCE.search(qtext):
                refusals['the ask depends on a figure, table or case study '
                         'the card cannot show'].append((year, level, ref, qtext[:80]))
                continue
            if BACK_REFERENCE.search(qtext):
                refusals["the ask's subject was chosen in a neighbouring part"].append(
                    (year, level, ref, qtext[:80]))
                continue
            topic = topic_for(qtext) or topic_for(' '.join(part.rows + part.answers))
            if topic is None:
                refusals['no LCPE topic matches the wording'].append(
                    (year, level, ref, qtext[:80]))
                continue

            if len(options) == 1 and not part.tariffs:
                worth = single_answer_tariff(part)
                if worth:
                    rows = [point('r-1', options[0], worth, '')]
                    cards.append(card(
                        card_id(year, level, key), year, lvl, topic,
                        concept_for(topic, qtext), ref, qtext,
                        f'{worth} marks', worth, rows, NOTES,
                        section=_section_of(key[0], year), tariff_kind='fixed'))
                    covered['cards'] += 1
                    continue
            if options:
                tariff = menu_tariff(part)
                if tariff is None:
                    refusals['the scheme prints no tariff that reads one way'].append(
                        (year, level, ref, f'{sorted(set(part.tariffs))}'))
                    continue
                claim, per = tariff
                if len(options) < claim:
                    refusals['the scheme states fewer answers than its tariff '
                             'pays for'].append(
                        (year, level, ref, f'{len(options)} for {claim} claimable'))
                    continue
                total = claim * per
                rows = [anyN('r-1', _row_label(part, qtext, claim), total,
                             claim, per, options,
                             f'{claim} answer{"s" if claim > 1 else ""} at {per} '
                             f'mark{"s" if per > 1 else ""} each, as the scheme '
                             f'prices it.')]
                notation = f'{claim} x {per} marks'
                kind, answer, of_parts, per_part = 'bestNofParts', claim, len(options), per
            elif points:
                total = sum(m for _, m in points)
                if total <= 0:
                    refusals['the scheme states an answer but prices no row'].append(
                        (year, level, ref, points[0][0][:60]))
                    continue
                rows = [point(f'r-{i + 1}', text, marks, '')
                        for i, (text, marks) in enumerate(points)]
                notation = ' + '.join(str(m) for _, m in points) + ' marks'
                kind, answer, of_parts, per_part = 'fixed', None, None, None
            else:
                refusals['the scheme states an answer but prices no row'].append(
                    (year, level, ref, (part.rows or [''])[0][:70]))
                continue

            cards.append(card(
                card_id(year, level, key), year, lvl, topic,
                concept_for(topic, qtext), ref, qtext, notation, total, rows,
                NOTES, section=_section_of(key[0], year), tariff_kind=kind,
                answer=answer, of_parts=of_parts, per_part=per_part))
            covered['cards'] += 1

    return cards, refusals, excluded, covered


def _band_evidence(part):
    """The scheme's own printed lines, so the exclusion cites the document."""
    rows = [r for r in part.rows if not S.TABLE_HEAD.match(r)]
    return ' / '.join(rows[:3])[:300]


def _section_of(q, year):
    """The paper's own section for a question number.

    Read from the paper's printed instructions, which every sitting sets on
    page 2: Section A short answers, Section B the case study, Section C the
    long questions. 2020 sat an altered examination whose Section C offered
    three questions rather than five, so its boundaries are its own.
    """
    if year == 2020:
        return 'A' if q <= 10 else ('B' if q == 11 else 'C')
    return 'A' if q <= 12 else ('B' if q == 13 else 'C')


def _row_label(part, qtext, claim):
    """A label for the menu, in the scheme's own words for its list."""
    lead = next((r for r in part.rows if S.LEAD_IN.match(r)), '')
    label = tidy(re.sub(r'\s*[:.]\s*$', '', lead))
    if not label or len(label) < 6:
        label = f'Any {claim} of the answers the scheme states'
    elif len(label) > 90:
        label = label[:87].rsplit(' ', 1)[0] + '…'
    return label


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()

    cards, refusals, excluded, covered = build()
    problems = audit(cards)

    if args.report:
        print(f'{len(cards)} card(s); {len(excluded)} band-only exclusion(s)')
        print(f'{covered["asks paired"]} paired asks over 13 sittings\n')
        print('REFUSALS')
        for bucket, rows in sorted(refusals.items(), key=lambda kv: -len(kv[1])):
            print(f'  {len(rows):>4}  {bucket}')
            print(f'          e.g. {rows[0]}')
        if problems:
            print('\nAUDIT')
            for p in problems:
                print('  ', p)
        by_year = collections.Counter((c['year'], c['level']) for c in cards)
        print('\nCARDS BY SITTING')
        for k in sorted(by_year):
            print(f'  {k[0]} {k[1]:<9}{by_year[k]}')
        return

    for p in problems:
        print('AUDIT', p, file=sys.stderr)
    if args.write:
        if problems:
            raise SystemExit('refusing to write: the audit is not clean')
        with open(OUT, 'w', encoding='utf-8') as fh:
            json.dump(cards, fh, ensure_ascii=False, indent=1)
        os.makedirs(os.path.dirname(EXCLUSIONS), exist_ok=True)
        with open(EXCLUSIONS, 'w', encoding='utf-8') as fh:
            json.dump(excluded, fh, ensure_ascii=False, indent=1)
        print(f'wrote {len(cards)} card(s) and {len(excluded)} exclusion(s)')
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
