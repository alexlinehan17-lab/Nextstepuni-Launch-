# Technical hardening plan

Last updated: 2026-08-23

## 1. Release integrity

- [x] Make verification a prerequisite of live deployment.
- [x] Build Cloud Functions in CI.
- [x] Deploy rules, indexes, Storage rules and Functions before Hosting.
- [x] Deploy the exact web artifact produced by the verified job.

## 2. Backend verification

- [x] Type-check test sources separately from application sources.
- [x] Add Firestore and Storage emulator rule tests.
- [x] Install Java in CI for Firebase emulators.
- [ ] Add callable-function authorization tests.
- [ ] Add Playwright coverage for registration, onboarding and staff access.
- [ ] Add non-signing Capacitor iOS and Android CI builds.

## 3. Progress data boundary

- [x] Add typed repositories for boot-critical user and progress reads.
- [x] Move module progress/points awarding behind an atomic repository method.
- [x] Move achievement and gamification mutations to field-level atomic writes.
- [ ] Migrate remaining feature hooks away from direct Firestore imports.
- [ ] Move unbounded or independently updated domains to subcollections.
- [ ] Add explicit schema-version migrations for progress documents.

## 4. Authorization

- [x] Remove client-side GC role inference from email patterns.
- [x] Synchronise server-managed role/school into Firebase custom claims.
- [x] Keep a Firestore-document fallback while existing tokens migrate.
- [x] Backfill the administrator custom claim and remove email-based admin
      authorization fallbacks.

Firebase App Check is registered and integrated for every client: reCAPTCHA
Enterprise on web, App Attest on iOS and Play Integrity on Android. Enforcement
remains deliberately staged until the updated native builds are released and
their legitimate traffic is visible in App Check metrics. Authentication,
server-owned custom claims and Security Rules remain the primary authorization
controls; App Check is an additional client-attestation boundary.

## 5. Generated content

- [x] Extract the 22,695-question Paper Trail topic corpus from TypeScript into
      generated JSON artifacts with a small typed adapter.
- [x] Keep generation deterministic from the verified subject wave files.
- [x] Restrict Tailwind's source scan so it does not traverse dependencies.
- [ ] Apply the artifact pattern to the largest Catch-Up Lane and Mark Bank
      corpora where profiling shows a worthwhile compiler/bundle benefit.
- [ ] Add per-artifact schema/version metadata and checksum validation.
