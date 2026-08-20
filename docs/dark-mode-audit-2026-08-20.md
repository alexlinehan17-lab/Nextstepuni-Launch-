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
