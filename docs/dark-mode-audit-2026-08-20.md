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
