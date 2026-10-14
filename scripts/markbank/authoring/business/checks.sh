#!/bin/bash
# The Business checkpoint: the generator reproduction check, the Business test
# files and the type gate. Run it through the shared heavy-check lock.
#   bash scripts/markbank/authoring/business/checks.sh
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
mkdir -p tmp/business-review
python3 scripts/markbank/authoring/business/reproduce.py --schemes > tmp/business-review/reproduce-latest.log 2>&1
echo "reproduce exit $?" >> tmp/business-review/reproduce-latest.log
npm test -- test/markBankBusinessCompletion.test.tsx test/businessExamTopics.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts test/markBankAuthoringToolkit.test.ts test/markBankSession.test.tsx test/markBankSessionPlanning.test.ts test/markBankCoverage.test.ts test/markBankSchemes.test.ts test/businessGlyphs.test.ts > tmp/business-review/tests-latest.log 2>&1
echo "tests exit $?" >> tmp/business-review/tests-latest.log
npm run typecheck > tmp/business-review/typecheck-latest.log 2>&1
echo "typecheck exit $?" >> tmp/business-review/typecheck-latest.log
