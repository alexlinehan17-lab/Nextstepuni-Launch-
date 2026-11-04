/** @license SPDX-License-Identifier: Apache-2.0 */
import rows from '../../data/paperTrail/physicalEducationTasks.json';
import type { PaperLang, PaperLevel } from '../../types/paperTrail';
import type { PaperTopicTags } from '../../types/paperTrailTopics';

export interface PhysicalEducationTask {
  cardId: string;
  subjectId: string;
  level: PaperLevel;
  lang: PaperLang;
  year: number;
  fileid: string;
  paperKey: string;
  n: string;
  parentQuestion: string;
  canonicalTopicId: string;
  specificationId: string;
  examTopicIds: string[];
  paperPages: number[];
  schemePages: number[];
  pageRotations: Record<number, 90 | 180 | 270>;
  questionRef: string;
  totalMarks: number;
}
export const PHYSICAL_EDUCATION_TASKS = rows as PhysicalEducationTask[];
type TaskIdentity = Pick<PhysicalEducationTask, 'subjectId' | 'year' | 'level' | 'lang' | 'fileid' | 'n'>;
const key = (q: TaskIdentity) => `${q.subjectId}|${q.year}|${q.level}|${q.lang}|${q.fileid}|${q.n}`;
const taskByKey = new Map(PHYSICAL_EDUCATION_TASKS.map(task => [key(task), task]));
export const physicalEducationTask = (q: TaskIdentity): PhysicalEducationTask | undefined => taskByKey.get(key(q));

/** Original numbered Paper Trail questions retain their identity and anchors.
 * Atlas uses the independently reviewed task boundaries for reviewed sittings.
 * English and Irish editions represent the same tasks; the original Irish
 * booklets remain in Paper Trail until their task-level wording is reviewed. */
export function withPhysicalEducationAtlasTasks(papers: PaperTopicTags[]): PaperTopicTags[] {
  const reviewedSittings = new Set(PHYSICAL_EDUCATION_TASKS.map(task => `${task.year}|${task.level}`));
  const result = papers.filter(paper => paper.subjectId !== 'physical-education'
    || !reviewedSittings.has(`${paper.year}|${paper.level}`));
  const taskPapers = new Map<string, PaperTopicTags>();
  for (const task of PHYSICAL_EDUCATION_TASKS) {
    const paperKey = `${task.year}|${task.level}|${task.lang}|${task.fileid}`;
    let paper = taskPapers.get(paperKey);
    if (!paper) {
      paper = { subjectId: task.subjectId, year: task.year, level: task.level,
        lang: task.lang, fileid: task.fileid, paperKey: task.paperKey, q: [] };
      taskPapers.set(paperKey, paper);
    }
    paper.q.push({ n: task.n, primary: task.canonicalTopicId });
  }
  return [...result, ...taskPapers.values()];
}

/** A task can have a different identity from its numbered Paper Trail anchor. */
export const fullPaperQuestionFor = (q: TaskIdentity): string => physicalEducationTask(q)?.parentQuestion ?? q.n;
