# Exclusions — the short list of paper asks that will never be cards

One JSON file per subject. Every entry is a claim that the scheme prints
nothing liftable for this ask, and the claim carries its evidence:

```json
[
  {
    "ref": "2023 OL Q7(b)",
    "reason": "pure drawing ask; the scheme prints only 'any reasonable sketch'",
    "evidence": "2023 OL scheme p.14: the full text of the marking cell"
  }
]
```

`reconcile.py` validates every entry: an exclusion that matches no OPEN ask is
reported as stale and counts against the exit code. Exclusions are rare on
purpose — drawing questions are usually cardable (split by what the scheme
says: 156 cardable against 13 not, the one time it was measured), so before
adding an entry here, re-read the scheme cell you are excluding.

## When exclusions are NOT rare

History is the exception the rule needed. Its papers print 1,430 asks and 681
of them — 48% — are excluded, because 48% of that paper is an essay and the
whole scheme entry for an essay is a ceiling:

    1.  Max. CM = 60  Max. OE = 40
    B - Max CM = 20 marks Max OE = 10 marks

There is no content under those lines to lift, at any level of effort. What
makes such a ledger honest rather than a place to hide unread asks is that it
is GENERATED, not typed: `hist_all.py --exclusions` writes every entry from the
scheme reader itself, so `schemeEvidence` is the line the SEC actually prints
and cannot drift from it, and an ask the reader finds content for stops being
excluded on the next run. If your exclusions file is large and hand-written,
that is the thing to fix first.
