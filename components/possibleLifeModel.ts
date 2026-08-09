import { CAREERS } from '../careerPathsData';
import type { CareerCard, CareerField } from '../types/careerPaths';

export const LIFE_PRIORITIES = [
  'creative', 'secure', 'social', 'independent', 'outdoors', 'useful',
  'flexible', 'challenging', 'calm', 'well-paid', 'close-to-home', 'open-to-travel',
] as const;

export type LifePriority = typeof LIFE_PRIORITIES[number];

export const PRIORITY_LABELS: Record<LifePriority, string> = {
  creative: 'Creative', secure: 'Secure', social: 'Social', independent: 'Independent',
  outdoors: 'Outdoors', useful: 'Useful', flexible: 'Flexible', challenging: 'Challenging',
  calm: 'Calm', 'well-paid': 'Well-paid', 'close-to-home': 'Close to home',
  'open-to-travel': 'Open to travel',
};

const FIELD_SIGNALS: Partial<Record<LifePriority, CareerField[]>> = {
  creative: ['creative', 'design', 'tech'], secure: ['health', 'education', 'engineering', 'trades'],
  social: ['health', 'psychology', 'education', 'business', 'law'], independent: ['tech', 'creative', 'design', 'science'],
  outdoors: ['animals', 'engineering', 'trades', 'science'], useful: ['health', 'education', 'psychology', 'engineering', 'trades'],
  flexible: ['tech', 'creative', 'design', 'business'], challenging: ['health', 'law', 'engineering', 'science', 'tech'],
  calm: ['design', 'science', 'education', 'animals'], 'well-paid': ['tech', 'law', 'health', 'engineering', 'business'],
};

const KEYWORDS: Partial<Record<LifePriority, string[]>> = {
  social: ['people', 'team', 'client', 'patient', 'teach'], independent: ['independent', 'focus', 'autonomy'],
  outdoors: ['outdoor', 'site', 'field', 'land'], flexible: ['flexible', 'remote', 'freelance', 'hybrid'],
  creative: ['creative', 'design', 'build', 'make'], useful: ['help', 'care', 'solve', 'support'],
  challenging: ['complex', 'problem', 'pressure', 'research'], calm: ['calm', 'steady', 'quiet'],
  'open-to-travel': ['travel', 'international', 'abroad'], 'close-to-home': ['community', 'local'],
};

const haystack = (career: CareerCard) => [career.tagline, ...career.whatYouDo, ...career.skills, ...career.pros].join(' ').toLowerCase();

export function scoreCareer(career: CareerCard, priorities: LifePriority[], matchedIds: string[] = []): number {
  const text = haystack(career);
  return priorities.reduce((score, priority) => {
    const fieldScore = FIELD_SIGNALS[priority]?.includes(career.field) ? 4 : 0;
    const wordScore = KEYWORDS[priority]?.some((word) => text.includes(word)) ? 2 : 0;
    const payScore = priority === 'well-paid' ? career.salary.experiencedK / 25 : 0;
    return score + fieldScore + wordScore + payScore;
  }, matchedIds.includes(career.id) ? 7 : 0);
}

/** Three possibilities, deliberately diversified. They are lenses, not a ranking. */
export function buildPossibilities(priorities: LifePriority[], matchedIds: string[] = []): CareerCard[] {
  const ranked = [...CAREERS].sort((a, b) => scoreCareer(b, priorities, matchedIds) - scoreCareer(a, priorities, matchedIds) || a.title.localeCompare(b.title));
  const picked: CareerCard[] = [];
  const match = ranked.find((career) => matchedIds.includes(career.id));
  if (match) picked.push(match);
  if (!picked.length && ranked[0]) picked.push(ranked[0]);
  const adjacent = ranked.find((career) => !picked.some((item) => item.id === career.id) && career.field !== picked[0]?.field);
  if (adjacent) picked.push(adjacent);
  const different = ranked.find((career) => !picked.some((item) => item.id === career.id) && !picked.some((item) => item.field === career.field));
  if (different) picked.push(different);
  for (const career of ranked) if (picked.length < 3 && !picked.some((item) => item.id === career.id)) picked.push(career);
  return picked.slice(0, 3);
}

export const FIELD_DAY: Record<CareerField, { rhythm: string; people: string; setting: string }> = {
  health: { rhythm: 'The day is structured, but rarely predictable.', people: 'You work closely with patients and a wider clinical team.', setting: 'Hospitals, clinics and community settings can all feel very different.' },
  animals: { rhythm: 'Practical work and unexpected problems shape the day.', people: 'You work with owners, colleagues and animals that cannot explain what is wrong.', setting: 'The setting may move between clinics, farms and outdoor work.' },
  tech: { rhythm: 'Long stretches of focused work alternate with reviews and decisions.', people: 'You build with a team, even when much of the work is done independently.', setting: 'Office, hybrid and remote patterns vary greatly by employer.' },
  engineering: { rhythm: 'Planning, checking and problem-solving share the day.', people: 'You translate between technical specialists, clients and real constraints.', setting: 'The work may move between a desk, workshop and site.' },
  law: { rhythm: 'Deadlines and careful preparation give the day its pace.', people: 'Clients and colleagues rely on clear judgement and precise communication.', setting: 'The balance between research, meetings and hearings varies by role.' },
  psychology: { rhythm: 'Listening and analysis require sustained attention.', people: 'The work is deeply people-facing, with professional boundaries that matter.', setting: 'Clinical, educational, organisational and research settings differ substantially.' },
  business: { rhythm: 'Priorities can change quickly as information arrives.', people: 'The work usually involves clients, colleagues or stakeholders with competing needs.', setting: 'The environment depends heavily on the organisation and role.' },
  education: { rhythm: 'The timetable is structured; the human moments are not.', people: 'Your energy is spent helping other people understand and progress.', setting: 'Preparation and follow-up continue beyond the visible classroom day.' },
  design: { rhythm: 'Exploration gives way to critique, revision and delivery.', people: 'You balance your own judgement with feedback from clients and collaborators.', setting: 'Studio, agency, in-house and freelance work each create a different life.' },
  science: { rhythm: 'Careful method and patient investigation shape progress.', people: 'You work independently at times, but evidence is challenged and shared.', setting: 'Laboratory, field and desk-based research offer distinct routines.' },
  trades: { rhythm: 'The day is concrete: diagnose, make, test and finish.', people: 'You coordinate with customers, other trades and the people sharing the site.', setting: 'Travel, early starts and changing sites can be part of the bargain.' },
  creative: { rhythm: 'Ideas matter, but deadlines and revision make them real.', people: 'Even personal creative work is shaped by audiences, commissioners or collaborators.', setting: 'Income and routine may be less predictable, particularly early on.' },
};
