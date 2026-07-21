/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Accreditation catalog — one entry per accredited module: what it is, why it
 * benefits students (both grounded in the module's compliance/evidence dossier
 * and fact-checked against it), and the SAME ordered reference list its inline
 * <Cite/> markers number against. Rendered by components/AccreditationPage.tsx.
 */

import { type Reference } from './references/types';
import { AFFIRMING_VALUES_REFERENCE_LIST } from './references/affirmingValues';
import { AGENCY_ARCHITECTURE_REFERENCE_LIST } from './references/agencyArchitecture';
import { AGENCY_PROTOCOL_REFERENCE_LIST } from './references/agencyProtocol';
import { ANSWER_ENGINEERING_REFERENCE_LIST } from './references/answerEngineering';
import { BEST_POSSIBLE_SELF_REFERENCE_LIST } from './references/bestPossibleSelf';
import { BIMODAL_BRAIN_REFERENCE_LIST } from './references/bimodalBrain';
import { CATASTROPHIC_THINKING_REFERENCE_LIST } from './references/catastrophicThinking';
import { COGNITIVE_ENDURANCE_REFERENCE_LIST } from './references/cognitiveEndurance';
import { CONTROLLABLE_VARIABLES_REFERENCE_LIST } from './references/controllableVariables';
import { DIGITAL_DISTRACTION_REFERENCE_LIST } from './references/digitalDistraction';
import { EFFECTIVE_STRUGGLE_REFERENCE_LIST } from './references/effectiveStruggle';
import { ELABORATIVE_INTERROGATION_REFERENCE_LIST } from './references/elaborativeInterrogation';
import { EMOTIONAL_INTELLIGENCE_REFERENCE_LIST } from './references/emotionalIntelligence';
import { EXAM_CRISIS_MANAGEMENT_REFERENCE_LIST } from './references/examCrisisManagement';
import { EXAM_HALL_STRATEGIES_REFERENCE_LIST } from './references/examHallStrategies';
import { GAME_DAY_REFERENCE_LIST } from './references/gameDay';
import { GROWTH_MINDSET_REFERENCE_LIST } from './references/growthMindset';
import { HOPE_PROTOCOL_REFERENCE_LIST } from './references/hopeProtocol';
import { ILLUSION_OF_COMPETENCE_REFERENCE_LIST } from './references/illusionOfCompetence';
import { LEAVING_CERT_STRATEGY_REFERENCE_LIST } from './references/leavingCertStrategy';
import { LINKING_STUDY_FUTURE_GOALS_REFERENCE_LIST } from './references/linkingStudyFutureGoals';
import { MARKING_SCHEME_DECODER_REFERENCE_LIST } from './references/markingSchemeDecoder';
import { ACTIVE_RECALL_REFERENCE_LIST } from './references/activeRecall';
import { INTERLEAVING_REFERENCE_LIST } from './references/interleaving';
import { SPACED_REPETITION_REFERENCE_LIST } from './references/spacedRepetition';
import { MENTAL_MODELLING_REFERENCE_LIST } from './references/mentalModelling';
import { NEUROPLASTICITY_REFERENCE_LIST } from './references/neuroplasticity';
import { POINTS_OPTIMIZATION_REFERENCE_LIST } from './references/pointsOptimization';
import { PROCRASTINATION_REFERENCE_LIST } from './references/procrastination';
import { REFRAMING_PROGRESS_REFERENCE_LIST } from './references/reframingProgress';
import { REVERSE_ENGINEERING_REFERENCE_LIST } from './references/reverseEngineering';
import { SELF_EFFICACY_REFERENCE_LIST } from './references/selfEfficacy';
import { STRATEGIC_ADVANTAGE_REFERENCE_LIST } from './references/strategicAdvantage';
import { FEEDBACK_LOOPS_REFERENCE_LIST } from './references/feedbackLoops';
import { HOW_MEMORY_WORKS_REFERENCE_LIST } from './references/howMemoryWorks';
import { COGNITIVE_LOAD_REFERENCE_LIST } from './references/cognitiveLoad';
import { CONTEXT_EFFECT_REFERENCE_LIST } from './references/contextEffect';
import { GRAMMAR_OF_GRIT_REFERENCE_LIST } from './references/grammarOfGrit';
import { IMPLEMENTATION_PROTOCOL_REFERENCE_LIST } from './references/implementationProtocol';
import { LEARNING_RADAR_REFERENCE_LIST } from './references/learningRadar';
import { MYELIN_MANUAL_REFERENCE_LIST } from './references/myelinManual';
import { NOTE_TAKING_PARADOX_REFERENCE_LIST } from './references/noteTakingParadox';
import { POWER_OF_YET_REFERENCE_LIST } from './references/powerOfYet';
import { PRAISE_PROTOCOL_REFERENCE_LIST } from './references/praiseProtocol';
import { SCIENCE_OF_MISTAKES_REFERENCE_LIST } from './references/scienceOfMistakes';
import { TEACHING_EFFECT_REFERENCE_LIST } from './references/teachingEffect';
import { SUBJECT_MATHEMATICS_REFERENCE_LIST } from './references/subjectMathematics';
import { SUBJECT_BUSINESS_REFERENCE_LIST } from './references/subjectBusiness';

export interface AccreditedModuleEntry {
  /** Course id from courseData.ts. */
  id: string;
  /** One sentence: what the student does or learns in the module. */
  what: string;
  /** One-two sentences: what the verified evidence shows and what it gives the student. */
  why: string;
  /** Ordered list — identical numbering to the module's inline citations. */
  references: Reference[];
}

export const ACCREDITED_MODULES: AccreditedModuleEntry[] = [
  {
    id: 'affirming-values-protocol',
    what: 'You learn how fear of being judged drains working memory in exams, then write a short piece about the values that matter to you.',
    why: 'Students under pressure who wrote briefly about their own values saw their grades rise, with effects lasting around two years, strongest for those facing the most threat. It is a defence you can set up yourself in fifteen minutes.',
    references: AFFIRMING_VALUES_REFERENCE_LIST,
  },
  {
    id: 'agency-architecture-protocol',
    what: 'You sort what you can and cannot control, then practise rewriting the story you tell yourself after a setback so the cause becomes something changeable.',
    why: 'Students taught to trace setbacks to changeable causes improved their grades, while treating failure as permanent and personal is the pattern that leads people to give up. How you explain a bad result is a habit you can retrain.',
    references: AGENCY_ARCHITECTURE_REFERENCE_LIST,
  },
  {
    id: 'agency-protocol',
    what: 'You picture a concrete future self, connect this week\'s study to it, and plan how to steer your own schooling instead of riding along.',
    why: 'Students who tie daily work to a picture of their future self follow through more, and those who feel like the driver, not the pawn, tend to do better in school. Knowledge from your home and community is a genuine asset.',
    references: AGENCY_PROTOCOL_REFERENCE_LIST,
  },
  {
    id: 'answer-engineering-protocol',
    what: 'You learn the answer structures examiners can credit: PEEL paragraphs, step-by-step working, and reading the mark allocation to size your answer.',
    why: 'Examiners working under time pressure can only credit points they can find, and in maths and science most marks go to the working, not the final answer. Clear structure lets you collect marks for knowledge you already have.',
    references: ANSWER_ENGINEERING_REFERENCE_LIST,
  },
  {
    id: 'best-possible-self-protocol',
    what: 'You write a detailed picture of your best possible future, then turn it into a WOOP plan: wish, outcome, obstacle, and an if-then step.',
    why: 'Pleasant daydreaming on its own can drain the energy needed to act. Pairing the dream with the obstacle in your way is what generates the drive, and a simple if-then plan makes follow-through much more likely.',
    references: BEST_POSSIBLE_SELF_REFERENCE_LIST,
  },
  {
    id: 'bimodal-brain-protocol',
    what: 'You learn when to grind at a problem and when to step away, then practise pairing focused blocks with real breaks that let ideas connect.',
    why: 'Stepping away from a stuck problem genuinely helps: people solved more problems after a break that let their minds wander. Even dreading a hard task can register as real discomfort, which a tiny start defuses.',
    references: BIMODAL_BRAIN_REFERENCE_LIST,
  },
  {
    id: 'reframing-catastrophic-thoughts-protocol',
    what: 'You catch catastrophic exam thoughts and work through them with a thought record, the "and then what?" technique, graded exposure and stepping back from the thought.',
    why: 'Acute stress temporarily blocks memory retrieval, which is why your mind goes blank under pressure; you\'ve lost the password, not the file. Cognitive behavioural techniques like these are among the best-evidenced ways to loosen anxious thinking.',
    references: CATASTROPHIC_THINKING_REFERENCE_LIST,
  },
  {
    id: 'cognitive-endurance-protocol',
    what: 'You build focus that lasts across weeks of exams by protecting sleep, fuelling steadily, using a calming breath during tests and training your concentration span.',
    why: 'Stress accumulates as physical wear on the body across an exam season, and cutting sleep short sacrifices the late-night REM that supports problem-solving and steady emotions. A slow, extended exhale lowers your arousal when a test spikes it.',
    references: COGNITIVE_ENDURANCE_REFERENCE_LIST,
  },
  {
    id: 'controllable-variables-protocol',
    what: 'You learn how sleep, food and exercise change how your brain works, then build a daily checklist to keep the three in your favour.',
    why: 'Sleep is when your brain files what you studied into memory, and 17 hours awake impairs you about as much as being at the drink-driving limit. Exercise raises a growth factor linked to brain health, and short sleep drives up hunger and cravings.',
    references: CONTROLLABLE_VARIABLES_REFERENCE_LIST,
  },
  {
    id: 'digital-distraction-protocol',
    what: 'You add friction to your phone and laptop, move the phone out of sight, and write if-then plans that make focused study the default.',
    why: 'Just having your phone in sight drains mental capacity, even face-down and silent, and after an interruption it takes around 23 minutes to fully refocus. Simple if-then plans reliably turn an intention into something you actually do.',
    references: DIGITAL_DISTRACTION_REFERENCE_LIST,
  },
  {
    id: 'effective-struggle-protocol',
    what: 'You learn to aim study at the right level of difficulty, treating the effort of recall, not the ease of re-reading, as the sign it\'s working.',
    why: 'A week after studying, students who re-read remembered about 40 per cent, while those who tested themselves remembered about 61 per cent, even though re-reading felt easier. Effortful recall builds more durable learning, and low-stakes practice can ease test anxiety.',
    references: EFFECTIVE_STRUGGLE_REFERENCE_LIST,
  },
  {
    id: 'elaborative-interrogation-protocol',
    what: 'You practise asking "why is this true?" about facts you\'re studying, across science, humanities and the Irish oral, instead of repeating them until they stick.',
    why: 'Explaining why a fact is true, instead of just reading it, can come close to doubling how much you remember. The technique works best when you already have some background knowledge to reason from, and it takes real effort.',
    references: ELABORATIVE_INTERROGATION_REFERENCE_LIST,
  },
  {
    id: 'emotional-intelligence-protocol',
    what: 'You learn to read your body\'s stress signals and practise ways to settle them: reframing nerves as excitement, reworking anxious thoughts, and slowing the breath.',
    why: 'Sustained stress can take the brain\'s thinking centre offline, which is why minds go blank under pressure. People who relabelled nerves as excitement performed better than people told to calm down, and brief structured breathing measurably lowered the body\'s stress arousal.',
    references: EMOTIONAL_INTELLIGENCE_REFERENCE_LIST,
  },
  {
    id: 'exam-crisis-management-protocol',
    what: 'You build a personal plan for when exams go wrong: a fast breathing reset for blank moments, a post-exam recovery rule, and a seven-day countdown routine.',
    why: 'Going blank is an acute stress response that passes, not lost knowledge. A double inhale with a slow exhale settled the body more than other breathing patterns tested, banked sleep cushioned later short nights, and slow-release breakfasts kept schoolchildren\'s concentration steadier.',
    references: EXAM_CRISIS_MANAGEMENT_REFERENCE_LIST,
  },
  {
    id: 'exam-hall-strategies-protocol',
    what: 'You rehearse an exam-day routine: dumping fragile facts and worries on paper first, sorting questions by difficulty, budgeting minutes per mark, and moving on when stuck.',
    why: 'Acute exam stress steals brainpower you need for the questions themselves. Students who spent the first minutes writing their worries down scored higher on classroom exams, and a daily practice of slow, structured breathing settles the nervous system.',
    references: EXAM_HALL_STRATEGIES_REFERENCE_LIST,
  },
  {
    id: 'game-day-protocol',
    what: 'You plan the run-up to exams like an athlete\'s season: adjusting sleep and food, tapering study, rehearsing exam-day steps, and setting a morning routine.',
    why: 'People who mentally rehearsed the steps of preparing performed better than people who only pictured the result. Writing tomorrow\'s list before bed helped people fall asleep faster, and the body works better when pressure is read as a challenge, not a threat.',
    references: GAME_DAY_REFERENCE_LIST,
  },
  {
    id: 'growth-mindset-protocol',
    what: 'You examine your own beliefs about ability, then practise growth habits: reframing "I can\'t" as "not yet", targeting your practice, and using feedback as information.',
    why: 'Brain imaging found that learning a new skill measurably changed the brain\'s physical structure within months. Skill is built through focused, effortful practice, and feedback works best when treated as directions for the next step, not a verdict on who you are.',
    references: GROWTH_MINDSET_REFERENCE_LIST,
  },
  {
    id: 'hope-protocol',
    what: 'You learn that hope is two trainable skills, willpower and waypower, then practise both: vividly picturing future goals and mapping several routes to reach them.',
    why: 'Vividly imagining a future goal made distant rewards feel more motivating in the present, and practising planning strengthens the brain pathways involved. That makes hope trainable, not wishful thinking.',
    references: HOPE_PROTOCOL_REFERENCE_LIST,
  },
  {
    id: 'illusion-of-competence-protocol',
    what: 'You learn why re-reading and highlighting feel like knowing, then test your real recall by explaining topics plainly and switching to spacing, mixing and self-testing.',
    why: 'Students routinely mistake recognising a page for being able to recall it, so passive study feels finished when little has stuck. Effortful self-testing, spacing and mixing build memory that lasts and transfers to new problems.',
    references: ILLUSION_OF_COMPETENCE_REFERENCE_LIST,
  },
  {
    id: 'leaving-cert-strategy-protocol',
    what: 'You use a CAO points calculator to see how best-six counting, the HL Maths bonus and component weightings shape where your marks actually come from.',
    why: 'The rules are public: only your best six subjects count, the Irish oral carries 40 per cent of the marks, and examiners\' reports name reciting knowledge instead of answering the question as a leading error. That lets you put effort where it pays.',
    references: LEAVING_CERT_STRATEGY_REFERENCE_LIST,
  },
  {
    id: 'linking-study-future-goals-protocol',
    what: 'You rate why each of your subjects matters to you, write short notes linking them to your own future, and turn vague goals into if-then plans.',
    why: 'Students who wrote briefly about how a subject connected to their own lives grew more interested and earned better grades, with the biggest gains for those struggling. Specific if-then plans make follow-through much more likely, while daydreaming alone can sap energy.',
    references: LINKING_STUDY_FUTURE_GOALS_REFERENCE_LIST,
  },
  {
    id: 'marking-scheme-decoder-protocol',
    what: 'You learn how SEC marking schemes are structured, sort attempt, method and answer marks, and practise decoding the conventions examiners use to award credit.',
    why: 'SEC schemes mark positively: examiners credit what\'s right and ignore what\'s wrong, correct method with a wrong answer can earn most of a Maths question\'s marks, and a relevant attempt earns marks where a blank scores zero. So always attempt, always show your steps.',
    references: MARKING_SCHEME_DECODER_REFERENCE_LIST,
  },
  {
    id: 'mastering-active-recall-protocol',
    what: 'You compare re-reading with self-testing, see why retrieval builds lasting memory, and set up a closed-book recall routine that continues past the first correct answer.',
    why: 'Students who tested themselves remembered far more a week later than students who re-read, and the habit carries to new problems, not just repeated facts. Most students also find low-stakes quizzing eases exam nerves rather than adding to them.',
    references: ACTIVE_RECALL_REFERENCE_LIST,
  },
  {
    id: 'mastering-interleaving-protocol',
    what: 'You compare blocked and mixed study plans, practise telling similar problem types apart, and build a timetable that puts your weakest topics first.',
    why: 'Students who mixed problem types learned maths better than those who worked topic by topic, because mixing forces you to choose the right method, exactly what an exam asks. The extra difficulty is the point, not a sign you\'re failing.',
    references: INTERLEAVING_REFERENCE_LIST,
  },
  {
    id: 'mastering-spaced-repetition-protocol',
    what: 'You learn how memory fades after studying, then build a spaced review schedule that tests you across days instead of re-reading in one sitting.',
    why: 'Without review, a large share of new material fades within the first day or two. Spacing the same study time across several days keeps it in memory far longer than cramming.',
    references: SPACED_REPETITION_REFERENCE_LIST,
  },
  {
    id: 'mental-modelling-protocol',
    what: 'You practise picturing and rotating 3D objects in your head for DCG and Engineering, working through a decompose, build, test and draw cycle.',
    why: 'Spatial skill is not a fixed talent; people who trained it got steadily better. Relying on memorised steps alone leaves you stuck the moment a problem looks unfamiliar.',
    references: MENTAL_MODELLING_REFERENCE_LIST,
  },
  {
    id: 'neuroplasticity-protocol',
    what: 'You learn how practice physically reshapes your brain, why the teenage brain changes especially fast, and which study habits build lasting connections.',
    why: 'Training grew real grey matter in three months and it shrank again once people stopped, so your brain is built by what you repeatedly do. Sleep locks that change in; ongoing stress works against it.',
    references: NEUROPLASTICITY_REFERENCE_LIST,
  },
  {
    id: 'points-optimization-protocol',
    what: 'You learn how the CAO points scale works, why H1 rates differ across subjects, and how marking schemes reward writing extra valid points.',
    why: 'The step from an H1 to an H2 costs more points than any grade drop below it, and marking schemes list more valid points than you need, so extra correct material can only help you.',
    references: POINTS_OPTIMIZATION_REFERENCE_LIST,
  },
  {
    id: 'procrastination-protocol',
    what: 'You learn why you put things off, then build if-then plans and a self-forgiveness habit that make starting the next task easier.',
    why: 'Putting things off is your brain dodging a bad feeling, not laziness. Students who forgave themselves for procrastinating before one exam went on to procrastinate less before the next.',
    references: PROCRASTINATION_REFERENCE_LIST,
  },
  {
    id: 'reframing-progress-protocol',
    what: 'You stop measuring study by hours logged and set up systems that track what you have actually learned and where you still need work.',
    why: 'Re-reading notes makes material feel familiar, which fools you into thinking you know it. Real progress comes from working on your weak spots and checking whether you have actually fixed them.',
    references: REFRAMING_PROGRESS_REFERENCE_LIST,
  },
  {
    id: 'reverse-engineering-protocol',
    what: 'You learn to plan backwards from the exam date, chunking the syllabus into phases and adding buffer time so the plan survives real life.',
    why: 'People consistently underestimate how long tasks take, so forward-built plans quietly run out of time. Building in buffer weeks and regular life checks corrects for that bias, while spaced, self-tested revision makes what you cover actually stick.',
    references: REVERSE_ENGINEERING_REFERENCE_LIST,
  },
  {
    id: 'self-efficacy-protocol',
    what: 'You map the four sources of belief in your own ability, from small wins to relatable role models, and set if-then plans to grow it.',
    why: 'Belief in your own ability shapes how hard you try and how you come back from setbacks. Students build more of it from role models who visibly struggled first than from people who make success look effortless.',
    references: SELF_EFFICACY_REFERENCE_LIST,
  },
  {
    id: 'strategic-advantage-protocol',
    what: 'You rework the story you tell about your own setbacks, reframing low points as turning points and writing your own redemption script.',
    why: 'Telling the story of a low point as a turning point is linked with greater resilience and well-being. Certain kinds of harder practice, like spacing study out instead of cramming, also tend to produce deeper, longer-lasting learning.',
    references: STRATEGIC_ADVANTAGE_REFERENCE_LIST,
  },
  {
    id: 'autodidact-engine-protocol',
    what: 'You build feedback into solo study: trying a problem before checking it, back-translating language work, and marking your own essays against real exam criteria.',
    why: 'Passive repetition builds little; skill grows when work is checked against a correct standard and errors get noticed and fixed. That means you can get honest feedback even with no teacher beside you.',
    references: FEEDBACK_LOOPS_REFERENCE_LIST,
  },
  {
    id: 'cognitive-architecture-protocol',
    what: 'You follow information through the brain\'s memory stores, see where most of it drops out, and choose techniques that move it into long-term memory.',
    why: 'Short-term memory holds about four chunks and loses unrehearsed material within half a minute. Testing yourself and spacing practice out are rated the most dependable everyday techniques for getting past that bottleneck.',
    references: HOW_MEMORY_WORKS_REFERENCE_LIST,
  },
  {
    id: 'cognitive-load-protocol',
    what: 'You learn that working memory tops out around four chunks, then practise cutting wasted mental effort so hard material actually gets learned.',
    why: 'Pushing past working memory\'s limit degrades learning. Even small fixes count: students learned substantially better when diagrams and their explanations sat together on the page instead of apart.',
    references: COGNITIVE_LOAD_REFERENCE_LIST,
  },
  {
    id: 'context-effect-protocol',
    what: 'You learn to rotate between a few study spots and match background noise to the task instead of always studying in one place.',
    why: 'Studying the same material in different places builds more retrieval routes, so what you learned isn\'t tied to one room. The effect is modest but stacks with other habits, and moderate background noise can help open-ended work.',
    references: CONTEXT_EFFECT_REFERENCE_LIST,
  },
  {
    id: 'grammar-of-grit-protocol',
    what: 'You examine how you explain setbacks to yourself, spot the personal, pervasive and permanent patterns, and practise rewriting those thoughts.',
    why: 'The way you explain a setback to yourself shapes whether you bounce back from it. Catching and rewriting harsh automatic thoughts is a core technique in cognitive behavioural therapy, and self-compassion gives you a steadier way to respond.',
    references: GRAMMAR_OF_GRIT_REFERENCE_LIST,
  },
  {
    id: 'implementation-protocol',
    what: 'You build if-then study plans, pair a task you enjoy with one you avoid, and set your own deadlines to act on your intentions.',
    why: 'Wanting to study predicts only a small part of whether you actually do it. Making a specific if-then plan for when and where roughly doubled follow-through across dozens of studies, and pairing a task with something you enjoy raised how often people showed up.',
    references: IMPLEMENTATION_PROTOCOL_REFERENCE_LIST,
  },
  {
    id: 'learning-radar-protocol',
    what: 'You test how well your sense of what you know matches what you can actually recall, then use self-testing to find your blind spots.',
    why: 'Your sense of how much you know lines up only modestly with what you can actually recall, so it\'s easy to feel ready when you aren\'t. Testing yourself, and judging your knowledge after a delay rather than right away, gives a more honest read.',
    references: LEARNING_RADAR_REFERENCE_LIST,
  },
  {
    id: 'myelin-manual-protocol',
    what: 'You learn how focused, error-rich practice at the edge of your ability physically speeds up the brain connections behind a skill.',
    why: 'Focused, effortful practice physically changes the brain, thickening the insulation around active connections so signals travel faster. Struggling at the edge of your ability is part of building a skill, not a sign of failing, though the gains fade if you stop.',
    references: MYELIN_MANUAL_REFERENCE_LIST,
  },
  {
    id: 'note-taking-paradox-protocol',
    what: 'You learn to write notes in your own words, use the Cornell layout to test yourself, and choose maps or lists to fit the material.',
    why: 'Copying words down as you hear them leads to shallower learning than putting ideas in your own words, which forces you to process the meaning. Notes built for self-testing, and maps for topics with lots of links, help more than plain transcription.',
    references: NOTE_TAKING_PARADOX_REFERENCE_LIST,
  },
  {
    id: 'power-of-yet-protocol',
    what: 'You catch your own "I can\'t" statements, add "yet", and turn each one into one specific next step you can actually take.',
    why: 'In one study, people who saw ability as growable paid more attention to their errors and adjusted after them. Pairing "yet" with one concrete next step uses plans that reliably beat vague intentions, so the next move is already decided.',
    references: POWER_OF_YET_REFERENCE_LIST,
  },
  {
    id: 'praise-protocol',
    what: 'You learn to spot the difference between praise for who you are and praise for what you did, then audit your own self-talk.',
    why: 'Children praised for being clever chose easier tasks, gave up sooner after failure, and often misrepresented their scores; children praised for how they worked kept going. Knowing the difference lets you talk to yourself in the way that sustains effort.',
    references: PRAISE_PROTOCOL_REFERENCE_LIST,
  },
  {
    id: 'science-of-making-mistakes-protocol',
    what: 'You learn what your brain does in the second after a mistake, then build a simple mistake log that turns each error into one fix.',
    why: 'Your brain fires an automatic alarm within a fraction of a second of an error, and the later signal of consciously noticing the mistake is linked to correcting it next time. The log habit puts that noticing to work.',
    references: SCIENCE_OF_MISTAKES_REFERENCE_LIST,
  },
  {
    id: 'teaching-effect-protocol',
    what: 'You study a topic as if you will have to teach it, then practise explaining it back in your own plain words.',
    why: 'Students who merely expected to teach a passage remembered more of it and organised it better, without ever teaching anyone. Explaining an example to yourself also exposes gaps, and students who did went on to solve more new problems.',
    references: TEACHING_EFFECT_REFERENCE_LIST,
  },
  {
    id: 'subject-mathematics-protocol',
    what: 'You learn how both Maths papers are structured, where the marks sit, and how to show work so every relevant step earns credit.',
    why: 'The Chief Examiner is explicit that a wrong answer with no work shown earns nothing, while relevant steps earn partial credit. Reworking problems from scratch beats re-reading, and mixing topics as you practise improves learning on maths problems.',
    references: SUBJECT_MATHEMATICS_REFERENCE_LIST,
  },
  {
    id: 'subject-business-protocol',
    what: 'You learn how the single 400-mark Business paper is structured, from the short questions to the ABQ, and how answers earn their marks.',
    why: 'The marking scheme awards no ABQ link mark unless theory is tied to the text, and the Chief Examiner rewards developed answers over one-word points. Knowing those rules lets you spend your time where the marks actually are.',
    references: SUBJECT_BUSINESS_REFERENCE_LIST,
  },
];
