#!/usr/bin/env python3
"""Recover the three uncarded 2023 Higher Home Economics tasks.

Sources were visually checked, including the table's continuation on page 13.
This is an additive task review, not a claim that the entire subject is complete.
Run with --write to merge these identities without changing other authored cards.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

import fitz

ROOT = Path(__file__).resolve().parents[3]
PAPER = 'examiner-reports/home-economics/papers/2023-hl-039-paper.pdf'
SCHEME = 'examiner-reports/home-economics/2023-marking-scheme.pdf'
HASHES = {
    PAPER: 'f81801f7c53b59c23a368c1640698d603c8f4361a440db2456f6d230439415ba',
    SCHEME: '885b58b2d7c1c5ad60b107a4367795762443399dd91778697367399b3e64ea2b',
}


def tidy(text):
    return re.sub(r'\s+', ' ', text).strip()


def between(text, start, end):
    assert text.count(start) == 1, start
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def criterion(key, heading, count, steps, guidance):
    # Aggregate steps are sums of the printed per-point ladder, never an
    # invented 0..maximum scale. The UI places each chosen point separately.
    totals = {0}
    for _ in range(count):
        totals = {total + mark for total in totals for mark in steps}
    row = dict(id=key, kind='criterion', verbatim=heading,
               marks=count * steps[-1], permittedMarks=sorted(totals),
               contextNote=guidance)
    if count > 1:
        row['parts'] = [dict(id=f'point-{i}', verbatim=f'Point {i}',
                             marks=steps[-1], permittedMarks=steps)
                        for i in range(1, count + 1)]
    return row


def card(key, section, ref, topic, concept, question, stem, marks, notation, rows, page):
    return dict(id=f'he-2023-hl-{key}', subjectId='home-economics',
                topicId=f'home-economics-{topic}', conceptId=concept,
                level='higher', year=2023, section=section,
                questionRef=f'2023 HL Section {section} {ref}',
                questionText=question, stem=stem, figureKey='', labelKey=[],
                tariffModel=dict(kind='fixed', notation=notation),
                totalMarks=marks, rows=rows,
                sourceMaterial=dict(kind='source-question', label='OFFICIAL QUESTION',
                                    title='Source and question', pages=[page],
                                    attribution='SEC Home Economics 2023 Higher Level examination paper — © State Examinations Commission.',
                                    presentationNote='Open the original examination page to review this task in context.'),
                notes='Independently reviewed against the paper and scheme; see he_review_2023_hl.py and home-economics/2023-hl-recovery-review.json. Open choices and required headings remain one task.')


def build():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    paper = fitz.open(ROOT / PAPER)
    scheme = fitz.open(ROOT / SCHEME)
    p3 = tidy(paper[2].get_text())
    s14 = tidy(scheme[13].get_text())
    s22 = tidy(scheme[21].get_text())
    fish_question = between(between(p3, 'Question 2', 'Question 3'), '(b) ', '(18 marks)')
    fish_question = fish_question.split('(c)', 1)[0].strip()
    assert fish_question.startswith('Give a detailed account of one process')
    fish_stem = '‘' + between(between(p3, 'Question 2', 'Question 3'), '‘', '(www.goodfoodireland.ie)') + ' (www.goodfoodireland.ie)'
    variants = []
    for label, page, top, bottom in [
        ('Freezing', 12, 431, 560), ('Salting/Brining', 12, 564, 630),
        ('Smoking', 12, 630, 745), ('Canning', 13, 35, 172),
        ('Vacuum packing', 13, 172, 262),
    ]:
        p = scheme[page - 1]
        name = tidy(p.get_text(clip=fitz.Rect(60, top, 180, bottom)))
        principle = tidy(p.get_text(clip=fitz.Rect(181, top, 380, bottom)))
        effects = tidy(p.get_text(clip=fitz.Rect(382, top, 540, bottom)))
        assert name == label, (label, name)
        assert principle.endswith('etc.') and effects.endswith('etc.'), label
        # Only typographic normalization: PDF uses superscript 'o' for °.
        principle = principle.replace('-30oC', '-30°C').replace('micro- organisms', 'micro-organisms')
        rows = [dict(id='name', kind='point', verbatim=name, marks=3),
                criterion('principle', 'underlying principle', 3, [0, 2, 3],
                          'Three distinct points about your chosen process, each graded 3:2:0. Scheme examples: ' + principle),
                criterion('effects', 'effects', 2, [0, 2, 3],
                          'Two distinct effects, each graded 3:2:0. Scheme examples: ' + effects)]
        variants.append(dict(id=re.sub(r'[^a-z]+', '-', label.lower()), label=label, rows=rows))
    variants.append(dict(id='another-process', label='Another valid process', rows=[
        criterion('name', 'name', 1, [0, 3], 'Name the process you described. The five printed examples are guidance for the open choice; the paper does not restrict the choice to them.'),
        criterion('principle', 'underlying principle', 3, [0, 2, 3], 'Give three accurate principle points for the same process. The scheme provides examples for freezing, salting/brining, smoking, canning and vacuum packing; it prints no model for another process.'),
        criterion('effects', 'effects', 2, [0, 2, 3], 'Give two accurate effects of that process on fish. Use the published 3:2:0 grading for each point; no model answer for this process is printed.'),
    ]))
    fish = card('sb-q2b', 'B', 'Q2(b)', '0-4', 'fish-preservation-process', fish_question,
                fish_stem, 18, 'Name 3 (3:0); underlying principle 3 × 3 (3:2:0); effects 2 × 3 (3:2:0)',
                deepcopy(variants[0]['rows']), 3)
    fish['answerVariants'] = variants

    # Q3 is an OPEN choice, not two separately scheduled cheese/margarine cards.
    food_question = 'Profile ' + between(p3, 'Profile', '(26 marks)')
    food_stem = '‘People are becoming more experimental in their culinary choices.’ (www.bordbia.ie)'
    packaging = between(s14, 'packaging and labelling wrapped', '(c)')
    packaging = 'wrapped ' + packaging
    food_variants = []
    for name, end in [('Cheese', 'Margarine'), ('Margarine', 'cook chill foods;')]:
        production = between(s14, name, end)
        rows = [dict(id='name', kind='point', verbatim=name, marks=2),
                criterion('production', 'stages of production', 6, [0, 2, 3],
                          'Six distinct stages, each graded 3:2:0. Scheme example: ' + production),
                criterion('packaging', 'packaging and labelling', 2, [0, 2, 3],
                          'Two relevant points for the food you chose, each graded 3:2:0. Scheme examples: ' + packaging)]
        food_variants.append(dict(id=name.lower(), label=name, rows=rows))
    other_names = between(s14, 'cook chill foods;', 'packaging and labelling wrapped')
    food_variants.append(dict(id='another-food', label='Another added value food', rows=[
        criterion('name', 'name', 1, [0, 2], 'It must be an added value food. Other scheme examples: cook chill foods; ' + other_names),
        criterion('production', 'stages of production', 6, [0, 2, 3], 'Give six accurate production stages for your chosen food. The scheme prints model stages for cheese and margarine only; use the same published 3:2:0 steps for each stage.'),
        criterion('packaging', 'packaging and labelling', 2, [0, 2, 3], 'Two relevant points, each graded 3:2:0. Scheme examples: ' + packaging),
    ]))
    food = card('sb-q3b', 'B', 'Q3(b)', '0-11', 'added-value-food-profile', food_question,
                food_stem, 26, 'Name 2 (2:0); stages of production 6 × 3 (3:2:0); packaging and labelling 2 × 3 (3:2:0)',
                deepcopy(food_variants[0]['rows']), 3)
    food['answerVariants'] = food_variants

    career_names = 'fashion designers;' + s22.split('fashion designers;', 1)[1]
    careers = [x.strip() for x in career_names.split(';') if x.strip() and x.strip() != 'etc.']
    assert len(careers) == 11
    career = card('sc-q2cii', 'C', 'E2 Q2(c)(ii)', '3-8', 'careers-in-clothing-and-textiles',
                  'Name and give details of one career opportunity in the clothing and textile industry.',
                  '‘The vintage clothing industry is growing 25 times faster than the overall retail market.’ (www.rediscoverycentre.ie)',
                  6, 'Name 1 × 2 (2:0); detail 1 × 4 (4:2:0)', [
                      dict(id='name', kind='anyN', verbatim='Name', marks=2, openList=True,
                           contextNote='Name one career. The list ends in “etc.”, so another valid career can also receive the naming marks.',
                           group=dict(claimMax=1, perOption=2, options=careers)),
                      criterion('detail', 'detail', 1, [0, 2, 4], 'Give a relevant detail about the career you named. The official scheme allocates 4 marks, graded 4:2:0, but does not print an example detail answer.'),
                  ], 6)
    return [fish, food, career]


if __name__ == '__main__':
    reviewed = build()
    if '--write' in sys.argv:
        path = ROOT / 'scripts/markbank/authored/home-economics.json'
        cards = json.loads(path.read_text())
        index = {c['id']: i for i, c in enumerate(cards)}
        for c in reviewed:
            if c['id'] in index:
                # These three identities are owned by this hash-pinned review.
                # No other authored or shipped identity may be replaced here.
                cards[index[c['id']]] = c
            else:
                cards.append(c)
        path.write_text(json.dumps(cards, ensure_ascii=False, indent=1) + '\n')
        held_path = ROOT / 'scripts/markbank/authored/home-economics-held.json'
        held = json.loads(held_path.read_text())
        held_path.write_text(json.dumps([c for c in held if c['id'] not in {x['id'] for x in reviewed}], ensure_ascii=False, indent=1) + '\n')
    print(json.dumps(reviewed, ensure_ascii=False, indent=2))
