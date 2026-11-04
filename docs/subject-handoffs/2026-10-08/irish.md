# Irish handoff — paused 2026-10-08

## Location and state

- Worktree: `/Users/alexlinehan/Documents/Nextstepuni-Irish-Completion-20261007`
- Branch: `codex/irish-corpus-completion-20261007`
- HEAD: `7bd1e9fbc5b39e62e982435169e298813c83ccbb` — Complete 2011 Foundation Irish written and listening practice.
- Goal is **paused**, at Alex’s explicit credit-limit instruction. The Irish objective is **not complete**. Do not resume research or implementation until instructed.
- No push, merge or deployment performed. Preserve all committed and uncommitted work; coordinating chat will snapshot and integrate validated work.
- No own Irish preview, browser, test, typecheck or build remains running. Preview session 45124 stopped with Ctrl-C; Chrome closed in browser script `finally`; build/test processes finished. Final escalated `ps -axo pid,ppid,etime,command` found no `irish-audit`, `Irish-Completion` or port `5587` process.

## Actual scope and progress

Objective: every independently practicable published mark boundary and finite printed selection in **all 91 Irish paper components, 2010–2026, Higher/Ordinary/Foundation**, in both Mark Bank and Topic Atlas, correctly tagged and carrying full passages, images, poems, schemes and listening material. Foundation completion alone would not complete the task.

Validated committed state: **1,538 Irish Bank cards** (1,087 Foundation +451 Higher/Ordinary), **2,091 Atlas identities**, 66 topics, 91 components. **17/91 fully reviewed; 74 pending; 55 have no Bank cards.** Full Foundation 2011–2025 and Higher 2024 Paper 2 are complete. All 91 papers and 51 unique schemes are locally available. Other Higher/Ordinary material remains partial; counts are not independent completeness evidence.

Latest commits: `7bd1e9fb` 2011 (92 cards: 22 aural +70 written), `e1258ff0` 2012 (74), `2bac2139` 2013 (68), `9f8ce05f` 2014; `b7293651` fixes shared PDF.js WASM/image assets. Earlier Foundation years 2015–2025 were committed previously. Do not lose that shared decoder fix.

## Exact stopping point: unvalidated 2010 draft

**2010 / Irish / Foundation / Irish version (`iv`) / written Paper One Q1–Q6**, with the last drafted task **Q6(b), cycling/horse incident**, and all 16 Q4/Q5/Q6 writing combinations. Only a new generator file has been written; **it has never been executed or syntax-tested**. No 2010 Bank JSON, answer maps, source-review JSON, tests, imports or counts have been added. It currently depends on the absent `scripts/markbank/authored/irish-foundation-2010-source-review.json`, so it is not ready to run.

All **16 written +8 aural +17 scheme pages** have been read and visually swept, including covers/blanks. Source text and rendered pairs are in `tmp/irish-audit/foundation2010/`. This sweep is not yet captured in a checked-in review ledger.

Sources and SHA-256:

- Written `paper-trail-corpus/exampapers/2010/LC001BLP100IV.pdf`: `7553abaa485b8b68ac585887e55e58522ad9597392fe85940289e167293fea1b`
- Aural `paper-trail-corpus/exampapers/2010/LC001BLPA00IV.pdf`: `e6e21527a147acb955fd6485c970724127f7fc60976b15b0288f3c26693938d3`
- Shared scheme `paper-trail-corpus/markingschemes/2010/LC001BLP000IV.pdf`: `a29bb58dc74195783c6e67b36ea6eea22b027aa838907c014a2d26a18f410be0`

2010 written draft: 70 cards =40 reading parts +8 writing variants +6 choose-two reading pairs +16 full writing products. Written total270: matching40, Q2=50, Q3=60, Q4=30, Q5=40, Q6=50. Internal Bank sections remain 2=reading, 3=writing. Full writing selections total120, with three source pages.

Important 2010 findings already incorporated in the draft, but still require validation:

- Matching key `EHDGAFBJCI`, scheme PDF3. Q2 answers PDF3; Q3 PDF4, special notes PDF5 for 3(a)(3), 3(b)(2), 3(c)(4). Special permitted marks `[0,4,6]`, not 2011’s `[0,2,4,6]`. Sharon: full paragraph explicitly accepted; “Ceol draíochta”4, “Bosca ceoil”/“Ceol”0. Gráinne excess information costs2. Poem two lines4, full stanza0.
- Poem **An Canaerí**, four complete stanzas/16 lines with cage and two bird illustrations, written PDF8.
- Notice Q4(a), written10/scheme7–9: 1+6+9+3+3+8=30, cycling trip/Club Óige Inis; preserve 2010 date/time/tense allowances.
- Reply Q4(b) to **Phil**, written11/scheme10–11: layout2+1+1; six required details×3; language8. The supplied invitation is in picture2; do not omit it or treat the six details as alternatives.
- Hardware-store letter Q5(a), written12/scheme12–14: layout6, pictures4+12+4+4, language10. One customer reference; two free-time activity references with −1 for an absent activity. Scheme’s picture2 heading says “san óstán” although paper/examples concern the store; explicit source note. Illustrative activity examples are not a closed selection menu.
- K-Club form Q5(b), written13/scheme14–15, **Áine Bhreathnach**, dates **21 Iúil /28 Iúil /4 Lúnasa**. Fields15 use doubled30÷2, rounding up once; relevant paragraph15/off-topic5, length reduction applies only to paragraph; language10. Published conflict: birth-date row½ vs doubled2, undoubled sum14½ vs printed15. Preserve both columns and disclose use of explicit doubled method.
- Q6(a) beach day, written14/scheme15–16; Q6(b) cycling/horse incident, written15/scheme16. Communication37 with proportional length adjustment, language13. Five references, but **no fixed −5 missing-reference penalty**. Accommodation guidance scheme17; no four-point conversion table or aural transcript.

2010 **aural remains a source gap**, not complete or integrated. Scheme PDF2 gives 22 parts/180 marks. Q1–3 a/b7 each; Q4/5 seven each; Q6–9 a/b8 each; Q10–12 a/b10 each. Map answer bottom right. All questions/images are in aural PDF2–6. Live SEC archive listing saved as `foundation2010/sec-archive.html`; only `LC001ZLP017IV.mp3` is listed, not Foundation `B` audio. Both `LC001BLP017IV.mp3` and `LC001BLPO17IV.mp3` returned404. Z recording returned200/38,471,356bytes but **has not been verified as Foundation and must not be substituted**. St Munchin’s Irish aural page explicitly labels 2010 Foundation unavailable: https://stmunchinscollege.com/academics/leaving-cert-programme/irish/ . Further recovery remains pending. Do not fabricate audio/transcript or mark this component complete.

## Files and authoritative ledgers

Uncommitted/untracked at stop:

- `scripts/markbank/authoring/irish_foundation_2010.py` — new, unrun draft above.
- `scripts/markbank/authored/irish-resume-checkpoint-20261007.json` — informal resume checkpoint; committed counts current, but its 2010 sweep note is stale. This handoff supersedes it.
- `tmp/irish-audit/` — substantial untracked QA evidence; preserve in full snapshot, do not bulk-add to a content commit.
- This handoff. No tracked modifications remained after the 2011 commit.

Authoritative project ledgers: `scripts/markbank/authored/irish-archive-inventory.json` (full91 scope/gaps), per-year `irish-foundation-*-source-review.json`, `irish-paper-reviews.json` (Higher), generated `components/MarkBank/cards/irish/*authored.json`, `data/examTopics/irish-local-crosswalk.json`, `scripts/paper-trail/topic-tags/tags/irish.json`, and answer maps in both `scripts/paper-trail/answers/` and `public/paper-answers/`.

2011 commit also changes `foundation.ts`, sizes, `vaultResolve.ts`, `paperIndex.mjs`, inventory authoring, Irish crosswalk builder, derived tags/runtime/anchors and regression counts. `paperIndex.mjs` now maps the exact older Foundation Paper One/Aural Paper pair from Bank sections1/2/3. Crosswalk filters by year **and file**, preserves twelve existing aural numeric identities, and uses the correct shared scheme filename. 2011 shared scheme is **`LC001BLP000EV.pdf`**, even though the verified text is Irish.

## Method and invariants

Read repository `AGENTS.md`; NextStepUni UI decisions also require `/Users/alexlinehan/Documents/Nextstepuni-Module-Brand-Review-20261005/AGENTS.md`. No new UI design is currently necessary. No subagents unless explicitly authorized.

Visually sweep every paper and entire applicable scheme; use published tariff boundaries, not parser counts. Classify every raw selection directive and fail unknown/stale entries; mechanically expand finite choose-k routes. Keep required headings, open content and illustrative examples intact. Carry full source context into every task/combination. Preserve source conflicts explicitly, never invent an SEC correction. Original PDFs stay untouched. 2011 needed geometry-based duplicate-glyph extraction; 2010 raw text is readable and draft uses raw extraction.

Preserve every prior Bank JSON byte-for-byte, every Atlas identity, prior answer-map fields and other subjects. **Never refresh the preservation baseline to make checks pass.** Source review, zero-open/zero-orphan reconciliation, preservation and required tests precede any completion claim. `irish_inventory.py` currently treats presence of a review as complete, so never feed an audio-blocked component into that reviewed list prematurely.

Heavy checks sequentially: Vitest one worker →typecheck →preview/browser (close) →build. No unrelated process termination. No push/deploy.

## Exact commands for resumption (not run during pause)

Run from the worktree above. For 2010, create/review its missing ledger before invoking the draft.

```sh
python3 scripts/markbank/authoring/irish_foundation_2010.py
python3 scripts/markbank/authoring/irish_foundation_2010.py --check
node scripts/paper-trail/build-irish-exam-topic-crosswalk.mjs
node scripts/paper-trail/topic-tags/build-tags.mjs
python3 scripts/markbank/authoring/irish_inventory.py
python3 scripts/markbank/authoring/irish_inventory.py --check
npx vitest run test/markBankIrish*.test.ts test/irishExamTopics.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts test/vaultAnchors.test.ts test/markBankSession.test.ts --maxWorkers=1
node node_modules/typescript/lib/tsc.js --noEmit
npm run dev -- --config tmp/irish-audit/vite.config.ts --host 127.0.0.1 --port 5587 --strictPort
node tmp/irish-audit/browser-materials.mjs
npm run build
git diff --check
```

Browser command needs approved external Chrome execution (`node tmp/irish-audit/browser-materials.mjs` prefix). Current general browser script is **2011**, not2010: saved identical copy `tmp/irish-audit/foundation2011/browser-materials.mjs`. Update routes/year/maps for the next batch. Preview supports historical split papers via `year=2010&atlas=...` (written) or `&aural=1` (aural). Source navigation now loops all pages. Assert actual source/scheme page counts, image decode warnings, audio playback, focus restoration and no overflow; inspect screenshots visually.

Preservation script for last batch: `python3 tmp/irish-audit/foundation2011/preservation.py`, pinned to `e1258ff0`/1446 old cards/2002 Atlas identities. **For new 2010 work create a new comparison against HEAD `7bd1e9fb` (1538/2091), rather than altering the frozen fixture.** Regeneration idempotence: hash generated Irish JSON/anchors/maps/tags before and after the generation chain; require identical bytes. Review new counts manually against swept boundaries.

## Last passed checks / limitations

2011: all364 regression checks passed across the full run and corrected targeted rerun. Exact last full log `foundation2011/tests-final.log`: **363 passed, one stale spacing assertion failed**; assertion fixed and `tests-targeted-final.log` then **10/10 passed**. No full-suite rerun after that text-only test fix. Previous paper-resolver and band failures were fixed; duplicate source notice fixed before final checks. Typecheck exit0 (`typecheck.log`).

Mobile: **20 Bank +21 Atlas routes**, readyState4 and actual playback of official 2011 audio, duration1865.613063sec; five listening source pages; three-page writing products; whole-writing11 scheme pages; zero JS/PDF image decode errors, no Bank horizontal overflow, focus restored. `browser-results.json` and65 screenshots in `foundation2011/`. Screenshots were captured **before the final spacing-only prose cleanup**; functional behavior unchanged. Production build after cleanup passed in16.31s plus service worker (`build-final.log`); normal large-chunk warning only. Generation idempotence and preservation passed after cleanup; all1446 pre-2011 Bank cards byte-identical,2002 old Atlas IDs and all2012–2025 answer fields retained, other subjects unchanged. `git diff --check` passed before commit.

**2010 draft: no generation, reconciliation, tests, typecheck, browser or build run.** Missing source-review input is a known prerequisite, not a tested failure. Do not integrate this draft as validated output.

## Next three actions after explicit resume

1. Finish the 2010 source-review ledger from the completed41-page sweep, classify every raw directive (draft adds `trí phointe`), record the Foundation audio gap separately, and validate/correct the unrun written generator against the actual PDF wording.
2. Generate and integrate only the validated2010 written tasks; add meaningful tariff/route/source/conflict regressions, preserve all1538 prior cards/2091 Atlas IDs, regenerate crosswalk/tags/inventory, then run sequential checks and mobile QA before checkpointing.
3. Continue the **entire remaining91-component scope**: recover the2010 Foundation recording if possible, review2026 Foundation, then remaining Higher/Ordinary papers. Keep unresolved material explicit; never declare the subject complete from Foundation coverage.

## Snapshot-critical local artifacts

Preserve `paper-trail-corpus/` PDFs and `scripts/paper-trail/out/manifest.jsonl` (ignored/local source inventory), `tmp/irish-audit/` in full, and the untracked resume checkpoint. `node_modules` is a symlink to the main repo’s installed dependencies; do not upload it as source. Particularly useful: 2010 TXT +all21 visual pair JPGs +live archive HTML; 2011 browser script/results/screenshots, logs and preservation script; generic `preview.tsx`, `preview.html`, `vite.config.ts`. Older per-year QA folders remain useful. Scratch `foundation2011/author.py` and `finalize-author.py` are stale: **do not rerun them**; the committed real generator is authoritative.
