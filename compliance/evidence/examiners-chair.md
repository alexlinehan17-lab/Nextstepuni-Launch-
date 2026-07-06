# Evidence Dossier — The Examiner's Chair (Launchpad)

**Tool:** `examiners-chair` (`components/ExaminersChair/`)
**Content data:** `data/examinersChair/{types,business,maths,index}.ts`
**Review date:** 2026-07-06
**Reviewer:** Pre-accreditation fact review (ahead of DCU / Brian MacCraith)
**Governing rule:** Every marking rule, mark value, scale and credit descriptor
presented as *real* is stated only where a primary SEC document supports it, cited on
the session that uses it. Questions, cases and sample scripts are **authored for the
exercise** and are labelled as such both in the data (`questionNote` on every session)
and in-app (home-screen footnote) — they are never presented as real SEC questions or
real candidates' work. Where a script is claimed to embody a documented candidate
behaviour, that claim carries its own citation (`embodies.cite`).

The sources are official SEC marking schemes and Chief Examiner's Reports — exam
marking rules are administrative facts, so verification is against the SEC documents
held in `/examiner-reports/` (each itself indexed with PDF + markdown + insights),
not CrossRef/DOI records.

A content-integrity test suite (`test/examinersChair.test.ts`) machine-checks the
hand-authored data on every CI run: grid keys award 0 or the full criterion value and
cover every criterion; scale ladders are strictly increasing with resolvable keys;
every session, grid, scale and embodied-insight citation is non-empty.

---

## Verified sources (all held in /examiner-reports/)

| Key | Source | Location | Verification |
|-----|--------|----------|--------------|
| MS-B-2025 | SEC Business HL marking scheme 2025 | `examiner-reports/business/2025-marking-scheme.{pdf,md}` + `2025-insights.md` | SEC-published finalised scheme; grids and rules below quoted/derived from the document held in-repo. |
| CER-B-2015 | Chief Examiner's Report, Business 2015 | `examiner-reports/business/2015-chief-examiner.{pdf,md}` + `2015-insights.md` | SEC-published report; behavioural findings cited by page. |
| MS-M-2023 | SEC LC Mathematics marking scheme 2023, Ordinary Level (Paper 2 portion) | `examiner-reports/maths/2023-marking-scheme-ol-p2.{pdf,md}` + `2023-insights.md` | SEC-published finalised scheme (mirrored copy retrieved 2026-07-05, filed per the examiner-reports process); scale system and rules below quoted from pp.[28]–[35]. |
| CER-M-2015 | Chief Examiner's Report, Mathematics 2015 | `examiner-reports/maths/2015-chief-examiner.{pdf,md}` + `2015-insights.md` | SEC-published report; behavioural findings cited by page. |
| MS-E-2025 | SEC LC English HL marking scheme 2025 | `examiner-reports/english/2025-marking-scheme.{pdf,md}` + `2025-insights.md` | SEC-published scheme (mirrored copy retrieved 2026-07-06); PCLM weightings and rules quoted by page. |
| CER-E-2013 | Chief Examiner's Report, English 2013 | `examiner-reports/english/2013-chief-examiner.{pdf,md}` + `2013-insights.md` | SEC-published report (latest for English); behavioural findings cited by page. |
| MS-BIO-2023 | SEC LC Biology HL marking scheme 2023 (Deferred sitting) | `examiner-reports/biology/2023-marking-scheme.{pdf,md}` + `2023-insights.md` | SEC-published scheme; general conventions are the SEC standard framework (identical across sittings), only per-question answers are paper-specific. |
| MS-GEO-2025 | SEC LC Geography HL marking scheme 2025 | `examiner-reports/geography/2025-marking-scheme.{pdf,md}` + `2025-insights.md` | SEC-published scheme; SRP system and rules quoted by page. |
| CER-GEO-2012 | Chief Examiner's Report, Geography 2012 | `examiner-reports/geography/2012-chief-examiner.{pdf,md}` + `2012-insights.md` | SEC-published report (latest for Geography); behavioural findings cited by page. |
| MS-IR-2025 | SEC LC Irish HL marking scheme 2025 (written papers) | `examiner-reports/irish/2025-marking-scheme.{pdf,md}` + `2025-insights.md` | SEC-published scheme; composition/comprehension rules quoted by page. Oral (Béaltriail) is a separate scheme, not covered. |
| MS-FR-2025 | SEC LC French HL marking scheme 2025 | `examiner-reports/french/2025-marking-scheme.{pdf,md}` + `2025-insights.md` | SEC-published scheme; two-axis and comprehension rules quoted by page. |
| MS-CHEM-2024 | SEC LC Chemistry HL marking scheme 2024 | `examiner-reports/chemistry/2024-marking-scheme.{pdf,md}` + `2024-insights.md` | SEC-published scheme; exact-term, Mr and // rules quoted by page. |
| CER-CHEM-2013 | Chief Examiner's Report, Chemistry 2013 | `examiner-reports/chemistry/2013-chief-examiner.{pdf,md}` | SEC-published report (latest for Chemistry); behavioural findings cited by page. |
| MS-PHY-2025 | SEC LC Physics HL marking scheme 2025 | `examiner-reports/physics/2025-marking-scheme.{pdf,md}` + `2025-insights.md` | SEC-published scheme; granule/unit/slip rules quoted by page. |
| MS-HIS-2025 | SEC LC History HL marking scheme 2025 | `examiner-reports/history/2025-marking-scheme.{pdf,md}` + `2025-insights.md` | SEC-published scheme; CM/OE system and caps quoted by page. |
| MS-ACC-2024 | SEC LC Accounting HL marking scheme 2024 | `examiner-reports/accounting/2024-marking-scheme.{pdf,md}` + `2024-insights.md` | SEC-published scheme; workmark, balancing and own-figure rules quoted by page. |

**Levels.** Each session is tagged with the level whose scheme its rules are verified
against. Sessions tagged `common` teach a marking convention the cited source states
applies across levels (e.g. the Maths A–D scale system, English PCLM, Biology's points
conventions) — these legitimately serve every level a subject offers. Level-specific
mark allocations are pinned to their own level. Every subject carries an in-app
`coverageNote` stating which levels have level-specific sessions yet.

---

## Claim-by-claim record — Business sessions

### B1 `biz-theory-link` — grid 2@5 (2+2+1) Name + Explain + Link
- **Grid:** the SEC 2025 ABQ Part (A) template is 4@5 (2+2+1) Name + Explain + Link
  (MS-B-2025 p.5–6). The session uses the per-point template verbatim, shortened to two
  points, and says so in `questionNote`.
- **Link rule:** links must be a direct relevant quote/phrase from the case; separate
  links required per section; "No link awarded without relevant theory" (MS-B-2025 p.6
  — the six-word quote is reproduced; all other phrasing is ours).
- **Embodied behaviours:** Script A = theory with no reference to the ABQ; Script B =
  ABQ treated as a comprehension piece and rewritten. Both are the Chief Examiner's two
  named ABQ failure modes (CER-B-2015 p.15). Script C embodies the separate-links rule
  (MS-B-2025 p.6).

### B2 `biz-list-rule` — grid 8m (3, 3, 1, 1)
- **Grid:** the 2025 scheme marked "List four grounds" at (3, 3, 1, 1) (MS-B-2025 p.8,
  Q1(C)(ii) grid).
- **Embodied behaviour:** Script A writes paragraphs explaining grounds where naming
  was required — flagged verbatim in CER-B-2015 p.17.
- **Factual content:** the discrimination grounds listed (age, disability, religion,
  race, civil status, family status, sexual orientation, membership of the Traveller
  community) are the statutory grounds of the Employment Equality Acts (excluding
  gender as the question stem does). Statutory fact, uncontroversial.

### B3 `biz-precision` — grid (3+2)(3+2)
- **Grid:** the (3+2)(3+2) two-developed-points template is used across the 2025
  Section 1 short-response questions (MS-B-2025 p.4).
- **Embodied behaviours:** Script A gives "telling the truth" for utmost good faith —
  the exact weak paraphrase flagged in CER-B-2015 p.19 ("disclosing all material
  facts" required); Script B gives valid but undeveloped one-liners — the brevity
  barrier (CER-B-2015 p.20).
- **Factual content:** definitions of utmost good faith and insurable interest are
  standard insurance principles; the "material facts" phrasing follows the CER's own
  correction.

### B4 `biz-evaluate` — grid 1@7 (1+2+1+3)
- **Grid:** the SEC 2025 ABQ Part (B)(i) template is 4@7 (1+2+1+3) Name + Explain +
  Link + Evaluate, evaluation being the heaviest single component (MS-B-2025 p.6);
  session shortened to one point, labelled.
- **Embodied behaviours:** Script A stops after the link (candidates who "do not
  evaluate at all"), Script B gives an unjustified verdict ("very superficial"
  evaluations) — both CER-B-2015 p.17.

### B5 `biz-workings` — grid 5@1m
- **Grid:** the 2025 Q7 Debt/Equity ratio was marked as five distinct 1-mark points
  (identify debt; identify equity = issued + reserves; substitute; calculate; express
  as ratio), with a bare answer capping at 1 mark (MS-B-2025 p.5).
- **Figures:** authored (loan €400k, issued €700k, reserves €100k, authorised €1,000k →
  0.5:1; wrong-path 400/1,100 ≈ 0.36:1). Arithmetic hand-verified.
- **Embodied behaviours:** Script A bare answer (grid cap, MS-B-2025 p.5); Script B
  uses Authorised instead of Issued capital — the documented misconception on this
  ratio (MS-B-2025-insights, Misconceptions).

### B6 `biz-chart` — grid 25m with calculations-only cap
- **Grid:** the 2025 Q8(C) breakeven chart grid: Title 2m, axes 1+1m, fixed-costs line
  3m, total-costs line 3m, total-revenue line 3m, BEP 4m, profit at forecast output 4m,
  margin of safety 4m; calculations only capped at 12m (MS-B-2025 p.11).
- **Embodied behaviours:** Script A calculations-only (the 12/25 cap, MS-B-2025 p.11);
  Script B unlabelled/untitled chart (CER-B-2015 p.18: marks lost for failing to label
  and title charts).

---

## Claim-by-claim record — Mathematics sessions

### Scale system (all sessions)
- Scales A–D, category counts, and the mark ladders used (10C = 0, 4, 6, 10;
  15D = 0, 5, 8, 12, 15) are quoted from the scheme's "Structure of the marking
  scheme" table (MS-M-2023 p.[28]).
- Credit-level descriptors ("response of no substantial merit", "response with some
  merit", "response about half-right", "almost correct response", "correct response")
  are the scheme's own (MS-M-2023 p.[28]).
- Margin annotations (L, M, H, F✱, tick, cross) are from the scheme's examiner
  annotation palette (MS-M-2023 p.[30]).

### M1 `maths-ladder` — Scale 10C
- **Rules:** "a correct relevant formula written is regarded as Work of merit, award
  the lowest non-zero level of credit"; the default that an unsupported answer earns
  the lowest non-zero credit; and the question-specific note pattern "Full credit:
  correct answer without supporting work" — all MS-M-2023 p.[29] and p.[31] (Q1(a)
  notes). High-partial descriptors ("correct formula fully substituted"; "error(s) in
  substitution but finishes correctly") from the same notes.
- **Question:** authored (distance A(2,1)–B(8,9) = 10; arithmetic verified). Script B's
  deliberate slip (64 written as 46 → √(36+46) = √82 ≈ 9.06) is arithmetically
  consistent as authored — the "error in substitution, finishes correctly" case.
- **Embodied behaviour:** Script B perseveres after an error — the HL perseverance
  contrast (CER-M-2015 p.20).

### M2 `maths-steps` — Scale 15D, steps → ladder
- **Rules:** the 2023 scheme marked its line-meets-circle question by enumerating four
  solution steps and mapping Low = some work of merit, Mid = two steps, High = three
  steps (MS-M-2023 p.[35], Q2(b) notes).
- **Question:** authored (y = x + 1 into x² + y² = 25 → (3,4) and (−4,−3); verified:
  9+16 = 25, 16+9 = 25).
- **Embodied behaviour:** Script C computes but does not answer the question asked
  (points, not x-values) — conclusion-drawing pattern (CER-M-2015 p.22).

### M3 `maths-conclusion` — Scale 10C + Full Credit −1
- **Rules:** the marking note "Full Credit (−1): No conclusion" on the point-on-circle
  verification (MS-M-2023 p.[34], Q2(a)(ii)); Full Credit −1 definition (p.[29]).
- **Question:** authored (verify (−3,4) on x² + y² = 25; 9+16 = 25 ✓). Script C's sign
  error ((−3)² as −9 → 7 ≠ 25) is finished consistently with its stated (wrong)
  conclusion — keyed high partial per the "error…finishes correctly" descriptor.

### M4 `maths-star` — Full Credit −1 traps
- **Rules:** Full Credit −1 for incorrect rounding / omitted units / non-oversimplifying
  misreads; rounding penalty applied each occurrence; no unit penalty when the question
  specifies the unit (MS-M-2023 p.[29]).
- **Question:** authored (area, r = 3.7 m → π×13.69 = 43.0084… → 43.01 m²; verified).
  Script A truncates to 43.00 → F−1.
- **Embodied behaviour:** rounding as a routine skill that should be developed to a
  high standard (CER-M-2015 p.30).

---

## Claim-by-claim record — English sessions (level: common — PCLM applies to every task, both papers, both levels)

### E1 `eng-purpose-cap` — the primacy-of-Purpose cap
- **Rules:** PCLM criteria and 30/30/30/10 split (MS-E-2025 p.3); the rule that Coherence
  and Language "cannot exceed the marks awarded for Clarity of Purpose" (MS-E-2025 p.3).
- **Scenario:** authored — a fluent but off-question Single Text answer with provisional
  Purpose 9/18, Language 18/18; the cap forces Coherence to 9. The arithmetic of the cap
  is a direct application of the stated rule.
- **Embodied behaviour:** fluent writing that does not engage the question (a low-Purpose
  profile) — the "knowledge/style managed to the question" theme (CER-E-2013 p.11, p.13).

### E2 `eng-unseen-poem` — the compulsory Unseen Poem
- **Rules:** the Unseen Poem is a compulsory 20-mark section (Poetry = Unseen 20 +
  Prescribed 50); no single "correct" reading, a supported personal response scores
  (MS-E-2025 p.42).
- **Embodied behaviour:** skipping the compulsory section, "a loss of up to twenty marks",
  and it being HL's lowest-scoring element (CER-E-2013 p.8–9, Table 4 p.7).

### E3 `eng-evidence` — evidence as the discriminator
- **Rules:** Comparative marked on PCLM (MS-E-2025 p.35); "the quality of evidence cited
  to support an opinion was a significant discriminator" and careless quotation
  undermines answers (CER-E-2013 p.18, p.8).
- **Scenario + scripts:** authored; the grid criterion is whether the reference actually
  supports the point (binary), teaching the discrimination the report describes.

## Claim-by-claim record — Biology sessions (level: common — general conventions apply HL and OL)

### BIO1 `bio-context` — the context rule
- **Rules:** points-based marking (3m per point here); a key term scores only in a
  correct statement (MS-BIO-2023 p.3–4). Synonyms accepted unless an exact term is
  demanded (p.3).
- **Scenario + scripts:** authored (osmosis into a root hair cell). Script A's osmosis
  statement reverses the gradient (soil water is higher), so the correct term sits in a
  false statement → 0, per the context rule.

### BIO2 `bio-surplus` — the Section A surplus penalty
- **Rules:** "A surplus wrong answer cancels the marks awarded for a correct answer"
  (Section A) (MS-BIO-2023 p.4–5).
- **Scenario:** authored — "Cellulose, glycogen" for structural carbohydrates. Cellulose
  is structural (3m); glycogen is a storage carbohydrate → surplus wrong answer → cancels
  → net 0. (Biology fact: cellulose is a structural polysaccharide; glycogen is a storage
  polysaccharide — standard, uncontroversial.)

### BIO3 `bio-asterisk` — the asterisk nullification (Sections B/C)
- **Rules:** for single-term answers, an added wrong alternative nullifies the correct
  one; such cases are flagged with * (MS-BIO-2023 p.5).
- **Scenario:** authored — "Carbon dioxide or lactic acid" for yeast anaerobic
  respiration. CO₂ is correct; lactic acid is the wrong (muscle) fermentation pathway;
  the hedge nullifies → 0. (Biology fact: yeast fermentation yields ethanol + CO₂; lactic
  acid fermentation is the animal-muscle pathway — standard.)

## Claim-by-claim record — Geography sessions (level: higher — SRP counts are HL-specific; system also governs OL)

### GEO1 `geo-srp` — what counts as an SRP
- **Rules:** an SRP is "a single piece of factual information" assigned a mark weighting,
  typically 2 marks (MS-GEO-2025 p.3); landform grid "Landform named 2 marks /
  Examination 14 × SRPs" (p.9).
- **Scenario + scripts:** authored; non-factual warm-up/opinion sentences score 0 SRPs,
  specific formation facts score 2 — the definition applied.

### GEO2 `geo-diagram` — the diagram rule
- **Rules:** a labelled diagram earns 1 SRP; "Diagram without labelling 0 marks"
  (MS-GEO-2025 p.6–14, recurring).
- **Scenario:** authored — an accurate but unlabelled diagram → 0.

### GEO3 `geo-wrong-process` — answer the question asked
- **Rules:** "Examination of processes of erosion 0 marks" where deposition was required
  (MS-GEO-2025 p.9).
- **Scenario:** authored — a detailed waterfall (erosion) answer to a deposition question
  → 0 for the examination. **Embodied behaviour:** the documented waterfall/deposition
  mismatch, "awarded no marks" (CER-GEO-2012 p.25).

### GEO4 `geo-coherence` — the graded Overall Coherence mark
- **Rules:** Options essays carry a graded Overall Coherence mark of 20, descriptors
  Excellent 20 / Very Good 17 / Good 14 / Fair 10 / Weak 6 / Poor 0 (MS-GEO-2025 p.47).
- **Scenario:** authored — unordered, topic-not-question facts land ~Weak (6).
  **Embodied behaviour:** "banks of knowledge" not shaped to the question (CER-GEO-2012
  p.30).

**Note on volatility (English & Geography schemes):** both 2025 schemes carry the SEC
caveat that details "are subject to change from one year to the next without notice"
(MS-E-2025 p.2; MS-GEO-2025 p.2). The rules used here are structural conventions (PCLM,
the SRP system, Overall Coherence) that are stable year to year; if a future scheme
changes them, the affected sessions and this dossier are updated together.

## Claim-by-claim record — Irish sessions (level: common — written-paper conventions, HL and OL)

- **IR1 `ir-cumas-gaeilge`:** composition = Stíl 5 + Ionramháil 15 + Cumas Gaeilge 80;
  language command is 80 of 100 marks, judged on range and accuracy (MS-IR-2025 p.13).
  Scenario: strong ideas / weak Irish sits in the lower Cumas Gaeilge band.
- **IR2 `ir-genre`:** Stíl marks genre discipline; wrong genre for the title → Stíl 0
  (MS-IR-2025 p.14). Scenario: a speech title answered as an essay.
- **IR3 `ir-own-words`:** comprehension Q6(b) is 12 marks and must be in the candidate's
  own words; a verbatim lift scores 0 (MS-IR-2025 p.16).

## Claim-by-claim record — French sessions (level: common — written-production conventions)

- **FR1 `fr-two-axes`:** written production is marked on two independent, equally weighted
  axes (Communication + Language) summed; "mere transcription … very poor treatment of
  the stimulus" is the Bottom Communication descriptor (MS-FR-2025 p.15–16). Scenario:
  flawless-but-transcribed French → Bottom Communication.
- **FR2 `fr-manipulation`:** comprehension tags questions "manipulation required"; a raw
  lift where manipulation is required is docked on the 5/4/3/2/1/0 ladder — «il a parlé»
  = 4, «j'ai parlé» = 5 (MS-FR-2025 p.13).
- **FR3 `fr-hedge`:** "If more than one answer offered = 0 Marks" (MS-FR-2025 p.6, p.12).

## Claim-by-claim record — Chemistry sessions (level: common — general conventions, HL and OL)

- **CH1 `chem-exact-term`:** exact-term demands enforced inline with "[do not accept …]";
  "clear" for "colourless" is rejected (MS-CHEM-2024 p.6; the recurring error is in
  CER-CHEM-2013 p.24).
- **CH2 `chem-mr`:** an Mr arithmetic slip is only −1 if the atomic-mass addition is
  shown; otherwise full Mr marks are lost (MS-CHEM-2024 p.3, point 7).
- **CH3 `chem-solidus`:** "//" separates mutually exclusive methods; "a partial answer
  from one side … may not be taken in conjunction with a partial answer from the other"
  (MS-CHEM-2024 p.3, point 3). (Chemistry example figures — Mr of CO₂ = 44, "should be
  46" for a different compound — are illustrative; the scheme rule, not a specific Mr, is
  what is cited.)

## Claim-by-claim record — Physics sessions (level: common — numerical-marking conventions, HL and OL)

- **PHY1 `phy-granules`:** numerical answers are a ladder of independent granules
  (formula / substitution / answer), each ~3 marks; the formula banks its granule alone
  (MS-PHY-2025 p.6–8). Scenario arithmetic (512 × 0.65 = 332.8) verified.
- **PHY2 `phy-unit`:** omitting/mis-writing units on a final answer = −1 (MS-PHY-2025 p.3,
  instruction 6).
- **PHY3 `phy-slip`:** each arithmetical slip = −1; downstream steps using the slipped
  value still score (error carried forward) (MS-PHY-2025 p.3, instruction 8).

## Claim-by-claim record — History sessions (level: higher — verified against the HL scheme)

- **HIS1 `his-cm-oe`:** essays marked 60/40 — Cumulative Mark (content) + Overall
  Evaluation (quality); OE rewards analysis, marshalled evidence, a conclusion; narrative
  caps in lower OE bands (MS-HIS-2025 p.12, p.14).
- **HIS2 `his-two-element`:** two-element titles carry "If only ONE, Max. CM = 50"
  (MS-HIS-2025 p.15–18).
- **HIS3 `his-dbq-compare`:** DBQ comparison "Answer referring to one document only = 5M
  max" (MS-HIS-2025 p.8–9).

## Claim-by-claim record — Accounting sessions (level: higher — verified against the HL scheme)

- **AC1 `acc-workings`:** workmark system — each adjusted figure is awarded through its
  numbered working (N-note); a bare wrong figure can't part-score, a shown working banks
  each correct step (MS-ACC-2024 p.3, p.5). Scenario adjustments arithmetic verified.
- **AC2 `acc-balance`:** the Balance Sheet's "Both totals correct *" is a discrete
  losable mark, independent of the line figures (MS-ACC-2024 p.4, p.27).
- **AC3 `acc-transfer`:** own-figure marking — an error is penalised once where it
  happens; a correct transfer of the candidate's own (wrong) figure earns the transfer
  marks; a non-transfer earns half (MS-ACC-2024 p.18, p.34).

**Volatility note (all subjects):** each scheme is the finalised scheme for its stated
year. The rules used are structural conventions stable year to year; if a future scheme
changes one, the affected session and this dossier are updated together.

---

## Honesty measures (in-app)

1. Every session's `questionNote` states the question/case/scripts are authored and
   names the real SEC template or note they are modelled on.
2. The home screen carries a permanent footnote: questions and scripts are written for
   the exercises; the grids, scales and credit rules are the real ones, cited per
   session.
3. Citations render on the session intro (grid/scale), on each revealed "documented
   pattern", and on every codex rule.
4. The calibration metric ("agreement") measures match with the authored key — it is
   presented as marking-judgement practice, never as a predictor of exam performance.

## Pedagogical basis

The tool is an application of self-assessment / rubric-internalisation practice: the
already-verified references in `compliance/evidence/marking-scheme-decoder.md` and the
teaching-effect record in `compliance/evidence/teaching-effect.md` cover the adjacent
claims the app makes elsewhere. This tool's own copy makes **no research claims** — its
claims are exclusively about how SEC marking works, each cited above.

## Scope & expansion protocol

Current coverage: **English, Mathematics, Business, Biology, Geography.** Per the product
direction (2026-07-06), the tool expands to **every applicable subject at Higher,
Ordinary and Foundation level (where the subject offers it)**. Protocol for each new
subject/level: (1) obtain the SEC marking scheme / Chief Examiner's Report, (2) file it
into `/examiner-reports/` (PDF + md + insights per the CLAUDE.md process), (3) author
sessions citing only rules the document supports, tagged with the verified level (or
`common` where the cited rule is a documented cross-level convention), (4) extend this
dossier in the same change. Subjects/levels for which no verifiable scheme can be
obtained are skipped and recorded here with the reason.

**Remaining subjects to add** (loop in progress): Irish, French/German/Spanish, History,
Chemistry, Physics, Accounting, Economics, Home Economics, Art, and the remaining LC
subjects — plus level-specific (OL/Foundation) worked examples for the subjects already
covered by shared conventions.
