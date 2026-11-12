/** Reviewed Russian questions sharing one published allocation.
 * The manifest is independently checked against pinned originals by the mandatory
 * authoring gate. Other subjects do not use this explicit coverage mechanism.
 */
import { readFileSync } from 'node:fs';
import { isDeepStrictEqual } from 'node:util';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const manifest = JSON.parse(readFileSync(resolve(root, 'scripts/markbank/authoring/russian-joint-tasks.json'), 'utf8'));
const compact = text => typeof text === 'string' ? text.replace(/\s+/g, ' ').trim() : '';
const same = (actual, expected, label) => {
  if (!isDeepStrictEqual(actual, expected)) throw new Error(`Russian joint task: ${label} does not match reviewed originals`);
};

export function reviewedRussianJointTask(source, card, registry = manifest) {
  const matches = registry.tasks.filter(task => task.id === source.id);
  if (matches.length > 1) throw new Error(`Duplicate reviewed Russian joint task ${source.id}`);
  const expected = matches[0];
  const declaresJoint = Object.hasOwn(source, 'coveredQuestionRefs') || Object.hasOwn(source, 'atlasQuestions');
  if (!expected && !declaresJoint) return null;
  if (!expected) throw new Error(`Unreviewed Russian joint task ${source.id}`);
  same(card?.subjectId, 'russian', 'subject');
  same(card.section, expected.section, 'card section');
  for (const key of ['id', 'year', 'level', 'questionRef']) {
    same(source[key], expected[key], `source ${key}`);
    same(card[key], expected[key], `card ${key}`);
  }
  for (const key of ['component', 'paperFileid', 'schemeFileid', 'paperPages', 'schemePages']) {
    same(source[key], expected[key], key);
  }
  same(source.questionPages, expected.paperPages, 'joint question pages');
  same(card.sourceMaterial?.pages, expected.paperPages, 'complete source passage pages');
  const questions = expected.questions.map(({ leafKey: _key, ...question }) => question);
  const refs = questions.map(question => question.questionRef);
  same(source.coveredQuestionRefs, refs, 'covered question references');
  same(source.atlasQuestions, questions, 'Atlas question identities/prompts/pages');
  if (new Set(refs).size !== refs.length || new Set(questions.map(q => q.n)).size !== questions.length) {
    throw new Error('Duplicate reviewed Russian joint question identity');
  }
  for (const question of questions) {
    if (!compact(question.n) || question.n !== compact(question.n) || !compact(question.questionRef)) {
      throw new Error('Missing Russian joint question identity');
    }
    for (const [key, allowed] of [['questionPages', expected.paperPages], ['schemePages', expected.schemePages]]) {
      const pages = question[key];
      if (!Array.isArray(pages) || !pages.length || new Set(pages).size !== pages.length
          || pages.some(page => !Number.isInteger(page) || page < 1 || !allowed.includes(page))) {
        throw new Error(`Missing or out-of-scope Russian joint ${key} for ${question.questionRef}`);
      }
    }
    if (!compact(question.questionText) || !compact(card.questionText).includes(compact(question.questionText))) {
      throw new Error(`Russian joint task omits original prompt ${question.questionRef}`);
    }
  }
  const explicitTopics = questions.some(q => Object.hasOwn(q, 'topicId') || Object.hasOwn(q, 'additionalTopicIds'));
  if (explicitTopics) {
    const union = new Set();
    for (const question of questions) {
      if (!compact(question.topicId) || !Array.isArray(question.additionalTopicIds)
          || question.additionalTopicIds.length > 1) {
        throw new Error(`Missing or unsupported Russian question topics ${question.questionRef}`);
      }
      const ids = [question.topicId, ...question.additionalTopicIds];
      if (ids.some(id => !compact(id) || id !== compact(id)) || new Set(ids).size !== ids.length) {
        throw new Error(`Invalid or duplicate Russian question topics ${question.questionRef}`);
      }
      for (const id of ids) union.add(id);
    }
    const cardTopics = [card.topicId, ...(card.additionalTopicIds ?? [])];
    if (new Set(cardTopics).size !== cardTopics.length) throw new Error('Duplicate Russian joint-card topics');
    same([...cardTopics].sort(), [...union].sort(), 'complete joint-card topic coverage');
  }
  return questions;
}

export function verifyRussianJointAnchors(source, card, map, registry = manifest) {
  const questions = reviewedRussianJointTask(source, card, registry);
  if (!questions) return;
  same(map.paperFileid, source.paperFileid, 'Atlas paper');
  same(map.schemeFileid, source.schemeFileid, 'Atlas scheme');
  for (const question of questions) {
    const anchors = map.q.filter(anchor => anchor.n === question.n);
    if (anchors.length !== 1) throw new Error(`Missing or duplicate Russian Atlas question ${question.n}`);
    const anchor = anchors[0];
    same(anchor.markBankCardId, card.id, `${question.n} Mark Bank resolution`);
    same(anchor.label, question.questionRef.replace(/^\d+ (?:HL|OL) /, ''), `${question.n} label`);
    same(anchor.pP, question.questionPages[0], `${question.n} question page`);
    same(anchor.paperRegion, source.paperPages.map(p => ({ p, r: [0, 0, 1, 1] })), `${question.n} complete passage`);
    same(anchor.region, question.schemePages.map(p => ({ p, r: [0, 0, 1, 1] })), `${question.n} scheme pages`);
  }
}


/** Exact per-question topics, or the unchanged legacy joint-card fallback. */
export function russianQuestionTag(question, source, card) {
  const explicit = Object.hasOwn(question, 'topicId');
  const topics = explicit ? question.additionalTopicIds : card.additionalTopicIds;
  return { n: question.n, primary: explicit ? question.topicId : source.topicId,
    ...(topics?.length ? { secondary: topics[0] } : {}) };
}

/** Preserve old tag metadata while removing only explicitly superseded topics. */
export function mergeRussianQuestionTag(existing, question, source, card) {
  const tag = russianQuestionTag(question, source, card);
  if (!existing) return tag;
  Object.assign(existing, tag);
  if (Object.hasOwn(question, 'topicId') && !Object.hasOwn(tag, 'secondary')) delete existing.secondary;
  return existing;
}

export function verifyRussianJointTags(source, card, tag, registry = manifest) {
  const questions = reviewedRussianJointTask(source, card, registry);
  if (!questions) return;
  for (const question of questions) {
    const records = tag.q.filter(q => q.n === question.n);
    if (records.length !== 1) throw new Error(`Missing or duplicate Russian question topic ${question.n}`);
    same({ n: records[0].n, primary: records[0].primary, ...(Object.hasOwn(records[0], 'secondary') ? { secondary: records[0].secondary } : {}) }, russianQuestionTag(question, source, card), `${question.n} source-reviewed topics`);
  }
}
