#!/usr/bin/env python3
"""Source review of 2023 Higher B2–B5: retain IDs, open choices and mark bands."""
from copy import deepcopy
import hashlib
import json
import re
import sys

import fitz
from he_review_2023_hl import ROOT, PAPER, SCHEME, HASHES, tidy, between, criterion


def paragraphs(text, headings):
    """Retain every word within independently checked printed heading blocks."""
    result = []
    for i, heading in enumerate(headings):
        assert text.count(heading) == 1, heading
        block = text.split(heading, 1)[1]
        if i + 1 < len(headings):
            block = block.split(headings[i + 1], 1)[0]
        block = block.strip()
        assert block.endswith('etc.'), (heading, block)
        result.append((heading, block))
    return result


def build():
    for path, sha in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha
    paper, scheme = fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)
    p3, p4 = [tidy(paper[n - 1].get_text()) for n in [3, 4]]
    # All task-internal choices on these pages are open choices. Required
    # headings remain one answer; the two earlier recovered cards own b2/b3.
    directives = re.findall(r'\b(?:choose|one\s+(?:of|process|physical conditioning agent|legal option)|any\s+\w+|either|or|answer\s+\w+\s+of)\b', p3 + ' ' + p4, re.I)
    assert directives == ['one process', 'one physical conditioning agent', 'one legal option'], directives
    qs = {2: between(p3, 'Question 2', 'Question 3'), 3: p3.split('Question 3', 1)[1],
          4: between(p4, 'Question 4', 'Question 5'), 5: p4.split('Question 5', 1)[1]}
    # Remove only the standalone printed page number, before joining pages.
    s = {n: tidy('\n'.join(line for line in scheme[n - 1].get_text().splitlines()
                           if line.strip() != str(n))) for n in range(12, 18)}
    fixes = {}

    def put(q, part, marks, notation, rows, variants=None):
        key = f'he-2023-hl-sb-q{q}{part}'
        text = between(qs[q], f'({part})', f'({marks} marks)')
        assert not re.search(r'\([abc]\)', text), key
        value = dict(questionText=text, stem=qs[q].split('(a)', 1)[0].strip(),
                     tariffModel=dict(kind='fixed', notation=notation), rows=rows,
                     notes='Paper and full scheme independently reviewed. Keep this published response boundary; use the printed grading steps without inventing definitions for partial marks. See he_review_2023_hl_section_b_rest.py.')
        if variants:
            value['answerVariants'] = variants
        fixes[key] = dict(reason='Independent 2023 Higher B2–B5 review: complete source wording, correct partial marks and published choice/heading rules.', set=value)

    nutrients = paragraphs(between(s[12], 'Nutrient 1; type 1; function/dietary 2', '(b)'),
                           ['Protein (16-18%),', 'Fat (0-18%),', 'Vitamins (1%)', 'Minerals (1%)', 'Water (65-80%)'])
    put(2, 'a', 20, '5 points × 4 (4:3:2:1:0); nutrient 1, type 1, function/dietary 2', [
        criterion('nutrients', 'Nutritional significance of fish', 5, [0, 1, 2, 3, 4],
                  'Mark five distinct points. Each has 1 mark for the nutrient, 1 for its type and 2 for function or dietary significance, using the published 4:3:2:1:0 steps.\n\n' +
                  '\n\n'.join(h + ' ' + body for h, body in nutrients))])
    fsai = s[13].split('(12marks)', 1)[1].strip()
    assert fsai.endswith('new methods of processing; etc.')
    put(2, 'c', 12, '2 points × 6 (6:3:0)', [criterion('role', 'role', 2, [0, 3, 6],
        'Describe two distinct points, each graded 6:3:0. Published guidance: ' + fsai)])
    factors = s[14].split('(b)', 1)[0].split('(12 marks)', 1)[1].strip()
    assert factors.endswith('influencers; etc.')
    put(3, 'a', 12, '3 points × 4 (4:2:0)', [criterion('factors', 'factors that affect food choices for families today', 3, [0, 2, 4],
        'Discuss three factors, each graded 4:2:0. The scheme lists headings but does not define an exact name-only partial grade. Published guidance: ' + factors)])

    agents = (s[14].split('Name: humectants;', 1)[1] + ' ' + s[15]).strip()
    agents = ['humectants; ' + agents.split('Name:', 1)[0]] + agents.split('Name:')[1:]
    assert len(agents) == 10
    expected_agents = ['humectants', 'emulsifiers', 'anti-caking agents', 'setting agent', 'stabilisers',
                       'anti-spattering agents', 'anti-foaming agents', 'firming agents', 'buffers', 'packaging gas']
    variants = []
    for text, label in zip(agents, expected_agents):
        names, role = text.strip().split('role:', 1)
        assert names.startswith(label + ';') and role.strip().endswith('etc.'), label
        variants.append(dict(id=re.sub(r'[^a-z]+', '-', label), label=label.capitalize(), rows=[
            dict(id='name', kind='point', verbatim=names.strip().rstrip(';'), marks=4),
            criterion('role', 'role', 2, [0, 4],
                      'Describe two distinct role points for the same agent. Each is graded 4:0. Published guidance: ' + role.strip())]))
    variants.append(dict(id='another-agent', label='Another physical conditioning agent', rows=[
        criterion('name', 'Name', 1, [0, 4], 'Name the physical conditioning agent you described. The paper leaves this choice open.'),
        criterion('role', 'role', 2, [0, 4], 'Describe two accurate role points for that agent, each graded 4:0. The scheme prints the ten example agents shown in the other answer routes; it does not print a model for another agent.')]))
    put(3, 'c', 12, 'Name 4; role 2 × 4 (4:0)', deepcopy(variants[0]['rows']), variants)

    management = paragraphs(between(s[16], 'one point on each factor plus one other', '(b)'),
                            ['stages in the life cycle of the family', 'employment patterns', 'values'])
    rows = [criterion(f'factor-{i}', h.capitalize(), 1, [0, 3, 5],
                      'One point on this required factor, graded 5:3:0. Published guidance: ' + body)
            for i, (h, body) in enumerate(management, 1)]
    rows.append(criterion('additional', 'one other', 1, [0, 3, 5],
                          'One further distinct point on any of the three factors above, graded 5:3:0. Do not score a point already used for a required factor again.'))
    put(4, 'a', 20, '4 points × 5 (5:3:0); one on each required factor plus one other', rows)
    retail = paragraphs(between(s[16], 'Max of 2 points under each technique.', '(c)'),
                        ['shop layout', 'in-store stimuli', 'product placement', 'shelf position', 'pricing', 'online shopping', 'loyalty cards'])
    row = criterion('techniques', 'techniques used by retailers', 4, [0, 3, 5],
                    'Mark four distinct points, graded 5:3:0. Count no more than two points under the same technique: if you wrote more, select its best two before using these slots. Each slot represents a point, not a whole technique.\n\n' +
                    '\n\n'.join(h + ' ' + body for h, body in retail))
    # Open self-assessment slots preserve 2+2, 2+1+1 and 1+1+1+1 responses.
    # An anyN of seven whole techniques incorrectly permits only one per head.
    put(4, 'b', 20, '4 points × 5 (5:3:0), maximum 2 points per technique', [row])
    responsibilities = s[16].rsplit('2 points @ 5 marks (graded 5:3:0)', 1)[1].strip()
    assert responsibilities.endswith('be environmentally aware; etc.')
    put(4, 'c', 10, '2 points × 5 (5:3:0)', [criterion('responsibilities', 'responsibilities of a consumer', 2, [0, 3, 5],
        'Describe two points showing how a consumer’s responsibilities can assist wise choices. Each is graded 5:3:0. Published guidance: ' + responsibilities)])
    changes = between(s[17], '5 points @ 4 marks (graded 4:2:0)', '(b)')
    assert changes.endswith('influence of religion; etc.')
    put(5, 'a', 20, '5 points × 4 (4:2:0)', [criterion('changes', 'changes that have taken place in the family', 5, [0, 2, 4],
        'Discuss five changes over the period named in the question. Each point is graded 4:2:0. The scheme lists headings but does not define exact descriptions for each grade. Published guidance: ' + changes)])
    terms = paragraphs(between(s[17], '3 points @ 5 marks (graded 5:3:0)', '(c)'),
                       ['universality of the family', 'kinship', 'monogamy'])
    put(5, 'b', 15, '3 required terms × 5 (5:3:0)', [
        criterion(f'term-{i}', h.capitalize(), 1, [0, 3, 5],
                  'Explain this required term, graded 5:3:0. Published guidance: ' + body)
        for i, (h, body) in enumerate(terms, 1)])
    legal = paragraphs(s[17].split('description 3 points @ 4 marks (graded 4:2:0)', 1)[1],
                       ['deed of separation arrangement', 'judicial separation granted', 'legal nullity partners', 'divorce spouse'])
    variants = []
    for h, body in legal:
        # Anchors include the first description word to distinguish headings
        # from later references to the same legal option within a paragraph.
        h, first_word = h.rsplit(' ', 1)
        body = first_word + ' ' + body
        variants.append(dict(id=h.replace(' ', '-'), label=h.capitalize(), rows=[
            criterion('name', h.capitalize(), 1, [0, 2, 3], 'Name the legal option you described, graded 3:2:0.'),
            criterion('description', 'description', 3, [0, 2, 4],
                      'Describe three distinct points about this option, each graded 4:2:0. Published 2023 examination guidance: ' + body)]))
    variants.append(dict(id='another-option', label='Another legal option', rows=[
        criterion('name', 'Name', 1, [0, 2, 3], 'Name an option valid for this 2023 examination question, graded 3:2:0.'),
        criterion('description', 'description', 3, [0, 2, 4],
                  'Describe three accurate points about the same option, each graded 4:2:0. The scheme prints four example options; it gives no model for another option.')]))
    put(5, 'c', 15, 'Name 3 (3:2:0); description 3 × 4 (4:2:0)', deepcopy(variants[0]['rows']), variants)
    assert len(fixes) == 10
    return fixes


def write():
    fixes = build()
    path = ROOT / 'scripts/markbank/card-corrections.json'
    saved = json.loads(path.read_text())
    saved['home-economics'].update(fixes)
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    path = ROOT / 'scripts/markbank/card-source-bindings.json'
    saved = json.loads(path.read_text())
    for q in range(2, 6):
        for part in 'abc':
            key = f'he-2023-hl-sb-q{q}{part}'
            # Full shared stem remains available without requiring a PDF tap.
            if key in saved['home-economics']:
                saved['home-economics'][key]['stripStem'] = False
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=2) + '\n')
    print('B2–B5: 10 marking corrections; two recovered cards retained; no new IDs.')


if __name__ == '__main__':
    if '--write' in sys.argv:
        write()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=2))
