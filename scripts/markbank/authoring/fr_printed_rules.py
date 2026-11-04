"""The SEC's own printed rules for French reading and listening cards.

Each function returns sentences exactly as the paper or scheme prints them
(see fr_printed for the only normalisation applied), and asserts that the
pattern finds one printed reading, so a changed page fails the build instead
of silently dropping or inventing a rule.
"""
from functools import lru_cache
from pathlib import Path
import re

from fr_printed import MARKER, clean, page_texts, printed, _doc

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'examiner-reports/french'


def paper(year, level, aural=False):
    return DATA / f'papers/{year}-{level}-{"A00" if aural else "000"}-paper.pdf'


def scheme(year, level):
    return DATA / f'schemes/{year}-{level}.pdf'


def _items(block):
    """A printed list block as its items: one per numbered or bulleted entry,
    bullet glyphs dropped, printed numbers kept."""
    parts = re.split(rf'\s(?=(?:\d\.|{MARKER}|o|x)\s+[A-Z])', ' ' + block)
    items = []
    for part in parts:
        part = re.sub(rf'^\s*(?:{MARKER}|o|x)\s+', '', part).strip()
        if part:
            items.append(part)
    return items


# -- Reading -----------------------------------------------------------------

def reading_language(year, level, kind):
    """The Section A instruction for this kind of question, as the paper prints it."""
    if kind == 'mcq':
        pattern = r'Dans le cas des questions à choix multiple, indiquez la bonne réponse en [^.]*\.'
    elif kind == 'french':
        pattern = r'Aux (?:autres )?questions en français, il faut répondre en français\.'
    else:
        pattern = r'Aux questions posées en irlandais/anglais,? il faut répondre en irlandais ou en anglais\.'
    text, page = printed(paper(year, level), pattern, what=f'{year} {level} {kind}')
    return text.replace('(✓ )', '(✓)'), page


def reading_mcq_instruction(year, level, pages):
    """The Ordinary paper's multiple-choice instruction on the comprehension's pages, if printed."""
    pattern = r'Answer multiple[‐-]choice questions by putting a tick \(✓ ?\) in the relevant box\.'
    found = {m.group(0).replace('(✓ )', '(✓)'): p for p in pages for t in page_texts(str(paper(year, level)), p) for m in re.finditer(pattern, t)}
    if not found:
        return None
    assert len(found) == 1, found
    return found.popitem()


@lru_cache(maxsize=None)
def reading_general_points(year, page):
    """The Higher scheme's general points for both reading comprehensions."""
    text, _ = printed(scheme(year, 'hl'), r'In both Reading Comprehensions, the following general points apply:.*?mentioned in (?:point )?2 above\.',
                      pages=[page], what=f'{year} hl general points')
    head, rest = text.split(':', 1)
    out = [head + ':']
    for part in re.split(r'\s(?=Where separate spaces|Any extra sub|Penalties:|Note:)', rest.strip()):
        if part.startswith('Penalties:'):
            out.append('Penalties:')
            out.extend(_items(part[len('Penalties:'):]))
        else:
            out.append(part.strip())
    return tuple(out)


@lru_cache(maxsize=None)
def ordinary_equivalence(year):
    """The Ordinary scheme's equivalent-meaning paragraph (comprehension 1, 2 and the opinion questions)."""
    text, _ = printed(scheme(year, 'ol'), r'Candidates are not required to produce the exact wording of the solutions proposed in this marking scheme for .*?equivalent meaning\.',
                      what=f'{year} ol equivalence')
    return tuple(re.split(r'(?<=Test\.)\s+', text))


@lru_cache(maxsize=None)
def ordinary_question_rules(year, rc):
    """The rules printed under the Ordinary scheme's Q.3 / Q.4 heading."""
    head = rf'(?:Q\.\s*{rc}\s*\(40 marks\)|Question {rc}\s*[–-]\s*40 marks)'
    text, page = printed(scheme(year, 'ol'), rf'{head}\s*(?:\d+\s+)?(.*?)(?=\s1\s?[.…])', what=f'{year} ol Q{rc} rules')
    body = re.sub(rf'^{head}\s*(?:\d+\s+)?', '', text)
    sentences = re.split(r'(?<!N\.B\.)(?<=\.)\s+(?=N\.B\.|[A-Z])', body)
    return tuple(s.strip() for s in sentences if s.strip()), page


def special_segment_rule(year):
    """The Higher scheme's Q.6 higher-segment rule, printed under the comprehension heading."""
    text, _ = printed(scheme(year, 'hl'), r'In Q\.6, where less than full marks is achieved in either segment, the higher mark is to be awarded to each segment\.',
                      what=f'{year} hl Q6 rule')
    return text


# -- Shared conventions --------------------------------------------------------

@lru_cache(maxsize=None)
def conventions(year, level):
    """The scheme's explanatory note on its answer conventions, one printed line per entry."""
    path = scheme(year, level)
    sentence = r'In this Marking Scheme, -? ?a bullet point indicates.*?round brackets indicate extraneous material which is not penalised\.'
    listed = r'Please note that, in the presentation of answers in this marking scheme, the following conventions apply:.*?enclosed in round brackets\.'
    for pattern in (sentence, listed):
        try:
            text, _ = printed(path, pattern, pages=range(1, 6), what=f'{year} {level} conventions')
        except AssertionError as error:
            if 'not printed' in str(error):
                continue
            raise
        if text.startswith('In this'):
            return tuple(re.split(r'\s(?=- )', text))
        head, rest = text.split('apply:', 1)
        return (head + 'apply:', *_items_lower(rest))
    raise AssertionError(f'{year} {level}: no printed conventions note')


PREAMBLE = (r'In the case of marking schemes that include model solutions or answers, it should be noted that these are not '
            r'intended to be exhaustive\. Variations and alternatives may also be acceptable\.')


@lru_cache(maxsize=None)
def scheme_notes(year, level):
    """The scheme's printed notes on reading it: its answer conventions, then
    (2013 onwards) its preamble that model answers are not exhaustive."""
    notes = list(conventions(year, level))
    try:
        text, _ = printed(scheme(year, level), PREAMBLE, pages=range(1, 5), what=f'{year} {level} preamble')
        notes.append(text)
    except AssertionError as error:
        if 'not printed' not in str(error):
            raise
    return tuple(notes)


def _items_lower(block):
    """The older list of conventions: one item per printed entry, bullet glyphs
    (which the 2015 text layer scatters to line ends) dropped."""
    block = re.sub(rf'(?<=\s)(?:{MARKER})(?=\s)', ' ', ' ' + block + ' ')
    parts = re.split(r'\s(?=where acceptable|a slash|certain incomplete|words or phrases)', block)
    return [p.strip() for p in parts if p.strip()]


# -- Listening -----------------------------------------------------------------

def aural_language(year, level):
    return printed(paper(year, level, aural=True), r'Questions to be answered in English, not necessarily in complete sentences\.',
                   what=f'{year} {level} aural language')


def aural_mcq_instruction(year, level, page):
    pattern = r'Answer (?:the )?multiple[‐-]choice questions? by putting a tick \(✓ ?\) in the relevant box\.'
    found = {m.group(0).replace('(✓ )', '(✓)') for t in page_texts(str(paper(year, level, aural=True)), page) for m in re.finditer(pattern, t)}
    if not found:
        return None
    assert len(found) == 1, found
    return found.pop()


@lru_cache(maxsize=None)
def listening_general(year, level, page):
    """The listening scheme's own general rules, in printed order."""
    path = scheme(year, level)
    for text in page_texts(str(path), page):
        out = []
        nb = re.search(r'N\.?B\.? ?-? ?Candidates are not required to give the exact wording.*?(?:award 0 marks?\.|for their answer\.)(?:\s*If both a correct and incorrect answer are given, award 0 marks?\.)?', text)
        if nb:
            out.extend(re.split(r'(?<=answer\.)\s+(?=If both)', nb.group(0)))
        general = re.search(r'General observations:\s*(.*?)(?=\s*In the following questions|\s*Section (?:[A-E]|I)\b|$)', text)
        if general:
            for item in _items(general.group(1)):
                out.extend(re.split(r'(?<=gained\.)\s+(?=These deductions)', item))
        if out:
            return tuple(out)
    raise AssertionError((year, level, page, 'no printed listening rules'))


SEGMENT = 'In the following questions, where less than full marks is achieved in either segment, the higher mark is to be awarded to each segment'


def listening_special(year, level, page):
    """The higher-segment rule with the printed list of questions it names,
    up to the first section heading of the answers."""
    pattern = rf'{SEGMENT}.*?(?=\s+Section\s+\w+\s*(?:\(|[–-]\s*\d)|$)'
    text, _ = printed(scheme(year, level), pattern, pages=[page], what=f'{year} {level} special')
    return text
