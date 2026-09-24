# Data Protection Impact Assessment

NextStepUni Learning Lab — Year 2 PwC Empowering Futures sponsorship

Document status: DRAFT for legal review
Prepared by: NextStepUni Ltd
Date: 2026-04-29

---

## 1. Description of the processing

### 1.1 Nature, scope, context, purposes

NextStepUni Ltd ("the Processor") operates an educational web application ("the Learning Lab") that delivers a structured study-skills programme to Irish secondary school students preparing for the Leaving Certificate State examinations. The application is a single-page web app (React 19 + TypeScript) backed by Google Firebase services (Firebase Authentication, Cloud Firestore, Firebase Hosting, Firebase Cloud Functions).

The processing is undertaken in the context of a CSR sponsorship from PwC Ireland under the Empowering Futures programme. PwC Ireland funds access for students attending DEIS schools in the Dublin region; PwC Ireland does not receive student-level personal data and is not a party to the data processing chain. **Reviewer note: this is the legal position the Processor is asserting; legal counsel should confirm that the absence of any aggregate-data feed to PwC has been validated against the executed sponsorship agreement.**

Year 1 (pilot, 2025/26 academic year) processed approximately 534 students across a small number of DEIS schools. Year 2 is targeted at approximately 2,000 students.

The purposes of processing are:

- to authenticate students and Guidance Counsellors and persist their account state;
- to deliver instructional content (43 educational modules across 7 thematic categories — see `courseData.ts`, `moduleRegistry.ts`);
- to capture student responses to module exercises so that progress is preserved between sessions;
- to operate a spaced-repetition study timetable (an SM-2 deterministic algorithm — see `components/timetableAlgorithm.ts`) personalised to the student's subject choices and target grades;
- to operate a CAO course-recommendation feature (the "Future Finder" — see `components/futureFinderAlgorithm.ts`) which scores Irish higher-education courses against the student's stated interests, values and predicted points;
- to operate a gamification layer (points, achievements, streaks, "Peer Island" decorative state) intended to sustain engagement;
- to operate a peer-support layer (anonymous "Flares", "Teachbacks", "Kudos", "Gifts") scoped to students within the same school;
- to give Guidance Counsellors at each school visibility of their own students' progress, allow them to record private notes and key dates, and allow them to initiate password resets.

### 1.2 Categories of personal data

The following inventory records the principal student-facing collections from
the original assessment and the programme-measurement additions. It is no longer
claimed as an exhaustive current-build inventory; a full collection audit is a
release gate for the final Year-2 DPIA.

**`users/{uid}`** — one document per authenticated user.

- `name` (string, ≤50 chars; firestore.rules:26)
- `avatar` (string, DiceBear seed identifier, ≤100 chars; firestore.rules:28)
- `school` (string, ≤50 chars; firestore.rules:30)
- `yearGroup` (`'5th'` or `'6th'`, written during onboarding; App.tsx:385)
- `role` (`'student'` | `'gc'` | `'admin'`; not writable by clients — firestore.rules:25)
- `isAdmin` (boolean; not writable by clients — firestore.rules:24)
- `needsPasswordChange` (boolean; written only by Cloud Function `resetStudentPassword` — functions/src/index.ts:62)
- The user's email address is held in Firebase Authentication (not in this Firestore document).

**`progress/{uid}`** — a single large document per student. Fields written by the application include:

- per-module progression: `{ [moduleId]: { unlockedSection: number } }` for up to 43 modules
- `pointsData.totalEarned`, `pointsData.totalSpent` (firestore.rules:74–80)
- `gamification.unlockedAchievements` (string[]; firestore.rules:82–85)
- `subjectProfile`: array of `{ name, level, isMaths }` items, plus `examStartDate`, `restDays`, `defaultBlockDuration`, `yearGroup`, `createdAt`, `updatedAt`
- `studySessions` (array, append-only): `{ dateKey, blockId, subjectName, sessionType, durationMinutes, pointsEarned, timestamp }`
- `studyDebriefs` (array, append-only): self-rated confidence before/after, perceived grade, free-text reflection
- `topicMastery.{subject}.{topic}`: `{ confidence, updatedAt, source, lastDebriefDate, sm2Quality }`
- `unifiedMockResults` (array): `{ id, label, date, entries:[{subjectName,grade,level}], totalPoints, timestamp }`
- `timetableCompletions.{dateKey}`: array of completed block IDs
- `timetableStreak`: `{ currentStreak, longestStreak, lastStreakDate }`
- `northStar` (object): the student's stated post-secondary aspiration ("North Star")
- `islandState`: 3D scene placement state, purchase history (timestamps)
- `cosmeticUnlocks`: avatar seeds, theme colours, card styles unlocked
- `flareCounts`, `rescueCount`, `lighthouseLevel` (peer-support gamification metrics)
- `strategyMastery`, `sm2States`, `teachBacksSeen`, `dismissedGuides`

**`settings/{uid}`** — UI preferences only: language, avatar seed, dark mode toggle, accent theme, card style, default work minutes, flares animation toggle, dashboard visibility, essentials mode toggle (firestore.rules `match /settings/{userId}`).

**`responses/{userId}`** — `{ [moduleId]: responseData }`. Free-text responses to module exercises. Some prompts elicit reflective writing; see Section 1.4 on special category data.

**`notifications/{userId}`** — system and GC-broadcast notifications: message, read flag, timestamps. **Access-control gap, see Section 3.**

**`gcNotes/{schoolId}/students/{studentId}`** — a Guidance Counsellor's free-text private notes about an individual student: `{ notes, updatedAt }` (GCStudentDetail.tsx:191).

**`gcSettings/{schoolId}`** — `{ dismissedAlerts: { alertId: boolean } }` (GCDashboard.tsx:145).

**`gcEvents/{schoolId}`** — `{ events: [{ title, date, type }] }` (school calendar).

**`kudos/{kudosId}`** — `{ fromUid, fromName, toUid, school, messageId, createdAt }` (useKudos.ts:89).

**`gifts/{giftId}`** — `{ fromUid, toUid, itemId, school, status, createdAt }`.

**`teachbacks/{teachbackId}`** — `{ authorUid, school, subject, explanation (≤500 chars), createdAt, helpfulCount }`.

**`flares/{flareId}`** plus subcollection `flares/{flareId}/responses/{responseId}` — peer SOS questions and replies. The flare carries `{ senderUid, school, subject, question (≤500 chars), status, createdAt, expiresAt, responseCount }`. Responses carry `{ responderUid, text (≤1000 chars), helpful, createdAt }`.

**`programmeEvents/{eventId}`** — time-limited pseudonymous, structured usage
events described in `PROGRAMME_MEASUREMENT_REGISTER.md`; no name, email, free
text, answer text or exact study duration. Client access is denied.

**`analyticsSubjects/{uid}`** — server-only mapping from account UID to the
separate random analytics identifier used in `programmeEvents`.

**`programmeEventRateLimits/{bucketId}`** — server-only daily event count and
48-hour expiry used to prevent event flooding.

In addition, the Firebase Authentication subsystem holds, for every user: email address, hashed password, last-sign-in timestamp, account creation timestamp, and any provider linkage. The application uses the email-and-password provider only.

### 1.3 Categories of data subjects

- **Students**: minors aged 15–18, attending DEIS schools in Dublin; data subjects in respect of all `users`, `progress`, `settings`, `responses`, `notifications`, peer-collaboration collections, and the entries about them in `gcNotes`.
- **Guidance Counsellors**: adult employees of the participating schools; data subjects in respect of their own `users` document and authentication record.
- **NextStepUni administrative users**: a single hard-coded administrator account (`admin@nextstep.app`; AuthContext.tsx:94–103, firestore.rules:40–41) used internally for support.

### 1.4 Special category data (GDPR Article 9)

The application does not deliberately solicit health, racial, ethnic, religious, biometric, sexual orientation or political opinion data. However, the following routes carry an inherent risk that students will *volunteer* health-adjacent data, in which case the resulting record falls within Article 9:

- The "Reframing Catastrophic Thoughts" module (ReframingProgressModule.tsx, CatastrophicThinkingModule.tsx) prompts students to type negative thought patterns relating to exam stress.
- The "Affirming Values" module (AffirmingValuesModule.tsx) and the "Grammar of Grit" module (TheGrammarOfGritModule.tsx) elicit personal reflection.
- The "Emotional Intelligence" and "Hope Protocol" modules (EmotionalIntelligenceModule.tsx, HopeProtocolModule.tsx) frame self-awareness exercises.
- The post-session debrief (StudyDebrief.tsx, used after every study block) accepts free-text reflection where students may write about anxiety, fatigue, concentration difficulty or family circumstances.
- The "Flare" feature lets students post free-text questions to same-school peers, where they may disclose the cause of a struggle.

**Risk position**: free-text fields cannot be reliably constrained to non-Article-9 content. The Processor must treat the `responses`, `progress.studyDebriefs`, `flares`, `flares/.../responses` and `gcNotes` collections as potentially containing Article 9 data and apply Article 9 protections (explicit consent or another Article 9 lawful condition; tighter access controls; clear retention policy). **Reviewer note: legal counsel should confirm whether the school's *in loco parentis* function combined with parental consent at school level is a sufficient Article 9 condition under the Data Protection Act 2018, or whether explicit student consent is required.**

### 1.5 Data flows

Logical data flow:

```
Student browser ────HTTPS───▶ Firebase Hosting (CDN, global edge)
       │
       ├──HTTPS──▶ Firebase Authentication (email + password)
       │
       ├──HTTPS──▶ Cloud Firestore (region us-central1; see Section 6)
       │
       ├──HTTPS──▶ Cloud Functions (resetStudentPassword, changeOwnPassword)
       │
       ├──HTTPS──▶ api.dicebear.com (avatar SVG; sends only the avatar seed)
       │
       └──HTTPS──▶ fonts.googleapis.com / fonts.gstatic.com / cdn.tailwindcss.com
                   (static asset delivery, no user identifiers)

GC browser ────────HTTPS───▶ same Firebase services
                              + can call Cloud Function resetStudentPassword
```

The application makes no calls to any LLM, ML inference API, third-party analytics SDK, advertising network, error-reporting service or third-party telemetry service. It does use a first-party, server-mediated programme-measurement stream described in `PROGRAMME_MEASUREMENT_REGISTER.md`: structured pseudonymous events are stored inside the same Firebase project, raw client access is denied, selected cohorts below five students are suppressed, and event TTL is 400 days. See AI_GOVERNANCE_SCHEDULE.md for AI detail.

### 1.6 Retention periods

**This remains a broader known gap for core student records.** Automated TTL is configured for anonymous feedback/rate limits and first-party programme-measurement events/rate limits, but not yet for the full `progress`, `responses` and historical account-data lifecycle. Specifically:

- Firestore TTL field overrides exist for `anonymousFeedback`, its rate limits, `programmeEvents` (400 days) and `programmeEventRateLimits` (48 hours). Core student-progress retention is still governed by account erasure rather than an automatic end-of-programme schedule.
- No Cloud Function or scheduled task purges old `progress`, `responses` or `studyDebriefs`.
- The `flares` collection has an `expiresAt` field set 24 hours from creation (useFlares.ts), but **no process deletes flares once they expire**; the field is used only for client-side filtering of "active" flares.
- In-product export and cascade erasure are implemented, including programme
  measurement. Automatic end-of-programme deletion for core records remains a
  gap (see Section 4 mitigation row M-RETN).

The Processor's intended retention policy is: **TBC — Alex to confirm intended retention period for student progress data after the student leaves school, and the retention period for free-text reflective content.** A common edtech default is to retain account data for the duration of the student's enrolment in the programme plus 12 months for support/audit, after which all personally identifying fields are erased. Until this is decided and *implemented*, the Processor is in effective indefinite retention, which is not defensible under Article 5(1)(e).

---

## 2. Necessity and proportionality

### 2.1 Lawful basis

The Processor's working position is that processing is carried out under:

- **Article 6(1)(e) — public interest task**: the school is the Controller, acting *in loco parentis* to deliver a state-curriculum-aligned educational service. **Reviewer note: this presumes the Department of Education / individual schools accept Controller status; legal counsel must confirm with at least one participating school's data protection lead before relying on this basis.**
- combined with **parental consent at the point of school enrolment** in the programme, in line with Irish DPC guidance on processing children's data and Article 8 GDPR.
- For Article 9 categories that may incidentally arise in free-text reflections (Section 1.4), **Article 9(2)(g) — substantial public interest (education)** is the proposed condition, supported by Section 41 of the Data Protection Act 2018. **Reviewer note: legal counsel to confirm.**

The Processor (NextStepUni Ltd) acts under Article 28 as Processor on behalf of each participating school as Controller. PwC Ireland is a sponsor, not a Controller and not a Processor; PwC receives no student-level data.

### 2.2 Data minimisation analysis

| Category | Necessary for purpose? | Minimisation comment |
|---|---|---|
| Name | Yes | Used for the in-app greeting and for GC dashboards. Could be reduced to first-name-only. |
| Email address | Yes (auth) | The application uses email + password authentication. |
| School | Yes | Required to scope GC access and same-school peer features. |
| Year group | Yes | Drives content sequencing. |
| Subject profile (subjects, levels, target grades, exam date) | Yes | Required input to the SM-2 timetable algorithm. |
| Study sessions, debriefs, topic mastery | Yes for progress; arguably excessive for study sessions retained indefinitely. | See retention gap. |
| Mock exam results | Yes | Drives recommendations and GC visibility. |
| Free-text reflections in modules and study debriefs | Pedagogically yes; carries Article 9 risk (Section 1.4). | Consider reflection-text retention reduction or local-only storage. |
| Cosmetic unlocks, island placements, purchase history | No (not necessary for educational purpose). | Could be moved to `localStorage` only. |
| Peer-support content (flares, teachbacks, kudos, gifts) | Yes for stated purpose. | 24-hour TTL exists in semantics but is not enforced (Section 1.6). |
| Avatar seed | Yes (UI). | Sent to DiceBear (Section 1.5) and may be a pseudonym from a fixed list. |

### 2.3 Proportionality

The application's purposes (educational delivery to a defined cohort of consenting school children) are legitimate and proportionate. Two specific proportionality concerns are raised in Section 3:

- The `progress/{uid}` document is readable by *any same-school authenticated peer* under firestore.rules:60–63. The pedagogical justification is the "Peer Island" feature, but the rule grants access to the full progress document, not only the fields rendered in that feature. This is over-broad relative to purpose.
- The `users/{uid}` document is readable by any same-school peer under firestore.rules:19–22, which lets a student enumerate the cohort of every other student at their school.

---

## 3. Risk assessment

Risks are scored on likelihood × severity (Low / Medium / High) using the Irish DPC's standard matrix. The "audit reference" column points to the source-of-truth document.

### R1 — Cross-user data leak via permissive Firestore read rule on `progress`

- Status: **Closed 2026-04-30**. Identified during Year 2 governance preparation. The two-step remediation:
  1. The offending rule block was removed from `firestore.rules`, denying all peer reads of `/progress/{userId}` (DPIA risk surface eliminated).
  2. A new `/islandPublic/{uid}` Firestore collection and two Cloud Function projection writers (`onProgressWritten`, `onUserWritten`) were introduced so the Peer Island feature can continue to operate against a minimal, auditable public projection rather than the full `progress` document. Per-placement `purchasedAt` timestamps and the raw `purchaseHistory` are not in the projection (replaced by a pre-computed `score`); academic, behavioural, and reflective fields are not in the projection at all.
  - Full design and field-by-field rationale: `compliance/PEER_ISLAND_REFACTOR_PLAN.md`.
  - Code changes (2026-04-29) and end-to-end deploy chronology (2026-04-30, including a post-deploy fix to the `/islandPublic` rule for query verification, and the hosting deploy that completed the refactor): `compliance/REMEDIATION_LOG.md`.
  - Smoke test verified end-to-end on 2026-04-30 with two same-school test accounts. The backfill script was deliberately not run; new projections are populated organically as students perform progress writes.
- **Product decision (Alex, 2026-04-29):** the `category` field (NorthStarCategory — values such as `college`, `independence`, `prove-myself`, `creative`, `change-maker`) is included in the `/islandPublic` projection, deliberately and not silently. The rationale recorded for the audit trail: this is a soft, self-chosen aspiration field (not a special category under GDPR Article 9); the value is already implicit in the rendered island theme (water colour, scene preset), so excluding the data field without removing the visual would be cosmetic rather than meaningful; and peer-visibility of the North Star is intrinsic to the Peer Island feature's social-motivation purpose. Privacy impact assessed as low.
- Description (as identified): `firestore.rules` previously contained, inside `match /progress/{userId}`, a "Peer Islands" rule (formerly at lines 60–63 of the rules file) that allowed any authenticated student to read any other same-school student's full `progress` document, including study sessions, topic mastery and reflective debrief text.
- Likelihood (as identified): **Medium** — no special skills required; could be triggered from the browser console by any logged-in student.
- Severity (as identified): **High** — exposed Article 9-adjacent reflective content; permitted cohort-wide enumeration of grades and confidence ratings.
- Overall risk (as identified): **High**.
- Audit reference: `docs/firestore-audit.md` (section "Peer Island progress reads"); `compliance/PEER_ISLAND_REFACTOR_PLAN.md` for the rebuild.

### R2 — `notifications` collection access-control gap

- Description: firestore.rules `match /notifications/{userId}` (around line 113) currently grants `read, create, update` to the user *and* to any GC at the matching school. Per the linked audit, earlier iterations of this rule allowed broader access; the Processor must verify that the present rule does not still allow cross-user writes from non-GC peers. The Processor flags that the architecture (peer-writable notifications) is fragile.
- Likelihood: **Medium**.
- Severity: **Medium-High** (impersonation of GC notifications to a student).
- Overall risk: **Medium-High**.
- Audit reference: `docs/firestore-audit.md`. Status: **partially mitigated** in the current rules (the Cloud-Function-only path is preferred but not enforced).

### R3 — Role escalation / school spoofing at registration

- Description: at registration the client supplies `school` as a free-text string; firestore.rules:30 limits length but does not validate against an approved list. A student could choose "Belvedere College" if they wished to gain visibility into that school's peers.
- Likelihood: **Medium** (trivial for a curious student; requires manipulating the registration form).
- Severity: **High** (defeats school-scoped access controls for peer collaboration and GC supervision).
- Overall risk: **High**.
- Audit reference: `docs/registration-audit.md`. Status: **open**.

### R4 — Progress document fabrication

- Description: firestore.rules:71–85 only validates `pointsData` and `gamification.unlockedAchievements` on update. A student can write arbitrary `topicMastery`, `subjectProfile`, `studySessions`, `studyDebriefs`, `unifiedMockResults` content to their own document.
- Likelihood: **Low** (requires intentional misuse via developer tools).
- Severity: **Low–Medium** (data integrity, not data confidentiality; affects the student's own record only).
- Overall risk: **Low–Medium**.
- Audit reference: `docs/firestore-audit.md`. Status: **open**.

### R5 — AI-generated harmful content reaching a student

- Description: the application **does not currently use any LLM**. README.md:18 and CLAUDE.md:22 reference `GEMINI_API_KEY`, but the bundle contains no Gemini SDK and no `generateContent` call (verified by exhaustive grep). All "AI-feeling" features (study timetable, course recommendation) are deterministic.
- Likelihood (today): **negligible**.
- Likelihood (forward-looking): **Medium** if Gemini integration is reactivated for content generation aimed at minors.
- Severity if realised: **High** (hallucinated advice to a 16-year-old, especially on exam strategy or career choice, is a direct safeguarding risk).
- Overall risk: **Low today; High if reactivated without controls.**
- Audit reference: this DPIA, AI_GOVERNANCE_SCHEDULE.md.

### R6 — Account takeover via guessable temporary password

- Description: the GC-initiated password reset Cloud Function (`functions/src/index.ts:53–57`) generates an 8-character alphanumeric temporary password (`abcdefghjkmnpqrstuvwxyz23456789`, vowels and confusables removed). This is returned to the GC in plaintext (`functions/src/index.ts:68`), who must convey it to the student out-of-band. There is no audit log of the reset event beyond Firebase Auth's internal logs, and no notification is sent to the student.
- Likelihood: **Low** (requires GC compromise or social engineering).
- Severity: **Medium-High** (full account access; access to reflective content).
- Overall risk: **Medium**.
- Audit reference: `functions/src/index.ts:16–70`.

### R7 — Third-party (DiceBear) link disclosure

- Description: the avatar URL (`utils/authUtils.ts:30–33`) sends the avatar seed (a value chosen from a fixed list of pseudonyms — `AVATAR_SEEDS`) to `api.dicebear.com`. The seed is not the student's name. However, the request includes the user's IP address and standard browser headers, which DiceBear may log.
- Likelihood: **High** (every page load that renders an avatar).
- Severity: **Low** (no PII in the URL beyond IP + user-agent; seed is pseudonymous).
- Overall risk: **Low**.
- Mitigation already in place: PWA cache (`vite.config.ts:58–63`) reduces request frequency to once per 30 days per avatar.

### R8 — Data residency outside the EEA

- Description: Firebase project `nextstepuni-app` is on Firestore default region. `firebase.json` does not configure a region; the project was created on `us-central1` (Iowa). Personal data of EU minors is therefore stored in the United States.
- Likelihood: **Certain** (this is the current configuration).
- Severity: **Medium** (lawful with Standard Contractual Clauses, but requires a documented Article 46 transfer mechanism and explicit notice).
- Overall risk: **Medium**.
- Audit reference: `firebase.json`; cross-checked against the Firebase console. **TBC — Alex to confirm exact Firestore region from the Firebase console**, since the absence of a `location` key in `firebase.json` does not by itself prove the region is `us-central1`.

### R9 — Data-subject rights workflow completeness and scale

- Description: the app now provides authenticated JSON export and cascade
  erasure for students, with GC/admin-authorised equivalents and retry audit
  records. Rectification/objection routing remains organisational, and the
  synchronous pilot export/erasure path must be replaced or load-tested before
  high-volume programme measurement is enabled.
- Likelihood: **Medium** until the Year-2 asynchronous workflow is complete.
- Severity: **Medium**.
- Overall risk: **Medium**.
- Audit reference: `functions/src/dataRights.ts`,
  `components/account/DataRightsModal.tsx`.

### R10 — Indefinite retention

- Description: see Section 1.6.
- Likelihood: **Certain**.
- Severity: **Medium**.
- Overall risk: **Medium**.

### R11 — Free-text content moderation

- Description: peer-to-peer content (`teachbacks`, `flares`, `flares/.../responses`) is published to same-school peers without server-side moderation. Firestore rules cap `explanation` to 500 chars, `question` to 500 chars and `text` to 1000 chars but do nothing about the *content* (firestore.rules:171, 194, 227).
- Likelihood: **Medium**.
- Severity: **Medium-High** (bullying, sharing of personal information, disclosure of self-harm ideation).
- Overall risk: **Medium-High**.
- Mitigation in place: GC has read access to all same-school flares/teachbacks. **No notification flow alerts a GC when a flare is posted.**

### R12 — DEV-mode artefacts in production builds

- Description: registration audit (`docs/registration-audit.md` H2) flagged a "DEV skip-login" path visible in production. The Processor must confirm this is no longer reachable. The current `App.tsx` does include an `onDevRankUp` prop on KnowledgeTree (visible in the recent commit history). **TBC — Alex to confirm whether the DEV rank-up tester is gated by an environment check.**
- Likelihood: **Low** (requires a user to find a hidden control).
- Severity: **Low** (gamification-only; cannot grant role).
- Overall risk: **Low**.

### R13 — Re-identification or over-collection in programme measurement

- Description: repeated behavioural events about a child can become identifying
  or enable unfair profiling when joined with account, school, year-group or
  free-text data. Small cohorts create an additional inference risk even when
  names are absent.
- Necessity: the bounded event set is required to report reach, activation,
  sustained participation and flow quality, and to decide which student journeys
  need improvement. Screen replay, raw text, exact location and cross-site data
  are not necessary and are excluded.
- Safeguards: a separate random analytics identifier; server-owned cohort
  metadata; exact-schema validation; no names/email/text/answers/exact duration;
  server-only raw collections; aggregate-only admin response; primary and
  complementary small-cell suppression plus secondary cohort suppression;
  300-event daily abuse cap; 400-day TTL; disabled-by-default client/server gate;
  complete access/export and erasure coverage; purpose register and child-facing
  disclosure.
- Likelihood after safeguards: **Low**.
- Severity: **Medium** (children and longitudinal behaviour remain involved).
- Overall residual risk: **Low-Medium**.
- Review trigger: any new event/field, individual score, equality characteristic,
  verified grade/outcome linkage, retention increase or third-party analytics
  integration requires a fresh assessment and controller approval.

---

## 4. Mitigation measures

### 4.1 Technical mitigations already in place

| ID | Measure | Source-of-truth |
|---|---|---|
| T1 | TLS in transit for all Firestore, Auth and Cloud Function traffic | Firebase default |
| T2 | Encryption at rest (AES-256) for Firestore data | Google Cloud platform default |
| T3 | Password hashing in Firebase Authentication (scrypt) | Firebase default |
| T4 | Role/admin fields immutable from client (`firestore.rules:24–25, 33–34`) | firestore.rules |
| T5 | Default-deny on undeclared Firestore paths (firestore.rules `match /{document=**}` end of file) | firestore.rules |
| T6 | Field-length validation for user-supplied strings (name ≤50, school ≤50, avatar ≤100, explanation ≤500, question ≤500, text ≤1000) | firestore.rules:26–30, 171, 194, 227 |
| T7 | Append-only achievements; monotonic-only points totals; +1000 per-write points cap | firestore.rules:74–85 |
| T8 | Pinned `+1` increment on `helpfulCount` and `responseCount` to prevent inflation | firestore.rules:180, 208 |
| T9 | School-scoped peer features (kudos, gifts, teachbacks, flares) — sender's school must equal recipient's school | firestore.rules `match /kudos`, `match /gifts`, `match /teachbacks`, `match /flares` |
| T10 | GC password reset gated by server-side role check in Cloud Function | functions/src/index.ts:33–48 |
| T11 | Forced-reset flow requires `needsPasswordChange` flag before allowing self-change | functions/src/index.ts:95–97 |
| T12 | Reserved email patterns (`admin@nextstep.app`, `gc-*@nextstep.app`) blocked at registration | LoginPage.tsx (registration validation) |
| T13 | Daily/weekly client-side rate limits on kudos, gifts and flares (3/day, 10/week) | useFlares.ts:82–86 (validation client-side; **note: not enforced in rules**) |
| T14 | Static avatar seeds drawn from a fixed list (no free-text PII reaches DiceBear) | utils/authUtils.ts (`AVATAR_SEEDS`) |
| T15 | PWA caching reduces external requests to DiceBear / Fonts to once per 30 days per asset | vite.config.ts:58–63 |
| T16 | No third-party analytics SDK, no error-tracking SDK, no LLM SDK present in the bundle; first-party measurement is schema-bounded and server-mediated | verified by source-tree grep; `PROGRAMME_MEASUREMENT_REGISTER.md` |

### 4.2 Technical mitigations required (not yet implemented)

| ID | Measure | Maps to risk |
|---|---|---|
| T-NEW-1 | Restrict same-school `progress` reads to a small allow-list of fields (name, points total, current streak, public achievements). Implement via a server-side projection in a Cloud Function rather than a Firestore rule, since rules cannot project. | R1 |
| T-NEW-2 | Restrict same-school `users` reads to `name`, `avatar`, `yearGroup` only — not the full document. | R1 (cohort enumeration) |
| T-NEW-3 | Validate `school` against an allow-list of participating schools at registration (Cloud Function callable, or Firestore rule with a maintained `allowedSchools` doc). | R3 |
| T-NEW-4 | Add field-level validation for `topicMastery`, `subjectProfile`, `studySessions`, `studyDebriefs`, `unifiedMockResults` in `firestore.rules`. | R4 |
| T-NEW-5 | Move all GC-initiated notification writes to a Cloud Function and remove the rules-level `create` path on `notifications`. | R2 |
| T-NEW-6 | Audit-log every password reset (who, when, target student) to a Firestore `audit` collection writable only by Cloud Functions. Notify the student by email immediately on reset. | R6 |
| T-NEW-7 | Configure Firestore TTL on `flares` (`expiresAt` field) so expired flares are auto-deleted. Implement a scheduled Cloud Function (or app-level cron) to purge `studySessions` older than the agreed retention period. | R10 |
| T-NEW-8 | Replace or load-test the implemented synchronous JSON export/cascade-erasure functions for Year-2 event volume; use an asynchronous file/deletion job if limits are exceeded. | R9 |
| T-NEW-9 | Configure or migrate to a Firestore database in `europe-west1` or another EEA region; document the resulting transfer position in DPA Schedule 6. | R8 |
| T-NEW-10 | Server-side moderation pass on flares/teachbacks/responses (a simple keyword/regex filter is the floor; an LLM moderation pass would be appropriate but introduces R5 considerations). Notify GC when a flare contains language indicative of distress. | R11 |
| T-NEW-11 | Enable Firebase App Check (reCAPTCHA Enterprise / DeviceCheck) on Firestore and Cloud Functions to prevent SDK-spoofed clients. | Multiple |
| T-NEW-12 | Remove or environment-gate the DEV rank-up tester. | R12 |

### 4.3 Organisational mitigations

- **Incident response**: a written incident response plan is **TBC — Alex to confirm** whether one exists. Industry-standard requirements: 24-hour internal escalation, 72-hour DPC notification under Article 33, communication template for affected schools.
- **Staff training**: NextStepUni Ltd is a small operator. Annual GDPR refresher and Article 8/9 children's-data training for all engineering staff is recommended; status **TBC**.
- **DPO**: under Article 37, an organisation that processes children's data on a large scale should appoint a Data Protection Officer. **Reviewer note: legal counsel to advise whether ~2,000 minors qualifies as "large scale"; a part-time external DPO is the proportionate option if so.**
- **Vendor management**: a signed Data Processing Addendum with Google (Firebase) is required. Status **TBC**. DiceBear is a public unauthenticated API; a vendor risk note acknowledging that DiceBear is in the data path even for low-sensitivity purposes is advisable.
- **Sub-processor register**: see DPA_SCHEDULES.md Schedule 4.
- **Data retention policy**: written policy required to back T-NEW-7. Status **TBC**.
- **Periodic Firestore-rules review**: a security review every release cadence (quarterly minimum), independent of feature work.

### 4.4 Residual risk after mitigation

Assuming all T-NEW items in Section 4.2 are implemented and the organisational items in Section 4.3 are documented:

| Risk | Pre-mitigation | Post-mitigation |
|---|---|---|
| R1 cross-user progress read | High | Low |
| R2 notifications gap | Medium-High | Low |
| R3 school spoofing | High | Low |
| R4 progress fabrication | Low-Medium | Low |
| R5 AI harmful content (forward-looking) | High | Medium (residual; depends on guardrails when reactivated) |
| R6 account takeover via reset | Medium | Low |
| R7 DiceBear disclosure | Low | Low |
| R8 data residency | Medium | Low |
| R9 DSAR workflow | Medium | Low |
| R10 indefinite retention | Medium | Low |
| R11 free-text moderation | Medium-High | Medium (residual; moderation is best-effort) |
| R12 DEV artefacts | Low | Negligible |
| R13 programme-measurement re-identification/over-collection | Medium-High | Low-Medium |

---

## 5. Sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Data Protection Officer (NextStepUni Ltd) |  |  |  |
| Engineering Lead |  |  |  |
| External legal counsel |  |  |  |
| Reviewing Controller (school DP lead) — sample |  |  |  |
| PwC Risk/Legal acknowledgement |  |  |  |

---

## 6. Document control

- Source code reviewed: commit `0ac6be4` on branch `main`.
- Companion documents: AI_GOVERNANCE_SCHEDULE.md, DPA_SCHEDULES.md, SUMMARY.md.
- Internal audit references: `docs/firestore-audit.md`, `docs/registration-audit.md`, `docs/round-trip-nav-audit.md`, `docs/nav-audit.md`.
