/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Chapter VII's course data, read straight from the app's list
 * (components/futureFinderData.ts — the same 149 rows Points Passport and
 * Future Finder use). Nothing here is typed by hand: the line, the body and
 * the card are assembled from a course's own fields, and the subjects are
 * kept only where the app knows a subject by that name.
 */

import { CAO_COURSES, INSTITUTIONS, REGIONS, type CAOCourse } from '../../futureFinderData';
import { LC_SUBJECTS } from '../../subjectData';
import { COPY } from '../copy';

const T = COPY.futurefinder;

export type { CAOCourse };
export const COURSE_COUNT = CAO_COURSES.length;

const APP_SUBJECTS = new Set(LC_SUBJECTS.map(s => s.name));

/** The course's bonus subjects, as the app names them. The data already uses the app's names; anything it does not know is dropped rather than guessed. */
export const subjectsOf = (c: CAOCourse): string[] => c.subjectBonus.filter(s => APP_SUBJECTS.has(s));

export const routeOf = (c: CAOCourse): 'cao' | 'plc' | 'apprenticeship' => c.pathwayType ?? 'cao';
export const institutionName = (c: CAOCourse): string => INSTITUTIONS[c.institution] ?? c.institution;
export const regionName = (c: CAOCourse): string => REGIONS[c.region] ?? c.region;

const YEARS = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six'];
export const durationWords = (n: number): string => {
  const word = Number.isInteger(n) ? YEARS[n] : undefined;
  return `${word ?? n} year${n === 1 ? '' : 's'}`;
};

/** The points figure for the card: the number, or the app's own words where the route has none. */
export const pointsLabel = (c: CAOCourse): string =>
  c.typicalPoints > 0 ? String(c.typicalPoints) : routeOf(c) === 'apprenticeship' ? T.noPoints.apprenticeship : T.noPoints.plc;

/** The italic line: code · institution · Level n · points — the points only where the data has them. */
export const courseLine = (c: CAOCourse): string => {
  const parts = [c.code, c.institution, `${T.level} ${c.level}`];
  if (c.typicalPoints > 0) parts.push(`${c.typicalPoints} ${T.points}`);
  return parts.join(' · ');
};

const list = (xs: string[], conj: string): string =>
  xs.length < 2 ? xs.join('') : `${xs.slice(0, -1).join(', ')} ${conj} ${xs[xs.length - 1]}`;

/** "at University College Dublin" — or the kind of place, where the row is a pathway rather than one named provider. */
const wherePhrase = (c: CAOCourse): string => {
  switch (c.institution) {
    case 'PLC': return 'on a Post Leaving Certificate course';
    case 'SOLAS': return 'as a SOLAS apprenticeship';
    case 'ETB': return 'with an Education and Training Board';
    default: return `at ${institutionName(c)}`;
  }
};

/** The rewritten body: what it is, how long and where, the subjects that count, where it leads, and what the app does with it. */
export const courseBody = (c: CAOCourse): string[] => {
  const body = [c.description, `${durationWords(c.duration)} ${wherePhrase(c)}, in ${regionName(c)}.`];
  const subjects = subjectsOf(c);
  if (subjects.length) body.push(`${T.card.subjects}: ${list(subjects, 'and')}.`);
  if (c.careerPaths.length) body.push(`${T.card.careers}: ${list(c.careerPaths, 'or')}.`);
  body.push(c.typicalPoints > 0 ? T.helps : T.helpsNoPoints);
  return body;
};

/** What the screen reader hears when the chapter turns. */
export const announceTurn = (c: CAOCourse): string =>
  T.turned.replace('{title}', c.title).replace('{institution}', institutionName(c)).replace('{line}', courseLine(c));

const haystack = (c: CAOCourse): string => `${c.code} ${c.title} ${c.institution} ${institutionName(c)}`.toLowerCase();

/**
 * Search by code, title or college. Every word typed must appear somewhere
 * in the row; rows are ordered by how the FIRST word hits — an exact code or
 * title, then a code prefix, a title prefix, a word inside the title, then
 * the college — and by the list's own order after that.
 */
export const searchCourses = (query: string, limit = 7): CAOCourse[] => {
  const words = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if (!words.length) return [];
  const [first] = words;
  const rank = (c: CAOCourse): number => {
    const title = c.title.toLowerCase();
    const code = c.code.toLowerCase();
    if (code === first || title === first) return 0;
    if (code.startsWith(first)) return 1;
    if (title.startsWith(first)) return 2;
    if (title.split(/[^a-z0-9]+/).some(w => w.startsWith(first))) return 3;
    if (title.includes(first)) return 4;
    return 5;
  };
  return CAO_COURSES
    .map((c, i) => ({ c, i, hay: haystack(c) }))
    .filter(x => words.every(w => x.hay.includes(w)))
    .map(x => ({ ...x, r: rank(x.c) }))
    .sort((a, b) => a.r - b.r || a.i - b.i)
    .slice(0, limit)
    .map(x => x.c);
};

/** The invitation under an empty field: the first row from a handful of places, in the list's own order. */
const firstFrom = (institution: string): CAOCourse | undefined => CAO_COURSES.find(c => c.institution === institution);
export const SAMPLE: CAOCourse[] = ['UCD', 'TCD', 'UCC', 'U of Galway', 'PLC', 'SOLAS']
  .map(firstFrom)
  .filter((c): c is CAOCourse => c !== undefined);
