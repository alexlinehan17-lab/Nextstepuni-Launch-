"""Reviewed 2010 Ordinary Páipéar II (Litríocht), carded new.

Paper PDF 1–8 (LC001GLP200IV: instructions on page 1; Roinn A Cúrsa Ainmnithe on 2–4, Ceist 1 Prós Ainmnithe on 2,
Ceist 2 Filíocht Ainmnithe on 3–4 with its poems; Roinn B Cúrsa Roghnach on 5–6; pages 7–8 “Leathanach Bán”) and the
Páipéar II pages of the combined LC001GLP000EV scheme (PDF 5–9; the file is named EV, its text is the Irish scheme)
reviewed on 2026-11-05. Counts are assertions, not corpus-completeness proof.

Páipéar II (110) before 2012 is literature only: “Freagair Ceist Iomlán, (a) agus (b), sa Phrós agus san Fhilíocht.”
Prose is the prescribed course (Roinn A Ceist 1) or the optional course (Roinn B Ceist 1), poetry likewise (Roinn A
Ceist 2 or Roinn B Ceist 2); each question is 55: (a) at 35 and (b) at 20, both answered. The scheme prints no answers
or sample points anywhere: each sub-question restated with its price, some prices split (“Cur síos gairid air 3 + 3 = 6
marc”, “Dhá fháth = 2 mharc × 2 = 4 marc”, “2 + 9 + 9 = 20marc”, “(10 marc × 2) = 20 marc”). So every award is
`tariffOnly` (the chip says “Tariff”), its guidance the scheme's restatement and price, and each language deduction is
its own criterion where the scheme prints one: 0–5 under each poetry (a), 0–3 under each (b). The scheme prints no
deduction under either prose (a) (its Nóta after each prose question names one for (a) but prints no range): those
cards carry none, and say so.

Cards (choice is not a route; a printed choice is one card unless the scheme marks the options differently or they are
different prescribed works):
- Prós Ainmnithe (a): the three prescribed works (An Cearrbhach Mac Cába, An Bhean Óg, Coileach Ghleann Phádraig), a
  card each; (b) (i) a theme in one of the other works, whole at 20, and (ii) two things in one, 10 × 2: priced
  differently, a card each.
- Filíocht Ainmnithe (a): the two prescribed poems (Jack, Faoiseamh a Gheobhadsa), a card each, (i)–(iv) as printed;
  (b) on Gealt?: (i) 2 + 9 + 9 and (ii) 7 + 7 + 6, a card each.
- Prós Roghnach (a): the folk tale, priced (i) 23 + title 2 and (ii) 3 + 3 and 2 + 2, and the short story, priced (i)
  23 + title and author 2 and (ii) 5 + 5: priced differently, a card each; (b) (i) a theme (9 + 9) or (ii) two things
  (9 × 2), each + title 2, marked alike: one card.
- Filíocht Roghnach (a): a modern poem by a woman ((i)–(iv), title) or by a man or a woman ((i)–(iv), title), priced
  differently: a card each; (b) (i) 9 + 9 + title or (ii) 12 + 6 + title: a card each.
- Practice cards: every prescribed-course (a) sub-question at its own printed price (the prose (i) and (ii), the poems'
  (i)–(iv)).

Two places where the scheme's restatement differs from the paper are kept as each prints them, and the card says so: the
short story's (i) is restated “Cuntas ar an mothúchán is láidre sa ghearrscéal” where the paper asks for the main events
(“tabhair cuntas ar na príomhimeachtaí (rudaí) a tharla sa ghearrscéal sin”); and Filíocht Roghnach (a)'s second option
prices (ii) “Teideal an dáin oiriúnach? = 4 marc” + “Fáth amháin le do fhreagra = 4 marc” (numbered “(iv)” in the
scheme) where the paper asks only whether the title suits. Permitted marks are the totals the printed prices make
(`printed_marks`): a price claimed whole is 0 or all of it.

No 2010 Ordinary card existed before. The 2010 Atlas files Páipéar II under the pre-2012 keys P-A, P-B, F-A, F-B; the
card keys extend them as 2011's do (P-A-a-1 …), which do not clash. `main` writes the card file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2010
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000EV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2010-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2010-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '101e8324e9c748700c8ec041aef9b647e7c25c15187b9c70e34a525c1644efd2'
SCHEME_SHA = '5dbf2d23c447f46e35a9704197612a59f99c11fb8c559e509e3e794d03e08081'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'  # types/markBank.ts
# The scheme's SymbolMT glyphs: U+F0B4 (×, PDF 3, 5–9) and U+F0B7 (•, PDF 11).
SYMBOL_FONT = {'': '×', '': '•', ' ': ' '}
LANG_A = '[Gaeilge lochtach: 0 – 5 a bhaint den iomlán a gnóthaíodh.]'
LANG_B = '[Gaeilge lochtach: 0 – 3 a bhaint den iomlán a gnóthaíodh.]'
LANG_B_HYPHEN = '[Gaeilge lochtach: 0 - 3 a bhaint den iomlán a gnóthaíodh.]'


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def in_order(prompt, text):
    return re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split() if comparable(w)), comparable(text))


def page_text(page):
    """The page's text with each SymbolMT glyph as the character it draws (every glyph is one SYMBOL_FONT reviewed)."""
    lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            parts = []
            for span in line['spans']:
                text = span['text']
                if span['font'] == 'SymbolMT':
                    assert all(c in SYMBOL_FONT for c in text), ('Unreviewed scheme glyph', page.number + 1, repr(text))
                    text = ''.join(SYMBOL_FONT[c] for c in text)
                parts.append(text)
            lines.append(''.join(parts))
    return '\n'.join(lines)


def criterion(id, label, marks, guidance, kind='indicative', deduction=False):
    # The 2010 Ordinary scheme prints only the tariff of every literature ask, no answer: each award but the language
    # deduction carries tariffOnly, and its chip says "Tariff" (coordinator, batch 7).
    return dict(id=id, label=label, kind='deduction' if deduction else 'award', maxMarks=marks,
                permittedMarks=list(range(marks + 1)) if deduction else printed_marks(guidance, marks), guidanceKind=kind,
                guidance=guidance, **({} if deduction else {'tariffOnly': True}))


def deduction(note, marks):
    return criterion('gaeilge-deduction', 'Gaeilge lochtach', marks, [note], 'quality', deduction=True)


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'], d['raw']) for d in decisions}
    found = {(i, clean(line)) for i, page in enumerate(paper, 1)
             for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found - expected, expected - found)
    return decisions


PRICE = re.compile(r'(?:=\s*)?\(?\s*(\d+)\s*m?h?arc\s*×\s*(\d+)\s*\)?\s*=\s*(\d+)\s*m?h?arc\b'  # “= 4 marc × 2 = 8 marc”
                   r'|\(?(\d+(?:\s*\+\s*\d+)+)\)?\s*=\s*(\d+)\s*m?h?arc\b'  # “3 + 3 = 6 marc”, “(9 + 9) = 18 marc”
                   r'|=\s*(\d+)\s*m?h?arc\b')  # “= 25 marc”


def printed_marks(guidance, marks):
    """The marks a criterion can be awarded: each printed price claimed whole or at the totals its printed split makes, in print
    order (“3 + 3” 0, 3, 6; “4 marc × 2” 0, 4, 8), the prices of one alternative added together, and the alternatives the scheme
    prints with “NÓ” between them each on its own. No step the scheme does not print (coordinator, batch 6)."""
    allowed, sums = set(), {0}
    for line in guidance + ['NÓ']:
        if line == 'NÓ':
            assert max(sums) == marks, (guidance, sorted(sums))
            allowed |= sums
            sums = {0}
            continue
        prices = list(PRICE.finditer(line))
        assert len(prices) <= 1, line
        for price in prices:
            each, times, total, parts, whole, alone = price.groups()
            if each:
                assert int(each) * int(times) == int(total), line
                steps = [int(each) * n for n in range(int(times) + 1)]
            elif parts:
                values = [int(v) for v in re.findall(r'\d+', parts)]
                assert sum(values) == int(whole), line
                steps = [sum(values[:n]) for n in range(len(values) + 1)]
            else:
                steps = [0, int(alone)]
            sums = {a + b for a in sums for b in steps}
    return sorted(allowed)


# Printed lines (paper PDF 1–6).
PROSE_CHOICE = 'Tá rogha ann idir an Cúrsa Ainmnithe (leathanach 2) agus an Cúrsa Roghnach (leathanach 5).'
POETRY_CHOICE = 'Tá rogha ann idir an Cúrsa Ainmnithe (na leathanaigh 3 agus 4) agus an Cúrsa Roghnach (leathanach 6).'
WHOLE = 'Freagair Ceist Iomlán, (a) agus (b), sa Phrós agus san Fhilíocht.'
BOTH = 'Freagair (a) agus (b) anseo.'
SEE_PAGE_1 = 'Chun an chuid seo a fhreagairt féach ar na treoracha atá ar leathanach 1.'
BOX = {'PA': f'ROINN A – CÚRSA AINMNITHE –\n{SEE_PAGE_1}\nCEIST 1 – PRÓS AINMNITHE – [55 mharc]',
       'FA': 'CEIST 2 – FILÍOCHT AINMNITHE – [55 mharc]',
       'PB': f'ROINN B – CÚRSA ROGHNACH –\n{SEE_PAGE_1}\nCEIST 1 – PRÓS ROGHNACH – [55 mharc]',
       'FB': 'CEIST 2 – FILÍOCHT ROGHNACH – [55 mharc]'}
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
OTHER_WORKS = ('Maidir leis na saothair eile a ndearna tú staidéar orthu le linn do chúrsa – Fiche Blian ag Fás, Lá Buí Bealtaine / '
               'Clare sa Spéir agus Lig Sinn i gCathú – roghnaigh saothar amháin díobh')
THEMES = 'greann\ngrá (nó fuath)\nan óige (nó an tseanaois)\naiféala\nsaol na hollscoile\nsaol na tuaithe'
EMOTIONS = 'eagla\nfearg\nionadh\náthas\nfaoiseamh\nimní'

# Each guidance slice is the scheme's text in print order. A slice leaves out the work's bracketed name printed before a price
# (“(Cearrbhach Mac Cába) = 25 marc”, “(Scéal Béaloidis)”, “(Dán nua a chum bean)”), a brace's total printed beside the heading
# between the two rows it totals (“Fáth ar/nár thaitin? = 10 marc” between the 6 and the 4), and the braces themselves: the card
# names the work and the criterion is the total, so each price reads with the ask it prices. Alternatives the scheme marks alike
# keep its “NÓ” between them (tariffs.ts reads each on its own).
PROSE_A = [
    ('P-A-a-1', 'prose-ainmnithe-a-1', 'Prós Ainmnithe (a) · An Cearrbhach Mac Cába', 2, [
        '(i) “Ansin chuaigh an Cearrbhach chuig an Bhás agus dúirt leis go bhfuair sé achainí mhaith an iarraidh seo. ‘Cad é an achainí í?’ '
        'arsa an Bás. ‘Chan insím sin do dhuine ar bith,’ arsa an Cearrbhach.” (An Cearrbhach Mac Cába)',
        'Tabhair cuntas ar ar tharla don Chearrbhach ina dhiaidh sin go dtí go ndeachaigh sé go hIfreann. (25 mharc)',
        '(ii) Cén sórt duine é Dia sa scéal seo, dar leat? Déan cur síos gairid air agus inis cén fáth ar thaitin (nó nár thaitin) sé leat. '
        '(Is leor dhá fháth.) (10 marc)'], [
        ('eolas-i', '(i) Eolas', 25, ['(i) Ón am a bhfuair an Cearrbhach an achainí nó go ndeachaigh sé go hIfreann.', '= 25 marc']),
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) An sórt duine é Dia, dar leat. Cur síos gairid air 3 + 3 = 6 marc', 'Fáth ar/nár thaitin?',
                                        'Dhá fháth = 2 mharc × 2 = 4 marc'])]),
    # The scheme prices An Bhean Óg's reasons whole (“Fáth ar/nár thaitin sé leat. = 4 marc”), with no × 2 split as the other two print.
    ('P-A-a-2', 'prose-ainmnithe-a-2', 'Prós Ainmnithe (a) · An Bhean Óg', 2, [
        '(i) “Máthair mhaith agus bean chéile mhaith í an bhean sa ghearrscéal An Bhean Óg.” Do thuairim uait faoi sin. (25 mharc)',
        '(ii) Cén sórt duine é an fear céile sa scéal dar leat? Déan cur síos gairid air agus inis cén fáth ar thaitin (nó nár thaitin) sé leat. (10 marc)'], [
        ('eolas-i', '(i) Eolas', 25, ['(i) Cur síos ar an mbean óg: máthair mhaith agus céile maith.', '= 25 marc']),
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) An sórt duine é an fear sa scéal. Cur síos gairid air. 3 + 3 = 6 marc',
                                        'Fáth ar/nár thaitin sé leat. = 4 marc'])]),
    ('P-A-a-3', 'prose-ainmnithe-a-3', 'Prós Ainmnithe (a) · Coileach Ghleann Phádraig', 2, [
        '(i) “ ‘Agus conas tá coileach Sally Tom?’ a d’fhiafraigh fear an bheáir. Tháinig cuma dhuairc ar aghaidh an Choilichín. ‘Faraor,’ '
        'ar seisean, ‘ní dócha go mbuafaidh sé bonn ar bith eile mura n-éireoidh leis an vet tarrtháil a dhéanamh air.’ ” (Coileach Ghleann Phádraig)',
        'Tabhair cuntas ar ar tharla nuair a thug an tréidlia agus Jim cuairt ar Ghleann Phádraig. (25 mharc)',
        '(ii) Cén sórt duine é an Coilichín sa scéal seo, dar leat? Déan cur síos gairid air agus inis cén fáth ar thaitin (nó nár thaitin) sé leat. (10 marc)'], [
        ('eolas-i', '(i) Eolas', 25, ['(i) Cuntas ar ar tharla nuair a thug an tréidlia agus Jim cuairt ar Ghleann Phádraig.', '= 25 mharc']),
        # The scheme prints “Fáth ar/nár thaitin ?”: kept as printed.
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) An sórt duine é an Coilichín, dar leat. Cur síos gairid air 3 + 3 = 6 marc', 'Fáth ar/nár thaitin ?',
                                        'Dhá fháth = 2 marc × 2 = 4 marc'])]),
]
PROSE_A_B = [
    ('P-A-b-i', 'prose-ainmnithe-b-i', 'Prós Ainmnithe (b)(i) · Téama', [
        f'(i) {OTHER_WORKS} a bhfuil ceann amháin de na téamaí seo a leanas i gceist ann.',
        'Tabhair cuntas gairid ar a bhfuil sa saothar faoin téama atá roghnaithe agat.', THEMES + ' (20 marc)'],
     'Cuntas gairid ar a bhfuil i gceann amháin de na saothair a luadh faoin téama atá roghnaithe agat as na téamaí atá luaite. = 20 marc'),
    ('P-A-b-ii', 'prose-ainmnithe-b-ii', 'Prós Ainmnithe (b)(ii) · Dhá rud', [
        f'(ii) {OTHER_WORKS}. Tabhair cuntas gairid ar dhá rud ann, rud amháin a thaitin leat agus rud amháin nár thaitin leat. (20 marc)'],
     'Cuntas gairid ar dhá rud i gceann amháin de na saothair a luadh, Rud amháin a thaitin leat agus rud amháin nár thaitin leat. (10 marc × 2) = 20 marc'),
]
POETRY_A = [
    ('F-A-a-1', 'poetry-ainmnithe-a-1', 'Jack', 3, [
        ('i', ['(a) Conas atá a fhios agat nach raibh Jack beag? (Jack thíos).', '(b) Cén post a bhí ag athair Jack?',
               '(c) Conas atá a fhios agat nár thit Jack i ngrá leis an bhfile an oíche sin?', '(d) Cén saghas urláir a bhí fúthu nuair a bhí siad ag rince?'], 8,
         ['(i) (a) Conas atá a fhios agat nach raibh Jack beag? (Jack). (b) Cén post a bhí ag athair Jack? (c) Conas atá a fhios agat nár thit Jack '
          'i ngrá leis an bhfile an oíche sin? (d) Cén saghas urláir a bhí fúthu nuair a bhí siad ag rince? = 8 marc']),
        ('ii', ['Luaigh dhá íomhá (pictiúr) atá sa dán. Déan cur síos i d’fhocail féin ar an dá íomhá sin sa dán.'], 8,
         ['(ii) Luaigh dhá íomhá (pictiúr) atá sa dán. Déan cur síos i d’fhocail féin ar an dá íomhá sin sa dán. = 8 marc']),
        ('iii', ['(a) Conas a léirítear sa dán go mbeidh a athair fial le Jack?', '(b) Conas a léirítear sa dán go dtitfidh Jack i ngrá le bean eile?',
                 '(c) Conas a léirítear sa dán gurbh fhearr leis an bhfile Jack ná fear ar bith eile an samhradh sin?'], 9,
         ['(iii) (a) Conas a léirítear sa dán go mbeidh a athair fial le Jack? (b) Conas a léirítear sa dán go dtitfidh Jack i ngrá le bean eile? '
          '(c) Conas a léirítear sa dán gurbh fhearr leis an bhfile Jack ná fear ar bith eile an samhradh sin? = 9 marc']),
        ('iv', ['Ar thaitin an dán seo leat? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)'], 10,
         ['(iv) Ar thaitin an dán leat? = 2 marc', 'Dhá fháth. = 4 marc × 2 = 8 marc'])]),
    ('F-A-a-2', 'poetry-ainmnithe-a-2', 'Faoiseamh a Gheobhadsa', 3, [
        ('i', ['(a) Cad a gheobhaidh an file nuair a bheidh sé i measc a dhaoine? (Faoiseamh a Gheobhadsa thíos)', '(b) Cá bhfuil cónaí ar a dhaoine?',
               '(c) Cad a dhéanfaidh sé gach maidin is tráthnóna?', '(d) Cá fhad a bheidh sé ar an oileán?'], 8,
         ['(i) (a) Cad a gheobhaidh an file nuair a bheidh sé i measc a dhaoine? (Faoiseamh a Gheobhadsa) (b) Cá bhfuil cónaí ar a dhaoine? '
          '(c) Cad a dhéanfaidh sé gach maidin is tráthnóna? (d) Cá fhad a bheidh sé ar an oileán? = 8 marc']),
        ('ii', ['Luaigh dhá mhothúchán atá sa dán.', 'Déan cur síos, i d’fhocail féin, ar an dá mhothúchán sin sa dán.'], 8,
         ['(ii) Luaigh dhá mhothúchán atá sa dán. Déan cur síos, i d’fhocail féin, ar an dá mhothúchán sin sa dán. = 8 marc']),
        ('iii', ['Luaigh trí rud a bhfaighidh sé faoiseamh uathu nuair a bheidh sé lena dhaoine.'], 9,
         ['(iii) Luaigh trí rud a bhfaighidh sé faoiseamh uathu nuair a bheidh sé lena dhaoine. = 9 marc']),
        # The paper asks “An maith leat an dán seo?”; the scheme restates it “Ar thaitin an dán leat?”: each as printed.
        ('iv', ['An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)'], 10,
         ['(iv) Ar thaitin an dán leat? = 2 marc', 'Dhá fháth = 4 marc × 2 = 8 marc'])]),
]
GEALT = 'Gealt?'
POETRY_A_B = [
    ('F-A-b-i', 'poetry-ainmnithe-b-i', 'Filíocht Ainmnithe (b)(i) · Gealt? · Mothúchán', [
        '(i) Maidir leis an dán Gealt? (thíos), roghnaigh mothúchán amháin as an liosta seo a leanas agus tabhair cuntas gairid ar a bhfuil sa dán faoin mothúchán atá roghnaithe agat.',
        EMOTIONS + ' (20 marc)'],
     ['Cuntas gairid ar a bhfuil sa dán, Gealt? faoin mothúchán atá roghnaithe agat as na mothúcháin atá luaite. 2 + 9 + 9 = 20marc']),
    ('F-A-b-ii', 'poetry-ainmnithe-b-ii', 'Filíocht Ainmnithe (b)(ii) · Gealt? · Príomhsmaointe agus íomhá', [
        '(ii) Maidir leis an dán Gealt? (thíos), tabhair cuntas gairid ar phríomhsmaointe an dáin agus ar íomhá (pictiúr) amháin sa dán sin a thaitin (nó nár thaitin) leat. (20 marc)'],
     ['Cuntas gairid ar phríomhsmaointe an dáin, Gealt? 7 + 7 =14 marc', 'Íomhá a thaitin leat (nó nár thaitin leat) = 6 marc']),
]
PROSE_B = [
    ('P-B-a-1', 'prose-roghnach-a-1', 'Prós Roghnach (a) · Scéal béaloidis', [
        '(i) Maidir le scéal béaloidis a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar dhuine amháin de na carachtair ann. (23 mharc)',
        'Ní mór teideal an scéil sin a scríobh síos go soiléir. (2 mharc)',
        '(ii) Déan cur síos gairid ar ghné amháin den scéal sin agus inis cén fáth ar thaitin (nó nár thaitin) sí leat. Is leor dhá fháth. (10 marc)'], [
        ('eolas-i', '(i) Eolas', 23, ['(i) Cuntas ar dhuine de na carachtair sa sliocht', '= 23 marc']),
        ('teideal', 'Teideal an scéil', 2, ['Teideal an scéil = 2 marc']),
        # The scheme prints (i)'s total with its title, “= 25 mharc”, after the title line: (ii) is its own two lines.
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) An Ghné den scéal is mó a thaitin leat. Cur síos gairid 3 + 3 = 6 marc',
                                        'Fáth ar/nár thaitin sí leat 2 + 2 = 4 marc'])]),
    # The scheme restates the short story's (i) as “Cuntas ar an mothúchán is láidre sa ghearrscéal” (the paper asks for the main
    # events) and misprints “ghearrrscéil”: kept as printed, and the card says so.
    ('P-B-a-2', 'prose-roghnach-a-2', 'Prós Roghnach (a) · Gearrscéal', [
        '(i) Maidir le gearrscéal a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (rudaí) a tharla sa ghearrscéal sin. (23 mharc)',
        'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)',
        '(ii) Déan cur síos gairid ar charachtar amháin sa ghearrscéal sin agus inis cén fáth ar thaitin (nó nár thaitin) sé leat. Is leor dhá fháth. (10 marc)'], [
        ('eolas-i', '(i) Eolas', 23, ['(i) Cuntas ar an mothúchán is láidre sa ghearrscéal = 23 marc']),
        ('teideal', 'Teideal + ainm an údair', 2, ['Teideal an ghearrrscéil/ ainm an údair. = 2 marc']),
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) Pearsa a thaitin(nó nár thaitin)leat. Dhá fháth ar/nár thaitin sé leat. 5 + 5 = 10 marc'])]),
]
PROSE_B_B = ('P-B-b', 'prose-roghnach-b', 'Prós Roghnach (b) · Téama nó dhá rud', [
    '(i) Maidir leis na saothair eile a ndearna tú staidéar orthu le linn do chúrsa, agus nár úsáid tú i gcuid (a) thuas, roghnaigh saothar amháin díobh a bhfuil ceann amháin de na téamaí seo a leanas i gceist ann.',
    'Tabhair cuntas gairid ar a bhfuil sa saothar faoin téama atá roghnaithe agat.', THEMES + ' (18 marc)',
    'Ní mór teideal an tsaothair sin, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)',
    'NÓ',
    '(ii) Maidir leis na saothair eile a ndearna tú staidéar orthu le linn do chúrsa, agus nár úsáid tú i gcuid (a) thuas, roghnaigh saothar amháin díobh.',
    'Tabhair cuntas gairid ar dhá rud ann, rud amháin a thaitin leat agus rud amháin nár thaitin leat. (18 marc)',
    'Ní mór teideal an tsaothair sin, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)'], [
    ('eolas', 'Eolas', 18, ['(i) Cuntas gairid ar a bhfuil i gceann amháin de na saothair eile nár úsáid tú i gcuid (a) faoin téama atá roghnaithe agat as na téamaí atá luaite. 9 + 9 = 18 marc',
                            'NÓ', '(ii) Cuntas gairid ar dhá rud i gceann amháin de na saothair eile nár úsáid tú i gcuid (a). Rud amháin a thaitin leat agus rud amháin nár thaitin. = 9 marc × 2 = 18 marc']),
    ('teideal', 'Teideal + ainm an údair', 2, ['Teideal an tsaothair /ainm an údair = 2 marc'])])
POETRY_B = [
    ('F-B-a-1', 'poetry-roghnach-a-1', 'Filíocht Roghnach (a) · Dán nua-aimseartha a chum bean', [
        ('i', '(i) Maidir le dán nua-aimseartha amháin a chum bean agus a ndearna tú staidéar air le linn do chúrsa, inis i d’fhocail féin, cad is téama don dán sin, dar leat. (8 marc)', 8,
         ['(i) Téama i d’fhocail féin.', '= 8 marc']),
        ('ii', '(ii) Roghnaigh dhá íomhá (pictiúr) a úsáideann an file sa dán seo agus déan cur síos orthu i d’fhocail féin. (8 marc)', 8,
         ['(ii) Cur síos i d’fhocail féin ar dhá íomhá = 4 marc × 2 = 8 marc']),
        ('iii', '(iii) An dóigh leat go bhfuil teideal an dáin seo oiriúnach? Cuir fáth amháin le do fhreagra. (8 marc)', 8,
         ['(iii) Teideal an dáin oiriúnach? = 4 marc', 'Fáth amháin le do fhreagra = 4 marc']),
        ('iv', '(iv) Ar thaitin an dán leat? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (9 marc)', 9,
         ['(iv) Ar thaitin an dán leat? = 1 marc', 'Dhá fháth. = 4 marc × 2 = 8 marc'])],
     'Teideal an dáin/file a chum. = 2 mharc'),
    ('F-B-a-2', 'poetry-roghnach-a-2', 'Filíocht Roghnach (a) · Dán nua-aimseartha a chum fear nó bean', [
        ('i', '(i) Maidir le dán nua-aimseartha amháin a chum fear nó bean agus a ndearna tú staidéar air le linn do chúrsa, inis cén mothúchán is mó atá sa dán, dar leat. Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (8 marc)', 8,
         ['(i) Mothúchán is mó.', '= 2 marc', 'Dhá fháth. 3 marc × 2 = 6 marc']),
        # The scheme numbers this “(iv)” and prices a reason the paper does not ask for (“Fáth amháin le do fhreagra = 4 marc”): the
        # slice leaves out the misprinted number, and the card says so.
        ('ii', '(ii) An dóigh leat go bhfuil teideal an dáin seo oiriúnach? (8 marc)', 8,
         ['Teideal an dáin oiriúnach? = 4 marc', 'Fáth amháin le do fhreagra = 4 marc']),
        ('iii', '(iii) Scríobh nóta gairid faoi rud amháin sa dán a bhí suimiúil, dar leat. (8 marc)', 8,
         ['(iii) Rud amháin sa dán a bhí suimiúil = 8 marc']),
        ('iv', '(iv) Ar thaitin an dán seo leat? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (9 marc)', 9,
         ['(iv) Ar thaitin an dán leat? = 1 marc', 'Dhá fháth. = 4 marc × 2 = 8 marc'])],
     'Teideal an dáin/ainm an fhile. = 2 marc'),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go soiléir. (2 mharc)'
POETRY_B_B = [
    ('F-B-b-i', 'poetry-roghnach-b-i', 'Filíocht Roghnach (b)(i) · Mothúchán', [
        '(i) Maidir leis na dánta eile a ndearna tú staidéar orthu le linn do chúrsa, agus nár úsáid tú i gcuid (a) thuas, roghnaigh dán amháin díobh a chum bean. Tabhair cuntas gairid ar cheann amháin de na mothúcháin seo a leanas mar a léirítear é sa dán a roghnaigh tú.',
        EMOTIONS + ' (18 marc)', TITLE_LINE],
     ['(i) Cuntas gairid ar a bhfuil i ndán a chum bean agus nár úsáid tú i gcuid (a) faoi mhothúchán amháin atá roghnaithe agat as na mothúcháin atá luaite. (9 + 9) = 18 marc'],
     'Teideal an dáin/ainm an fhile = 2 marc'),
    ('F-B-b-ii', 'poetry-roghnach-b-ii', 'Filíocht Roghnach (b)(ii) · Príomhsmaoineamh agus íomhá', [
        '(ii) Maidir leis na dánta eile a ndearna tú staidéar orthu le linn do chúrsa, agus nár úsáid tú i gcuid (a) thuas, roghnaigh dán amháin díobh a chum bean. Tabhair cuntas gairid ar phríomhsmaointe an dáin sin agus ar íomhá (pictiúr) sa dán a thaitin (nó nár thaitin) leat. (18 marc)',
        TITLE_LINE],
     ['(ii) Cuntas gairid ar phríomhsmaoineamh an dáin a chum bean agus nár úsáid tú i gcuid (a). = 12 marc',
      'Cuntas gairid ar íomhá a thaitin/nár thaitin leat = 6 marc'],
     'Teideal an dáin/ainm an fhile = 2 marc'),
]

_MATERIAL = None


def material():
    global _MATERIAL
    if _MATERIAL:
        return _MATERIAL
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/{YEAR}/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/{YEAR}/{SCHEME_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_SHA, 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == SCHEME_SHA, 'Scheme changed: repeat visual review'
    paper, doc = fitz.open(paper_path), fitz.open(scheme_path)
    assert len(paper) == 8 and len(doc) == 12
    texts = [clean(p.get_text()) for p in paper]
    stext = [clean(page_text(doc[p - 1])) for p in range(1, 13)]
    scheme = ' '.join(re.sub(r'^\d+\s', '', stext[p - 1]) for p in range(5, 10))
    assert not PUA.search(scheme), 'private-use glyph left in the scheme text'
    assert not re.search(r'Freagraí|Freagra:|Samplaí|samplacha|féideartha|Catagóir|Sármhaith|•', scheme)
    # Every guidance slice is the scheme's text, in print order within its question.
    slices = [g for card in PROSE_A for *_, crits in [card] for c in crits for g in c[3]]
    slices += [line for card in PROSE_A_B for line in [card[4]]]
    slices += [g for card in POETRY_A for sub in card[4] for g in sub[3]]
    slices += [g for card in POETRY_A_B for g in card[4]]
    slices += [g for card in PROSE_B for c in card[4] for g in c[3]] + [g for c in PROSE_B_B[4] for g in c[3]]
    slices += [g for card in POETRY_B for sub in card[3] for g in sub[3]] + [card[4] for card in POETRY_B]
    slices += [g for card in POETRY_B_B for g in card[4]] + [card[5] for card in POETRY_B_B]
    for g in slices:
        assert g in scheme, ('not in the scheme', g)
    # The language deductions, as printed: 0–5 under each poetry (a), 0–3 under each (b) (the poetry two with a hyphen), and none
    # under either prose (a): six in all.
    assert scheme.count(LANG_A) == 2 and scheme.count(LANG_B) == 2 and scheme.count(LANG_B_HYPHEN) == 2, (scheme.count(LANG_A), scheme.count(LANG_B))
    assert scheme.count('[Gaeilge lochtach') == 6
    prose_a = scheme[scheme.index('CEIST 1 - PRÓS AINMNITHE -'):scheme.index('(b) Cuntas gairid ar a bhfuil i gceann amháin de na saothair a luadh')]
    prose_b_a = scheme[scheme.index('CEIST 1 - PRÓS ROGHNACH -'):scheme.index('(b) (i) Cuntas gairid ar a bhfuil i gceann amháin de na saothair eile')]
    assert 'Gaeilge lochtach' not in prose_a and 'Gaeilge lochtach' not in prose_b_a
    # Question lines, as printed.
    for page, lines in [(2, [l for card in PROSE_A for l in card[4]] + [l for card in PROSE_A_B for l in card[3]]),
                        (5, [l for card in PROSE_B for l in card[3] if l != 'NÓ'] + [l for l in PROSE_B_B[3] if l != 'NÓ']),
                        (4, [l for card in POETRY_A_B for l in card[3]]),
                        (6, [sub[1] for card in POETRY_B for sub in card[3]] + [l for card in POETRY_B_B for l in card[3]] + [TITLE_LINE])]:
        for line in lines:
            assert in_order(line, texts[page - 1]), (page, line[:60])
    for key, slug, title, page, subs in POETRY_A:
        assert title in texts[page - 1], key
        for label, lines, marks, _ in subs:
            assert in_order(f'({label}) ' + ' '.join(lines) + f' ({marks} marc)', texts[page - 1]), (key, label)
    for page, line in [(1, WHOLE), (1, PROSE_CHOICE), (1, POETRY_CHOICE), (2, BOTH), (3, BOTH), (5, BOTH), (6, BOTH), (2, SEE_PAGE_1), (5, SEE_PAGE_1)]:
        assert comparable(line) in comparable(texts[page - 1]), (page, line)
    for key, box in BOX.items():
        for line in box.splitlines():
            assert comparable(line) in comparable(' '.join(texts)), (key, line)
    assert texts[6:] == ['Lch 7 de 8 Leathanach Bán', 'Lch 8 de 8 Leathanach Bán'], texts[6:]
    _MATERIAL = dict(paper=paper, texts=texts, decisions=selection_decisions(paper))
    return _MATERIAL


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, src, stem, notice=None, focus=None):
        cards.append(dict(
            id=f'irish-{YEAR}-ol-p2-{slug}', year=YEAR, level='ordinary', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'{YEAR} OL Paper 2 {ref}', stem=stem, questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria if c['kind'] == 'award'), topicId=topic,
            conceptId=f'irish-ol-p2-{slug}', paperFileid=FILE, paperPage=pages[0], schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=requirements, criteria=criteria, markingGuideNote=note, sourceMaterial=src,
            **({'sourceDiscrepancyNotice': notice} if notice else {}), **({'practiceFocus': focus} if focus else {})))

    question_ids, practice_ids = [], []
    prose_req = [WHOLE, PROSE_CHOICE, BOTH] + LIT
    poetry_req = [WHOLE, POETRY_CHOICE, BOTH] + LIT
    tariff_note = ('The scheme prints each price, and some splits, but no answers or sample points: each row is the scheme’s restatement '
                   'of the ask, claimed at its printed price or the totals its printed parts make. ' + UNPRINTED_ANSWER)
    no_deduction = ('The scheme prints no language deduction under this (a): its Nóta after the question names one for (a) but prints '
                    'no range, so none is shown.')

    # ---- Roinn A Ceist 1: Prós Ainmnithe ------------------------------------------------------------------------------
    for key, slug, ref, page, lines, crits in PROSE_A:
        criteria = [criterion(cid, label, marks, guide) for cid, label, marks, guide in crits]
        split = 'two reasons 2 × 2' if key != 'P-A-a-2' else 'the reasons 4'
        add(key, slug, ref, '(a)\n' + '\n'.join(lines), 'irish-4-7', [page], [5],
            criteria, prose_req, f'One complete SEC response at 35: (i) 25 and (ii) 10 (the character 3 + 3 and {split}). {tariff_note} '
            f'{no_deduction}', source('Prós Ainmnithe', ref.split(' · ')[1], [page]), BOX['PA'])
        question_ids.append(cards[-1]['id'])
        for (cid, label, marks, guide), sub in zip(crits, ['i', 'ii']):
            sub_lines = [l for l in lines if l.startswith(f'({sub}) ')]
            start = lines.index(sub_lines[0])
            end = next((i for i, l in enumerate(lines) if i > start and re.match(r'\((?:i|ii)\) ', l)), len(lines))
            add(f'{key}-{sub}', f'{slug}-{sub}', f'{ref} · ({sub})', '(a)\n' + '\n'.join(lines[start:end]), 'irish-4-7', [page], [5],
                [criterion('eolas', 'Eolas', marks, guide)], [WHOLE, PROSE_CHOICE, BOTH] + LIT[1:],
                f'One printed sub-question at its published tariff ({marks}). {tariff_note} {no_deduction}',
                source('Prós Ainmnithe', ref.split(' · ')[1], [page]), BOX['PA'])
            practice_ids.append(cards[-1]['id'])
    for key, slug, ref, lines, guide in PROSE_A_B:
        add(key, slug, ref, '(b)\n' + '\n'.join(lines), 'irish-4-7', [2], [6],
            [criterion('eolas', 'Eolas', 20, [guide]), deduction(LANG_B, 3)], prose_req,
            f'One complete SEC response at 20, then the 0–3 Gaeilge deduction once. {tariff_note}',
            source('Prós Ainmnithe', ref.split(' · ')[0], [2]), BOX['PA'])
        question_ids.append(cards[-1]['id'])

    # ---- Roinn A Ceist 2: Filíocht Ainmnithe ----------------------------------------------------------------------------
    for key, slug, title, page, subs in POETRY_A:
        scheme_pages = [6] if key == 'F-A-a-1' else [6, 7]
        criteria = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, guide) for label, lines, marks, guide in subs] + [deduction(LANG_A, 5)]
        prompt = f'(a) {title}\n' + '\n'.join(f'({label}) ' + '\n'.join(lines) + f' ({marks} marc)' for label, lines, marks, _ in subs)
        add(key, slug, f'Filíocht Ainmnithe (a) · {title}', prompt, 'irish-5-6', [page], scheme_pages, criteria, poetry_req,
            'One complete SEC response at 35: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs) + ', then the 0–5 Gaeilge '
            f'deduction once. The four questions of (i) and the three of (iii) are priced together. {tariff_note}',
            source('Filíocht Ainmnithe', title, [page]), BOX['FA'])
        question_ids.append(cards[-1]['id'])
        for label, lines, marks, guide in subs:
            add(f'{key}-{label}', f'{slug}-{label}', f'Filíocht Ainmnithe (a) · {title} · ({label})',
                f'(a) {title}\n({label}) ' + '\n'.join(lines) + f' ({marks} marc)', 'irish-5-6', [page], scheme_pages,
                [criterion('eolas', 'Eolas', marks, guide)], [WHOLE, POETRY_CHOICE, BOTH] + LIT[1:],
                f'One printed sub-question at its published tariff ({marks}). {tariff_note} The 0–5 Gaeilge deduction applies once to the '
                'whole 35-mark answer, never inside one sub-question.', source('Filíocht Ainmnithe', title, [page]), BOX['FA'])
            practice_ids.append(cards[-1]['id'])
    for key, slug, ref, lines, guide in POETRY_A_B:
        add(key, slug, ref, '(b)\n' + '\n'.join(lines), 'irish-5-6', [4], [7],
            [criterion('eolas', 'Eolas', 20, guide), deduction(LANG_B_HYPHEN, 3)], poetry_req,
            f'One complete SEC response at 20, then the 0–3 Gaeilge deduction once. {tariff_note}', source('Filíocht Ainmnithe', GEALT, [4]),
            BOX['FA'])
        question_ids.append(cards[-1]['id'])

    # ---- Roinn B Ceist 1: Prós Roghnach -------------------------------------------------------------------------------------
    for key, slug, ref, lines, crits in PROSE_B:
        criteria = [criterion(cid, label, marks, guide) for cid, label, marks, guide in crits]
        folk = key == 'P-B-a-1'
        notice = None if folk else (
            'Source note: the scheme restates (i) as “Cuntas ar an mothúchán is láidre sa ghearrscéal” (an account of the strongest emotion '
            'in the short story) where the paper asks for the main events of the short story; the price (23) is the same. The criterion '
            'carries the scheme’s words. See both sources.')
        parts = ('(i) 23, the title 2, (ii) 10 (the feature 3 + 3 and the reasons 2 + 2)' if folk
                 else '(i) 23, the title and writer 2, (ii) 10 (5 + 5)')
        add(key, slug, ref, '(a)\n' + '\n'.join(lines), 'irish-4-7', [5], [7] if folk else [8], criteria, prose_req,
            f'One complete SEC response at 35: {parts}. {tariff_note} The text is open content chosen by the candidate. '
            'The scheme prints no language deduction under this (a): its Nóta after the question names one for (a) but prints no range, '
            'so none is shown.', source('Prós Roghnach', ref.split(' · ')[1], [5]), BOX['PB'], notice=notice)
        question_ids.append(cards[-1]['id'])
    key, slug, ref, lines, crits = PROSE_B_B
    add(key, slug, ref, '(b)\n' + '\n'.join(lines), 'irish-4-7', [5], [8],
        [criterion(cid, label, marks, guide) for cid, label, marks, guide in crits] + [deduction(LANG_B, 3)], prose_req,
        f'One complete SEC response at 20: the account 18 (9 + 9, or 9 × 2 for two things) and the title and author 2, then the 0–3 '
        f'Gaeilge deduction once. {tariff_note}', source('Prós Roghnach', 'Prós Roghnach (b)', [5]), BOX['PB'])
    question_ids.append(cards[-1]['id'])

    # ---- Roinn B Ceist 2: Filíocht Roghnach ---------------------------------------------------------------------------------
    for key, slug, ref, subs, title_guide in POETRY_B:
        criteria = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, guide) for label, _, marks, guide in subs]
        criteria += [criterion('teideal', 'Teideal + ainm an fhile', 2, [title_guide]), deduction(LANG_A, 5)]
        notice = None
        if key == 'F-B-a-2':
            notice = ('Source note: the scheme numbers this option’s (ii) “(iv)” and prices it “Teideal an dáin oiriúnach? = 4 marc” and '
                      '“Fáth amháin le do fhreagra = 4 marc”, where the paper asks only whether the title suits the poem (8 marks). The '
                      'criterion carries the scheme’s prices. See both sources.')
        add(key, slug, ref, '(a)\n' + '\n'.join(text for _, text, _, _ in subs) + '\n' + TITLE_LINE, 'irish-5-6', [6],
            [8] if key == 'F-B-a-1' else [9], criteria,
            poetry_req, 'One complete SEC response at 35: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs) +
            f', the poem and poet 2, then the 0–5 Gaeilge deduction once. {tariff_note} The poem is open content chosen by the candidate.',
            source('Filíocht Roghnach', ref.split(' · ')[1], [6]), BOX['FB'], notice=notice)
        question_ids.append(cards[-1]['id'])
    for key, slug, ref, lines, guide, title_guide in POETRY_B_B:
        add(key, slug, ref, '(b)\n' + '\n'.join(lines), 'irish-5-6', [6], [9],
            [criterion('eolas', 'Eolas', 18, guide), criterion('teideal', 'Teideal + ainm an fhile', 2, [title_guide]),
             deduction(LANG_B_HYPHEN, 3)], poetry_req,
            f'One complete SEC response at 20: the account 18 and the poem and poet 2, then the 0–3 Gaeilge deduction once. {tariff_note}',
            source('Filíocht Roghnach', ref.split(' · ')[0], [6]), BOX['FB'])
        question_ids.append(cards[-1]['id'])

    assert len(question_ids) == 16 and len(practice_ids) == 14, (len(question_ids), len(practice_ids))
    assert len(cards) == 30 and len({c['id'] for c in cards}) == 30 and len({c['atlasQuestionId'] for c in cards}) == 30
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria'] if c['kind'] == 'award') == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not PUA.search(g) for g in c['guidance']), (card['id'], c['id'])
    # Each question card is the printed 35 or 20.
    assert sorted({c['totalMarks'] for c in cards if c['id'] in question_ids}) == [20, 35]
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=YEAR, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 9)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  # Before 2012 the reading is on Páipéar I (irish_ordinary_2010_p1.py): this paper has no whole reading question.
                  practiceCardIds=practice_ids, questionCardIds=question_ids, readingWholeCardIds=[],
                  examStructure=dict(prose=55, poetry=55, total=110),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  choicePolicy=('Choice is not a route: prose and poetry are each the prescribed or the optional course, and each question prints '
                                '(a) and (b), both answered; every printed option is one card unless the scheme marks the options alike (Prós '
                                'Roghnach (b)), where one card carries both; no combination cards.'),
                  boundaries=('16 question cards (Prós Ainmnithe (a) x3, (b) x2; Filíocht Ainmnithe (a) x2, (b) x2; Prós Roghnach (a) x2, (b); '
                              'Filíocht Roghnach (a) x2, (b) x2) and 14 practice cards (every prescribed-course (a) sub-question).'))
    return dict(review=review, cards=cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    scheme_words_in(data)  # guidance, question and task checks carry the SEC's words only (irish_lifted.py)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.exists() and OUT.read_text() == content, f'Stale output: {OUT}'
    else:
        OUT.write_text(content)
    print(f"Irish Ordinary {YEAR} Paper 2: {len(data['cards'])} reviewed cards (16 printed questions, 14 practice parts); the archive remains incomplete.")


if __name__ == '__main__':
    main()
