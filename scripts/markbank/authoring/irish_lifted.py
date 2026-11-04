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


def written(card: dict) -> list[str]:
    text = corpus(card['year'])
    return [piece for criterion in card['criteria'] for line in criterion['guidance']
            for piece, _, is_sec in split_line(line, text) if piece.strip() and not is_sec]


def scheme_words(cards: list[dict]) -> list[dict]:
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
