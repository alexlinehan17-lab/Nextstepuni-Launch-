"""Cross-deck card lint: the defect classes a student actually screenshots.

Each check exists because a shipped card failed it in front of the owner:

  scheme-leak     "The scheme groups its answer under: South;" printed as a
                  STEM told the student the answer structure before they tried.
                  Scheme metadata may appear only on the scheme side of a card
                  (contextNote, notes) — never in stem or questionText.
  ghost-figure    "...the site plan shown in an extract" with no extract
                  shipped. A question-side text that points at printed matter
                  ("shown", "the diagram", "extract") must carry a figure or a
                  question figure. "On your drawing ..." refers to the
                  student's own work and is exempt.
  label-junk      A stem that is diagram-label soup ("F A B x km 8 km ...") —
                  many short tokens, no sentence. The old Maths failure mode.

Usage: python3 cardlint.py [subject ...]   (default: every authored deck)
Exit 1 if anything is flagged.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUTHORED = os.path.join(HERE, '..', 'authored')

SUBJECTS = ['maths', 'physics', 'biology', 'chemistry', 'economics', 'business',
            'home-economics', 'agricultural-science', 'construction-studies']

# Verb-anchored: "the scheme" is also Irish farm-support vocabulary (an
# Agricultural Science paper about joining a suckler scheme is not a leak),
# and "Award" alone matched a Green Impact Award. What marks a leak is the
# SCHEME DOING something to marks in the question area.
SCHEME_LEAK = re.compile(
    r"\b[Tt]he (?:marking )?scheme(?:'s|\u2019s)?\s+"
    r'(?:marks?|accepts?|credits?|awards?|groups?|gives?|identifi|names?|'
    r'scores?|adds?|works|prints?|own)\b'
    r'|\bAccept(?:able)?:|\bAward(?:s)? (?:full |partial )?marks\b|'
    r'\bFull Credit\b|\bPartial Credit\b|\bLPC\b|\bHPC\b|\bMPC\b')
# A reference is a GHOST only when it points at something ON THE PAGE.
# Two noun classes, because they behave differently:
#  PICTORIAL — a diagram/photograph/map cannot be prose, so naming one at all
#    means the page prints it.
#  DESCRIBABLE — "the apparatus", "this circuit", "the graph", "the image" are
#    routinely set out in words ("Name the apparatus used", "the image distance
#    v"), so they only count when a locative pins them to the page. Without
#    that split, 71 of physics's 78 flags were false.
PICTORIAL = r'(?:diagram|figure|extract|photograph|photo|sketch|drawing)'
DESCRIBABLE = r'(?:apparatus|circuit|arrangement|set-?up|image|graph|table|chart|curve|pattern|map)'
LOCATIVE = r'(?:below|above|opposite|shown|overleaf|on the (?:right|left))'
FIG_REF = re.compile(
    r'\bshown\b'
    rf'|\b(?:the|this|following|above) {PICTORIAL}\b'
    rf'|\b{PICTORIAL} {LOCATIVE}\b'
    rf'|\b(?:the|this) {DESCRIBABLE} {LOCATIVE}\b'
    r'|\bin the extract\b|\baccompanying\b|\bgiven diagram\b', re.I)
SELF_WORK = re.compile(
    r'\b(?:on|to|in) your (?:drawing|sketch|graph|diagram|answer)\b|'
    r'\byour answers? (?:to|from|in)\b|\bshown? (?:all )?(?:your|the) work'
    r'|\bshow (?:your|that|how|the|two|three|one)\b'
    r'|\byou have (?:shown|drawn|named)\b', re.I)


# The authoring pass sometimes states outright that the artwork is not needed
# ("Nothing in this part depends on the photograph."). That is a reviewed
# judgement, recorded on the card, and the lint honours it.
NO_DEPENDENCY = re.compile(
    r'\bnothing (?:in this part )?depends on\b|\bdoes not depend on the\b'
    r'|\bno figure is needed\b', re.I)
# A card that PRINTS the table it refers to has already shipped it: a run of
# numbers is the table, inline. Physics 2021 OL Q2 carries its own pressure /
# volume readings, so "the table above" is satisfied by the card itself.
INLINE_TABLE = re.compile(r'(?:\b\d[\d.,/]*\b[^\w]{0,4}){6,}')


# A chemical equation or an algebraic identity is short-token dense by
# nature — "H2 (g) + 1/2 O2 (g) -> H2O (l)" is the question, not label soup.
FORMULA = re.compile(r'[\u2192\u21cc\u2194=]|\+\s*\S')


# A card that names lettered parts is a figure card whatever words it uses:
# "Name the parts A, B, C" carries no figure-reference word at all, so the
# ghost-figure rule missed eleven Biology cards that build-deck then dropped.
# Mirrored from build-deck.mjs's namesLetters gate — a lettered question needs
# both the crop and a decoded label key.
# Case matters: a labelled PART is a capital ("the parts labelled A, B and C"),
# while lower-case letters on a diagram are quantities to measure or use —
# "Measure the lengths labelled r, d, and h" needs no decode at all.
NAMES_LETTERS = re.compile(
    r'(?i:\blabelled )[A-Z]\b'
    r'|(?i:\bstructures? )[A-Z](?:,| and )'
    r'|(?i:\bparts? )[A-Z](?:,| and )'
    r'|(?i:\blabelled\s+(?:parts|structures)\b)')
INVITES_DRAWING = re.compile(r'\b(?:draw|sketch|label the diagram)\b', re.I)


def label_junk(text):
    """Mostly short tokens and numbers, no sentence shape."""
    if not text or len(text) < 20:
        return False
    if FORMULA.search(text):
        return False
    words = text.split()
    if len(words) < 8:
        return False
    short = sum(1 for w in words if len(w) <= 3)
    return short / len(words) > 0.72 and text.count('.') == 0


# Cards a figure pass OPENED the paper for and found nothing to show: the
# "diagram below" is a blank answer frame the candidate fills in, or "the
# table below" is a two-cell box holding one datum the card already carries.
# Each entry records the reason, the same evidence discipline the exclusions
# files use — an unexplained silence would be indistinguishable from a miss.
REVIEWED_PATH = os.path.join(HERE, 'cardlint-reviewed.json')
REVIEWED = (json.load(open(REVIEWED_PATH))
            if os.path.exists(REVIEWED_PATH) else {})


def lint(subject):
    path = os.path.join(AUTHORED, f'{subject}.json')
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        cards = json.load(fh)
    flags = []
    for c in cards:
        stem = c.get('stem') or ''
        qtext = c.get('questionText') or ''
        has_fig = bool(c.get('figureKey') or c.get('questionFigureKey'))
        for field, text in (('stem', stem), ('questionText', qtext)):
            if SCHEME_LEAK.search(text):
                flags.append((subject, c['id'], 'scheme-leak',
                              f'{field}: {text[:90]}'))
        joined = f'{stem} {qtext}'
        m = FIG_REF.search(joined)
        table_only = bool(m) and re.search(
            r'(?:table|chart|graph)\b', m.group(0), re.I) and INLINE_TABLE.search(joined)
        if (not has_fig and m and not SELF_WORK.search(joined)
                and not NO_DEPENDENCY.search(joined) and not table_only
                and c['id'] not in REVIEWED):
            flags.append((subject, c['id'], 'ghost-figure', joined.strip()[:90]))
        if label_junk(stem):
            flags.append((subject, c['id'], 'label-junk', stem[:90]))
        lettered = (NAMES_LETTERS.search(qtext)
                    and not INVITES_DRAWING.search(qtext))
        if lettered and c['id'] not in REVIEWED and not (
                has_fig and c.get('labelKey')):
            flags.append((subject, c['id'], 'undecoded-letters',
                          qtext.strip()[:90]))
    return flags


def main():
    subjects = sys.argv[1:] or SUBJECTS
    total = 0
    for s in subjects:
        flags = lint(s)
        total += len(flags)
        if flags:
            print(f'== {s}: {len(flags)} flag(s)')
            for _, cid, cls, note in flags:
                print(f'  {cls:<13} {cid}: {note}')
    if not total:
        print('clean')
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
