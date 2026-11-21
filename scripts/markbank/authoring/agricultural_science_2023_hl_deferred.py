"""2023 Higher DEFERRED sitting: every task from the complete deferred paper/scheme review.

The SEC's deferred paper (deferredexams/2023/LC024ALP000EV.pdf, 44 pages) and scheme (deferredmarkingschemes/2023/
LC024ALP000EV.pdf, 25 pages), each page looked at. The independent census (agricultural_science_census.py
HIGHER_2023_DEFERRED) was transcribed first, by a reader who did not see the cards; the cards were authored from a
second, separate reading of the same pages and must agree with it task for task (marks included). Every question and
row is lifted: questions and stems from the paper, rows from the scheme
(agricultural_science_2023_hl_deferred.json, the reviewed card record this file turns into cards).

The deferred sitting is its own edition, "LC024ALP000EV-deferred.pdf" in Paper Trail: cards are
agsci-2023-hl-deferred-<task>, cited "2023 HL Q... — Deferred sitting", their Atlas anchors in its own answer map.
"""
import json
from pathlib import Path

from agricultural_science_2010_hl import point, menu, region
from agricultural_science_2010_parity import scan

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / 'agricultural_science_2023_hl_deferred.json').read_text())
FILE = 'LC024ALP000EV.pdf'          # the deferred corpus files the sitting under June's id
EDITION = 'LC024ALP000EV-deferred.pdf'
YEAR = 2023
HASHES = {'deferredexams': '8affbd652ab012698a944549855b0f8d209af7e5a12a2b6010bc95d46b1af768',
          'deferredmarkingschemes': '19b2cc3ef9c1bd460f2ecf1688395cae7a319f3d3da61dca197e4b1d8643f67e'}
SELECTIONS = {key: tuple(value) for key, value in SPEC['selections'].items()}
SUPPLEMENTARY = [tuple(row) for row in SPEC.get('supplementary', [])]
SOURCE_NOTES = SPEC['sourceNotes']


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    notes = [dict(questionN=str(int(c['ref'][1:].split('(')[0])), questionRef=c['ref'], note=SOURCE_NOTES[c['key']])
             for c in SPEC['cards'] if c['key'] in SOURCE_NOTES]
    return dict(year=YEAR, level='higher', lang='ev', sitting='deferred', paperFileid=EDITION, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 45)), schemePagesInspected=list(range(1, 26)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=notes,
                independentBoundaryReview=SPEC['boundaryReview'],
                cropVisualReview='Every paper and scheme region set against the rendered page.',
                runtimeReview='Integrated card and Atlas checks with the deferred lane gate.',
                remaining=['Irish edition (deferred, out of scope)'])


def rows_of(spec_rows):
    out = []
    for r in spec_rows:
        if r['type'] == 'point' and r.get('criterion'):
            # A drawing the scheme prices only as a whole (manual question total, as June's drawings).
            out.append(point(r['text'], None, r.get('note'), kind='criterion'))
        elif r['type'] == 'point':
            out.append(point(r['text'], r['marks'], r.get('note')))
        else:
            out.append(menu(list(r['texts']), list(r['marks']), r.get('note')))
    return out


def reviewed_tasks():
    paper_review()
    cards, tasks = [], []
    for spec in SPEC['cards']:
        key, ref = spec['key'], spec['ref']
        cid = 'agsci-2023-hl-deferred-' + key
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows_of(spec['rows']))]
        manual = spec.get('manualTotal')
        pp = [region(p, y0, y1) for p, y0, y1 in spec['paper']]
        sp = [region(p, y0, y1) for p, y0, y1 in spec['scheme']]
        extra = tuple(spec.get('extra') or ())
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='higher',
                    section='A' if int(ref[1:].split('(')[0]) <= 12 else 'B',
                    questionRef=f'2023 HL {ref} — Deferred sitting', topicId='agsci-' + spec['topic'],
                    curriculumNodeIds=['agsci-' + t for t in (spec['topic'], *extra)],
                    conceptId=spec['concept'], questionText=spec['question'], rows=rows,
                    totalMarks=manual if manual is not None else sum(r['marks'] for r in rows),
                    tariffModel={'kind': 'questionTotal' if manual is not None else 'fixed'},
                    sourceMaterial=dict(kind='source-text', label='OFFICIAL QUESTION PAGE',
                                        title=f'Agricultural Science 2023 Higher, deferred — {ref}',
                                        pages=sorted({r['p'] for r in pp}),
                                        attribution='SEC Agricultural Science 2023 Higher Level deferred examination paper — © State Examinations Commission.',
                                        presentationNote='Open the original page for the published wording, photographs, tables and examination context.'))
        if extra:
            card['additionalTopicIds'] = ['agsci-' + t for t in extra]
        if spec.get('stem'):
            card['stem'] = spec['stem']
        if spec.get('figure'):
            # The scheme's own drawn answer (scripts/markbank/agricultural-science-audit/make_figures.py).
            card['figureKey'] = spec['figure']
        if spec.get('variants'):
            card['answerVariants'] = [dict(id=v['id'], label=v['label'],
                                           rows=[dict(r, id=f'r-{i+1}') for i, r in enumerate(rows_of(v['rows']))])
                                      for v in spec['variants']]
            card['rows'] = card['answerVariants'][0]['rows']
            rows = card['rows']
        task = dict(questionRef=card['questionRef'], paperPage=pp[0]['p'], schemePage=sp[0]['p'],
                    paperRegions=pp, schemeRegions=sp, atlasNumbers={cid: str(1001 + len(cards))}, cardIds=[cid],
                    marksPerRoute=card['totalMarks'], examTopicIds=list(spec['examTopicIds']),
                    selection=spec.get('selection') or {'kind': 'none', 'reason': 'Required response. Open examples and scheme alternatives remain marking menus, not finite printed routes.'},
                    evidence='All 44 deferred paper and 25 deferred scheme pages visually inspected. The independent census was transcribed before the cards and agrees with them task for task.')
        if key in SOURCE_NOTES:
            task['schemeNote'] = SOURCE_NOTES[key]
            rows[0]['contextNote'] = (rows[0].get('contextNote', '') + ' ' + SOURCE_NOTES[key]).strip()
        cards.append(card)
        tasks.append(task)
    assert len(cards) == 85, len(cards)
    return cards, tasks


def filings():
    """The Atlas model's filing of each card (scripts/atlas-model/filings/agricultural-science.json "asks"): r2 where
    the card reader and the independent census reader chose the same heading, r3 where they differed and the lane
    settled it (always the census reader's single heading, which the card reader had also given)."""
    return {'agsci-2023-hl-deferred-' + c['key']: c['filing'] for c in SPEC['cards']}


def scheme_text():
    """The scheme's text for the deck's provenance check (examiner-reports/agricultural-science/schemes/
    2023-hl-deferred.md): extract-scheme.py's row reading (marks cells apart), then each page read block by block.
    The deferred scheme sets answers in table cells side by side ("Mainly midlands and eastern counties" beside "Brown
    Earth"), which the row reading welds; a row is the SEC's own words if either reading holds it."""
    import subprocess
    import fitz
    root = HERE.parents[2]
    md = root / 'examiner-reports/agricultural-science/schemes/2023-hl-deferred.md'
    pdf = root / 'paper-trail-corpus/deferredmarkingschemes/2023' / FILE
    subprocess.run(['python3', str(root / 'scripts/markbank/extract-scheme.py'), str(pdf), '-o', str(md),
                    '--marks-column'], check=True, capture_output=True)
    with fitz.open(pdf) as doc:
        blocks = [f'\n## Page {i} (read block by block)\n\n' + '\n'.join(' '.join(b[4].split()) for b in page.get_text('blocks'))
                  for i, page in enumerate(doc, start=1)]
    md.write_text(md.read_text().rstrip('\n') + '\n' + '\n'.join(blocks) + '\n')


if __name__ == '__main__':
    import sys
    if '--scheme-text' in sys.argv:
        scheme_text()
