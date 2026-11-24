# Motion — Nextstepuni

The character we are after is Kobra's: **precise, fast-decelerating, connected.** Things travel,
draw and settle. Nothing bounces for fun, nothing fades in from nowhere. Sources and exact values:
`research/design-skills-and-kobra.md` (§1 emilkowalski/skills, §2.6 Kobra motion).

## 1. Decide whether to animate at all

| How often the student sees it | Animate? |
|---|---|
| 100+ times a day, or triggered from the keyboard (typing, tab switching by key, list arrowing) | **No.** |
| Tens of times a day (hover, moving through a list, answering a question) | Remove or reduce to a 120–150ms state change |
| Occasionally (sheets, toasts, picking a subject, starting a session) | Standard, per the tables below |
| Rare / first time (onboarding, a milestone, session complete) | May delight — one moment, not five |

Test: imagine the 50th time today. If it would annoy, cut it.

## 2. Tokens

```css
--ease-out:    cubic-bezier(0.23, 1, 0.32, 1);     /* enter, exit, most things */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* moving something already on screen */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* sheets, page slides, width changes */
--dur-press: 120ms;  --dur-state: 150ms;  --dur-enter: 220ms;
--dur-page: 320ms;   --dur-sheet: 400ms;  /* 500ms hard ceiling */
```

These already exist in the Kobra runtime (`--ease-out`, `--ease-in-out`) and in the sidebar /
login code (`[0.32,0.72,0,1]`, `[.22,1,.36,1]`, `[.16,1,.3,1]`). Use the three above for new work;
the two near-duplicates are acceptable where they already are.

- Never `ease-in` (feels sluggish at the start). `linear` only for constant motion (progress, hold-to-confirm).
- Hover/colour changes: plain `ease`, 150ms.
- Framer springs: `{ type: 'spring', duration: 0.35, bounce: 0 }`. Bounce 0 by default; up to 0.2
  only after a real gesture with momentum (drag release).

## 3. Durations and shapes

| Thing | Enter | Exit | From |
|---|---|---|---|
| Press feedback | 120 | 160 | `scale(0.97)` (icon buttons 0.96); starts on pointer-down |
| Toggle, checkbox, chip select | 150 | 150 | colour + the mark drawing |
| Tooltip / small popover | 150–200 | 120 | `scale(0.96)` + opacity, origin at the trigger |
| Menu / dropdown | 200 | 150 | `scale(0.95)` + opacity + 4px, origin at the trigger |
| Dialog (iPad/desktop) | 250 | 200 | `scale(0.96)` + opacity, centred |
| Bottom sheet | 400 | 300 | `translateY(100%)`, `--ease-drawer`; scrim fades 200 |
| Page push / pop | 320 | 320 | x ±20px + opacity (login's pattern), direction = depth |
| Toast | 300 | 200 | from the edge it lives on |
| List / section first appearance | 220 each | — | `translateY(8px)` + opacity, stagger 30–50ms, total < 300ms, once |

Rules:
- **Exit is faster than enter**, leaves the way it came, all at once (no reverse stagger).
- **Nothing scales from 0.** Smallest start is 0.95.
- **Only `transform` and `opacity`.** Never `transition: all`. Never animate height/top/left when a
  transform will do (layout animation via Framer `layout` is fine for small things).
- **Interruptible.** Anything a student can trigger twice quickly uses transitions or springs, not
  keyframes that must finish.
- Hover never moves the element itself. Hover is a fill or shadow change, behind `@media (hover: hover)`.
- If a crossfade between two texts looks muddy, add `filter: blur(2px)` at the midpoint (Kobra's text swap).
- Feedback begins within 100ms of the touch, even if the result takes longer.

## 4. The Nextstepuni vocabulary

Use these named moves so the same event always looks the same.

| Name | When | How |
|---|---|---|
| **Slide highlight** | The active tab, segment, nav item, selected step changes | One highlight element with a shared `layoutId`; spring 0.35s, bounce 0. The highlight travels; it does not fade out and in. |
| **Mark draw** | Something becomes selected or correct | Ring/border colour 120ms, then the tick's stroke draws (`pathLength 0 → 1`) 220ms `--ease-out`, starting ~60ms after the fill. Deselect is a 120ms fade — no un-draw on high-frequency lists. |
| **Selection dot** | A radio-style answer is chosen (Future Finder) | The orange dot grows from `scale(0.4)` to 1 in 180ms `--ease-out` while the ring colour changes; the row's tint wipes in 150ms. No overshoot. When advancing automatically, hold 220ms after the mark completes so the student sees their choice land. |
| **Numeral roll** | A count changes (points, timer minute, streak) | Old digit rises 4px and blurs 1.5px out, new one rises in; 260ms, 40ms stagger per digit. `tabular-nums` so nothing shifts. Never on a seconds counter. |
| **Attention ring** | A required control is missing (not-ready CTA tapped) | Scroll into view (smooth, ≤ 400ms), then one 1.5px orange ring expands 0 → 4px offset and fades, 400ms. Once. Plus a warning haptic. |
| **Reject shake** | Wrong / invalid | 6px horizontal, ~280ms, decaying. Plus the reason in words. |
| **Sheet rise** | A sheet opens | From the bottom, 400ms `--ease-drawer`; drags follow the finger 1:1; release settles with a spring. |
| **Moment** | Session complete, milestone, welcome | The one place for a larger, staged sequence (≤ 1.2s total) and a character. Skippable by tap. |

## 5. Reduced motion and haptics

- `@media (prefers-reduced-motion: reduce)`: keep opacity changes, remove translate/scale/draw/roll;
  sheets fade. Check every new animation.
- Haptics via Capacitor Haptics, in the same frame as the visual: selection tick on a choice,
  success on completion, warning on a not-ready tap. One per action. Never the only feedback.
- Sound follows the same rule and the existing Kobra `SoundEffects` layer: short, quiet, optional.
