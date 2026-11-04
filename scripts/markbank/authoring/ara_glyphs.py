#!/usr/bin/env python3
"""Derive the Arabic repair map from the glyph OUTLINES in the corpus itself.

    python3 scripts/markbank/authoring/ara_glyphs.py [--write]

`derive_glyphs.py` learns a broken font's characters from its GLYPH IDS, on the
rule that an id means the same character everywhere in the same font. That rule
does not hold here. Every Arabic paper and scheme in the corpus embeds its own
SUBSET of Arabic Typesetting, cut by Word in the order that document happened to
use the glyphs, so gid 2034 is لد in the 2023 Higher scheme and something else
three files later. Keying on the id would put a different letter on a card and
never say so.

What IS stable is the outline. A subset copies the glyf entry verbatim, so the
same character has byte-identical contours in every file that uses it. So the
key here is a hash of the outline, and the evidence is the rest of the corpus:
where one document's ToUnicode names a glyph correctly, every other document
that draws the same outline is named from it.

Two things this had to learn:

* **A composite glyph must hash its components AND their offsets.** Arabic
  builds ج and خ from one base and one dot, differing only in whether the dot
  sits above or below; hashing the component list alone collapsed the two and
  99 outlines came back with two different letters attached. With the offsets
  in the hash the conflicts fall to 17, and every one of those is the same
  letter in two encodings (ﻨ and ن, ﺘ and ت) which NFKC folds together anyway.
* **A subset renumbers its components too**, so a composite's component gids
  are meaningless across files and have to be resolved to their own outline
  hashes first, recursively.

THE WIDTH OF THE CORPUS IS THE WHOLE POINT
------------------------------------------
Derived from the bank's own ten sittings alone, this map left 1,414 draws over
70 outlines with no evidence anywhere, and 14.6% of the Arabic words in the
corpus came out damaged — two of the ten papers unreadable outright. Fetching
the seventeen sittings either side of the window, which the Paper Trail corpus
already holds, dropped that to 0.1%: an outline the 2024 scheme never names is
named by the 2013 one. So the evidence corpus is DELIBERATELY wider than the
denominator. Those extra sittings live under
`examiner-reports/arabic/glyph-corpus/`, out of the way of `paper_census.py`,
which must count only the sittings the bank cards.

    python3 scripts/markbank/fetch-corpus.py arabic --schemes --from 2010 --to 2026
    # then move everything outside 2021-2025 into glyph-corpus/

Nothing is guessed. A glyph whose outline appears nowhere in the corpus with a
sane ToUnicode entry stays U+FFFD, is counted by `ara_text.py --audit`, and the
word carrying it is reported damaged rather than repaired.
"""
import argparse
import collections
import glob
import hashlib
import json
import os
import struct
import sys
import unicodedata

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(HERE, 'glyphmap-arabic.json')
CORPUS = os.path.join(ROOT, 'examiner-reports', 'arabic')


def _tables(buf):
    n = struct.unpack('>H', buf[4:6])[0]
    return {buf[12 + 16 * i:16 + 16 * i].decode('latin1'):
            struct.unpack('>II', buf[20 + 16 * i:28 + 16 * i]) for i in range(n)}


def font_hashes(buf):
    """(gid -> outline hash, set of gids that draw NOTHING) for one subset.

    A glyph whose `loca` entry is empty paints no ink. In these fonts that is
    the word space — 2023 Higher draws gid 3 one thousand three hundred and
    seventy-nine times with no ToUnicode entry for it — and calling a blank
    glyph a damaged letter reported that whole paper unreadable when it is not.
    A blank is not a guess: the font says the glyph has no outline.
    """
    try:
        t = _tables(buf)
    except Exception:
        return {}
    if not {'glyf', 'loca', 'head', 'maxp'} <= set(t):
        return {}, set()
    ho, _ = t['head']
    fmt = struct.unpack('>h', buf[ho + 50:ho + 52])[0]
    mo, _ = t['maxp']
    n = struct.unpack('>H', buf[mo + 4:mo + 6])[0]
    lo, _ = t['loca']
    go, _ = t['glyf']
    try:
        if fmt == 0:
            locs = [struct.unpack('>H', buf[lo + 2 * i:lo + 2 * i + 2])[0] * 2
                    for i in range(n + 1)]
        else:
            locs = [struct.unpack('>I', buf[lo + 4 * i:lo + 4 * i + 4])[0]
                    for i in range(n + 1)]
    except Exception:
        return {}, set()
    blobs, blank = {}, set()
    for gid in range(n):
        a, b = locs[gid], locs[gid + 1]
        if b > a:
            blobs[gid] = buf[go + a:go + b]
        else:
            blank.add(gid)
    memo = {}

    def digest(gid, depth=0):
        if gid in memo:
            return memo[gid]
        blob = blobs.get(gid)
        if blob is None or depth > 5 or len(blob) < 10:
            memo[gid] = None
            return None
        memo[gid] = None                     # break cycles
        nc = struct.unpack('>h', blob[0:2])[0]
        if nc >= 0:
            out = hashlib.sha1(b'S' + blob).hexdigest()[:16]
        else:
            parts, off = [], 10
            try:
                while True:
                    flags, gi = struct.unpack('>HH', blob[off:off + 4])
                    off += 4
                    if flags & 1:
                        a1, a2 = struct.unpack('>hh', blob[off:off + 4]); off += 4
                    else:
                        a1, a2 = struct.unpack('>bb', blob[off:off + 2]); off += 2
                    if flags & 8:
                        off += 2
                    elif flags & 0x40:
                        off += 4
                    elif flags & 0x80:
                        off += 8
                    parts.append('%s@%d,%d' % (digest(gi, depth + 1) or '?', a1, a2))
                    if not (flags & 0x20):
                        break
            except Exception:
                memo[gid] = None
                return None
            out = hashlib.sha1(('C' + '|'.join(parts)).encode()).hexdigest()[:16]
        memo[gid] = out
        return out

    return {gid: digest(gid) for gid in blobs}, blank


def doc_hashes(doc):
    """font base name -> {gid: [candidate outline hashes]}, plus blank gids.

    One document embeds the SAME typeface several times — 2022 Ordinary carries
    FIVE cuts of Arabic Typesetting — and `get_texttrace()` reports only the
    base name, so a span cannot say which subset drew it. Taking the first and
    stopping looked glyph ids up in the wrong font: a silent wrong letter,
    which is the one failure this file exists to avoid.

    So every subset is read and each gid keeps ALL the outlines its subsets
    offer. The caller resolves a gid by looking every candidate up in the map
    and accepting only where the candidates agree on the character — 47 gids of
    2022 Ordinary are cut differently in two subsets, and where the two name
    different letters the glyph stays unresolved.
    """
    per_name = collections.defaultdict(list)
    seen = set()
    for pno in range(doc.page_count):
        for info in doc[pno].get_fonts(full=True):
            xref, base = info[0], info[3]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                buf = doc.extract_font(xref)[3]
            except Exception:
                continue
            if buf:
                per_name[base.split('+')[-1]].append(font_hashes(buf))
    merged, blanks = {}, {}
    for name, subsets in per_name.items():
        table = collections.defaultdict(list)
        blank = set()
        drawn = set()
        for sub, sub_blank in subsets:
            for gid, h in sub.items():
                if h is not None and h not in table[gid]:
                    table[gid].append(h)
                drawn.add(gid)
            blank |= sub_blank
        merged[name] = dict(table)
        blanks[name] = blank - drawn
    return merged, blanks


def _is_arabic(ch):
    o = ord(ch)
    return (0x0600 <= o <= 0x06FF or 0x0750 <= o <= 0x077F
            or 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF)


def unnamed(text):
    """True where a glyph's ToUnicode entry says nothing.

    U+FFFD is the honest form of "no entry". The older sittings have a second
    form: Word writes the glyph's own INDEX as the character, so a subset comes
    back as \x01, \x02, \x03 in painting order. Those are not letters, they are
    the absence of one, and letting them count as evidence put a control
    character on 534 outlines that other files name correctly.
    """
    if not text:
        return True
    return all(unicodedata.category(c) in ('Cc', 'Cn', 'Co', 'Cs')
               or c == '\ufffd' for c in text)


def _glyph_runs(chars):
    """(leading glyph id, full character string) for each drawn glyph."""
    out = []
    for uni, gid, _origin, _bbox in chars:
        if gid == -1 and out:
            out[-1] = (out[-1][0], out[-1][1] + chr(uni))
        else:
            out.append((gid, chr(uni)))
    return out


def derive(paths):
    """outline key -> character, learned from every file whose ToUnicode is sane."""
    evidence = collections.defaultdict(collections.Counter)
    unresolved = collections.Counter()
    for path in paths:
        doc = pymupdf.open(path)
        hashes, _blanks = doc_hashes(doc)
        for page in doc:
            for span in page.get_texttrace():
                if span.get('type') != 0:
                    continue
                gh = hashes.get(span['font'])
                if not gh:
                    continue
                # A ligature glyph carries SEVERAL characters — the ones
                # after it have glyph id -1 — and the whole string is what
                # that outline means. Recording only the first character was
                # the same truncation ara_text exists to undo.
                for gid, text in _glyph_runs(span['chars']):
                    cands = gh.get(gid)
                    # Only an UNAMBIGUOUS gid is evidence. Where two subsets of
                    # one name cut the same id differently there is no saying
                    # which drew this glyph, so it teaches nothing.
                    if not cands or len(cands) != 1:
                        continue
                    key = f"{span['font']}|{cands[0]}"
                    if unnamed(text):
                        unresolved[key] += 1
                    elif text.strip():
                        evidence[key][text] += 1
        doc.close()
    table = {}
    conflicts = []
    for key, counter in evidence.items():
        # The sittings before 2016 carry a THIRD kind of junk entry: Word
        # writes the glyph's position in the subset as an ASCII character, so
        # rah comes back as "C" and dal as "F". An outline that any file names
        # with an Arabic letter IS an Arabic letter, so the ASCII readings are
        # dropped before the vote rather than out-voting a real one where the
        # broken files happen to be in the majority.
        arabic = collections.Counter({t: n for t, n in counter.items()
                                      if any(_is_arabic(c) for c in t)})
        pool = arabic or counter
        best, _ = pool.most_common(1)[0]
        if len(pool) > 1:
            conflicts.append((key, dict(pool)))
        table[key] = best
    return table, unresolved, conflicts


def load():
    try:
        with open(OUT) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    paths = sorted(glob.glob(os.path.join(CORPUS, '**', '*.pdf'), recursive=True))
    if not paths:
        print(f'no PDFs under {CORPUS}', file=sys.stderr)
        return 1
    table, unresolved, conflicts = derive(paths)
    known = sum(v for k, v in unresolved.items() if k in table)
    total = sum(unresolved.values())
    print(f'{len(paths)} PDFs, {len(table)} outlines named by their own ToUnicode')
    print(f'{total} glyph draws have no ToUnicode entry; {known} of them '
          f'({100.0 * known / max(1, total):.1f}%) are named by an identical '
          f'outline elsewhere in the corpus')
    print(f'{len(conflicts)} outlines are named differently by two files:')
    for key, counter in conflicts[:20]:
        print('   ', key.split('|')[0], counter)
    still = [(k, v) for k, v in unresolved.items() if k not in table]
    print(f'{sum(v for _, v in still)} draws over {len(still)} outlines stay '
          f'unresolved and are reported, never guessed')
    if args.write:
        with open(OUT, 'w') as fh:
            json.dump(table, fh, ensure_ascii=False, indent=0, sort_keys=True)
        print(f'wrote {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
