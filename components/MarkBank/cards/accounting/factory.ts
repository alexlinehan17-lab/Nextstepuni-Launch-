/** @license SPDX-License-Identifier: Apache-2.0 */
import type { AccountingRubric, CardSourceMaterial, SecRubricCard } from '../../../../types/markBank';
import { resolveCurriculumSpecification } from '../../../../curriculumRegistry';
import authored from './authored.json';

type AuthoredTask = Omit<(typeof authored.cards)[number], 'level' | 'schemeRegions'> & {
  level: 'higher' | 'ordinary';
  schemeRegions: Array<{ p: number; r: [number, number, number, number]; rotate?: 0 | 90 | 180 | 270 }>;
};

const makeCard = (task: AuthoredTask): SecRubricCard => {
  const specification = resolveCurriculumSpecification('accounting', task.year);
  if (!specification || !specification.groups.some(group => group.topics.some(topic => topic.id === task.topicId))) {
    throw new Error(`${task.id}: missing canonical Accounting curriculum node`);
  }
  const sourceMaterial: CardSourceMaterial = {
    kind: 'source-table', label: `Question ${task.taskKey}`, title: 'Figures, tables and instructions',
    pages: task.paperPages, attribution: '© State Examinations Commission',
    presentationNote: 'Original Accounting examination pages. All figures and adjustments remain in their printed layout.',
  };
  const solution: AccountingRubric['solution'] = {
    kind: 'marking-scheme', label: `Question ${task.taskKey}`, title: 'Worked solution and mark allocation',
    sourceFileid: task.paperFileid,
    pages: [...new Set(task.schemeRegions.map(region => region.p))],
    regions: task.schemeRegions, attribution: '© State Examinations Commission',
    presentationNote: 'Original SEC marking scheme, including the workings associated with this task. Page numbers refer to the PDF.',
  };
  return {
    id: task.id, subjectId: 'accounting', level: task.level, topicId: task.topicId,
    conceptId: `accounting-${task.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`,
    source: 'sec', kind: 'rubric', year: task.year, paperFileid: task.paperFileid.replace(/\.pdf$/, ''),
    section: task.questionNumber <= 4 ? '1' : task.questionNumber <= 7 ? '2' : '3',
    questionRef: `${task.year} ${task.level === 'higher' ? 'HL' : 'OL'} Q${task.taskKey}`,
    stem: task.taskFocus ? `${task.title}. ${task.taskFocus}` : task.title,
    questionText: task.questionText, totalMarks: task.totalMarks, sourceMaterial,
    schemeCitation: `SEC Accounting ${task.year} ${task.level === 'higher' ? 'Higher' : 'Ordinary'} Level, PDF pages ${solution.pages.join(', ')} — © State Examinations Commission.`,
    schemeRegion: { schemeFileid: task.paperFileid, ...task.schemeRegions[0] },
    specVersion: specification.id,
    qa: {
      gates: ['verbatim-paper-prompt', 'visual-paper-and-scheme-review', 'published-task-allocation', 'complete-source-pages', 'selection-review'],
      humanReviewedBy: 'Codex visual PDF audit (no human sign-off claimed)',
      humanReviewedAt: task.reviewedAt,
    },
    rubric: { system: 'accounting', solution, allocationNote: task.allocationNote, taskFocus: task.taskFocus ?? undefined },
  };
};

export const accountingCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  (authored.cards as AuthoredTask[]).filter(task => task.level === level).map(makeCard);
