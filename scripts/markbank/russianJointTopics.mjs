/** Canonical year-specific validation for explicit Russian joint-question topics.
 * Kept out of product/runtime imports. Only the authoring generators call it.
 */
import { resolve } from 'node:path';
import { build } from 'esbuild';
import { reviewedRussianJointTask } from './russianJointTasks.mjs';

const resolverPromises = new Map();
async function canonicalResolver(root) {
  const resolvedRoot = resolve(root);
  if (!resolverPromises.has(resolvedRoot)) resolverPromises.set(resolvedRoot, build({
    stdin: { contents: 'export { resolveCurriculumSpecification } from "./curriculumRegistry";',
      resolveDir: resolvedRoot, sourcefile: 'russian-joint-curriculum.ts', loader: 'ts' },
    bundle: true, format: 'esm', platform: 'node', write: false, logLevel: 'silent',
    plugins: [{ name: 'leave-lazy-decks-unloaded', setup(builder) {
      // Curriculum metadata does not call deck loaders. Keep those original
      // dynamic imports external instead of parsing every subject's JSON.
      builder.onResolve({ filter: /.*/ }, args => args.kind === 'dynamic-import' ? { external: true } : undefined);
    } }],
  }).then(async result => {
    const module = await import(`data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString('base64')}`);
    return module.resolveCurriculumSpecification;
  }).catch(error => {
    resolverPromises.delete(resolvedRoot);
    throw error;
  }));
  return resolverPromises.get(resolvedRoot);
}

export async function validateReviewedRussianQuestionTopics(root, sources, cards, registry) {
  const byId = new Map(cards.map(card => [card.id, card]));
  const explicit = sources.flatMap(source => {
    const card = byId.get(source.id);
    const questions = reviewedRussianJointTask(source, card, registry);
    return questions?.some(q => Object.hasOwn(q, 'topicId') || Object.hasOwn(q, 'additionalTopicIds'))
      ? [{ source, card, questions }] : [];
  });
  if (!explicit.length) return;
  const resolveSpecification = await canonicalResolver(resolve(root));
  for (const { source, card, questions } of explicit) {
    const specification = resolveSpecification('russian', source.year);
    if (!specification || !specification.levels.includes(source.level)) {
      throw new Error(`No canonical Russian specification for ${source.year}/${source.level}`);
    }
    const canonical = new Map(specification.groups.flatMap(group => group.topics).map(topic => [topic.id, topic]));
    for (const question of questions) {
      const ids = [question.topicId, ...(question.additionalTopicIds ?? [])];
      for (const id of ids) {
        const topic = canonical.get(id);
        if (!topic || (topic.levels && !topic.levels.includes(source.level))) {
          throw new Error(`Noncanonical Russian question topic ${String(id)} for ${question.questionRef}`);
        }
      }
    }
    for (const id of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
      if (!canonical.has(id)) throw new Error(`Noncanonical Russian joint card topic ${id}`);
    }
  }
}
