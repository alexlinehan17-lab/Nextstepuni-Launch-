#!/usr/bin/env python3
"""Hash-pinned deferred Home Economics review; never borrow June answers.

Every page of both 2023 question booklets and the deferred scheme was visually
swept. Section A is published here; the independent B/C ledger stays open.
"""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, criterion, between, card

BASE = 'scripts/markbank/authoring/home-economics'
SOURCES = {
    'a': dict(fileid='LC098ALP014EV.pdf', path='paper-trail-corpus/deferredexams/2023/LC098ALP014EV.pdf', sha256='3841b3f1398f2a92c6378812733017cc0c30b39a81b565b1ffb723f172e1df30', pages=40),
    'bc': dict(fileid='LC098ALP039EV.pdf', path='paper-trail-corpus/deferredexams/2023/LC098ALP039EV.pdf', sha256='06fc5065019afdec8a60e87f85afe11a59c6f11c4c9761bfd3a2676f166008c3', pages=12),
    'scheme': dict(fileid='LC098ALP000EV.pdf', path='paper-trail-corpus/deferredmarkingschemes/2023/LC098ALP000EV.pdf', sha256='1ff62adab752ea79017ecd7b7f40c1e553a399c34bfb07bda4b7e7a96548b952', pages=32),
}


def documents():
    docs = {}
    for key, source in SOURCES.items():
        path = ROOT / source['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], key
        docs[key] = fitz.open(path)
        assert len(docs[key]) == source['pages']
    return docs


def a_regions(doc, pages, body_bottom=780):
    result = {}
    for page in pages:
        p = doc[page - 1]
        starts = [(int(w[4][:-1]), w[1] - 3) for w in p.get_text('words')
                  if re.fullmatch(r'\d+\.', w[4]) and w[0] < 100 and w[1] < 760]
        for i, (n, top) in enumerate(starts):
            bottom = starts[i + 1][1] if i + 1 < len(starts) else body_bottom
            # Retain every response line/table edge, trim blank page tails and
            # footers. Word boxes exclude whitespace-only PDF text blocks.
            ends = [w[3] for w in p.get_text('words') if w[1] >= top and w[3] <= bottom]
            ends += [d['rect'].y1 for d in p.get_drawings() if d['rect'].y0 >= top and d['rect'].y1 <= bottom]
            bottom = min(bottom, max(ends) + 8)
            result[n] = dict(page=page, rect=[0, top, p.rect.width, bottom])
    assert list(result) == list(range(1, 15))
    return result


def region_text(doc, region):
    return tidy(doc[region['page'] - 1].get_text(clip=fitz.Rect(region['rect']), sort=True))


def deferred_card(key, section, ref, topic, concept, question, stem, marks, notation, rows, page):
    c = card('deferred-' + key, section, ref, topic, concept, question, stem, marks, notation, rows, page)
    c['questionRef'] += ' — Deferred sitting'
    c['sourceMaterial']['attribution'] = 'SEC Home Economics 2023 Higher Level deferred examination paper — © State Examinations Commission.'
    c['notes'] = 'Paper and deferred scheme independently reviewed. Source identity, boundaries and open-choice decisions: he_review_2023_hl_deferred.py and home-economics/2023-hl-deferred-review.json.'
    return c


SELECTION = {
    1: ['one'], 2: [], 3: ['following', 'one', 'each'], 4: ['three'], 5: [],
    6: ['three', 'one', 'each'], 7: ['three'], 8: ['one'], 9: ['three'],
    10: ['three'], 11: ['following'], 12: ['two'], 13: ['two'], 14: ['one'],
}
QUESTIONS = {
    1: 'In relation to proteins, explain gel formation.',
    2: 'Complete the table below in relation to the digestion of lipids.',
    3: 'The following health conditions may result from a mineral deficiency in the diet. Identify one deficient mineral in each case.',
    4: 'List three properties of Vitamin B1 (thiamine).',
    5: 'In relation to the diet, explain the term energy balance.',
    6: 'Name three different sectors in the Irish food industry and give one example of a food exported in each case.',
    7: 'Outline three conditions that affect the growth of bacteria.',
    8: 'Explain the term ‘added value food’ and give one example of an added value food.',
    9: 'Outline three uses of sensory analysis in the food industry.',
    10: 'Describe three factors to consider when choosing a savings scheme.',
    11: 'Explain the following household insurance terms:',
    12: 'Identify two current features under Ireland’s National Housing Policy.',
    13: 'Outline two factors to consider when choosing household textiles.',
    14: 'Name one cause of water pollution and state the effect of this pollution on the environment. Explain how water pollution can be reduced.',
}


def build_a(docs):
    pr = a_regions(docs['a'], range(3, 8), body_bottom=730); sr = a_regions(docs['scheme'], range(4, 8))
    p = {n: region_text(docs['a'], r) for n, r in pr.items()}
    s = {n: region_text(docs['scheme'], r) for n, r in sr.items()}
    for n, question in QUESTIONS.items():
        assert question in p[n], (n, p[n])
        words = re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b', p[n], re.I)
        assert words == SELECTION[n], (n, words)
    # No finite combination pool: required table rows, paired open examples,
    # required headings, or an open count of points. Q1 alone has two separate
    # printed prompts and tariffs, so it becomes two independently usable cards.
    cards = []
    def add(n, topic, concept, rows, notation, marks=6, question=None, key=None, stem=''):
        cards.append(deferred_card(key or f'sa-q{n}', 'A', f'Q{n}' + (' — culinary example' if key else ''), topic, concept,
                      question or QUESTIONS[n], stem, marks, notation, rows, pr[n]['page']))
    def guidance(n, ladder):
        text = s[n].split(f'(graded {ladder})', 1)[1].strip()
        assert text
        return text
    gel = between(s[1], '(graded 2:1:0)', 'Give one culinary example')
    example = guidance(1, '2:0')
    add(1, '0-5', 'protein-gel-formation', [criterion('explain', 'gel formation', 2, [0, 1, 2], 'Two explanation points, each graded 2:1:0. Published guidance: ' + gel)], '2 points × 2 (2:1:0)', marks=4)
    assert 'Give one culinary example of gel formation.' in p[1]
    add(1, '0-5', 'protein-gel-culinary-example', [criterion('example', 'culinary example', 1, [0, 2], 'One example, graded 2:0. Published examples: ' + example)], '1 example × 2 (2:0)', marks=2,
        question='Give one culinary example of gel formation.', key='sa-q1-example', stem='In relation to proteins.')
    add(2, '0-7', 'lipid-digestion', [criterion(k, label, 1, [0, 1, 2], 'Required table entry, graded 2:1:0. Published answer: ' + answer)
        for k, label, answer in [('enzyme', 'Enzyme', 'Lipase'), ('substrate', 'Substrate', 'Lipids'), ('product', 'Product', 'Fatty acids and glycerol')]],
        '3 entries × 2 (2:1:0)', question=QUESTIONS[2] + '\nSecretion: Pancreatic juice\nEnzyme: _____\nSubstrate: _____\nProduct: _____')
    conditions = [('Rickets in children', 'calcium'), ('Muscular spasms and muscle cramps', 'potassium; sodium; magnesium; Calcium; iron'), ('Enlargement of the thyroid gland', 'iodine')]
    for label, answer in conditions:
        assert label in p[3] and answer in s[3]
    add(3, '0-8', 'mineral-deficiency', [criterion(f'condition-{i}', label, 1, [0, 2], 'Name one deficient mineral for this condition, graded 2:0. Published answers: ' + answer)
        for i, (label, answer) in enumerate(conditions, 1)], '3 minerals × 2 (2:0)', question=QUESTIONS[3] + '\n' + '\n'.join(label for label, _ in conditions))
    for n, topic, concept, label in [(4, '0-8', 'thiamine-properties', 'properties of Vitamin B1'), (5, '0-1', 'energy-balance', 'energy balance'), (7, '0-4', 'bacterial-growth', 'conditions that affect the growth of bacteria'), (9, '0-11', 'sensory-analysis-uses', 'uses of sensory analysis'), (10, '1-1', 'savings-scheme-factors', 'savings scheme')]:
        add(n, topic, concept, [criterion('points', label, 3, [0, 1, 2], 'Three distinct points, each graded 2:1:0. Published guidance: ' + guidance(n, '2:1:0'))], '3 points × 2 (2:1:0)')
    # Table text must be read by cells: the PDF's extraction order places four
    # sector labels before their corresponding exports.
    page = docs['scheme'][4]
    sectors = [('Dairy', 368, 413), ('Meat & livestock', 414, 453), ('Mariculture/ Fish', 454, 475),
               ('Horticulture', 475, 495), ('Beverages', 495, 516), ('Prepared consumer foods', 516, 537)]
    pairs = []
    for name, top, bottom in sectors:
        exports = tidy(page.get_text(clip=fitz.Rect(280, top, 550, bottom)))
        assert exports, name
        pairs.append(name + ': ' + exports)
    sector_guidance = '\n\n'.join(pairs)
    assert 'confectionary' in sector_guidance and 'milk powder' in sector_guidance
    rows = []
    for i in range(1, 4):
        row = criterion(f'sector-{i}', 'Sector in the Irish food Industry', 2, [0, 1], f'Pair {i}: choose a different sector for each pair. Sector 1 mark; suitable export 1 mark. Published examples:\n\n' + sector_guidance)
        row['parts'][0]['verbatim'] = 'Sector'; row['parts'][1]['verbatim'] = 'Matching export'
        rows.append(row)
    add(6, '0-11', 'irish-food-exports', rows, '3 pairs: sector 1 + export 1 (all 1:0)')
    definition = between(s[8], 'Added value food-', 'Example-')
    examples = s[8].split('Example-', 1)[1].strip()
    add(8, '0-11', 'added-value-food', [criterion('definition', 'added value food', 1, [0, 2, 4], 'Explanation graded 4:2:0. Published guidance: ' + definition),
        criterion('example', 'example', 1, [0, 2], 'One example, graded 2:0. Published examples: ' + examples)], 'Explanation 4 (4:2:0); example 2 (2:0)')
    add(11, '1-1', 'household-insurance-terms', [criterion('policy', 'Policy', 1, [0, 2, 3], 'Required term, graded 3:2:0. Published guidance: ' + between(s[11], 'Policy -', 'Premium-')),
        criterion('premium', 'Premium', 1, [0, 2, 3], 'Required term, graded 3:2:0. Published guidance: ' + s[11].split('Premium-', 1)[1])], '2 required terms × 3 (3:2:0)', question=QUESTIONS[11] + '\nPolicy\nPremium')
    add(12, '3-3', 'national-housing-policy-2023', [criterion('features', 'National Housing Policy', 2, [0, 2, 3], 'Two features, each graded 3:2:0. “Current” refers to this 2023 examination. Published 2023 guidance; policy names and measures may since have changed: ' + guidance(12, '3:2:0'))], '2 features × 3 (3:2:0)')
    add(13, '1-4', 'household-textiles-factors', [criterion('factors', 'household textiles', 2, [0, 2, 3], 'Two factors, each graded 3:2:0. Published guidance: ' + guidance(13, '3:2:0'))], '2 factors × 3 (3:2:0)')
    water = guidance(14, '2:1:0')
    add(14, '1-5', 'water-pollution', [criterion(key, label, 1, [0, 1, 2], 'Required heading, graded 2:1:0. Relate the effect to the pollution you named. Published guidance: ' + answer)
        for key, label, answer in [('cause', 'Cause', between(water, 'Cause –', 'Effect –')), ('effect', 'Effect', between(water, 'Effect –', 'Reduction measure –')), ('reduction', 'Reduction measure', water.split('Reduction measure –', 1)[1].strip())]], 'Cause 2; effect 2; reduction 2 (all 2:1:0)')
    assert len(cards) == 15 and sum(c['totalMarks'] for c in cards) == 84
    return sorted(cards, key=lambda c: (int(re.search(r'Q(\d+)', c['questionRef'])[1]), c['id'])), pr, sr


def write():
    docs = documents(); cards, pr, sr = build_a(docs)
    path = ROOT / 'scripts/markbank/authored/home-economics.json'; saved = json.loads(path.read_text())
    for c in cards:
        index = next((i for i, old in enumerate(saved) if old['id'] == c['id']), None)
        if index is None: saved.append(c)
        else: saved[index] = c
    path.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + '\n')
    scheme = ROOT / 'examiner-reports/home-economics/schemes/2023-hl-deferred.md'
    scheme.write_text('# SEC Home Economics 2023 Higher deferred marking scheme\n\n' + '\n\n'.join(
        f'## Physical page {i+1}\n\n' + '\n'.join(line.rstrip() for line in p.get_text().splitlines()).strip()
        for i, p in enumerate(docs['scheme'])).rstrip() + '\n')
    review = dict(schemaVersion=1, year=2023, level='higher', sitting='deferred', language='ev',
        status='partial-carding; all-source-pages-visually-reviewed; browser-QA-pending', sources=SOURCES,
        visualSweep=dict(a='All 40 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled answer pages 9–39, back cover 40.',
                         bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',
                         scheme='All 32 pages: cover 1, deferred marking notice 2, candidate rubric 3, A 4–7, B 8–17, C 18–30, blank 31, back cover 32.'),
        sectionStatus=dict(A='15 tasks carded, 84 offered marks', B='17 tasks open, 280 offered marks', C='26 tasks open, 385 offered marks'),
        offeredPracticeMarks=749, candidateMarks=[280, 320],
        boundaryDecisions=['A1: separate gel explanation (4) and culinary example (2).',
                          'A2/A3: required table entries remain one task per question.',
                          'A6: open choice of three paired sectors and exports; one task, not sector combinations.',
                          'A8/A11/A14: required or dependent headings remain one task.',
                          'Other A counts: open points/examples, no finite choice pool.',
                          'B5(c): scheme accidentally labels (b); paper identity (c) governs.',
                          'C1(a)(iii): published 5:3:0 ladder; allocation 3 provision/2 distribution does not permit standalone 2.',
                          'C1(c)(ii): published examples list inefficiencies, not model reductions; do not invent official models.',
                          'C4(a)(ii): heading says 9 × 2, but detailed 12+4+4 allocation and paper both require 20.',
                          'C4(c)(ii): historical marital-rights guidance needs an explicit consent clarification before publication.'],
        paperRegionsA=pr, schemeRegionsA=sr,
        tasks=[dict(id=c['id'], status='carded', section=c['section'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards])
    path = ROOT / BASE / '2023-hl-deferred-review.json'
    if path.exists():
        old = json.loads(path.read_text())
        review['tasks'] += [t for t in old.get('tasks', []) if t['section'] != 'A']
        for section in ['B', 'C']:
            review['sectionStatus'][section] = old.get('sectionStatus', {}).get(section, review['sectionStatus'][section])
        for key in ['sectionBQuestion1Review', 'sectionBRemainingReview'] + [k for k in old if k.startswith('sectionCQuestion')]:
            if key in old: review[key] = old[key]
        if old.get('completion') and len(review['tasks']) == 58:
            review['completion'] = old['completion']
            review['status'] = old['status']
            review['sectionStatus'] = old['sectionStatus']
    path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    print(f'2023 Higher deferred A: {len(cards)} cards, 84 offered marks. B: {review["sectionStatus"]["B"]} C: {review["sectionStatus"]["C"]}')


if __name__ == '__main__':
    if '--write' in sys.argv: write()
    else: print(json.dumps(build_a(documents())[0], ensure_ascii=False, indent=2))
