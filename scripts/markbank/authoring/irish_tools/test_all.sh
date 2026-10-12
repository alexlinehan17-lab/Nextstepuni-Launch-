#!/bin/bash
# Run every test file that touches Irish plus the shared topic/vault/curriculum gates, once.
# usage: test_all.sh [log-dir]   (default tmp/irish-tests). Heavy: run it under the session lock.
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
cd "$ROOT"
O=${1:-tmp/irish-tests}
mkdir -p "$O"
FILES=$(grep -li "irish" test/*.ts test/*.tsx | tr '\n' ' ')
EXTRA="test/examTopicRegistry.test.ts test/finalStudyclixExamTopics.test.ts test/paperTrailAnswers.test.ts test/paperTrailTopics.test.ts test/topicTagIntegrity.test.ts test/vaultTopics.test.ts test/vaultDeepLink.test.ts test/paperTrailPdfAssets.test.ts test/reviseByTopic.smoke.test.tsx test/curriculumCoverageSourceOfTruth.test.ts test/curriculum2026Inventory.test.ts"
echo "$FILES $EXTRA" | tr ' ' '\n' | grep -c . > "$O/file-count.txt"
npx vitest run $FILES $EXTRA --maxWorkers=1 > "$O/tests.log" 2>&1; status=$?
grep -E "Test Files|Tests " "$O/tests.log"
exit $status
