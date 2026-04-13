/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ── Types ──────────────────────────────────────────────────

export type PromptCategory = 'action' | 'check-in' | 'technique-switch' | 'energy-focus';

export interface StrategyPrompt {
  moduleId: string;
  strategyName: string;
  category: PromptCategory;
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
  PER_10_MINUTES: 15,
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

// Maximally distinct hex colors for SVG chart lines (no two should look alike)
// Headspace-style maximally distinct subject colours
export const SUBJECT_HEX_COLORS: Record<string, string> = {
  'English': '#0984E3',           // bright blue
  'Irish': '#00B894',             // teal green
  'Mathematics': '#2D3436',       // near-black
  'French': '#E84393',            // hot pink
  'German': '#FDCB6E',           // warm yellow
  'Spanish': '#E17055',           // warm coral
  'Italian': '#00CEC9',           // cyan
  'Japanese': '#A29BFE',          // soft lavender
  'Physics': '#74B9FF',           // sky blue
  'Chemistry': '#55EFC4',         // mint
  'Biology': '#00B894',           // teal green
  'Applied Mathematics': '#6C5CE7', // vivid purple
  'Applied Maths': '#6C5CE7',     // vivid purple (alias)
  'Agricultural Science': '#BADC58', // lime
  'Computer Science': '#74B9FF',  // sky blue
  'Accounting': '#FDCB6E',        // warm yellow
  'Business': '#0984E3',          // bright blue
  'Economics': '#E67E22',         // strong orange
  'History': '#D63031',           // warm red
  'Geography': '#00B894',         // teal green
  'Politics & Society': '#E84393',// hot pink
  'Religious Education': '#A29BFE', // soft lavender
  'Home Economics': '#E17055',    // warm coral
  'Music': '#FD79A8',             // rose pink
  'Art': '#FF7675',               // salmon
  'Construction Studies': '#636E72',// cool grey
  'Engineering': '#636E72',       // cool grey
  'Technology': '#636E72',        // cool grey
  'Design & Communication Graphics': '#6C5CE7', // vivid purple
  'Physical Education': '#D63031',// warm red
};

export function getSubjectHex(name: string): string {
  return SUBJECT_HEX_COLORS[name] || '#a855f7';
}

// Headspace-style distinct palette — 10 maximally spread colours for index-based assignment
const DISTINCT_PALETTE = [
  '#0984E3', // bright blue
  '#E84393', // hot pink
  '#E67E22', // strong orange
  '#6C5CE7', // vivid purple
  '#00B894', // teal green
  '#D63031', // warm red
  '#FDCB6E', // warm yellow
  '#A29BFE', // soft lavender
  '#00CEC9', // cyan
  '#2D3436', // near-black
];

/**
 * Returns a guaranteed-distinct hex color for a subject index.
 * Uses the named color if available, otherwise cycles through a distinct palette.
 */
export function getDistinctSubjectHex(name: string, index: number): string {
  return SUBJECT_HEX_COLORS[name] || DISTINCT_PALETTE[index % DISTINCT_PALETTE.length];
}

// ── Prompt Timing Config ──────────────────────────────────

export const PROMPT_INTERVAL_SECONDS = 300; // 5 minutes between prompts
export const PROMPT_AUTO_DISMISS_SECONDS = 30; // auto-dismiss after 30s

// ── Strategy Prompts (~108 across 9 strategies, 12 each) ──

export const STRATEGY_PROMPTS: StrategyPrompt[] = [
  // ─── Active Recall (mastering-active-recall-protocol) ───
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'action', prompt: 'Close your notes. Write down everything you remember about this topic before looking anything up.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'action', prompt: 'Pause and quiz yourself: what are the 3 most important ideas from what you just studied?' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'action', prompt: 'Cover your notes and try to list all the key terms from this section. Then check what you missed.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'check-in', prompt: 'How much of what you just read could you explain without looking? If less than 60%, test yourself now.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'check-in', prompt: 'Are you re-reading or actually retrieving? Close the book and write what you know — that\'s real learning.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'check-in', prompt: 'Quick check: could you answer an exam question on this right now? If not, that\'s your signal to self-test.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'technique-switch', prompt: 'Try the "blank page" method: open a fresh page and write everything you know about the topic from memory.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'technique-switch', prompt: 'Switch from reading to testing: write 3 questions about what you just covered, then answer them without notes.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'technique-switch', prompt: 'Try verbal recall — explain this concept out loud as if presenting to your class. No notes allowed.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'energy-focus', prompt: 'Before you finish, explain the hardest concept from today in your own words — no peeking. You\'ve got this.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'energy-focus', prompt: 'Retrieval is hard on purpose — that effort is the learning happening. Keep going.' },
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', category: 'energy-focus', prompt: 'Every time you struggle to remember and then check, you\'re strengthening that memory trace. Push through.' },

  // ─── Spaced Repetition (mastering-spaced-repetition-protocol) ───
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'action', prompt: 'Start by reviewing your flagged cards or notes from your last session on this topic.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'action', prompt: 'Mark any concept that felt shaky just now. Schedule it for review in 2 days.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'action', prompt: 'Write down 3 things from today\'s session you\'d forget if you didn\'t review them. Plan when you\'ll revisit.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'check-in', prompt: 'Which concepts feel shaky? Mark them for review tomorrow — spacing builds memory.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'check-in', prompt: 'When did you last review this material? If it\'s been more than a week, the forgetting curve is steep — revisit now.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'check-in', prompt: 'Rate your confidence on this topic 1-10. Anything below 7 needs a spaced review scheduled this week.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'technique-switch', prompt: 'Instead of re-reading everything, focus only on the items you got wrong or hesitated on last time.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'technique-switch', prompt: 'Try the Leitner method: sort your flashcards into "know well", "sort of", and "don\'t know" piles. Focus on the last.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'technique-switch', prompt: 'Mix old review material with new content. Revisit one thing from last week alongside today\'s work.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'energy-focus', prompt: 'Schedule a 5-minute review of today\'s weak spots for 2 days from now. Future-you will thank you.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'energy-focus', prompt: 'Spacing feels slower but lasts longer. Trust the process — you\'re building permanent knowledge.' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', category: 'energy-focus', prompt: 'Even 5 minutes of spaced review beats 30 minutes of cramming. Small, consistent sessions win.' },

  // ─── Interleaving (mastering-interleaving-protocol) ───
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'action', prompt: 'Mix it up: switch to a different topic or problem type than what you\'ve been working on.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'action', prompt: 'Try one problem that combines two different concepts you\'ve studied today.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'action', prompt: 'Shuffle your practice — do 3 problems from 3 different sections rather than 9 from one section.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'check-in', prompt: 'Have you been working on the same type of problem for a while? Time to switch topics — mixing strengthens learning.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'check-in', prompt: 'Are you in a comfort zone with one topic? Jump to a harder one — the contrast helps both stick.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'check-in', prompt: 'Quick check: can you tell which strategy or formula to use without being told? That\'s the real skill interleaving builds.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'technique-switch', prompt: 'Try alternating between theory and practice problems every 10 minutes instead of doing all of one first.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'technique-switch', prompt: 'Pick a random past exam question from a different chapter. See if you can identify which approach to use.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'technique-switch', prompt: 'Compare two related concepts side by side — how are they similar? How are they different? This builds discrimination.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'energy-focus', prompt: 'Interleaving feels harder than blocked practice — but that difficulty is exactly what makes it more effective.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'energy-focus', prompt: 'The confusion you feel switching topics? That\'s your brain building the ability to choose the right approach.' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', category: 'energy-focus', prompt: 'Keep mixing it up — the exam won\'t group questions by topic, so train the way you\'ll be tested.' },

  // ─── Elaboration (elaborative-interrogation-protocol) ───
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'action', prompt: 'Ask yourself "why does this work?" or "how does this connect to what I already know?"' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'action', prompt: 'Pick one concept and explain it as if teaching a friend who knows nothing about it.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'action', prompt: 'Write one real-world example or analogy for the concept you just studied.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'check-in', prompt: 'Can you explain WHY this works, not just WHAT it is? If not, dig deeper — surface knowledge won\'t hold up in exams.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'check-in', prompt: 'Could you link this to something from another subject? Cross-connections make knowledge stick.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'check-in', prompt: 'Are you memorising or understanding? Ask yourself "why?" about what you just read — that\'s the shift to deep learning.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'technique-switch', prompt: 'Draw a diagram or mind map of how today\'s concepts connect to each other.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'technique-switch', prompt: 'Write a "because" chain: This happens because... which causes... which means... Go 3 levels deep.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'technique-switch', prompt: 'Try the Feynman technique: explain this in the simplest possible terms. Where you get stuck is where to focus.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'energy-focus', prompt: 'Understanding beats memorising every time. The extra effort of "why" now saves hours of re-learning later.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'energy-focus', prompt: 'Your brain remembers stories and connections far better than isolated facts. Keep building those links.' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', category: 'energy-focus', prompt: 'One well-understood concept is worth ten that are half-memorised. Depth over breadth right now.' },

  // ─── Agency Mindset (agency-protocol) ───
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'action', prompt: 'Set a clear intention: what exactly will you know or be able to do after this session?' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'action', prompt: 'Write down one specific goal for the next 10 minutes. Make it measurable — "Complete 5 questions" not "study more".' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'action', prompt: 'Choose your next action deliberately. Don\'t drift — decide what you\'ll work on and commit to it.' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'check-in', prompt: 'Rate your focus 1-10 right now. If it\'s below 7, take a 60-second reset and refocus.' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'check-in', prompt: 'Are you studying with intention or just going through the motions? Reconnect with your goal for this session.' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'check-in', prompt: 'What was your plan for this session? Check in — are you on track or did you drift? Adjust now if needed.' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'technique-switch', prompt: 'If you\'re stuck, change your approach rather than pushing harder on something that isn\'t working.' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'technique-switch', prompt: 'Take 30 seconds to prioritise: what\'s the most important thing to learn in the time you have left?' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'technique-switch', prompt: 'Shift from passive to active: instead of reading, try writing, testing, or explaining.' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'energy-focus', prompt: 'You chose to study — that\'s the hardest step. Finish strong with 5 more focused minutes.' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'energy-focus', prompt: 'You\'re in control of this session. Every minute you stay focused is a choice that compounds over time.' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', category: 'energy-focus', prompt: 'Future you is counting on present you. The effort you put in now directly shapes your results.' },

  // ─── Growth Mindset (growth-mindset-protocol) ───
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'action', prompt: 'Write down one thing that was difficult today. Reframe it: what did that struggle teach you?' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'action', prompt: 'Find the hardest problem you can and attempt it. Getting it wrong is more valuable than avoiding it.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'action', prompt: 'Replace "I can\'t do this" with "I can\'t do this yet." Then identify the specific gap to work on.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'check-in', prompt: 'If something feels hard, lean in — your brain is literally building new connections right now.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'check-in', prompt: 'Are you avoiding the hard parts? Those are exactly where the growth happens. Lean into difficulty.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'check-in', prompt: 'How do you feel about mistakes right now — frustrated or curious? Curiosity is the growth mindset in action.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'technique-switch', prompt: 'Instead of re-reading something you already know, find something that challenges you. Comfort zone ≠ learning zone.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'technique-switch', prompt: 'Try tackling a problem you failed before. Your brain has been processing it since — you might surprise yourself.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'technique-switch', prompt: 'Pick the topic you\'re least confident in and spend 5 minutes on it. Small doses of discomfort build big confidence.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'energy-focus', prompt: 'Struggle means growth. Difficulty is the signal that learning is happening. Keep pushing.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'energy-focus', prompt: 'Your brain is like a muscle — it gets stronger through effort, not ease. This work is making you smarter.' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', category: 'energy-focus', prompt: 'Every expert was once a beginner who kept going. You\'re on that same path right now.' },

  // ─── Deep Focus (digital-distraction-protocol) ───
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'action', prompt: 'Put your phone face-down or in another room. Eliminate one distraction before continuing.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'action', prompt: 'Close any tabs or apps you don\'t need right now. Clear your workspace for the next 10 minutes.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'action', prompt: 'Set a mini-goal for the next 5 minutes and give it 100% — no checking anything else.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'check-in', prompt: 'If your mind wandered, that\'s normal. Gently bring it back — each refocus strengthens attention.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'check-in', prompt: 'On a scale of 1-10, how focused are you right now? If below 6, stand up, stretch for 30 seconds, then refocus.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'check-in', prompt: 'Have you checked your phone or social media? If so, put it away. Reclaim your attention for this session.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'technique-switch', prompt: 'If you\'re losing focus, change your posture or location slightly. A small shift can reset your attention.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'technique-switch', prompt: 'Try the "2-minute rule": commit to just 2 more minutes of deep focus. You\'ll often find you keep going.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'technique-switch', prompt: 'Switch from screen to paper (or vice versa) for the next 5 minutes. Variety helps sustain attention.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'energy-focus', prompt: 'You\'re in the final stretch. Channel all focus into these last minutes — quality over quantity.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'energy-focus', prompt: 'Deep focus is a skill you\'re training right now. Each distraction you resist makes the next one easier.' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', category: 'energy-focus', prompt: '30 minutes of real focus beats 2 hours of half-attention. Protect this time — it\'s your most valuable study tool.' },

  // ─── Metacognition (learning-radar-protocol) ───
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'action', prompt: 'Before diving in, ask: what\'s my plan for this session? What strategy will I use and why?' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'action', prompt: 'Rate your understanding of the current topic: 1 (lost) to 5 (could teach it). Adjust your approach based on the number.' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'action', prompt: 'Write down what you understand well and what confuses you. This is your roadmap for the rest of the session.' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'check-in', prompt: 'Check in: is your current approach working? If not, what could you do differently right now?' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'check-in', prompt: 'What strategy are you using right now? Is it the best one for this material, or are you just doing what\'s easiest?' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'check-in', prompt: 'Are you actually learning or just feeling busy? Pause and assess — real progress means you can recall and apply.' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'technique-switch', prompt: 'Try explaining your study strategy out loud: "I\'m doing X because Y." If you can\'t justify it, switch approaches.' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'technique-switch', prompt: 'Zoom out for 30 seconds: what\'s the big picture of this topic? Understanding the structure helps you fill in details.' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'technique-switch', prompt: 'If reading isn\'t clicking, try a different input: draw it, say it, or write it in your own words.' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'energy-focus', prompt: 'What worked well in this session? What will you do differently next time? This reflection is how you level up.' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'energy-focus', prompt: 'Being aware of HOW you learn is a superpower. You\'re building it right now by studying with intention.' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', category: 'energy-focus', prompt: 'Top students don\'t just study harder — they study smarter by monitoring what works. That\'s exactly what you\'re doing.' },

  // ─── Exam Strategy (exam-hall-strategies-protocol) ───
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'action', prompt: 'Set a timer for practice questions — simulating exam pressure builds real readiness.' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'action', prompt: 'Try answering one question under timed conditions, then check your answer structure against the marking scheme.' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'action', prompt: 'Pick a past exam question and plan your answer for 2 minutes before writing. Planning = higher marks.' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'check-in', prompt: 'Could you answer a 6-mark question on this topic right now? If not, what\'s missing from your understanding?' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'check-in', prompt: 'Are you studying content or practising answers? Both matter — make sure you\'re doing enough of each.' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'check-in', prompt: 'Think about mark allocation: do you know how to structure answers to maximise marks, not just knowledge?' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'technique-switch', prompt: 'Try writing a model answer, then compare it with the marking scheme. Where do you lose marks?' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'technique-switch', prompt: 'Practice reading questions carefully — highlight command words (describe, compare, evaluate). They tell you exactly what to do.' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'technique-switch', prompt: 'Try the "examiner\'s eye" technique: read your answer as if you\'re marking it. Would you give full marks?' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'energy-focus', prompt: 'Review your practice answer: did you hit all the marks? Note what to improve for next time.' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'energy-focus', prompt: 'Exam readiness is built through practice, not just knowledge. Every timed question you do builds confidence.' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', category: 'energy-focus', prompt: 'The students who do best aren\'t always the smartest — they\'re the ones who\'ve practised answering under pressure.' },
];
