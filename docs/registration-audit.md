# Registration Flow Audit

**Date:** 2026-04-11
**Scope:** LoginPage.tsx (primary), Auth.tsx (legacy), AuthContext.tsx, firestore.rules
**Lenses:** Security, Data Integrity, UX/Conversion

---

## Flow Map (LoginPage.tsx — primary registration path)

1. User fills Name, School (dropdown), Avatar (grid), Password, Confirm Password
2. `handleSubmit` (line 117) calls `handleRegister()` (line 77)
3. Client-side validation (lines 78-81): passwords match, name non-empty, school selected, avatar chosen
4. Email derived: `name.toLowerCase().replace(/\s+/g, '')@nextstep.app` (line 85) — no character validation
5. `createUserWithEmailAndPassword(auth, emailToUse, password)` (line 86)
6. `updateProfile(cred.user, { displayName: name.trim() })` (line 89)
7. `setDoc(doc(db, 'users', cred.user.uid), { name, avatar, school })` (lines 92-96) — no `role`, no `isAdmin`
8. `handleLoginSuccess({ uid, name, avatar, school, role: 'student' })` (lines 97-103) — role hardcoded client-side
9. `onAuthStateChanged` fires in AuthContext, fetches user doc, reads `userData.role` (undefined — never written)

---

## Executive Summary — Top 5 Findings

1. **CRITICAL: Auth.tsx catch block references wrong variable** — `catch {}` was changed by lint cleanup but catch body still references `error.code` which resolves to the React state string, not the exception. All registration errors show generic message.
2. **HIGH: No username character validation in LoginPage.tsx** — Special characters (`'`, `+`, `!`, emoji) pass through to email construction. Auth.tsx has `/^[a-z0-9_-]+$/` validation but LoginPage.tsx doesn't.
3. **HIGH: DEV skip-login buttons ship in production** — Two buttons bypass auth with hardcoded `uid: 'dev-student'`. Firestore rules block data access (no real auth token), but it's a visible security concern.
4. **HIGH: LoginPage.tsx doesn't clean up auth account on setDoc failure** — If `createUserWithEmailAndPassword` succeeds but `setDoc` fails, orphaned auth account persists. Auth.tsx handles this with `deleteUser()` rollback.
5. **MEDIUM: Firestore create rules allow arbitrary extra fields** — Only validates `name`, `avatar`, `school` exist and blocks `isAdmin`/`role`. A malicious client could add any other field.

---

## Critical

### C1. Auth.tsx catch block references wrong `error` variable

**File:** Auth.tsx:223-233
**Issue:** The lint cleanup changed `catch (e: any)` to `catch {` but the body references `error.code`. `error` resolves to the React `useState` state variable (a string), not the caught exception. `''.code` is `undefined`, so error-specific messages (weak password, name taken) never display.
**Impact:** All Auth.tsx registration errors show "Failed to create account. Please try again."
**Fix:** Change `catch {` to `catch (err: any) {` and reference `err.code`.

---

## High

### H1. No username character validation in LoginPage.tsx

**File:** LoginPage.tsx:85
**Issue:** Email is `name.toLowerCase().replace(/\s+/g, '')@nextstep.app`. Characters like `'`, `+`, `!`, `#`, emoji all pass through. Firebase Auth rejects some, but the error message is generic ("Registration failed").
**Contrast:** Auth.tsx:198 validates with `/^[a-z0-9_-]+$/` before calling Firebase.
**Fix:** Add the same regex check to LoginPage.tsx before the Firebase call.

### H2. DEV skip-login buttons in production

**File:** LoginPage.tsx:239, 351
**Issue:** Two buttons call `handleLoginSuccess({ uid: 'dev-student', ... })` bypassing Firebase Auth. No real auth token means Firestore rules block all data access, but it's a visible concern for external reviewers (PwC).
**Fix:** Gate behind `import.meta.env.DEV` or remove entirely.

### H3. No auth account rollback on Firestore failure

**File:** LoginPage.tsx:84-113
**Issue:** If `createUserWithEmailAndPassword` succeeds but `setDoc` fails (network, rules), the catch block runs but doesn't call `deleteUser()`. Auth.tsx:224-225 handles this correctly.
**Impact:** Orphaned auth accounts. User can't re-register with same name. Login creates degraded fallback session.
**Fix:** Add `deleteUser(cred.user)` to catch block, matching Auth.tsx pattern.

---

## Medium

### M1. No `createdAt` timestamp on user doc

**File:** Both LoginPage.tsx:92-96 and Auth.tsx:215-219
**Issue:** Neither writes `createdAt`. Firestore rules don't block it (they only forbid `isAdmin` and `role`). Missing audit trail.
**Fix:** Add `createdAt: new Date().toISOString()` to the user doc write.

### M2. `yearGroup` not set during registration

**File:** Neither form writes `yearGroup`
**Issue:** Only set during onboarding. If user never completes onboarding, year-group filtering doesn't work.
**Impact:** Low — by design. Onboarding handles it.

### M3. `school` field accepts any string from a malicious client

**File:** firestore.rules:30
**Issue:** Validates `school is string && school.size() <= 50` but doesn't check against approved list. A direct API call could write `school: 'fakeschool'`, placing the user outside any GC's visibility.
**Impact:** Low — user isolates themselves, can't access other schools' data.

### M4. Auth.tsx `onLoginSuccess` callback missing `school`

**File:** Auth.tsx:221
**Issue:** `registeredUser = { uid, name, avatar, isAdmin: false }` — no `school` or `role`. Brief period after Auth.tsx registration where school-dependent UI may not work.
**Fix:** Add `school: selectedSchool` to the callback object.

---

## Low

### L1. No minimum name length validation
Both forms accept single-character names. Email `a@nextstep.app` is valid.

### L2. No password strength feedback
Users discover the 6-character minimum only after a failed attempt.

### L3. Firestore rules allow arbitrary extra fields on create
The create rule validates required fields and blocks `isAdmin`/`role`, but doesn't restrict other fields. A malicious client could write `{ name: 'X', avatar: 'Y', foo: 'bar' }`.

---

## Verified Good

| # | Check | Result |
|---|-------|--------|
| V1 | Role escalation via registration blocked | **CONFIRMED.** Neither form writes `role`. Firestore rules:25 blocks `role` in creates. |
| V2 | Role immutable on update | **CONFIRMED.** Firestore rules:33 requires `role == resource.data.role`. |
| V3 | Cross-user doc write blocked | **CONFIRMED.** Firestore rules:23 requires `auth.uid == userId` for creates. |
| V4 | No plaintext password storage | **CONFIRMED.** Firebase Auth handles credentials server-side. |
| V5 | `updateProfile` sets `displayName` | **CONFIRMED.** Both forms call `updateProfile` with `name.trim()`. |
| V6 | Registration race condition mitigated | **CONFIRMED.** AuthContext no longer signs out on missing user doc. Uses fallback session with `displayName`. |
| V7 | Loading state during registration | **CONFIRMED.** `isLoading` disables button, changes text. |
| V8 | School dropdown uses predefined list | **CONFIRMED.** `SCHOOLS` from `schoolData.ts`. UI-level only (see M3). |
| V9 | XSS via name/school not exploitable | **CONFIRMED.** React JSX auto-escapes. No raw HTML insertion. |
| V10 | Post-registration landing correct | **CONFIRMED.** Shows onboarding if `needsOnboarding`, tree otherwise. |

---

## Recommended Fix Priority

| Priority | Issue | Effort |
|----------|-------|--------|
| CRITICAL | C1: Auth.tsx catch block wrong variable | 5 min |
| HIGH | H1: Username character validation | 10 min |
| HIGH | H2: Remove DEV skip-login from production | 5 min |
| HIGH | H3: Auth account rollback on Firestore failure | 15 min |
| MEDIUM | M1: Add createdAt timestamp | 10 min |
| MEDIUM | M4: Auth.tsx callback missing school | 2 min |
| LOW | L3: Tighten Firestore create rules | 15 min |
