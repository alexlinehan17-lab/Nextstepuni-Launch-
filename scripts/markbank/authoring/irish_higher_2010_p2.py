#!/usr/bin/env python3
"""Reviewed 2010 Higher Paper 2 (An Litríocht agus Stair na Gaeilge): new cards, no legacy component.

Before 2012 the Higher reading comprehension sits in Páipéar 1, so the 2010 Páipéar 2 (LC001ALP200IV, 180 marc) is all
literature and the history of the language: Ceist 1 Prós 40 (A Prós Ainmnithe or B Prós Roghnach, each (a) 25 and (b) 15),
Ceist 2 Próstéacs Breise 40 (one of A Gearrscéalta, B Úrscéalta, C Dírbheathaisnéisí, D Drámaí; within it (a) the named
text or (b) an optional one, each (i) or (ii)), Ceist 3 Filíocht 70 (A Filíocht Ainmnithe or B Filíocht Roghnach, 35, and C
Dánta Dualgais Breise, 35) and Ceist 4 Stair na Gaeilge 30 (two of (a)–(f)). Paper PDF 1–16 (1 cover, 2 the Treoracha,
3 Ceist 1, 4–7 Ceist 2, 8–10 Ceist 3A with the poems Jack, Níl Aon Ní and Faoiseamh a Gheobhadsa, 11 Ceist 3B, 12–14 Ceist 3C
with Úirchill an Chreagáin and An Chéad Dráma, 15 Ceist 4, 16 blank) and the Páipéar II pages of the combined LC001ALP000EV
scheme (PDF 14–18; named EV, printed in Irish) reviewed on 2026-11-05. Counts are assertions, not corpus-completeness proof.

The scheme restates each question briefly with its Eolas tariff ("Ionramháil Ábhair = 22 marc", "= 13 marc", "{ Ionramháil
Ábhair = 35 marc}", "(Jack) = 11 marc", "= 18 marc") and its Cumas Gaeilge award, and prints no supporting notes, band table or
grade table for Páipéar II: every judged answer is claimed whole at its printed price (no scale is printed for it). Where it
restates a sub-question's alternatives, each at that price ("(Lá Buí Bealtaine) Ionramháil Ábhair = 22 marc Nó … (Clare sa
Spéir) Ionramháil Ábhair = 22 marc Nó …"), each alternative is a row of its own and the one answered is claimed (tariffs.ts
reads them as printed alternatives). Ceist 1's Gaeilge is "(a) agus (b) le chéile = 5 marc"; Ceist 2's 5; Ceist 3's "(A nó B
agus C le chéile) = 10 marc" for the two routes together (the paper prints each route at 35, the scheme each route's Eolas at
30: the route card carries 5, its share of the 10, from those two printed numbers); Ceist 4 prints "13 + 12 (Eolas) móide 5
marc ar an gCumas Gaeilge (sa dá cheann le chéile) = 30 marc", its Eolas row stepped at that split (0, 12, 13, 25).

Cards (one per printed route; a printed choice inside a route is one card, as the options are marked alike and file under
one Atlas heading): Ceist 1 A and B; Ceist 2's eight routes A(a)–D(b), each "(i) nó (ii)"; Ceist 3 A, B and C; Ceist 4. Atlas
keys follow the 2010–2011 convention the crosswalk reads (P-A and F-A the prescribed prose and poetry, P-B and F-B the
optional; F-C the Dánta Dualgais Breise), with X-2A-a … X-2D-b and X-4 for the additional prose texts and Stair na Gaeilge,
as 2011's. Pre-2012 named texts have no Atlas nodes of their own: prose files under irish-4-7 (Prós: Ábhar Roghnach), poetry
under irish-5-6 (Filíocht: Ábhar Roghnach), the named additional texts A Thig Ná Tit Orm and An Triail under their nodes
(irish-6-1, irish-6-0), and Stair na Gaeilge under irish-7-0.

Glyph audit: the paper's SymbolMT dashes (U+F02D) flank the boxed section headings and print three dashes inside the poems
(Úirchill an Chreagáin, An Chéad Dráma); they are the Symbol encoding's minus sign (0x2D), read as U+2212. The scheme's
Páipéar II pages print no symbol-font span.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP200IV'
SCHEME_FILE = 'LC001ALP000EV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2010-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2010-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = 'c3ecba9e2accb4fffddac01ff59068ed2807d7bc616e35caa886138edfcc44f0'
SCHEME_SHA = 'e304dd29af73f46d972385ce1f625bce88a47a20010e63e2853c92ad3fbe0be5'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin|DHÁ', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
PAPER_GLYPHS = {(3, 'SymbolMT', ''): 4, (4, 'SymbolMT', ''): 2, (5, 'SymbolMT', ''): 2, (6, 'SymbolMT', ''): 2,
                (7, 'SymbolMT', ''): 2, (8, 'SymbolMT', ''): 2, (11, 'SymbolMT', ''): 2, (12, 'SymbolMT', ''): 3,
                (14, 'SymbolMT', ''): 2}


def clean(text):
    # The SymbolMT dashes (U+F02D) are the Symbol encoding's minus sign (0x2D), read as U+2212.
    return re.sub(r'\s+', ' ', symbol_text(text).replace('', '−')).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def criterion(id, label, marks, guidance, kind='indicative', permitted=None):
    return dict(id=id, label=label, kind='award', maxMarks=marks,
                permittedMarks=permitted if permitted is not None else [0, marks], guidanceKind=kind, guidance=guidance)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


def symbol_audit(doc, pages=None):
    audit = collections.Counter()
    for number, page in enumerate(doc, 1):
        if pages and number not in pages:
            continue
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    if span['font'].startswith(('Symbol', 'Wingdings')):
                        for char in span['chars']:
                            audit[(number, span['font'], char['c'])] += 1
    return dict(audit)


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
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2))}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)

    def page(self, number):
        return self.text.index(f'⟦{number}⟧')


LIT_REQUIREMENTS = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']

# Ceist 1. (key, slug, ref, paper prompt lines (a) then (b), scheme (a) start/end, (b) start/end)
PROSE = [
    ('P-A', 'prose-1a', 'Prós 1A · Prós Ainmnithe', 'A PRÓS AINMNITHE 40 marc', [
        '(a) Maidir leis an dráma Lá Buí Bealtaine, déan plé gairid ar an gcaoi a léirítear meon Nóirín Ní Chathasaigh agus Pheadair '
        'Mhic Fhlannchadha ann. (25 mharc)',
        'nó',
        'Maidir leis an scannán Clare sa Spéir, déan plé gairid ar do rogha dhá cheann de na gnéithe seo a leanas den scannán: (a) mar '
        'a d’athraigh iompar Eoin ó thús go deireadh an scannáin; (b) tábhacht na curiarrachta in imeachtaí an scannáin; (c) an greann '
        'sa scannán; (d) an úsáid a bhaintear as ceol sa scannán. (25 mharc)',
        'nó',
        '“Cé gur pearsa mhíthaitneamhach é An Cearrbhach Mac Cába, éiríonn leis bá an léitheora a choinneáil trína chuid scéiméireachta '
        'in aghaidh an Bháis.” An ráiteas sin a phlé. (25 mharc)',
        '(b) “Sa dírbheathaisnéis Fiche Blian ag Fás, tugtar léiriú spéisiúil ar eachtraí Mhuiris agus Thomáis agus ar an gceacht a '
        'd’fhoghlaim siad astu.” Déan plé gairid air sin. (15 mharc)',
        'nó',
        'Maidir leis an sliocht as an dírbheathaisnéis Fiche Blian ag Fás, déan plé gairid ar dhá thréith a bhaineann le Muiris ann. '
        '(15 mharc)'],
     ('(a) Mar a léirítear meon Nóirín', '(b) Léiriú spéisiúil'),
     ('(b) Léiriú spéisiúil', 'Cumas Gaeilge – (a) agus (b) le chéile')),
    ('P-B', 'prose-1b', 'Prós 1B · Prós Roghnach', 'B PRÓS ROGHNACH 40 marc', [
        '(a) Maidir le dráma roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar an gcaoi a léirítear meon na '
        'beirte príomhphearsan ann. (25 mharc)',
        'Ní mór teideal an dráma sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        'Maidir le scannán roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar dhá cheann de na gnéithe seo a '
        'leanas: (a) an suíomh is fearr leat ann agus an chaoi a gcuirtear le chéile é; (b) an radharc is fearr leat agus an modh a '
        'léirítear é; (c) an phearsa is fearr leat agus an chaoi a gcuirtear i láthair é/í; (d) cé chomh sásúil is atá críoch an '
        'scannáin. (25 mharc)',
        'Ní mór teideal an scannáin sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        'Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar dhá ghné den scéal sin a '
        'thaitin leat. (25 mharc)',
        'Ní mór teideal an scéil bhéaloidis sin a scríobh síos go cruinn.',
        '(b) Maidir leis an sliocht as an dírbheathaisnéis roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar cé '
        'chomh héifeachtach is atá an fhorbairt ar an bpríomhthéama ann. (15 mharc)',
        'Ní mór teideal na dírbheathaisnéise, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        'Maidir leis an sliocht as an dírbheathaisnéis roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar dhá '
        'thréith de chuid an údair ann. (15 mharc)',
        'Ní mór teideal na dírbheathaisnéise, mar aon le hainm an údair, a scríobh síos go cruinn.'],
     ('(a) An chaoi a léirítear meon na beirte', '(b) Plé ar an bhforbairt'),
     ('(b) Plé ar an bhforbairt', 'Cumas Gaeilge - (a) agus (b) le chéile')),
]

# Ceist 2: (key, slug, ref, topic, page, section heading, route heading, prompt lines)
EXTRA = [
    ('X-2A-a', 'extra-2a-a', 'Próstéacs 2A(a) · Scothscéalta', 'irish-4-7', 4, 'A GEARRSCÉALTA 40 marc', '(a) SCOTHSCÉALTA (40 marc)', [
        '(i) “I ngearrscéalta Phádraic Uí Chonaire, is minic a osclaíonn eachtra shuntasach croí agus aigne an duine ar a chás féin.”',
        'An ráiteas sin a phlé maidir le do rogha scéal amháin díobh seo a leanas: M’Fhile Caol Dubh; Anam an Easpaig; Ná Lig Sinn i '
        'gCathú; An Bhean ar Leag Dia Lámh uirthi.',
        'nó',
        '(ii) “Is in aigne agus i gcroí an duine is mó a tharlaíonn an choimhlint i ngearrscéalta Phádraic Uí Chonaire.”',
        'An ráiteas sin a phlé maidir le do rogha scéal amháin díobh seo a leanas: M’Fhile Caol Dubh; Teatrarc na Gaililí; Beirt Bhan '
        'Misniúil; Anam an Easpaig.']),
    ('X-2A-b', 'extra-2a-b', 'Próstéacs 2A(b) · Cnuasach gearrscéalta roghnach', 'irish-4-7', 4, 'A GEARRSCÉALTA 40 marc',
     '(b) CNUASACH GEARRSCÉALTA ROGHNACH (40 marc)', [
        '(i) “Is minic a thagann athrú nó forbairt ar phearsantacht na príomhphearsan in imeacht an scéil.”',
        'An ráiteas sin a phlé maidir le do rogha gearrscéal amháin as do chnuasach roghnach.',
        'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        '(ii) Maidir le gearrscéal ar bith as do chnuasach roghnach, déan plé ar thubaiste éigin i saol na príomhphearsan ann agus ar '
        'thionchar na tubaiste sin ar a s(h)aol.',
        'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn.']),
    ('X-2B-a', 'extra-2b-a', 'Próstéacs 2B(a) · Máire Nic Artáin', 'irish-4-7', 5, 'B ÚRSCÉALTA 40 marc', '(a) MÁIRE NIC ARTÁIN (40 marc)', [
        '(i) “Is éifeachtach an léiriú a dhéantar san úrscéal Máire Nic Artáin ar an tionchar a bhíonn ag an gné ghránna den saol ar '
        'aigne shoineanta an duine óig.”',
        'An ráiteas sin a phlé.',
        'nó',
        '(ii) “Is éifeachtach an léiriú a thugtar dúinn ar chúlra polaitiúil agus creidimh Bhéal Feirste agus ar an tionchar atá ag an '
        'gcúlra sin ar imeachtaí an úrscéil Máire Nic Artáin.”',
        'An ráiteas sin a phlé.']),
    ('X-2B-b', 'extra-2b-b', 'Próstéacs 2B(b) · Úrscéal roghnach', 'irish-4-7', 5, 'B ÚRSCÉALTA 40 marc', '(b) ÚRSCÉAL ROGHNACH (40 marc)', [
        '(i) Maidir leis an úrscéal roghnach a ndearna tú staidéar air, déan cur síos ar thréimhse áirithe i saol na príomhphearsan agus '
        'ar an tionchar atá ag an tréimhse sin ar a c(h)aidreamh le mórphearsa eile san úrscéal.',
        'Ní mór teideal an úrscéil, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        '(ii) Maidir leis an úrscéal roghnach a ndearna tú staidéar air, déan plé ar an tionchar a bhíonn ag eachtraí áirithe ar mhianta '
        'agus ar aislingí na príomhphearsan ann.',
        'Ní mór teideal an úrscéil, mar aon le hainm an údair, a scríobh síos go cruinn.']),
    ('X-2C-a', 'extra-2c-a', 'Próstéacs 2C(a) · A Thig Ná Tit Orm', 'irish-6-1', 6, 'C DÍRBHEATHAISNÉISÍ 40 marc', '(a) A THIG NÁ TIT ORM (40 marc)', [
        '(i) “In A Thig Ná Tit Orm faightear eolas mion ar shaol oibre agus sóisialta na nÉireannach in Chicago agus ar an gcoimhlint '
        'chiníoch ansin le linn an ama a chaith Maidhc Dainín ann.”',
        'Déan plé ar an ráiteas sin.',
        'nó',
        '(ii) “Tugtar léiriú maith sa dírbheathaisnéis seo ar an gcaoi ar fhás a ghrá don cheol i Maidhc Dainín agus ar an tairbhe a '
        'bhain sé as i rith a shaoil.”',
        'Déan plé ar an ráiteas sin.']),
    ('X-2C-b', 'extra-2c-b', 'Próstéacs 2C(b) · Dírbheathaisnéis roghnach', 'irish-4-7', 6, 'C DÍRBHEATHAISNÉISÍ 40 marc',
     '(b) DÍRBHEATHAISNÉIS ROGHNACH (40 marc)', [
        '(i) Maidir leis an dírbheathaisnéis roghnach a ndearna tú staidéar uirthi, déan cur síos ar an tionchar a bhí ag eachtraí áirithe '
        'ar shaol agus ar mheon an údair inti.',
        'Ní mór teideal na dírbheathaisnéise sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        '(ii) Maidir leis an dírbheathaisnéis roghnach a ndearna tú staidéar uirthi, déan cur síos ar an gcaidreamh a bhí ag an údar le '
        'beirt phearsan ina s(h)aol agus ar an tionchar a bhí ag na pearsana sin air/uirthi.',
        'Ní mór teideal na dírbheathaisnéise sin, mar aon le hainm an údair, a scríobh síos go cruinn.']),
    ('X-2D-a', 'extra-2d-a', 'Próstéacs 2D(a) · An Triail', 'irish-6-0', 7, 'D DRÁMAÍ 40 marc', '(a) AN TRIAIL (40 marc)', [
        '(i) “Fásann príomhchoimhlintí an dráma as lochtanna nó duáilcí daonna a cheiltear faoi chosúlacht an ghrá.”',
        'Déan plé ar an ráiteas sin agus tú ag tagairt don dráma An Triail.',
        'nó',
        '(ii) “Is iomaí teicníocht dhrámata a úsáidtear sa dráma An Triail chun forbairt a dhéanamh ar an bpríomhthéama.”',
        'Déan plé ar an ráiteas sin agus tú ag tagairt do dhá theicníocht dhrámata, ar a laghad.']),
    ('X-2D-b', 'extra-2d-b', 'Próstéacs 2D(b) · Dráma roghnach', 'irish-4-7', 7, 'D DRÁMAÍ 40 marc', '(b) DRÁMA ROGHNACH (40 marc)', [
        '(i) Maidir leis an dráma roghnach a ndearna tú staidéar air, déan plé ar an gcaidreamh atá ag an bpríomhphearsa le beirt '
        'phearsan eile sa dráma agus an tionchar a bhíonn ag an gcaidreamh sin ar imeachtaí an dráma.',
        'Ní mór teideal an dráma sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        '(ii) “Is iomaí teicníocht dhrámata a úsáidtear i ndráma chun forbairt a dhéanamh ar an bpríomhthéama ann.”',
        'Déan plé ar an ráiteas sin agus tú ag tagairt do dhá theicníocht dhrámata ar thug tú suntas dóibh sa dráma roghnach a ndearna '
        'tú staidéar air.',
        'Ní mór teideal an dráma sin, mar aon le hainm an údair, a scríobh síos go cruinn.']),
]

POEMS = {
    'F-A': ('poetry-3a', 'Filíocht 3A · Filíocht Ainmnithe', [8, 9, 10], 'A FILÍOCHT AINMNITHE 35 mharc', [
        'Freagair (a) atá thíos agus (b) atá thall ar leathanach 10.',
        '(a) (i) “Tá an pléisiúr agus an t-aiféala fite fuaite ina chéile i gcuimhní an fhile sa dán Jack (thíos).” Déan plé gairid ar '
        'an ráiteas sin. (12 mharc)',
        '(ii) Scríobh nóta gairid faoi éifeacht na húsáide a bhaineann an file as dhá cheann díobh seo a leanas: suíomh an dáin; an '
        't-atmaisféar; na híomhánna; an friotal. (8 marc)',
        'nó',
        '(i) “Cuireann na híomhánna go mór leis an gcodarsnacht sa dán Níl Aon Ní (thíos).” Déan plé gairid ar an ráiteas sin. (12 mharc)',
        '(ii) Scríobh nóta gairid faoi éifeacht na húsáide a bhaineann an file as dhá cheann díobh seo a leanas: dathanna; '
        'logainmneacha; uaim; an t-atmaisféar. (8 marc)',
        '(b) “Sa dán Faoiseamh a Gheobhadsa (thíos), tá codarsnacht láidir idir dhá ghné de shaol an fhile.” Déan plé gairid ar an '
        'ráiteas sin. (15 mharc)',
        'nó',
        'Maidir leis an dán Faoiseamh a Gheobhadsa, déan trácht gairid ar éifeacht na húsáide a bhaineann an file as dhá cheann díobh '
        'seo a leanas: an friotal; an t-atmaisféar; na híomhánna; na mothúcháin. (15 mharc)']),
    'F-B': ('poetry-3b', 'Filíocht 3B · Filíocht Roghnach', [11], 'B FILÍOCHT ROGHNACH 35 mharc', [
        'Freagair (a) agus (b).',
        '(a) (i) Maidir le dán nua-aimseartha a chum bean, agus a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar éifeacht '
        'na húsáide a bhaineann an file as dhá ghné díobh seo a leanas: (a) na híomhánna; (b) na mothúcháin; (c) an friotal; (d) forbairt '
        'an téama. (12 mharc)',
        '(ii) Luaigh an mothúchán is mó a mhúsclaíonn an dán ionat féin agus cuir fáth amháin le do rogha. (8 marc)',
        'Ní mór teideal an dáin, mar aon le hainm an fhile, a scríobh síos go cruinn.',
        'nó',
        '(i) Maidir le dán nua-aimseartha a chum fear, agus a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar an dá '
        'theicníocht is éifeachtaí a úsáideann an file chun príomhthéama an dáin a fhorbairt. (12 mharc)',
        '(ii) Déan plé gairid ar an gcaoi a ndeachaigh an dán seo i bhfeidhm ort féin. (8 marc)',
        'Ní mór teideal an dáin, mar aon le hainm an fhile, a scríobh síos go cruinn.',
        '(b) (i) Maidir le dán nua-aimseartha a chum bean, agus a ndearna tú staidéar air le linn do chúrsa, agus nár úsáid tú i gcuid '
        '(a) thuas, déan plé gairid ar phríomhthéama an dáin agus ar an gcaoi a léirítear an príomhthéama sa dán. (15 mharc)',
        'Ní mór teideal an dáin, mar aon le hainm an fhile, a scríobh síos go cruinn.',
        'nó',
        '(ii) Maidir le dán nua-aimseartha a chum fear agus a ndearna tú staidéar air le linn do chúrsa, agus nár úsáid tú i gcuid (a) '
        'thuas, déan plé gairid ar do rogha dhá cheann de na gnéithe seo: (a) cúlra an dáin; (b) dearcadh an fhile mar a léirítear sa '
        'dán é; (c) an mheadaracht; (d) an friotal. (15 mharc)',
        'Ní mór teideal an dáin, mar aon le hainm an fhile, a scríobh síos go cruinn.']),
    # The question quotes the poem's last verse as "domh" and "fán tSeanainn"; the poem (PDF 13) prints "damh" and "fan". The card
    # shows the question's words.
    'F-C': ('poetry-3c', 'Filíocht 3C · Dánta Dualgais Breise', [12, 13, 14], 'C DÁNTA DUALGAIS BREISE 35 mharc', [
        'Freagair (a) nó (b).',
        '(a) Freagair (i), (ii) agus (iii) thíos.',
        '(i) “Sa dán Úirchill a’ Chreagáin tá an t-eolas ar chás an fhile agus ar chás na tíre ar na rudaí is suntasaí ann.”',
        'An ráiteas sin a phlé maidir leis an dán thíos. (20 marc)',
        '(ii) Mínigh na línte seo:',
        '‘A ríoghain deas mhilis, más cinniúin domh tú féin mar stór,',
        'tabhair léagsa is gealladh domh sul fá n-aistre mé leat siar sa ród,',
        'má éagaim fán tSeanainn, i gcrích Mhanainn nó san Éiphte mhór',
        'gurb i gcill chumhra an Chreagáin a leagfar mé i gcré faoi fhód.’',
        '(6 mharc)',
        '(iii) Scríobh nóta ar mheadaracht an dáin agus léirigh í le do rogha véarsa as. (9 marc)',
        'nó',
        '(b) Freagair (i), (ii) agus (iii) thíos.',
        '(i) “Cé gur dán fáthchiallach ar an saol é An Chéad Dráma tá cás an fhile chun tosaigh ann.”',
        'An ráiteas sin a phlé. (20 marc)',
        '(ii) Mínigh na línte seo:',
        '‘Tá mo pháirt-se ar tí a bheith thart',
        'Ach ní raibh na focla a’am i gceart',
        'Thar fóir sa ngluaiseacht is ó smacht',
        'Ach tá na torthaí fós le theacht',
        'Chaill mé marcannaí.’',
        '(6 mharc)',
        '(iii) Scríobh nóta ar an úsáid a bhaintear sa dán as dhá cheann díobh seo a leanas: uaim agus comhuaim; comhardadh; an rithim; '
        'an friotal. (9 marc)']),
}
STAIR = ['Scríobh gearrchuntas ar DHÁ CHEANN díobh seo a leanas.',
         'I gcás (a) agus (b) is pointí gearra eolais atá á lorg.',
         'I gcás (c), (d), (e) agus (f) tá pointí níos faide á lorg.',
         '(a) Do rogha beirt díobh seo a leanas:',
         'Breandán Ó hEithir', 'Pádraig Mac Piarais', 'Peig Sayers', 'Biddy Jenkinson', 'Nuala Ní Dhomhnaill', 'Seathrún Céitinn',
         'Deirdre Brennan', 'Seán Ó Coisdealbha',
         '[Ní mór saol agus saothar gach duine díobh a lua.]',
         '(b) Do rogha dhá cheann díobh seo a leanas:',
         'An tSean-Ghaeilge; na gluaiseanna; logainmneacha na hÉireann; na Gaeltachtaí.',
         '(c) Scríbhneoirí Choláiste Lováin sa 17ú haois.', '[Is leor trí mhórphointe.]',
         '(d) Béaloideas na Gaeilge.', '[Is leor trí mhórphointe.]',
         '(e) Meath na Gaeilge sa naoú haois déag.', '[Is leor trí mhórphointe.]',
         '(f) Príomhchanúintí na Gaeilge.', '[Is leor trí mhórphointe.]']


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2010/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2010/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    assert symbol_audit(paper) == PAPER_GLYPHS and symbol_audit(doc, range(14, 19)) == {}, 'Symbol glyphs changed: repeat the glyph review'
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 14, 18)
    return dict(paper=paper, texts=texts, s=s, decisions=selection_decisions(paper))


def build():
    m = material()
    texts, s = m['texts'], m['s']
    cards = []

    def page_has(lines, pages):
        joined = comparable(' '.join(texts[p - 1] for p in pages))
        for line in lines:
            assert comparable(line) in joined, (pages, line[:60])

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, note, source, stem=None):
        cards.append(dict(
            id=f'irish-2010-hl-p2-{slug}', year=2010, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2010 HL Paper 2 {ref}', questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic, conceptId=f'irish-hl-p2-{slug}',
            paperFileid=FILE, schemeFileid=SCHEME_FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            reviewedAt=REVIEWED_AT, reviewedPaperPages=pages, taskRequirements=LIT_REQUIREMENTS, criteria=criteria,
            markingGuideNote=note,
            sourceMaterial=dict(kind='source-text', label=source[0], title=source[1], pages=pages,
                                attribution='© State Examinations Commission.', presentationNote=SOURCE_NOTE),
            **({'stem': stem} if stem else {})))
        return cards[-1]

    # ---- Ceist 1: Prós -------------------------------------------------------------------------------------------------
    head1 = 'Ceist 1\nPRÓS 40 MARC\nFreagair A (Prós Ainmnithe) nó B (Prós Roghnach) anseo thíos.'
    page_has(head1.splitlines(), [3])
    gaeilge1, g1pages = s.chunk('Cumas Gaeilge - (a) agus (b) le chéile', 'Ceist 2 -', s.page(15))
    assert gaeilge1.startswith('Cumas Gaeilge - (a) agus (b) le chéile = 5 marc C. 1 (A) nó (B) = 40 marc (22 + 13 + 5) Nóta:'), gaeilge1[:120]
    assert gaeilge1.endswith('bainfear marcanna mura luaitear iad.') and g1pages == [15], gaeilge1[-60:]
    gaeilge1a, _ = s.chunk('Cumas Gaeilge – (a) agus (b) le chéile', 'B - PRÓS ROGHNACH', s.page(14))
    assert gaeilge1a == 'Cumas Gaeilge – (a) agus (b) le chéile = 5 marc', gaeilge1a
    for key, slug, ref, heading, lines, (a_start, a_end), (b_start, b_end) in PROSE:
        page_has([heading, 'Freagair (a) agus (b).', *[line for line in lines if line != 'nó']], [3])
        part_a, a_pages = s.chunk(a_start, a_end, s.page(14))
        part_b, b_pages = s.chunk(b_start, b_end, s.page(14))
        assert part_a.count('= 22 marc') == part_a.lower().count('ionramháil ábhair = 22 marc') == 3, part_a
        assert part_b.count('= 13 marc') == 2, part_b
        gaeilge_lines = [gaeilge1a, gaeilge1] if key == 'P-A' else [gaeilge1]
        prompt = f'{heading}\nFreagair (a) agus (b).\n' + '\n'.join(lines)
        add(key, slug, ref, prompt, 'irish-4-7', [3], sorted(set(a_pages) | set(b_pages) | {15}),
            [criterion('eolas-a', '(a) Ionramháil Ábhair', 22, [part_a]), criterion('eolas-b', '(b) Ionramháil Ábhair', 13, [part_b]),
             criterion('gaeilge', 'Cumas Gaeilge', 5, gaeilge_lines, 'quality', list(range(6)))],
            'One complete SEC response: (a) Ionramháil Ábhair 22 and (b) Ionramháil Ábhair 13, each judged as a whole, and one shared '
            '5-mark Cumas Gaeilge award for (a) and (b) together. The paper prints (a) at 25 and (b) at 15; the scheme prints Eolas 22 + 13 '
            '+ Gaeilge 5. Each printed alternative of (a) and of (b) is one route of this card (marked alike, one Atlas heading). The '
            'scheme prints no notes, band table or grade table for Páipéar II, so each judged answer is claimed whole.'
            + (' The scheme deducts marks where the title and author are not given; it awards none for giving them.' if key == 'P-B' else ''),
            ('Prós', ref.split(' · ', 1)[1]), stem=head1)

    # ---- Ceist 2: Próstéacs Breise -------------------------------------------------------------------------------------
    head2 = ('Ceist 2\nPRÓSTÉACS BREISE 40 MARC\nFreagair do rogha CEANN AMHÁIN AS A nó B nó C nó D ar na leathanaigh 4 (thíos) agus 5, 6, 7 (thall).')
    page_has(head2.splitlines(), [4])
    rule2, r2pages = s.chunk('Ceist 2 - PRÓSTÉACS BREISE - 40 marc', 'CEIST 3 - FILÍOCHT', s.page(16))
    assert rule2.endswith('a thaispeáint go soiléir san ionad cuí ar an bhfreagarleabhar.') and r2pages == [16], rule2
    # The Eolas criterion reads its own price, as printed inside the braces; the selection line before it is the Gaeilge
    # criterion's, with the rest of the rule.
    eolas2 = 'Ionramháil Ábhair = 35 marc'
    assert rule2.count('{ Ionramháil Ábhair = 35 marc}') == 1 and rule2.count('{ Cumas Gaeilge = 5 marc}') == 1, rule2
    for key, slug, ref, topic, page, section, route, lines in EXTRA:
        page_has([section, 'Freagair (a) nó (b).', route, *[line for line in lines if line != 'nó']], [page])
        prompt = f'{section}\nFreagair (a) nó (b).\n{route}\n' + '\n'.join(lines)
        add(key, slug, ref, prompt, topic, [page], r2pages,
            [criterion('eolas', 'Ionramháil Ábhair', 35, [eolas2]), criterion('gaeilge', 'Cumas Gaeilge', 5, [rule2], 'quality', list(range(6)))],
            'One complete SEC response: Ionramháil Ábhair 35, judged as a whole, and Cumas Gaeilge 5 (scheme PDF 16). (i) and (ii) are the '
            'printed alternatives of this route, marked alike. The scheme prints no notes, band table or grade table for Ceist 2, so the '
            'answer is claimed whole.', ('Próstéacs Breise', ref.split(' · ', 1)[1]), stem=head2)

    # ---- Ceist 3: Filíocht -------------------------------------------------------------------------------------------------
    head3 = ('Ceist 3\nFILÍOCHT 70 MARC\nFreagair A (Filíocht Ainmnithe) ar na leathanaigh 8, 9 agus 10 nó B (Filíocht Roghnach) ar leathanach 11 '
             'agus freagair C (Dánta Dualgais Breise) ar na leathanaigh 12, 13 agus 14.')
    page_has(head3.splitlines(), [8])
    gaeilge3, g3pages = s.chunk('Cumas Gaeilge (A nó B agus C le chéile)', 'Ceist 4 - STAIR', s.page(18))
    assert gaeilge3.startswith('Cumas Gaeilge (A nó B agus C le chéile) = 10 marc Nóta:') and gaeilge3.endswith('ar an bhfreagarleabhar.'), gaeilge3
    # Each route's scheme text, cut at its sub-questions (the scheme's "(i)"/"(ii)"/"(iii)" restatements and their prices).
    a_i = [s.chunk('(a) (i) Pléisiúr agus aiféala', '(ii) Plé ar dhá cheann díobh seo: suíomh', s.page(16))[0],
           s.chunk('Nó (i) Mar a chuireann na híomhánna', '(ii) Plé ar dhá cheann de : dathanna', s.page(16))[0]]
    a_ii = [s.chunk('(ii) Plé ar dhá cheann díobh seo: suíomh', 'Nó (i) Mar a chuireann', s.page(16))[0],
            s.chunk('(ii) Plé ar dhá cheann de : dathanna', '(b) (i) Plé ar chodarsnacht', s.page(16))[0]]
    a_b = s.chunk('(b) (i) Plé ar chodarsnacht', 'B - FILÍOCHT ROGHNACH', s.page(16))[0]
    assert [x[-9:] for x in a_i] == ['= 11 marc'] * 2 and [x[-8:] for x in a_ii] == ['= 6 marc'] * 2, (a_i, a_ii)
    assert a_b.endswith('(Faoiseamh a Gheobhadsa) = 13 marc'), a_b
    b_i = [s.chunk('(a) (i) Plé ar éifeacht na húsáide', '(ii) An mothúchán is mó', s.page(17))[0],
           s.chunk('Nó (i) An dá theicníocht', '(ii) Plé ar an gcaoi a ndeachaigh', s.page(17))[0]]
    b_ii = [s.chunk('(ii) An mothúchán is mó', 'Nó (i) An dá theicníocht', s.page(17))[0],
            s.chunk('(ii) Plé ar an gcaoi a ndeachaigh', '(b) (i) Plé ar an bpríomhthéama', s.page(17))[0]]
    b_b = s.chunk('(b) (i) Plé ar an bpríomhthéama', 'Ní bhronnfar marcanna ar theidil', s.page(17))[0]
    titles3b = s.chunk('Ní bhronnfar marcanna ar theidil', '⟦18⟧', s.page(17))[0]
    c_i = [s.chunk('(a) Úirchill a’ Chreagáin (i)', '(ii) Mínigh na línte. = 4', s.page(18))[0],
           s.chunk('(b) An Chéad Dráma (i)', '(ii) Mínigh na línte = 4', s.page(18))[0]]
    c_ii = [s.chunk('(ii) Mínigh na línte. = 4', '(iii) Nóta ar mheadaracht', s.page(18))[0],
            s.chunk('(ii) Mínigh na línte = 4', '(iii) Nóta ar an úsáid', s.page(18))[0]]
    c_iii = [s.chunk('(iii) Nóta ar mheadaracht', '(b) An Chéad Dráma', s.page(18))[0],
             s.chunk('(iii) Nóta ar an úsáid', 'Cumas Gaeilge (A nó B', s.page(18))[0]]
    for group, mark in [(b_i, 11), (c_i, 18), (c_ii, 4), (c_iii, 8)]:
        assert all(re.search(rf'=\s*{mark} marc', x) for x in group), (group, mark)
    assert all(re.search(r'= 6 marc', x) for x in b_ii) and b_b.count('= 13 marc') == 2 and a_b.count('= 13 marc') == 2
    assert titles3b == 'Ní bhronnfar marcanna ar theidil/ainmneacha údar a lua ach bainfear marcanna mura luaitear iad.', titles3b
    routes3 = {
        'F-A': [('eolas-a-i', '(a)(i) Eolas', 11, a_i), ('eolas-a-ii', '(a)(ii) Eolas', 6, a_ii), ('eolas-b', '(b) Eolas', 13, [a_b])],
        'F-B': [('eolas-a-i', '(a)(i) Eolas', 11, b_i), ('eolas-a-ii', '(a)(ii) Eolas', 6, b_ii), ('eolas-b', '(b) Eolas', 13, [b_b, titles3b])],
        'F-C': [('eolas-i', '(i) Eolas', 18, c_i), ('eolas-ii', '(ii) Eolas', 4, c_ii), ('eolas-iii', '(iii) Eolas', 8, c_iii)],
    }
    scheme_pages3 = {'F-A': [16, 18], 'F-B': [17, 18], 'F-C': [18]}
    for key, (slug, ref, pages, heading, lines) in POEMS.items():
        page_has([heading, *[line for line in lines if line != 'nó']], pages)
        prompt = f'{heading}\n' + '\n'.join(lines)
        crits = [criterion(cid, label, marks, guidance) for cid, label, marks, guidance in routes3[key]]
        crits.append(criterion('gaeilge', 'Cumas Gaeilge', 5, [gaeilge3], 'quality', list(range(6))))
        add(key, slug, ref, prompt, 'irish-5-6', pages, scheme_pages3[key],
            crits,
            'One complete SEC response to this route of Ceist 3. The paper prints the route at 35; the scheme prints its Eolas at '
            + ('11 + 6 + 13 = 30' if key != 'F-C' else '18 + 4 + 8 = 30')
            + ' (the paper prints the sub-questions at ' + ('12, 8 and 15' if key != 'F-C' else '20, 6 and 9') + ' with their Irish) and one '
            'Cumas Gaeilge award of 10 for the two routes of Ceist 3 together (A or B, and C): this card carries 5, the route’s share '
            '(its printed 35 less its printed Eolas 30). Each printed alternative is one route of this card, marked alike. The scheme '
            'prints no notes, band table or grade table for Ceist 3, so each judged answer is claimed whole.'
            + (' The scheme deducts marks where the title and poet are not given; it awards none for giving them.' if key == 'F-B' else ''),
            ('Filíocht', ref.split(' · ', 1)[1]), stem=head3)

    # ---- Ceist 4: Stair na Gaeilge -------------------------------------------------------------------------------------
    head4 = 'Ceist 4\nSTAIR NA GAEILGE 30 MARC'
    page_has([*head4.splitlines(), *STAIR], [15])
    stair, spages = s.chunk('Ceist 4 - STAIR - 30 marc', None, s.page(18))
    assert stair.startswith('Ceist 4 - STAIR - 30 marc Dhá cheann le déanamh as (a), (b), (c), (d), (e), (f). 13 + 12 (Eolas) móide 5 marc')
    assert stair.endswith('a thaispeáint go soiléir san ionad cuí ar an bhfreagarleabhar.') and spages == [18], stair[-80:]
    # The Eolas criterion reads the two answers' split and what the scheme asks of each option; the "= 30 marc" that totals the
    # question with its Gaeilge is the Gaeilge criterion's, with the whole rule.
    split4 = 'Dhá cheann le déanamh as (a), (b), (c), (d), (e), (f). 13 + 12 (Eolas) móide 5 marc ar an gCumas Gaeilge (sa dá cheann le chéile)'
    rest4 = stair[stair.index('= 30 marc. ') + len('= 30 marc. '):]
    assert split4 in stair and rest4.startswith('I gcás (a) agus (b) tá cuntas le scríobh ar dhá cheann;'), rest4[:60]
    add('X-4', 'history-4', 'Stair na Gaeilge 4', head4 + '\n' + '\n'.join(STAIR), 'irish-7-0', [15], [18],
        [criterion('eolas', 'Eolas', 25, [split4, rest4]), criterion('gaeilge', 'Cumas Gaeilge', 5, [stair], 'quality', list(range(6)))],
        'One complete SEC response: two of (a)–(f), Eolas 13 for one and 12 for the other (25, the scheme’s “an marc a bhronntar as 25 '
        '(Eolas)”) and Cumas Gaeilge 5 for the two together. Each printed option is one choice inside this card. The scheme prints no '
        'answer for Ceist 4 and no scale: the Eolas steps only at its printed split, 12 or 13 for one answer and 25 for both.', ('Stair na Gaeilge', 'Ceist 4'))

    assert len(cards) == 14 and len({c['id'] for c in cards}) == 14 and len({c['atlasQuestionId'] for c in cards}) == 14
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'] in ('P-A', 'X-2A-a', 'F-A', 'F-C', 'X-4')) == 180
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-\xad]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2010, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=[], literatureRouteCardIds=[c['id'] for c in cards],
                  examStructure=dict(prose=40, additionalProse=40, poetry=70, history=30, total=180),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='14 route cards: Ceist 1 A and B; Ceist 2 A(a)–D(b), each (i) nó (ii); Ceist 3 A, B and C; Ceist 4 (two of (a)–(f)). '
                             '50 printed asks, each a printed alternative inside one of them.')
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance carries the SEC's words only; question and task checks the paper's (irish_lifted.py)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Higher 2010 Paper 2: {len(data['cards'])} reviewed literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
