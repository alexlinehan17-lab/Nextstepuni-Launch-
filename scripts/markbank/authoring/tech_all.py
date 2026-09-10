#!/usr/bin/env python3
"""Author every Technology part the scheme states and prices.

    python3 scripts/markbank/authoring/tech_all.py --report    # counts, refusals
    python3 scripts/markbank/authoring/tech_all.py > scripts/markbank/authored/technology.json

Census-driven, like Engineering and Computer Science: 809 asks is far too many
to enumerate by hand, and every card is the scheme's own text against the
paper's own ask.

WHAT THE PAIRING RESTS ON. Law 4 refuses a join made on the (question, letter,
roman) key alone, and this subject does not need one. The scheme REPRINTS the
question above its answer, so each priced part carries a cue in the question's
own words, and `tech_scheme.cue_score` scores that cue against the paper's ask
for the address the scheme printed. `--report` prints the confirmation rate per
sitting; a part whose cue contradicts its address is refused rather than
carded. Where the scheme prints no cue at all -- it sometimes goes straight to
the answer, "1(c) (i) CAD: Computer aided drawing/drafting" -- the address is
all there is, and those are counted and named separately so the number is
visible rather than assumed.

WHAT THE TARIFF MEANS. The scheme prints one of three shapes and each maps to
one deck convention. None is inferred:

  "(6 marks, 2 + 4)"  over (i) and (ii)   the split names what each part is
                                          worth: (i) 2, (ii) 4 -> a card each,
                                          at its own printed mark.
  "(6 marks, 2+2+2)"  over no parts       the question is one ask with three
                                          named answers -> one card, one row
                                          per answer, at the split's marks.
  "(6 marks)"                             one card at six, rows carrying no
                                          mark of their own (questionTotal).

A split whose term count does not match what the block prints is NOT divided:
the card states the total the scheme prints and claims nothing in between.

REFUSALS, each a named bucket `--report` counts with a real example.
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

import cardlint                                              # noqa: E402
import paper_census as PC                                    # noqa: E402
from tech_scheme import TechScheme, cue_score                # noqa: E402
from tech_topics import topic_for, topic_for_option          # noqa: E402

SUBJECT = 'technology'
MAX_ROWS = 12
# Mirrors MAX_LONG_OPTION_ROWS / MAX_OPTION_ROWS in optionCap.mjs.
CAP = {'A': 8, 'B': 16, 'C': 16}

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}

# A scheme line that states no answer. Each of these shipped as a card's whole
# answer in some other subject before it was gated.
NOT_A_POINT = re.compile(
    r'^(?:any (?:other|valid|two|three|one|four)\b.{0,24}$'
    r'|accept(?:able)?\b.{0,30}$'
    r'|award\b|allow\b|note:|marks? awarded'
    r'|suggested\b.{0,20}$'
    r'|or\b|and\b|etc\.?'
    r'|[^.?!]{0,28}:)\s*$', re.I)

# The running footer, and the page number the extractor leaves welded to a
# marking point's last line.
FOOTER = re.compile(
    r'\s*\d{0,3}\s*Leaving Certificate(?:\s+Examination)?[,\s].*$'
    r'|\s*Technology\s*[-–—]\s*(?:Higher|Ordinary)\s+Level.*$', re.I)

# A cue too short to identify anything: "Modification:", "Calculation:".
MIN_CUE_WORDS = 4
# How much of the scheme's cue the paper's ask must hold before the pairing
# counts as confirmed by wording rather than by address.
CUE_FLOOR = 0.5


def clean(text):
    text = FOOTER.sub('', ' '.join((text or '').split())).strip()
    return ' '.join(text.split())


# The answerbook's ruled writing lines, and the fill-in label that heads each
# of them. Technology prints them INSIDE the question block -- "State the
# meaning of each colour code. Red colour-coded sign: ______ Yellow
# colour-coded sign: ______" -- so they arrive as part of the ask.
BLANK_RULE = re.compile(r'[_\u2581\u00b7.]{3,}')
FILL_LABEL = re.compile(r'\s*[^.?!:]{1,40}:\s*$')


def clean_ask(text):
    """The printed question, with the answerbook's blank lines taken off.

    Not cosmetic. The labels above those blanks repeat the answer's own
    headings, so a scheme line stating the answer -- "Red colour-coded sign:
    Prohibition" -- reads as a REPRINT of the question and the whole answer
    was thrown away with it. Five Ordinary questions lost every marking point
    they had that way.
    """
    raw = text or ''
    text = clean(BLANK_RULE.sub(' ', raw))
    # Only where the answerbook's ruled lines were actually there. A trailing
    # colon is ALSO how a question introduces its own bullet list -- "Explain
    # each of the following in relation to DFA:" -- and stripping that left
    # the word "Explain" as the whole question on two cards, which the build
    # then dropped as too short to stand alone.
    if not BLANK_RULE.search(raw):
        return text
    while True:
        m = FILL_LABEL.search(text)
        # A label follows the sentence it belongs under, or the label before
        # it. Anything else is the question's own words.
        if not m or m.start() == 0 \
                or not re.search(r'[.?!:]\s*$', text[:m.start()]):
            return text
        text = text[:m.start()].strip()


def _tokens(text):
    return re.findall(r"[a-z0-9']+", (text or '').lower())


def split_cue(lines, ask):
    """(the question the scheme reprinted, the marking points under it).

    The scheme sets the ask again above its answer, at the same indent, so
    nothing in the geometry separates them -- the paper's own wording does,
    which is the argument lib.py's _TableSource makes for Chemistry. This
    consumes the paper's ask WORD BY WORD, in order: a scheme line is part of
    the reprint only while its words carry on through the ask from where the
    line before it stopped, and the reprint is over the moment the ask is
    used up.

    Bag-of-words overlap is not enough, and the difference is not cosmetic. A
    calculation's answer reuses the question's own nouns -- "Total energy =
    (50 watts/hour x 4 hours) x 0.15 = 30 watt/hour" against "Calculate the
    total energy a solar panel generates in 4 hours..." -- so every word of it
    is "in the ask" and thirty-nine parts had their whole answer thrown away
    as a reprint. Reading in order stops at the full stop instead.
    """
    ask_words = _tokens(ask)
    cue, points, at = [], list(lines), 0
    while points and at < len(ask_words):
        line_words = _tokens(points[0])
        if not line_words:
            cue.append(points.pop(0))
            continue
        pos, matched = at, 0
        for word in line_words:
            window = ask_words[pos:pos + 12]
            if word in window:
                pos += window.index(word) + 1
                matched += 1
        if pos > at and matched >= max(2, int(0.6 * len(line_words))):
            cue.append(points.pop(0))
            at = pos
        else:
            break
    return ' '.join(cue), points


def cardable(points):
    out = []
    for p in points:
        t = clean(p)
        # A cell of a table the extractor flattened -- "12000", "(EUR)" --
        # states no answer, and the provenance gate rightly refuses it. One
        # WORD is enough to be an answer, though: "Transistor." is the whole
        # of 2024 Higher Q4(i), and demanding two threw it away.
        if len(t) < 4 or NOT_A_POINT.match(t) \
                or not re.search(r'[A-Za-z]{3,}', t):
            continue
        out.append(t)
    return out


def keeps_stem(stem, question):
    """Whether the stimulus above a part is worth showing on its card."""
    text = clean(stem)
    if not text or cardlint.label_junk(text):
        return False
    if len(text) < 20:
        return False
    # The stem repeats the ask on a whole-question leaf: the census hands the
    # same sentence back as both, and printing it twice looks like a defect.
    if text.rstrip('.') in (question or '').rstrip('.'):
        return False
    return True


def leaf_key(section, q, letter, roman):
    return (section, q, letter, roman)


def ref_for(year, level, section, q, letter, roman):
    return (f'{year} {level.upper()} Section {section} Q{q}'
            + (f'({letter})' if letter else '')
            + (f'({roman})' if roman else ''))


def card_id(year, level, section, q, letter, roman):
    return (f'tech-{year}-{level}-{section.lower()}{q}'
            + (letter or '') + (f'-{roman}' if roman else ''))


def rows_for(points, marks, total, cap=MAX_ROWS):
    """(rows, tariff model) for one card, or None to refuse.

    `marks` is the printed split for this card's own answers, when the scheme
    printed one that fits. Otherwise the card states the total and divides
    nothing -- the rule that has cost this bank five incidents when broken.
    """
    points = points[:min(cap, MAX_ROWS)]
    if marks is None and len(points) == 1:
        # One stated answer for a priced part: the part's tariff IS that row's
        # mark. Nothing is divided, so nothing is guessed.
        marks = [total]
    if marks and len(marks) == len(points):
        rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': p, 'marks': m,
                 'openList': True}
                for i, (p, m) in enumerate(zip(points, marks), start=1)]
        return rows, {'kind': 'fixed'}
    rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': p, 'marks': None,
             'openList': True}
            for i, p in enumerate(points, start=1)]
    return rows, {'kind': 'questionTotal'}


ROMAN_ORDER = ['i', 'ii', 'iii', 'iv', 'v']


def block_units(block, leaves, year, level):
    """The cards this priced block should become.

    One per roman where the printed split has a term for each of them -- the
    ordinary case, and the one that gives a student a card per ask. Otherwise
    ONE card for the whole block, citing every leaf under it and stating the
    block's own printed total. That second shape is not a fallback for
    convenience; it is what "never guess a tariff" requires when the split
    names more parts than the scheme printed markers for. 2022 Higher
    Question 13 prices "(6 marks, 2 + 2 + 2)" over (i) and (ii), because (ii)
    itself asks for two things, and no reading of that says what (i) is worth.

    Each unit is (roman or None, the scheme lines, this unit's tariff, the
    census leaf keys it covers).
    """
    section, q, letter = block.section, block.q, block.letter
    romans = block.romans()
    # Per-roman cards need the PAPER to print those romans too. Where it does
    # not -- 2021 Higher Question 8 is one ask on the page and two in the
    # scheme -- the whole-block card is the honest shape: it covers the leaf
    # the paper actually prints instead of citing two the paper does not.
    if romans and all(block.marks_for(r) is not None for r in romans) \
            and all((section, q, letter, r) in leaves for r in romans):
        out = []
        for roman in romans:
            out.append((roman, block.part_lines(roman), block.marks_for(roman),
                        [(section, q, letter, roman)]))
        return out
    # Whole block. Its leaves are whatever the PAPER prints under this
    # address -- the scheme's own roman markers are not to be trusted here,
    # which is half of why this shape exists.
    covered = sorted(
        (k for k in leaves
         if k[0] == section and k[1] == q and k[2] == letter),
        key=lambda k: ROMAN_ORDER.index(k[3]) if k[3] in ROMAN_ORDER else -1)
    if not covered:
        covered = [(section, q, letter, None)]
    return [(None, [t for _, t in block.lines], block.total, covered)]


def joined_ask(covered, leaves):
    """The paper's own wording for every leaf one card covers, in order."""
    if len(covered) == 1:
        return clean_ask(leaves.get(covered[0], ''))
    parts = []
    for key in covered:
        text = clean_ask(leaves.get(key, ''))
        if text:
            parts.append(f'({key[3]}) {text}' if key[3] else text)
    return ' '.join(parts)


def joined_ref(year, level, covered):
    section, q, letter = covered[0][0], covered[0][1], covered[0][2]
    head = (f'{year} {level.upper()} Section {section} Q{q}'
            + (f'({letter})' if letter else ''))
    romans = [k[3] for k in covered if k[3]]
    if not romans:
        return head
    return head + '(' + ')('.join(romans[:1]) + ')' + ''.join(
        f', ({r})' for r in romans[1:])


def figure_index():
    """The inspected crops, keyed by the part they were cut FOR.

    A crop is cut once for a (section, question, letter) and every roman under
    it shows the same picture, because the paper prints it once. Read from the
    manifest bind-figures.mjs wrote, so a crop that was never inspected is not
    in here to be bound.
    """
    figs = {}
    path = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
    if not os.path.exists(path):
        return figs
    with open(path, encoding='utf-8') as fh:
        manifest = json.load(fh)
    for key in manifest:
        m = re.fullmatch(r'technology-(\d{4})-(HL|OL)-paper-sec([ABC])'
                         r'-q(\d{1,2})([a-d])?-art', key)
        if m:
            figs[(int(m.group(1)), m.group(2).lower(), m.group(3),
                  int(m.group(4)), m.group(5))] = key
    return figs


def author(bind_figures=True):
    census = PC.census_subject(SUBJECT)
    # tech_figures.py calls this with the binding OFF, so that its worklist is
    # every part that points at printed matter -- not just the ones still
    # uncovered. A cropper whose candidate set shrinks as its own crops are
    # bound cannot reproduce what it published.
    figures = figure_index() if bind_figures else {}
    cards, refused, examples = [], collections.Counter(), collections.defaultdict(list)
    verdicts = []
    stats = []

    for paper in census['papers']:
        year, level = paper['year'], paper['level']
        # The full printed wording, not the census REPORT's copy of it: that
        # one is truncated to 160 characters for display, and a card built
        # from it ends a question mid-word. The keys are the same walk either
        # way, so the denominator is unchanged.
        keys, texts, _files = PC.census_sections(SUBJECT, year, level)
        leaves = {tuple(k): texts[k] for k in PC.leaves_of(keys)}
        assert set(leaves) == {tuple(l['key']) for l in paper['leaves']}, \
            f'{year} {level}: the authored leaf set is not the census leaf set'
        # census_subject has just walked this sitting, so its stimulus table is
        # the one belonging to these very leaves.
        stems = PC.SECTION_STEMS.get((SUBJECT, year, level), {})
        S = TechScheme(year, level)
        confirmed = cueless = contradicted = 0

        for block in S.priced():
            section, q, letter = block.section, block.q, block.letter
            for roman, lines, total, covered in block_units(block, leaves,
                                                            year, level):
                covered = [k for k in covered if k in leaves] or covered
                ask = clean_ask(joined_ask(covered, leaves))
                ref = joined_ref(year, level, covered)

                def note(reason, ask_text=''):
                    verdicts.append({'year': year, 'level': level, 'ref': ref,
                                     'reason': reason})
                    refused[reason] += 1
                    if len(examples[reason]) < 80:
                        examples[reason].append(f'{ref}: {ask_text[:70]}')

                if not ask:
                    note('the paper prints no ask at this address')
                    continue

                cue, points = split_cue([clean(l) for l in lines], ask)
                score = cue_score(cue, ask)
                cue_words = len(re.findall(r"[a-z']{3,}", cue.lower()))
                if cue_words < MIN_CUE_WORDS:
                    # The part's own cue can be a single word -- 2021 Higher
                    # Q3 marks "'patched'" and "Anti-virus" -- but the BLOCK
                    # reprints the stimulus above them, and the paper prints
                    # the same stimulus as this question's stem. That is a
                    # second document agreeing on which question this is,
                    # which is what Law 4 asks for.
                    head = ' '.join(clean(t) for t in block.head_lines())
                    stem_text = (stems.get((section, q, letter))
                                 or stems.get((section, q, None)) or '')
                    if cue_score(head, stem_text) >= CUE_FLOOR \
                            and len(re.findall(r"[a-z']{3,}", head.lower())) \
                            >= MIN_CUE_WORDS:
                        cue, cue_words = head, MIN_CUE_WORDS
                        score = cue_score(head, stem_text)
                if cue_words >= MIN_CUE_WORDS:
                    if score >= CUE_FLOOR:
                        confirmed += 1
                    else:
                        contradicted += 1
                        note('the scheme cue does not match the paper ask here',
                             ask)
                        continue
                else:
                    cueless += 1
                    if not block.numbered and section == 'A':
                        # Position-numbered AND wordless: nothing but order
                        # supports the pairing, which Law 4 does not accept.
                        note('block number and pairing both rest on order alone',
                             ask)
                        continue

                points = cardable(points)
                if not points:
                    note('the scheme states no marking point for this part', ask)
                    continue
                if not total:
                    note('the scheme prints no tariff for this part', ask)
                    continue

                marks = None
                if roman is None and block.terms \
                        and len(block.terms) == len(points) \
                        and sum(block.terms) == total:
                    marks = block.terms

                stem = stems.get((section, q, letter)) or stems.get((section, q, None)) or ''
                question = clean(ask)
                topic = (topic_for_option(q) if section == 'C'
                         else topic_for(question, stem,
                                        ' '.join(block.head_lines())))
                if not topic:
                    note('files under no syllabus heading', question)
                    continue

                show_stem = clean(stem) if keeps_stem(stem, question) else ''
                joined = f'{show_stem} {question}'
                figure = figures.get((year, level, section, q, letter))
                if not figure and (
                        cardlint.FIG_REF.search(joined)
                        and not cardlint.SELF_WORK.search(joined)
                        and not cardlint.INLINE_TABLE.search(joined)):
                    note('points at printed matter the card cannot carry', question)
                    continue
                if cardlint.NAMES_LETTERS.search(joined) \
                        and not cardlint.INVITES_DRAWING.search(joined):
                    # A question naming labelled points needs those letters
                    # DECODED as well as shown, and the build drops a card that
                    # shows them without a label key. The crop alone is not
                    # enough, so these stay refused even where one exists.
                    note('names a lettered part this author cannot decode', question)
                    continue
                if cardlint.SCHEME_LEAK.search(joined):
                    note('the paper text carries scheme metadata', question)
                    continue
                if len(question) < 16 and len(show_stem) < 20:
                    note('the ask is too short to stand on its own', question)
                    continue

                trimmed = len(points) - min(len(points), CAP[section])
                rows, model = rows_for(points, marks, total, CAP[section])
                shown = sum(r['marks'] or 0 for r in rows)
                if model['kind'] == 'fixed' and shown != total:
                    note('the rows do not sum to the printed tariff', question)
                    continue
                model = dict(model, notation=block.notation)

                note_text = (f'The scheme prints {block.notation!r} for '
                             f'{"this part" if roman else "this question"}.')
                if trimmed:
                    # Disclosed trimming, the skill's own remedy for a menu
                    # over the display cap: the student is told the list goes
                    # on rather than shown a list that quietly stops.
                    note_text += (f' The scheme lists {len(points)} accepted '
                                  f'answers; the first {len(rows)} are shown.')

                cards.append({
                    'id': card_id(year, level, section, q, letter, roman),
                    'topicId': topic,
                    'conceptId': topic.replace('tech-', ''),
                    'level': LEVEL_WORD[level],
                    'year': year,
                    'subjectId': SUBJECT,
                    'section': section,
                    'questionRef': ref,
                    'questionText': question,
                    'stem': show_stem,
                    'figureKey': '',
                    # The SEC's own print of the picture the ask points at,
                    # shown BEFORE the reveal. A question figure may be shared
                    # by the siblings under one part, which is right here: the
                    # paper prints the picture once for the whole question.
                    'questionFigureKey': figure or '',
                    'labelKey': [],
                    'tariffModel': model,
                    'totalMarks': total,
                    'rows': rows,
                    'notes': note_text,
                })

        stats.append((year, level, confirmed, cueless, contradicted))

    return cards, refused, examples, verdicts, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--verdicts')
    args = ap.parse_args()

    cards, refused, examples, verdicts, stats = author()

    if args.verdicts:
        with open(args.verdicts, 'w', encoding='utf-8') as fh:
            json.dump(verdicts, fh, indent=1)
        print(f'wrote {args.verdicts}: {len(verdicts)} refusals')
    if args.report:
        census = PC.census_subject(SUBJECT)
        total = sum(p['leafCount'] for p in census['papers'])
        print(f'{len(cards)} card(s) against {total} census asks')
        print()
        print('PAIRING (Law 4): how each sitting\'s scheme parts were joined')
        for year, level, ok, cueless, bad in stats:
            n = ok + cueless + bad
            print(f'  {year} {level.upper()}: {ok:3} confirmed by wording, '
                  f'{cueless:3} address only (scheme prints no cue), '
                  f'{bad:3} refused for contradicting the address'
                  f'   [{100 * ok // max(n, 1)}% confirmed]')
        print()
        for reason, n in refused.most_common():
            print(f'  {n:4} REFUSED  {reason}')
            for e in examples[reason][:60 if args.all else 3]:
                print(f'            {e}')
        return 0
    print(json.dumps(cards, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
