#!/usr/bin/env python3
"""Pair a paper part with its scheme part by what they SAY, not by their keys.

    python3 scripts/markbank/authoring/align.py biology 2021 hl

Both documents are parsed into (question, letter, roman) keys, and the obvious
thing is to join on the key. It does not hold. The two documents number
themselves independently, sections restart, an "Or (b)" alternative shifts every
part beneath it, and a single misread anywhere slides the rest out of step. On
Biology 2021 HL the key join hands Q6(a) — a true/false statement about
adrenaline — the marking points for carpals and tarsals, which belong to Q7.

A card built on that pairing shows a real question with a real answer that does
not answer it, and every gate downstream passes it: the question is verbatim
from the paper, the marking point is verbatim from the scheme, and the
provenance check only asks whether each appears in its own document. Nothing
would catch it but a person reading the card.

So the pairing is earned instead. The scheme repeats the question it is marking
— its cue — and that cue is a compressed echo of the paper's wording. Scoring
every scheme part against every paper part on shared content words and keeping
only pairs that agree well enough turns an assumption into evidence. Parts that
cannot be paired confidently are reported, not guessed at.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper import Paper                                     # noqa: E402
from scheme_pdf import SchemePdf                            # noqa: E402

WORD = re.compile(r"[a-z']+")
# Words too common to carry evidence of a match.
STOP = {'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'for', 'is', 'are',
        'on', 'at', 'by', 'with', 'from', 'that', 'this', 'it', 'as', 'be',
        'one', 'two', 'three', 'each', 'following', 'above', 'below', 'your',
        'you', 'state', 'give', 'name', 'what', 'which', 'how', 'why'}


def bag(text):
    return {w for w in WORD.findall((text or '').lower()) if w not in STOP and len(w) > 2}


def score(a, b):
    """Jaccard-ish overlap, biased to how much of the SHORTER side is covered."""
    if not a or not b:
        return 0.0
    shared = len(a & b)
    return shared / min(len(a), len(b))


def align(subject, year, level, floor=0.55, margin=0.15, min_cue=4):
    P = Paper(subject, year, level)
    S = SchemePdf(subject, year, level)
    paper_parts = [(k, P.text(*k)) for k in P.paths()]
    paper_parts = [(k, t, bag(t)) for k, t in paper_parts if t]

    pairs, unpaired = {}, []
    for key in S.paths():
        points = S.points(*key)
        if not points:
            continue
        # The cue is whatever the scheme says before its answers; the first
        # point carries it, because this parser deliberately leaves it in place.
        cue = bag(points[0])
        # A three-word cue matches half the paper at full score and means
        # nothing. Evidence has to be substantial before it counts as evidence.
        if len(cue) < min_cue:
            unpaired.append((key, 0.0, 'cue too short to identify a part'))
            continue
        # Sorted on the score alone: part keys carry None and comparing them
        # as a tie-break raises rather than ordering.
        ranked = sorted(((score(cue, pbag), pkey) for pkey, _, pbag in paper_parts),
                        key=lambda pair: pair[0], reverse=True)
        best_score, best = ranked[0] if ranked else (0.0, None)
        runner = ranked[1][0] if len(ranked) > 1 else 0.0
        if best is None or best_score < floor:
            unpaired.append((key, round(best_score, 2), 'no part scores well enough'))
        elif best_score - runner < margin:
            # Two parts fit equally well, so the evidence does not pick one.
            unpaired.append((key, round(best_score, 2),
                             f'ambiguous — runner-up scores {runner:.2f}'))
        else:
            pairs[key] = (best, round(best_score, 2))
    return P, S, pairs, unpaired


if __name__ == '__main__':
    subject, year, level = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    P, S, pairs, unpaired = align(subject, year, level)
    agree = sum(1 for k, (pk, _) in pairs.items() if k == pk)
    print(f'{subject} {year} {level.upper()}: {len(pairs)} paired, '
          f'{len(unpaired)} unpaired; {agree} of the pairs match on key too')
    for k, sc, why in unpaired[:5]:
        print(f'  UNPAIRED {S.ref(k):<16} {sc}  {why}')
    print()
    for k, (pk, sc) in list(pairs.items())[:12]:
        mark = '=' if k == pk else '≠'
        print(f'  {S.ref(k):<16} {mark} {P.ref(pk):<16} {sc}  {(P.text(*pk) or "")[:64]}')


def align_ordered(subject, year, level, floor=0.30):
    """Pair the two documents by order as well as by wording.

    Text alone cannot pair every subject. Chemistry and Home Economics schemes
    barely restate the question they are marking — they list the accepted answer
    and stop — so on Chemistry 2021 HL only two of fifty-eight parts could be
    paired on wording, and pairing the rest by key is what hands Q6(a) the
    answers to Q7.

    But both documents run through the paper in the same order, and that is
    evidence too. This walks the two sequences together, Needleman-Wunsch
    fashion, scoring a pairing on shared wording and allowing either side to
    skip. Order is enforced by construction: a pairing can never cross another,
    so one misread cannot slide the rest out of step the way a key join does.

    A pair still has to earn its place. Where the wording gives no support at
    all the pairing rests on position alone, and those are returned separately
    so they can be looked at rather than trusted.
    """
    P = Paper(subject, year, level)
    S = SchemePdf(subject, year, level)
    pkeys = [k for k in P.paths() if P.text(*k)]
    skeys = [k for k in S.paths() if S.points(*k)]
    pbags = [bag(P.text(*k)) for k in pkeys]
    sbags = [bag(S.points(*k)[0]) for k in skeys]

    n, m = len(skeys), len(pkeys)
    GAP = -0.10
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = best[i - 1][j - 1] + score(sbags[i - 1], pbags[j - 1])
            up, left = best[i - 1][j] + GAP, best[i][j - 1] + GAP
            cell = max(diag, up, left)
            best[i][j] = cell
            back[i][j] = 'diag' if cell == diag else ('up' if cell == up else 'left')

    pairs, positional = {}, {}
    i, j = n, m
    while i > 0 and j > 0:
        step = back[i][j]
        if step == 'diag':
            s = score(sbags[i - 1], pbags[j - 1])
            (pairs if s >= floor else positional)[skeys[i - 1]] = (pkeys[j - 1], round(s, 2))
            i, j = i - 1, j - 1
        elif step == 'up':
            i -= 1
        else:
            j -= 1
    return P, S, pairs, positional
