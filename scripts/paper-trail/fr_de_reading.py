#!/usr/bin/env python3
"""French/German (LC010/LC011) reading-comprehension generator.

Replicates the shape of the verified lang_reading maps deterministically:
Section I holds two texts headed "Q.1"/"Q.2" on the paper AND the scheme, and
within each text the questions run "1." "2." … with "(i)/(ii)" sub-parts; the
scheme's answer blocks are headed "N.(i) …" lines. Chips are per sub-part with
"Text I · Q2(i)" labels, exactly like the committed maps.

Safety: the scan is BOUNDED to the reading section (from the first text header
to the written-production section), so aural/writing never enter; every paper
sub-part must find its scheme block (and vice versa within the bound) or the
paper drops; positions must be monotonic on both sides.

Regression: --check runs the generator on the committed years and reports any
divergence from the verified maps instead of writing anything.

Usage:
  python3 fr_de_reading.py --check           (2016-2018 regression)
  python3 fr_de_reading.py <years...>        (write missing years)
"""
import json
import os
import re
import sys
from collections import defaultdict

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANSWERS = os.path.join(HERE, "answers")
SIDECAR_V = 1
COPYRIGHT = "© State Examinations Commission"

ROMAN = {"i": "i", "ii": "ii", "iii": "iii", "iv": "iv", "v": "v"}
TEXT_HDR = re.compile(r"^Q[.,]?\s*([12])\b")
SUB_RE = re.compile(r"^\((i{1,3}v?|v)\)")
NUM_RE = re.compile(r"^(\d)\.\s*$|^(\d)\.\s")
SCHEME_BLOCK = re.compile(r"^(\d)\s*\.\s*\(\s*(i{1,3}v?|v|[a-e])\s*\)")
END_SECTION = re.compile(r"^\s*(SECTION\s+II\b|PRODUCTION\s+ÉCRITE|SCHRIFTLICHE|ÄUSSERUNG|WRITTEN\s+PRODUCTION)", re.I)


def lines_of(page):
    lines = defaultdict(list)
    for w in page.get_text("words"):
        lines[(w[5], w[6])].append(w)
    out = []
    H = page.rect.height
    for k in sorted(lines):
        lw = sorted(lines[k], key=lambda w: w[0])
        out.append((" ".join(w[4] for w in lw), lw[0][0], lw[0][1] / H))
    out.sort(key=lambda t: t[2])
    return out


def paper_chips(paper):
    """[(text#, n, sub, page0, y)] bounded to the reading section."""
    out, text, num, ended = [], None, None, False
    for pi in range(len(paper)):
        if ended:
            break
        for txt, x0, y in lines_of(paper[pi]):
            if END_SECTION.search(txt) and text is not None:
                ended = True
                break
            m = TEXT_HDR.match(txt)
            if m and x0 < 120:
                text, num = int(m.group(1)), None
                continue
            if text is None:
                continue
            fused = re.match(r"^(\d)\.\s*\((i{1,3}v?|v)\)", txt)
            if fused and x0 < 60:
                num = int(fused.group(1))
                out.append((text, num, fused.group(2), pi, y))
                continue
            nm = NUM_RE.match(txt)
            # the 60-70 x band holds both real questions and answer-point
            # enumerations; only a number continuing the ascending run is a
            # question there
            if nm and (x0 < 60 or (x0 < 70 and
                                   int(nm.group(1) or nm.group(2)) == (num or 0) + 1)):
                num = int(nm.group(1) or nm.group(2))
                # a numbered question with no sub-parts becomes its own chip;
                # sub-parts replace it when they follow
                out.append((text, num, "", pi, y))
                continue
            sm = SUB_RE.match(txt)
            if sm and num is not None and x0 < 100:
                out.append((text, num, sm.group(1), pi, y))
    # drop bare-number chips that have sub-parts
    with_subs = {(t, n) for t, n, s, *_ in out if s}
    out = [c for c in out if not (c[2] == "" and (c[0], c[1]) in with_subs)]
    # numbered passage paragraphs duplicate question numbers — the question
    # zone prints after the passage, so keep the LAST bare occurrence
    last = {}
    for i, c in enumerate(out):
        if c[2] == "":
            last[(c[0], c[1])] = i
    return [c for i, c in enumerate(out)
            if c[2] != "" or last[(c[0], c[1])] == i]


def scheme_blocks(scheme):
    """{(text#, n, sub): (page0, y)} bounded to the reading section."""
    blocks, text, ended = {}, None, False
    for pi in range(len(scheme)):
        if ended:
            break
        for txt, x0, y in lines_of(scheme[pi]):
            if END_SECTION.search(txt) and text is not None:
                ended = True
                break
            m = TEXT_HDR.match(txt)
            if m and x0 < 200:
                text = int(m.group(1))
                blocks.setdefault((text, 1, "i"), (pi, y))
                continue
            if text is None:
                continue
            bm = SCHEME_BLOCK.match(txt)
            if bm and x0 < 120:
                sub = bm.group(2)
                # modern schemes sub-part by LETTER; chips are question-level,
                # so the first letter block marks the whole question
                key = (text, int(bm.group(1)), "" if sub in "abcde" else sub)
                blocks.setdefault(key, (pi, y))
                continue
            # bare-number block ("6 ......" — the opinion question, one block
            # for all its sub-parts)
            nb = re.match(r"^(\d)\s*\.?\s*[.…]{2,}", txt) or re.match(r"^(\d)\s*$", txt)
            if nb and x0 < 120:
                blocks.setdefault((text, int(nb.group(1)), ""), (pi, y))
    return blocks


DE_LABELS = {
    ("1", "LV"): "Text I · Leseverständnis",
    ("1", "GR"): "Text I · Angewandte Grammatik",
    ("1", "AE"): "Text I · Äußerung zum Thema",
    ("2", "LV"): "Text II · Leseverständnis",
    ("2", "GR"): "Text II · Angewandte Grammatik",
    ("2", "AE"): "Text II · Äußerung zum Thema",
    ("3", "LV"): "Text III · Leseverständnis",
    ("3", "GR"): "Text III · Angewandte Grammatik",
    ("3", "AE"): "Text III · Äußerung zum Thema",
    ("SP", ""): "Schriftliche Produktion",
}


def de_headings(doc, start_page):
    """Ordered [(key, page0, y)] of component headings; tolerates the
    double-printed split headers ('TEXT'+'T II: LESEVE'+…) by gluing each
    line run and testing space-stripped tokens."""
    out, seen = [], set()
    for pi in range(start_page, len(doc)):
        ls = lines_of(doc[pi])
        for j, (txt, x0, y) in enumerate(ls):
            if x0 > 130 or y > 0.5:
                continue
            glue = "".join(t for t, _, yy in ls[j:j + 4] if yy - y < 0.06)
            glue = re.sub(r"\s+", "", glue).upper()
            key = None
            if glue.startswith("TEXT"):
                rm = re.match(r"TEXTT?(I{1,3}|\d)\s*[\s:(]", glue)
                if not rm:
                    continue
                text = str(len(rm.group(1))) if rm.group(1).startswith("I") else rm.group(1)
                if "LESEVE" in glue:
                    key = (text, "LV")
                elif "GRAMMATIK" in glue:
                    key = (text, "GR")
                elif "ÄUSSER" in glue or "ÄUßER" in glue or "AUSSER" in glue:
                    key = (text, "AE")
            elif glue.startswith("SCHRIFTLICHE"):
                key = ("SP", "")
            if key and key not in seen:
                seen.add(key)
                out.append((key, pi, y))
    return out


DE_Q_BLOCK = re.compile(r"^(?:Frage|Question|Aufgabe)\s+(\d)\s*:", re.I)
DE_OL_BLOCK = re.compile(r"^(\d)\s*\.\s*\(?\s*\d+\s*(?:marks?|Punkte|marc)", re.I)


def de_modern_zones(doc, start_page):
    """[(text#, start(pi,y), end(pi,y))] Leseverständnis zones via the
    glue-tolerant heading classifier."""
    hs = de_headings(doc, start_page)
    zones = []
    for i, (k, pi, y) in enumerate(hs):
        if k[1] != "LV":
            continue
        end = (hs[i + 1][1], hs[i + 1][2]) if i + 1 < len(hs) else (len(doc), 0.0)
        zones.append((int(k[0]) if k[0] != "SP" else 0, (pi, y), end))
    return zones


def de_modern_build(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    pz = de_modern_zones(paper, 1)
    sz = de_modern_zones(scheme, 1)
    if not pz or {t for t, *_ in pz} != {t for t, *_ in sz}:
        return None, f"LV zones mismatch {[t for t, *_ in pz]} vs {[t for t, *_ in sz]}"

    def collect(doc, zones, matchers):
        found = []
        for t, (sp, sy), (ep, ey) in zones:
            num = 0
            for pi in range(sp, min(ep + 1, len(doc))):
                for txt, x0, y in lines_of(doc[pi]):
                    if pi == sp and y <= sy:
                        continue
                    if pi == ep and ey and y >= ey:
                        break
                    for rx, seq in matchers:
                        m = rx.match(txt)
                        if m and x0 < 140:
                            n = int(m.group(1))
                            if not seq or n == num + 1:
                                if n == num + 1:
                                    num = n
                                found.append((t, n, pi, y))
                            break
        return found

    sq = collect(scheme, sz, [(DE_Q_BLOCK, False), (DE_OL_BLOCK, False)])
    smap = {}
    for t, n, pi, y in sq:
        smap.setdefault((t, n), (pi, y))
    # the scheme's block set defines each text's question numbers; the paper
    # walk accepts only the next expected number (gap-fill items are skipped)
    want = {t: sorted(n for tt, n in smap if tt == t) for t, *_ in pz}
    NUMLINE = re.compile(r"^(\d)\s*[\.\s]")
    pmap = {}
    for t, (sp, sy), (ep, ey) in pz:
        exp = [n for n in want.get(t, []) if n]
        for pi in range(sp, min(ep + 1, len(paper))):
            if not exp:
                break
            for txt, x0, y in lines_of(paper[pi]):
                if (pi == sp and y <= sy) or not exp:
                    continue
                if pi == ep and ey and y >= ey:
                    break
                m = NUMLINE.match(txt)
                if m and x0 < 140 and int(m.group(1)) == exp[0]:
                    pmap[(t, exp.pop(0))] = (pi, y)
    keys = sorted(pmap)
    if len(keys) < 6:
        return None, f"too few questions: {keys}"
    missing = [k for k in sorted(smap) if k not in pmap]
    if missing:
        return None, f"paper questions missing {missing}"
    resolved = [((t, n, ""), smap[(t, n)], pmap[(t, n)]) for t, n in keys]
    sc, err = emit(resolved, paper, scheme, paper_path, scheme_path)
    if sc is None:
        return None, err
    for q, (t, n) in zip(sc["q"], keys):
        q["label"] = f"Text {ROMANS[t]} · Q{n}"
    return sc, None


def de_build(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    ph = de_headings(paper, 1)
    if len(ph) < 4:
        return None, f"too few paper components: {[k for k, *_ in ph]}"
    sh = de_headings(scheme, 1)
    smap = {k: (pi, y) for k, pi, y in sh}
    missing = [k for k, *_ in ph if k not in smap]
    if missing:
        return None, f"scheme components missing {missing}"
    resolved = [((k, 0, ""), smap[k], (pi, y)) for k, pi, y in ph]
    sc, err = emit(resolved, paper, scheme, paper_path, scheme_path)
    if sc is None:
        return None, err
    for q, (k, *_ ) in zip(sc["q"], ph):
        q["label"] = DE_LABELS[k]
    return sc, None


OL_TEXT = re.compile(r"^[QC][.,]?\s*([1-4])\b")
OL_SCHEME_TEXT = re.compile(r"^Q[.,]?\s*([1-4])\s*\(")
OL_END = re.compile(r"^(Section\s+B|Roinn\s+B|Expression\s+[ÉE]crite)\b")
ROMANS = {1: "I", 2: "II", 3: "III", 4: "IV"}


OL_BANNER = re.compile(
    r"(FREAGAIR\s+IAD|ANSWER\s+IN\s+ENGLISH|R[ÉE]PONDEZ\s+EN\s+FRAN)", re.I)


def ol_paper_chips(paper):
    """Passages embed their own numbered items (interview questions, profile
    entries, margin section numbers), so numbers only count once the text's
    answer banner has been seen."""
    out, text, num, armed = [], None, None, False
    for pi in range(1, len(paper)):
        for txt, x0, y in lines_of(paper[pi]):
            if OL_END.match(txt) and x0 < 120 and out:
                return out
            m = OL_TEXT.match(txt)
            if m and int(m.group(1)) == (text or 0) + 1:
                text, num, armed = int(m.group(1)), None, False
                continue
            if text is None:
                continue
            if not armed and OL_BANNER.search(txt):
                armed, num = True, None
                continue
            nm = NUM_RE.match(txt)
            if (armed and nm and x0 < 70
                    and int(nm.group(1) or nm.group(2)) == (num or 0) + 1):
                num = int(nm.group(1) or nm.group(2))
                out.append((text, num, "", pi, y))
    return out


def ol_scheme_blocks(scheme):
    blocks, text, seeded = {}, None, set()
    for pi in range(len(scheme)):
        for txt, x0, y in lines_of(scheme[pi]):
            if OL_END.match(txt) and x0 < 120 and text:
                return blocks
            m = OL_SCHEME_TEXT.match(txt)
            if m and x0 < 120:
                text = int(m.group(1))
                blocks.setdefault((text, 1, ""), (pi, y))
                seeded.add((text, 1, ""))
                continue
            if text is None:
                continue
            bm = re.match(r"^(\d)\s*[\.\)…]", txt) or re.match(r"^(\d)\s*$", txt)
            if bm and x0 < 70:
                key = (text, int(bm.group(1)), "")
                if key in seeded:
                    # a real "1." block beats the header fallback
                    blocks[key] = (pi, y)
                    seeded.discard(key)
                else:
                    blocks.setdefault(key, (pi, y))
    return blocks


def ol_build(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    pc = ol_paper_chips(paper)
    if len(pc) < 12:
        return None, f"too few paper chips: {len(pc)}"
    sb = ol_scheme_blocks(scheme)
    missing = [c[:2] for c in pc if (c[0], c[1], "") not in sb]
    if missing:
        return None, f"scheme blocks missing {missing[:5]} of {len(pc)}"
    resolved = [((t, n, ""), sb[(t, n, "")], (pi, y)) for t, n, _, pi, y in pc]
    sc, err = emit(resolved, paper, scheme, paper_path, scheme_path)
    if sc is None:
        return None, err
    for q, (t, n, *_ ) in zip(sc["q"], pc):
        q["label"] = f"Text {ROMANS[t]} · Q{n}"
    return sc, None


def build(paper_path, scheme_path):
    base = os.path.basename(paper_path)
    if "LC011" in base and "BV" in base:
        return de_modern_build(paper_path, scheme_path)
    if "LC011" in base:
        return de_build(paper_path, scheme_path)
    if "GLP" in base and "BV" in base:
        sc, err = ol_build(paper_path, scheme_path)
        if sc is not None:
            return sc, err
        return fr_build(paper_path, scheme_path)
    return fr_build(paper_path, scheme_path)


def fr_build(paper_path, scheme_path):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    pc = paper_chips(paper)
    if len(pc) < 8:
        return None, f"too few paper chips: {len(pc)}"
    sb = scheme_blocks(scheme)
    # merge a question's paper sub-parts when the scheme carries ONE bare block
    merged, seen_merge = [], set()
    for t, n, sub, pi, y in pc:
        if (t, n, sub) not in sb and (t, n, "") in sb and sub:
            if (t, n) in seen_merge:
                continue
            seen_merge.add((t, n))
            merged.append((t, n, "*", pi, y))
        else:
            merged.append((t, n, sub, pi, y))
    pc = merged
    missing = [c[:3] for c in pc
               if (c[0], c[1], "" if c[2] == "*" else c[2]) not in sb
               and (c[0], c[1], c[2] or "i") not in sb]
    if missing:
        return None, f"scheme blocks missing {missing[:5]} of {len(pc)}"
    resolved = []
    for t, n, s, pi, y in pc:
        lookup = "" if s == "*" else s
        key = (t, n, lookup) if (t, n, lookup) in sb else (t, n, lookup or "i")
        resolved.append(((t, n, s), sb[key], (pi, y)))
    return emit(resolved, paper, scheme, paper_path, scheme_path)


def emit(resolved, paper, scheme, paper_path, scheme_path):
    S = len(scheme)
    pts = [r[1] for r in resolved]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        return None, "scheme blocks not monotonic"
    ppts = [r[2] for r in resolved]
    if any(b <= a for a, b in zip(ppts, ppts[1:])):
        return None, "paper anchors not monotonic"
    qs = []
    for i, ((t, n, s), (sp, sy), (p_pi, p_y)) in enumerate(resolved):
        ep, ey = resolved[i + 1][1] if i + 1 < len(resolved) else (S, 0.0)
        segs = [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]}]
        for p in range(sp + 1, min(ep, sp + 4)):
            segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
        if ep < sp + 4 and ey > 0.02:
            segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        nxt = resolved[i + 1][2] if i + 1 < len(resolved) else (len(paper), 1.0)
        py1 = nxt[1] if nxt[0] == p_pi else 1.0
        roman = "I" if t == 1 else "II"
        label = (f"Text {roman} · Q{n} (opinion)" if s == "*"
                 else f"Text {roman} · Q{n}" + (f"({s})" if s else ""))
        qs.append({"n": str(i + 1), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0, "label": label})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": "000", "band": [1, S + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def committed_compare(sidecar, committed_path):
    old = json.load(open(committed_path))
    a = [(q.get("label"), q["pP"]) for q in old["q"]]
    b = [(q.get("label"), q["pP"]) for q in sidecar["q"]]
    return a == b, (len(a), len(b))


def main():
    if "--check" in sys.argv:
        ok = bad = 0
        for year in range(2010, 2019):
            for code in ("LC010", "LC011"):
                for lvl in "AG":
                    f = f"{code}{lvl}LP000EV.pdf"
                    cp = os.path.join(ANSWERS, str(year), f"{f}.json")
                    pp = os.path.join(CORPUS, "exampapers", str(year), f)
                    sp = os.path.join(CORPUS, "markingschemes", str(year), f)
                    if not (os.path.exists(cp) and os.path.exists(pp) and os.path.exists(sp)):
                        continue
                    sc, err = build(pp, sp)
                    if sc is None:
                        print(f"CHECK {year} {f}: generator DROPPED ({err})")
                        bad += 1
                        continue
                    same, counts = committed_compare(sc, cp)
                    print(f"CHECK {year} {f}: {'MATCH' if same else 'DIFFER'} {counts}")
                    ok += same
                    bad += not same
        for year in (2019, 2020, 2021, 2022, 2023, 2024, 2025):
            for code in ("LC010", "LC011"):
                for lvl in "AG":
                    f = f"{code}{lvl}LP000BV.pdf"
                    cp = os.path.join(ANSWERS, str(year), f"{f}.json")
                    pp = os.path.join(CORPUS, "exampapers", str(year), f)
                    sp = os.path.join(CORPUS, "markingschemes", str(year),
                                      f"{code}{lvl}LP000EV.pdf")
                    if not (os.path.exists(cp) and os.path.exists(pp) and os.path.exists(sp)):
                        continue
                    sc, err = build(pp, sp)
                    if sc is None:
                        print(f"CHECK {year} {f}: generator DROPPED ({err})")
                        bad += 1
                        continue
                    same, counts = committed_compare(sc, cp)
                    print(f"CHECK {year} {f}: {'MATCH' if same else 'DIFFER'} {counts}")
                    ok += same
                    bad += not same
        print(f"\nregression: {ok} match · {bad} differ/drop")
        return
    years = [int(y) for y in sys.argv[1:]] or list(range(2010, 2027))
    okc = drop = 0
    for year in years:
        for code in ("LC010", "LC011"):
            for lvl in "AG":
                f = f"{code}{lvl}LP000{'BV' if year >= 2019 else 'EV'}.pdf"
                pp = os.path.join(CORPUS, "exampapers", str(year), f)
                sp = os.path.join(CORPUS, "markingschemes", str(year),
                                  f"{code}{lvl}LP000EV.pdf")
                if not (os.path.exists(pp) and os.path.exists(sp)):
                    continue
                dst = os.path.join(ANSWERS, str(year), f"{f}.json")
                if os.path.exists(dst):
                    continue
                sc, err = build(pp, sp)
                if sc is None:
                    print(f"DROP {year} {f}: {err}")
                    drop += 1
                    continue
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                json.dump(sc, open(dst, "w"), sort_keys=True, separators=(",", ":"))
                print(f"OK   {year} {f}: {len(sc['q'])} chips")
                okc += 1
    print(f"\nmapped {okc} · dropped {drop}")


if __name__ == "__main__":
    main()
