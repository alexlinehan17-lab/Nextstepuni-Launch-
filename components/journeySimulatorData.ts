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

export type TextVariant = {
  condition: { stat: StatKey; min?: number; max?: number } | { visited: string };
  text: string;
};

export type Scene = {
  id: string;
  phase: Phase;
  month: string;
  title: string;
  text: string;
  textVariants?: TextVariant[];
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
  systemSavvy: 'text-[var(--accent-hex)]',
  resilience: 'text-rose-500',
};

export const STAT_BG_COLORS: Record<StatKey, string> = {
  energy: 'bg-amber-500',
  academicCap: 'bg-blue-500',
  socialSupport: 'bg-emerald-500',
  systemSavvy: 'bg-[var(--accent-hex)]',
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
    accentColor: 'text-[var(--accent-hex)] dark:text-[var(--accent-hex)]',
    accentBg: 'bg-[rgba(var(--accent),0.1)] dark:bg-[rgba(var(--accent),0.15)]',
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
  END_REGROUPING: {
    id: 'END_REGROUPING',
    title: 'The Unfinished Chapter',
    icon: 'book-open',
    accentColor: 'text-violet-600 dark:text-violet-400',
    accentBg: 'bg-violet-100 dark:bg-violet-900/30',
    description: 'This year was tough, and the results didn\'t land where you wanted. But you\'re not broken — you\'re regrouping. You know more about yourself, how you learn, and what you want than you did twelve months ago. The points are one number on one day. They don\'t define your potential, your worth, or your future. The story isn\'t over — it\'s just getting started.',
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
    { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow' },
    { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol" },
  ],
  academicCap: [
    { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall' },
    { moduleId: 'mastering-spaced-repetition-protocol', moduleTitle: 'Mastering Spaced Repetition' },
    { moduleId: 'mastering-interleaving-protocol', moduleTitle: 'Mastering Interleaving' },
  ],
  socialSupport: [
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
  '__PEER_NETWORK_CHECK__': (state) => state.socialSupport > 60 ? 'PEER_NETWORK_EFFECT' : 'FINAL_STRETCH_START',
  '__SYSTEM_MASTERY_CHECK__': (state) => state.systemSavvy > 65 ? 'SYSTEM_MASTERY' : 'GAME_DAY_PREP',
  '__COMEBACK_CHECK__': (state, history) => {
    const visitedSpiral = history?.some(h => h.scene.id === 'PASSIVE_SPIRAL');
    if (visitedSpiral && state.resilience > 55) return 'COMEBACK_RALLY';
    return 'GAME_DAY_PREP';
  },
  '__CHRISTMAS_CHECK__': (state) => (state.energy >= 50 && state.resilience >= 50) ? 'CHRISTMAS_REFLECTION' : '__EARLY_MOMENTUM_CHECK__',
  '__MOCK_RESULTS_CHECK__': (state) => state.academicCap >= 50 ? 'MOCK_RESULTS_HIGH' : 'MOCK_RESULTS_LOW',
  '__ECHO_CHAIN__': (_state, history) => {
    const visited = history?.map(h => h.scene.id) ?? [];
    if (visited.includes('STUDY_GROUP') || visited.includes('STUDY_GROUP_LEADER')) return 'ECHO_STUDY_GROUP';
    if (visited.includes('PASSIVE_SPIRAL')) return 'ECHO_SPIRAL';
    if (visited.includes('HEAR_ADVOCATE')) return 'ECHO_ADVOCATE';
    return 'EXAM_ANXIETY';
  },
  '__NIGHT_BEFORE_CHECK__': (state) => (state.resilience >= 55 && state.energy >= 45) ? 'NIGHT_BEFORE' : '__END_ROUTE__',
  '__END_ROUTE__': (state, history) => {
    // Comeback ending — checked first so spiral players get rewarded for rebuilding
    const visitedSpiral = history?.some(h => h.scene.id === 'PASSIVE_SPIRAL');
    if (visitedSpiral && state.resilience > 55) return 'END_COMEBACK';
    // Balanced ending — all stats in a healthy range (widened band)
    const allStats = [state.energy, state.academicCap, state.socialSupport, state.systemSavvy, state.resilience];
    const isBalanced = allStats.every(s => s >= 45 && s <= 80);
    if (isBalanced) return 'END_BALANCED';
    // Scholarship ending — system mastery + strong academics
    if (state.systemSavvy > 65 && state.academicCap > 60) return 'END_SCHOLARSHIP';
    // Leader ending — built a real community
    if (state.socialSupport > 70) return 'END_LEADER';
    // Academic expert — high academics alone is enough
    if (state.academicCap > 70) return 'END_EXPERT';
    // Pathfinder — resilient and socially supported
    if (state.resilience > 60 && state.socialSupport > 50) return 'END_PATHFINDER';
    // Mentor — social + system savvy
    if (state.socialSupport > 60 && state.systemSavvy > 50) return 'END_MENTOR';
    // Good outcome — solid academics carry it
    if (state.academicCap > 55) return 'END_GOOD';
    // PLC — resilience + decent academics provide a structured pathway
    if (state.resilience > 45 && state.academicCap > 35) return 'END_PLC';
    // Regrouping — didn't get the points, no clear PLC plan, but not defeated
    if (state.resilience > 30 || state.socialSupport > 35 || state.energy > 35) return 'END_REGROUPING';
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
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Asking for help is a sign of strategic intelligence, not weakness.' },
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
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Peer learning accelerates understanding and builds bonds that sustain you under pressure.' },
      },
      {
        text: "Head to the library to research study techniques.",
        effects: { academicCap: 5, energy: -5 },
        nextSceneId: 'LIBRARY_DISCOVERY',
        requires: [{ stat: 'academicCap', min: 25 }],
        flavor: "Your academic curiosity drives you to find better methods.",
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'Self-directed learning about how to learn is the most leveraged investment a student can make.' },
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
      {
        text: "Talk to a parent or guardian about it.",
        effects: { resilience: 5, socialSupport: 5 },
        nextSceneId: 'PARENT_CONVERSATION',
        requires: [{ stat: 'socialSupport', min: 45 }],
        flavor: "Your support network gives you someone to turn to.",
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Sharing academic setbacks with trusted adults normalises struggle and builds family-level resilience.' },
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
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Sharing knowledge builds social capital — and teaching others deepens your own understanding.' },
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
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Your brain consolidates learning during rest and sleep, not during extra cramming.' },
      },
      {
        text: "Double down. The exams won't wait. Sacrifice everything for study.",
        effects: { academicCap: 10, energy: -15, socialSupport: -10 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Sleep and social connection aren\'t luxuries — they\'re biological inputs your brain needs to function.' },
      },
      {
        text: "Visit the school counsellor.",
        effects: { resilience: 5 },
        nextSceneId: 'WELLNESS_CHECK',
        requires: [{ stat: 'resilience', max: 35 }],
        flavor: "Your low resilience signals it's time to seek help.",
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Recognising when you need professional support is one of the most important emotional skills you can develop.' },
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
      {
        text: "Show your teacher the technique and ask for feedback.",
        effects: { academicCap: 5, socialSupport: 5 },
        nextSceneId: 'TEACHER_FEEDBACK',
        moduleLink: { moduleId: 'self-efficacy-protocol', moduleTitle: 'Self Efficacy', insight: 'Sharing your methods with a teacher invites expert feedback that accelerates improvement.' },
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
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Solo study builds knowledge, but peer learning builds the network that sustains you under pressure.' },
      },
      {
        text: "Go to the party instead — you've earned it.",
        effects: { socialSupport: 5 },
        nextSceneId: 'PEER_PRESSURE_PARTY',
        moduleLink: { moduleId: 'linking-study-future-goals-protocol', moduleTitle: 'Linking Study to Future Goals', insight: 'Social events aren\'t the enemy — but the timing and trade-offs matter more than you think.' },
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
        moduleLink: { moduleId: 'linking-study-future-goals-protocol', moduleTitle: 'Linking Study to Future Goals', insight: 'Short-term financial gains can undermine long-term outcomes. Connect today\'s choices to your future self.' },
      },
      {
        text: "Politely decline. 'The Leaving' has to come first.",
        effects: { resilience: 5, academicCap: 5, energy: -5 },
        nextSceneId: '__CHRISTMAS_CHECK__',
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
        nextSceneId: '__CHRISTMAS_CHECK__',
        moduleLink: { moduleId: 'reframing-progress-protocol', moduleTitle: 'Reframing Progress', insight: 'Progress isn\'t linear. What matters is recognising the pattern and adjusting your system.' },
      },
      {
        text: "Keep the extra shifts. The money stress is worse than the study stress.",
        effects: { energy: -10, academicCap: -10, resilience: -5 },
        nextSceneId: '__CHRISTMAS_CHECK__',
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
    textVariants: [
      {
        condition: { stat: 'energy', max: 35 },
        text: "Mock exams are next week and your body is screaming for rest. The coffee isn't working anymore. Every time you open a textbook, the words blur. You know you need to study, but you can barely keep your eyes open. Something has to give.",
      },
      {
        condition: { stat: 'academicCap', min: 65 },
        text: "Mock exams are next week, but for the first time this year, the feeling isn't dread — it's anticipation. Your active recall system is loaded, your weak topics are mapped, and you've got a clear plan. This isn't a test. It's a chance to prove your methods work.",
      },
    ],
    choices: [
      {
        text: "Panic-cram: Pull two all-nighters for your weakest subjects.",
        effects: { academicCap: 10, energy: -40, resilience: -15 },
        nextSceneId: '__MOCK_RESULTS_CHECK__',
        moduleLink: { moduleId: 'cognitive-endurance-protocol', moduleTitle: 'Cognitive Endurance', insight: 'All-nighters destroy memory consolidation. You\'re burning calories to produce less learning, not more.' },
      },
      {
        text: "Strategic Triage: Use Interleaving on high-yield topics and protect your sleep schedule.",
        effects: { academicCap: 15, energy: -10, resilience: 10, systemSavvy: 5 },
        nextSceneId: '__MOCK_RESULTS_CHECK__',
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
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Below a critical sleep threshold, your brain literally cannot form new long-term memories.' },
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
      {
        text: "Check social media to see how others are coping.",
        effects: { energy: -5 },
        nextSceneId: 'COMPARISON_TRAP',
        moduleLink: { moduleId: 'digital-distraction-protocol', moduleTitle: 'Creating Barriers for Digital Distractions', insight: 'Seeking validation through social comparison is a common stress response — but it rarely provides comfort.' },
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
    textVariants: [
      {
        condition: { stat: 'systemSavvy', max: 25 },
        text: "The CAO form stares back at you. Ten course choices, ranked in order. You barely understand the points system, let alone HEAR or DARE schemes. Everyone else seems to know exactly what they want. You're not even sure what half these courses involve.",
      },
    ],
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
      {
        text: "Ask your study partner what they're putting down.",
        effects: { socialSupport: 5 },
        nextSceneId: 'STUDY_PARTNER_CONFLICT',
        requires: [{ stat: 'socialSupport', min: 50 }],
        flavor: "Your close friendships create both support and complexity.",
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Navigating academic decisions with friends requires honest communication about different goals.' },
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
      {
        text: "Realize your timetable is already falling apart.",
        effects: { resilience: -5 },
        nextSceneId: 'REVISION_TIMETABLE_CRISIS',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'Recognising when a plan isn\'t working is the first step to building one that does.' },
      },
      {
        text: "A friend reaches out — they're really struggling.",
        effects: { socialSupport: 5 },
        nextSceneId: 'FRIEND_IN_CRISIS',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Being there for others during high-pressure periods tests your empathy and your boundaries.' },
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
      {
        text: "Consider dropping to Ordinary Level in your weakest subject.",
        effects: { systemSavvy: 5 },
        nextSceneId: 'SUBJECT_SWAP_DILEMMA',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Strategic level changes are one of the most underused tools in the Leaving Cert playbook.' },
      },
      {
        text: "A friend reaches out — they're really struggling.",
        effects: { socialSupport: 5 },
        nextSceneId: 'FRIEND_IN_CRISIS',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Being there for others during high-pressure periods tests your empathy and your boundaries.' },
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
        nextSceneId: '__ECHO_CHAIN__',
        moduleLink: { moduleId: 'points-optimization-protocol', moduleTitle: 'Points Optimization', insight: 'Generic plans work for average results. Elite performance requires personalised strategy.' },
      },
      {
        text: "Adapt the plan to my own weak areas using a Retrospective Log.",
        effects: { systemSavvy: 10, resilience: 5, academicCap: 5 },
        nextSceneId: '__ECHO_CHAIN__',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'A retrospective timetable works backwards from your exam, allocating more time to weaker areas.' },
      },
      {
        text: "Request one final practice exam from your teacher.",
        effects: { academicCap: 5, energy: -5 },
        nextSceneId: 'LAST_MOCK_PUSH',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Simulating exam conditions before the real thing builds confidence and reveals gaps.' },
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
    textVariants: [
      {
        condition: { stat: 'resilience', min: 65 },
        text: "The anxiety is there — it always is before exams. But it feels different now. It's not the paralysing terror of someone unprepared. It's the focused tension of an athlete before a race. You've trained for this. The nerves are fuel, not fear.",
      },
      {
        condition: { stat: 'energy', max: 30 },
        text: "You can't sleep. You can't focus. You can't stop thinking about tomorrow's exam. Your hands are shaking slightly as you try to review your notes. The words swim on the page. Every technique you've learned this year feels like it's evaporating from your mind.",
      },
    ],
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
      {
        text: "The pressure isn't from exams — it's from family expectations.",
        effects: { resilience: -5 },
        nextSceneId: 'FAMILY_PRESSURE',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'External pressure from family can be harder to manage than academic pressure because it carries emotional weight.' },
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
    textVariants: [
      {
        condition: { stat: 'socialSupport', max: 35 },
        text: "A classmate asks if you want to do a study session together. You hesitate — you've been doing this alone for months. The idea of studying with someone else feels unfamiliar, almost uncomfortable. But a small part of you wonders if that's been the problem all along.",
      },
    ],
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
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Study groups where everyone teaches their strength create exponential knowledge transfer.' },
      },
      {
        text: "Someone in your class has a panic attack before a test.",
        effects: { socialSupport: 5 },
        nextSceneId: 'GRACE_UNDER_PRESSURE',
        moduleLink: { moduleId: 'exam-crisis-management-protocol', moduleTitle: 'Exam Crisis Management', insight: 'How you respond to others in crisis reveals — and reinforces — your own emotional resilience.' },
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
    textVariants: [
      {
        condition: { stat: 'systemSavvy', min: 55 },
        text: "Your phone buzzes with another notification. But you've been here before — you know the research. Each distraction costs 23 minutes of refocus time. You've already mapped your distraction patterns and identified your weak moments. The question is execution.",
      },
    ],
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
      {
        text: "Create a pre-exam ritual for the morning.",
        effects: { resilience: 5 },
        nextSceneId: 'EXAM_EVE_RITUAL',
        requires: [{ stat: 'resilience', min: 50 }],
        flavor: "Your resilience lets you think beyond just studying.",
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Pre-performance rituals reduce anxiety by giving your brain a predictable sequence to follow.' },
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
    textVariants: [
      {
        condition: { stat: 'energy', min: 50 },
        text: "Tomorrow is game day. You look at your stat dashboard — energy stable, techniques sharp, friends solid, system understood, mind tough. Not many students get here with everything in balance. You don't need a last-minute miracle. You just need to show up and execute.",
      },
    ],
    choices: [
      {
        text: "Last-minute cramming session until 2 AM.",
        effects: { energy: -30, academicCap: 5 },
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Elite athletes never train the night before a competition. Your exam is your competition.' },
      },
      {
        text: "Do a 10-minute review of key formulas, then get a full night's sleep.",
        effects: { energy: 20, resilience: 10 },
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
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
      {
        text: "Go for a walk to clear your head the night before.",
        effects: { energy: 5 },
        nextSceneId: 'WALKING_TO_EXAM',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Physical movement before high-stakes events shifts the brain from anxious rumination to calm processing.' },
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
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Social capital compounds. Helping one person creates a ripple effect through their entire network.' },
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
        nextSceneId: '__CHRISTMAS_CHECK__',
        moduleLink: { moduleId: 'strategic-advantage-protocol', moduleTitle: 'Your Strategic Advantage', insight: 'Financial strategy is academic strategy. Removing money stress frees cognitive resources for learning.' },
      },
      {
        text: "Use the extra time for rest. Your energy reserves need rebuilding.",
        effects: { energy: 20, resilience: 10 },
        nextSceneId: '__CHRISTMAS_CHECK__',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Rest is not laziness — it\'s a strategic investment in your cognitive baseline.' },
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
        nextSceneId: '__BURNOUT_CHECK__',
        moduleLink: { moduleId: 'illusion-of-competence-protocol', moduleTitle: 'Overcoming Illusions of Competence', insight: 'Mock success is a data point, not a destination. The real exam is a different beast.' },
      },
      {
        text: "Share your strategy with friends who struggled.",
        effects: { socialSupport: 15, systemSavvy: 5, academicCap: 5 },
        nextSceneId: '__BURNOUT_CHECK__',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Sharing strategies that work builds deep trust and social capital that supports you under pressure.' },
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
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Post-anxiety calm creates a window of heightened focus. Use it strategically.' },
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
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
        moduleLink: { moduleId: 'exam-hall-strategies-protocol', moduleTitle: 'Exam Hall Strategies', insight: 'Exam-day confidence comes from preparation, not hope. You\'ve earned this.' },
      },
      {
        text: "Give a quiet nod of encouragement to a nervous classmate at the door.",
        effects: { socialSupport: 10, resilience: 15, energy: 5 },
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
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

  // ═══ EXPANDED STORY BRANCHES ═════════════════════════════════════════════

  // ── Phase 1: Foundation — New Branches ──────────────────────────────────────

  'LIBRARY_DISCOVERY': {
    id: 'LIBRARY_DISCOVERY',
    phase: 'Foundation',
    month: 'October',
    title: "The Library Discovery",
    mood: 'study',
    location: 'library',
    text: "You find a quiet corner in the school library and discover a shelf of study skills books. One chapter on \"desirable difficulties\" catches your eye — it claims that making learning harder actually makes it stick better.",
    choices: [
      {
        text: "Try the techniques on tonight's homework",
        effects: { academicCap: 10, resilience: 5, energy: -5 },
        nextSceneId: 'FIRST_BAD_GRADE',
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'Desirable difficulties — like testing yourself instead of re-reading — build stronger, more durable memories.' },
      },
      {
        text: "Interesting but sounds like too much effort",
        effects: { academicCap: 5 },
        nextSceneId: 'FIRST_BAD_GRADE',
        moduleLink: { moduleId: 'illusion-of-competence-protocol', moduleTitle: 'Overcoming Illusions of Competence', insight: 'The easiest study methods often produce the weakest learning. Effort is the signal, not the enemy.' },
      },
    ],
  },

  'PARENT_CONVERSATION': {
    id: 'PARENT_CONVERSATION',
    phase: 'Foundation',
    month: 'October',
    title: "The Parent Conversation",
    mood: 'social',
    location: 'home',
    text: "You show the result to your parent. Instead of disappointment, they share their own story of academic setbacks. \"Your grandmother failed her first exam too,\" they say. \"She became the first in the family to get a degree.\"",
    choices: [
      {
        text: "Ask for help setting up a study schedule at home",
        effects: { resilience: 15, socialSupport: 10, energy: 5 },
        nextSceneId: 'STUDY_METHOD_CHOICE',
        moduleLink: { moduleId: 'growth-mindset-protocol', moduleTitle: 'The Growth Protocol', insight: 'Family narratives of overcoming setbacks are a powerful source of resilience and identity.' },
      },
      {
        text: "Appreciate the talk but handle it yourself",
        effects: { resilience: 10, socialSupport: 5 },
        nextSceneId: 'STUDY_METHOD_CHOICE',
        moduleLink: { moduleId: 'self-efficacy-protocol', moduleTitle: 'Self Efficacy', insight: 'Verbal encouragement from trusted people is one of the four sources of self-efficacy.' },
      },
    ],
  },

  'PEER_PRESSURE_PARTY': {
    id: 'PEER_PRESSURE_PARTY',
    phase: 'Foundation',
    month: 'November',
    title: "The Party Dilemma",
    mood: 'social',
    location: 'social',
    text: "Your study group is meeting tonight, but someone's having a party and everyone's going. \"Come on, one night won't hurt,\" your friend texts. You know the mocks are getting closer.",
    choices: [
      {
        text: "Go for one hour, then head home to study",
        effects: { socialSupport: 10, energy: -5, academicCap: -5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Setting time boundaries on social events protects study time without sacrificing connection.' },
      },
      {
        text: "Skip it — text the group you're studying",
        effects: { academicCap: 10, socialSupport: -5, resilience: 5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'grammar-of-grit-protocol', moduleTitle: 'The Grammar of Grit', insight: 'Choosing long-term goals over short-term pleasure is the behavioural definition of grit.' },
      },
      {
        text: "Go all night — YOLO",
        effects: { socialSupport: 15, energy: -20, academicCap: -15 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'linking-study-future-goals-protocol', moduleTitle: 'Linking Study to Future Goals', insight: 'One night rarely matters — but the habit of choosing pleasure over preparation compounds over time.' },
      },
    ],
  },

  'TEACHER_FEEDBACK': {
    id: 'TEACHER_FEEDBACK',
    phase: 'Foundation',
    month: 'November',
    title: "Teacher Feedback",
    mood: 'study',
    location: 'school',
    text: "Your teacher is surprised — most students never ask about study methods. She pulls out a marking scheme and shows you exactly how examiners think. \"They're looking for these keywords,\" she explains, highlighting the patterns.",
    choices: [
      {
        text: "Start reverse-engineering every past paper",
        effects: { academicCap: 15, systemSavvy: 10, energy: -10 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'Understanding marking schemes turns exam prep from guessing into a systematic process.' },
      },
      {
        text: "Focus on the techniques, worry about exams later",
        effects: { academicCap: 10, resilience: 5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'Strong fundamentals in learning technique will serve you well regardless of exam format.' },
      },
    ],
  },

  'WELLNESS_CHECK': {
    id: 'WELLNESS_CHECK',
    phase: 'Foundation',
    month: 'December',
    title: "The Wellness Check",
    mood: 'reflection',
    location: 'school',
    text: "The counsellor's office is quieter than you expected. She doesn't lecture you about grades. Instead, she asks about sleep, about friends, about whether you're eating properly. For the first time in weeks, someone's asking how you actually feel.",
    choices: [
      {
        text: "Open up honestly about the pressure",
        effects: { resilience: 20, socialSupport: 15, energy: 10 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Professional support isn\'t a sign of weakness — it\'s a sign of self-awareness and strategic thinking.' },
      },
      {
        text: "Say everything's fine, just stressed about exams",
        effects: { resilience: 5, energy: 5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'Minimising your feelings to others often means minimising them to yourself. Honest disclosure reduces cortisol.' },
      },
    ],
  },

  'CHRISTMAS_REFLECTION': {
    id: 'CHRISTMAS_REFLECTION',
    phase: 'Foundation',
    month: 'December',
    title: "Christmas Reflection",
    mood: 'reflection',
    location: 'home',
    text: "Christmas break arrives and for the first time since September, you have space to breathe. Looking back on the term, you can see how far you've come. Your study habits are forming, your understanding of the system is growing.",
    choices: [
      {
        text: "Use the break to build a revision timetable for January",
        effects: { systemSavvy: 10, academicCap: 5, energy: 10 },
        nextSceneId: '__EARLY_MOMENTUM_CHECK__',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'Holiday planning removes decision fatigue when term starts. Your future self will thank you.' },
      },
      {
        text: "Fully switch off — rest is the priority",
        effects: { energy: 20, resilience: 10 },
        nextSceneId: '__EARLY_MOMENTUM_CHECK__',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Strategic rest during breaks prevents accumulated fatigue from destroying your January performance.' },
      },
      {
        text: "Get ahead on weak subjects",
        effects: { academicCap: 15, energy: -10 },
        nextSceneId: '__EARLY_MOMENTUM_CHECK__',
        moduleLink: { moduleId: 'mastering-spaced-repetition-protocol', moduleTitle: 'Mastering Spaced Repetition', insight: 'Holiday study sessions on weak areas create a spacing effect that strengthens memory over the break.' },
      },
    ],
  },

  // ── Phase 2: Pressure Cooker — New Branches ─────────────────────────────────

  'MOCK_RESULTS_HIGH': {
    id: 'MOCK_RESULTS_HIGH',
    phase: 'Pressure Cooker',
    month: 'January',
    title: "Mock Results — Better Than Expected",
    mood: 'triumph',
    location: 'school',
    text: "The results come back better than expected. Not perfect, but the gap between where you are and where you need to be feels bridgeable. Your teacher circles two subjects: \"These are your gain subjects — focus here for maximum point improvement.\"",
    choices: [
      {
        text: "Follow the teacher's advice — target the gain subjects",
        effects: { academicCap: 10, systemSavvy: 10 },
        nextSceneId: '__BURNOUT_CHECK__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Gain subjects — where you\'re close to the next grade band — offer the highest points-per-hour return.' },
      },
      {
        text: "Spread effort evenly across all subjects",
        effects: { academicCap: 5, resilience: 5 },
        nextSceneId: '__BURNOUT_CHECK__',
        moduleLink: { moduleId: 'mastering-interleaving-protocol', moduleTitle: 'Mastering Interleaving', insight: 'Even coverage prevents nasty surprises, but targeted effort creates breakthroughs.' },
      },
    ],
  },

  'MOCK_RESULTS_LOW': {
    id: 'MOCK_RESULTS_LOW',
    phase: 'Pressure Cooker',
    month: 'January',
    title: "Mock Results — Reality Check",
    mood: 'crisis',
    location: 'school',
    text: "The results hit hard. The numbers on the page don't match the hours you put in. Around you, classmates are comparing results and you feel the urge to hide yours. A knot forms in your stomach.",
    choices: [
      {
        text: "Analyze where the marks were lost — it's data, not destiny",
        effects: { resilience: 15, academicCap: 10, systemSavvy: 5 },
        nextSceneId: '__BURNOUT_CHECK__',
        moduleLink: { moduleId: 'growth-mindset-protocol', moduleTitle: 'The Growth Protocol', insight: 'Mock results are diagnostic data, not a verdict. The gap between effort and outcome often reveals method problems, not ability problems.' },
      },
      {
        text: "This confirms it — I'm not cut out for this",
        effects: { resilience: -15, energy: -10 },
        nextSceneId: '__BURNOUT_CHECK__',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'One set of results doesn\'t define your ceiling. The story you tell yourself about the result matters more than the result itself.' },
      },
      {
        text: "Talk to your teacher about what went wrong",
        effects: { academicCap: 15, socialSupport: 5, resilience: 5 },
        nextSceneId: '__BURNOUT_CHECK__',
        requires: [{ stat: 'socialSupport', min: 40 }],
        flavor: "Your social connections make it easier to ask for help.",
        moduleLink: { moduleId: 'self-efficacy-protocol', moduleTitle: 'Self Efficacy', insight: 'Seeking expert feedback after failure is one of the most powerful learning accelerators available.' },
      },
    ],
  },

  'STUDY_PARTNER_CONFLICT': {
    id: 'STUDY_PARTNER_CONFLICT',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "The Study Partner Conflict",
    mood: 'social',
    location: 'school',
    text: "Your study partner wants to copy your CAO order. \"We've always done everything together,\" they say. But your courses are different — their dream course could push yours down the preference list if you both get the same points.",
    choices: [
      {
        text: "Be honest — your priorities are different and that's okay",
        effects: { socialSupport: 5, resilience: 10, systemSavvy: 5 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Healthy boundaries in friendships require honest communication, not conflict avoidance.' },
      },
      {
        text: "Help them research their own best options",
        effects: { socialSupport: 15, systemSavvy: 5, energy: -10 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Helping others understand the CAO system deepens your own strategic understanding.' },
      },
    ],
  },

  'COMPARISON_TRAP': {
    id: 'COMPARISON_TRAP',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "The Comparison Trap",
    mood: 'crisis',
    location: 'online',
    text: "Your feed is full of study aesthetics — colour-coded notes, aesthetic desk setups, \"day in my life\" videos of people studying 12 hours straight. Everyone seems to have it together. You feel further behind than ever.",
    choices: [
      {
        text: "Mute study content, focus on your own plan",
        effects: { resilience: 10, energy: 5 },
        nextSceneId: 'CAO_DEADLINE',
        moduleLink: { moduleId: 'digital-distraction-protocol', moduleTitle: 'Creating Barriers for Digital Distractions', insight: 'Social comparison is a cognitive bias that distorts reality. Other people\'s highlight reels are not their full story.' },
      },
      {
        text: "Try to match their intensity",
        effects: { energy: -15, resilience: -10, academicCap: 5 },
        nextSceneId: 'CAO_DEADLINE',
        moduleLink: { moduleId: 'illusion-of-competence-protocol', moduleTitle: 'Overcoming Illusions of Competence', insight: 'Aesthetic study setups often mask passive methods. Hours studied matters less than how you study.' },
      },
    ],
  },

  'SUBJECT_SWAP_DILEMMA': {
    id: 'SUBJECT_SWAP_DILEMMA',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "The Subject Swap Dilemma",
    mood: 'opportunity',
    location: 'school',
    text: "Your mentor suggests something radical — drop to OL in your weakest subject and reinvest those hours into your strongest ones. \"It's not giving up,\" she says. \"It's strategic resource allocation.\" The maths checks out — you could actually gain more CAO points this way.",
    choices: [
      {
        text: "Make the strategic drop — maximise total points",
        effects: { systemSavvy: 15, academicCap: 10, resilience: 5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'The CAO rewards total points, not pride. Strategic level changes can unlock more points than grinding a weak subject.' },
      },
      {
        text: "Stay at Higher Level — prove you can do it",
        effects: { resilience: 10, energy: -10 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'grammar-of-grit-protocol', moduleTitle: 'The Grammar of Grit', insight: 'Grit and strategy aren\'t opposites — but knowing when persistence is costing you requires honest self-assessment.' },
      },
    ],
  },

  'REVISION_TIMETABLE_CRISIS': {
    id: 'REVISION_TIMETABLE_CRISIS',
    phase: 'Pressure Cooker',
    month: 'March',
    title: "Timetable Crisis",
    mood: 'crisis',
    location: 'home',
    text: "Three weeks into your revision plan and you're already two topics behind. The perfectly colour-coded timetable on your wall now mocks you. Each missed session compounds the anxiety.",
    choices: [
      {
        text: "Rewrite the timetable — be realistic this time",
        effects: { systemSavvy: 10, resilience: 10, energy: -5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'The best timetable is one you actually follow. Overambitious plans create guilt spirals.' },
      },
      {
        text: "Abandon the timetable and study by feel",
        effects: { energy: 5, systemSavvy: -10, resilience: -5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'procrastination-protocol', moduleTitle: 'Understanding Procrastination and Motivation', insight: 'Studying by feel usually means studying what\'s comfortable, not what\'s needed. Structure beats motivation.' },
      },
      {
        text: "Apply the Triage Protocol — rank topics by marks-per-hour",
        effects: { systemSavvy: 15, academicCap: 15, resilience: 5, energy: -10 },
        nextSceneId: 'FINAL_STRETCH_START',
        requires: [{ stat: 'systemSavvy', min: 55 }],
        flavor: "Your system knowledge unlocks a strategic approach to revision.",
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Triage means focusing on topics with the highest marks-per-hour return. Not all topics are created equal.' },
      },
    ],
  },

  'FRIEND_IN_CRISIS': {
    id: 'FRIEND_IN_CRISIS',
    phase: 'Pressure Cooker',
    month: 'March',
    title: "A Friend in Crisis",
    mood: 'social',
    location: 'home',
    text: "A friend messages you late at night. They're not coping. The pressure, the expectations, the fear of disappointing everyone — it's all hitting them at once. They don't explicitly ask for help, but you can read between the lines.",
    choices: [
      {
        text: "Drop everything and go be with them",
        effects: { socialSupport: 20, energy: -15, resilience: 10 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Being present for someone in crisis is one of the most powerful things a friend can do. It costs time but builds unbreakable bonds.' },
      },
      {
        text: "Listen and gently suggest the school counsellor",
        effects: { socialSupport: 10, resilience: 5, systemSavvy: 5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Knowing when to refer someone to professional help is a sign of emotional maturity, not abandonment.' },
      },
      {
        text: "You're barely holding it together yourself — send a supportive text",
        effects: { socialSupport: 5, resilience: -5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'You can\'t pour from an empty cup. Recognising your own limits is honest, not selfish.' },
      },
    ],
  },

  // ── Phase 3: Final Stretch — New Branches ───────────────────────────────────

  'LAST_MOCK_PUSH': {
    id: 'LAST_MOCK_PUSH',
    phase: 'Final Stretch',
    month: 'April',
    title: "One Last Practice Exam",
    mood: 'exam',
    location: 'school',
    text: "Your teacher agrees to mark one more paper under exam conditions. Saturday morning, empty classroom, three hours. The silence feels different from studying at home — it's the silence of the exam hall.",
    choices: [
      {
        text: "Treat it exactly like the real thing — no phone, strict timing",
        effects: { academicCap: 15, resilience: 10, energy: -10 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Simulating exam conditions in practice reduces the novelty penalty on the real day.' },
      },
      {
        text: "Use it as a diagnostic — check answers as you go",
        effects: { academicCap: 10, systemSavvy: 10, energy: -5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'Diagnostic practice with immediate feedback accelerates learning — but doesn\'t build exam stamina.' },
      },
    ],
  },

  'FAMILY_PRESSURE': {
    id: 'FAMILY_PRESSURE',
    phase: 'Final Stretch',
    month: 'April',
    title: "Family Expectations",
    mood: 'crisis',
    location: 'home',
    text: "\"Your cousin got 600 points.\" \"We've invested so much in your education.\" \"Have you thought about medicine?\" The expectations pile up like bricks on your chest. You know they mean well, but the weight is crushing.",
    choices: [
      {
        text: "Have an honest conversation about YOUR goals",
        effects: { resilience: 15, socialSupport: 10, energy: 5 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'best-possible-self-protocol', moduleTitle: 'Finding Your Best Possible Self', insight: 'Clarifying your own goals — separate from family expectations — is essential for authentic motivation.' },
      },
      {
        text: "Nod along and carry the weight silently",
        effects: { resilience: -10, energy: -10 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'Unexpressed pressure doesn\'t disappear — it compounds. Silent compliance breeds resentment and burnout.' },
      },
      {
        text: "Write them a letter explaining your actual plan",
        effects: { resilience: 10, socialSupport: 15, systemSavvy: 5 },
        nextSceneId: 'PEER_SUPPORT',
        requires: [{ stat: 'systemSavvy', min: 45 }],
        flavor: "Your system knowledge helps you articulate a credible plan.",
        moduleLink: { moduleId: 'linking-study-future-goals-protocol', moduleTitle: 'Linking Study to Future Goals', insight: 'A written plan with evidence shows family you\'re serious — and forces you to clarify your own thinking.' },
      },
    ],
  },

  'EXAM_EVE_RITUAL': {
    id: 'EXAM_EVE_RITUAL',
    phase: 'Final Stretch',
    month: 'May',
    title: "The Exam Eve Ritual",
    mood: 'reflection',
    location: 'home',
    text: "You've read about elite athletes having pre-game rituals. Why not apply the same logic? You design a morning routine: wake time, breakfast, review sheet, walk to school route, breathing exercise outside the exam hall.",
    choices: [
      {
        text: "Test-run it before a practice paper",
        effects: { resilience: 15, energy: 10, academicCap: 5 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Rehearsing your exam-day routine removes uncertainty and frees cognitive resources for the actual exam.' },
      },
      {
        text: "Write it down but wing it on the day",
        effects: { resilience: 5, systemSavvy: 5 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'exam-hall-strategies-protocol', moduleTitle: 'Exam Hall Strategies', insight: 'A plan you haven\'t rehearsed is just a wish. Practice turns intention into automatic behaviour.' },
      },
    ],
  },

  'GRACE_UNDER_PRESSURE': {
    id: 'GRACE_UNDER_PRESSURE',
    phase: 'Final Stretch',
    month: 'May',
    title: "Grace Under Pressure",
    mood: 'social',
    location: 'school',
    text: "During a class test, the student beside you starts hyperventilating. The teacher hasn't noticed yet. Everyone else is frozen, staring at their papers. You remember the Physiological Sigh technique from a module you completed.",
    choices: [
      {
        text: "Quietly help them with the breathing technique",
        effects: { socialSupport: 15, resilience: 10 },
        nextSceneId: 'DIGITAL_DISTRACTION',
        moduleLink: { moduleId: 'exam-crisis-management-protocol', moduleTitle: 'Exam Crisis Management', insight: 'Teaching someone a calming technique in the moment reinforces your own ability to use it under pressure.' },
      },
      {
        text: "Alert the teacher immediately",
        effects: { socialSupport: 5, resilience: 5 },
        nextSceneId: 'DIGITAL_DISTRACTION',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Knowing when a situation needs professional intervention is a form of emotional intelligence.' },
      },
    ],
  },

  'NIGHT_BEFORE': {
    id: 'NIGHT_BEFORE',
    phase: 'Final Stretch',
    month: 'June',
    title: "The Night Before",
    mood: 'reflection',
    location: 'home',
    text: "Tomorrow is the first exam. Your bag is packed, your pens are ready, your ID is by the door. The house is quiet. You lie in bed, staring at the ceiling. Every formula, every quote, every technique you've learned this year swirls through your mind.",
    choices: [
      {
        text: "Trust your preparation — close your eyes and breathe",
        effects: { resilience: 10, energy: 15 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'The night before is too late to learn anything new. Trust the months of preparation and let your brain consolidate.' },
      },
      {
        text: "One final look at your summary sheet, then sleep",
        effects: { academicCap: 5, energy: 5 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'mastering-spaced-repetition-protocol', moduleTitle: 'Mastering Spaced Repetition', insight: 'A brief review before sleep leverages the spacing effect — your brain processes it overnight.' },
      },
      {
        text: "Call your study partner — you promised you'd check in",
        effects: { socialSupport: 10, resilience: 10, energy: 5 },
        nextSceneId: '__END_ROUTE__',
        requires: [{ stat: 'socialSupport', min: 60 }],
        flavor: "Your deep connections mean you don't face this night alone.",
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Social connection before high-pressure events reduces cortisol and increases feelings of safety.' },
      },
    ],
  },

  'WALKING_TO_EXAM': {
    id: 'WALKING_TO_EXAM',
    phase: 'Final Stretch',
    month: 'June',
    title: "The Walk",
    mood: 'reflection',
    location: 'social',
    text: "The evening air is cool on your face. You walk the route you'll take tomorrow morning, past the school gates, along the corridor in your mind's eye. Something shifts. The months of pressure crystallize into a single, clear thought: you've done the work. Whatever happens tomorrow, you showed up every single day.",
    choices: [
      {
        text: "Head home with quiet confidence",
        effects: { resilience: 10, energy: 10 },
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Walking is one of the most effective ways to reduce anxiety. Movement shifts your brain from rumination to processing.' },
      },
      {
        text: "Text your friend — 'We've got this'",
        effects: { socialSupport: 10, resilience: 5, energy: 5 },
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Mutual encouragement before high-stakes events creates a shared sense of agency and belonging.' },
      },
    ],
  },

  // ── Consequence Echo Scenes (Phase 3) ───────────────────────────────────────

  'ECHO_STUDY_GROUP': {
    id: 'ECHO_STUDY_GROUP',
    phase: 'Final Stretch',
    month: 'April',
    title: "The Study Group Returns",
    mood: 'social',
    location: 'library',
    text: "The study group you started back in November is still going. What began as three people in a library corner has become a revision machine. Someone made a shared Google Drive. Someone else mapped every exam topic to a study session. You realize the compound returns of that one decision months ago.",
    choices: [
      {
        text: "Take the lead on final revision sessions",
        effects: { socialSupport: 10, academicCap: 10, energy: -5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Study groups that survive to exam season create exponential knowledge-sharing. Your early investment is paying compound interest.' },
      },
      {
        text: "Step back and let the group run itself",
        effects: { energy: 5, socialSupport: 5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'cognitive-endurance-protocol', moduleTitle: 'Cognitive Endurance', insight: 'Delegating leadership frees cognitive resources for your own preparation — a sign of maturity, not abandonment.' },
      },
    ],
  },

  'ECHO_SPIRAL': {
    id: 'ECHO_SPIRAL',
    phase: 'Final Stretch',
    month: 'April',
    title: "Recognizing the Pattern",
    mood: 'reflection',
    location: 'home',
    text: "You catch yourself highlighting a page of notes — the same passive habit that nearly derailed you back in November. But this time, you recognize it instantly. You put down the highlighter and reach for a blank page instead. The spiral taught you something no textbook could.",
    choices: [
      {
        text: "Channel that awareness into your strongest technique",
        effects: { resilience: 15, academicCap: 10 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'Metacognitive awareness — recognising your own study habits in real-time — is the ultimate learning superpower.' },
      },
      {
        text: "Share your story with a classmate who's struggling now",
        effects: { socialSupport: 15, resilience: 10, energy: -5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'growth-mindset-protocol', moduleTitle: 'The Growth Protocol', insight: 'Your struggle story is your most powerful teaching tool. Vulnerability builds trust and helps others see a path forward.' },
      },
    ],
  },

  'ECHO_ADVOCATE': {
    id: 'ECHO_ADVOCATE',
    phase: 'Final Stretch',
    month: 'April',
    title: "The Ripple Effect",
    mood: 'social',
    location: 'school',
    text: "A younger student approaches you in the corridor. \"You're the one who told my sister about HEAR, right? She got her offer last week.\" The ripple effects of a single conversation back in September have reached further than you imagined.",
    choices: [
      {
        text: "Offer to help more students with applications next year",
        effects: { socialSupport: 10, systemSavvy: 10, resilience: 5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'System knowledge shared widely creates community-level advantage. One informed student can change dozens of outcomes.' },
      },
      {
        text: "Smile and focus on your own exams",
        effects: { resilience: 5, energy: 5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'strategic-advantage-protocol', moduleTitle: 'Your Strategic Advantage', insight: 'Sometimes the best thing you can do is focus on yourself. Your success story will inspire others on its own.' },
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
  'END_REGROUPING': {
    id: 'END_REGROUPING',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Unfinished Chapter",
    mood: 'reflection',
    location: 'home',
    text: "The results weren't what you needed. It stings — there's no way around that. But you're still standing. You know more about yourself than you did a year ago. You know what works, what doesn't, and what matters to you. The points are one number on one day. Your story is far from over.",
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
