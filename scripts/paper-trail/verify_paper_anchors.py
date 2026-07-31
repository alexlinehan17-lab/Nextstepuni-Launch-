#!/usr/bin/env python3
"""PAPER-side screen for every committed answer sidecar — the counterpart to
verify_all.py.

verify_all.py opens the MARKING SCHEME and checks the answer crop. Nothing ever
opened the EXAM PAPER and checked the anchor, yet every sidecar carries one
(pP + pY) and components/PaperTrail/paperRegion.ts derives the question's whole
on-paper extent from it: anchors are sorted into print order and each question
runs from its own anchor to the NEXT one. So a marker matched somewhere it does
not belong does not merely mis-scroll a chip — it hands that question a crop of
someone else's text, and grows its neighbour's crop to swallow the difference.

Two independent screens, both deterministic:

  MARKER   the text at (pP, pY[0]) must open question n. Mirrors verify_all.py's
           detectors (Question/Ceist word, lead-int "N.", "Q.N" token) and its
           label-number allowance for section-restart maps.

  PAGETOP  an anchor with pY[0] == 0 that is NOT the lowest-numbered question on
           its page. Nothing legitimately starts a mid-page question at the very
           top of the page: the anchor collapsed to a page default, so the
           question sorts to the head of its page and paperRegion.ts gives it a
           sliver of the PREVIOUS question's tail. Seen in the bilingual
           two-column reading papers, where a question prints twice (Irish left,
           English right) and the duplicate pair collapses.

Both screens are advisory reports, not gates — the committed gate that runs in
CI without the corpus is test/paperTrailAnswers.test.ts. Run this locally, where
paper-trail-corpus/ exists.

Usage:
  python3 verify_paper_anchors.py            # screen every committed sidecar
  python3 verify_paper_anchors.py LC013      # only codes starting LC013
  python3 verify_paper_anchors.py --bad      # suppress the NOMARK listing
"""
import json
import os
import sys

import fitz

from verify_all import delig, first_marker, label_number

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANS = os.environ.get("PTANS_DIR") or os.path.join(HERE, "answers")

# Enough of the page to carry the question's opening line, no more — a wider
# band starts reading the question's body and finds its sub-part numbering.
BAND = 0.06


def band_text(pg, y0):
    W, H = pg.rect.width, pg.rect.height
    return pg.get_text("text", clip=fitz.Rect(0, y0 * H, W, min(1.0, y0 + BAND) * H))


def flat(txt):
    return " ".join(t.strip() for t in delig(txt).splitlines() if t.strip())[:70]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prefix = args[0] if args else ""
    bad_only = "--bad" in sys.argv
    n_ok = n_mis = n_nomark = n_skip = n_nopdf = 0
    mismatches, nomarks, pagetops = [], [], []

    for yd in sorted(os.listdir(ANS)):
        d = os.path.join(ANS, yd)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json") or (prefix and not fn.startswith(prefix)):
                continue
            sc = json.load(open(os.path.join(d, fn), encoding="utf-8"))
            code = f"{yd}/{fn[:-5]}"
            ppath = os.path.join(CORPUS, "exampapers", yd, sc["paperFileid"])
            try:
                pdoc = fitz.open(ppath)
            except Exception as e:
                print(f"!! {code}: cannot open paper {sc['paperFileid']}: {e}")
                n_nopdf += 1
                continue

            anchored = [q for q in sc["q"] if q.get("pP") and q.get("pY")]

            # --- PAGETOP: pY[0]==0 on a question that isn't first on its page ---
            by_page = {}
            for q in anchored:
                by_page.setdefault(q["pP"], []).append(q)
            for page, here in by_page.items():
                try:
                    ordered = sorted(here, key=lambda q: int(q["n"]))
                except (TypeError, ValueError):
                    continue
                for q in ordered[1:]:
                    if q["pY"][0] == 0.0:
                        pagetops.append(f"  PAGETOP  {code} Q{q['n']} p{page} "
                                        f"(page also holds Q{ordered[0]['n']})")

            # --- MARKER: the anchor must open its own question ---
            for q in anchored:
                try:
                    n = int(q["n"])
                except (TypeError, ValueError):
                    n_skip += 1
                    continue
                if q["pP"] > pdoc.page_count:
                    n_skip += 1
                    continue
                txt = band_text(pdoc[q["pP"] - 1], q["pY"][0])
                fm = first_marker(txt)
                lab = label_number(q)
                if fm is None:
                    n_nomark += 1
                    nomarks.append(f"  NOMARK   {code} Q{n} p{q['pP']}: {flat(txt)}")
                elif fm == n or (lab is not None and fm == lab):
                    n_ok += 1
                else:
                    n_mis += 1
                    mismatches.append(
                        f"  MISMATCH {code} Q{n}->found Q{fm} p{q['pP']}: {flat(txt)}")
            pdoc.close()

    if mismatches:
        print("=== MISMATCH (anchor does not open its own question) ===")
        print("\n".join(mismatches))
    if pagetops:
        print(f"\n=== PAGETOP ({len(pagetops)} collapsed anchors) ===")
        print("\n".join(pagetops))
    if nomarks and not bad_only:
        print(f"\n=== NOMARK ({len(nomarks)} anchors with no detectable marker) ===")
        print("\n".join(nomarks[:200]))
    elif nomarks:
        print(f"\n=== NOMARK x{len(nomarks)} ===")
    print(f"\n=== OK={n_ok}  MISMATCH={n_mis}  PAGETOP={len(pagetops)}  "
          f"NOMARK={n_nomark}  skipped={n_skip}  nopaper={n_nopdf} ===")
    return 0 if n_mis == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
