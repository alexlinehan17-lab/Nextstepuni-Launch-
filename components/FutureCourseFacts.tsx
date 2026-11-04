import { ArrowUpRight } from 'lucide-react';
import { REGIONS, getCoursePageUrl, type CAOCourse as Course } from './futureFinderData';

export const typicalEntry = (course: Course) => course.typicalPoints > 0
  ? `~${course.typicalPoints} points`
  : course.pathwayType === 'apprenticeship' ? 'Employer-based' : 'Open entry';

export function pointsDifference(course: Course, targetPoints: number) {
  if (course.typicalPoints === 0) return { label: 'Points gap', value: 'Not applicable', summary: 'No CAO points required' };
  const gap = course.typicalPoints - targetPoints;
  return gap > 0
    ? { label: 'Points gap', value: String(gap), summary: `${gap} ${gap === 1 ? 'point' : 'points'} above your target` }
    : gap < 0
      ? { label: 'Points ahead', value: String(-gap), summary: `${-gap} ${gap === -1 ? 'point' : 'points'} ahead of typical entry` }
      : { label: 'Points gap', value: '0', summary: 'Your target matches typical entry' };
}

export function CourseFacts({ course }: { course: Course }) {
  const facts = [
    ['Region', REGIONS[course.region] || course.region],
    ['Duration', `${course.duration} ${course.duration === 1 ? 'year' : 'years'}`],
    ['Salary band', course.salaryBand.charAt(0).toUpperCase() + course.salaryBand.slice(1)],
    ['Typical entry', typicalEntry(course)],
  ];
  return <dl className="ff-course-info">{facts.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>;
}

export function CoursePoints({ course, targetPoints }: { course: Course; targetPoints: number }) {
  const gap = pointsDifference(course, targetPoints);
  if (course.typicalPoints === 0) return <section className="ff-entry-route"><h3>Entry route</h3><p>{course.pathwayType === 'apprenticeship' ? 'Employer-based entry. Apply to an employer and check the apprenticeship’s training and entry requirements.' : 'Apply directly through the college. Check its current course and entry requirements.'} No CAO points are required.</p></section>;
  return <section className="ff-your-points"><h3>Your points, in context.</h3><dl><div><dt>Your target points</dt><dd>{targetPoints}</dd></div><div><dt>Typical entry · 2025</dt><dd>{course.typicalPoints}</dd></div><div><dt>{gap.label}</dt><dd>{gap.value}</dd></div></dl><p>{gap.summary}. Points change from year to year.</p></section>;
}

export function CollegeLink({ course }: { course: Course }) {
  const label = course.pathwayType === 'plc' ? 'Explore PLC courses' : course.pathwayType === 'apprenticeship' ? 'Visit apprenticeship page' : `Visit ${course.institution} page`;
  return <a className="ff-college-link" href={getCoursePageUrl(course)} target="_blank" rel="noopener noreferrer" aria-label={`${label} for ${course.title} (opens in a new tab)`}>{label}<ArrowUpRight size={16}/></a>;
}
