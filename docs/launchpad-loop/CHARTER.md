# Launchpad Improvement Loop — Charter

> The "prompt", designed once. This file is the policy a coding agent runs each
> iteration so the human edits the *loop*, not individual prompts.

## Purpose

Continuously deepen the **Launchpad** (ex–Innovation Zone) tools in both
**content** and **functionality**, grounded in **science-backed research**,
expanding each toward something that could stand on its own as an app.

## Scope — the 16 student-facing tools

Career/future: `future-finder-revamped`, `future-finder` (legacy), `career-paths`
(Exploring Options), `your-possible-life`. Aspiration/belonging: `how-they-did-it`,
`college-compass`. Study planning: `planner`, `war-room`, `comeback`, `catch-up-lane`.
Exam technique: `exam-reps`, `syllabus-xray`, `command-word-reflex`. Motivation:
`points-passport`, `cao-simulator`, `journey`.

All registered in `components/InnovationZone.tsx` (`tools` array + `TOOL_CHROME`).

## Each iteration

1. **DISCOVER** — read the target tool's code + data; assess content depth (1–5),
   functionality depth (1–5), thin/static spots, strengths.
2. **RESEARCH** — gather science-backed evidence for the domain (web-cited, real
   sources, skeptical about mixed evidence).
3. **IDEATE** — expansion concepts: content + functionality, each grounded in a
   cited claim, honouring the design system, inclusive for DEIS students.
4. **VET** — an independent skeptic hardens the scoring rubric (evidence &
   impact weighted over novelty).
5. **SCORE** — adversarial scoring; cited science is verified, feature-bloat is cut.
6. **SYNTHESIZE** — ranked build queue + completeness critic (missed tools/angles,
   weakest evidence).
7. **BUILD** (later iterations) — pop the top queue item, build it end-to-end,
   author content from primary sources, source-ground every claim.
8. **VERIFY** — run the gate; never self-verify (independent skeptics refute).
9. **COMMIT** — straight to `main`. **RECORD** the outcome in `build-queue.md`.

## Guardrails (set by the user, 2026-06-07)

- **Autonomy:** autonomous; commit straight to `main`.
- **Pause only for:** irreversible / outward-facing actions — `firebase deploy`,
  sending email, anything destructive or that publishes to real students.
- **Why commit-to-main is safe:** deployment is **manual** (`firebase deploy
  --only hosting`). Nothing reaches real students until the user deploys — so the
  deploy step *is* the human sign-off gate, consistent with "plan tools first".

## The gate (non-negotiable, every build iteration)

`npm run lint:ci` → `npm run typecheck` (real type gate, 0 errors) → `npm test`
→ `npm run build`. Verify behaviour with the app, not just green CI. A skeptic
vets findings; a completeness critic closes each cycle.

## Design constraints (hard)

Follow `CLAUDE.md` "Visual Design System" + project memory:
accent orange `#F26B1F` = action, success green `#3A8D5F` = correct (never orange
for "good"); **no** coloured left borders; **no** warm cream in module surfaces;
bold colour-as-environment, not tints; white cards, 2px `#1a1a1a` border, serif
titles; **mistake-first** pedagogy (lead with the wrong answer + visualise the
mark-loss); animation encodes meaning. Immersive decks share
`components/immersiveDeck/` HybridCard primitives (white header + pastel blob,
no saturated band, no emoji). **DEIS audience:** frame around autonomy,
incremental progress, belonging — never exclusionary high-achievement copy.

## Stop conditions

Stop and surface to the user when: the build queue is empty; the gate fails twice
on the same item and can't be fixed cleanly; a concept needs a product/ethics call
(e.g. minors' data, real student outcomes); or an irreversible/outward action is
required.

## Working memory

`build-queue.md` — the prioritized queue + per-item status log. The loop reads it
at the start of each iteration and updates it at the end. `design-dossier.md` —
the research + concept evidence base (regenerated when the loop re-runs discovery).
