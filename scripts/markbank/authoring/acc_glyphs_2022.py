#!/usr/bin/env python3
"""Derive the glyph repair map for the 2022 LC Accounting marking schemes.

The 2022 schemes embed Type0 / Identity-H TrueType subsets with no ToUnicode
CMap (and no cmap or post table inside the subset), so PyMuPDF emits each
glyph id as the code point. Step 0 proves that against page.get_texttrace().

Evidence sources (no seed map, nothing hand-typed into the map):
  vocab   - a cipher word whose length + repetition pattern fits reference
            words that all agree on an unknown glyph (reference = the other
            years' schemes: examiner-reports/accounting/schemes/*.md
            2010-2026 minus 2022, plus the 2021 and 2023 PDFs). Bare numbers
            are never evidence (any digit map makes valid numbers); case is
            checked against the subset's glyph heights (x-height vs cap).
  page    - the centred footer token on PDF page n reads n (names digits).
  shape   - stage 2: digits folded to one symbol, so "(#,###–#,###)" can
            name a glyph inside a number.
  context - stage 2: the neighbouring repaired word(s) must form a reference
            bigram/trigram, and one neighbour must contain letters (between
            two bare numbers x, @, +, = all fit: that once misread @ as x).
Dash variants (- ‐ – —) are one class in the reference (years differ); a
glyph is allowed in it only if its outline is a single flat bar, and its
advance width then names hyphen / en dash / em dash.
A pair glyph->char is accepted only with >= 2 independent pieces of evidence
(distinct reference spellings / pages / phrases) and more than three times
the support of the strongest rival reading. Iterate to a fixed point, then
GATE: recompute evidence with the final map (whole words only) and push
anything below 2 into the residue. VISUAL_READINGS (read off the crops) are
reported beside the residue and never merged into the map.

Times New Roman / Arial subsets are cross-checked against the macOS copies of
those fonts: a glyph id is accepted from the local cmap only when its advance and
decoded outline (every point) are identical in the subset and the local font.

Never read these PDFs with get_text("words"): it treats every code point
below U+0020 as whitespace and deletes Calibri's A B C D E (gids 4 17 18 24
28) and Times New Roman's digits and comma.

Run: python3 acc_glyph_2022.py [WORKTREE]
"""
import collections
import glob
import json
import os
import re
import struct
import sys
import unicodedata

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
WT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "small")
CORPUS = os.path.realpath(os.path.join(WT, "paper-trail-corpus"))
PDFS = {
    "HL": os.path.join(CORPUS, "markingschemes/2022/LC032ALP000EV.pdf"),
    "OL": os.path.join(CORPUS, "markingschemes/2022/LC032GLP000EV.pdf"),
}
REF_PDFS = [os.path.join(CORPUS, f"markingschemes/{y}/LC032{l}LP000EV.pdf")
            for y in (2021, 2023) for l in "AG"]
REF_MD = sorted(f for f in glob.glob(os.path.join(WT, "examiner-reports/accounting/schemes/*.md"))
                if not os.path.basename(f).startswith("2022"))
LOCAL_FONTS = {  # (family, bold) -> macOS copy, used only for byte-identical glyf checks
    ("TimesNewRoman", False): "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    ("TimesNewRoman", True): "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    ("Arial", False): "/System/Library/Fonts/Supplemental/Arial.ttf",
    ("Arial", True): "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
}
# Read off the rendered crops (acc-glyph-2022-crops/*.png) on 2026-10-27 for
# glyphs the word gate leaves open. Reported beside the residue so a reader
# can see what each one is; NEVER merged into "map".
VISUAL_READINGS = {
    ("Calibri", 0x043D): "+", ("Calibri", 0x039B): "@", ("Calibri", 0x038E): "*",
    ("Calibri", 0x0440): "\u00f7", ("Calibri", 0x0079): "X", ("Calibri", 0x042A): "\u00bd",
    ("Calibri", 0x0396): "'", ("Calibri", 0x0382): "{", ("Calibri", 0x0383): "}",
    ("Calibri", 0x007A): "Y", ("Calibri", 0x0376): "\u2014", ("Calibri", 0x034D): "?",
    ("Calibri", 0x043F): "\u00d7", ("Calibri", 0x0356): ";",
    # cover line "State Examinations Commission" (one line, printed in both PDFs)
    ("Cambria", 0x0016): "S", ("Cambria", 0x0096): "t", ("Cambria", 0x0083): "a",
    ("Cambria", 0x0087): "e", ("Cambria", 0x0008): "E", ("Cambria", 0x009A): "x",
    ("Cambria", 0x008F): "m", ("Cambria", 0x008B): "i", ("Cambria", 0x0090): "n",
    ("Cambria", 0x0091): "o", ("Cambria", 0x0095): "s", ("Cambria", 0x0006): "C",
}
OUT_JSON = os.path.join(HERE, "acc-glyph-2022.json")
CROPS = os.path.join(HERE, "acc-glyph-2022-crops")
SPACE_GID = 3
MIN_EV = 2
DIGITS = "0123456789"


def family(font):
    return font.split(",")[0]


def u(cp):
    return "U+%04X" % cp


def show(syms):
    return "".join(chr(s[1]) if s[0] != "plain" else s[1] for s in syms)


# ------------------------------------------------------------ TrueType bits
def tt_tables(buf):
    n = struct.unpack(">H", buf[4:6])[0]
    t = {}
    for i in range(n):
        tag, _cs, off, ln = struct.unpack(">4sIII", buf[12 + 16 * i:28 + 16 * i])
        t[tag.decode("latin-1")] = buf[off:off + ln]
    return t


def tt_glyphs(buf):
    """gid -> (advance, glyf bytes)."""
    t = tt_tables(buf)
    long_loca = struct.unpack(">h", t["head"][50:52])[0] == 1
    n = struct.unpack(">H", t["maxp"][4:6])[0]
    nh = struct.unpack(">H", t["hhea"][34:36])[0]
    loca = t["loca"]
    if long_loca:
        offs = struct.unpack(">%dI" % (n + 1), loca[:4 * (n + 1)])
    else:
        offs = [2 * x for x in struct.unpack(">%dH" % (n + 1), loca[:2 * (n + 1)])]
    adv = [struct.unpack(">H", t["hmtx"][4 * min(g, nh - 1):4 * min(g, nh - 1) + 2])[0] for g in range(n)]
    return {g: (adv[g], t["glyf"][offs[g]:offs[g + 1]]) for g in range(n)}


def tt_metrics(buf):
    t = tt_tables(buf)
    upm = struct.unpack(">H", t["head"][18:20])[0]
    os2 = t["OS/2"]
    ver = struct.unpack(">H", os2[0:2])[0]
    xh, cap = struct.unpack(">hh", os2[86:90]) if ver >= 2 else (None, None)
    return upm, xh, cap


def outline(rec):
    """Decoded outline of a simple glyph: bbox, contour ends, (x, y, on-curve)
    points. Hinting and the byte packing of flags/coordinates are ignored."""
    if len(rec) < 10:
        return rec
    n = struct.unpack(">h", rec[0:2])[0]
    if n < 0:
        return rec
    ends = struct.unpack(">%dH" % n, rec[10:10 + 2 * n])
    p = 10 + 2 * n
    p += 2 + struct.unpack(">H", rec[p:p + 2])[0]
    npts = ends[-1] + 1 if ends else 0
    flags = []
    while len(flags) < npts:
        f = rec[p]; p += 1
        flags.append(f)
        if f & 8:
            flags += [f] * rec[p]; p += 1
    coords = []
    for short, same in ((2, 16), (4, 32)):
        v, vals = 0, []
        for f in flags:
            if f & short:
                d = rec[p]; p += 1
                v += d if f & same else -d
            elif not f & same:
                v += struct.unpack(">h", rec[p:p + 2])[0]; p += 2
            vals.append(v)
        coords.append(vals)
    return (rec[:10], ends, tuple(zip(coords[0], coords[1], (f & 1 for f in flags))))


def family_metrics(docs, aff_by_pdf):
    """family -> {gid: (advance/upm, height class)} from the embedded subsets."""
    out = {}
    for tag, doc in docs.items():
        for name, (base, xref) in sorted(aff_by_pdf[tag].items()):
            fam = family(name)
            buf = doc.extract_font(xref)[3]
            upm, xh, cap = tt_metrics(buf)
            d = out.setdefault(fam, {})
            for g, (adv, rec) in tt_glyphs(buf).items():
                if g in d or (len(rec) < 10 and g != SPACE_GID):
                    continue
                cls = None
                if rec and xh and cap:
                    ymax = struct.unpack(">h", rec[8:10])[0]
                    half = (cap - xh) / 2
                    cls = "x" if abs(ymax - xh) < half else "cap" if abs(ymax - cap) < half else None
                d[g] = (adv / upm, cls)
                if len(rec) >= 10:
                    n, x0, y0, x1, y1 = struct.unpack(">5h", rec[:10])
                    if n == 1 and y1 - y0 < 0.12 * upm and x1 - x0 > 2 * (y1 - y0):
                        FLAT.add((fam, g))
    return out


# ------------------------------------------------------------ fonts
def affected_fonts(doc):
    out = {}
    for pno in range(len(doc)):
        for xref, _ext, ftype, base, _n, enc in doc.get_page_fonts(pno):
            if ftype == "Type0" and enc == "Identity-H" and \
                    doc.xref_get_key(xref, "ToUnicode")[0] == "null":
                out[base.split("+", 1)[-1]] = (base, xref)
    return out


def verify_cp_is_gid(doc, aff):
    same = diff = 0
    notes = []
    for pno, page in enumerate(doc):
        a = collections.defaultdict(collections.Counter)
        b = collections.defaultdict(collections.Counter)
        for s in page.get_texttrace():
            if s["font"] in aff:
                for c in s["chars"]:
                    a[s["font"]][c[1]] += 1
        for bl in page.get_text("rawdict")["blocks"]:
            for ln in bl.get("lines", []):
                for s in ln["spans"]:
                    if s["font"] in aff:
                        for c in s["chars"]:
                            if c["c"] != " ":
                                b[s["font"]][ord(c["c"])] += 1
        for f in set(a) | set(b):
            n = sum(a[f].values())
            d = sum(abs(a[f][k] - b[f][k]) for k in set(a[f]) | set(b[f]))
            same += n - d
            diff += d
            if d:
                notes.append(f"p{pno + 1} {f}: {d} glyph(s) differ (space glyphs MuPDF merged)")
    return {"glyphs_matched": same, "glyphs_differing": diff, "notes": notes}


# ------------------------------------------------------------ cipher text
SEP = None


def cipher_lines(doc, aff, tag):
    lines = []
    for pno, page in enumerate(doc):
        W, H = page.rect.width, page.rect.height
        for bl in page.get_text("rawdict")["blocks"]:
            for ln in bl.get("lines", []):
                syms, styles, boxes = [], [], []
                for s in ln["spans"]:
                    hit = s["font"] in aff
                    for c in s["chars"]:
                        ch = c["c"]
                        if hit and ch != " ":
                            syms.append((family(s["font"]), ord(ch)))
                            styles.append(s["font"])
                        elif ch.isspace():
                            syms.append(SEP); styles.append(None)
                        else:
                            syms.append(("plain", ch)); styles.append(None)
                        boxes.append(c["bbox"])
                lines.append({"pdf": tag, "page": pno + 1, "x": ln["bbox"][0] / W,
                              "y": ln["bbox"][1] / H, "syms": syms, "styles": styles,
                              "boxes": boxes})
    return lines


def is_sep(sym):
    return sym is SEP or (sym[0] != "plain" and sym[1] == SPACE_GID)


def tokens_of(line):
    toks, cur, curst = [], [], []
    for sym, sty in zip(line["syms"], line["styles"]):
        if is_sep(sym):
            if cur:
                toks.append((tuple(cur), tuple(curst)))
            cur, curst = [], []
        else:
            cur.append(sym); curst.append(sty)
    if cur:
        toks.append((tuple(cur), tuple(curst)))
    return toks


def pattern(seq):
    first = {}
    return tuple(first.setdefault(x, i) for i, x in enumerate(seq))


DIG = "\ue000"            # folded digit (the reference also prints a literal '#')
DASHES = "-\u2010\u2011\u2012\u2013\u2014\u2212"
DQUOTES = "\"\u201c\u201d"
CLASS_CHARS = {"-", '"'}  # word evidence names the class; glyph width picks the member
FLAT = set()              # (family, gid) whose outline is one flat bar (filled in main)


def fold(word):
    return re.sub(r"[0-9]", DIG, word)


def fold_classes(word):
    return word.translate({ord(c): "-" for c in DASHES} | {ord(c): '"' for c in DQUOTES})


def numeric(word):
    return any(c.isdigit() for c in word) and not any(c.isalpha() for c in word)


# ------------------------------------------------------------ reference
def reference():
    texts = [open(f, encoding="utf-8").read() for f in REF_MD]
    for f in REF_PDFS:
        if os.path.exists(f):
            texts.append("\n".join(p.get_text() for p in fitz.open(f)))
    toks, bigrams, trigrams = collections.Counter(), collections.Counter(), collections.Counter()
    for t in texts:
        for line in t.splitlines():
            ws = [fold_classes(w) for w in line.split()]
            toks.update(ws)
            bigrams.update(zip(ws, ws[1:]))
            trigrams.update(zip(ws, ws[1:], ws[2:]))
    return toks, bigrams, trigrams


def alpha_word(tok):
    w = tok.strip(".,:;()[]{}'\"!?*-–—/&%€£$+=<>’‘“”")
    return w if len(w) >= 2 and w.isalpha() else None


# ------------------------------------------------------------ solver
def consistent(syms, word, M, inv):
    local, linv = {}, {}
    for s, ch in zip(syms, word):
        if s[0] == "plain":
            if s[1] != ch:
                return False
            continue
        m = M.get(s)
        if m is not None:
            if m != ch:
                return False
            continue
        if ch == "-" and s not in FLAT:       # the dash class needs a flat bar glyph
            return False
        o = inv.get((s[0], ch))
        if o is not None and o != s and ch not in CLASS_CHARS:
            return False
        if local.setdefault(s, ch) != ch:
            return False
        if ch not in CLASS_CHARS and linv.setdefault((s[0], ch), s) != s:
            return False
    return True


def folded_syms(syms, M):
    return tuple(("plain", DIG) if s[0] != "plain" and M.get(s, "x") in DIGITS
                 else ("plain", DIG) if s[0] == "plain" and s[1] in DIGITS else s
                 for s in syms)


class Corpus:
    def __init__(self, lines, ref, ref_bi, ref_tri, heights):
        self.lines = lines
        self.ref, self.ref_bi, self.ref_tri = ref, ref_bi, ref_tri
        self.heights = heights          # family -> gid -> "x" | "cap" | None
        self.ref_fold = collections.Counter()
        for w, n in ref.items():
            self.ref_fold[fold(w)] += n
        self.bi_fold = {(fold(a), fold(b)) for a, b in ref_bi}
        self.tri_fold = {(fold(a), fold(b), fold(c)) for a, b, c in ref_tri}
        self.index = collections.defaultdict(list)
        for w in ref:
            if not numeric(w):          # a number matches any digit map: no evidence
                self.index[(len(w), pattern(w))].append(w)
        self.index_fold = collections.defaultdict(list)
        for w in self.ref_fold:
            self.index_fold[(len(w), pattern(w))].append(w)
        self.ctoks = collections.Counter()
        self.ctx = []                 # (prev, tok, next) occurrences
        self.pagetoks = []            # (pdf, page, syms)
        for ln in lines:
            toks = [t for t, _ in tokens_of(ln)]
            for i, t in enumerate(toks):
                if any(s[0] != "plain" for s in t):
                    self.ctoks[t] += 1
                    self.ctx.append((toks[i - 1] if i else None, t,
                                     toks[i + 1] if i + 1 < len(toks) else None))
            if 0.86 < ln["y"] < 0.95 and 0.4 < ln["x"] < 0.6 and len(toks) == 1 \
                    and 1 <= len(toks[0]) <= 2 and all(s[0] != "plain" for s in toks[0]):
                self.pagetoks.append((ln["pdf"], ln["page"], toks[0]))

    def case_filter(self, syms, cands):
        """Keep candidates whose letter case agrees with the glyph heights in
        the subset (an x-height letter must not sit on a cap-height glyph)."""
        if len(cands) < 2:
            return cands
        keep = []
        for w in cands:
            bad = 0
            for s, ch in zip(syms, w):
                if s[0] == "plain":
                    continue
                h = self.heights.get(s[0], {}).get(s[1])
                want = "cap" if ch.isupper() else "x" if ch in "acemnorsuvwxz" else None
                if h and want and h != want:
                    bad += 1
            if not bad:
                keep.append(w)
        return keep

    # each unit: (syms, candidates, kind, label); a proposal needs all candidates to agree
    def units(self, M, inv, stage):
        def known(t):
            return t is not None and all(s[0] == "plain" or s in M for s in t)

        def number_like(t):
            got = [M[s] if s[0] != "plain" else s[1] for s in t if s[0] == "plain" or s in M]
            return any(c in DIGITS for c in got) and not any(c.isalpha() for c in got)
        for t in self.ctoks:
            if known(t):
                continue
            if not number_like(t):
                pool = self.index.get((len(t), pattern(t)), ())
                yield t, self.case_filter(t, [w for w in pool if consistent(t, w, M, inv)]), "vocab", None
            if stage < 2:
                continue
            ft = folded_syms(t, M)
            pool = self.index_fold.get((len(ft), pattern(ft)), ())
            if ft != t or any(numeric(w) for w in pool[:1]):
                yield ft, [w for w in pool if consistent(ft, w, M, inv)], "shape", show_fold(ft, M)
        for prev, t, nxt in self.ctx if stage >= 2 else ():
            if known(t):
                continue
            a = repair(prev, M) if known(prev) else None
            b = repair(nxt, M) if known(nxt) else None
            if a is None and b is None:
                continue
            ft = folded_syms(t, M)
            pool = self.index_fold.get((len(ft), pattern(ft)), ())
            cands = []
            for w in pool:
                if not consistent(ft, w, M, inv):
                    continue
                if not any(c.isalpha() for c in (a or "") + (b or "")):
                    break                       # numbers either side: x, @, +, = all fit
                if a is not None and b is not None:
                    ok = (fold(a), w, fold(b)) in self.tri_fold
                elif a is not None:
                    ok = (fold(a), w) in self.bi_fold
                else:
                    ok = (w, fold(b)) in self.bi_fold
                if ok:
                    cands.append(w)
            yield ft, cands, "context", f"{a or '^'} _ {b or '$'}"
        best = self.page_offset(M, inv)
        if best is not None:
            for pdf, page, t in self.pagetoks:
                lab = str(page + best[pdf])
                yield t, [lab] if len(lab) == len(t) and consistent(t, lab, M, inv) else [], \
                    "page", f"{pdf} p{page}"

    def page_offset(self, M, inv):
        """Printed number = PDF page + k; only if exactly one k fits every footer."""
        out = {}
        for pdf in ("HL", "OL"):
            toks = [(p, t) for d, p, t in self.pagetoks if d == pdf]
            fits = []
            for k in range(-4, 5):
                ok = sum(1 for p, t in toks if len(str(p + k)) == len(t)
                         and consistent(t, str(p + k), M, inv))
                fits.append((ok, k))
            fits.sort(reverse=True)
            if not toks or fits[0][0] != len(toks) or fits[1][0] == len(toks):
                return None
            out[pdf] = fits[0][1]
        return out


def show_fold(ft, M):
    return "".join(s[1] if s[0] == "plain" else M.get(s, "?") for s in ft)


def repair(syms, M, unknown="⟨%04X⟩"):
    if syms is None:
        return None
    out = []
    for s in syms:
        if is_sep(s):
            out.append(" ")
        elif s[0] == "plain":
            out.append(s[1])
        else:
            out.append(M.get(s, unknown % s[1]))
    return "".join(out)


def proposals(C, M, inv, stage=2, cap=400):
    prop = collections.defaultdict(lambda: collections.defaultdict(set))
    for syms, cands, kind, label in C.units(M, inv, stage):
        if not cands or len(cands) > cap:
            continue
        for i, s in enumerate(syms):
            if s[0] == "plain" or s in M:
                continue
            chars = {w[i] for w in cands}
            if len(chars) != 1 or DIG in chars:
                continue
            ch = chars.pop()
            word = "|".join(sorted(cands)[:3])
            key = (kind, label or "", word.lower()) if kind in ("context", "page") else (kind, "", word.lower())
            prop[s][ch].add((key, show(syms), word, kind))
    return prop


def solve(C):
    """Stage 1: words + page footers (letters, punctuation, digits).
    Stage 2: adds digit-folded shapes and phrase context, once every digit
    glyph is named, so a glyph inside a number can no longer pose as a digit."""
    M, inv, rounds, log = {}, {}, 0, []
    stage = 1
    while True:
        rounds += 1
        prop = proposals(C, M, inv, stage)
        ranked = []
        for s, by in prop.items():
            for ch, ev in by.items():
                indep = len({e[0] for e in ev})
                against = max([len({e[0] for e in e2}) for c2, e2 in by.items() if c2 != ch] or [0])
                ranked.append((indep, against, s, ch))
        ranked.sort(key=lambda r: -r[0])
        took = 0
        for indep, against, s, ch in ranked:
            if indep < MIN_EV or against * 3 >= indep or s in M:
                continue
            if (s[0], ch) in inv and ch not in CLASS_CHARS:
                continue
            M[s] = ch
            inv.setdefault((s[0], ch), s)
            took += 1
            log.append((rounds, stage, u(s[1]), s[0], ch, indep, against))
        if not took:
            if stage == 2:
                return M, inv, rounds, log
            stage = 2


# ------------------------------------------------------------ final evidence
def final_evidence(C, M):
    """Recompute evidence with the final map. Digits count only footers;
    other glyphs in a number count only through the digit-folded shape."""
    ev = collections.defaultdict(dict)    # sym -> {key: text}

    def add(t, kind, key, text):
        for s in set(t):
            if s[0] == "plain":
                continue
            if M[s] in DIGITS and kind != "page":
                continue
            ev[s].setdefault((kind, key.lower()), text)

    def known(t):
        return t is not None and all(s[0] == "plain" or s in M for s in t)

    for t in C.ctoks:
        if not known(t):
            continue
        w = repair(t, M)
        if not numeric(w) and w in C.ref:
            add(t, "vocab", w, f"{show(t)} → {w}")
        elif fold(w) != w and fold(w) in C.ref_fold:
            add(t, "shape", fold(w), f"{show(t)} → {w}")
    for prev, t, nxt in C.ctx:
        if not (known(t) and (known(prev) or known(nxt))):
            continue
        w = repair(t, M)
        a = repair(prev, M) if known(prev) else None
        b = repair(nxt, M) if known(nxt) else None
        if not any(c.isalpha() for c in (a or "") + (b or "")):
            continue
        if a is not None and b is not None:
            hit = (fold(a), fold(w), fold(b)) in C.tri_fold
            phrase = f"{a} {w} {b}"
        elif a is not None:
            hit = (fold(a), fold(w)) in C.bi_fold
            phrase = f"{a} {w}"
        else:
            hit = (fold(w), fold(b)) in C.bi_fold
            phrase = f"{w} {b}"
        if hit:
            add(t, "context", fold(phrase), f"{show(t)} → {w}  [in “{phrase}”]")
    off = C.page_offset(M, {})
    if off:
        for pdf, page, t in C.pagetoks:
            lab = str(page + off[pdf])
            if repair(t, M) == lab:
                add(t, "page", f"{pdf}{page}", f"{show(t)} → {lab}  [footer, {pdf} PDF page {page}]")
    return ev


def refine_classes(M, metrics):
    """A glyph the words place in the dash class is named by its advance."""
    notes = {}
    for s, ch in list(M.items()):
        if ch == "-":
            w = metrics.get(s[0], {}).get(s[1], (None,))[0]
            if w is None:
                continue
            M[s] = "-" if w < 0.4 else "\u2013" if w < 0.7 else "\u2014"
            notes[s] = f"dash class; advance {w:.3f} em → {M[s]!r}"
    return notes


# ------------------------------------------------------------ local-font check
def local_font_map(docs, aff_by_pdf, fam_names=("TimesNewRoman", "Arial")):
    """gid -> char from macOS fonts, kept only where glyf bytes are identical."""
    out = collections.defaultdict(dict)
    report = []
    for tag, doc in docs.items():
        for name, (base, xref) in aff_by_pdf[tag].items():
            fam = family(name)
            if fam not in fam_names:
                continue
            bold = "Bold" in name
            path = LOCAL_FONTS.get((fam, bold))
            sub = tt_glyphs(doc.extract_font(xref)[3])
            ref = tt_glyphs(open(path, "rb").read())
            rf = fitz.Font(fontfile=path)
            cmap = {}
            for cp in list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + [0x20AC, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022]:
                g = rf.has_glyph(cp)
                if g and g not in cmap:
                    cmap[g] = chr(cp)
            used = {g for g, (a, b) in sub.items() if b}       # glyphs with outlines kept in the subset
            for g in sorted(used | {SPACE_GID}):
                same = g in ref and sub[g][0] == ref[g][0] and outline(sub[g][1]) == outline(ref[g][1])
                if g in cmap:
                    report.append({"pdf": tag, "font": name, "gid": g, "cp": u(g), "local_char": cmap[g],
                                   "glyf_identical": same, "advance": sub[g][0]})
                    if same:
                        out[(fam, name)][g] = cmap[g]
    return out, report


# ------------------------------------------------------------ main
def main():
    docs = {k: fitz.open(v) for k, v in PDFS.items()}
    aff_by_pdf = {k: affected_fonts(d) for k, d in docs.items()}
    aff_names = {k: set(v) for k, v in aff_by_pdf.items()}
    verify = {k: verify_cp_is_gid(d, aff_names[k]) for k, d in docs.items()}

    lines = []
    for k, d in docs.items():
        lines += cipher_lines(d, aff_names[k], k)
    ref, ref_bi, ref_tri = reference()
    metrics = family_metrics(docs, aff_by_pdf)
    heights = {f: {g: v[1] for g, v in d.items()} for f, d in metrics.items()}
    C = Corpus(lines, ref, ref_bi, ref_tri, heights)
    M, inv, rounds, log = solve(C)

    ev = final_evidence(C, M)
    class_notes = refine_classes(M, metrics)
    gated = {s: ch for s, ch in M.items() if len(ev[s]) >= MIN_EV}
    dropped = {s: ch for s, ch in M.items() if s not in gated}

    # local-font cross-check for Times New Roman / Arial: a glyph whose outline
    # and advance are identical to the macOS font's glyph at the same id is
    # accepted from that font's cmap (word evidence is too thin: ~60 glyphs).
    lf_map, lf_report = local_font_map(docs, aff_by_pdf)
    for (fam, name), m in lf_map.items():
        for g, ch in m.items():
            if g == SPACE_GID:
                continue
            sym = (fam, g)
            if sym in M and M[sym] != ch:
                print("CONFLICT words vs outline", fam, u(g), M[sym], ch)
                continue
            gated[sym] = ch
            dropped.pop(sym, None)
            ev[sym].setdefault(("outline", name), f"{name} gid {g}: glyf outline + advance identical to "
                                                  f"macOS {os.path.basename(LOCAL_FONTS[(fam, 'Bold' in name)])} "
                                                  f"gid {g} = U+{ord(ch):04X}")

    # ---- residue
    sym_count = collections.Counter()
    sym_examples = collections.defaultdict(list)
    sym_boxes = {}
    for ln in lines:
        toks = tokens_of(ln)
        for s, b in zip(ln["syms"], ln["boxes"]):
            if s is not SEP and s[0] != "plain" and s[1] != SPACE_GID:
                sym_count[s] += 1
                sym_boxes.setdefault(s, (ln["pdf"], ln["page"], b))
        rl = repair(ln["syms"], gated).strip()
        for t, _ in toks:
            for s in set(t):
                if s[0] != "plain" and s not in gated and len(sym_examples[s]) < 5 and rl not in sym_examples[s]:
                    sym_examples[s].append(rl[:90])
    os.makedirs(CROPS, exist_ok=True)
    residue = []
    for s, n in sorted(sym_count.items(), key=lambda kv: -kv[1]):
        if s in gated:
            continue
        pdf, page, box = sym_boxes[s]
        r = fitz.Rect(box)
        clip = fitz.Rect(r.x0 - 45, r.y0 - 4, r.x1 + 45, r.y1 + 4)
        png = os.path.join(CROPS, f"{s[0]}_{s[1]:04X}.png")
        pg = fitz.open(PDFS[pdf])[page - 1]          # fresh copy: the box is never saved
        pg.draw_rect(r + (-0.5, -0.5, 0.5, 0.5), color=(1, 0, 0), width=0.4)
        pg.get_pixmap(clip=clip, dpi=300).save(png)
        lfam = [v[s[1]] for (fam, name), v in lf_map.items() if fam == s[0] and s[1] in v]
        residue.append({"family": s[0], "cp": u(s[1]), "glyph_id": s[1], "count": n,
                        "visual_reading_not_in_map": VISUAL_READINGS.get(s),
                        "example_lines": sym_examples[s],
                        "word_evidence": [v for v in ev.get(s, {}).values()][:3],
                        "solver_guess_dropped_by_gate": dropped.get(s),
                        "local_font_identical_glyph": sorted(set(lfam)),
                        "crop": png})

    # ---- readability
    ref_alpha = {a.lower() for w in ref if (a := alpha_word(w))}

    def readability(style=None):
        tot = hit = 0
        miss = collections.Counter()
        for ln in lines:
            for t, sty in tokens_of(ln):
                if not any(s[0] != "plain" for s in t) or (style and style not in sty):
                    continue
                a = alpha_word(repair(t, gated))
                if not a:
                    continue
                tot += 1
                if a.lower() in ref_alpha:
                    hit += 1
                else:
                    miss[a] += 1
        return tot, hit, miss

    tot, hit, miss = readability()
    styles = sorted({st for ln in lines for st in ln["styles"] if st})
    per_style = {}
    for st in styles:
        t, h, _ = readability(st)
        if t:
            per_style[st] = {"words": t, "in_vocab": h, "fraction": round(h / t, 4)}

    # ---- assemble
    fams = sorted({s[0] for s in gated})
    by_family = {f: {u(s[1]): ch for s, ch in sorted(gated.items()) if s[0] == f} for f in fams}
    space_ev = collections.defaultdict(set)
    for ln in lines:
        for t1, t2 in zip(tokens_of(ln), tokens_of(ln)[1:]):
            a, b = repair(t1[0], gated), repair(t2[0], gated)
            if (a, b) in ref_bi and len(a) > 2 and len(b) > 2:
                for f in {s[0] for s in t1[0] + t2[0] if s[0] != "plain"}:
                    space_ev[f].add(f"{a} {b}")
    evidence = {f: {} for f in fams}
    for s in sorted(gated):
        items = list(ev[s].items())
        items.sort(key=lambda kv: ({"page": 0, "vocab": 1, "context": 2, "shape": 3, "outline": 4}[kv[0][0]], -len(kv[1])))
        kinds = collections.Counter(k[0] for k, _ in items)
        evidence[s[0]][u(s[1])] = {"char": gated[s], "n_independent": len(items), "by_kind": dict(kinds),
                                   "examples": [v for _, v in items[:5]]}
        if s in class_notes:
            evidence[s[0]][u(s[1])]["class_refinement"] = class_notes[s]
    for f in fams:
        if space_ev[f]:
            by_family[f][u(SPACE_GID)] = " "
            evidence[f][u(SPACE_GID)] = {"char": " ", "n_independent": len(space_ev[f]),
                                         "by_kind": {"context": len(space_ev[f])},
                                         "examples": sorted(space_ev[f], key=len)[-5:]}
    blank = {}
    for tag, doc in docs.items():
        for name, (base, xref) in aff_by_pdf[tag].items():
            rec = tt_glyphs(doc.extract_font(xref)[3]).get(SPACE_GID, (0, b"x"))[1]
            blank[base] = len(rec) == 0
    for f in fams:
        if u(SPACE_GID) in evidence[f]:
            evidence[f][u(SPACE_GID)]["blank_glyph_in_subsets"] = blank
    nfc_aliases = {}
    for f in fams:
        used = {s[1] for s in sym_count if s[0] == f}
        for cp, ch in by_family[f].items():
            n = unicodedata.normalize("NFC", chr(int(cp[2:], 16)))
            if n != chr(int(cp[2:], 16)) and len(n) == 1 and ord(n) not in used:
                nfc_aliases.setdefault(f, {})[u(ord(n))] = {"char": ch, "nfc_of": cp}
    collisions = []
    for cp in sorted({cp for f in by_family for cp in by_family[f]}):
        vals = {f: by_family[f][cp] for f in fams if cp in by_family[f]}
        if len(set(vals.values())) > 1:
            collisions.append({"cp": cp, "by_family": vals})

    result = {
        "fonts": {k: sorted(b for b, _ in v.values()) for k, v in aff_by_pdf.items()},
        "codepoint_is_glyph_id": verify,
        "how_to_apply": ("Code point = glyph id of the embedded subset; the map is per font FAMILY "
                         "(rawdict span['font'].split(',')[0]: Calibri / Cambria / TimesNewRoman / Arial). "
                         "'map' is the Calibri family (Calibri, Calibri,Bold, Calibri,Italic, "
                         "Calibri,BoldItalic share one glyph order). Read glyphs with rawdict or texttrace: "
                         "get_text('words') drops every code point below U+0020, which deletes Calibri "
                         "A B C D E and Times digits. A U+0020 inside these spans is a gap MuPDF "
                         "synthesised, not a glyph."),
        "map": by_family.get("Calibri", {}),
        "map_by_family": by_family,
        "collisions_between_families": collisions,
        "nfc_aliases": nfc_aliases,
        "evidence": evidence.get("Calibri", {}),
        "evidence_by_family": {f: v for f, v in evidence.items() if f != "Calibri"},
        "local_font_check": lf_report,
        "residue": residue,
        "readability": {
            "definition": ("repaired tokens with >=1 affected glyph, edge punctuation trimmed, "
                           "alphabetic, len>=2; in_vocab = lowercase form occurs in the 2010-2026 "
                           "(not 2022) scheme vocabulary"),
            "words": tot, "in_vocab": hit, "fraction": round(hit / tot, 4) if tot else None,
            "per_style": per_style,
            "out_of_vocab_top": miss.most_common(60),
        },
        "solver": {"rounds": rounds, "accept_log": log},
    }
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)

    print("affected fonts:", json.dumps(result["fonts"]))
    print("cp==gid:", {k: (v["glyphs_matched"], v["glyphs_differing"]) for k, v in verify.items()})
    print("rounds", rounds, "| map size:", {f: len(m) for f, m in by_family.items()},
          "| dropped by gate:", {s[0] + " " + u(s[1]): c for s, c in dropped.items()})
    print("map:", " ".join(f"{k[2:]}={v!r}" for k, v in sorted(result["map"].items())))
    for f in fams:
        if f != "Calibri":
            print(f, "map:", by_family[f])
    print("collisions:", collisions)
    print(f"readability: {hit}/{tot} = {hit / tot:.4f}", per_style)
    print("OOV top:", miss.most_common(30))
    print("local font check:", [(r["font"], r["cp"], r["local_char"], r["glyf_identical"]) for r in lf_report])
    print("residue:")
    for r in residue:
        print(f"   {r['family']} {r['cp']} x{r['count']} dropped={r['solver_guess_dropped_by_gate']} "
              f"local={r['local_font_identical_glyph']} | {r['example_lines'][:2]}")
    page_lines = sorted((ln for ln in lines if ln["pdf"] == "HL" and ln["page"] == 3),
                        key=lambda ln: (round(ln["y"], 3), ln["x"]))
    print("--- HL page 3")
    shown = 0
    for ln in page_lines:
        t = repair(ln["syms"], gated).strip()
        if t:
            print("   ", t)
            shown += 1
        if shown == 30:
            break


if __name__ == "__main__":
    main()
