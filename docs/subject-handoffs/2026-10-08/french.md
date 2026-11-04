# French handoff — paused 8 October 2026

## Location and state

- Actual worktree: `/Users/alexlinehan/Documents/Nextstepuni-French-Bank-Atlas-20261007`
- Branch: `codex/french-complete-bank-atlas-20261007`
- HEAD: `fdc123c3b829b9437f4e4982a514086afb8e0776` — Complete reviewed 2016 French writing with distinct formal-letter grid.
- Other recent commits: `986df44f` (2017 writing/cloze), `bb64cd9f` (2018 writing/cloze), `f51ef7ce` (2019 writing/cloze and 2010 census cue fix), `970badcf` (2010 reading), `195bd41b` (2011 reading).
- Explicitly paused by Alex to conserve credits. Preserve all edits. No push, merge, deployment, baseline update, or additional research performed for this handoff.
- Do not work in or overwrite the separate `Nextstepuni-French-Completion-20261007` worktree.

## Exact interruption point

**Uncommitted current batch: 2015 French, Higher and Ordinary Level, English paper edition (`ev`), main sitting, Section II writing and OL Section A(a) cloze.** All relevant original paper/scheme pages were visually reviewed. Generation, integration and 317 targeted tests passed. Its browser and type checks remain unfinished.

The next browser cases already configured in `tmp/french/browser.mjs` are:

- `fr-2015-ol-writing-b2a-route-123` — OL Section II B(a), message to cousin Thomas/Michelle in Paris, dark phone.
- `fr-2015-ol-cloze-b1a-gap-1` — OL Section II A(a), first gap (`écrit`), light phone.

The attempted browser command was aborted while awaiting execution/approval. **No `tmp/french/2015-writing-browser.log` exists, and no browser process is running. Do not claim this check passed.**

Read-only preparation had reached **2014 HL `ev`, Section II Q4(b), gender-equality cartoon on paper PDF page 12**. All four 2014 HL writing paper pages (6, 8, 10, 12) were seen. The subsequent tool call that would display HL scheme pages 16/17 was aborted: **those images have NOT been visually reviewed**. No 2014 writing/cloze ledger or generated additions exist. All 2014 OL writing pages and all 2014 writing schemes remain to be visually reviewed.

## Completed and unfinished scope

Objective: every separately practicable French Paper Trail task represented in Mark Bank and Topic Atlas, correctly mapped, with usable passage/image/audio sources. **The corpus is not complete.**

- Reading reviewed/generated for 2010–2026: **925 cards** (372 HL, 553 OL).
- Listening reviewed/generated for 2010–2026: **715 cards**. Earlier audio checks exercised actual MP3 seeking across all 17 years.
- Writing/cloze committed and checked for 2016–2026. Uncommitted 2015 adds 18 writing tasks + 10 cloze gaps.
- Current generated deck: **2,214 cards** = 4 preserved legacy cloze + 450 writing (96 HL, 354 OL) + 925 reading + 120 cloze + 715 listening.
- Current Atlas question count: **3,117**. Reviewed manifest: 2,210 tasks; 96 HL writing tasks reuse archive identities, so these are not added twice to the 1,003 archive questions.
- All original **260 card identities** preserved: 256 reading cards independently corrected with source evidence, four legacy cloze retained. Immediately before integration, all previous 432 writing and 110 cloze cards compared byte-equivalent by ID against HEAD.
- Latest reconciliation from `tmp/french/2015-writing-deck.log`: **1,806/1,876 paper asks covered; 70 OPEN; 0 orphan; 0 unparsed; 208 census flags**. Open asks correspond to 2010–2014 writing/cloze. The 208 flags still require final audit; counts are not independent completeness proof.
- Inventory: 98 paper variants, 150 source documents (98 papers, 52 schemes). Final whole-inventory variant/source alignment and zero-open/zero-orphan review still required.
- Coverage/preservation baselines have deliberately NOT been updated.

## Uncommitted tracked files

```
components/MarkBank/cards/french/cloze.json
components/MarkBank/cards/french/writing.json
components/MarkBank/cards/sizes.json
components/landing/subjectShowcase.json
data/examTopics/french-reviewed-tasks.json
public/paper-anchors/2015/LC010ALP000EV.pdf.json
public/paper-anchors/2015/LC010GLP000EV.pdf.json
scripts/markbank/authoring/fr_writing.py
scripts/markbank/authoring/french-cloze-review.json
scripts/markbank/authoring/french-selection-review.json
scripts/markbank/authoring/french-writing-review.json
scripts/markbank/authoring/french-writing-sources.json
test/frenchCloze.test.ts
test/frenchExamTopics.test.ts
test/frenchReading.test.ts
test/frenchWriting.test.ts
```

`tmp/french/` is untracked and contains essential local evidence/scripts; preserve it in the snapshot. This handoff is newly added, uncommitted.

## Authoritative ledgers and source method

- `scripts/markbank/authoring/french-writing-sources.json`: verified year-specific prompts, pages, tariffs, grids, format notes, source discrepancies and illustration decisions. This is authoritative over temporary add scripts.
- `french-writing-review.json`: generated review boundaries/source hashes.
- `french-cloze-review.json`: exact source hashes, answer sequence, printed word-bank order and gap boundaries.
- `french-selection-review.json`: raw selection directives and reviewed classifications, keyed by source hash/page. Both reading-only and whole-paper entries are intentional.
- `french-reading-review.json` and listening review/source ledgers in the same directory: completed earlier reviews.
- `data/examTopics/french-reviewed-tasks.json`: exact card-to-Atlas identities/source pages.
- `data/examTopics/french-local-crosswalk.json`, `data/examTopics/french-curriculum-crosswalk.json` and `data/examTopics/french-runtime.json`: generated topic links; use the crosswalk builder rather than inventing taxonomy. Existing archive identities must survive.
- Source PDFs: `examiner-reports/french/papers/{YEAR}-{hl|ol}-000-paper.pdf`, listening `{YEAR}-{hl|ol}-A00-paper.pdf`, and `examiner-reports/french/schemes/{YEAR}-{hl|ol}.pdf`. Source corpus is shared through symlinks to `/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus`. Do not alter shared source bytes.

Method: inspect original rendered paper and scheme pages visually, then extract text with PyMuPDF/`FrPaper`; record independently priced boundaries and source hash; classify every raw selection directive; pin exact source wording with generator assertions; generate cards and Atlas identities; compare all prior cards by ID; reconcile; run targeted tests and local mobile source-viewer checks. Tiled 2011 text required coordinate-based glyph reconstruction in `fr_pdf_words.py`; do not generalize deduplication blindly.

Repository `AGENTS.md` invariants apply: one card per independently practicable published mark boundary; mechanically expand every closed choose-k pool; preserve all shared context and source pages; do not expand open examples, compulsory bullets or real/imaginary scope. Never use parser/card counts as sole completeness proof. No baseline update before full visual sweep, original-ID preservation, zero-open/zero-orphan reconciliation and required tests.

Design decisions were read from `/Users/alexlinehan/Documents/Nextstepuni-Module-Brand-Review-20261005/AGENTS.md`: no emojis, visibly clickable controls, strong selected states, preserve approved treatments. PDF skill read earlier: `/Users/alexlinehan/.codex/plugins/cache/openai-primary-runtime/pdf/26.921.10847/skills/pdf/SKILL.md` (read-only source rendering).

## Important year-specific findings

- **2015:** 8 HL alternatives at 40/30 marks; all three email questions required; culture examples are open, not finite routes. B3(a) phone photo and B4(a) polling photo retained. B3(b) Béatrice quote uses verified paragraph override because PDF extraction order differs from visual order. OL form has five 2-mark fields and one 20-mark four-sentence unit; four other alternatives each require all three points. Form middle language band includes `some sense of register`; message scheme p12 omits it, and postcard/diary explicitly reference that grid. New `olTaskLanguageOmit` handles only B2A/B2B/B3A, verifies omitted text is absent and retained descriptors present. Formal letter appendix PDF18/19: Mullingar, le 10 juin 2015; more than three format mistakes gives 0, with separately stated top-layout one-mark exception. Field5 correctly says level of French; no 2016 discrepancy copied. Cloze: écrit, voyage, dernier, ballon, passer, dit, parents, pas, avec, de.
- **2016 committed:** HL Q2(b) job application uses Formule6 + Communication12 + Language12; all five application points and full ad retained. No published HL suballocation for format, so no invented 3+3. Only Q2(a) ignores layout. OL field5 paper says `Niveau de français`, scheme says years of study; visible source discrepancy limited to that card. Formal OL appendix PDF18/19, Buncrana 15 juin 2016.
- **2017 committed:** OL paper street Pasterolli vs scheme Pastorelli; preserve paper and disclose discrepancy. HL email requires four answers. Brexit boxed prompt uses source-verified paragraphs.
- **2014 next:** HL Q4(b) cartoon must retain full illustration; text layer contains only part of cartoon lettering, so use verified reaction prompt with source image. Q4(a) smoking boxed title/body/citation must remain together. No implementation started.

## Exact commands (run in this worktree, only after resume)

Generation and integration, sequential:

```sh
python3 scripts/markbank/authoring/fr_writing.py
python3 scripts/markbank/authoring/fr_cloze.py
# Only regenerate reading when intentionally changing its reviewed ledger:
python3 scripts/markbank/authoring/fr_reading.py
node scripts/markbank/build-deck.mjs scripts/markbank/authored/french.json > tmp/french/2015-writing-deck.log 2>&1
node scripts/paper-trail/build-french-exam-topic-crosswalk.mjs > tmp/french/2015-writing-crosswalk.log 2>&1
node scripts/paper-trail/french-reviewed-anchors.mjs
node scripts/build-subject-showcase.mjs
python3 scripts/markbank/authoring/reconcile.py french --json tmp/french/2015-reconciliation.json --open > tmp/french/2015-reconciliation.log 2>&1
```

Full reconciliation exits nonzero while asks remain open. Do not run blanket `fr_all` or update baselines to suppress that.

```sh
npm test -- --run test/frenchReading.test.ts test/frenchWriting.test.ts test/frenchCloze.test.ts test/frenchListening.test.ts test/frenchExamTopics.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts --maxWorkers=1 > tmp/french/2015-writing-tests.log 2>&1
python3 -m unittest discover -s scripts/markbank/authoring/tests -p 'test_fr_*.py'
npm run typecheck > tmp/french/2015-writing-types.log 2>&1
npm run typecheck:test >> tmp/french/2015-writing-types.log 2>&1
npm run build > tmp/french/final-production-build.log 2>&1
git diff --check
```

Use only one heavy check at a time; shared Mac memory is constrained. Do not launch new tests while paused.

Browser commands:

```sh
npm run dev -- --config tmp/french/vite.config.ts --host 127.0.0.1 --port 5440 --strictPort
node tmp/french/browser.mjs > tmp/french/2015-writing-browser.log 2>&1
```

Browser execution requires `sandbox_permissions: require_escalated` because Chromium Mach bootstrap fails in the sandbox. The custom Vite fs allowlist is needed for the real PDF worker path. Playwright resides in `tmp/french/qa/node_modules`. Browser intercepts source URLs with the local original SEC PDF bytes; this verifies rendering, **not production PDF availability**. Checks cover PDF canvas/zoom/navigation, 390px dark/light layouts, 44px score controls, JS errors and horizontal overflow. Inspect output PNGs visually. `browser-results.json` is overwritten each run and currently belongs to **2016**, not 2015. Field cards now select their sole score control instead of nonexistent Language mark.

## Last checks and known failures

- **2015 current:** generation and integration passed; 432 prior writing/110 prior cloze cards unchanged; **317 tests passed across 8 files**, log `tmp/french/2015-writing-tests.log` (08:32:44, 16.48s). Reconciliation 70 open, zero orphans/unparsed. Browser never started; typechecks and final diff check not yet run for this batch.
- **2016 HEAD:** 316 tests passed across 8 files; typecheck and typecheck:test passed (`2016-writing-types.log`, session27013 exit0). Both mobile cases passed after fixing the temporary field-selector harness. PNGs for application question/source/grid and field grid visually reviewed; no JS errors/overflow; controls44px. Initial browser run waited for nonexistent Language mark on field card and was safely stopped; rerun passed.
- **2017 commit:** 315 tests, typechecks and mobile checks passed.
- Python tests last passed earlier: 20 tests at the 2019 batch. New 2015 generator path is source-asserted and covered by the TypeScript content regression, but Python suite not rerun since.
- Production build last passed at 2019 commit `f51ef7ce`, before additions for 2018/17/16/15. Existing large-chunk warning only; final build still due.
- Known resolved 2015 generation failure: B3(b) boxed quote extraction order failed source assertion; verified paragraph override fixed it. **Do not rerun `tmp/french/add-2015-writing.py` blindly: it predates the final B3B override.** Similar earlier temporary add scripts may also be stale.
- `tmp/french/2010-reading-reconciliation.json` is stale from before the nested `paperCues` fix; use current deck log or rerun reconciliation later.

## Process state and artifacts to preserve

No browser, Vitest or typecheck process was running at handoff inspection. Only this worktree's preview remained: npm PID95481, Vite PID95493 on5440. The initial sandbox TERM was denied; the authorized escalated TERM succeeded. Final process inspection confirmed both preview PIDs and the French browser process absent. No other worktree process was touched.

Preserve all `tmp/french/`, especially:

- `browser.mjs`, `review.html`, `vite.config.ts`, browser fixtures and `qa/` dependency setup;
- `{YEAR}-{hl|ol}-writing-{paper|scheme}-{page}.png` source-review images, and browser `{case}-{question,source,grid,answer-guide}.png` evidence;
- `2015-writing-{deck,crosswalk,tests}.log`, `2016-writing-{tests,types,browser}.log`, `browser-results.json`;
- temporary add scripts and `RESUME-CHECKPOINT-20261007.txt` (that checkpoint is now stale; this handoff supersedes it);
- earlier reading/audio evidence, full census/source inventories, downloaded source metadata and all review notes.

`node_modules` is a symlink through the Module-Brand-Live worktree to Kobra-Sidebar dependencies. Source corpus symlinks and temporary review harness dependencies must be restored if snapshotting onto another machine.

## Next three actions — only after Alex resumes

1. Finish the uncommitted 2015 batch: restart only this preview, run the two configured browser cases, visually inspect screenshots, run typechecks and diff check; preserve original-ID/card equality; commit only the validated 2015 tracked files if authorized by integration workflow.
2. Resume at 2014 HL scheme PDF16/17, then OL paper10/11/12/14 and scheme10–15/18/19. Finish 2014 writing/cloze before moving to 2013–2010; retain source-specific boundaries, descriptors and all finite routes.
3. Once remaining papers are reviewed, resolve the 208 census flags and all98variant alignment, require zero-open/zero-orphan reconciliation and old-ID preservation, then final targeted checks/browser QA/build. Only then consider deliberate baseline updates or a completion claim; coordinate integration separately.

Goal status confirmed `paused` by `get_goal` at handoff. All tracked and temporary edits are preserved; nothing was committed during this handoff.
