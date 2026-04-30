# Gemini Integration Audit

NextStepUni Learning Lab — independent verification of the AI integration claim

Document status: AUDIT FINDING for legal review
Prepared by: NextStepUni Ltd
Date: 2026-04-29

---

## Conclusion

**(b), with nuance.** No live Google Gemini integration is present in the
deployed codebase. Historical commits show that Gemini-related *configuration
plumbing* — the bundling of a `GEMINI_API_KEY` environment variable into the
client JavaScript via `vite.config.ts` — existed from the initial commit and
was removed in commit `063d574` on 2026-04-06. **No actual Gemini SDK code
(`GoogleGenerativeAI`, `@google/genai`, `generateContent`, or any HTTP call to
`generativelanguage.googleapis.com`) has ever been present in this
repository's git history.**

The mentions of `GEMINI_API_KEY` in `README.md:18` and `CLAUDE.md:22` are
residue from the original Google AI Studio scaffold (`README.md:5` still
reads "Run and deploy your AI Studio app", and `README.md:9` links to the AI
Studio app dashboard). The scaffold pre-wired environment-variable plumbing
intended to support a future Gemini integration that was never actually
built.

This is documentation drift. README.md and CLAUDE.md tell developers to set
a key that, today, is not consumed by any code path.

---

## What was searched

### Source code

```
grep -ri "gemini\|generativeai\|@google/generative-ai\|@google/genai\|GoogleGenerativeAI\|GoogleGenAI\|generateContent" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.md" --include="*.example" .
```

Hits, excluding `node_modules`, `dist` and `compliance/`:

- `README.md:18` — instructional text "Set the `GEMINI_API_KEY`…"
- `CLAUDE.md:22` — instructional text "Requires `GEMINI_API_KEY`…"

No code matches. No SDK matches. No matches in `package.json` or
`package-lock.json`.

### Git history

```
git log --all --pretty=format:"%h %ad %s" --date=short -S "GoogleGenerativeAI"
git log --all --pretty=format:"%h %ad %s" --date=short -S "@google/genai"
git log --all --pretty=format:"%h %ad %s" --date=short -S "generateContent"
git log --all --pretty=format:"%h %ad %s" --date=short -S "generativelanguage.googleapis.com"
```

All four searches: **zero hits**. The Gemini SDK has never been imported in
this repository's history.

```
git log --all --pretty=format:"%h %ad %s" --date=short -S "GEMINI_API_KEY"
git log --all --pretty=format:"%h %ad %s" --date=short -S "process.env.API_KEY"
```

Hits:

- `fc3db43` 2026-02-07 — `feat: Initialize Nextstepuni app structure`. The
  initial scaffold added the `define:` block in `vite.config.ts` exposing
  `GEMINI_API_KEY` and `API_KEY` to the client bundle, plus the
  `README.md:18` line.
- `73d2f5f` 2026-02-08 — `fix: Add missing entry script tag and project
  setup files`. Touched related setup files; the env var plumbing was
  unchanged.
- `fd47d36` 2026-04-03 — `Major platform update: routing, Tailwind build,
  UI enhancements, War Room & Innovation Zone refactors`. Mentions of the
  API key configuration touched.
- `063d574` 2026-04-06 — `Complete visual overhaul + security fixes +
  module showcase redesign`. **The vite.config.ts `define:` block was
  removed in this commit** with the explicit changelog entry "Gemini API
  key leak removed from vite.config".

### Dependencies

```
grep -i "generative\|gemini\|genai\|anthropic\|openai" package.json package-lock.json
```

Zero hits in `package.json`. Zero hits in `package-lock.json`. There is no
LLM SDK declared as a dependency, nor any transitive dependency on one.

### Environment templates

There is no `.env.example` in the repository (`ls .env*` returns only the
gitignored `.env`). The current `.env` file is not committed to the
repository. **TBC — Alex to confirm** whether `.env` currently still holds a
`GEMINI_API_KEY` value and whether that key has been rotated or revoked
since the leak removal in commit `063d574`. If a key is still present in the
local `.env` it carries no exposure risk by itself (it is not bundled), but
operationally it should be rotated as a matter of hygiene.

### Module content

The `a75a4d7` commit (2026-04-03, "Rewrite all 52 modules in plain English
for Leaving Cert students") includes a changelog note "Academic language
from AI-generated content (Google Gemini + research papers)". This refers
to a *one-off use of Gemini outside the application* by Alex during content
authoring; the resulting text was hand-edited and pasted into module source
files. Nothing about that workflow installed or invoked Gemini from inside
the application's runtime. **No Article 22 / Annex III implication** —
Gemini was an authoring tool used by a human editor, not an automated
decision system operating on student data.

---

## Implications for the AI Governance Schedule

`compliance/AI_GOVERNANCE_SCHEDULE.md` Section 1 already documented "no live
Gemini integration in the current bundle". This audit confirms that headline
finding and refines it:

1. The AI Governance Schedule's claim that Gemini is "not implemented" is
   correct as of commit `0ac6be4`.
2. The claim that the README/CLAUDE references are "documentation drift
   from a previous iteration" is correct: they predate any decision to
   actually wire up the model and they survived the security cleanup of
   `063d574`.
3. The Schedule's forward-looking Section 6 (governance requirements
   *if* Gemini is reactivated) remains relevant; it does not need to be
   pulled.
4. The Schedule should be updated to (a) reference this audit explicitly,
   and (b) note that prior leaked-in-bundle configuration was remediated
   on 2026-04-06.

These updates are made in the same commit as this audit.

---

## Implications for README.md and CLAUDE.md

Per the Phase 1 spec, conclusion (b) requires: "remove all references to
GEMINI_API_KEY, Gemini setup, and AI features from README.md and CLAUDE.md.
Replace with a brief 'AI features: none currently active. Future GenAI
integration would require an updated AI Governance Schedule per
/compliance/.'"

This change is applied alongside this audit.

The README.md banner image and the line "Run and deploy your AI Studio app"
are vestigial AI Studio scaffold artefacts. They will also be removed: a
public-facing README that says "AI Studio app" while no AI feature is active
is misleading and would attract questions during external review.

---

## Reviewer note

This audit corrects a finding from the prior compliance documentation
session, which reported "no GenAI code present, no GenAI dependency
installed, no historical GenAI commits". The first two parts of that earlier
finding were correct. The third part — "no historical GenAI commits" — was
incorrect: the vite.config.ts `define:` block exposing `GEMINI_API_KEY` was
present in history, and a security commit explicitly removed it. The earlier
session's grep was scoped only to the working tree and did not include
`git log -S`, which is why the historical leak remediation was missed.

The substantive position for PwC has not changed (no live AI integration
today), but the more accurate factual record is more defensible: a
vulnerability *was* identified and fixed in the codebase's normal security
hygiene process, which is itself evidence of a working vulnerability
management practice.

---

## Document control

- Source code reviewed: working tree at commit `0ac6be4`; git history searched
  across all branches.
- Verification commands above are reproducible.
- Companion documents: `DPIA.md` (R5 unchanged; remains "negligible today,
  high if reactivated"), `AI_GOVERNANCE_SCHEDULE.md` (updated alongside this
  audit), `REMEDIATION_LOG.md` (no entry — this audit is a finding, not a
  remediation; the historical remediation in `063d574` is part of the
  baseline state of the codebase and is recorded here for the record).
