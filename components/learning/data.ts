import type { CourseData } from '../Library';
import { MODULE_SECTIONS, type SectionInfo } from '../../moduleSections';
import { SUBJECT_MODULE_CONTENT } from '../../subjectModuleData';
export type LearningProgress = Record<string, { unlockedSection: number }>;
export function sectionsFor(course: Pick<CourseData, 'id' | 'sectionsCount'>): SectionInfo[] {
  if (MODULE_SECTIONS[course.id]) return MODULE_SECTIONS[course.id];
  const subject = /^subject-(.+)-protocol$/.exec(course.id)?.[1];
  const content = subject ? SUBJECT_MODULE_CONTENT[subject] : undefined;
  if (content?.sections) return content.sections.map(({ title, eyebrow }) => ({ title, eyebrow }));
  return Array.from({ length: course.sectionsCount }, (_, i) => ({ title: `Section ${i + 1}`, eyebrow: '' }));
}
export function learningState(progress: LearningProgress) {
  const sectionCount = (course: CourseData) => Math.min(course.sectionsCount, Math.max(0, progress[course.id]?.unlockedSection ?? 0));
  const isComplete = (course: CourseData) => course.sectionsCount > 0 && sectionCount(course) >= course.sectionsCount;
  const nextCourse = (courses: CourseData[]) => courses.find(c => sectionCount(c) > 0 && !isComplete(c)) ?? courses.find(c => !isComplete(c)) ?? courses[0];
  const nextSection = (course: CourseData) => sectionsFor(course)[Math.min(sectionCount(course), course.sectionsCount - 1)]?.title;
  return { sectionCount, isComplete, nextCourse, nextSection };
}
// A transient navigation intent only: progress remains the authority for unlocking.
const sectionRequests = new Map<string, number>();
export function requestModuleSection(moduleId: string, section: number) { sectionRequests.set(moduleId, section); }
export function requestedModuleSection(moduleId: string | null) { return moduleId ? sectionRequests.get(moduleId) : undefined; }
export function clearModuleSectionRequest(moduleId: string) { sectionRequests.delete(moduleId); }
