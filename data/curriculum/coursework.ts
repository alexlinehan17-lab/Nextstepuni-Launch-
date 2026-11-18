/** Assessment research overlay. The canonical registry still owns subjects and specifications. */
import research from './courseworkResearch.json';
import { curriculumSubjectsForYear, resolveCurriculumSpecification } from '../../curriculumRegistry';

export type CourseworkFamily = 'research' | 'investigation' | 'making' | 'action' | 'portfolio' | 'modelling';
type ResearchRow = (typeof research.rows)[keyof typeof research.rows];
const rows: Record<string, ResearchRow> = research.rows;
export const courseworkSources = research.sources;
export const COURSEWORK_REVIEW_DATE = research.reviewedAt;
export function courseworkCatalogue(year: number) {
  return curriculumSubjectsForYear(year, ['leaving-certificate-established', 'lcvp'])
    .map(subject => ({ ...subject, research: year === 2027 || year === 2028 ? rows[subject.id] : undefined }))
    .sort((a, b) => a.name.localeCompare(b.name));
}
export function courseworkBrief(subjectId: string, year: number) {
  const specification = resolveCurriculumSpecification(subjectId, year);
  const row = year === 2027 || year === 2028 ? rows[subjectId] : undefined;
  if (!specification || !row) return undefined;
  const canCreate = !row.category.startsWith('Oral') && row.category !== 'Written examination only';
  const family: CourseworkFamily = row.category === 'Investigation' ? 'investigation' : row.category === 'Making / performance' ? 'making' : row.category === 'Action' ? 'action' : row.category === 'Portfolio' ? 'portfolio' : row.category === 'Modelling' ? 'modelling' : 'research';
  const limits = year === 2027 ? ({ business: { words: 1500, images: 10 }, biology: { words: 1500, images: 20 }, chemistry: { words: 1500, images: 20 }, physics: { words: 1500, images: 20 }, latin: { words: 1700 }, 'ancient-greek': { words: 1700 }, 'climate-action-and-sustainable-development': { words: 1800, images: 10 }, 'drama-film-and-theatre-studies': { words: 1700, images: 20 } } as Record<string, { words: number; images?: number }>)[subjectId] : undefined;
  return { specification, family, canCreate, assessment: year === 2027 ? row.assessment2027 : row.assessment2028, work: row.work, notes: row.notes,
    sources: row.sources.map(key => research.sources[key as keyof typeof research.sources]), limits,
    // Research dates are deliberately not scheduled until final SEC circulars are reconciled.
    dateStatus: 'Confirm your completion date with your teacher. Add their checkpoint to your plan.' };
}
export const workflowGuides: Record<CourseworkFamily, { capture: string; connection: string; steps: string[] }> = {
  research: { capture: 'Which source changed your thinking? Keep its author, date and page with your notes.', connection: 'What does this evidence support, and where does it fall short?', steps: ['Agree a focused question with my teacher', 'Gather and evaluate my sources', 'Connect evidence to my argument', 'Review my own writing and references', 'Prepare for teacher review'] },
  investigation: { capture: 'Record the conditions, units and raw observations now, while you can still explain them.', connection: 'What pattern did you find? What else could explain it?', steps: ['Agree my question and method with my teacher', 'Plan supervised evidence collection', 'Record my data and method decisions', 'Analyse findings and limitations', 'Prepare my report for teacher review'] },
  making: { capture: 'Keep a version or photo before you change it. What did you test, and what will change next?', connection: 'Which design choice does this test justify?', steps: ['Read the brief and agree my approach', 'Explore and record possible approaches', 'Make and document my work', 'Test, refine and explain decisions', 'Check the required files and prepare for review'] },
  action: { capture: 'What actually happened? Record your contribution and any evidence of an effect.', connection: 'What changed because of the action? What can you reasonably claim?', steps: ['Investigate the issue and agree an action', 'Plan responsibilities and evidence', 'Carry out and document my contribution', 'Evaluate the effect and limitations', 'Prepare my individual account for review'] },
  portfolio: { capture: 'Save one specific experience, what you did, and what you learned from it.', connection: 'What does this experience show about your learning?', steps: ['Check the required task with my teacher', 'Gather evidence from real experiences', 'Explain my own contribution and learning', 'Select evidence that fits the brief', 'Prepare the required submission for review'] },
  modelling: { capture: 'Keep your assumptions, calculations and model versions. Label estimates separately from measured data.', connection: 'How well does the model fit? Which assumption matters most?', steps: ['Choose and scope a problem from the brief', 'State assumptions and build a model', 'Test it using suitable evidence', 'Refine and evaluate the model', 'Prepare my report for teacher review'] },
};
