# Economics completion — working record, 7 October 2026

**Active goal: every Economics task and finite answer route in Paper Trail, in
Mark Bank and Topic Atlas under the correct topic, with required source material.
This is not complete.** Do not shrink the scope to the existing 2021–2025 cards.

Worktree: `/Users/alexlinehan/Documents/Nextstepuni-Economics-Completion-20261007`
Branch: `codex/economics-corpus-completion-20261007`, based on `8deb273f`.
No commits, merges or deployments yet. Other subjects are in other worktrees.
The corpus and node_modules are read-only symlinks to the Launch checkout.

## Scope and evidence

- `econ_inventory.py` starts from the actual Paper Trail index: 66 physical
  variants, 33 year/level pairs, 2010–2026, English and Irish. 2020 has Higher
  only. All 132 question/scheme PDFs exist. Covers match indexed years; no PDF
  hashes duplicate within either collection.
- Atlas has 1,098 top-level physical question mappings / 549 language-collapsed
  questions. These are not a task census or proof of complete classification.
- Mark Bank began with 697 EV cards for 2021–2025 (383 Higher / 314 Ordinary).
  It currently has **696 = 381 Higher + 315 Ordinary**, after additions and
  verified consolidations. Eighteen old IDs resolve through explicit progress
  aliases; every original identity is preserved either live or by alias.
- **10/66 physical variants reviewed; 56 pending.** All eight 2022 and 2023
  Higher/Ordinary English/Irish editions and both 2024 Higher editions are
  reviewed; no pending edition is treated as equivalent by default.
- 51 variants have no associated Mark Bank card; 56 have no primary-language
  card. The reviewed Irish editions now have checked shared logical cards. Equivalence
  must be checked, not assumed. Equivalent translated tasks may share a logical
  card, with correct source and Atlas associations; differing tasks may not.
- **Irish 2022 Higher Q6 is not a layout-identical translation of the English
  scheme:** PDF p.10 has `1x4`, `1x3`, then `4`, `2`, `2` in different positions.
  Both versions were viewed. Do not copy English per-part tariffs into IV based
  on question numbering. The completed Irish review retains both complete
  15-mark routes with unpriced rows; see the latest section below.

## Completed 2022 Higher English sweep

Visually reviewed paper PDF pp.2–39 (instructions, all asks, extra-answer page)
and scheme answer pages 5–41. The new independent review is:
`reviews/economics-2022-hl-ev.json` — 16 questions, **75 task routes**, manually
transcribed tariffs, question/scheme pages, topic IDs, reasons and source hashes.
All six Section B questions reconcile to 75 marks, counting an alternative once.

`econ_review.py` compares physical PDF hashes and raw selection wording with the
review. All 35 selection-related source lines are classified, including exam
selection, objective answer classification, genuine alternatives, required
headings and administrative wording. A changed hash, omitted directive or stale
key fails. The default command refuses corpus completion while papers remain
pending; `--allow-pending` explicitly reports 2/66 reviewed and 64 pending.
The Economics deck build now runs this guard in work-in-progress mode.

`data/examTopics/economics-sec-topic-reviews.json` has exact language/year/file/
question mappings for both 2022 EV papers (32 questions), plus three targeted
questions below.
Each mapping carries its physical paper hash, checked by the crosswalk builder.
The runtime registry returns reviewed mappings before historical commercial
heading joins, so erroneous old tags cannot be unioned back into corrected
questions. Original heading evidence remains available. **Part-level Atlas
anchors and a full-corpus task join are still outstanding.**

All 75 current 2022 HL cards have inspected official question-page attachments.
Many use the whole question's pages to retain preceding stem context. The existing
source reader supports navigation and zoom before revealing the answer.

### Restorations and corrections

- Q4(c) FDI restored at the published seven-mark alternative total. One complete
  response row, no invented per-reason split; three scheme examples with clear
  guidance that only two reasons are required.
- Q6 now has complete `(a)+(b)` and `(a)+(c)` routes, retaining both diagrams and
  explanations plus the selected alternative. `questionTotal`, 15 each, no
  inferred per-diagram or per-alternative rows. The old separate (a)(i)/(ii)
  cards inferred half of a shared diagram tariff. Both old IDs alias to the
  complete `(a)+(b)` route. Source/scheme uncertainty is recorded in the ledger.
- Q8(b) now contains all four scheme examples and asks for any two; the parser
  previously retained two and incorrectly required both.
- Q11(c)(iii) now requires one argument for and one against at 6+6. The old cards
  incorrectly assigned 12 to each side. Retain the older `...-for` ID for the
  complete task; `...-against` aliases to it.
- Q13(a)(i) now includes the missing four-mark example alongside the five-mark
  explanation, with all four original explanation examples restored.
- Q16(a)(i) restored to two impacts at 8+4. Q16(b)(ii) is separately practicable
  government/citizen responses at seven each; the previously missing citizen
  card includes all three scheme examples. Government examples no longer include
  a citizen heading/response. Q16(c)(iii) corrected from 2 to 5 (2+3).
- Topic corrections include ECB policy, opportunity cost, rent demand, land
  equilibrium/derived demand, gender pay gap, milk output and PED/revenue.
- Q7(a)(i) now uses the question paper's 2000–2020 interval (the scheme says 2021).
  Q4(b) no longer repeats separately marked (a); Q10(a) includes “Explain”.
- Q14(b)(i): paper asks for average TOTAL cost. Scheme mislabels it average
  variable cost while calculating total cost/output. Keep correct results and
  explicitly explain this source discrepancy; do not teach the wrong formula.
- Q1(a): official PED working crop restores fraction bars; hidden until reveal.
  Catalogue: `authored/economics-completion-figures.json`, scheme p.5,
  rect `[245,140,365,210]`, scale4. Shipped in the figure manifest/public folder.

## Targeted former exclusions

`economics-boundary-corrections.json` records three targeted reviews separately
from complete-paper reviews:

- **2021 OL Q3(i)–(ii)**: calculation and elastic interpretation together at 15,
  using the old `econ-2021-ol-sa-q3-i` ID. Paper p.4 / scheme p.5. Whole-question
  assessment avoids inventing a separate interpretation tariff. Source attached.
- **2022 OL Q12(a)(i)–(iii)**: both curves and equilibrium labels on the single
  28-mark diagram. Keep `...-q12-a-i`, alias old supply-only `...-q12-a-ii` to it.
  Paper p.13 / scheme p.16. Topic now Market Economy; source attached.
- **2023 HL Q16(a)(i)–(ii)**: definitions plus labelled demand-shift diagram and
  explanation at combined 23 (4+4+7+8), retaining `...-q16-a-ii`. Paper p.33 /
  scheme p.35. No per-row marks inferred from displaced cells. Source attached.

The only remaining exclusion is **2024 HL Q10(a)(i)**, visually confirmed on
paper p.12 as an example already completed for the student. It is not an ask.

Additional whole-question topic reviews (not full-paper boundary sweeps):
2021 OL Q3; 2022 OL Q12 pp.13–15; 2023 HL Q16 pp.33–36; 2024 HL Q10 p.12.
These are EV only. The complete 2022 OL review now supersedes its targeted Q12
review; do not mark any IV peers reviewed.

## UI and infrastructure

- Single-row whole-response assessment now shows “Check your complete response”,
  puts requirements before illustrative answers and removes “Select all”. The
  duplicated questionTotal explanation was removed. Example paragraphs separate.
- Source reader Escape now closes even when page navigation disables the focused
  Next button and the browser moves focus outside the dialog. Found by the Q6
  mobile browser check; regression simulates that exact focus-loss condition.
- Shared authoring audit supports questionTotal null row marks and rejects
  invented priced rows. Figure binder summary tolerates older missing optional
  label metadata. Its rewrite reformats unrelated manifest entries: if rerun,
  preserve existing raw formatting and append only changed Economics entries.
- Durable card changes are in author scripts and/or `card-corrections.json`;
  authored JSON/TS are generated, not manually maintained. Source attachments
  are in `card-source-bindings.json`. Keep unrelated JSON formatting intact.

## Verification and next work

Latest full focused run: **213 passed, 3 frozen-baseline failures** across seven
files. Only preservation assertions fail: Higher count 383→384, Ordinary314→313,
progress-alias count34→38. Global total happens to remain unchanged; that is not
proof of preservation. Direct comparison confirms all 697 old identities remain
live or resolve to live aliases. Four new Higher IDs, four deliberate aliases.

Application typecheck, scoped lint, JS syntax and whitespace checks pass.
Authoring provenance: 2,387 claims, zero untraceable. Legacy reconciliation after
completed deck write: **657/658 asks, one completed-example exclusion, zero OPEN,
zero orphans/unparsed**. This old census covers ten EV papers only and is NOT
full-corpus evidence. The deck builder runs that ledger before output write;
rerun reconciliation after the build for current evidence.

**Do not refresh preservation/coverage baselines yet.** Repository gates require
all physical papers/schemes, old-ID preservation, zero-open/orphan reconciliation
and targeted tests before refresh. The old coverage content hash also differs.

Mobile checks use isolated Playwright at390px because CUA is unavailable.
`tmp/economics-audit/` holds source renders, harness, browser scripts and logs.
The dev-only Vite config allows the shared node_modules PDF worker realpath.
Confirmed Q1 working hidden before reveal, source PDF opens/closes; FDI guidance;
Q6 two-page navigation, Escape fix and solution; social-benefits example; citizen
response. Browser errors were zero after the reader fix. All three targeted restorations also passed browser checks: source pages
rendered, solutions stayed hidden until reveal, and required answer content
was visible, with zero page errors. Screenshots were inspected.

Next: finish other physical paper/scheme sweeps and full task/selection ledgers;
compare both official languages (extend the English directive scan for Irish wording before
validating Irish reviews); author all missing 2010–2020 and 2026 material;
resolve year-specific curriculum metadata for old papers; implement complete
part-level Atlas associations; verify source/solution legibility and all finite
routes. Then run final corpus gates and deliberately refresh baselines.

Final follow-up: 165 tests across the Economics review, session, deck and curriculum
files passed after simplifying the whole-question assessment wording and replacing
the flattened diagram-label row with an actual scheme sentence. Typecheck/lint
were repeated. The directive scan now also catches spelled-out selection counts
and plural “choices”; two additional lines were reviewed (35 total). The local
dev server was stopped after browser verification.

## Completed 2022 Ordinary English sweep

Paper PDF pp.2–32 visually checked (all tasks pp.3–27; remaining pages are extra
work/copyright). Scheme answer pages5–32 visually checked, plus research-project
grading pages33–35, which are not examination asks. Independent ledger:
`reviews/economics-2022-ol-ev.json`: **16 questions, 64 practice tasks**, all20 raw
selection lines classified. Full corpus now **2/66 reviewed, 64 pending**.

- All64 tasks have whole-question source-page attachments and reviewed Atlas
  topics. The census includes a per-task topic ID, checked against the card and
  Atlas. CSO/census uses canonical0-0 (data for decisions); retailer sales/profits
  uses1-5; PED calculation1-4. Classification reasoning checked against official
  NCCA2019 specification, sections1.1,2.1–2.4.
- Q13(a)(ii) now has distinct current/capital routes, each requiring a definition6
  and example3. The old expenditure ID is retained for current; new capital ID
  `econ-2022-ol-q13-a-ii-capital`. The old menu mixed definitions/examples.
- Q14(b)(i) corrected7→10 (6+4), with(ii)7. All six long questions now sum75
  when an alternative is counted once.
- Q16(c)(i) is a complete8-mark definition+example, no invented4+4 split.
  Q16(c)(ii)–(iii) is combined16: scheme PDFp32 has two8 cells, one displaced
  beside the hidden-economy example and no cell adjacent to(iii). Old16+8 counted
  one cell twice. Keep`...q16-c-ii` with definition, other example AND economic
  effect; alias`...q16-c-iii` to it. Do not reintroduce a guessed per-part tariff.
- Q13(c)(ii) now has separate definition6/example4 rows instead of a menu that
  mixed required components. Q15(a)(ii) requires the scheme's linked concepts
  increased revenue6 and additional services3, with four illustrative uses.
- Removed question stems and next-question chart text from monopoly barriers,
  sustainable-business measures, minimum alcohol pricing, MNC local benefits,
  inflation effects and corporation-tax uses. Restored all8 separate sustainable
  measures (packaging was merged into another option). Other full example pools
  retained; cleaned trailing bullet and OR fragments.
- Two official scheme errors handled explicitly: Q15(a)(i) prose says€4m→€12m,
  but graph axis is millions and values approx€3,500m→€12,000m. Guidance uses
  graph units and flags the prose error. Q13(b)(iii) multiplier2 does not double
  all existing national income after a€1 injection; retain the scheme's accurate
  second wording, income increases by€2.
- New inspected solution crops restore PED fractions (schemePDFp11) and current
  expenditure percentage fraction (p19). Catalogued in Economics completion
  figures, hashed into manifest, hidden before reveal. Full working also has
  readable text guidance. Removed false old notes claiming other tasks were not
  carded, and an incorrect growth-chart explanation treating negative2020 as
  growth. Q10(b) prompt no longer gives wrong chart interval.
- Durable reviewed corrections are applied by `econ_2022_ol_review.py` from both
  ordinary author scripts. Generated deck unchanged in total:697 (384HL/313OL).
  Five additions/five aliases relative to original697; all original IDs resolve.
  Evidence:`tmp/economics-audit/2022-ol-preservation.json`.

Verification: rebuilt deck and Atlas; provenance2382claims/0untraceable; legacy
reconciliation657/658asks,1completed-example exclusion,0OPEN/orphan/unparsed
(still only tenEVpapers, not full corpus). Initial six-file test run:207passed,
3timeouts and3intentionally frozen preservation failures. Serial rerun of the
three timed-out files: **91passed**. Overall210passed, only3frozen-baseline
failures remain (counts383→384,314→313,aliases34→39). Baselines NOT refreshed.
Application typecheck, scoped ESLint, JS syntax and whitespace checks passed.

Browser QA completed using the installed standalone Chromium at390px. Six tasks
(PED, percentage, both expenditure alternatives, hidden economy, corporation-tax
trend) passed: source pages render; all five three-page attachments navigate
through both Next actions; Escape closes after the last page; solution images
remain hidden before reveal; no horizontal overflow or page/HTTP errors.
Screenshots inspected. Results:`tmp/economics-audit/browser-2022-ol-results.json`.

Mobile QA revealed that multiple-row questionTotal examples lost paragraph
breaks. The whole-response layout now applies to all questionTotal cards, not
only single-row cards: instructions precede examples, paragraphs remain
separate, no misleading Select-all shortcut. Final UI/review tests:93passed;
required preservation/curriculum/deck rerun:108passed, only the same3frozen
preservation baseline failures. Scoped ESLint and whitespace checks passed.
Application typecheck passed before this final boolean-condition/copy-only UI
adjustment. The Chrome application check stalled; standalone Chromium works
reliably and should be used for following reviews.

Next paper candidate:2022OrdinaryIrish. Text reconnaissance only (NOT reviewed)
found `Freagair`, `nó/NÓ`, `cé acu`, `aon` and current/capital alternatives. Add
Irish selection patterns before recording that review. Do not treat matching
page numbers as bilingual equivalence; inspect every task and scheme boundary.

The isolated Vite preview is still running on127.0.0.1:5367 (tool session3800,
nodePID94422) for the next review. The stalled Chrome/Node processes were
force-closed after the verified ordinary stop did not finish. No user browser
was touched. No commits, merges or deployments have been made.


## Completed 2022 Ordinary Irish sweep and bilingual source binding

All32 question-paper pages and all36 scheme pages visually inspected. The first24
paper pages were inspected before context compaction; the remaining pages and
all scheme pages were inspected in this continuation. Schemepp33–35 are research
project grading, not paper tasks. Ledger:
`reviews/economics-2022-ol-iv.json`:16questions, **65 practice routes**,32raw Irish
selection lines classified. Full corpus: **3/66 reviewed;63 pending**.

The Irish scheme resolves a real ambiguity in the English edition. PDFp32 aligns
8 separately with Q16(c)(i), (ii) and (iii). The English scheme places its last8
beside the example above (iii). After checking both physical papers and every
other tariff, restored Q16(c)(ii) definition+example8 and Q16(c)(iii) effect8 as
separate tasks, retaining both original IDs. Removed the temporary (iii)→(ii)
alias. The English ledger now also contains65 tasks. This supersedes the earlier
combined16 decision above; no guessed definition/example split was introduced.
Both long-question censuses sum75 when alternatives are counted once.

- All65 shared logical cards now have separate, visibly labelled English and
  Irish question-page readers. The sources remain the physical PDFs with their
  charts, axes, tables and original typography. Progress is shared for tasks
  independently confirmed equivalent; there are no duplicated translated cards.
- Equivalent-edition review records carry per-question explanations and exact
  task/card/mark/topic correspondence. `econ_review.py` now scans Irish directives
  (including Freagair, nó, cé acu, rogha/roghanna and agreement forms) and rejects
  stale/missing directives, changed source hashes, unexplained equivalence,
  different routes/tariffs and circular edition references. Future editions must
  be independently reviewed, not inferred from matching question numbers.
- `economicsEditions.mjs` attaches only validated edition reviews, cross-checking
  the actual cards, primary Paper Trail file, year, level, question, marks and
  topic before binding. Its answer notes are added only to revealed row guidance.
- POS in Q2 is Príomhoifig Staidrimh. Irish Q11 uses MCh/MI for average cost/revenue,
  C₁ for quantity and Co₁ for cost. Its scheme repeats the English diagram and
  mislabels both readingsC₁ in prose. Q12 uses É/É₂ and C₁/C₂; its schemep16 also
  mislabels the price guideC₁ and quantityQ₁. Prompt labels and revealed guidance
  follow the actual Irish question, explicitly mapping the English solution.
  The multiplier and tax-chart prose errors occur in both editions; previously
  corrected guidance remains applicable.
- Added16 Irish whole-question Atlas reviews with exact physical paper hash,
  inspected pages and canonical nodes. Registry tests verify that every one of
  the65 Irish routes has its card topic represented in Atlas. Complete part-level
  Atlas associations remain outstanding for the overall goal.
- Inventory distinguishes primary-paper cards from equivalent-edition cards.
  A reviewed task now requires an actual shipped source attachment with exact
  file/pages and a matching topic. The Irish edition has65 shared card links,
  zero primary English-card duplicates.55variants have no associated card;
  56have no primary-language card. These counts do not prove corpus completeness.

Deck now698=384HL+314OL: five additions and four consolidation aliases relative
to the original697. Every original identity resolves to a live card or alias;
Q16(c)(iii) is live again. Evidence:
`tmp/economics-audit/2022-ol-iv-preservation.json`.

Verification: deck and Atlas regenerated; provenance2381claims/0untraceable;
legacy reconciliation657/658asks,1completed-example exclusion,0OPEN/orphan/
unparsed (still only the old ten-English-paper census, not whole-corpus proof).
Required preservation/curriculum/deck plus Economics/session tests:204passed,
4frozen-baseline failures only (HLcount, OLidentity hash, globalcount, aliascount).
No baseline was refreshed. Final source-review/session rerun after additional
negative-equivalence and multi-row tests:98passed. Application typecheck passed;
scoped TypeScript ESLint, JavaScript syntax and whitespace checks passed. The
script directory is ignored by ESLint, so JS checks were syntax checks only.

Mobile browser QA used standalone Chromium at390px. Eight representative tasks
(POS, monopoly labels/readings, coffee curves, demand shift, equilibrium, hidden
explanation/example, hidden effect) passed all16 English/Irish source opens,
correct PDF links, every page navigation and Escape after last page. No answer
content before reveal, horizontal overflow or page/HTTP errors. Screenshots were
visually inspected. Evidence:
`tmp/economics-audit/browser-2022-ol-iv-results.json` and `mobile-iv-*.png`.

The new preview on5368 was stopped (session54183, exit130). The previous5367
server still occupied its port when starting; it was not modified this turn.
Sandbox-local curl initially failed, but escalated localhost checks worked.
No commits, merges or deployments. Next candidate:2022HigherIrish; its Q6scheme
annotations differ from English and must not be assigned the English tariffs
without full physical review. Full corpus, earlier-year authoring, part-level
Atlas joins and final preservation/coverage gates all remain active work.

## Completed 2022 Higher Irish sweep, source differences and diagrams

All40 paper pages and all48 scheme pages visually inspected. Paper asks occupy
pp3–38;39extra work;40copyright/back. Scheme answers5–41;42–45research project;
46–48blank/back. Ledger `reviews/economics-2022-hl-iv.json`:16questions,
75shared task routes,39raw directive lines classified. Added Irish should/should
not forms to the scanner (Ar/Ba/Níor/Ní/Nár chóir/cheart). All four2022 physical
editions are reviewed: **4/66,62pending**. This supersedes the earlier pending
Higher Irish statements; it does not establish full-corpus completion.

- All75 Higher cards now carry exact English and Irish question-page readers,
  and all16 Irish whole questions have reviewed Atlas mappings. Per-task topics
  are recorded in both Higher ledgers. Hidden-economy definitionQ8(a) corrected
  from fiscal policy3-1 to national income3-0 in both Mark Bank and Atlas.
- Irish Q2 infographic incorrectly shows OTN/GNP falling6.7%; its schemePDFp5
  explicitly acknowledges the typo. Revealed guidance distinguishes that from
  the asked export6.4/import5.4 figures. Q4scheme alternatives are misheaded
  (a)/(b); actual paper(b)/(c) controls. Q11paper requires arguments both for
  and against airport aid despite Irish scheme prose saying or: one each6.
- Q5(c) Irish scheme omits its7 cell; English schemePDFp9 explicitly gives7
  (4+3) to the matched government-policy task. Q10(a) Irish cell is missing;
  English schemePDFp13 explicitly gives6 for the same calculation/explanation.
  Cross-edition allocation evidence records file/pages/reason and is validated
  against the already reviewed primary question, not inferred by arithmetic.
- Q6 Irish mark cells are displaced; neither language supports a reliable
  shared part split. Complete(a+b) and(a+c) remain15each, with unpriced rows.
  Q12 Irish solution CI/II/MCH maps to MC/MR/AC; guidance appears only on reveal.
- Both editions mislabel the Q15exchange-rate axis€/£. The schemes interpret
  it as sterling bought per euro,£/€. Decimal0.80 is pounds,80p, not0.80pence.
  Removed incorrect units from the quoted example options; retained accurate
  source text and added worked graph guidance (2013~£0.83→2015~£0.74). These
  observed periods are open examples, not a closed answer pool.
- Browser QA found missing solution diagrams in Q12(b)(ii) and Q16(c)(i), and
  only a blank question graph in Q15(a)(iii). Restored inspected official scheme
  crops from PDFpp20,32,40. Each has a source rectangle and hash in the completion
  catalogue/manifest. All seven Higher drawing routes now have completed
  solutions hidden before reveal. The milk task retains its blank question
  diagram independently. Replaced flattened label strings with concise diagram
  headings and explained the minimum-price movement in quantity demanded.
- A subscript beta in the new milk guidance triggered the generator’s broken
  glyph filter and briefly dropped that card. Replaced it with plain EA/EB.
  `assertEconomicsReviewCoverage` now checks required reviewed IDs after all
  provenance/glyph/figure gates and BEFORE deck writes. Missing reviewed tasks
  fail the build. Final build:698cards,0dropped; independent inventory passes.

Final focused run (review, session, preservation, curriculum, deck, Atlas):
**223passed,4frozen-baseline failures only**. Same intentionally frozen Higher
count, OrdinaryIDhash, globalcount and aliascount assertions; no baseline was
refreshed. Typecheck, scoped TypeScript ESLint, JSsyntax and whitespace checks
passed. Provenance2381claims/0untraceable. Current post-write legacy reconcile:
657/658asks,1completed-example exclusion,0OPEN/orphan/unparsed. The builder’s
embedded reconcile is still pre-write and can show an older transient count;
use the separate post-write result. Legacy ledger covers tenEVpapers only.
All697original IDs resolve; five additions/fouraliases, deck698=384HL+314OL.
Evidence:`tmp/economics-audit/2022-hl-iv-preservation.json`.

Mobile browser QA at390px: nine tasks,18English/Irish source readers, exact PDF
files, full page navigation, Escape after final page, no premature solution,
horizontal overflow or page/HTTPerrors. Completed monopoly, milk-supply and
minimum-price screenshots inspected; axes/labels intact. Evidence:
`tmp/economics-audit/browser-2022-hl-iv-results.json` and`mobile-hl-iv-*.png`.

## Started 2023 Higher English — NOT a complete paper review

`drafts/economics-2023-hl-ev.json` records the independent SectionA census:
23tasks. PaperPDFpp1–14 and schemePDFpp1–14 visually inspected in paired renders.
Remaining paper15–40 and scheme15–44 have not been inspected in this sweep.
Paper13–14 beginsQ11; no full Q11boundary yet. Full raw directive scan, canonical
topic classification and card/source changes are still pending. The draft is
outside`reviews/` so it cannot increase completion counts or bind an edition.

Findings for next continuation:
- Q1(a)diagram3+explanation3 must be6, not existing3; Q2(a)tick1+explanation5
  must be6, not existing5; Q7(a)diagram3+explanation3 must be6, not existing3.
- Q2(c)advantage AND disadvantage jointly6(2x3), currently two isolated3cards;
  consolidate with stableID/alias. Q10 asks B and C with2@6, currentlycombined12;
  split named calculations preserving the oldID for one and full context inboth.
  A is already completed, not an ask. GNI324.2;modifiedGNI235.2.
- Q3(c)equimarginal utility is wrongly inelasticity1-4; check canonical consumer
  choice1-1. Q1(b)price discrimination currently1-1 also needs topic review.
- Q4English mark cells are missing/displaced. Targeted Irish schemePDFp9 visually
  checked: explicit6for(a),(b),(c), plus firstMC2/firstAC2/finaltwo1each for(a).
  The matching Irish paper has NOT yet been checked, so corroboration remains
  preliminary. Do not mark the Irish physical edition reviewed from this page.
- Q7scheme prose usesS1→S2/Pe1→Pe2 but diagram itself usesS→S1/Pe→Pe1.
- SectionA schemePDFp5 awards an extra mark to each of first4correct questions;
  this is an examination-level bonus, not an extra per-task tariff.

No2023card changes were made during this continuation. Full corpus authoring,
part-level Atlas joins and final completeness/preservation gates remain active.

### 2023 visual sweep completed later in the same continuation

The remaining English paper15–40 and scheme15–44 pages have now all been
visually inspected. The draft now records **73 independent task routes** across
16questions and38exact raw directive lines, with detailed boundary reasoning.
Every SectionB question sums75 when Q15(b)(iii)'s yes/no alternative counts once.
Paper asks3–36,extra37–39,back40. Scheme asks5–39,research40–43,back44.
This supersedes the unviewed-page statements above. It is still outsidevalidated
reviews: canonical topics, card bindings/corrections, figures, Atlas links and
verification remain pending; the full-corpus counter remains4/66.

Targeted Irish paperp6 and schemep9 now both visually checked forQ4: exactsame
question/table/alternatives, published6each; allocation ambiguity resolved.
Targeted Irish paperp33 and schemep35 checked forQ16(a). Both languages put4+4
among the definitions/next stem,7beside diagram,8beside explanation,5beside(iii).
Irish omits the stray3from English. No reliable split of(i)/(ii), so retainthe
complete23withunpriced rows. Full Irish edition stillpending. Irish diagram
prose calls demand a supply curve in error; actualD1→D2controls.

Further required2023 corrections recorded in the draft:
- Q11(a)(iii)negative+positive jointly10; Q12(b)(iii)advantage+disadvantagejoint10;
  Q16(c)(i)for+againstjoint12. PreserveoriginalIDs through aliases forconsolidation.
- Q13(a)(ii)must include definitions ANDtwoexamplesEACH forinjections/leakages:
  total12, notexisting4. Both multiplierformulae are valid:1/(MPS+MPM) equals
  1/[1−(MPC−MPM)], answer2. Injection€125m; superscript2annotationsaremarks.
- Q15(b)(iii)explicitYes/No concern-about-appreciation routes8each mustexpand.
  Q15(c)(iii)is causalclassificationNo,notanother stance pool despiteopinionwording.
- Q14(a)(ii)scheme explicitly awards4for any attempt becauseQNHSshouldbeLFS.
  Preservehistoricalprompt/source andexplaincredit; donotfabricateper-reasonmarks.
  Q14(a)(i)7.6→4.4 changeis3.2percentagepoints,notrelative3.2%.
- Q15(a)(i)mustretainbothtrendandconsumerimpactat6, no guessed3+3split. Scheme
  priceproseuses€21/€22whereaxisiseurocents;graphapprox23c→27c. CPI112.2,total19
  withoutpublishedcelltariffs. Sourceformulas/tablelayoutsneedreadablefigures.
- Q11(c)(iii)requiresonedisadvantageforeachofthetwochosenpolicies; retaincontext.
  Q12(c)windfalltaxrequiresbothsidesandthreedevelopedarguments(total18,8+5+5).

Existing authored2023Higher has75cards(23A+52B). Four required-heading
consolidations(Q2c,Q11aiii,Q12biii,Q16ci), splitQ10B/C andexpandedQ15biiiYes/No
produce73logicaltasks. Old IDs misleadingly nameQ15bii/biii foractualQ14cii/ciii,
andQ13bi/bii foractualQ13ci/cii; theirquestionRefsarecorrect. PreserveIDs; use
actualpaperreferences, notIDstrings, tobind tasks. No2023card edits yet.

Preview5368 was stopped after QA (session2136,exit130). Older5367 was not touched.
No commits, merges, deployments or baseline refreshes. Next action: reconcile
and implement the73-task2023Higher draft, checkcanonicaltopics, author missing
solution crops and sources, then promoteonlyafteritsgatespass. The activegoal
stillincludes everyphysicaledition andtask, notjustexistingcards.


## 2023 Higher English — corrected, reconciled and visually checked

Promoted `reviews/economics-2023-hl-ev.json`: independent 73-task census, all 40
paper and 44 scheme pages inspected, 38 raw selection directives classified.
Six long questions each reconcile to 75 with the alternative stance counted once.
All 73 cards ship with the complete question’s original source pages. All sixteen
Atlas whole-question mappings use the reviewed canonical topics. Part-level Atlas
associations remain outstanding, as does the remaining physical corpus.

Durable corrections run from `econ_2023_hl_review.py` before both historical
extractors emit. Four required-side pairs are consolidated, with explicit aliases:
Q2(c), Q11(a)(iii), Q12(b)(iii), Q16(c)(i). Q10’s B and C calculations are separate
six-mark tasks, retaining the old ID for B. Q15(b)(iii) mechanically emits Yes/No
stance routes, retaining the old ID for Yes. Neither objective yes/no classification
nor lists of scheme examples are treated as finite question choices.

Key corrections: Q1/Q7 include their omitted diagrams (3+3); Q2(a) includes the
choice (1+5); Q13(a)(ii) restores both definitions AND two examples of each (12);
Q14(b)(iii) restores the actual PUP cost-benefit task, three required headings at
four each, instead of the fabricated multiplier question. Q14(a)(ii) retains its
historical QNHS wording and the SEC’s automatic four-mark attempt credit. Q15(a)(i)
requires a trend, supporting figures in euro cents/kWh and consumer impact. Its
scheme has incorrect euro units and starting value; Q14’s chart differences are
percentage points. Q16 circular-economy challenges and government food-waste
initiatives now follow the actual prompts. All truncated response pools were
checked and restored, including first options and structural unemployment.

No fabricated equal tariffs: complete Q3(a), Q4(c), Q5 classifications/justifications,
Q6 canons, Q7 tax reasons and Q9 cost advantages retain their published totals.
Q5(a)’s obsolete labelKey was removed so the runtime cannot reintroduce per-label
scoring. Required for/against discussions use whole-response assessment where the
scheme does not attach fixed marks to the sides. Windfall tax explicitly requires
three arguments across both sides, with 8+5+5 guidance visible in the answer.

Three new inspected solution crops: ticket supply (scheme p5), rental supply shift
(p12) and perfect competition (p20). Together with existing circular flow and car
demand crops, all five drawing tasks have hidden-until-reveal official solutions.
Mathematical rows no longer flatten fractions/squares or present mark ticks as
exponents. Question readers preserve the original blank diagrams and tables.

Topic reasons cite the NCCA specification. Notable corrections: price-discrimination
conditions → Market Structures; equi-marginal utility → Consumer Demand; rental
and car equilibrium → Market Economy; hidden economy → National Income. PUP’s
cost-benefit analysis maps primarily to Scarcity and Choice (NCCA 1.2 expressly
names this task), with Market Failure additionally on the whole-question Atlas
mapping. This supersedes the earlier draft suggestion of Market Failure alone.

Targeted Irish evidence remains explicitly partial: paper pp6/33 and scheme pp9/35,
with both hashes and page bounds checked by `econ_review.py`. Q4 resolves to 6/6/6;
Q16(a)(i)–(ii) remains complete 23 without inventing displaced per-part tariffs.

Validation: build 696 / dropped0; provenance2377 / untraceable0; source gate5/66;
legacy reconcile657/658, one completed-example exclusion, zero OPEN/orphan/unparsed.
The legacy report covers ten 2021–25 EV papers and is not full-corpus completion.
Required six-suite run: 227 passes, four frozen preservation failures (HL count,
OL identity hash, global count, alias count). No baseline was refreshed. Separate
`tmp/economics-audit/2023-hl-preservation.json` proves all697 original identities
resolve: seven added IDs, eight consolidation aliases, zero unresolved IDs.
Typecheck, scoped TS lint, Python syntax and whitespace checks passed.

Mobile browser checks: twelve representative tasks, five hidden-until-reveal
solution images, original 2023 EV PDF readers rendering and navigating every
attached page, Escape dismissal, no horizontal overflow or browser errors.
Evidence: `browser-2023-hl-results.json` and `mobile-23-*` under the audit directory.
A first Vite startup produced a blank page; rerunning after dependency optimisation
completed succeeded. Content tests also caught and resolved the obsolete PPF label
scoring mode. Preview5368 is running in exec session94336 during the Irish review.


## Completed 2023 Higher Irish sweep

All40 paper and44 scheme pages visually reviewed. Scheme40–43 is the separate
research-project rubric and44 back cover. The independent comparison retains
all73 logical tasks and binds their full Irish question pages and16 Atlas
question mappings. Review hashes and exact equivalence are validated. No cards
or progress aliases changed in this step; the live deck remains696.

The Irish review records12 visible answer notes: utility-table 1+1 allocation;
PPF C/A/B versus inconsistent scheme P/C labels; officially acknowledged
direct/indirect-tax translation error and acceptance of any taxation principles;
rental É/D labels and supply-shift prose; missing9-mark policy drawback cell;
PC output label C; circular-flow savings mistranslated as spending; missing
leakage-definition2 cell; wrong sign/bracketing in the alternate multiplier
formula; energy-credit No mistranslated as Uimhir; and demand called supply
in the car-market explanation. Missing allocations cite the actual matching
English scheme pages18 and23, not arithmetic to force totals. Both editions'
electricity units and QNHS automatic-credit correction remain visible.

The raw selection scanner now includes Irish opinion/yes-no formulations
(an dóigh, an léiríonn, an bhfuil, Tá/Níl). All48 2023 HL Irish lines and41
2022 HL Irish lines are classified; the newly caught 2023 questions are
objective classifications, not invented No/Yes alternatives. Negative tests
remove those lines to confirm generation rejects an unreviewed directive.

Validation:12 mobile tasks passed source-file/year checks, all page navigation,
Escape close, concealed answer guidance and four concealed diagram solutions,
with no horizontal overflow or browser errors. Source/provenance checks pass:
2377 claims,0 untraceable. Legacy reconciliation remains657/658 asks covered,
1 completed-example exclusion,0 OPEN/orphan/unparsed (only the legacy EV
subset, not whole-corpus proof). Six suites:229 passed, four unchanged frozen
preservation failures; the additional scanner regression is run separately.
Typecheck and scoped lint passed. Baselines remain untouched.


## Completed 2023 Ordinary English and Irish reviews

Both physical 32-page papers and both 32-page schemes were visually swept in
full, including instructions, extra-answer pages and the separate research-project
rubrics (scheme29–31, back32). The independent English census has **63 task
routes:18 Section A and45 Section B**. Irish equivalence was checked per question,
including every tariff and diagram/table label, then bound to all63 shared cards.
All six long questions total75 when each alternative is counted once.

- Reviews: `reviews/economics-2023-ol-ev.json` and `...-iv.json`.
- Each has16 reviewed Atlas question mappings with curriculum reasons and physical
  source hashes. Full question pages accompany every task (1 short/3 long).
- Q16(b)(i) explicitly chooses two of scarce/transferable/utility. All three
  pairs are mechanically generated at14 each, with exact IDs, wording and7+7
  marks pinned in regression tests. The older misnamed ID remains the first pair.
- Q13(b)(ii) national income18 and balance of trade9 are independently practicable;
  the newly restored trade task retains the source table and formula context.
- Q11(c)(i) restored the separately required four-mark OTHER hidden-economy
  example after its six-mark definition. Q16(a)(ii) restored the two-mark Yes
  before its four-mark reason.
- Q10 requires private AND social benefits in one12-mark response; Q14(a)(ii)
  requires a cause AND consumer effect in one12-mark response. Their former
  separately priced sides were consolidated, with two explicit progress aliases.
- Q9, Q10, Q11(b)(ii), Q11(c)(ii), Q12(c)(iii), Q13(a)(i), Q14(a)(ii) retain
  whole-response totals with unpriced rows where the scheme supplies first/second
  or aggregate tariffs rather than a fixed heading allocation.
- Restored complete open answer menus; did not manufacture finite combinations
  from illustrative examples. Corrected unemployment commentary, HDI rank,
  price-data guidance, demand-curve requirements, and topic assignments for
  external benefits, hidden economy, vehicle percentages and productive factors.
- The Q11 equilibrium solution now uses a full crop including the vertical arrow
  tip: `economics-2023-OL-scheme-p13-q11bii-equilibrium.png`. The old asset remains
  intact. Source PDF p13, rect[101,308,510,615], scale3, with catalogue metadata.
- Mobile inspection caught the car-percentage fraction flattened into adjacent
  numbers. The answer now quotes the verified81.32% result, with complete readable
  working `(101,853 + 68,042) ÷ 208,913 × 100 = 81.32%` and the five-step tariff.

Irish-specific revealed guidance records:

- GDP initials OTI: given Oll, missing Táirgeacht/Intíre4 each, in a different
  order from English Domestic/Product.
- Scheme December2023 typo (paper December2022), eighth-place HDI vs scheme second,
  and Budget intro2022 vs chart2023.
- Equilibrium paper C1(output)/P1(price)/Co1(cost), while the schemes useQ1/C1;
  Irish drawing misnames equilibriumE asA. Full term translations also accompany
  labels1/2/3.
- **Q12(b)(i) conflicting mark cell:** Irish scheme p16 prints10, despite its own
  part(b) total20 and following task12. English scheme p16 explicitly gives8.
  Shared tariff8 is supported by the English source and both overall totals;
  the conflicting Irish10 is stated to students, not silently discarded.
- National-income table consumptionC is misprintedP in the Irish scheme;
  demand diagram axes Praghas/Méid mean price/quantity.

The scanner now recognises `ar bith`, which catches the Irish internal choose-two
instruction. All34 Ordinary Irish directives are classified. The broader pattern
also found a non-selection “anyone buying a drink” sentence on2023 Higher Irish
p36; it was visually rechecked and classified (49 directives now). A negative
regression test deletes the actual Irish choose-two line and requires rejection.

Verification at this checkpoint:

- Generation **697 cards (382HL/315OL),0 dropped**; all reviewed task IDs required
  by the build. Original697 identities all resolve:10 additions,10 aliases,0 lost.
- Source gate **8/66 passed,58 pending**. Provenance2375claims,0 untraceable.
- Legacy ten-paper reconciliation657/658 asks,1 completed-example exclusion,
  0OPEN/0orphans/0unparsed. This remains a limited legacy check, not whole-corpus proof.
- Six suites:237 functional checks pass after correcting a test that wrongly
  assumed a labelled-diagram card was a question card; three frozen preservation
  assertions remain (HL/OL counts and alias count). Baselines remain untouched.
- Typecheck, targeted ESLint and whitespace checks pass.
-14 English mobile cases passed;14 Irish mobile cases passed with no page/network
  errors, horizontal overflow, leaked answers or broken reader navigation.
  Revealed percentage, equity and GDP guidance and equilibrium source were
  visually inspected. Evidence lives in `tmp/economics-audit/browser-2023-ol-*`
  results/scripts and `mobile-23-ol-*` screenshots.

No commits, merges, deployments or coverage/preservation-baseline updates.


## Completed 2024 Higher English and Irish physical reviews

Each edition: all 40 paper pages and 52 scheme pages visually inspected.
Independent census: 83 task routes (24 Section A, 59 Section B), with every
Section B question reconciling to 75 after choosing one alternative. All 30
English and 35 Irish raw selection directives are classified. Reviews are
`reviews/economics-2024-hl-ev.json` and `reviews/economics-2024-hl-iv.json`.
Sixteen exact physical Atlas mappings per language and complete source-page
bindings for every route. Research rubric pp48–51 adds no written-paper tasks.

English corrections were durable in `econ_2024_hl_review.py` (retired by the
2026-10-12 re-review below; `econ_2024_hl.py` now authors both sections). Seven previously
missing tasks restored: Q6(a) diagram5; Q11(c) three diagrams5 each; Q11(b)(i)
meaning4; Q14(b)(i) explanation9; Q16(b)(ii) meaning4. Eight old side-only cards
now alias to complete required responses: AC slopes4, woodland cost/benefit6,
globalisation positive/negative10, surplus effects6, interest spending/debt8,
obesity economic/social10, DART cost/benefit10, indirect-tax advantage/disadvantage12.
First6/second4 tariffs retain unpriced rows where neither side has a fixed share.
Q16(a) both tasks corrected to10 each; price-discrimination definition4+example2,
corporation-tax trend4+explanation4 and capital definition4+nontransport example2
restored. Taxpayer/government4 and agree/disagree6 are both explicit finite routes.
Full open example menus restored without inventing a finite selection pool.

Five official solution crops added and visually checked at mobile size: MC/AC,
three organic-ice-cream shifts and monopolistic-competition equilibrium. The
flattened equilibrium-label extraction is replaced with the source heading and
readable criteria alongside the actual official diagram. Calculations explain
1/0.92=1.086956 (scheme truncates1.08, ordinary rounding1.09), midpoint YED0.81818,
inflation-rate decline rather than falling prices, and the paper’s correct
2022/2023 YED and 2023/2024 forecast dates. The 2011–2022 tax graph takes priority
over the scheme’s stale2021 introduction. Revenue’s 2003 statistical report
confirms the standard12.5% rate began1January2003; the scheme’s1998 claim is
identified as erroneous, with the primary reference retained in the review.

Irish per-question equivalence was checked physically. Guidance corrects the
Q1(b) reversed imports/exports phrase and explains É/Pc/Cc, MC/AC Irish labels,
OTI/OTN/GNI, PIT and Q14 C1 output versus C cost (including II/MR, CI/MC). Shared
source errors are recorded, not silently copied. Irish question pages are
attached to all83 logical tasks. No extra card is created for completed Q10(a)(i).

English mobile verification: 22 cases passed source loading/navigation, hidden
answers/solutions, image loading and horizontal-overflow checks. Visual review
found long criteria crowding the sticky grade footer; the summary is limited to
three lines while complete criteria remain above. All22 passed the new footer
height check and the final compact footer was visually inspected. All 18 Irish mobile cases also passed; final cost-curve solution and equilibrium
explanation were visually checked. Combined six-suite checks: 242 passes and the
four known frozen-baseline failures. Typecheck, scoped ESLint and whitespace
checks passed.

Before Irish attachment, six-suite verification had240 passing assertions and
four expected frozen-baseline failures: HL381vs383, OL315vs314, global10494vs10495,
aliases52vs34. All697 original IDs resolve live or through18 explicit aliases;
17new IDs. Provenance2377claims/zero untraceable; old ten-paper reconciliation
657/658 asks, one completed-example exclusion, zero OPEN/orphan/unparsed.
Do not refresh baselines, commit, merge or deploy. Corpus remains incomplete.

## 2026 Higher and Ordinary English (commit c00064751)

Independent censuses from every page: 2026 HL 90 routes (40 paper + 88 scheme
pages), 2026 OL 74 routes (32 + 47 pages); 164 new cards in econ_2026_hl.py and
econ_2026_ol.py (helpers in econ_2026_lib.py). Menus are split at the scheme's
own bold headings; econ_glyphfill.py restores the 2026 HL scheme glyphs whose
ToUnicode entry is a space ("G P" -> "GDP"), appended under a marker. A question
crop REPLACES the typed stem and ask in the session screen, so data-only crops
ride as the pre-reveal figure and only a card whose figure slot holds its
solution takes a question crop, which is then the whole printed question
(show_before_reveal). Browser QA found that defect, the HL Q1(b) heading
misattribution and two OL asks missing their table labels; all fixed, 45 English
mobile cases pass. Irish editions untouched.

## 2025 Higher English

All 40 paper and 77 scheme pages viewed (scheme PDF page = printed + 1).
econ_2025_hl.py now authors both sections from the census (the old Section A
script is retired; every ID it shipped is kept). 82 routes. Seven split
required-heading halves are withdrawn by card-corrections.json with progress
aliases: Q1(a) against, Q4(a) not-beneficial (one 6 cell, no printed tick),
Q4(b) consumers, Q11(b)(iii) disadvantage, Q12(a)(ii) government, Q12(c)(i)
employer, Q13(a)(ii) challenge. Six missing tasks added: Q11(b)(i) explanation
(9, split from the 12-mark diagram), Q12(a)(i) GDP trend route, Q14(b)(ii)
calculation (9; meaning 5 kept), Q16(b)(i) diseconomies of scale, Q16(b)(ii)
explanation (8, split from the 8-mark diagram), Q16(c)(ii) short-run loss.
Q14(c)(ii) now carries the negative effect too. Objective ticks stay one card
(Q4(c) cost-push, Q12(a)(iii) GNI*, Q12(b)(ii) regressive). Margin splits lifted:
Q14(b)(i) 2+6+6+3 (E, Pe, Qe 1 each), Q16(b)(ii) diagram 3+3+1+1. Citations corrected:
q16-b-i is Q16(c)(i) (its old text described a different question), q16-c is
Q16(c)(iii). The scheme prints 6 for each required heading of Q1(a) and Q4(b),
so those questions total 18 against 12 elsewhere in Section A; recorded as
printed. The scheme's Q14(b)(ii) meaning says a EUR1 price rise cuts quantity by
1.8%; guidance states the percentage reading. Two scheme headings drawn with
unrecoverable glyphs (bold K of "Knowledge Development Box", "cluster effect"
ligature) are lifted from their intact explanations. Eight hidden solution crops
and seven whole-question crops added.

## Preservation pins (commit 2a35ca591)

Economics now uses the additive form: the 697 pre-review IDs stay frozen with
their original identity hashes (frozen identity = live frozen IDs + Economics
alias keys, each resolving in one step to a live card of the same year and
level); reviewed additions are the explicit `economicsAdditionIds` set in
test/markBankCardPreservation.test.ts. Extend that set and the alias count with
every reviewed paper; never rewrite the frozen hashes. The coverage baseline is
re-measured for Economics only after each paper's checks pass.

## 2025 Ordinary English

All 32 paper and 47 scheme pages viewed (scheme PDF page = printed + 1).
econ_2025_ol.py now authors both sections from the census (the old Section A
script is retired; every ID it shipped is kept). 69 routes (72 before the
choose-N-of-M rule below). The earlier cards
had written their own stems and asks; every stem and ask is now sliced from the
paper. Three cards that held one part of a jointly priced answer are withdrawn
with progress aliases: Q6 social cost (one 12, 1st x 8 / 2nd x 4, for the
private AND social cost), Q8(ii) barrier (the tick and the barrier share one
12; the old tick card priced the tick alone at 12) and Q16(c)(i) industrial
action (2 @ 6 plus a 6-mark justification that was missing). Four routes
added: the Q13(b)(ii) marginal revenue route, Q13(c)(i) MNCs, and the Q14(b)(i)
positive and negative routes. Q11(b)(i) "any three of the following four
labels" is one card, `econ-2025-ol-q11-b-i`, whose menu lists all four labels
at 8 with a claim of three (see the rule below). Tariffs corrected: Q11(b)(iii) 4 (was
8), Q11(c)(i) 10 (was 8). Citations corrected: q13-c is Q13(c)(ii), q14-c is
Q14(b)(ii). Truncated menus restored (Q3(a) social, Q3(b), Q4(a), Q12(c)(iii)
savers, Q13(a)(iii), Q14(b)(ii), Q15(a)(iii)); page furniture removed. Joint
tariffs ("1st x 8, 2nd x 4" across required headings) are unpriced points, so
the session never prints a per-heading share the scheme does not fix.
Objective ticks stay one card (Q4(b) Yes, Q12(a)(ii) capital, Q14(c)(i)
improved, Q15(a)(ii) agree, Q16(a)(i) indirect). Two hidden solution crops,
three data crops and seven whole-question crops added.

## Choose-N-of-M items: one card (coordinator rule, 2026-10-12)

When the student chooses which N of M printed items to answer and the scheme
lists content for each at the same price, the bank publishes ONE card: an
`anyN` row listing all M items in the scheme's wording and marks, with a claim
of N. It never publishes a card per combination, because sessions do not
collapse route siblings and the student would meet the same question again
and again. Route cards stay only where the scheme marks the routes
differently (different scheme rows per route: agree/disagree, positive/
negative, one sector or the other, taxpayer or government).

- **2025 OL Q11(b)(i)** "any three of the following four labels": the four
  combination cards are now one `econ-2025-ol-q11-b-i` (3 @ 8 = 24, claim 3 of
  MC, Q, D=AR=MR, AC, each lifted from the scheme). The three other combination
  IDs (`-mc-q-ac`, `-mc-ar-ac`, `-q-ar-ac`) were added on this branch and were
  never on main (checked against origin/main), so no student progress exists
  for them: they are removed with their source bindings and their entries in
  `economicsAdditionIds`, not aliased. 2025 OL now 69 routes; Ordinary deck 388.
- **Sweep.** Every built Economics card was grouped by year, level and printed
  part, and every pair of route cards sharing a scheme row was listed. Besides
  the case above it found: 2024 HL Q11(c) diagram/explanation pairs (separately
  priced 5 and 4, so not a choice); 2025 OL Q14(b)(i) positive/negative (one shared trend-comment row,
  different development lists: a scheme-marked route split, kept); and
  **2023 OL Q16(b)(i)** "explain two of scarce / transferable / utility", carded
  as three combination cards (`econ-2023-ol-q16-a-i` on main;
  `-q16-b-i-scarce-utility` and `-q16-b-i-transferable-utility` branch-only).
  Its routes are mirrored task-for-task in the 2023 OL Irish review, so it was
  first left alone; the coordinator then approved the fold with a minimal
  mirror edit. **Folded 2026-10-12:** `econ-2023-ol-q16-a-i` is one card whose
  menu lists scarce, transferable and utility at 7 with a claim of two (2 @ 7 =
  14). The two other pair IDs were branch-only (not on origin/main), so they
  are removed with their bindings and `economicsAdditionIds` entries. The 2023
  OL English review now has 61 routes. The Irish review received ONLY the same
  route collapse in its Q16 task list (three b/i pair tasks to one `b/i` task
  on the kept card); its reasons, selections and guidance text are unchanged
  and its content was not re-reviewed.

## 2024 Higher English re-review (2026-10-12)

All 40 paper and 52 scheme pages viewed again (scheme PDF page = printed
page). `econ_2024_hl.py` now authors both sections from the census in
`drafts/economics-2024-hl-ev.json` with the 2025 method; `econ_2024_hl_seca.py`
and the correction module `econ_2024_hl_review.py` are retired. The census
confirms the same 83 routes (24 Section A, 59 Section B): every (key, card,
marks, topic) tuple equals the earlier review, which the 2024 Higher Irish
review mirrors task for task, so the Irish attachment is untouched and still
binds. No card ID changes; the eight required-heading aliases stand.

What changed on the cards:
- Every stem and ask is sliced from the paper. The earlier cards had written
  their own (for example "A new 30% income-tax rate ... is proposed", "Explain
  one economic effect of the ECB interest-rate increases on each of the
  following: consumer spending; Ireland's national debt", a paraphrased Coillte
  ask). The paraphrased Q9(a) ask was why `econ_refcheck.py` placed
  `econ-2024-hl-sa-q9-a-cost` under Q16(c)(ii); it now confirms against Q9(a).
- Menus are split at the scheme's own headings or response openings (sliced
  by bold heading, or by named opening words where the scheme sets a heading
  with a colon or none). Q15(a)(ii) now has the scheme's four steps (the
  earlier menu split one response at a non-bold sentence, giving five), and
  Q13(c)(iii) all six negative consequences (the earlier row held two).
- Required headings are heading rows at the scheme's price: Q6(b) 2 @ 2, Q9(a)
  3 + 3, Q13(c)(iii) 3 + 3, Q14(c)(i) 2 @ 4, Q15(b)(ii) 2 @ 5 (exports and
  imports, previously a two-of-two menu), Q16(c)(ii) 2 @ 5, Q16(c)(iii) 2 @ 6.
  Pairs priced 1 @ 6 then 1 @ 4 across two headings (Q13(b)(iii), Q15(c)(ii))
  stay unpriced points, so no per-heading share is printed.
- Q11(c)(i)-(iii): the explanation cards carry the scheme's 4 @ 1 criteria
  (shift, price, quantity, cause); the diagram cards carry the scheme's account
  of the shift beside the hidden solution diagram. The two no longer share a row.
- Q12(b)(ii) shows the clean answer 119.5 with the working in guidance, in place
  of a flattened table row.
- Figures: four whole-printed-question crops where the figure slot holds a
  hidden solution (Q3(a) diagram, Q4(a) table and ticks, Q10(a) accounts table
  and ladder, Q12(b)(ii) worksheet), and a new data crop of the Q16(a)
  homelessness chart. Q5(b) carries the Q5(a) solution diagram (hidden until
  reveal) and Q11(a)(iii) the tourism chart, because their lifted wording
  points at them (cardlint ghost-figure). The stale cardlint exemption for `econ-2024-hl-sa-q6-a` is removed (the
  card now carries the solution diagram) and the stale `econ_refs.HAND_CHECKED`
  entry for `econ-2024-hl-sa-q8-a` is replaced by the two four-word asks
  refcheck cannot place, Q5(b) and Q13(b)(i), both read against the paper.
- Source notes kept as guidance: the scheme's 2011-2021 introduction against the
  2011-2022 graph; the 12.5% rate dated 1998 by the scheme and 1 January 2003 by
  Revenue; the scheme's 2021/2022 YED table labels against the paper's
  2022/2023; the 2022/2023 labels in the PlayStation working against the paper's
  2023/2024; 1 / 0.92 = 1.086956 (scheme 1.08); the Budget 2023 mention in the
  energy-credit example.
- Choose-N rule: this paper prints no choose-N-of-M item pool. Q12(a)(iii) tax
  payer / government and Q14(a)(ii) agree / disagree stay routes because the
  scheme lists different content for each side.

## 2026 HL Q14(b)(ii): 16 printed options (recorded)

`econ-2026-hl-q14-b-ii` carries 16 import factors against the build's cap of 14
(an audit warning, not a failure). The 2026 HL scheme prints all 16 under
"Two factors ... 2 @ 4" (scheme pages 60-61); per the coordinator, the menu is
left whole and not trimmed.

## 2024 Ordinary English re-review (2026-10-12)

2024 OL was one of the batches left half-finished at the Codex pause, so it was
closed from a fresh census rather than from the cards already built: all 32
paper and 46 scheme pages viewed again (scheme PDF page = printed page), every
part counted from the paper and priced from the scheme, then compared with the
earlier review. The count is the same 61 routes (13 Section A, 48 Section B),
and every (key, card, marks, topic) tuple equals the earlier review, which the
2024 Ordinary Irish review mirrors task for task; the Irish attachment is
untouched and still binds. No card ID changes; the three aliases (Q1(ii),
Q8(ii), Q16(b)(ii) disadvantage) stand. Choose-N rule: no printed choose-N-of-M
item pool on this paper (Q9's four blanks, Q11(b)(i)'s three labels and Q15(a)'s
five cells are all required).

`econ_2024_ol.py` now authors both sections with the 2025 method;
`econ_2024_ol_seca.py` and the correction module `econ_2024_ol_review.py` are
retired. What changed on the cards:
- Every stem and ask is sliced from the paper. The earlier cards had written
  their own (for example "The exam's scenario describes Ireland's population as
  ageing rapidly", "In the paper's proposed-entry scenario", "Using the
  Gini-coefficient chart, name the country...", an Education ask that supplied
  the €44.22bn total). Their refcheck UNPLACED entries for the Q8 and Q14(a)(i)
  cards are gone; the one three-word ask, Q15(b)(ii) "Explain your answer.", is
  hand-checked in `econ_refs.HAND_CHECKED`.
- Tick and classification cards carry the scheme's statements as rows with the
  answer in guidance (Q3(a), Q7), or the scheme's answer line (Q2(a), Q10,
  Q14(b)(ii)); jointly priced pairs (1st @ 8, 2nd @ 4) are unpriced rows.
- Q11(b)(ii) is Q1 and P1 against the hidden solution diagram; Q13(a)(i) is
  axes 2 @ 2, FC 3, VC 5; Q15(a) lists all five required cells; Q15(c)(ii) is
  the answer and its explanation, priced together.
- Figures: five whole-printed-question crops where the figure slot holds a
  hidden solution (Q11(b)(ii), Q13(a)(i), Q15(a), Q15(b)(i)/(ii), Q15(c)(i)); the
  Q15(c)(ii) card now shows the chocolate table.
- Guidance kept, moved off the question side: the Pillar Two €750m turnover
  scope for Q16(b)(ii) is now in the answer guidance, not the stem; the ECB's
  symmetric 2% target (July 2021), migration not raising the world total, the
  age-based dependency ratio, the 0.1 percentage-point unemployment rise and the
  scheme's price-fall wording for a price rise in Q15(c)(ii) stay as guidance.

## 2023 Higher English re-review (2026-10-12)

All 40 paper and 44 scheme pages viewed again (scheme PDF page = printed + 2).
`econ_2023_hl.py` now authors both sections with the lifted-wording method;
`econ_2023_hl_seca.py` and the correction module `econ_2023_hl_review.py` are
retired. 74 routes (24 Section A, 50 Section B). No card ID is removed; the four
required-heading aliases stand.

One route change against the earlier census: **Q16(a)(i)** (individual demand
and market demand) is its own task, `econ-2023-hl-q16-a-i` (4 + 4), no longer
joined to the Q16(a)(ii) car-market diagram and explanation (7 + 8, kept on
`econ-2023-hl-q16-a-ii`). The scheme's four cells sit 4 and 4 beside the two
definitions, 7 beside the diagram and 8 beside the explanation; the earlier
census had kept an aggregate 23 because the two 4s print beside the (ii) stem.
The new ID was never on main; it is an `economicsAdditionIds` entry. The 2023
Higher Irish review received only the matching route change in its Q16 task list
(a/i+ii 23 split into a/i 8 and a/ii 15, the existing Irish answer guidance kept
on a/ii); its reasons and other text were not re-reviewed and still describe
the earlier aggregate. The boundary-corrections entry now points at the
definitions card.

What changed on the cards:
- Every stem and ask is sliced from the paper (the earlier cards had written
  their own, for example "The HHI for the Irish dairy market was 3,172 ...",
  "Choose two policies ...", "(Original 2023 question wording.)").
- Cards that need the printed data now carry it: whole-printed-question crops
  for Q3(a), Q4(a), Q7(a), Q11(a)(i), Q12(b)(i) and Q15(a)(iii) (each holds a
  hidden solution); data crops of the Q3(c) formula (the paper's text layer
  garbles it), the Q12(b) dairy chart for (ii), and the whole Q10 table and
  ladder for B and C; Q3(b) shows the utility table.
- Tariffs as printed: Q12(c) 1st @ 8, 2 @ 5 is one stepped menu of the seven
  For/Against arguments; Q11(c)(iii) is a stepped 5 + 4 menu (one disadvantage
  of each policy); single 6 cells over open lists (Q4(c), Q5(b), Q6(b), Q7(b),
  Q9(b)) are one priced point; Q15(a)(i) and Q14(a)(ii) stay unpriced pairs.
- Q14(a)(iii) institutional unemployment is lifted whole from the scheme's
  column run (the primary extraction splits it with a stray "(b)").
- Guidance kept: the scheme's S1 to S2 wording against its own S to S1 diagram
  (Q7(a)), the euro-cents units of the Q15(a)(i) chart, the award-to-all note for
  Q14(a)(ii), the small mark annotations in Q13(b)(iii) and Q14(b)(i).
- Choose-N rule: no printed choose-N-of-M item pool on this paper.

## 2023 Ordinary English re-review (2026-10-12)

All 32 paper and 32 scheme pages viewed again (scheme PDF page = printed + 2;
the unnumbered annotation table is PDF page 4). `econ_2023_ol.py` now authors
both sections with the lifted-wording method; `econ_2023_ol_seca.py` and the
correction module `econ_2023_ol_review.py` are retired. 61 routes (18 Section A,
43 Section B), every (key, card, marks, topic) tuple equal to the earlier review
and to the 2023 Ordinary Irish review that mirrors it; no Irish file changed.
No card ID is added or removed; the Q10 social-benefit and Q14(a)(ii) effect
aliases stand.

What changed on the cards:
- Every stem and ask is sliced from the paper (the earlier cards had written
  their own, for example "Calculate the level of National Income in 2023",
  "Explain how an increase in interest rates would affect consumers with a
  mortgage", "Ireland's GDP was predicted to increase").
- Figures cropped to the data: the Q5 supply diagram, the Q11(b) cost diagram
  for (i) and (iii) and the Q14 petrol chart for (a)(i) and (a)(ii) replace crops
  that carried clipped stem lines, neighbouring asks and answer boxes.
  Whole-printed-question crops for Q11(b)(ii) and Q16(a)(i), each of which holds
  a hidden solution (the scheme's completed equilibrium diagram; a new crop of
  its completed factors-of-production table).
- Menus are the scheme's bullet lists, including the one-word items the bullet
  splitter drops (Q3(a)(i) "Transport.", Q12(c)(iii) the three pillars).
- Tariffs as printed: jointly priced pairs stay unpriced rows under one total
  (Q8(i), Q8(ii), Q9, Q10, Q11(b)(ii), Q11(c)(ii), Q12(c)(iii), Q13(a)(i),
  Q14(a)(ii)); first/second pairs are stepped menus; Q16(a)(i) is four table
  rows at 4, 8, 4 and 8 for the six 4-mark cells.
- Guidance kept: the paper's "eighth" against the scheme's "second" (Q8(ii)),
  the petrol chart's cent units (Q14(a)), savings rising, falling or unchanged
  (Q13(c)(ii)).
- Choose-N rule: Q16(b)(i) "any two of the above terms" is the only printed
  choose-N-of-M pool, carried as one claim-two card (folded earlier the same day).

Checks: provcheck 3376 claims, 0 untraceable; reconcile 792/793, 0 OPEN (coverage
baseline re-measured); econ_review 16/66 reviewed variants pass; cardlint clean;
refcheck 0 wrong (the 6 unplaced are 2022 OL and 2026 OL cards, unchanged);
7 suites 319/319 after the baseline write; typecheck 0; 23 mobile cases pass
(`tmp/economics-audit/browser-2023-ol-rereview.mjs`).

### Irish browser checks (2026-10-12)

The 2026-10-08 handoff mentions 20 prepared Irish mobile QA cases, but no script
for them exists. Rebuilt from the Irish reviews as 19 + 2 and run in headless
Chrome at 390x844 (`tmp/economics-audit/browser-iv-checks.mjs`): every 2024
Ordinary card that carries Irish answer guidance (19, never run before), plus
`econ-2023-hl-q16-a-ii` and `econ-2023-ol-q16-a-i`, whose Irish task lists took
today's mirror edits. 21/21 pass: the Irish source opens the Irish PDF, its pages
render and navigate, guidance and solution stay hidden until reveal and show
after it, and nothing overflows. Nothing needed fixing.

## 2022 Higher English re-review (2026-10-12)

All 40 paper and 48 scheme pages viewed again (scheme PDF page = printed + 1;
PDF pages 42-45 are the research-project rubric). `econ_2022_hl.py` now authors
both sections with the lifted-wording method and `econ_2022_hl_seca.py` is
retired. 75 routes (24 Section A, 51 Section B), every (key, card, marks, topic)
tuple equal to the earlier review and to the 2022 Higher Irish review that
mirrors it; no Irish file changed. No card ID is added or removed; the Q6
per-diagram aliases and the Q11(c)(iii) against alias stand.

What changed on the cards:
- Every stem and ask is sliced from the paper. The earlier cards had written
  their own (for example a Q2(b) stem about "the quarter Ireland came out of its
  third lockdown", a Q7(a)(ii) stem describing the chart, a Q11(c)(i) ask that
  merged the runway stem into it).
- The twelve `card-corrections.json` entries that patched these cards' topics,
  wording, rows and figure (Q1(a), Q4(b), Q7(a), Q10(a), Q11(a)(i), Q11(b),
  Q14(b)(i), Q14(c)(ii), Q15(a)(i), Q15(b)(iii)) are folded into the authoring
  and removed; the three withdrawal entries stay.
- Menus restored from the scheme's own bullets where the extractor had cut
  them: Q11(a)(ii) (five interventions; the first had been split mid-sentence),
  Q5(a) (the fourth factor prints after the (b) marker; a stray "Adapted from"
  option is gone), Q12(a)(ii) and Q13(b)(ii).
- Tariffs as printed: Q12(a)(i) 3 x 3 is three points; Q15(a)(ii) subsidy and
  quota are two required 4-mark points; Q3(b) and Q14(a)(i) 3 + 3 are the
  explanation and the example; Q4(a), Q4(b) and Q15(c)(i) are unpriced rows under
  their printed totals.
- Figures: new data crops for Q1, Q2, Q10 (schedule and PPF chart together), Q11,
  Q12, Q13, Q14(c), Q15(a), Q15(b) and Q15(c) replace crops that carried
  neighbouring asks, answer boxes and clipped lines. Whole-printed-question crops
  for Q1(a), Q4(a), Q14(a)(ii), Q14(b) and Q15(a)(iii), each of which holds a
  hidden solution (Q15(a)(iii) previously showed only the blank diagram in place
  of its ask).
- Guidance kept: the scheme's "average variable cost" label against the paper's
  average total cost (Q14(b)(i)), its pence-for-pounds wording and the axis label
  (Q15(b)(i)), "2021" against the paper's 2020 (Q7(a)(i)), the capital-spending
  condition (Q11(c)(ii)).
- Choose-N rule: no printed choose-N-of-M item pool on this paper.

Checks: provcheck 3388 claims, 0 untraceable; reconcile 792/793, 0 OPEN (coverage
baseline re-measured); econ_review 16/66 reviewed variants pass; cardlint clean
(the two Q12(c)(ii) cards recorded in cardlint-reviewed.json: "shown" is a verb);
refcheck 0 wrong (Q12(a)(iii) hand-checked); 7 suites 320/320; typecheck 0;
27 mobile cases pass (`tmp/economics-audit/browser-2022-hl-rereview.mjs`).

## 2022 Ordinary English re-review (2026-10-12)

All 32 paper and 36 scheme pages viewed again (scheme PDF page = printed + 1).
`econ_2022_ol.py` now authors both sections with the lifted-wording method;
`econ_2022_ol_seca.py` and the correction module `econ_2022_ol_review.py`
(mentioned in the 2022 notes above) are retired. 62 routes (19 Section A, 43
Section B).

Three route changes against the earlier census. Q3, Q8 and Q14(b) each print ONE
tariff beside the stem across two printed parts (1st x 9, 2nd x 6 for Q3 and Q8;
1st x 10, 2nd x 7 for Q14(b)), the layout 2023 OL Q9 and 2024 OL Q1 already carry
as one task with unpriced rows. Each is now one card on its older (i) ID
(`sa-q3-i` 15, `sa-q8-i` 15, `q14-b-i` 17); `sa-q3-ii`, `sa-q8-ii` and
`q14-b-ii-water` were on main, so each is withdrawn by a card-corrections drop
with a progress alias (Economics aliases 31 to 34). The 2022 Ordinary Irish
review received only the matching task-list collapse for those three questions;
its reasons, guidance and evidence text were not re-reviewed and still describe
the earlier 9/6, 9/6 and 10/7 split.

What changed on the cards:
- Every stem and ask is sliced from the paper (the earlier cards had written
  their own, for example "Set beside a demand-and-supply diagram for Gym + Coffee
  clothing", "Set on a bar chart of the interest paid ...", a Q7(a)(i) ask that
  carried the cost table). The Irish label notes the earlier review placed on
  the Q2(i), Q11(b)(ii), Q12(a) and Q12(b)(iii) asks are kept as they were.
- Tick and two-answer tables are rows under their printed totals: Q4 (1st x 9,
  3 x 2), Q7(a)(ii) (4+4+1+1), Q1(i), Q6(i) and Q11(a)(i) (6+3 / 9+3), Q13(b)(i)
  (12 for I, X, M). Q13(c)(ii) explanation and example are an unpriced 6/4 pair;
  Q14(a)(i) is four rows at 6 lifted from the scheme's table cells; Q15(c)(i) is
  US 6 and UK 6; Q15(a)(ii) is revenue 6 and the services it pays for 3, as the
  scheme's "2 concepts" note prices it.
- Figures: data crops for Q1, Q10 (no figure before), Q11(b), Q12(b), Q13, Q15(a)
  and Q15(c) (no figure before); whole-printed-question crops for Q4, Q7(a)(ii),
  Q7(b), Q9(i), Q11(b), Q12(a), Q12(b), Q13(a)(i), Q13(b)(ii) and Q14(a)(i), each
  holding a hidden solution.
- Guidance kept: the scheme's "€4m to €12m" against the millions axis (Q15(a)(i)),
  the multiplier "will double" line left out (Q13(b)(iii)), the hidden-economy 8
  resolved from the Irish scheme layout (Q16(c)(ii)).
- Choose-N rule: no printed choose-N-of-M item pool on this paper.

Also: `econ-2022-hl-q11-c-i` ("Explain the term opportunity cost.", five words)
is added to `HAND_CHECKED`; the 2022 Higher re-review shortened its ask to the
paper's own words and refcheck listed it as unplaced, which that commit's note
did not mention.

Checks: provcheck 3391 claims, 0 untraceable; reconcile 792/793, 0 OPEN (coverage
baseline re-measured); econ_review 16/66 reviewed variants pass; cardlint clean;
refcheck 0 wrong (3 unplaced, all 2026 OL and unchanged); 7 suites 322/322;
typecheck 0; 21 mobile cases pass (`tmp/economics-audit/browser-2022-ol-rereview.mjs`).

## Regeneration and verification scripts (2026-10-12)

The per-paper scripts used for the 2022-2026 English reviews now live in
`scripts/markbank/authoring/economics/` (they had been in the untracked
`tmp/economics-audit/`). Paths are repo-relative and every script is
idempotent: re-running all of them on this commit changes no committed file.

- `census/census-<year>-<level>.py`: the independent census for one paper,
  written to `drafts/economics-<year>-<level>-ev.json`. Each asserts its route set
  against the recorded review (or the stated route changes).
- `record/record-*.py`: promote a draft to `reviews/` and refresh that paper's
  Atlas mappings (refusing node or page changes); `record/bind-*.py` writes the
  2025/2026 entries in `card-source-bindings.json`; `record/mirror-2022-ol-iv.py`
  is the 2022 Ordinary Irish task-list collapse.
- `crops/crop-*.py`: render, catalogue and register the review figures (PNG,
  `economics-completion-figures.json`, `components/MarkBank/figures.json`);
  `crops/unregister-figure.py <key>` removes one manifest entry before a re-crop.
- `browser/qa.sh <name>` runs `browser/browser-<name>.mjs` (the mobile cases per
  paper, and `iv-checks` for the 21 Irish checks) against `browser/review.html` on
  :5706; `browser/verify.sh <name>` adds the seven suites and the typecheck.
  Output goes to `tmp/economics-audit/`. Needs Google Chrome and playwright-core
  (`PLAYWRIGHT_CORE`, `CHROME_PATH`).

The cards themselves come from `econ_<year>_<level>.py` via `econ_all.py --write`
and `build-deck.mjs`, as before. Earlier one-off migration scripts from the
Codex batches (2022 ledger, 2024 OL integration, the first Irish reviews) are
superseded by these and not kept; the Irish review JSON files are the record.

## 2021 Higher English review (2026-10-12)

First review of this paper (no earlier review JSON; no Irish review, so nothing is
mirrored). Paired visual sweep of all 40 paper and 40 scheme pages (scheme PDF
page = printed + 1; PDF pages 36-40 are the research-project rubric and back
cover). 65 routes: 22 Section A + 43 Section B, every Section B question at 75
and every Section A question at 15 with its (b)/(c) alternative counted once.
`econ_2021_hl.py` now authors both sections from `econ_2026_lib`;
`econ_2021_hl_seca.py` is retired. Census: `economics/census/census-2021-hl.py`;
review recorded and 16 Atlas mappings added by `record/record-2021-hl.py`;
bindings by `record/bind-2021-hl.py` (which also drops the stale `stripStem` on
`q13-a-ii`, set while that card carried a written stem).

Two consolidations (both IDs were on main; aliases 34 -> 36 Economics, 68 -> 70
total, `[110, 24, 81, 12]`):
- Q12(a)(ii): the scheme prints 2 @ 8 (5 + 3) and 2 @ 5 (2 + 3) beside the one ask
  for two positive AND two negative impacts, not tied to either side. One 26-mark
  card on `q12-a-ii-pos`: one menu of the scheme's 5 positive + 8 negative
  headings, claim 4, steps 8, 8, 5, 5 (the 2023 HL windfall-tax layout).
  `q12-a-ii-neg` -> `q12-a-ii-pos`.
- Q16(b)(ii): one 10 (2 @ 5) (2 + 3) cell for one social AND one economic reason.
  One card on `q16-b-ii-social` with two required headings at 5.
  `q16-b-ii-economic` -> `q16-b-ii-social`.

Tariff corrections on kept IDs: `q11-a-ii` 5 -> 8 (the answer "highly
concentrated" 3 + explanation 5), `q11-b-ii` 8 -> 10 ("No" 2 + 2 @ 4), `q15-a`
7 -> 21 (7 + 7 + 7, unpriced rows; the scheme does not say which element earns
which). Q10(b) stays one card whose menu holds the two credited stances (maintain
or decrease); Q14(c)(iii) "choose two" is one any-two card.

Menus restored to the scheme's full headed lists (the earlier cards dropped
entries or mis-split them): Q1(b) 2 -> 3, Q3(b) 2 -> 3, Q5(b) 5 -> 6, Q6(b) 3 -> 4,
Q6(c) a mis-split four -> 4, Q11(b)(iii) 3 -> 4, Q11(c)(ii) 7 -> 8, Q12(a)(ii)
negative 7 -> 8, Q12(b)(i) a mis-split six -> 5, Q15(c)(iii) 3 -> 4, Q16(c)(i)
3 -> 5, Q16(c)(ii) 6 -> 7.

Topics corrected where demonstrably wrong (Atlas nodes follow): Q3(a)/(b) price
discrimination 1-1 -> 2-0 (as 2023/2024 HL file it); Q8 equi-marginal principle
1-4 -> 1-1 (as 2023 HL); Q13(c)(i) the PED calculation 1-1 -> 1-4; Q14(a)(i) the
inflation trend 3-1 -> 3-3.

Wording and figures: every stem and ask is sliced from the paper (the earlier
cards had written stems such as "A basic Netflix account cost far more per month
in Switzerland than in Rwanda" and a Q13(a)(ii) stem describing the scheme's
diagram). New crops (`crops/crop-2021-hl.py`): the Q3 Netflix chart and the Q8
printed ratios (data); the whole printed Q2 and Q13(a) (question crops for cards
whose figure slot holds a solution); the scheme's completed Q13(a)(i) diagram, the
Q13(c)(i) PED working and the Q15(c)(ii) multiplier working (solutions). The
minimum-wage graph now sits on Q16(b)(ii) as well as (b)(i). Q2's statements and
Q9(a)'s structures are rows lifted from the recovered table cells; the HHI answer
is the scheme's 4262 with the squares in the guidance (the text layer flattens
46² to 462).

Notes: the Q15(b)(iii) worked-example alternative is 791 characters, and
`econ_all.py` prints an AUDIT line for it; it is the scheme's own third
alternative, bounded by the next part, and is kept whole.
`econ-2021-hl-q11-c-i` ("Define Internal Economies of Scale.") is added to
`HAND_CHECKED`; `cardlint-reviewed.json` drops the stale `q13-a-ii` entry (the
card now carries its figures) and records `q13-c-ii` ("the figure you have
calculated" is the PED value).

Checks: provcheck 3429 claims, 0 untraceable; reconcile 792/793, 0 OPEN (coverage
baseline re-measured); econ_review 17/66 reviewed variants pass; cardlint clean;
refcheck 0 wrong (3 unplaced, all 2026 OL and unchanged); 7 suites 325/325;
typecheck 0; 22 mobile cases pass (`economics/browser/browser-2021-hl-review.mjs`).

## 2021 Ordinary English review (2026-10-12)

First full review of this paper (no Irish review, so nothing is mirrored; the
targeted Q3 boundary review is kept and its Atlas mapping is replaced by the full
one). Paired visual sweep of all 28 paper and 28 scheme pages (scheme PDF page =
printed + 1; PDF pages 25-28 are the research-project rubric and back cover).
57 routes: 14 Section A + 43 Section B, every Section B question at 75 and every
Section A question at 15 with its (a)/(b) alternative counted once.
`econ_2021_ol.py` now authors both sections from `econ_2026_lib`;
`econ_2021_ol_seca.py` is retired. Census `economics/census/census-2021-ol.py`;
review and 16 Atlas mappings by `record/record-2021-ol.py`; bindings by
`record/bind-2021-ol.py` (dropping the stale `stripStem` on `sa-q2`, `sa-q4` and
`q12-a-ii`).

One task added: Q14(b)(ii) prints a separate 1 @ 8 cell for each objective, and
the shipped card merged both lists into one any-one menu at 8. `q13-c-ii` keeps
Care for the Environment (its citation is now `2021 OL Q14(b)(ii) — care for the
environment` in `econ_refs.CORRECTIONS`) and `econ-2021-ol-q14-b-ii-services`
is new (preservation additions 191 -> 192, `[110, 24, 82, 12]`). No IDs withdrawn.

Tariffs at their printed cells: Q6(b) 10 -> 15 (9 explanation + 6 example), Q9(b)
10 -> 15 (9 then 6), Q12(b) 15 -> 21 (9 then 6 and 6). One cell for two required
headings becomes a heading card at the same total: Q13(b)(i) consumers and
interest rates (2 @ 7), Q16(b)(i) social and economic benefit (2 @ 10), Q16(c)(i)
consumers and businesses (2 @ 8); the earlier cards were any-two menus. First-
correct tariffs on objective answers are unpriced rows: Q2 (1 @ 9, 1 @ 6), Q6(a)
and Q9(a) (1 @ 9, 2 @ 3), Q10(a) (1 @ 9, 1 @ 6). Q11(b)(i) stays two routes
(advantage OR disadvantage). Menus restored to the full lists: Q10(b) 6 -> 8,
Q11(b)(i) advantages 3 -> 8 and disadvantages 3 -> 4, Q11(b)(iii) 6 -> 7,
Q14(c)(iii) 6 -> 7. Topic: Q16(a) factors of production 0-0 -> 0-1, as 2022 and
2023 OL file the same table.

Wording and figures: every stem and ask is sliced from the paper (the earlier
cards had written stems such as "Set on HDI tables for Ireland ..." and "Set on a
photograph of the outdoor flower market ...", and a Q13(c)(iii) ask about "one
type of inflation" where the paper asks for one possible cause). New crops
(`crops/crop-2021-ol.py`): both HDI tables in one data crop (the earlier card
showed 2019 only); whole printed questions for Q2, Q3, Q4, Q8 and Q12(a), each
holding a hidden solution; the scheme's completed Q8 demand-shift diagram. The
paper prints Ireland's 2019 HDI as 0.951 where the scheme's copy of the table
reads 0.942; no answer depends on it.

`econ-2021-ol-q11-c-i`, `q14-b-i` and `q15-c-i` (five-word asks) are added to
`HAND_CHECKED`.

Checks: provcheck 3455 claims, 0 untraceable; reconcile 792/793, 0 OPEN (853
cards, coverage baseline re-measured); econ_review 18/66 reviewed variants pass;
cardlint clean; refcheck 0 wrong (3 unplaced, all 2026 OL and unchanged); 7
suites 328/328; typecheck 0; 21 mobile cases pass
(`economics/browser/browser-2021-ol-review.mjs`).

## Scope boundary (coordinator decision, 2026-10-13)

Current syllabus complete; old-syllabus years need an outgoing spec first.

Economics is complete for its current syllabus: 2021–2026, English editions,
every paper reviewed against its own question paper and scheme (2022–2024 also
Irish). The 2010–2020 papers were sat on the outgoing syllabus (2020 Higher, the
only 2020 paper in the corpus, is a 400-mark paper: six of nine short questions,
then four long questions in answer books; there is no 2020 Ordinary paper).
`curriculumRegistry.ts` has only `economics:current`, and Curriculum Online /
NCCA is the authority for specification transitions, so carding those years
first needs an outgoing Economics specification and topic tree registered as
its own entry, the way the registry handles other transitions. That is separate
curriculum work and is deferred as its own project; no 2010–2020 card is authored
against the 2019 topic tree.

The Higher Irish attachment checks from the earlier reviews are now in the
committed harness too: `browser/browser-2022-hl-iv.mjs`, `-2023-` and `-2024-`
(run with `browser/qa.sh 2022-hl-iv` etc.). Seven of their answer needles quoted
English guidance the re-reviews replaced and were refreshed to the current text;
all three pass (9, 12 and 18 cases). The other one-off Codex scripts in
`tmp/economics-audit/` stay superseded, as recorded above.

## Old-syllabus census and the 2024 HL printed example (lane, 2026-11-04)

Scope moved on from the 13 October boundary above: the 4 November lane brief
puts 2010-2020 in scope under the Economics Topic Atlas taxonomy the Atlas
already uses for those papers (`1`-`9`, `B1`-`B8`); Syllabus X-Ray links for
old-syllabus cards are not required.

**2024 HL Section A Q10(a)(i) is printed matter, not an ask.** Paper p12 says
"use the information above to calculate part (ii). Part (i) has been completed
for you." and prints (i) worked through to "Ans: €325 bn"; scheme p14 prices
(a) at 6 for the (ii) calculation (GNI €326.5 bn). The leaf leaves the
denominator through `PRINTED_EXAMPLES` in paper_census.py (keyed, text-pinned,
raises a `printed-example` flag if the reader stops extracting the recorded
text), so `exclusions/economics.json` is empty and excluded is 0.

**The census now reads 2010-2020** with `econ_legacy_census.py`. The generic
merged walker found 8 to 46 asks per old paper because Section B restarts at
Question 1 (rejected as going backwards, all eight long questions filed under
Section A Q9), numbered table rows ("3. Cyclical unemployment ...") read as
heads, and ruled answer slots "(i)____" read as parts. Every old paper prints
seventeen bold left-margin heads (9 + 8) and marked section banners, so the
walker reads lines by position and weight and keys asks (section, q, letter,
roman); reconcile matches a 4-part key only under the cited section. Its own
check: each Section B question's printed part marks must sum to its printed 75
(all 168 do); each Section A question must print its marks (all 189 do).

Asks per sitting: 2010 HL 54 / OL 73, 2011 55 / 81, 2012 55 / 71, 2013 57 / 76,
2014 54 / 69, 2015 57 / 80, 2016 67 / 82, 2017 66 / 65, 2018 70 / 70,
2019 70 / 67, 2020 HL 75: 1,414 old-syllabus asks. Hand counts from rendered
pages, all exact: 2010 HL 54, 2019 HL 70, 2020 HL 75, 2014 OL 69, 2017 OL 65,
2019 OL 67, and 2011 OL Section A 17. Three page-read rules came out of those
counts: a letter after a letterless roman labels a table row (2020 HL A Q4(ii)
"Tick one option only" over rows (a)-(c)); romans may print out of order in a
grid (2015 OL A Q1, (ii) (iv) above (i) (iii)); two very short asks are recorded
in `SHORT_ASKS` (2010 OL A Q1(i) "IMF", 2014 OL B Q6(a)(ii) "Money;").

Economics: 792/1,219 covered, 1 excluded, 426 open, 40 flags before; 792/2,206,
0 excluded, 1,414 open, 0 flags after. Proof that nothing else moved (isolated
measurement tree, all 54 subjects): every other subject's census and reconcile
JSON identical; Economics 2021-2026 reconcile rows identical except 2024 HL
(75 -> 74 leaves, excluded 1 -> 0); census identical except that leaf and the
2025/2026 HL marks-checksum flags, which compared those papers against the
misread old-paper sum of 66 and no longer fire because the checksum now compares
each era with itself (`era` on the old papers).

## 2019 Higher English, old syllabus (lane, 2026-11-04)

The first old-syllabus paper carded. All 12 paper and 36 scheme pages viewed
(scheme pp1-5 cover, notes, index and the Summary of Mark Allocations, which
agrees with every tariff; paper p12 blank). 70 routes for the 70 printed asks:
14 Section A cards (Q7(a)(i)-(ii) is one card: one 5 + 4 cell over both ticks)
and 56 Section B cards (Q8(a)(ii) is two stance routes because the scheme lists
YES and NO separately). Census `economics/census/census-2019-hl.py`; review and
17 Atlas mappings by `record/record-2019-hl.py` (Section B keyed B1-B8 as the
Atlas numbers it); bindings `record/bind-2019-hl.py`; 17 crops
`crops/crop-2019-hl.py` (10 hidden scheme solutions, 7 paper crops).

Ids carry the section (`econ-2019-hl-sa-q1-a`, `econ-2019-hl-sb-q1-a-i`) and so
do citations ("2019 HL Section B Q1(a)(i)"), because Section B restarts at 1.
`econ_legacy_lib.py` holds the old-paper lifting helpers: the scheme prints
"graded" under its marks cells and the extractor leaves it inside sentences
("...the ability to price graded set..."), so a slice holding it mid-text is
refused and re-sliced from the block-order rendering or the table cells, which
hold the sentence whole; a trailing one is cut off.

Decisions on tariffs the scheme prints without attributing:
- Section A Q6 "11 + 6" beside both definitions, and Q7(a) "5 + 4" beside both
  ticks: questionTotal, unpriced rows (the 2021 HL Q15(a) layout).
- Section B Q4(a)(i) any two of three pairs, "2 @ 6 and 2 @ 4" for the four
  definitions: one menu of all six definitions, claim 4, steps 6, 6, 4, 4 (the
  2021 HL Q12(a)(ii) layout).
- Section B Q5(a)(ii) "4 @ 5" beside four printed lists (advantages and
  disadvantages, banks and consumers), the four heads the ask names: one heading
  row per list at 5.
- Section B Q5(b) "4 @ 4 (2 + 2) + 4": four arguments at 4, and the further 4 as
  a row carrying the scheme's own note beside it ("Note: Must link answers to
  current economic climate ..."). The scheme does not label that 4; the note is
  the only other thing it prints there.
- "graded" single cells (e.g. 5, 6) are one row with the scheme's explanation;
  graded totals over a list (B1(c)(i) 12, B6(a)(i) 8, B6(a)(iii) 9, B6(b)(iii) 8)
  are questionTotal with the listed points as unpriced rows.
Workings set as fractions (A Q1(b), B3(c)(i), B7(b)(iii)) are hidden scheme
crops, with the row holding only the printed answer; the reconstructed
fractions appendix drops their grouping and is not used. The nominal-wage
footnote mark is set back as the superscript the page prints ("inflation²)").

Topic review: Section A Q9 is filed under The Labour Market and Fiscal Policy
(its scheme reasons include income tax revenue and pensions); five commercial
headings for this paper are recorded as reference anomalies (A Q3 under
monetary policy, A Q9 under government intervention, B Q4(c) twice, B Q6 under
globalisation).

Also in this commit:
- `econ_refcheck.py` reads old papers with the census's own line reader
  (`econ_legacy_census.text_and_heads`), keyed (section, question): 0 wrong,
  936 confirmed, 3 unplaced (the 2026 OL three, unchanged).
- #294 had edited four Economics cards (2022 HL Q12(b)(ii) labels; 2023 OL
  Q12(a)(i), Q13(b)(ii) and its trade route) in the authored file and deck only,
  so any regeneration reverted them. Their shapes are now produced by
  `econ_2022_hl.py` and `econ_2023_ol.py`; regenerating leaves all 889 earlier
  cards byte-identical.

Checks: econ_review 19/66; provcheck 3761 claims, 0 untraceable; build 923
cards, 0 dropped; reconcile 862/2,206, 2019 HL 70/70, 0 excluded, 0 orphans;
cardlint clean; seven Economics suites pass.

## 2019 Ordinary English, old syllabus (lane, 2026-11-04)

All 12 paper and 40 scheme pages viewed (scheme pp1-5 cover, notes, index and
the Summary of Mark Allocations, which agrees with every tariff; scheme pp37-40
and paper pp11-12 blank). 66 routes for the 67 printed asks: 13 Section A cards
and 53 Section B cards. Section B Q1(b)(ii)-(iii) is one card, because the
scheme prices a characteristic with its note as one 2 @ 6 over both parts.
Q4(c)(ii) is two stance routes, because the scheme credits YES and NO with
different content. Census `economics/census/census-2019-ol.py`; review and
Atlas mappings `record/record-2019-ol.py`; bindings `record/bind-2019-ol.py`;
13 crops `crops/crop-2019-ol.py` (6 hidden scheme solutions, 5 whole-question
crops, 2 data crops). The scheme .md was generated the way 2019-hl.md
was: `--marks-column`, then tables, blocks (this file only), columns,
fractions and maths.

Decisions on tariffs the scheme prints without attributing them to a response:
- Section A Q3, Q4, Q6 and Q9 print a descending ladder over a list ("1 @ 8,
  1 @ 4, 2 @ 2"; "1 @ 8, 2 @ 4"; "1 @ 8, 3 @ 3"; "1 @ 5, 3 @ 4"). Each is one
  menu claimed at the printed steps. Q9's ladder runs across (a) and (b), so
  it is one card for the question.
- Section A Q1 "8 @ 2" over the eight words of three names: a row for each
  name at 2 marks a word (4, 6, 6).
- Section B Q2(a): the summary (scheme p5) PRINTS the split of the label marks,
  "(i) 11 (5 @ 2) + 1, (ii) 11 (5 @ 2) + 1, (iii) 6 (3+3) + 1 + 1". The graph
  notes (p13) price the labels on one line ("Labels: P, Q, D/C and S/C = 4
  marks"). (i) and (ii) ask for the demand and supply curves to be labelled,
  so their + 1 is D/C and S/C, and (iii)'s + 1 + 1 is P and Q. Each label is
  its own 1-mark row, sliced from that line, and the card's note cites both
  pages. (Corrected 2026-11-04 at the coordinator's review: the first version
  priced the whole labels line, "= 4 marks" in its text, at 1 or 2.) No row in
  the Economics bank prints "= N marks" against a different price; the 2019
  test pins that.
- Section B Q2(b) "2 @ 10 (4 + 4 + 2)" is one column for each situation. Each
  of (i)-(iii) is a card with a row for each situation, and each row pairs the
  situation with the scheme's cell.
- Section B Q3(c)(i), Q5(a), Q5(b), Q5(c)(ii) and Q8(b)(ii) price one response
  for each named head (firms and the economy; students, the university and
  banks; households, firms and government; customers, employees and the local
  community). Each head is a heading row at its printed price.
- Section B Q6(c) "4 @ 6 (3 + 3)": an argument for and an argument against any
  two of three measures. It is one card with a for row and an against row,
  each claimed twice at 6. Every option is named by the measure it is printed
  under ("<measure> — <argument>"; the measure, as the scheme's reprinted
  question bullet prints it, then the table cell). There are 10 for-options
  and 12 against-options.
- Section B Q7(c)(ii): the multiplier answer "2" is a single numeral the md
  loader drops, so it is cut from the raw scheme file. The fraction working is
  a hidden crop.

The 24 "label — value" menu options (Section A Q6's "INJECTIONS — EXPORTS" and
"LEAKAGES — IMPORTS", whose column heading and item are not adjacent in the
text layer, and the 22 Section B Q6(c) options) trace by
halves. That is the build's rule and markBankDeck's rule for a table read
across (2017 HL Biology Q15(b)(i)). `provcheck.mjs` does not have that rule
and reports them as untraceable. The build drops none of them.
`scratchpad/econ-lane/buildrule.mjs` applies the build's exact rule to every
2019 card: 549 claims, 0 untraceable.

Topic review: 7 commercial headings are recorded as reference anomalies:
- Section A Q1 under acronyms (a study-aid heading with no syllabus node).
- Section A Q3 under the labour market (the factors of production are Scarcity
  & Choice, as 2021-2023 OL file the same table).
- Section A Q8 under government intervention.
- Section B Q4 under globalisation (international trade).
- Section B Q5(b)-(c) twice, under globalisation and under formulas.
- Section B Q6 under government intervention (taxation and the Budget).

Refcheck: Section B Q3(b)(i), Q4(c)(i) and Q8(b)(i) are asks of four or five
words, read by hand against paper pp7 and 10 (`econ_refs.HAND_CHECKED`).

Checks:
- econ_review: 20/66.
- build: 989 cards, 0 dropped.
- reconcile: 929/2,206, with 2019 OL at 67/67, 0 excluded and 0 orphans.
- refcheck: 0 wrong, 3 unplaced (the 2026 OL three).
- cardlint: clean.
- The seven Economics suites pass.

## 2019 browser check and two fixes (lane, 2026-11-04)

Every 2019 figure card (34) and one text card in five (21), plus Section B
Q6(c) (OL) and Q8(a)(ii) YES (HL), were checked in installed Chrome at 390x844
and 1440x1000, in light and dark. That is 228 runs. The checks were:
- no solution or answer before reveal;
- every crop loads;
- no horizontal overflow;
- no console errors;
- the official page reader renders.
Screenshots of every screenful are in the lane's economics/shots/. Two defects
were found and fixed:
- HL Section B Q3(b)(ii). The scheme's text layer reports the "<" and ">" it
  prints as the modifier arrowheads U+02C2 and U+02C3. The app font sets those
  as small raised marks ("PED ˂1"). `econ_legacy_lib.traced` now sets them back
  as the signs the page prints. normalise() ignores both forms, so the slice
  still traces.
- HL Section B Q3(c)(i). The working crop carried 30% blank width, which set
  the fraction text at about 10 px on a phone. It is re-cut to the working
  (rect 65, 276, 380, 376), and its manifest hash is updated in place.
Both changes touch these two cards only: the deck diff is those two rows and
one srcHash.

## 2020 Higher English, old syllabus (lane, 2026-11-04)

The last old-syllabus Higher paper. 2020 has no Ordinary paper in this archive.
All 12 paper pages and 44 scheme pages were viewed:
- scheme pp1-4 are the cover, notes, index and the Summary of Mark
  Allocations, which agrees with every tariff;
- scheme pp41-44 are blank or the back cover.

There are 75 routes for the 75 printed asks. Section A has 17 asks and Section
B has 58. Census `economics/census/census-2020-hl.py`; review and Atlas mappings
`record/record-2020-hl.py`; bindings `record/bind-2020-hl.py`; 16 crops
`crops/crop-2020-hl.py`. The scheme .md comes from the 2019 recipe (extract
`--marks-column`, tables, blocks for this file only, columns, fractions,
maths), which reproduces 2019-hl.md byte for byte.

Decisions on tariffs the scheme does not attribute:
- Cross-part ladders are one card each, claimed at the printed steps. The
  2019 OL Q9 precedent applies.
  - Section A Q7: "1st x 9 & 2 x 4" beside (a) and (b), two arguments for and
    one against.
  - Section A Q8: the same tariff over two effects and one measure.
  - Section B Q3(c): "1st: 8, 2nd: 7, 2 x 5", printed beside (c)(ii) and
    printed for (c) as a whole in the summary, over two reasons and two
    measures. That menu has 15 options. `econ_lib.MAX_OPTIONS` was 14 and
    claimed to mirror `optionCapFor('B')`, which is now 25, so it is synced to
    25. The build already allowed 25.
- Section A Q1 "1st @ 10, 2nd @ 6" over the two effects: one menu, steps 10
  and 6.
- Some "N x M" cells sit over two printed sides: Section B Q1(c)(ii) (for and
  against), Q3(a)(ii) (benefits and challenges) and Q7(a)(ii) (positive and
  negative). Each is one menu. Every option is named by the scheme's side
  heading ("For — ...") and traces by halves.
- Diagrams the scheme prices without printed words become ask rows, with the
  scheme's print as the hidden solution: Section A Q4(i) (8), Section B
  Q2(b)(ii) diagram (6) and Q4(b)(ii) graph (10).
- Section B Q4(b)(i) "10 (10 x 1)": the ten values are label-value options
  ("MC1 — 10", "ATC2 — 13.5"). The scheme's printed ATC workings divide 20 by
  each output, although the answers it prints are right. Those workings are
  not shown, and the hidden crop is the completed table alone.
- Stance routes are Section A Q6(ii), Section B Q2(c)(iii) and Q7(c)(i): YES
  and NO each get their own list.

New coordinator rule on crops: no whole-question crops. Where a card's figure
slot holds the solution, the paper's data (the diagram or table alone) is the
question figure, and the typed stem and ask stay
(`econ_legacy_lib.beside_ask`, `questionFigureIncludesPrompt: false`). The
Q9 diagram is cut clear of its answer box. The wide tables (Section B Q1(a),
Q4(b), Q5(b) and Q8(b), about 400 pt) still set near 9-10 px on a 390 px
phone. They are the data the ask needs and cannot be cut smaller.

Lifting fixes in `econ_legacy_lib` (2019 output byte-identical):
- TAIL also trims a page header that has no "Q" and a "1st: 8 2nd:7" ladder
  left at an option's end.
- The B1(b)(ii) age-restriction measure is sliced on its own, because the tail
  trim took its closing "21." for a numeral.
- B2(c)(i) and B8(c)(i) both read "Explain the underlined term.", so each
  reads its stem sentence as part of the ask, passing the duplicate-question
  guard.

Refcheck: Section A Q6(i), Section B Q3(a)(i) and Q4(c)(i) are short asks,
read by hand against paper pp4, 8 and 9.

Topic review: 8 commercial headings are recorded as reference anomalies:
- Section A Q3 and Section B Q3 under government intervention.
- Section B Q5(a)-(b) under employment.
- Section B Q8 under economic concepts.
- Four topical-questions headings (Section A Q5, Q7 and Q8, and Section B
  Q1(c)). No syllabus node falls back to that heading.

Checks:
- econ_review: 21/66.
- build: 1,064 cards, 0 dropped.
- Build rule: 317 claims, 0 untraceable (40 by halves).
- provcheck: 41 more halves-only claims and the ask row, which it does not
  know.
- reconcile: 1,004/2,206, with 2020 HL at 75/75, 0 excluded and 0 orphans.
- refcheck: 0 wrong.
- cardlint: clean.

## 2018 Higher English, old syllabus (lane, 2026-11-04)

All 12 paper pages and 52 scheme pages were viewed. Scheme page numbers here
are the PDF's, two ahead of the printed numbers:
- pp1-5 are the SEC cover, the note, the title, the notes and index, and the
  Summary of Mark Allocations, which agrees with every tariff;
- pp50-52 are blank or the back cover.

There are 72 routes for the 70 printed asks: 13 in Section A and 57 in
Section B. Section B Q5(a)(ii) asks about monetary policy OR fiscal policy,
and Q5(c)(iii) is NO or YES. The scheme gives each its own list, so each has
two routes. Census `census-2018-hl.py`; record and bind
`record/record-2018-hl.py` and `bind-2018-hl.py`; 10 crops
`crops/crop-2018-hl.py` (6 hidden scheme solutions, 4 paper data crops,
none of them a whole question).

Decisions on tariffs the scheme does not attribute:
- Descending ladders over a list are one menu at the printed steps:
  - Section A Q5: "2 x 6, 2 x 2" over the four ticks.
  - Section A Q6: "1 x 5, 3 x 4" over the four canons.
  - Section A Q8: "6 + 6 + 5".
  - Section B Q6(b), Q7(b) and Q8(b): "7+6+6+6", two of each side, not tied to
    a side. One menu of both sides' lists, each option named by its side.
- Section A Q1(a) "8: 4 + 4" beside three statements: any two at 4.
- Section A Q4(b) "6 (2 + 4)" beside the answer and its reason together:
  questionTotal, unpriced rows.
- Graded totals over printed paragraphs are questionTotal with unpriced rows
  (the 2019 HL rule): Section B Q1(c)(ii), Q2(b)(ii) and Q3(b)(ii).
- Section B Q7(a) "4 x 5 (2 + 1 + 2)", each area priced as 2 marks + 1 mark +
  2 marks for an approximate figure, an accurate trend and a comment. Each
  area is a questionTotal card whose rows are the area's figure and points.
  The scheme prints one debt bullet twice; it is shown once.
- Section B Q1(a)(ii) "Diagram: 9 (9 x 1)": the scheme marks nine labels
  with a raised 1, and each label is a menu option at 1.
- Section B Q3(a)(ii) "MC: 7 points x 1 marks, Label: 1 mark": the seven
  values come from the scheme's completed MC table as "output — MC" options,
  plus a 1-mark row for the label.

Lifting fixes in `econ_legacy_lib` (2019 and 2020 output byte-identical):
- `split(..., source='cells')` slices the table-cell rendering. It holds a
  response cell whole, where the other two renderings weave in the marks
  column's notes ("Two points in favour and two against").
- TAIL trims a continued page's "Q Possible responses 7" header.
- The 2018 scheme's arrowhead sub-bullet, private-use U+F0D8, which the
  build's glyph map does not cover, is set as "•".

Refcheck: six asks of four or five words were read by hand against paper pp5,
7, 8 and 10.

Topic review: 7 commercial headings are reference anomalies:
- Section A Q4 under economic concepts.
- Section A Q7 under globalisation.
- Section B Q6(a)-(b) under the financial sector.
- Section B Q7(a) under topical questions.
- Section B Q8(b) under government intervention and under growth and
  development.
- Section B Q8(c) under government intervention.

Checks:
- econ_review: 22/66.
- build: 1,136 cards, 0 dropped.
- Build rule: 337 claims, 0 untraceable.
- reconcile: 1,074/2,206, with 2018 HL at 70/70, 0 excluded and 0 orphans.
- refcheck: 0 wrong.
- cardlint: clean.

## 2018 Ordinary English, old syllabus (lane, 2026-11-04)

All 12 paper pages and 36 scheme pages were viewed. Scheme pages are the
PDF's, two ahead of the printed numbers:
- pp1-5 are the covers, the notes and index, and the Summary of Mark
  Allocations, which agrees with every tariff;
- p36 is the back cover.

There are 72 routes for the 70 printed asks: 17 in Section A and 53 in
Section B. Census, record, bind and crop scripts are `*-2018-ol.py`; the 8
crops are 1 hidden scheme solution and 7 paper data crops, none of them a
whole question.

Decisions:
- Section A Q4(ii) "outline one contribution" of the economist named in (i).
  The scheme lists each of six economists with their own contributions, so
  there is one route per economist (as YES/NO lists are), each claimed at 6
  and counted once. Q4(i) is one card with the scheme's list of names.
- Section A Q3 "2 x 6 & 2 x 2" over four TRUE/FALSE answers and Section A Q9
  "1 x 9 & 2 x 4" over three terms are one menu each at the printed steps.
  Q3 covers (i)-(iv) in one card. Its ask is the paper's words with the
  answer table's header row dropped.
- Section A Q1 "(3+3+3), (2+1+1), (1+1+1)": a row per name at 9, 4 and 3.
- Section B Q5(a)(i) and (a)(ii) "6 (3+3)" beside the answer and its reasons
  together: questionTotal, unpriced rows.
- Section B Q5(b)(i)-(ii) share one "6 x 3" over six table cells, three names
  and three direct/indirect answers. Each part is a card of three 3-mark rows,
  and each tax is named by the paper's own bullet.
- Two-column tables are read from the table-cell rendering, one cell an
  option: positive and negative effects (B3(c)), advantages and disadvantages
  (B2(c)(ii), B4(b)(ii), B5(a)(iii)), and MNC benefits and challenges with
  their statements (B6(b)). B3(a)'s explanation cells are joined across their
  line-end hyphen ("pro- duction"); the gate's comparison ignores the break.
- Required heads are heading rows: B3(c) employees, businesses and
  consumers; B4(c)(ii) banks, businesses and consumers; B8(a)(ii) retailers,
  government finances and the balance of trade; B8(b) employees and
  government, two each.

Topic review: five questions carry a second Atlas node, so commercial
headings that are right stay matches:
- B2: the sugar tax is a Budget tax.
- B3: the minimum wage is a government-set floor whose effects include job
  losses.
- B5: education spending is growth.
- B7: Brexit is EU membership.
- B8: housing measures are intervention.
16 headings remain reference anomalies, among them the study-aid headings
acronyms and formulas, and national income for savings, the budget and
visible trade.

Refcheck: five short asks were read by hand.

Checks:
- econ_review: 23/66.
- build: 1,208 cards, 0 dropped.
- Build rule: 297 claims, 0 untraceable.
- reconcile: 1,144/2,206, with 2018 OL at 70/70, 0 excluded and 0 orphans.
- refcheck: 0 wrong.
- cardlint: clean.
- The seven Economics suites pass (583 tests).

## Old-syllabus census: printed choices and an inline part (lane, 2026-11-04)

While reading 2017 HL, two kinds of printed matter were found mis-keyed by the
legacy walker. They were fixed in `econ_legacy_census.py`, which only the
Economics census and refcheck import:
- A choice of romans is one ask. A letter whose ask reads "any N of the
  following" over more than N romans keeps the romans as its own text:
  - 2017 HL Section B Q1(a): any two of three pairs to distinguish.
  - 2017 HL Section B Q7(c): any three of five economists.
  - 2016 HL Section B Q5(c): any two of three items.
  - 2016 HL Section B Q7(a): any two of three pairs.
  Each had been counted as one ask per roman.
- The next letter printed inside the line it shares with the open one, after
  "and" and opening a sentence. In 2017 HL Section A Q6, "(a) Label the
  lines/curves in the diagram and (b) Use the diagram to explain ..." had lost
  (b).

A before/after census of every 2010-2020 sitting changes exactly these keys
and nothing else:
- 2016 HL goes 67 -> 63.
- 2017 HL goes 66 -> 61. A hand count from the rendered pages gives 61 (12 in
  Section A and 49 in Section B).
- Economics drops 2,206 -> 2,197.
The coverage ratchet refuses a shrinking denominator, so the baseline was
re-measured with `--accept-regression` for this deliberate correction.

## 2017 Higher English, old syllabus (lane, 2026-11-04)

All 8 paper pages and 40 scheme pages were viewed:
- the scheme prints no Summary of Mark Allocations, so every tariff is read
  beside its part;
- scheme page numbers are the PDF's, two ahead of the printed ones;
- p40 is the back cover.

There are 62 routes for the 61 printed asks (12 in Section A, 49 in Section B).
The one extra route is the Section B Q6(b)(ii) good/bad stance, each side
credited with its own table. 17 crops: 11 hidden scheme solutions and 6 paper
data crops.

Decisions:
- Printed choices are one card each:
  - B1(a) "any two of three pairs": six definitions, claimed at 7, 6, 6, 6.
  - B7(c) "any three of five economists". The scheme prices two contributions
    an economist, 5 (3+2) for the 1st correct response and 4 (2+2) for every
    other, so the card claims three economists at 9, 8, 8. Each option is that
    economist's contiguous list from the block-order rendering. A per-
    contribution menu would need 28 options, past the build's 25-option
    ceiling. The economist options run 600-1,800 characters.
- Ladders are claimed at their printed steps:
  - A Q2 "6 + 4 + 3 + 3".
  - A Q4 "6 + 5 + 5".
  - A Q8 "12 + 5".
  - A Q9 "9 + 8" (side-labelled, one advantage and one disadvantage).
  - B8(b) "7 (4+3) + 6 + 6 + 6".
- Diagram tariffs that list their marked elements ("D / S1 / S2 / Indication
  of lower equilibrium price, higher quantity: 1 marks each") are menus of
  those elements at 1 each, split where the scheme prints its slashes. The
  B1(b) explanation is split as the scheme prices it: shift 1, price 1,
  quantity 1, and the printed reason 2 (either of its two bullets).
- Graded totals over printed points are questionTotal with unpriced rows:
  A Q6(b), B2(b)(ii), B4(a)(ii) and B6(a)(i).
- A Q7(a): workings 8 (8 items at 1) and the answer 4. The working is a
  hidden crop, and the row holds its printed line "= - 4 x 0.95".
- B4(b)(i): 5 sectors at 1, 8 flows at 1 each (the scheme's ½ for component
  plus ½ for direction) and the explanation's five bullets at 2.
- B7(b)(ii): four arguments at 5 plus a 5-mark menu of the Irish examples the
  scheme prints.

Refcheck: two short asks were read by hand.

Topic review: 3 reference anomalies:
- A Q1 under government intervention (public pay is fiscal policy).
- A Q9 under government intervention (third-level fees are fiscal policy).
- B8(c) under topical questions.

Checks:
- econ_review: 24/66.
- build: 1,270 cards, 0 dropped.
- Build rule: 332 claims, 0 untraceable.
- reconcile: 1,205/2,197, with 2017 HL at 61/61.
- refcheck: 0 wrong.
- cardlint: clean.

## 2017 Ordinary English, old syllabus (lane, 2026-11-04)

All 12 paper pages and 36 scheme pages were viewed:
- the scheme prints no Summary of Mark Allocations, so every tariff is read
  beside its part;
- scheme page numbers are the PDF's, two ahead of the printed ones;
- scheme pp34-35 are blank and p36 the back cover; paper pp11-12 are blank.

There are 63 routes for the 65 printed asks (12 in Section A, 53 in Section B).
Two cards cover more than one ask, and one ask has two routes:
- B1(b)(i)-(ii) is one card: the scheme prices a barrier with its note, 3 x 7.
- B2(b)(i)-(iii) is one card: one graph priced D 10, S 10, the four labels
  "P, Q, D/C and S/C = 4 marks" on one line, and P1 and Q1 2 x 3. The labels
  line spans (i) and (ii), and with no summary to split it a per-part price
  would be a guess.
- B6(c)(ii) has YES and NO routes, each credited with its own list.

19 crops: 8 hidden scheme solutions and 11 paper data crops. None is a whole
question; each is the table, diagram or formula the ask needs.

Decisions:
- The scheme's text layer sets its spaces as no-break spaces (U+00A0) on 759
  lines. `Old` now reads them as spaces before slicing. No other old-syllabus
  scheme file holds one, so every other Economics card is byte-identical (the
  1,306 cards authored before this paper are unchanged).
- Raised marks beside the figures of a working are claimed as printed:
  - B5(a)(ii): 1 (2), 0.15 (3), 0.25 (3), 2.5 (2).
  - B5(a)(iii): €10 million (2), 2.5 (2), €25 million (2).
  - B6(a)(i): income 1, then the minus sign's 1 and the expenditure's 1 on one
    row (a minus sign is not claimable alone), then the surplus 2.
  - B7(a)(iii): each printed line's three 1s on one row (new exports 3, new
    balance 3), then the surplus 2.
  The text layer sets each raised numeral flat against its figure, so a row
  holds the figure alone and the hidden crop shows the working as printed.
- Ladders at their printed steps: A Q8 10 + 7 (one advantage and one
  disadvantage, priced by order) and B3(c)(ii) 7 + 6.
- Totals over several answers are questionTotal: A Q2(ii) 6, B1(a)(ii) 6 and
  B7(a)(ii) 8.
- Category tables (B4(c)(ii), B7(c)(ii), B8(a)(iii)) name each option by its
  development or area. Where the statement and explanation are adjacent cells
  (B4(c)(ii), B8(a)(iii)) the option holds both; in B7(c)(ii) one statement
  cell heads three explanations, so each option is one explanation.
- B6(b): one argument for and one against any two of three Budget 2017
  measures: two rows of two claims at 6, each option named by its measure.
- A Q4's four statements follow the ask as typed text from the paper's table
  rows, so a phone reader is not left to the table's small print alone.

Refcheck: four short asks were read by hand, and B4(b)(i) folds its stem into
the ask (B3(b)(i) opens with the same six words).

Topic review: 13 reference anomalies, each recorded with the review's reason
(5 are acronyms and formulas study-aid headings).

Checks:
- econ_review: 25/66.
- build: 1,333 cards, 0 dropped.
- Build rule: 264 claims on this paper, 0 untraceable (41 trace by halves).
- reconcile: 1,270/2,197, with 2017 OL at 65/65.
- refcheck: 0 wrong.
- cardlint: clean.

## 2016 Higher English, old syllabus (lane, 2026-11-04)

All 12 paper pages and 40 scheme pages were viewed:
- paper pp9-12 are blank;
- scheme pp1-4 are the covers, the note on published schemes, the title page
  and the notes and index, and p40 the back cover;
- scheme page numbers are the PDF's, two ahead of the printed ones;
- the scheme prints no Summary of Mark Allocations, so every tariff is read
  beside its part.

There are 62 routes for the 63 printed asks (15 in Section A, 48 in Section B):
- A Q8(a)-(b) is one card. The scheme prices two effects of the levy and one
  alternative method on one ladder, 7 (4+3) for the 1st correct response and
  5 (3+2) for each other, so neither part has a price of its own.
- B3(a)(i)-(iv) is one card: one ladder, the 1st correct response 8 and the
  2nd, 3rd and 4th 4 each.
- B8(a) is four cards, one for each printed area, each 5. The scheme prices an
  area "2 marks (approximate figure) + 3 marks (trend 1m + comment on trend
  2m)" without tying the marks to its lines, so each card is questionTotal, as
  2018 HL B7(a) is.

11 crops: 9 hidden scheme solutions and 2 paper data crops. Two crops blank a
sliver of neighbouring print that a rectangle could not leave out without
cutting the diagram's own axis label: the paper Q1 diagram sits beside the "3?"
that ends its ask, and the scheme's beside its answer table's border. Nothing of
either diagram is touched.

Decisions:
- The scheme's text layer reports its round bullet as U+0002 on 116 lines.
  `Old` now reads it as the bullet "•". No other old-syllabus scheme holds one,
  and a diff of economics.json against HEAD shows 1,369 cards unchanged and 62
  added.
- Marked items of a working are claimed one by one:
  - A Q6(i): nine items, each with a raised 1. They are a menu claimed nine
    times at 1: +100, x, €57,000, €63,000, +€6,000, 100, 200, + and 6.67.
  - A Q7(a): the definition is cut where its three printed 3s fall (the money
    supply, interest rates, the availability of credit).
  - B5(b)(iii): the starred working (4, * 1 mark each), Method 1 with Method 2
    accepted, then the answer 4.
  - B5(b)(iv): the five figures, each with a raised 2.
- B4(b)(ii): the MR and MC columns, 4 each. Each cell is sliced and the cells
  are joined with commas. The column-run rendering holds each column whole.
- B4(b)(iii): the graph's five marked elements are a menu at 1 each. The
  profit-maximising output is 3 and its explanation 4.
- Ladders at their printed steps: A Q9 7 + 5 + 5, B3(b)(ii) challenges 4 + 3
  with policies 4 + 4, and B7(c) 7 + 6 + 6 + 6.
- Totals not split: B2(a)(i) 7 (oligopoly with its reason) and the B8(a)
  areas.
- B1(b)(i)-(iv): TRUE/FALSE 2 and the explanation 4, a card for each
  statement.
- B5(c) and B7(a) "any two of three" are one card each, claimed twice at 10.

Refcheck: four short asks were read by hand.

Topic review: 5 reference anomalies, each recorded with the review's reason.

Checks:
- econ_review: 26/66.
- build: 1,395 cards, 0 dropped.
- Build rule: 315 claims on this paper, 0 untraceable (67 trace by halves).
- reconcile: 1,333/2,197, with 2016 HL at 63/63.
- refcheck: 0 wrong.
- cardlint: clean.

## 2016 Ordinary English, old syllabus (lane, 2026-11-04)

All 12 paper pages and 40 scheme pages were viewed:
- paper pp10-12 are blank;
- scheme pp1-4 are the covers, the note on published schemes, the title page
  and the notes and index, and pp37-40 blank or the back cover;
- scheme page numbers are the PDF's, two ahead of the printed ones;
- the scheme prints no Summary of Mark Allocations, so every tariff is read
  beside its part.

There are 81 routes for the 82 printed asks (15 in Section A, 67 in Section B):
- A Q6(a)-(b) is one card. The scheme prices the reason of (a) and the
  measure of (b) on one ladder, 10 for the first correct response and 7 for
  the second.
- B1(b)(ii)-(iii) is one card. The scheme answers both under one "(ii) &
  (iii)" head, 2 x 8 (state 4 + explain 4), and names the characteristics
  only.
- B5(a)(iii) has FOR and AGAINST routes, each credited with its own list.

8 crops: 2 hidden scheme solutions and 6 paper data crops. None is a whole
question.

Decisions:
- First-correct-response ladders are claimed at their printed steps:
  - A Q1 8 + 4 + 4.
  - A Q2 and A Q5 8 + 4 + 2 + 2.
  - A Q8(b) 8 + 4.
  - A Q9 8 + 3 + 3 + 3, over the four symbols the paper leaves blank. It prints
    Y1 and Q2.
- A Q4's figures are claimed one by one, as "Each correct figure" prices them:
  (a) 5 x 2, (b) 3 x 1 and (c) 3 x 1.
- B2(a)(i) and (ii) are a card each. The scheme's item table prices each label
  (2) and each equilibrium mark (2) on its own row, though one graph answers
  both.
- B2(b): one card per question, a row per factor, from the scheme's two-column
  table.
- B5(a)(i): each tax's explanation 3 and an example 2, the examples a menu.
- B5(b)(ii), B4(a)(iv) and B8(b)(ii): a heading row per printed category, any
  one of its responses.
- B7(c)(i): the EU 4 and GDP 6, the scheme's "10marks (4+6)" in the order
  printed.
- B8(b)(iii): any acceptable infrastructure 4 (the scheme's four as examples)
  and a reason 4, each reason named by its example.
- B8(c) "any three of four groups" is one card, claimed three times at 8.
- Six asks print "Explain the underlined term." three times on one page. The
  stem is folded into each so the card names its term. Refcheck places all
  six.
- A Q1 sets the paper's ruled blanks as ellipses, so the statement still reads
  as one to complete.
- B1(c)(ii) "raise the legal age ... to 21." is sliced whole. The shared
  trailing-numeral cut would take "21." for a list number.

Refcheck: four short asks were read by hand.

Topic review: 9 reference anomalies, each recorded with the review's reason
(5 are acronyms and formulas study-aid headings). B8 also files under
government intervention, as 2016 HL B7(c) does, for the government's
environmental taxes, grants and subsidies.

Checks:
- econ_review: 27/66.
- build: 1,476 cards, 0 dropped.
- Build rule: 376 claims on this paper, 0 untraceable (49 trace by halves).
- reconcile: 1,415/2,197, with 2016 OL at 82/82.
- refcheck: 0 wrong.
- cardlint: clean.

## Batch 2 browser check: printed statements in four question texts (lane, 2026-11-04)

The batch-2 phone check (390 px) showed four cards whose items appear only in a
wide printed table, set at phone width with text near 7.6-8.3 px. Each card's
ask cannot be answered without those items:
- 2017 HL Section A Q2, true or false;
- 2018 HL Section A Q5, true or false;
- 2017 OL Section A Q1, taxes to explanations;
- 2016 OL Section A Q5, ideas to economists.

Each now carries the paper's printed items after its ask, sliced from the
paper's text layer, as 2017 OL A Q4 and 2016 OL A Q2 already did. The matching
tables are set column by column, as the page prints them. The text layer
interleaves the two columns row by row, which would set each tax or idea
beside an answer it is not. The table crop stays beside the typed text. Only
these four cards' questionText changed. Every other card is byte-identical,
and refcheck places all four.

## 2015 Higher English, old syllabus (lane, 2026-11-04)

All 12 paper pages and 40 scheme pages were viewed:
- paper pp10-12 are blank;
- scheme pp1-4 are the covers, the note on published schemes, the title page
  and the notes and index, and pp37-40 blank or the back cover;
- scheme page numbers are the PDF's, two ahead of the printed ones;
- the scheme prints no Summary of Mark Allocations, so every tariff is read
  beside its part.

There are 58 routes for the 57 printed asks (14 in Section A, 43 in Section B).
The one extra route is the Section B Q8(a) agree/disagree stance, each side
credited with its own list; both carry the scheme's 6 (3 + 3) for reference to
the Irish economy. 11 crops: 9 hidden scheme solutions and 2 paper data crops.

Decisions:
- From this paper on, a stem stops before any printed table, and the table is
  the crop beside the typed ask (the coordinator's ruling: tables are never
  typed into a question). The A Q7 true/false statements are typed after the
  ask, as they must be read to answer.
- A Q1: the scheme prints one answer and prices "3 points of information: 8 +
  4 + 4". The three points are the phrases it sets in bold (scarce resources
  with alternative uses; unlimited wants; choices with an opportunity cost),
  claimed at the printed steps.
- B2(a)(ii): the diagram's 11 printed points are a menu at 1 each. The 14-mark
  explanation is one row per numbered head the scheme prints (equilibrium 1 + 2,
  price and output 2 + 1, cost 2, SNP 1 + 2, inefficiency 1 + 2). The build's
  6-row cap rules out a row per mark.
- B1(b)(i)-(iii): diagram elements at 1 each, then shift, price and quantity at
  1 and the reason for the shift 2. The reason is the scheme's second bullet;
  its other bullets describe how the market moves to the new equilibrium. The
  new equilibrium's raised 2 is set back as PE² and QE² (the build folds ²).
- B4(c)(i)-(ii): "3 at 5 marks (1 + 2 + 2)" is read by the scheme's Statement /
  Explanation / One main influence columns. (i) is three motives at 3 (1 + 2)
  and (ii) is three influences at 2.
- B6(a)(i): "No: 2 marks + 3 reasons at 5". The scheme credits No only.
- B3(b)(iii): the short run with its reason, printed as one 3: questionTotal.

Refcheck: two short asks were read by hand.

Topic review: 1 reference anomaly. A Q9 sits under the commercial government
intervention heading, but the review files it as population ageing (Economic
Growth), with its policies under fiscal policy and the labour market.

Checks:
- econ_review: 28/66.
- build: 1,534 cards, 0 dropped.
- Build rule: 320 claims on this paper, 0 untraceable (59 trace by halves).
- reconcile: 1,472/2,197, with 2015 HL at 57/57.
- refcheck: 0 wrong.
- cardlint: clean.

## 2015 Ordinary English, old syllabus (lane, 2026-11-04)

All 12 paper pages and 36 scheme pages were viewed:
- paper pp11-12 are blank;
- scheme pp1-2 are the cover and the note on published schemes, pp3-4 the
  title page and the support notes with the index, and pp34-36 blank;
- scheme page numbers are the PDF's, two ahead of the printed ones;
- the scheme prints no Summary of Mark Allocations, so every tariff is read
  beside its part.

There are 71 routes for the 80 printed asks (18 in Section A, 62 in Section
B). There are fewer routes than asks because a ladder the scheme prices
across parts is one card: A Q1 and A Q2 (four spaces each), A Q5(a)-(b),
B1(b)(ii)-(iii), B2(a)(i)-(iii) and B5(c)(i)-(iii). Section B Q4(c)(ii) has one
route for each economist the scheme names (Marx, Smith, Malthus, Ricardo), and
the question's 75 counts one of them. 12 crops: 5 hidden scheme solutions and
7 paper data crops.

Decisions:
- Stems stop before printed tables, and each table is the crop beside the
  typed ask. Printed items that must be read to answer are typed from the
  text layer: the A Q2 sentences (the table's header row dropped), the A Q4
  word list and statements (ruled blanks set as an ellipsis), the A Q6
  letters, the B3(a)(iii) costs, and the B5(c) rates, which are two boxed
  lines and not a table. B6(a)'s two budget figures are one printed line of
  labelled values, so they stay in the stem.
- Ladders are claimed at their printed steps: A Q1 and A Q2 8 + 4 + 2 + 2, A
  Q4 6 + 6 + 2 + 2, A Q5 6 + 6 + 4 (its (a) and (b) share one ladder, so one
  card), A Q6 6 + 6 + 5, A Q7(ii) 4 + 3, B1(a)(ii) 3 + 2, B3(c)(ii) 6 + 3 and
  B5(c) 12 + 6 + 6 (one card for (i)-(iii)).
- B3(b)(i): the scheme prints "7 marks" beside the national minimum wage but
  sets it as 4 + 2, and only 6 fits the paper's (24) for (b) with labour at 6
  and (ii) at 2 @ 6. It is priced 6.
- B2(b): each development's row carries the scheme's alternative answer (the
  design fault may shift demand left; the Apps may shift supply right) as an
  accepted alternative for (i) and (iii); its direction matches (ii) anyway.
- B6(b)(iii): the scheme prices its Statement and Explanation columns apart
  (12 marks: 2 at 3 marks, 2 at 3 marks), and its cells never print a
  statement beside its own explanation, so the card is two rows: a statement
  2 @ 3 and an explanation 2 @ 3, each response named by its category.
- B6(a)(i) and B5(a)(iii): the raised marks beside the working are each a
  claim (B6(a)(i) 1 + 2 + 2 with the minus sign joined to the expenditure
  figure), and the working is the hidden solution crop.
- B8(c)(ii): "each * figure at 2 marks": the four starred figures are a 4 @ 2
  menu, with the working as the hidden crop.
- B1(b)(ii)-(iii) is one card: the scheme prices each characteristic with its
  note, 2 at 8 (4 + 4).

Refcheck: three short asks were read by hand (B1(c)(i), B3(a)(i), B5(b)(i)).

Topic review: 11 reference anomalies, each a commercial heading the review
files elsewhere. A Q6, B4(b) and B6 sit under acronyms and B8 under formulas
(study-aid headings). A Q1 sits under the labour market, but land is a factor
of production. A Q4 and B5 sit under globalisation, but visible trade and the
exchange rate are international trade. A Q3 sits under government
intervention, but corporation tax is fiscal policy. A Q8 sits under government
intervention and under growth and development, but emigration is employment
and unemployment. B6 sits under national income, but the current budget is
fiscal policy.

Checks:
- econ_review: 29/66.
- build: 1,605 cards, 0 dropped.
- Build rule: 283 claims on this paper, 0 untraceable (44 trace by halves).
- reconcile: 1,552/2,197, with 2015 OL at 80/80.
- refcheck: 0 wrong.
- cardlint: clean.

## 2014 Higher English, old syllabus (lane, 2026-11-04)

All 12 paper pages and 40 scheme pages were viewed:
- paper pp9-12 are blank;
- scheme pp1-4 are the cover, the note on published schemes, the title page
  and the support notes with the index, and pp38-40 blank or the back cover;
- scheme page numbers are the PDF's, two ahead of the printed ones;
- the scheme prints no Summary of Mark Allocations, so every tariff is read
  beside its part.

There are 54 routes for the 54 printed asks (10 in Section A, 44 in Section B),
one card per ask. No printed choice is credited with a list for each side. 12
crops: 10 hidden scheme solutions and 2 paper data crops.

Decisions:
- The scheme draws its bullets in SymbolMT, and the text layer reports each one
  as the letter "x" at the start of a line. No slice crosses one. A bullet list
  is cut at its bullets. A response whose bullets belong together (the B1(c)(i)
  and B2(b)(i) explanations, two A Q8 implications) is read where the scheme
  file prints it without them (its column rendering), so it still traces. The
  B5(c)(ii) response does not appear whole in any rendering. Its row is the
  scheme's concluding bullet (GNP is probably the better measure), and the
  whole six-bullet response is the hidden crop.
- Ladders are claimed at their printed steps: A Q5 6 + 5 + 5, A Q6 and A Q7
  10 + 7, A Q8 11 + 6, A Q9 5 + 4 + 4 + 4 (two costs and two benefits on one
  ladder), B2(a)(i) 5 + 4 + 4, B2(c) 5 + 5 + 5 + 4 after the 1 for oligopoly,
  B6(c) 7 + 6 + 6 + 6, B8(b)(ii) 6 + 5.
- A diagram the scheme prices without words (B1(b)(i) 4, B1(c)(i) 8,
  B2(b)(i) 10) is claimed by the card's own ask, with the scheme's diagram as
  the hidden figure.
- B4(a): each term's explanation is a row at 3, and the examples are a 4 @ 2
  menu. The scheme prints an example for derived demand only and "Appropriate
  example." for the others.
- B3(b) is one unnumbered part with three asks (calculate, elastic or
  inelastic, the implication): one card, 10 + 2 + 8, with the working as the
  hidden crop.
- B5(a)(i)-(iv) each have their working crop as the hidden figure, and the
  data table is the crop beside each ask.
- B2(b)(i): one crop blanks the heading below the diagram, "Explanation of
  long run equilibrium:", which sits level with the Q2 and Quantity labels.
  Nothing of the diagram is touched.

Refcheck: one short ask was read by hand (B7(a)(ii)).

Topic review: no reference anomalies. All 16 of the commercial reference's
2014 Higher associations match the review.

Checks:
- econ_review: 30/66.
- build: 1,659 cards, 0 dropped.
- Build rule: 223 claims on this paper, 0 untraceable (13 trace by halves).
- reconcile: 1,606/2,197, with 2014 HL at 54/54.
- refcheck: 0 wrong.
- cardlint: clean.
