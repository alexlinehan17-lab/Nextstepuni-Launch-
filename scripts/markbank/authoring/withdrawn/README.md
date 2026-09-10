# Withdrawn cards — the short list of ids that used to ship and no longer do

One JSON file per subject, `{ "<card id>": "<why>" }`. `rebaseline.py` refuses
to update the preservation baseline when a previously shipped id disappears —
that guard exists because a total wipe once recorded itself as a clean run —
and this is the only way past it. An entry here is a claim that the card was
WRONG, not that it was inconvenient, and the reason is what a later reader has
to be able to check.

A withdrawn id is never reused: card ids key a student's review history, so a
better card for the same ask is a NEW id, and the old address stays covered by
whatever now cites it.
