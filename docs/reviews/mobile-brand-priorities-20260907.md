# Mobile brand priorities — implementation

P01–P07 are implemented on `codex/mobile-brand-priorities-20260907`, based on the approved Launchpad headers. P08 is excluded; no WIP-specific redesign or tool removal is included.

| Priority | Result |
| --- | --- |
| P01 | The original star character replaces the puffin in runtime screens. Module completion uses white, charcoal and orange, immediate Continue/Review actions, safe-area spacing and modal focus handling. Completion counts and North Star text remain. |
| P02 | Kanban tasks have readable full-width stages on phones and three columns on wider screens. Native selection menus support touch and keyboard movement. Done counts derive from the tasks, so moving a task back and forth cannot inflate the total. |
| P03 | Cornell main notes, cues and summary stack on phones, with labelled 16px fields and room to write. Wider screens retain cues beside main notes. Check/reset retain their behaviour; feedback explains that it checks structure rather than assessing scientific accuracy. |
| P04 | Shared subject controls use white surfaces, readable counts and clear scope selection. Retained tool surfaces replace cream with white; neutral grey remains for functional tracks. Existing charcoal tool headers and semantic feedback colours remain. The mobile Study entry also has an opaque white action area. |
| P05 | Insights leads with a recorded observation and links to Study, Timetable or the study record. Coloured stock-icon tiles are removed. Copy distinguishes session frequency/duration from productivity and self-reported confidence from exam outcomes. Existing analytics and thresholds remain. |
| P06 | The guide includes ten real current mobile captures, expandable images, readable copy, persistent Next/Back controls and direct tool actions. Desktop captures remain available on desktop. |
| P07 | Subject lessons render nested bold, italics, highlights and citations. Missing glossary descriptions produce emphasis without an empty tooltip. Malformed notation is preserved once. Curriculum source files are unchanged. |

## Validation

- Production and test TypeScript checks passed.
- Targeted Vitest checks passed for activities, every subject paragraph/bullet/commitment, guide navigation, insight evidence/actions, onboarding, study exit, Paper Trail navigation and study loop, Launchpad guidance, curriculum registry and Mark Bank preservation/deck behaviour.
- Browser checks covered 320, 393 and 430px mobile widths, typed Cornell notes and feedback, guide expansion/deep links, and dark mode. Cornell fields measured 238/311/348px respectively, all at 16px, without horizontal page overflow. Kanban stages measured 272px at a 320px viewport.
- Production Vite build passed. Existing bundle-size/dynamic-import warnings remain.
- Debug iOS build passed with Xcode for the iPhone 17 Pro simulator. Capacitor assets were synced and the exam figure corpus pruned using the repository script. Installed and launched successfully with the existing simulator account preserved.
- The Paper Trail archive opened the integrated document viewer with Paper/Scheme, Answers and Tools controls. The remote PDF did not finish loading during the browser check, so this is navigation verification rather than full live PDF rendering verification.

The simulator build is for review. This change has not been submitted to the App Store.
