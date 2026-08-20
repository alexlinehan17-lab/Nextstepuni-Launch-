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
