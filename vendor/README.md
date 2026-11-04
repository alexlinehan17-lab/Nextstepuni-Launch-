# Temporary development-tool dependency patch

`braces-3.0.4-nextstepuni.1.tgz` is a private local build, **not an upstream npm
release**. It preserves the MIT licence and upstream authorship. Its source is
micromatch/braces PR #72 at `28d440b5dd449dbf1fe6f3506cf94ecca4d02660`:
https://github.com/micromatch/braces/pull/72

The reviewed advisory GHSA-vfj7-8cjw-p6xm has no published patched version as of
3 October 2026. The upstream proposed fix limits nesting to 100 in the parser and
AST walkers and rejects cyclic parent chains. This prevents stack exhaustion in
the build tools used by Tailwind, glob matching and Firebase CLI without a major
Tailwind migration or disabling dependency audits. It is not bundled into the app.

The source revision's 904 upstream tests pass. The repository regression test
checks malicious patterns/direct ASTs, attempts to raise the cap, and ordinary
sets/ranges. Package metadata records provenance. Replace this override with the
official patched release when available.

To reproduce: download the pinned upstream revision; set package.json version to
`3.0.4-nextstepuni.1`, private to true and add the nextstepuniPatch provenance block;
run `npm pack --ignore-scripts`. No library implementation changes are made beyond
the pinned upstream pull request.
