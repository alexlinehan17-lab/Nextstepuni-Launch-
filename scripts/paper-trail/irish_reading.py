#!/usr/bin/env python3
"""Build READING-ONLY answer sidecars for the Irish-language family.

Modeled on lang_reading.py (same sidecar format: q.n + human `label`, tight
per-question crops, aural + composition skipped), but the anchors are
DETECTED and TEXT-VERIFIED rather than hand-authored. The paper is ground
truth: each reading question's printed text is extracted from the exam paper,
and its answer block is located in the scheme by matching that exact text
(schemes repeat the question verbatim above the acceptable answers). A
question ships only if:

  TEXT   its scheme anchor was found by unique full-text match of the
         question as printed on the paper, opening with the right number; or
  STRUCT the scheme block is bare (number + "(a)" but no repeated text) AND
         it is the unique correctly-numbered line pinned between two
         TEXT-verified neighbours in the same run.

Any other state — ambiguous match, wrong opening number, out-of-order
anchors, unexpected run shape, missing section boundary — DROPS THE WHOLE
PAPER. Missing is acceptable; wrong is not.

Families / grammars (verified against the PDFs):

  lc   LC Gaeilge HL/OL Paper Two (LC001[A|G]LP200IV): Ceist 1
       LEAMHTHUISCINT (100 marc) = two texts A+B whose questions are printed
       as two runs "1. (a) ..." .. "k. (a) ..." (k=6 HL / 5 OL, numbering
       restarts for text B). Scheme = LC001[A|G]LP000IV (covers both papers).
  jc   JC Gaeilge T2 HL/OL (JC001[A|G]LP000IV, 2022-): the scheme is a
       facsimile of the paper with model answers inserted. Reading = the
       Roinn-B Ceist blocks whose rubric is "Leigh ... agus freagair na
       ceisteanna" (HL: Ceist 4; OL: Ceist 4/6/7). q.n = printed Ceist
       number (continuous numbering, no restarts).
  lca  LCA Gaeilge Chumarsaideach (LB066CLP000IV): scheme is a facsimile.
       Reading = the CEIST blocks inside "Roinn 2 - Leamhthuiscint" (Ceist
       4 + 5; continuous numbering). q.n = printed number.

LC Foundation is intentionally NOT built: its reading section (matching
tasks + choose-2-of-3 passage options, numbering that restarts mid-paper)
was inspected and judged too irregular to map with certainty.

Usage:
  python3 irish_reading.py all            # run every job, write passing sidecars
  python3 irish_reading.py all --dry      # QA report only, write nothing
  python3 irish_reading.py 2024 --dry     # filter jobs by substring
"""
import json
import os
import re
import sys
import unicodedata

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
LIG = {"Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
       "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st"}


def delig(s):
    for k, v in LIG.items():
        if k in s:
            s = s.replace(k, v)
    return s


def norm(s):
    """Aggressive normalisation for cross-matching: de-ligature, strip fada,
    lowercase, alnum only."""
    s = delig(s)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s.lower() if c.isalnum())


class Doc:
    def __init__(self, path):
        self.d = fitz.open(path)
        self.npages = len(self.d)
        # lines: (page1, y0frac, x0, text) in reading order
        self.lines = []
        for pi in range(self.npages):
            pg = self.d[pi]
            H = pg.rect.height
            rows = []
            for b in pg.get_text("dict")["blocks"]:
                for ln in b.get("lines", []):
                    txt = delig("".join(s["text"] for s in ln["spans"])).strip()
                    if txt:
                        rows.append((pi + 1, max(0.0, ln["bbox"][1] / H),
                                     ln["bbox"][0], txt))
            rows.sort(key=lambda r: (r[1], r[2]))
            self.lines.extend(rows)

    def cap(self, pos):
        p, y = pos
        return (self.npages, 1.01) if p > self.npages else (p, min(1.01, y))

    def region_norm(self, start, end):
        """Normalised text of all lines in [(p,y) start, (p,y) end), in strict
        top-to-bottom reading order (immune to PDF block-order quirks such as
        footers extracted first)."""
        start, end = self.cap(start), self.cap(end)
        eps = 0.002
        out = []
        for p, y, x, txt in self.lines:
            if (p, y + eps) < start:
                continue
            if (p, y + eps) >= end:
                if p > end[0]:
                    break
                continue
            out.append(norm(txt))
        return "".join(out)


def pos_le(a, b):
    return (a[0], a[1]) <= (b[0], b[1])


def pos_lt(a, b):
    return (a[0], a[1]) < (b[0], b[1])


def lines_between(doc, start, end):
    for p, y, x, txt in doc.lines:
        if pos_le(start, (p, y)) and pos_lt((p, y), end):
            yield p, y, x, txt


NUMLINE = re.compile(r"^([1-9])\s*[\.\)]\s*(.*)$")


# ================================================================ LC HL/OL

def lc_paper_runs(pd):
    """The two reading-question runs on Paper Two: lines '<d>. (a) ...'
    (the '(a)' may sit on a neighbouring line box). Passage paragraphs are
    also numbered but never carry an '(a)' subpart marker nearby."""
    cands = []
    for i, (p, y, x, txt) in enumerate(pd.lines):
        m = NUMLINE.match(txt)
        if not m:
            continue
        near = []
        for q in range(max(0, i - 1), min(i + 4, len(pd.lines))):
            if pd.lines[q][0] == p:
                near.append(pd.lines[q][3])
        blob = " ".join(near).replace(" ", "")
        if "(a)" not in blob:
            continue
        cands.append((p, y, int(m.group(1)), txt))
    runs, cur = [], []
    for c in cands:
        if cur and c[2] == cur[-1][2] + 1:
            cur.append(c)
        elif c[2] == 1:
            if cur:
                runs.append(cur)
            cur = [c]
        # else: stray numbered line, ignore
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) >= 4]


def lc_paper_window(pd, run, i):
    """Normalised window of question i's text as printed on the paper,
    bounded by the next question line on the same page."""
    p, y, num, txt = run[i]
    if i + 1 < len(run) and run[i + 1][0] == p:
        end_y = run[i + 1][1]
    else:
        end_y = min(1.0, y + 0.12)
    w = pd.region_norm((p, y), (p, end_y))
    w = re.sub(r"^\d", "", w)
    if w.startswith("a"):  # the '(a)' subpart marker
        w = w[1:]
    return w


MATCH_LEN = 40  # 25-char windows collide on generic stems ("Luaigh dhá ...")
MARKTOKEN = re.compile(r"\(?\d{1,3}mh?a?rc\)?")


def demark(s):
    """Drop '(10 marc)'-style tokens: the paper prints per-question marks in
    boxes that share the question's visual row, the scheme does not."""
    return MARKTOKEN.sub("", s)


def lc_window_key(window):
    """Matchable key for an LC question: marks tokens dropped, cut before the
    '(Alt N)' paragraph reference (the scheme's repeat of the question often
    diverges into the answer right there / omits subpart (b))."""
    return re.split(r"alt\d", demark(window))[0][:MATCH_LEN]


def snap(pos):
    """Start a crop a hair above the anchor line so same-visual-row partners
    (a bare '2.' box and its '(a) ...' text box differ by ~0.001 in y) are
    always included regardless of extraction order."""
    return (pos[0], max(0.0, pos[1] - 0.004))


def lc_scheme_match(sd, want_num, window, lo, hi):
    """Find the unique scheme line 'want_num. ...' in (lo,hi) such that the
    question text `window` appears within the following ~1.3 pages. Returns
    (p, y) or ('AMBIG'/None)."""
    w = lc_window_key(window)
    if len(w) < 28:
        return None
    hits = []
    for p, y, x, txt in lines_between(sd, lo, hi):
        m = NUMLINE.match(txt)
        if not m or int(m.group(1)) != want_num:
            continue
        crop = demark(sd.region_norm(snap((p, y)), (p + 1, 0.30)))
        if w in crop:
            hits.append((p, y))
    if len(hits) == 1:
        return hits[0]
    return "AMBIG" if len(hits) > 1 else None


LC_TAIL_MARKERS = ("agbun", "anlitriocht", "siombaili", "roinnnalitriocht",
                   "antriail", "pros", "anpros", "filiocht", "anfhiliocht",
                   "ceist2", "aonad", "cuidii", "paipeara",
                   "taispeanfargosoileir", "leirighnamarcanna",
                   "leirighmionbhriseadh")


def lc_first_marker_after(sd, pos, names, hard_stop):
    for p, y, x, txt in lines_between(sd, pos, hard_stop):
        if pos_le((p, y), pos):
            continue
        n = norm(txt)
        for nm in names:
            if n.startswith(nm):
                return (p, y)
    return None


def build_lc(year, paper_fid, scheme_fid):
    pd = Doc(os.path.join(CORPUS, "exampapers", str(year), paper_fid))
    sd = Doc(os.path.join(CORPUS, "markingschemes", str(year), scheme_fid))

    runs = lc_paper_runs(pd)
    if len(runs) != 2 or len(runs[0]) != len(runs[1]):
        return None, [f"paper: expected exactly 2 equal '(a)' question runs, got {[len(r) for r in runs]}"]
    k = len(runs[0])

    # ---- text-anchor every question in the scheme, in order
    seq = []  # flat: (text_idx, i_in_run, window)
    for t in (0, 1):
        for i in range(k):
            seq.append((t, i, lc_paper_window(pd, runs[t], i)))
    anchors = [None] * len(seq)
    lo = (1, -1.0)
    hi = (sd.npages + 1, 0.0)
    reasons = []
    for idx, (t, i, w) in enumerate(seq):
        r = lc_scheme_match(sd, i + 1, w, lo, hi)
        if r == "AMBIG":
            reasons.append(f"text {'AB'[t]} Q{i + 1}: multiple scheme blocks match its text")
        elif r is not None:
            anchors[idx] = ("TEXT", r)
            lo = r  # subsequent anchors must come after (order enforced)
    if reasons:
        return None, reasons

    matched = [a for a in anchors if a]
    if len(matched) * 2 < len(seq):
        return None, [f"only {len(matched)}/{len(seq)} questions text-matched in scheme — below half"]

    # ---- STRUCT pass: bare blocks pinned between TEXT neighbours
    med_x = None
    xs = []
    for idx, a in enumerate(anchors):
        if a:
            p, y = a[1]
            for lp, ly, lx, ltxt in sd.lines:
                if lp == p and abs(ly - y) < 1e-9:
                    xs.append(lx)
                    break
    if xs:
        xs.sort()
        med_x = xs[len(xs) // 2]
    for idx, (t, i, w) in enumerate(seq):
        if anchors[idx]:
            continue
        prev_a = anchors[idx - 1] if idx > 0 else None
        next_a = anchors[idx + 1] if idx + 1 < len(seq) else None
        if not (prev_a and prev_a[0] == "TEXT" and (next_a is None or next_a[0] == "TEXT")):
            reasons.append(f"text {'AB'[t]} Q{i + 1}: no text match and neighbours not TEXT-verified")
            continue
        lo_b = prev_a[1]
        hi_b = next_a[1] if next_a else (sd.npages + 1, 0.0)
        cands = []
        for p, y, x, txt in lines_between(sd, lo_b, hi_b):
            if (p, y) == lo_b:
                continue
            m = NUMLINE.match(txt)
            if not m or int(m.group(1)) != i + 1:
                continue
            rest = m.group(2).replace(" ", "")
            if rest and not rest.startswith("(a)") and len(rest) > 6:
                continue  # long prose after the number: not a question block start
            if med_x is not None and abs(x - med_x) > 30:
                continue
            cands.append((p, y))
        if len(cands) == 1:
            anchors[idx] = ("STRUCT", cands[0])
        else:
            reasons.append(f"text {'AB'[t]} Q{i + 1}: bare block candidates={len(cands)} (need exactly 1)")
    if reasons:
        return None, reasons

    # ---- order sanity
    flat = [a[1] for a in anchors]
    for a, b in zip(flat, flat[1:]):
        if not pos_lt(a, b):
            return None, [f"scheme anchors out of order at {a} -> {b}"]

    # ---- crop ends
    b_q1 = anchors[k][1]
    tail_a = lc_first_marker_after(sd, anchors[k - 1][1],
                                   LC_TAIL_MARKERS + ("leamhthuiscintb", "b50marc"), b_q1) or b_q1
    hard = (min(sd.npages, anchors[-1][1][0] + 6) + 1, 0.0)
    tail_b = lc_first_marker_after(sd, anchors[-1][1], LC_TAIL_MARKERS, hard)
    if tail_b is None:
        return None, ["no end-of-reading marker found after last answer block"]

    questions = []
    for idx, (t, i, w) in enumerate(seq):
        start = snap(anchors[idx][1])
        if i + 1 < k:
            end = snap(anchors[idx + 1][1])
        elif t == 0:
            end = snap(tail_a)
        else:
            end = snap(tail_b)
        p, y, num, txt = runs[t][i]
        questions.append({"label": f"Léamhthuiscint {'AB'[t]} · Ceist {i + 1}",
                          "printed": i + 1, "verified": anchors[idx][0],
                          "pP": p, "pY": y, "start": start, "end": end,
                          "window": lc_window_key(w),
                          "crop_norm": sd.region_norm(start, end)})

    # ---- final per-question gates: the anchor's printed number must sit in
    # the crop's opening row(s) (same-row boxes can extract in any order)
    for q in questions:
        if str(q["printed"]) not in q["crop_norm"][:120]:
            reasons.append(f"{q['label']}: printed number {q['printed']} not in crop opening (crop: {q['crop_norm'][:40]})")
    for qi in questions:
        for qj in questions:
            if qi is qj or len(qj["window"]) < 28 or qj["window"] == qi["window"]:
                continue
            if qj["window"] in demark(qi["crop_norm"]) and qi["verified"] != "TEXT":
                reasons.append(f"{qi['label']}: crop contains text of {qj['label']} (collision)")
    if reasons:
        return None, reasons
    qa = [f"    {q['label']:<28} {q['verified']:<6} paper p{q['pP']} y{q['pY']:.3f} "
          f"scheme p{q['start'][0]} y{q['start'][1]:.3f}->p{q['end'][0]} y{q['end'][1]:.3f} "
          f"| {q['crop_norm'][:48]}" for q in questions]
    return _emit(paper_fid, scheme_fid, sd, questions, seq_n=True), qa


# ============================================== facsimile families (JC/LCA)

CEIST_RAW = re.compile(
    r"^\s*CEIST\s+(\d{1,2})\b\s*(\(\s*\d{1,3}\s*mh?arc\s*\))?\s*\d{0,3}\s*$",
    re.IGNORECASE)


def ceist_headers(doc, within):
    """Lines that ARE a 'Ceist N' heading (optionally '(NN marc)')."""
    out = []
    for p, y, x, txt in lines_between(doc, *within):
        m = CEIST_RAW.match(txt)
        if m:
            out.append((p, y, int(m.group(1)), txt))
    return out


def first_pass(headers):
    """First occurrence of each Ceist number, kept only while document
    position increases with the number (facsimile first pass; later repeats
    e.g. in an Aguisin are dropped)."""
    seen = {}
    for h in headers:
        if h[2] not in seen:
            seen[h[2]] = h
    seq = []
    for num in sorted(seen):
        h = seen[num]
        if seq and not pos_lt((seq[-1][0], seq[-1][1]), (h[0], h[1])):
            continue
        seq.append(h)
    return seq


def find_line(doc, start, names):
    for p, y, x, txt in doc.lines:
        if not pos_lt(start, (p, y)):
            continue
        n = norm(txt)
        for nm in names:
            if n.startswith(nm):
                return (p, y)
    return None


def build_facsimile(year, paper_fid, scheme_fid, family):
    pd = Doc(os.path.join(CORPUS, "exampapers", str(year), paper_fid))
    sd = Doc(os.path.join(CORPUS, "markingschemes", str(year), scheme_fid))
    label_prefix = {"jc": "Roinn B", "lca": "Roinn 2 Léamhthuiscint"}[family]

    if family == "lca":
        ps = find_line(pd, (1, 1.0), ("roinn2leamhthuiscint",))
        if ps is None:
            return None, ["paper: 'Roinn 2 - Leamhthuiscint' header not found (after cover)"]
        pe = find_line(pd, ps, ("roinn3",))
        ss = find_line(sd, (1, -1.0), ("roinn2leamhthuiscint",))
        if ss is None:
            return None, ["scheme: 'Roinn 2 - Leamhthuiscint' header not found"]
        if pe is None:
            return None, ["paper: Roinn 3 end boundary not found"]
        # the CEIST header can share a visual row with the Roinn 2 line
        ss = (ss[0], max(0.0, ss[1] - 0.02))
        p_hdrs = ceist_headers(pd, ((ps[0], max(0.0, ps[1] - 0.02)), pe))
        reading = sorted({h[2] for h in p_hdrs})
        if not reading:
            return None, ["no CEIST headers inside paper Roinn 2"]
        se = find_line(sd, ss, ("roinn3",))
        if se is None:
            # 2011-style scheme splits the "Roinn 3" heading across boxes:
            # accept a bare "Roinn" heading line as the boundary
            for p, y, x, txt in sd.lines:
                if pos_lt(ss, (p, y)) and norm(txt) == "roinn":
                    se = (p, y)
                    break
        if se is None:
            return None, ["scheme: no Roinn 3 boundary found after reading section"]
        s_hdrs = ceist_headers(sd, (ss, se))
        s_end_cap = se
    else:  # jc
        p_hdrs = first_pass(ceist_headers(pd, ((1, -1.0), (pd.npages + 1, 0.0))))
        ag = find_line(sd, (1, -1.0), ("aguisin",))
        s_end_cap = ag if ag else (sd.npages + 1, 0.0)
        s_hdrs = first_pass(ceist_headers(sd, ((1, -1.0), s_end_cap)))
        reading = []
        ordered = sorted(p_hdrs, key=lambda h: (h[0], h[1]))
        for i, h in enumerate(ordered):
            end = (ordered[i + 1][0], ordered[i + 1][1]) if i + 1 < len(ordered) else (pd.npages + 1, 0.0)
            head = pd.region_norm((h[0], h[1]), end)[:400]
            if "leigh" in head and "freagairnaceisteanna" in head:
                reading.append(h[2])
        if not reading:
            return None, ["no reading-rubric Ceist found on paper"]

    pmap, smap = {}, {}
    for h in p_hdrs:
        pmap.setdefault(h[2], h)
    for h in s_hdrs:
        smap.setdefault(h[2], h)
    p_sorted = sorted(pmap.values(), key=lambda h: (h[0], h[1]))
    s_sorted = sorted(smap.values(), key=lambda h: (h[0], h[1]))

    questions, reasons = [], []
    for num in reading:
        if num not in smap:
            reasons.append(f"Ceist {num}: header missing in scheme first pass")
            continue
        ph, sh = pmap[num], smap[num]
        nxt = [h for h in s_sorted if pos_lt((sh[0], sh[1]), (h[0], h[1]))]
        end = snap((nxt[0][0], nxt[0][1])) if nxt else s_end_cap
        p_next = [h for h in p_sorted if pos_lt((ph[0], ph[1]), (h[0], h[1]))]
        p_end = (p_next[0][0], p_next[0][1]) if p_next else (pd.npages + 1, 0.0)
        preg = pd.region_norm((ph[0], ph[1]), p_end)
        hn = norm(ph[3])
        if preg.startswith(hn):
            preg = preg[len(hn):]
        preg = re.sub(r"^\d{1,3}mh?arc", "", preg)
        window = preg[:60]
        crop = sd.region_norm(snap((sh[0], sh[1])), end)
        if f"ceist{num}" not in crop[:60]:
            reasons.append(f"Ceist {num}: 'Ceist {num}' not in crop opening (crop: {crop[:40]})")
            continue
        if len(demark(window)) >= 25 and demark(window)[:40] in demark(crop):
            ver = "TEXT"
        else:
            reasons.append(f"Ceist {num}: paper rubric window not found in scheme crop "
                           f"(window: {window[:40]} / crop: {crop[:60]})")
            continue
        questions.append({"label": f"{label_prefix} · Ceist {num}", "printed": num,
                          "pP": ph[0], "pY": ph[1], "start": snap((sh[0], sh[1])), "end": end,
                          "verified": ver, "crop_norm": crop, "window": window})
    if reasons:
        return None, reasons
    if not questions:
        return None, ["no questions detected"]
    for qi in questions:
        for qj in questions:
            if qi is qj or qj["window"][:30] == qi["window"][:30]:
                continue
            if qj["window"][:30] in qi["crop_norm"][:len(qi["crop_norm"]) // 2]:
                return None, [f"{qi['label']}: crop opens with text of {qj['label']} (collision)"]
    qa = [f"    {q['label']:<28} {q['verified']:<6} paper p{q['pP']} y{q['pY']:.3f} "
          f"scheme p{q['start'][0]} y{q['start'][1]:.3f}->p{q['end'][0]} y{q['end'][1]:.3f} "
          f"| {q['crop_norm'][:48]}" for q in questions]
    return _emit(paper_fid, scheme_fid, sd, questions, seq_n=False), qa


# ================================================================ emit

def _is_blank(pg):
    t = delig(pg.get_text("text")).strip().lower()
    return t in {"blank page", "leathanach ban", "blank"} or not t


def _emit(paper_fid, scheme_fid, sd, questions, seq_n):
    qout = []
    for i, q in enumerate(questions, start=1):
        (sp0, sy), (ep, ey) = sd.cap(q["start"]), sd.cap(q["end"])
        region = []
        if ep == sp0:
            end_y = ey if ey > sy else 1.0
            region.append({"p": sp0, "r": [0.0, round(sy, 4), 1.0, round(end_y, 4)]})
        else:
            region.append({"p": sp0, "r": [0.0, round(sy, 4), 1.0, 1.0]})
            for mid in range(sp0 + 1, ep):
                if not _is_blank(sd.d[mid - 1]):
                    region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
            if ey > 0.0:
                region.append({"p": ep, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        n = str(i) if seq_n else str(q["printed"])
        qout.append({"n": n, "label": q["label"], "pP": q["pP"],
                     "pY": [round(q["pY"], 4), 1.0], "region": region,
                     "mode": "crop", "conf": 1.0})
    return {"v": 1, "paperFileid": paper_fid, "schemeFileid": scheme_fid,
            "component": "000", "band": [1, sd.npages + 1],
            "copyright": "© State Examinations Commission", "q": qout}


# ================================================================ driver

def jobs():
    out = []
    for year in range(2011, 2026):
        for lev, code in (("HL", "A"), ("OL", "G")):
            out.append(("lc", year, f"LC irish {year} {lev}",
                        f"LC001{code}LP200IV.pdf", f"LC001{code}LP000IV.pdf"))
    for year in range(2022, 2026):
        for lev, code in (("HL", "A"), ("OL", "G")):
            out.append(("jc", year, f"JC jc-irish {year} {lev}",
                        f"JC001{code}LP000IV.pdf", f"JC001{code}LP000IV.pdf"))
    for year in [*range(2011, 2020), 2021, 2022, 2023, 2024, 2025]:
        scheme = "LB066CLP000iV.pdf" if year == 2024 else "LB066CLP000IV.pdf"
        out.append(("lca", year, f"LCA lca-gaeilge-chumarsaideach {year}",
                    "LB066CLP000IV.pdf", scheme))
    return out


def main():
    dry = "--dry" in sys.argv
    only = next((a for a in sys.argv[1:] if a not in ("all", "--dry")), None)
    written, dropped = [], []
    for fam, year, name, paper_fid, scheme_fid in jobs():
        if only and only not in name:
            continue
        ppath = os.path.join(CORPUS, "exampapers", str(year), paper_fid)
        spath = os.path.join(CORPUS, "markingschemes", str(year), scheme_fid)
        if not (os.path.exists(ppath) and os.path.exists(spath)):
            dropped.append((name, "PDF(s) not downloaded"))
            continue
        try:
            if fam == "lc":
                sidecar, info = build_lc(year, paper_fid, scheme_fid)
            else:
                sidecar, info = build_facsimile(year, paper_fid, scheme_fid, fam)
        except Exception as e:  # noqa: BLE001 — any parse anomaly = drop, never guess
            sidecar, info = None, [f"exception: {e!r}"]
        if sidecar is None:
            dropped.append((name, "; ".join(info)))
            print(f"DROP {name}")
            for r in info:
                print(f"    ! {r}")
            continue
        print(f"PASS {name} ({len(sidecar['q'])} questions)")
        for line in info:
            print(line)
        if not dry:
            out = os.path.join(HERE, "answers", str(year), paper_fid + ".json")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            json.dump(sidecar, open(out, "w"), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))
            written.append(out)
    print(f"\n=== written={len(written)} dropped={len(dropped)} ===")
    for n, r in dropped:
        print(f"  DROP {n}: {r[:170]}")


if __name__ == "__main__":
    main()
