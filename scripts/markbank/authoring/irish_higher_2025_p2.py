#!/usr/bin/env python3
"""Reviewed 2025 Higher Paper 2 (Léamhthuiscint agus Litríocht).

Paper PDF 1–16 and the Paper 2 pages of the combined LC001ALP000IV scheme
(PDF 18–47, plus 48 modified marking) visually reviewed on 2026-10-11. Counts are
assertions, not corpus-completeness proof.

The legacy generator already ships 26 cards for this component: the twelve
whole reading questions and the fourteen literature routes. Their IDs are kept.
`apply_legacy_review` (called by irish_cards.py) joins them to Atlas and replaces
their marking with the lifted 2025 scheme (each reading part and each poetry
sub-question keeps its own published tariff). `build` adds every published
reading part as a practice card, plus the independent 1 + 1 answer slots and the
6 + 6 point slots, beside the legacy file (the same shapes as the reviewed 2024
and 2026 Higher Paper 2).
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP200IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2025-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2025-p2-source-review.json'
REVIEWED_AT = '2026-10-11'
PAPER_SHA = '156b8550e26eeb1d870fe84538c6fac9d0eb15f65776a54673b4ce05756bfb15'
SCHEME_SHA = '2b4f503260b2bcb3704a3f428bee88bbcccd8746b2a2b58208142cf7e6ff1550'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|ceann amháin|pointe amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'


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
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()))

    def chunk(self, start, end=None, after=0):
        i = self.text.index(start, after)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:i])[-1])}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


GAEILGE_TABLE = re.compile(r'Gaeilge \(5 mharc\) Sárchumas.*?Cumas lag/an-lag maidir leis na príomhghnéithe de cheart na teanga \(gramadach, comhréir, struchtúr, deilbhíocht\) 1')


def printed_values(chunk, marks):
    return sorted({0, marks} | {int(v) for v in re.findall(r'= (\d+) mh?arc', chunk) if int(v) <= marks})


_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2025/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2025/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 18, 47)
    general = s.chunk('Freagair Léamhthuiscint A agus Léamhthuiscint B. Tá Ceist 1', 'Siombailí Anótála')[0]
    # (q, part, paper prompt, scheme anchor, marks, mode)
    passages = {
        'A': dict(title='Rory Gallagher – Laoch ceoil', pages=[4, 5], topic='irish-3-0', end='LÉAMHTHUISCINT B (50 marc)', parts=[
            ('1', 'a', '(a) Tabhair dhá chúis ar mhúscail díolachán uirlisí ceoil Rory Gallagher spéis mhór i measc lucht leanúna an rac‐cheoil agus bailitheoirí earraí cuimhneacháin araon. (Alt 1)', '1. (a) Tabhair dhá chúis', 3, 'ordered'),
            ('1', 'bi', '(b) (i) Cén fáth ar shantaigh Rory an giotár leictreach Fender Stratocaster? (Alt 1)', '(b) (i) Cén fáth ar shantaigh', 2, None),
            ('1', 'bii', '(ii) Scríobh síos cúis amháin a gcuirfear giotár íocónach Fender Stratocaster Rory Gallagher ar taispeáint in Ard‐Mhúsaem na hÉireann. (Alt 1)', '(ii) Scríobh síos cúis amháin a gcuirfear', 2, None),
            ('2', 'a', '(a) Scríobh síos dhá rud a léiríonn go raibh féith an cheoil i dtuismitheoirí Rory. (Alt 2)', '2. (a) Scríobh síos dhá rud', 3, 'ordered'),
            ('2', 'bi', '(b) (i) Cén tábhacht a bhain leis an stáisiún raidió AFN i saol Rory? (Alt 2)', '(b) (i) Cén tábhacht', 2, None),
            ('2', 'bii', '(ii) Cad a dhéanadh Rory a tharraingíodh aird na ndaoine a bhíodh bailithe os comhair an tsiopa i gceantar an Diamaint i nDoire? (Alt 2)', '(ii) Cad a dhéanadh Rory', 2, None),
            ('3', 'a', '(a) Cén fáth a raibh ceannach an ghiotáir Fender Stratocaster tábhachtach do Rory? (Alt 3)', '3. (a) Cén fáth a raibh ceannach', 3, None),
            ('3', 'bi', '(b) (i) Cén sárchumas a bhí sa ghrúpa Taste a thuill cáil dóibh? (Alt 3)', '(b) (i) Cén sárchumas', 2, None),
            ('3', 'bii', '(ii) Cad a tharla don ghrúpa Taste in 1970? (Alt 3)', '(ii) Cad a tharla don ghrúpa Taste', 2, None),
            ('4', 'a', '(a) Luaigh dhá bhealach a dtéadh Rory Gallagher i gcion go mór ar a lucht féachana ag a chuid ceolchoirmeacha beo. (Alt 4)', '4. (a) Luaigh dhá bhealach', 3, 'ordered'),
            ('4', 'bi', '(b) (i) Scríobh síos rud amháin a léiríonn an t‐ardmheas a bhí ar Rory i saol an rac‐cheoil faoin mbliain 1974. (Alt 4)', '(b) (i) Scríobh síos rud amháin a léiríonn', 2, None),
            ('4', 'bii', '(ii) Conas a thaispeántar go raibh ráchairt mhór ar an albam Live in Europe (1972) nuair a eisíodh é? (Alt 4)', '(ii) Conas a thaispeántar', 2, None),
            ('5', 'a', '(a) Scríobh síos dhá dhúshlán a chruthaigh tionscal an cheoil do Rory Gallagher mar ealaíontóir. (Alt 5)', '5. (a) Scríobh síos dhá dhúshlán', 3, 'ordered'),
            ('5', 'bi', '(b) (i) Scríobh síos dhá chomhartha ómóis do Rory Gallagher atá in Éirinn. (Alt 5)', '(b) (i) Scríobh síos dhá chomhartha', 2, 'slots'),
            ('5', 'bii', '(ii) Cad a rinne an comhlacht Fender sa bhliain 1998 chun ómós a thabhairt do Rory? (Alt 5)', '(ii) Cad a rinne an comhlacht Fender', 2, None),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Fháistineach in Alt 1 agus sampla d’ainmfhocal baininscneach sa tuiseal ginideach uatha in Alt 4.', '6. (a) Aimsigh sampla', 3, 'grammar'),
            ('6', 'b', '(b) ‘Ceoltóir as an ngnáth ba ea Rory Gallagher.’ Tabhair dhá phointe eolais, i d’fhocail féin, as an sliocht a léiríonn fírinne an ráitis sin, dar leat. (Is leor 60 focal.)', '(b) ‘Ceoltóir as an ngnáth', 12, 'points')]),
        'B': dict(title='Cúrsaí spóirt in Éirinn', pages=[6, 7], topic='irish-3-1', end='⟦26⟧', parts=[
            ('1', 'a', '(a) Cén fáth arb iad na Cluichí Oilimpeacha in 2024 na Cluichí Oilimpeacha is rathúla a bhí ag aon fhoireann Oilimpeach as Éirinn riamh? (Alt 1)', '1. (a) Cén fáth arb iad', 3, None),
            ('1', 'bi', '(b) (i) Cén t‐éacht speisialta a rinne an dornálaí Kellie Harrington agus na rámhaithe Paul O’Donovan agus Fintan McCarthy ag na Cluichí Oilimpeacha i bPáras? (Alt 1)', '(b) (i) Cén t-éacht speisialta', 2, None),
            ('1', 'bii', '(ii) Cén fáth ar moladh lúthchleasaithe Parailimpeacha uile na hÉireann a bhí san iomaíocht ag na Cluichí Parailimpeacha anuraidh? (Alt 1)', '(ii) Cén fáth ar moladh', 2, None),
            ('2', 'a', '(a) Luaigh dhá bhuntáiste a bhaineann leis an spórt. (Alt 2)', '2. (a) Luaigh dhá bhuntáiste', 3, 'ordered'),
            ('2', 'bi', '(b) (i) Tabhair dhá shampla de ghníomhaíochtaí coirp a dhéanann daoine mar chaitheamh aimsire. (Alt 2)', '(b) (i) Tabhair dhá shampla de ghníomhaíochtaí', 2, 'slots'),
            ('2', 'bii', '(ii) Cad air a mbíonn an bhéim sa spórt iomaíoch? (Alt 2)', '(ii) Cad air a mbíonn an bhéim', 2, None),
            ('3', 'a', '(a) Cén aidhm atá ag Cumann Lúthchleas Gael, ag Cumann Camógaíochta agus ag Cumann Pheil na mBan? (Alt 3)', '3. (a) Cén aidhm', 3, None),
            ('3', 'bi', '(b) (i) Scríobh síos slí amháin a bhfuil clubanna Chumann Lúthchleas Gael tábhachtach i bpobail ar fud na tíre. (Alt 3)', '(b) (i) Scríobh síos slí amháin', 2, None),
            ('3', 'bii', '(ii) Cad atá beartaithe ag Spórt Éireann maidir le cosaint na hiománaíochta agus na camógaíochta? (Alt 3)', '(ii) Cad atá beartaithe', 2, None),
            ('4', 'a', '(a) Scríobh síos ceann de phríomhaidhmeanna an rialtais atá leagtha amach sa Bheartas Náisiúnta Spóirt, 2018 – 2027. (Alt 4)', '4. (a) Scríobh síos ceann de phríomhaidhmeanna', 3, None),
            ('4', 'bi', '(b) (i) Tabhair dhá shampla a léiríonn go bhfuil an bhearna rannpháirtíochta idir na hinscní ag cúngú i gcúrsaí spóirt. (Alt 4)', '(b) (i) Tabhair dhá shampla a léiríonn', 2, 'slots'),
            ('4', 'bii', '(ii) Cén toradh a bheidh ar an obair go léir leis na grúpaí éagsúla sa tír, de réir an rialtais? (Alt 4)', '(ii) Cén toradh a bheidh', 2, None),
            ('5', 'a', '(a) Cén úsáid a bhainfear as na deontais a fógraíodh faoi mhaoiniú an rialtais de €230 milliún faoin gCiste Áiseanna Spóirt Pobail? (Alt 5)', '5. (a) Cén úsáid a bhainfear', 3, None),
            ('5', 'bi', '(b) (i) Luaigh dhá rud a sholáthraítear ar an gCampas Náisiúnta Spórt do na lúthchleasaithe ardfheidhmíochta. (Alt 5)', '(b) (i) Luaigh dhá rud a sholáthraítear', 2, 'slots'),
            ('5', 'bii', '(ii) Scríobh síos dhá rud atá ag teastáil chun córas spóirt éifeachtach a fhorbairt ar mhaithe le muinín an phobail ann a chinntiú. (Alt 5)', '(ii) Scríobh síos dhá rud atá ag teastáil', 2, 'slots'),
            ('6', 'a', '(a) Aimsigh sampla de bhreischéim na haidiachta in Alt 4 agus sampla den bhriathar saor san Aimsir Chaite in Alt 5.', '6. (a) Aimsigh sampla de bhreischéim', 3, 'grammar'),
            ('6', 'b', '(b) ‘Tá dul chun cinn maith á dhéanamh i gcúrsaí spóirt in Éirinn.’ Tabhair dhá phointe eolais, i d’fhocail féin, as an sliocht a léiríonn fírinne an ráitis sin, dar leat. (Is leor 60 focal.)', '(b) ‘Tá dul chun cinn', 12, 'points')]),
    }
    start_b = s.text.index('LÉAMHTHUISCINT B (50 marc)')
    for letter, passage in passages.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        anchors = [p[3] for p in passage['parts']]
        resolved = []
        pos = start_b if letter == 'B' else 0
        for index, (q, part, prompt, anchor, marks, mode) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            # Anchors are searched forward from the previous part so repeated stems resolve in printed order.
            here = s.text.index(anchor, pos)
            assert letter == 'B' or here < start_b, (letter, q, part)
            chunk, spages = s.chunk(anchor, anchors[index + 1] if index + 1 < len(anchors) else passage['end'], pos)
            pos = here + 1
            tariff = '6 mharc + 6 mharc' if mode == 'points' else (f'{{{marks} mharc' if mode != 'slots' else '{2 mharc: 1 mharc + 1 mharc}')
            assert tariff in chunk, (letter, q, part, chunk[:90])
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    lit = s
    note5 = lit.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Nóta: Níl na nótaí tacaíochta seo uileghabhálach ná críochnúil agus bronnfar marcanna ar phointí bailí')[0]
    notes = lit.chunk('Nóta: Níl na nótaí tacaíochta seo uileghabhálach ná críochnúil agus bronnfar marcanna ar phointí bailí', 'Gaeilge (5 mharc)')[0]
    gaeilge_table = GAEILGE_TABLE.search(lit.text, lit.text.index('⟦27⟧')).group(0)
    prose_table = lit.chunk('Catagóir Eolas (25 marc) (18 marc)', 'Ceist 2 PRÓS 30 marc')[0]
    general4 = lit.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Gaeilge (5 mharc)', lit.text.index('⟦39⟧'))[0]
    assert all(x in gaeilge_table for x in ['Sárchumas', 'Cumas lag/an-lag']) and '22-25' in prose_table and '30-35' in general4
    _MATERIAL = dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, notes=notes,
                     gaeilge_table=gaeilge_table, prose_table=prose_table, general4=general4,
                     decisions=selection_decisions(paper))
    return _MATERIAL


READING_REQUIREMENTS = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                        'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
PART_NOTE = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
             'Retained whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')


def part_criteria(q, part, marks, mode, chunk, general):
    if mode == 'points':
        return [criterion('point-1', 'Pointe eolais 1', 6, [chunk, general]), criterion('point-2', 'Pointe eolais 2', 6, [chunk, general])]
    if mode in ('ordered', 'grammar'):
        return [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks,
                          [chunk, general, 'Order-dependent award: the first correct item earns 2 and the other 1 (0, 2 or 3).'], permitted=[0, 2, 3])]
    return [criterion(part, 'Freagra', marks, [chunk, general], permitted=printed_values(chunk, marks))]


def gaeilge(m):
    return criterion('gaeilge', 'Gaeilge', 5, [m['gaeilge_table'], m['note5']], 'quality')


def apply_legacy_review(cards):
    """Lift the 2025 scheme onto the 26 retained legacy cards (IDs, totals and topics unchanged)."""
    m = material()
    by_id = {c['id']: c for c in cards}
    stamped = []

    def stamp(card_id, atlas, pages, scheme_pages, criteria, note, requirements=None):
        card = by_id[card_id]
        card.update(atlasQuestionId=atlas, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages, paperPage=pages[0],
                    schemePage=scheme_pages[0], schemePages=scheme_pages, criteria=criteria, markingGuideNote=note)
        if requirements:
            card['taskRequirements'] = requirements
        assert sum(c['maxMarks'] for c in criteria) == card['totalMarks'], card_id
        stamped.append(card_id)
        return card

    for letter, passage in m['passages'].items():
        by_q = {}
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            by_q.setdefault(q, []).append((part, marks, mode, chunk, spages))
        for q, parts in by_q.items():
            crits = [c for part, marks, mode, chunk, _ in parts for c in part_criteria(q, part, marks, mode, chunk, m['general'])]
            # Label each criterion with its printed part so the whole question reads as the paper does.
            labels = {'a': '(a)', 'bi': '(b)(i)', 'bii': '(b)(ii)', 'grammar': '(a)', 'point-1': '(b) Pointe eolais 1', 'point-2': '(b) Pointe eolais 2'}
            for c in crits:
                c['label'] = labels[c['id']] + (' Freagra' if not c['id'].startswith('point') else '')
            n = str(int(q) + (6 if letter == 'B' else 0))
            stamp(f'irish-2025-hl-p2-reading-{letter.lower()}-q{q}', n, passage['pages'], sorted({p for *_, sp in parts for p in sp}), crits,
                  'Retained complete printed question. Score each published part separately using these SEC allocations. '
                  'Two-answer grammar is one 0/2/3 placement; 6(b) points P1 and P2 are 6 marks each and must be in the candidate’s own words.',
                  ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                   'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.'])

    s, notes, prose_table = m['s'], m['notes'], m['prose_table']
    lit_requirements = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
    prose = [('prose-2a-a', 'P-2A-a', '(a) Freagair an cheist thíos ar an ngiota as an úrscéal Hurlamaboc.', 'nó (b) Freagair an cheist thíos ar an scéal béaloidis'),
             ('prose-2a-b', 'P-2A-b', 'nó (b) Freagair an cheist thíos ar an scéal béaloidis', '2B. Prós Roghnach'),
             ('prose-2b-a', 'P-2B-a', '(a) Maidir leis an ngiota as an úrscéal roghnach', 'nó (b) Maidir le scéal béaloidis roghnach'),
             ('prose-2b-b', 'P-2B-b', 'nó (b) Maidir le scéal béaloidis roghnach', 'Nóta: Níl na nótaí tacaíochta seo uileghabhálach ná críochnúil agus bronnfar marcanna ar phointí ábhartha')]
    for slug, atlas, start, end in prose:
        chunk, spages = s.chunk(start, end)
        assert 'Eolas = 25 marc' in chunk and 'Gaeilge (5 mharc)' not in chunk, slug
        stamp(f'irish-2025-hl-p2-{slug}', atlas, [8], sorted(set(spages) | {27}),
              [criterion('eolas', 'Eolas', 25, [re.sub(r'^nó ', '', chunk), prose_table, notes], 'indicative'), gaeilge(m)],
              'One complete SEC response: 25 Eolas and a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive; '
              'with only one of the required aspects discussed, the scheme marks the Eolas out of 18.', lit_requirements)

    poems = [('poetry-3a-a', 'F-3A-a', [9], '(a) An Spailpín Fánach (i)', 'nó (b) Colscaradh', ['(ii) Is é an spailpín féin', '(iii) Cén mheadaracht']),
             ('poetry-3a-b', 'F-3A-b', [10], 'nó (b) Colscaradh', '3B. Filíocht Roghnach', ['(ii) Is é an file féin a insíonn', '(iii) Cé a chum an dán seo?']),
             ('poetry-3b-a', 'F-3B-a', [11], '(a) (i) Maidir le dán seanaimseartha roghnach', 'nó (b) (i) Maidir le dán nua-aimseartha roghnach', ['(ii) Cén mothúchán is láidre', '(iii) Scríobh síos an teicníc fhileata']),
             ('poetry-3b-b', 'F-3B-b', [11], 'nó (b) (i) Maidir le dán nua-aimseartha roghnach', 'Freagair do rogha ceann amháin as Ceist 4', ['(ii) Cén teicníc fhileata is mó', '(iii) Cé a chum an dán seo?'])]
    for slug, atlas, pages, start, end, cuts in poems:
        whole, spages = s.chunk(start, end)
        # The printed Gaeilge table can sit between sub-questions; it belongs to the shared award, not to Eolas.
        whole = re.sub(r'^nó ', '', GAEILGE_TABLE.sub(' ', whole)).strip()
        assert 'Gaeilge (5 mharc)' not in whole, slug
        i2 = whole.index(cuts[0]); i3 = whole.index(cuts[1], i2)
        pieces = [whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()]
        for piece, cap in zip(pieces, ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc']):
            assert cap in piece, (slug, cap)
        guidance0 = [pieces[0], notes] if atlas.startswith('F-3A') else [pieces[0]]
        stamp(f'irish-2025-hl-p2-{slug}', atlas, pages, sorted(set(spages) | ({31} if atlas.startswith('F-3A') else set())),
              [criterion('eolas-i', '(i) Eolas', 13, guidance0, 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
               criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge(m)],
              'One complete SEC response with one shared five-mark Gaeilge award. The Eolas criteria keep the printed caps (13, 5, 7) and conditions. '
              'Supporting notes are indicative rather than exhaustive.', lit_requirements)

    options = [('literature-4-a', 'X-4A', '4A. An Triail', '4B. A Thig Ná Tit Orm'),
               ('literature-4-b', 'X-4B', '4B. A Thig Ná Tit Orm', '4C. Tóraíocht Dhiarmada'),
               ('literature-4-c', 'X-4C', '4C. Tóraíocht Dhiarmada', '4D. Gafa'),
               ('literature-4-d', 'X-4D', '4D. Gafa', '4E. Canary Wharf'),
               ('literature-4-e', 'X-4E', '4E. Canary Wharf', '4F. Dánta Breise')]
    for slug, atlas, start, end in options:
        chunk, spages = s.chunk(start, end, s.text.index('⟦40⟧'))
        assert 'Eolas = 35 marc' in chunk, slug
        stamp(f'irish-2025-hl-p2-{slug}', atlas, [12], sorted(set(spages) | {39}),
              [criterion('eolas', 'Eolas', 35, [chunk, m['general4']], 'indicative'), gaeilge(m)],
              'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
              lit_requirements)
    # 4F keeps its reviewed Eolas criteria (17, 9, 9); only the Gaeilge award and the Atlas join change.
    f = by_id['irish-2025-hl-p2-literature-4-f']
    assert [c['maxMarks'] for c in f['criteria']] == [17, 9, 9, 5]
    stamp(f['id'], 'X-4F', [12, 13, 14], f['schemePages'] if f.get('schemePages') else [45, 46, 47],
          [copy.deepcopy(c) for c in f['criteria'][:3]] + [gaeilge(m)], f['markingGuideNote'])
    assert len(stamped) == 26
    return cards, stamped


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, note, extra_topics=None, title=None):
        cards.append(dict(
            id=f'irish-2025-hl-p2-{slug}', year=2025, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2025 HL Paper 2 {ref}', questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic,
            **({'additionalTopicIds': extra_topics} if extra_topics else {}),
            conceptId=f'irish-hl-p2-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=READING_REQUIREMENTS, criteria=criteria, markingGuideNote=note,
            sourceMaterial=dict(kind='source-text', label=ref.split(' · ')[0], title=title, pages=pages,
                                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE)))

    for letter, passage in m['passages'].items():
        topic = passage['topic']
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            label = f'{q}({part[0]})' + (f'({part[1:]})' if len(part) > 1 else '')
            text = f'{label} ' + re.sub(r'^(\([a-z]+\)\s*)+', '', prompt)
            here = 'irish-3-3' if mode == 'grammar' else topic
            add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {label}', text, here,
                passage['pages'], spages, part_criteria(q, part, marks, mode, chunk, m['general']), PART_NOTE,
                [topic] if mode == 'grammar' else None, passage['title'])
            if mode == 'slots':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Freagra {slot}',
                        f'{text} Don chárta seo: tabhair freagra amháin don chuid seo (freagra {slot}, 1 mharc).', topic, passage['pages'], spages,
                        [criterion(f'{part}-{slot}', f'Freagra {slot}', 1, [f'Aon fhreagra ceart don chuid seo = 1 mharc. Ní féidir an freagra céanna a áireamh faoi dhó. {chunk}', m['general']])],
                        'The scheme prices the two answers 1 mharc + 1 mharc independently; this card practises one of them. ' + PART_NOTE, None, passage['title'])
            if mode == 'points':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Pointe {slot}',
                        f'{text} Don chárta seo: tabhair pointe eolais amháin, i d’fhocail féin (pointe {slot}, 6 mharc).', topic, passage['pages'], spages,
                        [criterion(f'point-{slot}', f'Pointe eolais {slot}', 6, [chunk, m['general']])],
                        'The scheme prices the two points 6 + 6 independently; this card practises one of them. ' + PART_NOTE, None, passage['title'])
    assert len(cards) == 48 and len({c['id'] for c in cards}) == 48
    for card in cards:
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    legacy = ([f'irish-2025-hl-p2-reading-{l}-q{q}' for l in 'ab' for q in range(1, 7)]
              + [f'irish-2025-hl-p2-prose-{k}' for k in ['2a-a', '2a-b', '2b-a', '2b-b']]
              + [f'irish-2025-hl-p2-poetry-{k}' for k in ['3a-a', '3a-b', '3b-a', '3b-b']]
              + [f'irish-2025-hl-p2-literature-4-{k}' for k in 'abcdef'])
    review = dict(year=2025, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingPracticeCardIds=[c['id'] for c in cards], legacyCardIds=legacy, readingWholeCardIds=legacy[:12],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 retained whole reading questions with 34 published parts and 14 independent answer/point slots; '
                             '4 retained prose, 4 poetry and 6 additional-literature routes.')
    return dict(review=review, cards=cards)


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
    print(f"Irish Higher 2025 Paper 2: {len(data['cards'])} added reading cards (+26 retained legacy cards); the archive remains incomplete.")


if __name__ == '__main__':
    main()
