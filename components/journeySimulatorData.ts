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
export type CapabilityKey = Exclude<StatKey, 'energy'>;

export type JourneyEvidence = Record<CapabilityKey, {
  earned: number;
  possible: number;
}>;

export type ModuleLink = {
  moduleId: string;
  moduleTitle: string;
  insight: string;
};

export type Choice = {
  text: string;
  effects: Partial<GameState>;
  nextSceneId: string;
  /** Safety and context choices can teach without judging the student's character. */
  scoreless?: boolean;
  moduleLink?: ModuleLink;
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
  energy: 65,
  academicCap: 50,
  socialSupport: 50,
  systemSavvy: 50,
  resilience: 50,
};

export const JOURNEY_SCORING_VERSION = 2;
export const CAPABILITY_KEYS: CapabilityKey[] = ['academicCap', 'socialSupport', 'systemSavvy', 'resilience'];

export const createJourneyEvidence = (): JourneyEvidence => ({
  academicCap: { earned: 0, possible: 0 },
  socialSupport: { earned: 0, possible: 0 },
  systemSavvy: { earned: 0, possible: 0 },
  resilience: { earned: 0, possible: 0 },
});

export const PHASE_METADATA: PhaseMetadata[] = [
  { name: 'Foundation', months: 'Sep – Dec', subtitle: 'Building the base. Every habit you form now echoes through the year.' },
  { name: 'Pressure Cooker', months: 'Jan – Mar', subtitle: 'The pressure builds. Your strategies are tested under fire.' },
  { name: 'Final Stretch', months: 'Apr – Jun', subtitle: 'The home straight. Everything you\'ve built is put to the ultimate test.' },
];

export const STAT_LABELS: Record<StatKey, string> = {
  energy: 'Energy Reserve',
  academicCap: 'Learning Strategy',
  socialSupport: 'Support Use',
  systemSavvy: 'Practical Planning',
  resilience: 'Recovery Skills',
};

const clampScore = (value: number): number => Math.max(0, Math.min(100, Math.round(value)));

/**
 * Legacy story deltas encode authored intent with inconsistent magnitudes.
 * Convert them into a small evidence scale before they reach the student score.
 */
export const normaliseCapabilityImpact = (value = 0): -2 | -1 | 0 | 1 | 2 => {
  if (value >= 15) return 2;
  if (value >= 5) return 1;
  if (value <= -15) return -2;
  if (value <= -5) return -1;
  return 0;
};

/** Energy is a changing reserve, not evidence of capability. */
export const normaliseEnergyImpact = (value = 0): number => {
  if (value <= -40) return -22;
  if (value <= -30) return -18;
  if (value <= -20) return -13;
  if (value <= -15) return -9;
  if (value <= -10) return -6;
  if (value <= -5) return -3;
  if (value >= 40) return 16;
  if (value >= 25) return 12;
  if (value >= 20) return 10;
  if (value >= 15) return 8;
  if (value >= 10) return 6;
  if (value >= 5) return 3;
  return 0;
};

const scoreFromEvidence = ({ earned, possible }: JourneyEvidence[CapabilityKey]): number => {
  // Four points of neutral prior evidence stops a single early answer producing an extreme score.
  const ratio = earned / (possible + 4);
  return clampScore(50 + (40 * Math.max(-1, Math.min(1, ratio))));
};

export function applyJourneyChoice(
  state: GameState,
  evidence: JourneyEvidence,
  choice: Choice,
  choicesSeen: Choice[],
): { state: GameState; evidence: JourneyEvidence } {
  const nextEvidence: JourneyEvidence = {
    academicCap: { ...evidence.academicCap },
    socialSupport: { ...evidence.socialSupport },
    systemSavvy: { ...evidence.systemSavvy },
    resilience: { ...evidence.resilience },
  };

  if (!choice.scoreless) {
    for (const capability of CAPABILITY_KEYS) {
      const opportunity = Math.max(
        0,
        ...choicesSeen
          .filter(candidate => !candidate.scoreless)
          .map(candidate => Math.abs(normaliseCapabilityImpact(candidate.effects[capability]))),
      );
      if (opportunity > 0) {
        nextEvidence[capability].possible += opportunity;
        nextEvidence[capability].earned += normaliseCapabilityImpact(choice.effects[capability]);
      }
    }
  }

  const nextState: GameState = {
    energy: clampScore(state.energy + normaliseEnergyImpact(choice.effects.energy) + (choice.scoreless ? 0 : 1)),
    academicCap: scoreFromEvidence(nextEvidence.academicCap),
    socialSupport: scoreFromEvidence(nextEvidence.socialSupport),
    systemSavvy: scoreFromEvidence(nextEvidence.systemSavvy),
    resilience: scoreFromEvidence(nextEvidence.resilience),
  };

  return { state: nextState, evidence: nextEvidence };
}

export function getWeakestCapability(state: GameState): CapabilityKey[] {
  const minimum = Math.min(...CAPABILITY_KEYS.map(key => state[key]));
  return CAPABILITY_KEYS.filter(key => state[key] === minimum);
}

export function getStrongestCapability(state: GameState): CapabilityKey[] {
  const maximum = Math.max(...CAPABILITY_KEYS.map(key => state[key]));
  return CAPABILITY_KEYS.filter(key => state[key] === maximum);
}

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
    title: 'The Adaptive Pathfinder',
    icon: 'compass',
    accentColor: 'text-emerald-600 dark:text-emerald-400',
    accentBg: 'bg-emerald-100 dark:bg-emerald-900/30',
    description: 'Your choices leaned on recovery, perspective and connection. You tended to adapt when plans changed and to involve other people rather than carrying every setback alone.',
  },
  END_EXPERT: {
    id: 'END_EXPERT',
    title: 'The Methodical Learner',
    icon: 'brain',
    accentColor: 'text-blue-600 dark:text-blue-400',
    accentBg: 'bg-blue-100 dark:bg-blue-900/30',
    description: 'Your choices consistently favoured feedback, retrieval and deliberate practice. Your strongest pattern was improving the method, not merely adding more hours.',
  },
  END_MENTOR: {
    id: 'END_MENTOR',
    title: 'The Knowledge Connector',
    icon: 'hand-helping',
    accentColor: 'text-[var(--accent-hex)] dark:text-[var(--accent-hex)]',
    accentBg: 'bg-[rgba(var(--accent),0.1)] dark:bg-[rgba(var(--accent),0.15)]',
    description: 'You repeatedly connected useful information with the people who needed it. Your profile combines collaboration with a practical understanding of how the education system works.',
  },
  END_GOOD: {
    id: 'END_GOOD',
    title: 'The Deliberate Builder',
    icon: 'target',
    accentColor: 'text-amber-600 dark:text-amber-400',
    accentBg: 'bg-amber-100 dark:bg-amber-900/30',
    description: 'You built progress through a sequence of workable decisions. The profile is not extreme in one direction; it reflects steady academic judgement and a willingness to adjust.',
  },
  END_REGROUPING: {
    id: 'END_REGROUPING',
    title: 'The Reflective Recalibrator',
    icon: 'book-open',
    accentColor: 'text-violet-600 dark:text-violet-400',
    accentBg: 'bg-violet-100 dark:bg-violet-900/30',
    description: 'Some choices created strain or uncertainty, but you also showed evidence of noticing what was not working. Your next advantage is to turn that reflection into one smaller, repeatable system.',
  },
  END_PLC: {
    id: 'END_PLC',
    title: 'The Route Explorer',
    icon: 'arrow-up-right',
    accentColor: 'text-teal-600 dark:text-teal-400',
    accentBg: 'bg-teal-100 dark:bg-teal-900/30',
    description: 'You showed a willingness to examine more than one route and to treat educational choices as a set of options rather than a single all-or-nothing outcome.',
  },
  END_REPEAT: {
    id: 'END_REPEAT',
    title: 'The Reset Builder',
    icon: 'rotate-ccw',
    accentColor: 'text-rose-600 dark:text-rose-400',
    accentBg: 'bg-rose-100 dark:bg-rose-900/30',
    description: 'Your route exposed several systems that need rebuilding. The useful signal is not a verdict about ability; it is a clearer view of where support, structure and recovery would change the next attempt.',
  },
  END_SCHOLARSHIP: {
    id: 'END_SCHOLARSHIP',
    title: 'The Opportunity Navigator',
    icon: 'award',
    accentColor: 'text-yellow-600 dark:text-yellow-400',
    accentBg: 'bg-yellow-100 dark:bg-yellow-900/30',
    description: 'You did more than study: you looked for relevant routes, checked processes and followed through on an opportunity. This profile reflects informed option-building, not a guaranteed application outcome.',
  },
  END_LEADER: {
    id: 'END_LEADER',
    title: 'The Collaborative Leader',
    icon: 'megaphone',
    accentColor: 'text-indigo-600 dark:text-indigo-400',
    accentBg: 'bg-indigo-100 dark:bg-indigo-900/30',
    description: 'You repeatedly created useful structures for learning with other people. The strongest evidence in your route was collaboration with boundaries, not self-sacrifice.',
  },
  END_COMEBACK: {
    id: 'END_COMEBACK',
    title: 'The Recovery Builder',
    icon: 'flame',
    accentColor: 'text-orange-600 dark:text-orange-400',
    accentBg: 'bg-orange-100 dark:bg-orange-900/30',
    description: 'You encountered an unhelpful pattern and later recognised it. Your defining evidence was the decision to change approach rather than repeat the same response.',
  },
  END_BALANCED: {
    id: 'END_BALANCED',
    title: 'The Balanced Learner',
    icon: 'scale',
    accentColor: 'text-cyan-600 dark:text-cyan-400',
    accentBg: 'bg-cyan-100 dark:bg-cyan-900/30',
    description: 'Your evidence is distributed across learning, planning, support and coping. No single capability carried the route; the pattern came from keeping several useful systems working together.',
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
  const totalImpact = (effects: Partial<GameState>): number =>
    (Object.entries(effects) as [StatKey, number][]).reduce((sum, [stat, value]) => (
      sum + Math.abs(stat === 'energy' ? normaliseEnergyImpact(value) : normaliseCapabilityImpact(value))
    ), 0);

  return [...history]
    .sort((a, b) => totalImpact(b.effects) - totalImpact(a.effects))
    .filter(item => totalImpact(item.effects) > 0)
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
  energy: "Your current energy reserve is low. Treat that as a prompt to review sleep, workload and support — not as a judgement about motivation or character.",
  academicCap: "Your choices produced less evidence of deliberate learning practice. A useful next step is one short retrieval session followed by feedback, rather than simply adding more hours.",
  socialSupport: "Your route produced less evidence of using support. One specific conversation with a teacher, guidance counsellor, family member or friend can make the next decision easier.",
  systemSavvy: "Your route produced less evidence of checking deadlines, requirements and available supports. Use official sources and a guidance counsellor to map the next practical step.",
  resilience: "Your route produced less evidence of a recovery plan after setbacks. Decide in advance whom you will contact and what small action you will take when pressure rises.",
};

// ─── Route Resolvers (invisible logic gates) ─────────────────────────────────

export function selectJourneyEnding(state: GameState, history: HistoryItem[] = []): string {
  const visited = new Set(history.map(item => item.scene.id));
  const capabilityValues = CAPABILITY_KEYS.map(key => state[key]);
  const capabilityMean = capabilityValues.reduce((sum, value) => sum + value, 0) / capabilityValues.length;
  const capabilitySpread = Math.max(...capabilityValues) - Math.min(...capabilityValues);
  const lowCapabilityCount = capabilityValues.filter(value => value < 40).length;
  const choseAlternativeRoute = history.some(item => /Level 6\/7|PLC|apprenticeship|alternative route/i.test(item.choiceText));

  if (state.energy < 20 && (capabilityMean < 55 || lowCapabilityCount >= 2)) return 'END_REPEAT';
  if (capabilityMean < 47 || lowCapabilityCount >= 3) return 'END_REGROUPING';

  const candidates: { id: string; score: number }[] = [
    { id: 'END_GOOD', score: capabilityMean },
    { id: 'END_EXPERT', score: state.academicCap },
    { id: 'END_PATHFINDER', score: (state.resilience + state.socialSupport) / 2 },
  ];

  if (capabilitySpread <= 12 && state.energy >= 40) {
    candidates.push({ id: 'END_BALANCED', score: 78 - capabilitySpread });
  }
  if (visited.has('SCHOLARSHIP_PATH')) {
    candidates.push({ id: 'END_SCHOLARSHIP', score: ((state.systemSavvy + state.academicCap) / 2) + 10 });
  }
  if (visited.has('PASSIVE_SPIRAL')) {
    candidates.push({ id: 'END_COMEBACK', score: state.resilience + 6 });
  }
  if (visited.has('STUDY_GROUP') || visited.has('STUDY_GROUP_LEADER') || visited.has('TEACHING_LEGACY')) {
    candidates.push({ id: 'END_LEADER', score: state.socialSupport + 5 });
  }
  if (visited.has('HEAR_ADVOCATE') || visited.has('TEACHING_LEGACY')) {
    candidates.push({ id: 'END_MENTOR', score: ((state.socialSupport + state.systemSavvy) / 2) + 3 });
  }
  if (choseAlternativeRoute) {
    candidates.push({ id: 'END_PLC', score: state.systemSavvy + 5 });
  }

  return candidates.sort((a, b) => b.score - a.score)[0].id;
}

export const ROUTE_RESOLVERS: Record<string, (state: GameState, history?: HistoryItem[]) => string> = {
  '__BURNOUT_CHECK__': (state) => state.energy < 30 ? 'BURNOUT_RECOVERY' : 'CAO_DEADLINE',
  '__ACADEMIC_CHECK__': (state) => state.academicCap >= 58 ? 'INTERLEAVING_CHOICE' : 'MENTOR_MOMENT',
  '__EARLY_MOMENTUM_CHECK__': (state) => (state.systemSavvy >= 56 && state.academicCap >= 54) ? 'EARLY_MOMENTUM' : 'MOCKS_LOOM',
  '__SYSTEM_MASTERY_CHECK__': (state) => state.systemSavvy >= 62 ? 'SYSTEM_MASTERY' : 'GAME_DAY_PREP',
  '__COMEBACK_CHECK__': (state, history) => {
    const visitedSpiral = history?.some(h => h.scene.id === 'PASSIVE_SPIRAL');
    if (visitedSpiral && state.resilience >= 56) return 'COMEBACK_RALLY';
    return '__SYSTEM_MASTERY_CHECK__';
  },
  '__CHRISTMAS_CHECK__': (state) => (state.energy >= 50 && state.resilience >= 50) ? 'CHRISTMAS_REFLECTION' : '__EARLY_MOMENTUM_CHECK__',
  '__MOCK_RESULTS_CHECK__': (state) => state.academicCap >= 54 ? 'MOCK_RESULTS_HIGH' : 'MOCK_RESULTS_LOW',
  '__ECHO_CHAIN__': (_state, history) => {
    const visited = history?.map(h => h.scene.id) ?? [];
    if (visited.includes('STUDY_GROUP') || visited.includes('STUDY_GROUP_LEADER')) return 'ECHO_STUDY_GROUP';
    if (visited.includes('PASSIVE_SPIRAL')) return 'ECHO_SPIRAL';
    if (visited.includes('HEAR_ADVOCATE')) return 'ECHO_ADVOCATE';
    return 'EXAM_ANXIETY';
  },
  '__NIGHT_BEFORE_CHECK__': (state) => (state.resilience >= 52 && state.energy >= 38) ? 'NIGHT_BEFORE' : '__END_ROUTE__',
  '__END_ROUTE__': (state, history) => selectJourneyEnding(state, history),
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
    text: "First week of 6th year. Guidance class introduces HEAR and DARE. They may be relevant depending on your circumstances, and both have eligibility rules, evidence requirements and deadlines to check.",
    choices: [
      {
        text: "Check the official criteria and timeline with the guidance counsellor.",
        effects: { systemSavvy: 15, energy: -5 },
        nextSceneId: 'MATHS_CLASS',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'HEAR and DARE are separate admissions schemes with specific eligibility and documentation rules. Check current official guidance early.' },
      },
      {
        text: "Note that they are not relevant to me, then check what other routes or supports are.",
        effects: { systemSavvy: 5, academicCap: 5 },
        nextSceneId: 'MATHS_CLASS',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'Strategic planning early on prevents last-minute scrambles later.' },
      },
      {
        text: "Share the official information with friends who may want to check their eligibility.",
        effects: { systemSavvy: 10, socialSupport: 5, energy: -5 },
        nextSceneId: 'HEAR_ADVOCATE',
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
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Peer learning accelerates understanding and builds bonds that sustain you under pressure.' },
      },
      {
        text: "Head to the library to research study techniques.",
        effects: { academicCap: 5, energy: -5 },
        nextSceneId: 'LIBRARY_DISCOVERY',
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'Self-directed learning about how to learn is the most leveraged investment a student can make.' },
      },
    ],
  },

  'FIRST_BAD_GRADE': {
    id: 'FIRST_BAD_GRADE',
    phase: 'Foundation',
    month: 'October',
    title: "The First Disappointing Result",
    mood: 'crisis',
    location: 'school',
    text: "Your first big English test comes back at H4, below the target you had set. Your heart sinks. What do you do with the result?",
    choices: [
      {
        text: "'This proves I'm not capable of my target grade.' Spend the evening feeling demotivated.",
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
        text: "Retrieval practice: Close the book and write what you can remember, then check the gaps.",
        effects: { energy: -15, academicCap: 15, resilience: 5 },
        nextSceneId: 'TECHNIQUE_UPGRADE',
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'Effortful retrieval can strengthen memory when it is followed by accurate feedback and spaced practice.' },
      },
      {
        text: "Teach a younger student what you've learned — explaining forces understanding.",
        effects: { socialSupport: 10, academicCap: 10, energy: -10 },
        nextSceneId: 'STUDY_GROUP_LEADER',
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Explaining material to someone else can expose gaps and prompt deeper processing, provided the explanation is checked for accuracy.' },
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
        moduleLink: { moduleId: 'mastering-spaced-repetition-protocol', moduleTitle: 'Mastering Spaced Repetition', insight: 'Spaced retrieval can improve long-term retention, especially when each attempt is checked against accurate feedback.' },
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
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'An honest conversation can reduce isolation and make practical support easier to access.' },
      },
      {
        text: "'I'm fine.' Push through alone. Don't show weakness.",
        effects: { socialSupport: -10, resilience: -5, energy: -10 },
        nextSceneId: 'SOCIAL_ISOLATION',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'Connection does not solve every worry, but it can interrupt isolation and bring another perspective into the problem.' },
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
        text: "Set a realistic evening cut-off and protect time for sleep, food and connection.",
        effects: { energy: 15, socialSupport: 10, resilience: 5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Sleep supports memory consolidation and attention. Protecting rest can be more useful than extending an already exhausted study session.' },
      },
      {
        text: "Double down. The exams won't wait. Sacrifice everything for study.",
        effects: { academicCap: -5, energy: -15, socialSupport: -10 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Sleep and social connection aren\'t luxuries — they\'re biological inputs your brain needs to function.' },
      },
      {
        text: "Speak to the school counsellor or another trusted adult.",
        effects: { socialSupport: 10, systemSavvy: 5 },
        nextSceneId: 'WELLNESS_CHECK',
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
    text: "The pop quiz was challenging, but you retrieved more of the key facts than last time. One result does not prove a method, but retrieval practice looks promising enough to keep testing.",
    choices: [
      {
        text: "Double down: 'This works. I'll build Spaced Repetition into my routine.'",
        effects: { academicCap: 15, resilience: 5 },
        nextSceneId: 'STUDY_GROUP',
        moduleLink: { moduleId: 'mastering-spaced-repetition-protocol', moduleTitle: 'Mastering Spaced Repetition', insight: 'Retrieval practice and spacing are complementary approaches with good evidence for improving durable learning.' },
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
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'Regular, distributed study is generally more reliable than leaving most work to one late block. Plan backwards from the assessment.' },
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
    text: "Your boss asks you to cover Thursday night. You need the income, but it overlaps with your usual study block. There may not be a cost-free option.",
    choices: [
      {
        text: "Take the needed shift and move one priority study block to a realistic time.",
        effects: { systemSavvy: 5, energy: -5 },
        nextSceneId: 'JOB_CONSEQUENCES',
        moduleLink: { moduleId: 'linking-study-future-goals-protocol', moduleTitle: 'Linking Study to Future Goals', insight: 'Paid work can be necessary. Protecting one realistic study commitment helps you plan around the constraint without blaming yourself for it.' },
      },
      {
        text: "Decline the shift if that is financially manageable this week.",
        effects: { resilience: 5, academicCap: 5, energy: -5 },
        nextSceneId: '__CHRISTMAS_CHECK__',
        moduleLink: { moduleId: 'best-possible-self-protocol', moduleTitle: 'Finding Your Best Possible Self', insight: 'Saying no to short-term temptation is easier when you have a vivid picture of your future self.' },
      },
      {
        text: "Ask whether the shift or your regular hours can be adjusted.",
        effects: { systemSavvy: 10, resilience: 10, energy: -5 },
        nextSceneId: 'FINANCIAL_STRATEGY',
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
    text: "The shift ran late and Friday feels harder. The income mattered, and the original study plan no longer fits. You need to adjust the week around what actually happened.",
    choices: [
      {
        text: "Review your hours and ask for a pattern that protects one reliable study block.",
        effects: { resilience: 10, systemSavvy: 5 },
        nextSceneId: '__CHRISTMAS_CHECK__',
        moduleLink: { moduleId: 'reframing-progress-protocol', moduleTitle: 'Reframing Progress', insight: 'Progress isn\'t linear. What matters is recognising the pattern and adjusting your system.' },
      },
      {
        text: "Keep the shifts you need and ask a teacher to help prioritise the work you can realistically complete.",
        effects: { socialSupport: 5, systemSavvy: 10, energy: -5 },
        nextSceneId: '__CHRISTMAS_CHECK__',
        moduleLink: { moduleId: 'strategic-advantage-protocol', moduleTitle: 'Your Strategic Advantage', insight: 'Financial pressure is a real constraint, not a character flaw. Prioritisation and support can make a limited schedule more workable.' },
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
        effects: { academicCap: -10, energy: -40, resilience: -15 },
        nextSceneId: '__MOCK_RESULTS_CHECK__',
        moduleLink: { moduleId: 'cognitive-endurance-protocol', moduleTitle: 'Cognitive Endurance', insight: 'All-nighters can impair attention, memory and next-day performance. Extra hours awake do not guarantee extra learning.' },
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
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'In an exam, budgeting time for familiar questions before harder ones can protect accessible marks, while still following the paper instructions.' },
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
    text: "You have hit a wall after the Mocks: exhausted, struggling to focus and unsure how much more you can manage. This is a signal to involve support rather than diagnose yourself or simply add more hours.",
    choices: [
      {
        text: "Tell a trusted adult or teacher, reduce the immediate load and make a realistic recovery plan.",
        effects: {},
        scoreless: true,
        nextSceneId: 'POST_BURNOUT',
        moduleLink: { moduleId: 'grammar-of-grit-protocol', moduleTitle: 'The Grammar of Grit', insight: 'Persistent exhaustion deserves support. Rest and workload changes may help, and ongoing or severe symptoms should be discussed with an appropriate health professional.' },
      },
      {
        text: "The symptoms feel severe or unfamiliar — ask an adult to help you decide whether medical support is needed now.",
        effects: {},
        scoreless: true,
        nextSceneId: 'ACUTE_EXHAUSTION',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Severe or unfamiliar symptoms should not be self-diagnosed or managed alone. A trusted adult can help assess the next step.' },
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
    text: "After very little sleep, you feel unwell at school and cannot focus on the question. The teacher asks if you are okay.",
    choices: [
      {
        text: "Tell the teacher you are unwell, pause, and use a slow breathing technique if it feels comfortable.",
        effects: {},
        scoreless: true,
        nextSceneId: 'POST_BURNOUT',
        moduleLink: { moduleId: 'exam-crisis-management-protocol', moduleTitle: 'Exam Crisis Management', insight: 'A brief structured breathing practice may reduce arousal for some people. It does not replace telling an adult when you are unwell.' },
      },
      {
        text: "Ask to contact a parent, guardian or another responsible adult, especially if the symptoms are severe or unfamiliar.",
        effects: {},
        scoreless: true,
        nextSceneId: 'POST_BURNOUT',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'It is appropriate to seek adult or medical help when symptoms feel severe, unfamiliar or unsafe.' },
      },
    ],
  },

  'POST_BURNOUT': {
    id: 'POST_BURNOUT',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "After Hitting the Wall",
    mood: 'reflection',
    location: 'home',
    text: "The period of exhaustion showed that the current workload was not sustainable. Your study approach needs a rethink, alongside support if the symptoms continue.",
    choices: [
      {
        text: "Make a manageable recovery plan: age-appropriate sleep, fewer late-night cues and regular movement.",
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
    text: "The CAO deadline is approaching. You can list up to ten Level 8 courses and up to ten Level 7/6 courses. The two lists are processed separately, so each should reflect your genuine order of preference — after you check entry requirements.",
    textVariants: [
      {
        condition: { stat: 'systemSavvy', max: 45 },
        text: "The CAO form feels confusing. Before submitting, you need to separate the Level 8 and Level 7/6 lists, check course requirements and rank each list by what you would genuinely prefer — not by last year's points.",
      },
    ],
    choices: [
      {
        text: "Rank both lists by genuine preference and verify every course requirement.",
        effects: { systemSavvy: 15, resilience: 5 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'CAO advises applicants to list courses in genuine order of preference. Points are not a forecast, and the Level 8 and Level 7/6 lists are processed separately.' },
      },
      {
        text: "Order courses by last year's points because the highest-points course must be best.",
        effects: { systemSavvy: -10 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'best-possible-self-protocol', moduleTitle: 'Finding Your Best Possible Self', insight: 'Previous points reflect past demand and available places; they do not tell you which course best fits your goals or what points will be required this year.' },
      },
      {
        text: "If potentially eligible, finish the HEAR or DARE process and separately check grants and scholarships.",
        effects: { systemSavvy: 15, resilience: 5, energy: -5 },
        nextSceneId: 'SCHOLARSHIP_PATH',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'HEAR, DARE, grants and scholarships have different criteria and processes. Eligibility or an application does not guarantee an offer or funding.' },
      },
      {
        text: "Cross-check research with a friend, then make your own order independently.",
        effects: { socialSupport: 5, systemSavvy: 5 },
        nextSceneId: 'STUDY_PARTNER_CONFLICT',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'A friend can help you spot missing information, but each applicant should order courses around their own preferences and requirements.' },
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
        moduleLink: { moduleId: 'mastering-interleaving-protocol', moduleTitle: 'Mastering Interleaving', insight: 'Interleaving asks you to distinguish between problem types and choose a method, which can support flexible application.' },
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
        text: "Accept the help and bring one question from the last paper.",
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
        text: "Explore whether a level change is appropriate with the subject teacher and guidance counsellor.",
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
        nextSceneId: 'ASSESSMENT_DEADLINES',
        moduleLink: { moduleId: 'points-optimization-protocol', moduleTitle: 'Points Optimization', insight: 'A general plan is a starting point. Adapt it using syllabus coverage, deadlines, feedback and the time you actually have.' },
      },
      {
        text: "Adapt the plan to my own weak areas using a Retrospective Log.",
        effects: { systemSavvy: 10, resilience: 5, academicCap: 5 },
        nextSceneId: 'ASSESSMENT_DEADLINES',
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

  'ASSESSMENT_DEADLINES': {
    id: 'ASSESSMENT_DEADLINES',
    phase: 'Final Stretch',
    month: 'April',
    title: "The Deadlines Beyond the Written Papers",
    mood: 'opportunity',
    location: 'school',
    text: "Written exams dominate the conversation, but your subjects may also involve oral, practical, project or coursework requirements. The dates and rules differ, and one deadline is closer than you remembered.",
    choices: [
      {
        text: "Build one source-checked calendar and ask each subject teacher to confirm the next deliverable.",
        effects: { systemSavvy: 15, resilience: 5 },
        nextSceneId: '__ECHO_CHAIN__',
        moduleLink: { moduleId: 'reverse-engineering-protocol', moduleTitle: 'Reverse Engineering Your Schedule', insight: 'A complete plan includes every assessed component, its source and its next concrete action — not just the final written papers.' },
      },
      {
        text: "Focus only on written exams and assume the other requirements will sort themselves out.",
        effects: { academicCap: 5, systemSavvy: -10, energy: -5 },
        nextSceneId: '__ECHO_CHAIN__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Untracked practical, oral or coursework requirements can become urgent. Confirming dates early protects both time and options.' },
      },
      {
        text: "Tell a teacher or guidance counsellor where workload or support needs are colliding, then agree one next action.",
        effects: { socialSupport: 10, systemSavvy: 10, energy: 5 },
        nextSceneId: '__ECHO_CHAIN__',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Early, specific communication gives the school a better chance to clarify requirements and connect you with relevant support.' },
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
    text: "It is 3 AM and anxious thoughts are keeping you awake. Your heart is racing and it is hard to settle. You need a small next step, not a perfect solution in the middle of the night.",
    textVariants: [
      {
        condition: { stat: 'resilience', min: 65 },
        text: "You notice the anxiety without treating it as proof that you are unprepared. A familiar wind-down plan gives you something concrete to follow while the feeling passes.",
      },
      {
        condition: { stat: 'energy', max: 30 },
        text: "You are exhausted and still awake. More revision is no longer landing, so the priority is to reduce stimulation, seek support if needed and give yourself the best chance to rest.",
      },
    ],
    choices: [
      {
        text: "Write the worries down, note one time to review practical concerns tomorrow, then return to a quiet wind-down routine.",
        effects: { resilience: 15, energy: 5 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'Writing worries down and postponing problem-solving can help some people disengage from repetitive thinking. It is a coping tool, not a guaranteed fix.' },
      },
      {
        text: "Lie there spiralling. Eventually check your phone until 5 AM.",
        effects: { energy: -20, resilience: -10 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'digital-distraction-protocol', moduleTitle: 'Creating Barriers for Digital Distractions', insight: 'Late-night scrolling can extend wakefulness through stimulation, notifications and light exposure, leaving less time for sleep.' },
      },
      {
        text: "Use the simple wind-down routine you practised and keep expectations realistic.",
        effects: { resilience: 20, energy: 10 },
        nextSceneId: 'CRISIS_AVERTED',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'A familiar routine can reduce uncertainty and decision load. It cannot guarantee that anxiety disappears.' },
      },
      {
        text: "The pressure is tied to family expectations; plan a safer time and person for an honest conversation.",
        effects: {},
        scoreless: true,
        nextSceneId: 'FAMILY_PRESSURE',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'External pressure from family can be harder to manage than academic pressure because it carries emotional weight.' },
      },
      {
        text: "Wake or contact a trusted adult if the symptoms feel unsafe or unmanageable.",
        effects: {},
        scoreless: true,
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Severe, unfamiliar or persistent symptoms should not be managed alone. A trusted adult can help decide whether medical support is needed.' },
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
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Preparing an explanation can reveal gaps and strengthen understanding when you verify it against reliable material.' },
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
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'A structured study group can pool different strengths, provided everyone checks explanations and protects individual study needs.' },
      },
      {
        text: "The class is interrupted when another student appears to be in acute distress.",
        effects: {},
        scoreless: true,
        nextSceneId: 'GRACE_UNDER_PRESSURE',
        moduleLink: { moduleId: 'exam-crisis-management-protocol', moduleTitle: 'Exam Crisis Management', insight: 'A possible health crisis should be passed to the responsible adult immediately; students are not expected to diagnose or treat it.' },
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
        text: "Your phone buzzes with another notification. You have already noticed when distraction is most likely and can now choose a boundary that fits the actual problem.",
      },
    ],
    choices: [
      {
        text: "Set a planned phone-free block and place the phone outside the study space.",
        effects: { academicCap: 15, energy: 5, resilience: 5 },
        nextSceneId: '__COMEBACK_CHECK__',
        moduleLink: { moduleId: 'digital-distraction-protocol', moduleTitle: 'Creating Barriers for Digital Distractions', insight: 'A physical boundary reduces cues and makes the intended action easier. The useful barrier is one you can sustain.' },
      },
      {
        text: "Promise yourself you'll have more willpower next time. Keep the phone on the desk.",
        effects: { academicCap: -5, energy: -10, resilience: -5 },
        nextSceneId: '__COMEBACK_CHECK__',
        moduleLink: { moduleId: 'bimodal-brain-protocol', moduleTitle: 'Focused vs Diffuse Mode', insight: 'Keeping a high-salience distraction close by can make sustained attention harder. Changing the environment reduces that demand.' },
      },
      {
        text: "Set up Focus mode or app limits and tell someone when the block should end.",
        effects: { academicCap: 15, energy: 10, systemSavvy: 5 },
        nextSceneId: '__COMEBACK_CHECK__',
        moduleLink: { moduleId: 'digital-distraction-protocol', moduleTitle: 'Creating Barriers for Digital Distractions', insight: 'Technical limits work best when they are specific, time-bounded and paired with a clear study task.' },
      },
      {
        text: "Create and test a simple pre-exam routine for the morning.",
        effects: { resilience: 5 },
        nextSceneId: 'EXAM_EVE_RITUAL',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'A familiar, practical routine may reduce uncertainty and avoidable decision-making before an exam.' },
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
        text: "Your bag is packed and the practical details are handled. You do not need a last-minute reinvention; the remaining decision is how to protect rest and reduce avoidable uncertainty.",
      },
    ],
    choices: [
      {
        text: "Last-minute cramming session until 2 AM.",
        effects: { energy: -30, academicCap: -5 },
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Late cramming reduces the time available for sleep and may leave you less alert. A short review is different from studying deep into the night.' },
      },
      {
        text: "Do a brief review of key information, then protect an age-appropriate night's sleep.",
        effects: { energy: 20, resilience: 10 },
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
        moduleLink: { moduleId: 'exam-hall-strategies-protocol', moduleTitle: 'Exam Hall Strategies', insight: 'Sleep consolidates memories and restores prefrontal cortex function — the brain region you need most in an exam.' },
      },
      {
        text: "Use a prepared checklist — food, required materials, travel plan, wind-down and morning routine.",
        effects: { energy: 25, resilience: 15, academicCap: 5 },
        nextSceneId: 'ELITE_PROTOCOL',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'A practical checklist can prevent avoidable problems and reduce decision load. Some uncertainty will always remain.' },
      },
      {
        text: "Go for a walk to clear your head the night before.",
        effects: { energy: 5 },
        nextSceneId: 'WALKING_TO_EXAM',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Gentle movement or a short walk can help some people step away from repetitive thinking, if it is safe and practical.' },
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
    text: "You share the official HEAR information and one friend realises the criteria may be relevant to them. They still need to check eligibility and documentation with the guidance counsellor.",
    choices: [
      {
        text: "Help them list questions, then direct them to the guidance counsellor and official application guidance.",
        effects: { socialSupport: 20, systemSavvy: 10, energy: -10 },
        nextSceneId: 'MATHS_CLASS',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Useful peer support means sharing accurate sources and connecting someone with the staff responsible for application guidance.' },
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
    text: "Your boss agrees to adjusted hours. Your research also surfaces a financial support that may be relevant, but you still need to verify its criteria, deadlines and application process.",
    choices: [
      {
        text: "Check eligibility through the official source and apply if the support is relevant.",
        effects: { systemSavvy: 15, academicCap: 10, energy: 5 },
        nextSceneId: '__CHRISTMAS_CHECK__',
        moduleLink: { moduleId: 'strategic-advantage-protocol', moduleTitle: 'Your Strategic Advantage', insight: 'Financial supports have specific criteria and are not guaranteed. Accurate information can still help you plan work, study and costs more realistically.' },
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
    text: "On a practice paper, the time-allocation strategy helps you complete more accessible questions before returning to harder ones. The paper still shows content gaps, but the timing evidence is useful.",
    choices: [
      {
        text: "Review the paper and refine the timing plan for the next practice attempt.",
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
    text: "You find a scholarship whose criteria may fit and confirm the deadline and evidence required. It is a separate application with no guaranteed outcome, so it needs to fit alongside your existing workload.",
    choices: [
      {
        text: "Prepare the application carefully and set a firm time limit so core study does not disappear.",
        effects: { systemSavvy: 15, resilience: 10, energy: -15 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'best-possible-self-protocol', moduleTitle: 'Finding Your Best Possible Self', insight: 'Scholarship criteria and selection processes vary. Use the provider\'s current guidance and support every claim with accurate evidence.' },
      },
      {
        text: "Decide not to apply after weighing the deadline against your current capacity.",
        effects: { academicCap: 10, energy: 5 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Not every relevant opportunity is worth pursuing at once. A deliberate no can protect higher-priority work.' },
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
    text: "The routine does not erase the anxiety, but it gives the night some structure. You write down the practical concerns, reduce stimulation and get some rest before morning.",
    choices: [
      {
        text: "Share your anxiety management routine with a struggling friend.",
        effects: { socialSupport: 15, resilience: 5 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'Sharing a coping strategy can prompt reflection, but each person may need different support and professional advice.' },
      },
      {
        text: "Channel the calm into a productive morning study session.",
        effects: { academicCap: 10, energy: 5 },
        nextSceneId: 'PEER_SUPPORT',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'After a difficult night, keep the morning plan modest and focus on controllable practical steps.' },
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
        nextSceneId: 'TEACHING_LEGACY',
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Creating a shared resource requires selection and synthesis; the group should also check it against the syllabus and reliable sources.' },
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
    title: "The Options Checklist",
    mood: 'triumph',
    location: 'online',
    text: "You have checked the relevant deadlines, course requirements and application steps using official sources. The plan is documented, and you know which questions still need guidance rather than guesswork.",
    choices: [
      {
        text: "Turn the process into a source-linked checklist a younger student can adapt next year.",
        effects: { socialSupport: 15, systemSavvy: 10, energy: -5 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'A useful checklist includes dates, source links and a reminder that criteria can change from year to year.' },
      },
      {
        text: "Close the planning loop and focus on the next exam task, without expecting perfect execution.",
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
        nextSceneId: 'DIGITAL_DISTRACTION',
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'Creating teaching material can deepen understanding, but accuracy checks and workload boundaries still matter.' },
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
    title: "The Prepared Morning",
    mood: 'exam',
    location: 'exam-hall',
    text: "Exam morning. The practical checklist reduces avoidable decisions: food you know you can manage, required materials, travel time and a brief review. You still feel nervous, but you are not searching for missing essentials.",
    choices: [
      {
        text: "Read the instructions, budget the time and begin with the plan you practised.",
        effects: { academicCap: 15, resilience: 10, energy: 5 },
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
        moduleLink: { moduleId: 'exam-hall-strategies-protocol', moduleTitle: 'Exam Hall Strategies', insight: 'Exam-day confidence comes from preparation, not hope. You\'ve earned this.' },
      },
      {
        text: "Give a quiet nod of encouragement to a nervous classmate at the door.",
        effects: { socialSupport: 10, resilience: 15, energy: 5 },
        nextSceneId: '__NIGHT_BEFORE_CHECK__',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'A small acknowledgement can support connection without making you responsible for another student’s emotions.' },
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
    text: "You recognise an earlier pattern that was not working and choose a smaller, more deliberate response. The useful change is not a dramatic transformation; it is noticing the pattern sooner and acting differently.",
    choices: [
      {
        text: "Prioritise a small set of high-value gaps and protect the remaining recovery time.",
        effects: { academicCap: 20, resilience: 10, energy: -15 },
        nextSceneId: 'GAME_DAY_PREP',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Late-stage prioritisation should use syllabus coverage, teacher feedback, prerequisites and recent evidence — not guesses about guaranteed marks.' },
      },
      {
        text: "Steady the ship. Consistent effort across all subjects, no heroics.",
        effects: { academicCap: 10, resilience: 15, energy: -5 },
        nextSceneId: 'GAME_DAY_PREP',
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
        moduleLink: { moduleId: 'illusion-of-competence-protocol', moduleTitle: 'Overcoming Illusions of Competence', insight: 'Familiarity can be mistaken for recall. Use a closed-book check to find out what you can retrieve, then review the gaps.' },
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
    title: "The Social Plan",
    mood: 'social',
    location: 'social',
    text: "A friend's celebration overlaps with a planned study session. Connection matters and so do sleep and preparation; the decision is about making the trade-off explicit.",
    choices: [
      {
        text: "Go for one hour, arrange the journey home and move the priority study task.",
        effects: { socialSupport: 10, energy: -5, systemSavvy: 5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'Setting time boundaries on social events protects study time without sacrificing connection.' },
      },
      {
        text: "Decline this time, explain briefly and use the evening for the planned work and rest.",
        effects: { academicCap: 10, energy: 5, resilience: 5 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'grammar-of-grit-protocol', moduleTitle: 'The Grammar of Grit', insight: 'A deliberate no can protect a prior commitment without implying that social time is unimportant.' },
      },
      {
        text: "Go without deciding when or how you will get home, and lose most of the night's sleep.",
        effects: { socialSupport: 5, energy: -20, academicCap: -10 },
        nextSceneId: 'PART_TIME_JOB',
        moduleLink: { moduleId: 'linking-study-future-goals-protocol', moduleTitle: 'Linking Study to Future Goals', insight: 'The problem is not attending a celebration; it is leaving sleep, transport and the next commitment unplanned.' },
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
    text: "Your teacher welcomes the question and compares a marking scheme with sample answers. She points out command words, required evidence and where marks were awarded — while warning that memorising isolated keywords is not the same as answering the question.",
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
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'It can be difficult to speak openly at a first appointment. Naming even one concrete concern gives the counsellor more useful information.' },
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
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'A break can support recovery from accumulated fatigue. The right balance of rest and study depends on your health, workload and upcoming commitments.' },
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
    text: "The results come back better than expected. Your teacher identifies two subjects where specific feedback suggests a realistic grade improvement, while reminding you to protect course requirements and essential work elsewhere.",
    choices: [
      {
        text: "Prioritise the identified gaps while maintaining required work in every subject.",
        effects: { academicCap: 10, systemSavvy: 10 },
        nextSceneId: '__BURNOUT_CHECK__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Use marking feedback, course requirements and teacher judgement to compare realistic gains. No subject offers a guaranteed points-per-hour return.' },
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
        moduleLink: { moduleId: 'self-efficacy-protocol', moduleTitle: 'Self Efficacy', insight: 'Specific feedback can turn a disappointing result into an actionable next step, especially when you apply it and check again.' },
      },
    ],
  },

  'STUDY_PARTNER_CONFLICT': {
    id: 'STUDY_PARTNER_CONFLICT',
    phase: 'Pressure Cooker',
    month: 'February',
    title: "The Application Cross-check",
    mood: 'opportunity',
    location: 'school',
    text: "You and a friend compare CAO research. You notice that one course has a subject requirement your friend missed, while your own Level 7/6 list is nearly empty. Comparing notes is useful; copying each other's order would not be.",
    choices: [
      {
        text: "Check the official requirements, then rank each list by your own genuine preference.",
        effects: { socialSupport: 5, resilience: 5, systemSavvy: 15 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Cross-checking facts is collaborative; the final preference order remains personal to each applicant.' },
      },
      {
        text: "Add suitable Level 6/7, PLC or apprenticeship routes to your wider options plan.",
        effects: { socialSupport: 5, systemSavvy: 15, resilience: 10, energy: -5 },
        nextSceneId: '__ACADEMIC_CHECK__',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'A wider options plan can include CAO Level 8 and Level 7/6 choices alongside PLC and apprenticeship routes. Check each route directly.' },
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
    title: "The Subject Level Decision",
    mood: 'opportunity',
    location: 'school',
    text: "You are considering changing level in one subject. It could make the workload more manageable, but the points calculation, course prerequisites and subject-specific implications all need checking before you decide.",
    choices: [
      {
        text: "Review the decision with the subject teacher and guidance counsellor, then check every target course requirement.",
        effects: { systemSavvy: 15, academicCap: 10, resilience: 5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'A level change can affect workload, points and eligibility. Use current official requirements and subject-specific advice before deciding.' },
      },
      {
        text: "Stay at the current level for now, with a review date and a targeted support plan.",
        effects: { resilience: 10, academicCap: 5, socialSupport: 5, energy: -5 },
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'grammar-of-grit-protocol', moduleTitle: 'The Grammar of Grit', insight: 'A time-limited trial with clear evidence is more useful than framing the decision as pride versus giving up.' },
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
    text: "A friend messages late at night saying they are not coping. This is not something you should assess or carry alone. The priorities are immediate safety, involving a trusted adult and connecting them with appropriate help.",
    choices: [
      {
        text: "Ask directly whether they are in immediate danger. If they are, call 112/999; involve a trusted adult and stay connected while help is arranged.",
        effects: {},
        scoreless: true,
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Take statements about immediate safety seriously. Emergency services are the right option when there is imminent danger.' },
      },
      {
        text: "Phone a trusted adult now and ask them to take over the next steps while you stay in contact with your friend.",
        effects: {},
        scoreless: true,
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'A student can listen and stay present, but a trusted adult should share responsibility for deciding what help is needed.' },
      },
      {
        text: "If there is no immediate danger, help them contact a parent, guardian, GP or out-of-hours service and arrange school support; do not promise secrecy.",
        effects: {},
        scoreless: true,
        nextSceneId: 'FINAL_STRETCH_START',
        moduleLink: { moduleId: 'reframing-catastrophic-thoughts-protocol', moduleTitle: 'Reframing Catastrophic Thoughts', insight: 'When someone may be at risk, privacy has limits. Involving appropriate adults is care, not betrayal.' },
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
        nextSceneId: 'ASSESSMENT_DEADLINES',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Simulating exam conditions in practice reduces the novelty penalty on the real day.' },
      },
      {
        text: "Use it as a diagnostic — check answers as you go",
        effects: { academicCap: 10, systemSavvy: 10, energy: -5 },
        nextSceneId: 'ASSESSMENT_DEADLINES',
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
    text: "You draft a simple morning routine: wake time, familiar food, required materials, travel plan and a brief settling exercise before the exam hall.",
    choices: [
      {
        text: "Test-run it before a practice paper",
        effects: { resilience: 15, energy: 10, academicCap: 5 },
        nextSceneId: '__COMEBACK_CHECK__',
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'Rehearsing your exam-day routine removes uncertainty and frees cognitive resources for the actual exam.' },
      },
      {
        text: "Write it down but wing it on the day",
        effects: { resilience: 5, systemSavvy: 5 },
        nextSceneId: '__COMEBACK_CHECK__',
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
    text: "During a class test, the student beside you appears to be in acute distress and is breathing rapidly. You are not expected to diagnose what is happening. The teacher has not noticed yet.",
    choices: [
      {
        text: "Alert the teacher immediately and follow their instructions.",
        effects: {},
        scoreless: true,
        nextSceneId: 'DIGITAL_DISTRACTION',
        moduleLink: { moduleId: 'exam-crisis-management-protocol', moduleTitle: 'Exam Crisis Management', insight: 'An adult should assess and manage an acute health situation. Alerting the teacher is the appropriate first action.' },
      },
      {
        text: "Once the teacher is helping, give the student space and calmly continue only when instructed.",
        effects: {},
        scoreless: true,
        nextSceneId: 'DIGITAL_DISTRACTION',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'Support can mean making space and letting the responsible adult lead, rather than trying to treat the situation yourself.' },
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
        moduleLink: { moduleId: 'game-day-protocol', moduleTitle: "Game Day: The Athlete's Protocol", insight: 'The night before offers limited time for useful new learning. Protecting sleep and reducing avoidable stress may be more valuable than extended cramming.' },
      },
      {
        text: "One final look at your summary sheet, then sleep",
        effects: { academicCap: 5, energy: 5 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'mastering-spaced-repetition-protocol', moduleTitle: 'Mastering Spaced Repetition', insight: 'Keep any final review brief and familiar. Spacing is built across repeated sessions, not created by one review immediately before sleep.' },
      },
      {
        text: "Call your study partner — you promised you'd check in",
        effects: { socialSupport: 10, resilience: 10, energy: 5 },
        nextSceneId: '__END_ROUTE__',
        moduleLink: { moduleId: 'emotional-intelligence-protocol', moduleTitle: 'Building Emotional Intelligence', insight: 'A brief check-in can increase a sense of connection before a high-pressure event, but it is not a substitute for sleep or professional support.' },
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
        moduleLink: { moduleId: 'controllable-variables-protocol', moduleTitle: 'Using Controllable Variables to Grow', insight: 'A short walk can help some people disengage from rumination. Choose a safe, familiar route and do not treat it as a guaranteed anxiety treatment.' },
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
        moduleLink: { moduleId: 'elaborative-interrogation-protocol', moduleTitle: 'Elaborative Interrogation', insight: 'A continuing study group can share explanations and planning work, while each student still needs targeted individual practice.' },
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
        moduleLink: { moduleId: 'mastering-active-recall-protocol', moduleTitle: 'Mastering Active Recall', insight: 'Recognising an unhelpful study habit in the moment gives you a chance to switch to a more useful action.' },
      },
      {
        text: "Share your story with a classmate who's struggling now",
        effects: { socialSupport: 15, resilience: 10, energy: -5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'growth-mindset-protocol', moduleTitle: 'The Growth Protocol', insight: 'If you choose to share an experience, focus on the practical change that helped and keep personal boundaries that feel safe.' },
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
    text: "A younger student approaches you in the corridor. Their sister heard about HEAR through your friend group and completed the relevant application steps before the deadline. No outcome is known, but the information reached someone who needed it.",
    choices: [
      {
        text: "Offer to help more students with applications next year",
        effects: { socialSupport: 10, systemSavvy: 10, resilience: 5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'leaving-cert-strategy-protocol', moduleTitle: 'The Leaving Cert Points Protocol', insight: 'Sharing current official information can widen awareness, while trained staff and scheme administrators remain the right sources for individual guidance.' },
      },
      {
        text: "Smile and focus on your own exams",
        effects: { resilience: 5, energy: 5 },
        nextSceneId: 'EXAM_ANXIETY',
        moduleLink: { moduleId: 'strategic-advantage-protocol', moduleTitle: 'Your Strategic Advantage', insight: 'Sometimes the best thing you can do is focus on yourself. Your success story will inspire others on its own.' },
      },
    ],
  },

  // ═══ REFLECTIVE PROFILES (11 total) ═══════════════════════════════════════

  'END_PATHFINDER': {
    id: 'END_PATHFINDER',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Adaptive Pathfinder",
    mood: 'triumph',
    location: 'home',
    text: "Across this simulation, you most often responded to pressure by adapting and using connection. That is a decision pattern to build on, not a prediction of grades, offers or future wellbeing.",
  },
  'END_EXPERT': {
    id: 'END_EXPERT',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Methodical Learner",
    mood: 'triumph',
    location: 'home',
    text: "Your clearest pattern was improving how you learned: retrieval, feedback and deliberate practice appeared repeatedly in your choices. The profile reflects simulated decisions, not measured academic attainment.",
  },
  'END_MENTOR': {
    id: 'END_MENTOR',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Knowledge Connector",
    mood: 'triumph',
    location: 'social',
    text: "You repeatedly connected useful information with other people while checking practical processes. Keep the collaboration, and keep verifying changing rules through official sources.",
  },
  'END_GOOD': {
    id: 'END_GOOD',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Deliberate Builder",
    mood: 'triumph',
    location: 'home',
    text: "Your route shows steady, workable decisions across several areas rather than one dramatic strength. It is a snapshot of judgement in the simulation, not an admissions outcome.",
  },
  'END_REGROUPING': {
    id: 'END_REGROUPING',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Reflective Recalibrator",
    mood: 'reflection',
    location: 'home',
    text: "Some choices left important systems underdeveloped, while others showed that you could notice and adjust. The next useful move is one smaller repeatable plan with the right support around it.",
  },
  'END_PLC': {
    id: 'END_PLC',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Route Explorer",
    mood: 'reflection',
    location: 'home',
    text: "You actively considered Level 6/7, PLC or apprenticeship routes alongside other options. Exploring more than one route widens the plan; it does not guarantee eligibility, a place or later progression.",
  },
  'END_REPEAT': {
    id: 'END_REPEAT',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Reset Builder",
    mood: 'reflection',
    location: 'home',
    text: "This route ended with low evidence across several capabilities and a depleted energy reserve. That is a prompt to rebuild support and structure, not a statement about ability or a recommendation to repeat a year.",
  },

  'END_SCHOLARSHIP': {
    id: 'END_SCHOLARSHIP',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Opportunity Navigator",
    mood: 'triumph',
    location: 'online',
    text: "You checked an additional opportunity and made space for its application requirements. That shows option-building; it does not imply eligibility, selection, funding or a course offer.",
  },

  'END_LEADER': {
    id: 'END_LEADER',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Collaborative Leader",
    mood: 'triumph',
    location: 'social',
    text: "Your route contains repeated evidence of organising learning with other people. The strongest version of that pattern combines contribution with boundaries, so helping others does not require carrying everything.",
  },

  'END_COMEBACK': {
    id: 'END_COMEBACK',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Recovery Builder",
    mood: 'triumph',
    location: 'home',
    text: "You revisited an earlier unhelpful pattern and chose a different response. The meaningful evidence is recognition and adjustment, not a claim that every setback has been resolved.",
  },

  'END_BALANCED': {
    id: 'END_BALANCED',
    phase: 'Final Stretch',
    month: 'August',
    title: "The Balanced Learner",
    mood: 'triumph',
    location: 'home',
    text: "Your route produced similar evidence across learning, support, planning and recovery. The balance belongs to these simulated choices and should be treated as a prompt for reflection, not a fixed student type.",
  },
};
