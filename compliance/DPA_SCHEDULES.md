# Data Processing Addendum — Technical Schedules

NextStepUni Learning Lab — schedules to attach to the DPA legal body

Document status: DRAFT for legal review
Prepared by: NextStepUni Ltd
Date: 2026-04-29
Source code reviewed: commit `0ac6be4` on branch `main`

These Schedules are the technical and operational appendices that attach to the DPA legal text (drafted separately). They describe the actual processing carried out by NextStepUni Ltd ("the Processor") on behalf of each participating school ("the Controller"). Each Schedule is referenced by Article number where possible.

---

## Schedule 1 — Subject matter and duration of processing (GDPR Art. 28(3))

### 1.1 Subject matter

Processing of personal data of secondary-school students attending DEIS schools that are participating in PwC Ireland's Empowering Futures programme, and of the staff (Guidance Counsellors) at those schools, for the purposes of delivering the NextStepUni Learning Lab study-skills programme.

### 1.2 Duration

Processing commences on the date a student account is created and continues for the duration of the student's enrolment in the programme plus a defined retention tail (Schedule 5, Section 5.7) for support and audit. **TBC — Alex to confirm** the tail length; the Processor's recommended position is twelve (12) months after the student's Leaving Certificate, after which all directly identifying fields are erased and any retained study-pattern data is anonymised.

Processing in respect of Guidance Counsellor accounts continues for the duration of their employment at the participating school plus a thirty- (30-) day support tail to assist handover, after which the GC account is deleted.

The Year 2 PwC sponsorship covers the academic year 2026/27. The Processor's contractual commitment to the Controller is for that academic year, plus the retention tail above.

---

## Schedule 2 — Nature and purpose of processing (GDPR Art. 28(3))

### 2.1 Nature

Storage, retrieval, organisation, structuring, alteration, erasure and consultation by automated means, in a multi-tenant cloud environment provided by Google Cloud (Firebase). No manual processing is performed by NextStepUni staff in the ordinary course; staff access is incidental and limited to debugging support requests.

### 2.2 Purposes

Detail in DPIA.md Section 1.1. In summary:

- authentication and account state persistence;
- delivery of 43 educational modules across 7 categories;
- persistence of student answers and reflective content;
- generation of a personalised spaced-repetition study timetable (deterministic SM-2 algorithm);
- generation of CAO course recommendations (deterministic weighted scoring);
- engagement gamification (points, achievements, streaks, decorative state);
- school-scoped peer support (Kudos, Gifts, Teachbacks, Flares);
- Guidance Counsellor visibility into their own students' progress and ability to record private notes, key dates, and initiate password resets.

### 2.3 Operations performed

| Operation | Mechanism |
|---|---|
| Collection | Web form input; client-side computation; Firebase Auth registration |
| Storage | Cloud Firestore documents in collections enumerated in Schedule 3 |
| Retrieval | Firestore client SDK reads, scoped by Firestore Security Rules (`firestore.rules`) |
| Alteration | Firestore client SDK writes and `runTransaction`, scoped by Firestore Security Rules |
| Disclosure to GC | Firestore Security Rules grant read access on `users/{uid}` and `progress/{uid}` to authenticated users with `role == 'gc'` and a matching `school` value |
| Erasure | Cloud Function and GC Dashboard initiate `deleteDoc` on `users/{uid}` and `progress/{uid}`. **Gap: not all related collections are erased; see DPIA Section 4.2 T-NEW-8.** |
| Restriction | Not implemented as a discrete operation. **Gap.** |
| Transmission | Within Google Cloud only, except: outbound HTTPS to api.dicebear.com (avatar SVG), fonts.googleapis.com / fonts.gstatic.com (fonts), cdn.tailwindcss.com (CSS) |

---

## Schedule 3 — Type of personal data and categories of data subject (GDPR Art. 28(3))

### 3.1 Categories of data subject

- Students aged 15–18 attending participating DEIS schools (data subjects in respect of all student-scoped processing).
- Guidance Counsellors employed by participating schools.
- A single NextStepUni administrative user.

### 3.2 Categories of personal data — exhaustive

The following inventory is taken directly from the application source. It is reproduced exhaustively here because it forms the core of the Controller's transparency obligation under Articles 13/14.

**Identity and account data (Firebase Authentication + `users/{uid}`):**

- email address (Firebase Auth)
- password hash (Firebase Auth — scrypt)
- account creation timestamp, last sign-in timestamp (Firebase Auth)
- display name `name` (firestore.rules:26)
- avatar seed `avatar` (firestore.rules:28; pseudonymous)
- school identifier `school` (firestore.rules:30)
- year group `yearGroup`
- role flag `role` (server-controlled)
- admin flag `isAdmin` (server-controlled; only `admin@nextstep.app`)
- password-reset flag `needsPasswordChange` (Cloud-Function-controlled)

**Educational profile (`progress/{uid}.subjectProfile`):**

- subjects taken, with level (Higher / Ordinary / Foundation) and a maths flag
- target grades per subject
- exam start date
- preferred rest days
- default study-block duration (minutes)

**Educational performance and engagement (`progress/{uid}`):**

- per-module section unlock state (43 modules)
- study session log: date, subject, session type, duration, points earned
- post-session debriefs: confidence ratings (0–5), perceived grade, free-text reflection
- topic mastery per subject and per topic, including SM-2 spaced-repetition state
- mock exam results: per-subject grade and level, total points, date
- timetable completion records
- timetable streak data
- Future Finder answer set and ranked recommendation output

**Engagement and gamification (`progress/{uid}`):**

- points earned, points spent
- unlocked achievements
- "North Star" — student's stated post-secondary goal (free text or selection)
- island scene state (decorative)
- cosmetic unlocks
- flare counts, lighthouse level, rescue count

**Communications (`notifications/{userId}`, `kudos/{kudosId}`, `gifts/{giftId}`):**

- system and GC-broadcast notifications: message body, read flag, timestamps
- peer kudos: sender UID, sender name, recipient UID, school, message identifier, timestamp
- peer gifts: sender UID, recipient UID, item identifier, school, status, timestamp

**Peer collaboration (`teachbacks/{teachbackId}`, `flares/{flareId}` and subcollection):**

- teachback: author UID, school, subject, free-text explanation up to 500 characters, timestamp, helpful count
- flare: sender UID, school, subject, free-text question up to 500 characters, status, timestamps, response count
- flare response: responder UID, free-text up to 1000 characters, helpful flag, timestamp

**Public projection of peer-visible island state (`islandPublic/{uid}`):**

This collection was introduced on 2026-04-29 as part of the R1 remediation (see `DPIA.md` and `PEER_ISLAND_REFACTOR_PLAN.md`). It is a server-maintained projection of a strict subset of `progress/{uid}` that other students at the same school are permitted to read for the Peer Island feature. The collection is written exclusively by Cloud Functions (`onProgressWritten`, `onUserWritten`) using the Admin SDK; client writes are denied by Firestore Security Rules.

Fields:

- `name` (string) — duplicated from `users/{uid}.name`
- `avatar` (string, DiceBear seed) — duplicated from `users/{uid}.avatar`
- `school` (string) — duplicated from `users/{uid}.school`; used as the same-school query filter
- `category` (NorthStarCategory enum: `college`, `independence`, `prove-myself`, `creative`, `change-maker`, etc.) — sourced from `progress/{uid}.islandState.category` with fallback to `progress/{uid}.northStar.category`. This is a soft self-chosen aspiration field, not Article 9 data. Inclusion in the projection is a deliberate product decision recorded in `DPIA.md` R1.
- `placements` (array of `IslandPlacementPublic`) — sourced from `progress/{uid}.islandState.placements`, with the per-placement `purchasedAt` timestamp **stripped** to avoid behavioural inference about user activity windows. All other placement fields (item, position, rotation, scale, starter flag) are preserved because they form the visible island.
- `placementCount` (number) — pre-computed count of non-starter placements; replaces a client-side filter on the array.
- `score` (number) — pre-computed leaderboard metric `(placementCount * 2) + (uniqueItems * 3)`. Replaces the raw `purchaseHistory` array, which is **not** in the projection.
- `schemaVersion` (number, currently `1`) — for future migration safety.
- `updatedAt` (server timestamp) — set on every projection write.

Fields from `progress/{uid}` that are **not** in this projection (and therefore cannot be read by peers): `pointsData`, `studySessions`, `studyDebriefs`, `topicMastery`, `unifiedMockResults`, `subjectProfile`, `timetableCompletions`, `timetableStreak`, `northStar.statement`, `flareCounts`, `lighthouseLevel`, `rescueCount`, `cosmeticUnlocks`, `strategyMastery`, `sm2States`, `teachBacksSeen`, `dismissedGuides`, `islandState.purchaseHistory` (raw), `islandState.totalSpent`, `islandState.lastPurchaseTimestamp`, `islandState.claimedRewards`, and per-placement `purchasedAt`. None of these are read by the Peer Island feature today, so excluding them does not change the user-visible feature.

**Guidance Counsellor data (`gcNotes/{schoolId}/students/{studentId}`, `gcSettings/{schoolId}`, `gcEvents/{schoolId}`):**

- free-text private notes about a named student
- dismissed-alerts state
- school calendar events

**UI-only data (`settings/{userId}`):**

- language, dark mode, accent theme, card style, default work minutes, animation toggles, dashboard visibility, "essentials mode" toggle.

**Special category data (Article 9):** not deliberately collected; may incidentally arise in free-text reflections and peer messages — see DPIA.md Section 1.4. The Processor's position on lawful condition is in DPIA.md Section 2.1.

**No biometric data, no location data beyond school name, no advertising identifiers, no cookies set by the Processor's domain beyond Firebase Authentication's session cookie.**

---

## Schedule 4 — List of sub-processors (GDPR Art. 28(2), 28(4))

### 4.1 Sub-processors authorised under this DPA

| # | Name | Role | Data shared with sub-processor | Region of processing | Safeguard |
|---|---|---|---|---|---|
| 1 | Google LLC / Google Ireland Ltd (Firebase Authentication, Cloud Firestore, Firebase Hosting, Cloud Functions, Firebase Cloud Storage) | Hosting, authentication, database, serverless compute, static asset delivery for the entire application | All personal data described in Schedule 3 | Default project region: **TBC — Alex to confirm Firestore region in the Firebase console**; based on `firebase.json` having no `location` key, the project was likely created in `us-central1` (United States) | Google Cloud Data Processing Addendum incorporating EU Standard Contractual Clauses (2021 controller-to-processor module). **Reviewer note: the executed Google DPA must be on file with NextStepUni and made available to the Controller on request.** |
| 2 | DiceBear (operated by Florian Körner / Studio Hyperdrive) | Generation of avatar SVGs from a pseudonymous seed | Avatar seed (a pseudonym from a fixed list — see `utils/authUtils.ts`); user IP address; user-agent string (incidental to HTTP request) | TBC — DiceBear's hosting region is not contractually fixed | DiceBear is an unauthenticated public API. **No DPA is in place.** Mitigation: PWA cache (vite.config.ts:58–63) reduces request frequency to once per 30 days per avatar; the seed value is pseudonymous. **Reviewer note: legal counsel to confirm whether the avatar URL fetch constitutes "processing on behalf of" within Art. 28, given that DiceBear does not store the seed and treats every request statelessly. The Processor's position is that DiceBear is a downstream content delivery provider rather than a sub-processor, but legal sign-off is required.** |
| 3 | Google LLC (Google Fonts) | Font file delivery | None — no personal data is sent in the font fetch beyond IP and user-agent | Google global edge | Standard Google ToS; no DPA. **Reviewer note: same Art. 28 question as DiceBear.** |
| 4 | Tailwind Labs Inc. (Tailwind CDN) | CSS framework delivery | None — IP and user-agent only | Cloudflare CDN (global) | Standard Tailwind ToS; no DPA. Same caveat. |

### 4.2 Sub-processor change procedure

The Processor will provide the Controller with at least thirty (30) days' written notice of any addition or replacement of sub-processors, during which the Controller may object on documented data-protection grounds. **Reviewer note: this language is to be lifted into the legal body of the DPA; no implementation in code is required for the notice mechanism, but a Controller contact register is needed — TBC.**

---

## Schedule 5 — Technical and Organisational Measures (GDPR Art. 32)

The Processor is **not** ISO 27001 certified. The control mapping below is provided to assist the Controller's risk assessment by reference to a familiar control taxonomy; it is not a claim of certification.

### 5.1 A.5 Information security policies

- Written information security policy: **TBC — to be drafted before Year 2 sign-off**.
- Acceptable-use policy for engineering staff: **TBC**.

### 5.2 A.8 Asset management

- Source code is held in a private GitHub repository (`https://github.com/alexlinehan17-lab/Nextstepuni-Launch-`).
- Production data is held in a single Firebase project (`nextstepuni-app`).
- Secrets (the Gemini API key referenced in `README.md` is **not currently in the bundle** — see AI_GOVERNANCE_SCHEDULE.md Section 1) are intended to be held in `.env.local`, which is gitignored. Reviewer note: a secrets-rotation policy is **TBC**.

### 5.3 A.9 Access control

| Control | Implementation | Source |
|---|---|---|
| Authentication | Firebase Authentication, email + password | firebase.ts |
| Password policy | Firebase default minimum (6 chars); **TBC — Alex to confirm** whether Firebase's password strength validator is enabled at console level | functions/src/index.ts:86 enforces ≥6 for self-change |
| Multi-factor authentication | **Not implemented.** Reviewer note: MFA on the GC and admin accounts at minimum is recommended for Year 2. | — |
| Role-based access in the application | Three roles: student / gc / admin. Student is default. GC is set server-side; admin is identified by hard-coded email | firestore.rules:7–9; AuthContext.tsx:94–103 |
| Role-based access at the database | Firestore Security Rules per collection | firestore.rules |
| Privileged access (admin email) | Hard-coded `admin@nextstep.app` email check | firestore.rules:40–41 |
| Default deny on undeclared paths | Yes | firestore.rules `match /{document=**}` end |
| Production access by NextStepUni staff | Engineering staff have Firebase Console access. Number of staff: **TBC — Alex to confirm**; principle of least privilege should be documented and enforced. | — |

### 5.4 A.10 Cryptography

- TLS 1.2+ in transit for all client-server traffic (Firebase default).
- AES-256 encryption at rest for Firestore data (Google Cloud platform default).
- Password hashing: scrypt (Firebase Authentication default).
- Application-level encryption: not implemented (and not required for the data classes processed).
- Cryptographic key management: handled by Google Cloud KMS; no customer-managed keys (CMEK) configured.

### 5.5 A.12 Operations security

- Change management: changes ship via GitHub commits to `main`; deploy is `npm run build` + `firebase deploy`. **TBC — Alex to confirm whether a written deploy checklist exists.**
- Logging: Firebase Authentication, Firestore and Cloud Functions emit logs to Google Cloud Logging. Application errors are written to the browser console (`console.error`). **No external error-tracking service is integrated** (see DPIA.md Section 1.5 and AI_GOVERNANCE_SCHEDULE.md Section 1).
- Backup: Cloud Firestore snapshot/backup posture: **TBC — Alex to confirm** whether daily exports to Cloud Storage are configured.
- Vulnerability management: dependency updates handled via npm `package.json`; no automated SCA configured (no Dependabot, Snyk or Renovate seen). **TBC**.
- Time synchronisation: Google Cloud platform default (NTP).

### 5.6 A.16 Incident management

- Incident response plan: **TBC — to be drafted**.
- Breach-notification timeline (Article 33 — 72 hours to DPC): captured in plan above; until then, the obligation rests on the named Engineering Lead by default. **Reviewer note**: a written escalation tree is required before Year 2 sign-off.
- Last incident: none reported.

### 5.7 A.18 Compliance

- Records of processing (Article 30): this DPIA, DPA Schedules and the AI Governance Schedule together form the core ROPA for the Processor. A formal Article 30 register **is to be maintained** — TBC.
- Data subject rights workflow (Articles 15–21): **not implemented in product**; the documented manual workflow is for a parent or student to write to NextStepUni at the published support address, after which the engineer manually exports / deletes the data. This is acceptable for Year 1 scale; for Year 2 (~2,000 students) an in-product workflow is required (DPIA.md Section 4.2 T-NEW-8).
- Retention policy: **TBC — to be agreed and implemented**. See Schedule 1 Section 1.2.
- Annual review of these Schedules: required, with a documented reviewer.

### 5.8 Application-specific TOMs (mapped from the codebase)

| Measure | Source |
|---|---|
| Field-level length validation in Firestore rules | firestore.rules:26–30, 171, 194, 227 |
| Append-only / monotonic-only validators on points and achievements | firestore.rules:74–85 |
| Pinned `+1` increment validators on `helpfulCount` and `responseCount` | firestore.rules:180, 208 |
| Same-school scoping on peer interactions | firestore.rules: kudos / gifts / teachbacks / flares blocks |
| Server-side role check in `resetStudentPassword` Cloud Function | functions/src/index.ts:33–48 |
| Reset-flag precondition in `changeOwnPassword` Cloud Function | functions/src/index.ts:95–97 |
| Reserved-email blocking at registration | LoginPage.tsx (registration validation) |
| Default-deny rule for undeclared collections | firestore.rules end of file |
| PWA caching to reduce third-party-CDN request frequency | vite.config.ts:32–66 |

---

## Schedule 6 — International data transfers (GDPR Chap. V)

### 6.1 Identified transfers

| Service | Personal data transferred | Region of processing | Mechanism under Chapter V |
|---|---|---|---|
| Cloud Firestore (`nextstepuni-app`) | All data in Schedule 3 | **TBC — Alex to confirm region from Firebase console.** Default for projects without explicit `location` is `us-central1` (United States) | EU Standard Contractual Clauses 2021 (controller-to-processor module) within Google Cloud DPA, supplemented per Schrems II by Google's published transfer-impact assessment. **Reviewer note: legal counsel must confirm that the executed Google DPA covers this transfer.** |
| Firebase Authentication | Email, password hash, sign-in metadata | Same as above | Same as above |
| Cloud Functions (`resetStudentPassword`, `changeOwnPassword`) | Student UID, temporary or new password (in transit only) | Same as above | Same as above |
| Firebase Hosting CDN | None (static assets) | Global edge | Not a transfer of personal data |
| api.dicebear.com | Avatar seed (pseudonymous), IP, user-agent | TBC — DiceBear's hosting region is not contractually fixed | No transfer mechanism in place. See Schedule 4 reviewer note on whether DiceBear is a sub-processor at all. |
| Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`) | IP, user-agent (incidental) | Google global | Not a transfer of personal data in the GDPR sense (no identifying request payload) |
| Tailwind CDN (`cdn.tailwindcss.com`) | IP, user-agent (incidental) | Cloudflare global | Same |

### 6.2 Transfer-impact assessment summary

The principal transfer of personal data outside the EEA is the entirety of the Firestore dataset (assuming `us-central1`). The risks under Schrems II — US government access requests — are mitigated by Google Cloud's published transparency reports and by the Standard Contractual Clauses incorporated into the Google Cloud DPA. The data classes involved are **educational performance and reflective content of minors**, which are sensitive but do not include health records, immigration data or other categories that would attract heightened US-authority interest.

The Processor's recommendation, captured in DPIA Section 4.2 T-NEW-9, is to migrate the Firestore database to an EEA region (e.g. `europe-west1`, Belgium) before Year 2 launch. This eliminates the transfer entirely and removes the Schrems II analysis from scope. **TBC — Alex to confirm whether migration is feasible within the Year 2 timeline.**

### 6.3 Transparency to data subjects

The Controller (school) is responsible for Article 13/14 transparency; the Processor will provide the Controller with the necessary text describing transfer mechanisms. A draft privacy notice section is recommended:

> "Your account and progress data is stored in cloud infrastructure operated by Google. It is currently held in [region — TBC] and is protected by [SCCs / regional adequacy] under GDPR Chapter V. NextStepUni Ltd is the Processor; your school is the Controller; PwC Ireland (the programme sponsor) does not receive your personal data."

**Reviewer note**: legal counsel to finalise the Article 13 notice text alongside this Schedule.

---

## Document control

- Source code reviewed: commit `0ac6be4` on branch `main`.
- Companion documents: DPIA.md, AI_GOVERNANCE_SCHEDULE.md, SUMMARY.md.
- Internal audit references: `docs/firestore-audit.md`, `docs/registration-audit.md`.
