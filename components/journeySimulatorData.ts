/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Types ───────────────────────────────────────────────────────────────────

export type Phase = 'Foundation' | 'Pressure Cooker' | 'Final Stretch';

export type Mood = 'opportunity' | 'crisis' | 'social' | 'study' | 'exam' | 'reflection' | 'triumph';
export type Location = 'school' | 'home' | 'exam-hall' | 'library' | 'social' | 'work' | 'online';

export type GameState = {
  energy: number;
  academicCap: number;
  socialSupport: number;
  systemSavvy: number;
  resilience: number;
};

export type StatKey = keyof GameState;

export type ModuleLink = {
  moduleId: string;
  moduleTitle: string;
  insight: string;
};

export type Choice = {
  text: string;
  effects: Partial<GameState>;
  nextSceneId: string;
  moduleLink?: ModuleLink;
  requires?: { stat: StatKey; min: number }[];
  requiresVisited?: string[];
  flavor?: string;
};

export type Scene = {
  id: string;
  phase: Phase;
  month: string;
  title: string;
  text: string;
  choices?: Choice[];
  mood: Mood;
  location: Location;
};

export type HistoryItem = {
  scene: Scene;
  choiceText: string;
  effects: Partial<GameState>;
  moduleLink?: ModuleLink;
};

export type Archetype = {
  id: string;
  title: string;
  icon: string;
  accentColor: string;
  accentBg: string;
  description: string;
};

export type PhaseMetadata = {
  name: Phase;
  months: string;
  subtitle: string;
};

// ─── Constants ───────────────────────────────────────────────────────────────

export const INITIAL_GAME_STATE: GameState = {
  energy: 60,
  academicCap: 30,
  socialSupport: 50,
  systemSavvy: 20,
  resilience: 40,
};

export const PHASE_METADATA: PhaseMetadata[] = [
  { name: 'Foundation', months: 'Sep – Dec', subtitle: 'Building the base. Every habit you form now echoes through the year.' },
  { name: 'Pressure Cooker', months: 'Jan – Mar', subtitle: 'The pressure builds. Your strategies are tested under fire.' },
  { name: 'Final Stretch', months: 'Apr – Jun', subtitle: 'The home straight. Everything you\'ve built is put to the ultimate test.' },
];

export const STAT_LABELS: Record<StatKey, string> = {
  energy: 'Energy',
  academicCap: 'Academic Mastery',
  socialSupport: 'Social Support',
  systemSavvy: 'System Savvy',
  resilience: 'Resilience',
};

export const STAT_COLORS: Record<StatKey, string> = {
  energy: 'text-amber-500',
  academicCap: 'text-blue-500',
  socialSupport: 'text-emerald-500',
  systemSavvy: 'text-purple-500',
  resilience: 'text-rose-500',
};

export const STAT_BG_COLORS: Record<StatKey, string> = {
  energy: 'bg-amber-500',
  academicCap: 'bg-blue-500',
  socialSupport: 'bg-emerald-500',
  systemSavvy: 'bg-purple-500',
  resilience: 'bg-rose-500',
};

// ─── Archetypes ──────────────────────────────────────────────────────────────

export const ARCHETYPES: Record<string, Archetype> = {
  END_PATHFINDER: {
    id: 'END_PATHFINDER',
    title: 'The Resilient Pathfinder',
    icon: 'compass',
    accentColor: 'text-emerald-600 dark:text-emerald-400',
    accentBg: 'bg-emerald-100 dark:bg-emerald-900/30',
    description: 'You navigated 6th year with remarkable resilience and heart. You built deep connections, supported your peers, and never lost sight of what matters. Your emotional intelligence is your superpower — it will take you further than points ever could.',
  },
  END_EXPERT: {
    id: 'END_EXPERT',
    title: 'The Efficiency Expert',
    icon: 'brain',
    accentColor: 'text-blue-600 dark:text-blue-400',
    accentBg: 'bg-blue-100 dark:bg-blue-900/30',
    description: 'You approached 6th year like a scientist. Your disciplined, evidence-based study methods and impeccable energy management produced outstanding results. You didn\'t just learn the material — you learned how to learn. That skill will compound for the rest of your life.',
  },
  END_MENTOR: {
    id: 'END_MENTOR',
    title: 'The Community Mentor',
    icon: 'hand-helping',
    accentColor: 'text-purple-600 dark:text-purple-400',
    accentBg: 'bg-purple-100 dark:bg-purple-900/30',
    description: 'You mastered the system and shared that knowledge freely. You understood every grant, scheme, and deadline, and became the go-to person for advice. Your network is your net worth, and you\'ve built a powerful foundation for success beyond school.',
  },
  END_GOOD: {
    id: 'END_GOOD',
    title: 'The Strategic Achiever',
    icon: 'target',
    accentColor: 'text-amber-600 dark:text-amber-400',
    accentBg: 'bg-amber-100 dark:bg-amber-900/30',
    description: 'You put in the work and it paid off. Your academic effort carried you to a solid result and you secured your offer. It wasn\'t always pretty, but your determination and focus got you across the line. The next chapter starts now.',
  },
  END_PLC: {
    id: 'END_PLC',
    title: 'The Stepping Stone',
    icon: 'arrow-up-right',
    accentColor: 'text-teal-600 dark:text-teal-400',
    accentBg: 'bg-teal-100 dark:bg-teal-900/30',
    description: 'The points didn\'t line up this time, but your resilience means this is a detour, not a dead end. You\'ve secured a PLC place that acts as a direct pathway to your dream degree. Many of Ireland\'s most successful people took this exact route. Your comeback story starts now.',
  },
  END_REPEAT: {
    id: 'END_REPEAT',
    title: 'The Comeback Story',
    icon: 'rotate-ccw',
    accentColor: 'text-rose-600 dark:text-rose-400',
    accentBg: 'bg-rose-100 dark:bg-rose-900/30',
    description: 'It was a bruising year, and the results didn\'t come. But you\'ve gained something more valuable than points: a year\'s worth of wisdom about how you learn. Armed with that knowledge, you\'re choosing to go again. This isn\'t failure — it\'s a strategic reset with better data.',
  },
  END_SCHOLARSHIP: {
    id: 'END_SCHOLARSHIP',
    title: 'The Full Package',
    icon: 'award',
    accentColor: 'text-yellow-600 dark:text-yellow-400',
    accentBg: 'bg-yellow-100 dark:bg-yellow-900/30',
    description: 'Points, scholarship, HEAR scheme — you played every angle and won. Your system mastery turned the CAO from a lottery into a strategy game. The university isn\'t just accepting you; they\'re investing in you. That\'s the power of knowing the system inside out.',
  },
  END_LEADER: {
    id: 'END_LEADER',
    title: 'The Community Leader',
    icon: 'megaphone',
    accentColor: 'text-indigo-600 dark:text-indigo-400',
    accentBg: 'bg-indigo-100 dark:bg-indigo-900/30',
    description: 'You didn\'t just survive 6th year — you built a community. Your study groups, mentoring, and relentless generosity created a network that lifted everyone around you. You enter college with more than a course offer: you have a reputation as someone who makes others better.',
  },
  END_COMEBACK: {
    id: 'END_COMEBACK',
    title: 'The Comeback Arc',
    icon: 'flame',
    accentColor: 'text-orange-600 dark:text-orange-400',
    accentBg: 'bg-orange-100 dark:bg-orange-900/30',
    description: 'You started weak. You spiralled. You hit bottom. And then you climbed back. Your final results don\'t tell the full story — your resilience does. Where you start doesn\'t determine where you finish, and you\'re living proof.',
  },
  END_BALANCED: {
    id: 'END_BALANCED',
    title: 'The Balanced Graduate',
    icon: 'scale',
    accentColor: 'text-cyan-600 dark:text-cyan-400',
    accentBg: 'bg-cyan-100 dark:bg-cyan-900/30',
    description: 'No stat below 50, no stat above 75 — you are genuinely well-rounded. Energy, academics, social life, system knowledge, resilience. You sacrificed nothing for nothing. Balance is the rarest and most sustainable superpower.',
  },
};

// ─── Module Recommendations by Stat ──────────────────────────────────────────

export const STAT_TO_MODULES: Record<StatKey, { moduleId: string; moduleTitle: string }[]> = {
  energy: [
    { moduleId: 'cognitive-baseline-protocol', moduleTitle: 'The Cognitive Baseline Protocol' },
    { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol" },
    { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow' },
  ],
  academicCap: [
    { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall' },
    { moduleId: 'mastering-spaced-repetition-protocol', moduleTitle: 'Mastering Spaced Repetition' },
    { moduleId: 'mastering-interleaving-protocol', moduleTitle: 'Mastering Interleaving' },
  ],
  socialSupport: [
    { moduleId: 'social-capital-protocol', moduleTitle: 'The Social Capital Protocol' },
    { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence' },
  ],
  systemSavvy: [
    { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol' },
    { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule' },
    { moduleId: 'digital-distraction-protocol', moduleTitle: 'Creating Barriers for Digital Distractions' },
  ],
  resilience: [
    { moduleId: 'growth-mindset-protocol', moduleTitle: 'The Growth Protocol' },
    { moduleId: 'grammar-of-grit-protocol', moduleTitle: 'The Grammar of Grit' },
    { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts' },
  ],
};

// ─── Utilities ───────────────────────────────────────────────────────────────

export function getStatGrade(value: number): { letter: string; color: string; bg: string } {
  if (value >= 80) return { letter: 'A', color: 'text-emerald-600 dark:text-emerald-400', bg: 'bg-emerald-100 dark:bg-emerald-900/30' };
  if (value >= 60) return { letter: 'B', color: 'text-blue-600 dark:text-blue-400', bg: 'bg-blue-100 dark:bg-blue-900/30' };
  if (value >= 40) return { letter: 'C', color: 'text-amber-600 dark:text-amber-400', bg: 'bg-amber-100 dark:bg-amber-900/30' };
  if (value >= 20) return { letter: 'D', color: 'text-orange-600 dark:text-orange-400', bg: 'bg-orange-100 dark:bg-orange-900/30' };
  return { letter: 'F', color: 'text-rose-600 dark:text-rose-400', bg: 'bg-rose-100 dark:bg-rose-900/30' };
}

export function getKeyTurningPoints(history: HistoryItem[]): HistoryItem[] {
  return [...history]
    .sort((a, b) => {
      const totalImpactA = Object.values(a.effects).reduce((sum, v) => sum + Math.abs(v), 0);
      const totalImpactB = Object.values(b.effects).reduce((sum, v) => sum + Math.abs(v), 0);
      return totalImpactB - totalImpactA;
    })
    .slice(0, 3);
}

export function getWeakestStat(state: GameState): StatKey {
  let weakest: StatKey = 'energy';
  let minVal = state.energy;
  for (const key of Object.keys(state) as StatKey[]) {
    if (state[key] < minVal) {
      minVal = state[key];
      weakest = key;
    }
  }
  return weakest;
}

// ─── Weakest Stat Insights ───────────────────────────────────────────────────

export const WEAKEST_STAT_INSIGHTS: Record<StatKey, string> = {
  energy: "Your energy was your biggest vulnerability. By the end of the year you were running on fumes — exhaustion erodes memory, focus, and motivation. In real life, sleep and recovery aren't luxuries; they're the foundation everything else is built on. If you notice yourself burning out, that's the signal to act, not push harder.",
  academicCap: "Your academic preparation was your weakest area. No matter how resilient or well-connected you are, the Leaving Cert ultimately tests what you know and how you apply it. Effective study techniques — active recall, spaced repetition, interleaving — aren't optional extras. They're the difference between hoping for results and engineering them.",
  socialSupport: "You were most isolated in your social support. Going through the Leaving Cert alone is one of the biggest mistakes students make. Isolation amplifies stress, removes accountability, and cuts you off from people who could have helped. A study group, a mentor, even one honest conversation can change the trajectory of your year.",
  systemSavvy: "Your system awareness was your blind spot. You may have studied hard, but understanding how the CAO system, grants, and deadlines work is just as important as knowing your subjects. Students who play the system smart — understanding how points are allocated, which subjects to prioritise, what supports exist — give themselves an unfair advantage.",
  resilience: "Your resilience took the biggest hit. When setbacks came — and they always do — you struggled to bounce back. The Leaving Cert is a marathon, not a sprint. The students who succeed aren't the ones who never fail; they're the ones who learn to recover quickly, reframe setbacks, and keep moving forward despite the pressure.",
};

// ─── Route Resolvers (invisible logic gates) ─────────────────────────────────

export const ROUTE_RESOLVERS: Record<string, (state: GameState, history?: HistoryItem[]) => string> = {
  '__BURNOUT_CHECK__': (state) => state.energy < 30 ? 'BURNOUT_RECOVERY' : 'CAO_DEADLINE',
  '__ACADEMIC_CHECK__': (state) => state.academicCap > 70 ? 'INTERLEAVING_CHOICE' : 'MENTOR_MOMENT',
  '__EARLY_MOMENTUM_CHECK__': (state) => (state.systemSavvy > 45 && state.academicCap > 55) ? 'EARLY_MOMENTUM' : 'MOCKS_LOOM',
  '__PEER_NETWORK_CHECK__': (state) => state.socialSupport > 70 ? 'PEER_NETWORK_EFFECT' : 'FINAL_STRETCH_START',
  '__SYSTEM_MASTERY_CHECK__': (state) => state.systemSavvy > 75 ? 'SYSTEM_MASTERY' : 'GAME_DAY_PREP',
  '__COMEBACK_CHECK__': (state, history) => {
    const visitedSpiral = history?.some(h => h.scene.id === 'PASSIVE_SPIRAL');
    if (visitedSpiral && state.resilience > 65) return 'COMEBACK_RALLY';
    return 'GAME_DAY_PREP';
  },
  '__END_ROUTE__': (state, history) => {
    // Check balanced ending first (all stats 50-75)
    const allStats = [state.energy, state.academicCap, state.socialSupport, state.systemSavvy, state.resilience];
    const isBalanced = allStats.every(s => s >= 50 && s <= 75);
    if (isBalanced) return 'END_BALANCED';
    // Scholarship ending
    if (state.systemSavvy > 75 && state.academicCap > 70) return 'END_SCHOLARSHIP';
    // Leader ending
    if (state.socialSupport > 80) return 'END_LEADER';
    // Comeback ending
    const visitedSpiral = history?.some(h => h.scene.id === 'PASSIVE_SPIRAL');
    if (visitedSpiral && state.resilience > 65) return 'END_COMEBACK';
    // Academic expert — high academics alone is enough
    if (state.academicCap > 80) return 'END_EXPERT';
    // Pathfinder — resilient and socially supported
    if (state.resilience > 70 && state.socialSupport > 60) return 'END_PATHFINDER';
    // Mentor — social + system savvy
    if (state.socialSupport > 70 && state.systemSavvy > 60) return 'END_MENTOR';
    // Good outcome — solid academics carry it
    if (state.academicCap > 65) return 'END_GOOD';
    // PLC — resilience or decent academics provide a pathway
    if (state.resilience > 50 || state.academicCap > 45) return 'END_PLC';
    return 'END_REPEAT';
  },
};

// ─── Scene Definitions ───────────────────────────────────────────────────────

export const STORY_DATA: Record<string, Scene> = {

  // ═══ PHASE 1: FOUNDATION (Sep–Dec) — 12 scenes ═══════════════════════════

  'START': {
    id: 'START',
    phase: 'Foundation',
    month: 'September',
    title: "The First Week Back",
    mood: 'opportunity',
    location: 'school',
    text: "First week of 6th year. A friend who made it to college last year pulls you aside: 'Apply for HEAR — it's a game-changer.'",
    choices: [
      {
        text: "Look into it. Sounds like a priority.",
        effects: { systemSavvy: 15, energy: -5 },
        nextSceneId: 'MATHS_CLASS',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Understanding access routes like HEAR and DARE can be worth more than 50 extra points.' },
      },
      {
        text: "Maybe later. I need to focus on just studying for now.",
        effects: { systemSavvy: -10, academicCap: 5 },
        nextSceneId: 'MATHS_CLASS',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'Strategic planning early on prevents last-minute scrambles later.' },
      },
      {
        text: "Research HEAR/DARE and tell your friends about it too.",
        effects: { systemSavvy: 20, socialSupport: 10, energy: -10 },
        nextSceneId: 'HEAR_ADVOCATE',
        requires: [{ stat: 'systemSavvy', min: 15 }],
        flavor: "Your system awareness opens a collaborative path.",
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Sharing access route knowledge multiplies its impact across your entire friend group.' },
      },
    ],
  },

  'MATHS_CLASS': {
    id: 'MATHS_CLASS',
    phase: 'Foundation',
    month: 'October',
    title: "The Pace of Higher Maths",
    mood: 'study',
    location: 'school',
    text: "Higher Level Maths is moving at lightning speed through Complex Numbers. You're falling behind, but asking a question feels terrifying.",
    choices: [
      {
        text: "Stay quiet and try to figure it out yourself later.",
        effects: { academicCap: -10, resilience: -5 },
        nextSceneId: 'FIRST_BAD_GRADE',
        moduleLink: { moduleId: 'social-capital-protocol', moduleTitle: 'The Social Capital Protocol', insight: 'Asking for help is a sign of strategic intelligence, not weakness.' },
      },
      {
        text: "Ask the teacher to explain it again after class.",
        effects: { academicCap: 10, socialSupport: 5, energy: -5 },
        nextSceneId: 'FIRST_BAD_GRADE',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Managing the discomfort of vulnerability is a core emotional skill.' },
      },
      {
        text: "Start a study group chat to work through it together.",
        effects: { socialSupport: 15, academicCap: 5, energy: -5 },
        nextSceneId: 'FIRST_BAD_GRADE',
        requires: [{ stat: 'socialSupport', min: 50 }],
        flavor: "Your social connections open collaborative options.",
        moduleLink: { moduleId: 'social-capital-protocol', moduleTitle: 'The Social Capital Protocol', insight: 'Peer learning accelerates understanding and builds bonds that sustain you under pressure.' },
      },
    ],
  },

  'FIRST_BAD_GRADE': {
    id: 'FIRST_BAD_GRADE',
    phase: 'Foundation',
    month: 'October',
    title: "The First Bad Grade",
    mood: 'crisis',
    location: 'school',
    text: "Your first big English test comes back: H4. Your heart sinks. What's the story you tell yourself?",
    choices: [
      {
        text: "'This proves I'm not a H1 student.' Spend the evening feeling demotivated.",
        effects: { resilience: -15, energy: -10 },
        nextSceneId: 'STUDY_METHOD_CHOICE',
        moduleLink: { moduleId: 'growth-mindset-protocol', moduleTitle: 'The Growth Protocol', insight: 'A fixed mindset interprets a bad grade as permanent identity. A growth mindset sees data.' },
      },
      {
        text: "'This is data. I haven't mastered this *yet*. I'll review the feedback tomorrow.'",
        effects: { resilience: 10, academicCap: 5 },
        nextSceneId: 'STUDY_METHOD_CHOICE',
        moduleLink: { moduleId: 'power-of-yet-protocol', moduleTitle: 'The Power of "Yet"', insight: 'Adding "yet" to any failure statement transforms it from a verdict into a timeline.' },
      },
    ],
  },

  'STUDY_METHOD_CHOICE': {
    id: 'STUDY_METHOD_CHOICE',
    phase: 'Foundation',
    month: 'November',
    title: "Sunday Night Study",
    mood: 'study',
    location: 'home',
    text: "Sunday night. Big Biology test on Friday. You have a 2-hour study block. What's the plan?",
    choices: [
      {
        text: "Passive Power-through: Re-read and highlight the key chapters. It feels productive.",
        effects: { energy: -5, academicCap: 5 },
        nextSceneId: 'FORGETTING_CURVE',
        moduleLink: { moduleId: 'illusion-of-competence-protocol', moduleTitle: 'Overcoming Illusions of Competence', insight: 'Highlighting feels productive but creates a dangerous "fluency illusion" — recognition without recall.' },
      },
      {
        text: "Active Recall Assault: Close the book and 'blurt' everything you know onto a page. It feels hard.",
        effects: { energy: -15, academicCap: 15, resilience: 5 },
        nextSceneId: 'TECHNIQUE_UPGRADE',
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'The harder it feels to retrieve information, the stronger the memory becomes. Difficulty is the signal of learning.' },
      },
      {
        text: "Teach a younger student what you've learned — explaining forces understanding.",
        effects: { socialSupport: 10, academicCap: 10, energy: -10 },
        nextSceneId: 'STUDY_GROUP_LEADER',
        requires: [{ stat: 'socialSupport', min: 60 }],
        flavor: "Your social network lets you teach, not just learn.",
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Teaching activates the Protégé Effect — explaining something forces deeper processing than any solo method.' },
      },
    ],
  },

  // ── Passive Path ───────────────────────────────────────────────────────────

  'FORGETTING_CURVE': {
    id: 'FORGETTING_CURVE',
    phase: 'Foundation',
    month: 'November',
    title: "The 'I Forgot Everything' Moment",
    mood: 'crisis',
    location: 'school',
    text: "You spent all weekend highlighting. Pop quiz today — your mind is blank. The 'Illusion of Competence' has struck.",
    choices: [
      {
        text: "Mindset Shift: 'I haven't mastered this YET.' Switch to Active Recall tonight.",
        effects: { resilience: 15, academicCap: 10, energy: -10 },
        nextSceneId: 'PASSIVE_RECOVERY',
        moduleLink: { moduleId: 'mastering-spaced-repetition-protocol', moduleTitle: 'Mastering Spaced Repetition', insight: 'The forgetting curve is real — but spacing your reviews at the right intervals defeats it completely.' },
      },
      {
        text: "Fixed Frustration: 'I'm just not a Science person.' Go back to re-reading.",
        effects: { resilience: -10, academicCap: -5, energy: -5 },
        nextSceneId: 'PASSIVE_SPIRAL',
        moduleLink: { moduleId: 'grammar-of-grit-protocol', moduleTitle: 'The Grammar of Grit', insight: 'Saying "I\'m not a Science person" treats ability as identity. Grit research shows ability is built, not born.' },
      },
    ],
  },

  'PASSIVE_RECOVERY': {
    id: 'PASSIVE_RECOVERY',
    phase: 'Foundation',
    month: 'November',
    title: "The Recovery",
    mood: 'triumph',
    location: 'school',
    text: "You switch to Active Recall. It's brutal at first — you keep getting things wrong. After a week, something clicks. You ace a surprise quiz.",
    choices: [
      {
        text: "Tell your study group about Active Recall. Maybe they'll want to try it too.",
        effects: { socialSupport: 10, academicCap: 5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'social-capital-protocol', moduleTitle: 'The Social Capital Protocol', insight: 'Sharing knowledge builds social capital — and teaching others deepens your own understanding.' },
      },
      {
        text: "Keep it to yourself. It's your competitive edge.",
        effects: { academicCap: 5, socialSupport: -5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'effective-struggle-protocol', moduleTitle: 'Effective Struggle and Growth', insight: 'Struggle alone builds knowledge, but shared struggle builds resilience and perspective.' },
      },
    ],
  },

  'PASSIVE_SPIRAL': {
    id: 'PASSIVE_SPIRAL',
    phase: 'Foundation',
    month: 'November',
    title: "The Downward Spiral",
    mood: 'crisis',
    location: 'home',
    text: "Results keep disappointing. Everyone else seems to 'get it' and you don't. The gap is widening. A friend notices you seem down.",
    choices: [
      {
        text: "Open up to your friend about how you're feeling.",
        effects: { socialSupport: 15, resilience: 10, energy: 5 },
        nextSceneId: 'SOCIAL_ISOLATION',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Emotional disclosure reduces cortisol and activates the brain\'s social reward circuits.' },
      },
      {
        text: "'I'm fine.' Push through alone. Don't show weakness.",
        effects: { socialSupport: -10, resilience: -5, energy: -10 },
        nextSceneId: 'SOCIAL_ISOLATION',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'Catastrophic thinking feeds on isolation. Connection is the antidote to spiralling.' },
      },
    ],
  },

  'SOCIAL_ISOLATION': {
    id: 'SOCIAL_ISOLATION',
    phase: 'Foundation',
    month: 'December',
    title: "The Isolation Trap",
    mood: 'crisis',
    location: 'home',
    text: "You've been cancelling plans, eating lunch alone to cram, scrolling instead of sleeping. You're becoming isolated.",
    choices: [
      {
        text: "Set a boundary: No studying after 8pm. Use evenings for friends and rest.",
        effects: { energy: 15, socialSupport: 10, academicCap: -5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'cognitive-baseline-protocol', moduleTitle: 'The Cognitive Baseline Protocol', insight: 'Your brain consolidates learning during rest and sleep, not during extra cramming.' },
      },
      {
        text: "Double down. The exams won't wait. Sacrifice everything for study.",
        effects: { academicCap: 10, energy: -15, socialSupport: -10 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Sleep and social connection aren\'t luxuries — they\'re biological inputs your brain needs to function.' },
      },
    ],
  },

  // ── Active Path ────────────────────────────────────────────────────────────

  'TECHNIQUE_UPGRADE': {
    id: 'TECHNIQUE_UPGRADE',
    phase: 'Foundation',
    month: 'November',
    title: "Technique Upgrade",
    mood: 'triumph',
    location: 'school',
    text: "The pop quiz was challenging, but you retrieved most of the key facts. Active Recall worked. A surge of confidence hits.",
    choices: [
      {
        text: "Double down: 'This works. I'll build Spaced Repetition into my routine.'",
        effects: { academicCap: 15, resilience: 5 },
        nextSceneId: 'STUDY_GROUP',
        moduleLink: { moduleId: 'mastering-spaced-repetition-protocol', moduleTitle: 'Mastering Spaced Repetition', insight: 'Combining Active Recall with Spaced Repetition is the most powerful study combo in cognitive science.' },
      },
      {
        text: "Get complacent: 'Great, I can ease off a bit now.'",
        effects: { academicCap: -5, energy: 5 },
        nextSceneId: 'OVERCONFIDENCE_TRAP',
        moduleLink: { moduleId: 'illusion-of-competence-protocol', moduleTitle: 'Overcoming Illusions of Competence', insight: 'One good result can create overconfidence. Real mastery requires sustained, deliberate practice.' },
      },
    ],
  },

  'STUDY_GROUP': {
    id: 'STUDY_GROUP',
    phase: 'Foundation',
    month: 'November',
    title: "The Study Group",
    mood: 'social',
    location: 'school',
    text: "Classmates want to form a weekly Maths and Science study group. Less solo time, but collaborative learning could be powerful.",
    choices: [
      {
        text: "Join the group. Teaching others will solidify my own understanding.",
        effects: { socialSupport: 15, academicCap: 10, energy: -5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Explaining "why" something works forces your brain to build deeper connections between ideas.' },
      },
      {
        text: "Decline. I work better alone and don't want to slow down.",
        effects: { academicCap: 5, socialSupport: -10 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'social-capital-protocol', moduleTitle: 'The Social Capital Protocol', insight: 'Solo study builds knowledge, but peer learning builds the network that sustains you under pressure.' },
      },
    ],
  },

  'OVERCONFIDENCE_TRAP': {
    id: 'OVERCONFIDENCE_TRAP',
    phase: 'Foundation',
    month: 'November',
    title: "The Overconfidence Trap",
    mood: 'crisis',
    location: 'school',
    text: "Two weeks of coasting after one good result. Major class test today — you haven't reviewed since. Overconfidence set a trap.",
    choices: [
      {
        text: "Use this as a wake-up call. Build a consistent revision schedule starting tonight.",
        effects: { resilience: 10, systemSavvy: 10, energy: -10 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'Consistent small sessions beat sporadic cramming every time. Schedule the work backwards from the test date.' },
      },
      {
        text: "Blame the teacher for going too fast. It's not fair.",
        effects: { resilience: -10, academicCap: -5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'agency-architecture-protocol', moduleTitle: 'Controlling the Controllables', insight: 'External attribution feels protective, but it steals your power to change the outcome.' },
      },
    ],
  },

  // ── Convergence Point ──────────────────────────────────────────────────────

  'PART_TIME_JOB': {
    id: 'PART_TIME_JOB',
    phase: 'Foundation',
    month: 'December',
    title: "Work-Life Balance",
    mood: 'opportunity',
    location: 'work',
    text: "Your boss asks you to cover Thursday night. Good money — but it's your biggest study evening of the week.",
    choices: [
      {
        text: "Take the shift. The money is too important right now.",
        effects: { energy: -20, academicCap: -10 },
        nextSceneId: 'JOB_CONSEQUENCES',
        moduleLink: { moduleId: 'connecting-education-to-goals-protocol', moduleTitle: 'Connecting Education to Goals', insight: 'Short-term financial gains can undermine long-term outcomes. Connect today\'s choices to your future self.' },
      },
      {
        text: "Politely decline. 'The Leaving' has to come first.",
        effects: { resilience: 5, academicCap: 5, energy: -5 },
        nextSceneId: 'MOCKS_LOOM',
        moduleLink: { moduleId: 'best-possible-self-protocol', moduleTitle: 'Finding Your Best Possible Self', insight: 'Saying no to short-term temptation is easier when you have a vivid picture of your future self.' },
      },
      {
        text: "Negotiate reduced hours with a study-first pitch to your boss.",
        effects: { systemSavvy: 10, resilience: 10, energy: -5 },
        nextSceneId: 'FINANCIAL_STRATEGY',
        requires: [{ stat: 'systemSavvy', min: 40 }],
        flavor: "Your system savvy lets you negotiate, not just choose.",
        moduleLink: { moduleId: 'strategic-advantage-protocol', moduleTitle: 'Your Strategic Advantage', insight: 'Strategic negotiation turns binary choices into win-win outcomes. System-aware students create options.' },
      },
    ],
  },

  'JOB_CONSEQUENCES': {
    id: 'JOB_CONSEQUENCES',
    phase: 'Foundation',
    month: 'December',
    title: "The Ripple Effect",
    mood: 'reflection',
    location: 'home',
    text: "You earned €70 but missed your study window. Fatigue from the late night is spilling into Friday classes. One choice rippled through the whole week.",
    choices: [
      {
        text: "Learn from it. Reduce shifts to weekends only until the exams are over.",
        effects: { resilience: 10, systemSavvy: 5 },
        nextSceneId: 'MOCKS_LOOM',
        moduleLink: { moduleId: 'reframing-progress-protocol', moduleTitle: 'Reframing Progress', insight: 'Progress isn\'t linear. What matters is recognising the pattern and adjusting your system.' },
      },
      {
        text: "Keep the extra shifts. The money stress is worse than the study stress.",
        effects: { energy: -10, academicCap: -10, resilience: -5 },
        nextSceneId: 'MOCKS_LOOM',
        moduleLink: { moduleId: 'strategic-advantage-protocol', moduleTitle: 'Your Strategic Advantage', insight: 'Financial pressure is real — but understanding it as a systemic challenge, not a personal failure, opens up strategic options.' },
      },
    ],
  },

  // ═══ PHASE 2: PRESSURE COOKER (Jan–Mar) — 10 scenes ═══════════════════════

  'MOCKS_LOOM': {
    id: 'MOCKS_LOOM',
    phase: 'Pressure Cooker',
    month: 'January',
    title: "The Mocks Are Looming",
    mood: 'exam',
    location: 'school',
    text: "Week before the Mocks. The material mountain feels impossible. Panic is setting in.",
    choices: [
      {
        text: "Panic-cram: Pull two all-nighters for your weakest subjects.",
        effects: { academicCap: 10, energy: -40, resilience: -15 },
        nextSceneId: '__BURNOUT_CHECK__',
        moduleLink: { moduleId: 'cognitive-endurance-protocol', moduleTitle: 'Cognitive Endurance', insight: 'All-nighters destroy memory consolidation. You\'re burning calories to produce less learning, not more.' },
      },
      {
        text: "Strategic Triage: Use Interleaving on high-yield topics and protect your sleep schedule.",
        effects: { academicCap: 15, energy: -10, resilience: 10, systemSavvy: 5 },
        nextSceneId: '__BURNOUT_CHECK__',
        moduleLink: { moduleId: 'mastering-interleaving-protocol', moduleTitle: 'Mastering Interleaving', insight: 'Interleaving — mixing topics in one session — feels harder but builds flexible, exam-ready knowledge.' },
      },
      {
        text: "Deploy the 'Surplus Rule' — bank easy marks first, then attack hard topics.",
        effects: { academicCap: 20, systemSavvy: 10, energy: -10 },
        nextSceneId: 'MOCK_MASTERY',
        requires: [{ stat: 'systemSavvy', min: 50 }, { stat: 'academicCap', min: 60 }],
        flavor: "Your system knowledge + academic base unlock an elite strategy.",
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'The Surplus Rule: secure guaranteed marks first, then use remaining time on high-risk questions.' },
      },
    ],
  },

  'BURNOUT_RECOVERY': {
    id: 'BURNOUT_RECOVERY',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "Strategic Reset",
    mood: 'crisis',
    location: 'home',
    text: "You've hit a wall. Exhausted. Mocks were brutal. Your body and brain are screaming for rest.",
    choices: [
      {
        text: "The 'Grit' Protocol: Take 2 days off entirely to recharge, then simplify the goal.",
        effects: { energy: 40, resilience: 20, academicCap: -5 },
        nextSceneId: 'POST_BURNOUT',
        moduleLink: { moduleId: 'grammar-of-grit-protocol', moduleTitle: 'The Grammar of Grit', insight: 'True grit includes knowing when to rest. Strategic withdrawal is not the same as giving up.' },
      },
      {
        text: "Push Through: Force yourself to study 4 hours tonight with caffeine.",
        effects: { energy: -20, academicCap: 5, resilience: -15 },
        nextSceneId: 'ACUTE_EXHAUSTION',
        moduleLink: { moduleId: 'cognitive-baseline-protocol', moduleTitle: 'The Cognitive Baseline Protocol', insight: 'Below a critical sleep threshold, your brain literally cannot form new long-term memories.' },
      },
    ],
  },

  'ACUTE_EXHAUSTION': {
    id: 'ACUTE_EXHAUSTION',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "Acute Exhaustion",
    mood: 'crisis',
    location: 'school',
    text: "Wired on caffeine, zero sleep. You read a question and... nothing. Total blank. The teacher asks if you're okay.",
    choices: [
      {
        text: "Breathe. Use the Physiological Sigh to reset. Ask for help after class.",
        effects: { resilience: 20, energy: 5, socialSupport: 5 },
        nextSceneId: 'POST_BURNOUT',
        moduleLink: { moduleId: 'exam-crisis-management-protocol', moduleTitle: 'Exam Crisis Management', insight: 'The "double inhale + long exhale" physiological sigh is the fastest way to activate your parasympathetic nervous system.' },
      },
      {
        text: "Panic. The catastrophic thoughts take over. Say nothing.",
        effects: { resilience: -20, academicCap: -10, energy: -10 },
        nextSceneId: 'POST_BURNOUT',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'Catastrophic spirals follow a predictable pattern. Learning to spot the trigger thought is the first step to breaking the cycle.' },
      },
    ],
  },

  'POST_BURNOUT': {
    id: 'POST_BURNOUT',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "After the Storm",
    mood: 'reflection',
    location: 'home',
    text: "The burnout was rough, but it taught you something. Your study approach needs a rethink — not just what you study, but how you manage yourself.",
    choices: [
      {
        text: "Overhaul your routine: 8 hours sleep, no phone after 9pm, daily walks.",
        effects: { energy: 20, resilience: 10, academicCap: 5 },
        nextSceneId: 'CAO_DEADLINE',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Sleep, nutrition, movement — these aren\'t optional extras. They\'re the biological foundation of cognition.' },
      },
      {
        text: "Just try to survive until the Mocks are over. No energy for big changes.",
        effects: { energy: 5, resilience: -5 },
        nextSceneId: 'CAO_DEADLINE',
        moduleLink: { moduleId: 'procrastination-protocol', moduleTitle: 'Understanding Procrastination and Motivation', insight: 'When everything feels overwhelming, the smallest possible action — even 5 minutes — can break the inertia.' },
      },
    ],
  },

  'CAO_DEADLINE': {
    id: 'CAO_DEADLINE',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "The CAO Deadline",
    mood: 'opportunity',
    location: 'home',
    text: "CAO deadline this week. Dream course vs. safe option. Your guidance counsellor says put 10 choices down.",
    choices: [
      {
        text: "Be realistic. Put the safer options down first.",
        effects: { systemSavvy: 5, resilience: -5 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'The CAO is a free list — there is zero cost to putting a dream course as #1. Strategic ordering matters.' },
      },
      {
        text: "Shoot for the stars. Put the dream course as #1.",
        effects: { resilience: 10, systemSavvy: 5 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'best-possible-self-protocol', moduleTitle: 'Finding Your Best Possible Self', insight: 'Visualising your best possible future activates the motivational circuits you need for the final push.' },
      },
      {
        text: "Apply to both courses, plus HEAR scheme and a scholarship application.",
        effects: { systemSavvy: 15, resilience: 10, energy: -15 },
        nextSceneId: 'SCHOLARSHIP_PATH',
        requires: [{ stat: 'systemSavvy', min: 60 }],
        flavor: "Your system mastery lets you play every angle at once.",
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'The CAO is a free list — strategic students layer HEAR, DARE, and scholarships on top for maximum options.' },
      },
    ],
  },

  'INTERLEAVING_CHOICE': {
    id: 'INTERLEAVING_CHOICE',
    phase: 'Pressure Cooker',
    month: 'March',
    title: "Advanced Strategy: Interleaving",
    mood: 'study',
    location: 'library',
    text: "You're feeling confident. A teacher mentions 'Interleaving' — mixing topics in one session. It sounds harder, but the research is compelling.",
    choices: [
      {
        text: "Stick with what works: Blocked practice. Master one topic before moving on.",
        effects: { academicCap: 5, energy: -5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'cognitive-architecture-protocol', moduleTitle: 'Cognitive Architecture', insight: 'Blocked practice feels smoother but builds fragile knowledge that crumbles under exam conditions.' },
      },
      {
        text: "Try Interleaving: Mix up different topics in one study session.",
        effects: { academicCap: 15, energy: -10, resilience: 5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'mastering-interleaving-protocol', moduleTitle: 'Mastering Interleaving', insight: 'Interleaving forces your brain to discriminate between problem types — exactly what exams demand.' },
      },
    ],
  },

  'MENTOR_MOMENT': {
    id: 'MENTOR_MOMENT',
    phase: 'Pressure Cooker',
    month: 'March',
    title: "The Mentor Moment",
    mood: 'social',
    location: 'school',
    text: "A teacher pulls you aside: 'I see your effort, but your method needs work. Stay back Tuesdays — I'll show you how to approach exam questions differently.'",
    choices: [
      {
        text: "Accept the help. Swallow the pride.",
        effects: { academicCap: 15, socialSupport: 10, resilience: 5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'self-efficacy-protocol', moduleTitle: 'Self Efficacy', insight: 'Accepting mentorship is one of the four sources of self-efficacy. A coach sees your blind spots.' },
      },
      {
        text: "Politely decline. 'I'll figure it out on my own.'",
        effects: { resilience: 5, academicCap: -5, socialSupport: -5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'autodidact-engine-protocol', moduleTitle: 'Using Feedback Loops', insight: 'Independence is powerful, but without external feedback you can\'t see what you don\'t know.' },
      },
    ],
  },

  // ═══ PHASE 3: FINAL STRETCH (Apr–Jun) — 6 scenes ═════════════════════════

  'FINAL_STRETCH_START': {
    id: 'FINAL_STRETCH_START',
    phase: 'Final Stretch',
    month: 'April',
    title: "The Final Push",
    mood: 'study',
    location: 'school',
    text: "April. The final push. Your teacher hands you a heavy-duty revision plan covering every topic. Overwhelming but thorough.",
    choices: [
      {
        text: "Follow their plan blindly. They know best.",
        effects: { systemSavvy: 5, academicCap: 5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'points-optimization-protocol', moduleTitle: 'Points Optimization', insight: 'Generic plans work for average results. Elite performance requires personalised strategy.' },
      },
      {
        text: "Adapt the plan to my own weak areas using a Retrospective Log.",
        effects: { systemSavvy: 10, resilience: 5, academicCap: 5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'A retrospective timetable works backwards from your exam, allocating more time to weaker areas.' },
      },
    ],
  },

  'EXAM_ANXIETY': {
    id: 'EXAM_ANXIETY',
    phase: 'Final Stretch',
    month: 'April',
    title: "The Anxiety Wave",
    mood: 'crisis',
    location: 'home',
    text: "3 AM. Heart racing. 'What if I blank? What if I fail?' The anxiety is physical — tight chest, racing pulse, scattered thoughts.",
    choices: [
      {
        text: "Get up and use the 'Worry Window' technique: write every fear down, then schedule 15 minutes tomorrow to address each one.",
        effects: { resilience: 15, energy: 5 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'Externalising worries onto paper reduces their cognitive load by up to 60%. Your brain stops looping when the thought is "stored" elsewhere.' },
      },
      {
        text: "Lie there spiralling. Eventually check your phone until 5 AM.",
        effects: { energy: -20, resilience: -10 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'digital-distraction-protocol', moduleTitle: 'Creating Barriers for Digital Distractions', insight: 'Phone screens emit blue light that suppresses melatonin. Late-night scrolling compounds sleep loss and anxiety.' },
      },
      {
        text: "Execute your pre-rehearsed exam routine — you planned for this exact moment.",
        effects: { resilience: 20, energy: 10 },
        nextSceneId: 'CRISIS_AVERTED',
        requires: [{ stat: 'resilience', min: 60 }, { stat: 'energy', min: 40 }],
        flavor: "Your resilience and energy reserves kick in automatically.",
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Pre-rehearsed routines bypass the panic response. Your brain follows the script instead of spiralling.' },
      },
    ],
  },

  'PEER_SUPPORT': {
    id: 'PEER_SUPPORT',
    phase: 'Final Stretch',
    month: 'May',
    title: "The Protégé Effect",
    mood: 'social',
    location: 'school',
    text: "A classmate is panicking about a Maths topic you've mastered. They ask for help — but it would eat into your revision time.",
    choices: [
      {
        text: "Help them out. Explaining it will probably strengthen my own understanding anyway.",
        effects: { socialSupport: 15, academicCap: 5, energy: -10, resilience: 5 },
        nextSceneId: 'DIGITAL_DISTRACTION',
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'The "Protégé Effect" is real: teaching activates deeper processing than simply reviewing your notes.' },
      },
      {
        text: "Sorry, I need to focus on my own weak areas. It's too close to the exams.",
        effects: { socialSupport: -10, academicCap: 10, energy: -5 },
        nextSceneId: 'DIGITAL_DISTRACTION',
        moduleLink: { moduleId: 'cognitive-endurance-protocol', moduleTitle: 'Cognitive Endurance', insight: 'In the final stretch, protecting your cognitive resources becomes as important as using them.' },
      },
      {
        text: "Organize a full study group workshop — everyone teaches their strongest topic.",
        effects: { socialSupport: 20, academicCap: 10, energy: -15 },
        nextSceneId: 'PEER_NETWORK_EFFECT',
        requires: [{ stat: 'socialSupport', min: 70 }],
        flavor: "Your deep social connections unlock collective intelligence.",
        moduleLink: { moduleId: 'social-capital-protocol', moduleTitle: 'The Social Capital Protocol', insight: 'Study groups where everyone teaches their strength create exponential knowledge transfer.' },
      },
    ],
  },

  'DIGITAL_DISTRACTION': {
    id: 'DIGITAL_DISTRACTION',
    phase: 'Final Stretch',
    month: 'May',
    title: "The Attention Heist",
    mood: 'crisis',
    location: 'home',
    text: "You check one notification... 45 minutes evaporate on TikTok. This has happened three times this week.",
    choices: [
      {
        text: "Nuclear option: Give your phone to a family member from 6-9pm every study night.",
        effects: { academicCap: 15, energy: 5, resilience: 5 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'digital-distraction-protocol', moduleTitle: 'Creating Barriers for Digital Distractions', insight: 'Willpower is a depletable resource. Physical barriers (removing the phone) beat mental resolve every time.' },
      },
      {
        text: "Promise yourself you'll have more willpower next time. Keep the phone on the desk.",
        effects: { academicCap: -5, energy: -10, resilience: -5 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'bimodal-brain-protocol', moduleTitle: 'Focused vs Diffuse Mode', insight: 'Your brain can\'t sustain focused mode with a distraction source in arm\'s reach. Environment design trumps willpower.' },
      },
      {
        text: "Already handled — you set up app blockers and a phone lockbox weeks ago.",
        effects: { academicCap: 15, energy: 10, systemSavvy: 5 },
        nextSceneId: 'GAME_DAY_PREP',
        requires: [{ stat: 'systemSavvy', min: 50 }],
        flavor: "Your foresight already solved this problem.",
        moduleLink: { moduleId: 'digital-distraction-protocol', moduleTitle: 'Creating Barriers for Digital Distractions', insight: 'System-savvy students design their environment in advance. The battle was won weeks ago.' },
      },
    ],
  },

  'GAME_DAY_PREP': {
    id: 'GAME_DAY_PREP',
    phase: 'Final Stretch',
    month: 'June',
    title: "Game Day Prep",
    mood: 'exam',
    location: 'home',
    text: "Night before your first exam. Bag packed, pens ready. What's the final move?",
    choices: [
      {
        text: "Last-minute cramming session until 2 AM.",
        effects: { energy: -30, academicCap: 5 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Elite athletes never train the night before a competition. Your exam is your competition.' },
      },
      {
        text: "Do a 10-minute review of key formulas, then get a full night's sleep.",
        effects: { energy: 20, resilience: 10 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'exam-hall-strategies-protocol', moduleTitle: 'Exam Hall Strategies', insight: 'Sleep consolidates memories and restores prefrontal cortex function — the brain region you need most in an exam.' },
      },
      {
        text: "Execute a precision exam protocol — meal prep, gear check, timed sleep, morning routine.",
        effects: { energy: 25, resilience: 15, academicCap: 5 },
        nextSceneId: 'ELITE_PROTOCOL',
        requires: [{ stat: 'academicCap', min: 70 }, { stat: 'resilience', min: 60 }],
        flavor: "Your elite preparation unlocks a military-grade game day routine.",
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Elite performers don\'t leave exam day to chance. Every variable is controlled in advance.' },
      },
    ],
  },

  // ═══ NEW BRANCHING SCENES ══════════════════════════════════════════════════

  // ── Foundation conditional branches ─────────────────────────────────────────

  'HEAR_ADVOCATE': {
    id: 'HEAR_ADVOCATE',
    phase: 'Foundation',
    month: 'September',
    title: "The HEAR Advocate",
    mood: 'social',
    location: 'school',
    text: "You told your friends about HEAR and one discovers they qualify. They're emotional — no one in their family knew this existed. You've changed someone's trajectory with information alone.",
    choices: [
      {
        text: "Help them with the application. This matters more than tonight's study.",
        effects: { socialSupport: 20, systemSavvy: 10, energy: -10 },
        nextSceneId: 'MATHS_CLASS',
        moduleLink: { moduleId: 'social-capital-protocol', moduleTitle: 'The Social Capital Protocol', insight: 'Social capital compounds. Helping one person creates a ripple effect through their entire network.' },
      },
      {
        text: "Point them to the guidance counsellor and get back to your own plan.",
        effects: { systemSavvy: 5, academicCap: 5 },
        nextSceneId: 'MATHS_CLASS',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'Delegation is a skill. Knowing when to direct someone to a better resource is its own intelligence.' },
      },
    ],
  },

  'STUDY_GROUP_LEADER': {
    id: 'STUDY_GROUP_LEADER',
    phase: 'Foundation',
    month: 'November',
    title: "The Study Group Leader",
    mood: 'social',
    location: 'library',
    text: "You've become the unofficial study group organizer. Three younger students now come to you for help. Teaching them is exhausting — but your own understanding has deepened dramatically.",
    choices: [
      {
        text: "Formalize it — set a weekly schedule and create shared resources.",
        effects: { socialSupport: 15, academicCap: 10, energy: -10, systemSavvy: 5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Creating teaching resources forces you to identify and fill your own knowledge gaps.' },
      },
      {
        text: "Scale back — you've given enough. Focus on your own exams now.",
        effects: { academicCap: 5, energy: 10, socialSupport: -5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'cognitive-endurance-protocol', moduleTitle: 'Cognitive Endurance', insight: 'Sustainable giving requires boundaries. Burnout from helping helps no one.' },
      },
    ],
  },

  'FINANCIAL_STRATEGY': {
    id: 'FINANCIAL_STRATEGY',
    phase: 'Foundation',
    month: 'December',
    title: "The Financial Strategy",
    mood: 'opportunity',
    location: 'work',
    text: "Your boss agreed to reduced hours. Better yet, your research uncovered a student grant you didn't know about. You've turned a binary choice into a strategic win.",
    choices: [
      {
        text: "Apply for the grant and use the freed-up time for focused revision.",
        effects: { systemSavvy: 15, academicCap: 10, energy: 5 },
        nextSceneId: 'MOCKS_LOOM',
        moduleLink: { moduleId: 'strategic-advantage-protocol', moduleTitle: 'Your Strategic Advantage', insight: 'Financial strategy is academic strategy. Removing money stress frees cognitive resources for learning.' },
      },
      {
        text: "Use the extra time for rest. Your energy reserves need rebuilding.",
        effects: { energy: 20, resilience: 10 },
        nextSceneId: 'MOCKS_LOOM',
        moduleLink: { moduleId: 'cognitive-baseline-protocol', moduleTitle: 'The Cognitive Baseline Protocol', insight: 'Rest is not laziness — it\'s a strategic investment in your cognitive baseline.' },
      },
    ],
  },

  'EARLY_MOMENTUM': {
    id: 'EARLY_MOMENTUM',
    phase: 'Foundation',
    month: 'December',
    title: "Early Momentum",
    mood: 'triumph',
    location: 'school',
    text: "A teacher notices your systematic approach and asks you to mentor a 5th year student. Your methods are clearly working — and now others can see it too.",
    choices: [
      {
        text: "Accept the mentoring role. Teaching will cement your own knowledge.",
        effects: { socialSupport: 15, academicCap: 10, resilience: 5, energy: -10 },
        nextSceneId: 'MOCKS_LOOM',
        moduleLink: { moduleId: 'self-efficacy-protocol', moduleTitle: 'Self Efficacy', insight: 'Being recognized as competent by authority figures is one of the four sources of self-efficacy.' },
      },
      {
        text: "Decline politely — channel that momentum into your own revision.",
        effects: { academicCap: 10, systemSavvy: 5 },
        nextSceneId: 'MOCKS_LOOM',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'Knowing when to say no protects your most valuable resource: focused study time.' },
      },
    ],
  },

  // ── Pressure Cooker conditional branches ────────────────────────────────────

  'MOCK_MASTERY': {
    id: 'MOCK_MASTERY',
    phase: 'Pressure Cooker',
    month: 'January',
    title: "Mock Mastery",
    mood: 'triumph',
    location: 'exam-hall',
    text: "Your surplus strategy paid off massively. You banked easy marks across every paper, then attacked the hard questions with confidence. Your mock results shock everyone — including you.",
    choices: [
      {
        text: "Stay humble. Refine the strategy for the real thing.",
        effects: { academicCap: 15, resilience: 10, systemSavvy: 10 },
        nextSceneId: 'CAO_DEADLINE',
        moduleLink: { moduleId: 'illusion-of-competence-protocol', moduleTitle: 'Overcoming Illusions of Competence', insight: 'Mock success is a data point, not a destination. The real exam is a different beast.' },
      },
      {
        text: "Share your strategy with friends who struggled.",
        effects: { socialSupport: 15, systemSavvy: 5, academicCap: 5 },
        nextSceneId: 'CAO_DEADLINE',
        moduleLink: { moduleId: 'social-capital-protocol', moduleTitle: 'The Social Capital Protocol', insight: 'Sharing strategies that work builds deep trust and social capital that supports you under pressure.' },
      },
    ],
  },

  'SCHOLARSHIP_PATH': {
    id: 'SCHOLARSHIP_PATH',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "The Scholarship Path",
    mood: 'opportunity',
    location: 'online',
    text: "Your scholarship application is in. The university wrote back — you're shortlisted. It's not just about points anymore. Your system awareness has opened doors that most students don't even know exist.",
    choices: [
      {
        text: "Prepare for the scholarship interview alongside your study routine.",
        effects: { systemSavvy: 15, resilience: 10, energy: -15 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'best-possible-self-protocol', moduleTitle: 'Finding Your Best Possible Self', insight: 'Scholarship interviews test your narrative, not just your grades. Know your story.' },
      },
      {
        text: "Focus on the exams. The scholarship is a bonus, not the plan.",
        effects: { academicCap: 10, energy: 5 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Layering strategies means you always have a fallback. Points are the foundation; scholarships are the bonus.' },
      },
    ],
  },

  'CRISIS_AVERTED': {
    id: 'CRISIS_AVERTED',
    phase: 'Final Stretch',
    month: 'April',
    title: "Crisis Averted",
    mood: 'triumph',
    location: 'home',
    text: "Your pre-built routine kicked in automatically. Deep breath, journal the fears, execute the morning protocol. By sunrise, the anxiety has passed. You feel ready — not panicked.",
    choices: [
      {
        text: "Share your anxiety management routine with a struggling friend.",
        effects: { socialSupport: 15, resilience: 5 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'Teaching others your coping strategies reinforces them in your own neural pathways.' },
      },
      {
        text: "Channel the calm into a productive morning study session.",
        effects: { academicCap: 10, energy: 5 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'cognitive-baseline-protocol', moduleTitle: 'The Cognitive Baseline Protocol', insight: 'Post-anxiety calm creates a window of heightened focus. Use it strategically.' },
      },
    ],
  },

  'PEER_NETWORK_EFFECT': {
    id: 'PEER_NETWORK_EFFECT',
    phase: 'Final Stretch',
    month: 'May',
    title: "The Network Effect",
    mood: 'social',
    location: 'library',
    text: "Your study group has become a well-oiled machine. Everyone teaches their strongest topic. The collective knowledge of the group now exceeds what any individual could achieve alone.",
    choices: [
      {
        text: "Create a shared revision resource pack for the whole group.",
        effects: { socialSupport: 10, academicCap: 10, systemSavvy: 5, energy: -10 },
        nextSceneId: 'DIGITAL_DISTRACTION',
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Collaborative resource creation forces synthesis — the highest level of Bloom\'s taxonomy.' },
      },
      {
        text: "Wind down the group to focus on individual weak spots.",
        effects: { academicCap: 10, energy: 5 },
        nextSceneId: 'DIGITAL_DISTRACTION',
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'In the final weeks, individual targeted recall practice beats group study for filling specific gaps.' },
      },
    ],
  },

  // ── Final Stretch conditional branches ──────────────────────────────────────

  'SYSTEM_MASTERY': {
    id: 'SYSTEM_MASTERY',
    phase: 'Final Stretch',
    month: 'May',
    title: "System Mastery",
    mood: 'triumph',
    location: 'online',
    text: "You've gamed every angle: HEAR, scholarship applications, optimal subject selection, grade appeals process. You understand the system better than most teachers. The exam is just one piece of your strategy.",
    choices: [
      {
        text: "Write down your entire system for a younger sibling or friend to use next year.",
        effects: { socialSupport: 15, systemSavvy: 10, energy: -5 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Documenting your system creates a legacy. The knowledge dies with you unless you share it.' },
      },
      {
        text: "Focus on execution. The system is built — now just execute perfectly.",
        effects: { academicCap: 10, resilience: 10 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'In the final stretch, switch from strategy mode to execution mode. Trust the system you\'ve built.' },
      },
    ],
  },

  'TEACHING_LEGACY': {
    id: 'TEACHING_LEGACY',
    phase: 'Final Stretch',
    month: 'May',
    title: "The Teaching Legacy",
    mood: 'social',
    location: 'school',
    text: "Your reputation as a study group leader has spread. A teacher asks you to create a study guide for next year's 6th years. It's a chance to leave something behind that outlasts your own exams.",
    choices: [
      {
        text: "Create the guide. This is your legacy, and the teaching deepens your own mastery.",
        effects: { socialSupport: 15, academicCap: 10, energy: -10 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Creating teaching materials is the ultimate form of active learning. You teach best what you need to learn most.' },
      },
      {
        text: "Politely decline. Every hour counts now.",
        effects: { academicCap: 5, energy: 10 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'cognitive-endurance-protocol', moduleTitle: 'Cognitive Endurance', insight: 'Protecting your final energy reserves is a form of self-respect, not selfishness.' },
      },
    ],
  },

  'ELITE_PROTOCOL': {
    id: 'ELITE_PROTOCOL',
    phase: 'Final Stretch',
    month: 'June',
    title: "The Elite Protocol",
    mood: 'exam',
    location: 'exam-hall',
    text: "Exam morning. Your routine executes like clockwork — balanced breakfast, brief warm-up review, physiological sigh at the school gate. You walk into the hall feeling like an athlete entering the arena.",
    choices: [
      {
        text: "Execute the exam with surgical precision. Trust the process.",
        effects: { academicCap: 15, resilience: 10, energy: 5 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'exam-hall-strategies-protocol', moduleTitle: 'Exam Hall Strategies', insight: 'Exam-day confidence comes from preparation, not hope. You\'ve earned this.' },
      },
      {
        text: "Give a quiet nod of encouragement to a nervous classmate at the door.",
        effects: { socialSupport: 10, resilience: 15, energy: 5 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Small acts of kindness under pressure reveal true character — and reduce your own stress through social bonding.' },
      },
    ],
  },

  'COMEBACK_RALLY': {
    id: 'COMEBACK_RALLY',
    phase: 'Final Stretch',
    month: 'June',
    title: "The Comeback Rally",
    mood: 'triumph',
    location: 'home',
    text: "Your academic scores are low, but your resilience is iron. You've stopped comparing yourself to others and started competing with yesterday's version of yourself. The late-game strategy surge begins.",
    choices: [
      {
        text: "Focus exclusively on high-yield topics. Maximise every remaining hour.",
        effects: { academicCap: 20, resilience: 10, energy: -15 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Triage is a survival skill. In the final weeks, focus on topics with the highest marks-per-hour ratio.' },
      },
      {
        text: "Steady the ship. Consistent effort across all subjects, no heroics.",
        effects: { academicCap: 10, resilience: 15, energy: -5 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'grammar-of-grit-protocol', moduleTitle: 'The Grammar of Grit', insight: 'Grit isn\'t about dramatic gestures. It\'s about showing up consistently when everything says to quit.' },
      },
    ],
  },

  // ═══ ENDINGS (10 total) ═══════════════════════════════════════════════════

  'END_PATHFINDER': {
    id: 'END_PATHFINDER',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Resilient Pathfinder",
    mood: 'triumph',
    location: 'home',
    text: "You got your course — and more. You're known as the person who never gives up and always has time for a friend.",
  },
  'END_EXPERT': {
    id: 'END_EXPERT',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Efficiency Expert",
    mood: 'triumph',
    location: 'home',
    text: "Stellar points. Flawless energy management. You didn't just learn the material — you learned how to learn.",
  },
  'END_MENTOR': {
    id: 'END_MENTOR',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Community Mentor",
    mood: 'triumph',
    location: 'social',
    text: "You mastered the system and shared it freely. Every grant, scheme, and deadline — you knew them all. Your network is your foundation.",
  },
  'END_GOOD': {
    id: 'END_GOOD',
    phase: 'Final Stretch',
    month: 'August',
    title: "Offer Received!",
    mood: 'triumph',
    location: 'home',
    text: "Offer received for one of your top choices. Hard work, strategy, and resilience got you here. The next chapter begins.",
  },
  'END_PLC': {
    id: 'END_PLC',
    phase: 'Final Stretch',
    month: 'August',
    title: "A Different Path",
    mood: 'reflection',
    location: 'home',
    text: "Points didn't line up — but you've secured a PLC place that's a direct pathway to your dream degree. A detour, not a dead end.",
  },
  'END_REPEAT': {
    id: 'END_REPEAT',
    phase: 'Final Stretch',
    month: 'August',
    title: "Another Lap",
    mood: 'reflection',
    location: 'home',
    text: "Results weren't what you hoped. But you're repeating armed with a year's worth of wisdom. This isn't failure — it's a strategic reset.",
  },

  'END_SCHOLARSHIP': {
    id: 'END_SCHOLARSHIP',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Full Package",
    mood: 'triumph',
    location: 'online',
    text: "Points. Scholarship. HEAR scheme. You didn't just get into your dream course — you got in with financial support and recognition. Your system mastery turned the game from a lottery into a strategy. The university doesn't just want you; they're investing in you.",
  },

  'END_LEADER': {
    id: 'END_LEADER',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Community Leader",
    mood: 'triumph',
    location: 'social',
    text: "You didn't just survive 6th year — you built a community around you. Your study group became a support network. Your friends say you changed their year. You enter college not just with a course offer, but with a reputation as someone who lifts others up.",
  },

  'END_COMEBACK': {
    id: 'END_COMEBACK',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Comeback Arc",
    mood: 'triumph',
    location: 'home',
    text: "You started weak. You spiralled. You hit rock bottom. And then you climbed back. Your final results don't tell the full story — your resilience does. You're the living proof that where you start doesn't determine where you finish.",
  },

  'END_BALANCED': {
    id: 'END_BALANCED',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Balanced Graduate",
    mood: 'triumph',
    location: 'home',
    text: "No stat below 50, no stat above 75. You are the rarest type of student — genuinely well-rounded. You managed energy, academics, social life, system knowledge, and mental toughness without sacrificing any one for another. Balance is its own superpower.",
  },
};
