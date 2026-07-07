#!/usr/bin/env python3
"""Build a READING-ONLY answer sidecar for a language paper from an agent spec.

Language papers interleave an AURAL section, a READING-comprehension section and
a WRITTEN-production section, each with its own restarting question numbers, so
the deterministic count-reconcile engine can't map them. Here an agent, having
read the paper + scheme, supplies — for the reading questions ONLY (skipping
aural + composition) — a text anchor for the question on the paper and for its
answer in the scheme. This finds those anchors' y-positions deterministically
and builds tight per-question crops, so the coordinates can't drift.

q.n is a sequential integer (keeps the monotonic-n integrity test happy + unique
keys); q.label is the human display ("Text II · Q1") because the paper's printed
numbers restart per section.

Spec JSON:
{
  "year": 2015, "paperFileid": "...", "schemeFileid": "...",
  "questions": [
    { "label": "Text I · Q1",
      "paperPage": 3, "paperAnchor": "1.",
      "schemeStartPage": 10, "schemeStartAnchor": "1. (12 marks",
      "schemeEndPage": 10,   "schemeEndAnchor": "2. (27 marks" },   # end exclusive
    ...
  ]
}

Where a scheme has table-bounded blocks whose content sits slightly above the
question-label cell (e.g. Arabic's RTL answer tables), text anchors would clip.
Explicit fraction overrides are supported and take precedence when present:
  "schemeStartY": 0.07, "schemeEndY": 0.44, "paperY": 0.418
(schemeStartY/schemeEndY apply on schemeStartPage/schemeEndPage respectively;
use them only for hand-verified page/block-bounded regions.)
Usage: python3 lang_reading.py <spec.json>   (writes answers/<year>/<paper>.json)
"""
import json, os, sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
LIG = {"Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi", "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
       "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st"}
BLANK_TEXTS = {"blank page", "leathanach ban", "blank"}


def delig(s):
    for k, v in LIG.items():
        if k in s:
            s = s.replace(k, v)
    return s


def find_y(page, anchor):
    """Top y-fraction of the first line whose (de-ligatured) text starts with anchor."""
    H = page.rect.height
    best = None
    a = delig(anchor)
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            txt = delig("".join(s["text"] for s in ln["spans"]).strip())
            if txt.startswith(a):
                y = ln["bbox"][1] / H
                if best is None or y < best:
                    best = y
    return best


def is_blank(page):
    return delig(page.get_text("text")).strip().lower() in BLANK_TEXTS or not page.get_text("text").strip()


def main():
    spec = json.load(open(sys.argv[1]))
    year = spec["year"]
    sd = fitz.open(os.path.join(CORPUS, "markingschemes", str(year), spec["schemeFileid"]))
    pd = fitz.open(os.path.join(CORPUS, "exampapers", str(year), spec["paperFileid"]))
    qout, report = [], []
    for i, q in enumerate(spec["questions"], start=1):
        sp0 = q["schemeStartPage"]
        if "schemeStartY" in q:
            sy = float(q["schemeStartY"])
        else:
            sy = find_y(sd[sp0 - 1], q["schemeStartAnchor"])
        if sy is None:
            report.append(f"!! {q['label']}: scheme start anchor {q['schemeStartAnchor']!r} NOT FOUND on p{sp0}")
            continue
        ep = q.get("schemeEndPage", sp0)
        ey = None
        if "schemeEndY" in q:
            ey = float(q["schemeEndY"])
        elif q.get("schemeEndAnchor"):
            ey = find_y(sd[ep - 1], q["schemeEndAnchor"])
        # region from (sp0, sy) to (ep, ey or page-bottom)
        region = []
        if ep == sp0:
            end_y = ey if (ey is not None and ey > sy) else 1.0
            region.append({"p": sp0, "r": [0.0, round(sy, 4), 1.0, round(end_y, 4)]})
        else:
            region.append({"p": sp0, "r": [0.0, round(sy, 4), 1.0, 1.0]})
            for mid in range(sp0 + 1, ep):
                if not is_blank(sd[mid - 1]):
                    region.append({"p": mid, "r": [0.0, 0.0, 1.0, 1.0]})
            end_y = ey if ey is not None else 1.0
            region.append({"p": ep, "r": [0.0, 0.0, 1.0, round(end_y, 4)]})
        if "paperY" in q:
            py = float(q["paperY"])
        else:
            py = find_y(pd[q["paperPage"] - 1], q.get("paperAnchor", ""))
            py = 0.0 if py is None else py
        qout.append({"n": str(i), "label": q["label"], "pP": q["paperPage"],
                     "pY": [round(py, 4), 1.0], "region": region, "mode": "crop", "conf": 1.0})
        # report text actually inside the first segment
        seg = region[0]; pg = sd[seg["p"] - 1]; H = pg.rect.height
        snip = " ".join(delig(pg.get_text("text", clip=fitz.Rect(0, seg["r"][1] * H, pg.rect.width, seg["r"][3] * H))).split())[:80]
        report.append(f"  {i:>2} [{q['label']}] sp{sp0} y{sy:.3f}: {snip}")
    sidecar = {"v": 1, "paperFileid": spec["paperFileid"], "schemeFileid": spec["schemeFileid"],
               "component": "000", "band": [1, len(sd) + 1],
               "copyright": "© State Examinations Commission", "q": qout}
    out_root = os.environ.get("PT_LANG_OUT") or os.path.join(HERE, "answers")
    out = os.path.join(out_root, str(year), spec["paperFileid"] + ".json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(sidecar, open(out, "w"), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    print(f"wrote {out} ({len(qout)} reading questions)")
    for r in report:
        print(r)


if __name__ == "__main__":
    main()
