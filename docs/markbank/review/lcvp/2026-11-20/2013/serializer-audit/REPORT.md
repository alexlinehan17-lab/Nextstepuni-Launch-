All 183 asks and all 840 marks were emitted. The complete comparison of all 183 generated objects found no lost non-empty source or scoring content. All 292 rows retain their printed wording, options, controls and marks.

The strict verifier stopped at the first of four empty `rows[0].contextNote` strings omitted by the unchanged generator: 2011 A7-2; 2013 B2(i), C1(b), and C1(b)-2. Its existing line 2167 emits this optional property only when truthy. The input verifier had documented empty top-level fields but not this nested field. The current any-N renderer also shows the note only when truthy, so an empty string and absent property both show no note.

A future verifier can allow exactly this empty-string-to-missing normalization, while comparing every other field and every non-empty note exactly. It must not prune arbitrary falsy values or alter the source cards. All six generated metadata fields per ask and all 183 paper bindings match the expected existing generator behavior.

The original failed run, its result flags and all input/output bytes remain unchanged. This read-only diagnostic does not certify the later checks that the failed run never reached, nor application, Atlas or release readiness. No generator or browser was run.
