#!/usr/bin/env python3
"""Reviewed 2026 Ordinary Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001GLP100IV scheme
(PDF 14–33, plus 34 modified marking) visually reviewed on 2026-10-11. Counts are
assertions, not corpus-completeness proof.
- Reading: every printed question is kept whole (10) and each (a)/(b) part is a
  5-mark practice card.
- Prescribed prose and poetry: each printed text is a whole 25-mark route; its
  printed sub-questions are practice cards at their own tariffs (3A(b)(i)(a)–(d)
  at 2 each). Optional prose/poetry routes stay whole (open text + title marks).
- “Freagair do rogha dhá cheann as (a), (b) nó (c)” is a choice, not a route: the
  mechanical two-route selections are built and then withdrawn (irish_choice), so each
  option carries the instruction instead. 2B(a)'s optional film or play share one grid
  and one Atlas heading, so one card carries both printed alternatives.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import re
from pathlib import Path
from irish_choice import withdraw_combinations

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP100IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2026-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2026-p2-source-review.json'
REVIEWED_AT = '2026-10-11'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|ceann amháin|pointe amháin|amháin', re.I)


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def before_language_note(text):
    return re.split(r'\[\s*Gaeilge lochtach', text)[0].strip()


def criterion(id, label, marks, guidance, kind='exact', permitted=None, deduction=False):
    return dict(id=id, label=label, kind='deduction' if deduction else 'award', maxMarks=marks,
                permittedMarks=permitted or list(range(marks + 1)), guidanceKind=kind, guidance=guidance)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


class Scheme:
    def __init__(self, doc, first, last):
        self.text = ''
        for p in range(first, last + 1):
            body = re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()).replace('', '•'))
            self.text += f' ⟦{p}⟧ ' + body

    def chunk(self, start, end=None):
        assert self.text.count(start) >= 1, start
        i = self.text.index(start)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:i])[-1])}
        for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw):
            if clean(m.group(2)) not in ('', 'nó'):
                pages.add(int(m.group(1)))
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2026/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2026/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'b0b8d3471daf6e303a387d7f7b3b9ec0114cd7702f0693a2c13d26c462724033', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '5cd471bc9b0b782f6f6e84ac41531a1716ff7e2790c94925ad321d8a82a76117', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    doc = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, source=None, **extra):
        card = dict(id=f'irish-2026-ol-p2-{slug}', year=2026, level='ordinary', paper=2, section='2',
                    atlasQuestionId=key, questionRef=f'2026 OL Paper 2 {ref}', questionText=prompt,
                    totalMarks=sum(c['maxMarks'] for c in criteria if c['kind'] == 'award'), topicId=topic,
                    **({'additionalTopicIds': extra_topics} if extra_topics else {}),
                    conceptId=f'irish-ol-p2-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
                    schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT,
                    reviewedPaperPages=pages, taskRequirements=requirements, criteria=criteria, markingGuideNote=note,
                    sourceMaterial=dict(kind='source-text', label=source[0] if source else ref, title=source[1] if source else ref,
                                        pages=source[2] if source else pages, attribution='© State Examinations Commission.',
                                        presentationNote='Shown page-for-page from the official examination paper; swipe to move between pages.'),
                    **extra)
        cards.append(card)
        return card

    # ---- Ceist 1: Léamhthuiscint (100) --------------------------------------------------
    note2 = 'Nóta: Má tá dhá phointe eolais i gceist, tá 3 mharc ar an gcéad cheann atá ceart agus 2 mharc ar an dara ceann atá ceart. Nóta: Gearrfar pionós i ngeall ar iomarcaíocht.'
    lang_read = 'Scheme: “Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh” — one deduction from each passage total (50), never inside a single part.'
    passages = {
        'A': dict(title='Pobal Ráth Chairn', pages=[4, 5], topic='irish-3-0', scheme=Scheme(doc, 15, 16), parts=[
            ('1', 'a', '(a) Cad a rinne seacht dteaghlach is fiche sa bhliain 1935? (Alt 1)', '1. (a) Cad a rinne'),
            ('1', 'b', '(b) Cad a tharla sa bhliain 1967? (Alt 1)', '(b) Cad a tharla'),
            ('2', 'a', '(a) Scríobh síos dhá chúis ar bunaíodh Comharchumann Ráth Chairn sa bhliain 1973. (Alt 2)', '2. (a) Scríobh síos dhá chúis'),
            ('2', 'b', '(b) Tabhair dhá phíosa eolais faoi na cluichí Gaelacha sa cheantar. (Alt 2)', '(b) Tabhair dhá phíosa eolais faoi na cluichí'),
            ('3', 'a', '(a) Scríobh síos an dá rud a léiríonn go bhfuil ag éirí go maith leis an gcomhlacht innealtóireachta agus athchúrsála Turmec Teoranta. (Alt 3)', '3. (a) Scríobh síos an dá rud'),
            ('3', 'b', '(b) Cén cineál oibre a dhéanann Anna Ní Dhonnchú ina stiúideo i Ráth Chairn? (Alt 3)', '(b) Cén cineál oibre'),
            ('4', 'a', '(a) Cén fáth a n‐eagraítear Féile na Mí? (Alt 4)', '4. (a) Cén fáth a n-eagraítear'),
            ('4', 'b', '(b) Cad atá Étáin agus Máire Ní Churraoin ag iarraidh a dhéanamh trí úsáid a bhaint as na meáin shóisialta? (Alt 4)', '(b) Cad atá Étáin'),
            ('5', 'a', '(a) Cén dá aidhm atá leis an bplean teanga oifigiúil do Ghaeltacht Ráth Chairn? (Alt 5)', '5. (a) Cén dá aidhm'),
            ('5', 'b', '(b) Cad atá ar fáil sna hagallaimh agus sna píosaí ceoil sa chartlann a bhronn RTÉ Raidió na Gaeltachta ar Choiste Oidhreachta Ráth Chairn? (Alt 5)', '(b) Cad atá ar fáil')]),
        'B': dict(title='The Corrs – Clann cheolmhar cháiliúil', pages=[6, 7], topic='irish-3-1', scheme=Scheme(doc, 17, 18), parts=[
            ('1', 'a', '(a) Tabhair dhá phíosa eolais faoi thuismitheoirí The Corrs. (Alt 1)', '1. (a) Tabhair dhá phíosa eolais'),
            ('1', 'b', '(b) Cén fáth a seasann The Corrs amach ó bhannaí ceoil eile? (Alt 1)', '(b) Cén fáth a seasann'),
            ('2', 'a', '(a) Scríobh síos dhá rud a rinne The Corrs sa bhliain 1991. (Alt 2)', '2. (a) Scríobh síos dhá rud'),
            ('2', 'b', '(b) Cén cuireadh ar ghlac The Corrs leis sa bhliain 1996? (Alt 2)', '(b) Cén cuireadh'),
            ('3', 'a', '(a) Scríobh síos dhá rud a rinne Sharon tar éis don ghrúpa sos a thógáil. (Alt 3)', '3. (a) Scríobh síos dhá rud a rinne Sharon'),
            ('3', 'b', '(b) Cad a rinne an ceathrar acu i mí na Bealtaine 2015? (Alt 3)', '(b) Cad a rinne an ceathrar'),
            ('4', 'a', '(a) Scríobh síos dhá phíosa eolais faoin óráid bheag a thugadh Andrea ag gach ceolchoirm ar an gcamchuairt Summer Sunshine in 2025. (Alt 4)', '4. (a) Scríobh síos dhá phíosa eolais'),
            ('4', 'b', '(b) Luaigh dhá ghaisce atá déanta ag an teaghlach ceolmhar seo ó tháinig siad le chéile mar bhanna ceoil den chéad uair. (Alt 4)', '(b) Luaigh dhá ghaisce'),
            ('5', 'a', '(a) Tabhair dhá shampla den obair charthanacha atá déanta ag The Corrs a thuill an gradam speisialta ón mBanríon Eilís a Dó in 2005. (Alt 5)', '5. (a) Tabhair dhá shampla'),
            ('5', 'b', '(b) Cad a chreideann Andrea Corr faoin gceol? (Alt 5)', '(b) Cad a chreideann')]),
    }
    reading_requirements = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
    for letter, passage in passages.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        anchors = [p[3] for p in passage['parts']]
        source = (f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        by_q = {}
        for index, (q, part, prompt, anchor) in enumerate(passage['parts']):
            assert comparable(re.sub(r'^\([ab]\) ', '', prompt)) in comparable(page_text), (letter, q, part)
            chunk, spages = passage['scheme'].chunk(anchor, anchors[index + 1] if index + 1 < len(anchors) else '[Gaeilge lochtach')
            assert '5 mharc' in chunk, (letter, q, part)
            two = '3 mharc + 2 mharc' in chunk
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            guidance = [chunk] + ([note2] if two else [])
            card = add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {q}({part})',
                       f'{q}{prompt}', passage['topic'], passage['pages'], spages, [criterion(part, 'Freagra', 5, guidance, permitted=permitted)],
                       reading_requirements, 'SEC allocation for this part' + (': first correct point 3, second 2 (0/3/5).' if two else '.') + ' ' + lang_read, None, source)
            by_q.setdefault(q, []).append((prompt, card))
        for q, parts in by_q.items():
            add(f'R-{letter}-{q}', f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}',
                f'{q}. ' + ' '.join(p for p, _ in parts) + ' (10 marc)', passage['topic'], passage['pages'],
                sorted({p for _, c in parts for p in c['schemePages']}), [dict(c['criteria'][0]) for _, c in parts],
                ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.'],
                'Retained complete printed question: (a) 5 + (b) 5. ' + lang_read, None, source)

    # ---- Ceist 2 & 3: An Litríocht ------------------------------------------------------------
    lit = Scheme(doc, 20, 33)
    sample_note = lit.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', 'Freagair do rogha dhá cheann')[0]
    deduction = lambda: criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, ['[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh] — applied once to this whole 25-mark answer.'], 'quality', deduction=True)
    lit_requirements = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
    lang_lit = 'Scheme: “Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh” applies to the whole 25-mark answer, never inside one sub-question.'
    routes = {}

    def prescribed(key, slug, ref, topic, page, intro, parts, scheme_start, scheme_end, group, source, slot_permitted=None):
        """parts: (label, prompt, marks, anchor)."""
        whole_chunk, spages = lit.chunk(scheme_start, scheme_end)
        anchors = [p[3] for p in parts]
        crits, part_cards = [], []
        for index, (label, prompt, marks, anchor) in enumerate(parts):
            assert comparable(prompt) in comparable(texts[page - 1]) or all(comparable(line) in comparable(texts[page - 1]) for line in prompt.split('\n')), (key, label)
            i0 = whole_chunk.index(anchor)
            i1 = whole_chunk.index(anchors[index + 1], i0 + len(anchor)) if index + 1 < len(anchors) else len(whole_chunk)
            chunk = before_language_note(whole_chunk[i0:i1])
            # 3A(b)(i) prints no 8 of its own: four 2-mark questions (a)–(d).
            assert f'({marks} mharc)' in chunk or f'({marks} marc)' in chunk or chunk.count('(2 mharc)') * 2 == marks == 8, (key, label, chunk[:80])
            cid = 'eolas-' + re.sub(r'[()]', '', label).replace(' ', '')
            # “3 mharc + 2 mharc”: first correct point 3, second 2 (order-dependent).
            permitted = [0, 3, 5] if '3 mharc + 2 mharc' in chunk else (slot_permitted or {}).get(label)
            crits.append(criterion(cid, f'({label}) Eolas', marks, [chunk, sample_note], 'indicative', permitted=permitted))
            part_key = f'{key}-{re.sub(r"[()]", "", label)}'
            part_cards.append((part_key, label, prompt, marks, chunk, permitted))
        whole = add(key, slug, ref, intro + '\n' + '\n'.join(f'({l}) {p}' for l, p, _, _ in parts) + '\n(25 marc)', topic, [page], spages,
                    crits + [deduction()], lit_requirements,
                    'One complete SEC response: the printed sub-questions keep their own tariffs and the 0–4 Gaeilge deduction applies once. Sample answers are indicative, not exhaustive.',
                    None, source)
        for part_key, label, prompt, marks, chunk, permitted in part_cards:
            add(part_key, f'{slug}-{re.sub(r"[()]", "", label)}', f'{ref} · ({label})', intro + f'\n({label}) {prompt}', topic, [page], spages,
                [criterion('eolas', 'Eolas', marks, [chunk, sample_note], 'indicative', permitted=permitted)], lit_requirements,
                f'One printed sub-question at its published {marks}-mark tariff. ' + lang_lit, None, source)
        routes.setdefault(group, []).append(whole)
        return whole

    # 2A Prós Ainmnithe
    head2a = 'Freagair 2A (Prós Ainmnithe) nó 2B (Prós Roghnach).\n2A Prós Ainmnithe — Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.'
    cm = [('i', 'Tabhair dhá chúis a bhfuil imní ar mháthair Catherine sa charr.', 5, '(i) Tabhair dhá chúis'),
          ('ii', 'Scríobh síos dhá rud a deir Paul le Catherine faoi bheith ar an raidió.', 5, '(ii) Scríobh síos dhá rud'),
          ('iii', 'Luaigh dhá bhréag a insíonn Catherine do Paul.', 5, '(iii) Luaigh dhá bhréag'),
          ('iv', 'Cén rud uafásach a dhéanann Catherine ag deireadh an scannáin?', 5, '(iv) Cén rud uafásach'),
          ('v', 'An maith leat Catherine sa scannán seo? Tabhair dhá fháth le do fhreagra.', 5, '(v) An maith leat Catherine')]
    prescribed('P-2A-a-caca-milis', 'prose-2a-a-caca-milis', 'Prós 2A(a) · Cáca Milis', 'irish-4-6', 8,
               head2a + '\n(a) Freagair na ceisteanna thíos faoin scannán Cáca Milis nó faoin dráma An Lasair Choille.\nCáca Milis', cm,
               'Cáca Milis (25 marc)', 'nó An Lasair Choille (25 marc)', '2A', ('Prós Ainmnithe', 'Cáca Milis', [8]))
    lc = [('i', 'Cén fáth nach bhfuil Micil, an seanfhear, ábalta codladh ag tús an dráma?', 5, '(i) Cén fáth nach bhfuil Micil'),
          ('ii', 'Cad a cheapann Micil den chomhrá a bhí ag Séamas leis an mBúrcach faoi dhul go Sasana?', 5, '(ii) Cad a cheapann Micil'),
          ('iii', 'Tabhair dhá chúis a bhfágann Míoda a hathair.', 5, '(iii) Tabhair dhá chúis a bhfágann'),
          ('iv', 'Céard a dhéanann Binncheol, an lasair choille, nuair a ligtear saor é?', 5, '(iv) Céard a dhéanann Binncheol'),
          ('v', 'An maith leat Míoda sa dráma seo? Tabhair dhá fháth le do fhreagra.', 5, '(v) An maith leat Míoda')]
    prescribed('P-2A-a-an-lasair-choille', 'prose-2a-a-an-lasair-choille', 'Prós 2A(a) · An Lasair Choille', 'irish-4-8', 8,
               head2a + '\n(a) Freagair na ceisteanna thíos faoin scannán Cáca Milis nó faoin dráma An Lasair Choille.\nAn Lasair Choille', lc,
               'An Lasair Choille (25 marc)', '(b) Freagair an cheist thíos faoin ngearrscéal Dís.', '2A', ('Prós Ainmnithe', 'An Lasair Choille', [8]))
    dis_chunk, dis_pages = lit.chunk('(b) Freagair an cheist thíos faoin ngearrscéal Dís.', '(c) Freagair na ceisteanna thíos faoin ngiota')
    dis_prompt = ('Freagair an cheist thíos faoin ngearrscéal Dís.\nDís\n‘Cheapas gur anuas ós na Flaithis a tháinig sí chugam. Ó, an sásamh a fuaireas scaoileadh liom féin…’\n'
                  'Tabhair cuntas ar an gcomhrá a bhí idir Seán agus a bhean chéile i ndiaidh chuairt bhean an tsuirbhé. (25 marc)')
    assert all(comparable(l) in comparable(texts[7]) for l in dis_prompt.replace(' (25 marc)', '').split('\n'))
    routes.setdefault('2A', []).append(add('P-2A-b', 'prose-2a-b', 'Prós 2A(b) · Dís', head2a + '\n(b) ' + dis_prompt, 'irish-4-4', [8], dis_pages,
        [criterion('eolas', 'Eolas', 25, [before_language_note(dis_chunk), sample_note], 'indicative'), deduction()], lit_requirements,
        'One complete SEC response: five points at 5 (2 for the bare point + 3 for development), 0–4 Gaeilge deduction once.', None, ('Prós Ainmnithe', 'Dís', [8])))
    hu = [('i', 'Scríobh síos dhá cheann de na hullmhúcháin atá déanta ag Lisín don chóisir.', 5, '(i) Scríobh síos dhá cheann'),
          ('ii', 'Tabhair dhá phointe eolais faoi Phól, fear céile Lisín.', 5, '(ii) Tabhair dhá phointe eolais faoi Phól'),
          ('iii', 'Luaigh dhá rud faoi Ruán, mac Lisín agus Phóil.', 5, '(iii) Luaigh dhá rud faoi Ruán'),
          ('iv', '‘Bhí Lisín gnóthach, ina ball de mhórán eagraíochtaí agus clubanna.’ Scríobh síos dhá phointe eolais faoin gcuid sin de shaol Lisín.', 5, '(iv) ‘Bhí Lisín gnóthach'),
          ('v', 'An maith leat Lisín sa ghiota seo? Tabhair dhá fháth le do fhreagra.', 5, '(v) An maith leat Lisín')]
    prescribed('P-2A-c', 'prose-2a-c', 'Prós 2A(c) · Hurlamaboc', 'irish-4-5', 8,
               head2a + '\n(c) Freagair na ceisteanna thíos faoin ngiota as an úrscéal Hurlamaboc.\nHurlamaboc', hu,
               '(c) Freagair na ceisteanna thíos faoin ngiota', '2B PRÓS ROGHNACH', '2A', ('Prós Ainmnithe', 'Hurlamaboc', [8]))

    # 2B Prós Roghnach — open texts, whole routes only
    head2b = ('Freagair 2A (Prós Ainmnithe) nó 2B (Prós Roghnach).\n2B Prós Roghnach — Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach. '
              'Freagair do rogha dhá cheann as (a), (b) nó (c) thíos.')
    optional_prose = [
        ('P-2B-b', 'prose-2b-b', 'Prós 2B(b) · Gearrscéal roghnach',
         '(b) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an ghearrscéil sin, dar leat. Tabhair cuntas ar na heachtraí is mó a léiríonn an príomhthéama sin sa ghearrscéal. (23 marc)\nNí mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)',
         '(b) Maidir le gearrscéal roghnach', '(c) Maidir le giota as úrscéal roghnach'),
        ('P-2B-c', 'prose-2b-c', 'Prós 2B(c) · Giota as úrscéal roghnach',
         '(c) Maidir le giota as úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phríomhphearsa (an príomhcharachtar) sa ghiota sin. Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin ó thús go deireadh an ghiota. (23 marc)\nNí mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)',
         '(c) Maidir le giota as úrscéal roghnach', 'CEIST 3'),
    ]
    # The optional film and the optional play share one grid and one Atlas heading (irish-4-7), so one card
    # carries both printed alternatives (choose-one refinement, 2026-10-12).
    film_play = ('(a) Freagair an cheist thíos faoin scannán roghnach nó faoin dráma roghnach.\n'
                 'Maidir le scannán roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa scannán sin. (23 marc)\n'
                 'Ní mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)\nnó\n'
                 'Maidir le dráma roghnach a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (príomhrudaí) a tharlaíonn sa dráma sin. (23 marc)\n'
                 'Ní mór teideal an dráma sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (2 mharc)')
    for line in film_play.split('\n'):
        assert comparable(re.sub(r'^\([abc]\) | \((23|2) m?h?arc\)$', '', line)) in comparable(texts[8]), line[:40]
    halves = []
    for start, end in [('Maidir le scannán roghnach', 'nó Maidir le dráma roghnach'), ('Maidir le dráma roghnach', '(b) Maidir le gearrscéal roghnach')]:
        chunk, spages = lit.chunk(start, end)
        chunk = before_language_note(chunk)
        t = chunk.index('Teideal an')
        assert chunk[t:].endswith('= 1 mharc (2 mharc)'), (start, chunk[t:])
        halves.append((chunk[:t].strip(), chunk[t:], spages))
    routes.setdefault('2B', []).append(add('P-2B-a', 'prose-2b-a', 'Prós 2B(a) · Scannán nó dráma roghnach', head2b + '\n' + film_play, 'irish-4-7', [9],
        sorted({p for h in halves for p in h[2]}),
        [criterion('eolas', 'Eolas', 23, [h[0] for h in halves], 'indicative'), criterion('teideal', 'Teideal + ainm an scríbhneora', 2, [h[1] for h in halves], 'exact'), deduction()],
        lit_requirements, 'One complete SEC response about an optional film or an optional play (the same scheme for both): 23 for five points (scheme weights 5/4) and 2 for the exact title and writer, then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate.',
        None, ('Prós Roghnach', '2B(a) · Scannán nó dráma roghnach', [9])))
    for key, slug, ref, prompt, start, end in optional_prose:
        for line in prompt.split('\n'):
            assert comparable(re.sub(r'^\([abc]\) | \((23|2) m?h?arc\)$', '', line)) in comparable(texts[8]), (key, line[:40])
        chunk, spages = lit.chunk(start, end)
        chunk = before_language_note(chunk)
        t = chunk.index('Teideal an')
        assert chunk[t:].endswith('= 1 mharc (2 mharc)'), (key, chunk[t:])
        routes.setdefault('2B', []).append(add(key, slug, ref, head2b + '\n' + prompt, 'irish-4-7', [9], spages,
            [criterion('eolas', 'Eolas', 23, [chunk[:t].strip()], 'indicative'), criterion('teideal', 'Teideal + ainm an scríbhneora/údair', 2, [chunk[t:]], 'exact'), deduction()],
            lit_requirements, 'One complete SEC response: 23 for five points (scheme weights 5/4) and 2 for the exact title and writer, then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate.',
            None, ('Prós Roghnach', ref.removeprefix('Prós '), [9])))

    # 3A Filíocht Ainmnithe
    head3a = 'Freagair 3A (Filíocht Ainmnithe) nó 3B (Filíocht Roghnach).\n3A Filíocht Ainmnithe — Freagair do rogha dhá cheann as (a), (b) nó (c).'
    ge = [('i', 'Scríobh síos dhá phointe eolais, i d’fhocail féin, faoi shaol an ainmhí i línte 1‐8 den dán.', 8, '(i) Scríobh síos dhá phointe eolais'),
          ('ii', 'Tabhair dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) den ainmhí a fhaighimid i línte 9‐12 den dán.', 8, '(ii) Tabhair dhá phointe eolais'),
          ('iii', 'An bhfuil an t‐ainmhí sásta i línte 13‐17 den dán, dar leat? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra.', 9, '(iii) An bhfuil an t-ainmhí sásta')]
    prescribed('F-3A-a', 'poetry-3a-a', 'Filíocht 3A(a) · Géibheann', 'irish-5-2', 10, head3a + '\n(a) Géibheann', ge,
               '(a) Géibheann (25 marc)', '(b) An tEarrach Thiar (25 marc)', '3A', ('Filíocht Ainmnithe', 'Géibheann', [10]))
    et = [('i', 'Cén séasúr atá i gceist sa dán seo? (b) Cén obair atá ar siúl ag an bhfear i véarsa a haon? (c) Cá bhfuil na mná i véarsa a trí? (d) Cén dath atá ar an bhfarraige i véarsa a ceathair?', 8, '(i) (a) Cén séasúr'),
          ('ii', 'Scríobh síos dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) den fhear a thugann an file dúinn i véarsa a dó den dán.', 8, '(ii) Scríobh síos dhá phointe eolais'),
          ('iii', 'An maith leat an dán seo? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra.', 9, '(iii) An maith leat an dán seo?')]
    whole_et = prescribed('F-3A-b', 'poetry-3a-b', 'Filíocht 3A(b) · An tEarrach Thiar', 'irish-5-3', 11, head3a + '\n(b) An tEarrach Thiar', et,
                          '(b) An tEarrach Thiar (25 marc)', '(c) An Spailpín Fánach (25 marc)', '3A', ('Filíocht Ainmnithe', 'An tEarrach Thiar', [11]),
                          slot_permitted={'i': [0, 2, 4, 6, 8]})
    # 3A(b)(i) prints four 2-mark questions (a)–(d): each is also a practice slot.
    et_chunk, et_pages = lit.chunk('(i) (a) Cén séasúr', '(ii) Scríobh síos dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) den fhear')
    for sub, question, nxt in [('a', 'Cén séasúr atá i gceist sa dán seo?', '(b) Cén obair'), ('b', 'Cén obair atá ar siúl ag an bhfear i véarsa a haon?', '(c) Cá bhfuil na mná'),
                               ('c', 'Cá bhfuil na mná i véarsa a trí?', '(d) Cén dath'), ('d', 'Cén dath atá ar an bhfarraige i véarsa a ceathair?', None)]:
        start = et_chunk.index(question)
        piece = et_chunk[start:et_chunk.index(nxt, start) if nxt else len(et_chunk)]
        assert '(2 mharc)' in piece and 'Freagra:' in piece, (sub, piece[:60])
        add(f'F-3A-b-i-{sub}', f'poetry-3a-b-i-{sub}', f'Filíocht 3A(b) · An tEarrach Thiar · (i)({sub})', head3a + f'\n(b) An tEarrach Thiar\n(i) ({sub}) {question}', 'irish-5-3', [11], et_pages,
            [criterion('eolas', 'Freagra', 2, [piece], 'exact', permitted=[0, 2])], lit_requirements,
            'One printed 2-mark question inside 3A(b)(i). ' + lang_lit, None, ('Filíocht Ainmnithe', 'An tEarrach Thiar', [11]))
    sp = [('i', 'Scríobh síos dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) den spailpín fánach a thugtar dúinn i véarsa a haon den dán.', 8, '(i) Scríobh síos dhá phointe eolais'),
          ('ii', 'Tabhair dhá phointe eolais, i d’fhocail féin, faoi mhargadh na saoire i véarsa a trí.', 8, '(ii) Tabhair dhá phointe eolais'),
          ('iii', 'An bhfuil trua agat don spailpín fánach sa dán seo? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra.', 9, '(iii) An bhfuil trua agat')]
    prescribed('F-3A-c', 'poetry-3a-c', 'Filíocht 3A(c) · An Spailpín Fánach', 'irish-5-1', 12, head3a + '\n(c) An Spailpín Fánach', sp,
               '(c) An Spailpín Fánach (25 marc)', '3B FILÍOCHT ROGHNACH', '3A', ('Filíocht Ainmnithe', 'An Spailpín Fánach', [12]))

    # 3B Filíocht Roghnach — open poems, whole routes
    head3b = ('Freagair 3A (Filíocht Ainmnithe) nó 3B (Filíocht Roghnach).\n3B Filíocht Roghnach — Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach. '
              'Freagair do rogha dhá cheann as (a), (b) nó (c) thíos. Níl cead an dán roghnach céanna a úsáid faoi dhó sna freagraí ar (a), (b) nó (c) thíos.')
    title_line = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'
    poem_prompts = {
        'a': ['(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin sin, dar leat. Tabhair dhá phointe eolais, i d’fhocail féin, faoin bpríomhthéama sin sa dán. (9 marc)',
              '(ii) Scríobh síos an mothúchán is láidre atá sa dán, dar leat. Tabhair dhá shampla, i d’fhocail féin, den mhothúchán sin sa dán. (7 marc)',
              '(iii) Cén íomhá (pictiúr) is mó a thaitníonn leat sa dán? Tabhair dhá phointe eolais, i d’fhocail féin, faoin íomhá (faoin bpictiúr) sin. (7 marc)'],
        'b': ['(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos, i d’fhocail féin, príomhsmaointe an dáin sin. (9 marc)',
              '(ii) Roghnaigh íomhá (pictiúr) amháin a úsáideann an file sa dán seo. Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
              '(iii) An maith leat an dán seo? Tabhair dhá fháth, i d’fhocail féin, le do fhreagra. (7 marc)'],
        'c': ['(i) Maidir le dán seanaimseartha roghnach (dán a cumadh sa tréimhse roimh 1850) a ndearna tú staidéar air le linn do chúrsa, scríobh síos, i d’fhocail féin, príomhsmaointe an dáin sin. (9 marc)',
              '(ii) Cén íomhá (pictiúr) is mó a thaitníonn leat sa dán? Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
              '(iii) Cén t‐atmaisféar atá sa dán seo, dar leat? Tabhair dhá shampla den atmaisféar sin sa dán. (7 marc)'],
    }
    p13 = comparable(texts[12])
    for lines in poem_prompts.values():
        for line in lines + [title_line]:
            assert comparable(line) in p13, line[:50]
    assert p13.count(comparable(title_line)) == 3
    optional_poems = [('a', '(a) (i) Maidir le dán nua-aimseartha', '(b) (i) Maidir le dán nua-aimseartha', [9, 7, 7]),
                      ('b', '(b) (i) Maidir le dán nua-aimseartha', '(c) (i) Maidir le dán seanaimseartha', [9, 7, 7]),
                      ('c', '(c) (i) Maidir le dán seanaimseartha', None, [9, 7, 7])]
    for letter, start, end, caps in optional_poems:
        chunk, spages = lit.chunk(start, end)
        chunk = before_language_note(chunk)
        i2, i3 = chunk.index('(ii)'), chunk.index('(iii)')
        t = chunk.index('Ní mór teideal an dáin')
        pieces = [chunk[:i2], chunk[i2:i3], chunk[i3:t], chunk[t:]]
        for piece, cap in zip(pieces[:3], caps):
            assert f'({cap} marc)' in piece, (letter, cap)
        prompt_text = f'({letter}) ' + '\n'.join(poem_prompts[letter] + [title_line])
        routes.setdefault('3B', []).append(add(f'F-3B-{letter}', f'poetry-3b-{letter}', f'Filíocht 3B({letter}) · Dán roghnach', head3b + '\n' + prompt_text, 'irish-5-6', [13], spages,
            [criterion('eolas-i', '(i) Eolas', 9, [pieces[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [pieces[1]], 'indicative'),
             criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), criterion('teideal', 'Teideal + ainm an fhile', 2, [pieces[3]], 'exact'), deduction()],
            lit_requirements, 'One complete SEC response: (i) 9, (ii) 7, (iii) 7, title and poet 2, then the 0–4 Gaeilge deduction once. The optional poem is open content; the same poem may not be used twice.',
            None, ('Filíocht Roghnach', f'3B({letter}) · Dán roghnach', [13])))

    # Mechanical two-route selections inside each chosen question.
    def combine(group, members):
        criteria = []
        for m in members:
            prefix = m['atlasQuestionId'].split('-', 1)[1].lower() + '-'
            for old in m['criteria']:
                cc = copy.deepcopy(old)
                cc['id'] = prefix + cc['id']
                cc['label'] = m['questionRef'].removeprefix('2026 OL Paper 2 ') + ' · ' + cc['label']
                criteria.append(cc)
        key = members[0]['atlasQuestionId'] + '+' + members[1]['atlasQuestionId'].split('-', 2)[2]
        ref = ' + '.join(m['questionRef'].removeprefix('2026 OL Paper 2 ') for m in members)
        topics = list(dict.fromkeys(t for m in members for t in [m['topicId'], *m.get('additionalTopicIds', [])]))
        # Slug = first route's slug + '--' + the second route's letter (e.g. prose-2a-a-caca-milis--b).
        slug = members[0]['id'].removeprefix('irish-2026-ol-p2-') + '--' + members[1]['atlasQuestionId'].split('-', 2)[2].lower()
        return add(key.replace('+', '--'), slug, ref,
                   f'Freagair do rogha dhá cheann as (a), (b) nó (c).\n\nAn rogha don chárta seo: {ref}' + ('\nNíl cead an dán roghnach céanna a úsáid faoi dhó.' if group == '3B' else '') +
                   '\n\n' + '\n\n'.join(m['questionRef'].removeprefix('2026 OL Paper 2 ') + '\n' + m['questionText'].split('\n', 2)[2] for m in members),
                   topics[0], sorted({p for m in members for p in m['reviewedPaperPages']}), sorted({p for m in members for p in m['schemePages']}),
                   criteria, [r for m in members for r in m['taskRequirements']],
                   'One permitted printed selection: two whole 25-mark answers. Each keeps its own awards and 0–4 Gaeilge deduction; alternative routes are not added together.',
                   topics[1:], (GROUP_LABELS[group], ' + '.join(re.sub(r'^(Prós|Filíocht) ', '', m['questionRef'].removeprefix('2026 OL Paper 2 ')) for m in members),
                                 sorted({p for m in members for p in m['sourceMaterial']['pages']})),
                   memberCardIds=[m['id'] for m in members])

    GROUP_LABELS = {'2A': 'Prós Ainmnithe', '2B': 'Prós Roghnach', '3A': 'Filíocht Ainmnithe', '3B': 'Filíocht Roghnach'}
    letter_of = lambda c: c['atlasQuestionId'].split('-')[2][0]
    for group in ['2A', '2B', '3A', '3B']:
        for m1, m2 in itertools.combinations(routes[group], 2):
            if letter_of(m1) != letter_of(m2):
                combine(group, [m1, m2])

    decisions = selection_decisions(paper)
    pairs = [c for c in cards if 'memberCardIds' in c]
    assert len(pairs) == 14 and {c['totalMarks'] for c in pairs} == {50}, (len(pairs))
    assert len(cards) == len({c['id'] for c in cards}) == len({c['atlasQuestionId'] for c in cards})
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        for cr in card['criteria']:
            assert cr['guidance'] and all(not re.search('[-]', g) for g in cr['guidance']), (card['id'], cr['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2026, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=decisions,
                  readingCardIds=[c['id'] for c in cards if '-reading-' in c['id']],
                  literatureCardIds=[c['id'] for c in cards if '-reading-' not in c['id'] and 'memberCardIds' not in c],
                  pairedRouteCardIds=[c['id'] for c in pairs],
                  examStructure=dict(readingA=50, readingB=50, prose=50, poetry=50, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries=f'{len([c for c in cards if "-reading-" in c["id"]])} reading cards; {len([c for c in cards if "-reading-" not in c["id"] and "memberCardIds" not in c])} literature routes and sub-questions; {len(pairs)} two-route selections.')
    return withdraw_combinations(dict(review=review, cards=cards))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Ordinary 2026 Paper 2: {len(data['cards'])} reviewed task/route cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
