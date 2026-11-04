#!/usr/bin/env python3
"""Arabic pages, read so that what comes out is what the SEC printed.

    python3 scripts/markbank/authoring/ara_text.py examiner-reports/arabic/schemes/2023-hl.pdf 3
    python3 scripts/markbank/authoring/ara_text.py --audit examiner-reports/arabic

Why this file exists
--------------------
Arabic is the first right-to-left subject in the bank, and every ordinary
reader in this repo gets it wrong in the same four ways. `ja_text.py` had to
fold ruby runs back before Japanese could be counted; this is the same job for
a script that runs the other way.

A PDF text layer stores glyphs in the order they are PAINTED, which for Arabic
set by Word is visual order — leftmost glyph first. Getting logical order back
is one reversal, and PyMuPDF already does it. The trouble is what the reversal
takes with it.

**1 · A ligature glyph is ONE glyph and several characters.** Arabic Typesetting
draws لد as a single glyph whose ToUnicode entry is the two-character string
"لد". PyMuPDF reverses CHARACTERS, so that glyph comes back as "دل" and the
2023 Higher scheme answers "تقود التقدم في البدل" where the page prints
"تقود التقدم في البلد" — a different word. It is not a rare shape: the same
fault turns باحثاً into ابحثاً, يقوله into يقوهل, الاعتماد into الاعامتد,
المخبز into اخملبز and بالله into ابلله, on the one page. So the reversal has
to be done over GLYPHS, and `page.get_texttrace()` is the only PyMuPDF call
that says where a glyph begins: a character whose glyph id is -1 is a
CONTINUATION of the character before it, never a glyph of its own.

**2 · A number is a left-to-right island inside a right-to-left line.** Reverse
the glyphs of ١٩٠٨ and you get ٨٠٩١, which is how the 2024 Higher paper's dates
read out of every naive extraction. Digits — Arabic-Indic and European alike —
and the separators inside a number are re-reversed after the line is, which is
the Unicode bidi rule for classes AN and EN, applied backwards.

**3 · Latin runs are islands too.** "5 marks", "(Accept any 4)" and
"Communication and Content" sit in the same table as the Arabic and come back
as "skram 5" without the same treatment.

**4 · The shaped forms are not the letters.** The text layer holds Arabic
Presentation Forms — FE97 ARABIC LETTER TEH INITIAL FORM rather than 062A
ARABIC LETTER TEH — because the glyphs were shaped before they were painted.
NFKC folds every one of them back, including the FC.. and FEF.. ligatures, and
is the only normalisation applied: the tatweel (0640) the SEC uses to stretch a
word is dropped, since it is typography and not spelling.

What this file does NOT fix
---------------------------
Some glyphs have no honest ToUnicode entry at all. Word writes a ligature
glyph's entry from whatever codepoint the subset happened to land on, so a
lam-alef comes back as ARMENIAN CAPITAL LETTER DA, a lam-heh as NKO LETTER NYA
WOLOSO and an ain as COMBINING RING ABOVE. Those are counted, never guessed:
`--audit` reports the rate per file and `alien_runs()` names the words they
damage. See ARABIC.md for the corpus-wide measurement and what it decided.
"""
import argparse
import collections
import glob
import os
import re
import sys
import unicodedata

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

# Arabic proper, the supplement, and the two Presentation Forms blocks the
# shaper emits. Anything else non-ASCII inside an Arabic line is a glyph whose
# ToUnicode entry is wrong — see alien_runs().
ARABIC_RANGES = ((0x0600, 0x06FF), (0x0750, 0x077F),
                 (0xFB50, 0xFDFF), (0xFE70, 0xFEFF))
# The kashida. Printed to stretch a word to the measure; not part of the word.
TATWEEL = 'ـ'
# Letters the SEC's fonts reach for that are not the Arabic ones. Word's shaper
# hands back the PERSIAN yeh (U+06CC ی) for ي, the keheh (U+06A9 ک) for ك and
# the heh doachashmee (U+06BE ھ) for ه, all of which print identically in this
# type and none of which is a letter of Arabic. Folded, so a search for
# "الصحيحة" finds the 2021 papers too — it did not, and Part 1 of both 2021
# sittings went uncounted for it. The alef maksura ى is NOT folded: that one is
# a real Arabic letter and a different word from one ending in ي.
FOREIGN_FORMS = str.maketrans({'ی': 'ي', 'ک': 'ك', 'ھ': 'ه', 'ے': 'ي'})
# Digits that read left to right inside a right-to-left line: European,
# Arabic-Indic (٠١٢٣…) and Extended Arabic-Indic (۰۱۲۳…).
DIGITS = set('0123456789') | {chr(c) for c in range(0x0660, 0x066A)} \
    | {chr(c) for c in range(0x06F0, 0x06FA)}
# Characters that stay inside a number run rather than ending it. The bidi
# algorithm calls these CS — comma, full stop, colon, solidus and the Arabic
# separators — and they bind digits on BOTH sides into one left-to-right run.
# A HYPHEN does not: it is class ES, which binds European digits only, so the
# Arabic-Indic range "١-٤" is two runs with a neutral between them and the SEC
# prints it that way. Gluing on the hyphen turned "من ١-٤" into "من ٤-١" on
# every Higher comprehension head, and "١٩٠٨-١٩٢١" is still right without it
# because each year re-reverses on its own.
NUMBER_GLUE = set('.,:/%٫٬')
# Two printed columns are never a word-space apart; a real word-space in this
# type is under a third of the point size. Measured on the scheme tables, whose
# narrowest cell gap is nine points at 22pt type.
COLUMN_GAP_PT = 9.0


def is_arabic(ch):
    o = ord(ch)
    return any(lo <= o <= hi for lo, hi in ARABIC_RANGES)


def is_ltr_island(ch):
    """True for a character that keeps its own left-to-right order in an RTL line."""
    return ch in DIGITS or ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')


_GLYPHMAP = None
_HASH_CACHE = {}


def _glyphmap():
    global _GLYPHMAP
    if _GLYPHMAP is None:
        import ara_glyphs
        _GLYPHMAP = ara_glyphs.load()
    return _GLYPHMAP


def _outline_hashes(doc):
    """Per-document {font: {gid: outline hash}}, computed once.

    The cache holds the document itself alongside its hashes. Keying on id()
    alone is not safe: CPython reuses the id of a collected object, so a
    document opened after another was closed can inherit the previous one's
    glyph map — which is a wrong LETTER, silently, on whichever page reads
    next. Holding the reference keeps the id alive for as long as the entry is.
    """
    key = id(doc)
    hit = _HASH_CACHE.get(key)
    if hit is not None and hit[0] is doc:
        return hit[1]
    import ara_glyphs
    if len(_HASH_CACHE) > 8:
        _HASH_CACHE.clear()
    _HASH_CACHE[key] = (doc, ara_glyphs.doc_hashes(doc))
    return _HASH_CACHE[key][1]      # (hashes, blanks)


def _glyphs(span, hashes=None):
    """Split a texttrace span's characters into GLYPHS, in painting order.

    A character whose glyph id is -1 is the second (or third) character of the
    glyph before it — the ToUnicode entry for a ligature. It must travel with
    that glyph through the reversal, or the letters inside the ligature come
    out backwards. This is the whole reason ara_text exists.

    A glyph the font's ToUnicode does not name at all arrives as U+FFFD. Where
    the same OUTLINE is named by another file in the corpus, ara_glyphs supplies
    that name; where it is not, the U+FFFD stands, so the word is reported
    damaged rather than quietly given a letter it does not have.
    """
    import ara_glyphs
    out = []
    gh = (hashes[0] if hashes else {}).get(span['font']) or {}
    blank = (hashes[1] if hashes else {}).get(span['font']) or set()
    table = _glyphmap()
    for uni, gid, origin, bbox in span['chars']:
        ch = chr(uni)
        if gid == -1 and out:
            out[-1] = (out[-1][0] + ch, out[-1][1], out[-1][2])
            continue
        if ara_glyphs.unnamed(ch):
            # A glyph with no outline paints nothing, so it is a space, not a
            # letter the reader failed to read.
            if gid in blank:
                ch = ' '
            else:
                named = {table.get(f"{span['font']}|{h}")
                         for h in gh.get(gid, ())}
                named.discard(None)
                ch = named.pop() if len(named) == 1 else '\ufffd'
        out.append((ch, bbox, origin))
    return out


def _unreverse_islands(text):
    """Put the left-to-right runs of an already-reversed line back the right way.

    After the glyph list of an RTL line is reversed, its Arabic reads correctly
    and everything that is not Arabic reads backwards: ١٩٠٨ became ٨٠٩١ and
    "marks" became "skram". Both are bidi classes that the algorithm lays out
    left to right regardless of the paragraph direction, so both are reversed
    again here — a digit run together with the separators printed inside it,
    and a Latin run together with the spaces printed inside it.
    """
    out = []
    i = 0
    n = len(text)
    while i < n:
        if is_ltr_island(text[i]):
            j = i
            while j < n and (is_ltr_island(text[j])
                             or (text[j] in NUMBER_GLUE | {' '}
                                 and j + 1 < n and is_ltr_island(text[j + 1]))):
                j += 1
            out.append(text[i:j][::-1])
            i = j
        else:
            out.append(text[i])
            i += 1
    return ''.join(out)


def _mirror_brackets(text):
    """Undo the bidi mirroring Word baked into the character, not the glyph.

    A parenthesis printed at the RIGHT-hand (opening) end of an Arabic clause
    is stored by Word as U+0029, the closing one, because that is the shape a
    reader sees there. Recovered into logical order it opens the clause with
    ")". The source is not consistent about it — the same 2021 Higher line
    prints "(أ) رأينا …" one way and ")جملة في محل نصب(" the other — so the
    brackets are read by DEPTH rather than by their codepoint: whichever
    bracket stands where an opener belongs is the opener.
    """
    out, depth = [], 0
    for ch in text:
        if ch in '()':
            if depth == 0:
                out.append('(')
                depth += 1
            else:
                out.append(')')
                depth -= 1
        else:
            out.append(ch)
    return ''.join(out)


# A hamza the shaper drew as its own glyph, on a letter that already carries
# one. Word gives the base letter its real codepoint AND the mark, so أ comes
# back as "أٔ" — a doubled hamza, which is not how the word is spelled. On a
# BARE carrier the mark is the spelling and is composed onto it instead.
HAMZA_ON = {'ا': 'أ', 'و': 'ؤ', 'ي': 'ئ', 'ى': 'ئ'}
HAMZA_BELOW_ON = {'ا': 'إ'}
CARRIES_HAMZA = 'أإآؤئ'


def _fold_hamza(text):
    out = []
    for ch in text:
        if ch == '\u0654' and out:
            if out[-1] in CARRIES_HAMZA:
                continue
            if out[-1] in HAMZA_ON:
                out[-1] = HAMZA_ON[out[-1]]
                continue
        if ch == '\u0655' and out:
            if out[-1] in CARRIES_HAMZA:
                continue
            if out[-1] in HAMZA_BELOW_ON:
                out[-1] = HAMZA_BELOW_ON[out[-1]]
                continue
        out.append(ch)
    return ''.join(out)


def _normalise(text):
    """Fold the shaped forms back to letters and drop the kashida."""
    text = unicodedata.normalize('NFKC', text)
    text = text.replace(TATWEEL, '').translate(FOREIGN_FORMS)
    # A part label typed as ")ج(" is the same label as "(ج)"; the SEC's own
    # source is inconsistent between the two and the brackets carry no meaning
    # beyond marking the label. Normalise the pair, never the contents.
    text = re.sub(r'\)\s*([؀-ۿ])\s*\(', r'(\1)', text)
    text = _mirror_brackets(text)
    # NFKC unshapes the presentation forms but leaves a hamza sitting as its
    # own combining mark — أ comes back as ا + U+0654, which reads "أٔ". NFC
    # puts it back on its letter, which is how the SEC spells the word.
    text = unicodedata.normalize('NFC', text)
    text = _fold_hamza(text)
    return re.sub(r'[ \t]+', ' ', text).strip()


def span_text(span, hashes=None):
    """One texttrace span, in logical order."""
    glyphs = _glyphs(span, hashes)
    rtl = bool(span.get('bidi_lvl', 0) % 2) or any(
        is_arabic(c) for g in glyphs for c in g[0])
    if rtl:
        glyphs = list(reversed(glyphs))
    text = ''.join(g[0] for g in glyphs)
    if rtl:
        text = _unreverse_islands(text)
    return text


def page_lines(page):
    """Every line of a page, in logical order, with its display bbox.

    Returns dicts: {'text', 'bbox' (x0, y0, x1, y1 in display space), 'rtl',
    'size'}.

    A line is built from GLYPHS, not from spans. A texttrace span groups by
    style and not by position: on 2025 Higher page 4 one span holds both
    "بالمشي" at x=265 and "ترشيد" at x=523, because Word justifies the measure
    by widening the advances inside a single run. Reading that span as a unit
    put the first two words of the paragraph into the middle of the line —
    every letter right, the sentence wrong — which is the same class of fault
    as reading the ligature backwards, and just as invisible. So each glyph is
    placed by its own origin, the line is assembled right to left across the
    whole measure, and a word space is whatever gap the type itself calls one.
    """
    mat = page.rotation_matrix
    hashes = _outline_hashes(page.parent)
    rows = collections.defaultdict(list)
    for span in page.get_texttrace():
        if span.get('type') != 0 or not span['chars']:
            continue
        size = span.get('size', 0) or 0
        space = span.get('spacewidth') or size * 0.25
        placed, pending = [], ''
        for text, bbox, origin in _glyphs(span, hashes):
            if not text.strip():
                continue
            # A vowel sign, a shadda or a tanween is drawn as its own glyph
            # with its own origin, and that origin can sit anywhere near the
            # letter it belongs to. Sorting it by its own x printed "تح ّدي"
            # for "تحدّي" and "باحثا عًن" for "باحثاً عن". In a run painted
            # left to right the mark is laid down BEFORE the letter it sits
            # on, so it waits for that letter and is then written after it,
            # which is the order Unicode combining marks require anyway.
            if all(unicodedata.category(c) == 'Mn' for c in text):
                pending += text
                continue
            r = pymupdf.Rect(bbox) * mat
            base = pymupdf.Point(origin) * mat
            placed.append({'text': text + pending, 'rect': r, 'size': size,
                           'space': space, 'base': base.y})
            pending = ''
        if pending and placed:
            placed[-1]['text'] += pending
        # Keyed on the BASELINE, not on the ink — and on the SPAN's baseline
        # where a glyph's own is only slightly off it. Arabic Typesetting sets
        # the لمج of المجتمع three points above the line it belongs to, on its
        # own text-matrix origin, so both the ink test and the raw baseline put
        # that one ligature on a line of its own: "ا تمع" on one line and
        # "لمج" on the next, which is not a word the SEC printed. A run of type
        # is one printed line unless it is displaced by a good part of its own
        # body size, which is what a real line break looks like.
        if placed:
            bases = sorted(g['base'] for g in placed)
            median = bases[len(bases) // 2]
            tol = max(0.35 * (size or 10), 1.0)
            for g in placed:
                key = median if abs(g['base'] - median) < tol else g['base']
                rows[round(key, 0)].append(g)
    ys = sorted(rows)
    merged = []
    for y in ys:
        # Baselines within two points are one printed line: the SEC's Arabic
        # and its Latin gloss sit on slightly different baselines in the same
        # row of the same table.
        if merged and y - merged[-1][0] <= 2.0:
            merged[-1][1].extend(rows[y])
        else:
            merged.append((y, list(rows[y])))
    lines = []
    for _y, glyphs in merged:
        rtl = any(is_arabic(c) for g in glyphs for c in g['text'])
        glyphs.sort(key=lambda g: g['rect'].x0, reverse=rtl)
        parts = []
        prev = None
        for g in glyphs:
            if prev is not None:
                gap = (prev['rect'].x0 - g['rect'].x1) if rtl \
                    else (g['rect'].x0 - prev['rect'].x1)
                if gap > COLUMN_GAP_PT:
                    parts.append('  ')
                elif gap > max(0.4 * prev['space'], 0.6):
                    parts.append(' ')
            parts.append(g['text'])
            prev = g
        text = ''.join(parts)
        if rtl:
            text = _unreverse_islands(text)
        text = _normalise(text)
        if not text:
            continue
        x0 = min(g['rect'].x0 for g in glyphs)
        x1 = max(g['rect'].x1 for g in glyphs)
        y0 = min(g['rect'].y0 for g in glyphs)
        y1 = max(g['rect'].y1 for g in glyphs)
        lines.append({'text': text, 'bbox': (x0, y0, x1, y1), 'rtl': rtl,
                      'size': max(g['size'] for g in glyphs)})
    return lines


def page_text(page):
    return '\n'.join(l['text'] for l in page_lines(page))


def doc_text(path):
    doc = pymupdf.open(path)
    try:
        return [page_text(p) for p in doc]
    finally:
        doc.close()


# ------------------------------------------------------------------ audit ----

def alien_runs(text):
    """Words damaged by a glyph whose ToUnicode entry is not Arabic.

    Returns (word, alien characters) for every whitespace-delimited word that
    mixes Arabic with a codepoint that is neither Arabic nor ASCII. These are
    ligature glyphs Word mis-tagged; the letters around them are sound, so the
    word is reported whole and never patched.
    """
    bad = []
    for word in text.split():
        if not any(is_arabic(c) for c in word):
            continue
        aliens = [c for c in word
                  if not is_arabic(c) and not c.isascii() and not c.isspace()
                  and unicodedata.category(c) not in ('Zs',)
                  and c not in '–—‘’“”•… ']
        if aliens:
            bad.append((word, aliens))
    return bad


def audit(paths):
    total_ar = total_alien = total_words = total_badwords = 0
    rows = []
    for path in paths:
        doc = pymupdf.open(path)
        ar = alien = words = badwords = 0
        seen = collections.Counter()
        for page in doc:
            text = page_text(page)
            for word in text.split():
                if not any(is_arabic(c) for c in word):
                    continue
                words += 1
            for w, a in alien_runs(text):
                badwords += 1
                for c in a:
                    seen[c] += 1
                    alien += 1
            ar += sum(1 for c in text if is_arabic(c))
        doc.close()
        rows.append((path, ar, alien, words, badwords, len(seen)))
        total_ar += ar; total_alien += alien
        total_words += words; total_badwords += badwords
    w = max(len(os.path.basename(r[0])) for r in rows)
    print(f'{"file":<{w}}  {"ar chars":>8} {"alien":>6} {"words":>6} '
          f'{"bad words":>9} {"rate":>7} {"distinct":>8}')
    for path, ar, alien, words, bad, distinct in rows:
        rate = 100.0 * bad / max(1, words)
        print(f'{os.path.basename(path):<{w}}  {ar:>8} {alien:>6} {words:>6} '
              f'{bad:>9} {rate:>6.1f}% {distinct:>8}')
    print(f'\n{total_badwords} of {total_words} Arabic words carry a glyph with no '
          f'Arabic ToUnicode entry ({100.0*total_badwords/max(1,total_words):.1f}%)')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('page', nargs='?', type=int)
    ap.add_argument('--audit', action='store_true',
                    help='report the alien-glyph rate for every PDF under PATH')
    args = ap.parse_args()
    if args.audit:
        paths = sorted(glob.glob(os.path.join(args.path, '**', '*.pdf'),
                                 recursive=True))
        return audit(paths)
    doc = pymupdf.open(args.path)
    pages = [args.page - 1] if args.page else range(doc.page_count)
    for pno in pages:
        print(f'===== page {pno + 1}')
        print(page_text(doc[pno]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
