# Google Play Console — listing and declarations

Everything needed to publish NextStepUni on Play, translated from the App Store
submission material (`docs/app-store-listing.md`) into Play's forms. Paste-ready.

**Account:** Nextstepuni Limited (organisation) · Account ID 7217671962208373647
**Package:** `com.nextstepuni.app`
**Bundle to upload:** `android/app/build/outputs/bundle/release/app-release.aab` (43.7 MB)
Rebuild with the command in [android-release.md](./android-release.md) — `JAVA_HOME` is mandatory.

---

## Store listing

**App name** (≤30) — `NextStepUni`

**Short description** (≤80):
```
Science-backed Leaving Cert revision, built on real examiner marking schemes.
```

**Full description** (≤4000):
```
NextStepUni is the Leaving Cert study partner that teaches you how to learn — not just what to learn.

Built around the science of how memory and motivation actually work, NextStepUni turns revision into a clear, personalised plan for your subjects, your goals, and your exam date.

LEARN THE STRATEGIES TOP STUDENTS USE
80+ interactive modules break down evidence-based techniques — spaced practice, retrieval, interleaving, beating exam stress — into short, hands-on lessons you can use the same day.

GROUNDED IN REAL EXAMINER INSIGHT
Our exam content is built from State Examinations Commission marking schemes and Chief Examiner reports — so you practise the way your paper is actually graded, and learn exactly where marks are won and lost.

PERSONALISED TO YOU
Tell us your subjects, levels, target grades and exam start date, and NextStepUni tailors your modules and study plan around them. Set a "North Star" goal for life after school and keep it in view.

TRACK REAL PROGRESS
Activity rings, streaks, points and topic-mastery tracking show how far you've come and what to revisit next — without the overwhelm.

DESIGNED WITH YOUR SCHOOL
NextStepUni is delivered through participating schools. Your guidance counsellor can support your progress, and you can cheer on and learn from classmates.

YOUR PRIVACY COMES FIRST
No ads. No tracking. No advertising identifiers. We never sell your information. Read our full Privacy Notice at nextstepuni-app.web.app/privacy.html

Start studying smarter today.
```

**Category:** Education · **Tags:** study aids, exam prep
**Email:** nextstepuniinfo@gmail.com
**Website:** https://nextstepuni-app.web.app/
**Privacy Policy URL:** https://nextstepuni-app.web.app/privacy.html

---

## Graphics — all prepared in `~/Downloads/_cap/play-shots/`

| Asset | Spec | Status |
|---|---|---|
| App icon | 512×512 PNG | Export from `ios/App/App/Assets.xcassets/AppIcon.appiconset/AppIcon-512@2x.png` (1024×1024 — resize to 512) |
| Feature graphic | 1024×500 | `feature-graphic-1024x500.png` ✅ |
| Phone screenshots | 2–8, max 2:1 ratio | `home / progress / modules-mind / launchpad / module-interior` at 1398×2796 ✅ |

The screenshots were captured at 1290×2796 for the App Store, which is 2.17:1 —
**over Play's limit that the long side may not exceed twice the short side.** They
have been padded to 1398×2796 (exactly 2.00:1) using each image's own background
colour, so no content was cropped and the padding is invisible.

---

## Data safety

Derived from `compliance/DPIA.md` and the Apple privacy label — the same facts in
Play's shape.

**Does your app collect or share any of the required user data types?** Yes.
**Is all data encrypted in transit?** Yes (HTTPS / Firebase).
**Do you provide a way for users to request that their data be deleted?** **Yes** —
in-app: Settings → Account → **Delete Account**, which erases the account and all
associated data. There is also a self-service data export in the same screen.

| Data type | Collected | Shared | Purpose | Required? |
|---|---|---|---|---|
| Name | Yes | No | App functionality, Account management | Required |
| Email address | Yes | No | App functionality, Account management | Required |
| User IDs (Firebase UID) | Yes | No | App functionality, Account management | Required |
| App interactions (module progress, sessions, points) | Yes | No | App functionality | Required |
| Other user-generated content (reflections, free-text answers) | Yes | No | App functionality | Optional |
| Other info (school, year group) | Yes | No | App functionality | Required |

**Shared = No throughout.** Firebase processes this data on our behalf as a
processor; under Play's definitions that is not "sharing" with a third party.

**Not collected:** location, financial info, health, contacts, messages, photos,
files, calendar, browsing history, installed apps, device identifiers for
advertising. **No advertising SDKs are bundled.**

---

## Content rating (IARC questionnaire)

Category: **Utility / Productivity / Education**. Answer **No** to violence,
sexual content, profanity, controlled substances, gambling, and horror.

**User interaction:** answer honestly but precisely — peer interaction exists and
is **preset, not free-text**. Students may send classmates kudos chosen from a
fixed list (`kudosData.ts`), and a limited public profile shows first name,
avatar, school, goal category and decorations. **Students cannot post arbitrary
text visible to other students.** Reflections and written answers are private to
the student and their school guidance counsellor. No unrestricted web access, no
location sharing, no user-to-user file sharing.

Expected outcome: PEGI 3 / Everyone.

---

## Target audience and content

**Age groups:** 13–15, 16–17, 18+ (Leaving Certificate students are typically 15–18).

⚠️ Selecting any under-18 group places the app under Google Play's **Families
policy**. What that requires of you here:
- No ads — true, the app serves none.
- No advertising IDs or third-party ad SDKs — true, none bundled.
- Data practices appropriate for children, matching the Data safety form above.
- Content appropriate for the declared ages — true.

**Do you want your app to be included in the "Designed for Families" programme?**
Not required for a 13+ audience. Declining keeps the listing simpler.

**Appeal to children:** the store listing must not be designed primarily to
attract children under 13. It isn't — it's explicitly a Leaving Cert product.

---

## App access

The app **requires sign-in**, so Play needs credentials or review will fail at
the login screen. Under "App access", choose **All or some functionality is
restricted** and provide:

```
Name:        Demo student account
Username:    appreview@nextstepuni.app
Password:    NextStep-Demo-2026
Instructions: Sign in with the credentials above to reach the full app. This is a
seeded demo student ("Aoife Brennan", 6th year, 5 subjects, 5 completed modules)
with populated progress. NextStepUni is delivered through participating Irish
secondary schools; in normal use accounts are provisioned via the school with
parental consent obtained at enrolment.
```

If that account is ever deleted during review, re-seed it with
`scripts/seed-demo.mjs`.

---

## Other declarations

- **Ads:** No, the app contains no ads.
- **Government app:** No.
- **Financial features:** None.
- **Health apps:** No.
- **News app:** No.
- **COVID-19 contact tracing:** No.

---

## Known gaps in this Android release

- **No Google Sign-In.** `signInWithPopup` has no popup inside the Capacitor
  webview; adding it needs a native plugin plus the release signing SHA-1
  registered in Firebase. v1 ships with email and password. Sign in with Apple is
  iOS-only by design and is correctly hidden on Android.
- **Release signing SHA-1** (for later, when wiring Google Sign-In):
  `C4:7E:DE:68:CD:DF:96:23:5F:9F:DE:9B:E4:00:FE:09:D8:A1:13:FE`
- The Android shell has had none of the device testing the iOS build received.
  Install the AAB on a real Android phone before rolling out to production.
