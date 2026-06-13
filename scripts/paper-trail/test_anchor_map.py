#!/usr/bin/env python3
"""
Phase 1 gate fixtures for anchor-map.py — the deterministic checks that must
hold before any Maths HL answer flag ships. Run: python3 test_anchor_map.py
(exits non-zero on failure). These assert against the EMITTED sidecars in
out/answers/, so run anchor-map.py first.

All page numbers are 1-BASED (pdf.js getPage / viewer data-page convention):
physical page 3 → 4, etc.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ANS = os.path.join(HERE, "answers")


def load(year, fid):
    with open(os.path.join(ANS, str(year), f"{fid}.json"), encoding="utf-8") as f:
        return json.load(f)


def q(sidecar, n):
    matches = [x for x in sidecar["q"] if x["n"] == n]
    assert len(matches) == 1, f"expected exactly one Q{n}, got {len(matches)}"
    return matches[0]


def check(name, cond):
    if not cond:
        print(f"  FAIL: {name}")
        return False
    print(f"  ok:   {name}")
    return True


def main():
    ok = True
    p1 = load(2022, "LC003ALP100EV.pdf")
    p2 = load(2022, "LC003ALP200EV.pdf")

    # 1. The substring-trap fix: Q1 is one anchor, on the right paper page.
    ok &= check("2022 P1 Q1 = exactly one anchor on paper page 4 (phys 3)",
                q(p1, "1")["pP"] == 4)
    ok &= check("2022 P1 has exactly 10 questions, monotonic 1..10",
                [x["n"] for x in p1["q"]] == [str(i) for i in range(1, 11)])

    # 2. The P1/P2 shared-scheme fix: each paper's Q1 points into its OWN band.
    ok &= check("2022 P1 Q1 → scheme page 7 (phys 6)",
                q(p1, "1")["region"][0]["p"] == 7)
    ok &= check("2022 P2 Q1 → scheme page 35 (phys 34)",
                q(p2, "1")["region"][0]["p"] == 35)
    ok &= check("2022 bands disjoint, P2 above P1",
                p1["band"][1] <= p2["band"][0])

    # 3. Every region page falls inside its own paper's band; fractions ∈ [0,1].
    for year in (2022, 2023, 2024, 2025):
        for comp in ("100", "200"):
            fid = f"LC003ALP{comp}EV.pdf"
            s = load(year, fid)
            lo, hi = s["band"]
            for item in s["q"]:
                for seg in item["region"]:
                    if not (lo <= seg["p"] < hi):
                        ok &= check(f"{year} {fid} Q{item['n']} page {seg['p']} in band [{lo},{hi})", False)
                    if "r" in seg and any(not (0.0 <= v <= 1.0) for v in seg["r"]):
                        ok &= check(f"{year} {fid} Q{item['n']} rect ∈ [0,1]", False)
                # crop regions must be monotonic in page order
                ps = [seg["p"] for seg in item["region"]]
                if item["mode"] == "crop" and ps != sorted(ps):
                    ok &= check(f"{year} {fid} Q{item['n']} region pages sorted", False)
    ok &= check("all region pages in-band, all fractions ∈ [0,1], crop pages sorted", True)

    print("\nGATE PASS" if ok else "\nGATE FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
