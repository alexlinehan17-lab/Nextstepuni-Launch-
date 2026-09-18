# Claude reconciliation — 18 September 2026

Base: `8a8963c3` on `main`. The approved Star Crew, Listening Room, Journey,
subject showcase and student-header work is retained.

## Included

- `fix/july-remainder-english-banner`: the remaining source-grounded English
  module corrections and Paper Trail availability notice. The notice now
  describes a failed sample accurately, limits request time and retries on a
  later visit after its one-minute cache expires.
- `waysin/census-fixes-8`: its last three commits. Earlier batches were already
  integrated through PRs #169, #171, #172 and #173. The resulting key-parts
  implementation matches the branch without replacing newer app screens.
- `markbank/maths-neighbour-solution-fix`: both dependent corrections, covering
  adjacent worked-solution crops and three question figures. Main's later
  printed wording for 2022 HL P2 Q10(c) and 2024 HL P1 Q2(b) is retained.
  The Maths content fingerprint reflects precisely those two retained changes
  relative to the Claude branch. Existing consolidation aliases remain.
- `markbank/engineering-e3-e4-e5-port`: the committed parser/marking corrections
  and five additional cards. The branch withdraws the invalid mini-excavator
  card `eng-2025-ol-q2-c-i`: it asked for three materials but awarded four marks
  for the seat alone. The local SEC scheme transcript (2025 OL, printed p.8)
  prices three materials at three marks each. This is an explicitly recorded
  content correction, not a taxonomy deletion. The subject remains incomplete.
- Subject-showcase counts regenerated from the reconciled live decks.

## Already included or superseded

Remote Claude branches `latest-codebase-changes-3pdtz1` and
`github-version-check-uvjuwn` are ancestors of main. The Economics chart-card
patch is already integrated. The older Accounting/Applied Maths branch is
superseded by main's verified curriculum taxonomy. The July branch's Biology,
History, Home Economics and examiner-insight work had already been ported.

Older Codex design explorations are accounted for in the 13 September release
record. Rejected prototypes and private PwC documents are not release assets.

## Separate working copy

The uncommitted expansion in `Nextstepuni-English` on `markbank/irish` is not
merged here. It is a separate, much larger corpus change, and wholesale copying
would overwrite newer cards. Its inclusion was raised with the owner.

## Validation

The initial integrated run passed 5,837 tests; three reconciliation failures
were then corrected: the Maths fingerprint, combined preservation arithmetic,
and regenerated subject counts. The focused preservation, curriculum, deck,
coverage and subject-showcase rerun passed all 365 tests. These checks verify
integration and identities; they do not establish exam-corpus completeness.
