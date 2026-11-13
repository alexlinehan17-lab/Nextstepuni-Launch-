#!/usr/bin/env python3
"""German written production on the scheme's own grid (FrenchRubric shape).

    python3 scripts/markbank/authoring/de_writing.py 2026 hl     # print the cards

Äußerung zum Thema (Higher, 25 marks) is marked "Content = 13 (A = 3; B = 4;
C = 4; Dis. 2)" and "Expression = 12", and the scheme prints a second, lower
expression scale beside the full one with the rule that switches to it: "If
the content mark is 8 or less, or the answer is too short (less than 60
words), mark expression out of 7". So a card's criteria are the content
points as printed (A, B, C, the discretionary marks) and Expression, whose
`lowerScale` carries the reduced scale, its bands and that rule verbatim.

Every string the card shows as the SEC's is lifted from the scheme's text
layer; the criterion labels for the bands ("Category 1") and the practice
notes are NextStepUni's, and the panel says so.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from de_paper import DePaper                       # noqa: E402
from de_scheme import DeScheme                     # noqa: E402

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$)')
RANGE = r'(\d{1,2})(?:\s*[–-]\s*(\d{1,2}))?'
# A row of the expression table: the lower range, the full range, then the
# descriptor's words ("0 – 2 0 – 3 verb forms/tense generally incorrect.").
SCALE_ROW = re.compile(rf'^{RANGE}\s+{RANGE}(?:\s+(.*))?$')


def _lines(S, start, stop):
    return [l.strip() for l in S.lines[start:stop] if l.strip() and not PAGE.match(l.strip())]


def _find(S, pattern, start=0):
    rx = re.compile(pattern, re.I)
    return next((i for i in range(start, len(S.lines)) if rx.search(S.lines[i].strip())), None)


def expression_scale(S):
    """The Äußerung expression table: ([full bands], [lower bands], rule, at).

    Each category opens with "Vocabulary …" and carries its two ranges on one
    of its lines; the range numbers are not part of the descriptor."""
    head = _find(S, r'^Marking Written Expression in [ÄA]u[ßs]{1,2}erung')
    if head is None:
        return None
    stop = _find(S, r'^N\.B\. Take a global view', head)
    lines = _lines(S, head + 1, stop)
    rule_at = next(i for i, l in enumerate(lines) if l.startswith('If the content mark is'))
    rule = lines[rule_at]
    if lines[rule_at + 1] == 'expression':
        rule = f'{rule} expression'
    rule_tail = lines[rule_at + 2] if lines[rule_at + 1] == 'expression' else lines[rule_at + 1]
    m = re.match(r'^(out of \d+)\b', rule_tail)
    if m:
        rule = f'{rule} {m.group(1)}'
    cats = []
    for line in lines:
        if line.startswith('Vocabulary'):
            cats.append({'lines': [], 'lower': None, 'full': None})
        if not cats:
            continue
        m = SCALE_ROW.match(line)
        if m and cats[-1]['lower'] is None:
            lo = (int(m.group(1)), int(m.group(2) or m.group(1)))
            fu = (int(m.group(3)), int(m.group(4) or m.group(3)))
            cats[-1]['lower'], cats[-1]['full'] = lo, fu
            # The range column cuts the descriptor where it is printed
            # ("… Verb" / "4 – 6 forms/tense …"): the words either side are
            # kept apart, as the scheme's text has them.
            cats[-1]['lines'].append(None)
            if m.group(5):
                cats[-1]['lines'].append(m.group(5).strip())
            continue
        cats[-1]['lines'].append(line)
    full, lower = [], []
    for n, c in enumerate(cats, start=1):
        assert c['full'] and c['lower'], (S.year, S.level, c)
        guidance = _join(c['lines'])
        full.append({'label': f'Category {n}', 'marks': list(range(c['full'][0], c['full'][1] + 1)),
                     'guidance': guidance})
        lower.append({'label': f'Category {n}', 'marks': list(range(c['lower'][0], c['lower'][1] + 1)),
                      'guidance': guidance})
    nb = ' '.join(_lines(S, stop, stop + 2)) if stop is not None else ''
    nb = re.match(r'^(N\.B\. Take a global view.*?category[^.]*\.)', nb)
    return full, lower, rule, (nb.group(1) if nb else None)


def _join(lines):
    """Descriptor lines as printed, a wrapped sentence joined: the scheme
    breaks "… word order, esp. verb position, very frequently wrong;" across
    lines mid-clause. Kept line by line where a line ends a clause, and never
    joined across a break (None) the range column makes."""
    out = []
    cut = False
    for line in lines:
        if line is None:
            cut = True
            continue
        if out and not cut and not re.search(r'[.;:]$', out[-1]):
            out[-1] = f'{out[-1]} {line}'
        else:
            out.append(line)
        cut = False
    return out


def theme_grid(S, letter):
    """The content points of Äußerung option (a) or (b): its head lines, and
    [(id, label, marks, [printed lines])] for A, B, C and Dis."""
    starts = [i for i, l in enumerate(S.lines) if re.match(r'^Content = 13 \(A = 3; B = 4; C = 4; Dis\. 2\)', l.strip())]
    at = starts['ab'.index(letter)]
    end = _find(S, r'^Dis\. 2 marks', at)
    lines = _lines(S, at, end + 1)
    head, points, cur = [], [], None
    for line in lines:
        m = re.match(r'^([ABC]): \((\d) marks\)$', line)
        if m:
            cur = {'id': m.group(1).lower(), 'label': m.group(1), 'marks': int(m.group(2)), 'lines': []}
            points.append(cur)
            continue
        if line.startswith('Dis. 2 marks'):
            points.append({'id': 'dis', 'label': 'Dis.', 'marks': 2, 'lines': [line]})
            cur = None
            continue
        (cur['lines'] if cur else head).append(line)
    assert [p['marks'] for p in points] == [3, 4, 4, 2], (S.year, S.level, letter, points)
    return head, points


def task_text(P, unit, letter):
    """The task as the paper prints it, a bullet to a line."""
    rows = [r for r in P.alternatives if r[0] == unit and r[1] == letter]
    rows.sort(key=lambda r: (r[4] == 'R', len(' '.join(r[2]))), reverse=True)
    lines = rows[0][2]
    page = rows[0][3]
    out = []
    for raw in lines:
        t = ' '.join(raw.replace('', '•').split())
        if not t:
            continue
        if out and not t.startswith('•') and not re.search(r'[.?!:)]$', out[-1]) and len(out) > 1:
            out[-1] = f'{out[-1]} {t}'
        else:
            out.append(t)
    return '\n'.join(out), page


def theme_card(year, level, letter, card_id, question_ref, concept_for, topic):
    P = DePaper(year, level, 'german')
    S = DeScheme(year, level, 'german')
    head, points = theme_grid(S, letter)
    full, lower, rule, nb = expression_scale(S)
    criteria = [{'id': p['id'], 'label': p['label'], 'maxMarks': p['marks'],
                 'permittedMarks': list(range(p['marks'] + 1)), 'guidance': p['lines']}
                for p in points]
    criteria.append({
        'id': 'expression', 'label': 'Expression', 'maxMarks': 12,
        'permittedMarks': list(range(13)), 'guidance': [], 'bands': full,
        'lowerScale': {'label': 'Lower E', 'maxMarks': 7, 'permittedMarks': list(range(8)),
                       'bands': lower, 'contentCriteria': [p['id'] for p in points],
                       'contentAtMost': 8, 'wordsUnder': 60, 'rule': rule},
    })
    text, page = task_text(P, 'AT', letter)
    requirements = [l for l in head if not re.match(r'^(Content|Expression) =', l)]
    requirements = ['Content = 13 (A = 3; B = 4; C = 4; Dis. 2)', 'Expression = 12'] + _join(
        [l.lstrip('• ').strip() for l in requirements if l.strip()])
    if nb:
        requirements.append(nb)
    return {
        'id': f'de-{year}-{level}-at-{letter}',
        'kind': 'rubric',
        'subjectId': 'german',
        'level': LEVEL_WORD[level],
        'year': year,
        'section': 'AT',
        'topicId': topic,
        'conceptId': concept_for(text),
        'questionRef': question_ref(year, level, 'AT', None, letter),
        'questionText': text,
        'totalMarks': 25,
        'rubric': {
            'system': 'french',
            'taskRequirements': requirements,
            'criteria': criteria,
            'markingGuideNote': '',
            'practiceNotes': [
                'Write your answer in German, then place it on the published grid.',
                'Place the content points first: the expression scale depends on them.',
            ],
        },
        'schemePages': sorted({_page_of(S, rule), _page_of(S, 'Content = 13')}),
        'sourceMaterial': {
            'kind': 'source-text',
            'label': 'ÄUSSERUNG ZUM THEMA',
            'title': f'Äußerung zum Thema ({letter}) — answer in German',
            'pages': [page],
            'attribution': (f'SEC German {year} {LEVEL_TITLE[level]} Level examination '
                            f'paper — © State Examinations Commission.'),
            'presentationNote': 'The task and its photograph exactly as the examination printed them.',
        },
    }


def _page_of(S, text):
    page = 1
    for line in S.lines:
        m = re.match(r'^##\s*Page\s*(\d+)', line.strip())
        if m:
            page = int(m.group(1))
        if text[:40] in line:
            return page
    return page


if __name__ == '__main__':
    import de_all
    y, l = int(sys.argv[1]), sys.argv[2]
    for letter in 'ab':
        card = theme_card(y, l, letter, de_all.card_id, de_all.question_ref, de_all.concept_for, 'german-7-0')
        print(json.dumps(card, ensure_ascii=False, indent=1))
