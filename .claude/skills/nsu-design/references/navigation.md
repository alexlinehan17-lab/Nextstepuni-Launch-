# Navigation — Nextstepuni

One model for the whole product. The Nov 2026 audit found nine back/close styles, six screens with
more than one way back, and ~11 bespoke headers; this file replaces all of them.

## 1. Structure

```
Tab (Home · Modules · Launchpad · Journey · Progress)        ← level 0, tab bar / sidebar
└─ Screen                                                    ← level 1, app bar with title only
   └─ Pushed screen (a tool, a subject, a topic)             ← level 2+, app bar with Back
      ├─ Sheet / dialog (picker, intro, details, confirm)    ← a layer over the screen: Close
      └─ Immersive session (study room, review, quiz)        ← full-screen, no tab bar: Leave
```

- Each screen belongs to exactly one place in this tree, and Back always goes to its parent —
  not to "wherever you came from". Cross-links (e.g. a module opened from Journey results) still
  show one Back, labelled for the place it actually returns to.
- History: Back pops. It must not push a new entry (the audit found every in-app back now pushes
  forward — fix in `contexts/NavigationContext.tsx` so system back and header Back agree).

## 2. The app bar (`components/ui/PageHeader.tsx`)

```
┌──────────────────────────────────────────────┐
│  (top safe area — background only)           │
│ [←]   START WITH YOU                  [·][·] │  52px row, page gutter left and right
│       Future Finder                          │
└──────────────────────────────────────────────┘
```

- Leading: `BackButton` (44×44, arrow-left 20px). Absent on level-1 tab screens.
- Centre-left: mono eyebrow (the section or parent) over the serif title (this screen). On
  level-1 screens the title may be the large 28px screen title in the content instead.
- Trailing: at most two icon buttons, all the same treatment. A third action goes in an overflow
  menu. Never a text button and an icon button of different heights side by side.
- No tool icon/artwork in the bar on phones beyond a single 28px identity tile if the tool has one.
  The identity is **never** repeated in the content below, and there is **no banner/hero card**
  (the black Launchpad masthead and its mobile "introduction" are removed; a first-visit intro, if
  wanted, is a bottom sheet).
- Sticky; paper background; hairline bottom border appears once content scrolls under it.
- The bar owns the top inset: `padding-top: max(8px, var(--sat))`.
- Progress for a multi-step flow (Future Finder's Your interests / What matters / Your
  possibilities) is a **step row directly under the bar**, inside the same gutter: three equal
  segments, 2px track, current label in ink, others muted — onboarding's segmented progress. It is
  not a second header and has no icon.

## 3. The five ways out

| | Glyph / label | Position | Behaviour |
|---|---|---|---|
| Back | arrow-left, icon only on phone, icon + parent name on iPad/desktop | App bar leading | Pop to parent. Never confirms, never loses work (auto-save or keep state). |
| Close | ✕ in a 44px icon button | Top-trailing of the sheet/dialog/viewer | Dismiss the layer. Also: swipe down, scrim tap, Esc. |
| Cancel | "Cancel" tertiary text | Leading of a form sheet's header, or left of Save in a footer | Abandon unsaved input; if any exists, confirm with an action sheet. |
| Done / Save | "Done" / verb | Trailing | Commit and dismiss. |
| Leave | "Leave" tertiary text | App-bar leading of an immersive session, replacing Back | If progress would be lost: action sheet ("Leave session? Your 18 minutes are saved." / Leave / Keep going). |

Forbidden combinations: Back + Close on the same layer; an in-content "← Back to …" link when the
bar has Back; a banner whose only job is to go back; two different exits that do the same thing
(the study timer's "X Leave" + "Minimise" must be two *different* things: Leave ends, Minimise keeps
running — label both in words or keep one).

## 4. Tab bar (phone) and sidebar (iPad, desktop)

- Phone: 5 tabs max, icon (Tabler 24, filled when active) + 11px label, paper background, hairline
  top, bottom padding `var(--sab)`. The active state is ink icon + label with the slide highlight
  — orange is not needed on all five.
- Visible on all hierarchical screens including pushed ones. Hidden only in immersive sessions,
  the module reader and onboarding.
- **There is only one bottom bar.** A screen that needs its own tools (Journey island: Your
  island / Fieldbook / Stickers / Visitors / Build) uses a *contextual toolbar*: a floating
  radius-full dock, `--surface-raised`, level-1 shadow, 12px above the tab bar, same icons/type
  tokens as the tab bar, max 4 items + one primary. It reads as part of the same system because it
  uses the same tokens, and as *secondary* because it floats and is smaller.
- iPad ≥ 768 / desktop: the existing Kobra sidebar. Same order and icons as the tabs.

## 5. Staff surfaces

Counsellor and Admin use the same app bar and the same tab-bar/sidebar pattern (their own
destinations). Log out is never a top-corner button on a phone: it lives in an Account/overflow
menu. Every section reachable on desktop must be reachable on a phone.
