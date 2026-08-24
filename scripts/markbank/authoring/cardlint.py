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
FIG_REF = re.compile(
    r'\bshown\b|\bthe (?:diagram|extract|map|photograph|photo|image|graph|chart) \b|'
    r'\bdiagram (?:below|above|opposite)\b|\bin the extract\b|\baccompanying\b|'
    r'\bgiven diagram\b|\bthe drawing shows\b', re.I)
SELF_WORK = re.compile(
    r'\b(?:on|to|in) your (?:drawing|sketch|graph|diagram|answer)\b|'
    r'\byour answers? (?:to|from|in)\b|\bshown? (?:all )?(?:your|the) work'
    r'|\bshow (?:your|that|how|the|two|three|one)\b', re.I)


def label_junk(text):
    """Mostly short tokens and numbers, no sentence shape."""
    if not text or len(text) < 20:
        return False
    words = text.split()
    if len(words) < 8:
        return False
    short = sum(1 for w in words if len(w) <= 3)
    return short / len(words) > 0.72 and text.count('.') == 0


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
        if not has_fig and FIG_REF.search(joined) and not SELF_WORK.search(joined):
            flags.append((subject, c['id'], 'ghost-figure', joined.strip()[:90]))
        if label_junk(stem):
            flags.append((subject, c['id'], 'label-junk', stem[:90]))
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
