/** Portable authoring contract checks; no PDFs, Vite, or runtime deck imports. */
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync, mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  reviewedRussianJointTask, verifyRussianJointAnchors, verifyRussianJointTags,
  russianQuestionTag, mergeRussianQuestionTag,
} from './russianJointTasks.mjs';
import { validateReviewedRussianQuestionTopics } from './russianJointTopics.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const read = path => JSON.parse(readFileSync(join(root, path), 'utf8'));
const registry = read('scripts/markbank/authoring/russian-joint-tasks.json');
const sources = read('scripts/markbank/authoring/russian-reviewed-sources.json');
const cards = read('components/MarkBank/cards/russian/reviewed.json');
const source = sources.find(row => row.id === 'ru-2011-hl-c2');
const card = cards.find(row => row.id === source.id);
const task = registry.tasks.find(row => row.id === source.id);
const originalMap = read('scripts/paper-trail/answers/2011/LC099ALP000EV.pdf.json');
const originalTag = read('scripts/paper-trail/topic-tags/tags/russian.json')
  .find(row => row.year === 2011 && row.fileid === source.paperFileid && row.level === source.level);

// Synthetic topic annotations on the real, already reviewed four-question shape.
// These are contract fixtures, not a reinterpretation of the original topics.
function explicitFixture() {
  const fixture = structuredClone({ source, card, registry: { version: 1, tasks: [task] } });
  fixture.registry.tasks[0].questions.forEach((q, index) => {
    q.topicId = index % 2 ? 'russian-0-3' : 'russian-1-0';
    q.additionalTopicIds = [];
  });
  syncQuestions(fixture);
  fixture.card.topicId = fixture.source.topicId = 'russian-1-0';
  fixture.card.additionalTopicIds = ['russian-0-3'];
  return fixture;
}
function syncQuestions(fixture) {
  fixture.source.atlasQuestions = fixture.registry.tasks[0].questions
    .map(({ leafKey: _leaf, ...question }) => structuredClone(question));
}
const check = fixture => reviewedRussianJointTask(fixture.source, fixture.card, fixture.registry);
const canonical = (fixture, atRoot = root) => validateReviewedRussianQuestionTopics(
  atRoot, [fixture.source], [fixture.card], fixture.registry,
);

test('all existing joint sources validate without changing their JSON or legacy tags', async () => {
  const before = JSON.stringify({ sources, cards, originalMap, originalTag });
  const questions = reviewedRussianJointTask(source, card);
  assert.equal(questions.length, 4);
  verifyRussianJointAnchors(source, card, originalMap);
  verifyRussianJointTags(source, card, originalTag);
  for (const q of questions) {
    const expected = { n: q.n, primary: source.topicId,
      ...(card.additionalTopicIds?.length ? { secondary: card.additionalTopicIds[0] } : {}) };
    assert.deepEqual(russianQuestionTag(q, source, card), expected);
    const old = originalTag.q.find(row => row.n === q.n);
    assert.deepEqual(mergeRussianQuestionTag(structuredClone(old), q, source, card), old);
  }
  await validateReviewedRussianQuestionTopics(root, sources, cards);
  assert.equal(JSON.stringify({ sources, cards, originalMap, originalTag }), before);
});

test('explicit leaf topics resolve through the actual year-specific Russian registry', async () => {
  const fixture = explicitFixture();
  assert.equal(check(fixture).length, 4);
  await canonical(fixture);
});

test('rejects partial topic annotations, duplicate IDs, whitespace and a second secondary', () => {
  for (const change of [
    q => { delete q[1].topicId; },
    q => { delete q[1].additionalTopicIds; },
    q => { q[0].topicId = ''; },
    q => { q[0].topicId = ' russian-1-0'; },
    q => { q[0].additionalTopicIds = [q[0].topicId]; },
    q => { q[0].additionalTopicIds = ['russian-0-3', 'russian-0-9']; },
  ]) {
    const fixture = explicitFixture();
    change(fixture.registry.tasks[0].questions); syncQuestions(fixture);
    assert.throws(() => check(fixture));
  }
});

test('rejects incomplete, duplicate and extra card topic coverage', () => {
  for (const additionalTopicIds of [[], ['russian-0-3', 'russian-0-3'], ['russian-0-3', 'russian-0-9']]) {
    const fixture = explicitFixture(); fixture.card.additionalTopicIds = additionalTopicIds;
    assert.throws(() => check(fixture));
  }
});

test('rejects synchronized missing pages and duplicate original question identities', () => {
  for (const change of [
    q => { q[0].n = ''; },
    q => { q[1].n = q[0].n; },
    q => { q[1].questionRef = q[0].questionRef; },
    q => { q[0].questionPages = []; },
    q => { q[0].questionPages = [99]; },
    q => { q[0].schemePages = [8, 8]; },
    q => { q[0].schemePages = ['8']; },
  ]) {
    const fixture = explicitFixture(); change(fixture.registry.tasks[0].questions); syncQuestions(fixture);
    fixture.source.coveredQuestionRefs = fixture.source.atlasQuestions.map(q => q.questionRef);
    assert.throws(() => check(fixture));
  }
});

test('rejects unknown source identities, wrong year/level and absent or mismatched original evidence', () => {
  for (const change of [
    f => { f.source.year = 2019; },
    f => { f.source.level = 'ordinary'; },
    f => { f.source.id = 'ru-2011-hl-unknown'; },
    f => { f.source.atlasQuestions[0].n = 'c2-unknown'; },
    f => { f.source.atlasQuestions[0].questionPages = [99]; },
    f => { f.source.atlasQuestions[0].schemePages = []; },
    f => { f.source.atlasQuestions[0].questionText = ''; },
    f => { f.source.coveredQuestionRefs.push(f.source.coveredQuestionRefs[0]); },
  ]) {
    const fixture = explicitFixture(); change(fixture);
    assert.throws(() => check(fixture));
  }
});

test('rejects synchronized noncanonical topics and unsupported level through the actual registry', async () => {
  const unknown = explicitFixture();
  unknown.registry.tasks[0].questions[0].topicId = 'russian-invented';
  unknown.card.additionalTopicIds.push('russian-invented'); syncQuestions(unknown);
  await assert.rejects(canonical(unknown), /Noncanonical Russian question topic/);
  const wrongLevel = explicitFixture();
  for (const row of [wrongLevel.source, wrongLevel.card, wrongLevel.registry.tasks[0]]) row.level = 'foundation';
  await assert.rejects(canonical(wrongLevel), /No canonical Russian specification/);
});

test('removes stale secondary only for an explicit replacement and preserves unrelated metadata', () => {
  const fixture = explicitFixture();
  const question = check(fixture)[0];
  const old = { n: question.n, primary: 'russian-0-9', secondary: 'russian-3-1', conf: 0.75, reviewer: 'original' };
  const changed = mergeRussianQuestionTag(structuredClone(old), question, fixture.source, fixture.card);
  assert.deepEqual(changed, { n: question.n, primary: question.topicId, conf: 0.75, reviewer: 'original' });
  const withSecondary = { ...question, additionalTopicIds: ['russian-0-3'] };
  assert.equal(mergeRussianQuestionTag(structuredClone(old), withSecondary, fixture.source, fixture.card).secondary, 'russian-0-3');
  const legacy = reviewedRussianJointTask(source, card)[0];
  assert.equal(mergeRussianQuestionTag(structuredClone(old), legacy, source, card).secondary, old.secondary);
});

test('checks every original anchor and exact topic identity, retaining unrelated tag metadata', () => {
  const fixture = explicitFixture();
  const questions = check(fixture);
  const tags = { q: questions.map(q => ({ ...russianQuestionTag(q, fixture.source, fixture.card), conf: 1 })) };
  verifyRussianJointAnchors(fixture.source, fixture.card, originalMap, fixture.registry);
  verifyRussianJointTags(fixture.source, fixture.card, tags, fixture.registry);
  for (const change of [
    t => { t.q.pop(); },
    t => { t.q.push(structuredClone(t.q[0])); },
    t => { t.q[0].primary = 'russian-0-9'; },
    t => { t.q[0].secondary = 'russian-0-9'; },
  ]) {
    const changed = structuredClone(tags); change(changed);
    assert.throws(() => verifyRussianJointTags(fixture.source, fixture.card, changed, fixture.registry));
  }
  const missingAnchor = structuredClone(originalMap);
  missingAnchor.q = missingAnchor.q.filter(q => q.n !== questions[0].n);
  assert.throws(() => verifyRussianJointAnchors(fixture.source, fixture.card, missingAnchor, fixture.registry));
});

test('caches registries by resolved worktree root and respects the selected year and topic level', async () => {
  const folder = mkdtempSync(join(tmpdir(), 'russian-registry-test-'));
  try {
    const fixture = explicitFixture();
    const permitted = "{levels:['higher'],groups:[{topics:[{id:'russian-1-0'},{id:'russian-0-3'}]}]}";
    writeFileSync(join(folder, 'curriculumRegistry.ts'), `export const resolveCurriculumSpecification = (subject, year) => subject === 'russian' && year === 2011 ? ${permitted} : undefined;`);
    await canonical(fixture, folder);
    const wrongYear = structuredClone(fixture);
    for (const row of [wrongYear.source, wrongYear.card, wrongYear.registry.tasks[0]]) row.year = 2019;
    await assert.rejects(canonical(wrongYear, folder), /No canonical Russian specification/);
    const other = mkdtempSync(join(folder, 'different-root-'));
    writeFileSync(join(other, 'curriculumRegistry.ts'), "export const resolveCurriculumSpecification = () => ({levels:['higher'],groups:[{topics:[{id:'russian-1-0',levels:['ordinary']},{id:'russian-0-3'}]}]});");
    await assert.rejects(canonical(fixture, other), /Noncanonical Russian question topic russian-1-0/);
    await canonical(fixture, root);
    await canonical(fixture, join(folder, '.'));
  } finally { rmSync(folder, { recursive: true, force: true }); }
});
