# Subject work: saved at the 8 October 2026 pause

Alex requested a stop to conserve credits, exact checkpoints on `main`, and integration of validated work only. All twelve original subject sessions wrote the handoffs linked below and stopped. Incomplete goals were paused; already completed goals were left complete. No subject research should restart automatically.

The archive is a preservation checkpoint, not a claim that every subject is finished or published. Each handoff was written by its original session and distinguishes completed review from drafts, known failures and checks still needed. It includes working instructions, commands, source locations and the next actions. Check the current main branch and release history before integrating a completed subject a second time.

| Subject | Exact checkpoint | Resume note |
| --- | --- | --- |
| Accounting | Local review complete: 1,370 tasks across 68 editions; integration checks still required. | [Accounting](accounting.md) |
| Applied Mathematics | Local review complete: 1,486 tasks, 66 source editions; final desktop/phone and build checks passed. | [Applied Maths](applied-mathematics.md) |
| Physical Education | Local review complete: 873 cards across 13 paper/scheme pairs. | [PE](physical-education.md) |
| Politics and Society | Local review complete: 1,086 tasks across 17 papers; original draft PR #223. | [Politics](politics-and-society.md) |
| English | 2016 Paper 1 Higher/Ordinary source inspection done; write the authoritative review ledgers next. | [English](english.md) |
| Mathematics | 2014 Foundation Paper 2 validated; research resumes at 2013 Foundation scheme PDF page 17, Q9(f). 18/111 English papers reviewed. | [Maths](mathematics.md) |
| French | 2015 writing/cloze generated and targeted tests passed; browser/type checks pending. Older 2010–2014 writing/cloze remain. | [French](french.md) |
| Irish | 17/91 components reviewed, 2011 Foundation committed; 2010 Foundation source sweep/draft unfinished. | [Irish](irish.md) |
| Business | 2020 Higher validated; 2021 Higher sources prepared next. Three frozen-count checks remain unresolved. | [Business](business.md) |
| Economics | 2024 Ordinary Irish sweep finished; latest corrections await final generation and validation. | [Economics](economics.md) |
| Agricultural Science | 2012 Higher English committed; 2012 Higher Irish crop/binding integration failed before publishing that batch. | [Agricultural Science](agricultural-science.md) |
| Construction Studies and shared earlier subject work | 2015 Higher theory complete locally; 2015 Ordinary Q1 validated draft, Q2 next. Large shared worktree also preserves preceding subject work. | [Construction/shared archive](construction-studies.md) |

## What is saved

`snapshots.json` maps every subject to its original worktree, original HEAD, exact snapshot tree and portable restore commit. The archive includes tracked changes, new implementation files, review ledgers, draft code, original subject-specific source files where locally available, browser harnesses and review evidence. File bytes for every changed path were verified against the source worktree before packaging. Each `SUBJECT.snapshot.json` lists explicitly omitted caches, local credential containers, dependency/corpus symlinks and unrelated documents. No original worktree was reset or cleaned.

`archive/` holds a split Git bundle; `archive-manifest.json` records its complete and per-part SHA-256 checksums. This is a substantial archive because it includes the preceding shared subject audit. Keep all parts together. A full-history clone of main supplies the bundle prerequisites. On a shallow clone, run `git fetch --unshallow origin` first.

Portable commits retain the exact saved file trees and source baselines but compact away unrelated historical ancestry. Original commit IDs are recorded as provenance. Do not cherry-pick a whole portable snapshot into today's app: it deliberately restores the historical subject environment, including its older shared files. Integrate relevant reviewed changes onto current main in a separate branch after checking overlap.

Dependencies, generated caches and the shared `paper-trail-corpus` symlink are not embedded. Install dependencies and obtain the canonical SEC corpus using the repository's fetch scripts and the subject note. Subject-specific source files included in a snapshot are available after restoration. Accounting's source PDFs also remain in the shared local corpus. `local-tools.tar.gz` preserves eleven referenced `/private/tmp` authoring/browser helpers; `local-tools.json` records their original paths. Extract them to a new scratch directory and adapt absolute paths rather than overwriting arbitrary local files.

## Restore one subject

From a full clone of the latest main:

```sh
python3 scripts/restore-subject-checkpoint.py --list
python3 scripts/restore-subject-checkpoint.py --verify
python3 scripts/restore-subject-checkpoint.py --subject irish --destination ../nextstepuni-resume-irish
```

The restore command verifies every part, imports the selected snapshot and creates a new branch/worktree. It refuses to overwrite an existing directory. Temporary bundle assembly needs approximately the size recorded in `archive-manifest.json`, plus space for the restored files. The verification-only command does not change the app checkout.

On Alex's Mac, the original worktrees are still present and are the cheapest way to resume. Read the relevant handoff, check HEAD and `git status`, and preserve any newer edits. Restore the archive into a separate directory only when needed.

## Shared working rules

- Read `AGENTS.md`. Use the canonical curriculum registry and stable specification/topic IDs; never replace a subject taxonomy with a local array.
- Read every relevant paper and marking scheme visually. A generated count is not independent completeness evidence.
- One card represents an independently practicable task at a published mark boundary. Expand finite printed answer choices mechanically; preserve stems, diagrams, passages, tariffs and scheme criteria on each route.
- Preserve prior card IDs, student progress aliases, Atlas identities and valid source links. Keep drafts and unfinished reviews explicitly labelled.
- Follow each subject's generator, reconciliation and source-review ledgers. Do not replay one-off mutation scripts blindly; the notes identify known non-idempotent helpers.
- Run the required preservation, curriculum and deck tests plus the affected subject checks. Test source readers on desktop and phone after shared UI integration. Do not change a frozen baseline solely to silence a failure.
- Work on one subject at a time unless Alex explicitly authorizes parallel workers. Keep a small checkpoint after each validated paper and update the subject handoff when stopping.

## Prompt for the next coding terminal

```text
Continue NextStepUni Mark Bank / Topic Atlas work from the saved 8 October 2026 checkpoints in the latest main branch.

First read AGENTS.md and docs/subject-handoffs/2026-10-08/README.md, then the chosen subject's handoff and snapshot manifest. Ask me which subject to resume if I have not named one. Do not start all subjects or spawn parallel workers.

Inspect current main/release history before doing any integration: Accounting, Applied Maths, PE and Politics were locally complete at the pause and may already have been integrated since. For unfinished subjects, reuse the original worktree if it is available and has no conflicting newer work; otherwise use scripts/restore-subject-checkpoint.py to restore that subject into a NEW directory. Verify the saved commit/tree and preserve every existing edit.

Resume at the exact paper, level, language, question and source page recorded in the handoff. Follow its established review method, generators, ledgers and test/browser commands. Do not repeat finished audits, treat drafts as complete, blindly replay mutation scripts, reset another worktree, or merge an entire historical snapshot onto main. Preserve all card IDs, source material, mark allocations, finite answer routes and canonical topic mappings. Save a small validated checkpoint and update the resume note after each completed paper. Report the next action before continuing.
```
