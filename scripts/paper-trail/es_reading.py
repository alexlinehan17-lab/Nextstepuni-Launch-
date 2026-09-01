#!/usr/bin/env python3
"""Spanish (LC012) modern era (2021+) — per-question generator.

Mirrors the committed 2021-2025 maps' granularity:
  HL: Section A Q1(a)·Q1-4 / Q1(b)·Q1-3 / Q2 (split (a)/(b) when the scheme
      does) + Section B Q1-4.  Section C (writing) has no indicative-answer
      blocks and gets no chips, exactly like the committed years.
  OL: Reading Q1-5.

Paper side: zone dividers ('Section A/B', 'Question 1 (b)', 'QUESTION 2') and
numbered question lines within each zone.  Scheme side: '1.(a)'/'1.(b)'/'2.'
headers with 'Q. N' sub-blocks, SECTION B with 'Q. N', OL 'Question N.'
blocks.  Monotonic + completeness gates; a paper drops rather than mis-chip.

--check regenerates committed years and reports pP/pY/region divergence
(labels are style, not geometry — not compared).

Usage:
  python3 es_reading.py --check
  python3 es_reading.py <years...>
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


def walk(doc, start=1):
    for pi in range(start, len(doc)):
        for txt, x0, y in lines_of(doc[pi]):
            yield txt.strip(), x0, y, pi


# ---------- HL ----------

P_SECA = re.compile(r"^(Section|Roinn)\s+A\b")
P_Q1B = re.compile(r"^(Question|Ceist)\s+1\s*\(\s*b\s*\)", re.I)
P_Q2 = re.compile(r"^(QUESTION|CEIST|Question|Ceist)\s+2\s*[\.\(]?\s*($|\(|Answer|Freagair)")
P_SECB = re.compile(r"^(Section|Roinn)\s+B\b")
P_SECC = re.compile(r"^(Section|Roinn)\s+C\b")
NUMQ = re.compile(r"^([1-9])\s*\.(\s|$)")

S_1A = re.compile(r"^1\s*\.\s*\(\s*a\s*\)")
S_1B = re.compile(r"^1\s*\.\s*\(\s*b\s*\)")
S_2 = re.compile(r"^2\s*\.\s*($|\()")
S_2A = re.compile(r"^\(\s*a\s*\)\s+\S")
S_2B = re.compile(r"^\(\s*b\s*\)\s+\S")
S_SECB = re.compile(r"^(SECTION|ROINN)\s+B\b", re.I)
S_SECC = re.compile(r"^(SECTION|ROINN)\s+C\b", re.I)
S_QN = re.compile(r"^[QC]\s*\.?\s*([1-9])\b")


def hl_paper(paper, want):
    """{key: (pi,y)}.  Articles number their own paragraphs, so within each
    zone the QUESTIONS are the LAST ascending run of the scheme's numbers —
    selected backward from the zone's end."""
    cur, found = None, {}
    cands = {z: [] for z in ("1a", "1b", "B")}
    for txt, x0, y, pi in walk(paper):
        if P_Q1B.match(txt) and x0 < 90:
            cur = "1b"
            found.setdefault(("zone", "1b"), (pi, y))
            continue
        if P_Q2.match(txt) and x0 < 90 and cur == "1b":
            cur = "2"
            found.setdefault(("2", ""), (pi, y))
            continue
        if P_SECB.match(txt) and x0 < 90 and y < 0.15:
            cur = "B"
            continue
        if P_SECC.match(txt) and x0 < 90 and y < 0.15:
            break
        if P_SECA.match(txt) and x0 < 90 and y < 0.15 and cur is None:
            cur = "1a"
            found.setdefault(("zone", "1a"), (pi, y))
            continue
        if cur in ("1a", "1b", "B"):
            m = NUMQ.match(txt)
            if m and x0 < 90:
                cands[cur].append((int(m.group(1)), pi, y))
        elif cur == "2":
            m = re.match(r"^\(\s*([ab])\s*\)($|\s)", txt)
            if m and x0 < 90:
                found.setdefault(("2", m.group(1)), (pi, y))
    for z in ("1a", "1b", "B"):
        exp = want.get(z, [])
        picked, idx = {}, len(cands[z])
        for n in reversed(exp):
            hit = next((i for i in range(idx - 1, -1, -1)
                        if cands[z][i][0] == n), None)
            if hit is None:
                picked = None
                break
            picked[n] = cands[z][hit][1:]
            idx = hit
        if picked:
            for n, pos in picked.items():
                found[(z, n)] = pos
    return found


def hl_scheme(scheme):
    blocks, cur = {}, None
    for txt, x0, y, pi in walk(scheme):
        if S_1A.match(txt) and x0 < 90:
            cur = "1a"
            blocks.setdefault(("zone", "1a"), (pi, y))
            continue
        if S_1B.match(txt) and x0 < 90:
            cur = "1b"
            blocks.setdefault(("zone", "1b"), (pi, y))
            continue
        if S_2.match(txt) and x0 < 90 and cur == "1b":
            cur = "2"
            blocks.setdefault(("2", ""), (pi, y))
            continue
        if S_SECB.match(txt):
            cur = "B"
            blocks.setdefault(("zone", "B"), (pi, y))
            continue
        if S_SECC.match(txt):
            blocks.setdefault(("end", ""), (pi, y))
            break
        if cur in ("1a", "1b", "B"):
            m = S_QN.match(txt)
            if m and x0 < 90:
                blocks.setdefault((cur, int(m.group(1))), (pi, y))
        elif cur == "2":
            if S_2A.match(txt) and x0 < 90:
                blocks.setdefault(("2", "a"), (pi, y))
            elif S_2B.match(txt) and x0 < 90:
                blocks.setdefault(("2", "b"), (pi, y))
    return blocks


def hl_build(paper_path, scheme_path, iv):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    S = len(scheme)
    sf = hl_scheme(scheme)
    want = {z: sorted(n for zz, n in sf if zz == z and isinstance(n, int))
            for z in ("1a", "1b", "B")}
    pf = hl_paper(paper, want)
    # Q2: chip per scheme granularity — (a)/(b) blocks if both sides split
    q2_split = (("2", "a") in sf and ("2", "b") in sf
                and ("2", "a") in pf and ("2", "b") in pf)
    keys = [("zone", "1a"), ("zone", "1b")]
    keys += [("2", "a"), ("2", "b")] if q2_split else [("2", "")]
    keys += [("B", n) for n in want["B"]]
    if len(want["B"]) < 2:
        return None, f"too few Section B questions: {want['B']}"
    missing = [k for k in keys if k not in sf or k not in pf]
    if missing:
        return None, f"anchors missing {missing}"
    word = ("Roinn", "Ceist") if iv else ("Section", "Q")
    lab = {}
    for k in keys:
        z, n = k
        if z == "zone" and n == "1a":
            lab[k] = ("Roinn A · Ceist 1(a) Litríocht" if iv
                      else "Section A · Q1(a) Literary text")
        elif z == "zone" and n == "1b":
            lab[k] = ("Roinn A · Ceist 1(b) Iriseoireacht" if iv
                      else "Section A · Q1(b) Journalistic text")
        elif z == "2":
            suf = f"({n})" if n else ""
            lab[k] = (f"Roinn A · Ceist 2{suf}" if iv else f"Section A · Q2{suf}")
        else:
            lab[k] = (f"Roinn B · Q{n}" if iv else f"Section B · Q{n}")
    return emit(keys, pf, sf, lab, paper, scheme, paper_path, scheme_path)


# ---------- OL ----------

OL_P_Q = [re.compile(rf"^(Question|Ceist)\s+{n}\b", re.I) for n in range(1, 6)]
OL_S_Q = [re.compile(rf"^(Question|Ceist)\s+{n}\s*[\.:]", re.I) for n in range(1, 6)]


def ol_build(paper_path, scheme_path, iv):
    paper, scheme = fitz.open(paper_path), fitz.open(scheme_path)
    pf, sf = {}, {}
    for txt, x0, y, pi in walk(paper):
        if P_SECB.match(txt) and x0 < 90 and y < 0.15:
            break
        for n in range(1, 6):
            if (n,) not in pf and OL_P_Q[n - 1].match(txt) and x0 < 90:
                pf[(n,)] = (pi, y)
    for txt, x0, y, pi in walk(scheme):
        if S_SECB.match(txt):
            sf[("end", "")] = (pi, y)
            break
        for n in range(1, 6):
            if (n,) not in sf and OL_S_Q[n - 1].match(txt) and x0 < 120:
                sf[(n,)] = (pi, y)
    keys = [(n,) for n in range(1, 6) if (n,) in pf]
    if len(keys) < 4:
        return None, f"too few OL questions: {sorted(pf)}"
    missing = [k for k in keys if k not in sf]
    if missing:
        return None, f"scheme anchors missing {missing}"
    lab = {(n,): (f"Roinn A · Ceist {n}" if iv else f"Reading Q{n}")
           for (n,) in keys}
    return emit(keys, pf, sf, lab, paper, scheme, paper_path, scheme_path)


def emit(keys, pf, sf, lab, paper, scheme, paper_path, scheme_path):
    S = len(scheme)
    pts = [sf[k] for k in keys]
    if any(b <= a for a, b in zip(pts, pts[1:])):
        return None, "scheme anchors not monotonic"
    ppts = [pf[k] for k in keys]
    if any(b <= a for a, b in zip(ppts, ppts[1:])):
        return None, "paper anchors not monotonic"
    end = sf.get(("end", ""), (S, 0.0))
    qs = []
    for i, k in enumerate(keys):
        sp, sy = sf[k]
        ep, ey = sf[keys[i + 1]] if i + 1 < len(keys) else end
        segs = [{"p": sp + 1, "r": [0.0, round(sy, 4), 1.0, 1.0]}]
        for p in range(sp + 1, min(ep, sp + 4)):
            segs.append({"p": p + 1, "r": [0.0, 0.0, 1.0, 1.0]})
        if ep < sp + 4 and ey > 0.02:
            segs.append({"p": ep + 1, "r": [0.0, 0.0, 1.0, round(ey, 4)]})
        p_pi, p_y = pf[k]
        nxt = pf[keys[i + 1]] if i + 1 < len(keys) else (len(paper), 1.0)
        py1 = nxt[1] if nxt[0] == p_pi else 1.0
        qs.append({"n": str(i + 1), "pP": p_pi + 1,
                   "pY": [round(p_y, 4), round(py1, 4)],
                   "region": segs, "mode": "crop", "conf": 1.0,
                   "label": lab[k]})
    sidecar = {"v": SIDECAR_V, "paperFileid": os.path.basename(paper_path),
               "schemeFileid": os.path.basename(scheme_path),
               "component": "000", "band": [1, S + 1],
               "copyright": COPYRIGHT, "q": qs}
    return sidecar, None


def build(pp, sp, lvl, lang):
    return (hl_build if lvl == "A" else ol_build)(pp, sp, lang == "IV")


def main():
    if "--check" in sys.argv:
        ok = bad = 0
        for year in (2021, 2022, 2023, 2024, 2025):
            for lvl in "AG":
                for lang in ("EV", "IV"):
                    f = f"LC012{lvl}LP000{lang}.pdf"
                    cp = os.path.join(ANSWERS, str(year), f"{f}.json")
                    pp = os.path.join(CORPUS, "exampapers", str(year), f)
                    sp = os.path.join(CORPUS, "markingschemes", str(year), f)
                    if not all(os.path.exists(p) for p in (cp, pp, sp)):
                        continue
                    sc, err = build(pp, sp, lvl, lang)
                    if sc is None:
                        print(f"CHECK {year} {lvl} {lang}: DROPPED ({err})")
                        bad += 1
                        continue
                    old = json.load(open(cp))
                    a = [(q["pP"], round(q["pY"][0], 2), q["region"][0]["p"],
                          round(q["region"][0]["r"][1], 2)) for q in old["q"]]
                    b = [(q["pP"], round(q["pY"][0], 2), q["region"][0]["p"],
                          round(q["region"][0]["r"][1], 2)) for q in sc["q"]]
                    same = a == b
                    print(f"CHECK {year} {lvl} {lang}: {'MATCH' if same else 'DIFFER'} ({len(a)}, {len(b)})")
                    ok += same
                    bad += not same
        print(f"\nregression: {ok} match · {bad} differ/drop")
        return
    years = [int(y) for y in sys.argv[1:] if y.isdigit()] or [2026]
    ok = drop = 0
    for year in years:
        for lvl in "AG":
            for lang in ("EV", "IV"):
                f = f"LC012{lvl}LP000{lang}.pdf"
                pp = os.path.join(CORPUS, "exampapers", str(year), f)
                sp = os.path.join(CORPUS, "markingschemes", str(year), f)
                if not (os.path.exists(pp) and os.path.exists(sp)):
                    continue
                dst = os.path.join(ANSWERS, str(year), f"{f}.json")
                if os.path.exists(dst):
                    continue
                sidecar, err = build(pp, sp, lvl, lang)
                if sidecar is None:
                    print(f"DROP {year} {lvl} {lang}: {err}")
                    drop += 1
                    continue
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                json.dump(sidecar, open(dst, "w"), sort_keys=True,
                          separators=(",", ":"))
                print(f"OK   {year} {lvl} {lang}: {len(sidecar['q'])} chips")
                ok += 1
    print(f"\nmapped {ok} · dropped {drop}")


if __name__ == "__main__":
    main()
