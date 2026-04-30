# Questions for Alex — facts to confirm before PwC sign-off

NextStepUni Learning Lab — structured checklist of every fact-of-the-world
item the compliance documents currently mark as TBC or assume

Document status: ACTION ITEMS for Alex
Date: 2026-04-29

---

## How to use this file

Each question below is a piece of factual information that the compliance
documents currently assume, mark as TBC, or otherwise do not have a
verified source for. Answer each in the "Your answer" line; once complete,
the next phase of compliance work can update the documents to remove the
TBC markers.

The questions are grouped by where the answer is found (account / console
access vs paper records vs operational practice). Aim to answer the whole
file in one sitting if possible — many questions reference each other.

Where a question depends on accessing the Google Cloud Console, the path
is given in italics.

---

## Section A — Firebase / Google Cloud configuration (console questions)

### Q1: Firestore region

**Where to find the answer:** Google Cloud Console → Firestore →
"Databases" → check the region of the `(default)` database for the
`nextstepuni-app` project. Alternatively, run `firebase firestore:databases:list`
once `firebase login --reauth` has been completed.

**Why it matters:** The Processor currently *assumes* `us-central1` because
no region is set in `firebase.json`. If true, EU SCCs are required for the
transfer to remain lawful. If the project is already in `europe-west1` or
similar, several documents simplify (DPIA R8 can be marked as not
applicable, DPA Schedule 6 is significantly shorter).

**Your answer:** **`europe-west2` (London, EEA).** Surfaced 2026-04-30 during the deploy of `onProgressWritten` — the Eventarc trigger path explicitly contained `locations/europe-west2/...`. Cloud Functions are still in `us-central1` (existing project pattern); a future move of the function execution region to match the data is out of scope for Phase 1. See `compliance/REMEDIATION_LOG.md` (2026-04-30 finding entry). DPIA R8, Section 1.5, Section 6, DPA Schedule 6 to be updated in a later doc-only pass.

---

### Q2: Firebase Authentication region

**Where to find the answer:** Firebase Console → Project settings → "Cloud
Messaging" / Auth provider region. Auth itself is multi-region.

**Why it matters:** Firebase Auth for Web is global by default; user
sign-in records may be processed across multiple regions. If a multi-region
deployment is in effect, the privacy notice should reflect this.

**Your answer:** _____________

---

### Q3: Firebase Cloud Storage region

**Where to find the answer:** Google Cloud Console → Cloud Storage →
buckets → check the location of `nextstepuni-app.firebasestorage.app`.

**Why it matters:** Storage is the implementation target for
`compliance/DSAR_SPEC.md` exports. If the bucket is in a US region, the
DSAR exports themselves are subject to the US transfer position.

**Your answer:** _____________

---

### Q4: Firebase Cloud Functions region

**Where to find the answer:** Google Cloud Console → Cloud Functions →
the `resetStudentPassword` and `changeOwnPassword` functions. Each shows
its deployed region.

**Why it matters:** Same as Firestore — region of execution determines
the transfer position.

**Your answer:** _____________

---

### Q5: Firestore backup schedule

**Where to find the answer:** Google Cloud Console → Firestore → "Backups
and Restore" / "Schedules", or `gcloud firestore backups schedules list`.

**Why it matters:** `compliance/RETENTION_POLICY.md` Section 3.7 has a TBC
that depends on this. If backups exist, their retention period is itself a
data-retention boundary that the policy must reconcile against.

**Your answer:** _____________

---

### Q6: Firebase App Check status

**Where to find the answer:** Firebase Console → App Check.

**Why it matters:** Without App Check, any party with the project's web
API key (which is bundled in the client and therefore public) can issue
Firestore SDK calls; only the Firestore Security Rules stand between an
attacker and the data. App Check binds Firestore access to attested
clients. DPIA T-NEW-11 lists this as a Year 2 requirement.

**Your answer (select):**
- [ ] Enabled with reCAPTCHA Enterprise on web
- [ ] Enabled with another provider
- [ ] Configured but not enforced (audit mode)
- [ ] Not configured

---

## Section B — Contractual / paper records

### Q7: Executed Google Cloud Data Processing Addendum

**Where to find the answer:** Google Cloud Console → IAM & Admin → Privacy
& Security → Data Processing and Security Terms. Look for "Accepted on
[date]". Alternatively check the email account that owns the project for
Google's confirmation email.

**Why it matters:** DPA Schedule 4 lists Google as a sub-processor and
asserts an executed DPA is on file. Without it, the sub-processor
relationship is unevidenced.

**Your answer (select):**
- [ ] Yes, accepted on _______ (date) under Google account _______
- [ ] No
- [ ] Unsure / cannot verify

---

### Q8: DiceBear terms / DPA

**Where to find the answer:** dicebear.com/legal (their Terms and Privacy
pages). DiceBear is a self-hosted-or-public-API service — at the time of
writing they publish Terms but not a customer-side DPA template.

**Why it matters:** DPA Schedule 4 row 2 has a reviewer note questioning
whether DiceBear is a sub-processor at all. Counsel will need to advise.
A pragmatic alternative is to self-host the DiceBear renderer (it's open
source, MIT licensed) so that no third-party fetch occurs.

**Your answer:**
- [ ] Continue using public API; counsel comfortable with no-DPA
- [ ] Self-host DiceBear (one-day engineering task) — eliminates the question
- [ ] Replace with another avatar provider (specify): _______

---

### Q9: Cyber / professional indemnity insurance

**Why it matters:** Standard expectation for any Processor handling
minors' data in 2026. Not a legal requirement under GDPR, but PwC's
risk team will likely ask.

**Your answer (select):**
- [ ] Policy in place; insurer ______, limit ______, expiry ______
- [ ] Quoted, not yet bound
- [ ] Not yet investigated

---

## Section C — Operational practice

### Q10: MFA on privileged Firebase accounts

**Where to find the answer:** Each owner / editor of the
`nextstepuni-app` project should have MFA enabled on their Google
account. Check `myaccount.google.com/security` for each account.

**Why it matters:** DPA Schedule 5.3 currently lists MFA as "not
implemented", which is true for the in-app `admin@nextstep.app` account.
The Google accounts that *administer* the Firebase project itself are the
more critical control plane — they have full read/write access to the
production database.

**Your answer:**
- Number of accounts with project owner / editor / admin role: _______
- Of those, number with 2FA / hardware-key MFA enabled: _______
- The `admin@nextstep.app` in-product account: MFA via Firebase
  Authentication is **not** currently enabled (Firebase Auth supports
  it; needs configuration). Plan to enable? Y / N: _______

---

### Q11: Incident response plan

**Why it matters:** Required for breach notification within 72 hours
under Article 33. DPA Schedule 5.6 currently marks this as TBC. PwC's
risk team will expect to see the plan or at least an outline.

**Your answer (select one):**
- [ ] Written IR plan exists (path or attachment): _______
- [ ] Partial — escalation tree exists but no full plan
- [ ] Nothing written; ad-hoc

If "partial" or "nothing": is the named first responder Alex? Y / N
: _______. Is there a designated DPC notification author? Y / N : _______.

---

### Q12: Data retention behaviour today

**Why it matters:** `compliance/RETENTION_POLICY.md` Section 2 audits the
*code* and finds no retention is enforced. Section 12 here asks whether
any *operational* retention happens — e.g. you manually delete inactive
accounts every quarter.

**Your answer:**
- Any manual retention activity in the past 12 months? Y / N : _______
- If yes, what was deleted, when, and on whose authority?
  ____________________________________

---

### Q13: Pen test history

**Why it matters:** Year 2 PwC sign-off may be conditional on a recent
penetration test. The Processor has not commissioned one to date.

**Your answer:**
- [ ] Pen test conducted on _______ by _______; report available
- [ ] No pen test conducted
- Year 2 plan: schedule pen test by _______ Y / N : _______

---

### Q14: Number of NextStepUni staff with production data access

**Why it matters:** Principle of least privilege under Article 32. DPA
Schedule 5.3 marks staff count as TBC. PwC's risk team will likely ask.

**Your answer:**
- Total engineering staff: _______
- Of those, with production Firebase Console access: _______
- Of those, with production data download/export access: _______
- Are access logs reviewed? Y / N : _______

---

### Q15: DPO appointment

**Why it matters:** Under Article 37 a Processor may need a DPO. Counsel
in DPIA Section 4.3 will need to advise; this question captures the
operational posture today.

**Your answer (select):**
- [ ] Internal DPO appointed: _______
- [ ] External DPO retained: _______
- [ ] Not yet appointed; awaiting legal advice
- [ ] Not yet appointed; do not believe one is required (justification): _______

---

### Q16: Parental consent mechanism

**Why it matters:** Article 8 requires verifiable parental consent for
processing children's data on the basis of consent. DPIA Section 2.1
asserts consent is collected at school enrolment. This question evidences
the actual process.

**Your answer:**
- Where is consent collected? (school enrolment form / Online via NextStepUni / other): _______
- What does the consent text say? (attach or quote): _______
- Where are the signed consents stored? _______
- Is there a withdrawal flow? Y / N : _______

---

## Section D — Code / product items raised by Phase 1

### Q17: GEMINI_API_KEY rotation status

**Where to find the answer:** Inspect `.env` in the local repo. Cross-
check against Google AI Studio / Google Cloud Console → APIs & Services →
Credentials.

**Why it matters:** The vite.config.ts leak was remediated in commit
`063d574` (2026-04-06). However, the API key value that was bundled into
client JavaScript before that date is, by definition, exposed forever to
anyone who downloaded that build. Best practice is to rotate the key
even if no Gemini code consumes it today, because the value itself is
compromised.

**Your answer:**
- Was the key in the leaked builds rotated/revoked after 2026-04-06?
  Y / N / Unsure : _______
- Current `.env` contains a `GEMINI_API_KEY` value? Y / N : _______
- If yes, date last rotated: _______
- Action: rotate now? Y / N : _______

---

### Q18: Peer Island feature post-deploy

**Why it matters:** The Phase 1 firestore.rules edit removes the
same-school peer read on `/progress/{userId}`. The Peer Island feature
relies on those reads. After deploy, the feature will silently fail
(reads denied). The remediation log records this expectation; the
question is what to do about it.

**Your answer (select):**
- [ ] Accept the feature degrades temporarily; ship a Cloud-Function
      aggregator in the next sprint
- [ ] Block the deploy until the aggregator is built
- [ ] Disable the feature in the UI before deploy (temporary)
- Other: _______

---

### Q19: Migrate admin to role-based identification

**Why it matters:** The Phase 1 spec described admin as `role == 'admin'`.
Today admin is identified by the hard-coded email `admin@nextstep.app`.
The Phase 1 fix did not migrate; both checks would need to be in place
during a transition. This is captured as a deviation in
`compliance/REMEDIATION_LOG.md`.

**Your answer (select):**
- [ ] Migrate now (small change: backfill `role: 'admin'` on the existing
      admin user document; add role-check OR email-check to relevant
      rules; ship in the same release as Phase 1)
- [ ] Defer to Phase 2; current email-based admin is acceptable for now
- [ ] Other: _______

---

### Q20: DEV rank-up tester / DEV skip-login button

**Why it matters:** `docs/registration-audit.md` (H2) flagged DEV-only
controls visible in production. Some are documented as fixed, but the
`onDevRankUp` hook on KnowledgeTree is still wired. Compliance docs
record this as DPIA R12.

**Your answer:**
- Is `onDevRankUp` still reachable in a production build today?
  Y / N : _______
- Is the DEV skip-login button reachable? Y / N : _______
- Plan: env-gate or remove? _______

---

### Q21: School allow-list

**Why it matters:** DPIA R3 ("school spoofing"). At registration the
client supplies `school` as free text. A controlled list eliminates the
risk.

**Your answer:**
- Do you have a definitive list of participating schools (Year 2)?
  Y / N : _______
- Where is it kept? (operational doc / spreadsheet / nothing yet): _______
- OK to ship a Firestore-backed allow-list (`allowedSchools/{id}`) in
  the next sprint? Y / N : _______

---

### Q22: Cleanup of debug log left in `components/KnowledgeTree.tsx`

**Why it matters:** A `console.log('[BentoTile DEBUG]', ...)` was
introduced during a separate debugging session and is still in the file
at line 162. It does not affect compliance directly but should be
removed before shipping; the Phase 1 hard rule "Do NOT touch any
application code outside firestore.rules" prevented removal during this
phase.

**Your answer:**
- [ ] Remove the log in Phase 2
- [ ] Leave for now (continuing the white-cards debug)
- [ ] Other: _______

---

## Section E — Things to do *now*, regardless of answers

These are not questions; they are next steps that arise immediately from
Phase 1. Listed here so they are not lost.

1. Run `firebase login --reauth` then deploy the staged firestore.rules
   change:
   ```
   firebase deploy --only firestore:rules --dry-run
   firebase deploy --only firestore:rules
   ```
   The dry-run output and deploy confirmation should be appended to
   `compliance/REMEDIATION_LOG.md`.
2. Read `compliance/PHASE1_COMPLETE.md` for the next prompt to run.

---

## Section F — Open questions arising from Phase 1 audits

### Q23: Was Gemini ever actually consumed in code?

**Why it matters:** `compliance/GEMINI_AUDIT.md` confirms there is no
Gemini SDK code in git history. But the env var was bundled. Was there
ever code that *attempted* to call Gemini using `process.env.API_KEY`,
that was removed in the same commit `063d574`? The grep didn't find any,
but a fuller manual review of that commit's full diff would close this
question definitively.

**Your answer:**
- [ ] Confirmed: no `fetch()` or similar against any Gemini endpoint
      ever existed
- [ ] There was code that called Gemini (specify): _______
- [ ] Don't recall

---

### Q24: AI-authored module content

**Why it matters:** Commit `a75a4d7` (2026-04-03) describes "Academic
language from AI-generated content (Google Gemini + research papers)".
This is content authoring with AI as a tool; the resulting text was hand-
edited and pasted in. PwC's risk team may ask about provenance of module
content.

**Your answer:**
- All AI-generated drafts were reviewed and edited by a human before
  shipping? Y / N : _______
- Source-of-record for the original AI prompts and drafts (kept anywhere
  for audit trail)? Y / N : _______
- Comfortable confirming this in a written statement to PwC? Y / N : _______

---

## Document control

This file is companion to `compliance/PHASE1_COMPLETE.md` and should be
worked through before the next phase of compliance hardening begins. Once
all answers are in, run the prompt in `PHASE1_COMPLETE.md` to fold the
answers back into the substantive compliance documents.
