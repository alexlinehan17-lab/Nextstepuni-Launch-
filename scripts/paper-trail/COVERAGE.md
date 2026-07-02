# Paper Trail — "see the answer" coverage record

Per-question marking-scheme answer chips. Status of EVERY SEC subject across the three cycles.

**Coverage (2026-07-02, audited against `paperTrailData.ts`): 83 subject-cycles carry the
`answers` flag on ≥1 paper — 1,121 papers mapped (including 20 wave-10 sidecars).** The
prose sections below predate several coverage waves and undercount; the authoritative,
per-paper source of truth is the committed sidecars in `answers/<year>/` plus
`QA_PASSED_ANSWER_PROFILES` in `build-index.py`. An audit script (see the repo audit note)
regenerates the exact per-subject counts.

The feature needs a clean per-question text anchor on both the paper and the scheme;
subjects that can't are documented below with the reason.

> **Wave 10 (2026-07-02): section-anchored essays.** Two subjects the generic engine drops
> now map via `wave10_sections.py`: **Politics & Society** (LC568, HL+OL EV — Section A/B
> per-question blocks; the discursive-essay menu maps to the shared Section C criteria) and
> **Classical Studies** (LC008, HL+OL EV new-spec 2023–2025 — Section A `N.` markers +
> the common Q11b–16 / Q12–16 essay rubric). 20 sidecars, render+text QA verified. Old-spec
> CS (pre-2023) and P&S HL "choose N of M" years drop cleanly (non-1..N paper sequence).
> **Ship step outstanding:** upload the 20 sidecars to Storage (`out/wave10-upload.tsv`),
> then re-run `build-index.py` to light the flags. See `WAVE10.md`.


## Leaving Cert

### ✅ Live (40)
**Accounting**, Agricultural Science, Ancient Greek, **Applied Mathematics**, Art, Biology, Bulgarian, **Business**, Chemistry, Computer Science, Construction Studies, Croatian, Czech, Danish, Dutch, Economics, **Engineering**, **English**, Finnish, **Geography**, History, **Home Economics S & S**, Hungarian, Latin, Latvian, Lithuanian, Maltese, Mathematics, Modern Greek, Physical Education, Physics, Physics & Chemistry, Portuguese, Religious Education, Romanian, Slovakian, Slovenian, **Swedish**, **Technology**, **Agricultural Economics**

> Wave 9 (2026-06-13): SHORT-ANSWER CROP TIER — per-question tight Y-band crops where scheme answers pack ~3/page. **Technology** HL+OL 2010–2025, **Swedish** HIGHER (reading comprehension), **Agricultural Economics** HL{2010,2015,2019}+OL{2018,2019}. Languages (Spanish/German/Japanese/Russian/French/Polish) dropped by skeptics as aural/coincidental; Italian dropped (section-restart numbering).

> Wave 8 (2026-06-13): per-paper agent-verified subsets. **Applied Mathematics** HL+OL 2010–2022 (clean `N.` worked solutions). **Home Economics** HL+OL 2020–2025 (Section B Q1–5). **English** HIGHER Paper 2 only (2010, 2012–2016 — literature: grade bands + indicative-material lists per essay question; P1 comprehension/composition not mappable). **Accounting** HL 2018 + OL (worked-solution tables w/ per-line marks). **Business** HIGHER Section 1 short-answer (2020–2022) + 2020 long booklet; the other long booklets reuse Section-1 coords and are dropped. Engine gained colon-marker (`QUESTION 1:`) + centered standalone `QUESTION N` header detection.

> Wave 7 (2026-06-13): **Geography** lights the **Part Two** structured/essay booklet (P043) only — Q1–12, HL+OL, 2020–2025 (the modern split-booklet format). The Part One short-answer answerbook collapses onto a 1-page scheme key and is deliberately dropped, and pre-2020 single-booklet years anchor on the cover. **Engineering** lights HL {2015, 2021–2025} and OL {2010, 2011, 2013–2016, 2018, 2019, 2021, 2023–2025}; the dropped years have a scheme summary-table that bleeds into the count and are dropped rather than mis-mapped. Engine gained ligature-mojibake normalisation (`QuesƟon`→`Question`), a short-answer↔structured grammar guard, paper/scheme spread guards (kills chip-on-cover + short-answer-key collapse), and a header-anchored last-question crop that stops at the practical-marking-scheme appendix.

### ⛔ Not text-mappable (4) — feature cannot apply
- Design & Communication Graphics — visual/drawing (DCG)
- Irish — Irish-medium paper, no EV
- Mandarin Chinese — aural/listening (Mandarin)
- Office Admin And Customer — no EV pair (LC Office Admin)

### 🔧 Bespoke / short-answer page-jump tier (19) — under verification
_Wave 9: Technology + Agricultural Economics now generate per-question page-jump maps (short-answer key); under adversarial verification along with the languages (checked for aural/coincidental mismaps)._
- Arabic — language, no scheme markers
- Classical Studies — ✅ LIVE (wave 10, new-spec 2023–2025 HL+OL): Section A `N.` markers + common essay rubric
- Estonian — language, scheme-grouped answers
- French — language
- German — language
- Hebrew Studies — language
- History (Early Modern) — wrong scheme-file pairing in corpus
- Italian — language off-by-one
- Japanese — language
- Link Modules — needs per-subject grammar
- Music — off-by-one/partial
- Polish — language
- Politics and Society — ✅ LIVE (wave 10, HL+OL EV): Section A/B per-Q blocks + shared Section C essay criteria
- Russian — language
- Spanish — language section-restart numbering
- Swedish — non-monotonic Q1-after-Q6
- Ukrainian — language reconcile 6/10

## Junior Cycle

### ✅ Live (10)
Business Studies, English, Geography, Home Economics, Jewish Studies, Mathematics, Music, Religious Education, Science, Wood Technology

### ⛔ Not text-mappable (12) — feature cannot apply
- Applied Technology — practical (Applied Technology)
- Art Craft Design — visual (Art Craft Design)
- Art — visual (Art)
- Classical Studies — visual (Classical Studies)
- Classics — visual (Classics)
- Engineering — visual/drawing (Engineering)
- Graphics — visual (Graphics)
- Irish T1 — Irish T1, no EV
- Irish — Irish-medium, no EV
- Material Technology (Wood) — old-spec, no clean index id
- Metalwork — practical (Metalwork)
- Technical Graphics — visual (Technical Graphics)

### 🔧 Bespoke grammar needed (10) — deferred (wrong-answer risk if rushed)
- Ancient Greek — pre-window (filtered from index)
- Civic Social and Political Education — partial
- Environ & Social Studies — reconcile 4/14
- French — language (chips on instructions)
- German — language 20/21
- History — DBQ/essay
- Italian — language
- Latin — needs per-subject grammar
- Spanish — language
- Technology — clustered/garbled last Q

## Leaving Cert Applied

### ✅ Live (12)
Agriculture / Horticulture, Childcare / Community Care, Crafts & Design, English and Communications, French, German, Hair And Beauty, Hotel / Catering & Tourism, Information & Communication Tech., Italian, Office Admin And Customer, Sign Language

### ⛔ Not text-mappable (9) — feature cannot apply
- Contemporary Issues Task — portfolio Task (no exam)
- Engineering — visual/drawing (LCA Engineering)
- Gaeilge Chumarsáideach — Gaeilge, no EV
- General Education Task — portfolio Task
- Intro. to Information & Comm. Technology — no EV pair
- Personal Reflection Task — portfolio Task
- Practical Achievement Task — portfolio Task
- Vocational Education Task — portfolio Task
- Vocational Preparation Task — portfolio Task

### 🔧 Bespoke grammar needed (6) — deferred (wrong-answer risk if rushed)
- Active Leisure Studies — needs per-subject grammar
- Graphics And Construction Studies — project marking-criteria, not per-Q
- Mathematical Applications — page-header framing
- Social Education — Q15->Q12 mismatch
- Spanish — language reconcile 7/8
- Technology — Q1 "Answer any Ten" instructions
