# Contrast sweep — resume note

Last updated 21 August 2026. Everything below is committed and pushed to
`main` (last commit `494036af`); the working tree was clean.

## Where to pick up

**Onboarding stages 3-7 are still unswept**, and there is a suspected product
bug blocking the walk (below). Stages 1 and 2 are verified clean.

### Suspected product bug — worth investigating on its own merits

Clicking "Get Started" on onboarding stage 1 *sometimes* advances the stage
counter to "STAGE 2 OF 7" while leaving stage 1's content on screen and the
"Next" button disabled — a dead end. It mounted correctly on one attempt and
failed on several others with identical steps, so it looks like a race, not a
consistent state.

It is not explained by the arithmetic: `currentStage = activeSteps.indexOf(step) + 1`
with `activeSteps = [1, 2, 4, 5, 6, 7, 9]`, so "stage 2" implies `step === 2`,
and the `{step === 2 && ...}` block at Onboarding.tsx:689 is unconditional.
Stage counter and rendered content should not be able to disagree. Worth a
proper look — if a real student hits it, onboarding is unfinishable.

Note `useState<Step>(draft?.step ?? 1)` restores from a localStorage draft
(`nextstepuni:onboarding-draft:v1:<uid>:fresh`), which is written on mount.
Clear that key before testing or you resume mid-flow and chase ghosts.

### Do not complete the flow on the Demo Account

Walking to the end calls `handleOnboardingComplete`, which writes the profile
(year, subjects, North Star) to Firestore. Draft writes are localStorage-only
and safe; the final submit is not. There is also a pre-existing draft for uid
`YzNqGyCKXPN5WdrJrerjUBO6r0j1` at step 9 in localStorage — not mine, leave it.

### What static analysis already covers

Every light-surface literal across `Onboarding.tsx`, `SubjectOnboarding.tsx`
and `NorthStarOnboarding.tsx` was checked against the compat remaps: the two
inline hex literals are covered, and the 4 `bg-white` classes without a
`dark:bg` sibling are covered by the `!important` rule at index.css:355 now
that the onboarding root carries `theme-compat`. So the *surfaces* are handled
for all stages; what stages 3-7 could still hide is stage-specific text
literals, which is what a live walk would catch.

## Also outstanding

- **AdminDashboard** was opted into `theme-compat` but **never verified live** —
  reaching it needs staff credentials, which I won't enter. Three of its panels
  (`AdminFeedbackInbox`, `AdminFunnelPanel`, `AdminGcAccessPanel`) have light
  literals and zero `dark:` variants, so re-check them if you ever get a session
  with admin access.
- **Light-mode tools**: 4 findings left, all 4.37–4.49:1 (`#78716c` and
  `#766e67` on tinted cards) — inside the tolerance Alex accepted for the world
  CTAs. Left deliberately.
- **Immersive deck interiors** were spot-checked, not exhaustively walked.

## The browser harness

Rebuild it in the page after any reload (HMR wipes it). Full source is in the
session transcript; the shape is:

- `window.__SCAN()` — returns failing text nodes. **Composites translucent
  background layers outward.** An earlier version skipped them and read through
  to an opaque ancestor, which both hid real failures (a 12%-black badge over a
  blue chip) and invented false ones (an 80%-alpha dark toast over a light
  card). Do not regress this.
- `window.__goP({view, tool, mod}, waitMs)` — pushState + `popstate`, which
  `NavigationContext` listens to. Routes: `?view=module&mod=<id>`,
  `?view=innovation-zone&tool=<id>`, `?view=onboarding`.
- `window.__sweepMods(a, b)` — batched module sweep. Keep batches ≤ ~11 or the
  45s CDP limit kills the call.

Log in with the **Demo Account** button. Dark mode must be toggled with the
in-app "Dark Mode (Beta)" button — writing `localStorage` before login does not
stick, because login overwrites settings from the user profile.

Focus rings need **real keyboard focus** (`computer` tool, key `Tab`);
programmatic `.focus()` does not trigger `:focus-visible`, so it silently
measures nothing.

## Rules learned the hard way — do not relearn these

1. **Remap the fill and the ink together, or neither.** A general
   `:not([style*="background"])` guard on ink remaps was tried and reverted: it
   fixed the Journey chip but regressed 8 tools to dark-on-dark, because College
   Compass and Points Passport depend on both being remapped.
2. **`[style*="color: …"]` also matches `background-color: …`.** Anchor every
   inline colour matcher with `^=` or a leading `"; "`. This bug shipped three
   times. `test/darkModeTokens.test.ts` now fails the build on an unanchored one.
3. **Fill tone ≠ text tone.** Bitten repeatedly: `ColorWorld.deep`,
   `CYCLE_META.accent`, the brand orange, `--mb-label`. A colour that works as a
   background almost never works as text on that same background's neighbours.
4. **Overlays render outside `.product-shell`**, so the dark compat layer never
   reaches them. `theme-compat` on the root is the fix; `ModalFrame` covers four
   consumers at once.
5. **Tint an overlay away from its ink, never toward it.**
6. Verify by **re-sweeping**, not by reading the diff — the nested blue-600
   badge regression was invisible in review and obvious in a scan.

## Current verified state (dark unless noted)

| Surface | Result |
|---|---|
| 16 shipping Innovation Zone tools | 0 failures (1 was left, then fixed by deepening the deck bands) |
| 83 modules | 0 |
| Base views | 0 |
| Modals / overlays / legal | 0 |
| Mobile 500px: views, tools, 27 modules | 0 |
| Focus rings, both themes | 6.78 dark / 4.99 light |
| Light-mode tools | 4 left, all 4.37–4.49 (accepted) |
| Onboarding stages 1–2 | 0 |
| Onboarding stages 3–7 | **unswept — resume here**, blocked by the bug above |
| Admin Dashboard | fix applied, unverified |

The six Workshop/WIP tools (`diagram-vault`, `answer-architect`,
`definition-drill`, `oral-trainer`, `examiners-chair`, `coursework-companion`)
are out of scope — Alex said not to bother with them.
