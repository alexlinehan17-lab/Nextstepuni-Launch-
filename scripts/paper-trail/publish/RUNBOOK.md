# Paper Trail — credentialed publish pass (task #94)

Everything here needs **your** Firebase/Storage credentials — it can't run from
the agent container (no gcloud/firebase CLI, Storage returns 403). Once you're
authenticated (`gcloud auth application-default login` or a service-account
`GOOGLE_APPLICATION_CREDENTIALS`, and `firebase login`), this is a
single sitting.

> **What is and isn't blocked by this.** The Topic Vault's **question crops are
> already live** — they come from `public/paper-anchors/` (deployed with the app)
> and from answer sidecars already on Storage. This pass lights up the remaining
> **marking-scheme reveals** (the "Show the marking scheme" toggle) on the papers
> whose answer sidecars were generated/edited this session, and — separately —
> deploys the Firestore rules that move the class-layer features off their
> on-device fallback.

## 1. Upload the answer sidecars

`upload_answers.py` takes one manifest (TSV of `localPath<TAB>remotePath`) and
PUTs each file to Storage. Uploads are idempotent (re-PUTing an identical object
is harmless), so running all manifests is safe.

```bash
cd scripts/paper-trail
for m in publish/audit-reupload.tsv publish/wave10-upload.tsv \
         publish/p2b-upload.tsv publish/p2c-upload.tsv \
         publish/cv1-upload.tsv publish/cv2-upload.tsv publish/cv3-upload.tsv \
         publish/irish-upload.tsv; do
  echo "== $m =="
  python3 upload_answers.py "$m"
done
```

Each row's `localPath` is a committed `scripts/paper-trail/answers/<year>/<fileid>.json`;
`remotePath` is `papers/<cycle>/<subject>/<year>/answers/<fileid>.json`. ~236 rows
total across the manifests (the session's new + re-uploaded sidecars; the other
~1,100 sidecars on disk are the originals already live on Storage).

## 2. Flip the `answers:1` index flags + rebuild

The classic Viewer shows its answer toggle only for `(subjectId, level, lang)`
profiles in `QA_PASSED_ANSWER_PROFILES` (top of `build-index.py`). (The **Topic
Vault** does not depend on this flag — it fetches the sidecar/anchor directly —
so this step is only for the classic full-paper Viewer.) For each subject/level/lang
you just uploaded and have eyeballed, add its tuple to that set, then:

```bash
cd scripts/paper-trail
python3 build-index.py        # regenerates ../../paperTrailData.ts + out/index-report.md
cd ../.. && npm run typecheck && npm run build   # verify
```

Review `git diff paperTrailData.ts` — it should only add `answers:1` flags to the
papers you uploaded. Commit + push to `main` to deploy (Vite build + Firebase
Hosting fire on push).

## 3. Deploy the Firestore rules (class-layer features)

`firestore.rules` (committed) carries the anonymous-by-construction counter-doc
rules for `chairCohorts/*` and `focusPresence/*`. Until deployed, the class
features fall back to on-device.

```bash
firebase deploy --only firestore:rules --project nextstepuni-app
```

(Or use the `deploy-rules.yml` GitHub Actions workflow delivered separately — it
needs a `FIREBASE_TOKEN` repo secret. It's not committed here because the
session's git token lacks `workflow` scope; add it to `.github/workflows/`
yourself.)

## 4. Verify live

- Open a paper in the classic Viewer whose profile you flagged → the **Answers**
  toggle appears and renders the scheme crop.
- In the Examiner's Chair / focus features, confirm a second device sees the
  shared anonymous counts (rules deployed).

That's the whole pass. Nothing here is destructive; every step is re-runnable.
