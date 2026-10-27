## Current checkpoint — ALL 68 EV papers published, 2026-10-23

Supersedes every count below. English-language (EV) editions 2010-2026 are
complete; Irish-version (IV) editions stay deferred (Alex, 2026-10-11).

- Published 68/68 EV papers, 2,685 cards (higher 738, ordinary 1,947);
  publisher refuses 0. All 650 legacy runtime cards are bridged, so the
  served English bank is exactly these 2,685 cards. Aliases 159.
- Denominator: 2,724 printed tasks by independent visual tally (68 papers,
  every sweep complete) minus 39 declared printed repeats = 2,685 asks.
  `paper_census.py english`: 2,685 leaf asks, 0 flags, 0 unreadable.
  `reconcile.py english --baseline check`: 2,685/2,685, 0 excluded, 0 open,
  0 orphans, 0 unparsed (exit 0). No exclusions exist.
- This round (oldest first): a1bcd915d 2017 OL P2 (Q1(b) and Q2(b) both
  published, Alex's decision: Q2(b) carries its printed lead-in),
  eebbb7858 2019 HL P1, 3a410b2f8 2019 HL P2, c10e77865 2019 OL P1,
  687f59002 2019 OL P2, e2d250549 2020 HL P1 (+ 2020 HL/OL grid sittings),
  0c9a25203 2020 HL P2, 4993bc443 2020 OL P1, 4523b270e 2020 OL P2 (+ 2020
  "F 1984" scheme-crop anchor, asserted), b817b4bc7 scheme .md for 2017/2019/
  2020 (markBankDeck needs one per sitting the deck draws on), 26b5f42df
  2011 OL P2 text-repair guard test.
- Whole-subject audit (scratchpad `audit_english.py`, every published card):
  all 2,685 resolve to an Atlas heading through their answer-map block (68
  maps hosted byte-identical and listed in HOSTED_ANSWER_OVERRIDES); every
  questionRef agrees with year/level/paper and with its cited block's
  section; every questionText is printed on its cited paper pages (2,663 via
  the text layer; 2011 OL P2 and the 2022 HL P2 Dickinson fragment via the
  page's own glyphs; 2013 OL Comparative B joins its printed aspect list to
  part (a) across the "(a)" marker). cardlint's rules applied to the English
  decks: 0 scheme-leak, 0 label-junk; 4 ghost-figure regex hits all
  reviewed (3 are "shown" used as a verb; 2020 HL composing 3 cites the TEXT
  2 extract as context only, like every composing lead-in). Since
  2026-10-25 `cardlint.py english` reads the served deck (all 2,685
  published cards, via DECK_LOADERS) and prints the count it read; the
  four hits are resolved in the lint itself (English "shown" rule, one
  reviewed entry).
- Checks at 26b5f42df: typecheck clean; typecheck:test only the 3
  pre-existing errors; lint (--ignore-pattern 'tmp/**') clean; build OK;
  full vitest 222 files / 5,373 tests pass (an earlier run's musicExamTopics
  30 s timeout was load only: 21/21 alone); Python English tests 81 pass; browser QA desktop + phone for the
  2017 (10 cards), 2019 (12) and 2020 (13) groups all ok.
- Printed misprints carried verbatim (lift rule): 2020 OL P2 Prescribed C
  Q1(a) "about the the baby" (paper PDF16, viewed); 2020 HL scheme PDF26
  names The Handmaid's Tale in the Persuasion (ii) note (not quoted on the
  card).
- Done 2026-10-25: Paper Trail answer-map labels no longer title-case
  after apostrophes ("Handmaid’s", "Yeats’s") and 2019 OL P2 keeps
  "(Extract: Lines 45 – 76)" — `title_case()` in
  scripts/paper-trail/english_p2_complete.py. Both P2 generators were
  re-run: 60 labels in 24 maps changed and nothing else (every region,
  page and band identical); Mark Bank cards unchanged.
- Integration: rebase onto current main as its own ship step; recompute the
  shared totals (cardAliases.ts, sizes.json, coverage-baseline.json,
  markBankCardPreservation totals) from the merged decks.

---

## Previous checkpoint — printed choices collapsed, 2026-10-12

Supersedes the card counts below (c1d45e931).

- RULE (coordinator): route cards only when the scheme prints different
  marking content per route. All 221 former `finite` decisions are now
  `printed-choice` (pools kept and validated, `printedChoices` = combination
  count); each is ONE card with a task-check line stating the printed choice.
  `english_choices.enumerate_choices` still lists every combination for tests.
  The publisher refuses label-only route groups.
- Repeated printed tasks: `scripts/markbank/authored/english-printed-duplicates.json`
  (6 entries); the canonical card keeps the others as `atlasPlacements`.
- Published 36 papers / 1,329 cards; decks higher 573, ordinary 1,364;
  aliases 38. Coverage 1,947/2,522 (575 open, declared).
- DO NOT re-run the old `tmp/english-audit/record-*.py` scripts: they write
  `finite` decisions back. If one must be re-run, re-run
  `tmp/english-audit/collapse-printed-choices.py` after it.
- Open: 2018 OL P1 A(iii)(b) is printed identically under all three texts
  but each copy carries its own TEXT reader, so it is not merged (needs a
  reader decision). Indicative bullets render without markers (existing
  SessionScreen display; candidate UI fix).
- NEXT: bridge extension for legacy withdrawn aliases, then 2025 OL P1/P2,
  2024-2021 (fix legacy HL Comparative Q1(a)/(b) grid in place with a
  correction record), 2016 P2, 2017, 2019-2020. One commit per paper.

---

## Current checkpoint — batch 3: 2026 complete, 2025 HL bridged, 2026-10-12

Supersedes the counts below.

- Published: 36 papers / 1,963 cards (2010-2015 all four, 2016 HL/OL P1, 2018
  all four, 2026 all four, 2025 HL P1 + P2). Gate: 68 papers, 2,724 base tasks,
  3,788 routes; pending taskSelections 10 / raw 1,016 / scheme 1,380 /
  paperReviews 32. Coverage baseline 2,581/3,156, 575 open (declared).
- Commits: a95c7a065 (reviewed answer maps hosted byte-identical in
  public/paper-answers + HOSTED_ANSWER_OVERRIDES; OL P2 scheme crops repaired),
  9b765abd7 (printed-case headings/titles; poet headings out of prompts; 2024
  OL P2 "Reflective/Hopeful/combination" -> one open response), c1e3b35de (2026
  OL P1, 22 tasks / 390 routes), 9d882850a (2025 HL P1 19/20, P2 27/27).
- LEGACY BRIDGE: `scripts/markbank/authored/english-legacy-bridge.json`. A
  2021-2025 paper publishes only when the ledger maps EXACTLY its legacy ids
  (authored.json) to reviewed cards: `same-id` (published card keeps the id) or
  `alias` (registered in components/MarkBank/cardAliases.ts — the publisher
  refuses until it is). Ledger written by `tmp/english-audit/write-legacy-bridge.py`.
  Manifests carry `bridgedPapers`, `bridgedLegacyIds`, `bridgeAliases`; the
  factory stops generating bridged legacy cards; reconcile/paper_census count
  the bridged paper by its published cards. authored.json never changes.
  2025 HL: 42 legacy ids -> 37 same-id + 5 aliases (P1 Composing 2 -> route 1;
  P2 Comparative A/B/C Q1 and Unseen Q1 -> part (a)). Lifted indicative
  material (verbatim, publisher-checked against the scheme page) replaces the
  old hand paraphrases on the six P1 QA(i)/(iii) cards.
- Atlas archive topics are now append-only (english_publish.py keeps existing
  order); re-run `node scripts/paper-trail/build-english-geography-exam-topic-runtime.mjs`
  after publishing. 67 additive archive topics; 965 exact mappings.
- KNOWN LEGACY DEFECT (fix when bridging): 2021, 2023 and 2024 HL schemes print
  ONE combined row for Comparative Q1(a) 30 / Q1(b) 40, but the legacy cards
  score them as discrete PCLM. Reviewed 2025/2026 cards use the combined row.
- OPEN DECISION: 2026 OL P1 Q A(iii)(a) is printed identically under all
  three texts; legacy 2022-2025 OL deduplicated such prompts via aliases, the
  reviewed publish keeps three copies (6 cards). T3 A(i) choose-two-of-eight
  plus one is 360 mechanical routes.
- NEXT: 2025 OL P1/P2 (legacy bridge; 2025 OL P1 already has 2 withdrawn
  aliases that the bridge must map), then 2024-2021, 2016 P2, 2017, 2019-2020.

---

## Current checkpoint — runtime publisher shipped on branch, 2026-10-11

Supersedes the counts below for runtime/Atlas state; review ledgers unchanged.

- `english_publish.py` publishes paper by paper: only papers whose OWN gate
  (`english_review_gate.check_paper`) passes. 33 papers / 1,526 cards today
  (2010-2015 all four, 2016 HL/OL P1, 2018 all four, 2026 OL P2, HL P1, HL P2).
  `--check` must stay clean; regenerate after recording any new paper review.
- Legacy 2021-2025 (650 cards, 10 aliases) untouched; refused for publication
  until `english-legacy-bridge.json` maps every legacy card of a paper.
- Grids/caps: `english-marking-grids.json` (exact prints; bound to scheme sha +
  page cells). HL 2010-2015 no cap, OL 2010-2015 Language-at-D, 2016/2018 HL/
  2026 C/L<=P, 2018 OL none. Runtime `capRule` + `printedGrid`.
- Atlas: 65 additive archive topics (builder reads
  `data/examTopics/english-reviewed-archive-topics.json`; re-run
  `build-english-geography-exam-topic-runtime.mjs` after publishing) and exact
  booklet links unioned in the registry (771 -> 954 mappings). 2026 OL P2's 19
  blocks wait for its answer-map upload + index rebuild (answers flag).
- Coverage baseline (English only): 2186/2783 covered, 597 open declared
  (unreviewed candidate tasks of the 15 non-legacy, unpublished papers).
- Browser QA: `tmp/english-audit/run-published-browser.sh` (port 5702, QA-only
  vite config allowing the symlinked pdf.js worker, local PDF mirror).
- NEXT reviews: 2026 OL P1, 2025, 2016 P2, 2017, 2019-2024; each new reviewed
  paper then publishes by re-running the publisher (+ Atlas builder, baseline).

---

## Current checkpoint — 2026 Higher Paper 2 recorded, 2026-10-11

Supersedes the counts below. Recorded by `tmp/english-audit/record-2026-hl-p2-review.py`.
2026 OL P2, HL P1 and HL P2 are now fully reviewed; 2026 OL P1 is the only
2026 paper still open (2 pages viewed earlier, nothing recorded).

- All 8 paper pages viewed. Scheme text PDF22–57; PDF22–50, 52 and 54 viewed.
- Independent tally **27 tasks / 28 routes**: Single 5 × (i)/(ii) 60; Comparative
  3 × (Q1(a) 30, Q1(b) 40, Q2 70); Unseen Q1(a) 10, Q1(b) 10, Q2 20 (either Q1
  or Q2); Prescribed 5 × 50. Only finite pool: General Vision Q1(a)
  “predominantly emotional or rational” (scheme PDF37 “should decide which is
  the more dominant”, same rule as 2016 OL T1 A(ii)). Q1(b) stays flexible:
  the dominant response is decided per freely chosen text and may differ.
- Poet headings removed from prescribed prompts via `promptHeading` (as
  2010–2015; NOTE 2018 HL P2 still carries the heading in its prompts — fix
  deliberately with its review hashes if wanted). Unseen reader “Library”
  (Alvy Carragher) PDF6.
- Criteria: Single 60, Comparative 70, Prescribed 50 discrete (C/L ≤ P);
  Comparative 30/40 and Unseen 10/20 holistic H1–H8 (PDF52, PDF54).
- 37 raw hits classified (16 task, 16 rubric, 1 poem line, 4 notice).
  Gate: routes 3,800; pending taskSelections 10 / raw 1,079 / scheme 1,448 /
  paperReviews 35. Python 45 tests, TS 132 tests, diff check pass.
- NEXT: 2026 OL Paper 1, then 2025 (newest first), then 2016 P2, 2017,
  2019–2024. Publisher work is a separate coordinated task.

---

## Earlier checkpoint — 2026 Higher Paper 1 recorded, 2026-10-11

Recorded by `tmp/english-audit/record-2026-hl-p1-review.py`.

- All 12 paper pages viewed (PDF9–11 “no examination material”, PDF12
  acknowledgements/copyright). Scheme (shared HL P1/P2) text PDF4–21, 51–57;
  PDF4–21, 52 (H1–H8 grids) and 55 (misreading rules) viewed.
- Independent tally **19 tasks / 20 routes**; only finite pool composing 5
  for/against (scheme PDF19 “argue on one side”). T1 B register, T3 A(i)
  either/both extracts and T3 A(iii) either/both writers are flexible.
- Readers now under printed headings: TEXT 2 “Influential Life Moment” and
  TEXT 3 “Influence of the Arts” (the extractor had taken the introduction
  sentence as the title). Composing 6 keeps TEXT 2 PDF4–5 under its printed
  heading (replaces an unreviewed invented title). B tasks carry no reader.
- Criteria: QA 15/20 holistic H1–H8 (PDF52); B 50 and composing 100 discrete,
  C/L ≤ P (PDF4). T3 A(ii) prints “Okora” (passage/scheme Okoro); kept.
- All 42 raw hits classified (9 task lines, 2 rubric, 27 passage prose,
  4 notice). Gate: routes 3,799; pending taskSelections 10 / raw 1,100 /
  scheme 1,475 / paperReviews 36, none from 2026 HL P1. Python 44, TS 132.

---

## Earlier checkpoint — 2026 Ordinary Paper 2 recorded, 2026-10-11

Batch order is now NEWEST FIRST (2026 OL P2, then 2026 HL P1 and HL P2).
Recorded by `tmp/english-audit/record-2026-ol-p2-review.py`.

- All 20 paper pages viewed one by one. Scheme (shared OL P1/P2 scheme) text
  PDF3, 4, 22–72 read; PDF3 and 22–72 viewed as rendered pages, including the
  Appendix grids PDF71 (discrete O1–O8) and PDF72 (combined O1–O8).
- Independent tally **104 tasks / 105 routes**: Single 9 × (Q1(a)(b)(c) 10 +
  Q2–Q4 30) = 54; Comparative 3 modes × 2 questions × (15 + 15 + 40) = 18;
  Unseen 2 × 10; Prescribed 6 × (15 + 15 + three 20-mark alternatives) = 30.
  Only finite pool: Unseen Q2 sad/hopeful (scheme PDF57 “ultimately choose one”).
- **Changed an earlier unreviewed decision**: Prescribed Q1(b) “positive or
  negative or both positive and negative” (×6) is now `flexible`, not three
  routes, matching reviewed 2010/2013/2014/2015 “X or Y or both” precedent
  (−12 routes). 2024 OL P2 “Reflective / Hopeful / a combination of both” is
  still an unreviewed three-route expansion: decide it the same way when 2024
  is reviewed, or record why it differs.
- Readers: unseen Long Distance (Moya Roddy) PDF14 only; each prescribed poem is
  complete on ONE page (identity `sourcePages` 15–20; the default two-page span
  opened the next poem). Title “It’S Not” corrected to “It’s Not”.
- Scheme errata recorded (paper wording kept): PDF68 prints “ex 20” boxes under
  poem F Q1(a)/(b) though both print (15) — tariff 15, combined 9/6; several
  single-text reprints differ slightly (see task-review reasons).
- Comparative Q1(b) and Q2(b) print IDENTICAL wording in all three modes; the
  extractor’s `schemePage` for Q2(b) therefore points at Q1(b)’s page. The
  reviewed `schemePages` in `english-task-review.json` are correct
  ([52,53], [54,55], [56]); the publisher must use those.
- All 167 raw hits on this paper re-classified from the viewed pages (118
  task lines, 37 rubric, 7 poem lines, 5 copyright notice); earlier
  auto-suggested two-task links replaced with single-task links.
- Gate report after recording: routes 3,799; pending taskSelections 10 /
  rawDirectives 1,133 / rawLinkedTasks 0 / schemeTasks 1,494 / paperReviews 37,
  none from 2026 OL P2. Python 43 tests, TS 132 tests, diff check pass.

---

## Earlier checkpoint — 2016 Paper 1 (HL and OL) recorded, 2026-10-11

Supersedes the counts below; everything else in the next section still applies.
Recorded by `tmp/english-audit/record-2016-p1-review.py` (ignored; never rerun
`record-2014-ol-p2-review.py`). No commits, baselines or other years touched.

- All 24 paper pages viewed (PDF9–12 blank in both). Scheme text HL PDF3–17,
  39, 40, 43; OL PDF3–13, 51, 52. Grids/decision pages viewed: HL PDF10, 40;
  OL PDF5, 52. Independent tallies: **HL 19 tasks / 34 routes**, **OL 22 / 39**.
- OL Text 1 A(ii) is now finite (mainly positive / mainly negative view of China,
  scheme PDF5). OL Text 3 A(ii) three reasons recorded open. HL Text 2 B keeps
  the printed “identity”. Poster order and the virtue pool are unchanged.
- New reviewed source exclusion (`kind: not-required`, see ENGLISH.md): OL Text 1
  A(iii)(b) and Text 3 A(iii)(a) are self-contained and carry no reader. OL Text 2
  A(i) reads De Brún only (PDF4); Text 2 A(iii)(a) keeps PDF4–5 because the
  prompt says “based on what you have read above”.
- 2016 criteria: C/L cannot exceed P at both levels (OL unlike 2015); historical
  grids HL PDF40 (A+–E-) and OL PDF52 (A–F/NG, 10-mark bands overlap, F/NG 1).
- Ledgers now: visual **438/888 pages, 31 sweeps, 30 full paper gates**; 1,126
  task reviews; 2,227 choice decisions (232 finite); raw 3,393 classified.
  Gate report: routes 3,811; pending taskSelections 10 / rawDirectives 1,198 /
  rawLinkedTasks 0 / schemeTasks 1,598 / paperReviews 40, none from 2016 P1.
  Strict gate still refuses on other years. Python 40 tests, TS 132 tests,
  typecheck and diff check pass.
- NEXT: 2016 Paper 2 (both levels), then 2017 and 2019–2026.

---

## Earlier checkpoint — 2010–2015 and 2018 reviews complete

This checkpoint supersedes ALL older counts and unresolved lists below. The goal
remains ACTIVE and unbounded. Work only in this isolated English worktree. No
commits, merges, deployment or external messages; no completeness claim yet.

- Inventory: 68 papers / 888 pages; 2,195 outer candidates / 2,724 marked leaf
  tasks. Fresh extraction matches all saved candidates field-for-field; latest
  2015 extraction merged into `fresh-candidates.json` (record ordering differs).
- Visual ledger: **418/888 pages**, **29 full sweeps**, **28 full paper gates**.
  All four papers in 2010–2015 and 2018 are fully reviewed. The earlier 2026 OL P2
  visual sweep still needs independent tally, full scheme and raw reviews.
- **1,085 task/scheme reviews**, 1,639 pending. **2,215 choice decisions**, 231
  finite tasks. The strengthened selection scanner currently resolves **3,809
  routes with 11 task selections pending**. Do not quote 3,809 as a final count.
  Before the scanner change, 3,818 routes; the newly found 2015 HL character
  choice adds two, while 11 newly flagged unreviewed tasks are withheld.
- Raw scan now **4,591 hits / 3,356 classified / 1,235 pending**. Number-of
  matching now covers one–ten, numerals and non-breaking whitespace. It found
  `two of the above characters` in 2015 HL P2. 416 new exact page-number footers
  were matched to physical page/document length and classified; other new hits
  in completed papers were individually reviewed. No linked-raw-task gaps.
  Publication gate remains closed. No baselines updated.
- 2014 counts: HL P1 19/20, OL P1 22/26, HL P2 23/23, OL P2 90/117.
  Full sources verified: The Peninsula/Heaney6; Coming Home/Sheers11;
  The Underground12, Poems for Breakfast14, Child16, The Collar18.
  Heaney A2iii keeps Underground plus A Constable Calls (2012 PDF12) and A Call
  (2024 PDF16). Plath C2iii source finding is resolved as described below.
- 2015 counts: HL P1 **19/25**, OL P1 **22/25**, HL P2 **23/25**, OL P2 **92/128**.
  HL P1 six genres and past/future traveller; OL Lizzie/Michael, podcast/radio
  diary and cover preferences. Required covers/passages remain together.
  OL Text2 Aiii(b) uses paragraph1 PDF4; Text3 cover-only Aiii(a) PDF7.
  Paper1 sources: Bono2–3, Briscoe4–5, Lively6–7; Doyle2–3, Beacom4–5,
  Tatty6–7. Wacker’s B retains optional passage context for the named pet shop.
- 2015 HL Never Let Me Go(ii) requires EXACTLY two of Kathy/Ruth/Tommy, unlike
  2014 at-least-two: mechanically expands three60-mark pairs. Peter Street/
  Peter Sirr is complete on PDF6, six tercets plus Whitefriar Street footnote.
  Poetry headings separated from question text without changing canonical IDs.
- 2015 OL P2: nine three-statement Single Text pools add18 routes; six comparative
  15-mark choices add8; three10-mark poetry descriptor pools add6 and two20-mark
  poetry pools add4, giving128. Four40-mark comparative responses remain open
  comparisons with full parent context, not forced to the earlier attribute.
  Flexible one-or-more and happy/sad/both stay together. Two Sean Walsh diaries
  remain one30 award. Today/McKechnie11; The Locket/Montague12;
  Revelation/Lochhead14; Ghost Estate/Wall16; The Bend in the Road18. All complete.
  Paper `memory` retained over scheme `memories`; `social class` retained over
  scheme33 missing `class`; Othello paper `play` retained over scheme28 `novel`.
- Plath companion reader: new `kind: linked-reading`, attributed publisher links
  to Poppies in July (CCEA2016 anthology PDF54/printed52) and The Arrival of the
  Bee Box (SEC2003 OL P2 PDF12). Both visually verified, exact hashes/provenance
  in source ledger. Links explicitly open a new tab; no copied protected text
  or attempted cross-origin embedding. Reader supports empty pages plus
  `readings`; extractor validates HTTPS SEC/CCEA origins and required metadata.
  Existing supplementary-text Yeats and cross-paper Hopkins readers remain.
- Reader browser QA passed1440x1000 and390x844, light/dark, linked and stanza
  readers, focus trap/Escape/return, navigation and zoom, no overflow or JS errors.
  New linked reader test was fixed with explicit JSX space in its accessible
  label. Latest validation:132 TS tests,36 Python tests, typecheck and diffcheck
  all pass after2015 review and scanner repair. No required checks running.
- Runtime still650legacy2021–2025 cards (660census including10aliases); full
  publisher NOT implemented. Atlas97topics/771coarse mappings still requires
  additive canonical atomic bridges. Preserve every ID, alias and n. Parent
  legacy bundles need aggregation of additionalSourceMaterials. The full
  publisher MUST invoke `english_review_gate.check(strict=True)`.
- Historical marking rules/grids still need runtime implementation. 2015OL
  PDF3 caps L only when BOTH P and C fail D, M independent; exact grid PDF47
  (10-mark F/NG prints1, not0). Do not impose modern C/L<=P on older years.
- Known later fix:2020 OL Q2 depends on Q1 context. Older OL continuation fixes
  are coded but sidecars not regenerated. Preserve four verified legacy crops.
- NEXT:2016 HL/OL Paper1 (renders prepared), then2016/2017 and2019–2026 full
  audits, remaining11 newly flagged task decisions, publisher/Atlas parity and
  integrated reader QA. Do not rerun `record-2014-ol-p2-review.py`: it predates
  the resolved Plath finding and would reintroduce it. Latest recording scripts
  are2015P1,2015HL P2,2015OL P2 andrecord-number-of-scan-review in ignoredtmp.

---

## Current checkpoint — 2010–2013 and 2018 reviews complete

This checkpoint supersedes ALL older counts and unresolved lists below. Goal remains
ACTIVE and unbounded. Work only in this isolated English completion worktree.
No commits, merges, deployment or external messages. Do not mark complete yet.

- 68 papers / 888 pages; 2,195 outer candidates / 2,724 marked leaf tasks.
  Full fresh extraction passed and matched every field. After new 2012 source
  reviews, a fresh 2012 extraction also matched; `fresh-candidates.json` and
  `all-candidates.json` now contain equal records (ordering differs).
- Visual ledger: **320 / 888 pages**, **21 full sweeps**, **20 full paper gates**.
  All four papers of 2010, 2011, 2012, 2013, 2018 are fully reviewed. 2026 OL P2 has only its earlier visual sweep,
  still needs independent tally and full scheme/raw reviews.
- **775 task/scheme reviews**, 1,949 pending. **2,122 choice decisions**, 232
  finite tasks, **3,820 routes**. Raw scan: 4,104 hits / 2,691 classified /
  **1,413 pending**. No task-selection or linked-raw-task gaps. Strict full
  corpus publication gate remains deliberately closed; no baselines updated.
- 2011 verified task/route counts: HL P1 **19/20**, OL P1 **19/21**,
  HL P2 **23/23**, OL P2 **91/111**. OL P1 QAiii(a/b) is ONE combined20
  per text. OL P2 has five women in Plough/Stars (scheme21), three seasons
  other than spring, four three-phrase pools, place/sister/relationship pools.
  F3iii support/oppose stays two routes because scheme20 requires a final side.
- 2012 verified counts: HL P1 **19/24**, OL P1 **22/35**, HL P2 **23/23**, OL P2 **90/113**.
  HL image choose2of3 gives3, A/B gives2, outings support/oppose2 and feature
  newspaper/magazine2. OL Google choose3of5 printed words gives10; diary topic
  routes sport/fear/play/musical/debate gives5. Three diaries retain one50 award.
  OL QAiii a/b now separate10 awards (unlike2011). Google logo name lost by
  text extraction was repaired in reader title; all relevant images retained.
- 2012 source pages: HL Personal Memories/Margaret Laurence2–3 (including B),
  Shared Memories/Mary Robinson4–5, Ghost Train/Paul Theroux6–7. OL Beacom/BOD
  2–3, McAleese4–5, Rigby/Google6–7; image-only parts use their specific page.
  OL McAleese B gets the source because scheme7 expects supporting reference.
  HL unseen The Beautiful Lie/Sheenagh Pugh is PDF6; all5stanzas verified.
  Prescribed poet headings removed from actual prompts via promptHeading,
  retaining canonical stem. Hamlet(ii)'s missing closing quote is in original.
- 2012 OL P2 readers corrected: Shoulders/Naomi Shihab Nye11; A Constable
  Calls/Heaney12; The Sun/Oliver14; A Summer Morning/Wilbur16; Mirror in
  February/Kinsella18. Full poem pages only. Sun1(c) quoted lines verified intact.
  Nine finite pools now retain exact printed statements/openings with stable IDs.
  ComparativeA2(b) stays open: scheme32 permits enjoying both characters equally.
  All90 tasks scheme-bound;53 additional raw occurrences classified. Independent
  route tally:90+23=113, including5openingpairs,4three-statement pools,Hamlet/
  Polonius,4three-collection pools and2Kinsella attitudes.
- **2010 Yeats reader exception is resolved**. Two verified public-domain
  reading editions (Innisfree1908 / Airman1919) replace the incorrect Wild Swans
  source. `supplementary-text` supports stanza-preserving poem slides, edition
  links, a clear not-in-exam notice, zoom, next/previous, dots and Escape close.
  Source ledger includes exact edition provenance; source URLs/content hashes
  validated from downloaded primary editions. Task now scheme-reviewed.
- **2011 Hopkins Spring + Inversnaid is resolved**. 2011 scheme36 requires both;
  Spring remains2011PDF16, additional Inversnaid reader uses visually verified
  2021OLP2PDF20. `sourceYear` and `sourceFileid` select the correct Paper Trail
  PDF. `source_from_attachment` verifies sourcePaperId/sourceSha256/page range.
  Additional source materials pass through factory and bind task fingerprints.
  Current extractor adds companions to leaf tasks; bundled legacy parents still
  need companion aggregation when implementing the final runtime publisher.
- SourceMaterialReader also fixes focus lost when the last-arrow button becomes
  disabled. Escape listener captures/stops propagation; focus moves to current
  dot. Browser passed1440x1000 desktop and390x844 phone in light/dark, navigation,
  zoom, close/reopen, focus return, no horizontal overflow or JS errors.
- Historical grading needs exact year support BEFORE full runtime publication.
  2011/2012 OL scheme3 caps Language at top of D only if BOTH P and C fail D;
  Mechanics independent. Exact old grids (2011PDF38,2012PDF44) differ from modern
  H/O bands and modern C/L<=P. Notes pinned in ledger and ENGLISH.md. Reconcile
  older2010/2013/2018 grading rules too; don't universally apply modern factory.
- Validation: **131 TS tests + typecheck + diff check passed** after reader and
  additional-source changes. Latest **29 Python audit tests passed** after2012;
  all finite route counts/IDs/tariffs, image word combinations and inherited
  source/context regressions pinned. Full gate report still intentionally pending.
- Vite session88410 remains on5198. All2012 renders, tests, gate and extraction
  finished. Gate pending: raw1413, scheme1949, paperReviews50;0 taskSelections
  and0 rawLinkedTasks. Reader browser script: `node tmp/english-audit/reader-browser.mjs`.
  CUA unavailable (`CUA_REPL_ENABLED_SURFACES` missing); installed Playwright used.
- NEXT: **2014 HL/OL Paper1**, renders prepared in review directories. Then2014
  P2 (known Heaney/Plath other-studied-poem readers need investigation). Remaining
  2014–2017,2019–2026 full paper/scheme/finite/raw audits. Future reviewed task
  changes must update source-bound fingerprints deliberately.
- Runtime still650old2021–2025 cards (660legacy census with10aliases), not full
  corpus. Atlas97topics/771coarse mappings still needs additive canonical atomic
  bridges. Preserve every legacy ID, alias and n. Sidecar continuation fixes for
  olderOL are coded but files not regenerated. Full publisher must invoke strict
  `english_review_gate.check`. Finish runtime/Atlas parity and integrated reader
  desktop/mobile QA before any completeness claim.

---

## Current checkpoint — 2010 / 2018 audits completed, source exception remains

This checkpoint supersedes older counts and unresolved lists below. The goal is
ACTIVE and unbounded. Continue in this isolated worktree only. No commits,
merges, deployment, or external messages have occurred.

- All four 2013 and all four 2018 papers have complete visual, independent
  tally, task/scheme and raw-selection reviews. All four 2010 papers have now
  been visually swept and their scheme boundaries checked. 2010 OL Paper 2 has
  one unresolved reader finding, explicitly blocking publication. 2026 OL P2
  has an older full visual sweep but still needs its independent tally and full
  scheme/raw review. Total: **227 / 888 pages**, **13 full visual sweeps**.
- Candidate corpus remains 68 papers, 2,195 outer records and 2,724 marked leaf
  tasks. The choices ledger has **2,003 decisions / 230 finite tasks** and now
  expands to **3,814 routes**. This is still a candidate count, not completeness
  evidence. Raw scan: 4,104 hits, **2,469 classified / 1,635 remaining**; all raw
  occurrences in 2010, 2013 and 2018 reviewed papers are classified. 2010 P2 OL
  shared section directions link all affected comparative tasks.
- `english-task-review.json` now binds **468** task/context/source fingerprints
  to paper/scheme hashes, scheme pages and exact criteria. The remaining 2,256
  tasks include the 2010 OL Yeats reader exception. `english_task_review.py`
  rejects stale evidence, wrong tariffs, or invented holistic submarks.
- `english_review_gate.py` combines choices, independent raw scan, task/scheme
  evidence, every-page visual sweeps and independent task/route tallies. It now
  also refuses publication while any visual-ledger `openFindings` remain.
  The eventual runtime publisher MUST invoke its strict gate.
- `english-task-context.json` and `apply_reviewed_context` preserve source-bound
  instructions outside numbered tasks. Currently nine 2010 OL comparative
  parts retain the shared requirement to name texts and character/theme.
  Context records bind the task wording and paper hash; orphaned records fail.
- New 2010 verified counts: HL P1 19 / 20; OL P1 19 / 29; HL P2 23 / 23;
  OL P2 89 / 115. OL P2 now expands the closed five-Mundy-sisters group
  (enumerated in scheme PDF13), the five printed Wild Swans stanzas, and the
  inherited five exclusion choices in the following image question. These add
  12 routes. Stanza/character evidence and tariff regressions are pinned.
- 2018 counts: HL P1 19 / 20; OL P1 22 / 24; HL P2 23 / 23; OL P2 92 / 104.
  HL composing7 “Language is a great weapon” is OPEN: paper permits free
  agreement/disagreement and scheme PDF20 allows reflective/discursive writing.
  The previous artificial binary expansion was removed deliberately.
- 2013 counts: HL P1 19 / 21; OL P1 22 / 32; HL P2 23 / 23; OL P2 90 / 107.
  All scheme grids and finite selection details are bound to exact tasks.
- 2010 HL unseen **Seed — Paula Meehan**, p6: its reader presentation note
  preserves the original image and explains the scheme PDF31 correction of
  “useless” to “useful”; both readings are accepted. `reviewed_source` supports
  verified presentation-note overrides. 2010 OL unseen **Nettles — Vernon
  Scannell**, p10, includes the illustration and glossary.
- 2010 source pages visually verified: HL/OL P1 Text1 pp2–3, Text2 pp4–5;
  HL Text3 prose pp6–7 and cover-only comparison p7; OL Text3 four-image set p6.
  OL poems A11/B13/C15/D16. 2018 HL illustrated Dead Man’s Dump is p6 only;
  2018 OL Text3 interview/poster pp6–7. 2013/2018 other verified readers remain.
- Current unresolved reader: `english-2010-ol-p2-prescribed-d-q2-iii` concerns
  **The Lake Isle of Innisfree** and **An Irish Airman Foresees his Death**, not
  Wild Swans. The scheme PDF35–36 allows one or both to be discussed. The task
  remains absent from task-review and has an explicit blocking openFinding.
  Exact crosswalk locates Innisfree in 2022 OL P2 p15 (needs visual source check).
  No Airman title found in prescribed crosswalk. Plan correct source handling;
  do not claim the parent paper supplies these poems. 2014 Heaney/Plath other-
  studied-poem choices need the same review later.
- Extractor repairs now verified: 2016 OL B Q1(a)(i) and 2017 OL B Q2(a)(i)
  retain shared stems and roman IDs; 2022 HL Dickinson damaged name repaired;
  2021 OL final poetry footer removed; 2010 OL P1 Question B heading full stop
  no longer leaks into prompt; standalone `(continued)` / `C (continued)` /
  `F (continued)` headings removed. 2010 HL poet headings explicitly recorded
  as `promptHeading` and removed from prompt while canonical stem stays intact.
- 2020 HL Text1 B Rentals for Writers cartoon on p3 visually verified. 2021 OL
  Jungian Cows / Inversnaid exact source pages corrected to19/20. Four additive
  legacy scheme-crop repairs retain original n/region (2013/2016/2018/2021).
- 24 Python audit tests passed after the new 2010 routes and open-finding gate.
  Last full gate before OL P2 additions: 3,802 routes, 1,694 raw pending,
  2,344 scheme tasks pending, 59 paper-review flags. Refresh gate after latest
  extraction. Full extraction rerun is currently in exec session **75913**;
  output is `tmp/english-audit/fresh-candidates.json`, NOT authoritative yet.
  Compare task fields to all-candidates, inspect any unexpected changes, then
  replace all-candidates. The previous fresh extraction had zero differences.

Next steps: finish current fresh extraction and strict report; resolve the Yeats
reader exception; continue full visual/scheme/raw audits for the remaining
papers. Then generate runtime/Atlas atomic entries while preserving all650 old
IDs and10 aliases, verify exact parity and source-reader desktop/mobile UX.
Runtime remains the old650 cards plus verified35-mark corrections. Atlas still
needs additive canonical topic and atomic n bridges. Do not update baselines
until all independent gates and preservation checks pass.

# English completion — active work, 7 October 2026

## Objective and worktree

Complete EVERY English question and finite answer route from Paper Trail in
Mark Bank and Topic Atlas, under the correct topic, with readable source texts,
poems and images that can be opened and closed during practice. This is not
complete, merged or published.

Worktree: `/Users/alexlinehan/Documents/Nextstepuni-English-Completion-20261007`
Branch: `codex/english-corpus-completion-20261007`
Base: `8deb273f` from the current Launch worktree.

Do not use `/Users/alexlinehan/Documents/Nextstepuni-English` for this work. It
is an older, dirty `markbank/irish` worktree with other subject work. The active
completion worktree has ignored symlinks to Launch's `node_modules` and
`paper-trail-corpus`; the latter contains all required PDFs.

Read this repo's AGENTS.md and the October 5/6 design decisions before work.
No delegation is authorized. Do not reduce the scope to the old 2021–2025 deck.

## Authoritative scope

`PAPER_TRAIL_INDEX.english` has 68 papers: 2010–2026, both levels, both papers.
There are 34 combined marking schemes. All 102 PDFs exist locally.

`scripts/markbank/authoring/english_complete.py` builds the committed
`scripts/markbank/authored/english-paper-inventory.json` directly from that
index, hashing the PDFs and recording current Mark Bank and sidecar counts.
It is explicitly an inventory, not a completeness certificate.

The runtime still has 650 cards, all from 2021–2025 (210 HL, 440 OL). The
legacy census has 660 entries, ten of which alias source-independent repeated
prompts. Preserve all 650 existing card IDs and the aliases. The inventory
test pins all 68 documents, independently of the candidate parser.

## Changes already made

- Corrected all 72 Ordinary Single Text cards from 2021–2022: 35 marks, not
  30. Q1 is 10+10+15. Q2–4 use the SEC's discrete P/C/L/M = 11/11/11/2.
  Corrected the legacy census generator, regenerated census and authored JSON,
  and supported the explicit 35-mark allocation in the runtime factory.
  Source evidence: both official OL schemes PDF p.19 state each question is
  35; pp.20–22 show the part tariffs and discrete allocation. Both first work
  paper pages and representative scheme pages were rendered and inspected.
- Removed the unsupported English "Every selectable response is included"
  product copy. Kept the compact menu's existing empty-topic filtering as a
  separate display choice. Irish behavior is unchanged.
- Repaired Paper Trail's structural header reader for `A.`/`B.` headings.
- Updated `english_p2_ol.py` to find the 2026 combined scheme (LP100 rather
  than LP000). Created `answers/2026/LC002GLP200EV.pdf.json` with 19 block
  anchors. These are BLOCKS, not atomic task counts. All 20 paper pages were
  visually inspected. Each of the 68 extracted outer tasks was checked for
  multiword matches inside its own block's scheme crop. This sidecar still
  needs finer task anchors, topic integration, index availability and runtime
  delivery as part of the full task.
- Fixed an existing OL Paper 2 collector truncation: the final poem's questions
  can continue beyond its heading page (2010, 2012, 2014, 2015). The generator
  now retains continuation pages. Older committed sidecars have NOT yet been
  regenerated; review them before writing corrected paper regions.
- Added `english_full_cards.py`, an extraction/review-candidate tool, which
  successfully visits all 68 papers and produces 2,195 outer candidates.
  It does NOT write cards to runtime or claim completion.
- Restored damaged 2011 OL poetry question text with source-hashed, visually
  transcribed page repairs in `english-paper-text-repairs.json`. Pages 10, 11,
  13, 15 and 16 were inspected. The actual poems/images stay in the PDF reader.
  That unseen section has THREE questions, choose any TWO. Never reduce it
  to the later two-question layout.

## Current commands and evidence

```
python3 scripts/markbank/authoring/english_complete.py --check
python3 -u scripts/markbank/authoring/english_full_cards.py
npm test -- test/markBankEnglish.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts
npm test -- test/englishCorpusInventory.test.ts
python3 scripts/paper-trail/english_p2_ol.py --check
```

The four required/English test files passed: 126 tests. The inventory test
passed: 2 tests. All 17 OL sidecar checks passed after the latest repairs; all
17 HL checks passed after the heading fix. `git diff --check` passed.

The English coverage content-hash test currently FAILS, as expected after the
verified tariff correction: baseline `45a6d15c88c98b41`, actual
`a70a862b4a959305`. The other two English coverage checks pass. Do not simply
refresh this baseline now: AGENTS.md requires the full paper/scheme sweep,
old-ID preservation and zero-open/zero-orphan reconciliation first.

Candidate output and evidence are under `tmp/english-audit/` (do not commit
the render/candidate scratch directory). `all-candidates.json` is reproducible
from the script and local corpus. `extraction.log` ends with 2,195 candidates,
zero failed papers. The intermediate older per-paper outputs may be stale;
regenerate before relying on them. All tool processes should be revalidated
by handle if a later turn finds one recorded as running.

## Next work — keep the full scope

1. Review and split the 370 currently flagged bundled boundaries at the
   scheme's independently practicable tariffs. Keep old parent IDs; add
   standalone tasks with all required shared context. Historical HL
   Comparative Q1/Q2 structures vary, so do not assume Q1 is always the split
   question. Ordinary Single Text before 2021 has Q1/Q2 plus Q3 alternatives;
   2021+ has four questions with a choose-two instruction.
2. Classify every finite choice, including inside the newly split tasks.
   Current outer candidates flag 425 prompts for selection review; that is
   not an independent or final denominator. Scan raw paper instructions too,
   including section-level closed pools. Derive n-choose-k routes mechanically,
   preserve route tariffs, pin wording and IDs, and fail on unclassified or
   stale directives. Explicit open/flexible-choice decisions need written
   reasons. Do not confuse open evaluation with a finite printed answer pool.
3. Replace heuristic/fallback candidate topic assignments with reviewed exact
   identities. Currently 278 work candidates fall back to `english-6-0`, 56
   poetry candidates to `english-8-1`, and 2 to `english-8-0`. Many historical
   works/poets are absent from the canonical catalogue, and Atlas lacks many
   archive topics, especially OL. Extend the canonical registry and exam-topic
   bridge, preserving IDs. Do not trust `closest_topic` fuzzy matching as
   evidence of the right text or poet.
4. Verify every source attachment. All P1 QA candidates currently include
   their source as a conservative candidate default; distinguish truly
   source-dependent tasks from source-independent ones. Some B and composing
   questions DO need sources: e.g. 2016 OL Text 2 B needs the 1916 diary;
   2020 HL composition 5 needs the three figures on the magazine cover on p.7.
   The old test claiming ALL B/compositions are source-independent is invalid
   for the expanded corpus. Resolve poem titles/bylines from the actual pages,
   not the temporary candidate labels, and prevent adjacent blank/question
   pages from entering source ranges.
5. Sweep every paper visually and cross-check every proposed task/route with
   its scheme. Only 2026 OL Paper 2 has had a full-paper visual sweep in this
   work. 2010 OL p.2, 2010 HL P1 p.3 and the specific 2011/2021/2022 pages
   listed above were also inspected; do not mark other papers reviewed.
6. Add every final task/route to Mark Bank AND Topic Atlas. Current Atlas uses
   numeric `n` sidecar identities, via `data/examTopics/registry.ts` and
   `components/PaperTrail/topics.ts`; preserve existing n values and add new
   numeric ones, with explicit source/scheme crops and correct topic IDs.
   `english-question-runtime.json` currently has only coarse associations.
   Keep every existing identity and practice history intact.
7. Verify browser behavior, including source open/close/page/zoom and return
   to the same task on desktop/mobile, using the approved brand treatment.
8. Reconcile the real full-corpus denominator, run required checks, deliberately
   update baselines only after their gates pass, and deliver the integrated
   result. Do not claim the goal complete on the strength of parser counts.

The goal remains ACTIVE. No blocking condition currently exists.
## Latest checkpoint — continued audit

This section supersedes stale candidate counts and identity/selection TODOs above.

- All 68 papers extract successfully: 2,195 outer candidates and 2,724 proposed
  marked leaf tasks. `extract_record(record)` in `english_full_cards.py` performs
  each paper atomically and scopes every leaf scheme match to its own sidecar
  block, preventing identical poetry questions from matching a different poem.
- Four visually verified bad legacy scheme crops were repaired additively with
  `schemeRegion`, preserving old `region` and numeric `n`: 2013 OL Comparative A
  starts PDF p.31; 2016 OL Ozymandias p.48; 2018 OL Child of Our Time p.48;
  2021 OL 1984 p.38. Manual starts are recorded in `english_p2_ol.py` where the
  structural detector misses a centred heading. Other sidecars still need review.
- `curriculum.ts` has 38 additive historical work/poet nodes. Exact source-hashed
  mappings for all 392 Single Text/prescribed blocks live in
  `english-exam-identities.json`; no fuzzy/fallback topic matches remain in
  candidates. Atlas archive topics and bridges have NOT been updated yet.
- `english_choices.py` mechanically expands reviewed fixed pools. There are
  currently 1,899 task-level decisions, including 228 finite tasks, producing
  3,803 resolved candidate routes with ZERO unreviewed flagged candidate tasks.
  This is NOT the independent full-corpus denominator. Decisions bind exact
  question hashes; stale/orphaned decisions fail. The raw-paper gate is separate.
- Single Text choices include all reviewed 2010–2026 explicit named pools,
  prescribed openings, 2018 character pairs and 2025 one-to-five star ratings.
  Reasoned literary agreement/disagreement remains open unless a formal position
  or prescribed opening is demanded. Phrase OR phrases / word OR words / at least
  / illustrative lists remain flexible with explicit reasons.
- Prescribed choices include historical word/phrase/poem pools, 2016 openings,
  the 2020 niece/nephew dialogue, 2021 dramatic-scene/short-film directions, and
  the three explicitly listed tone options in 2024 and 2026. 2026 unseen asks
  which ONE of sad/hopeful is best; both can be discussed, so the two routes
  retain that permission. Some decisions still need visual/scheme confirmation.
- 2013 OL Comparative B has three Tension/Climax/Resolution routes in every
  marked part, including dependent follow-up parts. 2014 OL Comparative B Q1(a)
  has two prescribed openings. 2015 OL Comparative A Q2(a) has social-class/
  conflict choices; B Q1(a) shocked/impressed and B Q2(a) clever/cruel/brave.
  2015 part (b) comparisons remain open with parent context: they do not require
  those attributes as the comparison focus (explicit reasons recorded).
- `english_raw_selection.py` scans native text from EVERY PDF page independently
  of the card crop parser, plus reviewed repairs for damaged 2011 text. It found
  4,104 directive occurrences. `english-raw-selection-review.json` currently
  binds 1,326 exact full-line occurrences to reviewed task IDs, source hashes,
  line/context hashes and linked question hashes. Latest raw report: 2,778
  unclassified, zero pending linked tasks. It has NOT been refreshed after the
  later poetry/comparative decisions. Further exact matches can be added, but
  prose and examination instructions still require explicit classification.
  Unknown/stale/orphaned raw entries fail strict generation. `--report` reports
  them without publishing. The eventual runtime publisher must invoke this gate.
- Visual ledger `english-visual-review.json` is authoritative: 111 of 888 paper
  pages inspected; full-paper sweeps completed for 2013 OL P2, 2018 OL P2 and
  2026 OL P2 ONLY. 2013 has independent visual tally 90 marked tasks / 107 routes;
  2018 has 92 / 104. Full scheme gates remain false. Scheme pages inspected in
  this continuation: 2013 OL 31–33, 2016 OL 48–50, 2018 OL 47–50, 2021 OL 38–41.
- Verified reader pages for every 2013/2018 OL prescribed poem are now stored as
  `sourcePages` on exact identities; they exclude question-only continuations
  and the next poem's page. Unseen reader titles/bylines were bound for Earbud
  (Bill Holm, 2013 OL PDF p.10, includes earbud photo) and Walking to Dublin
  (Richard Peabody, 2018 OL p.13). Other source ranges still require review.
  `english-source-review.json` now has 28 extra per-task attachments (previous 24
  writing sources plus those four unseen task attachments).
- Candidate references now use actual Paper/Text/Question labels rather than
  generated suffix labels. Parent question context and local notes are retained
  in leaf candidates; final runtime/UI delivery of that context is unfinished.
- Python audit regressions: 12 passed (choices, raw gate, two visually swept
  papers with pinned independent counts and source ranges). Run with
  `python3 -m unittest discover -s scripts/markbank/authoring -p 'test_english*py' -v`.
  Re-run after any later changes. Required TS preservation/registry/deck tests
  previously passed 111 after the canonical additions. Coverage baseline still
  deliberately unchanged and fails the known tariff-content hash.

### Specific unresolved issues discovered during review

1. 2016 OL Comparative B Q1(a)(i) and 2017 OL Comparative B Q2(a)(i) currently
   have candidate suffix `-a`, with `(i)` retained inside question text because
   a shared stem sits between markers. Inspect paper/scheme and repair the
   boundary/reference logic without splitting unmarked inner lists. Changing
   these IDs/wording requires deliberate selection/raw-ledger reconciliation.
2. Candidate `english-2022-hl-p2-prescribed-4` contains damaged extraction
   `Emi D ly ickinson`; visually verify and repair. Some earlier HL prompts retain
   the poet heading in questionText; clean it after source review.
3. `english-2021-ol-p2-prescribed-e-q2-iii` has footer
   `Ordinary Level – Paper 2` in questionText. Strip only actual footer material,
   visually verify, then deliberately update affected wording hashes.
4. Split tasks can depend on earlier outer questions, e.g. 2020 OL Single Text
   Q2 depends on Q1's relationship. ParentQuestionText only covers its own outer
   question, so explicit cross-parent context is still needed.
5. Choices asking about OTHER studied poems (2010 Yeats pair, 2014 Heaney/Plath
   triples) must not misleadingly attach only the current printed poem to every
   route. Review appropriate source handling, potentially a source reference to
   another official paper where that selected poem is printed. Do not invent
   poem text or imply the original paper supplies every studied poem.
6. 2020 HL Text 1 B Rentals for Writers cartoon is currently attached to p.3
   from an unverified page assumption; visually check it. Other 24 writing-source
   pages are text-informed but not all visually checked.
7. Raw source directives outside extracted task matches remain unclassified.
   Standalone OR, outer choose-two instructions, copyright/prose and poem
   wording need classification with reasons; do not treat renderer/parser
   success as review or blindly exempt every unmatched line.
8. Runtime still only contains the preserved 650 old cards plus the verified
   35-mark correction; NONE of the full new corpus is published to Mark Bank or
   Atlas yet. Source reader desktop/mobile browser QA remains outstanding.

Scratch input scripts under ignored `tmp/english-audit/` serialize manually
reviewed decisions: `write-single-review.py`, `finish-single-review.py`,
`record-2013-2018-p2-review.py`, `write-poetry-review.py`,
`write-comparative-review.py`, earlier QA/B/composing scripts. Do NOT rerun the
initial single helper blindly: the later helper corrects its two guessed labels
and removes optional 2012 talk agree/disagree expansions. Production evidence is
in the source-hashed JSON ledgers, not the scratch helpers.

The full user goal remains ACTIVE with no blocker. Nothing has been committed,
merged, deployed or externally messaged. Continue the remaining checks and
integration; do not stop at extraction/selection counts.
