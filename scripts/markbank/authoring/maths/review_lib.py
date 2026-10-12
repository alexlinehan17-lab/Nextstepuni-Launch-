"""Shared writer for the independently reviewed Higher/Ordinary Mathematics papers (2019-2022).

Each review_<year>_<level>_<paper>.py script declares the paper's published scale
units (prompt lifted from the paper, scale from the scheme) and the marking
points it quotes from the scheme, each labelled with the part of the scheme it
comes from. This module turns that declaration into:

  * scripts/markbank/mathematics/reviews/<year>-<level>-<paper>.json  (the review ledger)
  * the paper's cards in scripts/markbank/authored/maths.json

Run every script from the repository root. Re-running a script on the committed
state must reproduce both outputs byte for byte (reproduce.py checks this): the
review ledger is rewritten from the declaration, existing cards are updated in
place, and a card this paper ADDED is rebuilt and compared with the committed
card instead of being appended a second time.
"""
from pathlib import Path
import hashlib, json, os, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates  # noqa: E402
import fitz  # noqa: E402

LPC, MPC, HPC, PC, FC, FCM, ZC, SOL, NOTE, STEP = ('Low Partial Credit', 'Mid Partial Credit', 'High Partial Credit', 'Partial Credit',
    'Full Credit', 'Full Credit −1 (deduction)', 'Zero Credit', 'Model solution', 'Note', 'Step')
def L(label, q): return f'{label} — {q}'
LEVEL = {'hl': 'higher', 'ol': 'ordinary', 'fl': 'foundation'}
CTX = 'Each point is labelled with the part of the printed scheme it comes from. The original scheme reader provides the full solution, including diagrams, tables and graphs.'
MARK = re.compile(r'\s*(Full Credit ?[\(]?[-−–]1[\)]?|Zero Credit):?\s*')


class Paper:
    def __init__(self, year, lv, key, bands, paper, scheme):
        self.year, self.lv, self.key, self.SC = year, lv, key, bands
        self.P = Path(f'paper-trail-corpus/exampapers/{year}/{paper}'); self.S = Path(f'paper-trail-corpus/markingschemes/{year}/{scheme}')
        self.cards = []

    def A(self, suffix, parts, scale, scheme, pages, topic, atlas, prompt, stem=None, extra=None):
        c = dict(id=f'maths-{self.year}-{self.lv}-{self.key}-q' + suffix, printedParts=parts.split(','), totalMarks=int(scale[:-1]),
                 scale=scale, permittedMarks=self.SC[scale], schemePages=scheme, topicId='maths-' + topic, sourcePages=pages,
                 examTopicIds=[f'mathematics-{LEVEL[self.lv]}-' + a for a in atlas.split(',')])
        if stem: c['stem'] = stem
        c['questionText'] = prompt
        if extra: c.update(extra)
        self.cards.append(c)

    def check(self, marks, count):
        tot = {}
        for c in self.cards:
            q = re.match(r'Q(\d+)', c['printedParts'][0])[1]; tot[q] = tot.get(q, 0) + c['totalMarks']
        assert tot == marks, tot
        assert len(self.cards) == count, len(self.cards)
        assert len({c['id'] for c in self.cards}) == count

    def review(self, marks, method, scheme_pages, general, notes, selection_review, classify):
        r = dict(schemaVersion=1, subjectId='mathematics', year=self.year, level=LEVEL[self.lv], lang='ev', paperKey=self.key,
            paperFileid=self.P.name, schemeFileid=self.S.name, specificationId='mathematics:2015',
            paperSha256=hashlib.sha256(self.P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(self.S.read_bytes()).hexdigest(),
            reviewedAt='2026-10-12', reviewMethod=method,
            paperPagesInspected=list(range(1, len(fitz.open(self.P)) + 1)), schemePagesInspected=scheme_pages,
            printedQuestionMarks=marks, fullCreditMinusOne=True, generalNotesPages=general, sourceNotes=notes, cards=self.cards,
            selectionReview=selection_review)
        dec = {}
        for c in selection_candidates(self.P):
            d = classify(c['context'])
            if d is None: raise SystemExit(c)
            dec[c['id']] = {'classification': d[0], 'reason': d[1]}
        r['selectionDecisions'] = dec
        out = Path(f'scripts/markbank/mathematics/reviews/{self.year}-{LEVEL[self.lv]}-{self.key}.json')
        out.write_text(json.dumps(r, ensure_ascii=False, indent=2) + '\n')

    def apply(self, rows, label, added=(), ref_overrides=None, expect_added=(), card_overrides=None):
        """Write the paper's cards into the authored deck.

        expect_added: ids this paper ADDS. On the first run they are appended; on a
        re-run they already exist and are rebuilt and compared, never appended twice.
        card_overrides: {id: {field: value}} applied after the card is built, for a
        later, recorded decision about a card (e.g. a withdrawal note).
        """
        ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
        byid = {c['id']: c for c in authored}
        note = f'Prompt, grouped parts and context visually checked against the original {label} on 2026-10-12; exact question and scheme pages attached by the independent review.'
        moved, new, rebuilt = 0, [], []
        ref_overrides = ref_overrides or {}
        card_overrides = card_overrides or {}
        expect_added = list(expect_added)
        def pts(cid): return [dict(id=f'{cid}-solution-{i+1}', kind='point', verbatim=q, marks=None, contextNote=CTX) for i, q in enumerate(rows[cid])]
        def fresh(c):
            parts = ', '.join(p if i == 0 else p[len(re.match(r'Q\d+', p)[0]):] for i, p in enumerate(c['printedParts']))
            a = dict(id=c['id'], topicId=c['topicId'], conceptId=c['id'].split(f'-{self.lv}-')[1], level=LEVEL[self.lv], year=self.year,
                     subjectId='maths', section='A' if int(re.match(r'Q(\d+)', c['printedParts'][0])[1]) <= 6 else 'B',
                     questionRef=f"{self.year} {self.lv.upper()} Paper {self.key[1:]} {parts}", questionText=c['questionText'],
                     tariffModel={'kind': 'questionTotal'}, totalMarks=c['totalMarks'], rows=pts(c['id']), notes=note)
            if c.get('stem'): a['stem'] = c['stem']
            a.update(card_overrides.get(c['id'], {}))
            return a
        for c in self.cards:
            a = byid.get(c['id'])
            if c['id'] in expect_added:
                built = fresh(c)
                if a is None:
                    new.append(c['id']); authored.append(built)
                else:
                    if a != built:
                        diff = sorted(k for k in set(a) | set(built) if a.get(k) != built.get(k))
                        # A deliberate change to a paper's declaration is applied with
                        # MATHS_REVIEW_UPDATE=1; without it, any drift is an error.
                        if not os.environ.get('MATHS_REVIEW_UPDATE'):
                            raise SystemExit(f'{c["id"]}: committed card differs from the rebuilt one in {diff}')
                        authored[authored.index(a)] = built
                    rebuilt.append(c['id'])
                continue
            assert a is not None, f'{c["id"]} is not in the deck and is not declared as added'
            assert a['totalMarks'] == c['totalMarks'], c['id']
            a['questionText'] = c['questionText']
            if c.get('stem'): a['stem'] = c['stem']
            else: a.pop('stem', None)
            a['notes'] = note
            if c['id'] in ref_overrides: a['questionRef'] = ref_overrides[c['id']]
            if c['id'] in rows:
                a['tariffModel'] = {'kind': 'questionTotal'}
                a['rows'] = pts(c['id'])
                a.update(card_overrides.get(c['id'], {}))
                continue
            for r in a['rows']:
                g = r.get('group')
                if not g: continue
                extra, opts = [], []
                for o in g['options']:
                    m = MARK.search(o)
                    if m:
                        parts = MARK.split(o[m.start():])
                        for lab, text in zip(parts[1::2], parts[2::2]):
                            text = text.replace('\n', '; ').strip(' ;')
                            kind = 'Zero Credit (not a band)' if lab.startswith('Zero') else 'Full Credit −1 (a deduction, not a band)'
                            extra.append(f'{kind}: {text}')
                        o = o[:m.start()].rstrip()
                    opts.append(o)
                if extra:
                    assert all(opts), (c['id'], g['options'])
                    g['options'] = opts; r['verbatim'] = opts[0]
                    r['contextNote'] = (r.get('contextNote', '').rstrip() + ' ' + '. '.join(extra) + '.').strip()
                    moved += 1
            a.update(card_overrides.get(c['id'], {}))
        assert sorted(new + rebuilt) == sorted(expect_added), (new, rebuilt, expect_added)
        ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
        print('tasks', len(self.cards), 'marks', sum(c['totalMarks'] for c in self.cards), 'rows replaced', len(rows),
              'added', new, 'rebuilt and matched', len(rebuilt), 'notes moved', moved)


def quotes(rows, path):
    json.dump(rows, open(path, 'w'), ensure_ascii=False, indent=1)
