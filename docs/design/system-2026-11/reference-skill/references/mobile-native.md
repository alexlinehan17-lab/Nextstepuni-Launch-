# Native feel on iPhone and iPad — Nextstepuni

The app is a React SPA inside Capacitor. It will feel like a website in a shell unless these hold.
Sourced detail (Apple HIG, WCAG 2.2, WebKit, Capacitor, NN/g), with what could not be verified:
`research/mobile-ios-practice.md` (§14 there is the full 32-row tell list).

## 1. Safe areas

Setup that already exists: `viewport-fit=cover` (`index.html`), `--sat/--sar/--sab/--sal` from
`env(safe-area-inset-*)`, Capacitor `ios.contentInset: 'never'` and `StatusBar.overlaysWebView:
true` — so **CSS owns every inset**. Current iPhones: ~59–68pt top, 34pt bottom in portrait. Read
them from the variables; never hardcode.

The rule: **three primitives own the top inset, nothing else touches the top edge.**

| Primitive | Where the inset goes |
|---|---|
| App bar (`PageHeader`) | `padding-top: max(8px, var(--sat))` |
| Layer frame (`ModalFrame`: sheets, dialogs, viewers, intros) | Phones: bottom-anchored, `max-height: calc(100dvh - var(--sat) - 12px)`, footer `padding-bottom: max(16px, var(--sab))`. Full-screen covers get an app bar. |
| Immersive frame (study room, pause, breathing, review, quiz) | One wrapper with `padding: max(16px, var(--sat)) max(20px, var(--sar)) max(16px, var(--sab)) max(20px, var(--sal))`; its header row holds *all* top controls (Leave, sound, minimise) in normal flow |

- A control positioned `absolute/fixed` at `top: 16px; right: 20px` is the bug behind the Admin
  log-out, the pause-screen sound toggle and the Island Mode close. Controls go **in the header
  row's flow**, which sits below the inset by construction.
- `native-ios.css` per-class patches are a symptom; new screens must not need an entry there.
- Guard: a test greps for `fixed|sticky|absolute` + `top-` / `top:` outside the three primitives
  (ratchet the existing count down; never up).
- Bottom: tab bar, sticky CTAs, toasts and docks add `var(--sab)`. Scroll content ends with
  padding = chrome height + `var(--sab)` + 32.
- Landscape and iPad: also respect `--sal/--sar`.

## 2. Reach and targets

- 44×44 minimum hit area, 8 between targets. Visual size may be smaller; the hit area may not.
- Bottom half = primary action, frequent controls, pickers (sheets). Top corners = Back and rare
  actions. Nothing frequent in the top-right.
- Inputs ≥ 16px font. Use the right `inputmode`/`autocomplete`. Keep the focused field above the
  keyboard (Capacitor Keyboard events).

## 3. Presentation on phones

- Pickers, filters, intros, details → **bottom sheets** with a grabber, swipe-to-dismiss, and the
  current value ticked. Not centred cards, not a desktop popover under a button.
- Long or multi-step → full-screen cover with an app bar.
- Destructive confirm → action sheet from the bottom.
- One layer at a time.
- A select-style control must work on touch: do not rely on `blur` to close a custom listbox (iOS
  does not focus buttons on tap, so `relatedTarget` is null and the menu unmounts before the option's
  click — the My Progress section-picker bug). Close on outside pointer-down instead, or use the
  shared sheet/select.

## 4. Long pages: change the architecture, not the paint

A phone screen that runs past ~3 viewport heights needs restructuring. In order of preference:

1. **Search first** when the student usually knows what they want (a topic, a paper).
2. **Segmented control** for 2–4 parallel views of the same thing (level, paper, state).
3. **Drill-down** — one level per screen: Subject → Strand → Topic → Session. Each list fits in
   ~2 screens; rows show counts and progress so the student can choose without opening.
4. **Recents / continue** at the top so the common case is one tap.
5. **Collapsed sections with counts** when the student needs only a few of many groups.
6. **Detail on its own screen** rather than expanded inline.
7. Filters as chips in one scrolling row; a sheet for anything more.

Lists (rows + hairlines in one group) beat cards for many similar items. Virtualise lists over ~50.
Progressive disclosure goes two levels deep at most.

## 5. The tells — and the fix

| Tell | Fix |
|---|---|
| Control under the Dynamic Island / status bar | §1 primitives |
| `100vh` layouts that jump or hide the footer | `100dvh` |
| Primary action top-right | Sticky bottom CTA |
| Hover-only affordances, no pressed state | `@media (hover: hover)`; pressed state on everything |
| Small targets, text links as navigation | 44px; rows and buttons |
| Desktop dropdown under a trigger | Bottom sheet list |
| Centred floating modal with a corner ✕ | Bottom sheet |
| Wide table with horizontal scroll | Row list + detail screen |
| Fixed-column grids (`grid-cols-3` of stats) | 2-up or a stacked list at 390px |
| Two/three ways back, breadcrumb + back | One Back |
| Banner/hero above every tool | App bar identity only |
| Whole page rubber-bands; nested scroll traps | `overscroll-behavior` none on root, contain inside |
| Text selects / grey tap flash on buttons | `user-select: none`, transparent tap highlight on controls |
| Input zooms on focus | ≥ 16px |
| Spinner on a blank page | Skeleton of the real layout |
| Same layout stretched to iPad | Sidebar + two-pane at ≥ 768 |
| Bars and docks that don't match each other | One tab bar; contextual toolbar from the same tokens |
| Instant, unanimated state changes — or bouncy ones | `motion.md` |

## 6. iPad

Lay out by width, not device: ≥ 768 gets the sidebar, 24px gutters, two columns or list + detail.
Dialogs and popovers replace sheets. Pointer hover is an addition, never a requirement. Viewer
side panels and any `fixed top-0` element still respect `--sat`.
