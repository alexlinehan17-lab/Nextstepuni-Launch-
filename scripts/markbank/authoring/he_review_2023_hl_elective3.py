#!/usr/bin/env python3
"""Source-backed Social Studies review: required headings and paired schemes."""
import hashlib
import json
import re
import sys

import fitz
from he_review_2023_hl import ROOT, PAPER, SCHEME, HASHES, tidy, between, criterion
from he_review_2023_hl_section_b_rest import paragraphs


def build():
    for path, sha in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha
    paper, scheme = fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)
    p7 = tidy(paper[6].get_text())
    tasks = p7.split('3.(a)', 1)[1]
    directives = re.findall(r'\b(?:choose|one\s+(?:of|type)|two statutory schemes|any\s+\w+|either|or|answer\s+\w+\s+of)\b', tasks, re.I)
    assert directives == ['one type', 'two statutory schemes', 'or'], directives
    sections = {'a': between(p7, '3.(a)', '3.(b)'), 'b': between(p7, '3.(b)', '3.(c)'), 'c': p7.split('3.(c)', 1)[1]}
    s = {n: tidy('\n'.join(line for line in scheme[n - 1].get_text().splitlines() if line.strip() != str(n))).replace('low- paid', 'low-paid') for n in [23, 24, 25]}
    fixes = {}
    def put(part, roman, marks, notation, rows):
        q = sections[part]
        text = between(q, f'({roman})', f'({marks} marks)')
        assert not re.search(r'\((?:i|ii|iii)\)', text)
        fixes[f'he-2023-hl-sc-q3{part}{roman}'] = dict(
            reason='Independent 2023 Higher Social Studies review: full source guidance, required headings, paired name/detail responses and printed partial marks.',
            set=dict(questionText=text, stem=q.split('(i)', 1)[0].strip(), tariffModel=dict(kind='fixed', notation=notation), rows=rows,
                     sourceMaterial=dict(kind='source-question', label='OFFICIAL QUESTION', title='Source and question', pages=[7],
                                         attribution='SEC Home Economics 2023 Higher Level examination paper — © State Examinations Commission.',
                                         presentationNote='Open the original examination page to review this task in context.'),
                     notes='Independently checked against the paper and scheme. Choices remain one task; no combinations. Historic statutory material is the published 2023 examination guidance. See he_review_2023_hl_elective3.py.'))

    work = paragraphs(between(s[23], 'any other 3 points', '(ii)'), ['technology automation', 'flexibility flexi-time;'])
    work = [(h.split(' ', 1)[0], h.split(' ', 1)[1] + ' ' + body) for h, body in work]
    rows = [criterion(h, h, 1, [0, 2, 4], 'One required point on this heading, graded 4:2:0. Published guidance: ' + body) for h, body in work]
    rows.append(criterion('additional', 'any other 3 points', 3, [0, 2, 4], 'Three further distinct points on either heading, each graded 4:2:0. Do not score a point already used above again.'))
    put('a', 'i', 20, '5 × 4 (4:2:0): technology 1, flexibility 1, other 3', rows)
    roles = paragraphs(between(s[23], '3 points @ 5 marks (graded 5:3:0)', '(iii)'),
                       ['Role overload occurs', 'Role conflict caused', 'Distribution of parental responsibilities in the home greater'])
    roles = [(h.rsplit(' ', 1)[0], h.rsplit(' ', 1)[1] + ' ' + body) for h, body in roles]
    put('a', 'ii', 15, '3 required headings × 5 (5:3:0)', [
        criterion(f'heading-{i}', h, 1, [0, 3, 5], 'One point on this required heading, graded 5:3:0. Published guidance: ' + body)
        for i, (h, body) in enumerate(roles, 1)])
    childcare = s[23].split('Name 3 marks (graded 3:0), detail 4 points @ 3 marks (graded 3:2:0)', 1)[1]
    names, detail = childcare.split('location;', 1)
    assert names.strip().endswith('naíonraí; etc.') and detail.strip().endswith('convenience; etc.')
    put('a', 'iii', 15, 'Name 3 (3:0), detail 4 × 3 (3:2:0)', [
        criterion('name', 'Name', 1, [0, 3], 'Recommend one childcare option. Published guidance: ' + names.strip()),
        criterion('detail', 'detail', 4, [0, 2, 3], 'Analyse how the same chosen option meets the family’s needs. Four distinct points, graded 3:2:0. Published guidance: location; ' + detail.strip())])
    poverty = paragraphs(between(s[24], '2 points on each factor', '(ii)'),
                         ['cycle of deprivation in geographical areas', 'the influence of social policy on poverty'])
    put('b', 'i', 16, '2 required factors × 2 points × 4 (4:2:0)', [
        criterion(f'factor-{i}', h, 2, [0, 2, 4], 'Two distinct points on this required factor, each graded 4:2:0. Published 2023 marking guidance: ' + body)
        for i, (h, body) in enumerate(poverty, 1)])
    welfare = paragraphs(s[24].split('(Name 3 marks (graded 3:2:0), detail 4 marks (graded 4:2:0)) x2', 1)[1],
                         ['working family payment', 'back to school clothing and footwear allowance', 'national fuel scheme',
                          'book rental schemes', 'medical cards', 'GP visit card', 'Housing Assistance Payment (HAP)', 'mortgage allowance scheme'])
    guidance = '\n\n'.join(h + ' ' + body for h, body in welfare)
    rows = []
    for i in range(1, 3):
        rows.append(dict(id=f'scheme-{i}', kind='criterion', verbatim='statutory schemes', marks=7, permittedMarks=[0, 2, 3, 4, 5, 6, 7],
                         contextNote=f'Scheme {i} of the two you chose: name (3:2:0) and a matching detail (4:2:0). Choose two different schemes.' +
                         (' Published 2023 marking guidance:\n\n' + guidance if i == 1 else ' Use the complete scheme guidance above.'),
                         parts=[dict(id='name', verbatim='Name', marks=3, permittedMarks=[0, 2, 3]),
                                dict(id='detail', verbatim='Detail', marks=4, permittedMarks=[0, 2, 4])]))
    put('b', 'ii', 14, '2 schemes × (name 3 (3:2:0) + detail 4 (4:2:0))', rows)
    social = paragraphs(between(s[25], '1 point under each heading', '(ii)'),
                        ['changing attitudes to marriage', 'parenting roles women', 'increased participation of women in the workforce'])
    social = [(h.removesuffix(' women'), ('women ' if h.endswith(' women') else '') + body) for h, body in social]
    put('c', 'i', 18, '3 required headings × 6 (6:3:0)', [
        criterion(f'heading-{i}', h, 1, [0, 3, 6], 'One point on this required heading, graded 6:3:0. Published guidance: ' + body)
        for i, (h, body) in enumerate(social, 1)])
    employment = s[25].split('3 points @ 4 marks (graded 4:2:0)', 1)[1].strip()
    employment = employment.replace('low- paid', 'low-paid')
    assert employment.endswith('(under 18 years €7.91); etc.')
    put('c', 'ii', 12, '3 points × 4 (4:2:0)', [criterion('protection', 'protection to young people in work', 3, [0, 2, 4],
        'Describe three distinct points, each graded 4:2:0. Published 2023 examination guidance: ' + employment)])
    assert len(fixes) == 7
    return fixes


def write():
    path = ROOT / 'scripts/markbank/card-corrections.json'
    saved = json.loads(path.read_text()); saved['home-economics'].update(build())
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    print('Elective 3: seven existing tasks corrected; all 110 offered marks retained.')


if __name__ == '__main__':
    if '--write' in sys.argv:
        write()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=2))
