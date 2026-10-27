"""Shared engine for a source-reviewed Construction Studies theory paper: draft, validate, integrate.

One paper is one module of data (scripts/markbank/authoring/construction_<year>_<level>.py) plus one
draft script (docs/markbank-audit/2026-09-28/drafts/construction-<year>-<level>/...-draft.py) that
writes the content. This module holds the method every paper shares:

- Draft: lifts wording from the SEC paper, builds criterion rows whose verbatim is printed in the
  scheme, composes complete-question cards from their parts, renders pixel-exact figure crops
  (single rects or multi-page composites), classifies every selection word on the paper, and
  records each in-place correction of a pre-audit card with the SHA-256 of the card it replaces.
- validate(): re-derives all of it from the pinned PDFs and the paper's own expected structure
  (independent of the draft) and refuses on any drift.
- mutation_cases(): the defects a validator must reject, generated from the paper's own structure.
- integrate(): writes the reviewed file, the authored deck input, figures, manifest, the hosted
  paper anchor (from the tracked sidecar), retired build overrides, progress aliases for withdrawn
  live cards, the Atlas bridge and the fixture entry.

Rules carried here: lift, never write exam content; choice is not a route (a printed choose-N-of-M
is ONE card with one anyN group over all M items, and live per-item IDs alias to the kept card);
every pre-audit card keeps its ID and concept ID.
"""
import copy
import functools
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import fitz

import construction_corrections
import construction_figures

R = Path(__file__).resolve().parents[3]
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
DRAFT_ROOT = R / 'docs/markbank-audit/2026-09-28/drafts'
PATTERN = r'\b(?:choose|select|one\s+of|any\s+\w+|either|or|answer\s+\w+)\b'
LIGATURES = {'Ɵ': 'ti', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
FILEID = {'higher': 'LC029ALP000EV.pdf', 'ordinary': 'LC029GLP000EV.pdf'}
CODE = {'higher': 'HL', 'ordinary': 'OL'}
WORD = {'higher': 'Higher', 'ordinary': 'Ordinary'}
CROSSWALK = R / 'data/examTopics/construction-studies-curriculum-crosswalk.json'
CHOICE_RULE = ('Choice is not a route (coordinator rule, 2026-10-12): a printed choose-N-of-M is ONE card that prints all M items '
               'with one anyN group over them, never a card per item or per combination.')


def sources(year, level):
    return (f'paper-trail-corpus/exampapers/{year}/{FILEID[level][:-4]}.pdf', f'paper-trail-corpus/markingschemes/{year}/{FILEID[level][:-4]}.pdf')


def names(year, level):
    """(figure prefix, card-ID prefix, Atlas prefix, attribution)"""
    return (f'construction-studies-{year}-{CODE[level]}-', f'cons-{year}-{CODE[level].lower()}-', f'construction-studies-{level}-',
            f'SEC Leaving Certificate Construction Studies {year} {WORD[level]} Level — © State Examinations Commission.')


def card_hash(c):
    return hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


@functools.lru_cache(maxsize=None)
def page_text(f, page):
    with fitz.open(R / f) as pdf:
        return ' '.join(pdf[page - 1].get_text().split())


@functools.lru_cache(maxsize=None)
def page_count(f):
    with fitz.open(R / f) as pdf:
        return len(pdf)


def printed(text):
    for glyph, letters in LIGATURES.items():
        text = text.replace(glyph, letters)
    return text


def tokens(text):
    return re.findall(r'[a-z0-9]+', printed(text).replace('²', '2').lower())


def is_subsequence(needle, haystack):
    it = iter(haystack)
    return all(word in it for word in needle)


def normalise(text):
    return re.sub(r'[^a-z0-9Ā-ſ]+', '', printed(text).lower())


def r(n):
    return list(range(n + 1))


def qkey_of(key):
    return '10-alt' if key.startswith('q10-alt') else key[1:].split('-')[0]


def observed_selections(P):
    out = []
    with fitz.open(R / P) as pdf:
        for i, p in enumerate(pdf):
            text = ' '.join(p.get_text().split())
            out.extend((i + 1, m.start(), m.group(), text[max(0, m.start() - 80):m.end() + 80]) for m in re.finditer(PATTERN, text, re.I))
    return out


def region(P, qkey, paper_page, tails=None, alt=False, unnumbered=()):
    """The printed text of one question: from its number to the next question's (Q10 splits at OR when an
    alternative is printed). tails maps a question to a marker after which the text layer places more of it;
    a (marker, anchor) pair puts that text back after the anchor, where the page prints it (2013 OL Q6(a)'s
    bullets sit in the text layer after Q9). unnumbered names questions printed without the full stop after
    their number ("5 (a)")."""
    text = printed(page_text(P, paper_page[qkey]))
    if alt and qkey == '10':
        return text[text.index(' 10. '):text.index(' OR ')]
    if qkey == '10-alt':
        return text[text.index(' OR ') + 4:]
    mark = lambda n: f' {n} (a) ' if n in unnumbered else f' {n}. '  # noqa: E731
    start = text.index(mark(qkey))
    nxt = [text.index(mark(n), start) for n in map(str, range(int(qkey) + 1, 11)) if mark(n) in text[start:]]
    body = text[start:min(nxt) if nxt else len(text)]
    if tails and qkey in tails:
        marker, anchor = tails[qkey] if isinstance(tails[qkey], tuple) else (tails[qkey], None)
        tail = text[text.index(marker) + len(marker):]
        if anchor is None:
            body += tail
        else:
            assert body.count(anchor) == 1, (qkey, anchor)
            body = body.replace(anchor, anchor + tail.rstrip())
    return body


# ---------------------------------------------------------------- drafting
class Draft:
    """Write one paper's tasks. The pre-audit cards are snapshotted before integration so the draft
    regenerates byte-identically afterwards."""

    def __init__(self, here, year, level, hashes, legacy_count, questions, scheme_pages, alt=None):
        self.here, self.year, self.level = Path(here), year, level
        self.P, self.S = sources(year, level)
        self.FP, self.PREFIX, self.CROSS, self.ATTRIBUTION = names(year, level)
        self.hashes = {self.P: hashes[0], self.S: hashes[1]}
        for f, h in self.hashes.items():
            assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
        self.questions, self.scheme_pages, self.alt = questions, scheme_pages, alt
        legacy_file = self.here / f'prior-{year}-{level}-cards.json'
        if not legacy_file.exists():
            authored = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
            legacy_file.write_text(json.dumps([c for c in authored if c['id'].startswith(self.PREFIX)], ensure_ascii=False, indent=2) + '\n')
        self.legacy = {c['id']: c for c in json.loads(legacy_file.read_text())}
        assert len(self.legacy) == legacy_count, sorted(self.legacy)
        self.tasks, self.bindings, self.cards, self.question_figures = [], [], {}, []

    # figures
    def paper(self, page, rect):
        return (self.P, page, rect, False)

    def scheme(self, page, rect):
        return (self.S, page, rect, True)

    def composite(self, *panels):
        return construction_figures.composite([(self.S, p, rc) for p, rc in panels])

    def figures(self, specs):
        self.figure_specs = specs
        self.question_figures = [construction_figures.entry(self.FP + key, spec, self.here / f'{self.FP}{key}.png') for key, spec in specs.items()]

    def checks(self, paper_page, scheme_pages):
        return ([dict(file=self.P, page=p, textSha256=hashlib.sha256(page_text(self.P, p).encode()).hexdigest()) for p in (1, paper_page)]
                + [dict(file=self.S, page=p, textSha256=hashlib.sha256(page_text(self.S, p).encode()).hexdigest()) for p in [2, 3, *scheme_pages]])

    @staticmethod
    def row(rid, verbatim, marks, note, steps=None):
        steps = steps or r(marks)
        assert steps[0] == 0 and steps[-1] == marks
        return dict(id=rid, kind='criterion', verbatim=verbatim, marks=marks, contextNote=note, permittedMarks=steps)

    @staticmethod
    def anyn(rid, verbatim, claim, per, options, note):
        """options: [(scheme heading, note)]"""
        return dict(id=rid, kind='anyN', verbatim=verbatim, marks=claim * per,
                    contextNote=note + ' ' + ' '.join(f'{h}: {n}' for h, n in options),
                    group=dict(claimMax=claim, perOption=per, options=[h for h, _ in options]))

    def add(self, q, key, ref, text, rows, nodes, topics, figure, review, boundary, selection, groups=None, total=None, alt=False):
        meta = self.alt if alt else self.questions[q]
        qkey = '10-alt' if alt else q
        cid = f'{self.PREFIX}q{qkey}-{key}'
        concept = self.legacy[cid]['conceptId'] if cid in self.legacy else f"{meta['concept']}-{key}"
        card = dict(id=cid, subjectId='construction-studies', year=self.year, level=self.level, section='B',
                    topicId=nodes[0], conceptId=concept, questionRef=f'{self.year} {CODE[self.level]} Q{qkey}{ref}',
                    stem=meta['stem'], questionText=text, tariffModel={'kind': 'fixed'},
                    totalMarks=total if total is not None else sum(x['marks'] for x in rows), rows=rows,
                    questionFigureKey=f'{self.FP}q{qkey}-original', questionFigureIncludesPrompt=True)
        if figure:
            card['figureKey'] = self.FP + figure
        label = (f"ORIGINAL QUESTION 10{' — ALTERNATIVE' if alt else ''}" if (q == '10' and self.alt) else f'ORIGINAL QUESTION {q}')
        card['sourceMaterial'] = dict(kind='source-illustration', label=label, title=meta['title'], pages=[1, meta['page']],
                                      attribution=self.ATTRIBUTION, presentationNote=meta['note'])
        if groups:
            card['taskGroups'] = groups
        self.tasks.append(dict(questionNumber=q, alternative=alt, correction=cid in self.legacy, card=card,
                               sourceChecks=self.checks(meta['page'], self.scheme_pages[qkey]), boundaryReview=boundary, selectionReview=selection,
                               requiredQuestionFigures=[card['questionFigureKey']], requiredSolutionFigures=[self.FP + figure] if figure else []))
        self.bindings.append(dict(cardId=cid, markBankTopicId=nodes[0], canonicalTopicIds=nodes, canonicalTopicReview=review,
                                  questionNumber=q, atlasTopicIds=[self.CROSS + t for t in topics]))
        self.cards[cid] = card
        return card

    def compose(self, q, key, ref, children, figure, boundary, selection, text, labels=None, alt=False):
        qkey = '10-alt' if alt else q
        rows, groups = [], []
        for i, child in enumerate(children):
            prefix = child['id'].removeprefix(f'{self.PREFIX}q{qkey}-')
            rs = copy.deepcopy(child['rows'])
            for x in rs:
                x['id'] = f"{prefix}-{x['id']}"
            rows += rs
            groups.append(dict(sourceCardId=child['id'], label=labels[i] if labels else prefix, marks=child['totalMarks'],
                               rowIds=[x['id'] for x in rs]))
        kids = [next(b for b in self.bindings if b['cardId'] == c['id']) for c in children]
        nodes = list(dict.fromkeys(n for b in kids for n in b['canonicalTopicIds']))
        topics = list(dict.fromkeys(t.removeprefix(self.CROSS) for b in kids for t in b['atlasTopicIds']))
        return self.add(q, key, ref, text, rows, nodes, topics, figure, 'Keeps the union of its separately reviewed constituent tasks.',
                        boundary, selection, groups=groups, total=sum(c['totalMarks'] for c in children), alt=alt)

    @staticmethod
    def parts(*pairs):
        return '\n\n'.join(f'({letter}) {text}' for letter, text in pairs)

    def finish(self, ledger, finite_choices, reasons, consolidated=None, taxonomy_gaps=(), marked_alike=None, whole_choices=()):
        """whole_choices: keys of cards that are a whole question on their own: a choice card (an Ordinary Q8 term
        list) or an unlettered question (2013 Ordinary Q5, one drawing)."""
        observed = observed_selections(self.P)
        assert [(o[0], o[2]) for o in observed] == [(x[0], x[1]) for x in ledger], [(o[0], o[2]) for o in observed]
        selection_ledger = dict(pattern=PATTERN, unclassified=0, sourceHashes=self.hashes,
                                rows=[dict(page=o[0], start=o[1], match=o[2], context=o[3], classification=x[2]) for o, x in zip(observed, ledger)],
                                finiteQuestionChoices=finite_choices)
        if marked_alike:
            selection_ledger['optionSelectionsMarkedAlike'] = marked_alike
        consolidated = consolidated or {}
        kept_whole = set(whole_choices)
        choice_cards = {v['cardId'] for v in finite_choices.values()}
        whole = {}
        for t in self.tasks:
            c = t['card']
            if c['id'].endswith('-complete') or c['id'].removeprefix(self.PREFIX) in kept_whole:
                parts = [g['label'] for g in c.get('taskGroups', [])] or (['one card over every printed item'] if c['id'] in choice_cards
                                                                          else ['the whole unlettered question'])
                whole.setdefault('10-alt' if t['alternative'] else t['questionNumber'], []).append(dict(id=c['id'], parts=parts, marks=c['totalMarks']))
        assert set(reasons) | set(consolidated) == {k.removeprefix(self.PREFIX) for k in self.legacy}, \
            sorted({k.removeprefix(self.PREFIX) for k in self.legacy} ^ (set(reasons) | set(consolidated)))
        corrections = []
        for t in self.tasks:
            c = t['card']
            if c['id'] in self.legacy:
                old = self.legacy[c['id']]
                assert old['conceptId'] == c['conceptId'], c['id']
                corrections.append(dict(cardId=c['id'], priorSha256=card_hash(old), correctedSha256=card_hash(c),
                                        priorTotalMarks=old['totalMarks'], correctedTotalMarks=c['totalMarks'],
                                        priorTopicId=old['topicId'], correctedTopicId=c['topicId'],
                                        reason='Question wording lifted from the paper. ' + reasons[c['id'].removeprefix(self.PREFIX)]))
        assert len(corrections) == len(reasons)
        merged = [dict(cardId=self.PREFIX + k, aliasOf=self.PREFIX + v, preCorrectionSha256=card_hash(self.legacy[self.PREFIX + k]))
                  for k, v in consolidated.items()]
        out = dict(schemaVersion=1, subjectId='construction-studies', year=self.year, level=self.level, lang='ev', sitting='main',
                   paperKey='single', fileid=FILEID[self.level], component='theory',
                   status=f"Q1–Q{len(self.questions)}{' and alternative Q10' if self.alt else ''} source-reviewed draft; integration pending.",
                   sourceHashes=self.hashes, tasks=self.tasks, bindings=self.bindings, questionFigures=self.question_figures,
                   addedIds=[t['card']['id'] for t in self.tasks if not t['correction']], corrections=corrections,
                   selectionLedger=selection_ledger, questionRouteLedgers={q: dict(wholeRoutes=w) for q, w in whole.items()},
                   taxonomyGaps=list(taxonomy_gaps), questionsReviewed=list(self.questions), unreviewedQuestions=[],
                   alternativeQuestions=['10'] if self.alt else [])
        if merged:
            out['consolidatedLegacy'] = merged
        (self.here / f'{self.level}-{self.year}-draft.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(dict(tasks=len(self.tasks), added=len(out['addedIds']), corrected=len(corrections), consolidated=len(merged),
                              figures=len(self.question_figures),
                              perQuestion={q: sum(1 for t in self.tasks if t['questionNumber'] == q and not t['alternative']) for q in self.questions},
                              alternative=sum(1 for t in self.tasks if t['alternative']))))
        return out


# ---------------------------------------------------------------- validation
def _get(m, name, default):
    return getattr(m, name, default)


def validate(d, m, images=True, figure_dir=FIGURE_DIR, integrated=True):
    """m is the paper module: YEAR, LEVEL, HASHES, LEAF, COMPOSITE, TOTALS, TOPICS, FIGURES, SOLUTION, LEGACY,
    PAPER_PAGE, SCHEME_PAGES, LEDGER, PRIOR_COUNT and the optional CHOICES, LABELLED, GAPS, CONSOLIDATED,
    WORKED, RETIRED, TAILS, ALT, MARKED_ALIKE, CHOICE_FIGURE_PAGES."""
    year, level = m.YEAR, m.LEVEL
    P, S = sources(year, level)
    FP, PREFIX, CROSS, _ = names(year, level)
    choices, labelled, gaps = _get(m, 'CHOICES', {}), _get(m, 'LABELLED', set()), _get(m, 'GAPS', {})
    consolidated, worked, retired = _get(m, 'CONSOLIDATED', {}), _get(m, 'WORKED', []), _get(m, 'RETIRED', [])
    tails, alt = _get(m, 'TAILS', {}), _get(m, 'ALT', False)
    hashes = {P: m.HASHES[0], S: m.HASHES[1]}
    assert d['sourceHashes'] == hashes
    for f, h in hashes.items():
        assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
    assert (d['subjectId'], d['year'], d['level'], d['lang'], d['sitting'], d['paperKey'], d['fileid'], d['component']) == (
        'construction-studies', year, level, 'ev', 'main', 'single', FILEID[level], 'theory')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    expected = set(m.LEAF) | set(m.COMPOSITE)
    n = len(expected)
    assert set(cards) == expected and len(d['tasks']) == n, sorted(set(cards) ^ expected)
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks'] if t['card']['id'].removeprefix(PREFIX) not in m.LEGACY]
    assert len(d['addedIds']) == n - len(m.LEGACY) and all(t['correction'] == (k in m.LEGACY) for k, t in tasks.items())
    assert len({c['questionRef'] for c in cards.values()}) == n
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert set(bindings) == expected and len(d['bindings']) == n
    scheme = normalise(' '.join(page_text(S, p) for p in range(1, page_count(S) + 1)))
    crosswalk = json.loads(CROSSWALK.read_text())
    registry = set(re.findall(r"id: '(cons-\d+-\d+)'", (R / 'curriculumRegistry.ts').read_text()))
    library_nodes = {x for nodes in crosswalk.values() for x in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(m.FIGURES) and len(d['questionFigures']) == len(m.FIGURES)

    for key, c in cards.items():
        qk = qkey_of(key)
        q = '10' if qk == '10-alt' else qk
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q and t.get('alternative', False) == (qk == '10-alt'), key
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', year, level, 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f'{year} {CODE[level]} Q{qk}'), key
        assert c['questionFigureKey'] == f'{FP}q{qk}-original' and c['questionFigureIncludesPrompt'] is True, key
        assert c['sourceMaterial']['pages'] == [1, m.PAPER_PAGE[qk]] and t['requiredQuestionFigures'] == [c['questionFigureKey']], key
        assert c.get('figureKey') == (FP + m.SOLUTION[key] if key in m.SOLUTION else None), key
        assert t['requiredSolutionFigures'] == ([FP + m.SOLUTION[key]] if key in m.SOLUTION else []), key
        assert figures[f'q{qk}-original']['solution'] is False and (key not in m.SOLUTION or figures[m.SOLUTION[key]]['solution'] is True), key
        # Lift, never write: printed wording only; an item named by reference carries the scheme's heading after ' — '.
        words = tokens(region(P, qk, m.PAPER_PAGE, tails, alt, _get(m, 'UNNUMBERED', ())))
        heads, labels = [], []
        for para in c['questionText'].split('\n\n'):
            head, _, tail = para.partition(' — ')
            heads.append(head)
            labels += tail.split('; ') if tail else []
        assert is_subsequence(tokens(' '.join(heads)), words), (key, 'questionText not lifted')
        assert all(normalise(x) in scheme for x in labels), (key, 'item label not printed in the scheme')
        assert bool(labels) == (key in labelled), (key, labels)
        assert is_subsequence(tokens(c['stem']), words), (key, 'stem not lifted')
        for row in c['rows']:
            assert row['contextNote'].strip(), (key, row['id'])
            if row['kind'] == 'anyN':  # a closed choice: every printed option, in the scheme's own headings
                assert 'permittedMarks' not in row and row['marks'] == row['group']['claimMax'] * row['group']['perOption'], (key, row['id'])
                assert normalise(row['verbatim']) in scheme and all(normalise(o) in scheme for o in row['group']['options']), key
                continue
            assert row['kind'] == 'criterion', (key, row['id'])
            assert normalise(row['verbatim']) in scheme, (key, row['verbatim'])
            steps = row['permittedMarks']
            assert steps[0] == 0 and steps[-1] == row['marks'] and steps == sorted(set(steps)), (key, row['id'])
            # The named components a row is priced in (construction_rows.py): the scheme's own words, adding up to the row.
            for part in row.get('parts', []):
                assert normalise(part['verbatim']) in scheme and part['marks'] > 0, (key, row['id'], part['id'])
                assert part['permittedMarks'][0] == 0 and part['permittedMarks'][-1] == part['marks'] and part['permittedMarks'] == sorted(set(part['permittedMarks'])), (key, row['id'], part['id'])
            if row.get('parts'):
                assert len(row['parts']) >= 2 and len({p['id'] for p in row['parts']}) == len(row['parts']) and sum(p['marks'] for p in row['parts']) == row['marks'], (key, row['id'])
        assert 'questionBonus' not in c and c['totalMarks'] == sum(row['marks'] for row in c['rows']) == m.TOTALS[key], key
        if key in m.LEAF:
            assert [(row['id'], row['marks'], row.get('permittedMarks')) for row in c['rows']] == m.LEAF[key], key
            assert 'taskGroups' not in c, key
            nodes, topics = m.TOPICS[key]
            assert b['canonicalTopicIds'] == nodes and b['atlasTopicIds'] == [CROSS + x for x in topics], key
            covered = {x for a in b['atlasTopicIds'] for x in crosswalk[a]}
            assert set(nodes) - covered == gaps.get(key, set()), (key, 'canonical topics outside the Atlas crosswalk', set(nodes) - covered)
        else:
            kids = m.COMPOSITE[key]
            assert [g['sourceCardId'] for g in c['taskGroups']] == [PREFIX + k for k in kids] and len(kids) >= 2, key
            rows = []
            for kid, g in zip(kids, c['taskGroups']):
                rs = copy.deepcopy(cards[kid]['rows'])
                for row in rs:
                    row['id'] = kid.removeprefix(f'q{qk}-') + '-' + row['id']
                assert g['rowIds'] == [row['id'] for row in rs] and g['marks'] == cards[kid]['totalMarks'] and len(rs) <= 5 and g['label'].strip(), (key, kid)
                rows += rs
            assert c['rows'] == rows, key
            assert b['canonicalTopicIds'] == list(dict.fromkeys(x for k in kids for x in bindings[k]['canonicalTopicIds'])), key
            assert b['atlasTopicIds'] == list(dict.fromkeys(x for k in kids for x in bindings[k]['atlasTopicIds'])), key
        assert b['markBankTopicId'] == c['topicId'] == b['canonicalTopicIds'][0], key
        assert set(b['canonicalTopicIds']) <= registry & library_nodes and len(set(b['canonicalTopicIds'])) == len(b['canonicalTopicIds']), key
        assert all(x.startswith(CROSS) and x in crosswalk for x in b['atlasTopicIds']) and b['atlasTopicIds'], key
        assert len(b['canonicalTopicIds']) == 1 or b['canonicalTopicReview'].strip(), key
        assert [(x['file'], x['page']) for x in t['sourceChecks']] == [(P, 1), (P, m.PAPER_PAGE[qk])] + [(S, p) for p in [2, 3, *m.SCHEME_PAGES[qk]]], key
        for x in t['sourceChecks']:
            assert hashlib.sha256(page_text(x['file'], x['page']).encode()).hexdigest() == x['textSha256'], (key, x)

    # Worked answers quoted in the calculation cards are the scheme's own figures.
    for key, pages, values in worked:
        notes = ' '.join(row['contextNote'] for row in cards[key]['rows'])
        text = ' '.join(page_text(S, p) for p in pages)
        assert all(x in notes and x in text for x in values), (key, [x for x in values if x not in notes or x not in text])
    # The alternative Question 10 never combines with the printed Question 10.
    for key, c in cards.items():
        for g in c.get('taskGroups', []):
            assert key.startswith('q10-alt') == g['sourceCardId'].startswith(PREFIX + 'q10-alt'), key
    # Choice is not a route: each printed choice is ONE card holding one anyN group over every printed item,
    # and its figure carries every item's scheme drawings.
    for key, (rid, claim, per, options) in choices.items():
        anyn = [row for row in cards[key]['rows'] if row['kind'] == 'anyN']
        assert [row['id'] for row in anyn] == [rid] and anyn[0]['group'] == dict(claimMax=claim, perOption=per, options=options), key
    assert sorted(k for k in cards if any(row['kind'] == 'anyN' for row in cards[k]['rows']) and k not in m.COMPOSITE) == sorted(choices)
    for key in choices:
        assert not [k for k in cards if k.startswith(key + '-')], (key, 'per-item or per-combination route cards')
    for key, pages in _get(m, 'CHOICE_FIGURE_PAGES', {}).items():
        assert pages <= {p for _, p, _ in construction_figures.panels_of(m.FIGURES[m.SOLUTION[key]])}, (key, 'a choice item lost its scheme drawings')
    # One whole route per question: a complete card (or the one choice card that is the whole question), each worth the full marks.
    ledgers = d['questionRouteLedgers']
    full = 60 if level == 'higher' else 50
    kept_whole = set(_get(m, 'WHOLE_CHOICES', set()))  # choice cards and unlettered questions that are a whole question
    for qk in [str(i) for i in range(1, len(m.QUESTIONS) + 1)] + (['10-alt'] if alt else []):
        whole = sorted(k for k in cards if qkey_of(k) == qk and (k.endswith('-complete') or k in kept_whole))
        assert len(whole) == 1 and [w['id'] for w in ledgers[qk]['wholeRoutes']] == [PREFIX + k for k in whole], qk
        assert all(cards[k]['totalMarks'] == full for k in whole), qk
    sel = d['selectionLedger']
    assert sel['pattern'] == PATTERN and sel['unclassified'] == 0 and all(x['classification'].strip() for x in sel['rows'])
    assert {k: v['cardId'] for k, v in sel['finiteQuestionChoices'].items()} == {k: PREFIX + v for k, v in m.FINITE.items()}
    assert sel.get('optionSelectionsMarkedAlike') == _get(m, 'MARKED_ALIKE', None)
    observed = [(o[0], o[1], o[2]) for o in observed_selections(P)]
    assert observed == [(x['page'], x['start'], x['match']) for x in sel['rows']] and [(o[0], o[2]) for o in observed] == list(m.LEDGER)

    for key, f in figures.items():  # pixel-exact: a single crop, or a composite of exact page crops
        construction_figures.check(f, m.FIGURES[key], figure_dir, images)
    assert len({f['sha256'] for f in d['questionFigures']}) == len(m.FIGURES)

    # In-place corrections: same ID and concept ID, hash-linked to the pre-audit card they replace.
    drafts = DRAFT_ROOT / f'construction-{year}-{level}'
    legacy = {c['id']: c for c in json.loads((drafts / f'prior-{year}-{level}-cards.json').read_text())}
    assert set(legacy) == {PREFIX + k for k in m.LEGACY | set(consolidated)}
    fixes = {x['cardId']: x for x in d['corrections']}
    assert set(fixes) == {PREFIX + k for k in m.LEGACY} and len(d['corrections']) == len(m.LEGACY)
    merged = {x['cardId']: x for x in d.get('consolidatedLegacy', [])}
    assert merged == {PREFIX + k: dict(cardId=PREFIX + k, aliasOf=PREFIX + v, preCorrectionSha256=card_hash(legacy[PREFIX + k]))
                      for k, v in consolidated.items()}
    for cid, old in legacy.items():
        if cid in merged:
            continue
        new, fix = cards[cid.removeprefix(PREFIX)], fixes[cid]
        assert fix['priorSha256'] == card_hash(old) and fix['correctedSha256'] == card_hash(new), cid
        assert new['conceptId'] == old['conceptId'] and fix['reason'].strip(), cid
        assert (fix['priorTotalMarks'], fix['correctedTotalMarks'], fix['priorTopicId'], fix['correctedTopicId']) == (
            old['totalMarks'], new['totalMarks'], old['topicId'], new['topicId']), cid

    authored = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    by_id = {c['id']: c for c in authored}
    assert len(by_id) == len(authored)
    if integrated:
        prior = json.loads((drafts / 'prior-authored-card-hashes.json').read_text())
        assert prior['count'] == len(prior['cards']) == m.PRIOR_COUNT
        for cid in fixes:
            assert prior['cards'][cid] == fixes[cid]['priorSha256'], cid
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
        assert sorted(c for c in by_id if c.startswith(PREFIX)) == sorted(t['card']['id'] for t in d['tasks'])
        gone = {w['cardId']: w for w in d.get('withdrawn', [])}
        aliases = construction_corrections.card_aliases()
        assert set(gone) == set(merged)
        for cid, x in merged.items():  # live per-item cards withdrawn through a recorded progress alias to the kept card
            assert cid not in by_id and gone[cid]['aliasOf'] == x['aliasOf'] == aliases[cid], cid
            assert gone[cid]['priorSha256'] == x['preCorrectionSha256'] == prior['cards'][cid], cid
        for name in ['card-source-bindings.json', 'card-corrections.json']:  # no build-time override may replace reviewed content
            overrides = json.loads((R / 'scripts/markbank' / name).read_text()).get('construction-studies', {})
            assert not [k for k in overrides if k.startswith(PREFIX)], name
        assert sorted((x['file'], x['cardId']) for x in d.get('retiredBuildOverrides', [])) == sorted((f'scripts/markbank/{f}', PREFIX + k) for f, k in retired)
        assert all(x['reason'].strip() and 'override' in x for x in d.get('retiredBuildOverrides', []))
    elif integrated is False:  # before integration (None skips authored checks)
        assert all(card_hash(by_id[cid]) == card_hash(old) for cid, old in legacy.items())
    found = {}
    for g in d['taxonomyGaps']:
        assert g['atlasTopicId'] in bindings[g['cardId'].removeprefix(PREFIX)]['atlasTopicIds'] and g['reason'].strip()
        found.setdefault(g['cardId'].removeprefix(PREFIX), set()).update(g['canonicalTopicIds'])
    assert found == {k: v for k, v in gaps.items() if k in m.LEAF}
    assert d['questionsReviewed'] == [str(i) for i in range(1, len(m.QUESTIONS) + 1)] and d['unreviewedQuestions'] == []
    assert d.get('alternativeQuestions', []) == (['10'] if alt else [])
    return dict(tasks=n, addedTasks=n - len(m.LEGACY), correctedTasks=len(m.LEGACY), consolidatedLegacy=len(consolidated),
                leafTasks=len(m.LEAF), wholeQuestions=sum(len(v['wholeRoutes']) for v in ledgers.values()),
                anyNChoiceCards=len(choices), sourceFigures=len(m.FIGURES), paperComplete=True)


# ---------------------------------------------------------------- mutation cases
def mutation_cases(m, original):
    """The defects a paper's validator must reject, generated from the paper's own structure."""
    _, PREFIX, CROSS, _ = names(m.YEAR, m.LEVEL)
    FP = names(m.YEAR, m.LEVEL)[0]

    def card(d, key):
        return next(t['card'] for t in d['tasks'] if t['card']['id'] == PREFIX + key)

    def binding(d, key):
        return next(b for b in d['bindings'] if b['cardId'] == PREFIX + key)

    def figure(d, key):
        return next(f for f in d['questionFigures'] if f['key'] == FP + key)

    def clone(d, key, new_key):
        t = copy.deepcopy(next(t for t in d['tasks'] if t['card']['id'] == PREFIX + key))
        t['card']['id'] = PREFIX + new_key
        d['tasks'].append(t)

    cases = {}
    leaves = sorted(m.LEAF)
    rowful = next(k for k in leaves if any(x['kind'] == 'criterion' and x['marks'] >= 4 for x in card(original, k)['rows']))
    for key in sorted(getattr(m, 'CHOICES', {})):
        cases[f'{key} split into a per-item card'] = lambda d, k=key: clone(d, k, k + '-item')
        cases[f'{key} option dropped'] = lambda d, k=key: next(x for x in card(d, k)['rows'] if x['kind'] == 'anyN')['group']['options'].pop()
        cases[f'{key} claim limit changed'] = lambda d, k=key: next(x for x in card(d, k)['rows'] if x['kind'] == 'anyN')['group'].update(
            claimMax=next(x for x in card(d, k)['rows'] if x['kind'] == 'anyN')['group']['claimMax'] + 1)
        cases[f'{key} printed list trimmed'] = lambda d, k=key: card(d, k).update(questionText=card(d, k)['questionText'].rsplit(';', 1)[0] + '; invented item.')
        if key in m.SOLUTION:
            cases[f'{key} loses its solution figure'] = lambda d, k=key: card(d, k).pop('figureKey')
    comps = [k for k, spec in m.FIGURES.items() if construction_figures.is_composite(spec)]
    if comps:
        cases['composite loses a panel'] = lambda d: figure(d, comps[0])['panels'].pop()
    singles = [k for k, spec in m.FIGURES.items() if not construction_figures.is_composite(spec) and spec[3]]
    if singles:
        cases['cut off drawing'] = lambda d: figure(d, singles[0]).update(rect=figure(d, singles[0])['rect'][:3] + [figure(d, singles[0])['rect'][1] + 40])
    if getattr(m, 'ALT', False):
        cases['alternative combined with Q10'] = lambda d: card(d, 'q10-alt-complete')['taskGroups'].append(dict(sourceCardId=PREFIX + 'q10-a', label='a', marks=1, rowIds=[]))
    labelled = sorted(getattr(m, 'LABELLED', set()))
    if labelled:
        cases['invented item label'] = lambda d: card(d, labelled[0]).update(questionText=card(d, labelled[0])['questionText'].split(' — ')[0] + ' — Invented heading')
        cases['item named without its scheme heading'] = lambda d: card(d, labelled[0]).update(questionText=card(d, labelled[0])['questionText'].split(' — ')[0])
    complete = sorted(k for k in m.COMPOSITE if k.endswith('-complete') and len(m.COMPOSITE[k]) > 2)
    cases['lost part in the complete question'] = lambda d: card(d, complete[0])['taskGroups'].pop(1)
    cases['invented question wording'] = lambda d: card(d, leaves[0]).update(questionText='Explain why every house is always cheaper to heat.')
    stemmed = next(k for k in leaves if card(original, k)['stem'])
    cases['paraphrased stem'] = lambda d: card(d, stemmed).update(stem='A paraphrased description of the sketch.')
    cases['marking row not in scheme'] = lambda d: next(x for x in card(d, rowful)['rows'] if x['kind'] == 'criterion').update(verbatim='Any sensible answer')
    cases['changed tariff'] = lambda d: next(x for x in card(d, rowful)['rows'] if x['kind'] == 'criterion' and x['marks'] >= 4).update(
        marks=3, permittedMarks=r(3))
    pres = [k for k in leaves if any(x['id'] == 'presentation' for x in card(original, k)['rows'])]
    if pres:
        def reband(d):
            x = next(x for x in card(d, pres[0])['rows'] if x['id'] == 'presentation')
            x['permittedMarks'] = [0, x['marks']] if x['permittedMarks'] != [0, x['marks']] else r(x['marks'])
        cases['dropped drawing allowance'] = lambda d: card(d, pres[0])['rows'].pop()
        cases['changed drawing band'] = reband
    for key, _, _ in getattr(m, 'WORKED', [])[:2]:
        cases[f'wrong worked answer {key}'] = lambda d, k=key: [x.update(contextNote='Answer = 1.') for x in card(d, k)['rows']]
    multi = next(k for k in leaves if len(m.TOPICS[k][1]) > 1)
    cases['missing Atlas association'] = lambda d: binding(d, multi)['atlasTopicIds'].pop()
    cases['canonical node outside the crosswalk'] = lambda d: binding(d, leaves[0])['canonicalTopicIds'].append('cons-1-4')
    cases['broken composite topic union'] = lambda d: binding(d, complete[0])['canonicalTopicIds'].pop()
    cases['unreviewed source crop'] = lambda d: d['questionFigures'][1].update(visuallyInspected=False)
    sol_key = next(k for k in leaves if k in m.SOLUTION)
    cases['solution shown before reveal'] = lambda d: card(d, sol_key).update(questionFigureKey=FP + m.SOLUTION[sol_key])
    cases['unclassified selection'] = lambda d: d['selectionLedger'].update(unclassified=1)
    cases['selection row dropped'] = lambda d: d['selectionLedger']['rows'].pop()
    cases['uncertain source'] = lambda d: d['sourceHashes'].update({sources(m.YEAR, m.LEVEL)[0]: 'changed'})
    legacy = sorted(m.LEGACY)
    if legacy:
        cases['correction loses its concept ID'] = lambda d: card(d, legacy[0]).update(conceptId='renamed-concept')
        cases['correction not hash-linked'] = lambda d: d['corrections'][0].update(priorSha256='0' * 64)
        cases['legacy card replaced without a record'] = lambda d: d['corrections'].pop()
        cases['legacy card counted as an addition'] = lambda d: d['addedIds'].append(PREFIX + legacy[-1])
    if getattr(m, 'CONSOLIDATED', {}):
        cases['consolidation not hash-linked'] = lambda d: d['consolidatedLegacy'][0].update(preCorrectionSha256='0' * 64)
        cases['consolidated card aliased to the wrong card'] = lambda d: d['consolidatedLegacy'][0].update(aliasOf=PREFIX + leaves[0])
        cases['withdrawal not recorded'] = lambda d: d['withdrawn'].pop()
    if getattr(m, 'RETIRED', []):
        cases['stale build override kept'] = lambda d: d.update(retiredBuildOverrides=[])
    if getattr(m, 'GAPS', {}):
        gk = sorted(m.GAPS)[0]
        cases['undeclared taxonomy gap'] = lambda d: d['taxonomyGaps'].pop()
        cases['taxonomy gap pointing outside the card topics'] = lambda d: d['taxonomyGaps'][0].update(atlasTopicId=CROSS + 'sound')
    return cases


# ---------------------------------------------------------------- integration
def integrate(m, here, alt_text, anchor_from_sidecar=False):
    """Not replay-safe: refuses once the reviewed file exists."""
    year, level = m.YEAR, m.LEVEL
    P, _ = sources(year, level)
    FP, PREFIX, _, ATTRIBUTION = names(year, level)
    here = Path(here)
    read = lambda p: json.loads(Path(p).read_text())  # noqa: E731

    def save(p, d):
        # Keep a shared file's own indentation (card-corrections.json is indent 1, most others indent 2).
        indent = 1 if Path(p).exists() and Path(p).read_text().startswith('{\n "') else 2
        Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=indent) + '\n')

    draft = read(here / f'{level}-{year}-draft.json')
    report = validate(draft, m, figure_dir=here, integrated=False)
    review_path = R / f'scripts/markbank/authored/construction-studies-{year}-{level}-reviewed.json'
    bridge_path = R / f'scripts/markbank/atlas-reviews/construction-studies-{year}-{level}.json'
    authored_path = R / 'scripts/markbank/authored/construction-studies.json'
    manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
    aliases_path = R / 'components/MarkBank/cardAliases.ts'
    fixture = R / 'test/fixtures/constructionReviewedPapers.json'
    anchor_path = R / f'public/paper-anchors/{year}/{FILEID[level]}.json'
    assert not review_path.exists() and not bridge_path.exists()
    assert (R / f"examiner-reports/construction-studies/schemes/{year}-{'hl' if level == 'higher' else 'ol'}.md").exists()
    prior = read(authored_path)
    assert len(prior) == m.PRIOR_COUNT and len({c['id'] for c in prior}) == m.PRIOR_COUNT
    tasks = draft['tasks']
    corrected = {t['card']['id']: t['card'] for t in tasks if t['correction']}
    added = [t['card'] for t in tasks if not t['correction']]
    withdrawn_ids = [x['cardId'] for x in draft.get('consolidatedLegacy', [])]
    assert set(corrected) | set(withdrawn_ids) == {c['id'] for c in prior if c['id'].startswith(PREFIX)}
    assert not {c['id'] for c in added} & {c['id'] for c in prior}
    assert not {c['questionRef'] for c in [*added, *corrected.values()]} & {c['questionRef'] for c in prior if c['id'] not in corrected and c['id'] not in withdrawn_ids}
    manifest = read(manifest_path)
    known_md5 = {e['md5'] for e in manifest.values()}
    assert set(alt_text) == {f['key'].removeprefix(FP) for f in draft['questionFigures']}
    for f in draft['questionFigures']:
        src = here / f"{f['key']}.png"
        md5 = hashlib.md5(src.read_bytes()).hexdigest()
        assert f['key'] not in manifest and md5 not in known_md5 and not (FIGURE_DIR / src.name).exists(), f['key']
        known_md5.add(md5)

    if anchor_from_sidecar:  # the tracked classic sidecar's question anchors, each checked against its printed marker
        assert not anchor_path.exists()
        sidecar = read(R / f'scripts/paper-trail/answers/{year}/{FILEID[level]}.json')
        with fitz.open(R / P) as pdf:
            for q in sidecar['q']:
                page = pdf[q['pP'] - 1]
                h = page.rect.height
                lines = [(ln['bbox'][1] / h, ''.join(s['text'] for s in ln['spans']).strip())
                         for b in page.get_text('dict')['blocks'] for ln in b.get('lines', [])]
                marker = q['n'] if q['n'] in getattr(m, 'UNNUMBERED', ()) else f"{q['n']}."  # "5 (a)" printed without a full stop
                hits = [y for y, text in lines if text.split()[0:1] == [marker]]
                assert hits and abs(min(hits, key=lambda y: abs(y - q['pY'][0])) - q['pY'][0]) < 0.02, (q['n'], q['pY'], hits)
        anchor = dict(band=[1, 1], component='000', copyright=sidecar['copyright'], paperFileid=sidecar['paperFileid'], paperOnly=1, schemeFileid='', v=1,
                      q=[dict(conf=0.5, mode='pagejump', n=q['n'], pP=q['pP'], pY=q['pY'], region=[{'p': 1}]) for q in sidecar['q']])
        assert [q['n'] for q in anchor['q']] == [str(i) for i in range(1, len(m.QUESTIONS) + 1)] and sidecar['paperFileid'] == FILEID[level]
        anchor_path.write_text(json.dumps(anchor, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
    else:
        anchor = read(anchor_path)
        assert anchor['paperOnly'] == 1 and [q['n'] for q in anchor['q']] == [str(i) for i in range(1, len(m.QUESTIONS) + 1)]

    now = datetime.now(timezone.utc).isoformat()
    prior_hashes = {c['id']: card_hash(c) for c in prior}
    save(here / 'prior-authored-card-hashes.json', dict(count=m.PRIOR_COUNT, algorithm='sha256 of json.dumps(card, ensure_ascii=False, sort_keys=True)', cards=prior_hashes))
    for f in draft['questionFigures']:
        dst = FIGURE_DIR / f"{f['key']}.png"
        shutil.copyfile(here / dst.name, dst)
        manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(),
                                  alt=alt_text[f['key'].removeprefix(FP)], attribution=ATTRIBUTION, solution=f['solution'])
    save(manifest_path, manifest)

    retired = []
    for name, key in getattr(m, 'RETIRED', []):
        path = R / 'scripts/markbank' / name
        overrides = read(path)
        old = overrides['construction-studies'].pop(PREFIX + key)
        save(path, overrides)
        retired.append(dict(file=f'scripts/markbank/{name}', cardId=PREFIX + key, override=old,
                            reason='A pre-audit build-time override. The reviewed card carries its own lifted wording, scheme rows and source material, so the override is retired rather than allowed to replace reviewed content.'))
    for name in ['card-source-bindings.json', 'card-corrections.json']:
        assert not [k for k in read(R / 'scripts/markbank' / name).get('construction-studies', {}) if k.startswith(PREFIX)], name

    withdrawn = [dict(cardId=x['cardId'], priorSha256=prior_hashes[x['cardId']], reason=CHOICE_RULE, aliasOf=x['aliasOf'])
                 for x in draft.get('consolidatedLegacy', [])]
    if withdrawn:
        text = aliases_path.read_text()
        assert text.rstrip().endswith('};') and not any(f'"{w["cardId"]}"' in text for w in withdrawn)
        kept = sorted({w['aliasOf'] for w in withdrawn})
        block = (f'  /* {now[:10]}. Construction Studies {year} {WORD[level]}: each printed choice is one card (choice is not a route); the\n'
                 f'   * pre-audit per-item cards are consolidated into {", ".join(kept)} and their progress goes to it. */\n'
                 + ''.join(f'  "{w["cardId"]}": "{w["aliasOf"]}",\n' for w in withdrawn))
        aliases_path.write_text(text.rstrip()[:-2] + block + '};\n')

    extra = dict(withdrawn=withdrawn) if withdrawn else {}
    if retired:
        extra['retiredBuildOverrides'] = retired
    status = (f"{year} {WORD[level]} main English theory Q1–Q{len(m.QUESTIONS)}{' and the alternative Q10' if getattr(m, 'ALT', False) else ''}: "
              f"{len(tasks)} source-reviewed tasks ({len(added)} added, {len(corrected)} pre-audit cards corrected in place under their original IDs"
              + (f'; {len(withdrawn)} live per-item cards withdrawn into their one choice card through progress aliases' if withdrawn else '')
              + '); whole theory paper reconciled against the original paper and scheme. Practical component and Irish edition remain separate work.')
    review = dict(draft, status=status, reviewedAt=now, paperComplete=True, **extra,
                  fullPaperReconciliation=dict(questions=len(m.QUESTIONS), alternativeQuestions=1 if getattr(m, 'ALT', False) else 0,
                                               examRubric=m.RUBRIC + '; no full-exam Cartesian cards.',
                                               method=f'Same-operator source review of the paper and every scheme page; validator construction_{year}_{level}.py on the shared engine construction_paper.py.',
                                               validator=report),
                  priorAuthoredCardHashes=str((here / 'prior-authored-card-hashes.json').relative_to(R)),
                  priorCorrectedCards=str((here / f'prior-{year}-{level}-cards.json').relative_to(R)))
    save(review_path, review)
    gone = set(withdrawn_ids)
    merged = [corrected.get(c['id'], c) for c in prior if c['id'] not in gone] + added
    save(authored_path, merged)
    check = read(authored_path)
    kept_ids = [c['id'] for c in prior if c['id'] not in gone]
    assert [c['id'] for c in check[:len(kept_ids)]] == kept_ids and check[len(kept_ids):] == added
    save(bridge_path, dict(schemaVersion=1, subjectId='construction-studies', year=year, level=level, lang='ev', sitting='main',
                           paperKey='single', reviewedAt=now, authoringReview=str(review_path.relative_to(R)), sourceHashes=draft['sourceHashes'],
                           expectedRuntimeCards=len(tasks), reason=status,
                           questions=[dict(n=q, fileid=FILEID[level], topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q for t in b['atlasTopicIds']}))
                                      for q in draft['questionsReviewed']],
                           cards=draft['bindings']))
    papers = read(fixture) if fixture.exists() else []
    assert not [p for p in papers if (p['year'], p['level']) == (year, level)]
    papers.append(dict(year=year, level=level, validator=f'scripts/markbank/authoring/construction_{year}_{level}.py', result=report,
                       priorCount=m.PRIOR_COUNT, addedIds=[c['id'] for c in added], correctedIds=[t['card']['id'] for t in tasks if t['correction']],
                       withdrawnIds=withdrawn_ids, keptChoiceIds=sorted({w['aliasOf'] for w in withdrawn}),
                       choiceCardIds=[PREFIX + k for k in sorted(getattr(m, 'CHOICES', {}))]))
    papers.sort(key=lambda p: (-p['year'], p['level']))
    save(fixture, papers)
    save(here / 'integration.json', dict(reviewedAt=now, addedTasks=len(added), correctedTasks=len(corrected), withdrawnIntoAlias=len(withdrawn),
                                         retiredOverrides=len(retired), newAuthoredCount=len(merged), newFigures=len(draft['questionFigures']), validator=report))
    print(f'Integrated {len(tasks)} tasks ({len(added)} added, {len(corrected)} corrected, {len(withdrawn)} aliased, {len(retired)} overrides retired); '
          f'authored deck input {len(merged)} cards; {len(draft["questionFigures"])} figures.')


def main(m):
    """Validator entry point for a paper module."""
    print(json.dumps(validate(json.loads((R / f'scripts/markbank/authored/construction-studies-{m.YEAR}-{m.LEVEL}-reviewed.json').read_text()), m)))


if __name__ == '__main__':
    sys.exit('Run a paper module, e.g. python3 scripts/markbank/authoring/construction_2022_higher.py')
