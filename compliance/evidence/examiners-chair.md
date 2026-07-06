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

## Claim-by-claim record — tranche 4 subjects (practical / newer subjects)

Each source is the SEC marking scheme for its stated year, filed in
`/examiner-reports/<subject>/`.

- **Construction Studies** — MS-CS-2025 (`construction-studies/2025-marking-scheme`):
  CS1 `cs-labels` element draw(3)+annotation(1) split (p.37); CS2 `cs-sketch` note(3)+
  sketch(3) split (p.38); CS3 `cs-uvalue` per-step U-value marking (p.41).
- **Engineering** — MS-EN-2025 (`engineering/2025-marking-scheme`): EN1 `en-anyn` the
  "Any N" best-N cap (p.20); EN2 `en-headline` the 3+2 point+development split (p.7);
  EN3 `en-labels` separately-credited diagram labels 8+1+1 (p.16).
- **DCG** — MS-DCG-2025 (`dcg/2025-marking-scheme`): DCG1 `dcg-construction` construction
  (8) marked above the finished curve (4) (p.4); DCG2 `dcg-steps` independently-scored
  drawing steps (p.4); DCG3 `dcg-method` standalone "use of appropriate method" marks
  (p.4).
- **Politics & Society** — MS-PS-2025 (`politics-society/2025-marking-scheme`): PS1
  `ps-insight` "relevant but lacking insight" caps in the Good band (p.11); PS2
  `ps-summary` "summary … in the place of discussion" lower-band trap (p.15); PS3
  `ps-documents` split Conclusions/30 + Use-of-documents/20 rubric (p.12).
- **Religious Education** — MS-RE-2025 (`religious-education/2025-marking-scheme`): RE1
  `re-command` descriptive answer to a higher-order command capped at top of Fair (p.18);
  RE2 `re-holistic` four-dimension holistic banding where accuracy sets the band (p.2).
- **Music** — MS-MU-2022 (`music/2022-marking-scheme-deferred`; deferred sitting, grammar
  matches main per SEC note p.2): MU1 `mu-regimes` the two opposite over-answering regimes
  (p.9); MU2 `mu-precision` "partially correct = 1" description cap (p.11); MU3 `mu-chords`
  chords credited only within a good progression (p.7).

### Classical Studies (level: higher) — MS-CL-2025 (`classical-studies/2025-marking-scheme`)
- **CL1 `cl-unit`:** essay "unit of development" = point + evidence + development, 15 per
  unit (p.11). **CL2 `cl-two-part`:** a one-part answer caps units and holds Overall
  Quality in the Low range (~57/80) (p.11). **CL3 `cl-narrative`:** Overall Quality Low
  band = "relies mostly on narrative" (p.11).

### Italian (level: common) — MS-IT-2025 (`italian/2025-marking-scheme`)
- **IT1 `it-content-cap`:** two axes with a graduated cap — content ≤7 → Language out of 5
  (p.26). **IT2 `it-wrong-language`:** −50% for answering in the wrong language where the
  scheme sets it (p.11, p.13). **IT3 `it-rote`:** candidates "must not produce something
  learnt off by heart and off the point" (p.27).

### Art — Visual Studies (level: higher) — MS-ART-2024 (`art/2024-visual-studies-marking-scheme`)
- Authored against the **current revised spec** ("Visual Studies", first examined 2023/24),
  NOT the pre-2022 "History & Appreciation" paper (the 2019 old-spec scheme is filed in the
  same folder for reference but is not the basis for these sessions).
- **ART1 `art-analysis`:** Subject Knowledge High band needs "critical thinking to analyse
  and evaluate", not recall (printed p.22). **ART2 `art-examples`:** Relevant Examples is a
  separable 10-mark strand; vague references cap it (printed p.23). **ART3 `art-headings`:**
  Section A (a) answers are anchored to the paper's given headings (printed pp.17–19).

### LCVP Link Modules (level: common — single common level) — MS-LCVP-2024 (`lcvp/2024-marking-scheme`)
- **LC1 `lcvp-cliff`:** (0/2) all-or-nothing items score 0 for an undeveloped point (p.2).
  **LC2 `lcvp-repetition`:** "no repetition of expansions/points" on the 9-mark closers
  (p.6, p.14). **LC3 `lcvp-apply`:** Section B credit gated on relevance to the named case
  (p.3).

**Uncovered Chief Examiner's Reports:** no recent CER was obtainable for German, Spanish,
Home Economics, Ag Science, Applied Maths, DCG, Construction Studies, Engineering,
Politics & Society, Religious Education or Music (SEC publishes CERs selectively, and
examinations.ie is Cloudflare-gated to automated fetch). Each of those subjects is
grounded in its marking scheme alone; behavioural findings are drawn from the scheme's
own rules, not a cohort report. Where a CER was obtainable it was filed (Business, Maths,
Chemistry, English, Geography).

## Claim-by-claim record — tranche 3 subjects

Each source below is the SEC finalised marking scheme for its stated year, filed in
`/examiner-reports/<subject>/`. Sessions tagged `common` teach a documented cross-level
convention; `higher`-tagged sessions use an HL-specific allocation.

### German (level: common) — MS-DE-2025 (`examiner-reports/german/2025-marking-scheme`)
- **DE1 `de-length-gate`:** the "Lower-E" rule — if content ≤12 or the answer is under
  100 words, Expression is marked out of 18 not 25 (MS-DE p.[20]).
- **DE2 `de-half-lift`:** a quotation given without the required manipulation, or with
  extraneous material, is awarded half marks (MS-DE p.[10]).
- **DE3 `de-tense`:** tense-critical comprehension — a present-tense answer to a
  past-events question scores 0 ("Present Tense = 0", MS-DE p.[5]).

### Spanish (level: common) — MS-ES-2025 (`examiner-reports/spanish/2025-marking-scheme`)
- **SP1 `es-no-lift`:** "No marks will be awarded for phrases taken directly from the
  text" on the written question (MS-ES p.9).
- **SP2 `es-content-gates`:** "Where no marks are awarded for Content … no marks will be
  awarded for Language" — the axes are tied on Q5 (MS-ES p.9).
- **SP3 `es-verbs`:** production units gate full marks on correct verbs ("Verbs must be
  correct for full marks", MS-ES p.10–11).

### Economics (level: higher) — MS-EC-2025 (`examiner-reports/economics/2025-marking-scheme`)
- **EC1 `ec-develop`:** developed points are banded; "repetition of statement" is a
  Weak/0 descriptor (MS-EC p.2).
- **EC2 `ec-diagram-labels`:** diagrams carry itemised marks and the labels are separate
  components (S&D graph, MS-EC p.50).
- **EC3 `ec-workings`:** calculations step-marked; named deduction "Deduct 1 mark for
  omission of %" (MS-EC p.5, p.57).

### Home Economics (level: higher) — MS-HE-2025 (`examiner-reports/home-economics/2025-marking-scheme`)
- **HE1 `he-coarse-ladder`:** 20-mark parts use a 5:3:0 ladder — a thin point scores 0,
  no consolation (MS-HE p.13, p.16).
- **HE2 `he-headings`:** points must be spread across named headings, each capped
  independently (MS-HE p.16).
- **HE3 `he-name-describe`:** the "name" is a low, often all-or-nothing mark; the
  description/evaluation carries the marks (MS-HE p.8).

### Agricultural Science (level: common/higher) — MS-AG-2024 (`examiner-reports/agricultural-science/2024-marking-scheme`)
- **AG1 `ag-frontload`:** front-loaded points list 4 + 2 + 2 + 2 (MS-AG p.4).
- **AG2 `ag-surplus`:** a surplus wrong answer cancels a correct one (worked as 4 − 1,
  MS-AG p.4). (Breed facts — Texel = sheep, Charolais/Holstein-Friesian = cattle,
  Jersey/Montbéliarde/Norwegian Red = dairy cattle — are standard.)
- **AG3 `ag-iis-brevity` (higher):** IIS sections are holistically banded; "not to
  penalise skilful brevity, nor to reward unwarranted length" (MS-AG p.7).

### Applied Mathematics (level: common) — MS-AM-2024 (`examiner-reports/applied-maths/2024-marking-scheme`)
- **AM1 `am-blunder-slip`:** blunder −3, slip −1, misreading −1 (MS-AM p.3). Uses neither
  the Maths A–D scales nor the Physics granule ladder — the subtractive penalty system.
- **AM2 `am-scale-floor`:** systemic-error scale 27/24/16/8; any valid attempt banks the
  floor (MS-AM p.3, p.13).
- **AM3 `am-name-method`:** "Allow 3 marks for the name of a correct algorithm if no
  other work is presented" (MS-AM p.6).

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

## Cross-year verification

Because SEC schemes carry a "subject to change year to year" caveat, the load-bearing
rules are being re-checked against a **second year's** scheme per subject, to confirm
stability and catch any drift. Results so far (each filed as
`examiner-reports/<subject>/<year>-verification.md`):

| Subject | Basis year | Second year | Result |
|---------|-----------|-------------|--------|
| Geography | 2025 HL | 2024 HL | All 5 cited rules CONFIRMED identical (SRP definition, diagram-zero, wrong-process-zero, Overall Coherence bands, Part Two A20/B30/C30). |
| English | 2025 HL | 2024 HL | All 5 CONFIRMED identical (PCLM 30/30/30/10, primacy-of-P, different-texts rule, compulsory Unseen Poem 20, Mechanics 10%). |
| Mathematics | 2023 OL / 2025 FL | 2024 HL | Scale system, credit descriptors, work-of-merit and Full Credit −1 CONFIRMED (2024 HL presents Full Credit −1 via the annotation palette rather than prose — same rule). The unsupported-answer default is not stated *generally* in the 2024 HL scheme; the app cites it to the 2023 OL P2 scheme, which does state it generally — citation correct, no edit. |
| Business | 2025 HL | 2024 HL | Conventions CONFIRMED stable (Name/Explain/Link, "no link without theory", separate links per section, "List" pays names only, per-step numeric marking, chart labels carry marks). SEC sets each ABQ/Section *grid* per-question per year, so 2025-specific mark splits don't recur verbatim. **Acted on:** the "Evaluate means judge" session claimed evaluation is the heaviest ABQ component at a fixed 3-of-7 in Part (B)(i) — true for 2025 but not 2024 (Evaluate was in Part (C), lighter). Reframed the session to the year-stable convention: the ABQ always carries an Evaluate task with its own separately-awarded judgement mark, exact weight/location set per year. |

| Physics | 2025 HL | 2023 HL | All 4 cited rules CONFIRMED — the general notes are word-for-word identical (granule ladder, −1 units, −1 slip, // mutually-exclusive methods). No edit. |
| French | 2025 HL | 2024 HL | All 5 CONFIRMED verbatim/identical (two axes, "mere transcription" band, manipulation docking, hedging = 0, aural any-formulation + 50% wrong-language). No edit. |
| Biology | 2023 HL (Deferred) | 2025 HL (main) | All 4 CONFIRMED verbatim (points notation, context rule, Section A surplus penalty, Sections B/C asterisk). Also corrected a stale count in the 2023 insights file: Sections A and C each choose from **7** questions (best 5 of 7 / best 4 of 7), not 6 — the app's Biology sessions don't reference the count, so no session edit. |

Across the eight subjects verified so far (English, Maths, Business, Geography, Physics,
French, Biology — plus the Maths cross-level pass), the load-bearing rules are stable year
to year; the only content change required was the single Business reframing above. This is
a strong stability signal for accreditation: the conventions the tool teaches are not
one-year artefacts. Remaining subjects are added to this table as their pass completes.

## Pedagogical basis

The tool is an application of self-assessment / rubric-internalisation practice: the
already-verified references in `compliance/evidence/marking-scheme-decoder.md` and the
teaching-effect record in `compliance/evidence/teaching-effect.md` cover the adjacent
claims the app makes elsewhere. This tool's own copy makes **no research claims** — its
claims are exclusively about how SEC marking works, each cited above.

## Scope & expansion protocol

Per the product direction (2026-07-06), the tool covers **every applicable subject at
Higher, Ordinary and Foundation level (where the subject offers it)**. Protocol for each
subject/level: (1) obtain the SEC marking scheme / Chief Examiner's Report, (2) file it
into `/examiner-reports/` (PDF + md + insights per the CLAUDE.md process), (3) author
sessions citing only rules the document supports, tagged with the verified level (or
`common` where the cited rule is a documented cross-level convention), (4) extend this
dossier in the same change.

**Coverage — 27 subjects (loop complete):** English, Mathematics, Irish, Biology,
Business, Geography, French, History, Chemistry, Physics, Accounting, German, Spanish,
Economics, Home Economics, Agricultural Science, Applied Mathematics, Construction
Studies, Engineering, Design & Communication Graphics, Politics & Society, Religious
Education, Music, Classical Studies, Italian, Art (Visual Studies), LCVP Link Modules.

This spans the substantial-enrolment Leaving Certificate subjects. Any remaining
low-enrolment subject is added on the same protocol when a verifiable scheme is located;
none is asserted without one. Next refinements (not blocking): level-specific
(OL/Foundation) worked examples for subjects currently taught via shared `common`
conventions, and Chief Examiner's Reports for subjects where one becomes retrievable.
