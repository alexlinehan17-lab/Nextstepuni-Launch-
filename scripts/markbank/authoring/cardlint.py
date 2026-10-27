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
# Subjects generated straight into their deck keep no
# scripts/markbank/authored/<subject>.json: lint the deck's own card file
# (`{"cards": [...]}`), or the run would print "clean" without reading a card.
DECKS = os.path.join(HERE, '..', '..', '..', 'components', 'MarkBank', 'cards')
DECK_CARDS = {
    'geography': os.path.join(DECKS, 'geography', 'authored.json'),
}


def english_deck_cards():
    """The English cards the app serves, assembled as factory.ts does.

    English keeps two card files per level: the reviewed full-corpus
    manifests (published-{higher,ordinary}.json, written by
    english_publish.py) and the legacy 2021-2025 cards (authored.json). A
    legacy card is served only while no bridge has retired it, so reading
    authored.json alone linted 650 cards the app no longer shows and none of
    the 2,685 it does.
    """
    root = os.path.join(DECKS, 'english')
    cards, bridged = [], set()
    for level in ('higher', 'ordinary'):
        with open(os.path.join(root, f'published-{level}.json')) as fh:
            manifest = json.load(fh)
        if len(manifest['cards']) != manifest['cardCount']:
            raise SystemExit(f'cardlint: english {level} manifest count is stale')
        cards += manifest['cards']
        bridged |= set(manifest['bridgedLegacyIds'])
    with open(os.path.join(root, 'authored.json')) as fh:
        legacy = [c for c in json.load(fh)['cards'] if c['id'] not in bridged]
    return legacy + cards


# A deck whose served cards span several files is read by its own loader.
DECK_LOADERS = {
    'english': english_deck_cards,
}

SUBJECTS = ['agricultural-science', 'ancient-greek', 'applied-maths',
            'arabic', 'art', 'biology', 'bulgarian', 'business', 'chemistry',
            'classical-studies', 'computer-science', 'construction-studies',
            'croatian', 'czech', 'danish', 'dcg', 'dutch', 'economics',
            'engineering', 'english', 'estonian', 'finnish', 'french',
            'geography', 'german', 'history', 'home-economics', 'hungarian',
            'irish', 'italian', 'japanese', 'latin', 'latvian', 'lcvp',
            'lithuanian', 'mandarin-chinese', 'maths', 'modern-greek',
            'physical-education', 'physics', 'polish', 'portuguese',
            'religious-education', 'romanian', 'russian', 'slovakian',
            'slovenian', 'spanish', 'swedish', 'technology', 'ukrainian']

# Verb-anchored: "the scheme" is also Irish farm-support vocabulary (an
# Agricultural Science paper about joining a suckler scheme is not a leak),
# and "Award" alone matched a Green Impact Award. What marks a leak is the
# SCHEME DOING something to marks in the question area.
_LEAK_CORE = (
    r"\b[Tt]he (?:marking )?scheme(?:'s|\u2019s)?\s+"
    r'(?:marks?|accepts?|credits?|awards?|groups?|gives?|identifi|names?|'
    r'scores?|adds?|works|prints?|own)\b'
    r'|\bAccept(?:able)?:|\bAward(?:s)? (?:full |partial )?marks\b|'
    r'\bFull Credit\b|\bPartial Credit\b|\bLPC\b|\bHPC\b')
SCHEME_LEAK = re.compile(_LEAK_CORE + r'|\bMPC\b')

# MPC is a marking band (Middle Partial Credit) in most schemes and the
# Marginal Propensity to Consume in Economics, where it is printed on the
# question paper itself: "Assume that MPM is 0.25 and MPC is 0.65". Measured
# across every authored deck, the ONLY question-side occurrence of LPC, HPC or
# MPC in the bank is that Economics card — so the token has never caught a real
# leak and here it flags a correct question. Dropped for this subject only,
# rather than weakened for all of them.
SCHEME_LEAK_BY_SUBJECT = {'economics': re.compile(_LEAK_CORE)}
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
_FIG_REF_CORE = (
    rf'\b(?:the|this|following|above) {PICTORIAL}\b'
    rf'|\b{PICTORIAL} {LOCATIVE}\b'
    rf'|\b(?:the|this) {DESCRIBABLE} {LOCATIVE}\b'
    r'|\bin the extract\b|\baccompanying\b|\bgiven diagram\b')
FIG_REF = re.compile(r'\bshown\b|' + _FIG_REF_CORE, re.I)
# English questions use "shown" as an ordinary verb: "Love can be shown in
# many different ways", "the kindness or lack of kindness shown". Measured
# over all 2,685 served English cards, the word occurs on three cards, every
# one of them that verb, and none of them points at the page; the English
# references to printed matter are "the extract", "the photograph above" and
# the like, which the shared alternatives still catch. So for English a bare
# "shown" counts only when it points somewhere ("shown below", "shown on
# page 6"), rather than weakening the rule for every deck.
FIG_REF_BY_SUBJECT = {
    'english': re.compile(
        r'\bshown (?:below|above|opposite|overleaf|on (?:the )?(?:page|right|left))\b|'
        + _FIG_REF_CORE, re.I),
}
# A stimulus the PAPER never prints, so no crop could ever satisfy the
# reference. LCVP's Section A is answered from a DVD played in the examination
# hall: the paper prints the theme in words — "You will be shown a DVD about
# Voluntary Work in a Charity Shop as the theme." — and no artwork at all for
# the section. Flagging those seventy cards as ghost figures asks for a crop
# that cannot exist, and reviewing each one would record the same sentence
# seventy times. Named per subject, like SCHEME_LEAK_BY_SUBJECT above, rather
# than weakening the rule for every deck.
UNPRINTABLE_STIMULUS = {
    'lcvp': re.compile(r'\byou will be shown a DVD\b', re.I),
}
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


def load_cards(subject):
    """(cards, is_deck) for one subject; [] when it has no authored file."""
    if subject in DECK_LOADERS:
        return DECK_LOADERS[subject](), True
    deck = subject in DECK_CARDS
    path = DECK_CARDS[subject] if deck else os.path.join(AUTHORED, f'{subject}.json')
    if not os.path.exists(path):
        if deck:
            raise SystemExit(f'cardlint: {subject} deck file missing: {path}')
        return [], False
    with open(path) as fh:
        cards = json.load(fh)
    return (cards['cards'] if deck else cards), deck


READ_COUNTS = {}


def lint(subject):
    cards, deck = load_cards(subject)
    READ_COUNTS[subject] = len(cards)
    # The bindings file is where an OFFICIAL SOURCE page is declared; the
    # `sourceMaterial` field only appears once build-deck.mjs has resolved it
    # against the Paper Trail index. Reading the authored JSON alone therefore
    # reported five Physical Education cards as pointing at printed matter
    # they do not carry, when four of them carry the SEC's own page.
    bindings_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'card-source-bindings.json')
    bound = set()
    if os.path.exists(bindings_path):
        with open(bindings_path) as fh:
            bound = set(json.load(fh).get(subject, {}))
    flags = []
    for c in cards:
        stem = c.get('stem') or ''
        qtext = c.get('questionText') or ''
        # A bound OFFICIAL SOURCE page is the printed matter, shipped: the
        # card opens the examination page the reference points at. Counting
        # only crops flagged every LCVP case-study card, each of which already
        # carries the case study's own pages.
        has_fig = bool(c.get('figureKey') or c.get('questionFigureKey')
                       or c.get('sourceMaterial') or c['id'] in bound
                       # A deck card binds its crop directly; a solution crop
                       # is the answer, never the question's artwork.
                       or (deck and (c.get('questionFigure') or (
                           c.get('figure') and not c['figure'].get('solution')))))
        leak = SCHEME_LEAK_BY_SUBJECT.get(subject, SCHEME_LEAK)
        for field, text in (('stem', stem), ('questionText', qtext)):
            if leak.search(text):
                flags.append((subject, c['id'], 'scheme-leak',
                              f'{field}: {text[:90]}'))
        joined = f'{stem} {qtext}'
        m = FIG_REF_BY_SUBJECT.get(subject, FIG_REF).search(joined)
        table_only = bool(m) and re.search(
            r'(?:table|chart|graph)\b', m.group(0), re.I) and INLINE_TABLE.search(joined)
        unprintable = UNPRINTABLE_STIMULUS.get(subject)
        if (not has_fig and m and not SELF_WORK.search(joined)
                and not NO_DEPENDENCY.search(joined) and not table_only
                and not (unprintable and unprintable.search(joined))
                and c['id'] not in REVIEWED):
            flags.append((subject, c['id'], 'ghost-figure', joined.strip()[:90]))
        if label_junk(stem):
            flags.append((subject, c['id'], 'label-junk', stem[:90]))
        lettered = (NAMES_LETTERS.search(qtext)
                    and not INVITES_DRAWING.search(qtext))
        # A rubric card (Geography) decodes its letters in the scheme's own
        # rows, shown with the marking; it needs the printed page or crop that
        # shows the student the letters, not a label key over a figure.
        decoded = c.get('labelKey') or (deck and c.get('criteria'))
        if lettered and c['id'] not in REVIEWED and not (has_fig and decoded):
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
    # Name what was read: a subject whose cards live outside the file this
    # script opens reports zero here instead of a silent "clean".
    print(f'read {sum(READ_COUNTS.values())} cards: '
          + ', '.join(f'{s} {READ_COUNTS[s]}' for s in subjects))
    if not total:
        print('clean')
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
