#!/usr/bin/env python3
"""Content-level QA for answer sidecars: for every crop-mode chip, compare the
text INSIDE the scheme crop against the text of the paper's question band.

Many SEC schemes restate the question (or its key nouns) inside the answer
block, so a healthy map shows real word overlap between the two sides. A chip
whose crop shares (almost) no vocabulary with its question is either a decoy
anchor or a mis-banded crop — exactly the failures marker checks can't see
(the marker "6." is present on the WRONG question's block too).

This is a triage signal, not a verdict: LOW rows need eyes (some schemes are
answers-only and legitimately share few words); OK rows still get per-profile
render spot-checks before their profile lights.

Usage:
  python3 qa_overlap.py <year> [fileid-prefix ...]     one year
  python3 qa_overlap.py all [fileid-prefix ...]        every year directory
Writes a per-chip TSV to out/overlap-<scope>.tsv and prints a per-file summary
(median overlap, low-chip count).
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
OUT = os.path.join(HERE, "out")

WORD_RE = re.compile(r"[^\W\d_]{3,}", re.UNICODE)
# High-frequency exam boilerplate (EN + GA) that matches everywhere and
# therefore proves nothing about alignment.
STOP = set("""
the and for that with this from are was were has have had you your which not
answer answers question questions marks mark scheme marking page section leaving
certificate examination level higher ordinary foundation common each any all
give state name write explain describe outline discuss two three four five
freagair ceist ceisteanna marc mharc scéim mharcála leathanach roinn
ardteistiméireacht gnáthleibhéal ardleibhéal bonnleibhéal scrúdú tabhair luaigh
scríobh mínigh déan cur síos amháin dhá trí ceithre cúig aon bith seo sin agus
ar an na don den chun atá go gach nach mór
""".split())


def words(text):
    return {w.lower() for w in WORD_RE.findall(text)} - STOP


def band_words(doc, p1, y0, y1):
    """Words in the paper's question band (1-indexed page, fractional Y)."""
    if not (1 <= p1 <= len(doc)):
        return set()
    pg = doc[p1 - 1]
    h = pg.rect.height
    got = [w for w in pg.get_text("words") if y0 * h <= (w[1] + w[3]) / 2 <= y1 * h]
    return words(" ".join(w[4] for w in got))


def crop_words(doc, regions):
    out = set()
    for seg in regions:
        p1 = seg.get("p")
        if not (isinstance(p1, int) and 1 <= p1 <= len(doc)):
            continue
        pg = doc[p1 - 1]
        if "r" in seg:
            x0, y0, x1, y1 = seg["r"]
            W, H = pg.rect.width, pg.rect.height
            clip = fitz.Rect(x0 * W, y0 * H, x1 * W, min(1.0, y1) * H)
            out |= words(pg.get_text("text", clip=clip))
        else:
            out |= words(pg.get_text())
    return out


def main():
    scope = sys.argv[1] if len(sys.argv) > 1 else "all"
    prefixes = tuple(sys.argv[2:]) or ("",)
    years = ([scope] if scope != "all"
             else sorted(d for d in os.listdir(ANSWERS) if d.isdigit()))
    rows = []
    summary = defaultdict(lambda: [0, 0, []])  # file -> [chips, low, overlaps]
    for year in years:
        ydir = os.path.join(ANSWERS, year)
        if not os.path.isdir(ydir):
            continue
        for fn in sorted(os.listdir(ydir)):
            if not fn.endswith(".json") or not fn.startswith(prefixes):
                continue
            sc = json.load(open(os.path.join(ydir, fn)))
            if sc.get("fallback"):
                continue
            ppath = os.path.join(CORPUS, "exampapers", year, sc["paperFileid"])
            spath = os.path.join(CORPUS, "markingschemes", year, sc["schemeFileid"])
            if not (os.path.exists(ppath) and os.path.exists(spath)):
                continue
            pd, sd = fitz.open(ppath), fitz.open(spath)
            key = f"{year}/{sc['paperFileid']}"
            for q in sc["q"]:
                if q.get("mode") == "pagejump":
                    continue
                pw = band_words(pd, q["pP"], q["pY"][0], q["pY"][1])
                cw = crop_words(sd, q["region"])
                inter = len(pw & cw)
                denom = min(len(pw), len(cw)) or 1
                ov = inter / denom
                low = ov < 0.12 and inter < 4
                rows.append((key, q["n"], f"{ov:.2f}", inter, len(pw), len(cw),
                             "LOW" if low else "ok", q.get("label", "")))
                s = summary[key]
                s[0] += 1
                s[1] += low
                s[2].append(ov)
            pd.close()
            sd.close()
    os.makedirs(OUT, exist_ok=True)
    out_path = os.path.join(OUT, f"overlap-{scope}.tsv")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("file\tq\toverlap\tshared\tpaperWords\tcropWords\tflag\tlabel\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    n_low_files = 0
    for key in sorted(summary):
        chips, low, ovs = summary[key]
        med = sorted(ovs)[len(ovs) // 2] if ovs else 0.0
        if low:
            n_low_files += 1
            print(f"LOW {key}: {low}/{chips} low chips, median {med:.2f}")
    print(f"== {len(summary)} files, {len(rows)} chips, "
          f"{sum(s[1] for s in summary.values())} low chips in {n_low_files} files "
          f"-> {out_path} ==")


if __name__ == "__main__":
    main()
