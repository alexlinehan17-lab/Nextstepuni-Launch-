# Paper Trail — topic tags (Tier 2)

Per-question **topic tags** power two viewer features:
- **Frequency chips** — a chip on each question: *"Calculus — appeared in 5 of 5 tagged years"*, computed across the same subject/level/paper-slot.
- **Cross-year jump** — tap a chip → every sibling question tagged with that topic, across years and levels, one tap to open ("drill every Calculus question").

Tags attach to the **answer-map anchors** (question `n` is the join key), so the feature is available exactly on the papers that already carry verified per-question anchors. Tags are committed in-repo (small) — no Storage round-trip.

## Coverage

**98 subjects, 2,258 papers, 22,695 questions built in** (`build-tags.mjs`
output is the source of truth for this line) — every paper that has a
question anchor (an answer-map sidecar OR a hosted paper-anchor, see Waves
8-9) and a fitting curriculum taxonomy is topic-tagged. Anchored questions
are 100% covered per subject (a handful of honest nulls: the 2023/2024
Classical Studies HL Q12 cross-strand open essays).

Two coverage frontiers remain, both explicit (see "Not tagged yet"): the
**section-restart class** (papers whose question numbering restarts per
section — English P2, Irish, History essay papers, the continental
languages' section-numbered papers — which the contiguity-gated anchor
generator correctly refuses until it is section-aware), and papers with no
anchor of any kind.

- **Wave 1 — Mathematics** (25 papers, 249 q). Two verifiers, 0 disagreements.
- **Wave 2 — 14 subjects** (3,272 q): biology, geography, chemistry, physics,
  physics-and-chemistry, business, economics, accounting, agricultural-science,
  history, computer-science, applied-mathematics, construction-studies,
  physical-education.
- **Wave 3 — 8 subjects** (1,785 q): art, technology, engineering, and Junior
  Cycle science / mathematics / geography / business-studies / english.
- **Wave 4 — taxonomy alignment (2026-07-07)**: every subject's topic list
  verified against the Studyclix benchmark (73 harvested subject/level pages)
  with official syllabi/DES circulars as ground truth; 967 questions re-tagged
  onto finer exam-shaped ids (Biology organ systems, P&C Chemistry strand,
  Applied Maths old-course topics, Business unit ids, ...).
- **Wave 5 — coverage completion (2026-07-07)**: the Topic Vault made
  browse-by-topic the product, so the old "not tagged by design" exclusions
  were retired. 329 more papers / ~3,578 q: LC english (per-poet/per-text +
  task ids), irish, french, german, spanish, arabic, geography 2010-19,
  engineering 2010-20, business 2021-25 booklets, home-economics-s-and-s,
  link-modules, politics-and-society, classical-studies, music, religious-
  education, and JC history / irish / french / german / spanish / italian.
- **Wave 6 — TV-2 anchored languages (2026-07-07)**: the remaining 9 anchored
  languages got the exam-task taxonomy treatment (new task-view strands in
  `curriculum.ts`, excluded from the X-Ray in `syllabusMeta.ts`) and full
  verified tagging: italian, japanese, russian, mandarin-chinese, latin,
  ancient-greek, lithuanian, polish, portuguese — 149 papers / 1,585 q.
  Ground truth: the anchored papers' own structure (papers read from Storage
  per subject) plus the Studyclix benchmark where it exists (italian HL/OL,
  japanese). Independent verification: 6 subjects 0 errors; japanese 2
  corrections (2013 OL Q3, 2018 OL Q2); russian 21 corrections after the HL
  Q2 summary-writing sections were confirmed against the 2010/2014/2016/2018
  papers (EV/IV sidecar labels disagreed); italian re-verified via EV↔IV
  per-question consistency + per-year unseen/prescribed checks (2013 unseen
  confirmed against the paper; 2014 'Bianca come il latte' is the B1 unseen,
  not prescribed).
- **Wave 7 — TV-3 no-taxonomy subjects (2026-07-07)**: every anchored subject
  that had no `curriculum.ts` entry got a minimal honest, section/task-shaped
  taxonomy plus full tagging — 47 subjects / 409 papers / 3,438 q:
  - **20 LCA subjects** (189 papers / 1,614 q, DEIS priority): section-shaped
    strands mirroring each paper's printed sections (e.g. Active Leisure's six
    sections, Childcare's five, the MFL Listening / Reading+Written split);
    question-titled ids where the papers print them (Agriculture's six
    Section-Two modules, Engineering's Systems topics CAD/Electricity/
    Electronics/Mechanisms/Pneumatics, Graphics' Section-2 questions incl.
    Construction + Building Services, Technology's five titled questions);
    content-classified ids for Crafts & Design disciplines and Mathematical
    Applications themes.
  - **16 non-curricular EU languages** (144 papers / 869 q): shared honest
    shape — Part I Reading Comprehension (vocabulary-in-context vs
    comprehension/discussion of the set text) + Part II Written Production
    (anchored only in slovenian 2018/23/24 Q7 and danish 2018 Q7-Q8).
  - **9 JC subjects + jc-irish-t1 + agricultural-economics +
    history-early-modern** (76 papers / 955 q): task/section-shaped (Classics'
    four printed sections; RE / Jewish Studies content-themed strands; Irish
    T1 per-question task map; Ag-Econ Part 1 short questions; Early Modern
    DBQ).
  Ground truth: the anchored papers themselves — section headers and
  per-question stems read from Storage for every subject; sidecar crop regions
  used to resolve the graphics-and-construction 2016/2018/2023 anomalies
  (2023 Q3 is Building Services, 2018 Q4 is Woodcraft). Independent
  verification (3 passes: LCA, EU, JC/LC): 44 subjects 0 errors; corrections
  applied for lca-crafts-and-design 2014 Q8 (video terms, not photography) and
  swedish 2014 Q2 (synonym/vocabulary task), and — after the verifier showed
  JC RE / Jewish Studies exam sections are not thematically stable year to
  year — both subjects were re-tagged by question content against renamed
  thematic strands (38 + 10 tags, corroborated by a second independent pass;
  the one two-verifier disagreement, Jewish Studies 2022 Q11 Exodus, resolved
  to the liberation strand for cross-year consistency). jc-graphics has no
  anchored papers, so it remains untagged.
- **Waves 8-9 — the paper-anchor pipeline (2026-07-08)**: the vault stopped
  being bounded to answer-sidecar papers. Paper-side-only anchor files
  (`public/paper-anchors/`, PaperAnswerMap schema, mode:'pagejump', no scheme
  claim; see `PAPER-ANCHORS.md`) were generated for ~700 previously
  scheme-less papers under a contiguity gate (a numbering gap or a
  non-monotonic/rotated/cover-page anchor set → the paper is dropped, never a
  wrong crop), then tagged. This unlocked the modern eras of the highest-
  traffic subjects — mathematics (25→140 papers), physics (0→63), biology
  (20→89), chemistry, agricultural-science — plus DCG (496 q from anchors),
  the business/humanities corpus (accounting, art 119 papers, business,
  economics, geography, music, RE, ...), and the practical/STEM/language/JC/
  LCA sweep (construction, engineering, technology, physics-and-chemistry,
  spanish aural, latin, ancient-greek, mandarin, seven JC subjects, four LCA
  subjects). Every wave carried classify + rigorous per-question verify +
  an adversarial fresh re-classification; corrections applied at source
  (e.g. ag-science's 21 keyword-bias fixes, construction's 2 consistency
  fixes surfaced by the adversarial pass, geography's 29 body-text fixes).
  Trap classes the gates cannot see were caught by post-run render/textual
  QA and documented as SUBJECT_GRAMMAR CAUTIONs (marks-tables, answer-list
  fabricated numbers, back-cover grids, cover-instruction lists that satisfy
  the contiguity proof).

Every question is classified against the subject's `curriculum.ts` taxonomy and
re-checked by an independent adversarial verifier per chunk.

### Independent audit

A separate, read-only audit (fresh independent re-classification of a sampled
spread per subject, joined to the real stems) covered the original 23 subjects:
**120 formal samples, 100% agreement, 0 clear errors** — only a handful of
defensible two-topic/borderline calls. Wave 4/5 additions carried per-wave
independent verification passes (0-error verdicts recorded per subject in the
session transcripts). Accreditation-trustworthy.

### Not tagged yet (explicit, not silent)

- **The section-restart class** — papers whose printed question numbering
  restarts at 1 in each section (English P2 all years/levels + OL P1; Irish
  HL/OL P1/P2 and aurals; History essay papers; the continental languages'
  section-numbered reading/writing papers; pre-2020 combined
  business/economics/home-ec papers; PE's stray instruction-page references).
  The contiguity-gated anchor generator refuses these on purpose (restarting
  numbers are non-monotonic → a naive anchor would let one section's crop
  swallow the next). They need a **section-aware anchor generator** (detect
  section headers, anchor within each section's own numbering) — the next
  build-out. Enumerated per subject in the wave reports under
  `scripts/paper-trail/out/`.
- **Rotated/single-sheet formats** the vertical-band schema can't represent:
  DCG Section-A A3 quadrant sheets, geography map/photo inserts, art studio
  sheets, LCA practical/project sheets — correct wholesale refusals.
- **jc-graphics** has no anchored papers at all (rot-90 sheets only).
- A handful of genuine SEC misprints (dotless question headers, duplicate
  numbers) that break contiguity — dropped with the paper named in the report.

## The pipeline (verify-don't-guess, like the answer maps)

1. **Extract stems** — `node scripts/paper-trail/topic-tags/extract-stems.mjs <subjectId> [cycle]`.
   Reads the committed answer sidecars for that subject, downloads each paper,
   and pulls the opening text at every anchor → `out/<subject>-stems.json`.
2. **Classify** — split the stems across a few classifier agents. Each reads the
   stems + the subject's `curriculum.ts` subtopic taxonomy and assigns, per
   question, a `primary` (single best subtopic id) + optional `secondary`, a
   `confidence`, and an `evidence` phrase quoted from the stem. **Ground every
   tag in the actual question text — never guess.**
3. **Verify** — independent adversarial verifier agents re-classify from the
   stems and flag only genuine primary-tag errors (not defensible two-topic
   calls). Apply the corrections.
4. **Assemble** — group the verified tags by paper into a `PaperTopicTags[]` and
   write `tags/<subject>.json` (fields: subjectId, level, lang, year, fileid,
   paperKey `'p1'|'p2'|'single'`, `q[]` of `{n, primary, secondary?}`).
5. **Build** — `node scripts/paper-trail/topic-tags/build-tags.mjs` regenerates
   `data/paperTrail/topicTags.ts` (PAPER_TOPIC_TAGS + TOPIC_LABELS) from every
   wave file. Idempotent.

## Adding a subject

Drop a verified `tags/<subject>.json`, run `build-tags.mjs`, `npm run typecheck`.
The viewer lights the "Topics & frequency" tool automatically for any paper that
has both an answer map and a tag record. Frequency deepens as more years are
tagged — the chip is always honest ("N of M **tagged** years").

## Notes

- `paperKey` keeps P1 and P2 topic pools separate (Maths P1 ≈ algebra/calculus,
  P2 ≈ geometry/stats), so a frequency count never blurs the two papers.
- Irish-language (`iv`) papers that are exact translations are tagged identically
  to their English counterparts.
- `out/` is gitignored (regenerable); `tags/` is the committed source of truth.
