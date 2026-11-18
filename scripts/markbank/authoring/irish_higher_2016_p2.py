#!/usr/bin/env python3
"""Reviewed 2016 Higher Paper 2 (Léamhthuiscint agus Litríocht): new cards, no legacy component.

Paper PDF 1–12 (page 2 a pointer to the instructions, 3 the Treoracha, 4–7 the two reading
passages with their questions, 8 prose, 9 poetry with An tEarrach Thiar, 10 additional
literature, 11–12 the two versions of Caoineadh Airt Uí Laoghaire) and the Paper 2 pages of
the combined LC001ALP000IV scheme (PDF 16–30, plus 31 modified marking) reviewed on
2026-11-04. Counts are assertions, not corpus-completeness proof.

The reading cards follow the reviewed 2018–2026 Higher Paper 2 components: every printed
reading question is a whole card with one criterion per published part, each published part
is also a practice card, two independent one-mark answers (A 5(b)(i), B 3(b)(i)) expose their
own slots, order-dependent 2 + 1 items stay whole, and the two 6-mark halves of each 6(b)
(A: two aims, as 2020 A 6(b); B: two points of information, as 2025) expose their own slots.

2016's literature differs from 2018's. 2A (Oisín i dTír na nÓg) and 2B (an optional folk
tale) each print three sub-questions with "do rogha dhá cheann díobh seo a leanas"; the
scheme prints no supporting notes for them, only the rule "Dhá cheann le freagairt-an ceann is
fearr a mharcáil as 13 mharc agus an ceann eile a mharcáil as 12 mharc". Each is one card
carrying all three printed sub-questions, with the scheme's two Eolas marks (the better
answer 13, the other 12) and the shared Gaeilge 5 as criteria; a sub-question alone has no
printed price (13 or 12 depends on the other answer), so no per-sub-question card is made.
3A (An tEarrach Thiar) and 3B (an optional modern poem) price Eolas 13 + 5 + 7. Ceist 4A–4E
print no text of their own in the scheme: the Treoracha on PDF 28 price each as Eolas 35 and
Gaeilge 5, assessed as a unit. 4F (Caoineadh Airt Uí Laoghaire) prices Eolas 16 + 11 + 8.
The scheme prints no Gaeilge band table for Ceisteanna 2–4; the general grading table on
PDF 30 ("Grádú Marcála sna Ceisteanna") converts a grade to a mark for every total.
Boxed headings are removed by exact match.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001ALP200IV'
SCHEME_FILE = 'LC001ALP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/higher-2016-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-higher-2016-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = '9da506d18125881b747be2ad06c5bc0c7d53f7b8ae3b0eb22ab5da642c2b747d'
SCHEME_SHA = 'f3b2e8729023ab943d91df9d413a569e38917cd560db1af6a665ef901f7f6057'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|'
                       r'ceann amháin|pointe amháin|\bdhá\b|an dá\b|amháin', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
# Boxed page headings the 2016 text layer stores inside the literature pages; exact strings only.
FURNITURE = ('– PRÓS AINMNITHE nó PRÓS ROGHNACH – (30 marc)', '– FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH – (30 marc)',
             '– LITRÍOCHT BHREISE – (40 marc)')
# The examiner's marking-panel note that closes each prose and poetry answer: the boundary of the answer's own text.
PANEL = 'Nóta: Caithfidh an Scrúdaitheoir'
CHOOSE_TWO = 'Dhá cheann le freagairt-an ceann is fearr a mharcáil as 13 mharc agus an ceann eile a mharcáil as 12 mharc.'


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def unbox(text):
    for heading in FURNITURE:
        text = text.replace(heading, ' ')
    return clean(text)


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
        return unbox(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)

    def page(self, number):
        return self.text.index(f'⟦{number}⟧')


def printed_values(chunk, marks):
    # The marks a single-answer part can earn: 0, the full tariff and every partial the scheme prints for it.
    values = re.findall(r'= (\d+) mh?arc', chunk) + re.findall(r'bronntar (\d+) mh?arc', chunk) + re.findall(r'\((\d+) mh?arc\)', chunk)
    values += [int(a) - int(b) for a, b in re.findall(r'easnamhach \((\d+)-(\d+)\)', chunk)]
    return sorted({0, marks} | {int(v) for v in values if int(v) <= marks})


def material():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2016/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2016/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 16, 31)
    # The marking instructions, from their first rule (their heading "Treoracha do mharcáil na léamhthuisceana" is a title)
    # to the boxed section heading that the text layer stores after them.
    general = s.chunk('Tá Ceist 1 – 5 ar cómharc', 'Páipéar II (200 marc)')[0]
    assert general.endswith('sa fhreagarleabhar.'), general[-60:]
    # (q, part, paper prompt, scheme anchor, marks, mode, printed tariff). Each passage ends where the examiner's
    # marking panel for 6(b) begins ("Aidhm 1 (2) + Forbairt (4) = …", "P(1) (2) + E1 (4)= …").
    passages = {
        'A': dict(title='Na Cluichí Oilimpeacha – Prionsabail agus Conspóidí', pages=[4, 5], topic='irish-3-0',
                  end='Aidhm 1 (2) + Forbairt (4) = Aidhm 2 (2) + Forbairt (4) = Ceist 6 (b) (12) =', parts=[
            ('1', 'a', '(a) Luaigh dhá phointe eolais faoi Euro 2016, Corn na hEorpa sa sacar, atá ar siúl faoi láthair. (Alt 1)', '1. (a) Luaigh dhá phointe eolais faoi Euro 2016', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Cén fáth a raibh teannas san airéine ag deireadh throid Katie Taylor? (Alt 1)', '(b) (i) Cén fáth a raibh teannas', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Bua stairiúil ba ea bua Katie, dar leis an údar. Cén chúis atá lena thuairim? (Alt 1)', '(ii) Bua stairiúil ba ea bua Katie', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Scríobh síos dhá phointe eolais faoi Pierre de Coubertin mar oideachasóir sa Fhrainc. (Alt 2)', '2. (a) Scríobh síos dhá phointe eolais faoi Pierre', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Cén fáth nár reáchtáladh na Cluichí Oilimpeacha sna blianta 1916, 1940 agus 1944? (Alt 2)', '(b) (i) Cén fáth nár reáchtáladh', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cad a deirtear sa Chairt Oilimpeach faoin iomaíocht sna cluichí? (Alt 2)', '(ii) Cad a deirtear sa Chairt', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Luaigh dhá phointe eolais faoin nós a tosaíodh i mBeirlín agus atá fós ina dhlúthchuid de na Cluichí Oilimpeacha. (Alt 3)', '3. (a) Luaigh dhá phointe eolais faoin nós', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Cén fáth a raibh go leor tíortha buartha faoi Hitler agus na Cluichí Oilimpeacha? (Alt 3)', '(b) (i) Cén fáth a raibh go leor tíortha', 2, None, '{2 mharc}'),
            ('3', 'bii', '(ii) Conas a léirigh Jesse Owens nach raibh aon bhunús leis an dearcadh Naitsíoch? (Alt 3)', '(ii) Conas a léirigh Jesse Owens', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Tabhair dhá chúis ar moladh Ben Johnson ag na Cluichí Oilimpeacha in Seoul. (Alt 4)', '4. (a) Tabhair dhá chúis ar moladh', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cad a cuireadh i leith Johnson cúpla lá i ndiaidh dó an rás a bhuachan? (Alt 4)', '(b) (i) Cad a cuireadh i leith Johnson', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Cad a dhéantar anois le cosc a chur le húsáid na ndrugaí mídhleathacha sa spórt? (Alt 4)', '(ii) Cad a dhéantar anois le cosc', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Scríobh síos dhá rud a dúirt Uachtarán Choiste Idirnáisiúnta na gCluichí Oilimpeacha faoi shaol an spóirt faoi láthair. (Alt 5)', '5. (a) Scríobh síos dhá rud a dúirt', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cad iad na fadhbanna atá sa Bhrasaíl faoi láthair, dar leis an Uachtarán Bach? (Alt 5)', '(b) (i) Cad iad na fadhbanna atá sa Bhrasaíl', 2, 'slots', '{1 mharc + 1 mharc}'),
            ('5', 'bii', '(ii) Cad é ár nguí anseo in Éirinn, dar leis an údar? (Alt 5)', '(ii) Cad é ár nguí', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla d’ainmfhocal sa tuiseal ginideach iolra in Alt 1 agus sampla de bhriathar sa Mhodh Coinníollach in Alt 3.', '6. (a) Aimsigh sampla d’ainmfhocal sa tuiseal ginideach iolra', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Bunaithe ar an eolas sa sliocht thuas, déan plé, i d’fhocail féin, ar dhá aidhm a bhí ag an údar, dar leat, nuair a scríobh sé an sliocht seo. (Is leor 60 focal.)', '(b) Bunaithe ar an eolas sa sliocht thuas', 12, 'aims', '{6 mharc + 6 mharc}')]),
        'B': dict(title='Athrú Aeráide: Fadhb Mhór ár Linne', pages=[6, 7], topic='irish-3-1',
                  end='P(1) (2) + E1 (4)= P(2) (2) + E2 (4)=', parts=[
            ('1', 'a', '(a) Cad iad na hathruithe atá tar éis tarlú sa réigiún Artach le caoga bliain anuas? (Alt 1)', '1. (a) Cad iad na hathruithe atá tar éis tarlú', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('1', 'bi', '(b) (i) Cén fáth a mbíonn ar an mbéar bán a shaol a chur i mbaol go minic? (Alt 1)', '(b) (i) Cén fáth a mbíonn ar an mbéar bán', 2, None, '{2 mharc}'),
            ('1', 'bii', '(ii) Cad é an dúshlán is mó atá roimh an gcine daonna faoi láthair? (Alt 1)', '(ii) Cad é an dúshlán is mó', 2, None, '{2 mharc}'),
            ('2', 'a', '(a) Cad a scríobh John Maynard Keynes faoin mbaint a bhí ag an gcine daonna le háilleacht an dúlra? (Alt 2)', '2. (a) Cad a scríobh John Maynard Keynes', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('2', 'bi', '(b) (i) Cén t-athrú a tharla sa domhan forbartha sna blianta tar éis an Dara Cogadh Domhanda? (Alt 2)', '(b) (i) Cén t-athrú a tharla sa domhan forbartha', 2, None, '{2 mharc}'),
            ('2', 'bii', '(ii) Cad a bhí á fhiafraí ag na heolaithe faoi lár na 1970idí? (Alt 2)', '(ii) Cad a bhí á fhiafraí', 2, None, '{2 mharc}'),
            ('3', 'a', '(a) Luaigh dhá rud ar scríobh na heolaithe fúthu sa tuarascáil Ár dTodhchaí Chomónta. (Alt 3)', '3. (a) Luaigh dhá rud ar scríobh na heolaithe', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('3', 'bi', '(b) (i) Scríobh síos dhá cheann de na ceisteanna casta a phléann na toscairí idirnáisiúnta go rialta. (Alt 3)', '(b) (i) Scríobh síos dhá cheann de na ceisteanna casta', 2, 'slots', '{2 mharc: 1 mharc + 1 mharc}'),
            ('3', 'bii', '(ii) Cén ceangal a chuir Prótacal Kyoto ar gach tír? (Alt 3)', '(ii) Cén ceangal a chuir Prótacal Kyoto', 2, None, '{2 mharc}'),
            ('4', 'a', '(a) Cad iad na hathruithe atá tagtha ar phatrúin na haimsire in Éirinn le blianta beaga anuas? (Tabhair dhá cheann díobh.) (Alt 4)', '4. (a) Cad iad na hathruithe atá tagtha', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('4', 'bi', '(b) (i) Cad a tógadh ar pháirceanna glasa in Éirinn i rith ré an Tíogair Cheiltigh? (Alt 4)', '(b) (i) Cad a tógadh ar pháirceanna glasa', 2, None, '{2 mharc}'),
            ('4', 'bii', '(ii) Conas a chuireann an t-aerthaisteal leis an téamh domhanda? (Alt 4)', '(ii) Conas a chuireann an t-aerthaisteal', 2, None, '{2 mharc}'),
            ('5', 'a', '(a) Scríobh síos dhá cheann de na moltaí a dhéanann an t-údar maidir le cúrsaí taistil. (Alt 5)', '5. (a) Scríobh síos dhá cheann de na moltaí', 3, 'ordered', '{3 mharc: 2 mharc + 1 mharc}'),
            ('5', 'bi', '(b) (i) Cad a mhol an tUachtarán Ó hUiginn don aos óg a dhéanamh? (Alt 5)', '(b) (i) Cad a mhol an tUachtarán', 2, None, '{2 mharc}'),
            ('5', 'bii', '(ii) Cad a d’aontaigh na ceannairí idirnáisiúnta ag ollchruinniú i bPáras? (Alt 5)', '(ii) Cad a d’aontaigh na ceannairí', 2, None, '{2 mharc}'),
            ('6', 'a', '(a) Aimsigh sampla den bhriathar saor san Aimsir Láithreach in Alt 1 agus sampla d’ainmfhocal baininscneach sa tuiseal ginideach uatha in Alt 5.', '6. (a) Aimsigh sampla den bhriathar saor', 3, 'grammar', '{3 mharc: 2 mharc + 1 mharc}'),
            ('6', 'b', '(b) Déan plé i d’fhocail féin ar dhá phointe eolais faoin athrú aeráide a luann an t-údar sa sliocht seo. (Is leor 60 focal.)', '(b) Déan plé i d’fhocail féin ar dhá phointe eolais', 12, 'points', '{6 mharc + 6 mharc}')]),
    }
    start_b = s.text.index('LÉAMHTHUISCINT B (50 marc)')
    for letter, passage in passages.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        anchors = [p[3] for p in passage['parts']]
        resolved = []
        pos = start_b if letter == 'B' else 0
        for index, (q, part, prompt, anchor, marks, mode, tariff) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            # Anchors are searched forward from the previous part so repeated stems resolve in printed order.
            here = s.text.index(anchor, pos)
            assert letter == 'B' or here < start_b, (letter, q, part)
            chunk, spages = s.chunk(anchor, anchors[index + 1] if index + 1 < len(anchors) else passage['end'], pos)
            pos = here + 1
            assert tariff in chunk, (letter, q, part, chunk[:90])
            assert 'Siombailí' not in chunk and 'LÉAMHTHUISCINT B' not in chunk and 'Nóta: I gcás na gceisteanna' not in chunk, (letter, q, part)
            assert 'Ag bun Léamhthuiscint' not in chunk and 'Páipéar II' not in chunk and 'Ceist 2 PRÓS' not in chunk, (letter, q, part)
            resolved.append((q, part, prompt, anchor, marks, mode, chunk, spages))
        passage['resolved'] = resolved
    assert sum(len(p['resolved']) for p in passages.values()) == 34
    note5 = s.chunk('Nóta: I gcás na gceisteanna 2 (Prós)', 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach).')[0]
    # PDF 30: the general grading instruction and the grade-to-mark table for every total (the scheme's only grading
    # for Ceisteanna 2–4; it prints no literature band table this year).
    grading = s.chunk('Grádú Marcála sna Ceisteanna', '⟦31⟧', s.page(30))[0]
    general4 = s.chunk('Treoracha: Iarrtar ar na hiarrthóirí plé a dhéanamh ar an ráiteas', 'Eolas (35) = Gaeilge (5) =', s.page(28))[0]
    assert note5.endswith('ar Ghaeilge.') and '25 ar Eolas agus 5 ar Ghaeilge' in note5
    assert grading.endswith('D 7 7 6 6 5 5 4 4 4 3 3 2') and 'GRÁD 200 160 100' in grading and 'ansin cinneadh ar an marc.' in grading
    assert general4.endswith('sa fhreagarleabhar.') and 'an t-eolas a mharcáil as 35 marc agus an Ghaeilge san iarracht a mheas as 5 mharc' in general4
    return dict(paper=paper, texts=texts, s=s, general=general, passages=passages, note5=note5, grading=grading,
                general4=general4, decisions=selection_decisions(paper))


READING_REQUIREMENTS = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.',
                        'Úsáid an t-alt a luaitear. Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.']
WHOLE_REQUIREMENTS = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.',
                      'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.']
LIT_REQUIREMENTS = ['Freagair gach cuid den cheist atá priontáilte.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
PART_NOTE = ('SEC allocation for this task. Alternative correct answers in the scheme are answers to one task, not extra task routes. '
             'Whole questions and their practice parts are overlapping exercises; their marks are not added to infer the paper total.')
LABELS = {'a': '(a) Freagra', 'bi': '(b)(i) Freagra', 'bii': '(b)(ii) Freagra', 'grammar': '(a) Freagra',
          'aim-1': '(b) Aidhm 1', 'aim-2': '(b) Aidhm 2', 'point-1': '(b) Pointe eolais 1', 'point-2': '(b) Pointe eolais 2'}
# The two 6-mark halves of 6(b): (criterion id prefix, label, English practice focus).
HALVES = {'aims': ('aim', 'Aidhm', 'One of the two aims of the writer, discussed in your own words (aim {slot}, 6 marks)'),
          'points': ('point', 'Pointe eolais', 'One of the two points of information about climate change the writer mentions, discussed in your own words (point {slot}, 6 marks)')}


def part_criteria(part, marks, mode, chunk, general):
    if mode in HALVES:
        key, label, _ = HALVES[mode]
        return [criterion(f'{key}-1', f'{label} 1', 6, [chunk, general]), criterion(f'{key}-2', f'{label} 2', 6, [chunk, general])]
    if mode in ('ordered', 'grammar'):
        return [criterion('grammar' if mode == 'grammar' else part, 'Freagra', marks, [chunk, general], permitted=[0, 2, 3])]
    if mode == 'slots':
        # "{2 mharc: 1 mharc + 1 mharc}" / "{1 mharc + 1 mharc}": either answer alone earns 1.
        return [criterion(part, 'Freagra', marks, [chunk, general], permitted=[0, 1, 2])]
    return [criterion(part, 'Freagra', marks, [chunk, general], permitted=printed_values(chunk, marks))]


def split_parts(whole, cuts, caps):
    i2 = whole.index(cuts[0]); i3 = whole.index(cuts[1], i2)
    pieces = [whole[:i2].strip(), whole[i2:i3].strip(), whole[i3:].strip()]
    for piece, cap in zip(pieces, caps):
        assert cap in piece, cap
    return pieces


def build():
    m = material()
    texts, s = m['texts'], m['s']
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, extra_topics=None, source=None, **extra):
        cards.append(dict(
            id=f'irish-2016-hl-p2-{slug}', year=2016, level='higher', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'2016 HL Paper 2 {ref}', questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria), topicId=topic,
            **({'additionalTopicIds': extra_topics} if extra_topics else {}),
            conceptId=f'irish-hl-p2-{slug}', paperFileid=FILE, schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=requirements, criteria=criteria, markingGuideNote=note,
            sourceMaterial=dict(kind='source-text', label=source[0] if source else ref, title=source[1] if source else ref,
                                pages=source[2] if source else pages, attribution='© State Examinations Commission.',
                                presentationNote=SOURCE_NOTE),
            **extra))
        return cards[-1]

    # ---- Ceist 1: Léamhthuiscint A agus B (100) ---------------------------------------
    six_b = {'A': '6(b) prices two aims of the writer, 6 marks each (naming the aim 2 + its development 4), in the candidate’s own words.',
             'B': '6(b) prices two points of information about climate change, 6 marks each (stating the point 2 + discussing it with accurate information from the passage 4), in the candidate’s own words.'}
    for letter, passage in m['passages'].items():
        topic = passage['topic']
        source = (f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        by_question = {}
        for q, part, prompt, anchor, marks, mode, chunk, spages in passage['resolved']:
            label = f'{q}({part[0]})' + (f'({part[1:]})' if len(part) > 1 else '')
            text = f'{label} ' + re.sub(r'^(\([a-z]+\)\s*)+', '', prompt)
            here = 'irish-3-3' if mode == 'grammar' else topic
            card = add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {label}', text, here,
                       passage['pages'], spages, part_criteria(part, marks, mode, chunk, m['general']), READING_REQUIREMENTS, PART_NOTE,
                       [topic] if mode == 'grammar' else None, source)
            by_question.setdefault(q, []).append((part, prompt, card))
            if mode == 'slots':
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · Freagra {slot}',
                        text, topic, passage['pages'], spages, [criterion(f'{part}-{slot}', f'Freagra {slot}', 1, [chunk, m['general']])],
                        READING_REQUIREMENTS, 'The scheme prices the two answers 1 mharc + 1 mharc independently; this card practises one of them. ' + PART_NOTE,
                        None, source, practiceFocus=f'One of the two answers (answer {slot}, 1 mark)')
            if mode in HALVES:
                key, half, focus = HALVES[mode]
                for slot in (1, 2):
                    add(f'R-{letter}-{q}-{part}-{slot}', f'reading-{letter.lower()}-q{q}-{part}-{slot}', f'Léamhthuiscint {letter} · Ceist {label} · {half} {slot}',
                        text, topic, passage['pages'], spages, [criterion(f'{key}-{slot}', f'{half} {slot}', 6, [chunk, m['general']])],
                        READING_REQUIREMENTS, 'The scheme prices the two halves 6 + 6 independently (named 2 + developed 4); this card practises one of them. ' + PART_NOTE,
                        None, source, practiceFocus=focus.format(slot=slot))
        for q, parts in by_question.items():
            crits = [dict(c) for _, _, card in parts for c in card['criteria']]
            for c in crits:
                c['label'] = LABELS[c['id']]
            add(f'R-{letter}-{q}', f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}',
                f'{q}. ' + ' '.join(p for _, p, _ in parts) + (' (7 marc)' if q != '6' else ' (15 mharc)'), topic, passage['pages'],
                sorted({p for _, _, c in parts for p in c['schemePages']}), crits, WHOLE_REQUIREMENTS,
                'Complete printed question. Score each published part separately using these SEC allocations.'
                + (' Two-answer grammar is one 0/2/3 placement; ' + six_b[letter] if q == '6' else ''),
                ['irish-3-3'] if q == '6' else None, source)
            assert cards[-1]['totalMarks'] == (15 if q == '6' else 7), (letter, q)
            assert in_order(f'({7 if q != "6" else 15} m', texts[passage['pages'][1] - 1]), (letter, q)

    # ---- Ceisteanna 2–4: An Litríocht -------------------------------------------------------
    gaeilge = lambda: criterion('gaeilge', 'Gaeilge', 5, [m['note5'], m['grading']], 'quality')
    head2 = 'Freagair Ceist 2A (Prós Ainmnithe) nó Ceist 2B (Prós Roghnach) thíos.'
    head3 = 'Freagair Ceist 3A (Filíocht Ainmnithe) nó Ceist 3B (Filíocht Roghnach) thíos.'
    choose_note = ('One complete SEC response: two of the three printed sub-questions answered. The scheme marks the better answer out of 13 and the other '
                   'out of 12 (Eolas 25), plus a single shared 5-mark Gaeilge award; it prints no supporting notes for this question, and its general grading '
                   'table (PDF 30) converts a grade to a mark. A sub-question alone has no printed price, so the card is the whole question.')
    prose = [
        ('P-2A', 'prose-2a', 'Prós 2A · Oisín i dTír na nÓg', 'irish-4-1', '2A. Prós Ainmnithe Maidir leis an scéal béaloidis', 24,
         head2 + '\n2A. Prós Ainmnithe',
         'Maidir leis an scéal béaloidis Oisín i dTír na nÓg, déan plé gairid ar do rogha dhá cheann díobh seo a leanas:\n'
         '(i) An léiriú a fhaighimid ar Oisín mar dhuine grámhar dílis sa scéal.\n'
         '(ii) An pháirt a ghlacann Pádraig Naofa sa scéal. (Is leor dhá phointe eolais.)\n'
         '(iii) Scríobh síos dhá shampla den áibhéil sa scéal agus déan plé gairid ar gach ceann díobh. (30 marc)'),
        ('P-2B', 'prose-2b', 'Prós 2B · Scéal béaloidis roghnach', 'irish-4-7', '2B. Prós Roghnach Níl cead', 24,
         head2 + '\n2B. Prós Roghnach\nNíl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid i bhfreagra ar an bPrós Roghnach.',
         'Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, freagair do rogha dhá cheann díobh seo a leanas:\n'
         '(i) Scríobh síos an tréith is mó atá ag an bpríomhcharachtar (ag an bpríomhphearsa) sa scéal. Déan cur síos ar an léiriú a dhéantar ar an tréith sin sa scéal.\n'
         '(ii) Ainmnigh an mioncharachtar (an mhionphearsa) is tábhachtaí sa scéal, dar leat. Cén pháirt atá aige/aici sa scéal? (Is leor dhá phointe eolais.)\n'
         '(iii) Cad í an tréith bhéaloidis is mó atá sa scéal, dar leat? Scríobh síos dhá shampla den tréith sin sa scéal agus déan plé gairid ar gach ceann díobh.\n'
         'Ní mór teideal an scéil bhéaloidis sin a scríobh síos go cruinn. (30 marc)'),
    ]
    for key, slug, ref, topic, start, page, stem, prompt in prose:
        for line in [*stem.splitlines(), *prompt.splitlines()]:
            assert in_order(line, texts[7]), (key, line[:40])
        # The scheme reprints the question (on the card already); its own marking text is the choose-two rule after it.
        question, qpages = s.chunk(start, 'Dhá cheann le freagairt', s.page(page))
        assert all(in_order(re.sub(r'\s*\(30 marc\)$', '', line), question) for line in prompt.splitlines()[1:4]), (key, 'scheme reprint differs from the paper')
        rule, rpages = s.chunk('Dhá cheann le freagairt', PANEL, s.text.index(start, s.page(page)))
        assert rule == CHOOSE_TWO, (key, rule)
        add(key, slug, ref, prompt, topic, [8], sorted(set(qpages) | set(rpages)),
            [criterion('eolas-1', 'An ceann is fearr', 13, [rule, m['grading']], 'indicative'),
             criterion('eolas-2', 'An ceann eile', 12, [rule, m['grading']], 'indicative'), gaeilge()],
            LIT_REQUIREMENTS, choose_note, source=('Prós', ref.split(' · ', 1)[1], [8]), stem=stem)

    poems = [
        ('F-3A', 'poetry-3a', 'Filíocht 3A · An tEarrach Thiar', 'irish-5-3', '3A. Filíocht Ainmnithe (i)', 26, head3 + '\n3A. Filíocht Ainmnithe', [
            '(i) Cad é an príomhthéama sa dán An tEarrach Thiar (thíos), dar leat? Déan plé ar na híomhánna a úsáideann an file sa dán chun an príomhthéama sin a léiriú. (15 mharc)',
            '(ii) Cad é an mothúchán is láidre a léiríonn an file sa dán seo? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Úsáideann an file go leor aidiachtaí sa dán. Roghnaigh dhá cheann de na haidiachtaí sin agus déan plé gairid ar an tábhacht a bhaineann leo sa dán, dar leat. (9 marc)'],
         ['(ii) Cad é an mothúchán is láidre a léiríonn', '(iii) Úsáideann an file go leor aidiachtaí']),
        ('F-3B', 'poetry-3b', 'Filíocht 3B · Dán nua-aimseartha roghnach', 'irish-5-6', '3B. Filíocht Roghnach Níl cead', 27,
         head3 + '\n3B. Filíocht Roghnach\nNíl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid i bhfreagra ar an bhFilíocht Roghnach.', [
            '(i) Maidir le dán nua-aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, cad é an príomhthéama sa dán, dar leat? Déan plé ar an bhforbairt a dhéanann an file ar an bpríomhthéama sin ó thús deireadh an dáin. (15 mharc)',
            '(ii) Cad é an mothúchán is láidre atá sa dán, dar leat? (Is leor pointe amháin eolais as an dán mar thacaíocht le do fhreagra.) (6 mharc)',
            '(iii) Cad í an teicníc is mó a thaitníonn leat sa dán? Scríobh síos dhá phointe eolais faoin teicníc sin sa dán. (9 marc)',
            'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn.'],
         ['(ii) Cad é an mothúchán is láidre atá sa dán', '(iii) Cad í an teicníc']),
    ]
    for key, slug, ref, topic, start, page, stem, parts, cuts in poems:
        for line in [*stem.splitlines(), *parts]:
            assert in_order(line, texts[8]), (key, line[:40])
        whole, spages = s.chunk(start, PANEL, s.page(page))
        assert 'Eolas (25) =' not in whole and 'Gaeilge (5)' not in whole, key
        pieces = split_parts(whole, cuts, ['Eolas = 13 mharc', 'Eolas = 5 mharc', 'Eolas = 7 marc'])
        add(key, slug, ref, '\n'.join(parts), topic, [9], spages,
            [criterion('eolas-i', '(i) Eolas', 13, [pieces[0], m['grading']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 5, [pieces[1]], 'indicative'),
             criterion('eolas-iii', '(iii) Eolas', 7, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response with one shared five-mark Gaeilge award. The paper prints (i) 15, (ii) 6 and (iii) 9; the scheme assesses '
            'Eolas 13, 5 and 7 with the splits shown, plus Gaeilge 5 once. Supporting notes are indicative rather than exhaustive.',
            source=('Filíocht', ref.split(' · ', 1)[1], [9]), stem=stem)

    head4 = 'Freagair do rogha ceann amháin as Ceist 4 (A, B, C, D, E nó F) thíos.'
    options = [
        ('X-4A', 'literature-4-a', '4A. An Triail', 'irish-6-0',
         '4A. An Triail\n“Á, bhuel! Glacaimis misneach. Níl a fhios ag aon duine beo cad tá roimhe,” arsa Pádraig le Máire oíche an rince sa teach scoile.\n'
         'Déan plé ar an gcineál saoil a bhí roimh Mháire ón oíche sin ar aghaidh agus ar an gcaoi a ndeachaigh sí i ngleic leis an saol sin sa dráma An Triail. (40 marc)'),
        ('X-4B', 'literature-4-b', '4B. A Thig Ná Tit Orm', 'irish-6-1',
         '4B. A Thig Ná Tit Orm\n“Tugann Maidhc Dainín cuntas an-taitneamhach dúinn ar an tréimhse a chaith sé i gCeardscoil an Daingin agus ar shamhradh na bliana 1958 ina dhírbheathaisnéis A Thig Ná Tit Orm.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4C', 'literature-4-c', '4C. Tóraíocht Dhiarmada agus Ghráinne', 'irish-6-2',
         '4C. Tóraíocht Dhiarmada agus Ghráinne\n“Tá an draíocht agus an áibhéil ag baint le cuid mhór de na heachtraí a tharlaíonn sa Tóraíocht.”\nDéan plé ar an ráiteas sin. (40 marc)'),
        ('X-4D', 'literature-4-d', '4D. Gafa', 'irish-6-3',
         '4D. Gafa\n“Tá an mháthair, Eithne, tuirseach ó bheith ag plé le cás Eoin agus tuirseach den easpa tacaíochta ó Bhreandán sa sliocht as an úrscéal Gafa.”\n'
         'Déan plé ar an ráiteas sin. (40 marc)'),
        ('X-4E', 'literature-4-e', '4E. Canary Wharf', 'irish-6-4',
         '4E. Canary Wharf\n“Ní fheadar an gcuirfeadh cúrsaí mar a thit siad amach, díomá ar an Uasal Maxwell,” a smaoinigh Oscar dó féin sa scéal Mil.\n'
         'Déan plé ar na himeachtaí a tharla i ndiaidh bhás Maxwell agus ar an toradh a bhí ar na himeachtaí sin. (40 marc)'),
    ]
    for key, slug, ref, topic, prompt in options:
        assert all(in_order(line, texts[9]) for line in prompt.splitlines()), key
        # The scheme prints no text of its own for 4A–4E: the Treoracha (PDF 28) price each as Eolas 35 assessed as a unit.
        add(key, slug, f'Litríocht {ref}', head4 + '\n\n' + prompt, topic, [10], [28, 30],
            [criterion('eolas', 'Eolas', 35, [m['general4'], m['grading']], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
            'One complete SEC response: Eolas 35 assessed as a unit with a single shared 5-mark Gaeilge award. The 2016 scheme prints no notes for '
            '4A–4E beyond the Treoracha for Ceist 4; its general grading table (PDF 30) converts a grade to a mark.')
    closing4f = 'Ní mór don Scrúdaitheoir an marc ar eolas as 35 marc'
    whole, spages = s.chunk('4F. Dánta Breise – Caoineadh Airt Uí Laoghaire', closing4f, s.page(28))
    pieces = split_parts(whole, ['(ii) Cad é an mothúchán is mó sa dán seo', '(iii) Cén mheadaracht atá sa dán seo?'],
                         ['Eolas = 16 mharc', 'Eolas = 11 mharc', 'Eolas = 8 marc'])
    f_prompt = ('4F. Dánta Breise – Caoineadh Airt Uí Laoghaire\nFreagair (i), (ii) agus (iii) thíos.\n'
                'Nóta: Bain úsáid as Leagan 1 nó as Leagan 2 (lgh 11-12 thall) den dán i do fhreagraí.\n'
                '(i) Cén léiriú a thugtar dúinn ar an gcineál duine é Art Ó Laoghaire sna línte 8-35 den dán Caoineadh Airt Uí Laoghaire (thall)? (18 marc)\n'
                '(ii) Cad é an mothúchán is mó atá sa dán seo, dar leat? Is leor dhá phointe eolais faoin mothúchán sin. Bíodh tagairtí cruinne agat do théacs an dáin i do fhreagra. (12 mharc)\n'
                '(iii) Cén mheadaracht atá sa dán seo? Scríobh pointe amháin eolais faoin meadaracht seo agus léirigh do fhreagra le sampla cruinn ón dán. (10 marc)')
    assert all(in_order(line, texts[9]) for line in f_prompt.splitlines())
    add('X-4F', 'literature-4-f', 'Litríocht 4F · Dánta Breise – Caoineadh Airt Uí Laoghaire', head4 + '\n\n' + f_prompt, 'irish-6-6', [10, 11, 12],
        sorted(set(spages) | {30}),
        [criterion('eolas-i', '(i) Eolas', 16, [pieces[0], m['grading']], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 11, [pieces[1]], 'indicative'),
         criterion('eolas-iii', '(iii) Eolas', 8, [pieces[2]], 'indicative'), gaeilge()], LIT_REQUIREMENTS,
        'One complete SEC response: the paper prints (i) 18, (ii) 12 and (iii) 10; the scheme assesses Eolas 16, 11 (1 + 5 + 5) and 8 (2 + 4 + 2) '
        'plus one shared 5-mark Gaeilge award. Supporting notes are indicative rather than exhaustive.',
        source=('Dánta Breise', 'Caoineadh Airt Uí Laoghaire', [10, 11, 12]))

    reading = [c for c in cards if '-reading-' in c['id']]
    literature = [c for c in cards if '-reading-' not in c['id']]
    assert len(reading) == 54 and len(literature) == 10, (len(reading), len(literature))
    assert len({c['id'] for c in cards}) == len(cards) == 64 and len({c['atlasQuestionId'] for c in cards}) == 64
    assert sum(c['totalMarks'] for c in cards if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])) == 100
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria']) == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('[-]', g) for g in c['guidance']), (card['id'], c['id'])
            assert all(h not in g for h in FURNITURE for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    whole = [c['id'] for c in reading if re.fullmatch(r'R-[AB]-\d', c['atlasQuestionId'])]
    review = dict(year=2016, level='higher', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  readingWholeCardIds=whole, readingPracticeCardIds=[c['id'] for c in reading if c['id'] not in whole],
                  literatureRouteCardIds=[c['id'] for c in literature],
                  examStructure=dict(readingA=50, readingB=50, prose=30, poetry=30, additionalLiterature=40, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  boundaries='12 whole reading questions with 34 published parts, 4 independent one-mark answer slots and 4 six-mark 6(b) slots; '
                             '2 prose (2A Oisín i dTír na nÓg, 2B an optional folk tale; each choose two of three sub-questions), 2 poetry and 6 additional-literature routes.')
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
    print(f"Irish Higher 2016 Paper 2: {len(data['cards'])} reviewed reading and literature cards; the archive remains incomplete.")


if __name__ == '__main__':
    main()
