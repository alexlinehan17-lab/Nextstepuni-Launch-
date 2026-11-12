#!/usr/bin/env python3
"""Reviewed 2020 Ordinary Paper 2 (Léamhthuiscint agus Litríocht), carded new.

Paper PDF 1–12 and the Paper 2 pages of the combined LC001GLP000IV scheme (PDF 12–26,
plus 27 modified marking) reviewed on 2026-11-04. Counts are assertions, not
corpus-completeness proof. Same method as irish_ordinary_2022_p2.py.

No 2020 card existed before. `build` cards the component the way the reviewed
2021–2025 Ordinary Paper 2s are carded: the ten whole reading questions (each part its
own 5-mark criterion), the eight literature questions (each printed sub-question its own
criterion, the 0–4 Gaeilge deduction once), and the practice cards beside them: every
reading part (20), the five printed sub-questions of 2A(a) Dís, every prescribed-poetry
sub-question (6) and the three printed questions inside 3A(b)(i) An tEarrach Thiar.

2020's layout: “FREAGAIR GACH CEIST (1, 2 AGUS 3).” Ceist 1 is Léamhthuiscint A and B
(both); Ceist 2 is A (Prós Ainmnithe) or B (Prós Roghnach) and Ceist 3 is A (Filíocht
Ainmnithe) or B (Filíocht Roghnach), each section printing two questions, (a) and (b),
both to be answered (“Freagair (a) agus (b) anseo.”). Each literature card carries the
printed choice and “Freagair (a) agus (b) anseo.” as its task check (choice is not a
route; no card combines two questions), and the section's printed box heading
(“A – PRÓS AINMNITHE – (50 marc)” …) with, for B, the printed restriction as its lead-in.

The scheme's text layer stores each page's boxed heading (“CEIST 1 (A + B) -
LÉAMHTHUISCINT - 100 marc”, “B – (50 marc)” …) with the page body; `Scheme` removes
those exact strings so no heading lands inside an answer key.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from irish_lifted import PUA, scheme_words_in, symbol_text

ROOT = Path(__file__).resolve().parents[3]
YEAR = 2020
FILE = 'LC001GLP200IV'
SCHEME_FILE = 'LC001GLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/ordinary-2020-p2-authored.json'
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-ordinary-2020-p2-source-review.json'
REVIEWED_AT = '2026-11-04'
PAPER_SHA = '53b6be15b735812bcc70eb6a36a932d154fcede395a9fcd19d97195598d2e633'
SCHEME_SHA = '6214b57105f533f4650c8acf7082d19a6fdf8cf5df08d8e53b966050a5984d41'
DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Luaigh|Ainmnigh|\bnó\b|dhá phointe|dhá rud|dhá bh|dhá dh|dhá ch|dhá fh|dhá th|dhá ph|dhá sh|'
                       r'\ban dá\b|ceann amháin|pointe amháin|amháin|\bdhá\b', re.I)
SOURCE_NOTE = 'Shown page-for-page from the official examination paper; swipe to move between pages.'
ATTRIBUTION = '© State Examinations Commission.'
# Boxed page headings the 2020 scheme's text layer stores with the page body (exact strings, each printed once).
FURNITURE = ('CEIST 1 (A + B) - LÉAMHTHUISCINT - 100 marc', 'A – (50 marc)', 'B – (50 marc)',
             'CEIST 2 PRÓS – AINMNITHE nó ROGHNACH – (50 marc)', 'A – PRÓS AINMNITHE – (50 marc)', 'B – PRÓS ROGHNACH – (50 marc)',
             'CEIST 3 FILÍOCHT – AINMNITHE nó ROGHNACH – (50 marc)', 'A – FILÍOCHT AINMNITHE – (50 marc)', 'B – FILÍOCHT ROGHNACH – (50 marc)')
FURNITURE_PATTERN = re.compile('|'.join(r'\s*' + re.escape(h) + r'(?=\s|$)\s*' for h in sorted(FURNITURE, key=len, reverse=True)))


def clean(text):
    return re.sub(r'\s+', ' ', symbol_text(text)).strip()


def comparable(text):
    return re.sub(r'[^\w]+', '', text.lower())


def in_order(prompt, text):
    return re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split() if comparable(w)), comparable(text))


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
        self.removed = 0
        for p in range(first, last + 1):
            body = re.sub(r'^\d+\s', '', clean(doc[p - 1].get_text()))
            body, n = FURNITURE_PATTERN.subn(' ', body)
            self.removed += n
            self.text += f' ⟦{p}⟧ ' + clean(body)

    def chunk(self, start, end=None, after=0):
        i = self.text.index(start, after)
        j = self.text.index(end, i + len(start)) if end else len(self.text)
        raw = self.text[i:j]
        pages = {int(re.findall(r'⟦(\d+)⟧', self.text[:i])[-1])}
        pages |= {int(m.group(1)) for m in re.finditer(r'⟦(\d+)⟧([^⟦]*)', raw) if clean(m.group(2)) not in ('', 'nó')}
        return clean(re.sub(r'⟦\d+⟧', ' ', raw)), sorted(pages)


def before_language_note(text):
    return re.split(r'\[\s*Gaeilge lochtach', text)[0].strip()


def split_at(text, cuts, slug):
    idx = [text.index(cut) for cut in cuts]
    assert idx == sorted(idx), slug
    return [text[a:b].strip() for a, b in zip(idx, idx[1:] + [len(text)])]


# (q, part, paper prompt, scheme anchor)
PASSAGES = {
    'A': dict(title='An tAthrú Aeráide', pages=[4, 5], topic='irish-3-0', start='⟦12⟧', notes_end='An tAthrú Aeráide 1. (a)',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Cad is brí leis an téarma ‘athrú aeráide’? (Alt 1)', '1. (a) Cad is brí leis an téarma'),
        ('1', 'b', '(b) Tabhair dhá phíosa eolais faoin tonn teasa a bhí in Éirinn i samhradh 2018. (Alt 1)', '(b) Tabhair dhá phíosa eolais faoin tonn teasa'),
        ('2', 'a', '(a) Cad is cúis leis an athrú aeráide, dar leis na heolaithe aeráide? (Alt 2)', '2. (a) Cad is cúis leis an athrú aeráide'),
        ('2', 'b', '(b) Tabhair dhá athrú atá le feiceáil ar na patrúin aimsire anseo in Éirinn anois. (Alt 2)', '(b) Tabhair dhá athrú atá le feiceáil'),
        ('3', 'a', '(a) Scríobh síos dhá rud a tharlaíonn nuair a dhóitear na breoslaí: gual, gás, móin, ola, peitreal agus díosal. (Alt 3)', '3. (a) Scríobh síos dhá rud a tharlaíonn'),
        ('3', 'b', '(b) Luaigh dhá rud a scaoileann meatán agus ocsaíd nítriúil san atmaisféar. (Alt 3)', '(b) Luaigh dhá rud a scaoileann meatán'),
        ('4', 'a', '(a) Tabhair dhá chúis a bhfuil Greta Thunberg míshásta leis na polaiteoirí ar fud an domhain. (Alt 4)', '4. (a) Tabhair dhá chúis a bhfuil Greta'),
        ('4', 'b', '(b) Cad iad an dá rud a rinne na daoine óga ag Tionól Aeráide na nÓg i nDáil Éireann i mí na Samhna seo caite? (Alt 4)', '(b) Cad iad an dá rud a rinne na daoine óga'),
        ('5', 'a', '(a) Tabhair dhá bhealach atá luaite i bplean aeráide an rialtais chun leibhéal an charbóin san atmaisféar a ísliú sa tír seo faoin mbliain 2030. (Alt 5)', '5. (a) Tabhair dhá bhealach atá luaite'),
        ('5', 'b', '(b) Scríobh síos dhá rud is féidir le gach duine a dhéanamh ina shaol laethúil ar son an phláinéid. (Alt 5)', '(b) Scríobh síos dhá rud is féidir le gach duine')]),
    'B': dict(title='Mná agus an Spórt', pages=[6, 7], topic='irish-3-1', start='⟦15⟧', notes_end='1. (a)',
              end='Nóta: Gearrfar pionós i ngeall ar iomarcaíocht. Léireofar', parts=[
        ('1', 'a', '(a) Scríobh síos an dá chúis a raibh an rámhaí, Sanita Puspure, sa nuacht i mí Mheán Fómhair seo caite. (Alt 1)', '1. (a) Scríobh síos an dá chúis a raibh an rámhaí'),
        ('1', 'b', '(b) Cén gaisce a rinne foireann haca na mban i mí na Samhna seo caite? (Alt 1)', '(b) Cén gaisce a rinne foireann haca'),
        ('2', 'a', '(a) Tabhair dhá phíosa eolais a thaispeánann go raibh spórt na mban in Éirinn chun deiridh ar spórt na bhfear ar feadh na mblianta. (Alt 2)', '2. (a) Tabhair dhá phíosa eolais a thaispeánann'),
        ('2', 'b', '(b) Luaigh dhá sprioc atá ag an bhfeachtas 20 x 20. (Alt 2)', '(b) Luaigh dhá sprioc atá ag an bhfeachtas'),
        ('3', 'a', '(a) Scríobh síos dhá phíosa eolais faoin líon daoine a d’fhreastail ar chluichí ceannais pheil na mban i bPáirc an Chrócaigh anuraidh. (Alt 3)', '3. (a) Scríobh síos dhá phíosa eolais faoin líon daoine'),
        ('3', 'b', '(b) Conas atá peil na mban á cur chun cinn ag TG4 le beagnach fiche bliain anuas? (Alt 3)', '(b) Conas atá peil na mban á cur chun cinn'),
        ('4', 'a', '(a) Tabhair dhá phíosa eolais faoi na láithreoirí ar chlár RTÉ The Sunday Game. (Alt 4)', '4. (a) Tabhair dhá phíosa eolais faoi na láithreoirí'),
        ('4', 'b', '(b) Scríobh síos dhá rud a thaispeánann tábhacht an spóirt i saol na réaltaí ar na cláir Mná Spóirt: Croí is Anam. (Alt 4)', '(b) Scríobh síos dhá rud a thaispeánann tábhacht'),
        ('5', 'a', '(a) Tabhair an dá chúis mhórtais a bhí ag Katie Taylor ag na Cluichí Oilimpeacha i Londain in 2012. (Alt 5)', '5. (a) Tabhair an dá chúis mhórtais'),
        ('5', 'b', '(b) Scríobh síos dhá phíosa eolais faoin lúthchleasaí, Sonia O’Sullivan. (Alt 5)', '(b) Scríobh síos dhá phíosa eolais faoin lúthchleasaí')]),
}

# Printed lines (paper PDF 3, 8–12).
PROSE_CHOICE = 'Freagair A (Prós Ainmnithe) nó B (Prós Roghnach).'
POETRY_CHOICE = 'Freagair A (Filíocht Ainmnithe) nó B (Filíocht Roghnach).'
BOTH = 'Freagair (a) agus (b) anseo.'
BOX_2A, BOX_2B = 'A – PRÓS AINMNITHE – (50 marc)', 'B – PRÓS ROGHNACH – (50 marc)'
BOX_3A, BOX_3B = 'A – FILÍOCHT AINMNITHE – (50 marc)', 'B – FILÍOCHT ROGHNACH – (50 marc)'
NO_PRESCRIBED_PROSE = 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach.'
NO_PRESCRIBED_POETRY = 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe a úsáid sna freagraí ar an bhFilíocht Roghnach.'
STEM_2B = BOX_2B + '\n' + NO_PRESCRIBED_PROSE
STEM_3B = BOX_3B + '\n' + NO_PRESCRIBED_POETRY
# The 2023 builders' requirement lines; irish_lifted.printed_tasks gives each its English.
LIT = ['Freagair gach fochuid atá priontáilte sa rogha seo.', 'Úsáid tagairtí cruinne agus ábhartha don téacs.']
READING_PART = ['Léigh an sliocht iomlán a ghabhann leis an gceist. Freagair an chuid atá luaite ar an gcárta.', 'Úsáid an t-alt a luaitear.']
READING_WHOLE = ['Léigh an sliocht oifigiúil a ghabhann leis an gceist.', 'Freagair gach fochuid agus cloígh leis an alt a luaitear.']

# 2A(a) Dís: printed sub-questions at 5 each (the paper prints only the question's (25 marc)).
DIS = ('prose-2a-a', 'P-2A-a', 'a', 'Dís', 'irish-4-4', 'Freagair na ceisteanna thíos faoin ngearrscéal Dís.', [
    ('i', 'Tabhair dhá chúis a raibh bean Sheáin míshásta le Seán i dtús an ghearrscéil.', '(i) Tabhair dhá chúis a raibh bean Sheáin'),
    ('ii', 'Cén toradh a bhí ar an suirbhé, de réir an eolais ar an bpáipéar?', '(ii) Cén toradh a bhí ar an suirbhé'),
    ('iii', 'Conas a mhothaigh bean Sheáin an mhaidin ar tháinig bean an tsuirbhé chuig an teach? Tabhair dhá chúis ar mhothaigh sí mar sin.', '(iii) Conas a mhothaigh bean Sheáin'),
    ('iv', 'Scríobh síos dhá rud a dúirt bean Sheáin le bean an tsuirbhé faoi na fir.', '(iv) Scríobh síos dhá rud a dúirt bean Sheáin'),
    ('v', 'Cén sórt duine ba ea bean an tsuirbhé, dar leat? Tabhair dhá phointe eolais as an scéal.', '(v) Cén sórt duine ba ea bean an tsuirbhé')],
    '(a) Dís Freagair na ceisteanna thíos faoin ngearrscéal Dís. (25 marc)', '(b) Oisín i dTír na nÓg (25 marc)')
# 2A(b) Oisín i dTír na nÓg: one 25-mark question.
OISIN = ('prose-2a-b', 'P-2A-b', 'b', 'Oisín i dTír na nÓg', 'irish-4-1',
         '‘Cuirim geasa ort nach bhfulaingíonn fíorlaoch, a Oisín fhéil,’ arsa Niamh Chinn Óir, ‘mura dtaga tú ar ais liom go Tír na nÓg.’ Oisín i dTír na nÓg\n'
         'Tabhair cuntas ar na rudaí a tharla d’Oisín ón am a d’imigh sé le Niamh Chinn Óir go Tír na nÓg go dtí gur fhill sé ar Éirinn.',
         '(b) Oisín i dTír na nÓg (25 marc)', 'Níl cead aon ábhar a bhaineann le Prós Ainmnithe')
# 2B: (slug, atlas, paper lines, scheme start, scheme end, [(id, label, marks, cut-before)], source title)
PROSE_2B = [
    ('prose-2b-a', 'P-2B-a', ['(a) Maidir le gearrscéal roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos príomhthéama an ghearrscéil sin, dar leat. '
                              'Tabhair cuntas ar na heachtraí is mó a léiríonn an príomhthéama sin sa ghearrscéal. (23 marc)',
                              'Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair, a scríobh síos go cruinn. (2 mharc)'],
     '(a) Maidir le gearrscéal roghnach', '(b) Maidir le scéal béaloidis roghnach',
     [('priomhthema', 'An príomhthéama a lua', 1, None), ('eolas', 'Na heachtraí is mó', 22, 'Na heachtraí is mó a léiríonn'),
      ('teideal', 'Teideal + ainm an údair', 2, 'Ní mór teideal')], 'Gearrscéal roghnach'),
    ('prose-2b-b', 'P-2B-b', ['(b) Maidir le scéal béaloidis roghnach a ndearna tú staidéar air le linn do chúrsa, ainmnigh an phríomhphearsa (an príomhcharachtar) sa scéal. '
                              'Tabhair cuntas ar na heachtraí is mó a tharlaíonn don duine sin ó thús go deireadh an scéil. (23 marc)',
                              'Ní mór teideal an scéil bhéaloidis sin a scríobh síos go cruinn. (2 mharc)'],
     '(b) Maidir le scéal béaloidis roghnach', 'Freagair A (Filíocht Ainmnithe)',
     [('priomhphearsa', 'An phríomhphearsa a ainmniú', 1, None), ('eolas', 'Na heachtraí is mó', 22, '5 phointe eolais ag teastáil'),
      ('teideal', 'Teideal an scéil bhéaloidis', 2, 'Ní mór teideal')], 'Scéal béaloidis roghnach'),
]
# 3A: (slug, atlas, page, title, [(label, paper prompt, marks, scheme cut)], scheme start, scheme end)
POETRY_3A = [
    ('poetry-3a-a', 'F-3A-a', 10, 'Géibheann', [
        ('i', 'Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) den ainmhí a fhaighimid sna línte 1-8 sa dán. (Is leor dhá phointe eolais.)', 8,
         '(i) Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) den ainmhí'),
        ('ii', 'Conas a mhothaíonn an t-ainmhí sna línte 9-12 sa dán, dar leat? Tabhair dhá fháth, i d’fhocail féin, a mothaíonn sé mar sin.', 8,
         '(ii) Conas a mhothaíonn an t-ainmhí'),
        ('iii', 'An bhfuil an t-ainmhí sásta sna línte 13-17 sa dán, dar leat? Cuir fáthanna, i d’fhocail féin, le do fhreagra. (Is leor dhá fháth.)', 9,
         '(iii) An bhfuil an t-ainmhí sásta')],
     '(a) Géibheann (25 marc)', '(b) An tEarrach Thiar'),
    ('poetry-3a-b', 'F-3A-b', 11, 'An tEarrach Thiar', [
        ('i', '(a) Conas atá an aimsir i véarsa a haon?\n(b) Tabhair dhá phointe eolais faoi na mná i véarsa a trí.\n(c) Cén fhuaim atá le cloisteáil i véarsa a ceathair?', 8,
         '(i) (a) Conas atá an aimsir'),
        ('ii', 'Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) den fhear a thugann an file dúinn i véarsa a dó. (Is leor dhá phointe eolais.)', 8,
         '(ii) Déan cur síos, i d’fhocail féin, ar an íomhá (ar an bpictiúr) den fhear'),
        ('iii', 'An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.)', 9, '(iii) An maith leat an dán seo?')],
     '(b) An tEarrach Thiar', 'Níl cead aon ábhar a bhaineann le Filíocht Ainmnithe'),
]
POEM_TOPICS = {'poetry-3a-a': 'irish-5-2', 'poetry-3a-b': 'irish-5-3'}
# 3A(b)(i) prints three questions (a) 2, (b) 2 + 2, (c) 2: (slug, sub-question) -> [(letter, scheme question, marks, next cut)]
SLOTS_3A = {
    ('poetry-3a-b', 'i'): [('a', 'Conas atá an aimsir i véarsa a haon?', 2, '(b) Tabhair dhá phointe eolais faoi na mná'),
                           ('b', 'Tabhair dhá phointe eolais faoi na mná i véarsa a trí.', 4, '(c) Cén fhuaim'),
                           ('c', 'Cén fhuaim atá le cloisteáil i véarsa a ceathair?', 2, None)],
}
SLOT_PERMITTED = {('poetry-3a-b', 'i'): [0, 2, 4, 6, 8]}
POETRY_3B = [
    ('poetry-3b-a', 'F-3B-a', [
        '(i) Maidir le dán nua-aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa, scríobh síos i d’fhocail féin, príomhsmaointe an dáin. (9 marc)',
        '(ii) Scríobh síos an mothúchán is láidre sa dán, dar leat. Tabhair dhá shampla den mhothúchán sin sa dán. (7 marc)',
        '(iii) Cén íomhá (pictiúr) is mó a thaitníonn leat sa dán? Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)'],
     '(a) (i) Maidir le dán nua-aimseartha', '(b) (i) Maidir le dán nua-aimseartha', ['(ii) Scríobh síos an mothúchán', '(iii) Cén íomhá', 'Ní mór teideal an dáin']),
    ('poetry-3b-b', 'F-3B-b', [
        '(i) Maidir le dán nua-aimseartha roghnach a ndearna tú staidéar air le linn do chúrsa agus nár úsáid tú i gcuid (a) thuas, scríobh síos príomhthéama an dáin, dar leat. '
        'Tabhair dhá phointe eolais, i d’fhocail féin, faoin bpríomhthéama sin sa dán. (9 marc)',
        '(ii) Luaigh íomhá (pictiúr) amháin ón dán atá suimiúil, dar leat. Mínigh an íomhá (an pictiúr) sin i d’fhocail féin. (Is leor dhá phointe eolais.) (7 marc)',
        '(iii) An maith leat an dán seo? Cuir fáthanna le do fhreagra. (Is leor dhá fháth.) (7 marc)'],
     '(b) (i) Maidir le dán nua-aimseartha', None, ['(ii) Luaigh íomhá', '(iii) An maith leat', 'Ní mór teideal an dáin']),
]
TITLE_LINE = 'Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go cruinn. (2 mharc)'

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
    texts = [clean(p.get_text()) for p in paper]
    s = Scheme(doc, 12, 26)
    assert s.removed == len(FURNITURE), s.removed
    assert not PUA.search(s.text), 'private-use glyph left in the scheme text'
    lang_read = '[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh]'
    assert s.text.count(lang_read) == 2
    for letter, passage in PASSAGES.items():
        page_text = ' '.join(texts[p - 1] for p in passage['pages'])
        after = s.text.index(passage['start'])
        # Each passage prints its own two notes above Ceist 1.
        notes = s.chunk('Nóta: Má tá dhá phointe eolais i gceist', passage['notes_end'], after)[0]
        assert notes.endswith('Nóta: Gearrfar pionós i ngeall ar iomarcaíocht.') and 'Siombailí' not in notes, notes
        passage['notes'] = notes
        resolved = []
        anchors = [p[3] for p in passage['parts']]
        for index, (q, part, prompt, anchor) in enumerate(passage['parts']):
            assert in_order(prompt, page_text), (letter, q, part)
            # The last part ends where the scheme's penalty instructions and mark boxes begin.
            nxt = anchors[index + 1] if index + 1 < len(anchors) else passage['end']
            chunk, spages = s.chunk(anchor, nxt, after)
            after = s.text.index(anchor, after) + 1
            assert '5 mharc' in chunk and '50 marc' not in chunk and 'LÉAMHTHUISCINT' not in chunk and 'Léireofar' not in chunk, (letter, q, part, chunk[:80])
            two = '3 mharc + 2 mharc' in chunk
            permitted = [0, 3, 5] if (two or '= 3 mharc' in chunk) else [0, 5]
            resolved.append((q, part, prompt, chunk, spages, two, permitted))
        passage['resolved'] = resolved
    # The literature note is printed twice (above 2A on PDF 18 and above 3A on PDF 22), word for word.
    lit_note = s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', 'Freagair (a) agus (b) anseo.')[0]
    assert s.chunk('Nóta: Níl sé i gceist a chur in iúl go bhfuil na freagraí samplacha', 'Freagair (a) agus (b) anseo.',
                   s.text.index('⟦22⟧'))[0] == lit_note
    lang_lit = '[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh]'
    # Dís, 2B(a), 2B(b), Géibheann, An tEarrach Thiar, 3B(a), 3B(b); Oisín prints the note with a closing full stop.
    assert s.text.count(lang_lit) == 7 and s.text.count(lang_lit[:-1] + '.]') == 1, s.text.count(lang_lit)
    slug, atlas, letter, title, topic, intro, subs, start, end = DIS
    for line in [intro, title] + [p for _, p, _ in subs]:
        assert in_order(line, texts[7]), (slug, line[:40])
    slug, atlas, letter, title, topic, prompt, start, end = OISIN
    assert in_order(title, texts[7]) and in_order(prompt, texts[7]), slug
    for slug, atlas, lines, start, end, parts, title in PROSE_2B:
        for line in lines:
            assert in_order(line, texts[8]), (slug, line[:50])
    for slug, atlas, page, title, subs, start, end in POETRY_3A:
        assert in_order(title, texts[page - 1]), slug
        for label, prompt, marks, cut in subs:
            assert in_order(prompt.replace('\n', ' ') + f' ({marks} marc)', texts[page - 1]), (slug, label)
    for slug, atlas, prompts, start, end, cuts in POETRY_3B:
        for line in prompts + [TITLE_LINE]:
            assert in_order(line, texts[11]), (slug, line[:50])
    assert comparable(texts[11]).count(comparable(TITLE_LINE)) == 2
    for page, line in [(3, 'FREAGAIR GACH CEIST (1, 2 AGUS 3).'), (8, PROSE_CHOICE), (8, BOTH), (8, BOX_2A), (9, BOX_2B), (9, NO_PRESCRIBED_PROSE), (9, BOTH),
                       (10, POETRY_CHOICE), (10, BOTH), (10, BOX_3A), (12, BOX_3B), (12, NO_PRESCRIBED_POETRY), (12, BOTH)]:
        assert comparable(line) in comparable(texts[page - 1]), (page, line)
    _MATERIAL = dict(paper=paper, texts=texts, s=s, lang_read=lang_read, lit_note=lit_note, lang_lit=lang_lit,
                     decisions=selection_decisions(paper))
    return _MATERIAL


def deduction(m):
    return criterion('gaeilge-deduction', 'Gaeilge lochtach', 4, [m['lang_lit']], 'quality', deduction=True)


def reading_note(m):
    return 'Scheme: “' + m['lang_read'] + '” — one deduction from each passage total (50), never inside a single part.'


def source(label, title, pages):
    return dict(kind='source-text', label=label, title=title, pages=pages, attribution=ATTRIBUTION, presentationNote=SOURCE_NOTE)


def sub_permitted(piece, marks):
    """“3 mharc + 2 mharc”: first correct point 3, second 2 (0/3/5); other sub-questions keep the full range."""
    return [0, 3, 5] if (marks == 5 and '3 mharc + 2 mharc' in piece) else None


def dis_pieces(m):
    slug, atlas, letter, title, topic, intro, subs, start, end = DIS
    whole, spages = m['s'].chunk(start, end)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, cut in subs], slug)
    for (label, _, _), piece in zip(subs, pieces):
        assert '(5 mharc)' in piece, (slug, label)
    return pieces, sorted(set(spages) | {18})


def poem_pieces(m, slug, subs, start, end):
    whole, spages = m['s'].chunk(start, end)
    whole = before_language_note(whole)
    pieces = split_at(whole, [cut for _, _, _, cut in subs], slug)
    for (label, _, marks, _), piece in zip(subs, pieces):
        assert f'({marks} marc)' in piece or (slug, label) in SLOTS_3A, (slug, label, piece[:60])
    return pieces, sorted(set(spages) | {22})


def slot_pieces(piece, slots):
    out = []
    for sub, question, marks, nxt in slots:
        start_at = piece.index(question)
        slot = piece[start_at:piece.index(nxt, start_at) if nxt else len(piece)].strip()
        printed = '(2 mharc + 2 mharc)' if marks == 4 else '(2 mharc)'
        assert 'Freagraí samplacha:' in slot and printed in slot, (sub, slot[:60])
        out.append((sub, slot))
    return out


WHOLE_PROSE_NOTE = ('One complete SEC response: five points at 5 (2 for the bare point + 3 for development); the 0–4 Gaeilge deduction applies once '
                    'to this whole 25-mark answer. The sample points are indicative rather than exhaustive.')
LIT_DEDUCTION_NOTE = 'The 0–4 Gaeilge deduction applies once to this whole 25-mark answer, never inside one sub-question.'


def build():
    m = material()
    cards = []

    def add(key, slug, ref, prompt, topic, pages, scheme_pages, criteria, requirements, note, src, concept=None, stem=None):
        cards.append(dict(
            id=f'irish-{YEAR}-ol-p2-{slug}', year=YEAR, level='ordinary', paper=2, section='2',
            atlasQuestionId=key, questionRef=f'{YEAR} OL Paper 2 {ref}', **({'stem': stem} if stem else {}), questionText=prompt,
            totalMarks=sum(c['maxMarks'] for c in criteria if c['kind'] == 'award'), topicId=topic,
            conceptId=concept or f'irish-ol-p2-{slug}', paperFileid=FILE, paperPage=pages[0], schemeFileid=SCHEME_FILE,
            schemePage=scheme_pages[0], schemePages=scheme_pages, reviewedAt=REVIEWED_AT, reviewedPaperPages=pages,
            taskRequirements=requirements, criteria=criteria, markingGuideNote=note, sourceMaterial=src))

    # ---- Ceist 1: Léamhthuiscint A and B (whole questions first, then their parts) -----------------
    whole_ids, practice_ids = [], []
    for letter, passage in PASSAGES.items():
        src = source(f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        by_q = {}
        for q, part, prompt, chunk, spages, two, permitted in passage['resolved']:
            by_q.setdefault(q, []).append((part, prompt, chunk, spages, permitted))
        for q, parts in by_q.items():
            text = f'{q}. ' + ' '.join(prompt for _, prompt, *_ in parts)
            crits = [criterion(part, f'({part}) Freagra', 5, [chunk, passage['notes']], permitted=permitted) for part, _, chunk, _, permitted in parts]
            # The frozen Atlas identities 1–5 (A) and 6–10 (B) are the whole questions.
            add(str(int(q) + (5 if letter == 'B' else 0)), f'reading-{letter.lower()}-q{q}', f'Léamhthuiscint {letter} · Ceist {q}', text,
                passage['topic'], passage['pages'], sorted({p for *_, sp, _ in parts for p in sp}), crits, READING_WHOLE,
                'Complete printed question: (a) 5 + (b) 5, each scored separately at its SEC allocation. ' + reading_note(m), src,
                concept=f'irish-reading-{letter.lower()}-q{q}')
            whole_ids.append(cards[-1]['id'])
    for letter, passage in PASSAGES.items():
        src = source(f'Léamhthuiscint {letter}', passage['title'], passage['pages'])
        for q, part, prompt, chunk, spages, two, permitted in passage['resolved']:
            add(f'R-{letter}-{q}-{part}', f'reading-{letter.lower()}-q{q}-{part}', f'Léamhthuiscint {letter} · Ceist {q}({part})',
                f'{q}{prompt}', passage['topic'], passage['pages'], spages,
                [criterion(part, 'Freagra', 5, [chunk, passage['notes']], permitted=permitted)], READING_PART,
                'SEC allocation for this part' + (': first correct point 3, second 2 (0/3/5).' if two else '.') + ' ' + reading_note(m), src)
            practice_ids.append(cards[-1]['id'])

    note, lang = m['lit_note'], m['lang_lit']
    sub_note = 'One printed sub-question at its published tariff. ' + LIT_DEDUCTION_NOTE
    question_lit = []
    # ---- Ceist 2A: Dís (five sub-questions) and Oisín i dTír na nÓg -----------------------------------
    slug, atlas, letter, title, topic, intro, subs, start, end = DIS
    pieces, spages = dis_pieces(m)
    src = source('Prós Ainmnithe', title, [8])
    requirements = [PROSE_CHOICE, BOTH] + LIT
    add(atlas, slug, 'Prose 2A(a)', f'({letter}) {title}\n{intro}\n' + '\n'.join(f'({l}) {p}' for l, p, _ in subs) + '\n(25 marc)',
        topic, [8], spages,
        [criterion(f'eolas-{label}', f'({label}) Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))
         for (label, _, _), piece in zip(subs, pieces)] + [deduction(m)], requirements,
        'One complete SEC response: five printed sub-questions at 5 each, then the 0–4 Gaeilge deduction once. '
        'The sample answers are indicative rather than exhaustive.', src, concept=f'irish-prose-2a-{topic}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])
    slug_o, atlas_o, letter_o, title_o, topic_o, prompt_o, start_o, end_o = OISIN
    chunk, ospages = m['s'].chunk(start_o, end_o)
    assert '5 phointe eolais agus 5 mharc ar gach pointe eolais' in chunk
    add(atlas_o, slug_o, 'Prose 2A(b)', f'({letter_o}) {title_o}\n{prompt_o}\n(25 marc)', topic_o, [8], sorted(set(ospages) | {18}),
        [criterion('eolas', 'Eolas', 25, [before_language_note(chunk), note], 'indicative'), deduction(m)], [PROSE_CHOICE, BOTH] + LIT[1:],
        WHOLE_PROSE_NOTE, source('Prós Ainmnithe', title_o, [8]), concept=f'irish-prose-2a-{topic_o}', stem=BOX_2A)
    question_lit.append(cards[-1]['id'])

    # ---- Ceist 2B: Prós Roghnach (a) and (b) ------------------------------------------------------------
    for slug2, atlas2, lines, start2, end2, parts, title2 in PROSE_2B:
        chunk2, spages2 = m['s'].chunk(start2, end2)
        chunk2 = before_language_note(chunk2)
        cuts = [0] + [chunk2.index(cut) for _, _, _, cut in parts[1:]]
        bits = [chunk2[a:b].strip() for a, b in zip(cuts, cuts[1:] + [len(chunk2)])]
        crits = [criterion(cid, label, marks, [bit], 'exact' if cid == 'teideal' else 'indicative',
                           permitted=None if cid == 'eolas' else sorted({0, marks} | {int(v) for v in re.findall(r'= (\d) mharc', bit)}))
                 for (cid, label, marks, _), bit in zip(parts, bits)]
        assert crits[-1]['guidance'][0].endswith('(2 mharc)'), (slug2, crits[-1]['guidance'][0][-60:])
        add(atlas2, slug2, f'Prose 2B({atlas2[-1]})', '\n'.join(lines), 'irish-4-7', [9], spages2, crits + [deduction(m)],
            [PROSE_CHOICE, NO_PRESCRIBED_PROSE, BOTH] + LIT[1:],
            'One complete SEC response: ' + ', '.join(f'{label} {marks}' for _, label, marks, _ in parts) +
            ', then the 0–4 Gaeilge deduction once. The optional text is open content chosen by the candidate; the scheme prints no sample '
            'points for it, so its points are judged on merit against these allocations (indicative rather than exhaustive).',
            source('Prós Roghnach', title2, [9]), concept='irish-prose-2b-irish-4-7', stem=STEM_2B)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3A: Géibheann and An tEarrach Thiar ------------------------------------------------------
    poem_parts = {}
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3 = poem_pieces(m, slug3, subs3, start3, end3)
        poem_parts[slug3] = (pieces3, spages3)
        crits = [criterion(f'eolas-{label}', f'({label}) Eolas', marks, [piece, note], 'indicative', permitted=SLOT_PERMITTED.get((slug3, label)))
                 for (label, _, marks, _), piece in zip(subs3, pieces3)]
        prompt = '\n'.join(f'({label}) {p}' + f' ({marks} marc)' for label, p, marks, _ in subs3)
        add(atlas3, slug3, f'Poetry 3A({atlas3[-1]})', f'({atlas3[-1]}) {title3}\n' + prompt, POEM_TOPICS[slug3], [page], spages3, crits + [deduction(m)],
            [POETRY_CHOICE, BOTH] + LIT,
            'One complete SEC response: (i) 8, (ii) 8, (iii) 9 at their printed tariffs, then the 0–4 Gaeilge deduction once. '
            'The sample points are indicative rather than exhaustive; lines lifted straight from the poem without the candidate’s own words earn 2 + 2.',
            source('Filíocht Ainmnithe', title3, [page]), concept=f'irish-poetry-3a-{POEM_TOPICS[slug3]}', stem=BOX_3A)
        question_lit.append(cards[-1]['id'])

    # ---- Ceist 3B: Filíocht Roghnach (a) and (b) --------------------------------------------------------
    for slug4, atlas4, prompts, start4, end4, cuts4 in POETRY_3B:
        chunk4, spages4 = m['s'].chunk(start4, end4, m['s'].text.index('⟦25⟧'))
        chunk4 = before_language_note(chunk4)
        idx = [0] + [chunk4.index(cut) for cut in cuts4]
        bits = [chunk4[a:b].strip() for a, b in zip(idx, idx[1:] + [len(chunk4)])]
        for bit, cap in zip(bits, ['(9 marc)', '(7 marc)', '(7 marc)', '(2 mharc)']):
            assert cap in bit, (slug4, cap)
        crits = [criterion('eolas-i', '(i) Eolas', 9, [bits[0]], 'indicative'), criterion('eolas-ii', '(ii) Eolas', 7, [bits[1]], 'indicative'),
                 criterion('eolas-iii', '(iii) Eolas', 7, [bits[2]], 'indicative'),
                 criterion('teideal', 'Teideal + ainm an fhile', 2, [bits[3]], 'exact', permitted=[0, 1, 2])]
        add(atlas4, slug4, f'Poetry 3B({atlas4[-1]})', f'({atlas4[-1]}) ' + '\n'.join(prompts + [TITLE_LINE]), 'irish-5-6', [12], spages4,
            crits + [deduction(m)], [POETRY_CHOICE, NO_PRESCRIBED_POETRY, BOTH] + LIT,
            'One complete SEC response: (i) 9, (ii) 7, (iii) 7, poem and poet 2, then the 0–4 Gaeilge deduction once. '
            'The optional poem is open content; 3B(b) asks for a modern poem not used in 3B(a). The printed allocations are judged on merit '
            '(indicative rather than exhaustive).',
            source('Filíocht Roghnach', f'3B({atlas4[-1]}) · Dán roghnach', [12]),
            concept='irish-poetry-3b-irish-5-6', stem=STEM_3B)
        question_lit.append(cards[-1]['id'])

    # ---- Practice: the five Dís sub-questions, every prescribed-poetry sub-question, 3A(b)(i)(a)–(c) ----
    src = source('Prós Ainmnithe', title, [8])
    for (label, prompt, _), piece in zip(subs, pieces):
        # The paper prints no per-sub-question tariff for 2A(a); the scheme prices each at (5 mharc).
        add(f'{atlas}-{label}', f'{slug}-{label}', f'Prós 2A({letter}) · {title} · ({label})', f'({letter}) {title}\n{intro}\n({label}) {prompt}',
            topic, [8], spages, [criterion('eolas', 'Eolas', 5, [piece, note], 'indicative', permitted=sub_permitted(piece, 5))],
            [PROSE_CHOICE, BOTH] + LIT[1:], sub_note, src, stem=BOX_2A)
        practice_ids.append(cards[-1]['id'])
    for slug3, atlas3, page, title3, subs3, start3, end3 in POETRY_3A:
        pieces3, spages3 = poem_parts[slug3]
        topic3 = POEM_TOPICS[slug3]
        src3 = source('Filíocht Ainmnithe', title3, [page])
        head = f'({atlas3[-1]}) {title3}\n'
        for (label, prompt, marks, _), piece in zip(subs3, pieces3):
            slots = SLOTS_3A.get((slug3, label))
            add(f'{atlas3}-{label}', f'{slug3}-{label}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})', head + f'({label}) {prompt} ({marks} marc)',
                topic3, [page], spages3,
                [criterion('eolas', 'Eolas', marks, [piece, note], 'indicative', permitted=SLOT_PERMITTED.get((slug3, label)))],
                [POETRY_CHOICE, BOTH] + LIT[1:], sub_note, src3, stem=BOX_3A)
            practice_ids.append(cards[-1]['id'])
            if slots:
                printed = dict(re.findall(r'\(([a-c])\) ([^\n]+)', prompt))
                for (sub, slot), (_, _, smarks, _) in zip(slot_pieces(piece, slots), slots):
                    add(f'{atlas3}-{label}-{sub}', f'{slug3}-{label}-{sub}', f'Filíocht 3A({atlas3[-1]}) · {title3} · ({label})({sub})',
                        head + f'({label}) ({sub}) {printed[sub]}', topic3, [page], spages3,
                        [criterion('eolas', 'Freagra', smarks, [slot], 'indicative', permitted=list(range(0, smarks + 1, 2)))], [POETRY_CHOICE, BOTH] + LIT[1:],
                        f'One printed question inside 3A({atlas3[-1]})({label}), at its printed ({smarks} marc). ' + LIT_DEDUCTION_NOTE, src3, stem=BOX_3A)
                    practice_ids.append(cards[-1]['id'])

    assert len(whole_ids) == 10 and len(question_lit) == 8 and len(practice_ids) == 34, (len(whole_ids), len(question_lit), len(practice_ids))
    assert len(cards) == 52 and len({c['id'] for c in cards}) == 52 and len({c['atlasQuestionId'] for c in cards}) == 52
    for card in cards:
        assert sum(c['maxMarks'] for c in card['criteria'] if c['kind'] == 'award') == card['totalMarks'], card['id']
        for c in card['criteria']:
            assert c['guidance'] and all(not re.search('Siombailí Anótála|50 marc|Léirigh mionbhriseadh', g) and not PUA.search(g) for g in c['guidance']), (card['id'], c['id'])
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
                  boundaries=('10 whole reading questions with their 20 published parts; 8 literature questions; the 5 printed 2A(a) Dís '
                              'sub-questions, the 6 prescribed-poetry sub-questions and the 3 printed questions inside 3A(b)(i).'))
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
    print(f"Irish Ordinary {YEAR} Paper 2: {len(data['cards'])} reviewed cards (18 printed questions, 34 practice parts); the archive remains incomplete.")


if __name__ == '__main__':
    main()
