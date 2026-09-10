#!/usr/bin/env python3
"""Non-curricular EU language papers — the printed ask, and which is a leaf.

    python3 scripts/markbank/authoring/eu_paper.py portuguese 2024 hl
    python3 scripts/markbank/authoring/eu_paper.py portuguese 2022 ol --aural
    python3 scripts/markbank/authoring/eu_paper.py portuguese --audit

ONE reader, three subjects
--------------------------
Portuguese (SEC 018), Romanian (SEC 553) and Dutch (SEC 017) are the same
examination printed in three languages, and Polish's reader (pl_paper.py)
already showed what that examination looks like: a booklet printed in ONE
language edition rather than the bilingual 'B' booklet the curricular languages
use, a reading comprehension whose questions are LETTERED so no marker is ever
ambiguous with a numbered passage paragraph, and — in Portuguese only — a
Listening Comprehension Test in a booklet of its own.

Rather than a fourth, fifth and sixth copy of that walker, the marker
vocabulary is a table (`LANGS`) and the walk is shared. What differs between
the three is words, not structure: "Questão"/"PARTEA"/the Dutch paper's bare
"1.", "Parte A"/"PARTEA I", "Adaptado:"/"Publicat în".

TWO ERAS, and the corpus says which
-----------------------------------
* CLASSIC. One booklet, sat at ONE level, numbered questions on one or two
  printed texts, and — the fact that makes it cardable — **the tariff is
  printed on the QUESTION PAPER**, in its right-hand margin: "(5)", "(5×1)",
  "(5 puncte)", "(1 punt)". The scheme for these sittings prints answers and no
  marks at all, so the paper is the only place the price is written down.
  Portuguese 2021, and every Romanian and Dutch sitting in the corpus.
* MODERN. Two booklets and two levels, rebuilt in 2022: Part A Reading and
  Part B Written Production in the written booklet (component 000), and a
  Listening Comprehension Test in its own (component A00). Here the PAPER
  prints no per-ask marks and the SCHEME prices every ask. Portuguese 2022
  onward, and nothing else in this family.

The era is read from the booklets on disk, never assumed: a sitting with a
`-000-` component is modern, a lone `<year>-<level>-paper.pdf` is classic.
"""
import argparse
import glob
import os
import re
import sys
import unicodedata

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.dirname(HERE))
from markbank_text import unligature                            # noqa: E402


# --------------------------------------------------------- the vocabulary ---
# Everything that differs between the three subjects, and nothing that does
# not. A regex here is matched against a whole printed LINE, already normalised
# (see _norm) so U+00A0 and the SEC's private-use spaces are ordinary spaces.
LANGS = {
    'portuguese': {
        'name': 'Portuguese',
        # "Questão 1:", "Questão 1 – Leia este texto…", "Questão 3".
        'q_head': r'^Quest[ãa]o\s*(\d{1,2})\b',
        # The section tab the SEC sets in the margin of the page each section
        # opens on: "Parte A   Compreensão Escrita", "Parte B   Escrita".
        # "[AB]" and not "\w", because the same word heads the reading text's
        # own subsections — "Parte 1 – Como começou" — and a looser class read
        # those as section boundaries.
        'section_tab': r'^Parte\s+([AB])\b',
        'aural_tab': r'^Parte\s+([A-E])\b',
        # The classic examination's two halves, printed as words.
        'classic_part': r'^(Primeira|Segunda)\s+Parte\b',
        'classic_part_map': {'primeira': 'I', 'segunda': 'II'},
        # The second part's essay options, which the SEC titles rather than
        # numbers: "Tópico 1", "Tópico 2". The scheme numbers them "Tema 1"
        # and "Tema 2", so the paper's own title carries the number.
        'essay_title': r'^T[óo]pico\s+(\d)\b',
        # The `\b` used to close the whole run, so it had to hold after the
        # DASH of the running head — and "Portuguese – Higher Level" has a
        # space there, so the foot of every page reached the ask above it.
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Portuguese\s*[–—-]|^\d{1,3}$'),
        # The attribution the SEC prints under a reading text.
        'source_line': (r'^(?:Adaptado|Adapta[çc][ãa]o|Texto\s+adaptado|'
                        r'Fonte\s*:|In\s*:|Retirado)'),
        # Rubric printed between asks, which belongs to no ask.
        'rubric': (r'^(?:Responda\b|Answer\b|Based\s+on\b|Baseado\b|'
                   r'Leia\s+(?:o|este|atentamente)\b|Escreva\b|'
                   r'Todas\s+as\s+respostas\b|Observe\s+as\s+imagens\b)'),
    },
    # Romanian (SEC 553) is sat at ONE level in every year of the corpus and
    # prints ONE booklet with no Listening Comprehension Test at all, so only
    # the classic path is ever walked. Its parts are numbered in Romanian
    # ordinals — "PARTEA I", "PARTEA a II-a", "PARTEA a III-a" — and the third
    # part appears only from 2023; 2021 and 2022 set two.
    'romanian': {
        'name': 'Romanian',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        'classic_part': r'^PARTEA\s+(I{1,3}|a\s*I{1,2}I?\s*[-‐–]\s*a)\b',
        'classic_part_map': {},
        # The two quotations the third part offers. The SEC letters them
        # "a." and "b." in 2024 and numbers them "1." and "2." in 2023 and
        # 2025, and both forms are read — inside a WRITING part only, where a
        # bare "1." cannot be a question because the questions are all in the
        # first part.
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        # The `\b` used to close the whole run, so it had to hold after the
        # DASH of the running head — and "Romanian – Higher Level" has a
        # space there, so the foot of every page reached the ask above it.
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Romanian\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:Adaptare|Text\s+adaptat|Sursa\s*:|Publicat\s+în)',
        'rubric': (r'^(?:R[ăa]spunde[țt]i\b|Citi[țt]i\b|Scrie[țt]i\b|'
                   r'Discuta[țt]i\b|[ÎI]NTREB[ĂA]RI\b)'),
    },
    # Dutch (SEC 017) is Romanian's twin in shape: ONE level, ONE booklet, no
    # Listening Comprehension Test, and parts numbered "Deel 1", "Deel 2" and
    # — from 2023 — "Deel 3". Its reading text numbers its paragraphs with a
    # bare "10" and its questions with "1)", so the full stop or bracket after
    # the digit is what tells an ask from a paragraph of the passage.
    'dutch': {
        'name': 'Dutch',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        'classic_part': r'^Deel\s+([123])\b',
        'classic_part_map': {'1': 'I', '2': 'II', '3': 'III'},
        # The two topics the last part offers. The SEC letters them "a)" and
        # "b)" up to 2024 and numbers them "1." and "2." in 2025, and both are
        # read — inside a WRITING part only.
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        'letter': 'colon',
        # The `\b` used to close the whole run, so it had to hold after the
        # DASH of the running head — and "Dutch – Higher Level" has a
        # space there, so the foot of every page reached the ask above it.
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Dutch\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:Bron\s*:|Naar\s+aanleiding|Uit\s*:|Bewerkt)',
        'rubric': (r'^(?:Vragen\b|Beantwoord\b|Lees\b|Schrijf\b|'
                   r'Alle\s+antwoorden\b|Geef\s+je\s+eigen)'),
    },
    # ---------------------------------------------------------------------
    # The nine remaining non-curricular EU languages, added 10 September 2026.
    # Every one of them is the CLASSIC examination and nothing else — there is
    # no 2022 rebuild here, no second level and no Listening Comprehension
    # Test — so only `_walk_classic` is ever entered for them, and only the
    # classic knobs below are read. What the corpus shows, before any of it is
    # believed: one booklet a year, file letter 'A', component '000'.
    #
    # The examination itself is ONE paper printed in nine languages:
    #
    #     PART I    (30/100)  six questions on one printed text, the first of
    #                         them five expressions a) to e) priced "(5 × 1)"
    #     PART II   (30/100)  a commentary of 100-150 words
    #     PART III  (40/100)  an essay of about 300 words, two titles offered
    #
    # and in the 2021 and 2022 sittings the commentary is dropped, leaving
    # PART I (30/70) and PART II (40/70) — which is why the part token is read
    # from the page and never from the year.
    #
    # Only PART I is answered with stated content. Parts II and III are
    # answered by the same four-quality percentage grid in all nine languages
    # ("Megértés – 30%", "Coherence – 30%", "Nyelvhelyesség – 10%"), which is
    # the shape of a piece of writing and not an answer; they are excluded
    # with that grid as the evidence, exactly as Romanian's and Dutch's are.
    'hungarian': {
        'name': 'Hungarian',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        # "I. RÉSZ", "II. RÉSZ", "III. RÉSZ".
        'classic_part': r'^(I{1,3})\s*\.?\s*R[ÉE]SZ\b',
        # The 2020 booklet sets "I." and "RÉSZ" in two cells of one printed
        # row, and read as separate lines neither is a part head: that sitting
        # censused zero asks until the two were joined.
        'classic_part_tail': r'^R[ÉE]SZ\b',
        # The 2020 SCHEME drops the word altogether and heads its first part
        # "I (30 pont / 100 pont)". A bare Roman numeral is a head only when
        # the part's own price is printed beside it, which is what separates
        # it from the "I." of a numbered list.
        'scheme_part': (r'^(I{1,3})\s*\.?\s*(?:R[ÉE]SZ\b|'
                        r'\(\s*\d{1,3}\s*pont)'),
        'classic_part_map': {},
        # The essay titles Part III offers, which the SEC numbers "1." and
        # "2." — and, in the scheme, "1. lehetőség".
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        # Hungarian letters the parts of Question 1 with a COMMA — "a," — and
        # not a bracket. See LETTER_COMMA.
        'letter': 'comma',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Hungarian\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:Forr[áa]s\s*:|Adapt[áa]ci[óo]|[-–—]\s*\w+.*(?:HVG|adapt))',
        'rubric': (r'^(?:V[áa]laszoljon\b|Olvassa\s+el\b|[ÍI]rjon\b|'
                   r'Kommentálja\b|Fejtse\s+ki\b|Minden\s+v[áa]laszt\b)'),
    },
    'bulgarian': {
        'name': 'Bulgarian',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        # "Първа част", "Втора част", "Трета част" — the ordinal is a word.
        # The ordinal is a WORD, and the SEC prints it on either side of
        # the noun: "Първа част" up to 2020 and "Част първа" in 2021 and 2022.
        # Both orders are read, and the space between them is optional because
        # four sittings letterspace the head — 2011 sets it "Пъ рва час т" —
        # and the walker retries a short head with its spaces squeezed out.
        'classic_part': (r'^(?:(Първа|Втора|Трета)\s*част|'
                         r'част\s*(Първа|Втора|Трета))\b'),
        'classic_part_map': {'първа': 'I', 'втора': 'II', 'трета': 'III'},
        # Bulgarian letters the five expressions of Question 1 in CYRILLIC —
        # "а)", "б)", "в)", "г)", "д)" — which look like Latin letters and are
        # not. See LETTERS_FOR.
        'letters': 'абвгде',
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Bulgarian\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:Източник\s*:|По\s+материали|Адаптиран)',
        'rubric': (r'^(?:Отговорете\b|Прочетете\b|Напишете\b|'
                   r'Коментирайте\b|Всички\s+отговори\b)'),
    },
    'slovakian': {
        'name': 'Slovakian',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        # "ČASŤ I", "ČASŤ II", "ČASŤ III" — and the 2015 sitting sets the same
        # head in a subset font whose ToUnicode map is broken ("ýASġ I"), so
        # the head is matched on its NUMERAL and the four letters around it
        # rather than on the word alone.
        # ...and the 2021 and 2022 sittings name the two parts in WORDS
        # instead — "Prvá časť", "Druhá časť".
        'classic_part': (r'^(?:[ČýC][AÁ]S[ŤġT]\s*(I{1,3}|[123])|'
                         r'(Prv[áa]|Druh[áa]|Tretia)\s*[čc]as[ťt])\b'),
        'classic_part_map': {'prvá': 'I', 'prva': 'I', 'druhá': 'II',
                             'druha': 'II', 'tretia': 'III'},
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Slovakian\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:Zdroj\s*:|Upraven|Podľa\b|Prevzat)',
        'rubric': (r'^(?:Odpovedzte\b|Pre[čc][íi]tajte\b|Nap[íi][šs]te\b|'
                   r'Vyjadrite\b|V[šs]etky\s+odpovede\b)'),
    },
    'swedish': {
        'name': 'Swedish',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        # "Del I", "Del II", "Del III".
        'classic_part': r'^Del\s*(I{1,3})\b',
        'classic_part_map': {},
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Swedish\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:K[äa]lla\s*:|Ur\s*:|Bearbetad|Publicerad)',
        'rubric': (r'^(?:Svara\b|L[äa]s\b|Skriv\b|Kommentera\b|'
                   r'Alla\s+svar\b|F[öo]rklara\s+dessa\s+ord)'),
    },
    'estonian': {
        'name': 'Estonian',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        # "I ÜLESANNE", "II ÜLESANNE", "III ÜLESANNE" — with or without the
        # full stop after the numeral, which the SEC prints both ways.
        'classic_part': r'^(I{1,3})\s*\.?\s*[ÜU]LESANNE\b',
        'classic_part_tail': r'^[ÜU]LESANNE\b',
        'classic_part_map': {},
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Estonian\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:Allikas\s*:|Lühendatult|Kohandatud)',
        'rubric': (r'^(?:Vasta\b|Loe\b|Kirjuta\b|Kommenteeri\b|'
                   r'K[õo]ik\s+vastused\b)'),
    },
    'finnish': {
        'name': 'Finnish',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        # "I TEHTÄVÄ", "II Tehtävä:", "III TEHTÄVÄ" — the case changes between
        # sittings and the colon appears in some of them.
        # Finnish letters the five expressions of Question 1 with a FULL
        # STOP — "a. jämäkkä" — where the rest of the family brackets them.
        'letter': 'dot',
        'classic_part': r'^(I{1,3})\s*TEHT[ÄA]V[ÄA]\b',
        'classic_part_tail': r'^TEHT[ÄA]V[ÄA]\b',
        'classic_part_map': {},
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Finnish\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:L[äa]hde\s*:|Mukailtu|Lyhennetty)',
        'rubric': (r'^(?:Vastaa\b|Lue\b|Kirjoita\b|Ohje\s*:|'
                   r'Kommentoi\b)'),
    },
    'croatian': {
        'name': 'Croatian',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        # "I. dio", "II. dio", "III. dio" — and the 2020 sitting numbers the
        # same three parts "1. dio", "2. dio", "3. dio".
        # Six sittings (2014-2019) print the head over TWO printed lines,
        # the numeral in one cell and the word in the next, so
        # `classic_part_tail` joins them; without it those six censused zero.
        'classic_part': r'^(I{1,3}|[123])\s*\.?\s*dio\b',
        'classic_part_tail': r'^dio\b',
        'classic_part_map': {},
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Croatian\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:Izvor\s*:|Prilagođeno|Prema\b|Preuzeto)',
        'rubric': (r'^(?:Odgovorite\b|Pro[čc]itajte\b|Napi[šs]ite\b|'
                   r'Komentirajte\b|Svi\s+odgovori\b)'),
    },
    'danish': {
        'name': 'Danish',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        # "Opgave I", "Opgave II", "Opgave III" — and four sittings head the
        # same three parts in ENGLISH, "Part 1", "Part II", "Part III".
        'classic_part': r'^(?:Opgave|Part)\s+(I{1,3}|[123])\b',
        'classic_part_map': {},
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Danish\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:Kilde\s*:|Bearbejdet|Uddrag\s+af|Fra\s*:)',
        'rubric': (r'^(?:Besvar\b|L[æae]s\b|Skriv\b|Forklar\s+din\s+mening|'
                   r'Alle\s+svar\b)'),
    },
    'slovenian': {
        'name': 'Slovenian',
        'q_head': None,
        'section_tab': None,
        'aural_tab': None,
        # "1. DEL", "2. DEL", "3. DEL" — Slovenian numbers its parts with
        # digits where the other eight use Roman numerals.
        # The 2018 booklet sets the first head as "1.  DE", the L in a span
        # the text layer drops, so the L is optional; a Slovenian question
        # never opens "DE".
        'classic_part': r'^([123])\s*\.\s*DEL?\b',
        'classic_part_map': {'1': 'I', '2': 'II', '3': 'III'},
        'essay_title': r'^([12ab])\s*[.)]\s+\S',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Page\s*\d+)\b|'
                      r'^Slovenian\s*[–—-]|^\d{1,3}$'),
        'source_line': r'^(?:Vir\s*:|Prirejeno|Povzeto|Po\s*:)',
        'rubric': (r'^(?:Odgovorite\b|Preberite\b|Napi[šs]ite\b|'
                   r'Komentirajte\b|Vsi\s+odgovori\b)'),
    },
}


def cfg(subject, key, default=None):
    return LANGS[subject].get(key, default)


def papers_dir(subject):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_path(year, level, component, subject):
    """The booklet on disk, whatever the fetcher called it.

    A classic sitting is a single booklet and lands as `2021-hl-paper.pdf` with
    no component token; a modern one prints two and lands as `…-000-paper.pdf`
    and `…-A00-paper.pdf`. Requiring the component silently found nothing for
    the classic sittings, which is every Romanian and Dutch paper in the
    corpus.
    """
    stem = f'{year}-{level}'
    names = ([f'{stem}-{component}-paper.pdf'] if component
             else [f'{stem}-paper.pdf', f'{stem}-000-paper.pdf'])
    for name in names:
        path = os.path.join(papers_dir(subject), name)
        if os.path.exists(path):
            return path
    return None


# --------------------------------------------------------------- the page ---
# The SEC sets these booklets with U+00A0 between every word in some years and
# with ordinary spaces in others. Folded here so one set of patterns reads
# every sitting.
NBSP = '\u00a0\u2000\u2001\u2002\u2003\u2007\u2009\u200a\u202f\u2060\ufeff'
# The Symbol and Wingdings space, which those fonts encode in the private-use
# area. It is a space and nothing else, and left as itself it reaches a card as
# an unresolvable glyph the build refuses.
SYMBOL_SPACE = '\uf020\uf0a0'


def _norm(text):
    """One printed line, with the SEC's broken font glyphs put back.

    `unligature` is the bank's shared map rather than a local one: these papers
    set "ginásƟca" and "İsico" with a subset font whose ti and fi ligatures
    have no ToUnicode entry, and a card carrying either quotes a word the SEC
    never printed.
    """
    out = ''.join(' ' if c in NBSP or c in SYMBOL_SPACE else c
                  for c in unligature(text))
    return re.sub(r'\s+', ' ', out).strip()


class Line:
    __slots__ = ('page', 'x', 'y', 'x1', 'text')

    def __init__(self, page, x, y, x1, text):
        self.page, self.x, self.y, self.x1, self.text = page, x, y, x1, text

    def __repr__(self):
        return (f'Line(p{self.page} x={self.x:.1f} y={self.y:.1f} '
                f'{self.text[:60]!r})')


# A marker printed alone in its cell, in every form these booklets use: the
# bracketed letter or roman "(b)", the classic paper's bare "b)", the numbered
# "1." and — the Listening booklet's own — the bracketed number "(1)". Without
# the last, an item whose question wrapped onto a second line kept the wrap and
# lost the marker's own line, and censused as an empty leaf.
# The dotted form "a." is here as well as the bracketed one: the Finnish
# booklet sets its five expressions "a." at x=57 and the word itself at x=85,
# and a marker vocabulary that knew only "a)" left all five as empty leaves.
# A whole printed line that is one letter and a stop is a marker in every
# sitting of this corpus.
MARKER_ONLY = re.compile(r'^\(\s*([a-z]{1,4})\s*\)\.?$|^([a-z])\s*[).]$|'
                         r'^(\d{1,2})\s*[.)]$|^\(\s*(\d{1,2})\s*\)$', re.I)
# How far above or below its own baseline the text beside a marker may sit.
# A marker is set CENTRED in its table cell while the sentence beside it wraps
# around it, so the whole cell is gathered rather than one baseline.
CELL_TOL = 20.0
# How far right of the letter column a marker may still be a LETTER. Measured
# rather than guessed: the SEC's own table cells drift several points inside
# one page.
LETTER_TOL = 8.0
# How far below a kept line the next one may sit and still be the same ask.
# Below the ask comes the answer space, which is blank.
LINE_GAP = 32.0
# How far past the page's own left margin a question head may be set and still
# be a question head. The 2025 Dutch booklet indents "1. Wat betekenen volgende
# woorden of uitdrukkingen:" to x=74.6 where its passage sets at 56.7, and a
# margin-tight window found no question in that sitting at all. Safe at this
# width because the number still has to be the NEXT one in the run, which no
# line of a passage ever is.
HEAD_INDENT = 30.0
# How far below its ask the SEC may set that ask's right-margin price.
TARIFF_GAP = 70.0
# How far ABOVE the line before it a line may sit and still follow it. Two
# cells of one printed row do not share a vertical centre to the point: the
# 2021 Romanian paper sets "principii." at y=399.96 and the "(5 puncte)" it is
# priced by at y=399.90, six hundredths of a point higher, and a window that
# started at zero dropped the price of that question on the floor.
# The word the SEC prints beside a number when it prices something, in every
# language on this reader. Kept as ONE string rather than repeated in four
# patterns, because the four have to agree: a word missing from any one of
# them silently drops that language's prices in exactly one place. Hungarian
# "pont", Bulgarian "точки/точка", Slovakian and Croatian "bodov/bodova/bod",
# Swedish "poäng", Estonian "punkti/punkt", Finnish "pistettä", Danish
# "point", Slovenian "točk/točke/točka", beside the Portuguese, Romanian and
# Dutch words already here.
# The word the SEC sometimes prints IN FRONT of a price — "(maks. 5 point)",
# "kuni 30 punkti", "(Totalt 30 poäng)", "(Max. 100 poäng)". It is a cap, not
# a different price, and eight Danish sittings print every one of their asks
# that way; without it those asks read as unpriced and could not be carded.
CAP_WORD = r'maks|maksimum|max|maximum|kuni|totalt|total|najviac|ukupno|ungef[äa]r'
MARK_WORD = (r'puncte|punct|punten|punt|pontos|ponto|marks|mark|'
             r'pontot|pont|точки|точка|bodova|bodov|bodu|body|bod|'
             r'po[äa]ng|punkti|punkt|pistett[äa]|pistett|point|'
             r'to[čc]ke|to[čc]ka|to[čc]k')

# The most marks one ask of this examination can be worth. Its parts print
# 30, 30 and 40 on their own heads, so a bracketed number larger than the
# largest part is not a price at all — the 2022 Croatian reading text sets
# "(61)" and "(32)" inside its own paragraphs, and read as tariffs they made
# two paragraphs of a passage look like priced asks and blocked the restart
# that separates the text from the questions.
MAX_ASK_MARKS = 40
BAND_TOL = 4.0
# Where the right-hand marks margin of a classic booklet starts.
TARIFF_X = 380.0


# A price the SEC set in the right-hand margin with NO bracket around it.
# Bulgarian prints every one of its prices that way — "1 точка", "5 точки" at
# x=454 — and Finnish abbreviates the word to a letter, "1p.", "5p." at
# x=482. Neither is bracketed anywhere in the corpus, so a bracket-only reader
# left 156 Bulgarian asks and 51 Finnish ones unpriced and therefore uncarded,
# with the price printed plainly beside each of them. Read only as a WHOLE
# cell in the marks margin, so no number inside an ask's own words reaches it.
# The same price where it has been glued onto the END of the ask's own words:
# the Bulgarian booklet sets "а) привързаност" and "1 точка" on one baseline,
# so the two arrive as one line and the card asked for "привързаност 1 точка".
# Only at the end, and only a whole price — nothing inside the ask is touched.
BARE_TRAILING_PRICE = re.compile(
    r'\s+(?:\d{1,2}\s*[x×*]\s*)?\d{1,3}\s*(?:' + MARK_WORD + r'|p)\.?\s*$',
    re.I)
BARE_PRICE = re.compile(
    r'^(?:(\d{1,2})\s*[x×*]\s*)?(\d{1,3})\s*(?:' + MARK_WORD + r'|p)\.?$',
    re.I)


def _is_tariff_cell(line):
    if line.x >= TARIFF_X and BARE_PRICE.match(line.text.strip()):
        return True
    return line.x >= TARIFF_X and bool(
        re.fullmatch(r'[(\[]\s*(?:(?:' + CAP_WORD + r')\.?\s*)?'
                     r'(?:\d{1,2}\s*[x×*]\s*)?\d{1,3}\s*'
                     r'(?:' + MARK_WORD + r')?'
                     r'\s*[)\]]', line.text.strip(), re.I))


def read_lines(path, drop=None):
    """Every printed line, in reading order, with the marker column intact.

    A part marker is set in its own table cell — "(b)" at x=56.7 and its
    question at x=85.1 on the same baseline — so the two are joined back
    together here. Left apart, every lettered ask in the corpus reads as an
    empty leaf.
    """
    out = []
    with pymupdf.open(path) as doc:
        for pno, page in enumerate(doc, 1):
            raw = []
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    text = _norm(''.join(s['text'] for s in line['spans']))
                    if not text:
                        continue
                    x0, y0, x1, y1 = line['bbox']
                    # Page furniture is dropped BEFORE markers are glued, not
                    # after: the running footer "Romanian – Higher Level" sits
                    # within one cell-height of a marker at the foot of a page,
                    # and glued to it, it shipped inside the ask's own words.
                    if drop is not None and len(text) < 60 and drop.match(text):
                        continue
                    raw.append(Line(pno, x0, (y0 + y1) / 2, x1, text))
            raw.sort(key=lambda l: (round(l.y, 0), l.x))
            out += _join_markers(raw)
    return out


def _join_part_heads(lines, numeral_only, tail_pat):
    """A part head the SEC set in TWO printed cells, put back together.

    The Croatian booklet prints "I." in one cell and "dio" in the next — six
    of its thirteen sittings do — and a walker that only ever sees whole lines
    finds no part in any of them and censuses the sitting as empty. Joined
    only where the numeral is a WHOLE printed line and the very next line
    opens with the part's own noun, so no numbered question can reach it.
    """
    out, skip = [], -1
    for i, line in enumerate(lines):
        if i == skip:
            continue
        if numeral_only.match(line.text) and i + 1 < len(lines) \
                and tail_pat.match(lines[i + 1].text):
            out.append(Line(line.page, line.x, line.y, lines[i + 1].x1,
                            f'{line.text} {lines[i + 1].text}'.strip()))
            skip = i + 1
            continue
        out.append(line)
    return out


def _join_markers(lines):
    """Glue a marker printed alone in its cell onto the text beside it."""
    out, used = [], set()
    for i, line in enumerate(lines):
        if i in used:
            continue
        if MARKER_ONLY.match(line.text):
            mates = [j for j in range(max(0, i - 4), min(i + 5, len(lines)))
                     if j != i and j not in used and lines[j].x > line.x + 4
                     and abs(lines[j].y - line.y) <= CELL_TOL
                     and not MARKER_ONLY.match(lines[j].text)]
            if mates:
                # Only the marker's OWN column. A table sets the marker in a
                # narrow cell and the question beside it wraps over three
                # lines, but the page also carries a wider rubric at a
                # different margin within the same band, and a purely vertical
                # window pulled that in instead of the question.
                near = min(mates, key=lambda j: abs(lines[j].y - line.y))
                column = lines[near].x
                mates = [j for j in mates if abs(lines[j].x - column) <= 8]
                mates.sort(key=lambda j: (lines[j].y, lines[j].x))
                used.update(mates)
                body = ' '.join(lines[j].text for j in mates)
                out.append(Line(line.page, line.x,
                                min([line.y] + [lines[j].y for j in mates]),
                                max(lines[j].x1 for j in mates),
                                f'{line.text} {body}'))
                continue
        out.append(line)
    return out


# ------------------------------------------------------------- the markers ---
# A lettered part, in either of the two ways this family prints one: "(a)" in
# the modern booklets and a bare "a)" in the classic ones.
LETTER = re.compile(r'^\(?\s*([a-l])\s*\)\s*(.*)$', re.I)
# The Dutch booklet letters the parts of its first question with a COLON —
# "a: 'Het' in de zin:" — where every other paper in the family uses a
# bracket. Kept per subject rather than widened for all three, because a
# bracket is unambiguous and a colon is not: "Verbeek: 'Het beïnvloedt…'" is a
# line of the passage.
LETTER_COLON = re.compile(r'^\(?\s*([a-l])\s*[):]\s*(.*)$', re.I)
# The Hungarian booklet letters the parts of its first question with a COMMA —
# "a, Magyarázza meg…" — which no other paper in the family does. Kept per
# subject for the same reason the colon is: a comma after a single letter is
# unambiguous in Hungarian only because the passage above it never opens a
# line that way, and widening it for all twelve subjects would read "a, b és c"
# in a Dutch rubric as a marker.
LETTER_COMMA = re.compile(r'^\(?\s*([a-l])\s*[,)]\s*(.*)$', re.I)


def letters_for(subject):
    """The alphabet this subject's paper letters its parts with.

    Latin a-l everywhere except Bulgarian, which is printed in Cyrillic and
    letters Question 1's five expressions "а) б) в) г) д)". Those five are
    consecutive code points (U+0430..U+0434), so `next_letter` reads their
    sequence the same way it reads a-e, and a Cyrillic "а" is never confused
    with a Latin one because the alphabet is read from the subject, not
    guessed from the glyph.
    """
    return cfg(subject, 'letters') or LETTERS


def letter_pattern(subject):
    """The marker form this subject prints, over its own alphabet."""
    alpha = letters_for(subject)
    cls = '[' + alpha + alpha.upper() + ']'
    close = {'colon': '[):]', 'comma': '[,)]', 'dot': r'[.)]'}.get(
        cfg(subject, 'letter'), r'\)')
    return re.compile(r'^\(?\s*(' + cls + r')\s*' + close + r'\s*(.*)$')
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|ix|x)\s*\)\s*(.*)$', re.I)
# A question head, with the letter the SEC sometimes glues to it: the 2016
# Swedish booklet numbers the two halves of its first question "1a." and
# "1b." rather than lettering them beneath a "1.", and a pattern that stopped
# at the digit matched neither — so the run never reached 1, every later
# number failed the sequence test, and that whole sitting censused zero asks.
# The stop after the number is optional, but only where the SEC set the text
# at a TAB STOP instead: the 2026 Slovakian booklet prints "5  Uvažujte, aké
# zásady…" with two spaces and no full stop, and a pattern that required the
# stop lost Question 5, which then failed the run for Question 6 as well. One
# of the two — punctuation, or the gap — has to be there, so a passage line
# opening "5 000 ľudí" is still not a head.
NUMBERED = re.compile(
    r'^\(?(\d{1,2})\s*([a-l])?\s*(?:[.)]\s*|\s+(?=[^\W\d]))(.*)$')
# The first roman marker printed INSIDE an item's own line, after its stem.
INNER_FIRST_ROMAN = re.compile(r'\(\s*i\s*\)\s*')
LETTERS = 'abcdefghijkl'
# The price the CLASSIC paper prints in its right-hand margin, and the only
# place that sitting's tariff is written down: "(5)", "(5×1)", "(5 puncte)",
# "(1 punt)", "(10 puncte)". Read from the paper because the classic schemes
# print answers with no marks beside them at all.
# The bracket is round in eleven of the twelve languages and SQUARE in
# Croatian, which prints "[5 bodova]" and "[5 × 1 bod]" against every ask.
PAPER_TARIFF = re.compile(
    r'[(\[]\s*(?:(?:' + CAP_WORD + r')\.?\s*)?'
    r'(?:(\d{1,2})\s*[x×*]\s*)?(\d{1,2})\s*'
    r'(?:' + MARK_WORD + r'|m)?\s*[)\]]', re.I)
# The same, with the multiplier written second: "(5×1)" is five answers at one
# point each and the SEC also sets "(1×5)". Both are read, and which is the
# count is settled by the group beneath it, never by picking the larger.
TRAILING_MARK = re.compile(
    r'\s*[(\[]\s*(?:(?:' + CAP_WORD + r')\.?\s*)?'
    r'\d{1,2}\s*(?:[x×*]\s*\d{1,2}\s*)?'
    r'(?:' + MARK_WORD + r')?\s*[)\]]\s*$', re.I)


def next_letter(current, first='a'):
    """The SEC's own numbering, used as a second way in.

    A marker that is the NEXT letter after the one before it IS that letter,
    wherever the cell puts it. "(i)" is excluded from this path on purpose: it
    is the one marker that can also be a roman, so it still has to satisfy BOTH
    the column and the sequence.

    `first` is the alphabet's own opening letter, because one subject on this
    reader is not written in Latin: the Bulgarian scheme letters Question 1
    "а) б) в) г) д)" in CYRILLIC, and a hard-coded 'a' meant the first item of
    every Bulgarian sitting failed the sequence test and the whole part read
    as one ask. The letters after it are consecutive code points in both
    alphabets, so only the first has to be told.
    """
    return first if not current else chr(ord(current) + 1)


class Ask:
    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'page', 'stem',
                 'tariff', 'notation', 'margin_price')

    def __init__(self, section, q, letter, roman, text, page):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.text, self.page = text, page
        self.stem = ''
        # (count, per, total) where the CLASSIC paper printed a price beside
        # this ask, and None where it did not. Never inferred.
        self.tariff = None
        self.notation = ''
        # The price cell the SEC set in the right-hand margin against this
        # ask, where it set one. Kept apart from the ask's own words because
        # a bracketed number INSIDE those words is usually not a price: the
        # 2022 Croatian booklet writes its five expressions "a) dobrovoljna
        # davateljica(2)", where the (2) is the PARAGRAPH the expression comes
        # from, and read as a tariff it made that expression worth two marks
        # and the next one worth thirteen.
        self.margin_price = ''

    @property
    def key(self):
        """The address the PAPER prints: its section tab, then its number."""
        return (self.section, self.q, self.letter, self.roman)

    @property
    def full_text(self):
        """The ask as a reader meets it: its parent's stem, then its own."""
        if self.stem and len(self.text) < 60:
            return _norm(f'{self.stem} {self.text}')
        return self.text

    def __repr__(self):
        return f'Ask({self.key} {self.text[:60]!r})'


class EuPaper:
    """One sitting's booklets, walked into the leaf asks they print."""

    def __init__(self, year, level, subject):
        self.year, self.level, self.subject = year, level, subject
        self.path = paper_path(year, level, None, subject)
        if self.path is None:
            raise FileNotFoundError(
                f'no {subject} written paper for {year} {level}')
        self.aural_path = paper_path(year, level, 'A00', subject)
        # The era, read from the booklets on disk rather than from a year.
        self.era = ('modern' if self.path.endswith('-000-paper.pdf')
                    else 'classic')
        self.furniture = re.compile(cfg(subject, 'furniture'), re.I)
        self.lines = read_lines(self.path, self.furniture)
        self.flags = []
        self.text_pages = {}          # question number -> [pages of its text]
        self.leads = {}               # question number -> its printed title
        self.letter_x = self._letter_column()
        self.left_margin = self._left_margin()
        self._asks = (self._walk() if self.era == 'modern'
                      else self._walk_classic())
        self._aural = self._walk_aural() if self.aural_path else []

    # ------------------------------------------------------------ layout ---
    def _letter_column(self):
        """Where a part LETTER is printed, measured from the unambiguous ones.

        a-h and j-l are letters and nothing else; only "(i)" can be read two
        ways. So the column is measured from the markers that cannot lie, and
        "(i)" is then tested against it. The MODE, never the minimum: one
        outlier four points left of the column its thirty siblings sit in put
        every real letter outside the tolerance when the minimum was used.
        """
        pattern = cfg(self.subject, 'q_head')
        head = re.compile(pattern) if pattern else None
        # Every letter of this subject's own alphabet EXCEPT "i", which is
        # also the first roman — see the docstring. Bulgarian's Cyrillic
        # alphabet has no such collision, so all five of its letters count.
        alpha = ''.join(c for c in letters_for(self.subject) if c != 'i')
        column_pat = re.compile(r'^\(?\s*[' + alpha + alpha.upper() +
                                r']\s*[,).:]\s')
        by_q, q = {}, None
        for line in self.lines:
            m = head.match(line.text) if head else None
            if m:
                q = int(m.group(1))
                continue
            if column_pat.match(line.text):
                by_q.setdefault(q, []).append(round(line.x))
        self.letter_x_by_q = {k: max(set(v), key=v.count)
                              for k, v in by_q.items()}
        every = [x for v in by_q.values() for x in v]
        return max(set(every), key=every.count) if every else 56.7

    def _left_margin(self):
        """The page's own left margin — the x most printed lines start at."""
        xs = [round(l.x) for l in self.lines]
        return max(set(xs), key=xs.count) if xs else 56.7

    def _column_for(self, q):
        return self.letter_x_by_q.get(q, self.letter_x)

    def _is_letter(self, x, prev_letter, q=None):
        """Is this "(i)" the ninth letter or the first roman?

        Both conditions, never one. Indent alone reads an indented roman as a
        letter; sequence alone reads "(h)(i)" as the letter after (h).
        """
        return x <= self._column_for(q) + LETTER_TOL and prev_letter == 'h'

    # ------------------------------------------------------------- walking --
    def _walk(self):
        """The MODERN booklet: Part A Reading and Part B Written Production."""
        first_letter = letters_for(self.subject)[0]
        q_head = re.compile(cfg(self.subject, 'q_head'))
        section_tab = re.compile(cfg(self.subject, 'section_tab'))
        furniture = re.compile(cfg(self.subject, 'furniture'), re.I)
        source_line = re.compile(cfg(self.subject, 'source_line'), re.I)
        rubric = re.compile(cfg(self.subject, 'rubric'), re.I)

        asks, q = [], None
        letter = roman = None
        current, last_y = None, None
        text_pages, leads = {}, {}

        def close():
            nonlocal current
            if current is not None:
                current.text = _norm(current.text)
                asks.append(current)
                current = None

        # The section tab is printed in the MARGIN of the page its section
        # opens on, and pymupdf reports it after the questions beside it. Read
        # in stream order it arrives too late to file a single ask. It is a
        # property of the PAGE, so it is resolved per page before the walk —
        # and the pages BEFORE the first tab are Part A, because the tab marks
        # where a section starts and Part A is the first one.
        by_page = self._section_by_page(self.lines, section_tab, first='A')
        section = 'A'

        for line in self.lines:
            if furniture.match(line.text) and len(line.text) < 60:
                continue
            section = by_page.get(line.page, section)
            if section_tab.match(line.text):
                continue
            head = q_head.match(line.text)
            if head and not _is_choice_rubric(line.text):
                close()
                q = int(head.group(1))
                letter = roman = None
                last_y = None
                leads[q] = line.text
                continue
            if q is None:
                continue
            lm = LETTER.match(line.text)
            rm = ROMAN.match(line.text)
            marker = None
            if rm and not (rm.group(1).lower() == 'i'
                           and self._is_letter(line.x, letter, q)):
                marker = ('roman', rm.group(1).lower(), rm.group(2))
            elif lm and (not rm or self._is_letter(line.x, letter, q)):
                # A letter marker stands at the question's own left margin. A
                # word that merely begins with a bracketed letter does not.
                if line.x <= self._column_for(q) + LETTER_TOL \
                        or lm.group(1).lower() == next_letter(
                            letter, first_letter):
                    marker = ('letter', lm.group(1).lower(), lm.group(2))
            if marker:
                kind, mark, rest = marker
                close()
                if kind == 'letter':
                    letter, roman = mark, None
                    # "(e) (i) Qual é o seu público-alvo?" — the SEC glues a
                    # letter and its first roman onto one printed line, and
                    # reading only the letter loses the roman entirely.
                    inner = ROMAN.match(rest)
                    if inner:
                        roman, rest = inner.group(1).lower(), inner.group(2)
                else:
                    roman = mark
                current = Ask(section, q, letter, roman, rest, line.page)
                last_y = line.y
                continue
            if current is not None and line.page == current.page \
                    and last_y is not None and 0 <= line.y - last_y <= LINE_GAP \
                    and not rubric.match(line.text):
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
            # In the WRITTEN PRODUCTION section a question's rubric is its
            # options' only printed words: 2023 Higher heads Question 5
            # "Observe as imagens com atenção e escolha uma: (a) ou (b) ou
            # (c)." and then prints three PICTURES, so (a), (b) and (c) have
            # no text of their own at all. Kept on the question, the option is
            # an ask a reader can see; dropped, it censuses as an empty leaf.
            if section == 'B' and letter is None and q is not None \
                    and len(leads.get(q, '')) < 400:
                leads[q] = _norm(f'{leads.get(q, "")} {line.text}')
            # Everything printed before the first ask of a question is its
            # reading text, and the card carries those pages beside the ask.
            if letter is None and not source_line.match(line.text):
                text_pages.setdefault(q, [])
                if line.page not in text_pages[q]:
                    text_pages[q].append(line.page)
        close()
        self.text_pages, self.leads = text_pages, leads
        asks = _dedupe(asks)
        self._check_sections(asks)
        return asks

    def _walk_classic(self):
        """The CLASSIC booklet: two or three numbered PARTS on printed texts.

        The passage comes first and the questions after it, both at the same
        left margin. What separates them is not wording: it is the SEC's own
        NUMBERING. A question opens with the number after the one before it —
        1, then 2, then 3 — printed with a full stop or a bracket at the
        part's left margin, and no line of a passage does that. (The Dutch
        booklet proves the rule from the other side: it numbers its passage
        PARAGRAPHS too, "10 Schilders als Rembrandt…", and prints them with no
        stop and no bracket at all.) Reading the boundary off an attribution
        line instead found nothing at all in Portuguese 2021, whose text is
        signed "Sophia de Mello Breyner Andresen, in Contos Exemplares".

        The tariff is printed HERE, in the right-hand margin — "(5)", "(5×1)",
        "(5 puncte)", "(1 punt)" — and nowhere else in the sitting's two
        documents, because the classic schemes print answers with no marks
        beside them at all.

        Only the FIRST part sets numbered questions. The parts after it are
        written production: either a single prompt, or two titled options the
        candidate chooses between, and both are read here so that the
        denominator holds them and the exclusions ledger can answer for them.
        """
        part_pat = re.compile(cfg(self.subject, 'classic_part'), re.I)
        part_map = cfg(self.subject, 'classic_part_map') or {}
        essay_pat = cfg(self.subject, 'essay_title')
        essay_pat = re.compile(essay_pat, re.I) if essay_pat else None
        letter_pat = letter_pattern(self.subject)
        first_letter = letters_for(self.subject)[0]
        # The head's second half, where the SEC sets it in a cell of its own:
        # the Croatian booklet prints "I." and "dio" as two printed lines.
        tail = cfg(self.subject, 'classic_part_tail')
        tail_pat = re.compile(tail, re.I) if tail else None
        numeral_only = re.compile(r'^(I{1,3}|[123])\s*\.?$')
        furniture = re.compile(cfg(self.subject, 'furniture'), re.I)

        asks, part, q, letter = [], None, None, None
        current, last_y = None, None
        # The last line of the reading part that opened no ask. Where the SEC
        # prints a question with no number of its own, that line IS its words.
        pending_stem = ''
        text_pages = {}
        first_part = None
        # The writing part's own prompt, gathered until an option marker
        # appears. If none does, the whole prompt IS the part's single ask.
        prompt, prompt_page = [], None

        def close():
            nonlocal current
            if current is not None:
                _read_paper_tariff(current)
                # Every printed price comes OUT of the ask's own words, not
                # just a trailing one: the Dutch paper sets "(alinea 1)(1
                # punt)" in the middle of Question 1(c) and the card carried
                # its own tariff inside the question.
                current.text = _norm(PAPER_TARIFF.sub(' ', current.text))
                current.text = _norm(
                    BARE_TRAILING_PRICE.sub(' ', current.text))
                asks.append(current)
                current = None

        def close_part():
            nonlocal prompt, prompt_page
            close()
            if part is not None and part != first_part and prompt \
                    and not any(a.section == part for a in asks):
                asks.append(Ask(part, 1, None, None, _norm(' '.join(prompt)),
                                prompt_page or 1))
            prompt, prompt_page = [], None

        lines = self.lines
        if tail_pat is not None:
            lines = _join_part_heads(lines, numeral_only, tail_pat)
        for line in lines:
            if furniture.match(line.text) and len(line.text) < 60:
                continue
            pm = part_pat.match(line.text)
            if pm is None and len(line.text) < 40:
                # A head the SEC LETTERSPACED. The 2011 Bulgarian paper sets
                # "Пъ рва час т" — spaces inside the words, not between them —
                # and read as printed it matched nothing, so that whole sitting
                # censused zero asks. Retried with the spaces squeezed out;
                # only on a short line, so no sentence can reach this path.
                pm = part_pat.match(re.sub(r'\s+', '', line.text))
            if pm:
                close_part()
                token = next(g for g in pm.groups() if g).lower()
                part = part_map.get(token) or _part_token(token)
                first_part = first_part or part
                q, letter = None, None
                continue
            if part is None:
                continue
            if part != first_part:
                # A WRITING part. Only a titled option opens an ask here; every
                # other line is the prompt those options are chosen under.
                em = essay_pat.match(line.text) if essay_pat else None
                if em:
                    close()
                    q = _option_number(em.group(1))
                    current = Ask(part, q, None, None, line.text, line.page)
                    last_y = line.y
                    continue
                if current is not None and last_y is not None \
                        and 0 <= line.y - last_y <= LINE_GAP \
                        and line.page == current.page:
                    current.text += ' ' + line.text
                    last_y = line.y
                    continue
                close()
                prompt.append(line.text)
                prompt_page = prompt_page or line.page
                continue
            nm = NUMBERED.match(line.text)
            lm = letter_pat.match(line.text)
            at_margin = line.x <= self.left_margin + HEAD_INDENT
            # The RUN RESTARTS at 1, and where it does the questions have not
            # begun until now. Six Croatian sittings and eight Estonian ones
            # print the part head ABOVE the reading text rather than below it,
            # so the text's own numbered paragraphs — "1. Za razliku od…" —
            # run 1 to 11 inside Part I and are read as its questions, and the
            # SEC's Question 1 then censuses as Question 12.
            #
            # What separates them is the PRICE. Every question of this part
            # carries a printed tariff in the right-hand margin and no
            # paragraph of a reading text ever does, so a restart is taken
            # only where nothing collected so far in this part was priced;
            # where something was, the two runs are both kept and the census
            # flags the overlap rather than this quietly throwing a real ask
            # away.
            if nm and at_margin and int(nm.group(1)) == 1 and (q or 0) >= 2 \
                    and part == first_part \
                    and not any(a.section == part and a.margin_price
                                for a in asks + ([current] if current else [])):
                close()
                for a in [a for a in asks if a.section == part]:
                    text_pages.setdefault(part, [])
                    if a.page not in text_pages[part]:
                        text_pages[part].append(a.page)
                asks = [a for a in asks if a.section != part]
                q, letter = None, None
            # The number after the one before it, at the left margin, IS the
            # next question. Both conditions: a passage sentence can open with
            # a year and a full stop, and a wrapped line can start at the
            # margin, but neither is ever the next number in the run.
            if nm and int(nm.group(1)) == (q or 0) + 1 and at_margin:
                close()
                q, letter = int(nm.group(1)), None
                if nm.group(2):
                    # The letter glued to its question's own number — the 2016
                    # Swedish booklet's "1a." and "1b.". The question is that
                    # letter's parent and carries no words of its own.
                    if not any(a.key == (part, q, None, None) for a in asks):
                        asks.append(Ask(part, q, None, None, '', line.page))
                    letter = nm.group(2).lower()
                    current = Ask(part, q, letter, None, nm.group(3), line.page)
                    last_y = line.y
                    continue
                inner = letter_pat.match(nm.group(3))
                if inner and inner.group(1).lower() == 'a':
                    # The FIRST lettered part printed on its question's own
                    # line: the Hungarian booklet sets "1. a, Magyarázza meg…"
                    # and prints b to e beneath it. Read whole, the question
                    # swallowed its own first part and Question 1 censused as
                    # one leaf where the SEC prices five. Only "a" — a later
                    # letter on a question head would mean the marker column
                    # has been misread, and that is a fault to see, not to
                    # absorb.
                    asks.append(Ask(part, q, None, None, '', line.page))
                    letter = inner.group(1).lower()
                    current = Ask(part, q, letter, None, inner.group(2),
                                  line.page)
                else:
                    current = Ask(part, q, None, None, nm.group(3), line.page)
                last_y = line.y
                continue
            # A letter where the SEC printed NO number for its question. The
            # 2018 Slovenian booklet heads its first part "1. DEL" and then
            # sets the first question with no number of its own at all — its
            # five expressions run a) to e) and the next head printed is "2."
            # A letter can only belong to a question, and the question before
            # the printed "2." is Question 1.
            if lm and q is None and lm.group(1).lower() == 'a' \
                    and part == first_part:
                close()
                q = 1
                asks.append(Ask(part, q, None, None, pending_stem, line.page))
            if lm and q is not None \
                    and (lm.group(1).lower() == next_letter(letter,
                                                            first_letter)
                         or line.x <= self.letter_x + LETTER_TOL):
                close()
                letter = lm.group(1).lower()
                current = Ask(part, q, letter, None, lm.group(2), line.page)
                last_y = line.y
                continue
            if current is not None and last_y is not None \
                    and line.page == current.page \
                    and -BAND_TOL <= line.y - last_y <= (TARIFF_GAP
                                                         if _is_tariff_cell(line)
                                                         else LINE_GAP):
                # A right-margin price belongs to the ask above it however far
                # down the SEC set it: the 2021 Romanian paper prints Question
                # 6 over two lines and its "(5 puncte)" thirty-four points
                # below them, and a line-gap window left that ask unpriced.
                if _is_tariff_cell(line):
                    current.margin_price = line.text
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
            if q is None:
                pending_stem = line.text
                text_pages.setdefault(part, [])
                if line.page not in text_pages[part]:
                    text_pages[part].append(line.page)
        close_part()
        # The classic examination sets its text or texts before the questions
        # and asks every question of the part about them, so the pages are
        # collected under the PART and handed to each of its questions.
        self.text_pages = {}
        pages = text_pages.get(first_part) or []
        for a in asks:
            self.text_pages.setdefault(a.q, pages)
        self.leads = {}
        asks = _dedupe(asks)
        _walk_down_paper_splits(asks)
        return asks

    @staticmethod
    def _section_by_page(lines, pattern, first=None):
        """{page: section}, the tab carrying forward until the next one."""
        seen, out, current = {}, {}, first
        for line in lines:
            m = pattern.match(line.text)
            if m and line.page not in seen:
                seen[line.page] = m.group(1).upper()
        for page in range(1, max((l.page for l in lines), default=0) + 1):
            current = seen.get(page, current)
            out[page] = current
        return out

    def _check_sections(self, asks):
        """The tab and the question numbers must tell the same story."""
        by_q = {}
        for a in asks:
            by_q.setdefault(a.q, set()).add(a.section)
        for q, secs in sorted(by_q.items()):
            if len(secs) > 1:
                self.flags.append(
                    {'type': 'section-split', 'where': f'Q{q}',
                     'detail': f'the same question is tabbed {sorted(secs)}'})
        reading = sorted(q for q, s in by_q.items() if s == {'A'})
        writing = sorted(q for q, s in by_q.items() if s == {'B'})
        if reading and writing and max(reading) >= min(writing):
            self.flags.append(
                {'type': 'section-order', 'where': '',
                 'detail': f'Section A holds {reading} and Section B {writing}'})
        if None in {a.section for a in asks}:
            self.flags.append({'type': 'section-missing', 'where': '',
                               'detail': 'an ask was printed before any tab'})

    # ----------------------------------------------------------- listening --
    def _walk_aural(self):
        """The Listening Comprehension booklet's own asks.

        Counted, never carded: the ask can only be answered from the recording.
        The count is what the denominator needs and what the exclusions ledger
        has to match one for one.
        """
        aural_tab = re.compile(cfg(self.subject, 'aural_tab'))
        furniture = re.compile(cfg(self.subject, 'furniture'), re.I)
        asks, section, item, roman = [], None, None, None
        current, last_y = None, None

        def close():
            nonlocal current
            if current is not None:
                current.text = _norm(current.text)
                asks.append(current)
                current = None

        lines = read_lines(self.aural_path, self.furniture)
        by_page = self._section_by_page(lines, aural_tab)
        for line in lines:
            if furniture.match(line.text) and len(line.text) < 60:
                continue
            page_section = by_page.get(line.page)
            if page_section != section:
                close()
                section, item, roman = page_section, None, None
            if aural_tab.match(line.text):
                continue
            if section is None:
                continue
            nm = NUMBERED.match(line.text)
            if nm:
                close()
                item, roman = int(nm.group(1)), None
                rest = ((nm.group(2) or '') + ' ' + nm.group(3)).strip()
                inner = ROMAN.match(rest)
                if inner:
                    roman, rest = inner.group(1).lower(), inner.group(2)
                # "(1) Aconteceu algo misterioso. (i) Quando?" — the SEC
                # sets an item's stem and its FIRST part on one printed line
                # of the listening booklet, and reading only the number left
                # the roman inside the stem: the part censused as absent and
                # its sibling "(ii)" reported a roman-gap for having no (i).
                inner = INNER_FIRST_ROMAN.search(rest)
                if roman is None and inner and inner.start() > 0:
                    stem = _norm(rest[:inner.start()])
                    if stem:
                        asks.append(Ask(f'L{section}', item, None, None, stem,
                                        line.page))
                    roman, rest = 'i', rest[inner.end():]
                current = Ask(f'L{section}', item, None, roman, rest, line.page)
                last_y = line.y
                continue
            rm = ROMAN.match(line.text)
            if rm and item is not None:
                close()
                roman = rm.group(1).lower()
                current = Ask(f'L{section}', item, None, roman, rm.group(2),
                              line.page)
                last_y = line.y
                continue
            if current is not None and last_y is not None \
                    and 0 <= line.y - last_y <= LINE_GAP \
                    and line.page == current.page:
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
        close()
        return _dedupe(asks)

    # ------------------------------------------------------------- the API --
    def all_asks(self):
        """Every leaf the booklets print: a lettered ask with romans under it
        is not a leaf, its romans are."""
        asks = self._asks + self._aural
        has_roman = {(a.section, a.q, a.letter) for a in asks if a.roman}
        has_letter = {(a.section, a.q) for a in asks if a.letter}
        parents = {(a.section, a.q, a.letter): a for a in asks
                   if a.roman is None}
        parents.update({(a.section, a.q, None): a for a in asks
                        if a.letter is None and a.roman is None})
        out = []
        for a in asks:
            if a.roman:
                parent = parents.get((a.section, a.q, a.letter))
                a.stem = parent.text if parent is not None else ''
                out.append(a)
            elif a.letter:
                parent = parents.get((a.section, a.q, None))
                if parent is not None and parent is not a:
                    a.stem = parent.text
                elif not CHOICE_ONLY.sub('', a.text).strip():
                    # No parent ask, and no words of its own: the question's
                    # own printed rubric is all this option has.
                    a.stem = self.leads.get(a.q, '')
                if (a.section, a.q, a.letter) not in has_roman:
                    out.append(a)
            elif (a.section, a.q) not in has_letter \
                    and (a.section, a.q, None) not in has_roman:
                out.append(a)
        return out

    def reading_asks(self):
        return [a for a in self.all_asks()
                if a.section == 'A' or a.section == 'I']

    def writing_asks(self):
        return [a for a in self.all_asks() if a.section in ('B', 'II', 'III')]

    def aural_asks(self):
        return [a for a in self.all_asks() if (a.section or '').startswith('L')]

    def _part_totals(self):
        pattern = cfg(self.subject, 'classic_part')
        if not pattern:
            return {}
        return _part_head_tariff(self.lines, re.compile(pattern, re.I))

    def lead(self, q):
        return self.leads.get(q, '')

    def pages_for(self, q):
        return self.text_pages.get(q) or []

    def cover_marks(self):
        """What the booklets say on their own covers or instructions, added.

        A CLASSIC booklet may state no total at all — the 2021 Dutch paper
        prints "(30 punten)" beside Deel 1 and "(40 punten)" beside Deel 2 and
        nowhere says seventy — so where the sentence is absent the PART HEADS
        are added instead. Both are printed on the paper; nothing is inferred.
        """
        if self.era == 'classic':
            parts = self._part_totals()
            # The Romanian paper prints each part's share AND the paper's own
            # total in one cell — "(30/100)" — so where that denominator is
            # printed it is the total, and a sum is not needed. The 2023 paper
            # sets no cell at all beside "PARTEA a II-a", and summed it made a
            # hundred-mark paper look like a seventy-mark one.
            denom = {d for _v, d in parts.values() if d}
            if len(denom) == 1:
                return denom.pop()
            if parts:
                return sum(v for v, _d in parts.values())
        total = 0
        for path in [self.path] + ([self.aural_path] if self.aural_path else []):
            with pymupdf.open(path) as doc:
                text = _norm(' '.join(doc[p].get_text()
                                      for p in range(min(3, doc.page_count))))
            # The sentence the booklet states its own total in, before any
            # per-section figure: "This examination carries 180 marks in
            # total." Taking the first "N marks" on the page instead took
            # Section A's 50 in 2022 and called the booklet a 50-mark paper.
            # The sentence the booklet states its own total in, before any
            # per-section figure: "This examination carries 180 marks in
            # total.", "Maximum: 100 de puncte", "Totaal: 100 punten". Taking
            # the first "N marks" on the page instead took Section A's 50 in
            # 2022 and called the booklet a 50-mark paper.
            m = re.search(r'carries\s+(\d{2,3})\s*marks', text, re.I) \
                or re.search(r'(?:M[áa]ximo|Maximum|Totaal|Total)'
                             r'[^\d\n]{0,30}?(\d{2,3})\b', text, re.I) \
                or re.search(r'(\d{2,3})\s*marks\b', text, re.I)
            if m:
                total += int(m.group(1))
        return total


# The word the SEC prints BETWEEN two options of a choice. It is furniture, not
# an ask's text: 2024 Ordinary's Question 5(c) is a picture with "OU" above it,
# and read as the option's own words it censused as a leaf saying "OU".
CHOICE_ONLY = re.compile(r'^\s*(?:OU|OR|NO)\s*$', re.I)


def _part_token(raw):
    """"i", "a ii-a", "2" — the part number, as a Roman numeral token."""
    raw = re.sub(r'[\s‐–-]', '', raw.lower())
    table = {'i': 'I', 'ii': 'II', 'iii': 'III',
             'aiia': 'II', 'aiiia': 'III',
             '1': 'I', '2': 'II', '3': 'III'}
    return table.get(raw, raw.upper())


def _option_number(raw):
    """The option's own number, whether the SEC titled it "1" or "a"."""
    raw = raw.strip().lower()
    return int(raw) if raw.isdigit() else ord(raw) - ord('a') + 1


def _dedupe(asks):
    """An ask printed twice keeps the printing that has the question in it.

    The written booklet reprints Question 5's three options on a page of its
    own as an ANSWER SHEET — "Opção:  (a)   (b)   (c)" — and the listening
    booklet does the same with a table. Those markers open asks with no words
    at all, and taken as the later printing they overwrote the real question:
    every Section B option in the corpus censused as an empty leaf.
    """
    best = {}
    order = []
    for a in asks:
        if a.key not in best:
            best[a.key] = a
            order.append(a.key)
        elif len(a.text) > len(best[a.key].text):
            best[a.key] = a
    return [best[k] for k in order]


def _part_head_tariff(lines, part_pat):
    """{part head text: the marks printed beside it}, from the same baseline.

    The SEC right-aligns a part's own total against the head that names it —
    "PARTEA I" at x=56.7 and "(30/100)" at x=467.8 on one line — and pymupdf
    reports the two as separate lines, so they are put back together by y.
    """
    out = {}
    for i, line in enumerate(lines):
        if not part_pat.match(line.text):
            continue
        for other in lines[max(0, i - 3):i + 4]:
            if other is line or other.page != line.page:
                continue
            if abs(other.y - line.y) > 4.0 or other.x < line.x + 40:
                continue
            # At the END of the cell, not the whole of it: the 2023 Dutch
            # paper prints "tekstbegrip (30 punten)" as one text cell, and a
            # whole-cell match found no total for Deel 1 at all.
            # The bracket is round in nine languages and SQUARE in
            # Croatian ("I. dio [30 bodova]"); the number may carry its own
            # mark word on BOTH sides of the slash ("(30 pont / 100 pont)");
            # and four languages print a word before it — "kuni 30 punkti",
            # "maksimum 30 point", "Totalt 30 poäng", "Max. 100 poäng". All
            # four forms are the same printed total, and a pattern that knew
            # only the first read no total at all for five of the twelve
            # subjects on this reader.
            m = re.search(
                r'[(\[]\s*(?:\w+\.?\s+){0,2}?(\d{1,3})\s*'
                r'(?:' + MARK_WORD + r')?\s*'
                r'(?:/\s*(\d{1,3})\s*(?:' + MARK_WORD + r')?\s*)?[)\]]$',
                other.text.strip(), re.I)
            if m:
                out[line.text] = (int(m.group(1)),
                                  int(m.group(2)) if m.group(2) else None)
                break
    return out


def _walk_down_paper_splits(asks):
    """A split printed on the QUESTION, walked down to the parts it prices.

    The classic paper prices Question 1 "(5×1)" in its right-hand margin and
    then prints five expressions a) to e) beneath it with no marks beside any
    of them. The tariff for each part IS stated — it is the "1" of the "5×1" —
    but one level above the ask it belongs to. Walked ONLY where the split and
    the parts agree in number; where they do not, nothing is inferred and each
    part keeps whatever it printed for itself.
    """
    kids = {}
    for a in asks:
        if a.letter:
            kids.setdefault((a.section, a.q), []).append(a)
    parents = {(a.section, a.q): a for a in asks if a.letter is None}
    # A "N × M" price is the GROUP's, wherever the SEC set it. The Romanian
    # paper right-aligns "(5 × 1 punct)" against the last of Question 1's five
    # expressions, so it lands on the baseline of "e) ființă socială" — and
    # read as that ask's own price it made one expression worth five marks and
    # the other four worth nothing.
    for key, group in kids.items():
        parent = parents.get(key)
        if parent is None or parent.tariff is not None:
            continue
        split = [k for k in group
                 if k.tariff and k.tariff[0] > 1 and k.tariff[1] is not None]
        if len(split) == 1 and split[0].tariff[0] == len(group):
            parent.tariff, parent.notation = split[0].tariff, split[0].notation
            split[0].tariff, split[0].notation = None, ''
            split[0].text = _norm(TRAILING_MARK.sub('', split[0].text))
    for a in asks:
        if a.letter or a.tariff is None:
            continue
        group = kids.get((a.section, a.q)) or []
        count, per, _total = a.tariff
        if per is not None and count != len(group) and per == len(group):
            # "(1 × 5 poäng)" — the SEC writes the split the other way round
            # as often as it writes "(5 × 1)", and which number is the COUNT
            # is settled by the group beneath it, never by picking the larger.
            # The 2014 Swedish paper prices Question 1 that way over five
            # expressions, and read as one answer worth five it left all five
            # of them unpriced and uncarded.
            count, per = per, count
            a.tariff = (count, per, count * per)
        if per is None or not group or len(group) != count \
                or any(k.tariff and k.margin_price for k in group):
            # A kid's own MARGIN price is its own and stops the walk-down; a
            # bracketed number inside its words does not, because the SEC
            # priced the group once, on the head, and the number in the words
            # is a paragraph reference (2022 Croatian Question 1).
            continue
        for kid in group:
            kid.text = _norm(PAPER_TARIFF.sub(' ', kid.text)) \
                if kid.tariff else kid.text
            kid.tariff = (1, per, per)
            kid.notation = (f'{a.notation} on the head of Q{a.q}, walked down '
                            f'to its {count} parts')


def _read_paper_tariff(ask):
    """The price the CLASSIC paper prints in its right-hand margin.

    "(5)" is a total; "(5×1)" is five answers at one point each. Both are read
    and neither is invented — a classic sitting whose ask carries no bracketed
    number keeps `tariff = None` and is refused rather than priced by guesswork.
    """
    # For a LETTERED part the margin cell wins where the SEC printed one — see
    # Ask.margin_price: a lettered expression's own words are the expression,
    # and a bracket inside them is a paragraph reference, not a price.
    #
    # For a whole QUESTION the words win, because the SEC prices a question
    # inside them: the 2022 Dutch paper sets "Geef drie voorbeelden … (3
    # punten) Leg ook uit waarom … (2 punten)" and the question is worth five.
    # Reading only the margin there took the last of the two and made that
    # question worth two.
    source = (ask.margin_price if ask.letter else '') or ask.text
    found = list(PAPER_TARIFF.finditer(source))
    if not found and ask.margin_price:
        bare = BARE_PRICE.match(ask.margin_price.strip())
        if bare:
            count = int(bare.group(1)) if bare.group(1) else 1
            per = int(bare.group(2))
            ask.tariff = (count, per, count * per)
            ask.notation = ask.margin_price.strip()
            return
    if not found:
        return
    split = [m for m in found if m.group(1)]
    if split:
        m = split[-1]
        count, per = int(m.group(1)), int(m.group(2))
        ask.tariff = (count, per, count * per)
        ask.notation = m.group(0).strip()
        return
    if len(found) > 1:
        # SEVERAL flat prices against one printed ask, which is the SEC
        # pricing two requirements inside it: 2022 Dutch Question 2 reads
        # "Geef drie voorbeelden … (3 punten) Leg ook uit waarom … (2 punten)"
        # and is worth five. Taking the last of them made the question worth
        # two, and Deel 1 then added to 27 against the 30 its own head prints
        # — which is how this was found.
        total = sum(int(m.group(2)) for m in found)
        ask.tariff = (len(found), None, total)
        ask.notation = ' + '.join(m.group(0).strip() for m in found)
        return
    m = found[0]
    ask.tariff = (1, int(m.group(2)), int(m.group(2)))
    ask.notation = m.group(0).strip()


# The line that NAMES the questions of a section rather than heading one:
# "Responda às TRÊS questões - Questão 3 (a) ou (b) ou (c), Questão 4 …". The
# SEC wraps it, so its tail reaches the reader as a line of its own that opens
# with a question head and is not one. Recognised by naming TWO question
# numbers, which a real head never does.
def _is_choice_rubric(text):
    return len(re.findall(r'Quest[ãa]o\s*\d', text, re.I)) > 1


# --------------------------------------------------------------- matching ---
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
# Words too common to be evidence of anything, in any of the three languages
# or in the English half of the paper.
STOP = {
    'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'for', 'is', 'are', 'on',
    'at', 'by', 'with', 'from', 'that', 'this', 'it', 'as', 'be', 'what',
    'which', 'how', 'why', 'does', 'do', 'did', 'was', 'were', 'has', 'have',
    'give', 'details', 'detail', 'about', 'his', 'her', 'him', 'she', 'they',
    'que', 'nao', 'para', 'com', 'uma', 'dos', 'das', 'por', 'seu', 'sua',
    'como', 'quais', 'qual', 'razao', 'texto', 'segundo', 'acordo',
    'paragrafo', 'paragrafos', 'parte', 'partes', 'sao', 'esta', 'este',
    'dos', 'nos', 'mais', 'pelo', 'pela', 'ele', 'ela', 'seus', 'suas',
}


def fold(text):
    """Lower-cased and accent-stripped, so ã and a are one word.

    Portuguese, Romanian and Dutch diacritics all survive the text layer
    intact, so this is a matching convenience, not a repair.
    """
    text = (text or '').lower()
    return ''.join(c for c in unicodedata.normalize('NFKD', text)
                   if not unicodedata.combining(c))


def bag(text):
    return {w for w in WORD.findall(fold(text)) if w not in STOP and len(w) > 2}


def score(a, b):
    """Shared content words over the LONGER side."""
    if not a or not b:
        return 0.0
    return len(a & b) / max(len(a), len(b))


# ----------------------------------------------------------------- the CLI ---
def sittings(subject):
    out = set()
    for path in glob.glob(os.path.join(papers_dir(subject), '*-paper.pdf')):
        m = re.match(r'(\d{4})-(hl|ol|cl)', os.path.basename(path))
        if m:
            out.add((int(m.group(1)), m.group(2)))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--aural', action='store_true')
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()

    if args.audit:
        for year, level in sittings(args.subject):
            P = EuPaper(year, level, args.subject)
            print(f'{year} {level.upper():2}  {P.era:7} '
                  f'{len(P.all_asks()):4} leaves '
                  f'({len(P.reading_asks())} reading, '
                  f'{len(P.writing_asks())} writing, '
                  f'{len(P.aural_asks())} listening)  '
                  f'cover {P.cover_marks()} marks  '
                  f'letter column x={P.letter_x:.1f}')
            for f in P.flags:
                print(f'      FLAG {f["type"]} {f["where"]} — {f["detail"]}')
        return 0

    P = EuPaper(args.year, args.level, args.subject)
    asks = P.aural_asks() if args.aural else [
        a for a in P.all_asks() if not (a.section or '').startswith('L')]
    for a in asks:
        label = f'{a.section} Q{a.q}' + (f'({a.letter})' if a.letter else '')
        label += f'({a.roman})' if a.roman else ''
        print(f'p{a.page:<3} {label:22} {a.notation:10} {a.text[:100]}')
    print(f'\n{len(asks)} leaf ask(s)')
    for f in P.flags:
        print(f'FLAG {f["type"]} {f["where"]} — {f["detail"]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
