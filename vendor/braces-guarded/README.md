# Bounded braces for build tooling

This private, MIT-licensed fork retains the published `braces@3.0.3` implementation
and API. It adds a fixed maximum depth of 64 in the parser (brace and parenthesis
blocks), and iterative AST-depth validation before compile, expand and stringify.
Caller options cannot raise the limit. Deep or cyclic child-node graphs fail with
a controlled `SyntaxError` before an upstream recursive walker runs.

Upstream provenance: npm `braces@3.0.3`, tarball integrity
`sha512-yQbXgO/OSZVD2IsiLlro+7Hf6Q18EJrKSEsdoMzKePKXct3gvD8oLcOQdIzGupr5Fj+EDe8gO/lxc1BzfMpxvA==`.
The upstream copyright and licence are retained in `LICENSE`.

The root override replaces the transitive build-tool dependency used by Tailwind,
Chokidar and Micromatch. It is not included in the browser or Functions runtime.
The npm audit step remains enabled and unchanged.

Reason: [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm),
reviewed 2 October 2026. The upstream advisory has no released patch as of
3 October 2026. Its report recommends limiting parser depth before recursive
walkers: [upstream issue 70](https://github.com/micromatch/braces/issues/70).

Regression coverage lives in `test/bracesGuard.test.ts`, including malicious
patterns, direct ASTs, representative globs and the installed override.
Remove this fork and override when a patched upstream release passes those
checks. Do not remove the audit or force a Tailwind major upgrade to hide it.
