# Paper anchors — paper-side-only sidecars for the Topic Vault

**Problem.** The Topic Vault (`components/PaperTrail/VaultQuestionCard.tsx`) renders
question crops from answer-map sidecars: `paperRegionFor` derives each question's
paper-side extent from its own anchor (`pP`/`pY`) to the next question's anchor.
~2,000 index papers have **no** sidecar (marking scheme unmappable or not yet
attempted), so their questions can't be cropped or drilled by topic — even though
the paper side alone is enough for the crop. `mode:'crop'` is only needed for the
answer-reveal toggle (`canReveal` in the card); everything else works from anchors.

**Solution.** A **paper-side-only anchor artifact** in the existing
`PaperAnswerMap` schema (`types/paperTrail.ts`) that carries real per-question
paper anchors but claims **no scheme mapping**:

```jsonc
{
  "v": 1,
  "paperFileid": "LC562ALP039EV.pdf",
  "schemeFileid": "",          // ← no scheme claimed
  "component": "039",
  "band": [1, 1],              // ← empty band; nothing indexes into a scheme
  "copyright": "© State Examinations Commission",
  "paperOnly": 1,              // ← marker for tooling; ignored by the app
  "q": [
    { "n": "1", "label": "B-1", "pP": 2, "pY": [0.105, 1.0],
      "region": [{ "p": 1 }], "mode": "pagejump", "conf": 0.5 },
    ...
  ]
}
```

- `mode:'pagejump'` everywhere → `canReveal` is false → the card shows the real
  paper crop with the honest **"Open beside its marking scheme"** fallback
  button, exactly as it does today for degraded questions in verified sidecars.
- `region:[{p:1}]` is a schema-required placeholder; the vault never renders a
  pagejump region and the Viewer never loads these files (the `answers:1` index
  flag is not set).
- `conf: 0.5` sits deliberately below anchor-map's 0.6 "jump to the right scheme
  page" tier — these entries make **no** claim about where the answer lives.
- `n` is the **sequential question index in print order** (`"1"`, `"2"`, …) and
  `label` the printed number (`"B-1"`, `"C-4"`), matching the `types/paperTrail.ts`
  contract. **Topic-tag authors must reference the sequential `n`**, not the label
  (`siblingsFor` sorts with `Number(n)`; the card matches `map.q.find(x => x.n
  === sibling.n)`).

## Hosting — no Storage objects (task #94)

Storage uploads are credential-blocked, so the artifact is **committed to the
repo** at `public/paper-anchors/<year>/<paperFileid>.json` and deploys with the
app via Firebase Hosting on every push to `main`. Vite copies `public/` into
`dist/` verbatim; `<year>/<fileid>` is unique (fileids recur across years but
encode exam + subject code + level + component + language) and mirrors the
committed `scripts/paper-trail/answers/<year>/<fileid>.json` layout.

Size: sidecars are ~1 KB each (DCG pilot: 62 files, ~316 KB). Workbox precache
only globs `js/css/html`, so these JSONs are **not** added to the service-worker
precache; they're fetched on demand.

### Discovery — no flag needed

`vaultResolve.ts` resolves every sibling to an ordered candidate list
(`answerMapUrls`): the verified **Storage sidecar first** (it may carry scheme
crops), the **hosted anchors path second**. The card tries them in order and
takes the first valid map. There is no feature flag and no index change:

- Papers with a verified Storage sidecar behave exactly as before (first fetch
  hits; the hosted path is never tried).
- Papers with only hosted anchors cost **one extra small fetch** on the Storage
  404 (per-URL memoised for the session, cards for the same paper share it, and
  cards fetch lazily via IntersectionObserver only when near the viewport).
- Papers with neither degrade **exactly as today**: both candidates miss → the
  compact "open it in the full paper" row.

**The SPA-rewrite subtlety:** `firebase.json` rewrites every unknown path to
`/index.html` with HTTP 200, so a *missing* hosted sidecar returns HTML, not a
404. "Miss" is therefore detected by parse + the `isAnswerMap` shape guard in
`vaultResolve.ts`, never by status code. The guard also protects against any
valid-JSON-wrong-shape response reaching the renderer.

## Generation pipeline

`scripts/paper-trail/paper_anchors.py <subjectId>` (see its docstring for flags):

1. Reads the subject's slice of the committed index (`paperTrailData.ts`) —
   papers that already have `answers: 1` are skipped, never overridden.
2. Downloads each paper over the public Storage REST endpoint into the
   gitignored `paper-trail-corpus/` cache (same layout as `download.py`).
3. Detects question-start markers in the text layer using the anchor-map.py
   detector conventions (left-margin line starts, unrotated pages, ligature
   normalisation): `section_token` (`A-1.` / `B-2` / `C-3.` — DCG-style
   sectioned papers), `question` (`Question N` / `Ceist N`), `lead_int` (`N.`),
   `sectioned_lead_int` (`N.` whose numbering **restarts per section** — see
   below). A subject pins its grammar in `SUBJECT_GRAMMAR`; unpinned subjects
   run all detectors and the longest clean sequence wins.
4. Emits the sidecar JSONs into `public/paper-anchors/<year>/` plus a per-run
   report in `scripts/paper-trail/out/` (gitignored).

## The `sectioned_lead_int` detector (section-restart numbering)

Some papers restart their bare `N.` question numbering **per section** — a
language reading paper numbers Q1..Qk under text A and then Q1..Qk again under
text B. `det_lead_int` collapses those into one broken run (two `1.`s, a gap,
non-monotonic order) and the paper drops. `det_sectioned_lead_int` walks the
pages in print order maintaining a **current section index**: a left-margin
line matching one of the active subject's `SUBJECT_SECTION_PATTERNS` opens the
next section, and each bare `N.` emits `sort_key=(section_index, N)`. Because
the sort key carries the section, `build_anchors` keeps `(0,1)` and `(1,1)` as
**distinct** questions (mirroring how `section_token`'s `A-1`/`B-1` keys stay
distinct for DCG), and every unchanged gate then runs per section: each
section's run must be contiguous `1..N`, monotonic, span-bounded. The human
`A-1`/`B-2`-style id lands in the sidecar **`label`**; `make_sidecar` still
renumbers `n` sequentially `1..N` in print order, so the `types/paperTrail.ts`
"`n` is the sequential index" contract and `test/vaultAnchors.test.ts` hold.

**Opt-in, zero-regression.** The detector is registered in `DETECTORS` but is
a **byte-identical clone of `det_lead_int`** unless the run is explicitly
pinned to `sectioned_lead_int` (via `SUBJECT_GRAMMAR` or `--grammar`): the
module flag `SECTIONED_ENABLED` gates the section-pattern lookup, so in auto
mode `section_index` stays `0`, every label is the bare `N`, and the output is
identical hit-for-hit — proven in-session against Irish/French/German. On a tie
`build_anchors` keeps the earlier detector, so adding it never displaces
`lead_int`. Populating a `SUBJECT_SECTION_PATTERNS` entry therefore cannot
change an unpinned subject's result.

### Pilot outcome (TV-7): verified structure, **deferred** — do NOT pin yet

`SUBJECT_SECTION_PATTERNS` carries the confirmed section grammar for the three
cleanest-looking section-restart candidates, but **none are pinned in
production** because a bare-`N.` detector cannot safely anchor them:

- **irish** (Paper Two léamhthuiscint, `LC001[A|G]LP200IV`): the reading texts
  A/B number their **passage paragraphs** `1.`..`k.` at the left margin, in the
  *same* section as the real `1. (a)`.. questions. First-occurrence-wins anchors
  land on the paragraphs, the real questions read as out-of-position duplicates,
  and every HL/OL paper drops non-monotonic. Paper One (Cluastuiscint) is worse:
  Cuid I → A/B/C → *Mír* → `1,2,3` restarts three levels deep.
- **french** (`LC010…P000`): reading passages number their **sentences** `1.`..
  `n.`; the `Q.1`/`Q.2` groups then restart `1.(a)`.. Same paragraph-collision
  drop.
- **german** (`LC011…P000`): the reading questions themselves *are* clean per
  `TEXT I/II` section (passage line-numbers are dot-less, so they don't fire),
  **but** the Text-II `Satzhälften` matching task and the `Angewandte Grammatik`
  sub-lists print their own `1.`..`n.` runs inside a question, and stray
  ordinals (`18. Geburtstag`) fire too — fabricating phantom Q5/Q6 that only the
  span / numbering / tail gates catch **by luck, not by guarantee**.

Evidence: `--grammar sectioned_lead_int --dry-run` over 2021–2024 anchored
**0 / 20 irish, 0 / 16 french, 0 / 16 german** — every drop traced to a decoy
(`duplicate marker … out of position (numbering restart?)`, `missing question
number(s) … in the 1..25 run`). See `out/paper-anchors-{irish,french,german}-sectioned-report.md`.
Because `qa_verify` only re-confirms the marker text *is present* at the anchor
(it cannot tell a question from a numbered paragraph), a decoy-contaminated map
that slipped the paper-level gates would still pass re-verify — so pinning these
would risk a wrong crop on future automated runs. **Refusing all of them is the
correct result** (cardinal rule: a wrong crop is worse than none).

These reading papers belong to the same **armed / subsection-aware frontier**
as English P2 and History (below). Unblocking them needs a detector that
recognises the question-block header (`Ceisteanna`, `Beantworten Sie`,
`Répondez`) to **arm** question detection and **disarm** the numbered passages —
strictly more than section-restart tracking. Do not pin `irish` / `french` /
`german` to `sectioned_lead_int` until that lands.

### Still deferred (section-/subsection-restart backlog)

- **irish / french / german reading papers** — passage/matching-task/grammar
  decoy numbering (above). Needs armed question-block detection.
- **other MFL reading papers** (italian, spanish 015/O15 handouts, russian,
  japanese, …) — same numbered-passage class.
- **English Paper 2** — numbering restarts per **subsection** (comparative
  modes; unseen vs prescribed poetry) plus Section I's lettered A–E text
  alternatives. Needs subsection-aware nesting, not just section-aware.
- **History** — topic essays renumber per section behind the DBQ Q1–4;
  topic-aware detection required.

## QA protocol — a wrong crop is worse than none

Question-level (drop the question):
- marker must start a line at the left margin of an **unrotated** page;
- duplicates: first occurrence in print order wins; the sequence must stay
  **monotonic** in print order or the paper drops;
- **independent re-verification**: after building the map, every anchor is
  re-checked — the printed marker text must be re-found at `(pP, pY[0])`; any
  mismatch fails the whole paper.

Paper-level (drop the paper):
- **coverage gate**: ≥3 anchored questions;
- **numbering gate**: the detected numbers must form ONE contiguous run per
  section. The run may start above 1 (biology Section-C docs legitimately
  print 11..17 — "expected" counts `first..last`, not `1..N`). ANY gap inside
  a run hard-drops the paper: a missing number is a missing **marker** (the
  2011 OL maths P2 IV paper prints Q4's header as a dotless "4", so Q4 goes
  undetected and Q3's derived crop would silently swallow it);
- **monotonic gate**: anchors must be monotonic in print order;
- **span gate**: consecutive anchors more than 3 pages apart (`MAX_PAGES`)
  make the viewer's `paperRegionFor` refuse the crop — drop rather than emit
  a sidecar CI would reject;
- **contiguity proof → continuation-page tolerance**: when the run is gap-free
  AND every raw detector hit sits inside its own question's print span (an
  out-of-place duplicate would betray a numbering restart) AND the anchors
  plausibly tile the document (≤3 content pages before the first anchor;
  anchored span ≥50 % of the content pages), anchor-less content pages
  *between or after* anchors are **continuation pages** (answer booklets,
  multi-page questions) — they belong to the preceding question's crop and
  the paper ships, with the tolerated pages noted in the report. Content
  after the last anchor is acceptable under the proof (continuation + answer
  space); note that the last question's crop is anchor → end of its **own**
  page (viewer contract), so later continuation pages are simply not shown —
  verify by render that last questions are neither truncated mid-part nor
  absurdly over-extended;
- **strict fallback**: when the contiguity proof fails, the original blanket
  gates apply — **hole gate** (a non-blank, unrotated page *between* anchors
  with no anchor means a missed question whose neighbour's derived crop would
  swallow it → drop) and **tail gate** (pages after the last anchor must be
  blank/"no examination material" fillers or a short back cover; any real
  content there makes the last question's extent uncertain → drop).

Render QA (`--qa-render N`): renders N **derived** crops per anchored paper
(a Python port of `paperRegionFor`, anchor N → anchor N+1) to PNG for visual
verification that each crop starts at the right question. The first and last
questions are always in the sample (crop-start and last-question/tail are the
highest-risk classes); the rest is a random draw. Multi-page crops are stacked
into one PNG — note pymupdf clipped Pixmaps keep their clip origin, so each
segment is re-origined (`set_origin`) before compositing, else segments land
blank/misplaced.

CI QA (`test/vaultAnchors.test.ts`): every committed sidecar must pass the
runtime shape guard, claim no scheme (`schemeFileid: ""`, all `pagejump`,
`conf < 0.6`), have sequential `n` + monotonic anchors, and yield a non-null
`paperRegionFor` region for **every** question.

## Pilot — design-and-communication-graphics (DCG)

124 papers (2010–2025, HL+OL, EV+IV) → **62 anchored, 62 dropped**, all 8/8
questions (`B-1..B-3`, `C-1..C-5`) on every anchored paper, IV included.
Every drop is a *correct* refusal, not a failure:

- All "Section A" sheets: the four short questions sit in quadrants of a single
  **rotated A3 sheet** — unrepresentable in the vertical-band (`pY`) schema, so
  they anchor 0 questions and drop cleanly (the vault's full-paper fallback
  still opens them).
- 2011 quirk: the SEC archive's fileids are swapped relative to the index
  labels (the doc labelled "Section A"/014 is actually the B&C booklet and vice
  versa). Sidecars key by **fileid** and reflect actual file contents, so the
  anchored maps are correct regardless of the label.

Visual QA: 3 random derived crops per anchored paper (186 PNGs) rendered;
sampled crops across years/levels/languages all start exactly at the question
header with the full figure content.

## Per-subject rollout recipe (remaining ~2,000 papers)

1. Pick a subject with a committed topic taxonomy but missing/partial sidecars.
2. Skim 2–3 papers' text layers (`pt_inspect.py` or fitz) to identify the
   question grammar; pin it in `SUBJECT_GRAMMAR` (add a detector if the grammar
   is new — keep the left-margin/line-start/unrotated rules).
3. `python3 paper_anchors.py <subjectId> --dry-run` — read the report; every
   DROP reason must be explainable (rotated sheets, answer-booklet formats, no
   text layer). Investigate any unexplained drop before shipping anything.
4. Re-run with `--qa-render 3` and visually verify a sample of crops per
   level/language/era (layout changes between syllabus eras are the main risk).
5. Commit `public/paper-anchors/<year>/*.json` for that subject —
   `test/vaultAnchors.test.ts` re-validates every file in CI.
6. Ensure the topic tags for the subject reference the sidecar's sequential
   `n` (labels like "B-2" go in `label`, not `n`).
7. When Storage credentials return (task #94), these artifacts can be uploaded
   as regular `answers/` sidecars and the hosted copies retired — the schema is
   identical, so no app change is needed either way.
