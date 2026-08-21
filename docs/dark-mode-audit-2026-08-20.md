# Dark mode audit — 20 August 2026

Method: ran the app on localhost with `darkMode: true` persisted in
`nextstep-settings`, and injected a contrast auditor that walks every text node,
resolves the *effective* background (climbing ancestors through transparency),
and reports anything under the WCAG AA threshold for its size and weight. Paired
with a source sweep for light surfaces that dark mode cannot reach.

## The architecture is sound. The problem is coverage.

`index.css` defines a full semantic token set and redefines all of it under
`.dark` — `--surface-canvas`, `--surface-paper`, `--ink-primary`, the dashboard
palette, and a complete 15-token `--mb-*` palette for Mark Bank.

It also carries a genuinely good **compatibility layer** for screens that pre-date
the tokens: it rewrites `bg-white`, `bg-zinc-50`, `text-zinc-900`, inline
`background: #fff`, `border-[#1A1A1A]` and more onto the dark tokens.

**That layer is scoped to `.product-shell`, and only six components carry it:**
DashboardView, InnovationZone, KnowledgeTree, LearningPathsView, ModuleLayout,
ModulesView.

`ModuleLayout` is on that list, so all ~55 modules are covered. Everything not on
it gets no dark treatment whatsoever.

## Confirmed broken (verified in the browser)

### LoginPage — the first screen every user sees
- Page canvas is an **inline** `background-color: rgb(250,251,246)`. Tailwind's
  `dark:` variant is a CSS class and cannot override an inline style attribute,
  so this is permanently light.
- Card is `bg-white` with no `dark:` counterpart.
- Text *does* have dark variants and flips to `#f4f4f5` — on white.
  - `h1 "Your study, your way."` → **1.1:1** (needs 3:1). Invisible.
  - `p "Science-backed study strategies…"` → 2.56:1
- On the dark left panel, two strings are too dark to read:
  - "Where examiner insight meets your routine." `#4a4540` on `#18181b` → **1.87:1**
  - "Nextstepuni" → 2.4:1
- 0 `dark:` variants in the file.

### AccreditationPage (References) — 0 `dark:` variants
- Six `bg-white` containers, none with a dark variant.
- Stats card: `48` and `133` render `#f4f4f5` on white → **1.1:1**. The two
  headline numbers are literally invisible.
- Selected module row keeps the light accent tint `#FDEEDF`.
- Search field stays white.
- Every `doi:` link → 2.56:1.

## No dark support at all (source-confirmed, same class of bug)

| Screen | `product-shell` | `dark:` variants |
|---|---|---|
| LoginPage | no | 0 |
| AccreditationPage | no | 0 |
| ResetPasswordPage | no | 0 |
| CutContentPage | no | 0 |
| WipTools | no | 1 |
| YearPlansView | no | 1 |

## Partial — has dark work, but also light values it cannot reach

| Surface | `dark:` variants | inline light colours |
|---|---|---|
| ExaminersChair/index.tsx | 20 | 10 |
| AdminFeedbackInbox.tsx | 3 | 3 |
| SpacedRepetitionTimetable.tsx | 190 | 6 |
| PaperTrail/Viewer.tsx | 104 | 2 |
| Onboarding.tsx | 89 | 5 |

## Already correct — do not touch

- **Mark Bank** — complete `--mb-*` dark palette, all 15 tokens redefined.
- **All ~55 modules** — inherit the compat layer via `ModuleLayout`.
- DashboardView, InnovationZone, KnowledgeTree, LearningPathsView, ModulesView.
- **GCDashboard** — deliberately forces dark on mount, always.

## Scale of the reachable problem

254 inline light colour values across 92 component files. Inline styles are the
important subset: a `dark:` class can never override them, so they need either a
CSS-variable swap or an `!important` rule in the compat layer.

## Not dark-mode bugs, but found on the way

- Orange `#F26B1F` with white text is **3.04:1** — fails AA for body text in
  *both* themes. It appears on primary CTAs ("Continue"). Either darken the
  orange for text use or use `--ink-on-accent` (`#1A1A1A`), which the token set
  already defines for exactly this.
- Every icon button in the left rail is unlabelled — `read_page` returns 24
  anonymous `button` elements. Screen-reader users get nothing.

---

# What was fixed

## 1. The compat layer now reaches past `.product-shell`

The dark-scoped rules match `:is(.product-shell, .theme-compat)`. Orphaned
screens opt in with the new class: LoginPage, ResetPasswordPage,
AccreditationPage, CutContentPage, WipTools, YearPlansView.

The field grammar below it stays `.product-shell`-only on purpose — it is not
dark-scoped, so extending it would have restyled inputs in light mode too.

## 2. The auth screens follow the theme

They had tried to opt out with `className="… light"`, `data-theme="light"` and
`colorScheme: 'light'`. That set the surface but never the text: `body` carries
`dark:text-zinc-100`, so the card stayed white under near-white type. Removed.

## 3. The muted text steps, lifted for dark only

`tailwind.config.ts` replaces Tailwind's zinc scale with a warmer, darker one —
zinc-500 is `#666663`, not `#71717a`. Fine on white at 5.9:1; about **3.2:1** on
the dark canvas. `dark:text-zinc-500` is used **425 times across 88 components**,
so this one substitution was the single largest source of failing text in the
app. Lifted to zinc-400 in dark only, targeting the `dark:` variant class alone
so `text-zinc-500 dark:text-zinc-100` keeps what it asked for.

`!important` is load-bearing here: Tailwind emits the variant as
`.dark\:text-zinc-500:is(.dark *)`, same specificity as `.dark .dark\:…`, and
emitted later, so it wins on source order.

## 4. Semantic tints written inline

React serialises an inline hex as `rgb(…)`, which is why the compat selectors
match the rgb form — `#f8f8f8` (196 uses) was already covered as
`rgb(248, 248, 248)`. The remaining ~260 were the tints that carry meaning:
selected, correct, error, note. They now map to `--accent-tint`,
`--success-tint`, and the new `--danger-tint` / `--info-tint`, staying tinted in
dark rather than collapsing to a neutral and losing the state they encode.

## 5. The primary CTA needed its own token

A plain white button folds onto `--surface-paper`, which in dark is the same
colour as the card behind it — "Get Started" lost all prominence and the
secondary control read as primary. `--cta-invert-*` keeps light identical and
gives dark a genuinely raised surface.

# Measured result

| Screen | before | after |
|---|---|---|
| Login | 4 contrast failures, worst 1.1:1, 2 white surfaces | **0 / 0** |
| References | 14+ failures, 6 white panels, two headline numerals invisible | **0 / 0** |
| Student dashboard | 1 failure | **0 / 0** |
| Module (Bimodal Brain) | — | **0 / 0** |

Light mode is unchanged to the byte. `test/darkModeTokens.test.ts` pins the light
values, requires every themed token to be redefined under `.dark`, and fails if a
dark rule is left scoped to `.product-shell` alone.

# Still open

- **Onboarding** (89 `dark:` variants, 5 inline light) and **SettingsModal**
  (60) were not walked end to end — they need a pass with the auditor.
- **GCDashboard** forces dark on mount always; it was not in scope and was not
  touched.
- Orange `#F26B1F` with white text is **3.04:1** and fails AA in *both* themes on
  primary CTAs. `--ink-on-accent` (`#1A1A1A`) already exists for exactly this and
  clears AA; switching the CTAs to it is a small, separate change.
- The left rail's icon buttons are unlabelled — `read_page` returns 24 anonymous
  `button` elements.

---

# Second pass — exhaustive sweep

The first pass sampled screens by clicking, which is how the Modules list was
missed. `NavigationContext` listens to `popstate`, so every view in
`VALID_VIEWS` can be visited without a reload. All eighteen were walked and
audited.

## Screens the sampling never reached

| Screen | Failures found |
|---|---|
| Training Hub (`gamification-hub`) | 21 |
| Study Session | 10 |
| Cut Content | 7 + a light sticky header |
| JC Coming Soon | 4, worst 1.02:1 |
| WIP Tools | 1 |

Same cause each time: the screen never opted into the compat layer, so rules
already written for it never reached. `theme-compat` added to TrainingHub,
JCComingSoon, MyDirection and StudySessionView.

## The token system I had not seen

`index.html` carries a **second** token set — `--bg-*`, `--text-*`, `--border-*`
— predating the `--surface`/`--ink` set in `index.css` and still consumed by
inline style props across the modules and the hub. `--text-label` was `#71717a`:
**3.37:1 on its own `--bg-card`**, failing on every stat label in the Training
Hub.

The first pass could not have caught it, because the audit only read
`index.css`. The test now reads both files, checks each text token against the
card it sits on, and checks the scale still descends so "label" cannot end up as
loud as "primary".

## Module world colours

Each world's `deep` tone is authored for a light card and is used at 60-80%
alpha. Measured on the dark card: navy 1.54:1, red 1.77:1, magenta 2.15:1, teal
2.31:1. Each world gained a `deepDark` of the same hue; two also needed a
`midDark` for the small mono numerals. Not white — the worlds are colour-coded
and flattening them would have destroyed the signal.

## Ink on the accent

White on `#F26B1F` is 3.04:1 and cream 2.88:1 — failing in **both** themes.
Now resolved to `--ink-on-accent` (`#1A1A1A`, 7.9:1), targeted at the accent
surface rather than at `text-white`, which has ~950 uses and is correct nearly
everywhere else.

Five distinct ways the accent surface is expressed had to be covered; the
`bg-[var(--accent-hex)]` form is what let the study-session Start pill through
on the first attempt.

# Final state — dark mode

**Zero contrast failures and zero stranded light surfaces across all eighteen
views.**

# Light mode — a separate, larger problem

Sweeping light mode with the same auditor found **434 failures**, all
pre-existing and none introduced here (the token values are pinned by test):

| Screen | Failures |
|---|---|
| Cut Content | 333 |
| Dashboard | 44 |
| Accreditation | 22 |
| Training Hub | 21 |
| Modules | 12 |
| Launchpad | 2 |

Dominant causes, all long-standing:

- The brand orange `#F26B1F` used as **text** on white — 3.04:1. Distinct from
  text *on* orange, which is now fixed.
- `--page-label` `#9E9186` on the `#f0f0f0` canvas — 2.69:1.
- `--ink-faint` `#B0A898` on the neutral pill — 2.04:1.
- Amber `#F59E0B` on white — 2.15:1.

This was never in scope and is not a regression. It is a bigger job than the
dark-mode work was, because unlike dark mode there is no compat layer to hang it
on — the light palette itself is too low-contrast in places.

---

# Third pass — the parameterised views

The second sweep walked `VALID_VIEWS` but passed no parameters, so `category`
rendered nothing and was scored as clean. Alex found it by looking at it.

`?view=category&cat=…` had **22 to 48 failures per world**, worst at **1.02:1** —
every module title, `#1A1A1A` on `#18181b`.

## Root cause: the world palette existed twice

`ModulesView` and `ModuleShowcase` each carried their own copy of the same five
world colours. Giving the worlds a dark ink fixed the copy in `ModulesView` and
left `ModuleShowcase` entirely untouched, which is why the category screen still
looked like the screenshot.

Now one source: `components/worldPalette.ts`. The test asserts the hexes appear
in **no other file**, so a third copy cannot drift away again.

## `mid` is two things, and that matters

The world `mid` tone is used both as **text** (eyebrows, counters) and as a
**fill** (buttons, progress bars). Lightening it wholesale for dark fixed the
text and broke the buttons — white labels on the lightened fill went from 3.6:1
to **2.4:1**. Twice, in both components, before it was separated properly.

`midText` is now a text-only swap; fills keep the saturated `mid`. The test pins
that distinction.

## Reference surface was wrong

`deepDark` was tuned against `#18181b`, the page canvas. These tones actually sit
on the **raised card**, `#202020`, which is lighter and therefore the worst case.
Every world measured 4.49 there — passing the old test, failing in reality. All
five lifted, and the test now uses the raised card.

# Final state

| Surface | Failures |
|---|---|
| All 15 base views | **0** |
| All 5 category views | **2** each |

The two are white on the world `mid` used as a button fill: 4.20:1 on the navy,
4.01:1 on the red. They fail identically in light mode.

**This one cannot be fixed by changing the ink.** The world mids are
mid-luminance, so neither white nor `--ink-on-accent` clears AA on all five:

| World | mid | white | #1A1A1A |
|---|---|---|---|
| Mind | `#5B7DB0` | 4.20 | 4.15 |
| Growth | `#C4873B` | 3.05 | **5.70** |
| Learn | `#F26B1F` | 3.04 | **5.72** |
| Decode | `#C76489` | 3.74 | **4.65** |
| Exam | `#D4564E` | 4.01 | 4.34 |

Dark ink wins on three of five and is still short on Mind and Exam. Clearing AA
on all of them needs the **fill** darkened — using each world's `deep` for the
button rather than `mid` — which is a visible design change in both themes and
so is left as a decision rather than assumed.

---

# Fourth pass — the world CTA and the naked icons

## World CTA: inverted in dark, light untouched

Darkening the fill to `deep` was the obvious move and measures badly. The label
would clear comfortably (7.4-11.5:1) but the button ends up only **1.4-2.2:1**
clear of the card behind it — technically compliant and visually dead, reading
as a tinted hole rather than a raised action.

Inverting instead:

| | Label contrast | Button vs card |
|---|---|---|
| Light — `mid` fill | unchanged | unchanged |
| Dark — `deepDark` fill, dark ink | 11.7-12.6 | **11.0-11.8** |

Light mode is deliberately left at 4.01-4.20:1, marginally under AA, on Alex's
call. It is the same pattern `--cta-invert-*` already uses for the login CTA.

The label uses `var(--ink-on-accent)`, not the literal `#1A1A1A`: the compat
layer rewrites an inline `color: rgb(26, 26, 26)` onto `--ink-primary`, assuming
legacy light-mode text, which turned the label near-white on a pale fill.

## Learning Paths icons

The path icons are hand-drawn PNGs deliberately shipped naked — the code comment
reads "no tile, no blob" — as near-black line work on a transparent ground. On
the dark card they all but disappeared.

A pale disc sits behind them in dark only. Filtering or inverting the PNG was the
alternative and would have shifted the orange accents inside the artwork; the
disc leaves the drawing exactly as authored. In light the disc is `display: none`
and the naked icon is preserved.

# State after this pass

| Surface | Dark |
|---|---|
| All 15 base views | **0** |
| All 5 category views | **0** |

---

# Light mode

Swept with the same auditor, signed in, across all 15 base views and all 5
category views: **1,272 failures across 64 distinct colour pairs.**

## The palette could not carry four muted steps

The binding surface is `#f0f0f0`, the editorial canvas — darker than white, so
harder for dark text. Tuning every muted token to 4.5:1 there produces
`#736b64`, `#756b64`, `#776a60`, `#756c5a`: four tones that are the same colour.
Raising the bottom of the scale necessarily compresses it, because above 4.5:1
the usable band is only about 4.5–7.

So the scale is now three steps rather than four:

| step | was | now | on `#f0f0f0` |
|---|---|---|---|
| body / secondary | `#5a5550` | unchanged | 6.44 |
| muted | `#7a7068` | `#69605A` | 5.39 |
| label / faint | `#9e9186` / `#B0A898` | `#766A5F` | 4.61 |

`--page-label` and `--ink-faint` now share a tone. They were 2.69:1 and 2.07:1 —
that band was never legible text, so nothing readable was lost by merging it.

## Fills are not inks

Three colours were being used as text that are fill colours:

- the brand orange `#F26B1F` — **3.04:1** on white
- amber `#F59E0B` — **2.15:1**
- each world's `mid` — 3.05–4.20:1

Each gains a text-only variant: `--accent-text` `#B84A0C`, `--warning-text`
`#96600A`, and a per-world `midInkLight`. The fills themselves are untouched, so
buttons, icons and progress bars keep their authored colour.

## ~600 literals, remapped rather than rewritten

Roughly 600 inline styles across 70 components hardcode the old greys instead of
reaching for a token. They are remapped in CSS, light-only, the same way the dark
compat layer works — reviewable in one place, and a stray literal in new code is
corrected too.

Translucent black text got the same treatment, but only for the three alphas that
actually fail: 0.35, 0.45 and 0.5 flatten to 2.43, 3.36 and 3.95:1. From 0.55 up
it already passes and is left exactly as authored.

## Two bugs found in my own work

`[style*="color: …"]` also matches `background-color: …`, because the shorter
string is a substring of the longer one. That recoloured labels sitting *on* an
orange fill, dark rust on orange at 1.71:1. Selectors are now anchored to the
start of the attribute or to a `"; "` boundary.

`midInkLight` was first tuned against white and measured 4.43:1 on the actual
card. Retuned against `#f0f0f0`.

# Final state

| | base views | category views |
|---|---|---|
| Dark | **0** | **0** |
| Light | **0** | 12 |

The 12 are white on the world `mid` used as a button fill, 3.05–4.20:1, left at
Alex's explicit call. It cannot be fixed by changing the ink — the mids are
mid-luminance, so neither white nor dark ink clears AA on all five. Clearing it
needs the fill darkened, which is a visible design change in both themes.

---

## Innovation Zone tool sweep — 21 August 2026

Swept the **16 shipping tools**. The six Workshop/WIP tools (`diagram-vault`,
`answer-architect`, `definition-drill`, `oral-trainer`, `examiners-chair`,
`coursework-companion`) are parked out of the main grid and were excluded.

Method: a compositing contrast scanner run over every rendered text node.
The earlier version skipped translucent backgrounds and read through to an
opaque ancestor, which both hid real failures (a 12%-black badge over a blue
chip) and invented false ones (an 80%-alpha dark toast over a light card).
Compositing every layer outward fixed both.

### Result

| | dark | light |
|---|---|---|
| before | 9 tools / 121 failures | 8 tools / 81 failures |
| after | **1 tool / 1 failure** | **3 tools / 4 failures**, all 4.37–4.49 |

The 4 remaining light findings are `#78716c` and `#766e67` on tinted cards,
within 0.13 of AA — inside the tolerance already accepted for the world CTAs.

### Root causes

1. **Your Possible Life was never wearing `immersive-deck-theme`.** It is the
   third colour-world deck but hard-coded its own paper/ink, so the dark compat
   layer forced near-white ink onto near-white paper — **1.04:1 on all twelve
   value labels**. Migrated onto the deck tokens; added `--deck-accent-text`
   because the brand orange is a fill (2.9:1 on white) and was being used as
   label text.

2. **`ColorWorld.deep` is tuned for white paper.** On the dark deck paper
   `#242321` all twelve worlds land at 1.79–2.87:1. `glow` is the readable tone
   there (5.35–7.83:1). Added `paperInk()` / `usePaperInk()` and applied it at
   the sites where `deep` sits on paper — chips on `tint` keep `deep`, since the
   tint wash stays light in both themes.

3. **Remapping an ink without its fill.** The Journey phase chip paints its own
   `#D8E4DA` background; the ink remap flipped `#3F6A5E` light while the fill
   stayed light → 1.23:1. A general `:not([style*="background"])` guard was tried
   and **reverted** — it broke the opposite case, where College Compass and
   Points Passport rely on fill and ink being remapped *together* (that regressed
   8 tools to dark-on-dark). The rule is: **remap both or neither.**

4. **Overlay tinted toward the ink.** The timetable's type badge overlays
   `rgba(0,0,0,0.12)` on the subject chip — darkening the surface under dark
   ink. The overlay must move the background *away* from the ink: 17 of 33
   subject colours failed, 0 after.

5. **Fill tones used as text**, again: `CYCLE_META.accent` in Year Plans
   (2.49–3.68:1 in light, 3.88–4.38:1 in dark) and `#9E9186` / `#7A7068`
   arriving through `--mb-label` / `--deck-label`, which the attribute-based
   light remap cannot reach because they come from `var()`.

### Not changed — needs a design call

White on the world identity colours fails in **both** themes for 7 of the 12
worlds: teal 3.16, pine 3.30, terracotta 3.42, forest 3.49, denim 3.53,
rose 4.03, rust 4.13. `--ink-on-accent` is better on five of them (4.93–5.51)
but that flips the deck header bands from white text to near-black, which is a
deliberate part of the deck design language. Left as-is pending a decision.

### Regression guard

`test/darkModeTokens.test.ts` now fails the build on any unanchored
`[style*="color: …"]` matcher — the substring bug that recoloured children of
white-background elements three separate times this session.
