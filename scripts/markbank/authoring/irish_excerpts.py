#!/usr/bin/env python3
"""Re-cut an Irish reading or literature card's scheme excerpt across the pages it runs onto.

    python3 scripts/markbank/authoring/irish_excerpts.py [--write]

irish_cards.py reads each Léamhthuiscint question's answers from the ONE
scheme page that best matches the question, and cuts from "N. (a)" on that
page. Two things the scheme does defeat that: it sets "2." on one line and
"(a)" on the next, and it runs a question over a page break, so the best page
holds "(b) (i)" but not "(a)". The excerpt then starts mid-question or stops
short, its tariffs do not add up to the criterion, and cards/irish/answers.ts
cannot cut it into rows (31 reading cards on 2026-10-27).

This reads the local scheme markdown (examiner-reports/irish/schemes), joins
the cited page with its neighbours, finds "N." then "(a)" with any line break
between them, and cuts to the next question's "(a)" or the section's end
("LÉAMHTHUISCINT B", "A – (50 marc)", "CEIST …"). The text is the scheme's,
chunked exactly as irish_cards.chunk_guide chunks it; nothing is retyped. The
cited scheme page is kept (the excerpt still starts on or beside it).

Re-running changes nothing: the cut is a function of the scheme text.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import irish_cards as IC  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
AUTHORED = os.path.join(ROOT, 'components', 'MarkBank', 'cards', 'irish', 'authored.json')
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'irish', 'schemes')
_pages = {}


def md_pages(year, level):
    key = (year, level)
    if key not in _pages:
        with open(os.path.join(SCHEMES, f'{year}-{"hl" if level == "higher" else "ol"}.md'), encoding='utf-8') as fh:
            parts = re.split(r'^## Page (\d+)\s*$', fh.read(), flags=re.M)
        _pages[key] = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
    return _pages[key]


def start_of(number):
    return re.compile(rf'(?m)^\s*{number}\.\s*(?:\n\s*)?\(a\)')


def end_of(number):
    # The next question, the next passage (its questions restart at "1. (a)"), or the paper's next part.
    # "B – (50 marc)" at a page's foot is the running section label, not an end: page_text drops it.
    return re.compile(rf'(?m)^\s*{number}\.\s*(?:\n\s*)?(?:\(a\)|[A-ZÁÉÍÓÚ])|^\s*1\.\s*(?:\n\s*)?\(a\)|^\s*LÉAMHTHUISCINT\s+[AB]\b'
                      r'|^\s*CEIST\s+\d|^\s*Cuid\s+II\b|^\s*An Cheapadóireacht\b'
                      # the general notes the scheme prints after the last question
                      r'|^\s*(?:Na )?Siombailí Anótála|^\s*Stíl chuí scríbhneoireachta|^\s*An Cumas Gaeilge\s*\(|^\s*Glacfar le freagraí i bhfocail')


FOOTER = re.compile(r'(?m)^\s*[AB]\s*[–-]\s*\(?\d+\s*marc\)?\s*$')
# The Ordinary scheme closes a passage's answers with its language deduction; nothing after it is this passage's.
DEDUCTION = re.compile(r'\[Gaeilge lochtach:[^\]]*\]')


def page_text(pages, number):
    return FOOTER.sub('', IC.clean_lines(pages.get(number, ''), drop_answer_slots=False))


def recut(card):
    """The card's reading excerpt as chunk_guide chunks, cut across the cited page and its neighbours; None when its "N. (a)" is not there."""
    match = re.search(r'Ceist (\d)', card['questionRef'])
    if not match:
        return None
    number = int(match.group(1))
    pages = md_pages(card['year'], card['level'])
    page = card['schemePage']
    for span in ((page,), (page - 1, page), (page, page + 1), (page - 1, page, page + 1)):
        text = '\n'.join(page_text(pages, q) for q in span)
        start = start_of(number).search(text)
        if not start:
            continue
        end = end_of(number + 1).search(text, start.end())
        if end or span[-1] >= page + 1:
            excerpt = text[start.start():end.start() if end else len(text)]
            deduction = DEDUCTION.search(excerpt)
            if deduction:
                excerpt = excerpt[:deduction.end()]
            return chunk(excerpt)
    return None


def chunk(value):
    """irish_cards.chunk_guide's chunking without its 2,200-character cap: the
    cap kept a prose excerpt readable, but a question that runs onto a second
    page is longer than that, and cut there its (b) half is lost — which is
    the fault this tool exists to mend. The rows are structured now, so the
    whole excerpt is what the student needs."""
    value = IC.clean_lines(value, drop_answer_slots=False)
    value = re.sub(r'(?m)^\s*(?:nó|Nó)\s*$', '', value)
    value = IC.compact(value)
    if not value:
        return []
    sentences = re.split(r'(?<=[.;!?])\s+(?=[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛ(a-z0-9•])', value)
    chunks, current = [], ''
    for sentence in sentences:
        sentence = IC.compact(sentence)
        if not sentence:
            continue
        if current and len(current) + len(sentence) + 1 > 430:
            chunks.append(current)
            current = sentence
        else:
            current = f'{current} {sentence}'.strip() if current else sentence
    if current:
        chunks.append(current)
    return chunks


LITERATURE = re.compile(r'(?:Prose|Poetry|Literature) (\d[AB]?)\(([a-f])\)')
OPTION_FOOT = re.compile(r'(?m)^\s*(?:Eolas\s*\(\d+\)\s*=|C\d[AB]?\s*\([a-f]\)\s*\(\d+\)\s*=|Gaeilge\s*\(\d+\)\s*=)\s*$')


def literature_recut(card):
    """A literature option's whole scheme block — "(b)" to the next option or question — cut across the cited page and the pages after it.

    irish_cards.literature_scheme cut 1,550 characters from the line that best
    matched the prompt, which for a three-part option is the middle of it: the
    (i) part and its tariff were lost. The option letter the scheme prints at
    the start of a line ("(b)", "(b) Colscaradh (25 marc)", or "4F." for the
    Litríocht Bhreise question) is the boundary that was always there. The
    start is taken on the cited page first — a "(b)" on the page before may be
    another option's sub-question — and the end is the next option letter on a
    line that asks nothing (a sub-question's "(c) Cá mbíodh …?" is not an
    option), the next question's header, or the paper's next part.
    """
    match = LITERATURE.search(card['questionRef'])
    if not match:
        return None
    number, letter = match.group(1), match.group(2)
    pages = md_pages(card['year'], card['level'])
    page = card['schemePage']
    start_of_option = re.compile(rf'(?m)^\s*(?:\({letter}\)(?=\s|$)|{number}{letter.upper()}\.\s)')
    # An option boundary is a letter alone, before "(i)", with a title and a two-digit tariff, or with a short title;
    # a sub-question's "(b) Conas atá …? (2 mharc)" or "(b) Luaigh dhá …" is not one.
    end_of_option = re.compile(rf'(?m)^\s*\((?!{letter}\))[a-f]\)(?:\s*\n\s*\(i\)|\s*\n(?![^\n]*\?)[^\n]*\n|\s+(?=\(i\))|\s+[^\n]*\(\d{{2}}\s*m?h?arc\)[^\n]*$|\s+[A-ZÁÉÍÓÚ][^\n?]{{0,40}}$|\s+(?:Maidir le|Freagair)\b)'
                               rf'|^\s*\d[A-F]?\.\s|^\s*(?:FILÍOCHT|PRÓS|LITRÍOCHT|An Cheapadóireacht|AN CHEAPADÓIREACHT|Cuid\s+I|CUID\s+I)\b')
    own_header = re.compile(rf'(?m)^\s*(?:CEIST|Ceist)\s+{number[0]}\b[^\n]*$|^\s*(?:FILÍOCHT|PRÓS|LITRÍOCHT)[^\n]*\d+\s*marc\s*$')
    end_of_option = re.compile(end_of_option.pattern + rf'|^\s*(?:CEIST|Ceist)\s+(?!{number[0]}\b)\d')

    def text_of(span):
        return '\n'.join(own_header.sub('', OPTION_FOOT.sub('', FOOTER.sub('', IC.clean_lines(pages.get(q, ''), drop_answer_slots=False)))) for q in span)
    for first in (page, page - 1):
        head = text_of((first,))
        start = start_of_option.search(head)
        if not start:
            continue
        for last in range(first, page + 4):
            text = text_of(tuple(range(first, last + 1)))
            end = end_of_option.search(text, start.end())
            if end or last >= page + 3:
                return chunk(text[start.start():end.start() if end else len(text)])
    return None


def main():
    with open(AUTHORED, encoding='utf-8') as fh:
        data = json.load(fh)
    changed = []
    for card in data['cards']:
        if 'Léamhthuiscint' in card['questionRef']:
            guide = recut(card)
            target = card['criteria'][0]
        elif LITERATURE.search(card['questionRef']):
            guide = literature_recut(card)
            target = next((criterion for criterion in card['criteria'] if criterion['guidanceKind'] == 'indicative'), None)
        else:
            continue
        if guide and target and guide != target['guidance']:
            target['guidance'] = guide
            changed.append(card['id'])
    print(f'{len(changed)} reading excerpts re-cut: {", ".join(changed[:5])}{" …" if len(changed) > 5 else ""}', file=sys.stderr)
    if '--write' in sys.argv:
        with open(AUTHORED, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
