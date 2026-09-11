#!/usr/bin/env python3
"""Author every Physical Education ask whose scheme STATES its answer.

    python3 scripts/markbank/authoring/pe_all.py --report   # covered/741 + buckets
    python3 scripts/markbank/authoring/pe_all.py            # emit JSON
    python3 scripts/markbank/authoring/pe_all.py --write    # authored/ + exclusions/

THE MEASUREMENT THIS SUBJECT TURNS ON.  Physical Education's written paper is
one of three components — the other two are a physical performance and a
coursework project, neither of which this corpus holds and neither of which
any paper prints.  The question that decides the written paper is whether its
scheme prints ANSWERS or BANDS, and it prints both:

    STATED   "Barriers may include: -Facilities -Access -Finance -Influence
              of family -Peer Group"                      (2024 HL Q2(b))
    BAND     "Clear and accurate definition. 2 / Some accuracy in the
              definition. 1"                              (2024 HL Q2(a))

Both are priced; only the first is liftable.  A band ladder states nothing a
student could have written, so it is EXCLUDED with its own printed lines as
the evidence — generated from the scheme reader, never hand-typed — and the
stated parts are carded.  The share swings hard by sitting, which is why the
verdict is counted per sitting and never read off one paper.

WHAT A TARIFF MAY COME FROM.  Only the scheme's own printed arithmetic:

    "8 (2 x 4 marks)"     a menu of answers, two claimable at four each
    "4 x 2 marks"         the same, written without the total
    "2x1marks=2"          the same again, spelled out with its total
    "3 marks + 3 marks"   the same as a repeat
    "2 marks", "1 mark"   one stated answer at its own printed value

Nothing is derived by dividing a total by a count the SEC did not state.  A
part whose tariff cannot be read one way is REFUSED, and every refusal is a
named bucket reported with a count and a real example.

WHAT THE PAPER PRINTS AND THE SCHEME DOES NOT.  Some asks are answered by the
candidate's OWN performance, project or chosen physical activity, and the
scheme prices them by band because there is no answer to print.  Those are
exclusions with evidence, not gaps.  What is a gap is an ask whose scheme
prints a good answer this reader cannot reach; every one of those is reported
OPEN by `--report` and by reconcile.py, and none is quietly dropped.
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
from paper import Paper                                         # noqa: E402
from markbank_authoring import anyN, make_audit, make_card, point  # noqa: E402

OUT = os.path.join(ROOT, 'scripts/markbank/authored/physical-education.json')
EXCLUSIONS = os.path.join(DIR, 'exclusions', 'physical-education.json')
# The build refuses a menu longer than this; see groupFault() in build-deck.mjs.
HARD_OPTION_CAP = 16
MAX_OPTION_CHARS = 700

card = make_card('physical-education', default_section='A')
audit = make_audit(HARD_OPTION_CAP)

# The paper's own page furniture, printed inside a stem.
STEM_JUNK = re.compile(
    r'\s*(?:This question continues on the next page\.?'
    r'|Space for extra work.*$|Do not write on this page.*$'
    r'|Section\s+[ABC]\b.*$|\(\d{1,3}\s*marks?\)'
    r'|Indicate clearly the question number.*$)', re.I)
# A stem that OPENS with the paper's own instruction is the ask itself: the
# walker keeps the stimulus sentence as the part's text and files the
# imperative printed under it as the stem, so 106 of the 741 leaf asks print
# their verb one level away from their own text.
ASK_OPENER = re.compile(
    r'^(what|why|how|when|where|which|who|name|state|give|list|define|explain'
    r'|describe|identify|suggest|outline|discuss|examine|analyse|compare'
    r'|evaluate|justify|complete|write|select|choose|tick|put|match|fill'
    r'|apply|label|comment|account|distinguish|calculate|draw|using|from the)\b',
    re.I)
# An ask the candidate cannot answer without the figure, case study, table or
# printed list beside it. Held rather than shipped blind: a card that quotes
# "Make two statements about doping in cycling based on information presented
# in Figure 12" without Figure 12 is unanswerable.
NEEDS_SOURCE = re.compile(
    r'\b(figure\s*\d|in the (?:figure|table|graph|case study|photograph)'
    r'|shown (?:above|below)|the (?:image|photograph|graph|diagram) above'
    r'|with reference to the case study|from the case study|in the box'
    r'|tick|✓|the data (?:above|below|shown)|the score ?sheet'
    r'|(?:table|diagram) below|listed below|words provided|from above)\b', re.I)
# A card must not cite an ask whose subject lives in a neighbouring part —
# "one of the measures named by you in question 13" answers nothing alone.
BACK_REFERENCE = re.compile(
    r'\bidentified by you in\b|\bnamed by you in\b|\bchosen by you in\b'
    r'|\bstated by you in\b|\boutlined by you in\b|\bcorrectly named in\b'
    r'|\bgiven by you in\b|\bin question \d|\bin part \(|\bin \([ivx]+\)'
    r'|\byou have identified\b|\byou identified\b', re.I)

# An option the SEC prints that is not an answer.
NOT_A_POINT = re.compile(
    r'^(?:etc\.?|and so on|any other\b|other relevant\b|accept\b|award\b'
    r'|allow\b|note:|no marks\b|max\b|total\b|marks?\b|description\b|or\b)\s*$',
    re.I)
TARIFF_RESIDUE = re.compile(r'\b\d{1,2}\s*(?:m|marks?)\b|\d\s*[x×@]\s*\d', re.I)
# The SEC closes most of its lists by saying the list is not closed. That tail
# is not an answer — "Positivity, Excellent negotiation skills and other
# relevant" is one answer and a disclaimer — and the card says the same thing
# in its notes, in the scheme's own words.
OPEN_LIST_TAIL = re.compile(
    r'\s*(?:[,;]\s*)?(?:and|or)?\s*(?:other relevant(?:\s+\w+)?'
    r'|other appropriate(?:\s+\w+)?|any other relevant(?:\s+\w+)?'
    r'|etc\.?|and so on)\s*[.;,]?\s*$', re.I)


def tidy(s):
    return ' '.join((s or '').split())


# ------------------------------------------------------------------ asks ----

_PAPERS = {}


def paper_for(year, level):
    if (year, level) not in _PAPERS:
        _PAPERS[(year, level)] = Paper(L.SUBJECT, year, level)
    return _PAPERS[(year, level)]


def ask_text(year, level, key, census_text):
    """The whole printed ask, in the paper's own words.

    The census keeps what the walker filed under the leaf's own marker. Where
    that is the stimulus and the imperative was filed one level up — which is
    what the walker does when the SEC prints "Physical Education is a concept
    of physical activity." and then "Explain Physical Education in this
    context." as two blocks — the instruction is put back on the end, in the
    order the page prints it. Only an instruction is ever added: a stem that
    does not OPEN with one of the paper's own ask verbs is a table heading, a
    figure caption or a continuation notice, and adding one of those would
    make the question worse rather than whole.
    """
    text = tidy(census_text)
    if ASK_OPENER.match(text):
        return text
    stem = tidy(STEM_JUNK.sub(' ', paper_for(year, level).stem(key[0], key[1]) or ''))
    if stem and ASK_OPENER.match(stem) and stem.lower() not in text.lower():
        return tidy(f'{text} {stem}')
    return text


# --------------------------------------------------------------- answers ----

def options_for(part, year, level, qtext):
    """The scheme's stated answers for one part, as a menu.

    Every option is SLICED from the scheme, checked against the scheme
    markdown the provenance gate reads, and refused if it is the ask's own
    words rather than an answer to it — the SEC reprints the question above
    its table often enough that a reader taking every content line would
    otherwise ship the question as its own answer.
    """
    out, untraceable, restated = [], [], []
    ask = re.sub(r'[^a-z0-9]+', '', (qtext or '').lower())
    for text in S.answers_of(part):
        text = tidy(OPEN_LIST_TAIL.sub('', tidy(text))).strip(' .;,')
        if not text or NOT_A_POINT.match(text) or len(text) < 3:
            continue
        if TARIFF_RESIDUE.search(text) or len(text) > MAX_OPTION_CHARS:
            untraceable.append(text)
            continue
        if not L.traces(year, level, text):
            untraceable.append(text)
            continue
        flat = re.sub(r'[^a-z0-9]+', '', text.lower())
        if flat and ask and flat in ask:
            restated.append(text)         # the ask's own words, not an answer
            continue
        if text not in out:
            out.append(text)
    # A single answer line holding the SEC's own list — "Facilities; Access;
    # Finance" or "continuous training; weight training; plyometrics" — is that
    # list, not one answer. Split it only where the SEC's own separator is
    # there and every piece still traces to the scheme on its own.
    if len(out) == 1 and re.search(r'[;,]', out[0]):
        for sep in (r'\s*;\s*', r'\s*,\s*'):
            pieces = [tidy(x).strip(' .;,') for x in re.split(sep, out[0])]
            pieces = [p for p in pieces if 3 <= len(p) <= 90]
            if len(pieces) >= 2 and all(L.traces(year, level, p) for p in pieces):
                out = pieces
                break
    return out[:HARD_OPTION_CAP], untraceable, restated


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


def single_tariff(part):
    """The price of a part the scheme answers ONCE, or None.

    Read only where every marks value printed anywhere in the part agrees:
    two different values mean the part is priced in pieces, and choosing
    between them would be inventing a tariff.
    """
    values = set()
    for text in [part.cue] + part.rows + part.answers + part.cells:
        for m in re.finditer(r'(\d{1,2})\s*(?:marks?|m)\b', text or '', re.I):
            values.add(int(m.group(1)))
    if len(values) == 1:
        return next(iter(values))
    return None


# ------------------------------------------------------------------ refs ----

def ref_for(year, level, key):
    q, letter, roman = key
    tail = (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
    return f'{year} {level.upper()} Q{q}{tail}'


def ref_for_many(year, level, keys):
    """The citation for a card that answers SEVERAL of a question's asks.

    Named leaf by leaf, never by the letter or the question above them. A card
    written from a scheme part that prices Q3(b) and Q3(d) covers exactly those
    two, and citing it "2021 OL Q3" would claim (a) and (c) as well — which is
    what made the Q3(c) exclusion report stale, the ledger's way of saying two
    rows of it disagree about the same ask.
    """
    q = keys[0][0]
    tail = ', '.join((f'({letter})' if letter else '')
                     + (f'({roman})' if roman else '')
                     for _q, letter, roman in keys)
    return f'{year} {level.upper()} Q{q}{tail if tail.startswith("(") else ""}'


def card_id(year, level, key):
    q, letter, roman = key
    return f'pe-{year}-{level}-q{q}' + (letter or '') + (roman or '')


def section_of(q, year):
    """The paper's own section for a question number.

    Read from the printed instructions every sitting sets on page 2: Section A
    short answers, Section B the case study, Section C the long questions.
    2020 sat an altered examination whose Section A ran to ten questions and
    whose Section C offered three rather than five, so its boundaries are its
    own.
    """
    if year == 2020:
        return 'A' if q <= 10 else ('B' if q == 11 else 'C')
    return 'A' if q <= 12 else ('B' if q == 13 else 'C')


NOTES = ('The list is what the SEC published and is not exhaustive — the '
         "scheme's own note says the suggestions and examples in it are not "
         'exhaustive and alternative valid answers are acceptable.')


def band_evidence(part):
    """The scheme's own printed lines, so an exclusion cites the document."""
    rows = [r for r in part.rows if not S.TABLE_HEAD.match(r)]
    if part.cue:
        rows = [part.cue] + rows
    return ' / '.join(rows[:4])[:400] or '(the scheme prints no row for this part)'


def row_label(part, claim):
    """A label for the menu, in the scheme's own words for what it pays for."""
    lead = next((r for r in part.rows
                 if S.LEAD_IN.match(r) and len(tidy(r)) > 8), '')
    if not lead:
        lead = next((r for r in part.rows
                     if not S.TABLE_HEAD.match(r) and not S.EXAMINER_NOTE.match(r)
                     and len(S.strip_tariff(r)) > 12), '')
    label = tidy(re.sub(r'\s*[:.]\s*$', '', S.strip_tariff(lead)))
    if not label or len(label) < 8:
        label = f'Any {claim} of the answers the scheme states'
    elif len(label) > 110:
        label = label[:107].rsplit(' ', 1)[0] + '…'
    return label


# ----------------------------------------------------------------- build ----

def build():
    cards, refusals, excluded = [], collections.defaultdict(list), []
    covered, seen_parts = [], {}

    for year, level in L.SITTINGS:
        lvl = 'higher' if level == 'hl' else 'ordinary'
        _paper, _parts, pairs, unpaired, _why = L.pair(year, level)
        texts = {key: ask_text(year, level, key, text)
                 for key, _label, text in L.leaves(year, level)}
        for key, label, _text in unpaired:
            refusals['no scheme part prices this ask'].append(
                (year, level, label, ''))

        # One card per SCHEME PART, not per leaf: where the scheme prices a
        # letter the paper numbers romans under, the ask is inside that part
        # and one card covers every leaf beneath it — which is how
        # reconcile.py reads a citation one level up.
        by_part = collections.OrderedDict()
        for key, (part, route, _sc) in pairs.items():
            by_part.setdefault(id(part), (part, []))[1].append(key)

        for part, keys in by_part.values():
            keys.sort()
            key = keys[0]
            ref = (ref_for(year, level, key) if len(keys) == 1
                   else ref_for_many(year, level, keys))
            qtext = texts.get(part.address) or texts.get(key) or ''
            options, untraceable, restated = options_for(part, year, level, qtext)

            def refuse(bucket, detail=''):
                for k in keys:
                    refusals[bucket].append((year, level, ref_for(year, level, k),
                                             detail))

            if not options:
                # A part whose only stated content is the QUESTION reprinted
                # above its table states no answer either: the SEC sets
                # "Explain two of the following terms: Sports endorsement;
                # Sports merchandising; Sports related advertising" and then
                # a band ladder, and the three terms are what was ASKED. That
                # is the band-only case with the question quoted into it, and
                # it is excluded on the same evidence — unless the ask points
                # at a figure or table, where the answer is on the page rather
                # than in the scheme and the refusal belongs to the figure.
                if S.band_only(part) or (restated
                                         and not NEEDS_SOURCE.search(qtext)):
                    for k in keys:
                        excluded.append({
                            'ref': ref_for(year, level, k),
                            'reason': 'the scheme prices this ask by band '
                                      'descriptor and states no answer'
                                      + (' beyond the question\'s own wording'
                                         if restated else ''),
                            'evidence': band_evidence(part),
                        })
                elif restated and NEEDS_SOURCE.search(qtext):
                    # The scheme names the labels and the paper prints the
                    # diagram they sit on: "Effort (2 marks) / Load (2 marks) /
                    # Fulcrum (2 marks)" answers "Label the load, effort and
                    # fulcrum on the diagram below" only with the diagram.
                    refuse('the ask depends on a figure, table or printed list '
                           'the card cannot show', qtext[:80])
                elif untraceable:
                    refuse('a marking point does not trace to its own scheme',
                           untraceable[0][:70])
                else:
                    refuse('the scheme states nothing this reader can lift',
                           (part.rows or [''])[0][:70])
                continue

            # The build's own floor, mirrored here so the ask lands in a named
            # bucket instead of being dropped after the deck is written:
            # "Figure 16 400m" is a caption the walker kept, not a question.
            if len(qtext) < 16 and not ASK_OPENER.match(qtext):
                refuse('the paper prints no ask text under this key', qtext[:60])
                continue
            if NEEDS_SOURCE.search(qtext):
                refuse('the ask depends on a figure, table or printed list the '
                       'card cannot show', qtext[:80])
                continue
            if BACK_REFERENCE.search(qtext):
                refuse("the ask's subject was chosen in a neighbouring part",
                       qtext[:80])
                continue
            topic = (topic_for(qtext)
                     or topic_for(' '.join(part.rows + part.answers)))
            if topic is None:
                refuse('no LCPE topic matches the wording', qtext[:80])
                continue

            groups = sorted(set(part.tariffs))
            steps = next((st for text in [part.cue] + part.rows + part.cells
                          for st in [S.steps_in(text or '')] if st), [])
            total = part.total
            if len(groups) == 1 and len(options) >= groups[0][0]:
                claim, per = groups[0]
                total = claim * per
                rows = [anyN('r-1', row_label(part, claim), total, claim, per,
                             options,
                             f'{claim} answer{"s" if claim > 1 else ""} at {per} '
                             f'mark{"s" if per > 1 else ""} each, as the scheme '
                             f'prices it.')]
                notation = f'{claim} x {per} marks'
                kind, answer, of_parts, per_part = ('bestNofParts', claim,
                                                    len(options), per)
            elif steps and len(options) >= len(steps):
                # A DESCENDING tariff: the SEC's own note says the first
                # correct answer is worth the first step and each later one
                # the next. It is not a best-of, so it rides perOptionSteps.
                claim = len(steps)
                total = sum(steps)
                rows = [anyN('r-1', row_label(part, claim), total, claim,
                             steps[0], options,
                             'The scheme pays '
                             + ' then '.join(f'{m}' for m in steps)
                             + ' marks, in the order the answers are credited.',
                             steps=steps)]
                notation = ' + '.join(str(m) for m in steps) + ' marks'
                kind, answer, of_parts, per_part = 'fixed', None, None, None
            elif total is not None and len(options) == 1 \
                    and single_tariff(part) == total:
                rows = [point('r-1', options[0], total, '')]
                notation = f'{total} marks'
                kind, answer, of_parts, per_part = 'fixed', None, None, None
            elif total is not None:
                # The scheme prices the PART and states its answers without
                # ever saying what each is worth — a shape `questionTotal`
                # exists for. What a student may claim is bounded by the
                # printed total, and no per-answer value is invented.
                rows = [point(f'r-{i + 1}', text, None, '')
                        for i, text in enumerate(options[:16])]
                notation = f'{total} marks'
                kind, answer, of_parts, per_part = ('questionTotal', None,
                                                    None, None)
            else:
                refuse('the scheme prints no tariff that reads one way',
                       f'{sorted(set(part.tariffs))}')
                continue

            cid = card_id(year, level, part.address if len(keys) > 1 else key)
            if cid in seen_parts:
                refuse('a second scheme part claims an id already written',
                       seen_parts[cid])
                continue
            seen_parts[cid] = ref
            built = card(
                cid, year, lvl, topic, concept_for(topic, qtext), ref, qtext,
                notation, total, rows, NOTES,
                section=section_of(part.address[0], year), tariff_kind=kind,
                answer=answer, of_parts=of_parts, per_part=per_part)
            if kind == 'questionTotal':
                # The type is `{ kind: 'questionTotal' }` and nothing else: the
                # scheme states no split, so the card must not carry fields
                # that imply one.
                built['tariffModel'] = {'kind': 'questionTotal'}
            cards.append(built)
            covered.extend(keys)

    return cards, refusals, excluded, covered


def report():
    cards, refusals, excluded, covered = build()
    problems = audit(cards)
    total = sum(len(L.leaves(y, lv)) for y, lv in L.SITTINGS)
    n_open = total - len(covered) - len(excluded)
    print(f'{len(covered)}/{total} leaf asks covered by {len(cards)} card(s); '
          f'{len(excluded)} excluded; {n_open} open')
    print('\nOPEN BUCKETS')
    for bucket, rows in sorted(refusals.items(), key=lambda kv: -len(kv[1])):
        print(f'  {len(rows):>4}  {bucket}')
        print(f'          e.g. {rows[0]}')
    if problems:
        print('\nAUDIT')
        for p in problems[:20]:
            print('  ', p)
    by_year = collections.Counter((c['year'], c['level']) for c in cards)
    print('\nCARDS BY SITTING')
    for k in sorted(by_year):
        print(f'  {k[0]} {k[1]:<9}{by_year[k]}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    if args.report:
        report()
        return
    cards, refusals, excluded, covered = build()
    problems = audit(cards)
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
