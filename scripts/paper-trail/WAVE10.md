# Paper Trail — "See the answer" audit + Wave 10

**Date:** 2026-07-02
**Scope:** (1) audit which subjects have the answer ribbon, (2) verify the ones that do
render correctly, (3) implement it for subjects that don't where possible.

---

## 1. Audit — who has it

Counted directly from `paperTrailData.ts` (the shipped index) by the `answers:1` flag.

- **81 subject-cycles** carry the flag on ≥1 paper today; **1,121 papers** flagged.
- **19 subject-cycles have zero coverage.** Every one is accounted for below.
- After Wave 10 ships (this change): **83 covered, 17 zero** (P&S + Classical Studies move to live).

### The 19 zero-coverage subjects, classified

**Genuinely impossible — the feature cannot apply (no per-question text answer to show):**
- Design & Communication Graphics, JC Graphics, LCA Engineering — visual/drawing papers
- Mandarin Chinese — aural/listening
- Irish (LC + JC), Gaeilge Chumarsáideach (LCA), JC Irish — Irish-medium, no English paper
- JC History — document/essay (no per-question key)
- JC French, JC Italian, LCA Spanish, JC French — language papers whose scheme answers are
  grouped/aural (dropped by earlier waves as coincidental-mapping risk)

**Feasible now → DONE in Wave 10:**
- **Politics & Society** and **Classical Studies** (see §3).

**Feasible but deferred (low yield / high wrong-answer risk / corpus fix needed):**
- Arabic, Estonian, Hebrew Studies, Ukrainian — reading-comprehension language maps
  possible in principle but low yield; dropped earlier as aural/coincidental. Not worth the
  wrong-answer risk without per-subject verification.
- Link Modules — needs its own grammar.
- **History (Early Modern)** — *not a grammar problem: the corpus pairs the wrong scheme
  file* (COVERAGE.md notes this). A data-pairing fix in the harvest, not the engine.

## 2. Verification — do the live ones render correctly?

Checked all **1,121** committed answer maps, not a sample:

- **Structural invariants (all 1,121):** ✅ every map — question numbering sequential &
  unique, `pY`/rect fractions in `[0,1]`, every region page inside the map's scheme `band`,
  crop pages ordered, confidence in `(0,1]`. **0 problems.**
- **Deployed parity (all 1,121 Storage sidecars fetched):** ✅ **1,120 byte-identical** to
  the committed source. **1 drift:** `italian/2014` OL(IV) — the deployed sidecar is an
  older 5-question page-jump map; the committed local is the correct 20-question crop map.
  Re-upload fixes it (included in the ship step below).
- **Render QA (diverse sample across every risk category — Ag Science, Maths, Geography,
  Business, English P2 essays, Spanish/Japanese/Italian language-reading, Art, JC Maths,
  LCA, Technology, History, Home Ec):** ✅ every paper anchor lands on the right question and
  every scheme crop shows that question's own marking-scheme region. Language maps correctly
  pair the paper's L2 prompt with the scheme's English/marks block.
- **Test gate:** `test/paperTrailAnswers.test.ts` green (1,139 assertions, +15 for wave 10).

**Verdict: the ones that have it are showing correctly.** The single Italian drift is the
only defect and is fixed by the re-upload below.

## 3. Implementation — Wave 10 (Politics & Society + Classical Studies)

Both were in the "bespoke grammar needed / deferred" bucket. The generic `anchor-map.py`
drops them because the marking scheme has **one shared criteria block** for the discursive
essays rather than a per-question block. New generator: **`wave10_sections.py`**.

- **Politics & Society (LC568, HL+OL EV):** Section A (stimulus) and Section B (document)
  questions get their own scheme blocks; the Section C discursive-essay menu (Q3–Q7 HL /
  Q5–Q10 OL) all map to the **shared Section C marking-criteria block**, labelled honestly
  ("Question N · Section C — common marking criteria"). 9 papers.
- **Classical Studies (LC008, HL+OL EV, new-spec 2023–2025):** Section A (Q1–10) anchored on
  the scheme's `N.` answer markers; Section B essays (Q11b–16 / Q12–16) map to the **common
  essay rubric block**. Q11's own descriptor grid is kept separate. 11 papers. Old-spec
  (pre-2023) drops cleanly — no `Question N` grammar.
- **Safety:** same COUNT-RECONCILE gate — a paper ships only when every one of its questions
  lands a region; otherwise the whole paper drops (better no chip than a wrong one).
  Coordinates-only, real scheme pixels, © SEC. **20 sidecars, all render+text verified.**

### To ship Wave 10 live (needs Storage write credentials — not available in CI)

The sidecars are committed; the profiles are registered. Two credentialed steps remain
(Storage is `allow write: if false` — uploads go only through the gcloud pipeline):

```bash
# 1. Upload the 20 new sidecars + re-sync the 1 drifted Italian map to Storage.
#    Regenerate the TSV (out/ is gitignored) then upload:
python3 - <<'PY'
import os
rows=[]
for yr in os.listdir('scripts/paper-trail/answers'):
    d=f'scripts/paper-trail/answers/{yr}'
    if not (yr.isdigit() and os.path.isdir(d)): continue
    for fn in os.listdir(d):
        if fn.startswith(('LC568','LC008')):
            sid='politics-and-society' if fn.startswith('LC568') else 'classical-studies'
            rows.append(f"{d}/{fn}\tpapers/lc/{sid}/{yr}/answers/{fn[:-5]}.json")
rows.append("scripts/paper-trail/answers/2014/LC013ALP000IV.pdf.json\t"
            "papers/lc/italian/2014/answers/LC013ALP000IV.pdf.json")
open('scripts/paper-trail/out/wave10-upload.tsv','w').write('\n'.join(sorted(rows))+'\n')
print(len(rows),'rows')
PY
python3 scripts/paper-trail/upload_answers.py scripts/paper-trail/out/wave10-upload.tsv

# 2. Re-light the flags: build-index reads the committed sidecars + the (now updated)
#    QA_PASSED_ANSWER_PROFILES and regenerates paperTrailData.ts with answers:1 on the
#    20 papers. (Needs the local SEC harvest manifest in out/, as usual.)
python3 scripts/paper-trail/build-index.py
git add paperTrailData.ts && git commit -m "Paper Trail: light Wave 10 answer flags"
```

Until step 2 regenerates `paperTrailData.ts`, the flags stay off — so **no student ever
sees an "Answers" toggle that 404s.** That ordering is deliberate (sidecars in Storage
first, flag second), matching the pilot's ship discipline.
