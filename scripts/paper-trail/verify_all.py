#!/usr/bin/env python3
"""Deterministic off-by-marker screen for EVERY committed answer sidecar.

Mirrors the engine's three question-number detectors (Question/Ceist word,
lead-int 'N.', 'Q.N' token) but runs them on the TEXT THAT ACTUALLY FALLS
INSIDE each question's crop rectangle. The invariant a correct crop must
satisfy: the FIRST marker inside question N's crop resolves to N. If the first
marker is some other number, the crop is showing the wrong question — exactly
the failure the user caught.

Buckets:
  OK       first marker in the crop == n
  MISMATCH first marker == some other number  (HIGH PRIORITY — wrong question)
  NOMARK   no marker found in the crop         (passage-language / recovered —
                                                needs a render eyeball, not auto-trust)

Usage:
  python3 verify_all.py                 # screen all committed sidecars
  python3 verify_all.py LC005           # only codes starting LC005
  python3 verify_all.py --bad           # print ONLY mismatch+nomark lines
"""
import json, os, re, sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(REPO, "paper-trail-corpus")
ANS = os.environ.get("PTANS_DIR") or os.path.join(HERE, "answers")
LIG = {"Ɵ": "ti", "Ʃ": "tt", "ϐ": "fi", "ﬀ": "ff", "ﬁ": "fi",
       "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st"}

QWORD = re.compile(r"\b(?:Question|QUESTION|Ceist|CEIST)\s+(\d{1,2})\b")
LEADINT = re.compile(r"^(\d{1,2})[.:]")
QTOKEN = re.compile(r"\bQ\.?(\d{1,2})\b")


def delig(s):
    for k, v in LIG.items():
        if k in s:
            s = s.replace(k, v)
    return s


def first_marker(txt):
    """First question-number marker reading top-to-bottom, or None.

    Scans line by line (clip text is already in reading order). A line yields a
    marker if it contains 'Question/Ceist N', starts with 'N.'/'N:', or has a
    'Q.N' token. Returns the number of the first such line."""
    for raw in txt.splitlines():
        ln = delig(raw.strip())
        if not ln:
            continue
        m = QWORD.search(ln)
        if m:
            return int(m.group(1))
        m = LEADINT.match(ln)
        if m:
            return int(m.group(1))
        m = QTOKEN.search(ln)
        if m:
            return int(m.group(1))
    return None


LABEL_NUM = re.compile(r"(?:Q|Question|Ceist)\.?\s*(\d{1,2})", re.I)


def label_number(q):
    """Printed question number carried by a section-restart `label`, or None.

    lang_reading/wave10 maps set q.n to a sequential integer while the paper's
    printed numbers restart per section; the printed number lives in the label
    (e.g. "Text II · Q1"). When present, the crop's first marker should match
    THIS, not n. (Audit 2026-07: label-consistency auto-clears 1,059 of the
    1,230 language flags the n-only screen raises.)"""
    lab = q.get("label")
    if not lab:
        return None
    m = LABEL_NUM.search(lab)
    return int(m.group(1)) if m else None


def clip_text(pg, r):
    W, H = pg.rect.width, pg.rect.height
    x0, y0, x1, y1 = r
    return pg.get_text("text", clip=fitz.Rect(x0 * W, y0 * H, x1 * W, min(1.0, y1) * H))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prefix = args[0] if args else ""
    bad_only = "--bad" in sys.argv
    n_ok = n_mis = n_nomark = n_jump = 0
    mismatches, nomarks = [], []
    for yd in sorted(os.listdir(ANS)):
        d = os.path.join(ANS, yd)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if prefix and not fn.startswith(prefix):
                continue
            sc = json.load(open(os.path.join(d, fn)))
            try:
                sd = fitz.open(os.path.join(CORPUS, "markingschemes", yd, sc["schemeFileid"]))
            except Exception as e:
                print(f"!! {yd}/{fn}: cannot open scheme {sc['schemeFileid']}: {e}")
                continue
            for q in sc["q"]:
                n = int(q["n"])
                seg0 = q["region"][0]
                if q.get("mode") == "pagejump" or "r" not in seg0:
                    n_jump += 1
                    continue
                txt = clip_text(sd[seg0["p"] - 1], seg0["r"])
                fm = first_marker(txt)
                code = f"{yd}/{fn[:-5]}"
                ln_expect = label_number(q)
                if fm is None:
                    n_nomark += 1
                    line0 = " ".join(t.strip() for t in delig(txt).splitlines() if t.strip())[:60]
                    nomarks.append(f"  NOMARK  {code} Q{n} p{seg0['p']}: {line0}")
                elif fm == n or (ln_expect is not None and fm == ln_expect):
                    n_ok += 1
                else:
                    n_mis += 1
                    line0 = " ".join(t.strip() for t in delig(txt).splitlines() if t.strip())[:60]
                    mismatches.append(f"  MISMATCH {code} Q{n}->found Q{fm} p{seg0['p']}: {line0}")
            sd.close()
    if mismatches:
        print("=== MISMATCH (crop's first marker != its question number) ===")
        print("\n".join(mismatches))
    if nomarks and not bad_only:
        print(f"\n=== NOMARK ({len(nomarks)} crops with no detectable marker) ===")
        print("\n".join(nomarks[:200]))
    elif nomarks:
        print(f"\n=== NOMARK x{len(nomarks)} ===")
        print("\n".join(nomarks))
    print(f"\n=== OK={n_ok}  MISMATCH={n_mis}  NOMARK={n_nomark}  pagejump/whole={n_jump} ===")
    return 0 if n_mis == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
