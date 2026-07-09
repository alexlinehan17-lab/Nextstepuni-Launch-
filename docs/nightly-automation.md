# Nightly automation — the honest way to run unattended work

> **Why this is a doc and not a live workflow.** GitHub blocks OAuth tokens
> without `workflow` scope from creating/updating `.github/workflows/*.yml`, and
> the session token used to build this lacks that scope. So the two workflows
> below are ready to paste — add them yourself (Settings has the scope, or just
> commit the files from your own machine) and they go live.

There are two separate things people mean by "run it overnight." They have very
different risk profiles — pick deliberately.

---

## 1. Nightly guardrail (safe, recommended, no secrets)

Push/PR CI only fires when someone changes code. This runs the **same gate
suite** on a schedule, so time- or dependency-driven breakage (a transitive bump,
a date-sensitive test, external data drift) is caught on a quiet day. It is
read-only: no secrets, pushes nothing, just goes red in the Actions tab.

Create `.github/workflows/nightly-guardrail.yml`:

```yaml
name: Nightly guardrail

on:
  schedule:
    - cron: '0 3 * * *' # 03:00 UTC nightly
  workflow_dispatch: {}

permissions:
  contents: read

jobs:
  gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - name: Lint (strict)
        run: npm run lint
      - name: Type check
        run: npm run typecheck
      - name: Test
        run: npm test
      - name: Topic Vault crop contracts
        run: npx vitest run test/vaultAnchors.test.ts test/paperRegion.test.ts test/vaultTopics.test.ts
      - name: Build
        run: npm run build
        env:
          GEMINI_API_KEY: 'dummy-key-for-ci'
```

That is the whole thing. Turn it on and forget it.

---

## 2. Autonomous agent nightly (powerful, higher risk — read before enabling)

This runs Claude Code headless on a schedule to *do work* — the "keep refining
the tool overnight" idea. **It is genuinely risky and must never push to `main`
unattended.** The safe pattern, baked into the template below:

- It runs on a **branch** and opens a **pull request** — a human reviews before
  anything reaches `main` / the live app (remember: push to `main` = deploy live).
- It is scoped by an explicit prompt to a **safe lane** (tests, docs, UX polish
  on the Topic Vault) and told **never to generate new answer-map crops** — a
  wrong crop shown to a student is the worst failure, and crop generation needs
  render-QA that a headless run can't do safely.
- It needs an `ANTHROPIC_API_KEY` repo secret. Token spend is real and unbounded
  per run — set a conservative model/turn cap.

> **My honest recommendation:** run **#1** always, and only enable **#2** if you
> want to review a PR most mornings. An agent that both writes code *and* merges
> it with no human in the loop is not something I'd point at a live student app.
> The overnight "loop" that failed before failed precisely because unattended
> autonomy in an ephemeral container isn't a thing — this PR-based CI is.

Create `.github/workflows/nightly-agent.yml` (requires the `ANTHROPIC_API_KEY`
secret; pin the action to a released version you've reviewed):

```yaml
name: Nightly vault agent (PR-only)

on:
  schedule:
    - cron: '0 4 * * *' # 04:00 UTC, after the guardrail
  workflow_dispatch: {}

permissions:
  contents: write        # to push the working branch
  pull-requests: write   # to open the PR
  # NOTE: deliberately NOT granting anything that can merge or deploy.

jobs:
  refine:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci

      # Use the official Claude Code action (review its source + pin a tag first).
      - name: Run the vault-quality agent
        uses: anthropics/claude-code-action@v1   # pin to a reviewed release
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Safe lane only — NO crop generation, NO push to main.
          prompt: |
            Make ONE small, genuinely valuable, verified improvement to the
            Topic Vault (components/PaperTrail/): a UX polish, an edge-case fix,
            or a unit/smoke test. Run typecheck + lint (--max-warnings 0) + build
            + vitest and only keep the change if all pass. Do NOT generate or edit
            answer-map crops/sidecars (scripts/paper-trail/, public/paper-anchors/).
            Do NOT push to main. Read CONVENTIONS.md §8 (Topic Vault row) first.

      # Open a PR from whatever the agent committed on its branch.
      - name: Open a review PR
        run: |
          git switch -c "nightly-vault/$(date -u +%Y%m%d)" || true
          git push -u origin HEAD || exit 0
          gh pr create --fill --base main --label automated --draft || true
        env:
          GH_TOKEN: ${{ github.token }}
```

Adjust the runner step to whatever agent runner you actually trust; the load-
bearing safety is the two rules — **PR not push, and no crop generation.**

---

## Verify

- Guardrail: open **Actions → Nightly guardrail → Run workflow**; it should go
  green in a few minutes and re-run nightly.
- Agent (if enabled): the morning after, look for a **draft PR** labelled
  `automated`. Review the diff, run it locally, merge if it's good, close if not.
