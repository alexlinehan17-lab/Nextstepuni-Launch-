# App-wide UI/UX audit against `nsu-design` — November 2026

Companion to the review page in this folder (`index.html`, published privately as an artifact) and
the skill at `.claude/skills/nsu-design/`. This file holds the code-level findings the
implementation phases work from.

**How it was produced.** Static reading of the whole codebase, plus the running app (demo account,
390×844) on nine student screens: Home, My Progress, Launchpad, Future Finder, Paper Trail, Mark
Bank, Journey, Study setup, Modules. Staff dashboards, in-session screens (timer, pause) and module
interiors were read in code only. Items marked *(inferred)* were reasoned from the code and not
observed on a device.

## 1. Root cause: two design languages

| | Kobra / "Paper & Ink" | Legacy "chunky" |
|---|---|---|
| Borders | 1px hairline (`--hairline`, `--nsu-edge`) | `2px solid #1A1A1A` |
| Depth | Soft layered shadows or none | Hard offset `shadow-[4px_4px_0_0_#1A1A1A]` (~268 uses, 70 files) |
| Primary button | Ink fill, radius 12, 48–56 high (`.auth-live-primary`, `.setup-continue`, `.product-action--primary`) | Orange fill + ink border + hard shadow, or orange pill |
| Lives in | Login, onboarding, sidebar, settings, home, study, Future Finder, Paper Trail | Most modules, `ui/ChoiceControl`, `ui/SystemState`, older tools, pop-ups (quick tour, Journey welcome) |

Counts: 8 primary-button recipes; ~25 distinct radii; `#1a1a1a` hardcoded ×773 in 134 files;
`bg-[#F26B1F]` ×56 (the old orange — the token is now `#eb692a`); three sans faces in play (DM
Sans, ABC Diatype under four aliases, Apercu Mono) plus Roboto Mono and Departure Mono.

CLAUDE.md's "Visual Design System — Module Components" section specifies the legacy language
(2px ink borders, orange pill CTA). Adopting Paper & Ink for modules means rewriting that section.

## 2. Safe areas

Setup is correct: `viewport-fit=cover` (`index.html:6`), `--sat/--sar/--sab/--sal` (`index.html:61-64`),
Capacitor `ios.contentInset:'never'`, `StatusBar.overlaysWebView:true`. The failures are all
components positioning themselves at the top edge.

**Confirmed**
1. Admin log-out — `.admin-masthead` is `position:sticky; top:0` with no inset
   (`components/admin/admin-dashboard.css:52`); button `AdminDashboard.tsx:676-678`, top-right at ≤1400px (`css:121`).
2. Pause-screen sound control — `.study-break-tools{position:absolute;right:28px;top:22px}`
   (`components/study/study-motion.css:19`, `top:16px` at ≤700px `:52`), positioned against
   `.study-break-experience`, so `native-ios.css`'s padding on `.study-break` never moves it.
   `.study-room-stage .study-break` padding (`study-motion.css:18,53`) probably also overrides the
   inset by cascade order *(inferred)*.
3. Island Mode intro — `journey/JourneyWelcome.tsx:28-45`, `journey/journey-welcome.css:3-7,33-35`:
   fixed inset-0 overlay, 12px padding, card `max-height:calc(100dvh - 24px)`, 36px close button
   (also under the 44px target).

**Same fault, other screens**
- `GCDashboard.tsx:533` mobile header (Log Out top-right); `:626` student tray; `gc/GCStudentDetail.tsx:268` sticky header (back `:342`, close `:320`).
- `SiteGuide` — `site-guide.css:1,40-41`, close `SiteGuide.tsx:215`.
- `RankUpModal.tsx:110` — `absolute top-6 right-6`.
- `MyDirection.tsx:72` — `.direction-navigation` (`student-screens.css:77,108`).
- `App.tsx:940` achievement toast (`fixed top-4`), `OfflineBanner.tsx:46` (`fixed top-0`), `Toast.tsx:154` (`fixed top-3`).
- `max-h-[90vh]` centred modals: `CollegeCompass.tsx:130`, `FutureFinder.tsx:1333`, `FutureFinderResults.tsx:773`.
- Paper Trail viewer side panels at ≥768px: `PaperTrail/Viewer.tsx:1773,1819,2037…` (`fixed top-0 h-full`).
- Marginal: `YearPlansView.tsx:98`, `WipTools.tsx:35` (`pt-16` ≈ 64px vs ~59–68px inset).
- Double inset: `AppRouter.tsx:872` banner + `learning/reader.css:1`.

**Fix shape:** three owners of the top edge — `ui/PageHeader` (app bar), `ui/ModalFrame` (sheet on
phones), a new session frame for study/review/quiz — and a ratchet test on
`fixed|sticky|absolute` + `top` outside them. `native-ios.css` per-class patches then go away.

## 3. Back / Close / Exit

Nine styles: shared `BackButton` (6 direct + 7 via `PageHeader`); muted text links "← All subjects"
(15 files, e.g. `DiagramVault.tsx:126`, `ExaminersChair/index.tsx:615`, `PaperTrail/ReviewSession.tsx:166`);
bespoke icon squares (`WipTools.tsx:39`, `CutContentPage.tsx:224`, `MyDirection.tsx:72`,
`gc/GCStudentDetail.tsx:342`, `YourPossibleLife.tsx:55`); shadow pills (`JCComingSoon.tsx:54`,
`AppRouter.tsx:874`); `ChevronLeft` + "Back" (`FutureFinder.tsx:493,904`, `FutureFinderResults.tsx:456`,
`ComebackEngine.tsx:1037`); Kobra ghost buttons (`ModuleLayout.tsx:283`, `PaperTrail/Viewer.tsx:1362`
— an arrow used as Close); large text backs (`InsightsView.tsx:31`, `PaperTrail/index.tsx:836`,
`JourneyView.tsx:356`); four shapes of ✕; LogOut-icon exits.

Screens with more than one way back:
1. Module opened from Journey — banner (`AppRouter.tsx:874`) + `ModuleLayout.tsx:262` "Back to modules" (both go to Journey; label wrong).
2. Every Launchpad tool sub-view — fixed header back (`InnovationZone.tsx:933/939`) + the tool's own text link; `ReviewSession` shows two (`:166`, `:188`); plus the first-visit intro ✕ (`ToolMasthead.tsx:23`).
3. Future Finder quiz — header back + "Pause" (`FutureFinderPaper.tsx:151`) + "Back to introduction / Previous question" (`:156`).
4. Journey — wordmark and "← Home" both call `onBack` (`JourneyView.tsx:351,356`).
5. Study timer — ✕ "Leave" and "Minimise" both exit (`StudySessionTimer.tsx:58`); pause adds two more (`StudyBreak.tsx:93,100`).
6. Library — Home menu item (`Library.tsx:208`) + BackButton (`:459`).

Also: no in-app back calls `nav.goBack()` any more; every back pushes a new history entry
(`InnovationZone.tsx:933`). `docs/iz-back-button-bug.md` and `docs/round-trip-nav-audit.md` are
stale, and the tool↔grid ping-pong may be back *(not verified)*.

## 4. Headers

Eleven implementations: `InnovationZone.tsx:923-963` (fixed tool header); `launchpad/ToolMasthead.tsx:61-94`
(the black card; `ToolIntroduction` on mobile at `InnovationZone.tsx:1074`, once per uid+tool);
`ToolHeader.tsx:52`; Future Finder's own `.ff-masthead` + `.ff-steps` + `aside.ff-journey`
(`FutureFinderPaper.tsx:129,134,144-149`); `ModuleLayout.tsx:261-270`; `ui/PageHeader.tsx`;
Paper Trail `.pt-toolbar` (`PaperTrail/index.tsx:787,958-961`, `archive.css:145` pushes "Saved"
right with `margin-left:auto`) and viewer `.pvc-top`; Mark Bank `.mb-masthead` and session bar
(`SessionScreen.tsx:3017-3046`); Journey `header.student-nav` (`JourneyView.tsx:350-375`);
Admin `.admin-masthead`; GC mobile bar (`GCDashboard.tsx:533`).

Future Finder's duplicated icon is `FutureFinderPaper.tsx:129` — it does not use `ToolMasthead`,
so the context that hides nested mastheads on mobile does not catch it.

## 5. Known issues — where they live

| Issue | Location | Cause |
|---|---|---|
| My Progress section picker does nothing | `dashboard/ProgressSectionPicker.tsx:17,29-31,50` | Root closes on `blur` when `relatedTarget` is outside. iOS does not focus a button on tap, so the menu unmounts before the option's `onClick` *(inferred from code; matches known WebKit behaviour)*. Close on outside pointer-down instead, or use a sheet. |
| My Progress subject filter / Insights popovers | `dashboard/progress/SubjectPicker.tsx`, `ProgressCharts.tsx:18-20` | No static cause found; needs a device check. `index.css:1917-1927` fixes the portal wrapper for Select only, not Popover. |
| My Progress spacing | `progress.css:146` (30px margins), `DashboardView.tsx:508` (`gap-4`), `mobile-editorial.css:36-37` (20px), milestones 20–24px (`refinements.css:146-170`) | Four different gaps, none ≥ 2× the inner gap. |
| Start Session feedback | `study/StudySessionView.mobile.tsx:278-289`, `StudySessionSetup.tsx:297`, `study-kobra.css:349-358` | `startHint` exists but renders as 12px text under the card; button is `disabled`. |
| Study timer | `study/StudySessionTimer.tsx:144`, `study-session.css:160-186` (`#ff862c` dot, bar, Pause); mini pill `StudyMiniTimer.tsx:30-45`, `study-mini-timer.css` | Three orange elements together; a fourth orange value. |
| Journey bar | `journey/JourneyView.tsx:449-478`, `journey/paper/paper.css:334-368, 999-1026, 1683-1720` | A second bar above `MobileBottomNav` (`App.tsx:78-118`); different radius, border, type, background; conflicting `bottom` rules. |
| Paper Trail character | `PaperTrail/index.tsx:962-965`, `.pt-subject-art` 155×155 (`paper-kobra.css:8`) | Hero-sized on a task screen. |
| Paper Trail arrows | `archive.css:51,57,98` (orange) vs `PaperSubjects.tsx:30-53` (ink) | Two arrow colours; `.pt-home-links` is a 2-col grid holding one button (`:58`). |
| Future Finder selection | `FutureFinderPaper.tsx:148`, `future-finder-details.css:47-48` | Static; no Motion import; auto-advances after 280ms. |
| Mark Bank length | `MarkBank/MarkBankLibrary.tsx` (masthead, toolbar, notes, index strip, full topic list, practice card on one page; `mark-bank-library.css:285-317`) | One page, six jobs. State: `groupId`, `selectedId`, `query`, `availableOnly`, `amount` (`:61-63`). |
| Counsellor on phones | `GCDashboard.tsx:469` (`hidden md:flex` sidebar), `:351-358` (sections unreachable on mobile), `gc/GCOverview.tsx:1136` (`grid-cols-3`), `:1569`, `GCHandInGrid.tsx:109` (`min-w-[640px]`) | Desktop layout with the nav removed. |
| Admin on phones | `AdminDashboard.tsx:655-680`, `admin/admin-dashboard.css` | 8 nav items in a 4-col grid; 40px log-out; `AdminFeedbackInbox`, `AdminFunnelPanel`, `AdminGcAccessPanel` have no dark styles. |
| "Practice" button oversized | Not found. `.lp-practice-entry` and `.mb-compact-practice` are dead CSS. | Needs a screenshot from the owner. |

Dead code found along the way: `components/Onboarding.desktop.tsx` (1,641 lines, unimported),
`auth-paper.css`, `account-entry.css`, `PeerIslandsList`, `TrainingHub`, `_handleBack*` in `App.tsx:868-870`,
`.dashboard-mobile .dashboard-filters select` (`mobile-editorial.css:42`).

## 6. Dark mode

Mechanism: Tailwind `darkMode:'class'`, `html.dark` toggled in `hooks/useSettings.ts:115,124`.
The zinc scale is overridden in `tailwind.config.ts` (950 `#131313`, 900 `#191919`, 800 `#262626`).

**Page background has four values:** body and app root `dark:bg-zinc-950` = `#131313`
(`index.html:291`, `App.tsx:937`); `--bg-page #09090b` (`index.html:89`); `--surface-canvas #151515`
(`index.css:129`, what students see); Kobra `--background` = `#0a0a0a` (anything portalled outside
`.student-sidebar-page`).

**Surface tiers:** ~11 canvas values, ~17 card values, ~16 raised/soft values. `--surface-soft`
alone has three different dark values (`index.css`, `index.css:1912`, `module-cards.css:6`).
Tailwind usage: `dark:bg-[var(--module-surface)]` ×315, `dark:bg-zinc-900` ×243, `zinc-800` ×176,
`zinc-700` ×53, `zinc-950` ×21.

**Canonical set (already the most used; pinned by `test/darkModeTokens.test.ts`):**
`--surface-canvas #151515`, `--surface-paper #202020`, `--surface-soft #282624`,
`--surface-raised #2B2927`, `--hairline #34312E`, `--outline-soft #494541`.
Everything else aliases to these: `--mb-*`, `--deck-*`, `--module-*`, `--nsu-surface`, `--ss-*`,
`--sc-*`, `--wi-*`, `--al-*`, `--cw-*`, `--ap-*`, `--journey-panel`, `--legal-paper`,
`--student-paper`, `--control-paper`, Kobra's `--background/--card/--popover/--muted/--sidebar/--shell*`,
and the legacy `--bg-*` block in `index.html:71-101`.

**Mismatch sites**
- Today's plan: `.crew-empty` (`crew-experiences.css:5,33`) paints `--surface-paper` edge to edge with no radius on the `#151515` shell (`HomeNextStep.tsx:29`, `KnowledgeTree.tsx:166-172`). Also used by `CareerPaths.tsx` and `SpacedRepetitionTimetable.tsx`.
- The compat layer (`index.css:379`, `!important`) overrides authored `dark:bg-zinc-900/950`, so `ui/ModalFrame.tsx:96`, `StudyPassportModal` (`:87,91`), and the mobile headers in `ModulesView.tsx:558,647` and `LearningPathsView.tsx:113` render `#202020` on a `#151515` page.
- Inline white maps to two different card colours (`index.html:161` → `#18181b`; `index.css:260` → `#202020`).
- Bottom nav `App.tsx:94` is `#191919`; `UserProfileMenu` sheet `#191919`; Kobra `--sidebar #18181b`, `--card #171717`.
- Own canvases: study `#202020`, Journey `#202020`, Mark Bank `#141414`, Ways In `#141413`, Paper Trail viewer `#131313` (header resolves to `#0a0a0a`), Answer Desk `#141414`, quiz stage `#222220`, legal `#242720`, coursework `#181818`, figure zoom `#0f0f0e`.

**Light-only surfaces:** 60 `bg-white` with no dark pair (31 files), 227 inline light backgrounds
(56 files), 61 CSS white rules without a `.dark` rule. Worst: `PaperTrail/Viewer.tsx:1605` (audio
bar, portalled, stays white) and `:1951-2661`; `VaultQuestionCard.tsx:316-449`; `MockExamBuilder`;
`ReviewSession`; `Flashcards`; `ProgressDashboard`; `MarkBank/SessionScreen.tsx:3660,3827`;
`FutureFinder.tsx:795-814`; `FutureFinderResults.tsx:347-366`; `PointsPassport.tsx:667,824`;
`ComebackEngine.tsx:963-1073`; `CatchUpLane/index.tsx:236,245`; `ExamReps/index.tsx:161-377`;
`ExaminersChair/index.tsx` (49 sites); `gc/GCStudentDetail.tsx:302-382`; `gc/GCOverview.tsx:55,1993`.

Earlier audits (`docs/dark-mode-audit-2026-08-20.md`, `-09-22.md`, `contrast-sweep-RESUME.md`)
were contrast passes; none unified surfaces. Still open from them: six of twelve "world" colours
fail AA with white text; AdminDashboard never verified live; native iOS/Android not checked.

## 7. Screen grades

| Grade | Screens |
|---|---|
| Good already | Login; onboarding; sidebar; settings |
| Minor refinement | Home; Modules and categories; module reader shell; study setup; study room and timer; Future Finder; Insights, Learning Paths, Year Plans, Your Setup; My Direction |
| Component / layout redesign | My Progress; study pause and breathing; Launchpad tool shell; Paper Trails (home, selection, viewer on iPad); Journey / Island; all phone pop-ups (tour, rank-up, site guide, College Compass, Future Finder results); toasts and offline banner; older tools (Comeback Engine, Catch-Up Lane, Command-Word Reflex, Examiner's Chair, Exam Reps) |
| Rebuild for mobile | Mark Bank; Counsellor dashboard; Admin dashboard |

Not yet walked individually: the ~58 module interiors, Points Passport, War Room, College Compass,
Coursework Studio, Listening Studio, Topic Atlas, Diagram Vault, Irish Oral Trainer.

## 8. Implementation phases

1. **Foundations** — four dark surfaces with every feature palette aliased; spacing/radius/motion
   scales; app bar, sheet (bottom sheet on phones), session frame, sheet-picker; button levels with
   the not-ready state; ratchet tests (top-edge positioning, dark literals, back affordances).
2. **Safe areas and navigation sweep** — the 15 top-edge sites; one Back per screen; Back pops;
   remove the Launchpad black card and intro; all phone pop-ups become sheets.
3. **Named screens** — My Progress; Start Session; timer; pause; Future Finder header and
   selection; Paper Trail home and bar; Journey bar and intro; Today's plan.
4. **Mark Bank** — Today / Browse / Saved with topic screens.
5. **Counsellor and Admin on phones.**
6. **Long tail** — dark sweep (remaining greys, ~60 light-only components); older tools and ~70
   module files off the chunky style; one icon set; iPad list-and-detail pass.

## 9. Owner decisions pending

Direction (Paper & Ink recommended); whether modules move; one sans (ABC Diatype recommended);
timer; Journey bar; Paper Trails character; Mark Bank structure; a screenshot of the Practice button.
