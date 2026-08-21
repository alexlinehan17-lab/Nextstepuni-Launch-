# Contrast sweep — resume note

Paused 21 August 2026. Everything below is committed and pushed to `main`
(last commit `742e2587`); the working tree was clean at the pause.

## Where to pick up

**One known failure is still open**, in onboarding stage 1 (`?view=onboarding`),
dark mode: 4 instances of `#d6d0c9` on `#dcdcdb` at **1.11:1** — the
"Your North Star" / "Your Subjects" / "Grade Targets" / "Exam Countdown" chips.

Cause, already traced: the chip carries inline
`background-color: rgba(255, 255, 255, 0.85)`. No background remap matches a
*translucent* white, so the fill stayed light while an ink remap turned its text
light. This is the recurring **"remap the ink but not the fill"** bug.

Fix in flight: add a dark compat background remap for
`rgba(255, 255, 255, 0.85)` so the fill darkens alongside its ink, next to the
other surface remaps in `index.css`. Then re-scan `?view=onboarding` — it should
go 4 → 0.

## Then: onboarding stages 2–7 are unswept

Stage 1 is the only one measured. The flow is 7 stages; walk through them and
scan each. Reachable directly at `?view=onboarding` while logged in as Demo
Account — no account creation needed.

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
| Onboarding stage 1 | **4 left — resume here** |
| Onboarding stages 2–7 | unswept |
| Admin Dashboard | fix applied, unverified |

The six Workshop/WIP tools (`diagram-vault`, `answer-architect`,
`definition-drill`, `oral-trainer`, `examiners-chair`, `coursework-companion`)
are out of scope — Alex said not to bother with them.
