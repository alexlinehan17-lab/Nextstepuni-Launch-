# Approved mobile design — 21 September 2026

This is the working app, using its existing localhost demo account. Run `npm run dev -- --host 127.0.0.1 --port 5202`, open `/output/mobile-editorial-20260921/index.html` directly. The preview automatically loads its sample account on every visit, refresh and screen change; no login is needed. The same-origin development iframe activates the mobile design at 320, 390 or 430 CSS pixels. This preview is not part of the production build.

## Applied choices

- Editorial orange rule on Home, Progress, Study, Journey and Launch; existing Lucide icons.
- Journey's DM Sans for mobile headings; original serif numbers and labels-above-number Progress stats.
- Five-section Progress selector, outlined subject picker and underline Week/Month/Year tabs.
- Original Launchpad search and scrolling category controls, compact tool rows, original artwork (including the Future Finder telescope).
- Compact tool name/artwork in the top bar. A dismissible introduction on the first visit, remembered per tool and account on this device. Nested tool mastheads no longer repeat it.
- Mark Bank: stacked subject/level controls, practice entry, then searchable topic groups. No card/curriculum content changes.
- Points Passport: original large score card and calculations, underline section controls.
- Future Finder: Wayfinder illustration and editorial discovery choices, connected to the existing 42/72-question flow.
- Planner: Star Crew blocks, underline day/week controls, readable week agenda, expandable explanation; existing scheduling and actions.
- Paper Trail: compact header, underline collection selector, original archive/search/saved-paper flows.
- Insights: compact header and cohesive heading typography; existing evidence and actions.
- Study timer, Year Plans, Learning Paths, Module list, Module worlds and Lesson reader unchanged apart from the shared bottom-navigation selection style.

## Deeper Progress work

All subjects are visible in mobile confidence, with each average opening into its recorded reflections. Subject allocation no longer silently stops at six. Secondary evidence is expandable. Full mock totals retain all-subject scope and open into their actual grades. Milestones shows the all-time record without weekly filters. Subject and period selections survive section changes.

Readiness now joins canonical subject IDs through the curriculum registry. This restores Irish/Irish (Gaeilge) and Applied Maths/Applied Mathematics matches without changing stored records or inventing missing topics.

## Validation

TypeScript application and test checks, ESLint and production build. Targeted analytics, mobile navigation, tool-introduction, Points Passport, Paper Trail, timetable and Mark Bank preservation tests. New regressions cover first-visit/dismissal/return/account isolation/storage failure, all-subject confidence, canonical readiness aliases and filter preservation across all five Progress sections.

Browser checks use the local demo only, at 320/390/430 CSS pixels. JPEG screenshots in this folder are actual browser captures, not proposed mockups. They do not establish native iPhone behaviour. The earlier native exam-date alignment check remains outstanding.
