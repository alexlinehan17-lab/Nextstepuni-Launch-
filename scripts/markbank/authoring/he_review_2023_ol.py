#!/usr/bin/env python3
"""Recover four 2023 Ordinary tasks and the held statutory-scheme detail."""
from copy import deepcopy
import hashlib
import json
import re
import sys

import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_section_b_rest import paragraphs

PAPER_A = 'examiner-reports/home-economics/papers/2023-ol-014-paper.pdf'
PAPER_BC = 'examiner-reports/home-economics/papers/2023-ol-039-paper.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2023/LC098GLP000EV.pdf'
HASHES = {
    PAPER_A: '6a3f42524c13a8fc9d3661f53dd767c7aa66917d81a863a58fe6547e6a313da0',
    PAPER_BC: '25ba9252a844743751fe0933052603ce8071c07b1227de413acf31b52b21491f',
    SCHEME: '856913d37890c8ffc78aa2c03b4f3507f909730c9dc3d2b5d4ba80f477f5db82',
}
FIGURES = {
    'home-economics-2023-ol-sa-q14-symbols': dict(source=PAPER_A, page=7, bounds=[83, 322, 220, 626],
        sha256='f1d7366a56f9d51b3067b3a47d143f33012de3e1b261b6be828c48ece659ef82',
        alt='Two care symbols, in vertical order. Top: a square containing three vertical lines. Bottom: a square containing a circle, with a diagonal cross over it.'),
    'home-economics-2023-ol-sb-q1a-table': dict(source=PAPER_BC, page=2, bounds=[54, 199, 542, 439],
        sha256='bcb457f5dc75ec7710ed3898fee3ce3569cd858c2f78964ef12f09f71e1094e1',
        alt='Nutrition per 100 g. Columns: Peanut & chocolate; Peanut & caramel; Crunchy peanut butter. Energy: 492, 373, 518 kcal. Protein: 25.6, 36.3, 25 g. Carbohydrates: 24, 16, 26 g; of which sugars: 15, 3, 16 g. Fibre: 13.6, 16.1, 14 g. Fat: 30, 15.9, 12 g; of which saturates: 9, 8, 5 g. Salt: 0.95, 0.73, 0.59 g.'),
}


def page_text(doc, n):
    # Physical page numbers and printed scheme numbers diverge from p10.
    # Exclude only the footer zone, never a numeral in the question/table.
    page = doc[n - 1]
    return tidy(page.get_text(clip=fitz.Rect(0, 0, page.rect.width, 810)))


def card(key, section, ref, topic, concept, question, stem, marks, notation, rows, page):
    return dict(id=f'he-2023-ol-{key}', subjectId='home-economics', topicId=f'home-economics-{topic}',
                conceptId=concept, level='ordinary', year=2023, section=section, questionRef=f'2023 OL Section {section} {ref}',
                questionText=question, stem=stem, figureKey='', labelKey=[], tariffModel=dict(kind='fixed', notation=notation),
                totalMarks=marks, rows=rows,
                sourceMaterial=dict(kind='source-question', label='OFFICIAL QUESTION', title='Source and question', pages=[page],
                                    attribution='SEC Home Economics 2023 Ordinary Level examination paper — © State Examinations Commission.',
                                    presentationNote='Open the original examination page to review this task in context.'),
                notes='Independently reviewed against paper and full scheme; preserve the published response boundary. See he_review_2023_ol.py.')


def build():
    for path, sha in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha
    a, bc, scheme = fitz.open(ROOT / PAPER_A), fitz.open(ROOT / PAPER_BC), fitz.open(ROOT / SCHEME)
    p2, p3, p7 = [page_text(bc, n) for n in [2, 3, 7]]
    directives = re.findall(r'\b(?:choose|one\s+(?:of|statutory scheme)|any\s+\w+|either|or|answer\s+\w+\s+of)\b', p2 + ' ' + p3 + ' ' + p7, re.I)
    # Section-level choices, one open statutory scheme, then C3(b)/C3(c).
    assert directives == ['any other', 'either', 'or', 'one statutory scheme', 'or'], directives
    s9, s10, s12, s20 = [page_text(scheme, n) for n in [9, 10, 12, 20]]
    # These two questions use all required headings; no finite-option expansion.
    # Bar selection is one of three printed data columns, with one answer route
    # per column within ONE card. Menu and statutory scheme are open choices.
    q2 = between(p3, 'Question 2', 'Question 3')
    assert 'two‐course menu' in q2 and '(i) the nutritive value and (ii) the dietetic value' in q2
    assert 'Name and give details of one statutory scheme' in p7
    symbols_question = 'What information ' + between(page_text(a, 7), 'What information', '(www.beezzly.com)')
    assert symbols_question.endswith('convey to the consumer?')
    assert '2 @ 3 mharc (graded 3:2:0)' in s9
    assert 'drip dry' in s9 and 'do not tumble dry' in s9
    symbols = card('sa-q14', 'A', 'Q14', '1-4', 'fabric-care-symbols', symbols_question, '', 6,
                   '2 symbols × 3 (3:2:0)', [
                       criterion('top', 'drip dry', 1, [0, 2, 3], 'Meaning of the top symbol. Use the printed 3:2:0 steps.'),
                       criterion('bottom', 'do not tumble dry', 1, [0, 2, 3], 'Meaning of the bottom symbol. Use the printed 3:2:0 steps.')], 7)
    symbols.update(questionFigureKey='home-economics-2023-ol-sa-q14-symbols', questionFigureIncludesPrompt=False)
    bar_guidance = paragraphs(s10.split('Name: 4 marks (graded 4:0), Reasons: 4 @ 5 marks (graded 5:4:3:2:0)', 1)[1],
                              ['Peanut & chocolate:', 'Peanut & caramel:', 'Crunchy peanut butter:'])
    variants = []
    for h, detail in bar_guidance:
        name = h.rstrip(':')
        variants.append(dict(id=re.sub(r'[^a-z]+', '-', name.lower()), label=name, rows=[
            dict(id='name', kind='point', verbatim=name, marks=4),
            criterion('reasons', 'Reasons', 4, [0, 2, 3, 4, 5],
                      'Give four distinct reasons for the bar you selected, each graded 5:4:3:2:0. Published scheme guidance: ' + detail)]))
    bars = card('sb-q1a', 'B', 'Q1(a)', '0-1', 'protein-bar-comparison', between(p2, '(a)', '(24 marks)'),
                p2.rsplit('Question 1', 1)[1].split('The table below', 1)[0].strip() + '\n\nThe table below shows nutritional information per 100 g, for three protein bars.',
                24, 'Name 4 (4:0); four reasons × 5 (5:4:3:2:0)', deepcopy(variants[0]['rows']), 2)
    bars.update(answerVariants=variants, questionFigureKey='home-economics-2023-ol-sb-q1a-table', questionFigureIncludesPrompt=False)
    meat = paragraphs(between(s12, '(1 reference to nutritive value, 1 reference to dietetic value, plus 2 others)', '(b)'),
                       ['nutritive:', 'dietetic:'])
    rows = [criterion(f'heading-{i}', h.rstrip(':'), 1, [0, 2, 3, 4, 5],
                      'One required point on this heading, graded 5:4:3:2:0. Published guidance: ' + body)
            for i, (h, body) in enumerate(meat, 1)]
    rows.append(criterion('additional', 'plus 2 others', 2, [0, 2, 3, 4, 5],
                          'Two further distinct points on either heading, each graded 5:4:3:2:0. Do not score a point already used above again.'))
    nutrition = card('sb-q2a', 'B', 'Q2(a)', '0-9', 'nutritive-and-dietetic-value-of-meat', between(q2, '(a)', '(20 marks)'),
                     q2.split('(a)', 1)[0].strip(), 20, '4 × 5 (5:4:3:2:0): nutritive 1, dietetic 1, other 2', rows, 3)
    menu_question = between(q2.split('(b)', 1)[1], 'Using meat', '(20 marks)')
    menu_question = 'Using meat ' + menu_question
    reason_guidance = between(s12, '(1 point must refer to low income)', '(c)')
    assert reason_guidance.endswith('easy to digest; etc.')
    assert 'Spaghetti Bolognese' in s12 and 'Apple crumble' in s12
    menu = card('sb-q2b', 'B', 'Q2(b)', '0-10', 'low-income-family-meat-menu', menu_question,
                q2.split('(a)', 1)[0].strip(), 20, '2 courses × 4; 3 reasons × 4, including low income (4:2:0)', [
                    criterion('menu', 'Menu', 2, [0, 2, 4], 'Design two suitable courses, each graded 4:2:0. Keep meat as the main ingredient and the family’s low income in mind. The printed sample menu is Spaghetti Bolognese followed by Apple crumble; it is an example, not the only valid menu.'),
                    criterion('income', 'low income', 1, [0, 2, 4], 'One reason must refer to low income, graded 4:2:0. The scheme includes cost in its guidance.'),
                    criterion('other', 'reasons', 2, [0, 2, 4], 'Two further distinct reasons for the foods you chose, each graded 4:2:0. Do not count the low-income reason again. Published guidance: ' + reason_guidance)], 3)
    names = s20.split('social welfare assistance and benefits:', 1)[1].strip()
    assert names.endswith('MABS; Abhaile; etc.')
    career = dict(reason='The printed task combines name and detail. Restore its full 8-mark tariff on the existing ID; source prints names and a detail criterion, not model details.', set=dict(
        questionRef='2023 OL Section C E3 Q3(a)(iv)', questionText=between(p7, '(iv)', '(8 marks)'),
        stem=between(p7, '3.(a)', '(i)'), totalMarks=8, tariffModel=dict(kind='fixed', notation='Name 4 (4:2:0); detail 4 (4:2:0)'),
        rows=[criterion('name', 'Name', 1, [0, 2, 4], 'Name one statutory scheme that provides support to unemployed people. Published examples: ' + names),
              criterion('detail', 'Details', 1, [0, 2, 4], 'Give a relevant detail about the scheme you named. The official scheme allocates 4 marks, graded 4:2:0, but prints no model detail answer.')],
        sourceMaterial=dict(kind='source-question', label='OFFICIAL QUESTION', title='Source and question', pages=[7],
                            attribution='SEC Home Economics 2023 Ordinary Level examination paper — © State Examinations Commission.',
                            presentationNote='Open the original examination page to review this task in context.'),
        notes='Full named-scheme response restored on its existing ID. Detail criterion is explicit and honest about the absence of a printed model answer. See he_review_2023_ol.py.'))
    return [symbols, bars, nutrition, menu], {'he-2023-ol-sc-q3aiv': career}


def write():
    added, fixes = build()
    path = ROOT / 'scripts/markbank/authored/home-economics.json'; saved = json.loads(path.read_text())
    index = {c['id']: i for i, c in enumerate(saved)}
    for c in added:
        if c['id'] in index:
            saved[index[c['id']]] = c
        else:
            saved.append(c)
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    path = ROOT / 'scripts/markbank/card-corrections.json'; saved = json.loads(path.read_text()); saved['home-economics'].update(fixes)
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    path = ROOT / 'scripts/markbank/authored/home-economics-held.json'; held = json.loads(path.read_text())
    path.write_text(json.dumps([c for c in held if c['id'] != 'he-2023-ol-sc-q3aiv-details'], ensure_ascii=False, indent=1) + '\n')
    path = ROOT / 'components/MarkBank/figures-home-economics.json'; manifest = json.loads(path.read_text())
    for key, source in FIGURES.items():
        target = ROOT / f'public/exam-figures/home-economics/{key}.png'
        if not target.exists():
            fitz.open(ROOT / source['source'])[source['page'] - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(source['bounds'])).save(target)
        assert hashlib.sha256(target.read_bytes()).hexdigest() == source['sha256'], 'Inspected source crop changed'
        manifest[key] = dict(src=f'/exam-figures/home-economics/{key}.png', md5=hashlib.md5(target.read_bytes()).hexdigest(), alt=source['alt'],
                             attribution=f'SEC Home Economics 2023 Ordinary Level examination paper, page {source["page"]} — © State Examinations Commission.',
                             sourceNote=f'Original source crop, visually inspected with all content and borders. Bounds {source["bounds"]}, 2×. No marking-scheme answer content.')
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Recovered four missing tasks and restored the statutory-scheme detail on its existing ID.')


if __name__ == '__main__':
    if '--write' in sys.argv:
        write()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=2))
