# Feedback parked on 17 October 2026

Alex chose what to build from the feedback review on 17 Oct 2026 (in-app inbox, 32 real messages to that date, plus the Marino 12 Oct, Joeys 15 Oct and O'Connells/Larkin 16 Oct sessions). Everything below was **not** picked up that day. Nothing here is lost. Pick items up from this list.

**Being built (not parked):** missing subjects in onboarding (LCVP, PE, every examined language, Foundation level for Maths and Irish, the full LCA list including courses without a written exam); changing your exam date; Mark Bank described as flashcards; notifications, starting with "your study time is up"; the iOS lock-screen timer (Live Activity); Paper Trail completeness (deferred sittings, pre-2010 years, papers for any new subject); classmates' islands for your school year.

## Parked, in the priority order from the review

| # | Item | Raised by | Evidence / notes |
|---|---|---|---|
| 1 | **Students can't get into their accounts at workshops** | Alex, every session | Failed vs successful sign-ins: 296/17 (Marino 12 Oct), 90/22 (Joeys 15 Oct), 110/22 (O'Connells + Larkin 16 Oct). Since #251 every logged failure is `credentials` (wrong email or password): zero lockouts, zero network errors. Likely contributor, unproven: web auth uses `browserSessionPersistence` (`firebase.ts`), so a new tab or a closed browser signs the student out minutes after signing up. First step: a two-minute iPad test (sign up, open a new tab). Option: "Keep me signed in on this device". |
| 2 | **A wrong join code deletes the new account** | Server logs | First-try join-code failures: 13 of 60 sign-ups (15 Oct), 28 of 112 (16 Oct). Security gap: the wrong-guess limit is keyed by uid (`functions/src/schoolAccess.ts`) and the account is deleted on a wrong code, so the count never passes 1. With a memorable code (e.g. `Marino01`) that is guessable. Fix: keep the account and let the student re-enter the code, and count guesses per email or device. |
| 3 | Quiz at the end of a study session | 2 students (16 Oct) | The debrief only says "test yourself in a day or two". Mark Bank cards are filed by topic, so 3–5 on the topic just studied fit. |
| 4 | More Geography in Mark Bank | 1 student | 754 cards live; the paused `claude/geography-audit-20261011` branch has 2015–2026 done (about double). Ship it. |
| 5 | Custom subjects or topics | 1 student | For anything the subject list still misses. |
| 6 | Paper Trail answer data | Alex (15 Oct) | Biology 2024 Q10's scheme area also covers Q11 (audit spillover estate-wide). Music 2026 (LC067ALP006EV) and Japanese 2026 (LC058ALP000BV) answer files are flagged but missing from Storage. |
| 7 | Physics & Chemistry deck in Mark Bank | 1 student | The subject is selectable and has papers, but its Mark Bank deck has no cards yet. |
| 8 | A game as a reward for studying | 1 student | The island link at the end of a session is live. Today's Question from the landing page could become a daily in-app game. |
| 9 | Animal options for the capybara tile | 1 student | Parked by Alex on 14 Oct. |
| 10 | A section for after school | 1 student | The `graduated` year group already keeps access. Product decision. |
| 11 | Studying live with others | 1 student (Aug) | Large. Marked Planned in the inbox. |

## Quick checks (about five minutes each)

- **Island speed on a real iPad.** #235 fixed it in Safari on a Mac but was never tested on a device.
- **Timer on iPad Safari after switching apps.** One student says it stops. The code counts from the wall clock and should catch up.
- **iOS 1.0.7.** Submitted 16 Oct and still showing 1.0.6 on the App Store on 17 Oct. It carries the lost-study-time fix for iPhone users.
- **Admin password.** Change it, since the admin account was left signed in on a school laptop. Sessions were revoked on 15 Oct.

## Housekeeping

- The admin feedback inbox still shows 31 of 32 real messages as New. Mark the shipped ones Fixed and archive the 5 tests.
- Accounts with misspelled school emails (`marinocollge.ie`, `marincollege.ie`, `marino.ie`) can never receive a reset.
- Guidance counsellors haven't yet been shown the counsellor reset tool.
- Check nextstepuniinfo@gmail.com for reset requests from students with older username accounts. 14 failed sign-ins on 16 Oct used a username.

## Decisions still open from the 14 Oct round

- Size of the keep-going bonus, and whether it pays once per session.
- Where the minimised timer returns to (Home or the previous view).
- Where Your setup sits in navigation.

## Considered and left out on purpose

- **LCA students taking a Leaving Cert modern language** on top of their LCA language. The programme allows it, but it's rare. The LCA flow records no grades, so it would add nothing but a duplicate-looking list entry. Students can still use Paper Trail and Mark Bank for it.
- **"Wood technology" for LCA.** It isn't an LCA course: Wood Technology is a Junior Cycle subject. The nearest LCA courses are Craft and Design and Graphics and Construction Studies.
- **2028 subject names as separate subjects.** Construction Technology and Life, Community and Work replace Construction Studies and LCVP Link Modules for students who started 5th year in Sept 2026. The app treats each pair as one subject, so onboarding search finds the new names and the profile keeps the stable name.
