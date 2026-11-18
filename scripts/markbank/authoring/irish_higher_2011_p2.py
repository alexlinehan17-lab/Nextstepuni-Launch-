#!/usr/bin/env python3
"""Reviewed 2011 Higher Paper 2 (An Litríocht agus Stair na Gaeilge): new cards, no legacy component.

Before 2012 the Higher reading comprehension sits in Páipéar 1, so the 2011 Páipéar 2 (LC001ALP200IV, 180 marc) is all
literature and the history of the language: Ceist 1 Prós 40 (A Prós Ainmnithe or B Prós Roghnach, each (a) 25 and (b) 15),
Ceist 2 Próstéacs Breise 40 (one of A Gearrscéalta, B Úrscéalta, C Dírbheathaisnéisí, D Drámaí; within it (a) the named
text or (b) an optional one, each (i) or (ii)), Ceist 3 Filíocht 70 (A Filíocht Ainmnithe or B Filíocht Roghnach, 35, and C
Dánta Dualgais Breise, 35) and Ceist 4 Stair na Gaeilge 30 (two of (a)–(f)). Paper PDF 1–16 (1 cover, 2 the Treoracha,
3 Ceist 1, 4–7 Ceist 2, 8–10 Ceist 3A with the poems Jack, Bímse Buan ar Buairt Gach Ló and Gealt?, 11 Ceist 3B, 12–13 Ceist 3C
with Oíche Nollaig na mBan and Dán do Mhelissa, 14 Ceist 4, 15–16 blank) and the Páipéar II pages of the combined
LC001ALP000IV scheme (PDF 15–19) reviewed on 2026-11-05. Counts are assertions, not corpus-completeness proof.

The scheme restates each question briefly with its Eolas tariff ("Ionramháil Ábhair = 22 marc", "= 13 marc", "{ Ionramháil
Ábhair = 35 marc}", "(Jack) = 11 marc", "= 18 marc") and its Cumas Gaeilge award, and prints no supporting notes, band table or
grade table for Páipéar II: every judged answer is claimed whole at its printed price (coordinator rulings 2 and 4: no scale is
printed for it). Where it restates a sub-question's alternatives, each at that price ("(An Bhean Óg) Ionramháil Ábhair = 22
marc Nó … (Coilleach Ghleann Phádraig) Ionramháil Ábhair = 22 marc Nó …"), each alternative is a row of its own and the one
answered is claimed (tariffs.ts reads them as printed alternatives). Ceist 1's Gaeilge is "(a) agus (b) le chéile = 5 marc";
Ceist 2's 5; Ceist 3's "(A nó B agus C le chéile) = 10 marc" for the two routes together (the paper prints each route at 35,
the scheme each route's Eolas at 30: the route card carries 5, its share of the 10, from those two printed numbers); Ceist 4
prints "13 + 12 (Eolas) móide 5 marc ar an gCumas Gaeilge (sa dá cheann le chéile) = 30 marc", its Eolas row stepped at that
split (0, 12, 13, 25).

Cards (one per printed route; a printed choice inside a route is one card, coordinator ruling and BRIEF rule 5, as the
options are marked alike and file under one Atlas heading): Ceist 1 A and B; Ceist 2's eight routes A(a)–D(b), each
"(i) nó (ii)"; Ceist 3 A, B and C; Ceist 4. Atlas keys follow the 2010–2011 convention the crosswalk reads (P-A and F-A the
prescribed prose and poetry, P-B and F-B the optional; F-C the Dánta Dualgais Breise), with X-2A-a … X-2D-b and X-4 for the
additional prose texts and Stair na Gaeilge, as 2012's Litríocht Bhreise X-4A …. Pre-2012 named texts have no Atlas nodes of their own: prose files under
irish-4-7 (Prós: Ábhar Roghnach), poetry under irish-5-6 (Filíocht: Ábhar Roghnach), the named additional texts A Thig Ná Tit
Orm and An Triail under their nodes (irish-6-1, irish-6-0), and Stair na Gaeilge under irish-7-0.

Glyph audit: the paper's SymbolMT dashes (U+F02D) flank the boxed section headings only; no card reads them, and the two
selection lines that do (the B headings of Ceist 1 and 3) read them as the Symbol encoding's minus sign (U+2212). The
scheme's Páipéar II pages print no symbol-font span.
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
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2011-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2011-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '6e23d97e53e1545e79b77aa86ae869dd266bb06ac4f0cc2a879537d014f9371b'
SCHEME_SHA = 'b5f7c77e673759308a08e4a8cdef08000045789921a3c64278c739bb510783b0'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin|DHÁ', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
PAPER_GLYPHS = {(3, 'SymbolMT', ''): 4, (4, 'SymbolMT', ''): 2, (5, 'SymbolMT', ''): 2, (6, 'SymbolMT', ''): 2,
                (7, 'SymbolMT', ''): 2, (8, 'SymbolMT', ''): 2, (11, 'SymbolMT', ''): 2, (12, 'SymbolMT', ''): 2}


def clean(text):
    # The boxed headings' SymbolMT dashes (U+F02D) are the Symbol encoding's minus sign (0x2D), read as U+2212.
    return re.sub(r'\s+', ' ', symbol_text(text).replace('\uf02d', '\u2212')).strip()


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
TITLE_REQUIREMENT = 'Ní mór teideal an téacs, mar aon le hainm an údair, a scríobh síos go cruinn.'

# Ceist 1. (key, slug, ref, paper prompt lines (a) then (b), scheme (a) start/end, (b) start/end)
PROSE = [
    ('P-A', 'prose-1a', 'Prós 1A · Prós Ainmnithe', 'A PRÓS AINMNITHE 40 marc', [
        '(a) Maidir leis an ngearrscéal An Bhean Óg, déan plé gairid ar do rogha dhá cheann de na gnéithe seo a leanas den scéal: '
        '(i) an caidreamh idir an bhean óg agus a páistí; (ii) an modh inste; (iii) tréithe na mná óige; (iv) an t-atmaisféar i rith an scéil. (25 mharc)',
        'nó',
        'Maidir leis an ngearrscéal Coileach Ghleann Phádraig, déan plé gairid ar do rogha dhá cheann de na gnéithe seo a leanas den scéal: '
        '(i) páirt Sally Tom sa scéal; (ii) tréithe an tréidlia; (iii) tréithe mhuintir Ghleann Phádraig; (iv) an greann sa scéal. (25 mharc)',
        'nó',
        '‘Sa sliocht as an úrscéal Lig Sinn i gCathú faighimid léargas suimiúil ar choimhlintí idir na pearsana ann.’ '
        'Déan plé gairid ar dhá choimhlint a léirítear sa sliocht. (25 mharc)',
        '(b) ‘Is deacair trua a bheith againn don Chearrbhach sa scéal béaloidis An Cearrbhach Mac Cába.’ Déan plé gairid air sin. (15 mharc)',
        'nó',
        'Maidir leis an scéal béaloidis An Cearrbhach Mac Cába, scríobh nóta gairid ar dhá cheann díobh seo a leanas i gcomhthéacs an scéil: '
        'An t-osnádúr; an áibhéil; an greann; an tsaint. (15 mharc)'],
     ('(a) Dhá cheann de na gnéithe seo a leanas a phlé: (a) caidreamh', '(b) Plé ar thrua a bheith'),
     ('(b) Plé ar thrua a bheith', 'Cumas Gaeilge – (a) agus (b) le chéile')),
    ('P-B', 'prose-1b', 'Prós 1B · Prós Roghnach', 'B PRÓS ROGHNACH 40 marc', [
        '(a) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar chaidreamh na príomhphearsan '
        'le mórphearsa eile sa scéal. (25 mharc)',
        'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        'Maidir le sliocht as úrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar an dá ghné den sliocht '
        'is mó a chuaigh i bhfeidhm ort. (25 mharc)',
        'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        '(b) Maidir leis an scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid air mar shampla den '
        'chineál sin litríochta. (15 mharc)',
        'Ní mór teideal an scéil bhéaloidis a scríobh síos go cruinn.',
        'nó',
        'Maidir leis an scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, déan plé gairid ar dhá cheann díobh seo '
        'i gcomhthéacs an scéil: An t-osnádúr; an áibhéil; an greann; an tsaint. (15 mharc)',
        'Ní mór teideal an scéil bhéaloidis a scríobh síos go cruinn.'],
     ('(a) Plé ar chaidreamh idir beirt', '(b) Plé ar an scéal seo mar shampla'),
     ('(b) Plé ar an scéal seo mar shampla', 'Cumas Gaeilge - (a) agus (b) le chéile')),
]

# Ceist 2: (key, slug, ref, topic, page, section heading, route heading, prompt lines)
EXTRA = [
    ('X-2A-a', 'extra-2a-a', 'Próstéacs 2A(a) · Scothscéalta', 'irish-4-7', 4, 'A GEARRSCÉALTA 40 marc', '(a) SCOTHSCÉALTA (40 marc)', [
        '(i) ‘I ngearrscéalta Phádraic Uí Chonaire, is minic a bhíonn an bhean ag fulaingt ag lámha na bhfear.’',
        'An ráiteas sin a phlé maidir le do rogha scéal amháin díobh seo a leanas: Neil; An Bhean a Ciapadh; Nóra Mharcais Bhig; Teatrarc na Gaililí.',
        'nó',
        '(ii) ‘Bíonn an pholaitíocht agus cás an duine aonair fite fuaite ina chéile i ngearrscéalta Phádraic Uí Chonaire.’',
        'An ráiteas sin a phlé maidir le do rogha scéal amháin díobh seo a leanas: M’Fhile Caol Dubh; Beirt Bhan Misniúil; Anam an Easpaig.']),
    ('X-2A-b', 'extra-2a-b', 'Próstéacs 2A(b) · Cnuasach gearrscéalta roghnach', 'irish-4-7', 4, 'A GEARRSCÉALTA 40 marc',
     '(b) CNUASACH GEARRSCÉALTA ROGHNACH (40 marc)', [
        '(i) Maidir le gearrscéal ar bith as do chnuasach roghnach, déan plé ar an gcaoi a gcuireann an choimhlint in aigne na '
        'príomhphearsan le forbairt an ghearrscéil.',
        'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        '(ii) Maidir le gearrscéal ar bith as do chnuasach roghnach, déan plé ar do rogha dhá cheann díobh seo a leanas: '
        '(i) príomhthéama an scéil; (ii) príomhphearsa an scéil; (iii) buaicphointe an scéil; (iv) críoch an scéil.',
        'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn.']),
    ('X-2B-a', 'extra-2b-a', 'Próstéacs 2B(a) · Máire Nic Artáin', 'irish-4-7', 5, 'B ÚRSCÉALTA 40 marc', '(a) MÁIRE NIC ARTÁIN (40 marc)', [
        '(i) Déan an t-úrscéal Máire Nic Artáin a phlé i gcás do rogha dhá cheann díobh seo a leanas: (i) dhá shuíomh sa scéal; '
        '(ii) forbairt an phlota; (iii) an eachtra is mó a chuireann casadh cinniúnach sa scéal; (iv) an ghné den úrscéal is mó a thaitin leat.',
        'nó',
        '(ii) ‘Ceann de na gnéithe is spéisiúla san úrscéal Máire Nic Artáin is ea an chodarsnacht idir óige shona Mháire i gContae '
        'an Dúin agus a saol achrannach i mBéal Feirste.’',
        'An ráiteas sin a phlé.']),
    ('X-2B-b', 'extra-2b-b', 'Próstéacs 2B(b) · Úrscéal roghnach', 'irish-4-7', 5, 'B ÚRSCÉALTA 40 marc', '(b) ÚRSCÉAL ROGHNACH (40 marc)', [
        '(i) Maidir leis an úrscéal roghnach a ndearna tú staidéar air, déan an t-úrscéal a phlé i gcás do rogha dhá cheann díobh seo '
        'a leanas: (i) dhá shuíomh sa scéal; (ii) forbairt an phlota; (iii) an eachtra is mó a chuireann casadh cinniúnach sa scéal; '
        '(iv) an ghné den úrscéal is mó a thaitin leat.',
        'Ní mór teideal an úrscéil, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        '(ii) Maidir leis an úrscéal roghnach a ndearna tú staidéar air, déan plé ar an tionchar a bhíonn ag beirt de na mionphearsana '
        'ar imeachtaí an scéil.',
        'Ní mór teideal an úrscéil, mar aon le hainm an údair, a scríobh síos go cruinn.']),
    ('X-2C-a', 'extra-2c-a', 'Próstéacs 2C(a) · A Thig Ná Tit Orm', 'irish-6-1', 6, 'C DÍRBHEATHAISNÉISÍ 40 marc', '(a) A THIG NÁ TIT ORM (40 marc)', [
        '(i) ‘Is le súil ghéar agus le greann a thugann Maidhc Dainín cuntas ina dhírbheathaisnéis A Thig Ná Tit Orm ar na daoine '
        'ar bhuail sé leo agus é ar imirce i Sasana.’',
        'Déan plé ar an ráiteas sin.',
        'nó',
        '(ii) Maidir leis an leabhar A Thig Ná Tit Orm, déan plé gairid ar dhá cheann de na gnéithe seo a leanas: (i) cúrsaí oideachais '
        'le linn óige an údair; (ii) caitheamh aimsire na Gaeltachta agus an t-údar ag fás aníos ann; (iii) an imirce; (iv) an ciníochas i Meiriceá.']),
    ('X-2C-b', 'extra-2c-b', 'Próstéacs 2C(b) · Dírbheathaisnéis roghnach', 'irish-4-7', 6, 'C DÍRBHEATHAISNÉISÍ 40 marc',
     '(b) DÍRBHEATHAISNÉIS ROGHNACH (40 marc)', [
        '(i) Maidir leis an dírbheathaisnéis roghnach a ndearna tú staidéar uirthi, déan plé ar an léiriú a dhéanann an t-údar inti '
        'ar na daoine ar bhuail sé/sí leo i rith tréimhse áirithe dá s(h)aol.',
        'Ní mór teideal na dírbheathaisnéise sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        '(ii) Maidir leis an dírbheathaisnéis roghnach a ndearna tú staidéar uirthi, déan plé gairid ar an léiriú a dhéanann an t-údar '
        'ar an saol mar a bhí le linn a (h)óige.',
        'Ní mór teideal na dírbheathaisnéise sin, mar aon le hainm an údair, a scríobh síos go cruinn.']),
    ('X-2D-a', 'extra-2d-a', 'Próstéacs 2D(a) · An Triail', 'irish-6-0', 7, 'D DRÁMAÍ 40 marc', '(a) AN TRIAIL (40 marc)', [
        '(i) ‘Léiríonn na pearsana Pádraig Mac Cárthaigh agus Mailí sa dráma An Triail dhá thaobh chontrártha den saol inar mhair '
        'Máire Ní Chathasaigh.’',
        'Déan plé ar an ráiteas sin.',
        'nó',
        '(ii) ‘Cuireann príomhchoimhlintí an dráma An Triail go mór lenár dtuiscint ar shaol na hÉireann ag am a scríofa.’',
        'Déan plé ar an ráiteas sin.']),
    ('X-2D-b', 'extra-2d-b', 'Próstéacs 2D(b) · Dráma roghnach', 'irish-4-7', 7, 'D DRÁMAÍ 40 marc', '(b) DRÁMA ROGHNACH (40 marc)', [
        '(i) Maidir leis an dráma roghnach a ndearna tú staidéar air, déan plé ar an gcaidreamh atá ag an bpríomhphearsa le beirt '
        'eile sa dráma agus an tionchar a bhíonn ag an gcaidreamh sin ar imeachtaí an dráma.',
        'Ní mór teideal an dráma sin, mar aon le hainm an údair, a scríobh síos go cruinn.',
        'nó',
        # The paper prints "drama" without its fada here; the card shows the paper's.
        '(ii) Maidir leis an drama roghnach a ndearna tú staidéar air, déan plé ar an gcaoi a dtéann gnéithe den saol sóisialta nó '
        'den saol polaitiúil i bhfeidhm ar an gcaidreamh idir beirt de na príomhphearsana ann.',
        'Ní mór teideal an dráma sin, mar aon le hainm an údair, a scríobh síos go cruinn.']),
]

POEMS = {
    'F-A': ('poetry-3a', 'Filíocht 3A · Filíocht Ainmnithe', [8, 9, 10], 'A FILÍOCHT AINMNITHE 35 mharc', [
        'Freagair (a) atá thíos agus (b) atá thall ar leathanach 10.',
        '(a) (i) Luaigh dhá cheann de na mothúcháin is mó, dar leat, sa dán Jack (thíos) agus déan cur síos ar an gcaoi a gcuirtear '
        'in iúl iad. (12 mharc)',
        '(ii) Luaigh an íomhá (pictiúr) is mó a chuaigh i bhfeidhm ort agus abair cén fáth. (8 marc)',
        'nó',
        '(i) Maidir leis an dán Bímse Buan ar Buairt Gach Ló (thíos) déan plé gairid ar an gcaoi a léirítear príomh-mhothúcháin '
        'an dáin. (12 mharc)',
        '(ii) Luaigh an íomhá (pictiúr) is mó a chuaigh i bhfeidhm ort agus abair cén fáth. (8 marc)',
        '(b) (i) Maidir leis an dán Gealt? (thíos), déan trácht ar na híomhánna (pictiúir) is mó a threisíonn le príomhthéama an dáin '
        'dar leat. (15 mharc)',
        'nó',
        '(ii) Maidir leis an dán Gealt? (thíos), cad a spreag eachtraí an dáin, dar leat, agus léirigh mar a d’fhorbair an file na '
        'heachtraí sin. (15 mharc)']),
    'F-B': ('poetry-3b', 'Filíocht 3B · Filíocht Roghnach', [11], 'B FILÍOCHT ROGHNACH 35 mharc', [
        'Freagair (a) agus (b).',
        '(a) (i) Maidir le dán seanaimseartha a chum bean, agus a ndearna tú staidéar air le linn do chúrsa, déan plé ar aigne an '
        'fhile sa dán agus ar an gcaoi a léirítear í. (12 mharc)',
        '(ii) Luaigh an ghné den dán is mó a chuaigh i bhfeidhm ort agus mínigh do rogha. (8 marc)',
        'Ní mór teideal an dáin, mar aon le hainm an fhile, a scríobh síos go cruinn.',
        'nó',
        '(i) Maidir le dán nua-aimseartha a chum fear, agus a ndearna tú staidéar air le linn do chúrsa, déan plé ar a éifeachtaí is '
        'a léiríonn na híomhánna an príomhthéama ann. (12 mharc)',
        '(ii) Déan trácht ar an mothúchán is treise sa dán dar leat. (8 marc)',
        'Ní mór teideal an dáin, mar aon le hainm an fhile, a scríobh síos go cruinn.',
        '(b) (i) Maidir le dán nua-aimseartha a chum bean, agus a ndearna tú staidéar air le linn do chúrsa, agus nár úsáid tú i gcuid '
        '(a) thuas, déan plé gairid ar phríomhthéama an dáin agus inis cén fáth a ndeachaigh an dán i bhfeidhm ort féin. (15 mharc)',
        'Ní mór teideal an dáin, mar aon le hainm an fhile, a scríobh síos go cruinn.',
        'nó',
        '(ii) Maidir le dán nua-aimseartha a chum fear agus a ndearna tú staidéar air le linn do chúrsa, agus nár úsáid tú i gcuid (a) '
        'thuas, déan plé gairid ar do rogha dhá cheann de na gnéithe seo: (a) na híomhánna; (b) an t-atmaisféar; (c) teideal an dáin; '
        '(d) an t-athrá. (15 mharc)',
        'Ní mór teideal an dáin, mar aon le hainm an fhile, a scríobh síos go cruinn.']),
    'F-C': ('poetry-3c', 'Filíocht 3C · Dánta Dualgais Breise', [12, 13], 'C DÁNTA DUALGAIS BREISE 35 mharc', [
        'Freagair (a) nó (b).',
        '(a) Freagair (i), (ii) agus (iii) thíos.',
        '(i) ‘Sa dán Oíche Nollaig na mBan baineann an file úsáid as íomhánna (pictiúir) láidre neamhghnácha lena smaointe agus a '
        'mhothúcháin a chur in iúl.’',
        'An ráiteas sin a phlé maidir leis an dán thíos. (20 marc)',
        '(ii) Mínigh na línte seo:',
        'Ba mhaith liom go dtiocfadh an stoirm sin féin',
        'An oíche go mbeadsa go lag',
        'Ag filleadh abhaile ó rince an tsaoil',
        'Is solas an pheaca ag dul as.',
        '(6 mharc)',
        '(iii) Scríobh nóta ar an úsáid a bhaineann an file as codarsnachtaí sa dán. (9 marc)',
        'nó',
        '(b) Freagair (i), (ii) agus (iii) thíos.',
        '(i) I gcás an dáin Dán do Mhelissa déan plé ar an bpríomhthéama atá sa dán agus ar an gcaoi a gcuirtear os ár gcomhair é. (20 marc)',
        '(ii) Mínigh na línte seo:',
        'Bheadh an damh ag súgradh leis an madra,',
        'An naíonán ag gleáchas leis an nathair nimhe,',
        'Luífeadh an leon síos leis an uan caorach.',
        '(6 mharc)',
        '(iii) Scríobh nóta gairid ar éifeacht dhá chodarsnacht i léiriú phríomhthéama an dáin. (9 marc)']),
}
STAIR = ['Scríobh gearrchuntas ar DHÁ CHEANN díobh seo a leanas.',
         'I gcás (a), (b) agus (f), is pointí gearra eolais atá á lorg.',
         'I gcás (c), (d) agus (e), tá pointí níos faide á lorg.',
         '(a) Do rogha beirt díobh seo a leanas:',
         'Liam Ó Flaithearta', 'Máirtín Ó Direáin', 'Máire Mhac an tSaoi', 'Peig Sayers', 'Biddy Jenkinson', 'Nuala Ní Dhomhnaill',
         'Caitlín Maude', 'Séamus Ó Grianna',
         '[Ní mór saol agus saothar gach duine díobh a lua.]',
         '(b) Do rogha dhá cheann díobh seo a leanas:',
         'An Ghaeilge mar theanga Cheilteach; Annála na gCeithre Máistrí; Ogham; An Aisling Pholaitiúil.',
         '(c) An Fhiannaíocht.', '[Is leor trí mhórphointe.]',
         '(d) Filíocht na mBard.', '[Is leor trí mhórphointe.]',
         '(e) Na Cúirteanna Filíochta.', '[Is leor trí mhórphointe.]',
         '(f) Do rogha dhá cheann díobh seo a leanas:',
         'Gael Linn; Oireachtas na Gaeilge; Drámaíocht na Gaeilge; Údarás na Gaeltachta.']


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2011/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2011/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    assert symbol_audit(paper) == PAPER_GLYPHS and symbol_audit(doc, range(15, 20)) == {}, 'Symbol glyphs changed: repeat the glyph review'
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 15, 19)
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
            id=f'irish-2011-hl-p2-{slug}', year=2011, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2011 HL Paper 2 {ref}', questionText=prompt,
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
    gaeilge1, g1pages = s.chunk('Cumas Gaeilge - (a) agus (b) le chéile', 'CEIST 2 -' if 'CEIST 2 -' in s.text else 'Ceist 2 -', s.page(16))
    assert gaeilge1.startswith('Cumas Gaeilge - (a) agus (b) le chéile = 5 marc C. 1 (A) nó (B) = 40 marc (22 + 13 + 5) Nóta:'), gaeilge1[:120]
    assert gaeilge1.endswith('bainfear marcanna mura luaitear iad.') and g1pages == [16], gaeilge1[-60:]
    gaeilge1a, _ = s.chunk('Cumas Gaeilge – (a) agus (b) le chéile', 'B - PRÓS ROGHNACH', s.page(15))
    assert gaeilge1a == 'Cumas Gaeilge – (a) agus (b) le chéile = 5 marc', gaeilge1a
    for key, slug, ref, heading, lines, (a_start, a_end), (b_start, b_end) in PROSE:
        page_has([heading, 'Freagair (a) agus (b).', *[line for line in lines if line != 'nó']], [3])
        part_a, a_pages = s.chunk(a_start, a_end, s.page(15))
        part_b, b_pages = s.chunk(b_start, b_end, s.page(15))
        assert part_a.count('= 22 marc') == part_a.lower().count('ionramháil ábhair = 22 marc') == (3 if key == 'P-A' else 2), part_a
        assert part_b.count('= 13 marc') == 2, part_b
        gaeilge_lines = [gaeilge1a, gaeilge1] if key == 'P-A' else [gaeilge1]
        prompt = f'{heading}\nFreagair (a) agus (b).\n' + '\n'.join(lines)
        add(key, slug, ref, prompt, 'irish-4-7', [3], sorted(set(a_pages) | set(b_pages) | {16}),
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
    rule2, r2pages = s.chunk('Ceist 2 - PRÓSTÉACS BREISE - 40 marc', 'CEIST 3 - FILÍOCHT', s.page(17))
    assert rule2.endswith('a thaispeáint go soiléir san ionad cuí ar an bhfreagarleabhar.') and '{ Ionramháil Ábhair = 35 marc}' in rule2, rule2
    # The Eolas criterion reads its own price, as printed inside the braces; the selection line before it is the Gaeilge
    # criterion's, with the rest of the rule.
    eolas2 = 'Ionramháil Ábhair = 35 marc'
    assert rule2.count('{ Ionramháil Ábhair = 35 marc}') == 1 and rule2.count('{ Cumas Gaeilge = 5 marc}') == 1, rule2
    for key, slug, ref, topic, page, section, route, lines in EXTRA:
        page_has([section, 'Freagair (a) nó (b).', route, *[line for line in lines if line != 'nó']], [page])
        prompt = f'{section}\nFreagair (a) nó (b).\n{route}\n' + '\n'.join(lines)
        add(key, slug, ref, prompt, topic, [page], r2pages,
            [criterion('eolas', 'Ionramháil Ábhair', 35, [eolas2]), criterion('gaeilge', 'Cumas Gaeilge', 5, [rule2], 'quality', list(range(6)))],
            'One complete SEC response: Ionramháil Ábhair 35, judged as a whole, and Cumas Gaeilge 5 (scheme PDF 17). (i) and (ii) are the '
            'printed alternatives of this route, marked alike. The scheme prints no notes, band table or grade table for Ceist 2, so the '
            'answer is claimed whole.', ('Próstéacs Breise', ref.split(' · ', 1)[1]), stem=head2)

    # ---- Ceist 3: Filíocht -------------------------------------------------------------------------------------------------
    head3 = ('Ceist 3\nFILÍOCHT 70 MARC\nFreagair A (Filíocht Ainmnithe) ar na leathanaigh 8, 9 agus 10 nó B (Filíocht Roghnach) ar leathanach 11 '
             'agus freagair C (Dánta Dualgais Breise) ar na leathanaigh 12 agus 13.')
    page_has(head3.splitlines(), [8])
    gaeilge3, g3pages = s.chunk('Cumas Gaeilge (A nó B agus C le chéile)', 'Ceist 4 - STAIR', s.page(19))
    assert gaeilge3.startswith('Cumas Gaeilge (A nó B agus C le chéile) = 10 marc Nóta:') and gaeilge3.endswith('ar an bhfreagarleabhar.'), gaeilge3
    # Each route's scheme text, cut at its sub-questions (the scheme's "(i)"/"(ii)"/"(iii)" restatements and their prices).
    a_i = [s.chunk('(a) (i) Dhá cheann de na mothúcháin', '(ii) An íomhá is mó a chuaigh i bhfeidhm ort agus cén fáth. (Jack)', s.page(17))[0],
           s.chunk('Nó (i) Plé ar an gcaoi a léirítear', '(ii) An íomhá is mó a chuaigh i bhfeidhm ort agus cén fáth. (Bímse', s.page(17))[0]]
    a_ii = [s.chunk('(ii) An íomhá is mó a chuaigh i bhfeidhm ort agus cén fáth. (Jack)', 'Nó (i) Plé ar an gcaoi', s.page(17))[0],
            s.chunk('(ii) An íomhá is mó a chuaigh i bhfeidhm ort agus cén fáth. (Bímse', '(b) (i) Trácht', s.page(17))[0]]
    a_b = s.chunk('(b) (i) Trácht ar na híomhánna', 'B - FILÍOCHT ROGHNACH', s.page(17))[0]
    assert [x[-9:] for x in a_i] == ['= 11 marc'] * 2 and [x[-8:] for x in a_ii] == ['= 6 marc'] * 2 and a_b.endswith('(Gealt?) = 13 marc'), (a_i, a_ii, a_b)
    b_i = [s.chunk('(a) (i) Plé ar aigne an fhile', '(ii) An ghné den dán', s.page(18))[0],
           s.chunk('Nó (i) A éifeachtaí a léiríonn', '(ii) Trácht ar an mothúchán', s.page(18))[0]]
    b_ii = [s.chunk('(ii) An ghné den dán', 'Nó (i) A éifeachtaí', s.page(18))[0],
            s.chunk('(ii) Trácht ar an mothúchán', '(b) (i) Plé ar an bpríomhthéama', s.page(18))[0]]
    b_b = s.chunk('(b) (i) Plé ar an bpríomhthéama', 'Ní bhronnfar marcanna ar theidil', s.page(18))[0]
    titles3b = s.chunk('Ní bhronnfar marcanna ar theidil', '⟦19⟧', s.page(18))[0]
    c_i = [s.chunk('(a) Oíche Nollaig na mBan (i)', '(ii) Mínigh na línte. = 4', s.page(19))[0],
           s.chunk('(b) Dán do Mhelissa (i)', '(ii) Mínigh na línte = 4', s.page(19))[0]]
    c_ii = [s.chunk('(ii) Mínigh na línte. = 4', '(iii) Nóta ar an úsáid', s.page(19))[0],
            s.chunk('(ii) Mínigh na línte = 4', '(iii) Nóta ar éifeacht', s.page(19))[0]]
    c_iii = [s.chunk('(iii) Nóta ar an úsáid', '(b) Dán do Mhelissa', s.page(19))[0],
             s.chunk('(iii) Nóta ar éifeacht', 'Cumas Gaeilge (A nó B', s.page(19))[0]]
    for group, mark in [(b_i, 11), (c_i, 18), (c_ii, 4), (c_iii, 8)]:
        assert all(re.search(rf'=\s*{mark} marc', x) for x in group), (group, mark)
    assert all(re.search(r'= 6 marc', x) for x in b_ii) and b_b.count('= 13 marc') == 2 and a_b.count('= 13 marc') == 2
    assert titles3b == 'Ní bhronnfar marcanna ar theidil/ainmneacha údar a lua ach bainfear marcanna mura luaitear iad.', titles3b
    routes3 = {
        'F-A': [('eolas-a-i', '(a)(i) Eolas', 11, a_i), ('eolas-a-ii', '(a)(ii) Eolas', 6, a_ii), ('eolas-b', '(b) Eolas', 13, [a_b])],
        'F-B': [('eolas-a-i', '(a)(i) Eolas', 11, b_i), ('eolas-a-ii', '(a)(ii) Eolas', 6, b_ii), ('eolas-b', '(b) Eolas', 13, [b_b, titles3b])],
        'F-C': [('eolas-i', '(i) Eolas', 18, c_i), ('eolas-ii', '(ii) Eolas', 4, c_ii), ('eolas-iii', '(iii) Eolas', 8, c_iii)],
    }
    scheme_pages3 = {'F-A': [17, 19], 'F-B': [18, 19], 'F-C': [19]}
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
    page_has([*head4.splitlines(), *STAIR], [14])
    stair, spages = s.chunk('Ceist 4 - STAIR - 30 marc', None, s.page(19))
    assert stair.startswith('Ceist 4 - STAIR - 30 marc Dhá cheann le déanamh as (a), (b), (c), (d), (e), (f). 13 + 12 (Eolas) móide 5 marc')
    assert stair.endswith('a thaispeáint go soiléir san ionad cuí ar an bhfreagarleabhar.') and spages == [19], stair[-80:]
    # The Eolas criterion reads the two answers' split and what the scheme asks of each option; the "= 30 marc" that totals the
    # question with its Gaeilge is the Gaeilge criterion's, with the whole rule.
    split4 = 'Dhá cheann le déanamh as (a), (b), (c), (d), (e), (f). 13 + 12 (Eolas) móide 5 marc ar an gCumas Gaeilge (sa dá cheann le chéile)'
    rest4 = stair[stair.index('= 30 marc. ') + len('= 30 marc. '):]
    assert split4 in stair and rest4.startswith('I gcás (a), (b), (f), tá cuntas le scríobh ar dhá cheann;'), rest4[:60]
    add('X-4', 'history-4', 'Stair na Gaeilge 4', head4 + '\n' + '\n'.join(STAIR), 'irish-7-0', [14], [19],
        [criterion('eolas', 'Eolas', 25, [split4, rest4]), criterion('gaeilge', 'Cumas Gaeilge', 5, [stair], 'quality', list(range(6)))],
        'One complete SEC response: two of (a)–(f), Eolas 13 for one and 12 for the other (25, the scheme’s “an marc a bhronntar as 25 '
        '(Eolas)”) and Cumas Gaeilge 5 for the two together. Each printed option is one choice inside this card. The scheme prints no '
        'answer for Ceist 4 and no scale: the Eolas steps only at its printed split, 12 or 13 for one answer and 25 for both.', ('Stair na Gaeilge', 'Ceist 4'))

    assert len(cards) == 14 and len({c['id'] for c in cards}) == 14 and len({c['atlasQuestionId'] for c in cards}) == 14
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'] in ('P-A', 'X-2A-a', 'F-A', 'F-C', 'X-4')) == 180
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-\xad]', g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=2011, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=[], literatureRouteCardIds=[c['id'] for c in cards],
                  examStructure=dict(prose=40, additionalProse=40, poetry=70, history=30, total=180),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='14 route cards: Ceist 1 A and B; Ceist 2 A(a)–D(b), each (i) nó (ii); Ceist 3 A, B and C; Ceist 4 (two of (a)–(f)). '
                             '49 printed asks, each a printed alternative inside one of them.')
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
    print(f"Irish Higher 2011 Paper 2: {len(data['cards'])} reviewed literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
