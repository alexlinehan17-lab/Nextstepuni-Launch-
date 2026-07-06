# Home Economics — Second-Year Verification (2024 vs. 2025)

**Purpose.** Second-year stability check for the "Examiner's Chair" feature file
`data/examinersChair/homeeconomics.ts`, whose marking rules are cited to the SEC LC Home
Economics HL (and OL) marking scheme **2025**. This document verifies each load-bearing rule
against a **different year (2024)** so the feature's claims are not artefacts of a single year's
scheme.

## Sources obtained

| File | What it is | Provenance |
|------|-----------|-----------|
| `2024-marking-scheme.pdf` / `.md` (42 pp.) | SEC LC 2024 Marking Scheme — **Higher Level** — Home Economics (Scientific and Social) | educateplus.ie mirror of the SEC PDF; cover page carries the Coimisiún na Scrúduithe Stáit / State Examinations Commission imprint. Retrieved 2026-07-06. |
| `2024-ol-marking-scheme.pdf` / `.md` (38 pp.) | SEC LC 2024 Marking Scheme — **Ordinary Level** — Home Economics (Scientific and Social) | Same source; cover page confirms "Leaving Certificate 2024 … Ordinary Level". Retrieved 2026-07-06. |

Page references below are the `<!-- page N -->` PDF-page markers in the extracted `.md`, which
align with the printed footer numbers from p.3 onward (pp.1–2 = cover + "Note to teachers and
students").

**Retrieval note.** `examinations.ie` and `betterexams.ie` returned 403/Cloudflare challenges on
direct fetch (2026-07-06); the SEC-imprinted PDFs were retrieved via the educateplus.ie mirror,
the same route used for the 2025 filings. betterexams' `home-economics-s-and-s` path returned 403
(exists, blocked) vs. 404 for wrong slugs, corroborating the canonical subject slug.

**Structural parity check.** The 2024 HL and OL papers carry the identical top-level structure to
2025 (verbatim, p.3 of each): Section A = 60 marks (answer **ten** questions, **each 6 marks**);
Section B = 180 marks (Q1 compulsory @ 80, plus two of Q2–Q5 @ 50 each); Section C = 40 or 80
marks (one elective or core Q4). The general marking preamble ("only key phrases given…",
"alternative valid answers acceptable", "detail determined by the marks assigned…") is likewise
verbatim across years. No structural drift.

---

## Rule-by-rule verification

| # | Rule as asserted in `homeeconomics.ts` | 2025 cite (file) | 2024 evidence | Verdict |
|---|----------------------------------------|------------------|---------------|---------|
| **HE1** | 20-mark "Discuss" parts marked on a coarse **5:3:0** point ladder — well-developed point = 5, partial = 3, thin/undeveloped = **0** (no 1s or 2s; no consolation mark). | HL p.13, p.16 | **Present.** `4 strategies @ 5 marks (graded 5:3:0)` on a 20-mark part — HL **p.13**. Also `2 points @ 5 marks (graded 5:3:0)` — HL **p.15**. The 5:3:0 ladder pays 0 for a thin point exactly as asserted. (2024 also shows finer 5-mark ladders — `5:4:3:2:1:0`, `5:3:1:0` — confirming the scheme's own note that ladder detail can vary; the 5:3:0 form the session teaches is a genuine, recurring pattern.) | ✅ **Stable** (rule identical; page drifts p.13→p.13/p.15) |
| **HE2** | Structured parts distribute a fixed number of points across **named headings**; each named heading is **capped independently** — surplus points under one heading do not roll over. | HL p.16 | **Present.** "Give an account of Folic Acid/Folate under each of the following headings: • sources `3 sources @ 2 marks` • biological functions `3 functions @ 2 marks` • properties `3 properties @ 2 marks`" — HL **p.14** — each heading has its own independent cap of 3 points. Same pattern under Contaminant/Source/Effect headings (`1 @ 1 mark x2` each) — HL **p.8**. Points under one heading cannot fill another's cap. | ✅ **Stable** (rule identical; page drifts p.16→p.8/p.14) |
| **HE3** | In "name and describe/evaluate" parts, the **name** is a low, often **all-or-nothing** mark; the **description/evaluation carries the marks**. | HL p.8 | **Present.** `[Name 2 marks (graded 2:0), Description 2 marks (graded 2:1:0), Culinary application 2 marks (graded 2:1:0)] x3` — HL **p.12**: the name is graded **2:0 (all-or-nothing)** while the described components are graded to reward development. Also `Name 1 @ 3 marks (graded 3:2:0)` — HL **p.9** — low name mark. | ✅ **Stable** (rule identical; page drifts p.8→p.9/p.12) |
| **HE4** | **OL Section A** true/false-tick and fill-the-blank items are graded **2:0 (all-or-nothing)**, no partial credit and no penalty for a wrong answer — so a blank and a wrong guess both score 0; guessing is pure upside. | OL p.6–7, p.6 | **Present.** OL Q1 "Indicate with a tick whether each of the following statements is true or false. `3 @ 2 marks (graded 2:0)`" — OL **p.6**; OL Q5 same true/false pattern — OL **p.7**. Items score 2 (correct) or 0 (blank/incorrect); no negative marking appears anywhere in the OL scheme. Confirms the 2:0 all-or-nothing grading the session relies on. | ✅ **Stable** (rule identical; pages match: p.6–7) |

---

## Logical / no-penalty note (HE4)

The session's decision claim — "no penalty for a wrong answer, so a wrong guess and a blank both
score 0" — is not stated as an explicit sentence in either year's scheme; it is the direct logical
reading of the **2:0 grading** (only 2 or 0 available, no negative band) combined with the absence
of any deduction rule in the SEC general instructions. This inference holds identically in 2024
and 2025. Confidence: high.

## Conclusion

All four load-bearing rules (HE1 5:3:0 ladder, HE2 per-heading independent capping, HE3
name-is-cheap/describe-carries-the-marks, HE4 OL Section A 2:0 all-or-nothing) are **present and
unchanged in the 2024 HL and OL schemes**. The only cross-year differences are minor **page-number
drift** for the HL rules (a natural consequence of a one-page-shorter 2024 HL scheme, 42 pp. vs.
2025's 44 pp.); the OL Section A cite (p.6–7) is stable to the page. The 2025 in-app citations
carry year and page, so the page drift does not misrepresent the 2024 scheme — the 2025 cites
remain accurate for 2025. **No edits to `data/examinersChair/homeeconomics.ts` are warranted.**

**Verdict: all rules stable across a second year.**
