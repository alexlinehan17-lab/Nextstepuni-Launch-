#!/usr/bin/env python3
"""Reviewed 2011 Ordinary Páipéar II (Litríocht), carded new.

Paper PDF 1–8 (LC001GLP200IV: instructions on page 1; Roinn A Cúrsa Ainmnithe on 2–5, Ceist 1 Prós Ainmnithe on 2,
Ceist 2 Filíocht Ainmnithe on 3–5 with its poems; Roinn B Cúrsa Roghnach on 6–7; page 8 “Leathanach Bán”) and the
Páipéar II pages of the combined LC001GLP000IV scheme (PDF 5–9) reviewed on 2026-11-05. Counts are assertions, not
corpus-completeness proof.

Páipéar II (110) before 2012 is literature only: “Freagair Ceist Iomlán, ( (a) agus (b) ), sa Phrós agus san
Fhilíocht.” Prose is the prescribed course (Roinn A Ceist 1) or the optional course (Roinn B Ceist 1), poetry likewise
(Roinn A Ceist 2 or Roinn B Ceist 2); each question is 55: (a) at 35 and (b) at 20, both answered. The scheme prints no
answers or sample points anywhere: each sub-question restated with its price, some prices split (“Cur síos gairid air
3 + 3 = 6 marc”, “Dhá fháth = 2 mharc × 2 = 4 marc”, “2 + 9 + 9 = 20marc”, “(10 marc × 2) = 20 marc”). So every award is
`tariffOnly` (the chip says “Tariff”), its guidance the scheme's restatement and price, and each language deduction is
its own criterion as printed (0–5 under each (a), 0–3 under each (b)).

Cards (choice is not a route; a printed choice is one card unless the scheme marks the options differently or they are
different prescribed works):
- Prós Ainmnithe (a): the three prescribed works (Fiche Blian ag Fás, Clare sa Spéir, Lá Buí Bealtaine), a card each;
  (b) (i) a theme in one of the other works, whole at 20, and (ii) two things in one, 10 × 2: priced differently, a card
  each.
- Filíocht Ainmnithe (a): the two prescribed poems (Gealt?, Bímse Buan ar Buairt Gach Ló), a card each, (i)–(iv) as
  printed; (b) on Faoiseamh a Gheobhadsa: (i) 2 + 9 + 9 and (ii) 7 + 7 + 6, a card each.
- Prós Roghnach (a): the autobiography extract, priced (i) 23 + title 2 and (ii) “Cur síos gairid 5 + 5”, and the film
  or the play, both priced (i) 23 + title 2 and (ii) “Dhá fháth … 5 + 5”: two cards (the film and the play are marked
  alike: one card carrying both); (b) (i) a theme (9 + 9) or (ii) two characters (9 × 2), each + title 2, marked alike:
  one card.
- Filíocht Roghnach (a): a modern poem by a woman ((i)–(iv), title) or by a woman or a man ((i)–(iv), title), priced
  differently: a card each; (b) (i) 9 + 9 + title or (ii) 12 + 6 + title: a card each.
- Practice cards: every prescribed-course (a) sub-question at its own printed price (the prose (i) and (ii), the poems'
  (i)–(iv)).

Two places where the paper and the scheme print different prices are kept as each prints them: Filíocht Roghnach (a)'s
first option prints “(7 marc)” for (iii) and “(10 marc)” for (iv), where the scheme prices them 8 (4 + 4) and 9 (1 + 4 × 2);
the criteria carry the scheme's prices (the same 17) and the card says so. The scheme prints the play's (i) price “= 23
marc” beside (ii)'s first line and the autobiography's (i)+title total “= 25 mharc” beside its (ii): both are read
where the arithmetic and the paper put them ((i) 23; (ii) 10). Permitted marks are the totals the printed prices make
(`printed_marks`): a price claimed whole is 0 or all of it.

No 2011 Ordinary card existed before. The 2011 Atlas files Páipéar II under the pre-2012 keys P-A, P-B, F-A, F-B; the
card keys extend them (P-A-a-1 …), which do not clash. `main` writes the card file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2011
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2011-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2011-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '8cca86282ac3c573b669dc23ff297808f2f8da68afaa81467bbfa13a2d43765f'
SCHEME_SHA = '6e73ff5b1d21c777f7d39b3731cb7d7e6b0156fe6043c00f4fea9291032e0ad3'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'  # types/markBank.ts
# The scheme's SymbolMT glyphs: U+F0B4 (×, PDF 3, 5, 6, 8, 9) and U+F0B7 (•, PDF 11).
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
    # The 2011 Ordinary scheme prints only the tariff of every literature ask, no answer: each award but the language
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


# Printed lines (paper PDF 1–7).
PROSE_CHOICE = 'Tá rogha ann idir an Cúrsa Ainmnithe (leathanach 2) agus an Cúrsa Roghnach (leathanach 6).'
POETRY_CHOICE = 'Tá rogha ann idir an Cúrsa Ainmnithe (leathanach 3, 4 agus 5) agus an Cúrsa Roghnach (leathanach 7).'
WHOLE = 'Freagair Ceist Iomlán, ( (a) agus (b) ), sa Phrós agus san Fhilíocht.'
BOTH = 'Freagair (a) agus (b) anseo.'
BOX = {'PA': 'ROINN A – CÚRSA AINMNITHE –\nCEIST 1 – PRÓS AINMNITHE – [55 mharc]',
       'FA': 'CEIST 2 – FILÍOCHT AINMNITHE – [55 mharc]',
       'PB': 'ROINN B – CÚRSA ROGHNACH –\nCEIST 1 – PRÓS ROGHNACH – [55 mharc]',
       'FB': 'CEIST 2 – FILÍOCHT ROGHNACH – [55 mharc]'}
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
OTHER_WORKS = ('Maidir leis na saothair eile a ndearna tú staidéar orthu le linn do chúrsa, Lig Sinn i gCathú, An Bhean Óg / '
               'Coileach Ghleann Phádraig agus An Cearrbhach Mac Cába, roghnaigh saothar amháin díobh')

# Each guidance slice is the scheme's text in print order. A slice leaves out the work's bracketed name printed before a price
# (“(Fiche Blian ag Fás) = 25 marc”, “(Dírbheathaisnéis)”, “(Dán nua a chum bean)”, “(Dráma)”), a brace's total printed beside the
# heading between the two rows it totals (“Fáth ar/nár thaitin sé leat. = 10 marc” between the 6 and the 4), and the braces
# themselves: the card names the work and the criterion is the total, so each price reads with the ask it prices. Alternatives
# the scheme marks alike keep its “NÓ” between them (tariffs.ts reads each on its own).
PROSE_A = [
    ('P-A-a-1', 'prose-ainmnithe-a-1', 'Prós Ainmnithe (a) · Fiche Blian ag Fás', 2, [
        '(i) “ ‘An bhfuil a fhios agat cad a cheannóm?’ arsa Tomás i gcogar liom.” (Fiche Blian ag Fás)',
        'Tabhair cuntas ar ar tharla ina dhiaidh sin sa scéal go dtí gur fhág na buachaillí an teach tábhairne. (25 mharc)',
        '(ii) Cén sórt duine é Tomás dar leat? Déan cur síos gairid air.',
        'Abair cén fáth ar thaitin (nó nár thaitin) sé leat. (Is leor dhá fháth.) (10 marc)'], [
        ('eolas-i', '(i) Eolas', 25, ['(i) Cuntas ar an am a chaith na buachaillí sa teach tábhairne.', '= 25 marc']),
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) An sórt duine é Tomás, dar leat. Cur síos gairid air 3 + 3 = 6 marc',
                                        'Fáth ar/nár thaitin sé leat.', 'Dhá fháth = 2 mharc × 2 = 4 marc'])]),
    ('P-A-a-2', 'prose-ainmnithe-a-2', 'Prós Ainmnithe (a) · Clare sa Spéir', 2, [
        '(i) Tabhair cuntas ar ar tharla sa ghearrscannán Clare sa Spéir ó d’fhág Eoin an teach an chéad mhaidin go dtí deireadh an scannáin. (25 mharc)',
        '(ii) Cén sórt duine í Clare dar leat? Déan cur síos gairid uirthi.',
        'Abair cén fáth ar thaitin (nó nár thaitin) sí leat. (Is leor dhá fháth.) (10 marc)'], [
        ('eolas-i', '(i) Eolas', 25, ['(i) Cuntas ar ar tharla ó d’fhág Eoin an teach go dtí an deireadh.', '= 25 marc']),
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) An sórt duine í Clare sa scannán, dar leat. Cur síos gairid uirthi. 3 + 3 = 6 marc',
                                        'Fáth ar/nár thaitin sí leat.', 'Dhá fháth = 2 marc × 2 = 4 marc'])]),
    ('P-A-a-3', 'prose-ainmnithe-a-3', 'Prós Ainmnithe (a) · Lá Buí Bealtaine', 2, [
        '(i) ‘Buachaillí óga agus cailíní óga ag obair ar an bportach. Spórt agus gáirí acu.’ (Lá Buí Bealtaine)',
        'Tabhair cuntas ar ar tharla idir Nóinín agus Peadar an samhradh sin nuair a bhí siad óg. (25 mharc)',
        '(ii) Cén sórt duine é Páid Ó Sé (fear a bhí i ngrá le Nóinín), dar leat?',
        'Déan cur síos gairid air. Abair cén fáth ar thaitin (nó nár thaitin) sé leat. (Is leor dhá fháth.) (10 marc)'], [
        ('eolas-i', '(i) Eolas', 25, ['(i) Cuntas ar ar tharla idir Nóinín agus Peadar agus iad óg.', '= 25 mharc']),
        # The scheme prints “Páid ó Sé” and “Fáth ar/nár thaitin ?”: kept as printed.
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) An sórt duine é Páid ó Sé, dar leat. Cur síos gairid air 3 + 3 = 6 marc',
                                        'Fáth ar/nár thaitin ?', 'Dhá fháth = 2 marc × 2 = 4 marc'])]),
]
PROSE_A_B = [
    ('P-A-b-i', 'prose-ainmnithe-b-i', 'Prós Ainmnithe (b)(i) · Téama', [
        f'(i) {OTHER_WORKS} a bhfuil ceann amháin de na téamaí seo a leanas i gceist ann.',
        'Tabhair cuntas gairid ar a bhfuil sa saothar faoin téama atá roghnaithe agat.',
        'saol na tuaithe\ngrá (nó fuath)\ngliceas\nuaigneas\ndraíocht\nsaol na hollscoile (20 marc)'],
     'Cuntas gairid ar a bhfuil i gceann amháin de na saothair a luadh faoin téama atá roghnaithe agat as na téamaí atá luaite. = 20 marc'),
    ('P-A-b-ii', 'prose-ainmnithe-b-ii', 'Prós Ainmnithe (b)(ii) · Dhá rud', [
        f'(ii) {OTHER_WORKS}. Tabhair cuntas gairid ar dhá rud ann, rud amháin a thaitin leat agus rud amháin nár thaitin leat. (20 marc)'],
     'Cuntas gairid ar dhá rud i gceann amháin de na saothair a luadh, Rud amháin a thaitin leat agus rud amháin nár thaitin leat. (10 marc × 2) = 20 marc'),
]
POETRY_A = [
    ('F-A-a-1', 'poetry-ainmnithe-a-1', 'Gealt?', 3, [
        ('i', ['(a) Cár shuigh an ghealt ar an mbus? (Gealt? thíos)', '(b) Cad a rinne na Gardaí i Ráth Fearnáin?', '(c) Cá raibh an rúnaí ag dul?',
               '(d) Cén duine a d’aithin an Ghealt nuair a stad an bus?'], 8,
         ['(i) (a) Cár shuigh an ghealt ar an mbus? (Gealt?) (b) Cad a rinne na Gardaí i Ráth Fearnáin? (c) Cá raibh an rúnaí ag dul? '
          '(d) Cén duine a d’aithin an ghealt nuair a stad an bus? = 8 marc']),
        ('ii', ['Luaigh dhá íomhá (pictiúr) atá sa dán. Déan cur síos i d’fhocail féin ar an dá íomhá (pictiúr) sin sa dán.'], 8,
         ['(ii) Luaigh dhá íomhá (pictiúr) atá sa dán. Déan cur síos i d’fhocail féin ar an dá íomhá sin sa dán. = 8 marc']),
        ('iii', ['(a) Conas a léirigh an bhean óg go raibh sí an-neirbhíseach?', '(b) Cad a bhí ag na dochtúirí nuair a tháinig siad go dtí an bus?',
                 '(c) Cén fáth a raibh an rúnaí chomh buartha sin?'], 9,
         ['(iii) (a) Conas a léirigh an bhean óg go raibh sí an - neirbhíseach? (b) Cad a bhí ag na dochtúirí nuair a tháinig siad go dtí an bus? '
          '(c) Cén fáth a raibh an rúnaí chomh buartha sin? = 9 marc']),
        ('iv', ['An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)'], 10,
         ['(iv) An maith leat an dán seo? = 2 marc', 'Dhá fháth. = 4 marc × 2 = 8 marc'])]),
    ('F-A-a-2', 'poetry-ainmnithe-a-2', 'Bímse Buan ar Buairt Gach Ló', 4, [
        # The scheme reprints (i)(a) as “Cén fáth a raibh an file ag gol?” (the paper: “a bhfuil”) and (iii) with “tré chéile”
        # (the paper: “trína chéile”): kept as printed.
        ('i', ['(a) Cén fáth a bhfuil an file ag gol? (Bímse Buan ar Buairt Gach Ló thíos)', '(b) Conas atá a fhios agat nár chodail an file?',
               '(c) Cé eile atá brónach?', '(d) Cén t-ainm a thugann an file ar a laoch?'], 8,
         ['(i) (a) Cén fáth a raibh an file ag gol? (Bímse Buan ar Buairt Gach Ló) (b) Conas atá fhios agat nár chodail an file? (c) Cé eile atá '
          'brónach? (d) Cén t-ainm a thugann an file ar a laoch? = 8 marc']),
        ('ii', ['Luaigh dhá mhothúchán atá sa dán.', 'Déan cur síos, i d’fhocail féin, ar an dá mhothúchán sin sa dán.'], 8,
         ['(ii) Luaigh dhá mhothúchán atá sa dán. Déan cur síos, i d’fhocail féin, ar an dá mhothúchán sin sa dán. = 8 marc']),
        ('iii', ['Luaigh trí rud sa dán a thaispeánann go raibh an dúlra trína chéile.'], 9,
         ['(iii) Luaigh trí rud a thaispeánann go raibh an dúlra tré chéile. = 9 marc']),
        ('iv', ['Ar thaitin an dán seo leat? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)'], 10,
         ['(iv) Ar thaitin an dán leat? = 2 marc', 'Dhá fháth = 4 marc × 2 = 8 marc'])]),
]
FAOISEAMH = 'Faoiseamh a Gheobhadsa'
POETRY_A_B = [
    ('F-A-b-i', 'poetry-ainmnithe-b-i', 'Filíocht Ainmnithe (b)(i) · Faoiseamh a Gheobhadsa · Mothúchán', [
        '(i) Maidir leis an dán Faoiseamh a Gheobhadsa (thíos), roghnaigh mothúchán amháin as an liosta seo a leanas agus tabhair cuntas gairid ar a bhfuil sa dán faoin mothúchán atá roghnaithe agat.',
        'sásamh/faoiseamh\ngrá\nuaigneas\nmíshásamh\nsíocháin\nbuairt aigne (20 marc)'],
     ['Cuntas gairid ar a bhfuil sa dán, Faoiseamh a Gheobhadsa faoin mothúchán atá roghnaithe agat as na mothúcháin atá luaite. 2 + 9 + 9 = 20marc']),
    # The paper prints “Gheobadsa” in (ii): kept as printed.
    ('F-A-b-ii', 'poetry-ainmnithe-b-ii', 'Filíocht Ainmnithe (b)(ii) · Faoiseamh a Gheobhadsa · Príomhsmaointe agus íomhá', [
        '(ii) Maidir leis an dán Faoiseamh a Gheobadsa (thíos), tabhair cuntas gairid ar phríomhsmaointe an dáin agus ar íomhá (pictiúr) amháin sa dán a thaitin go mór leat. (20 marc)'],
     ['Cuntas gairid ar phríomhsmaointe an dáin, Faoiseamh a Gheobhadsa 7 + 7 =14 marc', 'Íomhá a thaitin leat = 6 marc']),
]
PROSE_B = [
    ('P-B-a-1', 'prose-roghnach-a-1', 'Prós Roghnach (a) · Dírbheathaisnéis', [
        '(i) Maidir le sliocht as dírbheathaisnéis a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (rudaí) a tharla sa sliocht sin. (23 mharc)',
        'Ní mór teideal na dírbheathaisnéise sin, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)',
        '(ii) Déan cur síos gairid ar phearsa amháin a thaitin (nó nár thaitin) leat.',
        'Abair cén fáth ar thaitin (nó nár thaitin) sé/sí leat. (Is leor dhá fháth.) (10 marc)'], [
        ('eolas-i', '(i) Eolas', 23, ['(i) Cuntas ar na príomhimeachtaí sa sliocht', '= 23 marc']),
        ('teideal', 'Teideal + ainm an údair', 2, ['Teideal an tsaothair /ainm an údair = 2 marc']),
        # The scheme prints (i)'s total with its title, “= 25 mharc”, beside (ii)'s first line: (ii) is its own two lines.
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) Pearsa a thaitin (nó nár thaitin) leat.', 'Cur síos gairid 5+ 5 = 10 marc'])]),
    ('P-B-a-2', 'prose-roghnach-a-2', 'Prós Roghnach (a) · Gearrscannán nó dráma', [
        '(i) Maidir le gearrscannán a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar an eachtra is mó a thaitin (nó nár thaitin) leat sa ghearrscannán sin. (23 mharc)',
        'Ní mór teideal an ghearrscannáin sin, mar aon le hainm an stiúrthóra, a scríobh síos go soiléir. (2 mharc)',
        '(ii) Déan cur síos gairid ar phearsa (carachtar) amháin sa ghearrscannán sin a thaitin (nó nár thaitin) leat. (Is leor dhá fháth.) (10 marc)',
        'NÓ',
        '(i) Maidir le dráma a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (rudaí) a tharla sa dráma sin. (23 mharc)',
        'Ní mór teideal an dráma, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)',
        '(ii) Déan cur síos gairid ar phearsa (carachtar) amháin sa dráma sin a thaitin (nó nár thaitin) leat. (Is leor dhá fháth.) (10 marc)'], [
        # The scheme prints the play's (i) price “= 23 marc” beside (ii)'s first line (PDF 8): read with (i), where the paper prints
        # “(23 mharc)” and the option's 35 puts it. The film's title line misprints “ghearrrscannáin”: kept as printed.
        ('eolas-i', '(i) Eolas', 23, ['(i) Eachtra is mó a/nár thaitin leat sa ghearrscannán = 23 marc', 'NÓ',
                                      '(i) Cuntas ar na príomhimeachtaí a tharla sa dráma.', '= 23 marc']),
        ('teideal', 'Teideal + ainm', 2, ['Teideal an ghearrrscannáin/ ainm an stiúrthóra = 2 marc', 'NÓ', 'Teideal an dráma / ainm an údair. = 2 marc']),
        # The film's and the play's (ii) are priced in the same printed words: lifted once.
        ('eolas-ii', '(ii) Eolas', 10, ['(ii) Pearsa a thaitin (nó nár thaitin) leat. Dhá fháth ar/nár thaitin sé leat. 5 + 5 = 10 marc'])]),
]
PROSE_B_B = ('P-B-b', 'prose-roghnach-b', 'Prós Roghnach (b) · Téama nó dhá phearsa', [
    '(i) Maidir leis na saothair phróis eile a ndearna tú staidéar orthu le linn do chúrsa, agus nár úsáid tú i gcuid (a) thuas, roghnaigh saothar amháin díobh a bhfuil ceann amháin de na téamaí seo a leanas i gceist ann.',
    'Tabhair cuntas gairid ar a bhfuil sa saothar faoin téama atá roghnaithe agat.',
    'saol na tuaithe grá (nó fuath) gliceas\nuaigneas draíocht áthas (18 marc)',
    'Ní mór teideal an tsaothair sin, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)',
    'NÓ',
    '(ii) Maidir leis na saothair phróis eile a ndearna tú staidéar orthu le linn do chúrsa, agus nár úsáid tú i gcuid (a) thuas, roghnaigh saothar amháin díobh.',
    'Tabhair cuntas gairid ar dhá phearsa (carachtar) ann, pearsa (carachtar) amháin a thaitin leat agus pearsa (carachtar) amháin nár thaitin leat. (18 marc)',
    'Ní mór teideal an tsaothair sin, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)'], [
    ('eolas', 'Eolas', 18, ['(i) Cuntas gairid ar a bhfuil i gceann amháin de na saothair eile nár úsáid tú i gcuid (a) faoin téama atá roghnaithe agat as na téamaí atá luaite. 9 + 9 = 18 marc',
                            'NÓ', '(ii) Cuntas gairid ar dhá phearsa i gceann amháin de na saothair eile nár úsáid tú i gcuid (a). Pearsa amháin a thaitin leat agus pearsa amháin nár thaitin. = 9 marc × 2 = 18 marc']),
    ('teideal', 'Teideal + ainm an údair', 2, ['Teideal an tsaothair /ainm an údair = 2 marc'])])
POETRY_B = [
    ('F-B-a-1', 'poetry-roghnach-a-1', 'Filíocht Roghnach (a) · Dán nua-aimseartha a chum bean', [
        ('i', '(i) Maidir le dán nua-aimseartha amháin a chum bean agus a ndearna tú staidéar air le linn do chúrsa, inis i d’fhocail féin, cad is téama don dán sin, dar leat. (8 marc)', 8,
         ['(i) Téama i d’fhocail féin.', '= 8 marc']),
        ('ii', '(ii) Luaigh dhá íomhá (pictiúr) atá sa dán seo agus déan cur síos orthu i d’fhocail féin. (8 marc)', 8,
         ['(ii) Cur síos i d’fhocail féin ar dhá íomhá = 4 marc × 2 = 8 marc']),
        # The paper prints (iii) at 7 and (iv) at 10; the scheme prices them 8 (4 + 4) and 9 (1 + 4 × 2), the same 17: the criteria
        # carry the scheme's prices, and the card says so.
        ('iii', '(iii) An dóigh leat go bhfuil teideal an dáin seo oiriúnach? Cuir fáth amháin le do thuairim. (7 marc)', 8,
         ['(iii) Teideal an dáin oiriúnach? = 4 marc', 'Fáth amháin le do fhreagra = 4 marc']),
        ('iv', '(iv) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (10 marc)', 9,
         ['(iv) Ar thaitin an dán leat? = 1 marc', 'Dhá fháth. = 4 marc × 2 = 8 marc'])],
     'Teideal an dáin/file a chum. = 2 mharc'),
    ('F-B-a-2', 'poetry-roghnach-a-2', 'Filíocht Roghnach (a) · Dán nua-aimseartha a chum bean nó fear', [
        ('i', '(i) Maidir le dán nua-aimseartha amháin a chum bean nó fear agus a ndearna tú staidéar air le linn do chúrsa, abair cén mothúchán is mó atá sa dán, dar leat. Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (8 marc)', 8,
         ['(i) Mothúchán is mó.', '= 2 marc', 'Dhá fháth. 3 marc ×2 = 6 marc']),
        ('ii', '(ii) Roghnaigh dhá mheafar a úsáideann an file sa dán seo agus déan cur síos, i d’fhocail féin, ar an dá mheafar sin. (8 marc)', 8,
         ['(ii) Dhá mheafar sa dán = 2 marc', 'Cur síos i d’fhocail féin ar an dá mheafar = 6 marc']),
        ('iii', '(iii) Scríobh nóta gairid faoi rud amháin sa dán a bhí suimiúil, dar leat. (8 marc)', 8,
         ['(iii) Rud amháin sa dán a bhí suimiúil = 8 marc']),
        ('iv', '(iv) Ar thaitin an dán seo leat? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (9 marc)', 9,
         ['(iv) Ar thaitin an dán leat? = 1 marc', 'Dhá fháth. = 4 marc × 2 = 8 marc'])],
     'Teideal an dáin/ainm an fhile. = 2 marc'),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go soiléir. (2 mharc)'
POETRY_B_B = [
    ('F-B-b-i', 'poetry-roghnach-b-i', 'Filíocht Roghnach (b)(i) · Mothúchán', [
        '(i) Maidir leis na dánta eile a ndearna tú staidéar orthu le linn do chúrsa, agus nár úsáid tú i gcuid (a) thuas, roghnaigh dán amháin díobh a chum fear agus a bhfuil ceann amháin de na mothúcháin seo a leanas i gceist ann. Tabhair cuntas gairid ar a bhfuil sa dán faoin mothúchán sin atá roghnaithe agat.',
        'sásamh / faoiseamh\ngrá\nuaigneas\nmíshásamh\nsíocháin\nbuairt aigne (18 marc)', TITLE_LINE],
     ['(i) Cuntas gairid ar a bhfuil i ndán a chum fear agus nár úsáid tú i gcuid (a) faoi mhothúchán amháin atá roghnaithe agat as na mothúcháin atá luaite. (9 + 9) = 18 marc'],
     'Teideal an dáin/ainm an fhile = 2 marc'),
    ('F-B-b-ii', 'poetry-roghnach-b-ii', 'Filíocht Roghnach (b)(ii) · Príomhsmaoineamh agus íomhá', [
        '(ii) Maidir leis na dánta eile a ndearna tú staidéar orthu le linn do chúrsa, agus nár úsáid tú i gcuid (a) thuas, roghnaigh dán amháin díobh a chum fear. Tabhair cuntas gairid ar phríomhsmaointe an dáin agus ar íomhá (pictiúr) amháin sa dán a thaitin leat (nó nár thaitin leat). (18 marc)',
        TITLE_LINE],
     ['(ii) Cuntas gairid ar phríomhsmaoineamh an dáin a chum fear agus nár úsáid tú i gcuid (a). = 12 marc',
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
    # The language deductions, as printed: 0–5 under each (a), 0–3 under each (b) (one with a hyphen).
    assert scheme.count(LANG_A) == 3 and scheme.count(LANG_B) == 3 and scheme.count(LANG_B_HYPHEN) == 2, (scheme.count(LANG_A), scheme.count(LANG_B))
    # Question lines, as printed.
    for page, lines in [(2, [l for card in PROSE_A for l in card[4]] + [l for card in PROSE_A_B for l in card[3]]),
                        (6, [l for card in PROSE_B for l in card[3] if l != 'NÓ'] + [l for l in PROSE_B_B[3] if l != 'NÓ']),
                        (5, [l for card in POETRY_A_B for l in card[3]]),
                        (7, [sub[1] for card in POETRY_B for sub in card[3]] + [l for card in POETRY_B_B for l in card[3]] + [TITLE_LINE])]:
        for line in lines:
            assert in_order(line, texts[page - 1]), (page, line[:60])
    for key, slug, title, page, subs in POETRY_A:
        assert title in texts[page - 1], key
        for label, lines, marks, _ in subs:
            assert in_order(f'({label}) ' + ' '.join(lines) + f' ({marks} marc)', texts[page - 1]), (key, label)
    for page, line in [(1, WHOLE), (1, PROSE_CHOICE), (1, POETRY_CHOICE), (2, BOTH), (3, BOTH), (6, BOTH), (7, BOTH)]:
        assert comparable(line) in comparable(texts[page - 1]), (page, line)
    for key, box in BOX.items():
        for line in box.splitlines():
            assert comparable(line) in comparable(' '.join(texts)), (key, line)
    assert texts[7] == 'Lch 8 de 8 Leathanach Bán', texts[7]
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

    # ---- Roinn A Ceist 1: Prós Ainmnithe ------------------------------------------------------------------------------
    for key, slug, ref, page, lines, crits in PROSE_A:
        criteria = [criterion(cid, label, marks, guide) for cid, label, marks, guide in crits] + [deduction(LANG_A, 5)]
        add(key, slug, ref, '(a)\n' + '\n'.join(lines), 'irish-4-7', [page], [5],
            criteria, prose_req, f'One complete SEC response at 35: (i) 25 and (ii) 10 (the character 3 + 3 and two reasons 2 × 2), then the '
            f'0–5 Gaeilge deduction once. {tariff_note}', source('Prós Ainmnithe', ref.split(' · ')[1], [page]), BOX['PA'])
        question_ids.append(cards[-1]['id'])
        for (cid, label, marks, guide), sub in zip(crits, ['i', 'ii']):
            sub_lines = [l for l in lines if l.startswith(f'({sub}) ')]
            start = lines.index(sub_lines[0])
            end = next((i for i, l in enumerate(lines) if i > start and re.match(r'\((?:i|ii)\) ', l)), len(lines))
            add(f'{key}-{sub}', f'{slug}-{sub}', f'{ref} · ({sub})', '(a)\n' + '\n'.join(lines[start:end]), 'irish-4-7', [page], [5],
                [criterion('eolas', 'Eolas', marks, guide)], [WHOLE, PROSE_CHOICE, BOTH] + LIT[1:],
                f'One printed sub-question at its published tariff ({marks}). {tariff_note} The 0–5 Gaeilge deduction applies once to the '
                'whole 35-mark answer, never inside one sub-question.', source('Prós Ainmnithe', ref.split(' · ')[1], [page]), BOX['PA'])
            practice_ids.append(cards[-1]['id'])
    for key, slug, ref, lines, guide in PROSE_A_B:
        add(key, slug, ref, '(b)\n' + '\n'.join(lines), 'irish-4-7', [2], [6],
            [criterion('eolas', 'Eolas', 20, [guide]), deduction(LANG_B, 3)], prose_req,
            f'One complete SEC response at 20, then the 0–3 Gaeilge deduction once. {tariff_note}',
            source('Prós Ainmnithe', ref.split(' · ')[0], [2]), BOX['PA'])
        question_ids.append(cards[-1]['id'])

    # ---- Roinn A Ceist 2: Filíocht Ainmnithe ----------------------------------------------------------------------------
    for key, slug, title, page, subs in POETRY_A:
        criteria = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, guide) for label, lines, marks, guide in subs] + [deduction(LANG_A, 5)]
        prompt = f'(a) {title}\n' + '\n'.join(f'({label}) ' + '\n'.join(lines) + f' ({marks} marc)' for label, lines, marks, _ in subs)
        add(key, slug, f'Filíocht Ainmnithe (a) · {title}', prompt, 'irish-5-6', [page], [6], criteria, poetry_req,
            'One complete SEC response at 35: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs) + ', then the 0–5 Gaeilge '
            f'deduction once. The four questions of (i) and the three of (iii) are priced together. {tariff_note}',
            source('Filíocht Ainmnithe', title, [page]), BOX['FA'])
        question_ids.append(cards[-1]['id'])
        for label, lines, marks, guide in subs:
            add(f'{key}-{label}', f'{slug}-{label}', f'Filíocht Ainmnithe (a) · {title} · ({label})',
                f'(a) {title}\n({label}) ' + '\n'.join(lines) + f' ({marks} marc)', 'irish-5-6', [page], [6],
                [criterion('eolas', 'Eolas', marks, guide)], [WHOLE, POETRY_CHOICE, BOTH] + LIT[1:],
                f'One printed sub-question at its published tariff ({marks}). {tariff_note} The 0–5 Gaeilge deduction applies once to the '
                'whole 35-mark answer, never inside one sub-question.', source('Filíocht Ainmnithe', title, [page]), BOX['FA'])
            practice_ids.append(cards[-1]['id'])
    for key, slug, ref, lines, guide in POETRY_A_B:
        add(key, slug, ref, '(b)\n' + '\n'.join(lines), 'irish-5-6', [5], [7],
            [criterion('eolas', 'Eolas', 20, guide), deduction(LANG_B_HYPHEN, 3)], poetry_req,
            f'One complete SEC response at 20, then the 0–3 Gaeilge deduction once. {tariff_note}', source('Filíocht Ainmnithe', FAOISEAMH, [5]),
            BOX['FA'])
        question_ids.append(cards[-1]['id'])

    # ---- Roinn B Ceist 1: Prós Roghnach -------------------------------------------------------------------------------------
    for key, slug, ref, lines, crits in PROSE_B:
        criteria = [criterion(cid, label, marks, guide) for cid, label, marks, guide in crits] + [deduction(LANG_B, 3)]
        add(key, slug, ref, '(a)\n' + '\n'.join(lines), 'irish-4-7', [6], [7, 8], criteria, prose_req,
            f'One complete SEC response at 35: (i) 23, the title and writer 2, (ii) 10 (5 + 5), then the 0–3 Gaeilge deduction once. '
            f'{tariff_note} The text is open content chosen by the candidate.', source('Prós Roghnach', ref.split(' · ')[1], [6]), BOX['PB'])
        question_ids.append(cards[-1]['id'])
    key, slug, ref, lines, crits = PROSE_B_B
    add(key, slug, ref, '(b)\n' + '\n'.join(lines), 'irish-4-7', [6], [8],
        [criterion(cid, label, marks, guide) for cid, label, marks, guide in crits] + [deduction(LANG_B, 3)], prose_req,
        f'One complete SEC response at 20: the account 18 (9 + 9, or 9 × 2 for two characters) and the title and author 2, then the 0–3 '
        f'Gaeilge deduction once. {tariff_note}', source('Prós Roghnach', 'Prós Roghnach (b)', [6]), BOX['PB'])
    question_ids.append(cards[-1]['id'])

    # ---- Roinn B Ceist 2: Filíocht Roghnach ---------------------------------------------------------------------------------
    for key, slug, ref, subs, title_guide in POETRY_B:
        criteria = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, guide) for label, _, marks, guide in subs]
        criteria += [criterion('teideal', 'Teideal + ainm an fhile', 2, [title_guide]), deduction(LANG_A, 5)]
        notice = None
        if key == 'F-B-a-1':
            notice = ('Source note: the paper prints (iii) at 7 marks and (iv) at 10; the scheme prices (iii) at 8 (4 + 4) and (iv) at 9 '
                      '(1 + 4 × 2), the same 17. The criteria follow the scheme. See both sources.')
        add(key, slug, ref, '(a)\n' + '\n'.join(text for _, text, _, _ in subs) + '\n' + TITLE_LINE, 'irish-5-6', [7], [8, 9], criteria,
            poetry_req, 'One complete SEC response at 35: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs) +
            f', the poem and poet 2, then the 0–5 Gaeilge deduction once. {tariff_note} The poem is open content chosen by the candidate.',
            source('Filíocht Roghnach', ref.split(' · ')[1], [7]), BOX['FB'], notice=notice)
        question_ids.append(cards[-1]['id'])
    for key, slug, ref, lines, guide, title_guide in POETRY_B_B:
        add(key, slug, ref, '(b)\n' + '\n'.join(lines), 'irish-5-6', [7], [9],
            [criterion('eolas', 'Eolas', 18, guide), criterion('teideal', 'Teideal + ainm an fhile', 2, [title_guide]),
             deduction(LANG_B_HYPHEN, 3)], poetry_req,
            f'One complete SEC response at 20: the account 18 and the poem and poet 2, then the 0–3 Gaeilge deduction once. {tariff_note}',
            source('Filíocht Roghnach', ref.split(' · ')[0], [7]), BOX['FB'])
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
                  # Before 2012 the reading is on Páipéar I (irish_ordinary_2011_p1.py): this paper has no whole reading question.
                  practiceCardIds=practice_ids, questionCardIds=question_ids, readingWholeCardIds=[],
                  examStructure=dict(prose=55, poetry=55, total=110),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  choicePolicy=('Choice is not a route: prose and poetry are each the prescribed or the optional course, and each question prints '
                                '(a) and (b), both answered; every printed option is one card unless the scheme marks the options alike (the film '
                                'or the play; Prós Roghnach (b)), where one card carries both; no combination cards.'),
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
