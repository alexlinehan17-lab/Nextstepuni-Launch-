/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ── Types ──────────────────────────────────────────────────

export interface StrategyPrompt {
  moduleId: string;
  strategyName: string;
  phase: 'start' | 'mid' | 'push';
  prompt: string;
}

export interface StudySessionRecord {
  id: string;
  date: string; // YYYY-MM-DD
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  plannedMinutes: number;
  actualSeconds: number;
  startedAt: number; // timestamp
  completedAt: number; // timestamp
  pointsEarned: number;
  hadReflection: boolean;
  strategiesShown?: string[]; // moduleIds of strategies used (auto-tracked + self-reported)
}

export interface StrategyDefinition {
  moduleId: string;
  strategyName: string;
  description: string;
}

export const STRATEGY_REGISTRY: StrategyDefinition[] = [
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', description: 'Test yourself from memory before reviewing notes' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', description: 'Review material at increasing intervals to build long-term memory' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', description: 'Mix different topics and problem types during practice' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', description: 'Ask "why" and "how" to deepen understanding' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', description: 'Set clear intentions and take ownership of your learning' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', description: 'Embrace challenge as a signal that learning is happening' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', description: 'Eliminate distractions and protect your attention' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', description: 'Monitor and adjust your learning strategies in real time' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', description: 'Practice under timed conditions to build exam readiness' },
];

// ── Duration Presets ───────────────────────────────────────

export const DURATION_PRESETS = [
  { minutes: 15 },
  { minutes: 25 },
  { minutes: 45 },
] as const;

// ── Points Config ──────────────────────────────────────────

export const STUDY_SESSION_POINTS = {
  PER_10_MINUTES: 5,
} as const;

// ── Subject Colors (duplicated from DeepFocusTimer.tsx to avoid refactoring) ──

export const SUBJECT_COLORS: Record<string, { dot: string; bg: string; border: string; text: string }> = {
  'English':    { dot: 'bg-blue-500',    bg: 'bg-blue-50 dark:bg-blue-900/20',    border: 'border-blue-200 dark:border-blue-800/40',    text: 'text-blue-700 dark:text-blue-300' },
  'Irish':      { dot: 'bg-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Mathematics':{ dot: 'bg-indigo-500',  bg: 'bg-indigo-50 dark:bg-indigo-900/20',  border: 'border-indigo-200 dark:border-indigo-800/40',  text: 'text-indigo-700 dark:text-indigo-300' },
  'French':     { dot: 'bg-rose-500',    bg: 'bg-rose-50 dark:bg-rose-900/20',    border: 'border-rose-200 dark:border-rose-800/40',    text: 'text-rose-700 dark:text-rose-300' },
  'German':     { dot: 'bg-amber-500',   bg: 'bg-amber-50 dark:bg-amber-900/20',   border: 'border-amber-200 dark:border-amber-800/40',   text: 'text-amber-700 dark:text-amber-300' },
  'Spanish':    { dot: 'bg-orange-500',  bg: 'bg-orange-50 dark:bg-orange-900/20',  border: 'border-orange-200 dark:border-orange-800/40',  text: 'text-orange-700 dark:text-orange-300' },
  'Italian':    { dot: 'bg-lime-500',    bg: 'bg-lime-50 dark:bg-lime-900/20',    border: 'border-lime-200 dark:border-lime-800/40',    text: 'text-lime-700 dark:text-lime-300' },
  'Japanese':   { dot: 'bg-pink-500',    bg: 'bg-pink-50 dark:bg-pink-900/20',    border: 'border-pink-200 dark:border-pink-800/40',    text: 'text-pink-700 dark:text-pink-300' },
  'Physics':    { dot: 'bg-cyan-500',    bg: 'bg-cyan-50 dark:bg-cyan-900/20',    border: 'border-cyan-200 dark:border-cyan-800/40',    text: 'text-cyan-700 dark:text-cyan-300' },
  'Chemistry':  { dot: 'bg-teal-500',    bg: 'bg-teal-50 dark:bg-teal-900/20',    border: 'border-teal-200 dark:border-teal-800/40',    text: 'text-teal-700 dark:text-teal-300' },
  'Biology':    { dot: 'bg-green-500',   bg: 'bg-green-50 dark:bg-green-900/20',   border: 'border-green-200 dark:border-green-800/40',   text: 'text-green-700 dark:text-green-300' },
  'Applied Mathematics': { dot: 'bg-violet-500', bg: 'bg-violet-50 dark:bg-violet-900/20', border: 'border-violet-200 dark:border-violet-800/40', text: 'text-violet-700 dark:text-violet-300' },
  'Agricultural Science': { dot: 'bg-lime-600', bg: 'bg-lime-50 dark:bg-lime-900/20', border: 'border-lime-200 dark:border-lime-800/40', text: 'text-lime-700 dark:text-lime-300' },
  'Computer Science':    { dot: 'bg-sky-500', bg: 'bg-sky-50 dark:bg-sky-900/20', border: 'border-sky-200 dark:border-sky-800/40', text: 'text-sky-700 dark:text-sky-300' },
  'Accounting':          { dot: 'bg-emerald-600', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Business':            { dot: 'bg-blue-600', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300' },
  'Economics':           { dot: 'bg-yellow-500', bg: 'bg-yellow-50 dark:bg-yellow-900/20', border: 'border-yellow-200 dark:border-yellow-800/40', text: 'text-yellow-700 dark:text-yellow-300' },
  'History':             { dot: 'bg-amber-600', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300' },
  'Geography':           { dot: 'bg-teal-600', bg: 'bg-teal-50 dark:bg-teal-900/20', border: 'border-teal-200 dark:border-teal-800/40', text: 'text-teal-700 dark:text-teal-300' },
  'Politics & Society':  { dot: 'bg-purple-500', bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800/40', text: 'text-purple-700 dark:text-purple-300' },
  'Religious Education': { dot: 'bg-fuchsia-500', bg: 'bg-fuchsia-50 dark:bg-fuchsia-900/20', border: 'border-fuchsia-200 dark:border-fuchsia-800/40', text: 'text-fuchsia-700 dark:text-fuchsia-300' },
  'Home Economics':      { dot: 'bg-orange-600', bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300' },
  'Music':               { dot: 'bg-pink-600', bg: 'bg-pink-50 dark:bg-pink-900/20', border: 'border-pink-200 dark:border-pink-800/40', text: 'text-pink-700 dark:text-pink-300' },
  'Art':                 { dot: 'bg-red-500', bg: 'bg-red-50 dark:bg-red-900/20', border: 'border-red-200 dark:border-red-800/40', text: 'text-red-700 dark:text-red-300' },
  'Construction Studies':{ dot: 'bg-stone-500', bg: 'bg-stone-50 dark:bg-stone-900/20', border: 'border-stone-200 dark:border-stone-800/40', text: 'text-stone-700 dark:text-stone-300' },
  'Engineering':         { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-900/20', border: 'border-zinc-200 dark:border-zinc-800/40', text: 'text-zinc-700 dark:text-zinc-300' },
  'Technology':          { dot: 'bg-slate-500', bg: 'bg-slate-50 dark:bg-slate-900/20', border: 'border-slate-200 dark:border-slate-800/40', text: 'text-slate-700 dark:text-slate-300' },
  'Design & Communication Graphics': { dot: 'bg-indigo-600', bg: 'bg-indigo-50 dark:bg-indigo-900/20', border: 'border-indigo-200 dark:border-indigo-800/40', text: 'text-indigo-700 dark:text-indigo-300' },
  'Physical Education':  { dot: 'bg-red-600', bg: 'bg-red-50 dark:bg-red-900/20', border: 'border-red-200 dark:border-red-800/40', text: 'text-red-700 dark:text-red-300' },
};

const DEFAULT_COLOR = { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' };

export function getSubjectColor(name: string) {
  return SUBJECT_COLORS[name] || DEFAULT_COLOR;
}

export const SUBJECT_STROKE_COLORS: Record<string, string> = {
  'English': 'stroke-blue-500',
  'Irish': 'stroke-emerald-500',
  'Mathematics': 'stroke-indigo-500',
  'French': 'stroke-rose-500',
  'German': 'stroke-amber-500',
  'Spanish': 'stroke-orange-500',
  'Italian': 'stroke-lime-500',
  'Japanese': 'stroke-pink-500',
  'Physics': 'stroke-cyan-500',
  'Chemistry': 'stroke-teal-500',
  'Biology': 'stroke-green-500',
  'Applied Mathematics': 'stroke-violet-500',
  'Agricultural Science': 'stroke-lime-600',
  'Computer Science': 'stroke-sky-500',
  'Accounting': 'stroke-emerald-600',
  'Business': 'stroke-blue-600',
  'Economics': 'stroke-yellow-500',
  'History': 'stroke-amber-600',
  'Geography': 'stroke-teal-600',
  'Politics & Society': 'stroke-purple-500',
  'Religious Education': 'stroke-fuchsia-500',
  'Home Economics': 'stroke-orange-600',
  'Music': 'stroke-pink-600',
  'Art': 'stroke-red-500',
  'Construction Studies': 'stroke-stone-500',
  'Engineering': 'stroke-zinc-500',
  'Technology': 'stroke-slate-500',
  'Design & Communication Graphics': 'stroke-indigo-600',
  'Physical Education': 'stroke-red-600',
};

export function getSubjectStroke(name: string): string {
  return SUBJECT_STROKE_COLORS[name] || 'stroke-purple-500';
}

// ── Strategy Prompts (27 across 9 strategies) ─────────────

export const STRATEGY_PROMPTS: StrategyPrompt[] = [
  // Active Recall (mastering-active-recall-protocol)
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', phase: 'start', prompt: 'Close your notes. Write down everything you remember about this topic before looking anything up.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', phase: 'mid', prompt: 'Pause and quiz yourself: what are the 3 most important ideas from what you just studied?' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', phase: 'push', prompt: 'Before you finish, explain the hardest concept from today in your own words — no peeking.' },

  // Spaced Repetition (mastering-spaced-repetition-protocol)
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', phase: 'start', prompt: 'Start by reviewing your flagged cards or notes from your last session on this topic.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', phase: 'mid', prompt: 'Which concepts feel shaky? Mark them for review tomorrow — spacing builds memory.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', phase: 'push', prompt: 'Schedule a 5-minute review of today\'s weak spots for 2 days from now.' },

  // Interleaving (mastering-interleaving-protocol)
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', phase: 'start', prompt: 'Mix it up: start with a different topic or problem type than you ended with last time.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', phase: 'mid', prompt: 'Switch to a different problem type or subtopic now — mixing strengthens your ability to choose strategies.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', phase: 'push', prompt: 'Try one problem that combines two different concepts you studied today.' },

  // Elaboration (elaborative-interrogation-protocol)
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', phase: 'start', prompt: 'Ask yourself "why does this work?" or "how does this connect to what I already know?"' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', phase: 'mid', prompt: 'Pick one concept and explain it as if teaching a friend who knows nothing about it.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', phase: 'push', prompt: 'Write one real-world example or analogy for the trickiest idea from today\'s session.' },

  // Agency Protocol (agency-protocol)
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', phase: 'start', prompt: 'Set a clear intention: what exactly will you know or be able to do after this session?' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', phase: 'mid', prompt: 'Rate your focus 1-10 right now. If it\'s below 7, take a 60-second reset and refocus.' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', phase: 'push', prompt: 'You chose to study — that\'s the hardest step. Finish strong with 5 more focused minutes.' },

  // Growth Mindset (growth-mindset-protocol)
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', phase: 'start', prompt: 'Remind yourself: struggle means growth. Difficulty is the signal that learning is happening.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', phase: 'mid', prompt: 'If something feels hard, lean in — your brain is literally building new connections right now.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', phase: 'push', prompt: 'Write down one thing that was difficult today and one thing you improved at. That\'s growth.' },

  // Deep Focus (digital-distraction-protocol)
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', phase: 'start', prompt: 'Put your phone face-down or in another room. Eliminate one distraction before you begin.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', phase: 'mid', prompt: 'If your mind wandered, that\'s normal. Gently bring it back — each refocus strengthens attention.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', phase: 'push', prompt: 'You\'re in the final stretch. Channel all focus into these last minutes — quality over quantity.' },

  // Metacognition (learning-radar-protocol)
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', phase: 'start', prompt: 'Before diving in, ask: what\'s my plan for this session? What strategy will I use?' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', phase: 'mid', prompt: 'Check in: is your current approach working? If not, what could you do differently right now?' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', phase: 'push', prompt: 'What worked well in this session? What will you do differently next time?' },

  // Exam Strategy (exam-hall-strategies-protocol)
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', phase: 'start', prompt: 'Set a timer for practice questions — simulating exam pressure builds real readiness.' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', phase: 'mid', prompt: 'Try answering one question under timed conditions, then check your answer structure.' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', phase: 'push', prompt: 'Review your practice answer: did you hit all the marks? Note what to improve for next time.' },
];
