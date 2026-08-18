# Play Store listing — Misleading Claims rejection (August 2026)

## What happened
Google Play rejected the app under the **Misleading Claims** policy with two
functionality issues:

1. **Missing Source Link for Government Information** — the app provides
   government information but gave no clear, accessible URL to the original
   sources.
2. **Missing Clear Disclaimer of Non-Official Status** — no easy-to-see
   statement that the app does not represent a government entity.

The trigger is this line in the store listing: *"Our exam content is built from
State Examinations Commission marking schemes and Chief Examiner reports."* The
SEC is an Irish public body, so the app is classed as carrying government
information whether or not it claims affiliation.

## Do NOT appeal
The appeal path in Google's mail is only for developers who hold **written
documentation proving government affiliation or authorisation**. NextStepUni has
none and claims none, so an appeal would be rejected and cost 7+ days. This is a
fix-and-resubmit.

## What the app actually carries
Six public bodies, not just the SEC. All are named in the listing and in Terms:

| Body | Where it appears | Source |
|---|---|---|
| State Examinations Commission | Mark Bank, Paper Trail, all exam content | https://www.examinations.ie |
| CAO | Future Finder, College Compass | https://www.cao.ie |
| SUSI | College Compass | https://www.susi.ie |
| Higher Education Authority | College Compass | https://hea.ie |
| Qualifax | Future Finder | https://www.qualifax.ie |
| Citizens Information | College Compass | https://www.citizensinformation.ie |
| gov.ie | College Compass | https://www.gov.ie |

## What was changed in the app
- `components/legal/legalContent.ts` — new Terms section **"Where our content
  comes from"**: the non-affiliation statement plus a linked source per body.
  Single source of truth, so it reaches the in-app modal *and* the public
  `/terms` page from one edit.
- `components/SettingsModal.tsx` — the disclaimer is visible in Settings without
  opening a document, because the policy asks for it to be *easy to see*.
- `vite.config.ts` + `components/legal/LegalModal.tsx` — bare URLs render as real
  links in both surfaces; a URL as plain text is not an "accessible link".
- `test/legalSourcesDisclosure.test.ts` — pins both requirements so a future copy
  edit cannot silently re-trigger the rejection.

## What YOU still have to do in Play Console
1. Wait until https://nextstepuni-app.web.app/terms shows the new
   "Where our content comes from" section. Google will click that link.
2. **Store presence → Main store listing → Full description**: replace with
   `play-full-description.txt` in this folder (3,008 chars, limit 4,000).
3. Check the **screenshots and feature graphic** carry no government crest,
   harp, SEC/Department of Education logo or wording implying official status.
4. Upload a build containing the in-app changes above.
5. **Publishing overview → send changes for review.** Do not use "Submit an
   appeal".

## Why the description matters most
Both of Google's resolution steps say *"in your description"* — that is the
surface the reviewer reads. The in-app changes back it up if the reviewer opens
the app, but the listing text is what was flagged and what gets re-checked.
