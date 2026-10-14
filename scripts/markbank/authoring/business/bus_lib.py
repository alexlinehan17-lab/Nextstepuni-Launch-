"""Level-aware helpers for reviewing a Business paper into rubric cards.

Question strings are slices of the normalised SEC paper text (asserted
present); quoted scheme strings are asserted present on the cited scheme page.
Legacy card IDs keep their ID and total and receive a pinned correction.
"""
from abq_authoring import response, notes
from pathlib import Path
import hashlib, json, re, unicodedata, fitz
import sys
sys.path.insert(0, 'scripts/markbank')
from glyph_ids import load_table as load_glyph_table, document_map, page_text

ORIGINAL = {c['id']: c for c in json.load(open('scripts/markbank/authored/business.json'))}


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    for a, b in {'Ɵ': 'ti', 'Ʃ': 'tt', 'Ō': 'ft', '‐': '-', '\xa0': ' ', ' ': ' ', '': ' ', '': ' '}.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()


def comps(label, marks, names=None, i=1):
    return response(i, label, [(f'component-{k}', names[k - 1] if names else f'Component {k}', m)
                               for k, m in enumerate(marks, 1)])


def points(label, n, marks, names=None):
    return [comps(f'{label} {i}', marks, names, i) for i in range(1, n + 1)]


def seq(*groups):
    out = []
    for g in groups:
        out.extend(g if isinstance(g, list) else [g])
    for i, r in enumerate(out, 1):
        r['id'] = f'response-{i}'
    return out


def unequal(label, splits, names):
    return seq([comps(f'{label} {i}', s, names) for i, s in enumerate(splits, 1)])


def single(label, mark, name=None):
    r = response(1, label, [('component-1', name or label, mark)])
    r['allocations'][0]['permittedMarks'] = [0, mark]
    return r


def ten_five(label):
    """The common OL 'two points' tariff: 10 (7 + 3) and 5 (4 + 1), not tied to named items."""
    return unequal(label, [(7, 3), (4, 1)], None)


def cumulative_steps(seq_marks):
    steps, total = [0], 0
    for m in seq_marks:
        total += m
        steps.append(total)
    return steps


class Paper:
    def __init__(self, year, level, papers, scheme, tariff):
        self.year, self.level = year, level
        self.lv = 'hl' if level == 'higher' else 'ol'
        self.LV = 'HL' if level == 'higher' else 'OL'
        self.papers, self.scheme_id, self.tariff = papers, scheme, tariff
        self.docs = {f: fitz.open(f'paper-trail-corpus/exampapers/{year}/{f}.pdf') for f in papers.values()}
        # Before 2020 the paper and its scheme share one file id (LC033GLP000EV),
        # so the scheme's pages are held under a key of their own.
        self.scheme_key = scheme if scheme not in papers.values() else scheme + '#scheme'
        self.docs[self.scheme_key] = fitz.open(f'paper-trail-corpus/markingschemes/{year}/{scheme}.pdf')
        # Read every glyph by its font and glyph id (scripts/markbank/glyph_ids.py)
        # before normalising, so a lifted snippet never inherits "seƫng", nor the
        # "/($9,1*" or "W\x04z\x1c" a CID font with no Unicode leaves for
        # "LEAVING" and "PAYE". page_text reads each glyph where it is drawn; the
        # document map then catches a mangled code point the trace did not place.
        table = load_glyph_table()
        self.text = {}
        for f, d in self.docs.items():
            dmap = document_map(d, table)[0]
            for i, p in enumerate(d):
                self.text[(f, i + 1)] = norm(''.join(dmap.get(c, c) for c in page_text(p, table)))
        self.created, self.pools = [], []

    def lift(self, section, page, *snippets, sep='\n'):
        book = self.papers[section]
        for s in snippets:
            assert s in self.text[(book, page)], (book, page, s)
        return sep.join(snippets)

    def scheme(self, page, snippet):
        assert snippet in self.text[(self.scheme_key, page)], (page, snippet)
        return snippet

    def source(self, kind, f):
        return dict(fileid=f + '.pdf', sha256=hashlib.sha256(
            Path(f'paper-trail-corpus/{kind}/{self.year}/{f}.pdf').read_bytes()).hexdigest())

    def sources(self, section):
        return dict(exampapers=self.source('exampapers', self.papers[section]),
                    markingschemes=self.source('markingschemes', self.scheme_id))

    def add(self, section, q, suffix, ref, prompt, total, topic, concept, page, support, requirement, responses,
            guidance=None, extra=None, marknote=None, fix=None, new=False):
        cid = f'bus-{self.year}-{self.lv}-s{section}-q{q}{suffix}'
        c = dict(id=cid, year=self.year, level=self.level, section=str(section), paperFileid=self.papers[section],
                 paperPages=[page], sourceLabel='QUESTION PAPER',
                 sourceTitle=f'{self.year} Business · Section {section} Question {q}',
                 questionRef=f'{self.year} {self.LV} Section {section} {ref}', questionText=prompt, totalMarks=total,
                 topicId=topic, conceptId=concept,
                 rubric=dict(system='business', taskRequirements=requirement if isinstance(requirement, list) else [requirement],
                             guidance=guidance or [], responses=responses, schemeFileid=self.scheme_id,
                             schemePages=[self.tariff[(section, q)]] + support, markingGuideNote=marknote or notes))
        if extra:
            c['additionalTopicIds'] = extra
        marks = sum(a['maxMarks'] for r in responses for a in r['allocations'])
        assert marks == total, (cid, marks, total)
        assert len({r['id'] for r in responses}) == len(responses), cid
        legacy = ORIGINAL.get(cid)
        if legacy:
            assert not new, cid
            assert legacy['totalMarks'] == total, (cid, legacy['totalMarks'], total)
            changes = ['question text lifted from the printed paper', 'the published response allocations replace the fixed example ticks']
            if legacy['questionRef'] != c['questionRef']:
                changes.append(f"the reference is corrected from “{legacy['questionRef']}”")
            if legacy['topicId'] != topic:
                changes.append(f"canonical topic corrected from {legacy['topicId']} to {topic}")
            if fix:
                changes.append(fix)
            c['correction'] = dict(originalQuestionText=legacy['questionText'], originalTotalMarks=legacy['totalMarks'],
                reason=f"Visually verified paper page {page} and scheme PDF pages {', '.join(map(str, c['rubric']['schemePages']))}: "
                       + '; '.join(changes) + '. Retain the existing card ID and total marks.')
        self.created.append(c)
        return c

    def cumulative(self, section, q, suffix, ref, prompt, sequence, topic, concept, page, support, key, extra=None, fix=None, noun='answers'):
        total = sum(sequence)
        steps = cumulative_steps(sequence)
        c = self.add(section, q, suffix, ref, prompt, total, topic, concept, page, support,
                     f'Complete every row. The published sequence is {" + ".join(map(str, sequence))}.',
                     [comps('Correct answers', (total,), ['Total from the published sequence'])],
                     [key, f'For {", ".join(map(str, range(len(steps) - 1)))} or {len(steps) - 1} correct {noun}, record {", ".join(map(str, steps[:-1]))} or {steps[-1]} marks. The larger allowances are not tied to particular printed rows.'],
                     extra, marknote='Use the official answer key and the published sequence. Each correct answer counts once.', fix=fix)
        c['rubric']['responses'][0]['allocations'][0]['permittedMarks'] = steps
        return c

    def pool(self, section, q, suffix, ref, page, schemes, choose, wording, prompt, options, total, requirement, guidance,
             topic, concept, selection, legacy=None, ordered=None):
        pid = f'bus-{self.year}-{self.lv}-s{section}-q{q}{suffix}'
        p = dict(id=pid, choose=choose, sourceWording=wording, routePrompt=prompt, options=options,
                 review=dict(status='partial-subject-review', year=self.year, level=self.level, section=str(section), question=ref,
                             sources=self.sources(section), paperPagesReviewed=[page], schemePagesReviewed=schemes,
                             boundaries={ref: total}, selectionAnalysis=selection, sourceClarifications=guidance),
                 template=dict(year=self.year, level=self.level, section=str(section), paperFileid=self.papers[section], paperPages=[page],
                               sourceLabel='QUESTION PAPER', sourceTitle=f'{self.year} Business · Section {section} Question {q}',
                               questionRef=f'{self.year} {self.LV} Section {section} Q{ref}', totalMarks=total, conceptId=concept,
                               rubric=dict(system='business', taskRequirements=[requirement], guidance=guidance, schemeFileid=self.scheme_id,
                                           schemePages=schemes, markingGuideNote=notes)))
        if legacy:
            p['legacyRoute'] = legacy
        if ordered:
            p['orderedResponses'] = ordered
        for o in options:
            o.setdefault('topicId', topic)
        self.pools.append(p)
        return p

    def write(self, sections, selection_text, classify, topic_reason, abq=None, component_ids=()):
        qnum = lambda c: c['questionRef'].split(' Q')[1].split('(')[0].split(' ')[0]
        path = Path('components/MarkBank/cards/business/rubric-authored.json')
        d = json.loads(path.read_text())
        ids = {c['id'] for c in self.created}
        d['cards'] = [c for c in d['cards'] if c['id'] not in ids] + self.created
        d['reviews'] = [r for r in d['reviews'] if not (r['year'] == self.year and r['level'] == self.level and r['section'] in [str(s) for s, _ in sections])]
        for section, questions in sections:
            for q in questions:
                cohort = [c for c in self.created if c['section'] == str(section) and qnum(c) == str(q)]
                if not cohort:
                    continue
                d['reviews'].append(dict(
                    status='partial-subject-review', year=self.year, level=self.level, section=str(section), question=str(q),
                    cardIds=[c['id'] for c in cohort], sources=self.sources(section), paperPagesReviewed=sorted({p for c in cohort for p in c['paperPages']}),
                    schemePagesReviewed=sorted({p for c in cohort for p in c['rubric']['schemePages']}),
                    boundaries={c['id'].split('-q', 1)[1]: c['totalMarks'] for c in cohort},
                    selectionAnalysis=selection_text[section], sourceClarifications=[g for c in cohort for g in c['rubric']['guidance']]))
        d['cards'].sort(key=lambda c: (c['year'], c['section'], c['id']))
        d['reviews'].sort(key=lambda r: (r['year'], r['section'], r['question']))
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

        if self.pools:
            path = Path('components/MarkBank/cards/business/route-pools.json')
            rp = json.loads(path.read_text())
            rp['pools'] = [p for p in rp['pools'] if p['id'] not in {x['id'] for x in self.pools}] + self.pools
            path.write_text(json.dumps(rp, ensure_ascii=False, indent=2) + '\n')

        path = Path('data/examTopics/business-source-reviewed-topics.json')
        t = json.loads(path.read_text())
        t['questions'] = [r for r in t['questions'] if not (r['year'] == self.year and r['level'] == self.level and r['n'] != 'ABQ')]
        single = len(set(self.papers.values())) == 1
        for section, questions in sections:
            key = 'single' if single else ('p1' if section == 1 else 'p2')
            for q in questions:
                cohort = [c for c in self.created if c['section'] == str(section) and qnum(c) == str(q)]
                topics = list(dict.fromkeys(x for c in cohort for x in [c['topicId']] + c.get('additionalTopicIds', [])))
                for p in self.pools:
                    if p['template']['section'] == str(section) and p['template']['questionRef'].split(' Q')[1].split('(')[0] == str(q):
                        topics += [o['topicId'] for o in p['options'] if o['topicId'] not in topics]
                n = f'S{section}Q{q}' if single and section > 1 else str(q)
                t['questions'].append(dict(year=self.year, level=self.level, paperKey=key, n=n, canonicalNodeIds=list(dict.fromkeys(topics)),
                                           reason=topic_reason.format(year=self.year, section=section, q=q)))
        t['questions'].sort(key=lambda r: (r['year'], r['level'], r['paperKey'], str(r['n'])))
        path.write_text(json.dumps(t, ensure_ascii=False, indent=2) + '\n')

        path = Path('scripts/markbank/authored/business-selection-reviews.json')
        sel = json.loads(path.read_text())
        inv = json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
        counted = 0
        for doc in inv['documents']:
            if not (doc['year'] == self.year and doc['level'] == self.level and doc['language'] == 'ev'):
                continue
            for item in doc['selectionDirectives']:
                if item['id'] in sel['reviews']:
                    continue
                cat, why, pid = classify(doc['paperFileid'].replace('.pdf', ''), item['page'], item['matchedText'], item['wording'])
                r = dict(wording=item['wording'], paperSha256=item['paperSha256'], classification=cat, reason=why)
                if pid:
                    r['cardId' if cat == 'finite-choice' else 'poolId'] = pid
                sel['reviews'][item['id']] = r
                counted += 1
        path.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')
        return counted


def fixed(label, entries):
    """Named entries that are each right or wrong (no partial marks)."""
    r = response(1, label, [(f'entry-{k}', name, m) for k, (name, m) in enumerate(entries, 1)])
    for a in r['allocations']:
        a['permittedMarks'] = [0, a['maxMarks']]
    return r


def legacy_route(cid, selected, page, schemes, note):
    legacy = ORIGINAL[cid]
    return dict(id=cid, selectedOptionIds=selected, correction=dict(
        originalQuestionText=legacy['questionText'], originalTotalMarks=legacy['totalMarks'],
        reason=f"Visually verified paper page {page} and scheme PDF pages {', '.join(map(str, schemes))}: {note} "
               'Retain the existing card ID and total marks for saved progress.'))


def opt_resp(parts):
    return dict(allocations=[dict(id=k, label=l, maxMarks=m, permittedMarks=list(range(m + 1))) for k, l, m in parts])


def permit(card, response_index, steps, allocation_index=0):
    card['rubric']['responses'][response_index]['allocations'][allocation_index]['permittedMarks'] = steps
    return card
