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

v1 ships Business (HL) and Mathematics. Per the product direction (2026-07-06), the
tool expands to **every applicable subject/paper**: for each new subject, (1) obtain
the SEC marking scheme / Chief Examiner's Report, (2) file it into `/examiner-reports/`
(PDF + md + insights per the CLAUDE.md process), (3) author sessions citing only rules
that document supports, (4) extend this dossier in the same change. Subjects for which
no verifiable scheme can be obtained are skipped and recorded here with the reason.
