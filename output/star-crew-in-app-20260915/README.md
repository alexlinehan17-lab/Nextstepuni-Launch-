# Star Crew — placement proposal

[Open the updated study preview](http://localhost:3047/output/star-crew-in-app-20260915/index.html#study).

## Current direction

- **Account:** white panels, the original eight personal characters, and an orange selection ring. No tick badge.
- **Subject onboarding:** the approved subject artwork and three selectable alternatives to ticks: Added text (recommended), Orange card, and Underlined name. Selection remains a labelled button with `aria-pressed`.
- **Grade goals:** subject names and grade controls, with no avatars.
- **Home:** the existing Today’s plan section, with subject artwork replacing the letter-code slot. No new home layout or subject-card section is proposed.
- **Study:** the existing study setup screen and its two-column subject grid. Enlarge the subject cards and replace their coloured dots with subject avatars. Other study controls, the sidebar, headings and responsive layout come from the existing app component.

## Sizes

| Surface | Desktop | Mobile |
| --- | --- | --- |
| Personal choices | 88px | 62px |
| Subject onboarding row | 52px | 48px |
| Home plan subject | 44px | 44px |
| Study subject card | 64px icon, minimum 96px card height | 44px icon, minimum 86px card height |
| Study plan row | 36px | 36px |

Long subject names can make a mobile card taller. Both columns stretch together; subject labels remain visible. All artwork uses the existing measured framing and retains its white circular background.

## How the preview preserves the app

`existing-screens.tsx` renders **HomeNextStep** and **StudySessionSetup** directly. A preview-only adapter places the artwork into their existing icon slots. The only study-card styling changes are size, padding, spacing and text wrapping. Production components are not modified.

The Home tab intentionally shows the existing plan section as a placement detail. The surrounding home page is outside this design change. The Study tab renders the actual setup component rather than a newly designed study flow. Start Session and secondary navigation mark the boundary of this local preview; their production behavior is unchanged.

## Interaction and data

Choose a personal character, switch the selection treatment, add or remove subjects, then view the current study screen. The chosen subjects carry into the study cards. Selecting a study subject updates the existing session summary. Duration and work-type controls use their existing callbacks with in-memory preview state.

All student and plan data are illustrative. Choices live in memory and reset on refresh. There are no account, authentication or Firestore writes. The walkthrough jumps between selected existing onboarding stages; it does not remove the other stages or account requirements.

## Production integration points

- `components/LoginPage.tsx`, `components/Avatar.tsx` and `components/UserProfileMenu.tsx`: original personal eight, local asset resolution and existing fallback behavior.
- `components/onboarding/DesktopSetup.tsx` and `components/onboarding/SetupFlow.tsx`: subject selection artwork only; no grade-goal avatars.
- `components/HomeNextStep.tsx`: replace subject-letter codes in the current rows.
- `components/study/StudySessionSetup.tsx`: larger subject cards with artwork, plus inline icons in its plan rows. Keep the existing screen composition and session flow.

Use canonical subject IDs for a shared artwork mapping. Existing labels are aliases, not identifiers. This preview reads artwork metadata and does not introduce curriculum content.

## Files

- `index.html`, `preview.css`, `preview.js`: account, subject and grade previews, selection comparison controls and screen navigation.
- `existing-screens.html`, `existing-screens.tsx`, `existing-screens.css`: isolated preview of current app components with subject artwork.
- Artwork: `../star-crew-20260915/` and `../star-crew-subjects-20260915/`, reused without pixel edits.
