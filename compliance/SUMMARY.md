# Compliance Documentation — Summary

NextStepUni Learning Lab — PwC Year 2 sign-off package

Document status: DRAFT for legal review
Prepared by: NextStepUni Ltd
Date: 2026-04-29
Source code reviewed: commit `0ac6be4` on branch `main`

This summary accompanies three documents in the same directory:

- `DPIA.md` — Data Protection Impact Assessment (Irish DPC template)
- `AI_GOVERNANCE_SCHEDULE.md` — AI feature inventory and EU AI Act position
- `DPA_SCHEDULES.md` — Schedules 1–6 to attach to the legal DPA body

It surfaces the items most likely to attract scrutiny from PwC's risk and legal team, the gaps where external help is required, and the rough effort to close each one.

---

## 1. Top three risks PwC's legal team will likely query

### 1.1 Same-school cross-user reads on `progress/{uid}`

`firestore.rules:60–63` permits any authenticated student to read the *complete* `progress/{uid}` document of any other student in the same school. The pedagogical justification is the Peer Island feature, but the rule is over-broad: it grants visibility into reflective debriefs, mock results and topic mastery, not just the leaderboard fields the feature renders. A reviewer reading the rules file will spot this immediately. It interacts with Article 9 (reflective content may be health-adjacent) and Article 5(1)(c) data-minimisation. Tracked as **DPIA R1** with mitigation **T-NEW-1**.

### 1.2 No data-subject-rights workflow

There is no in-product mechanism for export (Art. 15), erasure (Art. 17) or objection (Art. 21). Account deletion exists only as a GC-initiated action and does not erase derivative records (`responses`, `notifications`, peer collaboration). At pilot scale (534 students) a manual back-office process was tolerable; at ~2,000 students it is not. Tracked as **DPIA R9** with mitigation **T-NEW-8**.

### 1.3 Indefinite retention with no policy

No Firestore TTL is configured; no scheduled job purges old `studySessions`, `studyDebriefs`, expired `flares` or stale `notifications`. The `flares.expiresAt` field is set but not acted on. The Processor has no documented retention policy; until one exists and is implemented, the position under Article 5(1)(e) is indefensible. Tracked as **DPIA R10** with mitigation **T-NEW-7**.

### Other items the legal team will probably also raise

These did not make the top three but each is worth pre-empting:

- **Documentation drift**: `README.md:18` and `CLAUDE.md:22` instruct developers to set `GEMINI_API_KEY`, but the deployed bundle contains no Gemini integration. A diligent reviewer will assume the key is in production and ask awkward questions. The fix is a one-line README edit; the framing is in `AI_GOVERNANCE_SCHEDULE.md` Section 1.
- **Data residency**: Firestore region was not configured in `firebase.json`, which means the project sits on the Firebase default `us-central1`. **Alex to verify in the Firebase console.** If confirmed, the Schrems II framing in `DPA_SCHEDULES.md` Schedule 6 is the floor; migrating to `europe-west1` is the strong answer.
- **School spoofing at registration** (DPIA R3). Trivially demonstrable; the fix is an allow-list either as a Firestore rule lookup or a Cloud Function.
- **Notifications collection write path** (DPIA R2) — partially addressed in current rules but the Cloud-Function-only architecture would be cleaner.
- **No MFA** on GC or admin accounts — a routine expectation in 2026.
- **No Firebase App Check** — leaves the project open to SDK-spoofed clients.

---

## 2. Gaps requiring external help

| # | Gap | Who is needed | Why |
|---|---|---|---|
| G1 | Lawful basis confirmation for child data and Article 9 free-text content | Data protection lawyer (Irish, fluent in DPA 2018 §41) | DPIA Section 2.1 asserts Art. 6(1)(e) plus parental consent at school level and Art. 9(2)(g) for incidental health data. Each of those needs a formal sign-off — they are not self-evident. |
| G2 | Confirmation that PwC sits outside the data chain | Same lawyer + review of executed sponsorship agreement | DPIA Section 1.1 asserts this; the sponsorship agreement must be read against the assertion. |
| G3 | Data Protection Officer | Either an appointed internal DPO or a part-time external DPO under retainer | Article 37: an org processing children's data on a "large scale" should appoint a DPO. ~2,000 minors is borderline; counsel should advise. |
| G4 | Google Cloud DPA — confirm executed and on file | Engineering / commercial lead | Sub-processor relationship with Google must be evidenced for the Controller. |
| G5 | Security baseline (ISO 27001 control mapping → policy artefacts) | A security consultant for ~2 weeks, or an external firm for an SOC 2-style observation | DPA Schedule 5 is a control map, not a control implementation. Several rows are TBC: information-security policy, incident-response plan, vulnerability-management process, MFA on privileged accounts, App Check enablement. |
| G6 | Firestore region migration (if needed) | Engineering | If `Alex` confirms the project is in `us-central1`, migration to `europe-west1` is achievable but is a one-shot operation that requires careful planning of Cloud Functions and Auth region alignment. |
| G7 | Privacy notice text (Articles 13/14) for the Controller | Lawyer to draft, school's DP lead to adopt | The Controller (school) must communicate; the Processor must provide the substance. Currently absent. |
| G8 | Parental consent mechanism | Operational / lawyer review | Whatever is currently happening at school enrolment must be evidenced; if it is not enough for explicit Article 8/9 purposes, a forms-and-process refresh is needed. |

---

## 3. Estimated effort to close each gap

The estimates below are calendar effort, not cost. They assume a single engineer is available and that legal items run in parallel. "S" = under one week; "M" = one to three weeks; "L" = more than three weeks.

| Item | Type | Effort | Critical path? |
|---|---|---|---|
| **DPIA R1 — restrict same-school progress reads** (T-NEW-1) | Engineering | M | Yes — it is the highest-severity finding. Requires a Cloud-Function projection; cannot be done in rules alone. |
| **DPIA R9 — DSAR endpoints** (T-NEW-8) | Engineering | M | Yes — Year 2 scale demands an in-product flow. |
| **DPIA R10 — retention policy + implementation** (T-NEW-7) | Policy + engineering | M (S for policy, M for code) | Yes |
| **DPIA R3 — school allow-list** (T-NEW-3) | Engineering | S | Yes |
| **DPIA R2 — notifications via Cloud Function** (T-NEW-5) | Engineering | S | No (medium severity) |
| **DPIA R4 — progress field validation** (T-NEW-4) | Engineering | M | No |
| **DPIA R8 — Firestore region migration** (T-NEW-9) | Engineering | M | Conditional on confirming current region is non-EEA. If yes, **must finish before Year 2 onboarding**. |
| **DPIA R6 — password-reset audit log + student notification** (T-NEW-6) | Engineering | S | No |
| **DPIA R11 — content moderation on flares/teachbacks** (T-NEW-10) | Engineering | M (basic regex) / L (LLM moderation, which re-opens AI Act questions) | No, but advisable |
| **DPIA R12 — DEV artefacts removal** (T-NEW-12) | Engineering | S | No |
| **App Check enablement** (T-NEW-11) | Engineering | S | No |
| **Documentation drift fix (Gemini references)** | Engineering | S | No, but the fastest "win" — a one-line README change makes the AI Governance Schedule headline finding immediately verifiable |
| **G1 / G2 lawful basis confirmation** | Legal | S–M | Yes (without it, the DPIA cannot be signed off) |
| **G3 DPO appointment** | Legal + commercial | S–M | Yes |
| **G4 Google DPA evidence** | Commercial | S | Yes |
| **G5 security baseline (policies, IR plan, MFA, vuln mgmt)** | Security consultant + engineering | M | Yes |
| **G7 privacy notice text** | Legal | S–M | Yes |
| **G8 parental consent mechanism** | Operational + legal | M | Yes |

### 3.1 Suggested running order

1. **Now (this week)**: fix the README/CLAUDE.md drift; confirm Firestore region; engage the lawyer (G1, G2, G7, G8).
2. **Within two weeks**: ship T-NEW-1 (cross-user read restriction), T-NEW-3 (school allow-list), T-NEW-12 (DEV artefacts), T-NEW-11 (App Check), and the password-reset audit log T-NEW-6.
3. **Within four weeks**: ship the DSAR endpoints (T-NEW-8) and the retention policy + implementation (T-NEW-7). Decide on Firestore region migration (T-NEW-9) and execute if needed.
4. **Before Year 2 launch**: G3 (DPO), G5 (security baseline + IR plan + MFA), the consent mechanism (G8), and the privacy notice (G7).
5. **Continuous**: quarterly Firestore-rules review, annual review of these documents.

---

## 4. Document control

- Source code reviewed: commit `0ac6be4` on branch `main`.
- Author: NextStepUni Ltd (engineering).
- Reviewer: NextStepUni Ltd (commercial / legal counsel).
- Files in this directory:
  - `DPIA.md`
  - `AI_GOVERNANCE_SCHEDULE.md`
  - `DPA_SCHEDULES.md`
  - `SUMMARY.md` (this file)

The companion internal audit documents in `docs/` (`firestore-audit.md`, `registration-audit.md`, `round-trip-nav-audit.md`, `nav-audit.md`) remain the operational source-of-truth for individual issues; the documents in `compliance/` translate them into the language and structure that PwC's Risk/Legal team and the Controller's data-protection lead will expect.
