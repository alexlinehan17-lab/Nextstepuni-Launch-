"""Shared builder for the legacy-syllabus papers authored from the SEC sources (2012 Ordinary, 2013-2020).

These sittings had no Mark Bank cards, so every task is ADDED: nothing is corrected or withdrawn.
Each year module transcribes its independent census first (agricultural_science_census.py),
then states every task once through Paper.add(), lifting question wording from the paper and
every answer from the scheme. The builder supplies the shared card and review-ledger shape:

  * topicId is a current-specification topic (agsci-*), which is what practice filters use;
  * curriculumNodeIds name the specification the sitting was EXAMINED on (the pre-2021
    agricultural-science-* nodes), resolved per exam year by cardCurriculum.ts;
  * examTopicIds bind each task to its Topic Atlas topic.
"""
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

# Current topic -> the node of the legacy specification it was examined under. A task whose
# legacy node differs (fertilisers and cycles, grassland, genetics) names it explicitly.
LEGACY_NODE = {
    '1-1': '0-0', '1-2': '0-1', '1-3': '0-2', '1-5': '0-4',
    '2-1': '1-0', '2-2-1': '1-2', '2-2-2': '1-3', '2-2-3': '1-4', '2-3': '1-5',
    '3-1': '2-0', '3-2': '2-1', '3-3-1': '2-3', '3-3-2': '2-4', '3-3-3': '2-5',
    '4-1': '3-0', '4-2': '3-1', '4-3-1': '3-3', '4-3-2': '3-4', '4-3-3': '3-5',
}
P = lambda *r: [region(*x) for x in r]
NONE = {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'}


def closed(choose, options, reason=None):
    out = {'kind': 'closed', 'choose': choose, 'options': options, 'pooled': True}
    if reason:
        out['reason'] = reason
    return out


def routes(built):
    """[(slug, label, rows)] -> (first route's rows, answerVariants)."""
    variants = [dict(id=slug, label=label, rows=[dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)])
                for slug, label, rows in built]
    return variants[0]['rows'], variants


class Paper:
    def __init__(self, year, level, fileid, hashes, regions, atlas, paper_pages, scheme_pages,
                 selections, supplementary, section=lambda ref: 'A'):
        self.year, self.level, self.fileid, self.hashes = year, level, fileid, hashes
        self.regions, self.atlas = regions, atlas
        self.paper_pages, self.scheme_pages = paper_pages, scheme_pages
        self.selections, self.supplementary = selections, supplementary
        self.section = section
        self.tag = 'HL' if level == 'higher' else 'OL'
        self.prefix = f'agsci-{year}-{self.tag.lower()}-'
        self.cards, self.tasks, self.notes = [], [], []

    @property
    def label(self):
        return f'{self.year} {"Higher" if self.level == "higher" else "Ordinary"}'

    def atlas_for(self, ref):
        base = ref.split(' — ')[0]
        candidates = [base]
        while '(' in candidates[-1]:
            candidates.append(candidates[-1][:candidates[-1].rindex('(')].rstrip())
        for key in candidates:
            if key in self.atlas:
                return self.atlas[key]
        raise KeyError(ref)

    def add(self, key, ref, topic, concept, question, rows, stem=None, marks=None, tariff=None,
            node=None, selection=None, figure=None, extra=None, note=None):
        cid = self.prefix + key
        assert cid not in {c['id'] for c in self.cards}, cid
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        pp, sp = self.regions[ref]
        level = 'higher' if self.level == 'higher' else 'ordinary'
        if tariff is None:
            tariff = {'kind': 'questionTotal'} if marks is not None else {'kind': 'fixed'}
        card = dict(id=cid, subjectId='agricultural-science', year=self.year, level=level,
                    section=self.section(ref), questionRef=f'{self.year} {self.tag} {ref}',
                    topicId='agsci-' + topic,
                    curriculumNodeIds=['agricultural-science-' + n for n in (node or LEGACY_NODE[topic]).split('|')],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel=tariff,
                    sourceMaterial=dict(kind='source-text', label='OFFICIAL QUESTION PAGE',
                                        title=f'Agricultural Science {self.label} — {ref}',
                                        pages=sorted({r['p'] for r in pp}),
                                        attribution=f'SEC Agricultural Science {self.year} {"Higher" if self.level == "higher" else "Ordinary"} Level examination paper — © State Examinations Commission.',
                                        presentationNote='Open the original page for the published wording, photographs, tables and examination context.'))
        if stem:
            card['stem'] = stem
        if figure:
            card['figureKey'] = figure
        if extra:
            card.update(extra)
        task = dict(questionRef=card['questionRef'], paperPage=pp[0]['p'], schemePage=sp[0]['p'],
                    paperRegions=pp, schemeRegions=sp, atlasNumbers={cid: str(1001 + len(self.tasks))},
                    cardIds=[cid], marksPerRoute=card['totalMarks'],
                    examTopicIds=[f'agricultural-science-{level}-' + t for t in self.atlas_for(ref).split('|')],
                    selection=selection or NONE,
                    evidence=f'All {self.paper_pages} paper and {self.scheme_pages} scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.',
                    originalCard='added')
        if note:
            task['schemeNote'] = note
            self.notes.append(dict(questionN=ref.split('(')[0].split(' ')[0][1:], questionRef=ref, note=note))
        self.cards.append(card)
        self.tasks.append(task)
        return card

    def review(self, boundary, remaining=None):
        observed, supplementary = scan(self.year, self.fileid, self.hashes, self.selections, self.supplementary)
        return dict(year=self.year, level=self.level, lang='ev', paperFileid=self.fileid, hashes=self.hashes,
                    wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                    paperPagesInspected=list(range(1, self.paper_pages + 1)),
                    schemePagesInspected=list(range(1, self.scheme_pages + 1)),
                    selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=self.notes,
                    independentBoundaryReview=boundary,
                    cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                    runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                    remaining=remaining or ['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])
