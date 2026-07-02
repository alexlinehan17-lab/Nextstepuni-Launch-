# Paper Trail — topic tags (Tier 2)

Per-question **topic tags** power two viewer features:
- **Frequency chips** — a chip on each question: *"Calculus — appeared in 5 of 5 tagged years"*, computed across the same subject/level/paper-slot.
- **Cross-year jump** — tap a chip → every sibling question tagged with that topic, across years and levels, one tap to open ("drill every Calculus question").

Tags attach to the **answer-map anchors** (question `n` is the join key), so the feature is available exactly on the papers that already carry verified per-question anchors. Tags are committed in-repo (small) — no Storage round-trip.

## Coverage

Grows wave by wave, one subject at a time. Each wave = one verified
`tags/<subject>.json`.

- **Wave 1 — Mathematics** (25 papers, 249 questions). HL/OL/Foundation, P1+P2, 2012–2025. Two independent adversarial verifiers, **0 disagreements**.

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
