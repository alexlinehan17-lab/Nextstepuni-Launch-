/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The single model's topic record, derived (plan section 5, M1-M3): one record per ask, keyed by the card id, giving
 * the printed question the ask belongs to and the Topic Atlas headings it is filed under. The Mark Bank and the Topic
 * Atlas both read the generated file (data/atlasModel/<subject>.json, components/PaperTrail/atlasModel.ts); this module
 * is what writes it (scripts/atlas-model/build-ask-topics.mjs) and what the check re-derives it with
 * (test/atlasModelChecks.test.ts), so the committed file can never drift from the deck and the Atlas.
 *
 * Biology's rule is the one test/markBankBiologyReview.test.ts already holds every card to: the card's printed
 * question is an Atlas question; of that question's reviewed exam-topic headings (examTopicIdsForQuestion), the card
 * is filed under each one whose crosswalk (ExamTopicDefinition.curriculumNodeIds) holds the card's own curriculum
 * topic (topicId and additionalTopicIds; bio-u1 is read as bio-u2, the test's ATLAS_UNIT_EQUIV). Nothing here is a
 * new judgement: it narrows the question-level headings to the ones each part's own topic belongs to.
 */
import { loadCards, levelsFor } from '../../components/MarkBank/deck';
import { topicsForPaper } from '../../components/PaperTrail/topics';
import { isDeferredFileid } from '../../components/PaperTrail/sitting';
import {
  curriculumNodeIdsForExamTopic, examTopicDefinition, examTopicIdsForQuestion, examTopicTaxonomyFor,
} from '../../data/examTopics/registry';
import type { SecCard } from '../../types/markBank';

/** Subjects whose Mark Bank and Topic Atlas read one topic record per ask. */
export const MODEL_SUBJECTS = ['biology'] as const;

/** Curriculum topics with no Atlas heading of their own, read as the topic the subject's own Atlas check uses. */
const NODE_EQUIV: Record<string, Record<string, string>> = { biology: { 'bio-u1': 'bio-u2' } };

export interface AskTopicFile {
  v: 1;
  subjectId: string;
  atlasSubjectId: string;
  headings: string;
  rule: string;
  groups: Array<{ id: string; level: string; label: string; topics: number[] }>;
  topics: Array<{ id: string; level: string; code: string; title: string }>;
  /** [year, level, booklet, printed question number, [[card id, [topic index…]]…]] */
  questions: Array<[number, string, string, string, Array<[string, number[]]>]>;
}

const splitLabel = (label: string) => {
  const m = /^((?:\d+(?:\.\d+)*\.?)|(?:U\d+))\s+(.*)$/.exec(label.trim());
  return m ? { code: m[1].replace(/\.$/, ''), title: m[2] } : { code: '', title: label.trim() };
};

export interface AskDerivation { file: AskTopicFile; problems: string[] }

export async function deriveAskTopics(subjectId: string): Promise<AskDerivation> {
  const taxonomy = examTopicTaxonomyFor(subjectId);
  if (!taxonomy) throw new Error(`${subjectId} has no Atlas exam-topic headings`);
  // One topic list: the course the cards' own curriculum topics are crosswalked to (Biology: the new course).
  const groups = taxonomy.groups.filter(group => group.course === 'new' || !group.course);
  const topicIds = groups.flatMap(group => group.topicIds);
  const topicIndex = new Map(topicIds.map((id, index) => [id, index]));
  const equiv = NODE_EQUIV[subjectId] ?? {};
  const problems: string[] = [];
  const byQuestion = new Map<string, AskTopicFile['questions'][number]>();
  const cards: SecCard[] = [];
  for (const level of levelsFor(subjectId)) cards.push(...await loadCards(subjectId, level));
  for (const card of [...cards].sort((a, b) => a.id.localeCompare(b.id))) {
    const n = /\bQ(\d+)/.exec(card.questionRef)?.[1];
    const fileid = `${String(card.paperFileid).replace(/\.pdf$/i, '')}.pdf`;
    const paper = topicsForPaper(subjectId, card.year, card.level as 'higher' | 'ordinary', 'ev', fileid);
    if (!n || !paper || !paper.q.some(q => q.n === n)) { problems.push(`${card.id}: no Atlas question ${fileid} Q${n}`); continue; }
    const filed = examTopicIdsForQuestion(subjectId, card.level as 'higher' | 'ordinary', card.year,
      isDeferredFileid(fileid) ? 'deferred' : 'main', n, paper.paperKey, 'ev', fileid);
    const nodes = new Set([card.topicId, ...(card.additionalTopicIds ?? [])].map(id => equiv[id] ?? id));
    const own = filed.filter(id => topicIndex.has(id) && examTopicDefinition(id)?.level === card.level
      && curriculumNodeIdsForExamTopic(id).some(node => nodes.has(node)));
    if (!own.length) { problems.push(`${card.id}: ${[...nodes].join('+')} under none of Q${n}'s headings`); continue; }
    const key = `${card.year}|${card.level}|${fileid}|${n}`;
    const entry = byQuestion.get(key) ?? [card.year, card.level, fileid, n, []];
    entry[4].push([card.id, own.map(id => topicIndex.get(id)!).sort((a, b) => a - b)]);
    byQuestion.set(key, entry);
  }
  const questions = [...byQuestion.values()].sort((a, b) => b[0] - a[0] || a[1].localeCompare(b[1])
    || a[2].localeCompare(b[2]) || Number(a[3]) - Number(b[3]));
  return {
    problems,
    file: {
      v: 1,
      subjectId,
      atlasSubjectId: subjectId,
      headings: 'Topic Atlas exam-topic headings (new course), one list per level',
      rule: 'scripts/atlas-model/askTopics.ts: each part is filed under the headings of its printed question whose crosswalk holds the part\'s own curriculum topic.',
      groups: groups.map(group => ({ id: group.id, level: group.level, label: group.label.replace(/^.*?·\s*(?=Strand|Unifying)/, ''), topics: group.topicIds.map(id => topicIndex.get(id)!) })),
      topics: topicIds.map(id => { const d = examTopicDefinition(id)!; return { id, level: d.level, ...splitLabel(d.label) }; }),
      questions,
    },
  };
}
