import { buildStudentProfile, codeFromProfile, scoreCourseFit, RIASEC_LETTERS, type RiasecLetter, type WorkValue, type CourseFitResult } from './futureFinderRiasec';
import { RIASEC_ITEMS, VALUE_ITEMS } from './futureFinderRiasecItems';
import { CAO_COURSES, type CAOCourse } from './futureFinderData';
import { COURSE_RIASEC } from './futureFinderRiasecData';
import { compareRecommendations, scoreRecommendation } from './futureFinderRecommendation';

export function computeAnalysis(
  responses: Record<string, number>,
  valueResponses: Record<string, number>,
  studentPoints: number,
  studentSubjectNames: string[],
) {
  const byScale: Partial<Record<RiasecLetter, number[]>> = {};
  for (const it of RIASEC_ITEMS) { const r = responses[it.id]; if (r) (byScale[it.scale] ??= []).push(r); }
  const studentProfile = buildStudentProfile(byScale);
  const studentCode = codeFromProfile(studentProfile);
  const valScore: Partial<Record<WorkValue, number>> = {};
  for (const v of VALUE_ITEMS) { const r = valueResponses[v.id]; if (r) valScore[v.value] = (valScore[v.value] ?? 0) + r; }
  const studentValues = (Object.entries(valScore).sort((a, b) => (b[1] as number) - (a[1] as number)).slice(0, 3).map((x) => x[0]) as WorkValue[]);
  const scored = CAO_COURSES
    .map((course) => {
      const cr = COURSE_RIASEC[course.code];
      if (!cr) return null;
      const fit = scoreCourseFit({ studentProfile, studentCode, studentPoints, studentSubjects: studentSubjectNames, studentValues, course: { ...cr, typicalPoints: course.typicalPoints } });
      return { course, fit, recommendation: scoreRecommendation(course, fit, studentPoints) };
    })
    .filter((x): x is { course: CAOCourse; fit: CourseFitResult; recommendation: ReturnType<typeof scoreRecommendation> } => x !== null)
    .sort(compareRecommendations);
  const maxScale = Math.max(1, ...RIASEC_LETTERS.map((l) => studentProfile[l]));
  return { studentProfile, studentCode, studentValues, maxScale, shown: scored.filter((s) => s.fit.fitBucket !== 'none').slice(0, 24) };
}

export type CourseResult = ReturnType<typeof computeAnalysis>["shown"][number];
