#!/usr/bin/env python3
"""Reviewed 2012 Ordinary Paper 2 (Léamhthuiscint agus Litríocht), carded new.

Paper PDF 1–12 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 9–13, plus
14 Socruithe Réasúnta) reviewed on 2026-11-05. Counts are assertions, not
corpus-completeness proof. Same layout as irish_ordinary_2013_p2.py and
irish_ordinary_2014_p2.py: “FREAGAIR GACH CEIST (1, 2 AGUS 3).” Ceist 1 is Léamhthuiscint
A and B (both); Ceist 2 is A (Prós Ainmnithe) or B (Prós Roghnach) and Ceist 3 is A
(Filíocht Ainmnithe) or B (Filíocht Roghnach), each section printing two questions, (a)
and (b), both to be answered (“Freagair (a) agus (b) anseo.”).

What the 2012 scheme prints is much less than 2013's, and the cards carry only that:

- Reading (PDF 9): no answers. Each question's asks restated in a line and one price for
  the whole question (“1. (a) Cad as do thuismitheoirí Evanne Ní Choileáin (b) Dhá scoil ar
  fhreastail sí orthu = 10 marc”); the paper prints “10 marc” per question and no price per
  part. Each of the ten questions is one card with one 10-mark criterion whose guidance is
  that line, claimed whole (0 or 10): splitting it between (a) and (b) would be a price the
  SEC never printed, so no part is a practice card of its own. The scheme's restatement
  misprints two names (“Evanne Ní Choileáin”, “Kieran Boland”: the passage prints Ní
  Chuilinn and Behan) and B 2's price (“= 10 mar”); all kept as printed.
- Literature (PDF 10–13): the scheme reprints each question with its printed price and, for
  2A only, how its points are priced: 2A(a) Hurlamaboc “6 phointe eolais. ( 5 mharc ar an
  gcéad phointe + 5 phointe eile ar 4 mharc an ceann).” and 2A(b) Oisín i dTír na nÓg “4
  phointe eolais. (7 marc ar an gcéad phointe + 6 mharc an ceann ar trí phointe eile).”;
  no sample points anywhere. 2A(a)'s six printed points are asks inside the one summary:
  the scheme prices the first point made and the rest, not each printed point, so they stay
  on the question card (no point is a practice card at a price of its own). 2B(a) an
  optional novel extract and 2B(b) an optional folk tale (account 23 + title 2); 3A(a)
  Géibheann and 3A(b) An tEarrach Thiar ((i) four questions (a)–(d) priced together at 8,
  (ii) 8, (iii) 9); 3B(a) a modern poem by a woman and 3B(b) one by a man ((i) 8, (ii) 8,
  (iii) 7, title and poet 2). The scheme's reprint of 3A(b)(i) is cut at the right margin
  (“(8 mar”, PDF 12): that criterion's guidance is the paper's own print of the question,
  with its “(8 marc)”.

No 2012 Ordinary card existed before. `build` cards the ten whole reading questions, the
eight literature questions (each printed sub-question its own criterion, the 0–4 Gaeilge
deduction once), and practice cards for the six prescribed-poetry sub-questions, the only
parts the scheme prices on their own. The 2012 Atlas files Paper 2 under the pre-2015
keys (“1”–“3” for the questions, “R-A”, “R-B”, “P-A” … for sections), so the whole reading
questions are keyed R-A-1 … R-B-5, as 2014 Higher's are; the literature keys follow 2013/2014.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2012
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2012-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2012-p2-source-review.json'
REVIEWED_AT = '2026-11-05'
PAPER_SHA = '0687a08ada6a00b63a5ed1e7e14baba82074f6ab32908541a7ed5dbd94c70067'
SCHEME_SHA = 'be4c4acab9de2f39e527fd72d22df0741ec5e464a301f481c49aee8c62e65af8'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'  # types/markBank.ts
# The scheme's SymbolMT glyphs: U+F0B4 (×, PDF 4, 5, 8) and U+F0B7 (•, PDF 14); none on the Paper 2 pages.
SYMBOL_FONT = {'': '×', '': '•', ' ': ' '}
LANG_READ = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh.]'
LANG_LIT = '[Gaeilge lochtach: 0 – 4 a bhaint den iomlán a gnóthaíodh.]'


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
    """Scheme pages joined with page markers so every chunk knows the PDF pages it spans."""

    def __init__(self, doc, first, last):
        self.text = ''
        for p in range(first, last + 1):
            self.text += f' ⟦{p}⟧ ' + re.sub(r'^\d+\s', '', clean(page_text(doc[p - 1])))

    def chunk(self, start, end=None, after=0):
        i = self.text.index(start, after)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:i])[-1])}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2))}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


# (letter, title, paper pages, topic, [(q, paper prompt lines, scheme start, scheme price as printed)])
PASSAGES = {
    'A': ('Evanne Ní Chuilinn: Guth Úr Nua i Roinn Spóirt RTÉ', [4, 5], 'irish-3-0', [
        ('1', ['(a) Cad as do thuismitheoirí Evanne Ní Chuilinn?', '(b) Luaigh an dá scoil ar fhreastail sí orthu.'], '1. (a) Cad as', '= 10 marc'),
        ('2', ['(a) Cén cineál ceoil is maith léi?', '(b) Cén rud a rinne sí ar scoil a chabhraigh léi níos déanaí?'], '2. (a) Cineál ceoil', '= 10 marc'),
        ('3', ['(a) Cén teanga a ndearna sí staidéar uirthi agus í ar an ollscoil i mBaile Átha Cliath?',
               '(b) Cén dá chomhlacht lena bhfuair sí taithí oibre?'], '3. (a) An teanga', '= 10 marc'),
        ('4', ['Tabhair dhá phíosa eolais faoina cuid oibre le RTÉ.'], '4. Dhá phíosa eolais', '= 10 marc'),
        # The paper misprints “fáth” as “fath”: kept as printed.
        ('5', ['(a) Cé hiad na laochra is mó ina saol?', '(b) Cén fath a bhfuil meas mór ag Evanne ar Kieran Behan?'], '5. (a) Na laochra', '= 10 marc')]),
    'B': ('Dáithí Ó hEithir: Laoch Óg Leadóige.', [6, 7], 'irish-3-1', [
        ('1', ['(a) Cá bhfuil Dáithí ar an ollscoil anois?', '(b) Cén airde é?'], '1. (a) Cá bhfuil Dáithí', '= 10 marc'),
        # The scheme prints B 2's price “= 10 mar”: kept as printed (the paper prints “10marc”).
        ('2', ['(a) Luaigh dhá spórt eile seachas an leadóg a d’imir Dáithí.', '(b) Cá mbíodh Dáithí ag traenáil agus é san Idirbhliain?'],
         '2. (a) Dhá sport', '= 10 mar'),
        ('3', ['(a) Luaigh dhá chlub leadóige ar imir Dáithí leo.', '(b) Cá fhad a chaith sé i gcampa leadóige Mhoyá?'], '3. (a) Dhá chlub', '= 10 marc'),
        ('4', ['(a) Cén fáth ar fhill Dáithí ar Choláiste Eoin?', '(b) Luaigh dhá bhuntáiste atá ag Dáithí in Ollscoil Memphis.'],
         '4. (a) An fáth', '= 10 marc'),
        ('5', ['(a) Cad a bheidh ar siúl ag Dáithí an samhradh seo?', '(b) Cén aidhm atá ag Dáithí?'], '5. (a) A mbeidh', '= 10 marc')]),
}

# Printed lines (paper PDF 3, 4, 8–11).
PROSE_CHOICE = 'Freagair A (Prós Ainmnithe) nó B (Prós Roghnach).'
POETRY_CHOICE = 'Freagair A (Filíocht Ainmnithe) nó B (Filíocht Roghnach).'
BOTH = 'Freagair (a) agus (b) anseo.'
BOX_2A, BOX_2B = 'A – PRÓS AINMNITHE – [50 marc]', 'B – PRÓS ROGHNACH – [50 marc]'
BOX_3A, BOX_3B = 'A – FILÍOCHT AINMNITHE – [50 marc]', 'B – FILÍOCHT ROGHNACH – [50 marc]'
# The 2023 builders' requirement lines; irish_lifted.printed_tasks gives each its English.
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

# 2A: (slug, atlas, letter, title, topic, printed question lines, scheme start, scheme end, the scheme's point prices, steps)
PROSE_2A = [
    ('prose-2a-a', 'P-2A-a', 'a', 'Hurlamaboc', 'irish-4-5',
     ['(a) “Bean tí den scoth a bhí i Lisín … Agus bhí Lisín sásta …” Hurlamaboc',
      'Tabhair achoimre ar an scéal seo. Luaigh na pointí seo:',
      '(i) Déan cur síos ar Lisín.', '(ii) Luaigh an gaol a bhí aici lena fear céile agus lena mic.',
      '(iii) Cad a bhí á cheiliúradh sa chlann?', '(iv) Cad iad na hullmhúcháin a rinne sí don cheiliúradh seo?',
      '(v) Conas a chaith sí a cuid ama de ghnáth?', '(vi) Luaigh fáth amháin ar/nár thaitin Lisín leat.', '(25 mharc)'],
     '(a) “Bean tí den scoth', '(b) “Niamh Chinn Óir',
     '6 phointe eolais. ( 5 mharc ar an gcéad phointe + 5 phointe eile ar 4 mharc an ceann).', [0, 5, 9, 13, 17, 21, 25]),
    ('prose-2a-b', 'P-2A-b', 'b', 'Oisín i dTír na nÓg', 'irish-4-1',
     ['(b) “Niamh Chinn Óir is ainm dom … is mé iníon Rí na nÓg, … tháinig mé le grá do do mhac féin, Oisín.”',
      'Oisín i dTír na nÓg', 'Inis cad a tharla d’Oisín ina dhiaidh sin sa scéal go dtí gur fhill sé ar Ghleann na Smól.', '(25 mharc)'],
     '(b) “Niamh Chinn Óir', 'B - PRÓS ROGHNACH',
     '4 phointe eolais. (7 marc ar an gcéad phointe + 6 mharc an ceann ar trí phointe eile).', [0, 7, 13, 19, 25]),
]
# 2B: (slug, atlas, letter, ref title, printed question, printed title line, scheme start, scheme end)
PROSE_2B = [
    ('prose-2b-a', 'P-2B-a', 'a', 'Sliocht as úrscéal roghnach',
     '(a) Maidir le sliocht as úrscéal a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar an bpríomhphearsa (bpríomhcharachtar) ann. (23 mharc)',
     'Ní mór teideal an úrscéil sin, mar aon le hainm an údair, a scríobh síos go soiléir. (2 mharc)',
     '(a) Maidir le sliocht as úrscéal', '(b) Maidir le scéal béaloidis'),
    ('prose-2b-b', 'P-2B-b', 'b', 'Scéal béaloidis roghnach',
     '(b) Maidir le scéal béaloidis a ndearna tú staidéar air le linn do chúrsa, tabhair cuntas ar na príomhimeachtaí (rudaí) a tharla sa scéal sin. (23 mharc)',
     'Ní mór teideal an scéil sin a scríobh síos go soiléir. (2 mharc)',
     '(b) Maidir le scéal béaloidis', None),
]
# 3A: (slug, atlas, paper page, title, topic, [(label, printed lines, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 9, 'Géibheann', 'irish-5-2', [
        ('i', ['(a) Cad as don ainmhí seo? (Géibheann thíos)', '(b) Cá bhfuil an t-ainmhí anois, dar leat?',
               '(c) Cad a rinne an t-ainmhí uair amháin?', '(d) Cad a dhéanann an t-ainmhí anois?'], 8, '(i) (a) Cad as don ainmhí'),
        ('ii', ['Luaigh dhá mhothúchán atá sa dán.', 'Déan cur síos, i d’fhocail féin, ar an dá mhothúchán sin sa dán.'], 8, '(ii) Luaigh dhá mhothúchán'),
        ('iii', ['Ar thaitin an dán seo leat? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)'], 9, '(iii) Ar thaitin an dán seo leat?')],
     '(a) (i) (a) Cad as don ainmhí', 'Géibheann Ainmhí mé'),
    ('poetry-3a-b', 'F-3A-b', 10, 'An tEarrach Thiar', 'irish-5-3', [
        ('i', ['(a) Conas atá an aimsir sa dán seo? (An tEarrach Thiar thíos)', '(b) Cén dath a bhí ar an bhfeamainn?',
               '(c) Cá bhfios duit go raibh an iascaireacht go maith?', '(d) Cathain a d’fhill na hiascairí ar an gcladach?'], 8,
         '(i) (a) Conas atá an aimsir'),
        ('ii', ['Luaigh dhá íomhá (phictiúr) atá sa dán.', 'Déan cur síos, i d’fhocail féin, ar an dá íomhá sin sa dán.'], 8, '(ii) Luaigh dhá íomhá'),
        ('iii', ['An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)'], 9, '(iii) An maith leat an dán seo?')],
     '(b) (i) (a) Conas atá an aimsir', 'An tEarrach Thiar Fear ag glanadh'),
]
# 3B: (slug, atlas, letter, ref title, [(label, printed lines, marks, scheme cut)], printed title line, scheme start, scheme end)
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', 'a', 'Dán nua-aimseartha a chum bean', [
        ('i', ['Maidir le dán nua-aimseartha amháin a chum bean agus a ndearna tú staidéar air le linn do chúrsa, inis i d’fhocail féin, cad is téama don dán sin, dar leat.'], 8,
         '(a) (i) Maidir le dán nua-aimseartha amháin a chum bean'),
        ('ii', ['Roghnaigh dhá mhothúchán a úsáideann an file sa dán seo agus déan cur síos orthu i d’fhocail féin.'], 8, '(ii) Roghnaigh dhá mhothúchán'),
        ('iii', ['Ar thaitin an dán leat? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)'], 7, '(iii) Ar thaitin an dán leat?')],
     'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go soiléir. (2 mharc)',
     '(a) (i) Maidir le dán nua-aimseartha amháin a chum bean', '(b) (i) Maidir le dán nua-aimseartha amháin a chum fear'),
    ('poetry-3b-b', 'F-3B-b', 'b', 'Dán nua-aimseartha a chum fear', [
        ('i', ['Maidir le dán nua-aimseartha amháin a chum fear agus a ndearna tú staidéar air le linn do chúrsa, inis cén mothúchán is mó atá sa dán, dar leat.',
               'Cuir fáthanna le do fhreagra. (Is leor dhá fháth)'], 8, '(b) (i) Maidir le dán nua-aimseartha amháin a chum fear'),
        ('ii', ['Roghnaigh dhá íomhá (phictiúr) a úsáideann an file sa dán seo agus déan cur síos orthu i d’fhocail féin.'], 8, '(ii) Roghnaigh dhá íomhá'),
        ('iii', ['An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)'], 7, '(iii) An maith leat an dán seo?')],
     'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go soiléir. (2 mharc)',
     '(b) (i) Maidir le dán nua-aimseartha amháin a chum fear', 'Nóta: Caithfidh an Scrúdaitheoir'),
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
    assert len(paper) == 12 and len(doc) == 16
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 9, 13)
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    # Each passage prints its 0–5 deduction once, and B's penalty note closes the reading pages.
    assert s.text.count(LANG_READ) == 2 and 'Nóta: Gearrfar pionós i ngeall ar iomarcaíocht .' in s.text
    # Hurlamaboc, Oisín, 2B(a), 2B(b), Géibheann, An tEarrach Thiar, 3B(a), 3B(b): eight literature language notes.
    assert s.text.count(LANG_LIT) == 8, s.text.count(LANG_LIT)
    # No sample answer, answer bullet or band table anywhere on the Paper 2 pages.
    assert not re.search(r'Freagraí|Freagra:|Samplaí|samplacha|féideartha|Catagóir|Sármhaith|•', s.text)
    reading = {}
    for letter, (title, pages, topic, questions) in PASSAGES.items():
        page_text_ = ' '.join(texts[p - 1] for p in pages)
        assert in_order(title, page_text_), letter
        after = s.text.index(f'{letter} (50 marc)')
        out = []
        for index, (q, lines, start, price) in enumerate(questions):
            for line in lines:
                assert in_order(line, page_text_), (letter, q, line)
            assert in_order(f'{q}. ' + ' '.join(lines) + ' 10 marc', page_text_.replace('10marc', '10 marc')), (letter, q)
            nxt = questions[index + 1][2] if index + 1 < len(questions) else LANG_READ
            chunk, spages = s.chunk(start, nxt, after)
            after = s.text.index(start, after) + 1
            assert chunk.endswith(price) and chunk.count('=') == 1 and spages == [9], (letter, q, chunk)
            out.append((q, lines, chunk, spages))
        reading[letter] = out
    # The printed lines the literature cards carry, in the paper's order.
    for line in [l for *_, lines, _, _, _, _ in PROSE_2A for l in lines]:
        assert in_order(line, texts[7]), line[:50]
    for slug, atlas, letter, title, question, title_line, start, end in PROSE_2B:
        assert in_order(question, texts[7]) and in_order(title_line, texts[7]), slug
    for slug, atlas, page, title, topic, subs, start, end in POETRY_3A:
        assert in_order(title, texts[page - 1]), slug
        for label, lines, marks, cut in subs:
            assert in_order(f'({label}) ' + ' '.join(lines) + f' ({marks} marc)', texts[page - 1]), (slug, label)
    for slug, atlas, letter, title, subs, title_line, start, end in POETRY_3B:
        for label, lines, marks, cut in subs:
            assert in_order(f'({label}) ' + ' '.join(lines) + f' ({marks} marc)', texts[10]), (slug, label)
        assert in_order(title_line, texts[10]), slug
    assert comparable(texts[10]).count(comparable(POETRY_3B[0][5])) == 2
    for page, line in [(3, 'FREAGAIR GACH CEIST (1, 2 AGUS 3).'), (4, 'Freagair A agus B anseo.'), (8, PROSE_CHOICE), (8, BOTH), (8, BOX_2A),
                       (8, BOX_2B), (9, POETRY_CHOICE), (9, BOTH), (9, BOX_3A), (11, BOX_3B), (11, BOTH)]:
        assert comparable(line) in comparable(texts[page - 1]), (page, line)
    _MATERIAL = dict(paper=paper, texts=texts, s=s, reading=reading, decisions=selection_decisions(paper))
    return _MATERIAL


def deduction(note):
    return criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [note], 'quality', deduction=True)


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def language_note(chunk):
    assert chunk.count(LANG_LIT) == 1, chunk[-160:]
    return LANG_LIT


def cut(chunk, cuts, slug):
    idx = [chunk.index(c) for c in cuts]
    assert idx == sorted(idx), slug
    return [chunk[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk)])]


READING_NOTE = ('One SEC price for the whole question (10); the scheme restates what each part asks and does not split the price between them, '
                'so the question is claimed whole (0 or 10). ' + UNPRINTED_ANSWER + ' Scheme: “' + LANG_READ + '” — one deduction from each '
                'passage total (50), never inside a single question.')
LIT_DEDUCTION_NOTE = 'The 0–4 Gaeilge deduction applies once to this whole 25-mark answer, never inside one sub-question.'


def build():
    m = material()
    s = m['s']
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, src, concept=None, stem=None, focus=None):
        cards.append(dict(
            id=f'irish-{YEAR}-ol-p2-{slug}', year=YEAR, level='ordinary', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'{YEAR} OL Paper 2 {ref}', **({'stem': stem} if stem else {}), questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria if c['kind'] == 'award'), topicId=topic,
            conceptId=concept or f'irish-ol-p2-{slug}', paperFileid=FILE, paperPage=pages[0], schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=requirements, criteria=criteria, markingGuideNote=note, sourceMaterial=src,
            **({'practiceFocus': focus} if focus else {})))

    # ---- Ceist 1: Léamhthuiscint A and B: ten whole questions, each one 10-mark criterion --------------------------
    whole_ids, practice_ids, question_lit = [], [], []
    for letter, (title, pages, topic, _) in PASSAGES.items():
        src = source(f'Léamhthuiscint {letter}', title, pages)
        for q, lines, chunk, spages in m['reading'][letter]:
            label = '(a) + (b)' if len(lines) == 2 else 'Freagra'
            add(f'R-{letter}-{q}', f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}', f'{q}. ' + ' '.join(lines),
                topic, pages, spages, [criterion('eolas', label, 10, [chunk], permitted=[0, 10])], READING_WHOLE, READING_NOTE, src,
                concept=f'irish-reading-{letter.lower()}-q{q}')
            whole_ids.append(cards[-1]['id'])

    # ---- Ceist 2A: (a) Hurlamaboc, (b) Oisín i dTír na nÓg -----------------------------------------------------------
    for slug, atlas, letter, title, topic, lines, start, end, price, steps in PROSE_2A:
        chunk, spages = s.chunk(start, end)
        lang = language_note(chunk)
        assert chunk.endswith(f'(25 mharc) {price} {lang}'), chunk[-200:]
        assert all(in_order(line, chunk) for line in lines), slug
        add(atlas, slug, f'Prós 2A({letter}) · {title}', '\n'.join(lines), topic, [8], spages,
            [criterion('eolas', 'Eolas', 25, [price], 'indicative', permitted=steps), deduction(lang)], [PROSE_CHOICE, BOTH] + LIT[1:],
            f'One complete SEC response at 25: the scheme prices its points of information in order ({price}), so the answer steps '
            f'{", ".join(str(v) for v in steps[1:])} as each point is made; then the 0–4 Gaeilge deduction once. The scheme prints no sample '
            'points; each point is judged on merit.', source('Prós Ainmnithe', title, [8]), concept=f'irish-prose-2a-{topic}', stem=BOX_2A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 2B: (a) an optional novel extract, (b) an optional folk tale --------------------------------------------
    for slug, atlas, letter, title, question, title_line, start, end in PROSE_2B:
        chunk, spages = s.chunk(start, end) if end else s.chunk(start, 'CEIST 3')
        lang = language_note(chunk)
        assert chunk.replace(f'{lang} ', '').replace(f' {lang}', '') == f'{question} {title_line}', chunk
        crits = [criterion('eolas', 'Eolas', 23, [question], 'indicative', permitted=[0, 23]),
                 criterion('teideal', 'Teideal' + (' + ainm an údair' if 'údair' in title_line else ''), 2, [title_line], permitted=[0, 2]),
                 deduction(lang)]
        add(atlas, slug, f'Prós 2B({letter}) · {title}', f'{question}\n{title_line}', 'irish-4-7', [8], spages, crits,
            [PROSE_CHOICE, BOTH] + LIT[1:],
            'One complete SEC response: 23 for the account and 2 for the title' + (' and the author' if 'údair' in title_line else '') +
            ', then the 0–4 Gaeilge deduction once. The scheme prints each price whole, with no points, scale or sample answers, so each is '
            'claimed whole. The optional text is open content chosen by the candidate.',
            source('Prós Roghnach', title, [8]), concept='irish-prose-2b-irish-4-7', stem=BOX_2B)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3A: Géibheann and An tEarrach Thiar ----------------------------------------------------------------------
    poem_parts = {}
    for slug, atlas, page, title, topic, subs, start, end in POETRY_3A:
        chunk, spages = s.chunk(start, end)
        lang = language_note(chunk)
        pieces = cut(chunk.replace(lang, '').strip(), [c for *_, c in subs], slug)
        guidance = []
        for (label, lines, marks, _), piece in zip(subs, pieces):
            if piece.endswith('(8 mar'):
                # PDF 12 prints 3A(b)(i)'s reprint cut at the right margin (“(8 mar”): its price is the paper's own print.
                assert (slug, label) == ('poetry-3a-b', 'i'), (slug, label)
                assert all(in_order(line, piece) for line in lines), piece
                piece = f'({label}) ' + ' '.join(lines) + f' ({marks} marc)'
                assert in_order(piece, m['texts'][page - 1])
            assert piece.endswith(f'({marks} marc)') and all(in_order(line, piece) for line in lines), (slug, label, piece[-60:])
            guidance.append(piece)
        poem_parts[slug] = (guidance, spages)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [g], 'indicative', permitted=[0, marks])
                 for (label, _, marks, _), g in zip(subs, guidance)]
        prompt = '\n'.join(f'({label}) ' + '\n'.join(lines) + f' ({marks} marc)' for label, lines, marks, _ in subs)
        add(atlas, slug, f'Poetry 3A({atlas[-1]})', f'({atlas[-1]}) {title}\n' + prompt, topic, [page], spages, crits + [deduction(lang)],
            [POETRY_CHOICE, BOTH] + LIT,
            'One complete SEC response: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs) +
            ' at their printed tariffs, then the 0–4 Gaeilge deduction once. The scheme prints each sub-question’s price whole (the four '
            'questions of (i) together at 8), with no split, scale or sample answers, so each is claimed whole. ' + UNPRINTED_ANSWER,
            source('Filíocht Ainmnithe', title, [page]), concept=f'irish-poetry-3a-{topic}', stem=BOX_3A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3B: Filíocht Roghnach (a) a modern poem by a woman, (b) one by a man -------------------------------------
    for slug, atlas, letter, title, subs, title_line, start, end in POETRY_3B:
        chunk, spages = s.chunk(start, end)
        lang = language_note(chunk)
        pieces = cut(chunk.replace(lang, '').strip(), [c for *_, c in subs] + ['Ní mór teideal an dáin'], slug)
        assert pieces[-1] == title_line, pieces[-1]
        crits = []
        for (label, lines, marks, _), piece in zip(subs, pieces):
            assert piece.endswith(f'({marks} marc)'), (slug, label, piece[-40:])
            crits.append(criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece], 'indicative', permitted=[0, marks]))
        crits.append(criterion('teideal', 'Teideal + ainm an fhile', 2, [title_line], permitted=[0, 2]))
        prompt = '\n'.join(f'({label}) ' + '\n'.join(lines) + f' ({marks} marc)' for label, lines, marks, _ in subs)
        add(atlas, slug, f'Poetry 3B({letter})', f'({letter}) ' + prompt + '\n' + title_line, 'irish-5-6', [11], spages, crits + [deduction(lang)],
            [POETRY_CHOICE, BOTH] + LIT,
            'One complete SEC response: ' + ', '.join(f'({label}) {marks}' for label, _, marks, _ in subs) + ', poem and poet 2, then the '
            '0–4 Gaeilge deduction once. The scheme prints each price whole, with no split, scale or sample answers, so each is claimed '
            'whole. The optional poem is open content chosen by the candidate.',
            source('Filíocht Roghnach', f'3B({letter}) · {title}', [11]), concept='irish-poetry-3b-irish-5-6', stem=BOX_3B)
        question_lit.append(cards[-1]['id'])

    # ---- Practice: every prescribed-poetry sub-question at its own printed price ------------------------------------------
    for slug, atlas, page, title, topic, subs, start, end in POETRY_3A:
        guidance, spages = poem_parts[slug]
        head = f'({atlas[-1]}) {title}\n'
        for (label, lines, marks, _), g in zip(subs, guidance):
            add(f'{atlas}-{label}', f'{slug}-{label}', f'Filíocht 3A({atlas[-1]}) · {title} · ({label})', head + f'({label}) ' + '\n'.join(lines) + f' ({marks} marc)',
                topic, [page], spages, [criterion('eolas', 'Eolas', marks, [g], 'indicative', permitted=[0, marks])],
                [POETRY_CHOICE, BOTH] + LIT[1:], f'One printed sub-question at its published tariff ({marks}), claimed whole: the scheme prints no '
                'split, scale or sample answers for it. ' + LIT_DEDUCTION_NOTE, source('Filíocht Ainmnithe', title, [page]), stem=BOX_3A)
            practice_ids.append(cards[-1]['id'])

    assert len(whole_ids) == 10 and len(question_lit) == 8 and len(practice_ids) == 6, (len(whole_ids), len(question_lit), len(practice_ids))
    assert len(cards) == 24 and len({c['id'] for c in cards}) == 24 and len({c['atlasQuestionId'] for c in cards}) == 24
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria'] if c['kind'] == 'award') == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('Scrúdaitheoir|Iomlán|50 marc|Gearrfar|Taispeánfar', g) and not PUA.search(g) for g in c['guidance']), (card['id'], c['id'])
    sr = json.loads(SOURCE_REVIEW.read_text())
    review = dict(year=YEAR, level='ordinary', paperFileid=FILE + '.pdf', schemeFileid=SCHEME_FILE + '.pdf',
                  paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
                  reviewedPaperPages=list(range(1, 13)), reviewedSchemePages=sr['reviewedSchemePages'], schemeScope=sr['schemeScope'],
                  reviewDate=REVIEWED_AT, status='reviewed', fullPaperAndApplicableSchemeVisualSweep=True, selectionDecisions=m['decisions'],
                  practiceCardIds=practice_ids, questionCardIds=whole_ids + question_lit, readingWholeCardIds=whole_ids,
                  examStructure=dict(readingA=50, readingB=50, prose=50, poetry=50, total=200),
                  nonPoolDecisions=sr['nonPoolDecisions'], openIssues=[], caveats=sr['sourceFindings'],
                  choicePolicy=('Choice is not a route: Ceist 2 and Ceist 3 are each A or B, and each section prints two questions, (a) and (b), both '
                                'to be answered; every printed question is one card carrying the printed choice and “Freagair (a) agus (b) anseo.”; '
                                'no combination cards.'),
                  boundaries=('10 whole reading questions (each one 10-mark price, not split between its parts); 8 literature questions (2A(a) '
                              'Hurlamaboc, 2A(b) Oisín i dTír na nÓg, 2B(a), 2B(b), 3A(a) Géibheann, 3A(b) An tEarrach Thiar, 3B(a), 3B(b)); '
                              'the 6 prescribed-poetry sub-questions as practice cards.'))
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
    print(f"Irish Ordinary {YEAR} Paper 2: {len(data['cards'])} reviewed cards (18 printed questions, 6 practice parts); the archive remains incomplete.")


if __name__ == '__main__':
    main()
