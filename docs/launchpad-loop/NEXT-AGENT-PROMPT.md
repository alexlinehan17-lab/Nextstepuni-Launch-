# Next-Agent Kickoff Prompt — Subject Content Build

> Copy the block below and paste it to a fresh Claude Code session (web/phone or
> CLI) pointed at this repo, on branch `main`. It tells the agent to read the
> in-repo playbook and continue the subject-by-subject content build in both
> tools — Catch-Up Lane + Command-Word Reflex — figures and all, exactly the way
> previous sessions did it.
>
> **Phone-only note:** each cloud session starts from a fresh clone with no local
> `exam-papers/` (those PDFs are gitignored — local only). That's expected: the
> workflow re-downloads the subject's papers in step 1. Requires the environment's
> network policy to allow `examinations.ie` (set to **Full** on 2026-06-09).

---

```
You're continuing an established content-build pipeline in the Nextstepuni repo
(branch: main). Do NOT improvise the method — it's already documented in the repo.

STEP 1 — Read these in full before doing anything:
• docs/launchpad-loop/build-queue.md — especially the "▶▶ STANDING DIRECTIVE
  (2026-06-09)" block at the top, the per-subject "Done" log, and the
  SELF-CONTAINMENT, LEVEL-FILTER, and FIGURE-PIPELINE rules.
• docs/launchpad-loop/CHARTER.md — the loop policy.
• CLAUDE.md — the design system, citation discipline, and the Catch-Up Lane /
  Command-Word Reflex sections.

STEP 2 — Continue the standing directive: work through the most common Leaving
Cert subjects one at a time, building BOTH tools substantially for each. The next
subject is ACCOUNTING (SEC subject code 032, ~6,500 candidates; calculation-heavy
— final accounts, ratios, control accounts). After Accounting: Spanish, then Art
(Art History essays only).

For Accounting, follow the exact per-subject process the previous subjects used:
1. Download 5 years (2021–2025) of SEC exam papers + marking schemes, HL+OL, into
   exam-papers/accounting/ (gitignored). Resolve the real SEC file codes via the
   archive listing — don't guess; verify each file is a real PDF (HTTP 200 +
   application/pdf + sane size); never fabricate a paper. Network access is now
   "Full", so examinations.ie is reachable.
2. DUP-CHECK curriculum.ts for a pre-existing "accounting" subject (search the
   `"id": "accounting"` pattern) BEFORE adding anything; add/confirm accurate
   syllabus strands from the SEC syllabus.
3. Build Catch-Up Lane cards into catchUpLaneData.ts — both levels, grouped under
   real syllabus strands, with `focus` labels, and REAL screen-captured figures
   via tools/extract_exam_figure.py → public/exam-figures/accounting/ (committed)
   wherever a question is genuinely visual (layouts, ratio/data tables). Embed the
   data each question needs so it's self-contained.
4. Build Command-Word Reflex stems into commandWordData.ts — both levels, real
   cues, figure-attached where they fit.

HOLD THE DISCIPLINE the playbook insists on:
• Source every fact from the actual papers/marking schemes, NOT from memory.
  Keep verbatim quotes under the 15-word threshold.
• VIEW every figure crop you make. RECOMPUTE every numeric answer.
• Self-containment: every question must be answerable from what the card shows +
  general subject knowledge — never silently depend on an unseen paper.
• Adversarially verify with an independent skeptic agent; NEVER self-verify.
  (This caught 3 fabricated questions on earlier subjects — drop anything you
  can't ground.)
• Helper agents RETURN data; they must NOT edit the data files directly.
• SEC copyright is cleared — reproduce freely WITH "© State Examinations
  Commission" attribution; the only constraint is accuracy.

VERIFY + SHIP:
• Run the gate after integration: npm run typecheck (0 errors), npm run lint
  (0 warnings), npm test, npm run build — all must pass.
• Commit to main and push. Deploying is now AUTOMATIC — .github/workflows/
  deploy.yml deploys to Firebase Hosting (live) on every push to main, so do NOT
  run `firebase deploy` manually. After pushing, confirm the "Deploy to Firebase
  Hosting" GitHub Action goes green; it's then live at
  https://nextstepuni-app.web.app.
• Append a "Done" line to docs/launchpad-loop/build-queue.md with the subject,
  card/stem counts, figure list, and commit SHAs — same format as existing entries.

Work autonomously, pace it, and report per batch (download → Catch-Up Lane →
Command-Word Reflex). Pause only for irreversible/outward actions.
```
