# Module dark-mode audit — 5 October 2026

The local Kobra sidebar preview now has a consistent dark module library and
lesson reader. No deployment, native sync, or App Store submission was performed.

## Scope and findings

Audited all **83 registered modules and 505 sections**, including the subject
protocols, at 1440px and 390px widths. Also checked the library overview and all
five category pages at both widths.

The reader had lost its `theme-compat` boundary during the Kobra conversion.
Older exercises consequently kept white panels while their text switched to a
light colour. The initial HTML-text sweep found 1,205 contrast issues and 279
large light surfaces. Module cards also retained greenish backgrounds, bright
offset shadows, cream chips, and glowing actions.

## Changes

- Restored the reader's compatibility boundary and paired legacy activity
  surfaces with readable dark-theme ink, scoped to module lessons.
- Gave library and category cards neutral charcoal surfaces, quiet borders,
  subtle elevation, neutral section previews, and clear current-card states.
- Standardised reader text, input backgrounds, placeholders, focus outlines,
  selected contents rows, dividers, and tool links.
- Lifted chart labels and semantic feedback ink. Preserved chart data and hues;
  deepened red, violet, and pink actions for readable labels at rest and hover.
- Styled the portalled notes notebook and module completion screen to match.
- Removed obsolete top-right account spacing, kept the phone section counter
  together, and marked the decorative quotation mark as hidden from assistive
  technology.

Lesson wording, exercises, progress logic, curriculum, and Mark Bank content are
unchanged. Existing purchased Kobra controls remain in use.

## Verification

| Coverage | Result |
| --- | --- |
| Desktop: 83 modules / 505 sections | 12,283 measured text nodes; 0 contrast findings, light panels, or horizontal overflow |
| Phone: 83 modules / 505 sections | 11,900 measured text nodes; 0 contrast findings, light panels, or horizontal overflow |
| Overview plus five categories at both widths | 0 text-contrast findings or horizontal overflow |
| Representative exercise hover/active states, reframing, answer selection, notes, contents, sources, reading controls, completion | 0 dark text-contrast findings or horizontal overflow |
| Additional humanities feedback and both nutrition selection states, dark/light reader smoke checks | 16 checks passed |
| Six existing regression suites | 46 tests passed |
| TypeScript, changed-component ESLint, production build, diff whitespace check | Passed |

The final sweep includes SVG text labels as well as HTML text. Identified problem
modules were checked again after their fixes; the machine-readable companion
records the combined results. The local harness rendered the actual registry
components with inert progress callbacks and no signed-in account. It was removed
after verification.

The contrast check used rendered foreground/background colours against the
[WCAG 2.2 text thresholds](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
(4.5:1 for normal text, 3:1 for large text). Disabled controls, hidden content,
decorative elements, transitional opacity, and unresolved image/gradient
backgrounds are excluded. SVG plot geometry is reviewed visually rather than
treated as an HTML background. This is an audit of measured states, not a claim
that every possible exercise state or the whole app is WCAG conformant.

Visual review covered both themes, phone and desktop layouts, charts, notes, and
completion. Browser checks used Chromium; native iOS and Safari remain outside
this local audit. Review at <http://127.0.0.1:5224/sidebar-review.html>.
