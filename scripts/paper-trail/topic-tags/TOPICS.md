# Paper Trail — topic tags (Tier 2)

Per-question **topic tags** power two viewer features:
- **Frequency chips** — a chip on each question: *"Calculus — appeared in 5 of 5 tagged years"*, computed across the same subject/level/paper-slot.
- **Cross-year jump** — tap a chip → every sibling question tagged with that topic, across years and levels, one tap to open ("drill every Calculus question").

Tags attach to the **answer-map anchors** (question `n` is the join key), so the feature is available exactly on the papers that already carry verified per-question anchors. Tags are committed in-repo (small) — no Storage round-trip.

## Coverage

**41 subjects, 786 papers, 8,884 questions** — every subject that has both
answer-map anchors and a fitting curriculum taxonomy. Each subject's anchored
questions are 100% covered (reconstruction is diffed against the extracted stems
and gaps re-run until zero; two honest nulls: the 2023/2024 Classical Studies
HL Q12 cross-strand open essays).

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

- **Anchored, but taxonomy not exam-task-shaped yet** (149 papers): italian,
  japanese, russian, mandarin-chinese, latin, ancient-greek, lithuanian,
  polish, portuguese — need the exam-task taxonomy treatment french/german/
  spanish received.
- **Anchored, but no curriculum.ts entry** (~407 papers): 16 non-curricular
  EU/heritage languages, all 20 LCA subjects, 9 further JC subjects,
  agricultural-economics, history-early-modern.
- **DCG** has a taxonomy but no anchored papers yet.
- Papers with no answer-map anchors at all cannot be tagged until they get
  paper-side anchors (the sidecar pipeline).

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
