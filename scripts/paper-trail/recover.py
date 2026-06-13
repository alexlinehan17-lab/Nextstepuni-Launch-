#!/usr/bin/env python3
"""Recovery helper — build ONE precise answer sidecar from text anchors.

For papers the auto-engine can't map (passage-numbered languages, mis-filed
schemes, boundary bugs), an agent supplies, per question, a short text snippet
that uniquely starts the answer in the scheme (and the question on the paper).
This finds those snippets' y-positions and builds a tight per-question crop —
deterministic, no hand-typed fractions, so the coordinates can't drift.

Usage: python3 recover.py <spec.json>
spec = {
  "year": 2011, "paperFileid": "...", "schemeFileid": "...",
  "q": [ {"n":"1", "paperPage":4, "paperAnchor":"1.", "schemePage":3,
          "schemeAnchor":"1.", "schemeEnd":"2."}, ... ]   # schemeEnd optional
}
Writes answers/<year>/<paperFileid>.json and prints a render-check report.
"""
import json, os, sys, re
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
LIG = {"Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl"}


def delig(s):
    for k, v in LIG.items():
        s = s.replace(k, v)
    return s


def find_y(page, anchor):
    """Top y-fraction of the first line whose (de-ligatured) text starts with anchor."""
    H = page.rect.height
    best = None
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            txt = delig("".join(s["text"] for s in ln["spans"]).strip())
            if txt.startswith(anchor):
                y = ln["bbox"][1] / H
                if best is None or y < best:
                    best = y
    return best


def main():
    spec = json.load(open(sys.argv[1]))
    year = spec["year"]
    sd = fitz.open(os.path.join(CORPUS, "markingschemes", str(year), spec["schemeFileid"]))
    pd = fitz.open(os.path.join(CORPUS, "exampapers", str(year), spec["paperFileid"]))
    qs = sorted(spec["q"], key=lambda q: (q["schemePage"], 0))
    qout = []
    report = []
    for i, q in enumerate(spec["q"]):
        spage = q["schemePage"] - 1
        sy = find_y(sd[spage], q["schemeAnchor"])
        if sy is None:
            report.append(f"Q{q['n']}: scheme anchor {q['schemeAnchor']!r} NOT FOUND on p{q['schemePage']}")
            continue
        # end: next question's scheme anchor on the same page, else page bottom
        end_y = 1.0
        end_page = spage
        if q.get("schemeEnd"):
            ey = find_y(sd[spage], q["schemeEnd"])
            if ey and ey > sy:
                end_y = ey
        ppage = q["paperPage"] - 1
        py = find_y(pd[ppage], q.get("paperAnchor", q["n"] + "."))
        py = 0.0 if py is None else py
        region = [{"p": spage + 1, "r": [0.0, round(sy, 4), 1.0, round(end_y, 4)]}]
        qout.append({"n": str(q["n"]), "pP": ppage + 1, "pY": [round(py, 4), 1.0],
                     "region": region, "mode": "crop", "conf": 1.0})
        txt = delig(sd[spage].get_text("text", clip=fitz.Rect(0, sy * sd[spage].rect.height,
                    sd[spage].rect.width, end_y * sd[spage].rect.height)))
        report.append(f"Q{q['n']}: scheme p{q['schemePage']} y={sy:.3f}-{end_y:.3f} :: "
                      + " ".join(l.strip() for l in txt.splitlines() if l.strip())[:70])
    sidecar = {"v": 1, "paperFileid": spec["paperFileid"], "schemeFileid": spec["schemeFileid"],
               "component": "000", "band": [1, len(sd) + 1],
               "copyright": "© State Examinations Commission", "q": qout}
    out = os.path.join(HERE, "answers", str(year), spec["paperFileid"] + ".json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(sidecar, open(out, "w"), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    print(f"wrote {out} ({len(qout)} questions)")
    for r in report:
        print("  " + r)


if __name__ == "__main__":
    main()
