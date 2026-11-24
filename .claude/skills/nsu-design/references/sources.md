# Sources and status of the rules

Researched November 2026. Full notes with URLs per rule: `research/`.

| Source | Used for | File |
|---|---|---|
| emilkowalski/skills (github.com/emilkowalski/skills) | Motion: frequency gate, the three easing curves, durations, press scale, stagger, interruptibility, reduced motion; mobile baseline | `research/design-skills-and-kobra.md` §1 |
| kobra.systems (HTML + CSS bundle read) | Visual language (achromatic neutrals, hairlines, 10px radius family, layered micro-shadows, two-weight type, mono for technical labels) and motion character (continuity, draw/sweep, per-component timing) | same, §2 |
| Kobra as implemented in this repo (`approved-ui-runtime`, sidebar, login, onboarding) | The actual tokens, the ink primary button, the eyebrow/serif pair | in-repo; summary in `docs/design/system-2026-11/` |
| Anthropic frontend-design, Vercel Web Interface Guidelines, Rauno Freiberg, ibelick/ui-skills, pbakaus/impeccable | Token-plan-first, outcome-named CTAs, concentric radii, layered shadows, loading/optimistic patterns, contrast, "space above headings" | same, §3 |
| Apple Human Interface Guidelines | Safe areas, 44pt targets, tab bar vs sidebar, Back/Cancel/Done semantics, sheets, type floor, dark base/elevated surfaces | `research/mobile-ios-practice.md` |
| WCAG 2.2, WebKit, web.dev, Capacitor docs, NN/g, Baymard, Smashing | Contrast, target size, `env()` insets, `dvh`, Capacitor inset/keyboard behaviour, disabled-button guidance, lists vs cards, progressive disclosure | same |

## House decisions (where sources disagree or are silent)

- **Press scale 0.97** (Emil 0.97, Rauno ~0.96, Kobra 0.985).
- **Feedback ≤ 150ms, UI transitions ≤ 320ms, sheets ≤ 500ms** (Rauno/ibelick say 200; Emil < 300).
- **Close vs Cancel vs Leave** as three distinct roles is our convention; HIG treats Cancel/Close
  as one and does not define Exit.
- **Not-ready CTA stays tappable and explains itself** — reconciles HIG ("available only after
  required data") with HIG Feedback ("help them understand why") and Smashing's guidance.
- **Uppercase mono eyebrows and the serif** are kept although generic "AI-look" lists flag them:
  they are house style, confined to one eyebrow per region.
- **Spacing/margin numbers (20px gutter, 32px section gap)** are ours; Apple publishes no values.
- **Body 16px** (HIG says 17pt) to match the web build; reading surfaces may use 17.

## Not verified

Mobbin was not consulted (no logged-in browser in the research session). Kobra was read from
markup and CSS, not viewed rendered; its Pro "AI skills" were not retrieved. Material's dark-theme
numbers, UIKit transition durations and Refactoring UI were not retrieved. See the "could not
verify" lists at the end of each research file.
