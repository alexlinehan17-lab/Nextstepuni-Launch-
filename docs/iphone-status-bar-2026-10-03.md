# iPhone status-bar correction — 3 October 2026

The installed app displayed a full-width black strip above its content. The
bootstrap disabled status-bar overlay without setting a background colour, so
the Capacitor plugin inserted its default black native view. This was reproduced
in the existing iPhone simulator installation.

The iOS app now draws behind a transparent status bar. Native configuration
sets this at startup and the JavaScript bootstrap preserves it. Standalone Home,
Study and Mark Bank session headers receive native-only safe-area padding.
Capacitor's text styles were also reversed: `LIGHT` supplies dark text for a
light background and `DARK` supplies light text for a dark background. Onboarding
and the Study timer declare their own appearance while mounted, then restore the
account theme when dismissed.

Verification:

- Production web build, app TypeScript check, changed-source lint, and config
  TypeScript check passed.
- 42 tests passed across Study setup/exit, avatar settings, onboarding appearance,
  mobile guest onboarding and desktop onboarding.
- A fresh Xcode iPhone simulator build passed. The rebuilt app's account screen
  showed a continuous background in both light and dark mode.
- An isolated copy of the simulator build exercised the live status-bar API:
  overlay remained enabled; light/dark text styles, a screen override, and its
  restoration all passed. Its safe-area measurement was 62px. Home, Study setup,
  the ink timer and the Mark Bank session header measured 84/78/82/74px top
  padding; the account brand controls began at 78px. These padding measurements
  used CSS fixtures, not authenticated walkthroughs of those screens.
- Local evidence is in `output/iphone-status-bar/`. Temporary QA instrumentation
  exists only in a separate simulator copy; the release source and build contain
  none of it. The clean rebuilt app was reinstalled after verification.

This is a local source and simulator correction. It requires a new native iOS
release to reach installed phones; no App Store build was uploaded or submitted.
