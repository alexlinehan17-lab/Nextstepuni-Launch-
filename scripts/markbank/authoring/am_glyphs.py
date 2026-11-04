#!/usr/bin/env python3
"""Repair the Applied Maths schemes' variable names from their GLYPH IDS.

    python3 scripts/markbank/authoring/am_glyphs.py --audit

The fault
---------
The 2022-2024 schemes embed CambriaMath as a subset whose ToUnicode CMap is
wrong for about half its italic letters, and wrong in a way that hides itself:
every letter it gets wrong is mapped to ANOTHER letter of the same case. So

    |OB| = 20      arrives as   |OO| = 20
    v² = u² + 2as  arrives as   v² = u² + 2aa
    ∫dv = ∫2te⁻ᵗdt arrives as   ∫dd = ∫2te⁻ᵗdd

and mathtext.demangle(), which collapses the doubled italics this font also
emits, then collapses the two identical letters into one — so the line reads
"|O| = 20" and "v² = u² + 2a" and looks merely terse rather than wrong. 289
printed lines across the ten schemes are damaged this way. Every one of them
would have shipped a marking point the SEC never wrote.

Neither reader can see through it: `get_text()` and `get_texttrace()` both
report what the CMap says.

The repair
----------
The glyph id can. A subset font keeps the original font's glyph order, so the
italic capitals occupy one contiguous run of ids and the italic smalls another
— in the 2024 Higher scheme, gid 1827 is A and gid 1852 is Z, gid 1853 is a
and gid 1876 is z. Where the CMap happens to be right it corroborates the run;
where it is wrong the run outvotes it. This is derive_glyphs.py's argument
(glyph ids are trustworthy where ToUnicode is not) applied to a font whose
wrong answers are still valid Unicode, which is why derive_glyphs — which only
looks at codepoints outside the sane ranges — cannot see this one at all.

Nothing here is hand-mapped. `--audit` prints, per scheme, how many letters
the CMap got wrong, and the agreement rate on the ones it got right; a run
whose offset is not agreed by a clear majority is left alone rather than
guessed.
"""
import argparse
import collections
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'applied-maths', 'schemes')

# The alphabets a subset font lays out in one run, and where each starts.
# MATHEMATICAL ITALIC SMALL H is not in the block — Unicode had already
# assigned U+210E PLANCK CONSTANT to that glyph — so it is spelled out.
ALPHABETS = [
    ('U', 0x1D434, 26),      # MATHEMATICAL ITALIC CAPITAL A .. Z
    ('L', 0x1D44E, 26),      # MATHEMATICAL ITALIC SMALL a .. z
    ('g', 0x1D6FC, 25),      # MATHEMATICAL ITALIC SMALL ALPHA .. OMEGA
]
PLANCK = 0x210E              # the italic h


def _slot(ch):
    """(alphabet, index) for a character that belongs to one, else None."""
    u = ord(ch)
    if u == PLANCK:
        return 'L', 7
    for name, base, size in ALPHABETS:
        if base <= u < base + size:
            return name, u - base
    return None


def _char(name, index):
    for n, base, size in ALPHABETS:
        if n == name:
            if not 0 <= index < size:
                return None
            return chr(PLANCK) if (n == 'L' and index == 7) else chr(base + index)
    return None


MIN_VOTES = 3          # a run offset needs this many corroborating letters
MIN_SHARE = 0.55       # and this share of the run's own evidence
GAP = 40               # gids this far apart are different runs


def derive(doc):
    """{(font, gid): character} for every italic letter this document draws.

    Read from the drawn glyphs, not from the CMap: each run of ids is fitted to
    the alphabet it lays out, and the fit is decided by majority vote of the
    letters the CMap did get right.
    """
    seen = collections.defaultdict(collections.Counter)
    for page in doc:
        for sp in page.get_texttrace():
            for u, gid, _origin, _adv in sp['chars']:
                if gid is None or gid < 0:
                    continue
                slot = _slot(chr(u))
                if slot:
                    seen[(sp['font'], slot[0])][(gid, slot[1])] += 1
    out, stats = {}, collections.Counter()
    for (font, name), votes in seen.items():
        entries = sorted({gid for gid, _ in votes})
        runs, run = [], []
        for gid in entries:
            if run and gid - run[-1] > GAP:
                runs.append(run)
                run = []
            run.append(gid)
        if run:
            runs.append(run)
        for run in runs:
            offsets = collections.Counter()
            for (gid, index), n in votes.items():
                if gid in run:
                    offsets[gid - index] += n
            if not offsets:
                continue
            offset, best = offsets.most_common(1)[0]
            total = sum(offsets.values())
            if best < MIN_VOTES or best / total < MIN_SHARE:
                stats['run-not-agreed'] += 1
                continue
            for gid in run:
                ch = _char(name, gid - offset)
                if ch is None:
                    continue
                out[(font, gid)] = ch
            for (gid, index), n in votes.items():
                if gid in run:
                    stats['agree' if gid - index == offset else 'repaired'] += n
    return out, stats


# Where the derivation fitted a glyph id to the wrong letter, and what the
# page itself says. derive() reads each glyph's own ToUnicode through
# get_texttrace(); rawdict reads the same glyph through a different path, and
# where the two disagree the fit follows texttrace. For one id in this corpus
# texttrace is the one that is wrong.
#
# CambriaMath gid 1844. The 2022 Ordinary scheme sets Question 7's normal
# reactions and rawdict reads them correctly -- "𝑅𝑅2 × 5 = 800 × 3",
# "𝑅𝑅1 + 𝑅𝑅2 = 800" -- while texttrace's ToUnicode names the glyph 𝜇, so the
# fit taught the table μ and page_fix then overwrote every R on the page.
# The cards read "𝜇₂ = 480 N": the coefficient of friction is a RATIO and has
# no units, so 480 newtons of it is not a wrong answer but a meaningless one.
#
# Settled by the page and not by preference: the scheme prices the ask "find
# the reaction forces at the supports", the paper's own question asks for a
# force in newtons, and rawdict spells the letter R at every one of the seven
# places texttrace calls it μ. gid 2020 IS μ in this same font -- confirmed by
# both readers wherever it appears -- and is left alone.
GID_OVERRIDES = {
    ('CambriaMath', 1844): '\U0001d445',      # R, not μ
}


def page_fix(page, table):
    """{(block, line, span, char): the character it really is, or None to drop}.

    Keyed by POSITION in `page.get_text('rawdict')`, not by drawing origin.
    Origin cannot key it: this font emits a zero-advance ECHO after every
    italic letter, and rawdict reports that echo at the origin of the letter
    that FOLLOWS it, so "du" and "dt" both arrive as four glyphs at three
    origins and an origin-keyed table overwrites the very letter it is trying
    to repair.

    The two readers enumerate the same glyphs in the same order once spaces
    are set aside — get_texttrace() drops the ones rawdict reports — so the
    sequences are zipped and the walk is REFUSED outright if they ever fall
    out of step, rather than repairing a glyph by a position that has drifted.
    """
    trace = [(sp['font'], u, gid)
             for sp in page.get_texttrace()
             for (u, gid, _o, _a) in sp['chars'] if chr(u).strip()]
    out, i = {}, 0
    for bi, b in enumerate(page.get_text('rawdict')['blocks']):
        for li, ln in enumerate(b.get('lines', [])):
            for si, sp in enumerate(ln.get('spans', [])):
                for ci, c in enumerate(sp['chars']):
                    if not c['c'].strip():
                        continue
                    if i >= len(trace):
                        return {}
                    font, u, gid = trace[i]
                    i += 1
                    if gid is None or gid < 0:
                        out[(bi, li, si, ci)] = None
                        continue
                    # Only ever what the GLYPH ID says. Falling back on
                    # texttrace's own character replaced good text with
                    # U+FFFD wherever that reader has no mapping at all —
                    # 2025 Higher Q2 came out as "v�v�s�t��" for a line
                    # rawdict and glyphmap.json read perfectly well.
                    ch = table.get((font, gid))
                    if ch and ch != c['c']:
                        out[(bi, li, si, ci)] = ch
    return out if i == len(trace) else {}


def audit():
    for path in sorted(glob.glob(os.path.join(SCHEMES, '*.pdf'))):
        import pymupdf
        with pymupdf.open(path) as doc:
            table, stats = derive(doc)
            wrong = collections.Counter()
            for page in doc:
                for key, ch in page_fix(page, table).items():
                    wrong[ch] += 1
        print(f'{os.path.basename(path)[:-4]}: {len(table)} glyph ids fitted, '
              f'{stats["agree"]} letters confirmed, {stats["repaired"]} repaired, '
              f'{stats["run-not-agreed"]} run(s) left alone')
        if wrong:
            print('    repaired to: ' + ', '.join(
                f'{c}x{n}' for c, n in wrong.most_common(12)))
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--audit', action='store_true')
    ap.parse_args()
    sys.exit(audit())
