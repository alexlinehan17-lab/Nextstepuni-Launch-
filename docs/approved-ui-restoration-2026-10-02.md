# Approved UI restoration — 2 October 2026

This release restores eight approved areas to the source used by the main-branch deployment. Earlier Hosting-only releases contained much of this work, but their implementations had not been committed to main and were subsequently replaced by CI builds.

## Included

- Final onboarding Dark / Light choice: Dark is preselected, the choice is saved on completion, and the wider previews sit below the reviews in the right column. The existing summary layout remains in place.
- Filled original artwork in dark mode: paired dark assets and an alpha-based pale edge preserve the original colour and filled forms.
- Module reader and interactive exercises: notebook contents, reading progress, section search, source popovers, completion controls, and focused/diffuse exercises.
- My Progress: subject filters, activity/confidence/mock charts, milestones, and the learning record use the current student's data.
- Planner and Study Room: week/day views, block details, plan settings, saved skips, editable to-dos, subject selection, and the study handoff.
- Paper Trail: subject and document selection, question/marking-scheme pairing, and document deep links.
- Onboarding grade menus and interface sound controls, on desktop and mobile.
- Admin navigation's sliding underline, with resize/font loading and reduced-motion support.

## Integration

The release retains the newer Signature cards for notes, the journal, subject setup and locked tools, along with the existing reflection-writing flow and shared back controls. It does not include the separate Future Finder or Mark Bank redesign/content work. Curriculum, exam content, backend permissions, and point-award logic are unchanged.

Editable purchased controls remain in the private local checkout. The app commits only their compiled runtime, scoped CSS and generated TypeScript declarations. A normal build or CI installation does not require that checkout. To refresh these artifacts locally, set `NSU_CONTROLS_SOURCE` and run `npm run build:approved-controls`.

## Verification

Local verification includes production and test type checks, strict lint, the production build, component-library packaging, and the unit suite. The protected PR additionally runs the Firebase emulator rules, dependency audits, Android build, function build and CodeQL analysis before merging. Main's workflow deploys its verified artifact after the backend step.

Fresh browser capture was unavailable in the current automation environment. Existing archived captures were used as design evidence; they are not presented as new captures of this integration.
