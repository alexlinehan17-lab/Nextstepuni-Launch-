#!/usr/bin/env python3
"""German listening: the Listening Comprehension Test as Mark Bank cards.

    python3 scripts/markbank/authoring/de_listen.py 2026 hl     # read one sitting

A German sitting is two booklets, and the listening one is answered from the
SEC's own recording (data/germanAudio.json, one file a year for both levels,
pinned by size, duration and hash). Each printed listening ask is a card:

  * its QUESTION is the booklet's English column (de_paper.aural_ask_lines),
    with a tick-box ask's printed choices kept as its choices;
  * its MARKING ROWS are the scheme's, read here, paired with the paper on the
    printed address both state (part, question, roman) — the census's key;
  * its SOURCE is the booklet page it is printed on, resolved by build-deck.mjs
    as the sitting's "Aural Paper", and its audio the year's recording.

WHY A READER OF ITS OWN
-----------------------
de_scheme.py reads the reading comprehensions, whose schemes number their
answers under a reprinted question. The listening scheme prints shapes the
reading one never does, and every one of them is a tariff:

  * the phone note: "Anruf von: (Alexander) K – A – I – S – E – R (2 marks)
    All or nothing", "Grund des Anrufs:" over a priced answer, "AND", and
    "(Any two: 2 x 1 mark)" over a lettered list — fields of a form, each
    priced on its own line;
  * a priced answer ahead of a menu: "(a) Event: biggest sailing event in the
    world (1)" then "(Any other two: 2 x 1 mark)" over (b)-(e);
  * an answer priced in components: "21st (1) to 29th (1) June (2 marks)";
  * an answer marked down letter by letter: "Deduct 1 mark for each
    incorrect/missing letter:" over "Name: S – T – E – I – N – E – R (4 marks)";
  * a rate printed only on the head: "1. (8 marks: 6, 2 marks)" over two
    unnumbered answers.

Every row's words are the scheme's; the only words this writes are the row
headings the bank already uses ("The answers the scheme accepts in full") and
the language note. Rows that do not add up to the printed tariff are refused
with the reason, never rounded.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

from de_paper import DePaper                                     # noqa: E402
from de_scheme import (DeScheme, UNIT_LISTEN, LISTEN_PART, TRANSCRIPT,   # noqa: E402
                       PART_NAMES, read_rate, head_total, UNIT_LV, UNIT_AG, UNIT_AT,
                       UNIT_SP)

AUDIO = os.path.join(ROOT, 'data', 'germanAudio.json')
MAX_OPTIONS = 16

Q_HEAD = re.compile(r'^(\d{1,2})\s*\.\s*(\(?\s*\d{1,3}\s*marks?\b.*)$', re.I)
R_HEAD = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)\s*(.*)$', re.I)
ROMANS = ('i', 'ii', 'iii', 'iv', 'v', 'vi')
PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$)')

# An examiner's instruction, never an answer. One ending in a colon governs
# the row beneath it ("All or nothing:", "Deduct 1 mark for each
# incorrect/missing letter:").
NOTE = re.compile(
    r'^\(?\s*(?:Where answers|Answers in|Deduct\b|Allow\b|Accept\b|N\.?\s?B\b|'
    r'Note\b|Any (?:two|three|four); no marks|No marks for\b|Evidence|Penalise|Do not\b|'
    r'Ignore\b|All or nothing\b|\[?All or nothing\]?)', re.I)
ALL_OR_NOTHING = re.compile(r'^\[?\s*All or nothing\s*\]?\s*:?.*$', re.I)
# A priced alternative printed under an answer: "allow: in summer (1 mark only)".
ALLOW_ONLY = re.compile(r'^allow:?\s*(.+?)\s*\((\d)\s*marks?\s*only\)\s*$', re.I)
DEDUCT_EACH = re.compile(r'\bDeduct\s+(\d)\s+marks?\s+for\s+each\b', re.I)
CONNECTOR = re.compile(r'^(?:AND|PLUS|UND)\s*:?$', re.I)
TICK = re.compile(r'^Tick\b|^\(?Tick\b', re.I)
TICK_LINE = re.compile(r'Tick\s*\(✓\)\s*the correct (?:box|answer)\.?\s*(?:Tick one box only\.?)?\s*', re.I)

# A form field or a named half of an ask, with or without its answer on the
# line: "Anruf von: …", "Grund des Anrufs:", "Der Anrufer:", "How many
# countries: 185 (1)", "Day: Saturday/20th January (3 marks)". At most four
# words, the first capitalised, no digit.
LABEL = re.compile(r'^([A-ZÄÖÜ][A-Za-zÄÖÜäöüß’\']*(?:\s+[A-Za-zÄÖÜäöüß’\']+){0,3})\s*:\s*(.*)$')
LABEL_ALONE = re.compile(r'^(Der Anrufer|Die Anruferin|Problem|Grund des Anrufs|'
                         r'Why|What|How|Where|When|Who)\s*[?:]?\s*$')

# A list marker at the head of an answer line.
MARKER = re.compile(r'^(?:\(\s*([a-z])\s*\)|([•▪◦\-–*])|(\d{1,2})\s*\.(?!\d))\s*(.*)$')
# A price at the end of an answer: "(2 marks)", "(1)", "(2 marks)" followed by
# an examiner's remark ("All or nothing", "– all or nothing", "(Are healthier
# = 0)", "[All or nothing]") that is kept as the row's note.
PRICE = re.compile(r'\(\s*(\d{1,2})\s*(?:marks?)?\s*\)')
TRAIL = re.compile(r'^(.*?)\s*\(\s*(\d{1,2})\s*(?:marks?)?\s*\)\s*'
                   r'((?:[–\-]\s*)?(?:\[?\s*All or nothing\s*\]?|\(\s*All or nothing\s*\)|\(.*=\s*0\s*\)|'
                   r'\([^()]*=\s*[1-9]\s*(?:marks?)?\)|'
                   r'N\.?\s?B\b.*|Allow\b.*|\(.*\b(?:only|needed|required)\)))?\s*$', re.I)
BRACKET_NOTE = re.compile(r'\s*\[\s*All or nothing\s*\]\s*', re.I)


# ----------------------------------------------------------------- tariffs --
def _term(seg):
    """What one printed term of a split is worth: "2 x 2 marks" 4, "3, 1" 4,
    "1 + 3x1 marks" 4, "4 marks (1, 1 mark, 2 marks)" 4."""
    s = ' '.join((seg or '').split()).strip(' :;,.()')
    m = re.match(r'^(\d{1,3})\s*marks?\s*(?:[(:.]|$)', s, re.I)
    if m:
        return int(m.group(1))
    s = re.sub(r'^Any\s+(?:other\s+)?\w+\s*:?\s*', '', s, flags=re.I)
    total = 0
    found = False
    for part in re.split(r'[+,]', s):
        t = re.search(r'(\d{1,2})\s*[x×]\s*(\d{1,2})', part)
        if t:
            total += int(t.group(1)) * int(t.group(2))
            found = True
            continue
        n = re.search(r'\d{1,3}', part)
        if n:
            total += int(n.group(0))
            found = True
    return total if found else None


def _steps(seg):
    """The per-answer marks one printed rate names, in printed order, or None.
    "(Any two: 2 x 2 marks)" [2, 2]; "Any TWO details: 4 marks: 3, 1" [3, 1];
    "Any two (2 x 1 mark):" [1, 1]; "6, 2 marks" [6, 2]."""
    s = ' '.join((seg or '').split()).strip()
    s = s.rstrip(':').strip()
    while s.startswith('(') and s.endswith(')') and s.count('(') == s.count(')'):
        s = s[1:-1].strip()
    s = re.sub(r'^(Any\s+(?:other\s+)?\w+(?:\s+details?)?)\s*\((.*)\)\s*:?$', r'\1: \2', s, flags=re.I)
    s = re.sub(r'^Any\s+other\s+', 'Any ', s, flags=re.I)
    # "Any one reaction: 3 marks" (2021 Ordinary): the noun names what is
    # counted, as "details" does.
    s = re.sub(r'^(Any\s+\w+)\s+(?!details?\b|examples?\b|points?\b|of\b)[A-Za-z]+(?=\s*:)', r'\1', s, flags=re.I)
    got, _cnt = read_rate(s)
    if got is not None:
        return got
    m = re.match(r'^(?:\d{1,3}\s*marks?\s*[:.;]?\s*)?(\d{1,2}(?:\s*,\s*\d{1,2})+)\s*(?:marks?)?$', s, re.I)
    if m:
        return [int(n) for n in re.findall(r'\d{1,2}', m.group(1))]
    return None


def rate_line(s):
    """(steps, remark) where the line is a rate, else (None, None). The SEC
    sets a remark beside the rate — "(Any two: 2 x 2 marks) Allow apt German
    quotation.", "(Any two: 2 x 1 mark) (Plurals needed)" — kept as a note."""
    s = ' '.join(s.split())
    if not re.search(r'\bmarks?\b|\bAny\b|[x×]\s*\d', s, re.I):
        return None, None
    got = _steps(s)
    if got is not None:
        return got, None
    inner = s[1:-1].strip() if s.startswith('(') and s.endswith(')') else s
    # "(Any two. Allow apt German quotation: 2 x 2 marks)" (2023 Higher): the
    # remark sits between the claim count and its rate.
    m = re.match(r'^(Any\s+\w+)\s*\.\s*(.+?)\s*:\s*(\d.*\bmarks?)$', inner, re.I)
    if m:
        got = _steps(f'{m.group(1)}: {m.group(3)}')
        if got is not None:
            return got, m.group(2).strip() + '.'
    m = re.match(r'^(.*?\bmarks?)\s*\.\s+(\S.*?)\.?$', inner, re.I)
    if m:
        got = _steps(m.group(1))
        if got is not None:
            return got, m.group(2).strip() + '.'
    m = re.match(r'^(\((?:[^()]|\([^()]*\))*\)|Any\b[^()]*?\bmarks?\)?:?)\s+(\S.*)$', s, re.I)
    if m:
        got = _steps(m.group(1))
        if got is not None:
            return got, m.group(2).strip()
    return None, None


def clause_split(clause, romans):
    """({roman: total}, {roman: default steps}) from a question head's clause.

    "(7 marks: (i) 2 x 2 marks; (ii) 3 x 1 mark)" names its romans; "(6 marks:
    1 x 4 marks; 2 marks)" splits in printed order. Either is only believed
    where it accounts for every roman the paper prints.
    """
    s = clause or ''
    m = re.match(r'^\s*\(?\s*\d{1,3}\s*marks?\s*[:.;]?\s*', s, re.I)
    body = (s[m.end():] if m else s).strip()
    body = re.sub(r'\)\s*$', '', body)
    totals, steps = {}, {}
    if romans and not re.search(r'\(\s*(?:i{1,3}|iv|v)\s*\)', body, re.I):
        # The deferred 2022 scheme splits "(7 marks: (a) 1 mark (b) 6 marks)"
        # over the paper's "(i)" and "(ii)": its letters, in order, are those.
        letters = re.findall(r'\(\s*([a-h])\s*\)', body)
        if len(letters) == len(romans):
            for letter, roman in zip(letters, romans):
                body = body.replace(f'({letter})', f'({roman})', 1)
    parts = re.split(r'\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)', body, flags=re.I)
    if (len(parts) >= 3 and romans and romans[0] == 'i' and parts[1].lower() == 'ii'
            and parts[0].strip(' ,;:')):
        # "(6 marks: 1+1 mark, (ii) 2 x 2 marks)" (2023 Higher L1 Q2): the
        # split prints (ii)'s marker and not (i)'s; what comes before it
        # prices (i).
        parts = ['', 'i', parts[0]] + parts[1:]
    if len(parts) >= 3:
        for roman, seg in zip(parts[1::2], parts[2::2]):
            seg = seg.split(';')[0]
            totals[roman.lower()] = _term(seg)
            steps[roman.lower()] = _steps(seg)
    elif romans and body:
        segs = [x for x in body.split(';') if x.strip()]
        if len(segs) == len(romans):
            for roman, seg in zip(romans, segs):
                totals[roman] = _term(seg)
                steps[roman] = _steps(seg)
    if romans and (set(totals) != set(romans) or None in totals.values()):
        return {}, {}
    return totals, steps


# ------------------------------------------------------------ the scheme --
class Leaf:
    __slots__ = ('part', 'q', 'roman', 'total', 'lines', 'default', 'rule', 'line',
                 'q_total', 'q_split')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def scheme_leaves(S, keys):
    """{(part, q, roman): Leaf} for the census keys, from the scheme's lines."""
    lines = S.lines
    start = next((i for i, l in enumerate(lines) if UNIT_LISTEN.match(l.strip())), None)
    if start is None:
        return {}, {}
    part = None
    questions = {}          # (part, q) -> [clause, [lines], line_no]
    rules = {}              # part -> [the part's own language rule lines]
    cur = None
    for i in range(start + 1, len(lines)):
        s = lines[i].strip()
        # The listening test ends at its transcript, or where the scheme
        # prints it first (2021 Ordinary) at the written paper's first unit.
        if TRANSCRIPT.match(s) or any(rx.match(s) for rx in (UNIT_LV, UNIT_AG, UNIT_AT, UNIT_SP)) \
                or re.match(r'^Teil\s+(?:Eins|Zwei|Drei|Vier)\b', s):
            # (the deferred 2022 transcript is headed "Teil Eins")
            break
        m = LISTEN_PART.match(s)
        if m:
            part = PART_NAMES[m.group(1).lower()]
            rules[part] = []
            inline = re.search(r'\((Answers? in [^)]*half marks)\)', s, re.I)
            if inline:
                rules[part].append(inline.group(1))
            cur = None
            continue
        if part is None:
            continue
        m = Q_HEAD.match(s)
        if m:
            cur = (part, int(m.group(1)))
            questions[cur] = [m.group(2), [], i]
            continue
        if cur is None:
            if s and not PAGE.match(s) and re.search(r'answers?\b.*\bin\b|half marks', s, re.I):
                rules[part].append(s)
            continue
        questions[cur][1].append(s)
    out = {}
    by_q = {}
    for p, q, r in keys:
        by_q.setdefault((p, q), []).append(r)
    for (p, q), romans in by_q.items():
        entry = questions.get((p, q))
        if entry is None:
            continue
        clause, block, line_no = entry
        romans = [r for r in romans if r]
        rule = ' '.join(rules.get(p, []))
        if not romans:
            out[(p, q, None)] = Leaf(part=p, q=q, roman=None, total=head_total(clause),
                                     lines=block, default=_steps(clause), rule=rule,
                                     line=line_no + 1)
            continue
        totals, defaults = clause_split(clause, romans)
        heads = []
        want = list(romans)
        for i, s in enumerate(block):
            m = R_HEAD.match(s)
            if want and m and m.group(1).lower() == want[0]:
                heads.append((i, want.pop(0), m.group(2)))
        if not heads and len(romans) > 1 and romans[0] == 'i':
            # The scheme prints no "(i)" over the first ask (2024 Higher L1
            # Q1: "Wladimir Kaminer is an author. Give details …" straight
            # under the head): the first ask runs from the head to "(ii)".
            want = list(romans[1:])
            for i, s in enumerate(block):
                m = R_HEAD.match(s)
                if want and m and m.group(1).lower() == want[0]:
                    heads.append((i, want.pop(0), m.group(2)))
            if heads and not want:
                end = heads[0][0]
                # A tariff line just above "(ii)" prices (ii), not (i).
                if end > 0 and re.match(r'^\(\s*\d{1,3}\s*marks?\s*:', block[end - 1].strip(), re.I):
                    end -= 1
                heads.insert(0, (-1, 'i', ''))
                block = list(block)
            else:
                heads = []
        for n, (i, roman, rest) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
            if i < 0 and end > 0 and re.match(r'^\(\s*\d{1,3}\s*marks?\s*:', block[end - 1].strip(), re.I):
                end -= 1
            body = ([rest] if rest.strip() else []) + block[i + 1:end]
            out[(p, q, roman)] = Leaf(part=p, q=q, roman=roman, total=totals.get(roman),
                                      lines=body, default=defaults.get(roman), rule=rule,
                                      line=line_no + 2 + i, q_total=head_total(clause),
                                      q_split=_steps(clause))
    return out, rules


# ------------------------------------------------------------- the rows ----
def _words(text):
    return {w for w in re.findall(r"[a-zäöüß']+", (text or '').lower()) if len(w) > 2}


def _is_cue(line, asked):
    if TICK.match(line):
        return True
    # A reprinted question closes on its place in the text or its own
    # question mark, whatever language the paper's rendering was read in.
    if not MARKER.match(line) and re.search(
            r'\((?:lines?|Zeile[n]?|Par\.|Abschnitt|Einleitung)[^)]*\)\s*\??$|\?$', line.strip()):
        return True
    w = _words(line)
    return bool(w) and len(w & asked) / len(w) >= 0.6


def _components(text):
    """[(words, marks)] where one answer prices its own components — "21st (1)
    to 29th (1) June (2 marks)" — else None."""
    pieces = []
    pos = 0
    for m in PRICE.finditer(text):
        words = text[pos:m.start()].strip()
        if not words:
            return None
        pieces.append((words, int(m.group(1))))
        pos = m.end()
    if len(pieces) < 2 or text[pos:].strip():
        return None
    return pieces


def leaf_rows(leaf, asked_text):
    """(rows, notes) for one leaf, or a str naming why it cannot be carded."""
    asked = _words(asked_text)
    body = [s for s in leaf.lines if s.strip() and not PAGE.match(s.strip())]
    # The reprinted question opens the block.
    k = 0
    # A question the scheme begins on its head line ("2. (6 marks) Write down
    # three examples …") goes on in lower case on the first line of the block.
    if body and re.match(r'^[a-zäöü]', body[0].strip()) and not PRICE.search(body[0]) \
            and not MARKER.match(body[0].strip()):
        k = 1
    while k < len(body) and _is_cue(body[k], asked) and not PRICE.search(body[k]):
        k += 1
    body = body[k:]
    # The ask's own tariff restated above its question ("(ii) (6 marks: 3 x 2
    # marks)" then the question, deferred 2022) is its head, not a rate over
    # answers: the question beneath it is read as the question.
    if k == 0 and len(body) > 1 and re.match(r'^\(\s*\d{1,3}\s*marks?\s*[:)]', body[0].strip()) \
            and _is_cue(body[1], asked):
        k2 = 1
        while k2 < len(body) and _is_cue(body[k2], asked) and not PRICE.search(body[k2]):
            k2 += 1
        body = body[k2:]
    # A tariff summary over a priced answer and the list beside it — "(2 + (2
    # x 1) marks)" — states the whole field; each half prints its own.
    body = [x for x in body if not re.fullmatch(
        r'\(\s*\d{1,2}\s*\+\s*\(\s*\d\s*x\s*\d\s*\)\s*marks?\s*\)', x.strip(), re.I)]
    items = []              # [{'kind', 'text', 'marks', 'label', 'notes', 'parts', 'group'}]
    general = []
    pending = []
    label = None
    group = None
    last = None

    def close():
        nonlocal group
        if group is not None and group['options']:
            items.append(group)
        elif group is not None:
            general.extend(group['notes'])
        group = None

    last_note = None
    for raw in body:
        s = ' '.join(raw.split())
        if CONNECTOR.match(s):
            last = last_note = None
            continue
        # "AND (Any two: 2 x 1 mark)": the connector and the rate on one line.
        s = re.sub(r'^(?:AND|PLUS)\s+(?=\()', '', s)
        # A note runs on until a rate, a marker or a priced line opens.
        if (last_note is not None and not MARKER.match(s) and rate_line(s)[0] is None
                and not PRICE.search(s) and not LABEL.match(s)):
            holder, at = last_note
            holder[at] = f'{holder[at]} {s}'
            continue
        last_note = None
        steps, remark = rate_line(s)
        if (steps is not None and len(steps) == 1 and re.fullmatch(r'\(\s*\d{1,2}\s*marks?\s*\)', s, re.I)
                and group is not None and group['steps'] is None and len(group['options']) == 1):
            # The answer's own price, wrapped onto a line of its own:
            # "Wasserrohr gebrochen // … alles voller Wasser" / "(2 marks)".
            opt = group['options'][0]
            group = None
            last = {'kind': 'point', 'text': opt['text'], 'marks': steps[0], 'label': label,
                    'notes': list(pending)}
            pending = []
            items.append(last)
            continue
        if steps is not None and not MARKER.match(s):
            close()
            group = {'kind': 'group', 'steps': steps, 'options': [], 'label': label,
                     'notes': ([remark] if remark else []) + pending, 'rated': True}
            pending = []
            last = None
            continue
        if NOTE.match(s) and not MARKER.match(s):
            if s.endswith(':') or (ALL_OR_NOTHING.match(s) and len(s) < 40):
                pending.append(s.rstrip(':').strip())
                continue
            holder = (last['notes'] if last is not None
                      else group['notes'] if group is not None else general)
            holder.append(s)
            last_note = (holder, len(holder) - 1)
            continue
        m = LABEL_ALONE.match(s)
        if m:
            close()
            label = m.group(1)
            last = None
            continue
        marker = MARKER.match(s)
        text = s
        if marker:
            text = marker.group(4).strip()
            if marker.group(1) and re.fullmatch(r'\(\s*\d{1,2}\s*marks?\s*\)', text, re.I):
                # The answer is the letter itself: "(d) (2 marks)" for a
                # choice printed "(a) … (d)" in the question (2021 Ordinary).
                text = f'({marker.group(1)}) {text}'
                marker = None
        else:
            m = LABEL.match(s)
            if m and not re.search(r'\d', m.group(1)) and not re.match(r'^Any\b', m.group(1), re.I):
                rest = m.group(2).strip()
                got, _r = rate_line(rest) if rest else (None, None)
                summary = re.match(r'^\(?\s*\d{1,3}\s*marks?\b', rest, re.I)
                if got is None and not summary and re.fullmatch(r'\((?!\s*\d)[^()]*\)', rest):
                    # "Das Problem: (Answer in English/Irish: half marks)": a
                    # heading with its remark, which governs the rows under it.
                    close()
                    label = m.group(1)
                    pending.append(rest.strip('()'))
                    last = None
                    continue
                if got is not None and not summary:
                    # "Where: (Any two: 2 x 2 marks)" — the half's own list.
                    close()
                    label = m.group(1)
                    group = {'kind': 'group', 'steps': got, 'options': [], 'label': label,
                             'notes': ([_r] if _r else []) + pending}
                    pending = []
                    last = None
                    continue
                if not rest or got is not None or summary:
                    close()
                    label = m.group(1)
                    last = None
                    continue
                close()
                label = m.group(1)
                text = rest
                # A field opens here: the line is its own answer, never the
                # second line of the list above it ("… zurück" / "Anrufer:
                # erhält … einen Rückruf (2 marks)", 2021 Higher).
                last = None
        # An unmarked line under a marked answer is that answer's second line,
        # and a bracket alone ("(Two details)") is a remark on it.
        # A wrapped line follows a full one (the scheme's lines run to some
        # 75-90 characters); a short line under a short one is an answer of
        # its own — "jumper/sweater/pullover hoodie = 0" / "pants/trousers".
        if (not marker and last is not None and last['kind'] == 'option'
                and (re.fullmatch(r'\(.*\)', text) or last['width'] >= 60
                     or (last['marked'] and re.match(r'^[a-zäöü(…./]', text)))):
            last['text'] = f"{last['text']} {text}"
            last['width'] = len(s)
            continue
        if (not marker and last is not None and last['kind'] == 'point'
                and re.fullmatch(r'\(.*\)', text)):
            last['notes'].append(text)
            continue
        # Under a rate, a marked line is one of its answers even where it
        # prices itself: "(Two marks: 1 + 1 mark)" over "(a) … (1)", "(Any two:
        # 2 x 2 marks)" over "(f) coffee comes mainly (1) from Brazil and
        # Vietnam (1)".
        if marker and group is not None and group['steps'] is not None:
            opt = {'kind': 'option', 'text': text, 'notes': [], 'marked': True, 'width': len(s)}
            group['options'].append(opt)
            last = opt
            continue
        text = BRACKET_NOTE.sub(' ', text).strip() if BRACKET_NOTE.search(text) else text
        if BRACKET_NOTE.search(s):
            pending.append('All or nothing')
        comps = _components(text)
        tm = TRAIL.match(text)
        if comps:
            close()
            last = {'kind': 'parts', 'text': text, 'marks': sum(m for _w, m in comps),
                    'parts': comps, 'label': label, 'notes': pending}
            pending = []
            items.append(last)
            continue
        if tm and tm.group(1).strip():
            if group is not None and group['options']:
                close()
            last = {'kind': 'point', 'text': tm.group(1).strip(), 'marks': int(tm.group(2)),
                    'label': label, 'notes': pending + ([tm.group(3).strip(' –-')] if tm.group(3) else [])}
            pending = []
            items.append(last)
            continue
        if group is None:
            group = {'kind': 'group', 'steps': None, 'options': [], 'label': label,
                     'notes': list(pending)}
            pending = []
        opt = {'kind': 'option', 'text': text, 'notes': [], 'marked': bool(marker), 'width': len(s)}
        group['options'].append(opt)
        last = opt
    close()
    if pending:
        general.extend(pending)
    # An answer wrapped onto a second line carries its price there: "• Name
    # nicht auf der Prüfungsliste // … seinen Namen" / "auf die Liste zu
    # setzen// (2 marks)". Under no rate, it is a priced answer of its own.
    for n, it in enumerate(items):
        if it['kind'] == 'group' and it['steps'] is None and len(it['options']) == 1:
            tm = TRAIL.match(' '.join(it['options'][0]['text'].split()))
            if tm and tm.group(1).strip():
                items[n] = {'kind': 'point', 'text': tm.group(1).strip(), 'marks': int(tm.group(2)),
                            'label': it['label'],
                            'notes': it['notes'] + ([tm.group(3).strip(' –-')] if tm.group(3) else [])}
    # A list whose every answer prices itself at the rate's own value, in
    # order, is those answers each at its price: "(Two marks: 1 + 1 mark)" over
    # "(a) (Christmas music) can affect mental health (1)" and "(b) … (1)".
    for n, it in enumerate(items):
        if it['kind'] != 'group' or not it['steps'] or len(it['options']) != len(it['steps']):
            continue
        priced = [TRAIL.match(' '.join(o['text'].split())) for o in it['options']]
        if all(tm and tm.group(1).strip() and not tm.group(3) for tm in priced) and \
                [int(tm.group(2)) for tm in priced] == list(it['steps']):
            items[n:n + 1] = [{'kind': 'point', 'text': tm.group(1).strip(), 'marks': int(tm.group(2)),
                               'label': it['label'], 'notes': list(it['notes']) if k == 0 else []}
                              for k, tm in enumerate(priced)]
    # A list the block printed no rate for takes the head's: "1. (8 marks: 6, 2
    # marks)" over "jumper/…" and "pants/trousers".
    for it in items:
        if it['kind'] == 'group' and it['steps'] is None:
            fixed = sum(x['marks'] for x in items if x['kind'] in ('point', 'parts'))
            if leaf.default and sum(leaf.default) + fixed == (leaf.total or 0):
                it['steps'] = list(leaf.default)
            elif len(it['options']) == 1 and leaf.total is not None and leaf.total > fixed:
                it['steps'] = [leaf.total - fixed]
            else:
                return 'the scheme prints answers with no rate this reads for them'
    got = sum(x['marks'] for x in items if x['kind'] in ('point', 'parts')) + \
        sum(sum(x['steps']) for x in items if x['kind'] == 'group')
    if not items:
        return 'the scheme prints no answers this reads for the ask'
    if leaf.total is None:
        # The head prints its split only as a list of answer prices — "3. 6
        # marks: 2, 2, 2 marks" over "(i)" with two answers priced "(2)" each
        # and "(ii)" with one (2022 Ordinary L1 Q3). Where every row of the
        # roman prices itself, its total is those printed prices; cards()
        # then checks that the romans' prices, in order, are the head's list.
        if leaf.q_split and all(x['kind'] == 'point' for x in items):
            leaf.total = got
            return items, general
        # A head printing its total alone ("4. (7 marks)") over romans that
        # each print their own rate ("(Any four: 4 x 1 mark)", "(Any three:
        # 3 x 1 mark)", deferred 2022 L4 Q4): each roman is worth its own
        # printed rate; cards() checks the romans add to the head's total.
        if leaf.q_total is not None and all(x['kind'] in ('point', 'parts') or x.get('rated')
                                            for x in items):
            leaf.total = got
            return items, general
        return 'the scheme prints no total this reads for the ask'
    if got != leaf.total:
        return f'the scheme prices this ask {leaf.total} and its own rows add to {got}'
    for it in items:
        if it['kind'] == 'group' and len(it['options']) < len(it['steps']):
            return 'the scheme prices more answers than it states'
    return items, general


# A priced alternative the scheme prints beside an answer: "N.B. Crime: 1
# mark" under it, "… N.B. She got a (new/another) dress: 1 mark" or "(Allow:
# cheap = 1 mark)" inside it. Paid in place of the answer, never beside it.
PARTIAL_NOTE = re.compile(r'^(?:N\.?\s?B\.?:?\s*(.+?)\s*[:=]\s*([1-9])\s*marks?\.?'
                          r'|\((?!.*\bN\.?B)(.+?)\s*=\s*([1-9])\s*(?:marks?)?\))$', re.I)
PARTIAL_INLINE = re.compile(r'\s+(?:N\.?\s?B\.?:?\s*(.+?)\s*[:=]\s*([1-9])\s*marks?|'
                            r'\(Allow:?\s*(.+?)\s*[:=]\s*([1-9])\s*marks?\))\s*$', re.I)


def _partials(rows):
    """Each priced alternative made claimable through optionOf, as the
    Spanish deck's partials are: an answer and its alternative are one pick,
    paid once at the better of the two claimed."""
    out = []
    for row in rows:
        note = row.get('contextNote') or ''
        if row['kind'] == 'point':
            parts = [x for x in re.split(r'(?<=[.)”])\s+(?=N\.?\s?B\b)', note)]
            parts = [y for x in parts for y in re.split(r'(?<=[)”.])\s+(?=\()', x)]
            hit = next((PARTIAL_NOTE.match(x.strip()) for x in parts if PARTIAL_NOTE.match(x.strip())), None)
            alt, n = ((hit.group(1), hit.group(2)) if hit and hit.group(1) else
                      (hit.group(3), hit.group(4)) if hit else (None, None))
            if hit and int(n) < row['marks']:
                keep = ' '.join(x for x in parts if not PARTIAL_NOTE.match(x.strip()))
                said = (f'The scheme allows “{alt}” for {n} '
                        f'mark{"s" if n != "1" else ""}, in place of the answer above, never beside it.')
                row = {'id': row['id'], 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts in full',
                       'marks': None,
                       'group': {'claimMax': 1, 'perOption': row['marks'],
                                 'options': [row['verbatim'], alt],
                                 'optionMarks': [row['marks'], int(n)],
                                 'optionOf': [None, 0]},
                       'contextNote': ' '.join(x for x in (keep, said) if x)}
        elif row['kind'] == 'anyN' and not row['group'].get('perOptionSteps') and not row['group'].get('optionMarks'):
            g = row['group']
            options, marks, parents, said = [], [], [], []
            for o in g['options']:
                m = PARTIAL_INLINE.search(o)
                options.append(o[:m.start()].strip() if m else o)
                marks.append(g['perOption'])
                parents.append(None)
                if m:
                    alt, n = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
                    if int(n) < g['perOption']:
                        said.append((alt, n, len(options) - 1))
            if said:
                for alt, n, of in said:
                    options.append(alt)
                    marks.append(int(n))
                    parents.append(of)
                row = dict(row)
                row['group'] = {**g, 'options': options, 'optionMarks': marks, 'optionOf': parents}
                text = ' '.join(f'The scheme allows “{alt}” for {n} mark{"s" if n != "1" else ""}, in '
                                f'place of “{options[of]}”, never beside it.' for alt, n, of in said)
                row['contextNote'] = ' '.join(x for x in (row.get('contextNote'), text) if x)
        out.append(row)
    return out


def mark_rows(items, language_note, general=()):
    """The card's MarkRows from the read items. What the scheme prints for the
    whole ask ("Any three; no marks for tone of voice …") rides on the first
    row, after the language note."""
    rows = []
    for n, it in enumerate(items, start=1):
        notes = []
        if it.get('label') and it['kind'] != 'group':
            notes.append(f'The scheme heads this answer “{it["label"]}”.')
        notes += [x if re.search(r'[.!?)]$', x) else f'{x}.' for x in it['notes'] if x]
        if it['kind'] == 'point':
            deduct = next((DEDUCT_EACH.search(x) for x in it['notes'] if DEDUCT_EACH.search(x)), None)
            if deduct:
                row = {'id': f'r-{n}', 'kind': 'criterion', 'verbatim': it['text'],
                       'marks': it['marks'],
                       'permittedMarks': list(range(it['marks'] + 1))}
            else:
                row = {'id': f'r-{n}', 'kind': 'point', 'verbatim': it['text'],
                       'marks': it['marks']}
        elif it['kind'] == 'parts' and any(ALLOW_ONLY.match(x) for x in it['notes']):
            # A components answer with a priced alternative printed under it:
            # "21st (1) to 29th (1) June (2 marks)" / "allow: in summer (1 mark
            # only)" (2025 Ordinary L4 Q1(i)). Parts must add to their row, so
            # the alternative cannot be one; instead each component is an
            # answer of a menu at its own printed price, and the alternative a
            # partial of the component it stands in for — the dearest, the
            # month — paid once at the better of the two (optionOf). Both dates
            # pay 2, "in summer" alone 1, the whole never more than the ask.
            allow = next(ALLOW_ONLY.match(x) for x in it['notes'] if ALLOW_ONLY.match(x))
            comps = it['parts']
            of = max(range(len(comps)), key=lambda k: (comps[k][1], k))
            assert int(allow.group(2)) <= comps[of][1], it
            notes = [x for x in notes if not ALLOW_ONLY.match(x.rstrip('.'))]
            notes.append(f'The scheme prints this answer as “{it["text"]}” and, under it, '
                         f'“{allow.group(0)}”: “{allow.group(1)}” is paid in place of '
                         f'“{comps[of][0]}”, never beside it.')
            marks = [m for _w, m in comps] + [int(allow.group(2))]
            row = {'id': f'r-{n}', 'kind': 'anyN',
                   'verbatim': 'The answers the scheme accepts in full', 'marks': None,
                   'group': {'claimMax': len(comps), 'perOption': max(marks),
                             'options': [w for w, _m in comps] + [allow.group(1)],
                             'optionMarks': marks,
                             'optionOf': [None] * len(comps) + [of]}}
        elif it['kind'] == 'parts':
            row = {'id': f'r-{n}', 'kind': 'criterion', 'verbatim': it['text'],
                   'marks': it['marks'], 'permittedMarks': list(range(it['marks'] + 1)),
                   'parts': [{'id': f'p{i}', 'verbatim': w, 'marks': m,
                              'permittedMarks': list(range(m + 1))}
                             for i, (w, m) in enumerate(it['parts'], start=1)]}
        else:
            steps = it['steps']
            options = [' '.join(o['text'].split()) for o in it['options']]
            if len(steps) == 1 and len(options) == 1:
                row = {'id': f'r-{n}', 'kind': 'point', 'verbatim': options[0],
                       'marks': steps[0]}
            else:
                trimmed = len(options) - MAX_OPTIONS
                group = {'claimMax': len(steps), 'perOption': steps[0],
                         'options': options[:MAX_OPTIONS]}
                if len(set(steps)) > 1:
                    group['perOptionSteps'] = steps
                if len(steps) == len(options) and trimmed <= 0:
                    notes.append('The scheme pays every one of these; none is optional.')
                if trimmed > 0:
                    notes.append(f'The scheme lists {trimmed} further accepted answer(s) for this '
                                 f'ask, in the order it prints them; a valid answer of your own counts.')
                row = {'id': f'r-{n}', 'kind': 'anyN',
                       'verbatim': (f'{it["label"]}: the answers the scheme accepts' if it.get('label')
                                    else 'The answers the scheme accepts in full'),
                       'marks': None, 'group': group,
                       **({'openList': True} if trimmed > 0 else {})}
        if n == 1:
            head = [language_note] if language_note else []
            head += [f'For the whole question the scheme prints: “{" ".join(g.split())}”'
                     + ('' if re.search(r'[.!?]$', g.strip()) else '.') for g in general]
            notes = head + notes
        if notes:
            row['contextNote'] = ' '.join(notes)
        rows.append(row)
    return _partials(rows)


# ------------------------------------------------------------- the paper ---
def _norm(text):
    return ' '.join(re.sub(r"[^\w€%]+", ' ', (text or '').lower()).split())


def question_text(lines, answers=()):
    """(text, choices) from the booklet's English lines.

    A wrapped line joins the one above it; a bullet opens a line of its own.
    A tick-box ask's printed choices are found from the scheme's answer, which
    is one of them: the line it is printed on, and the lines set at the same
    indent either side of it ("True" / "False"; "a boyfriend and girlfriend" …
    "two students"). The question's own lines are set at another indent, by a
    point or more, in every booklet.
    """
    if not lines:
        return '', None
    choices = None
    tick = next((n for n, (t, _x) in enumerate(lines) if TICK.match(t.strip())), None)
    if tick is not None:
        said = [_norm(a) for a in answers if _norm(a)]
        anchor = next((n for n in range(tick + 1, len(lines))
                       if _norm(lines[n][0]) and any(
                           _norm(lines[n][0]) == a or _norm(lines[n][0]) in a.split(' (')[0]
                           or a == _norm(lines[n][0]).rstrip('.') for a in said)), None)
        if anchor is None:
            # The scheme's words for a choice can differ by a bracket ("170
            # million (Euro)" for "170 million Euro"): match without it.
            bare = [_norm(re.sub(r'\([^)]*\)', ' ', a)) for a in answers]
            anchor = next((n for n in range(tick + 1, len(lines))
                           if _norm(lines[n][0]) in bare
                           or _norm(re.sub(r'\([^)]*\)', ' ', lines[n][0])) in bare), None)
        if anchor is not None and lines[anchor][1] is not None:
            # A choice sits within two points of the choice beside it (2026
            # Higher sets "afraid" at 354 and "bored" at 355); the question
            # above them is set further in or out, or ends as a question or
            # a lead-in does ("running group?", "At the end of the
            # conversation,", "The phone call is to:").
            sentence = lines[anchor][0].strip().endswith('.')

            def near(a, b):
                t = lines[b][0].strip()
                return (lines[b][1] is not None and abs(lines[b][1] - lines[a][1]) <= 2.5
                        and not re.search(r'[?:,]$', t) and not TICK.match(t)
                        # a bare choice ("False") under a sentence that ends
                        # with a full stop: the sentence is the statement
                        and (sentence or not t.endswith('.'))
                        # a lead-in breaks off on its article or preposition
                        # ("The telephone call is to a")
                        and not re.search(r'\b(?:a|an|the|to|is|are|of|between|for|says)$', t, re.I))
            lo = hi = anchor
            while lo - 1 > tick and near(lo, lo - 1):
                lo -= 1
            while hi + 1 < len(lines) and near(hi, hi + 1):
                hi += 1
            if hi > lo:
                choices = []
                for t, _x in lines[lo:hi + 1]:
                    t = ' '.join(t.split())
                    # A choice the booklet wraps onto a second line: "he
                    # should discuss this with her" / "and his father".
                    if choices and re.match(r'^(?:and|or|und|oder)\b', t):
                        choices[-1] = f'{choices[-1]} {t}'
                    else:
                        choices.append(t)
                lines = lines[:lo] + lines[hi + 1:]
    paras = []
    for text, _x in lines:
        t = ' '.join(text.split())
        if not t:
            continue
        if paras and not t.startswith('•') and (
                not re.search(r'[.?!:]$', paras[-1])
                or (not paras[-1].startswith('•') and not paras[-1].endswith(':'))):
            paras[-1] = f'{paras[-1]} {t}'
        else:
            paras.append(t)
    return '\n'.join(paras), choices


def language_of(rule, asked):
    """The language an answer must be in, from the scheme's part rule and the
    ask's own instruction ("Write down in German")."""
    if re.search(r'\bin German\b', asked or '', re.I):
        return 'German'
    if re.search(r'answers are in English', rule or '', re.I):
        return 'German'
    return 'English or Irish'


def language_note(language, rule):
    quoted = f' The scheme reads: “{rule}”' if rule else ''
    if language == 'German':
        return f'Answer this one in German.{quoted}'
    return f'Answer in English or Irish.{quoted}'


TAGS = os.path.join(ROOT, 'scripts', 'paper-trail', 'topic-tags', 'tags', 'german.json')
AURAL_FILEID = {'hl': 'LC011ALPA00{}.pdf', 'ol': 'LC011GLPA00{}.pdf'}
PART_TITLE = {1: 'First Part', 2: 'Second Part', 3: 'Third Part', 4: 'Fourth Part'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}


def aural_fileid(year, level, sitting=None):
    fileid = AURAL_FILEID[level].format('BV' if year >= 2019 else 'EV')
    return fileid.replace('.pdf', '-deferred.pdf') if sitting else fileid


def atlas_tags(year, level, sitting=None):
    """{n: tag} for the sitting's listening booklet in the Topic Atlas, whose
    questions are the booklet's four parts ("1" to "4")."""
    with open(TAGS, encoding='utf-8') as fh:
        papers = json.load(fh)
    fileid = aural_fileid(year, level, sitting)
    for p in papers:
        if (p['year'] == year and p['level'] == LEVEL_WORD[level] and p['lang'] == 'ev'
                and p['fileid'] == fileid):
            return {q['n']: q for q in p['q']}
    return {}


def recording(year, sitting=None):
    with open(AUDIO, encoding='utf-8') as fh:
        return next(r for r in json.load(fh) if r['year'] == year and r.get('sitting') == sitting)


def cards(year, level, refuse, card_id, question_ref, concept_for, sitting=None):
    """Every listening card of one sitting; refuse(reason, ref, evidence) for
    an ask that cannot be carded, which then stays open in the census. A
    deferred sitting's cards are "de-2022-hl-deferred-…", cited "… — Deferred
    sitting", on the deferred booklets and recording."""
    P = DePaper(year, level, 'german', sitting)
    S = DeScheme(year, level, 'german', sitting)
    asks, heads, labels = P.aural_ask_lines()
    keys = [(p, i, r) for p, i, r, _t in P.aural_asks()]
    leaves, _rules = scheme_leaves(S, keys)
    tags = atlas_tags(year, level, sitting)
    rec = recording(year, sitting)
    fileid = aural_fileid(year, level, sitting)
    if sitting:
        _id, _ref = card_id, question_ref
        card_id = lambda *a: _id(*a).replace(f'de-{year}-{level}-', f'de-{year}-{level}-deferred-', 1)  # noqa: E731
        question_ref = lambda *a: f'{_ref(*a)} — Deferred sitting'  # noqa: E731
    assert fileid in rec['paperFileids'], (year, level, fileid)
    out = []
    # Romans priced only by the head's list of answer prices: read each, and
    # card them only where their printed prices, in order, are that list.
    derived = {}
    for key, leaf in leaves.items():
        if key[2] and leaf.total is None and (leaf.q_split or leaf.q_total is not None):
            lines_, _pg = asks.get(key, ([], None))
            got_ = leaf_rows(leaf, ' '.join(t for t, _x in lines_))
            derived.setdefault(key[:2], []).append((key[2], got_))
    bad_q = set()
    for qkey, romans in derived.items():
        flat = []
        for roman, got_ in sorted(romans, key=lambda r: ROMANS.index(r[0])):
            if isinstance(got_, str):
                flat = None
                break
            flat += [x['marks'] if x['kind'] in ('point', 'parts') else m
                     for x in got_[0] for m in ([x.get('marks')] if x['kind'] in ('point', 'parts') else x['steps'])]
        leaf0 = leaves[(qkey[0], qkey[1], romans[0][0])]
        romans_in_q = [k for k in keys if k[:2] == qkey and k[2]]
        alone = len(leaf0.q_split or []) <= 1
        if (flat is None or (not alone and flat != list(leaf0.q_split)) or sum(flat) != leaf0.q_total
                or len(romans) != len(romans_in_q)):
            bad_q.add(qkey)
            for roman, _g in romans:
                leaves[(qkey[0], qkey[1], roman)].total = None
    for part, q, roman in keys:
        unit = f'L{part}'
        ref = question_ref(year, level, unit, q, None, roman)
        lines, page = asks.get((part, q, roman), ([], None))
        leaf = leaves.get((part, q, roman))
        if not lines:
            refuse('the listening booklet prints no English ask this reads', ref,
                   f'{year} {level.upper()} listening booklet, part {part} Q{q}')
            continue
        if leaf is None:
            refuse('the scheme prints no block for this listening ask', ref,
                   f'{year} {level.upper()} scheme, listening part {part} Q{q}')
            continue
        if (part, q) in bad_q:
            refuse('the head prints its split as a list of prices the romans\' own rows do not '
                   'match', ref, f'{year} {level.upper()} scheme, listening part {part} Q{q}')
            continue
        printed = ' '.join(t for t, _x in lines)
        got = leaf_rows(leaf, printed)
        if isinstance(got, str):
            refuse(got, ref, f'{year} {level.upper()} scheme, listening part {part} Q{q}'
                             f'{f"({roman})" if roman else ""}')
            continue
        items, general = got
        said = ([it['text'] for it in items if it['kind'] == 'point']
                + [o['text'] for it in items if it['kind'] == 'group' for o in it['options']])
        text, choices = question_text(lines, said)
        tag = tags.get(str(part))
        if tag is None:
            refuse('the Topic Atlas holds no question for this listening part', ref,
                   f'{year} {level.upper()} {fileid}: no Atlas question {part}')
            continue
        lang = language_of(leaf.rule, printed)
        rows = mark_rows(items, language_note(lang, leaf.rule), general)
        head_lines, _hp = heads.get(part, ([], page))
        # The part's own heading ("Second Part") is the source's title; the
        # stem is what the booklet says is played, how often, and in what
        # language to answer.
        stem = ' '.join(' '.join(head_lines[1:]).split())
        if labels.get((part, q)):
            stem = f'{stem} {labels[(part, q)]}'
        terms = ' + '.join(
            str(it['marks']) if it['kind'] in ('point', 'parts')
            else ' + '.join(map(str, it['steps'])) for it in items)
        card = {
            'id': card_id(year, level, unit, q, None, roman),
            'subjectId': 'german',
            'level': LEVEL_WORD[level],
            'year': year,
            'section': unit,
            'topicId': tag['primary'],
            'conceptId': concept_for(TICK_LINE.sub('', text)),
            'questionRef': ref,
            'questionText': text,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': leaf.total,
            'rows': rows,
            'notes': (f'The scheme prices this ask {leaf.total} marks ({terms}); the listening '
                      f'booklet prints it on page {page}.'),
            'stem': stem,
            'sourceMaterial': {
                'kind': 'source-text',
                'label': 'LISTENING COMPREHENSION TEST',
                'title': f'{PART_TITLE[part]} — Question {q}'
                         + (f'({roman})' if roman else ''),
                'pages': [page],
                # Resolved by build-deck.mjs from Paper Trail's index: the
                # listening booklet is its own SEC document.
                'sourceLabel': 'Aural Paper',
                'attribution': (f'SEC German {year} {LEVEL_TITLE[level]} Level '
                                f'{"deferred " if sitting else ""}Listening '
                                f'Comprehension Test — © State Examinations Commission.'),
                'presentationNote': ('The question page of the listening booklet. '
                                     'Play the recording, then answer.'),
            },
            'audioMaterial': {**rec['source'], 'label': f'{PART_TITLE[part]} · listening'},
        }
        if choices:
            card['questionChoices'] = choices
        out.append(card)
    return out


def main():
    year, level = int(sys.argv[1]), sys.argv[2]
    P = DePaper(year, level, 'german')
    S = DeScheme(year, level, 'german')
    asks, heads, labels = P.aural_ask_lines()
    keys = [(p, i, r) for p, i, r, _t in P.aural_asks()]
    leaves, rules = scheme_leaves(S, keys)
    ok = 0
    for key in keys:
        lines, page = asks.get(key, ([], None))
        printed = ' '.join(t for t, _x in lines)
        leaf = leaves.get(key)
        got = leaf_rows(leaf, printed) if leaf else None
        said = ([it['text'] for it in got[0] if it['kind'] == 'point']
                + [o['text'] for it in got[0] if it['kind'] == 'group' for o in it['options']]
                if isinstance(got, tuple) else [])
        text, choices = question_text(lines, said)
        print(f'== L{key[0]} Q{key[1]}{f"({key[2]})" if key[2] else ""} p{page}: {text[:100]!r}'
              + (f' CHOICES {choices}' if choices else ''))
        if leaf is None:
            print('   REFUSED: no scheme block')
            continue
        if isinstance(got, str):
            print(f'   REFUSED: {got} (total {leaf.total}, default {leaf.default})')
            for l in leaf.lines[:14]:
                print('      |', l)
            continue
        ok += 1
        items, general = got
        lang = language_of(leaf.rule, text)
        for row in mark_rows(items, language_note(lang, leaf.rule), general):
            g = row.get('group')
            print(f"   {row['kind']:9} {row.get('marks')} {row['verbatim'][:90]!r}"
                  + (f" steps={g.get('perOptionSteps') or [g['perOption']] * g['claimMax']} opts={len(g['options'])}" if g else '')
                  + (f" parts={[(p['verbatim'], p['marks']) for p in row['parts']]}" if row.get('parts') else ''))
            if row.get('contextNote'):
                print(f"             note: {row['contextNote'][:160]}")
            if g:
                for o in g['options']:
                    print(f'               - {o[:100]}')
    print(f'{year} {level}: {ok}/{len(keys)} read')


if __name__ == '__main__':
    main()
