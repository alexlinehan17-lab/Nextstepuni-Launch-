# ⚠️ Biology HL Section A&B — QUARANTINED, needs correct remap (2026-07-23)

Biology Higher Section A&B (`LC025ALP038EV`, years 2020/2022/2023) was mis-anchored:
the map anchored each question on its END-of-block summary mark-table
("Qn (a)–(f) Number of correct responses / Mark") instead of the "Question N"
DETAIL heading, so question N's Answers ribbon revealed question N+1's scheme
(user caught Q3 showing Q4). PULLED live in commit `020002b` (de-flagged; 1262→1259).
The 3 broken sidecars are saved in `scripts/paper-trail/_quarantine_biology038/`.
**To remap correctly:** anchor schemeStart on "Question N" (detail heading), end on
"Question N+1", via lang_reading.py spec; the Ordinary 038 (2019, LC025GLP038EV) is
CORRECT and shows the right layout to match. Only these 3 HL papers were affected —
scope-scanned all 1259 shipped maps, everything else aligns. Profile
('biology','higher','ev') stays QA-passed for its OLD-format 000 years (correct).

---

# Next answer-mapping wave — PAUSED 2026-07-22 (mid-flight)

Nothing committed or pushed. Live app untouched. All new sidecars are untracked
files under `answers/`; no `answers:1` flag lights until `build-index.py` is
re-run AND `paperTrailData.ts` is committed. So this is a clean pause.

## What's on disk (258 new sidecars vs prior commit `1107403`)

Snapshot of the file list: `wave_all.txt` was in scratch (regen with
`find answers -name "*.json" -newer rem_wave.py`, but note rem_wave.py mtime may
have moved — better: `git status --short answers/` once these are staged, OR diff
against the 1,262 already flagged).

### Bucket A — deterministic engine maps (216) — SHIPPABLE tier, sample-verify then ship
Produced by `rem_wave.py EV,IV,BV B` (Foundation) + the additive engine sweep.
Under **already-QA-passed** profiles → will light on build-index. Same reliability
tier as everything already live (engine drops on count-reconcile failure).
- **Foundation Maths** LC003B: 18 sidecars (ev+iv, 2010–2023). Profiles
  `('mathematics','foundation','ev'/'iv')` already passed. Spot-checked Q5 2023 = clean.
- Plus ~200 additive older years across passed profiles (Maths HL/OL, Art HL/OL,
  Economics, Accounting, Ag Econ, Latin, English OL, sciences, IV variants…).
  See `light_run1.json` in scratch for the exact (subject,level,lang,years) that light.
- **Irish Foundation** LC001B: engine reconciled 0 — nothing to ship.
- Remaining self-QA before shipping: render a representative sample per profile
  receiving NEW years (contact-sheet.py or lang_render.py) and eyeball. Delete failures.

### Bucket B — BV-language written papers (42) — NOT VERIFIED, DO NOT SHIP YET
Agent-authored via `lang_reading.py` specs in the `bv-language-answer-wave` workflow
(run `wf_a6155d51-c62`). **The workflow ran OUT OF CREDITS mid-verification (resets
Jul 28 06:00 Europe/Dublin), so NONE of these are render-verified.** Founder rule =
nothing ships unverified. They passed a deterministic integrity check (monotonic n,
sane y-bounds, coherent per-paper labels) but that is NOT the visual QA gate.
- French LC010 (partial), German LC011 (all yrs), Italian LC013 (all yrs),
  Japanese LC058 (partial). **Russian LC099 never authored** (died on credits first).
- These are 2019–2025 written papers — the BV doc IS the main paper (EV scheme pair).
  All 10 lang profiles (fr/de/it/ja/ru × HL/OL) are ALREADY in QA_PASSED, so these
  WILL light the moment they're on Storage + build-index runs — which is exactly why
  they must be verified or deleted first.
- Resume options: (a) after Jul 28 reset, resume the workflow
  `Workflow({scriptPath:".../bv-language-answer-wave-wf_a6155d51-c62.js", resumeFromRunId:"wf_a6155d51-c62"})`
  — cached authors replay free, only verifiers + Russian re-run; OR (b) self-verify by
  rendering each with `python3 lang_render.py answers/<yr>/<file>.json` and reading crops.
- Finish scope: Russian LC099 (13 papers) + Japanese remaining years still un-authored.

## Ship checklist (when resumed)
1. Delete any Bucket-B sidecar that fails visual QA (never overwrite/ship approximate).
2. Build upload TSV (localPath\tremotePath, remote = `papers/lc/<subjectId>/<year>/answers/<fileid>.json`? — CHECK: answers path is `answers/<...>`; see upload_answers.py + out/answers-upload-manifest.jsonl for the exact remote key).
3. `python3 upload_answers.py <tsv>` (gcloud authed nextstepuniinfo@gmail.com, project nextstepuni-app).
4. Add any genuinely-new QA profile tuples to `QA_PASSED_ANSWER_PROFILES` in build-index.py
   (Foundation Maths already present; most Bucket-A light under existing profiles — likely NO new tuples needed).
5. `python3 build-index.py` → regenerates `paperTrailData.ts`.
6. Verify diff is answers-flags-only (+curriculumId links): `git diff paperTrailData.ts`.
7. Integrity: curl every new `answers:1` file on Storage (expect HTTP 200). SSL note: use curl not urllib on macOS.
8. Gate: `npm run typecheck` + `npm run build` (+ `npm test`).
9. Commit + push to main (deploys live via CI).

## Cleanup already done this session
- Deleted 11 English OL Paper-1 engine strays (`LC002GLP100EV`, P1 declared not-mappable).
- Deleted 8 French BV engine dupes (belong to the agent workflow, not the engine).
- Patched `rem_wave.py`: `levels` arg was dead (build_pairs reads the global SCOPE_LEVELS);
  now unions LEVELS into `am.SCOPE_LEVELS`. Foundation ('B') papers were silently excluded before.
