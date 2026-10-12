"""Shared writer for the independently reviewed 2026 Higher/Ordinary Mathematics papers.

Each review_2026_<level>_<paper>.py script declares the paper's published scale
units (prompt lifted from the paper, scale from the scheme) and the solution
lines it quotes from the scheme. This module writes the review ledger
(scripts/markbank/mathematics/reviews/2026-<level>-<paper>.json) and the paper's
cards in scripts/markbank/authored/maths.json.

Run every script from the repository root. On a first run the cards are
appended. On a re-run, when every card already exists, each card is rebuilt and
compared with the committed one, and the review ledger is rewritten from the
declaration -- so reproduce.py can prove the committed output byte for byte.
"""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates

SCALES = {}

def scale_marks(code, table):
    return table[code]

class Paper:
    def __init__(self, *, year, level, paper_key, paper_file, scheme_file, prefix, ref, scales,
                 reviewed_at, general_notes, scheme_pages, printed_marks, review_method, source_notes,
                 out_name, atlas_prefix, section_of):
        self.__dict__.update(locals()); del self.__dict__['self']
        self.cards = []

    def add(self, suffix, parts, scale, scheme, pages, topic, atlas, prompt, quotes, stem=None, extra=None):
        card = dict(
            id=f'{self.prefix}-q{suffix}', printedParts=parts.split(','), totalMarks=int(scale[:-1]),
            scale=scale, permittedMarks=self.scales[scale], schemePages=scheme, topicId='maths-' + topic,
            sourcePages=pages, examTopicIds=[self.atlas_prefix + a for a in atlas.split(',')],
        )
        if stem:
            card['stem'] = stem
        card['questionText'] = prompt
        card['solutionQuotes'] = quotes
        if extra:
            card.update(extra)
        self.cards.append(card)

    def write(self, selection_review, classify, finite_choices=None):
        P = Path(f'paper-trail-corpus/exampapers/{self.year}/{self.paper_file}')
        S = Path(f'paper-trail-corpus/markingschemes/{self.year}/{self.scheme_file}')
        import fitz
        n_pages = len(fitz.open(P))
        totals = {}
        for c in self.cards:
            q = re.match(r'Q(\d+[A-Z]?)', c['printedParts'][0])[1]
            totals[q] = totals.get(q, 0) + c['totalMarks']
            assert c['permittedMarks'][-1] == c['totalMarks'], c['id']
            assert all(1 <= p <= n_pages for p in c['sourcePages']), c['id']
            assert set(c['schemePages']) <= set(self.scheme_pages), c['id']
        assert totals == self.printed_marks, (totals, self.printed_marks)
        ids = [c['id'] for c in self.cards]
        assert len(ids) == len(set(ids))
        parts = [p for c in self.cards for p in c['printedParts']]
        assert len(parts) == len(set(parts)), 'repeated printed part'
        review = dict(
            schemaVersion=1, subjectId='mathematics', year=self.year, level=self.level, lang='ev',
            paperKey=self.paper_key, paperFileid=P.name, schemeFileid=S.name, specificationId='mathematics:2015',
            paperSha256=hashlib.sha256(P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(S.read_bytes()).hexdigest(),
            reviewedAt=self.reviewed_at, reviewMethod=self.review_method,
            paperPagesInspected=list(range(1, n_pages + 1)), schemePagesInspected=self.scheme_pages,
            printedQuestionMarks=self.printed_marks, fullCreditMinusOne=True, generalNotesPages=self.general_notes,
            sourceNotes=self.source_notes, cards=self.cards, selectionReview=selection_review,
        )
        if finite_choices:
            review['finiteChoices'] = finite_choices
        decisions = {}
        for cand in selection_candidates(P):
            d = classify(cand)
            if not d:
                raise SystemExit(f'unclassified selection directive {cand}')
            decisions[cand['id']] = {'classification': d[0], 'reason': d[1]}
        review['selectionDecisions'] = decisions
        out = Path('scripts/markbank/mathematics/reviews') / self.out_name
        out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
        authored_path = Path('scripts/markbank/authored/maths.json')
        authored = json.loads(authored_path.read_text())
        existing = {c['id']: c for c in authored}
        present = [i for i in ids if i in existing]
        assert not present or len(present) == len(ids), f'partially present paper: {len(present)} of {len(ids)}'
        rerun = bool(present)
        level_word = {'higher': 'Higher Level', 'ordinary': 'Ordinary Level'}[self.level]
        for c in self.cards:
            q = int(re.match(r'Q(\d+)', c['printedParts'][0])[1])
            card = dict(
                id=c['id'], topicId=c['topicId'], conceptId=c['id'].split(f'-{self.year}-')[1].split('-', 1)[1],
                level=self.level, year=self.year, subjectId='maths', section=self.section_of(q),
                questionRef=f'{self.ref} ' + ', '.join(c['printedParts']),
            )
            if c.get('stem'):
                card['stem'] = c['stem']
            card.update(
                questionText=c['questionText'], tariffModel={'kind': 'questionTotal'}, totalMarks=c['totalMarks'],
                rows=[dict(id=f"{c['id']}-solution-{i + 1}", kind='point', verbatim=a, marks=None,
                           contextNote='The original scheme reader provides the full solution, including graphical answers and all credit notes.')
                      for i, a in enumerate(c['solutionQuotes'])],
                notes=f'Independently visually checked against the {self.year} {level_word} Paper {self.paper_key[1:]} and its scheme on {self.reviewed_at}.',
            )
            if rerun:
                if existing[c['id']] != card:
                    diff = sorted(k for k in set(card) | set(existing[c['id']]) if card.get(k) != existing[c['id']].get(k))
                    raise SystemExit(f"{c['id']}: committed card differs from the rebuilt one in {diff}")
            else:
                authored.append(card)
        authored_path.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
        print('rebuilt and matched' if rerun else 'appended', 'tasks', len(self.cards), 'offered marks', sum(c['totalMarks'] for c in self.cards), '->', out)
