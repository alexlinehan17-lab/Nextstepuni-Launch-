# App Store Connect — Listing Metadata (draft)

_Draft for the NextStepUni iOS submission. Fill these into App Store Connect once the company account + app record exist. Character limits noted; trim before pasting._

## Identity
- **App Name** (≤30): `NextStepUni`
  - Discoverability alt (if you want keywords in the name): `NextStepUni: Leaving Cert` (25)
- **Subtitle** (≤30): `Leaving Cert study, smarter`
- **Primary category:** Education
- **Secondary category:** (optional) Productivity
- **Bundle ID:** `com.nextstepuni.app`

## URLs
- **Privacy Policy URL** (required): `https://nextstepuni-app.web.app/privacy.html`
  - Switch to `https://nextstepuni.com/privacy.html` once that domain is live.
- **Support URL** (required): `https://nextstepuni-app.web.app/` (or a dedicated support/contact page)
- **Marketing URL** (optional): `https://nextstepuni.com`

## Promotional text (≤170, updatable anytime without review)
> Study the way examiners actually mark. Personalised, science-backed strategies for every Leaving Cert subject — built on marking schemes, not rote memorisation.

## Description (≤4000)
> **NextStepUni is the Leaving Cert study partner that teaches you _how_ to learn — not just what to learn.**
>
> Built around the science of how memory and motivation actually work, NextStepUni turns revision into a clear, personalised plan for your subjects, your goals, and your exam date.
>
> **Learn the strategies top students use**
> 80+ interactive modules break down evidence-based techniques — spaced practice, retrieval, interleaving, beating exam stress — into short, hands-on lessons you can use the same day.
>
> **Grounded in real examiner insight**
> Our exam content is built from State Examinations Commission marking schemes and Chief Examiner reports — so you practise the way your paper is actually graded, and learn exactly where marks are won and lost.
>
> **Personalised to you**
> Tell us your subjects, levels, target grades and exam start date, and NextStepUni tailors your modules and study plan around them. Set a "North Star" goal for life after school and keep it in view.
>
> **Track real progress**
> Activity rings, streaks, points and topic-mastery tracking show how far you've come and what to revisit next — without the overwhelm.
>
> **Designed with your school**
> NextStepUni is delivered through participating schools. Your guidance counsellor can support your progress, and you can cheer on and learn from classmates.
>
> **Your privacy comes first**
> No ads. No tracking. No advertising identifiers. We never sell your information. Read our full Privacy Notice at nextstepuni-app.web.app/privacy.html.
>
> Start studying smarter today.

## Keywords (≤100 chars total, comma-separated, no spaces after commas)
`leaving cert,study,revision,exam,LC,study skills,study planner,exams,grinds,maths,irish,exam prep`

## What's New (version 1.0)
> First release of NextStepUni — science-backed, examiner-grounded study for the Leaving Cert. We'd love your feedback at nextstepuniinfo@gmail.com.

## Age rating questionnaire — recommended answers
- Violence / sexual content / profanity / drugs etc.: **None**
- **Unrestricted web access:** No
- **User-Generated / peer content:** **Minimal and NOT free-text.** As of 2026-07 the teach-back and SOS-Flare features were removed. The only remaining peer interactions are: (a) **preset kudos** — students send classmates a message chosen from a fixed list (`kudosData.ts`), with **no free-text input**; and (b) a **limited public "island" projection** — first name, avatar, school, chosen goal *category*, and preset decorations/score. Students cannot post arbitrary text that other students see. Reflections and free-text module answers are **private** (visible only to the student and their school guidance counsellor — never to classmates).
  - **App Review Guideline 1.2 (UGC):** Because there is no free-text peer content, the filter/report/block requirements are largely satisfied by design — preset messages cannot carry abuse, and there is nothing free-text to moderate. The audience is closed and school-supervised (a guidance counsellor oversees each student). Explain this in the review notes rather than claiming a report/block UI the app doesn't need.
  - When Apple's age questionnaire asks about **communication / sharing user-generated content**, answer honestly: limited, preset, non-free-text peer interaction within a closed school group. Expected rating **4+ / 12+**.

## App Privacy ("nutrition label") — from compliance/DPIA.md
Declare **Data Collected → Linked to the user → used for App Functionality** (NOT for Tracking). No data used for tracking; no third-party advertising SDKs.

| Data type | Category | Linked | Purpose |
|---|---|---|---|
| Name | Contact Info | Yes | App Functionality |
| Email Address | Contact Info | Yes | App Functionality, Account |
| User Content (reflections, free-text module answers) | User Content | Yes | App Functionality |
| User ID (Firebase UID) | Identifiers | Yes | App Functionality |
| Product Interaction (module progress, sessions, points) | Usage Data | Yes | App Functionality |
| Other (school name, year group) | Other Data | Yes | App Functionality |

- **Tracking:** None.
- **Third-party SDKs that collect data:** None bundled. (Sign in with Apple uses Apple's system framework; auth/data via Firebase as processor.)
- Note: a `PrivacyInfo.xcprivacy` privacy manifest may be requested at upload — Firebase's SDK ships its own; the app itself collects nothing requiring "required reason API" declarations beyond standard.

## Review notes (App Store Connect "Notes for Reviewer")
Suggested text:
> NextStepUni is an educational study app delivered through participating Irish secondary schools for Leaving Certificate students. Accounts are normally provisioned via the school with parental consent obtained at enrolment. For review, a demo account is provided below. Peer interaction is limited to students within the same school and is supervised by a school guidance counsellor: students can send classmates preset "kudos" messages (chosen from a fixed list — there is no free-text peer posting) and see a limited public profile (first name, avatar, chosen goal category, decorations). A student's written reflections and answers are private to them and their counsellor.
>
> Demo login: **appreview@nextstepuni.app** / **NextStep-Demo-2026**
> (Seeded demo student "Aoife Brennan" — 6th year, 5 subjects, 5 completed modules, populated progress. This is a demo-only account.)

## Pre-submission asset checklist
- [ ] App icon 1024×1024 (already in the build) — upload in App Store Connect
- [x] iPhone 6.7" screenshots (1290×2796) captured — `~/Downloads/_cap/ns-shots2/`: `home`, `progress`, `modules-mind`, `launchpad`, `module-interior` (Training Hub). Fully populated via the seeded demo account.
- [x] **Privacy Policy URL live** — https://nextstepuni-app.web.app/privacy.html (deployed)
- [x] **Reviewer demo account created + seeded** — appreview@nextstepuni.app / NextStep-Demo-2026
- [x] Export-compliance handled in Info.plist (`ITSAppUsesNonExemptEncryption=false`) — no per-upload question.
