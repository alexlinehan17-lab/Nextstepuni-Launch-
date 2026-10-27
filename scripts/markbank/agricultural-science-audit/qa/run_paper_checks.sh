#!/bin/bash
# usage: HEAVY=<path to heavy.sh> bash scripts/markbank/agricultural-science-audit/qa/run_paper_checks.sh <outdir>
# The per-paper gate: the eight targeted suites, browser QA over qa-cases.json, typecheck and typecheck:test.
cd "$(dirname "$0")/../../../.."
OUT="$1"; mkdir -p "$OUT"; H="${HEAVY:-}"
$H npx vitest run test/markBankCoverage.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts test/markBankAgriculturalScienceCompletion.test.ts test/agriculturalScienceExamTopics.test.ts test/vaultAnchors.test.ts test/waysInCorpus.test.ts > "$OUT/tests.log" 2>&1; echo "TESTS $?"
$H bash scripts/markbank/agricultural-science-audit/qa/run_browser_qa.sh "$OUT/browser"; echo "QA $?"
$H npm run typecheck > "$OUT/typecheck.log" 2>&1; echo "TC $?"
$H npm run typecheck:test > "$OUT/test-typecheck.log" 2>&1; echo "TCT $?"; grep "error TS" "$OUT/test-typecheck.log"
