# Classical Studies — Examiner's Chair second-year verification (2024)

## Purpose
Cross-year stability check for `data/examinersChair/classical.ts`, whose marking rules
are cited to the **SEC LC Classical Studies marking scheme 2025** (HL + OL). This document
re-checks every load-bearing rule against a **second year — the SEC 2024 marking scheme**,
to confirm the rules the sessions teach are standing scheme features and not artefacts of a
single year. Special focus (per task): confirm the Low-Quality descriptor **"relies mostly
on narrative"** is genuinely present and stable.

## Sources obtained
- **2024 HL marking scheme** — `examiner-reports/classical-studies/2024-marking-scheme.pdf`
  (extracted `2024-marking-scheme.md`, `<!-- page N -->` markers). Retrieved from the
  exams.ie mirror of the SEC PDF (`exams.ie/paper-files/lc/classical-studies/higher/ms/2024/p0/ms.pdf`).
  examinations.ie itself is Cloudflare-gated to non-browser clients; the exams.ie copy is the
  unmodified SEC document (cover page: "Coimisiún na Scrúduithe Stáit … Leaving Certificate 2024
  Marking Scheme Higher Level Classical Studies").
- **2024 OL marking scheme** — `examiner-reports/classical-studies/2024-ol-marking-scheme.pdf`
  (extracted `2024-ol-marking-scheme.md`). Same mirror, ordinary-level path.
- Compared against the previously-filed **2025** schemes (`2025-marking-scheme.md`,
  `2025-ol-marking-scheme.md`).

### Page-location note (cites are year-anchored)
The `classical.ts` HL essay rules cite **"p.11"**. That is correct **for the cited 2025 scheme**:
the common essay-marking scheme (unit of development, full-question NB, Overall Quality bands)
sits on **PDF page 11** of the 2025 HL scheme. In the **2024** HL scheme the *identical* rules
appear on **PDF page 12** (printed page "8"). The page number shifts year-to-year; the rule
content does not. Verifying rule stability, not page-number stability, is the point of this check.

---

## Rule-by-rule result

| # | Session | Rule (as taught in `classical.ts`) | 2025 (cited) | 2024 (2nd year) | Verdict |
|---|---------|------------------------------------|--------------|-----------------|---------|
| CL1 | `cl-unit` | A markable Section B unit = **relevant point + relevant evidence + development (analysis/elaboration)**; **15 marks per unit**; a point-with-evidence that stops before analysing sits in the lower bands, not the top. | p.11 — verbatim | p.12 — verbatim | **STABLE** |
| CL2 (structural) | `cl-two-part` | A two-part (a/b) essay: unless the **full question** is addressed, **no more than three units** of development count **and** Overall Quality **cannot rise above the Low range**. | p.11 — verbatim | p.12 — verbatim | **STABLE** |
| CL2 (quantitative) | `cl-two-part` | The one-part ceiling is **"~57/80"**. | 3×15 + 12 (2025 Low-max) = **57** | 3×15 + 10 (2024 Low-max) = **55** | **YEAR-SPECIFIC** (see reframe) |
| CL3 (descriptor) | `cl-narrative` | The Low Overall-Quality band is defined as **"relies mostly on narrative"**. | p.11 — verbatim | p.12 — verbatim | **STABLE — descriptor confirmed both years** |
| CL3 (band cutoffs) | `cl-narrative` | Overall Quality bands stated as **Low 1–12 / Good 13–17 / High 18–20**. | 1–12 / 13–17 / 18–20 | **1–10 / 11–15 / 16–20** | **YEAR-SPECIFIC** (see reframe) |
| CL4 (OL) | `cl-ol-section-a` | At **OL, Section A = 300 marks, Section B = 100** (inverted vs HL). | OL scheme — "Section A: 300 marks" / "Section B: 100 marks" | OL scheme p… — "Section A: 300 marks" (l.167) / "Section B: 100 marks" (l.319) | **STABLE** |
| context | CL4 note | **HL is 200/200** (Section A stimulus 200 / Section B essays 200). | 200/200 | 2024 HL: "SECTION A: STIMULUS QUESTIONS 200 MARKS" / "SECTION B: EXTENDED ANSWERS 200 MARKS" | **STABLE** |
| context | `coverageNote` | OL softens "develops" to **"some development"** and **drops the top quality tier**. | OL 2025 | 2024 OL: unit feature "makes **some development**" (l.372); OL Overall Quality has only **Good / Low** tiers (l.382/385) — no High tier | **STABLE** |

### The "relies mostly on narrative" descriptor — explicit confirmation
**Confirmed and stable.** The full Low-Quality descriptor is verbatim-identical in both years:

- **2025 HL, p.11:** "1-12: Low Quality • limited engagement with the question; attempt to make points, but there is a lack of evidence/examples to support points made; **relies mostly on narrative**."
- **2024 HL, p.12:** "1-10: Low Quality • limited engagement with the question; attempt to make points, but there is a lack of evidence/examples to support points made; **relies mostly on narrative**."

The only difference is the band's upper bound (12 in 2025, 10 in 2024). The named descriptor
CL3 depends on — "relies mostly on narrative" — is a standing feature of the scheme, present in
both years. The session's core teaching point (a vivid retelling with no argument is held in the
Low band, however good the storytelling) holds in both years.

### CL1 unit-band detail (informational — not a `classical.ts` claim)
`classical.ts` does not assert the internal unit-band cut-offs, but for the record they also drift
by year:
- **2025:** 15 highly-developed / 13–14 well-developed / 11–12 developed / 3–10 basic.
- **2024:** 14–15 highly-developed / 12–13 well-developed / 10–11 developed / 3–9 basic.

`classical.ts` only claims the *structure* (point+evidence+development, development is the
differentiator, 15 per unit) — all of which is stable. The 4/4/7 sub-split inside CL1's `grid`
is an **authored pedagogical illustration**, not a scheme figure (the scheme awards the 15
holistically by development level, not 4+4+7), and `ruleNote` frames it as such. No year problem.

---

## Load-bearing conclusion
Every **structural** rule the four sessions are built on is **verbatim-stable across 2024 and 2025**:
- unit of development = point + evidence + development, 15 per unit (CL1);
- full-question requirement gating >3 units and Overall-Quality-above-Low (CL2);
- the "relies mostly on narrative" Low-Quality descriptor (CL3);
- OL Section A 300 / Section B 100 vs HL 200/200 (CL4);
- OL "some development" softening + dropped top tier (coverageNote).

The **only** cross-year drift is in two **quantitative cut-offs** that `classical.ts` states as
2025 values: the Overall-Quality band boundaries (**1–12 / 13–17 / 18–20** in 2025 vs
**1–10 / 11–15 / 16–20** in 2024) and the derived one-part **ceiling (~57 in 2025 vs 55 in 2024)**.
Because the file cites the 2025 scheme explicitly, these numbers are *correct for 2025*; but they
are taught to students as marking facts and they move year-to-year, so year-stable reframes are
proposed below.

**Confidence: high.** Both years' schemes are the authentic SEC PDFs (verified cover pages), and
the essay-marking rules were compared side by side.

---

## Proposed year-stable reframes (NOT applied — `classical.ts` left unedited per task)

These are the only two edits worth considering. The structural sessions need no change.

### Reframe A — CL2 one-part ceiling (`57` is a 2025-only figure; 2024 = 55)

`cl-two-part.scale.levels`, id `m57`:
- OLD: `{ id: 'm57', label: 'Max ~57 (one part only)', annotation: '57', marks: 57 }`
- NEW: `{ id: 'm57', label: 'Capped low (one part only)', annotation: '55', marks: 55 }`
  (or keep as-is but relabel to a range — see note text below)

`cl-two-part.scale.notes[2]`:
- OLD: `'That imposes a structural ceiling around 57/80, however good the one part is.'`
- NEW: `'That imposes a structural ceiling in the mid-50s/80 (three units max ≈ 45, plus a Low-range quality mark), however good the one part is.'`

`cl-two-part.scripts[0].keyNote`:
- OLD: `'Capped around 57 of 80 — a one-part answer can’t have more than three units count, and its Overall Quality is held in the Low range, no matter how strong part (a) is. Even a short, weaker treatment of part (b) removes the ceiling. Always give both parts of the question real attention.'`
- NEW: `'Capped in the mid-50s of 80 — a one-part answer can’t have more than three units count (≈45), and its Overall Quality is held in the Low range, no matter how strong part (a) is. Even a short, weaker treatment of part (b) removes the ceiling. Always give both parts of the question real attention.'`

`cl-two-part.takeaway.rule`:
- OLD: `'Address both parts, or you’re capped near 57/80.'`
- NEW: `'Address both parts, or you’re capped in the mid-50s/80.'`

`cl-two-part.takeaway.detail`:
- OLD: `'A one-sided answer to a two-part Classical Studies essay caps its units and holds Overall Quality in the Low range — roughly 57/80. Give both parts genuine treatment; even a brief second part lifts the ceiling.'`
- NEW: `'A one-sided answer to a two-part Classical Studies essay caps its units (three max ≈ 45) and holds Overall Quality in the Low range — a mid-50s/80 ceiling. Give both parts genuine treatment; even a brief second part lifts the ceiling.'`

Also the question stem `cl-two-part.question` ("roughly a 57/80 ceiling … Roughly where does the 80-mark essay top out?") and `questionNote` ("roughly a 57/80 ceiling for a one-sided answer") would move from `57` to "mid-50s".

### Reframe B — CL3 Overall-Quality band cut-offs (2025 numbers; 2024 differs)

The **descriptor** ("relies mostly on narrative") is stable — keep it. Only the numeric band
edges (1–12 / 13–17 / 18–20) are 2025-specific.

`cl-narrative.scale.levels`:
- OLD:
  `{ id: 'low', label: 'Low (1–12) — narrative', annotation: 'L', marks: 10 }`
  `{ id: 'good', label: 'Good (13–17)', annotation: 'G', marks: 15 }`
  `{ id: 'high', label: 'High (18–20)', annotation: 'H', marks: 19 }`
- NEW (drop the exact edges, keep the three-band shape):
  `{ id: 'low', label: 'Low — narrative', annotation: 'L', marks: 10 }`
  `{ id: 'good', label: 'Good', annotation: 'G', marks: 15 }`
  `{ id: 'high', label: 'High', annotation: 'H', marks: 19 }`

`cl-narrative.scale.notes[1]`:
- OLD: `'Low band (1–12): “relies mostly on narrative”.'`
- NEW: `'Low band: “relies mostly on narrative”.'`

`cl-narrative.question`:
- OLD: contains `The Low Quality band is defined as “relies mostly on narrative”.` (keep — stable)
- The band-number-free descriptor is already the load-bearing part; no numeric edit needed in the
  stem beyond removing "(1–12)"-style figures if any are added later.

**Recommendation:** Reframe B (dropping the exact band edges while keeping the verbatim descriptor)
is the safer long-term choice — the descriptor is the durable fact, the edges are not. Reframe A
likewise trades a single-year figure for a stable structural statement. Neither is urgent while the
file's citation remains explicitly the 2025 scheme, but both improve year-durability.

---

## Files created by this verification
- `examiner-reports/classical-studies/2024-marking-scheme.pdf`
- `examiner-reports/classical-studies/2024-marking-scheme.md`
- `examiner-reports/classical-studies/2024-ol-marking-scheme.pdf`
- `examiner-reports/classical-studies/2024-ol-marking-scheme.md`
- `examiner-reports/classical-studies/2024-verification.md` (this file)
