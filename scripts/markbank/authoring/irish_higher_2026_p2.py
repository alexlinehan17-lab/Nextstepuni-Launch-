#!/usr/bin/env python3
"""Reviewed 2026 Higher Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001ALP100IV scheme
(PDF 17–48, plus 49 modified marking) visually reviewed on 2026-10-11. Counts are
assertions, not corpus-completeness proof. The card shapes follow the reviewed
2024 Higher Paper 2: every printed reading question is kept whole and each
published part is also a practice card; two independent one-mark answers and
two independent six-mark points expose their own slots; order-dependent 2 + 1
items stay whole. Each prescribed text, optional form and Q4 option is a route.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP200IV'
SCHEME_FILE = 'LC001ALP100IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2026-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2026-p2-source-review.json'
REVIEWED_AT = '2026-10-11'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|ceann amháin|pointe amháin|\bdhá\b|\ban dá\b', re.I)


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def in_order(prompt, text):
    return re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split() if comparable(w)), comparable(text))


def criterion(id, label, marks, guidance, kind='exact', permitted=None):
    return dict(id=id, label=label, kind='award', maxMarks=marks,
                permittedMarks=permitted or list(range(marks + 1)), guidanceKind=kind, guidance=guidance)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


class Scheme:
    """Scheme pages joined with page markers so every chunk knows the PDF pages it spans."""

    def __init__(self, doc, first, last):
        self.text = ''
        for p in range(first, last + 1):
            body = clean(doc[p - 1].get_text())
            body = re.sub(r'^\d+\s', '', body)  # printed page number
            self.text += f' ⟦{p}⟧ ' + body

    def chunk(self, start, end=None):
        assert self.text.count(start) == 1, (start, self.text.count(start))
        i = self.text.index(start)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        before = re.findall(r'⟦(\d+)⟧', self.text[:i])
        pages = {int(before[-1])}
        # A page counts only when the chunk carries real content on it (not just a trailing “nó”).
        for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw):
            if clean(m.group(2)) not in ('', 'nó'):
                pages.add(int(m.group(1)))
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2026/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2026/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'ff6eb26cf2cfc63093ef0e1863a83848a20cbe4c36542bc5d0bd4793bdf1294e', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == 'd7e9de038bf91ee9cf9735854e1d9272100982744ef7c1ebcc0f17ca025e2239', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    doc = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, source=None, **extra):
        card = dict(id=f'irish-2026-hl-p2-{slug}', year=2026, level='higher', paper=2, section='2',
                    atlasQuestionId=key, questionRef=f'2026 HL Paper 2 {ref}', questionText=prompt,
                    totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic,
                    **({'additionalTopicIds': extra_topics} if extra_topics else {}),
                    conceptId=f'irish-hl-p2-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
                    schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT,
                    reviewedPaperPages=pages, taskRequirements=requirements, criteria=criteria, markingGuideNote=note,
                    sourceMaterial=dict(kind='source-text', label=source[0] if source else ref, title=source[1] if source else ref,
                                        pages=source[2] if source else pages, attribution='© State Examinations Commission.',
                                        presentationNote='Shown page-for-page from the official examination paper; swipe to move between pages.'),
                    **extra)
        cards.append(card)
        return card

    # ---- Ceist 1: Léamhthuiscint A agus B (100) ---------------------------------------
    general = Scheme(doc, 17, 17).chunk('Tá Ceist 1 – 5 ar cómharc', 'Siombailí Anótála')[0]
    passages = {
        'A': dict(title='An tSiúr Stan – a saol agus a hoidhreacht', pages=[4, 5], topic='irish-3-0', scheme=Scheme(doc, 18, 20), parts=[
            ('1', 'a', '(a) Conas a chaith an tSiúr Stan a saol ar fad? (Alt 1)', '1. (a) Conas a chaith', 3, None),
            ('1', 'bi', '(b) (i) Cén fáth ar bhunaigh an tSiúr Stan Focus Point in 1985? (Alt 1)', '(b) (i) Cén fáth ar bhunaigh', 2, None),
            ('1', 'bii', '(ii) Cad a dúirt Príomhfheidhmeannach Focus Ireland, Pat Dennigan, faoin tSiúr Stan? (Alt 1)', '(ii) Cad a dúirt Príomhfheidhmeannach', 2, None),
            ('2', 'a', '(a) Conas a mhothaigh Treasa sa timpeallacht inar tógadh í? (Alt 2)', '2. (a) Conas a mhothaigh', 3, None),
            ('2', 'bi', '(b) (i) Cén fáth a ndeachaigh Treasa isteach i Siúracha na Carthanachta nuair a roghnaigh sí a bheith ina bean rialta? (Alt 2)', '(b) (i) Cén fáth a ndeachaigh Treasa', 2, None),
            ('2', 'bii', '(ii) Cén fáth arbh oscailt súl don tSiúr Stan an obair a rinne sí le himircigh Éireannacha i Londain? (Alt 2)', '(ii) Cén fáth arbh oscailt súl', 2, None),
            ('3', 'a', '(a) Cén rud ar chreid an bheirt, an tEaspag Birch agus an tSiúr Stan, ann? (Alt 3)', '3. (a) Cén rud ar chreid', 3, None),
            ('3', 'bi', '(b) (i) Cén fáth a ndeirtear go raibh Seirbhísí Sóisialta Chill Chainnigh ceannródaíoch? (Alt 3)', '(b) (i) Cén fáth a ndeirtear', 2, None),
            ('3', 'bii', '(ii) Conas a chuidigh an bunús acadúil le hobair na Siúrach Stan? (Alt 3)', '(ii) Conas a chuidigh an bunús', 2, None),
            ('4', 'a', '(a) Cén fáth ar éist an tSiúr Stan agus na taighdeoirí le scéalta pearsanta na mban gan dídean i mBaile Átha Cliath? (Alt 4)', '4. (a) Cén fáth ar éist', 3, None),
            ('4', 'bi', '(b) (i) Cén fhís a bhí ag an tSiúr Stan don eagraíocht Focus Point? (Alt 4)', '(b) (i) Cén fhís', 2, None),
            ('4', 'bii', '(ii) Cad a dhéanadh an tSiúr Stan chun fadhb an mhaoinithe a shárú? (Alt 4)', '(ii) Cad a dhéanadh an tSiúr Stan', 2, None),
            ('5', 'a', '(a) Conas a chabhraigh an Chomhairle um Inimircigh in Éirinn leis na hinimircigh a bhí ag teacht chuig Éirinn? (Alt 5)', '5. (a) Conas a chabhraigh', 3, None),
            ('5', 'bi', '(b) (i) Cén aidhm atá leis an tionscnamh na Nuálaithe Sóisialta Óga? (Alt 5)', '(b) (i) Cén aidhm atá leis', 2, None),
            ('5', 'bii', '(ii) Cén fáth ar cheap Uachtarán na hÉireann ag an am, Máire Mhic Ghiolla Íosa, an tSiúr Stan ina ball den Chomhairle Stáit? (Alt 5)', '(ii) Cén fáth ar cheap Uachtarán', 2, None),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Chaite in Alt 2 agus sampla de bhreischéim na haidiachta in Alt 5.', '6. (a) Aimsigh sampla', 3, 'grammar'),
            ('6', 'b', '(b) ‘Chaith an tSiúr Stan a saol ar fad ag cabhrú le grúpaí éagsúla.’ Tabhair dhá phointe eolais, i d’fhocail féin, as an sliocht a léiríonn fírinne an ráitis sin, dar leat. (Is leor 60 focal.)', '(b) ‘Chaith an tSiúr Stan', 12, 'points')]),
        'B': dict(title='An mearfhaisean ag dul as faisean', pages=[6, 7], topic='irish-3-1', scheme=Scheme(doc, 21, 24), parts=[
            ('1', 'a', '(a) Cad is brí leis an téarma ‘mearfhaisean’? (Alt 1)', '1. (a) Cad is brí', 3, None),
            ('1', 'bi', '(b) (i) Scríobh síos rud amháin a dhéanann na comhlachtaí mearfhaisin chun cabhrú leo cinneadh a dhéanamh faoi na cineálacha éadaí ba chóir a chur ar fáil. (Alt 1)', '(b) (i) Scríobh síos rud amháin', 2, None),
            ('1', 'bii', '(ii) Luaigh dhá bhealach a bhfuil déantús na méideanna móra éadaí ag déanamh dochar don chomhshaol. (Alt 1)', '(ii) Luaigh dhá bhealach', 2, 'slots'),
            ('2', 'a', '(a) Cad a chiallaíonn ‘faisean ciorclach’? (Alt 2)', '2. (a) Cad a chiallaíonn', 3, None),
            ('2', 'bi', '(b) (i) Luaigh dhá dheis a bhaineann leis an bhfaisean ciorclach. (Alt 2)', '(b) (i) Luaigh dhá dheis', 2, 'slots'),
            ('2', 'bii', '(ii) Scríobh síos dhá rud faoi na héadaí a chuirfear ar mhargadh an Aontais Eorpaigh faoin mbliain 2030 de réir na Straitéise um Theicstílí Inbhuanaithe agus Ciorclacha. (Alt 2)', '(ii) Scríobh síos dhá rud faoi na héadaí', 2, 'slots'),
            ('3', 'a', '(a) Cad a iarrtar ar dhaoine a dhéanamh de réir an fheachtais ‘Iompaigh an Treocht Droim ar Ais’? (Alt 3)', '3. (a) Cad a iarrtar', 3, None),
            ('3', 'bi', '(b) (i) Cén fáth a n‐eagraítear ceardlanna, seimineáir agus malartuithe éadaí faoi stiúir scoláirí mar chuid den fheachtas oideachasúil Let’s Fix Fashion? (Alt 3)', '(b) (i) Cén fáth a n-eagraítear', 2, None),
            ('3', 'bii', '(ii) Cad a mhúintear ar na cúrsaí oiliúna sa rannóg Rediscover Fashion san Ionad Náisiúnta don Gheilleagar Ciorclach i mBaile Munna? (Alt 3)', '(ii) Cad a mhúintear', 2, None),
            ('4', 'a', '(a) Scríobh síos dhá rud atá á ndéanamh ag go leor comhlachtaí éadaí Éireannacha a léiríonn go bhfuil siad ag iompú ar an bhfaisean inbhuanaithe. (Alt 4)', '4. (a) Scríobh síos dhá rud', 3, 'ordered'),
            ('4', 'bi', '(b) (i) Cén fáth a bhfuil an comhlacht Human Collective deimhnithe mar chomhlacht Fair Wear? (Alt 4)', '(b) (i) Cén fáth a bhfuil an comhlacht', 2, None),
            ('4', 'bii', '(ii) Scríobh síos dhá chúis a bhfuil cáil bainte amach ag an dearthóir Aoife McNamara mar cheannaire i dtionscal an fhaisin inbhuanaithe. (Alt 4)', '(ii) Scríobh síos dhá chúis', 2, 'slots'),
            ('5', 'a', '(a) Scríobh síos dhá bhealach a bhfuil a gcúl tugtha ag cuid mhór daoine in Éirinn leis an mearfhaisean. (Alt 5)', '5. (a) Scríobh síos dhá bhealach', 3, 'ordered'),
            ('5', 'bi', '(b) (i) Cén deis a thugann an comórtas Junk Kouture do dhaoine óga? (Alt 5)', '(b) (i) Cén deis a thugann', 2, None),
            ('5', 'bii', '(ii) Cad a dhéantar sa tionscnamh CycleUp? (Alt 5)', '(ii) Cad a dhéantar sa tionscnamh', 2, None),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Láithreach in Alt 1 agus sampla de bhriathar sa Mhodh Coinníollach in Alt 2.', '6. (a) Aimsigh sampla', 3, 'grammar'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, an bhfuil tú dóchasach go bhfuil deireadh ag teacht leis an mearfhaisean sa tír seo? Tabhair dhá fháth, i d’fhocail féin, as an sliocht, mar thacaíocht le do fhreagra. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas', 12, 'opinion')]),
    }
    reading_requirements = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                            'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
    part_note = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
                 'Retained whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
    for letter, passage in passages.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        anchors = [p[3] for p in passage['parts']]
        topic = passage['topic']
        source = (f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        by_question = {}
        for index, (q, part, prompt, anchor, marks, mode) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            chunk, spages = passage['scheme'].chunk(anchor, anchors[index + 1] if index + 1 < len(anchors) else None)
            tariff = f'{{{marks} mharc' if marks < 12 else '{12 mharc}'
            assert tariff in chunk, (letter, q, part, chunk[:90])
            label = f'{q}({part[0]})' + (f'({part[1:]})' if len(part) > 1 else '')
            text = f'{label} ' + re.sub(r'^(\([a-z]+\)\s*)+', '', prompt)
            permitted = [0, 2, 3] if mode in ('grammar', 'ordered') else None
            if mode == 'points':
                crits = [criterion('point-1', 'Pointe eolais 1', 6, [chunk, general]), criterion('point-2', 'Pointe eolais 2', 6, [chunk, general])]
            elif mode == 'opinion':
                crits = [criterion('opinion', 'Tuairim (T)', 2, [chunk, general]), criterion('reason-1', 'Fáth 1 (F1)', 5, [chunk]),
                         criterion('reason-2', 'Fáth 2 (F2)', 5, [chunk])]
            else:
                crits = [criterion(part if mode != 'grammar' else 'grammar', 'Freagra', marks,
                                   [chunk, general] + (['Order-dependent award: the first correct item earns 2 and the other 1 (0, 2 or 3).'] if permitted else []),
                                   permitted=permitted)]
            topic_here = 'irish-3-3' if mode == 'grammar' else topic
            card = add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {label}',
                       text, topic_here, passage['pages'], spages, crits, reading_requirements, part_note,
                       [topic] if mode == 'grammar' else None, source)
            by_question.setdefault(q, []).append((part, prompt, card))
            if mode == 'slots':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Freagra {slot}',
                        f'{text} Don chárta seo: tabhair freagra amháin don chuid seo (freagra {slot}, 1 mharc).', topic, passage['pages'], spages,
                        [criterion(f'{part}-{slot}', f'Freagra {slot}', 1, [f'Aon fhreagra ceart don chuid seo = 1 mharc. Ní féidir an freagra céanna a áireamh faoi dhó. {chunk}', general])],
                        reading_requirements, 'The scheme prices the two answers 1 mharc + 1 mharc independently; this card practises one of them. ' + part_note, None, source)
            if mode == 'points':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Pointe {slot}',
                        f'{text} Don chárta seo: tabhair pointe eolais amháin, i d’fhocail féin (pointe {slot}, 6 mharc).', topic, passage['pages'], spages,
                        [criterion(f'point-{slot}', f'Pointe eolais {slot}', 6, [chunk, general])], reading_requirements,
                        'The scheme prices the two points 6 + 6 independently; this card practises one of them. ' + part_note, None, source)
        for q, parts in by_question.items():
            crits = [dict(c) for _, _, card in parts for c in card['criteria']]
            add(f'R-{letter}-{q}', f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}',
                f'{q}. ' + ' '.join(p for _, p, _ in parts) + (' (7 marc)' if q != '6' else ' (15 mharc)'), topic, passage['pages'],
                sorted({p for _, _, c in parts for p in c['schemePages']}), crits,
                ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.', 'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.'],
                'Retained complete printed question. Score each published part separately using these SEC allocations. Two-answer grammar is one 0/2/3 placement; opinion and point conditions remain inside their response awards.',
                ['irish-3-3'] if q == '6' else None, source)
            assert cards[-1]['totalMarks'] == (15 if q == '6' else 7), (letter, q)

    # ---- Ceisteanna 2–4: An Litríocht -------------------------------------------------------
    lit = Scheme(doc, 25, 48)
    gaeilge_table, _ = Scheme(doc, 26, 26).chunk('Gaeilge (5 mharc)', 'PRÓS AINMNITHE nó PRÓS ROGHNACH')
    note5, _ = Scheme(doc, 26, 26).chunk('Nóta: I gcás na gceisteanna 2', 'Gaeilge (5 mharc)')
    prose_table, _ = Scheme(doc, 26, 26).chunk('Catagóir Plé (25 marc)', 'Ceist 2')
    gaeilge = lambda: criterion('gaeilge', 'Gaeilge', 5, [gaeilge_table, note5], 'quality')
    lit_requirements = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
    prose = [
        ('P-2A-a-caca-milis', 'prose-2a-a-caca-milis', 'Prós 2A(a) · Cáca Milis', 'irish-4-6',
         'Freagair an cheist thíos ar an scannán Cáca Milis nó ar an dráma An Lasair Choille.\n\nCáca Milis\n‘Tugtar léiriú sa scannán Cáca Milis ar an gcineál duine í Catherine tríd an gcaidreamh a bhí aici lena máthair agus leis an bhfear dall, Paul.’\nDéan plé ar an ráiteas sin. (30 marc)',
         [lit.chunk('Cáca Milis (2A(a)S)', 'An Lasair Choille (2A(a)D)')]),
        ('P-2A-a-an-lasair-choille', 'prose-2a-a-an-lasair-choille', 'Prós 2A(a) · An Lasair Choille', 'irish-4-8',
         'Freagair an cheist thíos ar an scannán Cáca Milis nó ar an dráma An Lasair Choille.\n\nAn Lasair Choille\n‘Tugtar léiriú sa dráma An Lasair Choille ar an saol atá ag an bhfear óg, Séamas, le Micil agus ar an athrú a thagann ar thuiscint Shéamais ar an saol sin de bharr chuairt Mhíoda.’\nDéan plé ar an ráiteas sin. (30 marc)',
         [lit.chunk('An Lasair Choille (2A(a)D)', '(b) Freagair an cheist thíos ar an ngearrscéal Dís.')]),
        ('P-2A-b', 'prose-2a-b', 'Prós 2A(b) · Dís', 'irish-4-4',
         'Freagair an cheist thíos ar an ngearrscéal Dís.\n\nDís\n‘Tugtar léiriú sa ghearrscéal Dís ar an gcineál saoil atá ag bean Sheáin agus ar an dearcadh atá aici ar an saol sin.’\nDéan plé ar an ráiteas sin. (30 marc)',
         [lit.chunk('(b) Freagair an cheist thíos ar an ngearrscéal Dís.', '2B. Prós Roghnach')]),
        # The optional film and the optional play share one grid and one Atlas heading (irish-4-7),
        # so one card carries both printed alternatives (choose-one refinement, 2026-10-12).
        ('P-2B-a', 'prose-2b-a', 'Prós 2B(a) · Scannán nó dráma roghnach', 'irish-4-7',
         'Freagair an cheist thíos ar an scannán roghnach nó ar an dráma roghnach.\n\nMaidir leis an scannán roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé ar an léargas a thugtar dúinn ar iompar an phríomhcharachtair (na príomhphearsan) agus ar an gcaoi a dtéann iompar an duine sin i bhfeidhm ar imeachtaí an scannáin.\n\nNí mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (30 marc)\n\nnó\n\nMaidir leis an dráma roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé ar an léargas a thugtar dúinn ar iompar an phríomhcharachtair (na príomhphearsan) agus ar an gcaoi a dtéann iompar an duine sin i bhfeidhm ar imeachtaí an dráma.\n\nNí mór teideal an dráma sin, mar aon le hainm an scríbhneora, a scríobh síos go cruinn. (30 marc)',
         [lit.chunk('Maidir leis an scannán roghnach', 'nó Maidir leis an dráma roghnach'),
          lit.chunk('Maidir leis an dráma roghnach', 'nó (b) Freagair an cheist thíos ar an ngearrscéal roghnach.')]),
        ('P-2B-b', 'prose-2b-b', 'Prós 2B(b) · Gearrscéal roghnach', 'irish-4-7',
         'Freagair an cheist thíos ar an ngearrscéal roghnach.\n\nMaidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé ar an léargas a thugtar dúinn ar shaol agus ar mheon an phríomhcharachtair (na príomhphearsan) ó thús deireadh an ghearrscéil.\n\nNí mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (30 marc)',
         [lit.chunk('nó (b) Freagair an cheist thíos ar an ngearrscéal roghnach.', '⟦32⟧')]),
    ]
    head2 = 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach).'
    for key, slug, ref, topic, prompt, chunks in prose:
        for line in prompt.splitlines():
            if line:
                assert in_order(line, texts[7]), (key, line)
        guidance = [c for c, _ in chunks] + [prose_table]
        spages = sorted({p for _, ps in chunks for p in ps} | {26})
        section = ('2A. Prós Ainmnithe\nFreagair do rogha ceann amháin de (a) nó (b) thíos.' if key.startswith('P-2A') else
                   '2B. Prós Roghnach\nFreagair do rogha ceann amháin de (a) nó (b) thíos.\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.')
        add(key, slug, ref, head2 + '\n\n' + section + '\n\n' + ('(a) ' if key[-1] != 'b' else '(b) ') + prompt, topic, [8], spages,
            [criterion('eolas', 'Eolas', 25, guidance, 'indicative'), gaeilge()], lit_requirements,
            'One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award. Supporting notes are indicative; other valid points are credited on their merits. '
            'With only one of the two required aspects discussed, the scheme marks the Eolas out of 18. Do not add alternative route tariffs together.')

    poems = [
        ('F-3A-a', 'poetry-3a-a', 'Filíocht 3A(a) · An tEarrach Thiar', 'irish-5-3', 9, '(a) An tEarrach Thiar', '(b) Mo ghrá-sa', [
            '(i) ‘Sa dán An tEarrach Thiar (thíos), úsáideann an file íomhánna chun saol an oileáin le linn a óige a chur os ár gcomhair.’ É sin a phlé. (15 mharc)',
            '(ii) Cén éifeacht atá ag athrá na bhfocal ‘San Earrach thiar’ ag deireadh gach véarsa, dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile sin. (9 marc)']),
        ('F-3A-b', 'poetry-3a-b', 'Filíocht 3A(b) · Mo ghrá‐sa (idir lúibíní)', 'irish-5-4', 10, '(b) Mo ghrá-sa', '3B. Filíocht Roghnach', [
            '(i) ‘Roghnaíonn an file íomhánna ón nádúr chun léiriú a thabhairt dúinn ar chuma agus ar thréithe an fhir sa dán Mo ghrá‐sa (idir lúibíní) (thíos).’ É sin a phlé. (15 mharc)',
            '(ii) Cén éifeacht a bhaineann le húsáid na lúibíní sa dán seo, dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile sin. (9 marc)']),
        ('F-3B-a', 'poetry-3b-a', 'Filíocht 3B(a) · Dán roghnach', 'irish-5-6', 11, '(a) (i) Maidir le dán nua-aimseartha roghnach', 'nó (b) (i) Maidir le dán nua-aimseartha roghnach', [
            '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin, dar leat. Déan plé ar an bhforbairt a dhéantar ar an bpríomhthéama sin ó thús deireadh an dáin. (15 mharc)',
            '(ii) Cén mothúchán is láidre atá sa dán, dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile sin. (9 marc)']),
        ('F-3B-b', 'poetry-3b-b', 'Filíocht 3B(b) · Dán roghnach', 'irish-5-6', 11, 'nó (b) (i) Maidir le dán nua-aimseartha roghnach', 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F). Treoracha', [
            '(i) Maidir le dán nua‐aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an dáin, dar leat. Déan plé ar an léiriú a thugtar ar an bpríomhthéama sin ó thús deireadh an dáin. (15 mharc)',
            '(ii) An bhfuil teideal an dáin oiriúnach do phríomhthéama an dáin, dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cé a chum an dán seo? Scríobh nóta gairid ar shaol agus ar shaothar an fhile sin. (9 marc)']),
    ]
    head3 = 'Freagair Ceist 3A (Filíocht Ainmnithe) nó Ceist 3B (Filíocht Roghnach).'
    for key, slug, ref, topic, page, start, end, parts in poems:
        whole, spages = lit.chunk(start, end)
        for part in parts:
            assert in_order(part, texts[page - 1]), (key, part[:40])
        i2 = whole.index('(ii) ', whole.index('Eolas = 13 mharc'))
        i3 = whole.index('(iii) Cé a chum an dán seo?')
        pieces = [whole[:i2], whole[i2:i3], whole[i3:]]
        for piece, cap in zip(pieces, ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc']):
            assert cap in piece, (key, cap)
        section = ('3A. Filíocht Ainmnithe\nFreagair do rogha ceann amháin de (a) nó (b).\n\n' + start if key.startswith('F-3A') else
                   '3B. Filíocht Roghnach\nFreagair do rogha ceann amháin de (a) nó (b) thíos.\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.\n\n(' + key[-1] + ')')
        add(key, slug, ref, head3 + '\n\n' + section.replace('Mo ghrá-sa', 'Mo ghrá‐sa (idir lúibíní)') + '\n' + '\n'.join(parts), topic, [page], spages,
            [criterion('eolas-i', '(i) Eolas', 13, [pieces[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
             criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge()], ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.'],
            'One complete SEC response with one shared five-mark Gaeilge award. The Eolas criteria keep the printed caps (13, 5, 7) and conditions. Supporting notes are indicative rather than exhaustive.',
            source=('Filíocht Ainmnithe' if key.startswith('F-3A') else 'Filíocht Roghnach', ref.split(' · ', 1)[1], [page]))

    general4, _ = lit.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Ceist 4 LITRÍOCHT BHREISE')
    options = [
        ('X-4A', 'literature-4-a', '4A. An Triail', 'irish-6-0', '4A. An Triail', '4B. A Thig Ná Tit Orm',
         '4A. An Triail\n‘Sa dráma An Triail, fulaingíonn an cailín óg, Máire Ní Chathasaigh, go mór de bharr rialacha na sochaí ag an am.’\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig Ná Tit Orm', 'irish-6-1', '4B. A Thig Ná Tit Orm', '4C. Tóraíocht Dhiarmada',
         '4B. A Thig Ná Tit Orm\nDéan plé ar an dá thréith is mó, dar leat, a bhaineann le Maidhc Dainín mar a léirítear iad sa dírbheathaisnéis A Thig Ná Tit Orm. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2', '4C. Tóraíocht Dhiarmada', '4D. Gafa',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n‘Cuirtear Diarmaid romhainn mar laoch dílis tragóideach sa Tóraíocht.’\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3', '4D. Gafa', '4E. Canary Wharf',
         '4D. Gafa\n‘Tugtar léiriú dúinn sa sliocht as an úrscéal Gafa ar bhriseadh croí Eithne, an mháthair, agus í ag plé le handúil a mic, Eoin, agus leis an easpa tacaíochta óna fear céile, Breandán.’\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4', '4E. Canary Wharf', '4F. Dánta Breise',
         '4E. Canary Wharf\n‘Sa scéal Cúrsa Eitilte, tugtar léiriú dúinn ar an gcaoi ar éirigh le Theo na deacrachtaí go léir a cuireadh roimhe a shárú agus é ar a bhealach chun bualadh le Alana.’\nDéan plé ar an ráiteas sin. (40 marc)'),
    ]
    head4 = 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.'
    for key, slug, ref, topic, start, end, prompt in options:
        assert all(in_order(line, texts[11]) for line in prompt.splitlines()), key
        chunk, spages = lit.chunk(start, end)
        assert 'Eolas = 35 marc' in chunk
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [12], sorted(set(spages) | {40}),
            [criterion('eolas', 'Eolas', 35, [chunk, general4], 'indicative'), gaeilge()], lit_requirements,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.')
    f_chunk, f_pages = lit.chunk('4F. Dánta Breise', None)
    f_chunk = f_chunk.split('Socruithe Réasúnta')[0]
    i2 = f_chunk.index('(ii) A bhfuil i gceist'); i3 = f_chunk.index('(iii) An bhfuil trua')
    f_parts = [f_chunk[:i2], f_chunk[i2:i3], f_chunk[i3:]]
    for piece, cap in zip(f_parts, ['Eolas = 19 marc', 'Eolas = 7 marc', 'Eolas = 9 marc']):
        assert cap in piece
    f_prompt = ('4F. Dánta Breise – Colmáin\nFreagair (i), (ii) agus (iii) thíos.\n'
                '(i) Cad é príomhthéama an dáin Colmáin (thall), dar leat? Déan plé ar an bhforbairt a dhéantar ar an bpríomhthéama sin ó thús deireadh an dáin. (20 marc)\n'
                '(ii) A bhfuil i gceist leis na línte seo a mhíniú: Ar na laethe úd a mhothaíodh sé dáimh as an ghnáth leis na colmáin, bhíodh iontas an domhain air nach ndéanfadh siad cuideachta leis i dtráth ná in antráth. (10 marc)\n'
                '(iii) An bhfuil trua agat do chás an chait sa dán? Tabhair dhá fháth le do fhreagra. Bíodh tagairtí cruinne agat do théacs an dáin i do fhreagra. (10 marc)')
    assert all(in_order(line, texts[11]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – Colmáin', head4 + '\n\n' + f_prompt, 'irish-6-9', [12, 13],
                  sorted(set(f_pages) | {40}),
                  [criterion('eolas-i', '(i) Eolas', 19, [f_parts[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [f_parts[1]], 'indicative'),
                   criterion('eolas-iii', '(iii) Eolas', 9, [f_parts[2]], 'indicative'), gaeilge()],
                  ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.'],
                  'One complete SEC response with one shared five-mark Gaeilge award. The Eolas criteria keep the printed caps (19, 7, 9). Supporting notes are indicative rather than exhaustive.',
                  source=('Dánta Breise', 'Colmáin', [12, 13]))

    decisions = selection_decisions(paper)
    assert len(cards) == 71 and len({c['id'] for c in cards}) == 71, len(cards)
    assert len({c['atlasQuestionId'] for c in cards}) == 71
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2026, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=decisions,
                  readingCardIds=[c['id'] for c in cards if '-reading-' in c['id']],
                  literatureRouteCardIds=[c['id'] for c in cards if '-reading-' not in c['id']],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 34 published parts and 10 independent answer/point slots; 6 prose, 4 poetry and 6 additional-literature routes.')
    return dict(review=review, cards=cards), doc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data, _ = build()
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Higher 2026 Paper 2: {len(data['cards'])} reviewed task/route cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
