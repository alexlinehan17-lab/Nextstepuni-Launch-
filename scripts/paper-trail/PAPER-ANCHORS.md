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
   sectioned papers), `question` (`Question N` / `Ceist N`), `lead_int` (`N.`).
   A subject pins its grammar in `SUBJECT_GRAMMAR`; unpinned subjects run all
   detectors and the longest clean sequence wins.
4. Emits the sidecar JSONs into `public/paper-anchors/<year>/` plus a per-run
   report in `scripts/paper-trail/out/` (gitignored).

## QA protocol — a wrong crop is worse than none

Question-level (drop the question):
- marker must start a line at the left margin of an **unrotated** page;
- duplicates: first occurrence in print order wins; the sequence must stay
  **monotonic** in print order or the paper drops;
- **independent re-verification**: after building the map, every anchor is
  re-checked — the printed marker text must be re-found at `(pP, pY[0])`; any
  mismatch fails the whole paper.

Paper-level (drop the paper):
- **coverage gate**: ≥3 anchored questions and ≥60 % of expected (expected =
  contiguous `1..max` per section, so a gap counts against coverage);
- **hole gate**: a non-blank, unrotated page *between* anchors with no anchor
  means a missed question whose neighbour's derived crop would swallow it →
  drop the paper (this is what protects against the silent-missing-marker
  failure mode);
- **tail gate**: pages after the last anchor must be blank/"no examination
  material" fillers or a short back cover; any real content there makes the
  last question's extent uncertain → drop.

Render QA (`--qa-render N`): renders N random **derived** crops per anchored
paper (a Python port of `paperRegionFor`, anchor N → anchor N+1) to PNG for
visual verification that each crop starts at the right question.

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
