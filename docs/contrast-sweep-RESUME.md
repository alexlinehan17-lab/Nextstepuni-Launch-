# Contrast sweep — resume note

Last updated 22 August 2026. Everything below is committed and pushed to `main`.

## Where to pick up

**Onboarding is now swept and clean** — all ten internal steps, both themes.
What is left is the Admin Dashboard, which needs staff credentials.

### How onboarding was reached without driving the flow

The walk was the blocker: the tab is hidden under automation, so framer-motion
never settles and clicking through is unreliable — and completing the flow on
the Demo Account writes its profile to Firestore, which must not happen.

Neither is necessary. Onboarding restores itself from a localStorage draft:

    nextstepuni:onboarding-draft:v1:<uid>:<mode>      uid "demo-student", mode "fresh"

Seed that key with `{version:1, step:N, ...}` and remount the view (push
`?view=home`, then `?view=onboarding`) and step N renders directly, with no
clicking and no submit. Ten steps, two themes, in two calls. Remove the key
afterwards. There are ten internal steps behind the seven the counter shows.

### What that found, and what was fixed

Four failures, all in dark:

- `#8A8178` on the exam-date card, 4.26:1 on a 10px bold label ("Exam date",
  "days", "to go"). The literal had a LIGHT remap and no dark one, so the card
  under it was remapped to #202020 while the ink kept its authored grey — rule 1
  below, in the one direction the rule did not already cover. Dark remap added.
- "Projected Gain" at `rgba(var(--accent),0.7)`, which composites to 3.27:1.
  Now the full accent, which is 5.35:1 there and matches the number it labels.

### The scanner must skip disabled controls

Light step 6 reported 21 failures at 1.7:1 — every grade button below your
current grade, which onboarding disables because it cannot be a target. SC 1.4.3
exempts an inactive user interface component. Without the skip, those 21 bury
every real finding under the same noise on every future sweep.

### The "stage counter desync" was MY automation, not a bug — corrected

An earlier version of this note reported a suspected product bug: clicking
"Get Started" advanced the counter to "STAGE 2 OF 7" while stage 1's content
stayed on screen. **That was wrong.** The same symptom then appeared in Your
Possible Life ("02 / 05" with stage 01 content), a completely unrelated
component, and `document.visibilityState` was `"hidden"` with
`document.hasFocus() === false` throughout.

A hidden tab throttles `requestAnimationFrame`, so framer-motion never
progresses and `AnimatePresence` never completes the swap: the old content
stays mounted and the new content sits at `opacity: 0`. Nothing is wrong with
the onboarding state machine. Do not go hunting for it.

Two consequences for anyone resuming:

- **Colour measurements need `__forceSettled`** (inject
  `*{opacity:1 !important;transform:none !important}` around the scan).
  Without it, animated content reads as `opacity: 0` and is skipped entirely —
  which is why the first sweeps missed everything behind an animation.
- **Multi-stage walks are unreliable while the tab is hidden.** Bring the tab
  to the foreground before driving a flow that animates between steps — or
  better, do not drive the flow at all: seed its saved draft and remount, as
  onboarding was swept above.

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

- `window.__forceSettled(true/false)` — injects
  `*{opacity:1 !important;transform:none !important}`. **Wrap every scan in
  this.** A hidden tab throttles rAF, so framer-motion never settles and
  animated content sits at `opacity: 0`, where the scanner skips it. This blind
  spot is what hid the Catch-Up Lane, Mark Bank, Planner and Command Word
  Reflex failures through several "clean" sweeps.
- `window.__drill(tool, depth)` — clicks the largest non-nav control repeatedly
  to walk a tool inwards. Entry-screen scans are NOT sufficient; every failure
  found on 21 Aug was at least one interaction deep.
- `window.__SCAN()` — returns failing text nodes. **Composites translucent
  background layers outward.** An earlier version skipped them and read through
  to an opaque ancestor, which both hid real failures (a 12%-black badge over a
  blue chip) and invented false ones (an 80%-alpha dark toast over a light
  card). Do not regress this. It must also **skip anything inside a `disabled`
  or `aria-disabled` control** — SC 1.4.3 exempts an inactive component, and
  onboarding alone has 21 of them.
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
| 16 tools drilled 3–4 levels deep (not just entry) | 0 |
| Onboarding, all 10 internal steps, dark | 0 (was 4) |
| Onboarding, all 10 internal steps, light | 0 |
| Admin Dashboard | fix applied, **unverified — resume here**; needs staff credentials |

The six Workshop/WIP tools (`diagram-vault`, `answer-architect`,
`definition-drill`, `oral-trainer`, `examiners-chair`, `coursework-companion`)
are out of scope — Alex said not to bother with them.
