# Dark artwork and surface audit — 22 September 2026

The Home illustrations contained opaque, slightly textured white paper. The
new rank control, notification panel and several recent CSS components also
used white surfaces independently of the existing theme tokens.

## Changes

- Render Star Crew and editorial tool artwork with a shared, inline SVG filter
  in dark mode: remove near-white paper and use white linework while retaining
  orange. Original PNGs and the light-mode rendering remain intact. Explicitly
  light sign-in, onboarding and landing experiences opt out of this treatment.
- Theme the rank control, avatar surround, progress track and notification
  envelope/panel. The rank control's outer background is transparent in dark.
- Theme shared Back buttons, the Progress section dropdown and technique marks.
- Remove the forced white disc behind editorial Crew illustrations; cover the
  Home cards, personal/subject avatars, learning mix, Planner and Future Finder.
- Theme study break/completion/receipt surfaces and fields, including the
  receipt's decorative edges; achievement stamps and empty states; Journey
  welcome/help, navigation, build shelf and dialogs; feedback and its disabled state; first-visit coach marks; and
  Paper Trail's question controls.

## Verification

- Browser checks with the real app and its localhost-only sample account:
  desktop Home, rank control, notifications, avatar settings and feedback;
  mobile Progress and its expanded section selector; Launchpad, Planner,
  Future Finder, Points Passport, Mark Bank, Paper Trail, Study, Journey and
  Insights. Checked artwork with both light and dark appearance.
- Phone layouts reviewed at 390 px; Future Finder also checked at 320 px with
  document width and scroll width both 320 px.
- Study receipt/reflection and break states rendered directly with the real
  components and inert preview callbacks. Confirmed the receipt and its
  decorative edges use the dark palette.
- 71 tests passed across dark tokens, Star Crew, student header/screens,
  Crew experiences, Journey welcome, feedback, student dashboard, Paper Trail
  study loop and mobile coach marks. TypeScript, full ESLint and production
  build pass.

This was a Chrome review with simulated phone widths, not native iOS/Android
or Safari validation. Exam-paper pages, thumbnails and authored diagrams
retain their document colours. Independent light entry/marketing experiences
remain light.

Local review helper and screenshots: `output/dark-mode-audit-20260922/` (not
included in the application build or this commit).
