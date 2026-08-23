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
