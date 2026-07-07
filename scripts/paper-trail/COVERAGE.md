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

> **P2C wave (2026-07-07): zero-coverage minor-language tail re-examined.** Agent-authored
> `lang_reading.py` specs (the reading-only mechanism; script gained optional explicit
> `schemeStartY`/`schemeEndY`/`paperY` overrides for table-bounded RTL blocks) now map 17
> sidecars across 7 subjects, each with per-question crop-text QA: **Estonian** LC
> {2025, 2019, 2016}, **Ukrainian** LC {2025 — its only paper}, **Arabic** LC {2025 HL,
> 2024 HL, 2023 OL — reading Q1–6, literature Q7–9 indicative blocks, grammar Q10–14;
> composition Q15 skipped}, **Mandarin Chinese** LC written papers {2025 HL, 2025 OL,
> 2024 HL — READING Q1–4 only; aural/writing skipped}, **LCA Spanish** {2023–2025 —
> Section 2 reading; Section 1 aural skipped}, **JC French** {2024, 2025 — Section B
> Q8–14}, **JC Italian** {2024, 2025 — Section B Q9–15}. **Hebrew Studies is
> confirmed-infeasible** (scheme is generic marking guidance, no per-question answers).
> Remaining years of these subjects need the same per-paper spec authoring before they
> can light. **Ship step outstanding:** upload the 17 sidecars (`out/p2c-upload.tsv`),
> then re-run `build-index.py`.


## Leaving Cert

### ✅ Live (40)
**Accounting**, Agricultural Science, Ancient Greek, **Applied Mathematics**, Art, Biology, Bulgarian, **Business**, Chemistry, Computer Science, Construction Studies, Croatian, Czech, Danish, Dutch, Economics, **Engineering**, **English**, Finnish, **Geography**, History, **Home Economics S & S**, Hungarian, Latin, Latvian, Lithuanian, Maltese, Mathematics, Modern Greek, Physical Education, Physics, Physics & Chemistry, Portuguese, Religious Education, Romanian, Slovakian, Slovenian, **Swedish**, **Technology**, **Agricultural Economics**

> Wave 9 (2026-06-13): SHORT-ANSWER CROP TIER — per-question tight Y-band crops where scheme answers pack ~3/page. **Technology** HL+OL 2010–2025, **Swedish** HIGHER (reading comprehension), **Agricultural Economics** HL{2010,2015,2019}+OL{2018,2019}. Languages (Spanish/German/Japanese/Russian/French/Polish) dropped by skeptics as aural/coincidental; Italian dropped (section-restart numbering).

> Wave 8 (2026-06-13): per-paper agent-verified subsets. **Applied Mathematics** HL+OL 2010–2022 (clean `N.` worked solutions). **Home Economics** HL+OL 2020–2025 (Section B Q1–5). **English** HIGHER Paper 2 only (2010, 2012–2016 — literature: grade bands + indicative-material lists per essay question; P1 comprehension/composition not mappable). **Accounting** HL 2018 + OL (worked-solution tables w/ per-line marks). **Business** HIGHER Section 1 short-answer (2020–2022) + 2020 long booklet; the other long booklets reuse Section-1 coords and are dropped. Engine gained colon-marker (`QUESTION 1:`) + centered standalone `QUESTION N` header detection.

> Wave 7 (2026-06-13): **Geography** lights the **Part Two** structured/essay booklet (P043) only — Q1–12, HL+OL, 2020–2025 (the modern split-booklet format). The Part One short-answer answerbook collapses onto a 1-page scheme key and is deliberately dropped, and pre-2020 single-booklet years anchor on the cover. **Engineering** lights HL {2015, 2021–2025} and OL {2010, 2011, 2013–2016, 2018, 2019, 2021, 2023–2025}; the dropped years have a scheme summary-table that bleeds into the count and are dropped rather than mis-mapped. Engine gained ligature-mojibake normalisation (`QuesƟon`→`Question`), a short-answer↔structured grammar guard, paper/scheme spread guards (kills chip-on-cover + short-answer-key collapse), and a header-anchored last-question crop that stops at the practical-marking-scheme appendix.

### ⛔ Not text-mappable (4) — feature cannot apply
- Design & Communication Graphics — visual/drawing (DCG). Confirmed 2026-07-07 against the 2025 HL scheme: there is NO
  short-answer Section A — the Section A paper (LC562ALP014EV) is a 3-page draw-on answer booklet (cover + return
  notice + Section C contour-map insert) with no text-anchorable question headers, and Section B&C are drawing sheets.
  The paper side has nothing to anchor a chip to, so the feature can't apply. (Nuance for a future wave: the scheme
  itself DOES carry per-question text — pp4–13 itemised mark breakdowns "Question A-1…C-5" plus graphical solution
  sheets pp15–24 — the blocker is the paper side, not the scheme.)
- Hebrew Studies — scheme carries only generic marking guidance (how parts (a)/(b)/(c)
  are marked), zero question-specific answers; verified against HL 2019, HL 2018, OL 2015.
  Anchoring paper questions onto generic guidance would present non-answers as answers — drop.
- Irish — Irish-medium paper, no EV
- Mandarin Chinese aural papers — aural/listening (the WRITTEN papers' reading section ✅
  maps: P2C wave 2025 HL+OL, 2024 HL)
- Office Admin And Customer — no EV pair (LC Office Admin)

### 🔧 Bespoke / short-answer page-jump tier (19) — under verification
_Wave 9: Technology + Agricultural Economics now generate per-question page-jump maps (short-answer key); under adversarial verification along with the languages (checked for aural/coincidental mismaps)._
- Arabic — ✅ sidecars ready (P2C wave: 2025 HL, 2024 HL, 2023 OL). The "no scheme markers"
  diagnosis was wrong: schemes are per-question RTL table blocks keyed by English number-words
  ("One"…"Fifteen", sub-parts أ/ب/ج), verified page-by-page; remaining 28 papers need the same
  per-paper verification
- Classical Studies — ✅ LIVE (wave 10, new-spec 2023–2025 HL+OL): Section A `N.` markers + common essay rubric
- Estonian — ✅ sidecars ready (P2C wave: 2025, 2019, 2016). "Scheme-grouped answers" diagnosis
  was wrong: HINDAMISJUHEND numbers every I ÜLESANNE answer 1–6; II/III (writing) skipped
- French — language
- German — language
- Hebrew Studies — moved to ⛔ (scheme has no question-specific answers; see above)
- History (Early Modern) — ✅ sidecars ready (P2B wave 2026-07-07, `hem_history.py`: HL EV 2021–2022, the only years
  with a scheme in the corpus). The "wrong scheme-file pairing" diagnosis was wrong: the SEC publishes ONE combined
  History scheme per level/year (Later Modern half then Early Modern half) and the LC096 scheme uploads are
  byte-identical to the LC004 ones — correct pairing. The generic engine still can't map it (first-hit markers land in
  the Later Modern half = wrong field of study), so the bespoke generator pins the band to the "Early Modern" divider
  page and maps the 4 DBQ questions, mirroring shipped LC004 HL coverage. QA: crops match each paper's case study
  (2021 Jesuit mission in China, 2022 Meiler Magrath); `verify_all.py LC096` 8/8 OK. Drops: OL 2021–2022 (the OL scheme
  repeats a compact 1.–4. "four parts" instruction list right before the real DBQ answers → first-marker banding
  ambiguous; mainstream History OL is unshipped for the same reason), IV (out of EV scope)
- Italian — language off-by-one
- Japanese — language
- Link Modules — ✅ sidecars ready (P2B wave 2026-07-07, `link_modules.py`: ALL 16 EV years 2010–2025, 277 questions;
  2016/2017 papers live under the letter-O fileid `LC462CLPO00EV.pdf`). The needed grammar: Sections A/B/C each restart
  Q.1–Q.N and the scheme mirrors the same `Q.n` blocks (mostly echoing the question text verbatim). Chips carry
  `label: "Section X · Q n"` with globally sequential `n` (like the shipped language sidecars). Paper anchors pick the
  marker PASS spanning the most pages (menu list and pre-2018 examiner marks grid each collapse onto 1–2 pages);
  scheme pages where a section's numbering restarts (2019's embedded Section C menu) are blacklisted. QA: automated
  paper-text↔crop-text word-overlap across all 277 questions (4 low-overlap flags manually verified correct — stimulus
  vs sub-question phrasing); label-aware `verify_all.py LC462` 274 OK / 3 flags, each an extraction artifact
  ("Q. 8" spaced marker / block-order clip) verified correct by the text echo. Drops: IV (out of EV scope); the 2016
  Case Study stimulus booklet has no questions/scheme of its own
- Music — off-by-one/partial
- Polish — language
- Politics and Society — ✅ LIVE (wave 10, HL+OL EV): Section A/B per-Q blocks + shared Section C essay criteria
- Russian — language
- Spanish — language section-restart numbering
- Swedish — non-monotonic Q1-after-Q6
- Ukrainian — ✅ sidecar ready (P2C wave: 2025 HL, the subject's only paper — ЧАСТИНА I Q1–6;
  ЧАСТИНА II/III writing skipped)

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
- Graphics — visual (Graphics). Confirmed 2026-07-07 against the 2025 scheme: the answer pages are annotated DRAWING
  solutions with mark stamps ("Q1 (a) 2 2 2 2 (4 x 2 marks)") — per-question "Page N – Question N" headers exist, but
  the content is graphical, not a readable text answer; correctly classified
- Irish T1 — Irish T1, no EV
- Irish — Irish-medium, no EV
- Material Technology (Wood) — old-spec, no clean index id
- Metalwork — practical (Metalwork)
- Technical Graphics — visual (Technical Graphics)

### 🔧 Bespoke grammar needed (10) — deferred (wrong-answer risk if rushed)
- Ancient Greek — pre-window (filtered from index)
- Civic Social and Political Education — partial
- Environ & Social Studies — reconcile 4/14
- French — ✅ sidecars ready (P2C wave: 2025, 2024 EV — Section B reading Q8–14; numbering is
  continuous across sections so the old chips-on-instructions failure does not recur with
  explicit Q-anchors; listening + writing skipped)
- German — language 20/21
- History — ✅ sidecars ready (P2B wave 2026-07-07, `jc_history.py`: all 4 EV years 2022–2025, 32 questions). The
  "DBQ/essay" diagnosis is stale for the new-spec Junior Cycle scheme: every answer page carries a left-margin "Q N"
  table stamp and the paper has clean "Question 1..8" headers, so each question's answer is the contiguous page RUN
  stamped with its number (runs must tile the answer band or the paper drops). QA: all 32 crops open with the (a)
  sub-question matching the paper's topic verbatim; `verify_all.py JC004` shows NOMARK (the spaced "Q N" stamp is
  invisible to its detectors) — eyeballed via the generator's text echo instead. Drops: IV (out of EV scope)
- Italian — ✅ sidecars ready (P2C wave: 2025, 2024 EV — Section B reading Q9–15 via `Q.N`
  scheme markers; listening + writing skipped)
- Latin — needs per-subject grammar
- Spanish — language
- Technology — clustered/garbled last Q

## Leaving Cert Applied

### ✅ Live (12)
Agriculture / Horticulture, Childcare / Community Care, Crafts & Design, English and Communications, French, German, Hair And Beauty, Hotel / Catering & Tourism, Information & Communication Tech., Italian, Office Admin And Customer, Sign Language

### ⛔ Not text-mappable (8) — feature cannot apply
- Contemporary Issues Task — portfolio Task (no exam)
- Gaeilge Chumarsáideach — Gaeilge, no EV
- General Education Task — portfolio Task
- Intro. to Information & Comm. Technology — no EV pair
- Personal Reflection Task — portfolio Task
- Practical Achievement Task — portfolio Task
- Vocational Education Task — portfolio Task
- Vocational Preparation Task — portfolio Task

### 🔧 Bespoke grammar needed (7) — deferred (wrong-answer risk if rushed)
- Active Leisure Studies — needs per-subject grammar
- Engineering — ✅ sidecars ready (CV2 wave 2026-07-07, `lca_engineering.py`: ALL 14 EV scheme years
  2011–2019 + 2021–2025, 12 chips each = 168 regions; manifest `publish/cv2-upload.tsv`). The old "visual/drawing"
  record was WRONG — it is a WRITTEN 240-mark exam whose scheme is an answered copy of the paper: Section 1 Q1–Q3,
  Section 2 Q4–Q7, plus Q7's five choose-two topic pages "Q7 (a)"–"Q7 (e)" mapped as labelled chips (n=8–12). The
  page grammar is identical every year ("Section N  Qn." fused marker lines; 2025 splits them, 2013 splits the
  topic name — both handled); count reconcile = exact Q1..Q7 + topics (a)..(e) on both sides with topic-NAME
  string match, else drop. QA: per-chip paper↔crop text echo matches on all 168 chips; `verify_all.py LB836`
  = OK=168 MISMATCH=0 NOMARK=0. Drops: none (2010 has no scheme, 2020 not sat — not in scope). IV papers have
  no scheme pair
- Graphics And Construction Studies — project marking-criteria, not per-Q
- Mathematical Applications — page-header framing
- Social Education — Q15->Q12 mismatch
- Spanish — ✅ sidecars ready (P2C wave: 2025, 2024, 2023 EV — Section 2 reading/written-exercise
  Q1–6 with exact scheme answers; Section 1 aural skipped; IV papers have no scheme pair)
- Technology — Q1 "Answer any Ten" instructions

## Aural audio (probe, 2026-07-07)

**FEASIBLE-AFTER-CREDS, not before.** The index already carries aural question
booklets (368 across 11 languages) but no audio: the v1 harvest deliberately
skipped .mp3 assets and the manifest holding their fileids was never committed
(out/ is gitignored). examinations.ie now serves a Cloudflare interactive
challenge to non-browser requests, so neither re-enumeration nor deep-linking
is possible from CI; file-level deep links also have no precedent in the app
and unverifiable stability. Route when credentials + a harvest path exist:
re-enumerate the 11 aural languages' mp3 fileids → download → upload under
papers/{cycle}/{sid}/{year}/audio/ → PaperItem gains optional audio doc →
a small <audio> bar in the Viewer beside the aural booklet, same © SEC
attribution. Sizing note: several hundred exam-length mp3s = real Storage/
egress cost; size it from the recovered manifest first.
