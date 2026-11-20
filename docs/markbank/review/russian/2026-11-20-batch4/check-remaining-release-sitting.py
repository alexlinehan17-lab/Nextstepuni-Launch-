"""Check one approved older sitting, including preserved one-to-many ask evidence."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys

root = Path.cwd()
old = Path('/Users/alexlinehan/Documents/Nextstepuni-Russian-Continuation-20261106')
plans = Path('/Users/alexlinehan/Documents/NextStepUni-MarkBank-Lanes-20261104')
year, short = int(sys.argv[1]), sys.argv[2]
level = {'hl': 'higher', 'ol': 'ordinary'}[short]
out = root / f'tmp/russian-release/{year}-{short}'
out.mkdir(parents=True, exist_ok=True)
base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert root.name == 'Nextstepuni-Russian-Release-20261119'
import re
assert re.fullmatch(r'codex/russian-release-20261119(?:-batch-[2-9])?', subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip())

def run(name, command, allowed=(0,)):
    assert shutil.disk_usage(root).free > 8 * 1024 ** 3, 'Free disk below 8 GB'
    with (out / f'{name}.log').open('w') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    print(name, result.returncode, flush=True)
    if result.returncode not in allowed:
        print((out / f'{name}.log').read_text()[-18000:], flush=True)
        raise SystemExit(result.returncode or 1)

def read(relative):
    return json.loads((root / relative).read_text())

def previous(relative):
    return json.loads(subprocess.check_output(['git', 'show', base + ':' + relative]))

def serial(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'

run('author', ['python3', f'scripts/markbank/authoring/ru_review_{year}_{short}.py'])
source_check = root / f'scripts/markbank/authoring/test_ru_{year}_{short}_sources.py'
if source_check.exists():
    run('source', ['python3', '-m', 'unittest', 'discover', '-s', 'scripts/markbank/authoring', '-p', source_check.name, '-v'])
run('source-passages', ['python3', '-c',
    'import json,sys;sys.path.insert(0,"scripts/markbank/authoring");from ru_verify_review import verify;'
    + f'verify([c for c in json.load(open("scripts/markbank/authored/russian-reviewed.json")) if c["year"]=={year} and c["level"]=={level!r}])'])
run('runtime', ['node', 'scripts/markbank/build-russian-reviewed.mjs'])
run('deck', ['node', 'scripts/markbank/build-deck.mjs', 'scripts/markbank/authored/russian.json'])
run('anchors', ['node', 'scripts/paper-trail/build-russian-reviewed-anchors.mjs', f'{year}:{level}'])
run('tags', ['node', 'scripts/paper-trail/topic-tags/build-tags.mjs'])
run('showcase', ['node', 'scripts/build-subject-showcase.mjs'])
run('ask-topics', ['node', 'scripts/landing/ask-topics.mjs'])

# Remove only this sitting's superseded exclusion records after its original
# papers and source-backed boundaries have passed. Other sittings stay untouched.
exclusions = 'scripts/markbank/authoring/exclusions/russian.json'
items = read(exclusions)
remaining = [x for x in items if not x['ref'].startswith(f'{year} {short.upper()} ')]
(root / exclusions).write_text(serial(remaining))

runtime_path = 'components/MarkBank/cards/russian/reviewed.json'
legacy = {c['id']: c for c in previous('scripts/markbank/authored/russian.json')}
before = {**legacy, **{c['id']: c for c in previous(runtime_path)}}
after = {**legacy, **{c['id']: c for c in read(runtime_path)}}
selected = {cid: c for cid, c in after.items() if c['year'] == year and c['level'] == level}
proposal = {c['id']: c for c in json.loads((plans / 'REVIEW/2026-11-19-russian-after-release/proposed-runtime-cards.json').read_text())}
body = lambda card: {k: v for k, v in card.items() if k != 'qa'}
assert not before.keys() - after.keys()
for cid, card in before.items():
    assert after[cid]['conceptId'] == card['conceptId'], cid
    if cid not in selected:
        assert after[cid] == card, ('Unrelated card changed', cid)
for cid, card in selected.items():
    assert body(card) == body(proposal[cid]), ('Differs from approved proposal', cid)

sources = {s['id']: s for s in read('scripts/markbank/authoring/russian-reviewed-sources.json')}
tags = read('scripts/paper-trail/topic-tags/tags/russian.json')
for cid, card in selected.items():
    source = sources[cid]
    identities = source.get('atlasQuestions', [])
    assert len(identities) <= 1, ('Unexpected multi-ask identity', cid)
    key = identities[0]['n'] if identities else source.get('atlasQuestionKey', cid.removeprefix(f'ru-{year}-{short}-'))
    maps = read(f"public/paper-answers/{year}/{source['paperFileid']}.json")
    matches = [q for q in maps['q'] if q['n'] == key]
    question_pages = source.get('questionPages', source.get('paperPages'))
    assert isinstance(question_pages, list) and question_pages and all(isinstance(page, int) and page > 0 for page in question_pages), cid
    assert len(matches) == 1 and matches[0]['pP'] == question_pages[0], cid
    if source.get('atlasQuestionKey') or identities:
        assert matches[0]['markBankCardId'] == cid, cid
    else:
        assert matches[0].get('markBankCardId', cid) == cid, cid
    tag = next(t for t in tags if t['year'] == year and t['fileid'] == source['paperFileid'] and t['lang'] == 'ev')
    question = next(q for q in tag['q'] if q['n'] == key)
    assert question['primary'] == card['topicId'], (cid, question)

# The model lane is independently re-filing the released cards. Supply only
# new asks or asks whose question/topic changed; do not replace its decisions
# for existing unchanged questions with a mechanical copy of card.topicId.
filing_path = root / 'scripts/atlas-model/filings/russian.json'
if filing_path.exists():
    filing = json.loads(filing_path.read_text())
else:
    filing = json.loads((old / 'scripts/atlas-model/filings/russian.json').read_text())
    filing['asks'] = {}
filing_ids = [cid for cid, card in selected.items() if cid not in before or any(
    card.get(field) != before[cid].get(field)
    for field in ['questionText', 'questionRef', 'topicId', 'additionalTopicIds'])]
for cid in filing_ids:
    filing['asks'][cid] = [[after[cid]['topicId']], 'x']
filing['releaseScope'] = 'New or changed asks replayed after the 19 November release. Combine with the coordinator’s independent Stage 1r filings before enabling the single model; unchanged existing asks are deliberately not re-filed here.'
filing_path.parent.mkdir(parents=True, exist_ok=True)
filing_path.write_text(serial(filing))

run('cardlint', ['python3', 'scripts/markbank/authoring/ru_cardlint.py'])
run('reconcile', ['python3', 'scripts/markbank/authoring/reconcile.py', 'russian', '--baseline', 'write', '--json', str(out / 'ledger.json')], allowed=(0, 1, 120))
ledger = json.loads((out / 'ledger.json').read_text())
paper = next(p for p in ledger['papers'] if p['year'] == year and p['level'] == short)
queue = json.loads((plans / 'codex-continuation-20261106/russian/REPLAY-QUEUE-20261119.json').read_text())
expected = next(row for row in queue['sittings'] if row['year'] == year and row['level'] == short)
assert paper['covered'] == paper['leaves'] == expected['asksCountedFromPapers'], paper
assert len(selected) == expected['candidateCards'] and not paper['open'] and paper['excluded'] == 0, paper
if paper['leaves'] != len(selected):
    assert (year, short) == (2015, 'hl') and paper['leaves'] == len(selected) + 1
    joint = selected['ru-2015-hl-l3-3']
    assert joint['totalMarks'] == 8
    assert len(sources[joint['id']]['printedQuestionParts']) == 2
test_prefix = f'russian{year}{"Higher" if short == "hl" else "Ordinary"}Reviewed.test.'
tests = sorted((root / 'test').glob(test_prefix + '*'))
if (year, short) == (2026, 'hl'):
    tests = [root / 'test/russian2026Reviewed.test.ts']
assert len(tests) == 1 and tests[0].is_file(), tests
test = str(tests[0].relative_to(root))
run('required', ['node', 'node_modules/vitest/vitest.mjs', 'run', test, 'test/russian2026Reviewed.test.ts', 'test/russian2019ApprovedIntegration.test.tsx', 'test/russian2020ApprovedIntegration.test.tsx', 'test/russianHostedAnswerRoutes.test.ts', 'test/markBankCardPreservation.test.ts', 'test/curriculumRegistry.test.ts', 'test/markBankDeck.test.ts', 'test/markBankCoverage.test.ts', 'test/paperTrailAnswers.test.ts', 'test/russianSummaryLanguageExceptions.test.ts', '--maxWorkers=1', '--pool=threads'])
run('changed-lint', ['node', 'node_modules/eslint/bin/eslint.js', test, 'test/russianHostedAnswerRoutes.test.ts', '--max-warnings', '0'])
for folder in ['components/MarkBank/cards', 'scripts/markbank/authored']:
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', base, folder], text=True).splitlines()
    for relative in paths:
        if '/russian/' in relative or '/russian' in relative or relative.endswith('/sizes.json'):
            continue
        assert (root / relative).read_bytes() == subprocess.check_output(['git', 'show', base + ':' + relative]), relative
result = {'checkedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'base': base,
    'sitting': f'Russian {year} {level.title()}', 'asksCarded': paper['covered'], 'cards': len(selected),
    'newCards': sum(cid not in before for cid in selected),
    'changedExistingCards': sum(cid in before and body(card) != body(before[cid]) for cid, card in selected.items()),
    'unchangedReviewedCards': sum(cid in before and body(card) == body(before[cid]) for cid, card in selected.items()),
    'allPreviousIdsAndConceptIdsPreserved': True, 'otherRussianCardsByteIdentical': True,
    'selectedCardsExactlyMatchApprovedProposalExceptQaDate': True,
    'allOtherSubjectCardFilesByteIdentical': True, 'selectedCardAtlasPrimaryMismatches': 0,
    'supersededExclusionsRemoved': len(items) - len(remaining),
    'subjectReconciliation': 'ledger.json; later approved sittings still to replay',
    'sourceFilingsProvidedThisSitting': len(filing_ids), 'sourceFilingsProvidedInBatch': len(filing['asks']),
    'generatedModel': 'Coordinator must combine these new/changed asks with its independent Stage 1r filings; model builder pending on this base'}
(out / 'validation.json').write_text(serial(result))
review = root / f'scripts/markbank/authoring/reviews/russian-{year}-{short}-release-20261119'
review.mkdir(parents=True, exist_ok=True)
(review / 'validation.json').write_text(serial(result))
print(serial(result), flush=True)
