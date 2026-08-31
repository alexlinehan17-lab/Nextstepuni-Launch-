#!/usr/bin/env python3
"""Author every Engineering part the scheme states and prices.

    python3 scripts/markbank/authoring/eng_all.py            # emit JSON
    python3 scripts/markbank/authoring/eng_all.py --report   # counts, refusals

Census-driven, like Computer Science: 806 asks is too many to enumerate by
hand, and every card is the scheme's own text against the paper's own ask.

WHAT THE TARIFF NOTATION MEANS, and the deck convention each maps to. All four
are the paper's own arithmetic; none is inferred.

  "Any two @ 8 + 8"      the candidate picks two from the scheme's list and
  "Any three parts @ 5"  each is worth the same -> an anyN row whose group is
                         the list, claimMax two, perOption eight.

  "3 + 2" with as many   the scheme has priced each point in turn -> one row
  points as terms        per point carrying its own mark.

  "3 + 2" with MORE      the split is ORDERED, not per point: the question
  points than terms      asks for two safety precautions, the scheme lists
                         five, and the first answer given earns 3 and the
                         second 2. Which point it is does not decide its
                         value, so per-row values do not exist -- orderedSplit,
                         rows carrying none, exactly as Chemistry's "ANY TWO:
                         (3 + 2)" already does.

  "5" with one point     one row at five.
  "5" with several       the points are alternatives and any one earns the
                         five -> an alt row.

REFUSALS, each the rule already in force elsewhere:

  * the ask is an option the candidate chooses BETWEEN, not a question. The
    papers print those with roman markers -- "Select any two of the plastic
    materials listed below: (i) Polyvinyl Chloride (PVC), (ii) Nylon," -- and
    the census counts them as leaves because that is what they look like.
  * the scheme states nothing at this key or above it,
  * it prints no tariff that reads one way,
  * the wording files under no syllabus topic.
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

import reconcile as R                                       # noqa: E402
from paper_census import census_subject                     # noqa: E402
from lib import Author, Refused                             # noqa: E402
from eng_scheme import EngScheme                            # noqa: E402
from eng_topics import topic_for, concept_for               # noqa: E402
import cardlint                                             # noqa: E402

MAX_ROWS = 12
# An "ask" that is really one of the options the question lists. It has no
# sentence in it: "Nylon,", "Full hybrid;", "Ferdinand Porsche", "Basin".
NOT_AN_ASK = re.compile(r'^[^.?!]{0,40}[,;.]?$')
# What separates an ask from a list item is not its LENGTH. "Explain the term
# bioplastic." is 28 characters and is the whole question; "Ferdinand Porsche"
# is 17 and is one of three names under "Outline the contribution made by each
# of the following". Refusing everything short refused 256 leaves, among them
# every short imperative in the subject.
#
# The command word is the real signal, and it is DERIVED rather than invented:
# these are the words that open the 550 census leaves too long to be anything
# but an ask, minus the stems that came with them ("nominal", "the", "using"),
# plus sketch/label/indicate, which open one ask each and are imperative in
# the same way. "Select" is excluded -- it opens "Select any two from the
# following", which is a lead-in to options rather than an ask.
COMMAND_WORD = re.compile(
    r'^(?:briefly|calculate|compare|define|describe|determine|differentiate'
    r'|discuss|distinguish|draw|explain|give|identify|indicate|label|list'
    r'|name|outline|sketch|state|suggest)\b', re.I)
# Printed on the page but not stated by anyone: the running footer, and a
# heading that INTRODUCES the marking points rather than being one. Both were
# reaching cards as the whole answer -- "Page 17" for eighteen marks, "A -
# Vacuum forming:" for ten, "Any two:" for twelve.
NOT_A_POINT = re.compile(r'^(?:Page\s+\d+|\d+\s+of\s+\d+)\s*$'
                         r'|^[^.?!]{0,28}:\s*$', re.I)
# The examiner talking to the examiner rather than stating an answer.
CREDIT_RULE = re.compile(
    r'^(?:award|allow|accept|max\b|total\b|note:|any other|or\b'
    # A bare "Any three" is the examiner saying how many of the points
    # below to credit, not one of them. It shipped as a card's whole
    # twelve-mark answer.
    r'|any\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s*[:.]?$)',
    re.I)


def keeps_stem(stem, figure):
    """Whether this card's stimulus prose is worth showing.

    A stem earns its place by saying something the card does not. Once the
    QUESTION FIGURE is bound, the labels printed on that figure no longer do:
    "1400 1000 600 200 C X Temperature °C 723°C 0.83% % Carbon 1 2 3 4 5 6"
    is the axis of the diagram now shown above it, and "defect A defect B" is
    written on the picture itself. What separates them from a real stem is
    that a real one is a SENTENCE -- "Give brief answers to any ten of the
    following:" closes on its colon, and a run of labels closes on nothing.
    """
    text = ' '.join((stem or '').split())
    if not text or cardlint.label_junk(text):
        return False
    if figure and not re.search(r'[.?!:]$', text):
        return False
    return True


def looks_like_an_ask(text):
    t = ' '.join((text or '').split())
    if not t:
        return False
    if len(re.findall(r'[a-z]{3,}', t)) < 4:
        return False
    if COMMAND_WORD.match(t):
        return True
    return not NOT_AN_ASK.match(t) or len(t) > 45


def cardable(points):
    """The marking points a card may claim, the examiner's asides removed."""
    out = []
    for p in points:
        t = ' '.join(p.split())
        if len(t) < 3 or CREDIT_RULE.match(t) or NOT_A_POINT.match(t):
            continue
        out.append(t)
    return out


def cardable_indexed(points):
    """(index, text) into the SCHEME's own list, not into a filtered copy.

    lib.card rebuilds its candidates from the scheme and `use` selects into
    that, so a filtered copy would silently shift every index past the first
    thing removed -- the fault that put a lead-in on nineteen Computer Science
    cards.
    """
    out = []
    for i, p in enumerate(points):
        t = ' '.join(p.split())
        if len(t) < 3 or CREDIT_RULE.match(t) or NOT_A_POINT.match(t):
            continue
        out.append((i, t))
    return out


def resolve(S, q, letter, roman):
    """The nearest PRICED key at or above this leaf, and what it covers.

    Requiring the points and the tariff at the SAME key found 56 cards in 806
    asks, because at Ordinary Level the two are almost never at the same
    depth: the scheme prices the letter and answers its romans.
    """
    # Before climbing to the question: if the question states what EACH of its
    # parts is worth, this part is priced and does not need to climb. Question
    # 1 is answered "any ten of the following" and prices only the question, so
    # every one of its thirteen to eighteen parts resolved to the whole
    # question and one card carried all of them.
    per = S.per_part(q)
    if per and (letter or roman) and not S.tariff(q, letter, roman):
        keep = cardable_indexed(S.points_under(q, letter, roman))
        if keep:
            return (q, letter, roman), keep
    # The same at the LETTER. "Any three parts @ 6 marks" prices each of (b)'s
    # romans at six, so a roman with an answer of its own does not have to
    # climb to (b) and drag its siblings with it. That matters beyond the
    # tariff: a card at (b) carries every roman's text, and one roman saying
    # "shown opposite" refuses the whole part -- 54 of the figure refusals are
    # a parent condemned by one child.
    if roman and letter and not S.tariff(q, letter, roman):
        parent = S.rule(q, letter, None)
        if parent:
            keep = cardable_indexed(S.points_under(q, letter, roman))
            if keep:
                return (q, letter, roman), keep
    for key in ((q, letter, roman), (q, letter, None), (q, None, None)):
        priced = S.tariff(*key)
        if priced:
            keep = cardable_indexed(S.points_under(*key))
            if keep:
                return key, keep
            # PRICED but unanswered is a failure to read THIS key, and
            # climbing past it answers the part with its neighbours' work:
            # 2021 OL Q2(d) asks which metals make solder, bronze and brass,
            # and the question above it answers about three furnaces. The
            # part goes unresolved instead.
            return None, []
    return None, []


def holds(points, n):
    """Whether this prose states N things, however few points it is split into.

    The scheme often writes a multi-part answer as ONE run: "Name the type of
    flame produced for each of the following" is priced three parts at three
    marks and answered "Excess acetylene: Carburising flame Excess oxygen:
    Oxidising flame Equal amounts: Neutral flame" -- all three, on one line.
    Counting the pieces it is punctuated into says whether they are all there,
    and "Material: Rubber" against three materials says they are not.
    """
    parts = [c for c in re.split(r'[;,:]', ' '.join(points))
             if re.search(r'[A-Za-z]{3,}', c)]
    return len(parts) >= n


def rows_for(notation, total, rule, points):
    """(row kind, marks per row, tariff model) for a part, or None to refuse."""
    points = points[:MAX_ROWS]
    if rule:
        n, per = rule
        if n <= len(points):
            return ('anyN', None, {'kind': 'fixed'}, (n, per))
        # Fewer points than parts, but the prose may hold them all.
        if holds(points, n):
            return ('point', None, {'kind': 'questionTotal'}, None)
        return None
    terms = [int(x) for x in re.findall(r'\d{1,2}', notation or '')]
    if len(terms) > 1:
        if len(terms) == len(points):
            return ('point', terms, {'kind': 'fixed'}, None)
        if len(points) > len(terms):
            return ('point', None,
                    {'kind': 'orderedSplit', 'notation': notation}, None)
        # FEWER points than the split names. The scheme has not left anything
        # out -- it has written the whole answer as one run of prose. "Give
        # two reasons why tubular aluminium is used in scaffolding" is priced
        # "3 + 2" and answered "Aluminium tubing has a high strength-to-weight
        # ratio, it is lightweight, resists corrosion...", both reasons in one
        # sentence. The card shows what the scheme wrote and states the total
        # the table prints, and divides nothing.
        #
        # A RULE is different: "Three parts @ 5 marks" against two points
        # means a part really is missing, and a card claiming fifteen marks
        # for two of three parts would be wrong. That stays refused above.
        if holds(points, len(terms)):
            return ('point', None, {'kind': 'questionTotal'}, None)
        # ... and only when the prose really does hold as many clauses as the
        # split names parts. "Calculate Young's modulus for metal A and for
        # metal B" is priced "2 + 2" and the scheme read gives one line,
        # "Young's Modulus of elasticity for metal B = 60 kN/mm²". Metal A's
        # answer is missing, and a card stating four marks over it would be
        # showing half an answer for full marks.
        return None
    if len(points) == 1:
        return ('point', [total], {'kind': 'fixed'}, None)
    # One total, several points, and no split stated anywhere. Treating them
    # as alternatives paid the whole tariff for each — "4" against two points
    # became 4 marks apiece — and lib.card rightly refused it. The scheme has
    # not said how the four are divided, so the card does not say either: it
    # shows the points the scheme states and the total the table prints, and
    # claims nothing in between. Never guess a tariff.
    return ('point', None, {'kind': 'questionTotal'}, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--verdicts', help='write one line per REFUSED leaf, with '
                                       'the reason, for counting where the '
                                       'open asks actually are')
    args = ap.parse_args()

    # The crops question_art.py cut for the parts that point at a picture,
    # keyed by the part they were cut FOR. A card that carries the crop is no
    # longer a ghost, so this is read before the figure gate below.
    figs = {}
    manifest = os.path.join(ROOT, 'components/MarkBank/figures.json')
    if os.path.exists(manifest):
        for key in json.load(open(manifest)):
            m = re.match(r'engineering-(\d{4})-(HL|OL)-paper-q(\d+)'
                         r'([a-hj-z])?((?:i|ii|iii|iv|v|vi|vii|viii)?)-art$', key)
            if m:
                year, level = int(m.group(1)), m.group(2).lower()
                q, le, rm = int(m.group(3)), m.group(4) or None, m.group(5) or None
                figs[(year, level, q, le, rm)] = key
                # The picture is printed ONCE for the part that owns it, and
                # every part beneath it may show it -- 2021 HL Q2(d) prints
                # one hybrid vehicle diagram, (d)(i) identifies it and (d)(ii)
                # describes its operation from the labels on it. Registering
                # the letter as well is what lets the siblings find it.
                if rm:
                    figs.setdefault((year, level, q, le, None), key)

    idx = R.leaf_index(census_subject('engineering'))
    cards, refused = [], collections.Counter()
    verdicts = []
    examples = collections.defaultdict(list)

    for (year, level, _), leaves in sorted(idx.items()):
        A = Author('engineering', year, level)
        S = EngScheme(year, level)
        seen, noted = set(), set()
        siblings = collections.defaultdict(list)
        for lf in sorted(leaves):
            if lf[1] and lf[2]:
                siblings[(lf[0], lf[1])].append(lf[2])
        for leaf in sorted(leaves):
            q, letter, roman = leaf[0], leaf[1], leaf[2]
            ref = (f'{year} {level.upper()} Q{q}'
                   + (f'({letter})' if letter else '')
                   + (f'({roman})' if roman else ''))
            try:
                ask = A.paper.text(q, letter, roman) or ''
            except Exception:                                # noqa: BLE001
                ask = ''

            def note(reason):
                verdicts.append((year, level, q, letter, roman, ref, reason))
                # A promoted parent is reached once per option beneath it.
                # Counting it each time trebles a single refusal and makes the
                # report read as three problems.
                if ref in noted:
                    return
                noted.add(ref)
                refused[reason] += 1
                examples[reason].append(f'{ref}: {" ".join(ask.split())[:70]}')

            if not looks_like_an_ask(ask):
                # The census counts each roman as a leaf, and under "Discuss
                # the contribution that any one of the following has made to
                # technology:" the romans are Ferdinand Porsche, Hedy Lamarr
                # and Nikolaus Otto. None is an ask; the PARENT is, the
                # student picks one, and the scheme prices the parent "Any one
                # @ 5" with one point per name.
                #
                # A ref shallower than the census covers everything beneath
                # it, so ONE card at the parent answers all three -- and
                # without it neither the parent nor its options are carded at
                # all, because the parent is not a leaf.
                if letter and roman:
                    try:
                        above = ' '.join((A.paper.text(q, letter, None)
                                          or '').split())
                    except Exception:                        # noqa: BLE001
                        above = ''
                    if looks_like_an_ask(above):
                        # The options are part of the parent's ask: without
                        # the three names "Discuss the contribution that any
                        # one of the following has made to technology:"
                        # cannot be answered, and files under no topic
                        # either, because every topic word it has is in the
                        # names. Both halves are printed, and the paper sets
                        # them exactly this way -- lead-in, then the list.
                        items = []
                        for sib in siblings.get((q, letter), ()):
                            try:
                                t = ' '.join((A.paper.text(q, letter, sib)
                                              or '').split())
                            except Exception:                # noqa: BLE001
                                t = ''
                            if t:
                                items.append(t.rstrip(' ;,.'))
                        ref = f'{year} {level.upper()} Q{q}({letter})'
                        ask = f'{above} {"; ".join(items)}.' if items else above
                        roman = None
                    else:
                        note('an option the question lists, not an ask')
                        continue
                else:
                    note('an option the question lists, not an ask')
                    continue
            key, keep = resolve(S, q, letter, roman)
            # A "marking point" that repeats the ask is the scheme naming the
            # part, not answering it. 2021 OL Q6(b) lists cutting fluids,
            # clearance angle and chuck key as the three things to describe,
            # and the scheme heads each answer with the same words; taken as
            # the answer, the card shows the student the question again.
            # Indices are kept, because `use` selects into the SCHEME's own
            # list and a filtered copy shifts every one past the first drop.
            bare = re.sub(r'[^a-z0-9]', '', ask.lower())
            keep = [(i, t) for i, t in keep
                    if len(t) > 60
                    or re.sub(r'[^a-z0-9]', '', t.lower()) not in bare]
            points = [t for _, t in keep]
            if not key:
                note('the scheme states and prices nothing at this key or above')
                continue
            if key in seen:
                continue
            lead = S.lead(*key) or ''
            # The ask decides ALONE first. Blending the scheme's lead into
            # the same haystack let the lead outvote the question: "Draw the
            # electronic symbol for each electronic component named" filed
            # under Metrology, and "Identify any two lubricants commonly used
            # when machining" under Plastics. Each source is consulted in turn,
            # nearest first, and the first one that shelves the part wins.
            topic = None
            for source in (ask, f'{ask} {lead}'):
                topic, _ = topic_for(source)
                if topic:
                    break
            if not topic:
                # A part's own words are often too generic to shelve it --
                # "Label the main parts of the furnace" names no furnace --
                # and the QUESTION says which. Consulted only as a fallback,
                # so the ask decides whenever it can: a safety part under a
                # heat-treatment question is a safety part.
                # The QUESTION head carries no text of its own in this
                # subject -- the context sits on the parent PART, which is
                # where "Select one of the furnaces shown at Q2(a) above"
                # lives -- so the walk goes up one level at a time.
                for above in ((q, letter, None), (q, None, None)):
                    if above == (q, letter, roman):
                        continue
                    try:
                        parent = A.paper.text(*above) or ''
                    except Exception:                        # noqa: BLE001
                        continue
                    topic, _ = topic_for(parent)
                    if topic:
                        break
            if not topic:
                note('files under no syllabus topic')
                continue
            # Card lint's own two gates, applied BEFORE the card is written
            # rather than after it is flagged. Engineering asks about printed
            # matter constantly -- "Describe, with the aid of a diagram(s), a
            # suitable mechanism", "Identify the crystal structures A, B and
            # C" -- and this subject has had no figure pass yet, so a card
            # that points at a picture it cannot show is refused.
            stem = ''
            try:
                stem = A.paper.stem(q, key[1]) or A.paper.stem(q) or ''
            except Exception:                                # noqa: BLE001
                pass
            # The same join lib.card will make. A part that is only a cue --
            # "Answer any three of the following:" -- hands its ask to the
            # romans beneath it, and the diagram reference arrives from one of
            # THEM: checking the cue alone let three cards through pointing at
            # a mechanism they could not show.
            whole = ask
            if key[2] is None and len(' '.join(ask.split())) < 40:
                # lib.card's own rule, copied so the two agree: the children
                # of the CITED key, which for a whole-question card is every
                # lettered part beneath it.
                kids = sorted((k for k in A.paper.parts
                               if k[0] == q
                               and (k[1] == key[1] if key[1]
                                    else k[1] is not None or k[2])
                               and (k[1], k[2]) != (key[1], key[2])),
                              key=lambda k: (k[1] or '', k[2] or ''))
                whole = ' '.join([ask] + [(A.paper.text(*k) or '') for k in kids])
            joined = ' '.join(f'{stem} {whole}'.split())
            figure = (figs.get((year, level, q, key[1], key[2]))
                      or figs.get((year, level, q, letter, roman))
                      or figs.get((year, level, q, key[1], None)))
            if not figure and (
                    (cardlint.FIG_REF.search(joined)
                     and not cardlint.SELF_WORK.search(joined)
                     and not cardlint.NO_DEPENDENCY.search(joined))
                    or cardlint.NAMES_LETTERS.search(joined)):
                note('points at printed matter the card cannot carry')
                continue
            # A card that NAMES a lettered part needs the letters decoded as
            # well as shown, which is what card lint asks for and what this
            # author cannot supply. Refusing here rather than letting the deck
            # build drop it keeps the authored file and the deck the same.
            if cardlint.NAMES_LETTERS.search(joined):
                note('names a lettered part this author cannot decode')
                continue
            tariff_here = S.tariff(*key)
            notation_here = S.notation(*key)
            rule_here = S.rule(*key)
            if tariff_here is None and (key[1] or key[2]):
                # Priced by the question's "@ N marks each", or by the
                # letter's "Any three parts @ 6 marks" -- either way it is
                # what this part is worth and what the scheme printed.
                per = S.per_part(key[0])
                if not per and key[2] and key[1]:
                    up = S.rule(key[0], key[1], None)
                    per = up[1] if up else None
                if per:
                    tariff_here, rule_here = per, None
                    notation_here = f'{per} marks'
            shape = rows_for(notation_here, tariff_here, rule_here, points)
            if not shape:
                note('the printed split does not fit the points stated')
                continue
            kind, marks, model, group = shape
            cid = (f'eng-{year}-{level}-q{q}'
                   + (f'-{key[1]}' if key[1] else '')
                   + (f'-{key[2]}' if key[2] else ''))
            try:
                if kind == 'anyN':
                    n, per = group
                    A.card(*key, topic=topic, concept=concept_for(ask),
                           source='table', card_id=cid,
                           use=[[i for i, _ in keep[:MAX_ROWS]]],
                           marks=[n * per], tariff='fixed',
                           row_kind='anyN', total=n * per, question_figure=figure,
                           stem=keeps_stem(stem, figure),
                           notes=f'The scheme prints {notation_here!r}.')
                elif model['kind'] == 'orderedSplit':
                    # Rows carry no marks and the total is given, which is the
                    # shape lib already has for a scale: `ladder`. Which point
                    # it is does not decide its value, so inventing one per row
                    # is the thing being avoided.
                    A.card(*key, topic=topic, concept=concept_for(ask),
                           source='table', card_id=cid,
                           use=[i for i, _ in keep[:MAX_ROWS]],
                           tariff='orderedSplit', question_figure=figure,
                           notation=model['notation'],
                           ladder=tariff_here,
                           stem=keeps_stem(stem, figure))
                elif model['kind'] == 'questionTotal':
                    A.card(*key, topic=topic, concept=concept_for(ask),
                           source='table', card_id=cid,
                           use=[i for i, _ in keep[:MAX_ROWS]],
                           tariff='questionTotal', question_figure=figure,
                           total=tariff_here,
                           stem=keeps_stem(stem, figure),
                           notes=f'The scheme prints {notation_here!r}.')
                else:
                    A.card(*key, topic=topic, concept=concept_for(ask),
                           source='table', card_id=cid,
                           use=[i for i, _ in keep[:MAX_ROWS]],
                           marks=marks, tariff='fixed', question_figure=figure,
                           total=tariff_here,
                           stem=keeps_stem(stem, figure))
                # Card lint reads the text the CARD carries, which lib builds
                # from the key's own ask with its children joined on.
                # Rebuilding that here to guess at it was wrong in both
                # directions, so the finished card is tested with card lint's
                # own condition and withdrawn if it points at a picture it
                # cannot show. Twenty-one Engineering cards were shipping that
                # way -- "Identify the hybrid vehicle configuration shown
                # opposite", with nothing opposite.
                made = A.cards[-1] if A.cards else None
                # A card that NAMES lettered parts needs those letters
                # DECODED as well as shown, and this author cannot supply a
                # label key. Having a figure is not enough: the deck build
                # drops such a card, and a card the author writes and the
                # build throws away leaves the authored file and the deck
                # disagreeing about what the subject holds.
                if made is not None:
                    final = f'{made.get("stem") or ""} {made.get("questionText") or ""}'
                    if cardlint.NAMES_LETTERS.search(final) \
                            and not made.get('labelKey'):
                        A.cards.pop()
                        note('names a lettered part this author cannot decode')
                        continue
                if made is not None and not (made.get('figureKey')
                                            or made.get('questionFigureKey')):
                    stem_t = made.get('stem') or ''
                    qtext = made.get('questionText') or ''
                    final = f'{stem_t} {qtext}'
                    hit = cardlint.FIG_REF.search(final)
                    table_only = bool(hit) and re.search(
                        r'(?:table|chart|graph)\b', hit.group(0), re.I) \
                        and cardlint.INLINE_TABLE.search(final)
                    ghost = (hit and not cardlint.SELF_WORK.search(final)
                             and not cardlint.NO_DEPENDENCY.search(final)
                             and not table_only)
                    lettered = (cardlint.NAMES_LETTERS.search(qtext)
                                and not cardlint.INVITES_DRAWING.search(qtext))
                    if ghost or lettered:
                        A.cards.pop()
                        note('points at printed matter the card cannot carry')
                        continue
                seen.add(key)
            except Refused as exc:
                note(str(exc).split(':', 1)[-1].strip()[:60])
        cards.extend(A.cards)

    if args.verdicts:
        with open(args.verdicts, 'w', encoding='utf-8') as fh:
            json.dump([{'year': v[0], 'level': v[1], 'q': v[2], 'letter': v[3],
                        'roman': v[4], 'ref': v[5], 'reason': v[6]}
                       for v in verdicts], fh, indent=1)
        print(f'wrote {args.verdicts}: {len(verdicts)} refusals')
    if args.report:
        total = sum(len(v) for v in idx.values())
        print(f'{len(cards)} card(s) from {total} asks')
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
