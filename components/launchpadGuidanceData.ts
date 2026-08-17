/**
 * Plain-language guidance for the Launchpad. Product names stay intact, but
 * every explanation starts from the situation a student recognises.
 */

export interface ToolGuidance {
  bestWhen: string;
  useWhen: string;
  whatItDoes: string;
  outcome: string;
}

export const TOOL_GUIDANCE: Record<string, ToolGuidance> = {
  journey: {
    bestWhen: 'you want to think through the choices ahead',
    useWhen: 'You are wondering how the decisions you make during the school year could affect where you finish.',
    whatItDoes: 'Puts you inside realistic school-year situations and lets you explore the consequences of different choices.',
    outcome: 'A clearer picture of your habits, pressure points and one useful module to work on next.',
  },
  planner: {
    bestWhen: 'you need a realistic plan for the week',
    useWhen: 'You know you need to study, but fitting every subject into the week feels messy.',
    whatItDoes: 'Builds focused study blocks around your subjects, targets, available time and rest days.',
    outcome: 'A balanced weekly timetable with a specific subject assigned to each session.',
  },
  'war-room': {
    bestWhen: 'you do not know what deserves attention first',
    useWhen: 'You have time to study but are unsure which subject or topic needs attention, or you want to check syllabus coverage.',
    whatItDoes: 'Combines your cohort-specific syllabus map, confidence, targets, results and weekly plan in one workspace.',
    outcome: 'One clear priority plus a trustworthy view of what is not started, shaky or solid.',
  },
  comeback: {
    bestWhen: 'a difficult week has knocked you off track',
    useWhen: 'Work has piled up, your routine has slipped or trying to fix everything at once feels impossible.',
    whatItDoes: 'Turns your current study pattern into a small, realistic seven-day recovery plan.',
    outcome: 'A manageable route back into study without pretending you can catch up all at once.',
  },
  'future-finder': {
    bestWhen: 'you are unsure which senior-cycle subjects might suit you',
    useWhen: 'You want help connecting your interests with subjects you could enjoy in senior cycle.',
    whatItDoes: 'Uses your interests to surface subject areas worth investigating further.',
    outcome: 'A shortlist of subjects to explore and better questions to ask before choosing.',
  },
  'future-finder-revamped': {
    bestWhen: 'you have no idea which courses or careers might suit you',
    useWhen: 'You want possible directions based on your interests, without being told there is only one right answer.',
    whatItDoes: 'Connects your interests with real CAO courses and related career possibilities.',
    outcome: 'A ranked set of possibilities worth researching, with points kept visible and honest.',
  },
  'points-passport': {
    bestWhen: 'you want to understand your points and possible grade gains',
    useWhen: 'You want to know where your results currently place you and which improvements could move your total.',
    whatItDoes: 'Tracks mock results, calculates points and lets you test realistic grade scenarios.',
    outcome: 'A clear view of your current points, target and the grade changes worth exploring.',
  },
  'college-compass': {
    bestWhen: 'you need to keep college routes and deadlines in order',
    useWhen: 'CAO, HEAR, DARE, scholarships and application dates are beginning to feel like too much to track.',
    whatItDoes: 'Places the major college-access steps in a clear sequence for your year group.',
    outcome: 'A practical roadmap of what matters now, what comes later and what to verify officially.',
  },
  'catch-up-lane': {
    bestWhen: 'you missed a class or need one topic explained quickly',
    useWhen: 'You were absent, lost track during a topic or need a clean way back into the lesson.',
    whatItDoes: 'Breaks a missed topic into a short explanation and focused catch-up activity.',
    outcome: 'Enough understanding to rejoin the class without restarting the entire subject.',
  },
  'mark-bank': {
    bestWhen: 'you want repeated practice with real exam questions',
    useWhen: 'You want to answer exam questions, see exactly how marks are awarded and revisit weak areas later.',
    whatItDoes: 'Marks real exam practice point by point and brings questions back before you forget them.',
    outcome: 'A marked attempt, a record of what cost marks and a smarter revision queue.',
  },
  'paper-trail': {
    bestWhen: 'you need a real past paper or marking scheme',
    useWhen: 'You are ready to practise a specific subject, paper or exam year.',
    whatItDoes: 'Keeps SEC past papers beside their official marking schemes and maps answers to questions.',
    outcome: 'The right paper, the right question and the official evidence needed to review your answer.',
  },
  'command-word-reflex': {
    bestWhen: 'you misread what exam questions are asking',
    useWhen: 'Words such as explain, evaluate or compare keep costing you marks.',
    whatItDoes: 'Uses real questions to train you to spot command words and avoid their common traps.',
    outcome: 'Faster recognition of what a question expects before you begin writing.',
  },
  'how-they-did-it': {
    bestWhen: 'you need proof that progress is possible from where you are',
    useWhen: 'Advice feels abstract and you would rather see how real people handled difficult starting points.',
    whatItDoes: 'Shows honest stories from people who faced barriers and the practical moves they made.',
    outcome: 'A realistic example and one move you can adapt to your own situation.',
  },
  'your-possible-life': {
    bestWhen: 'you want to understand what a career is actually like',
    useWhen: 'A course or career sounds interesting, but you cannot picture the ordinary working day or route into it.',
    whatItDoes: 'Lets you explore real work, pay, routes and trade-offs before treating an idea as a decision.',
    outcome: 'A possibility worth testing and a practical next question or action.',
  },
};

export type RecommendationGoalId = 'priority' | 'catch-up' | 'exam' | 'points' | 'future' | 'plan';

export interface RecommendationOption {
  id: string;
  label: string;
  candidates: string[];
}

export interface RecommendationGoal {
  id: RecommendationGoalId;
  label: string;
  question: string;
  options: RecommendationOption[];
}

export const RECOMMENDATION_GOALS: RecommendationGoal[] = [
  {
    id: 'priority',
    label: 'I don’t know what to study',
    question: 'What kind of answer would help most?',
    options: [
      { id: 'today', label: 'Give me one priority for today', candidates: ['war-room', 'planner'] },
      { id: 'week', label: 'Build me a plan for the whole week', candidates: ['planner'] },
      { id: 'marks', label: 'Show me my syllabus gaps', candidates: ['war-room', 'paper-trail'] },
    ],
  },
  {
    id: 'catch-up',
    label: 'I’ve fallen behind',
    question: 'Which situation is closest to yours?',
    options: [
      { id: 'topic', label: 'I missed one class or topic', candidates: ['catch-up-lane'] },
      { id: 'several', label: 'Several subjects need attention', candidates: ['war-room', 'comeback', 'planner'] },
      { id: 'restart', label: 'I need a realistic restart after a bad week', candidates: ['comeback', 'planner'] },
    ],
  },
  {
    id: 'exam',
    label: 'I want to practise for an exam',
    question: 'What would be most useful right now?',
    options: [
      { id: 'paper', label: 'Find a real past-paper question', candidates: ['paper-trail'] },
      { id: 'marking', label: 'Learn where marks are won and lost', candidates: ['mark-bank', 'paper-trail'] },
      { id: 'access', label: 'Make a difficult question easier to enter', candidates: ['mark-bank', 'paper-trail'] },
      { id: 'repeat', label: 'Practice and revisit my weak questions', candidates: ['mark-bank', 'paper-trail'] },
      { id: 'wording', label: 'Stop misreading command words', candidates: ['command-word-reflex'] },
    ],
  },
  {
    id: 'points',
    label: 'I want to improve my grades or points',
    question: 'What are you trying to work out?',
    options: [
      { id: 'position', label: 'Where my points stand now', candidates: ['points-passport'] },
      { id: 'gain', label: 'Which grade improvement could help most', candidates: ['points-passport', 'war-room'] },
      { id: 'attention', label: 'Which subject deserves more attention', candidates: ['war-room', 'planner'] },
    ],
  },
  {
    id: 'future',
    label: 'I’m thinking about courses or careers',
    question: 'Where are you in the process?',
    options: [
      { id: 'unknown', label: 'I have no idea what might suit me', candidates: ['future-finder-revamped', 'future-finder', 'how-they-did-it'] },
      { id: 'reality', label: 'I want to understand a career properly', candidates: ['your-possible-life', 'how-they-did-it'] },
      { id: 'deadlines', label: 'I need the route and important deadlines', candidates: ['college-compass', 'points-passport'] },
      { id: 'stories', label: 'I want to see how other people found a way forward', candidates: ['how-they-did-it'] },
    ],
  },
  {
    id: 'plan',
    label: 'I need to plan what comes next',
    question: 'How far ahead are you trying to see?',
    options: [
      { id: 'week', label: 'Just organise this study week', candidates: ['planner'] },
      { id: 'year', label: 'Understand the college timeline ahead', candidates: ['college-compass', 'planner'] },
      { id: 'choices', label: 'Think through the choices in my school year', candidates: ['journey', 'planner'] },
    ],
  },
];

export interface ToolRecommendation {
  toolId: string;
  goalId: RecommendationGoalId;
  answerId: string;
  goalLabel: string;
  answerLabel: string;
}

export function availableRecommendationGoals(availableToolIds: Iterable<string>): RecommendationGoal[] {
  const available = new Set(availableToolIds);
  return RECOMMENDATION_GOALS
    .map(goal => ({
      ...goal,
      options: goal.options.filter(option => option.candidates.some(id => available.has(id))),
    }))
    .filter(goal => goal.options.length > 0);
}

export function recommendTool(
  goalId: RecommendationGoalId,
  answerId: string,
  availableToolIds: Iterable<string>,
): ToolRecommendation | null {
  const available = new Set(availableToolIds);
  const goal = RECOMMENDATION_GOALS.find(item => item.id === goalId);
  const answer = goal?.options.find(item => item.id === answerId);
  if (!goal || !answer) return null;
  const toolId = answer.candidates.find(id => available.has(id));
  if (!toolId) return null;
  return {
    toolId,
    goalId,
    answerId,
    goalLabel: goal.label,
    answerLabel: answer.label,
  };
}
