#!/usr/bin/env python3
"""Irish guidance carries the SEC's words only: lift, never write (coordinator decision, 2026-11-04).

A criterion's `guidance` is shown to students as the published scheme. Builders used to add their own
sentences to it: Irish ones ("Aon fhreagra ceart don chuid seo = 1 mharc. …"), and English examiner
notes ("Apply only the 0–4 language deduction printed by the scheme; …"). `scheme_words(cards)` is the
last step of every Irish builder before it writes its file:

- Each guidance line is cut into fragments (sentences, bullets, "—" clauses). A fragment is the SEC's
  when it is in that year's printed Irish papers or marking schemes: the local corpus PDFs and the
  repaired scheme extractions in examiner-reports/irish/schemes. Whitespace, case and punctuation are
  ignored, and a fragment with at least 60% of its three-word runs in that text is the SEC's too (a
  table read across its columns, a line broken by a page).
- A run of consecutive fragments that is not the SEC's leaves the guidance. If the run is English it is
  our examiner note and moves, word for word, to the card's English `markingGuideNote`; if it is Irish
  it is dropped: the card says nothing in Irish of our own.

The question is the paper's print too (`printed_question`, run first): the lines builders added to it in Irish
("An rogha don chárta seo: A(a).", "Léigh an téacs ar leathanach 7.", "Don chárta seo: tabhair freagra amháin …")
are gone. What a one-answer card practises is said in English in `practiceFocus`, and a source note is English.
A task check (`taskRequirements`) is the paper's own instruction or English (`printed_tasks`).

`written(card)` lists what a card still carries that is not the SEC's; irish_tools/lift_audit.py runs it
over every committed card file, and regenerate.sh --check fails if anything remains.
"""
from __future__ import annotations
import glob
import os
import re
import unicodedata
from functools import lru_cache

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SPLIT = re.compile(r'(?<=[.?!;:])\s+|\s+[•▪]\s*|¶|\s+—\s+')
# English words that are not also Irish ones ("a", "an", "as", "do", "is" are both).
ENGLISH = frozenset('the and of to are only for this that with be by not apply mark marks scheme paper printed when '
                    'where each its it from or at than per both once which then than into'.split())
# A line keeps its SEC fragments when at least this share of it is the SEC's; below it the line is ours.
SEC_SHARE = 0.3


def norm(text: str) -> str:
    return re.sub(r'[^a-z0-9áéíóú]+', '', unicodedata.normalize('NFKC', text).lower())


@lru_cache(maxsize=None)
def corpus(year: int) -> str:
    import fitz
    texts = []
    for kind in ('markingschemes', 'exampapers'):
        for path in sorted(glob.glob(os.path.join(ROOT, 'paper-trail-corpus', kind, str(year), 'LC001*.pdf'))):
            texts.append(' '.join(page.get_text() for page in fitz.open(path)))
    for path in sorted(glob.glob(os.path.join(ROOT, 'examiner-reports', 'irish', 'schemes', f'{year}-*.md'))):
        texts.append(open(path, encoding='utf-8').read())
    assert texts, f'No local Irish papers or schemes for {year}'
    return norm(' '.join(texts))


def sec(fragment: str, text: str) -> bool:
    words = [w for w in (norm(x) for x in fragment.split()) if w]
    joined = ''.join(words)
    if len(joined) < 6 or joined in text:
        return True
    runs = [''.join(words[i:i + 3]) for i in range(max(1, len(words) - 2))]
    return sum(run in text for run in runs) / len(runs) >= 0.6


def english(fragment: str) -> bool:
    words = re.findall(r'[A-Za-z]+', fragment.lower())
    hits = sum(word in ENGLISH for word in words)
    return bool(words) and (hits >= 2 or hits / len(words) >= 0.2)


def label(fragment: str) -> bool:
    """A heading such as "Foclóir:" or "Nótaí (scheme PDF 6):", which introduces what follows it."""
    return fragment.strip().endswith(':') and len(fragment.split()) <= 6


def split_line(line: str, text: str):
    """The line as (fragment, separator after it, is the SEC's), in order; joining fragment + separator
    for every entry gives the line back."""
    pieces, pos = [], 0
    for match in SPLIT.finditer(line):
        pieces.append((line[pos:match.start()], match.group(0)))
        pos = match.end()
    pieces.append((line[pos:], ''))
    return [(piece, sep, sec(piece, text)) for piece, sep in pieces]


# Lines the builders added to a card's question in Irish of their own: "An rogha don chárta seo: A(a)." after a
# printed option, "Léigh an téacs ar leathanach 7." before a Foundation question, "Don chárta seo: tabhair freagra
# amháin …" after a two-answer part. The paper prints none of them.
CARD_SCOPE = re.compile(r'Don chárta seo|An rogha don chárta seo|Léigh an téacs ar leathanach \d')
OPTION_LINE = re.compile(r'\n\nAn rogha don chárta seo: [^\n]*$')
PAGE_POINTER = re.compile(r'^Léigh an téacs ar leathanach \d+\.\n\n')


# Builder-written Irish task checks: the paper's own sentence where it prints the instruction, else English.
TASK_PRINTED = {
    'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.':
        'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t-ábhar a scríobhtar.',
    'Timpeall 500–600 focal.': 'Ní gá níos mó ná 500-600 focal nó mar sin a scríobh i gcás ar bith.',
    'Freagair i nGaeilge, ach amháin nuair nach gá sin.':
        'Caithfidh do chuid freagraí uile sa triail seo a bheith i nGaeilge, ach amháin nuair nach gá sin.',
}
TASK_ENGLISH = {
    # Whole lines whose printed pieces are too short to stand alone.
    'Luaigh 1/3/2/2 pointe faoi na ceithre phictiúr; seoladh, dáta, tús agus críoch oiriúnach.':
        'Give 1, 3, 2 and 2 points about the four pictures; an address, a date, and a suitable opening and close.',
    'Luaigh 1/2/3/2 pointe faoi na ceithre phictiúr; seoladh, dáta, tús agus críoch oiriúnach.':
        'Give 1, 2, 3 and 2 points about the four pictures; an address, a date, and a suitable opening and close.',
    'Luaigh gach pointe agus dhá rud faoin gceolchoirm; tús agus críoch oiriúnach.':
        'Cover every point and two things about the concert; a suitable opening and close.',
    'Luaigh gach pointe agus dhá rud faoin gcluiche; tús agus críoch oiriúnach.':
        'Cover every point and two things about the match; a suitable opening and close.',
    'Dhá phointe eolais faoi gach ceann de na ceithre phictiúr; leagan amach cuí.':
        'Two points of information about each of the four pictures; a suitable layout.',
    'Tabhair cúig thagairt ar a laghad; i 6(b), ceann do gach pictiúr agus pointe amháin eile.':
        'Give at least five references; in 6(b), one for each picture and one more point.',
    'Tabhair cúig thagairt ar a laghad; i5(b), ceann do gach pictiúr agus ceann amháin eile.':
        'Give at least five references; in 5(b), one for each picture and one more.',
    'Líon gach réimse riachtanach; cúig ábhar scoile agus trí chaitheamh aimsire.':
        'Fill in every required field; five school subjects and three pastimes.',
    'Líon gach réimse; cúig ábhar scoile agus trí spórt.': 'Fill in every field; five school subjects and three sports.',
    'Líon gach réimse; cúig ábhar scoile agus trí chaitheamh aimsire.': 'Fill in every field; five school subjects and three pastimes.',
    'Líon gach réimse riachtanach; cúig ábhar scoile agus trí spórt is féidir leat a mhúineadh.':
        'Fill in every required field; five school subjects and three sports you could teach.',
    'Scríobh chuig Úna faoin gcluiche rugbaí; sé shonra i bpictiúr 1 agus na trí threoir eile.':
        'Write to Úna about the rugby match; six details in picture 1 and the other three instructions.',
    # Sentences.
    'Léigh an sliocht iomlán a ghabhann leis an gceist.': 'Read the whole extract that goes with the question.',
    'Freagair an chuid atá luaite ar an gcárta.': 'Answer the part this card names.',
    'Úsáid an t-alt a luaitear.': 'Use the paragraph the question names.',
    'Éist leis an taifeadadh.': 'Listen to the recording.',
    'Úsáid na pictiúir ar an leathanach nuair is gá.': 'Use the pictures on the page where needed.',
    'Úsáid tagairtí cruinne agus ábhartha don téacs.': 'Use accurate, relevant references to the text.',
    'Glacfar le focail an tsleachta nó le do chuid focal féin, ach ní mór 6(b) a fhreagairt i d’fhocail féin.':
        'The extract’s words or your own are accepted, but 6(b) must be answered in your own words.',
    'Léigh an sliocht oifigiúil a ghabhann leis an gceist.': 'Read the official extract that goes with the question.',
    'Freagair gach fochuid agus cloígh leis an alt a luaitear.': 'Answer every sub-part and keep to the paragraph the question names.',
    'Freagair gach fochuid atá priontáilte sa rogha seo.': 'Answer every sub-part printed in this option.',
    'Éist leis an taifeadadh oifigiúil.': 'Listen to the official recording.',
    'Lean an fhoirm scríbhneoireachta a iarrtar sa cheist.': 'Write in the form the question asks for.',
    'Coinnigh ceangal cinnte leanúnach idir an teideal agus an t-ábhar.': 'Keep a clear, continuous link between the title and what you write.',
    'Bain úsáid as do chuid focal féin nuair a iarrtar ort é.': 'Use your own words where the question asks you to.',
    'Freagair gach mír atá priontáilte ar an gcárta.': 'Answer every item printed on the card.',
    'Úsáid eolas cruinn agus samplaí ábhartha ón téacs.': 'Use accurate information and relevant examples from the text.',
    'Freagair i nGaeilge, ach amháin nuair nach gá sin.': 'Answer in Irish, except where that is not needed.',
    'Freagair gach cuid den cheist atá priontáilte.': 'Answer every printed part of the question.',
    'Bain úsáid as Gaeilge chruinn, shaibhir atá oiriúnach don tasc.': 'Use accurate, rich Irish suited to the task.',
    'Timpeall 500–600 focal.': 'About 500–600 words.',
    'Scríobh timpeall 90 focal in Iris na Scoile.': 'Write about 90 words for the school magazine (Iris na Scoile).',
    'Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.': 'Give at least five references to the event in the pictures.',
    'Ná húsáid ábhar ainmnithe i bhfreagra ar an ábhar roghnach.': 'Do not use prescribed material in an answer on optional material.',
    'Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.': 'Write a notice based on the four pictures and the instructions.',
    'Ní mór teideal an tsaothair agus ainm an scríbhneora a scríobh síos go cruinn.': 'Write the title of the work and the writer’s name accurately.',
    'Líon gach réimse agus scríobh alt timpeall 40 focal.': 'Fill in every field and write a paragraph of about 40 words.',
    'Scríobh fógra faoin turas rothaíochta bunaithe ar gach pictiúr agus ar na treoracha.':
        'Write a notice about the cycling trip based on every picture and the instructions.',
    'Scríobh freagra chuig Phil agus freagair gach ceann de na sé threoir.': 'Write a reply to Phil and answer each of the six instructions.',
    'Scríobh chuig cara faoin ollstór agus an áit, trí phointe faoin obair, tagairt faoi na custaiméirí, agus dhá thagairt do na himeachtaí sa phictiúr deireanach.':
        'Write to a friend about the superstore and the place: three points about the work, a reference to the customers, and two references to the events in the last picture.',
    'Scríobh timpeall 40 focal faoi obair ar Chúrsa Gailf.': 'Write about 40 words about working on a golf course.',
    'Scríobh fógra bunaithe ar gach pictiúr agus ar na treoracha.': 'Write a notice based on every picture and the instructions.',
    'Scríobh chuig cara faoin ngaráiste agus an áit, trí phointe faoin obair, dhá phointe faoi na daoine, agus na gníomhaíochtaí saor-ama.':
        'Write to a friend about the garage and the place: three points about the work, two points about the people, and the free-time activities.',
    'Scríobh timpeall 40 focal faoi obair in Ollstór Tesco.': 'Write about 40 words about working in Tesco.',
    'Scríobh timpeall40 focal faoi bheith ag obair in Ionad Spóirt.': 'Write about 40 words about working in a sports centre.',
    'Scríobh litir chuig do chara faoi do phost samhraidh san ospidéal.': 'Write a letter to your friend about your summer job in the hospital.',
    'Scríobh timpeall 40 focal faoin bpost san óstán.': 'Write about 40 words about the job in the hotel.',
    'Scríobh litir chuig do chara faoi do phost samhraidh san aerfort.': 'Write a letter to your friend about your summer job at the airport.',
    'Scríobh timpeall 40 focal faoin bpost sa chumann gailf.': 'Write about 40 words about the job in the golf club.',
    'Scríobh freagra ar chuireadh Áine mar Colm.': 'Write a reply to Áine’s invitation as Colm.',
    'Scríobh timpeall 40 focal faoin bpost sa siopa ríomhaireachta.': 'Write about 40 words about the job in the computer shop.',
    'Scríobh litir chuig do dheartháir nó do dheirfiúr i Londain faoin gcluiche mór.': 'Write a letter to your brother or sister in London about the big match.',
    'Scríobh freagra ar chuireadh Áine mar Ruairí.': 'Write a reply to Áine’s invitation as Ruairí.',
    'Scríobh litir chuig do dheartháir nó do dheirfiúr i gCeanada faoin saoire.': 'Write a letter to your brother or sister in Canada about the holiday.',
    'Scríobh litir chuig d’aintín nó d’uncail i Meiriceá faoin gceolchoirm.': 'Write a letter to your aunt or uncle in America about the concert.',
    'Scríobh litir chuig do chara faoi do phost san óstán.': 'Write a letter to your friend about your job in the hotel.',
    'Scríobh litir chuig do chara faoin turas go Londain.': 'Write a letter to your friend about the trip to London.',
}
# Printed task lines the 2011 corpus cannot show word for word: the Irish paper is a scan, and the English-version
# scheme prints "50 Marc" between the heading and the instruction ("Ceist 2 50 Marc Freagair do rogha …").
TASK_SCAN_PRINTED = {'Ceist 2 Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.',
                     'Ceist 3 Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.'}


ENGLISH_TASKS = frozenset(TASK_ENGLISH.values())


def english_task(fragment: str) -> bool:
    return fragment.strip() in ENGLISH_TASKS or english(fragment)


def task_printed(fragment: str, text: str) -> bool:
    return norm(fragment) in text or (fragment.strip() in TASK_SCAN_PRINTED and sec(fragment, text))


def printed_tasks(card: dict) -> dict:
    """A task check is the paper's own instruction or plain English: the student reads it under "Task check", and
    Irish there reads as the SEC's. A line the paper prints stays; a line of ours becomes the paper's sentence for
    the same instruction where it prints one (TASK_PRINTED), else its English (TASK_ENGLISH). Anything else fails."""
    text = corpus(card['year'])
    out: list[str] = []
    for line in card.get('taskRequirements', []):
        if line in ENGLISH_TASKS:
            out.append(line)
            continue
        if line in TASK_PRINTED and not task_printed(line, text) and norm(TASK_PRINTED[line]) in text:
            out.append(TASK_PRINTED[line])
            continue
        if line in TASK_ENGLISH and not task_printed(line, text):
            out.append(TASK_ENGLISH[line])
            continue
        printed_run: list[str] = []
        english_run: list[str] = []

        def flush() -> None:
            if printed_run:
                out.append(' '.join(printed_run))
                printed_run.clear()
            if english_run:
                out.append(' '.join(english_run))
                english_run.clear()
        for fragment in (f.strip() for f in SPLIT.split(line) if f and f.strip()):
            if task_printed(fragment, text):
                if english_run:
                    flush()
                printed_run.append(fragment)
            elif fragment in TASK_PRINTED and norm(TASK_PRINTED[fragment]) in text:
                flush()
                out.append(TASK_PRINTED[fragment])
            elif fragment in TASK_ENGLISH or english_task(fragment):
                if printed_run:
                    flush()
                english_run.append(TASK_ENGLISH.get(fragment, fragment))
            else:
                raise AssertionError((card['id'], 'task check of ours with no printed or English form', fragment))
        flush()
    card['taskRequirements'] = list(dict.fromkeys(out))
    return card


# The SEC typesets bullets and arrows in SymbolMT, whose codes the text layer returns as private-use characters
# (U+F0xx) that no student font draws. Adobe Symbol encoding gives each code its character: 0xB7 is the bullet,
# 0xAE the right arrow. The fonts were read from the PDFs (2019, 2021, 2022, 2024), not guessed.
SYMBOL_PUA = {'\uf0b7': '•', '\uf0ae': '→'}
PUA = re.compile('[\ue000-\uf8ff]')


def symbol_text(text: str) -> str:
    for code, char in SYMBOL_PUA.items():
        text = text.replace(code, char)
    return text


def repair_glyphs(card: dict) -> dict:
    for field in ('questionText', 'stem', 'markingGuideNote'):
        if card.get(field):
            card[field] = symbol_text(card[field])
    card['taskRequirements'] = [symbol_text(line) for line in card.get('taskRequirements', [])]
    for criterion in card['criteria']:
        criterion['guidance'] = [symbol_text(line) for line in criterion['guidance']]
    return card


def printed_question(cards: list[dict]) -> list[dict]:
    """A card's question is the paper's print only. The chosen option is already the one printed option the card
    shows, and a Foundation card's page is in its source reader, so both lines go; a card that practises one answer
    of a printed pair says so in English, in `practiceFocus` (shown as "Practise: …"), never in the question."""
    for card in cards:
        repair_glyphs(card)
        text = OPTION_LINE.sub('', card['questionText'])
        if PAGE_POINTER.match(text):
            assert card.get('sourceMaterial', {}).get('pages'), (card['id'], 'page pointer without a source reader')
            text = PAGE_POINTER.sub('', text)
        card['questionText'] = text
        for field in ('questionText', 'stem', 'practiceFocus', 'practiceInstruction'):
            assert not CARD_SCOPE.search(card.get(field) or ''), (card['id'], field, 'card-scope Irish of ours')
        notice = card.get('sourceDiscrepancyNotice')
        assert not notice or english(notice), (card['id'], 'source note in Irish of ours')
        printed_tasks(card)
    return cards


def written(card: dict) -> list[str]:
    text = corpus(card['year'])
    out = [piece for criterion in card['criteria'] for line in criterion['guidance']
           for piece, _, is_sec in split_line(line, text) if piece.strip() and not is_sec]
    out += [f'{field}: {match.group(0)}' for field in ('questionText', 'stem', 'practiceFocus', 'practiceInstruction')
            for match in [CARD_SCOPE.search(card.get(field) or '')] if match]
    notice = card.get('sourceDiscrepancyNotice')
    if notice and not english(notice):
        out.append(f'sourceDiscrepancyNotice: {notice[:60]}')
    shown = [card.get('questionText') or '', card.get('stem') or '', card.get('markingGuideNote') or '',
             *card.get('taskRequirements', []), *(line for criterion in card['criteria'] for line in criterion['guidance'])]
    out += [f'private-use glyph {hex(ord(match.group(0)))}' for line in shown for match in [PUA.search(line)] if match]
    out += [f'taskRequirements: {fragment[:80]}' for line in card.get('taskRequirements', []) if line not in ENGLISH_TASKS
            for fragment in (f.strip() for f in SPLIT.split(line) if f and f.strip())
            if not task_printed(fragment, text) and not english_task(fragment)]
    return out


# A poetry Plé band table ("Catagóir Plé (11 mharc) Marcanna Sármhaith … 10-11 … Lag/An-lag … 0-3", 2026 without
# the "(11 mharc)"): the scheme prints it after the question's last part, so a builder that cuts parts in print order
# leaves it on (ii) or (iii). Its header (or its top printed value) is the price of the one row it scales.
PLE_BAND = re.compile(r'Catagóir Plé(?: \((\d+) mharc\))? Marcanna Sármhaith .*?Lag/An-lag Eolas an-bhearnach, '
                      r'an-mhíchruinn agus an-lochtach (\d+)\s*-\s*(\d+)')


def return_band_tables(card: dict) -> dict:
    """Return a Plé band table to the criterion whose row it prices: where its host has no row at the table's price and
    exactly one other criterion of the card does ("Plé … = 11 mharc"), the table moves there, as printed."""
    def priced(criterion, marks):
        return any(re.search(rf'=\s*{marks}\s*mh?arc\b', line) for line in criterion['guidance'])
    for host in card['criteria']:
        for index, line in enumerate(host['guidance']):
            for table in list(PLE_BAND.finditer(line)):
                tops = [int(v) for v in re.findall(r'(\d+)\s*-\s*(\d+)|(?<=\s)(\d+)(?=\s)', table.group(0)) for v in v if v]
                marks = int(table.group(1)) if table.group(1) else max(tops)
                if priced(host, marks):
                    continue
                homes = [c for c in card['criteria'] if c is not host and priced(c, marks)]
                if len(homes) != 1:
                    continue
                host['guidance'][index] = re.sub(r'\s{2,}', ' ', line.replace(table.group(0), ' ')).strip()
                homes[0]['guidance'].append(table.group(0))
                line = host['guidance'][index]
        host['guidance'] = [line for line in host['guidance'] if line.strip()]
    return card


def scheme_words(cards: list[dict]) -> list[dict]:
    printed_question(cards)
    for card in cards:
        return_band_tables(card)
    for card in cards:
        text = corpus(card['year'])
        notes: list[str] = []

        def leave(run: list[str]) -> None:
            # An English run is our examiner note: it moves to the card's note. An Irish run is dropped, and so
            # is a bare heading of ours ("Nótaí (scheme PDF 6):"); an English one ("S4 applies to this title:")
            # keeps its sense in the note.
            if not run or not english(' '.join(run)):
                return
            if len(run) == 1 and label(run[0]):
                if sum(word in ENGLISH for word in re.findall(r'[A-Za-z]+', run[0].lower())) >= 2:
                    notes.append(run[0].rstrip(': ') + '.')
                return
            notes.append(' '.join(run))

        for criterion in card['criteria']:
            kept_lines = []
            for line in criterion['guidance']:
                pieces = split_line(line, text)
                total = sum(len(norm(p)) for p, _, _ in pieces) or 1
                share = sum(len(norm(p)) for p, _, is_sec in pieces if is_sec) / total
                if all(is_sec for _, _, is_sec in pieces):
                    kept_lines.append(line)
                    continue
                # A compact list we typed from a printed table ("80–90 focal: 0; 60–79: −2; …", "seoladh2; aois1; …")
                # is ours as a whole, even where some of its items match the table.
                items = line.split(';')
                compact = len(items) >= 4 and sum(len(norm(item)) for item in items) / len(items) < 30
                if share < SEC_SHARE or compact:
                    leave([line.strip()])
                    continue
                kept, run = [], []
                for index, (piece, sep, is_sec) in enumerate(pieces):
                    following = pieces[index + 1] if index + 1 < len(pieces) else None
                    if piece.strip() and not is_sec:
                        run.append(piece.strip())
                        continue
                    # A heading of the SEC's whose content was ours goes with it ("Foclóir:" before a typed list).
                    if label(piece) and following and following[0].strip() and not following[2]:
                        continue
                    leave(run)
                    run = []
                    kept.append(piece + sep)
                leave(run)
                line_out = re.sub(r'^[\s;:,—–-]+|[\s;,—–-]+$', '', re.sub(r'\s{2,}', ' ', ''.join(kept).strip()))
                if norm(line_out):
                    kept_lines.append(line_out)
            criterion['guidance'] = kept_lines
        if notes:
            base = card.get('markingGuideNote', '').strip()
            extra = [n for n in dict.fromkeys(notes) if norm(n) not in norm(base)]
            card['markingGuideNote'] = ' '.join([base, *extra]).strip()
    return cards


def scheme_words_in(output: dict) -> dict:
    """`scheme_words` on a builder's output: a card file ({'cards': […], …}) or several keyed by name."""
    if isinstance(output.get('cards'), list):
        scheme_words(output['cards'])
    else:
        for value in output.values():
            if isinstance(value, dict) and isinstance(value.get('cards'), list):
                scheme_words(value['cards'])
    return output


LENGTH_TABLE = re.compile(r'Líon [Ff]ocal Pionós.*?(?:<\s?30(?: focal)? - 4(?: mharc)?|<10 - 3|1-19 - 1)')


def printed(text: str, pattern: str) -> str:
    """The scheme's own words matching `pattern` in a page's text, on one line (asserting they are printed)."""
    match = re.search(pattern, re.sub(r'\s+', ' ', text))
    assert match, ('Not printed on this scheme page', pattern)
    return match.group(0).strip()


def printed_length(text: str) -> str:
    """The Foundation scheme's printed word-count table ("Líon Focal Pionós 80-90 0 60-79 - 2 …")."""
    return printed(text, LENGTH_TABLE.pattern)


HEAD = re.compile(r'^Freagair (?:Ceist )?([23])A \((?:Prós|Filíocht) Ainmnithe\) nó (?:Ceist )?\1B \((?:Prós|Filíocht) Roghnach\)\.')
OPTION = re.compile(r'^\((?:a|b|c)\)(?:\s|$)')


def printed_lead_in(cards: list[dict]) -> list[dict]:
    """The section lines a literature question's page prints before the question proper ("Freagair 2A … nó 2B …",
    "2B Prós Roghnach", "Freagair do rogha …", "Níl cead aon ábhar …") become the card's stem, one printed line to
    a line, so the restriction is its own lead-in line, never a sentence of the question's last part (as the
    2022 and 2024 Higher routes do). The question text starts at the printed option, "(a)", "(b)" or "(c)"."""
    for card in cards:
        text = card['questionText']
        if not HEAD.match(text):
            continue
        lines = text.split('\n')
        start = next(index for index, line in enumerate(lines) if OPTION.match(line.strip()))
        # The builders joined a heading to its directive with " — " and the directives with spaces; the paper
        # sets each on its own line.
        head = [sentence.strip() for line in lines[:start] for part in line.split(' — ')
                for sentence in re.split(r'(?<=\.)\s+(?=(?:Freagair|Níl)\b)', part) if sentence.strip()]
        card['stem'] = '\n'.join(head)
        card['questionText'] = '\n'.join(lines[start:]).strip()
    return cards
