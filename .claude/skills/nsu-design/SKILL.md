---
name: nsu-design
description: The Nextstepuni product-design system — one design language for iPhone, iPad and desktop. Use BEFORE any UI, UX, layout, styling, navigation, motion, dark-mode or "make this look/feel better" work on the app or site, and when reviewing or auditing a screen. Defines spacing, type, colour and dark tokens, radius, cards, buttons, Back/Close/Cancel/Exit, navigation, sheets, dropdowns, states, touch targets, safe areas, icons, characters, motion, and how mobile differs from desktop.
---

# nsu-design — the Nextstepuni design system

**Status: v1, November 2026. Direction "Paper & Ink" is the recommended default and is NOT yet
approved by the owner.** Sections marked ⚑ depend on that choice (see `public/design/` — live at nextstepuni.com/design — and `docs/design/system-2026-11/AUDIT.md`
for the three directions shown to the owner). Everything unmarked holds whichever direction wins.
When the owner decides, update this file and CLAUDE.md's "Visual Design System" section in the same change.

Read this file fully before touching UI. Then read the reference you need:

| Doing | Read |
|---|---|
| Any animation, transition, press state, gesture | `references/motion.md` |
| Anything on iPhone/iPad: safe areas, sheets, pickers, native feel | `references/mobile-native.md` |
| Headers, back buttons, modals, tab bar, sidebar | `references/navigation.md` |
| Where the rules came from / checking a claim | `references/sources.md` |

## 0. How to work

1. **System first, screen second.** Never fix a screen with a one-off. If the fix needs a value,
   component or behaviour the system lacks, add it to the system (token / shared primitive / this
   file), then use it. A fix that only one screen can use is a new inconsistency.
2. **Reuse before you build.** The shared primitives already exist — `components/ui/`
   (`ActionButton`, `BackButton`, `PageHeader`, `ModalFrame`, `FormControls`, `SystemState`,
   `HorizontalTabs`, `controls.css`) and the Kobra kit (`components/approved-ui-runtime`,
   `kobra-navigation-runtime`). Grep for an existing one before writing markup.
3. **Design the phone screen as a phone screen.** Not the desktop layout made narrower. Ask: what
   is the one task here, where does the thumb go, what can be a second screen instead of more scroll?
4. **Run the self-check in §14 before saying it's done**, and `/verify`.

## 1. What makes it ours

Good UI is not the goal; *recognisably Nextstepuni* is. These eight signatures must survive on
every screen. If a screen has none of them it is off-brand however tidy it is.

1. **Paper and ink, one orange.** Neutral paper surfaces, near-black ink, and a single orange
   (`#eb692a`) used as a *signal* — selection, progress, the one thing to notice. Never decoration.
2. **The ink button with the orange arrow.** ⚑ The primary action is ink-filled with its label left
   and an orange arrow right (onboarding's `.setup-continue`, login's `.auth-live-primary`).
3. **Mono eyebrow over a serif title.** A small uppercase Departure Mono line naming *where you
   are* ("START WITH YOU"), then the thing itself in Source Serif 4 at weight 500 with tight
   tracking ("Future Finder"). This pair is the page identity everywhere. Nothing else is needed
   above it — no banner, no hero card, no second icon.
4. **Hairlines, not boxes.** ⚑ 1px warm-grey rules and borders carry structure. Depth is reserved
   for things that genuinely float.
5. **Big honest numerals.** Progress is shown as large tabular numbers (onboarding's countdown and
   points), not as decorated widgets.
6. **Moment surfaces.** Full-bleed orange or ink screens exist, but only for moments: welcome,
   session complete, a milestone. Day-to-day screens are paper.
7. **Characters are guests.** The crew/subject characters and Star Guy bring warmth at intros,
   empty states and celebrations — small, slightly rotated, never between the student and the task.
8. **Motion that connects.** Things travel, draw and settle; they do not pop, bounce or fade from
   nowhere. Fast, decelerating, precise (Kobra's character).

**Warmth comes from** the serif, the warm greys, the characters, the moment surfaces and the copy —
*not* from extra colours, gradients, emoji or rounded-everything.

## 2. Spacing

4px base. Only these steps: **4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 56 · 72**.
Tailwind: `1 2 3 4 5 6 8 10 14 18`. Any other gap is a bug (no `gap-[13px]`, no `mt-7`).

| Relationship | Phone | iPad / desktop |
|---|---|---|
| Icon ↔ label, chip internals | 8 | 8 |
| Lines inside one item (title ↔ meta) | 4 | 4 |
| Items inside a card | 12 | 12–16 |
| Card padding | 16 | 20–24 |
| Cards in the same group | 12 | 16 |
| Section heading ↔ its content | 12 | 16 |
| **Section ↔ section** | **32** | **40–56** |
| Page title block ↔ first section | 24 | 32 |
| Last content ↔ bottom chrome | 32 + chrome height + safe area | 56 |

Rules:
- **Proximity is the hierarchy.** Space *between* groups must be at least 2× the space *within*
  them. If two boxes "feel bunched", the section gap is wrong, not the box.
- **More space above a heading than below it** (32 above / 12 below on phone).
- Lay out with `gap` on a flex/grid parent. No per-child margins to fake rhythm.
- One vertical rhythm per screen: a page is `flex flex-col gap-8` of sections; a section is
  `flex flex-col gap-3`.

## 3. Page margins and grid

| | Width | Gutter | Columns | Content max |
|---|---|---|---|---|
| Phone | < 768 | **20** (16 at ≤ 360) | 1 (4-col for tiles) | full |
| iPad | 768–1099 | 24 | 8 | 720 reading / 960 dashboards |
| Desktop | ≥ 1100 | 32–40 | 12 | 720 reading / 1120 app |

- Every screen uses the same gutter. Edge-to-edge is allowed only for: horizontal scrollers
  (which still start at the gutter), list groups in a sheet, media, and moment surfaces.
- Nothing is "shifted right": top-bar content aligns to the same gutter as the page below it.
- Reading text holds ~65 characters (`max-w-[65ch]`).

## 4. Typography

Three families, each with one job:

| Family | Job | Weights |
|---|---|---|
| **Source Serif 4** (`font-serif`) | Titles and headings — the voice | 500 (600 for small headings) |
| **UI sans** ⚑ — ABC Diatype recommended, DM Sans today | Body, controls, labels | 400 and 700 only |
| **Departure Mono** | Eyebrows and small data labels only | 400 |

⚑ Two near-identical sans faces (DM Sans and ABC Diatype) are both live. Recommended: ABC Diatype
for all UI (it is Kobra's face and what login uses). Until approved, do not introduce a third.

Phone scale (desktop in brackets). Do not invent sizes between these.

| Role | Size / line | Face, weight, tracking |
|---|---|---|
| Display (moment screens) | 40/42 (64/64) | sans 700, −0.04em — rare |
| **Screen title** | 28/32 (36/40) | serif 500, −0.02em |
| Section heading | 20/26 (22/28) | serif 500, −0.015em |
| Card title | 17/22 | serif 600, −0.01em |
| **Body** | 16/24 | sans 400 |
| Secondary | 14/20 | sans 400 |
| Caption | 12/16 | sans 400 — floor for sentences |
| Eyebrow | 11/14 | mono 400, UPPERCASE, +0.12em — floor, labels only |
| Numeral | 40–96 | sans 700, −0.04em, `tabular-nums` |

Rules:
- Hierarchy by **size, then weight, then colour** — never by adding a box or a colour.
- Max three text sizes in one card. Max one serif size per card.
- Nothing below 11px. Sentences never below 12px. Inputs are ≥ 16px (iOS zooms otherwise).
- Sentence case everywhere except eyebrows. No all-caps buttons.
- One eyebrow per region. An eyebrow must say something true and useful (section, step, count).
- `text-wrap: balance` on titles, `tabular-nums` on anything that counts or lines up.

## 5. Colour

Use the tokens in `index.css` (`:root` and `.dark`). **Never write a hex for a surface, border or
text colour** — if you need one, the system is missing a token; add it there.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--surface-canvas` | #FFFFFF | #151515 | The page |
| `--surface-paper` | #FFFFFF | #202020 | Cards, sheets, bars |
| `--surface-soft` | #F4F4F5 | #282624 | Insets, quiet fills, pressed, tracks |
| `--surface-raised` | #FFFFFF | #2B2927 | Floating layers: menus, toasts, dock |
| `--hairline` | #EDEBE8 | #34312E | Dividers, default card border |
| `--outline-soft` | #D4D4D8 | #494541 | Control borders |
| `--outline-strong` | #383838 | #A8A29E | Selected / emphasised border, focus |
| `--ink-primary` | #1A1A1A | #FAF8F4 | Titles, body |
| `--ink-secondary` | #5F5A55 | #D6D0C9 | Supporting text |
| `--ink-muted` | #69605A | #A8A29E | Labels, eyebrows, placeholders |
| `--nsu-orange` | #eb692a | #eb692a | Signal fill: selection, progress, the arrow |
| `--accent-text` | #B84A0C | (see note) | Orange *as text* |
| `--accent-tint` / `-ink` | #FDEEDF / #8C3A0E | #3A2417 / #F6B98C | Selected fill |
| `--success` + tint | #3A8D5F / #E8F2EC | / #1D3327 | Correct, complete |
| `--danger-tint` / `-ink` | #FDE4E4 / #8E2C2C | #3A2020 / #F0A9A9 | Errors, destructive |

Note: `--accent-text` has no dark value yet; use `#F99A63` (account-controls' dark ring) and add it
to `.dark` when you first need it.

Rules:
- **Orange budget: at most one orange *fill* in view at rest** (the selected thing, or the progress,
  or the arrow on the primary button). If two things are orange, one of them is wrong.
- **Orange ≠ good.** Correct / complete / healthy is `success` green. Unchanged from CLAUDE.md.
- Orange text on paper uses `--accent-text`, never the fill orange (3:1 only).
- Text contrast ≥ 4.5:1; large text and control boundaries ≥ 3:1. Status is never colour alone.
- Subject/tool identity colours may appear as a small tile, dot or illustration — never as a page
  background, card fill or button on task screens.
- No gradients, no glows, no purple, no second accent.

### Dark mode

- **Exactly four surfaces** (canvas → paper → soft → raised). Each step up is lighter. Never invent
  a fifth; never use a literal near-black (`#131313`, `#18181b`, `#191919`, `#1c1c1c`, `#222220`…).
- In `className`, dark surfaces are `bg-[var(--surface-paper)]` etc. — **not** `dark:bg-zinc-900 /
  950 / 800` (those resolve to three more off-system greys). Do not add new `dark:bg-zinc-*`.
- A section sitting on the page has **no background of its own**. Only cards (paper, radius 16) and
  floating layers have a fill. A full-width band of a different shade is a bug (the "Today's plan"
  defect).
- Feature palettes (`--mb-*`, `--ss-*`, `--module-*`, `--journey-*`, Kobra's `--background/--card`…)
  must alias to the four surfaces, not define their own blacks.
- Elevation in dark is the lighter surface plus a hairline — not a bigger shadow.
- No transition on theme switch.
- Every new component is checked in both themes before it is done.

## 6. Radius, borders, elevation

**Radius — four steps and full. Nothing else.**

| Token | px | Tailwind | Use |
|---|---|---|---|
| sm | 8 | `rounded-lg` | Chips, tags, small inner elements, checkboxes |
| md | 12 | `rounded-xl` | Buttons, inputs, list rows, icon buttons |
| lg | 16 | `rounded-2xl` | Cards, list groups, menus |
| xl | 24 | `rounded-3xl` | Sheets, dialogs, moment panels |
| full | — | `rounded-full` | Avatars, dots, pill chips, the tab-bar dock |

Nested radii are concentric: inner = outer − padding (a 16 card with 8 padding holds 8-radius items).

**Borders** ⚑
- Default: `1px solid var(--hairline)` (cards) or `--outline-soft` (controls).
- Selected / emphasised: `1.5px solid var(--outline-strong)` — or orange when it is *the* selection.
- No 2px ink boxes and no hard offset shadows (`shadow-[4px_4px_0_0_#1A1A1A]`) in new work.
- No coloured left borders on cards. (The Callout primitive keeps its 3px left rule.)

**Elevation** — border *or* shadow, never both for the same job.
- Level 0 (on page): hairline, no shadow.
- Level 1 (floating: menu, toast, tab-bar dock, sticky CTA): `--surface-raised` + soft layered
  shadow `0 2px 3px #00000008, 0 13px 25px -9px #00000025`.
- Level 2 (sheet, dialog): scrim `rgba(0,0,0,.4)` + the same shadow family, larger.

## 7. Cards and lists

- **Card:** paper, hairline, radius 16, padding 16 (phone) / 20–24. Title (card title style) →
  content → at most one action. A whole-card tap target has a trailing chevron, not a button inside.
- **Use a list, not cards, for many similar things.** Rows inside one radius-16 group separated by
  hairlines: 56–64px rows, leading icon/tile, title + one meta line, trailing value or chevron.
  A page of 20 separate cards is always wrong on a phone.
- **Selected card:** `--accent-tint` fill + 1.5px orange border + the selection mark (§12 motion).
- **Quiet inset:** `--surface-soft`, no border, radius 12 — for a note or figure inside a card.
- No cards inside cards. If you need a second level, use an inset or a divider.
- No coloured card backgrounds on task screens.

## 8. Buttons

One system: `ActionButton` / `.product-action` (`components/ui/controls.css`). Heights are fixed —
**a button never gets bigger to be more important; it moves up a level.**

| Level | Look ⚑ | Height | Use |
|---|---|---|---|
| **Primary** | Ink fill, paper text, radius 12, label left + orange arrow right when it advances | 48 | The one thing this screen is for. **One per screen.** |
| **Secondary** | Paper, 1.5px `--outline-soft`, ink text | 48 (44 inline) | The alternative |
| **Tertiary** | No border, no fill, ink-secondary text, 600 | 44 | Low-commitment, "Skip", "Not now" |
| **Destructive** | Tertiary shape, `--danger-tint-ink` text; filled only inside a confirm sheet | 44 | Delete, leave and lose |
| **Icon button** | 44×44 hit area, 40 visual, radius 12, hairline border *or* bare — one treatment per bar | 44 | Bar actions |
| **Chip / filter** | Radius full, 36 visual in a 44 row, hairline; selected = ink fill | 36 | Filters, quick picks |

Rules:
- Labels are verbs that name the outcome: "Start session", "Save plan". Never "Submit"/"OK".
- On phones the primary action lives at the **bottom**, full width within the gutter, in a sticky
  footer that respects the bottom safe area — not top-right.
- Side-by-side buttons are the same height. Primary on the right (or on top when stacked).
- Loading keeps the label and width; add a spinner, don't swap the text for one.
- **A button looks like a button; nothing else does.** Arrows/chevrons mean exactly: trailing
  chevron-right = "opens the next level"; arrow-right inside a primary = "advance". No decorative
  arrows, no arrows in three colours. If it is tappable and not a row/card/chip/tab, it is one of
  the levels above.

### Disabled and "not ready" states

- A primary action that is waiting on the student is **not** greyed-out-and-dead. It becomes the
  *not-ready* state: quiet fill (`--surface-soft`, ink-muted text), **still tappable**, and its
  label says what is missing: "Choose a subject to start".
- Tapping it: (1) scrolls the first missing control into view, (2) runs the attention ring on that
  control (`references/motion.md` — one 1.5px orange ring sweep, 400ms), (3) warning haptic on
  native, (4) the helper line under the control states the requirement in words.
- Use `aria-disabled="true"` (not `disabled`) so it stays focusable and announces the reason.
- Truly unavailable actions (no permission, offline) are hidden or shown with the reason — never a
  mystery grey button.

## 9. Navigation, Back, Close, Cancel, Exit

Full model in `references/navigation.md`. The contract:

| Word | Glyph | Means | Where |
|---|---|---|---|
| **Back** | arrow-left (the shared `BackButton`), no label on phone | Go up one level in the hierarchy. Never loses work. | Top-leading of the app bar. **Exactly one per screen.** |
| **Close** | ✕ | Dismiss something that came *over* the screen (sheet, dialog, viewer, intro). Nothing to lose. | Top-trailing of that layer |
| **Cancel** | the word | Abandon an edit with unsaved input. | Leading text button, paired with Save/Done; confirm if input exists |
| **Done / Save** | the word | Commit and dismiss. | Trailing, paired with Cancel |
| **Leave** | the word | Exit an immersive session (study timer, Mark Bank review, quiz). Replaces Back; confirms if progress would be lost. | Top-leading text button |

- Never two ways to do the same one. No in-page "← All subjects" links, no "Back to X" banners, no
  wordmark-as-back, no Back *and* Close on one layer. The header Back is the way back; its
  destination is the parent level.
- A sheet has Close (or Cancel + Done). It never has Back unless it pushes its own sub-level, in
  which case Back replaces Close on the sub-level only.
- iOS edge-swipe and Android/system back perform exactly the header Back.
- **One app bar** (`PageHeader`): `[Back] · eyebrow + title · [≤ 2 icon actions]`, 52px tall plus
  the top safe area, aligned to the page gutter, hairline appears on scroll. No per-feature headers.
- **Phone:** bottom tab bar (≤ 5 destinations), visible on every hierarchical screen; hidden only
  in immersive sessions, the module reader and onboarding. In-screen modes (Journey's island
  tools) are a *segmented control or contextual toolbar inside the screen*, styled from the same
  tokens — never a second, different-looking bottom bar.
- **iPad ≥ 768 and desktop:** the sidebar replaces the tab bar. Same destinations, same order,
  same icons (Tabler, outline → filled when active).

## 10. Sheets, dialogs, dropdowns

| Need | Phone | iPad / desktop |
|---|---|---|
| Pick one of a few (≤ 5, short) | Segmented control inline | Same |
| Pick one from a list / filter / sort | **Bottom sheet** list with a checkmark on the current value | Popover menu anchored to the trigger |
| Short scoped task, details, intro | **Bottom sheet**, grabber, radius 24 top, swipe down to dismiss | Centred dialog, max 480–560 |
| Long or multi-step task | Full-screen cover with its own app bar | Dialog or page |
| Confirm something destructive | Action sheet from the bottom (destructive, then Cancel) | Small alert dialog |
| Brief status | Toast above the tab bar | Toast bottom-right |

- **Phones do not get centred floating cards.** Intros, pop-ups and pickers are bottom sheets:
  the close affordance is then nowhere near the Dynamic Island, and it is in thumb reach.
- Sheet height: content-sized up to `calc(100dvh - var(--sat) - 12px)`; body scrolls inside,
  header and footer stay pinned; footer pads `max(16px, var(--sab))`.
- A dropdown trigger looks like a field (label, current value, chevron-down). It must *do
  something* on tap in every breakpoint — verify on a 390px viewport. Never ship a custom popover
  that is clipped by an `overflow:hidden` ancestor; portal it.
- One layer at a time. No sheet over a sheet over a dialog.

## 11. Empty, loading, error, offline

Use `components/ui/SystemState.tsx`. Every list and data view defines all four.

- **Empty:** one line of what this is, one line of what to do, one action. A character may appear
  here (§13). Sits directly on the canvas — no filled band.
- **Loading:** nothing under 1s; skeletons that mirror the real layout after that. No spinners
  centred on blank pages.
- **Error:** what happened, in plain words, and the way out ("Try again"). Next to the thing that
  failed. Never titled "Error", never colour alone.
- **Offline / locked:** say why and when it comes back.

## 12. Touch, safe areas, native feel

Details and the full "website in a shell" tell-list: `references/mobile-native.md`.

- **Touch targets ≥ 44×44** with ≥ 8 between them. A 36px visual control still gets a 44px hit area.
- **Safe areas are owned by primitives, not screens.** The top inset is handled by exactly three
  things: the app bar (`PageHeader`), the sheet/dialog frame (`ModalFrame`), and the immersive
  frame (study/quiz/session). **No other component may use `fixed`, `sticky` or `absolute` with a
  `top` value near the screen edge.** If you are typing `top-4 right-4` on an overlay, stop: put
  the control in the layer's header row.
- Inset values: `var(--sat) / --sab / --sal / --sar` (defined in `index.html`). Pad with
  `max(<design padding>, var(--sat))` — the inset is 0 on the web. Only *backgrounds* may extend
  under the status bar / Dynamic Island; no text, no controls.
- Heights use `100dvh`, never `100vh`.
- The primary action and frequent controls live in the bottom half. Top corners are for Back and
  low-frequency actions only.
- Hover effects only inside `@media (hover: hover)`. Every interaction has a pressed state.
- No text selection or tap-highlight flash on controls; no whole-page rubber-banding
  (`overscroll-behavior`); inner scrollers `contain`.
- Haptics (Capacitor) on commits: selection tick, success, warning. One per action, never alone.

## 13. Icons, illustration, characters

- **Icons: Tabler**, 20px, stroke 1.8 in bars and rows (24px for tab bar), outline by default and
  the Filled variant for the active tab. Do not add new `lucide-react` icons to chrome; migrate
  when you touch a file. Icons inherit `currentColor`. No emoji as icons.
- One glyph per meaning app-wide: arrow-left = Back, ✕ = Close, chevron-right = opens next level,
  chevron-down = opens a picker, arrow-right = advance (primary only).
- **Characters and illustration**
  - Allowed at: intros, empty states, celebrations/moment surfaces, section identity tiles.
  - On a task screen (choosing, answering, reading) a character is at most **96px** tall and sits
    beside or above the title — never a hero. On a phone it may not take more than ~15% of the
    viewport height, and it must never push the first interactive control below the fold.
  - On moment surfaces it may be large (up to ~40% of the height).
  - One character per screen. Slight rotation (−8° to 10°) is the house gesture.
  - Tool identity appears **once** per screen (in the app bar). Never repeat the icon further down.

## 14. Motion (summary — read `references/motion.md` before animating)

- **Ask how often.** Hundreds of times a day or keyboard-driven → no animation. Tens → minimal.
  Occasional (sheets, toasts) → standard. Rare (first run, milestone) → may delight.
- Curves: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)` for enter/exit and most things;
  `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)` for on-screen movement;
  `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)` for sheets and page slides. Never ease-in, never linear (except constant motion).
- Durations: press 120 · state change 150 · small enter 220 · page/sheet 300–340 · sheet max 500.
  Exits are ~25% faster than enters. Feedback to a tap starts within 100ms.
- Press: `scale(0.97)` (0.96 for icon buttons). Nothing scales from 0 — start at 0.95 + opacity 0.
- **Continuity:** a highlight slides between items (shared `layoutId`), a tick *draws*, a sheet
  comes from the edge it lives on, a selection mark grows from the tap. Springs use bounce 0.
  Overshoot is reserved for tiny physical moments (never selection, never navigation).
- Success = draw or sweep. Rejection = a short horizontal shake (6px, ~280ms). Needs-attention = one
  ring sweep.
- Animate `transform` and `opacity` only. Never `transition: all`.
- `prefers-reduced-motion`: keep opacity, drop movement and scale.
- Import from `components/Motion.tsx`, never `framer-motion` directly.

## 15. Phone vs iPad vs desktop

Same tokens, same components, same words — different *arrangement*.

| | Phone | iPad | Desktop |
|---|---|---|---|
| Primary nav | Bottom tab bar | Sidebar | Sidebar |
| Primary action | Sticky bottom, full width | In content, trailing | In content, trailing |
| Pickers / intros | Bottom sheet | Popover / dialog | Popover / dialog |
| Many items | Search + drill-down list, one level per screen | List + detail side by side | List + detail, or table |
| Density | One column, 16px body | 2 columns | Up to 3; can show eyebrows, meta, hover |
| Back | Icon only | Icon + label | Icon + label |
| Detail | Pushed screen | Split view | Split view / panel |

- A phone screen does **one job**. If it scrolls for more than ~3 viewport heights, it needs
  information architecture, not styling: search-first, segmented tabs, drill-down, collapsed
  sections with counts, or a separate detail screen (§ long pages in `mobile-native.md`).
- Tables do not exist on phones: they become lists of rows with the two most important fields, and
  a detail screen for the rest.
- Staff surfaces (Counsellor, Admin) follow the same system. They are not exempt.

## 16. Self-check before you call it done

- [ ] Uses existing primitives; no new one-off header, button recipe, back link or dark colour.
- [ ] Only scale values for spacing, type, radius. Section gaps ≥ 2× inner gaps.
- [ ] One primary button; nothing enlarged for emphasis; ≤ 1 orange fill at rest.
- [ ] Exactly one Back (or Leave); Close only on layers; no duplicate ways out.
- [ ] Nothing interactive under the status bar / Dynamic Island or home indicator; no stray
      `fixed/absolute top-*`.
- [ ] All targets ≥ 44px; primary action in thumb reach on phone.
- [ ] Every dropdown/picker actually works at 390px wide.
- [ ] Empty / loading / error / not-ready states exist and explain themselves.
- [ ] Light **and** dark checked; only the four surface tokens; no band of a different shade.
- [ ] Motion follows the frequency gate, the three curves, reduced-motion.
- [ ] Checked at 390×844 (phone), 820×1180 (iPad), 1440×900 (desktop) — as three designs, not one stretched.
- [ ] At least two of the §1 signatures are visibly present.
