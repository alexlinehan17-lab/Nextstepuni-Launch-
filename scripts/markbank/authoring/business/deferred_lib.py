"""The SEC's deferred Business sittings, carded as papers of their own.

    from deferred_lib import Sitting, response, notes
    D = Sitting(2022, 'higher', {1: 'LC033ALP032EV', 2: 'LC033ALP041EV', 3: 'LC033ALP041EV'}, 'LC033ALP000EV')
    D.add(1, 'q1', 'Q1', D.lift(1, 3, '...'), 10, 'business-3-18', 'tax-abbreviations', 3, [3], '...', [...])
    D.emit(selection, atlas)

A deferred sitting is the SEC's own examination for candidates who could not sit
in June (deferredexams/<year>/ and deferredmarkingschemes/<year>/ in the
corpus). Its booklets are filed by Paper Trail as "<fileid>-deferred" and are
numbered as June's, so every card names the sitting three times, as every
deferred card in the bank does (CARD-STANDARD.md section 4): its id
("bus-2022-hl-deferred-s1-q1"), its reference ("2022 HL Section 1 Q1 —
Deferred sitting") and its booklet ("LC033ALP032EV-deferred").

The cards are June's rubric cards (components/MarkBank/cards/business/rubric.ts)
and are built the same way as the June generators (add-<year>.py): question
strings are slices of the normalised SEC paper text, every quoted scheme string
is asserted present on the scheme page it cites, marks must sum to the printed
tariff. The scheme's printed responses (`rubric.expected`, what bus_expected.py
lifts for June) are quoted line by line from the cited scheme page and asserted
present there; nothing is typed in their place.

They are kept in their own file, components/MarkBank/cards/business/
deferred-authored.json, so June's generators, inventory and expected-answer
lifter (which key a sitting by year and level alone) never see them, and each
deferred generator replaces only its own sitting's records there.
"""
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import fitz

STORE = Path('components/MarkBank/cards/business/deferred-authored.json')
# The Topic Atlas questions a deferred sitting prints, with the topics of the cards each holds (registry.ts reads
# them under the booklet's own file id; scripts/paper-trail/business_deferred.py tags them for Paper Trail).
ATLAS = Path('data/examTopics/business-deferred-question-topics.json')
NOTES = ('The official support notes give possible responses, not an exhaustive list. Other relevant answers are '
         'considered on their merits. Apply the published allocation to your answer; do not count the same point twice.')
LINK_NOTE = ('Use a separate relevant quotation, phrase or statement from the case study for each point. No link is '
             'awarded without relevant theory.')
DEFERRED_REF = ' — Deferred sitting'


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    for a, b in {'Ɵ': 'ti', 'Ʃ': 'tt', 'Ō': 'ft', '‐': '-', '\xa0': ' ', ' ': ' ', '': ' '}.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()


def response(i, label, parts):
    a = [dict(id=k, label=l, maxMarks=m, permittedMarks=list(range(m + 1))) for k, l, m in parts]
    for x in a:
        if x['id'] == 'link':
            x['requiresAnyOf'] = [y['id'] for y in a if y['id'] in ['name', 'explain', 'develop']]
    return dict(id=f'response-{i}', label=label, allocations=a)


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


def unequal(label, splits, names=None):
    return seq([comps(f'{label} {i}', s, names) for i, s in enumerate(splits, 1)])


class Sitting:
    def __init__(self, year, level, booklets, scheme):
        self.year, self.level = year, level
        self.lv = 'hl' if level == 'higher' else 'ol'
        self.LV = self.lv.upper()
        self.booklets = booklets            # section -> SEC file id (June's id; the deferred folder holds it)
        self.scheme_fid = scheme
        paths = {fid: Path(f'paper-trail-corpus/deferredexams/{year}/{fid}.pdf') for fid in set(booklets.values())}
        paths[scheme] = Path(f'paper-trail-corpus/deferredmarkingschemes/{year}/{scheme}.pdf')
        self.paths = paths
        self.text = {}
        for fid, path in paths.items():
            with fitz.open(path) as doc:
                for i, page in enumerate(doc):
                    self.text[(fid, i + 1)] = norm(page.get_text())
        self.cards, self.pools, self.questions = [], [], {}

    # ---------------------------------------------------------------- lifting
    def lift(self, section, page, *snippets, sep='\n'):
        fid = self.booklets[section]
        for s in snippets:
            assert s in self.text[(fid, page)], (fid, page, s)
        return sep.join(snippets)

    def sch(self, page, snippet):
        assert norm(snippet) == snippet, snippet
        assert snippet in self.text[(self.scheme_fid, page)], (page, snippet)
        return snippet

    def expected(self, page, *items):
        """The scheme's printed responses for a part, item by item, each quoted from its page.

        An item is a string, (string, [detail lines]) or (page, string[, details]) where the item sits on
        another page than the first (a response list that runs on)."""
        out = []
        for n, item in enumerate(items, 1):
            p, details = page, []
            if isinstance(item, tuple):
                if isinstance(item[0], int):
                    p, item, *rest = item
                    details = rest[0] if rest else []
                else:
                    item, details = item
            entry = {'id': f'e{n}', 'text': self.sch(p, item)}
            if details:
                entry['detail'] = [self.sch(p, d) for d in details]
            out.append(entry)
        return {'page': page, 'items': out}

    def split(self, spans, heads, drop=(), first=None):
        """The scheme's printed responses cut at their own printed headings.

        spans: [(page, start, end)] -- the page text from `start` (inclusive) up to `end` (exclusive; None for
        the page's end), each asserted on its page, joined in order. heads: the printed headings (or item
        openings) that start each response, in print order, each asserted in the block. Each item is its
        heading, with the words up to the next heading as its detail. drop: marks-column furniture the text
        layer interleaves with the prose ("2@7 (5+2) Benefit and Link"), each asserted present and removed.
        Every word is the page's own; this only says where one printed response ends and the next begins."""
        block = []
        for page, start, end in spans:
            text = self.text[(self.scheme_fid, page)]
            a = text.find(start)
            assert a >= 0, (page, start)
            b = len(text) if end is None else text.find(end, a + len(start))
            assert b >= 0, (page, end)
            block.append(text[a:b].strip())
        block = ' '.join(block)
        for d in drop:
            assert d in block, d
            block = block.replace(d, ' ')
        block = re.sub(r'\s+', ' ', block)
        at, pos = [], 0
        for h in heads:
            i = block.find(h, pos)
            assert i >= 0, (spans[0][0], h)
            at.append(i)
            pos = i + len(h)
        items = []
        for n, (h, i) in enumerate(zip(heads, at)):
            j = at[n + 1] if n + 1 < len(at) else len(block)
            detail = block[i + len(h):j].strip()
            entry = {'id': f'e{n + 1}', 'text': h}
            if detail:
                entry['detail'] = [detail]
            items.append(entry)
        return {'page': first or spans[0][0], 'items': items}

    def source(self, fid, kind):
        return dict(fileid=f'{fid}.pdf', sha256=hashlib.sha256(
            Path(f'paper-trail-corpus/{kind}/{self.year}/{fid}.pdf').read_bytes()).hexdigest())

    def sources(self, section):
        return dict(deferredexams=self.source(self.booklets[section], 'deferredexams'),
                    deferredmarkingschemes=self.source(self.scheme_fid, 'deferredmarkingschemes'))

    # ---------------------------------------------------------------- cards
    def cid(self, section, key):
        return f'bus-{self.year}-{self.lv}-deferred-s{section}-{key}'

    def add(self, section, key, ref, prompt, total, topic, concept, page, schemes, requirement, responses,
            guidance=(), expected=None, extra=None, marknote=None, label=None, title=None, pages=None):
        c = dict(id=self.cid(section, key), year=self.year, level=self.level, section=str(section),
                 paperFileid=f'{self.booklets[section]}-deferred', paperPages=pages or [page],
                 sourceLabel=label or 'QUESTION PAPER',
                 sourceTitle=title or f'{self.year} Business deferred · Section {section} Question {qnum(ref)}',
                 questionRef=f'{self.year} {self.LV} Section {section} {ref}{DEFERRED_REF}', questionText=prompt,
                 totalMarks=total, topicId=topic, conceptId=concept,
                 rubric=dict(system='business', taskRequirements=requirement if isinstance(requirement, list) else [requirement],
                             guidance=list(guidance), responses=responses, schemeFileid=f'{self.scheme_fid}-deferred',
                             schemePages=list(schemes), markingGuideNote=marknote or NOTES))
        if label == 'CASE STUDY':
            del c['sourceLabel']
        if extra:
            c['additionalTopicIds'] = extra
        if expected:
            assert expected['page'] in schemes, (c['id'], expected['page'], schemes)
            # Cut from the scheme page's own text at its printed anchors, as June's hand-checked slices are
            # (bus_expected.py, business-expected-slices.json): the text layer may join a two-column page's
            # words in another order than the scheme markdown, so the provenance gate reads them word by word.
            c['rubric']['expected'] = {**expected, 'lifted': 'slice'}
        marks = sum(a['maxMarks'] for r in responses for a in r['allocations'])
        assert marks == total, (c['id'], marks, total)
        assert len({r['id'] for r in responses}) == len(responses), c['id']
        assert c['id'] not in {x['id'] for x in self.cards}, c['id']
        self.cards.append(c)
        return c

    def cumulative(self, section, key, ref, prompt, total, seqmarks, topic, concept, page, schemes, requirement,
                   permitted, expected=None, guidance=(), extra=None, marknote=None):
        c = self.add(section, key, ref, prompt, total, topic, concept, page, schemes, requirement,
                     [comps('Correct answers', (total,), ['Total from the published sequence'])], guidance, expected, extra,
                     marknote or 'Use the official answer key and the published cumulative sequence. Each correct answer counts once.')
        c['rubric']['responses'][0]['allocations'][0]['permittedMarks'] = permitted
        return c

    # ---------------------------------------------------------------- finite pools
    def pool(self, key, ref, page, schemes, choose, wording, prompt, options, total, requirement, guidance, topic,
             concept, selection, ordered=None, expected=None, label=None):
        section = 3 if self.level == 'higher' else 2
        template = dict(year=self.year, level=self.level, section=str(section),
                        paperFileid=f'{self.booklets[section]}-deferred', paperPages=[page],
                        sourceLabel=label or 'QUESTION PAPER',
                        sourceTitle=f'{self.year} Business deferred · Section {section} Question {qnum(ref)}',
                        questionRef=f'{self.year} {self.LV} Section {section} {ref}{DEFERRED_REF}',
                        totalMarks=total, conceptId=concept,
                        rubric=dict(system='business', taskRequirements=[requirement], guidance=guidance,
                                    schemeFileid=f'{self.scheme_fid}-deferred', schemePages=schemes, markingGuideNote=NOTES))
        if expected:
            template['rubric']['expected'] = {**expected, 'lifted': 'slice'}
        p = dict(id=self.cid(section, key), choose=choose, sourceWording=wording, routePrompt=prompt, options=options,
                 review=dict(status='deferred-sitting-review', year=self.year, level=self.level, sitting='deferred',
                             section=str(section), question=ref, sources=self.sources(section), paperPagesReviewed=[page],
                             schemePagesReviewed=schemes, boundaries={ref: total}, selectionAnalysis=selection,
                             sourceClarifications=guidance),
                 template=template)
        if ordered:
            p['orderedResponses'] = ordered
        for o in options:
            o.setdefault('topicId', topic)
        self.pools.append(p)
        return p

    # ---------------------------------------------------------------- the sitting's record
    def atlas(self, section, n, booklet_key, reason):
        """The Topic Atlas question this printed question is, with the topics of every card it holds."""
        self.questions[(section, str(n))] = dict(paperKey=booklet_key, reason=reason)

    def emit(self, totals, selection, reviewed):
        """Check the sitting's printed question totals, then replace its records in the deferred store.

        totals: {(section, question number): printed marks}; selection: the sitting's selection analysis, by
        section; reviewed: {section: [paper pages visually reviewed], 'scheme': [scheme pages]}."""
        prefix = f'bus-{self.year}-{self.lv}-deferred-'
        for (section, q), want in totals.items():
            got = sum(c['totalMarks'] for c in self.cards if c['section'] == str(section) and qnum(c['questionRef']) == q)
            got += sum(p['template']['totalMarks'] for p in self.pools
                       if p['template']['section'] == str(section) and qnum(p['template']['questionRef']) == q)
            assert got == want, (section, q, got, want)
        d = json.loads(STORE.read_text()) if STORE.exists() else dict(schemaVersion=1, cards=[], pools=[], reviews=[])
        atlas = json.loads(ATLAS.read_text()) if ATLAS.exists() else dict(v=1, questions=[])
        d['cards'] = [c for c in d['cards'] if not c['id'].startswith(prefix)] + self.cards
        d['pools'] = [p for p in d['pools'] if not p['id'].startswith(prefix)] + self.pools
        d['reviews'] = [r for r in d['reviews'] if not (r['year'] == self.year and r['level'] == self.level)]
        atlas['questions'] = [q for q in atlas['questions'] if not (q['year'] == self.year and q['level'] == self.level)]
        for (section, q) in sorted(totals, key=lambda k: (k[0], int(k[1]) if k[1].isdigit() else 0)):
            cohort = [c for c in self.cards if c['section'] == str(section) and qnum(c['questionRef']) == q]
            pooled = [p for p in self.pools if p['template']['section'] == str(section) and qnum(p['template']['questionRef']) == q]
            d['reviews'].append(dict(
                status='deferred-sitting-review', year=self.year, level=self.level, sitting='deferred', section=str(section),
                question=q, cardIds=[c['id'] for c in cohort], poolIds=[p['id'] for p in pooled], sources=self.sources(section),
                paperPagesReviewed=sorted({p for c in cohort for p in c['paperPages']} | {p for x in pooled for p in x['template']['paperPages']}),
                schemePagesReviewed=sorted({p for c in cohort for p in c['rubric']['schemePages']} | {p for x in pooled for p in x['template']['rubric']['schemePages']}),
                boundaries={c['id'][len(prefix):]: c['totalMarks'] for c in cohort} | {p['id'][len(prefix):]: p['template']['totalMarks'] for p in pooled},
                selectionAnalysis=selection[section],
                sourceClarifications=[g for c in cohort for g in c['rubric']['guidance']]))
            topics = list(dict.fromkeys(t for c in cohort for t in [c['topicId']] + c.get('additionalTopicIds', [])))
            for p in pooled:
                topics += [o['topicId'] for o in p['options'] if o['topicId'] not in topics]
            meta = self.questions[(section, q)]
            atlas['questions'].append(dict(year=self.year, level=self.level, fileid=f"{self.booklets[section]}-deferred.pdf",
                                       paperKey=meta['paperKey'], n=q, canonicalNodeIds=topics, reason=meta['reason']))
        d.setdefault('sittings', [])
        d['sittings'] = [s for s in d['sittings'] if not (s['year'] == self.year and s['level'] == self.level)]
        d['sittings'].append(dict(year=self.year, level=self.level, booklets={str(k): v for k, v in self.booklets.items()},
                                  scheme=self.scheme_fid,
                                  sources={kind: self.source(fid, kind) for fid, kind in
                                           [*[(f, 'deferredexams') for f in sorted(set(self.booklets.values()))],
                                            (self.scheme_fid, 'deferredmarkingschemes')]},
                                  paperPagesReviewed={str(k): v for k, v in reviewed.items() if k != 'scheme'},
                                  schemePagesReviewed=reviewed['scheme']))
        d['cards'].sort(key=lambda c: (c['year'], c['level'], int(c['section']), c['id']))
        d['pools'].sort(key=lambda p: p['id'])
        d['reviews'].sort(key=lambda r: (r['year'], r['level'], int(r['section']), int(r['question']) if r['question'].isdigit() else 0, r['question']))
        atlas['questions'].sort(key=lambda r: (r['year'], r['level'], r['fileid'], int(r['n']) if r['n'].isdigit() else 0, r['n']))
        d['sittings'].sort(key=lambda s: (s['year'], s['level']))
        STORE.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
        ATLAS.write_text(json.dumps(atlas, ensure_ascii=False, indent=2) + '\n')
        print(f'{self.year} {self.level} deferred: {len(self.cards)} cards, {len(self.pools)} route pools, '
              f'{len(totals)} printed questions.')


def qnum(ref):
    m = re.search(r'(?:^|\s)(?:Q(\d+)|(ABQ))', ref)
    return m.group(1) or m.group(2)
