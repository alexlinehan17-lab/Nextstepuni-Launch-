import { sectionsFor } from '../components/learning/data';
import type { CourseData } from '../components/Library';
import estimates from '../data/moduleReadingEstimates.json';
import type { UserProgress } from '../types';

const OUTCOMES: Record<string, string> = {
  'agency-protocol': 'Choose one action you can take towards a goal that matters to you.',
  'hope-protocol': 'Make an alternative route when your original plan gets blocked.',
  'affirming-values-protocol': 'Identify the values you want your study choices to reflect.',
  'best-possible-self-protocol': 'Turn a future you want into an if–then plan for this week.',
  'grammar-of-grit-protocol': 'Rewrite a fixed judgement as a skill you can work on.',
  'agency-architecture-protocol': 'Separate what you can change from what you cannot control.',
  'strategic-advantage-protocol': 'Choose a study approach that makes use of your strengths.',
  'self-efficacy-protocol': 'Build confidence using evidence of small, specific successes.',
  'illusion-of-competence-protocol': 'Check whether you can recall an idea without your notes.',
  'procrastination-protocol': 'Write a small first step and a plan for the obstacle that stops you.',
  'neuroplasticity-protocol': 'Explain how repeated practice can change a skill over time.',
  'myelin-manual-protocol': 'Design a short practice block with attention to accuracy.',
  'praise-protocol': 'Give yourself useful feedback about effort, choices and methods.',
  'effective-struggle-protocol': 'Recognise when to persist, change methods or ask for help.',
  'science-of-making-mistakes-protocol': 'Use an error to choose what to practise next.',
  'autodidact-engine-protocol': 'Build a feedback loop: attempt, check, adjust and try again.',
  'power-of-yet-protocol': 'Turn something you cannot do yet into a workable next step.',
  'mastering-active-recall-protocol': 'Create a question that tests an idea from memory.',
  'mastering-spaced-repetition-protocol': 'Choose when to revisit a topic instead of cramming it once.',
  'mastering-interleaving-protocol': 'Mix related question types so you practise choosing a method.',
  'cognitive-architecture-protocol': 'Use attention, working memory and retrieval to plan a study block.',
  'elaborative-interrogation-protocol': 'Explain why an idea works and connect it to something you know.',
  'cognitive-endurance-protocol': 'Plan work and recovery across a demanding exam week.',
  'mental-modelling-protocol': 'Break a spatial problem into objects and transformations you can picture.',
  'bimodal-brain-protocol': 'Use focused work and a break deliberately when solving a problem.',
  'leaving-cert-strategy-protocol': 'Make a revision plan that accounts for your subjects and assessment.',
  'reverse-engineering-protocol': 'Work backwards from an exam date to a manageable weekly plan.',
  'exam-hall-strategies-protocol': 'Plan question selection, timing and checks for an exam paper.',
  'exam-crisis-management-protocol': 'Practise recovering focus when exam pressure interrupts your thinking.',
  'growth-mindset-protocol': 'Choose a different strategy after a setback, rather than label your ability.',
  'controllable-variables-protocol': 'Adjust one study or recovery habit and observe what happens.',
  'reframing-progress-protocol': 'Notice progress beyond a single grade and choose your next target.',
  'learning-math-protocol': 'Practise showing mathematical reasoning and using a question-specific marking scheme.',
  'linking-study-future-goals-protocol': 'Connect a current subject to options you want to keep open.',
  'game-day-protocol': 'Prepare a practical routine for the day before and morning of an exam.',
  'reframing-catastrophic-thoughts-protocol': 'Examine a worrying prediction and write a more balanced alternative.',
  'mastering-foreign-languages-protocol': 'Plan language practice across speaking, listening, reading and writing.',
  'emotional-intelligence-protocol': 'Name an emotion and choose a response that helps you move forward.',
  'mastering-the-sciences-protocol': 'Practise scientific explanations, calculations and investigation skills.',
  'mastering-the-humanities-protocol': 'Build an answer around a claim, supporting evidence and the question asked.',
  'mastering-english-protocol': 'Build an English answer around the question, textual evidence and analysis.',
  'mastering-business-protocol': 'Apply a business concept to evidence from a specific situation.',
  'applied-sciences-protocol': 'Plan project evidence and written practice for your technical subjects.',
  'digital-distraction-protocol': 'Set up a study environment with fewer interruptions.',
  'mastering-the-creatives-protocol': 'Practise a creative skill and explain the choices behind your work.',
  'points-optimization-protocol': 'Compare realistic subject targets when planning your Leaving Certificate points.',
  'marking-scheme-decoder-protocol': 'Read a marking scheme and identify what evidence an answer needs.',
  'answer-engineering-protocol': 'Structure an answer to respond directly to the command and available marks.',
  'learning-radar-protocol': 'Compare what you think you know with what an attempt actually shows.',
  'note-taking-paradox-protocol': 'Make notes that prompt thinking and recall rather than copying.',
  'teaching-effect-protocol': 'Explain an idea simply and use gaps in the explanation to guide revision.',
  'cognitive-load-protocol': 'Break a difficult task into steps your working memory can handle.',
  'implementation-protocol': 'Write a specific trigger and action for a study habit.',
  'context-effect-protocol': 'Vary a practice context and check whether you can still retrieve the idea.',
};
export function moduleOutcome(course: CourseData): string {
  return OUTCOMES[course.id] ?? (course.id.startsWith('subject-') ? `Build a revision plan for ${course.title.replace(/^Mastering /, '')} using your exam year, level and assessment requirements.` : course.description);
}
export function moduleReadingTime(course: CourseData, essentials = false): string {
  const counts = (estimates as Record<string, { full: number; essentials: number }>)[course.id];
  const words = counts?.[essentials ? 'essentials' : 'full'];
  if (!words) return `${Math.max(2, course.sectionsCount)}–${Math.max(4, course.sectionsCount * 2)} min reading`;
  const low = Math.max(2, Math.ceil(words / 220));
  return `About ${low}–${Math.max(low + 2, Math.ceil(words / 160))} min reading`;
}
export const MODULE_ENTRY_ROUTES = [
  { id: 'remember', title: 'I forget what I study', description: 'Try recall and build a review schedule.', moduleIds: ['mastering-active-recall-protocol', 'mastering-spaced-repetition-protocol', 'illusion-of-competence-protocol'] },
  { id: 'start', title: 'I keep putting it off', description: 'Make starting smaller and plan for distractions.', moduleIds: ['procrastination-protocol', 'implementation-protocol', 'digital-distraction-protocol'] },
  { id: 'understand', title: 'This topic won’t click', description: 'Break it down, explain it and get useful feedback.', moduleIds: ['cognitive-load-protocol', 'elaborative-interrogation-protocol', 'autodidact-engine-protocol'] },
  { id: 'exam', title: 'I’m preparing for an exam', description: 'Plan your revision and how you will approach the paper.', moduleIds: ['reverse-engineering-protocol', 'exam-hall-strategies-protocol', 'marking-scheme-decoder-protocol'] },
  { id: 'worry', title: 'Exam pressure is getting to me', description: 'Prepare a recovery plan and work through a worrying thought.', moduleIds: ['exam-crisis-management-protocol', 'reframing-catastrophic-thoughts-protocol', 'emotional-intelligence-protocol'] },
  { id: 'direction', title: 'I want something to aim for', description: 'Explore a future you care about and a next step towards it.', moduleIds: ['best-possible-self-protocol', 'linking-study-future-goals-protocol', 'hope-protocol'] },
];
export function directResumeCourse(courses: CourseData[], progress: UserProgress): CourseData | undefined {
  const visited = courses.filter(course => progress[course.id]?.reading?.lastVisitedAt)
    .sort((a, b) => (progress[b.id].reading?.lastVisitedAt ?? '').localeCompare(progress[a.id].reading?.lastVisitedAt ?? ''));
  return visited[0] ?? courses.find(course => (progress[course.id]?.unlockedSection ?? 0) > 0 && (progress[course.id]?.unlockedSection ?? 0) < course.sectionsCount);
}
export function searchModuleSections(courses: CourseData[], query: string) {
  const words = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  if (!words.length) return [];
  const matches = (text: string) => words.every(word => text.toLocaleLowerCase().includes(word));
  return courses.flatMap(course => {
    const sections = sectionsFor(course).map((section, index) => ({ ...section, index })).filter(section => matches(`${course.title} ${section.title} ${section.eyebrow}`));
    return matches(`${course.title} ${course.description} ${course.tags.join(' ')} ${moduleOutcome(course)}`) || sections.length ? [{ course, sections }] : [];
  });
}
