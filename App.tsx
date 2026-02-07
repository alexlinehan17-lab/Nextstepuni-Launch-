
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, Suspense, lazy } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, LogOut } from 'lucide-react';
import { Library, CourseData } from './components/Library';
import { KnowledgeTree, CategoryType } from './components/KnowledgeTree';
import { LoadingSpinner } from './components/LoadingSpinner';
import { Auth, SessionUser } from './components/Auth';
import { AdminDashboard } from './components/AdminDashboard';
import { auth, db } from './firebase';
import { onAuthStateChanged, signOut, User as FirebaseUser } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';

// FIX: Cast motion components to any to bypass broken type definitions
const MotionDiv = motion.div as any;

type ModuleProgress = {
  unlockedSection: number;
};

type UserProgress = {
  [moduleId: string]: ModuleProgress;
};


// Dynamically import all module components for code-splitting
const AgencyProtocolModule = lazy(() => import('./components/AgencyProtocolModule').then(module => ({ default: module.AgencyProtocolModule })));
const HopeProtocolModule = lazy(() => import('./components/HopeProtocolModule').then(module => ({ default: module.HopeProtocolModule })));
const AffirmingValuesModule = lazy(() => import('./components/AffirmingValuesModule').then(module => ({ default: module.AffirmingValuesModule })));
const BestPossibleSelfModule = lazy(() => import('./components/BestPossibleSelfModule').then(module => ({ default: module.BestPossibleSelfModule })));
const TheGrammarOfGritModule = lazy(() => import('./components/TheGrammarOfGritModule').then(module => ({ default: module.TheGrammarOfGritModule })));
const SocialCapitalModule = lazy(() => import('./components/SocialCapitalModule').then(module => ({ default: module.SocialCapitalModule })));
const AgencyArchitectureModule = lazy(() => import('./components/AgencyArchitectureModule').then(module => ({ default: module.AgencyArchitectureModule })));
const StrategicAdvantageModule = lazy(() => import('./components/StrategicAdvantageModule').then(module => ({ default: module.StrategicAdvantageModule })));
const SelfEfficacyModule = lazy(() => import('./components/SelfEfficacyModule').then(module => ({ default: module.SelfEfficacyModule })));
const NeuroplasticityProtocolModule = lazy(() => import('./components/NeuroplasticityProtocolModule').then(module => ({ default: module.NeuroplasticityProtocolModule })));
const TheMyelinManualModule = lazy(() => import('./components/TheMyelinManualModule').then(module => ({ default: module.TheMyelinManualModule })));
const ThePraiseProtocolModule = lazy(() => import('./components/ThePraiseProtocolModule').then(module => ({ default: module.ThePraiseProtocolModule })));
const EffectiveStruggleAndGrowthModule = lazy(() => import('./components/EffectiveStruggleAndGrowthModule').then(module => ({ default: module.EffectiveStruggleAndGrowthModule })));
const TheScienceOfMakingMistakesModule = lazy(() => import('./components/TheScienceOfMakingMistakesModule').then(module => ({ default: module.TheScienceOfMakingMistakesModule })));
const TheAutodidactsEngineModule = lazy(() => import('./components/TheAutodidactsEngineModule').then(module => ({ default: module.TheAutodidactsEngineModule })));
const ThePowerOfYetModule = lazy(() => import('./components/ThePowerOfYetModule').then(module => ({ default: module.ThePowerOfYetModule })));
const TheCognitiveBaselineModule = lazy(() => import('./components/TheCognitiveBaselineModule').then(module => ({ default: module.TheCognitiveBaselineModule })));
const IllusionOfCompetenceModule = lazy(() => import('./components/IllusionOfCompetenceModule').then(module => ({ default: module.IllusionOfCompetenceModule })));
const MasteringActiveRecallModule = lazy(() => import('./components/MasteringActiveRecallModule').then(module => ({ default: module.MasteringActiveRecallModule })));
const MasteringSpacedRepetitionModule = lazy(() => import('./components/MasteringSpacedRepetitionModule').then(module => ({ default: module.MasteringSpacedRepetitionModule })));
const MasteringInterleavingModule = lazy(() => import('./components/MasteringInterleavingModule').then(module => ({ default: module.MasteringInterleavingModule })));
const TheCognitiveArchitectureModule = lazy(() => import('./components/TheCognitiveArchitectureModule').then(module => ({ default: module.TheCognitiveArchitectureModule })));
const ElaborativeInterrogationModule = lazy(() => import('./components/ElaborativeInterrogationModule').then(module => ({ default: module.ElaborativeInterrogationModule })));
const CognitiveEnduranceModule = lazy(() => import('./components/CognitiveEnduranceModule').then(module => ({ default: module.CognitiveEnduranceModule })));
const MentalModellingModule = lazy(() => import('./components/MentalModellingModule').then(module => ({ default: module.MentalModellingModule })));
const BimodalBrainModule = lazy(() => import('./components/BimodalBrainModule').then(module => ({ default: module.BimodalBrainModule })));
const ProcrastinationModule = lazy(() => import('./components/ProcrastinationModule').then(module => ({ default: module.ProcrastinationModule })));
const LeavingCertStrategyModule = lazy(() => import('./components/LeavingCertStrategyModule').then(module => ({ default: module.LeavingCertStrategyModule })));
const ReverseEngineeringModule = lazy(() => import('./components/ReverseEngineeringModule').then(module => ({ default: module.ReverseEngineeringModule })));
const AchievingEffectiveLearningOutcomesModule = lazy(() => import('./components/AchievingEffectiveLearningOutcomesModule').then(module => ({ default: module.AchievingEffectiveLearningOutcomesModule })));
const ExamHallStrategiesModule = lazy(() => import('./components/ExamHallStrategiesModule').then(module => ({ default: module.ExamHallStrategiesModule })));
const ExamCrisisManagementModule = lazy(() => import('./components/ExamCrisisManagementModule').then(module => ({ default: module.ExamCrisisManagementModule })));
const SubjectSpecificAdviceModule = lazy(() => import('./components/SubjectSpecificAdviceModule').then(module => ({ default: module.SubjectSpecificAdviceModule })));
const GrowthMindsetModule = lazy(() => import('./components/GrowthMindsetModule').then(module => ({ default: module.GrowthMindsetModule })));
const InnovationZone = lazy(() => import('./components/InnovationZone').then(module => ({ default: module.InnovationZone })));
const ControllableVariablesModule = lazy(() => import('./components/ControllableVariablesModule').then(module => ({ default: module.ControllableVariablesModule })));
const ReframingProgressModule = lazy(() => import('./components/ReframingProgressModule').then(module => ({ default: module.ReframingProgressModule })));
const LearningMathModule = lazy(() => import('./components/LearningMathModule').then(module => ({ default: module.LearningMathModule })));
const LinkingStudyFutureGoalsModule = lazy(() => import('./components/LinkingStudyFutureGoalsModule').then(module => ({ default: module.LinkingStudyFutureGoalsModule })));
const GameDayModule = lazy(() => import('./components/GameDayModule').then(module => ({ default: module.GameDayModule })));
const CatastrophicThinkingModule = lazy(() => import('./components/CatastrophicThinkingModule').then(module => ({ default: module.CatastrophicThinkingModule })));
const LanguageMasteryModule = lazy(() => import('./components/LanguageMasteryModule').then(module => ({ default: module.LanguageMasteryModule })));
const EmotionalIntelligenceModule = lazy(() => import('./components/EmotionalIntelligenceModule').then(module => ({ default: module.EmotionalIntelligenceModule })));
const ConnectingEducationToGoalsModule = lazy(() => import('./components/ConnectingEducationToGoalsModule').then(module => ({ default: module.ConnectingEducationToGoalsModule })));
const MasteringTheSciencesModule = lazy(() => import('./components/MasteringTheSciencesModule').then(module => ({ default: module.MasteringTheSciencesModule })));
const MasteringTheHumanitiesModule = lazy(() => import('./components/MasteringTheHumanitiesModule').then(module => ({ default: module.MasteringTheHumanitiesModule })));
const MasteringEnglishModule = lazy(() => import('./components/MasteringEnglishModule').then(module => ({ default: module.MasteringEnglishModule })));
const MasteringBusinessModule = lazy(() => import('./components/MasteringBusinessModule').then(module => ({ default: module.MasteringBusinessModule })));
const AppliedSciencesModule = lazy(() => import('./components/AppliedSciencesModule').then(module => ({ default: module.AppliedSciencesModule })));
const DigitalDistractionModule = lazy(() => import('./components/DigitalDistractionModule').then(module => ({ default: module.DigitalDistractionModule })));
const MasteringTheCreativesModule = lazy(() => import('./components/MasteringTheCreativesModule').then(module => ({ default: module.MasteringTheCreativesModule })));


const moduleComponents: { [key: string]: React.LazyExoticComponent<React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void; }>> } = {
  'agency-protocol': AgencyProtocolModule,
  'hope-protocol': HopeProtocolModule,
  'affirming-values-protocol': AffirmingValuesModule,
  'best-possible-self-protocol': BestPossibleSelfModule,
  'grammar-of-grit-protocol': TheGrammarOfGritModule,
  'social-capital-protocol': SocialCapitalModule,
  'agency-architecture-protocol': AgencyArchitectureModule,
  'strategic-advantage-protocol': StrategicAdvantageModule,
  'self-efficacy-protocol': SelfEfficacyModule,
  'illusion-of-competence-protocol': IllusionOfCompetenceModule,
  'procrastination-protocol': ProcrastinationModule,
  'neuroplasticity-protocol': NeuroplasticityProtocolModule,
  'myelin-manual-protocol': TheMyelinManualModule,
  'praise-protocol': ThePraiseProtocolModule,
  'effective-struggle-protocol': EffectiveStruggleAndGrowthModule,
  'science-of-making-mistakes-protocol': TheScienceOfMakingMistakesModule,
  'autodidact-engine-protocol': TheAutodidactsEngineModule,
  'power-of-yet-protocol': ThePowerOfYetModule,
  'cognitive-baseline-protocol': TheCognitiveBaselineModule,
  'mastering-active-recall-protocol': MasteringActiveRecallModule,
  'mastering-spaced-repetition-protocol': MasteringSpacedRepetitionModule,
  'mastering-interleaving-protocol': MasteringInterleavingModule,
  'cognitive-architecture-protocol': TheCognitiveArchitectureModule,
  'elaborative-interrogation-protocol': ElaborativeInterrogationModule,
  'cognitive-endurance-protocol': CognitiveEnduranceModule,
  'mental-modelling-protocol': MentalModellingModule,
  'bimodal-brain-protocol': BimodalBrainModule,
  'leaving-cert-strategy-protocol': LeavingCertStrategyModule,
  'reverse-engineering-protocol': ReverseEngineeringModule,
  'achieving-effective-learning-outcomes-protocol': AchievingEffectiveLearningOutcomesModule,
  'exam-hall-strategies-protocol': ExamHallStrategiesModule,
  'exam-crisis-management-protocol': ExamCrisisManagementModule,
  'subject-specific-advice-protocol': SubjectSpecificAdviceModule,
  'growth-mindset-protocol': GrowthMindsetModule,
  'controllable-variables-protocol': ControllableVariablesModule,
  'reframing-progress-protocol': ReframingProgressModule,
  'learning-math-protocol': LearningMathModule,
  'linking-study-future-goals-protocol': LinkingStudyFutureGoalsModule,
  'game-day-protocol': GameDayModule,
  'reframing-catastrophic-thoughts-protocol': CatastrophicThinkingModule,
  'mastering-foreign-languages-protocol': LanguageMasteryModule,
  'emotional-intelligence-protocol': EmotionalIntelligenceModule,
  'connecting-education-to-goals-protocol': ConnectingEducationToGoalsModule,
  'mastering-the-sciences-protocol': MasteringTheSciencesModule,
  'mastering-the-humanities-protocol': MasteringTheHumanitiesModule,
  'mastering-english-protocol': MasteringEnglishModule,
  'mastering-business-protocol': MasteringBusinessModule,
  'applied-sciences-protocol': AppliedSciencesModule,
  'digital-distraction-protocol': DigitalDistractionModule,
  'mastering-the-creatives-protocol': MasteringTheCreativesModule,
};

const categoryColorMap: Record<CategoryType, { gradient: string; accentColor: string; auraColor: string; }> = {
    'architecture-mindset': {
        gradient: 'bg-gradient-to-tr from-blue-100 via-white to-stone-50',
        accentColor: 'text-blue-700',
        auraColor: 'hover:shadow-[0_20px_50px_rgba(59,130,246,0.15)]'
    },
    'science-growth': {
        gradient: 'bg-gradient-to-tr from-amber-100 via-white to-stone-50',
        accentColor: 'text-amber-700',
        auraColor: 'hover:shadow-[0_20px_50px_rgba(245,158,11,0.15)]'
    },
    'learning-cheat-codes': {
        gradient: 'bg-gradient-to-tr from-teal-100 via-white to-stone-50',
        accentColor: 'text-teal-700',
        auraColor: 'hover:shadow-[0_20px_50px_rgba(13,148,136,0.15)]'
    },
    'subject-specific-science': {
        gradient: 'bg-gradient-to-tr from-slate-100 via-white to-stone-50',
        accentColor: 'text-slate-700',
        auraColor: 'hover:shadow-[0_20px_50px_rgba(71,85,105,0.15)]'
    },
    'exam-zone': {
        gradient: 'bg-gradient-to-tr from-red-100 via-white to-stone-50',
        accentColor: 'text-red-700',
        auraColor: 'hover:shadow-[0_20px_50px_rgba(220,38,38,0.15)]'
    },
    'the-shield': { // Fallback, not currently used by any module
        gradient: 'bg-gradient-to-tr from-indigo-100 via-white to-stone-50',
        accentColor: 'text-indigo-700',
        auraColor: 'hover:shadow-[0_20px_50px_rgba(79,70,229,0.15)]'
    },
    'the-launchpad': { // Fallback, not currently used by any module
        gradient: 'bg-gradient-to-tr from-rose-100 via-white to-stone-50',
        accentColor: 'text-rose-700',
        auraColor: 'hover:shadow-[0_20px_50px_rgba(225,29,72,0.15)]'
    }
};

const COURSE_DEFINITIONS = [
  {
    id: 'agency-protocol',
    category: 'architecture-mindset',
    title: 'Establishing Your Academic Identity',
    subtitle: 'The Driver\'s Manual',
    description: 'Synthesising research on motivation and identity, this module provides the blueprint for becoming the "Origin" of your academic success.',
    sectionsCount: 6,
    tags: ['Mindset', 'Motivation'],
  },
  {
    id: 'hope-protocol',
    category: 'architecture-mindset',
    title: 'The Hope Protocol',
    subtitle: 'Your Brain\'s Engineering Manual',
    description: 'Explore the neurobiology of hope, learning how to engineer the mental circuits for motivation and resilience under pressure.',
    sectionsCount: 6,
    tags: ['Brain Science', 'Resilience'],
  },
  {
    id: 'affirming-values-protocol',
    category: 'architecture-mindset',
    title: 'Affirming Values',
    subtitle: 'The Psychological Shield Protocol',
    description: 'Learn the science of "stereotype threat" and how a 15-minute writing exercise can act as a psychological shield in high-stakes exams.',
    sectionsCount: 5,
    tags: ['Mindset', 'Resilience'],
  },
  {
    id: 'best-possible-self-protocol',
    category: 'architecture-mindset',
    title: 'Finding Your Best Possible Self',
    subtitle: 'The Future-Proofing Protocol',
    description: 'Learn how to turn vague daydreams into actionable plans using the scientifically-proven WOOP method for goal achievement.',
    sectionsCount: 5,
    tags: ['Motivation', 'Productivity'],
  },
  {
    id: 'grammar-of-grit-protocol',
    category: 'architecture-mindset',
    title: 'The Grammar of Grit',
    subtitle: 'The Language of Resilience Protocol',
    description: 'Discover how the words you use to define yourself can either build resilience or create fragility in the face of failure.',
    sectionsCount: 5,
    tags: ['Mindset', 'Resilience'],
  },
  {
    id: 'social-capital-protocol',
    category: 'architecture-mindset',
    title: 'The Social Capital Protocol',
    subtitle: 'The Network Engineering Protocol',
    description: 'Understand the invisible social forces that shape your success and learn how to engineer your network for upward mobility.',
    sectionsCount: 5,
    tags: ['Exam Tactics', 'Productivity'],
  },
  {
    id: 'agency-architecture-protocol',
    category: 'architecture-mindset',
    title: 'Controlling the Controllables',
    subtitle: 'The Attribution Retraining Protocol',
    description: 'Learn to distinguish between what you can and cannot control, and rewire your brain to see failure as feedback, not a final verdict.',
    sectionsCount: 5,
    tags: ['Mindset', 'Resilience'],
  },
  {
    id: 'strategic-advantage-protocol',
    category: 'architecture-mindset',
    title: 'Your Strategic Advantage',
    subtitle: 'The Narrative Identity Protocol',
    description: 'Discover how to turn your personal story of adversity into your greatest competitive advantage in academia and beyond.',
    sectionsCount: 5,
    tags: ['Mindset', 'Resilience'],
  },
  {
    id: 'self-efficacy-protocol',
    category: 'architecture-mindset',
    title: 'Self Efficacy',
    subtitle: 'The Architecture of Agency',
    description: 'Move beyond "trying harder" and learn the science of building bulletproof belief in your own ability. This module deconstructs the myth of "natural talent" and gives you the tools to reverse-engineer success.',
    sectionsCount: 5,
    tags: ['Mindset', 'Motivation'],
  },
  {
    id: 'illusion-of-competence-protocol',
    category: 'architecture-mindset',
    title: 'Overcoming Illusions of Competence',
    subtitle: 'The Fluency Illusion Protocol',
    description: 'Deconstruct the cognitive biases that trick you into feeling confident when you\'re unprepared, and learn the science-backed strategies to build real, durable knowledge.',
    sectionsCount: 6,
    tags: ['Learning Strategy', 'Brain Science'],
  },
  {
    id: 'procrastination-protocol',
    category: 'architecture-mindset',
    title: 'Understanding Procrastination and Motivation',
    subtitle: 'The Architecture of Delay Protocol',
    description: 'Go beyond "laziness" and understand the real science of why you delay. Learn to master your motivation with evidence-based strategies.',
    sectionsCount: 8,
    tags: ['Motivation', 'Productivity'],
  },
  {
    id: 'reframing-catastrophic-thoughts-protocol',
    category: 'architecture-mindset',
    title: 'Reframing Catastrophic Thoughts',
    subtitle: 'The CBT Protocol',
    description: 'Deconstruct the neurobiology of exam panic and learn the gold-standard psychological tools (CBT & ACT) to dismantle catastrophic thinking and regain control.',
    sectionsCount: 8,
    tags: ['Resilience', 'Performance Psych'],
  },
  {
    id: 'emotional-intelligence-protocol',
    category: 'architecture-mindset',
    title: 'Building Emotional Intelligence',
    subtitle: 'The Stress Management Protocol',
    description: 'Learn the neurobiology of exam stress and master the "top-down" and "bottom-up" strategies to transform anxiety into a high-performance state.',
    sectionsCount: 8,
    tags: ['Performance Psych', 'Resilience'],
  },
  {
    id: 'connecting-education-to-goals-protocol',
    category: 'architecture-mindset',
    title: 'Connecting Education to Goals',
    subtitle: 'The Purpose Protocol',
    description: 'Synthesizing research on Future Time Perspective and Self-Determination Theory to forge a powerful, resilient link between today\'s effort and tomorrow\'s success.',
    sectionsCount: 6,
    tags: ['Motivation', 'Mindset'],
  },
  {
    id: 'neuroplasticity-protocol',
    category: 'science-growth',
    title: 'The Neuroplasticity Protocol',
    subtitle: 'Your Brain\'s User Manual',
    description: 'Discover that your brain isn\'t fixed. Learn the science of how your brain physically changes when you study, and how to use this to your advantage.',
    sectionsCount: 6,
    tags: ['Brain Science', 'Learning Strategy'],
  },
  {
    id: 'myelin-manual-protocol',
    category: 'science-growth',
    title: 'The Myelin Manual',
    subtitle: 'The Neurobiology of Mastery',
    description: 'Reframe "struggle" from a sign of failure into the biological trigger for building faster, more efficient brain circuits. This is the science of Deep Practice.',
    sectionsCount: 5,
    tags: ['Brain Science', 'Learning Strategy'],
  },
  {
    id: 'praise-protocol',
    category: 'science-growth',
    title: 'The Praise Protocol',
    subtitle: 'The Architecture of Potential',
    description: 'Learn how the language you use to interpret success and failure programs your brain for a fixed or growth mindset. It’s not what you say, but how you say it.',
    sectionsCount: 6,
    tags: ['Mindset', 'Motivation'],
  },
  {
    id: 'effective-struggle-protocol',
    category: 'science-growth',
    title: 'Effective Struggle and Growth',
    subtitle: 'The Cognitive Architecture of Friction',
    description: 'Synthesizing key learning theories to define the "sweet spot" of difficulty where real learning happens. Re-calibrate your internal dashboard for what growth feels like.',
    sectionsCount: 6,
    tags: ['Learning Strategy', 'Brain Science'],
  },
  {
    id: 'science-of-making-mistakes-protocol',
    category: 'science-growth',
    title: 'The Science of Making Mistakes',
    subtitle: 'The Neural Architecture of Failure',
    description: 'Learn why your brain\'s reaction to mistakes predicts success, and how to rewire it for resilience under pressure in high-stakes exams.',
    sectionsCount: 5,
    tags: ['Brain Science', 'Resilience'],
  },
  {
    id: 'autodidact-engine-protocol',
    category: 'science-growth',
    title: 'Using Feedback Loops',
    subtitle: 'The Autodidact\'s Engine',
    description: 'Become your own teacher by learning to build autonomous feedback loops. This is the science of Deliberate Practice without a coach.',
    sectionsCount: 6,
    tags: ['Learning Strategy', 'Productivity'],
  },
  {
    id: 'power-of-yet-protocol',
    category: 'science-growth',
    title: 'The Power of "Yet"',
    subtitle: 'The Persistence Protocol',
    description: 'A simple, three-letter word that can rewire your brain for resilience. This module unpacks the neuroscience of error-processing and gives you a practical protocol to turn failure from a verdict into a fuel source.',
    sectionsCount: 5,
    tags: ['Mindset', 'Resilience'],
  },
  {
    id: 'cognitive-baseline-protocol',
    category: 'science-growth',
    title: 'The Cognitive Baseline Protocol',
    subtitle: 'Your Brain\'s Fuel & Maintenance',
    description: 'Your brain is a high-performance machine. This module provides the user manual for its biological needs: sleep, nutrition, and hydration. Learn the non-negotiable minimums for high-level thinking.',
    sectionsCount: 6,
    tags: ['Brain Science', 'Performance Psych'],
  },
   {
    id: 'controllable-variables-protocol',
    category: 'science-growth',
    title: 'Using Controllable Variables to Grow',
    subtitle: 'The Biological Blueprint',
    description: 'Learn to manage your brain as a biological system. This module covers the non-negotiable inputs of Sleep, Nutrition, and Exercise required for high performance.',
    sectionsCount: 6,
    tags: ['Performance Psych', 'Brain Science'],
  },
  {
    id: 'reframing-progress-protocol',
    category: 'science-growth',
    title: 'Reframing Progress',
    subtitle: 'The Outcome-Based Protocol',
    description: 'Shift from measuring "hours logged" to "wins secured." This module gives you the project management tools to study smarter, not just harder.',
    sectionsCount: 7,
    tags: ['Productivity', 'Mindset'],
  },
   {
    id: 'linking-study-future-goals-protocol',
    category: 'science-growth',
    title: 'Linking Study to Future Goals',
    subtitle: 'The Architecture of Purpose',
    description: 'Deconstruct the "why bother?" problem and learn the science of linking today\'s effort to tomorrow\'s success. This is the antidote to burnout.',
    sectionsCount: 7,
    tags: ['Motivation', 'Productivity'],
  },
  {
    id: 'achieving-effective-learning-outcomes-protocol',
    category: 'science-growth',
    title: 'Achieving Effective Learning Outcomes',
    subtitle: 'The Cognitive Architecture of Friction',
    description: 'Synthesizing key learning theories to define the \'sweet spot\' of difficulty where real learning happens. Re-calibrate your internal dashboard for what growth feels like.',
    sectionsCount: 6,
    tags: ['Learning Strategy', 'Brain Science'],
  },
  {
    id: 'growth-mindset-protocol',
    category: 'science-growth',
    title: 'The Growth Protocol',
    subtitle: 'The Mind\'s Operating System',
    description: 'Upgrade your brain\'s core operating system from "fixed" to "growth." This module deconstructs the science of neuroplasticity and gives you the tools to see challenges as opportunities.',
    sectionsCount: 6,
    tags: ['Mindset', 'Brain Science'],
  },
  {
    id: 'mastering-active-recall-protocol',
    category: 'learning-cheat-codes',
    title: 'Mastering Active Recall',
    subtitle: 'The Test Effect Protocol',
    description: 'Go beyond "practice testing" and learn the science of why active retrieval is the single most effective way to build durable, long-term memory.',
    sectionsCount: 6,
    tags: ['Learning Strategy', 'Brain Science'],
  },
  {
    id: 'mastering-spaced-repetition-protocol',
    category: 'learning-cheat-codes',
    title: 'Mastering Spaced Repetition',
    subtitle: 'The Forgetting Curve Protocol',
    description: 'Learn to defeat the "forgetting curve" by understanding the science of when and how often to review material for maximum long-term retention.',
    sectionsCount: 6,
    tags: ['Learning Strategy', 'Productivity'],
  },
  {
    id: 'mastering-interleaving-protocol',
    category: 'learning-cheat-codes',
    title: 'Mastering Interleaving',
    subtitle: 'The Topic Salad Protocol',
    description: 'Ditch "blocked" study and learn the science of mixing topics to build deep, flexible knowledge that stands up under exam pressure.',
    sectionsCount: 5,
    tags: ['Learning Strategy', 'Brain Science'],
  },
  {
    id: 'cognitive-architecture-protocol',
    category: 'learning-cheat-codes',
    title: 'Cognitive Architecture',
    subtitle: 'Your Brain\'s User Manual',
    description: 'Understand the fundamental architecture of your memory to move information from the fragile workbench of Short-Term Memory to the permanent library of Long-Term Memory.',
    sectionsCount: 6,
    tags: ['Brain Science', 'Learning Strategy'],
  },
  {
    id: 'elaborative-interrogation-protocol',
    category: 'learning-cheat-codes',
    title: 'Elaborative Interrogation',
    subtitle: 'The "Why" Protocol',
    description: 'Move beyond rote learning by mastering the art of asking "Why?". This module teaches you how to transform shallow facts into deep, interconnected knowledge for the new Leaving Cert.',
    sectionsCount: 6,
    tags: ['Learning Strategy', 'Mindset'],
  },
  {
    id: 'cognitive-endurance-protocol',
    category: 'learning-cheat-codes',
    title: 'Cognitive Endurance',
    subtitle: 'The Marathon Protocol',
    description: 'The Leaving Cert isn\'t a sprint. Learn the science of mental stamina and train your brain to perform under the sustained pressure of the exam timetable.',
    sectionsCount: 6,
    tags: ['Performance Psych', 'Brain Science'],
  },
  {
    id: 'mental-modelling-protocol',
    category: 'learning-cheat-codes',
    title: 'Mental Modelling',
    subtitle: 'The Mind\'s Eye Protocol',
    description: 'Learn to see the answer in your mind\'s eye. This module deconstructs the \'hidden curriculum\' of subjects like DCG and Engineering, teaching you how to build robust mental simulations.',
    sectionsCount: 6,
    tags: ['Learning Strategy', 'Subject Strategy'],
  },
  {
    id: 'bimodal-brain-protocol',
    category: 'learning-cheat-codes',
    title: 'Focused vs Diffuse Mode',
    subtitle: 'The Bimodal Brain Protocol',
    description: 'Your brain has two gears. Learn to switch between intense focus and creative relaxation to unlock deep learning and solve complex problems.',
    sectionsCount: 6,
    tags: ['Brain Science', 'Productivity'],
  },
  {
    id: 'learning-math-protocol',
    category: 'subject-specific-science',
    title: 'The Maths Protocol',
    subtitle: 'Deconstructing the Exam',
    description: 'A strategic deep-dive into the structure, marking schemes, and high-yield topics of the Leaving Cert Higher Level Maths exam.',
    sectionsCount: 9,
    tags: ['Subject Strategy', 'Exam Tactics'],
  },
  {
    id: 'mastering-foreign-languages-protocol',
    category: 'subject-specific-science',
    title: 'Mastering Foreign Languages',
    subtitle: 'The Language Mastery Protocol',
    description: 'A strategic deconstruction of the MFL exams, providing a bifurcated strategy for both foundational proficiency and top-tier performance.',
    sectionsCount: 8,
    tags: ['Subject Strategy', 'Exam Tactics'],
  },
  {
    id: 'mastering-the-sciences-protocol',
    category: 'subject-specific-science',
    title: 'Mastering the Sciences',
    subtitle: 'The STEM Grade Optimization Protocol',
    description: 'A strategic deconstruction of the STEM exams, revealing the "hidden curriculum" of Biology, Chemistry, Physics, and Ag Science.',
    sectionsCount: 7,
    tags: ['Subject Strategy', 'Exam Tactics'],
  },
  {
    id: 'mastering-english-protocol',
    category: 'subject-specific-science',
    title: 'Mastering English',
    subtitle: 'The PCLM Protocol',
    description: 'A strategic deconstruction of the Leaving Cert English exam, focusing on mastering the PCLM marking scheme and optimizing for H1 performance.',
    sectionsCount: 7,
    tags: ['Subject Strategy', 'Exam Tactics'],
  },
   {
    id: 'mastering-business-protocol',
    category: 'subject-specific-science',
    title: 'Mastering Business',
    subtitle: 'The Grade Optimization Protocol',
    description: 'Deconstruct the Business exam for 2026, focusing on the ABQ, "outcome verbs", and the "SEE/SEEE" structure to engineer a H1.',
    sectionsCount: 6,
    tags: ['Subject Strategy', 'Exam Tactics'],
  },
  {
    id: 'applied-sciences-protocol',
    category: 'subject-specific-science',
    title: 'Mastering Applied Sciences',
    subtitle: 'The 2026 Technical Briefs',
    description: 'A deep dive into the 2026 briefs for Engineering, DCG, CS, Construction & Technology, blending theory with project strategy.',
    sectionsCount: 6,
    tags: ['Subject Strategy', 'Exam Tactics'],
  },
  {
    id: 'mastering-the-creatives-protocol',
    category: 'subject-specific-science',
    title: 'Mastering the Creatives',
    subtitle: 'The Art, Music & Film Protocol',
    description: 'A strategic deconstruction of the \'creative\' subjects, revealing them as learnable skills governed by process, not just talent.',
    sectionsCount: 6,
    tags: ['Subject Strategy', 'Exam Tactics', 'Creativity'],
  },
  {
    id: 'leaving-cert-strategy-protocol',
    category: 'exam-zone',
    title: 'The Leaving Cert Points Protocol',
    subtitle: 'The Economics of Academic Assessment',
    description: 'Deconstruct the Leaving Cert as a points-based marketplace and learn the tactical framework for maximizing your score.',
    sectionsCount: 6,
    tags: ['Exam Tactics', 'Productivity'],
  },
  {
    id: 'subject-specific-advice-protocol',
    category: 'exam-zone',
    title: 'Subject Specific Advice',
    subtitle: 'The Decryption Key',
    description: 'Deconstruct the specific marking algorithms for each subject to transform your approach from passive learning to active "Grade Engineering".',
    sectionsCount: 6,
    tags: ['Exam Tactics', 'Subject Strategy'],
  },
  {
    id: 'reverse-engineering-protocol',
    category: 'exam-zone',
    title: 'Reverse Engineering Your Schedule',
    subtitle: 'The Temporal Architecture Protocol',
    description: 'Ditch the failed \'start-to-finish\' study plan. Learn to plan backwards from your exam date to create a realistic, resilient, and effective study schedule.',
    sectionsCount: 6,
    tags: ['Productivity', 'Exam Tactics'],
  },
  {
    id: 'exam-hall-strategies-protocol',
    category: 'exam-zone',
    title: 'Exam Hall Strategies',
    subtitle: 'The Operational Playbook',
    description: 'Deconstruct the exam hall as a resource-management challenge and learn the operational tactics used by elite performers to close the "Execution Gap".',
    sectionsCount: 7,
    tags: ['Exam Tactics', 'Performance Psych'],
  },
  {
    id: 'exam-crisis-management-protocol',
    category: 'exam-zone',
    title: 'Exam Crisis Management',
    subtitle: 'The Cognitive Athlete\'s Playbook',
    description: 'Learn the neurobiology of exam stress and master the physiological protocols to maintain mental stamina and overcome the "Blank Mind" phenomenon.',
    sectionsCount: 7,
    tags: ['Resilience', 'Performance Psych'],
  },
  {
    id: 'game-day-protocol',
    category: 'exam-zone',
    title: 'Game Day: The Athlete\'s Protocol',
    subtitle: 'Peak Performance on Demand',
    description: 'Transform your exam preparation by adopting the mindset and physiological protocols of an elite athlete. This is your playbook for peak performance.',
    sectionsCount: 8,
    tags: ['Performance Psych', 'Exam Tactics'],
  },
  {
    id: 'mastering-the-humanities-protocol',
    category: 'exam-zone',
    title: 'Mastering the Humanities',
    subtitle: 'The Grade Optimisation Protocol',
    description: 'Deconstruct the "hidden curriculum" of History, Geography, and Politics & Society to transform your strategic application and maximize your grade.',
    sectionsCount: 6,
    tags: ['Subject Strategy', 'Exam Tactics'],
  },
  {
    id: 'digital-distraction-protocol',
    category: 'exam-zone',
    title: 'Creating Barriers for Digital Distractions',
    subtitle: 'The Cognitive Sovereignty Protocol',
    description: 'A blueprint for reclaiming your focus from the attention economy, using neuroscience-backed hardware, software, and behavioral barriers.',
    sectionsCount: 7,
    tags: ['Productivity', 'Performance Psych'],
  },
] as const;

export const ALL_COURSES: CourseData[] = COURSE_DEFINITIONS.map(course => {
  const colors = categoryColorMap[course.category] || {
    gradient: 'bg-gradient-to-tr from-stone-100 via-white to-stone-50',
    accentColor: 'text-stone-700',
    auraColor: 'hover:shadow-[0_20px_50px_rgba(71,85,105,0.15)]'
  };
  return {
    ...course,
    ...colors,
  };
});

const UserProfile = ({ user, onLogout, darkMode, setDarkMode }: { user: SessionUser, onLogout: () => void, darkMode: boolean, setDarkMode: (v: boolean) => void }) => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div className="relative">
      <button onClick={() => setIsOpen(!isOpen)} className="flex items-center gap-2">
        <img src={`https://api.dicebear.com/7.x/adventurer/svg?seed=${user.avatar}`} alt="User Avatar" className="w-10 h-10 rounded-full bg-stone-200" />
      </button>
      <AnimatePresence>
        {isOpen && (
          <MotionDiv
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            className="absolute top-full right-0 mt-2 w-64 bg-white/80 dark:bg-stone-900/80 backdrop-blur-2xl border border-stone-200/50 dark:border-white/10 rounded-2xl shadow-2xl p-4"
          >
            <div className="flex items-center gap-3 border-b border-stone-200/50 dark:border-white/10 pb-3 mb-3">
              <img src={`https://api.dicebear.com/7.x/adventurer/svg?seed=${user.avatar}`} alt="User Avatar" className="w-12 h-12 rounded-full bg-stone-200" />
              <div>
                <p className="font-bold text-stone-800 dark:text-white">{user.name}</p>
                <p className="text-xs text-stone-500">{user.isAdmin ? 'Admin' : 'Student'}</p>
              </div>
            </div>
            
            <button onClick={() => setDarkMode(!darkMode)} className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-stone-100 dark:hover:bg-white/5">
                <span className="text-sm font-medium text-stone-700 dark:text-stone-300">Theme</span>
                 <AnimatePresence mode="wait">
                    {darkMode ? (
                      <MotionDiv key="sun" initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }} transition={{ duration: 0.2 }}>
                        <Sun size={16} className="text-amber-400" />
                      </MotionDiv>
                    ) : (
                      <MotionDiv key="moon" initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }} transition={{ duration: 0.2 }}>
                        <Moon size={16} className="text-stone-600" />
                      </MotionDiv>
                    )}
                </AnimatePresence>
            </button>
            <button onClick={onLogout} className="w-full flex items-center gap-2 p-2 rounded-lg hover:bg-stone-100 dark:hover:bg-white/5 mt-1">
              <LogOut size={16} className="text-rose-500" />
              <span className="text-sm font-medium text-rose-500">Log Out</span>
            </button>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  )
}

const App: React.FC = () => {
  const [viewState, setViewState] = useState<'tree' | 'category' | 'module' | 'innovation-zone'>('tree');
  const [currentCategory, setCurrentCategory] = useState<CategoryType | null>(null);
  const [currentModuleId, setCurrentModuleId] = useState<string | null>(null);
  const [darkMode, setDarkMode] = useState(true);
  const [user, setUser] = useState<SessionUser | null>(null);
  const [userProgress, setUserProgress] = useState<UserProgress>({});
  const [isLoadingAuth, setIsLoadingAuth] = useState(true);

  // Set up the real-time auth listener
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser: FirebaseUser | null) => {
      if (firebaseUser) {
        // User is signed in. Fetch their profile and progress from Firestore
        const userDocRef = doc(db, "users", firebaseUser.uid);
        const progressDocRef = doc(db, "progress", firebaseUser.uid);
        
        try {
          const [userDoc, progressDoc] = await Promise.all([getDoc(userDocRef), getDoc(progressDocRef)]);

          if (userDoc.exists()) {
            const userData = userDoc.data();
            setUser({
              uid: firebaseUser.uid,
              name: userData.name,
              avatar: userData.avatar,
              isAdmin: userData.isAdmin || false,
            });
            if (progressDoc.exists()) {
              setUserProgress(progressDoc.data() as UserProgress);
            } else {
              setUserProgress({});
            }
          } else {
             // This can happen if user creation was interrupted. Log them out.
            await signOut(auth);
            setUser(null);
            setUserProgress({});
          }
        } catch (error) {
           console.error("Error fetching user data:", error);
           await signOut(auth);
        }

      } else {
        // User is signed out
        setUser(null);
        setUserProgress({});
      }
      setIsLoadingAuth(false);
    });

    return () => unsubscribe(); // Cleanup subscription on unmount
  }, []);

  // Sync dark mode state with document class
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const handleLoginSuccess = (loggedInUser: SessionUser) => {
    setUser(loggedInUser);
  };

  const handleLogout = async () => {
    // If the local admin is logging out, just clear the state
    if (user?.isAdmin && user.uid === 'admin-uid') {
        setUser(null);
        return;
    }
    // For Firebase users, sign out properly
    await signOut(auth);
  };

  const handleProgressUpdate = async (moduleId: string, newProgress: ModuleProgress) => {
    if (!user || user.isAdmin) return;

    const updatedProgress = { 
      ...userProgress, 
      [moduleId]: newProgress 
    };
    setUserProgress(updatedProgress); // Optimistic UI update

    try {
      const progressDocRef = doc(db, "progress", user.uid);
      await setDoc(progressDocRef, updatedProgress, { merge: true });
    } catch (error) {
      console.error("Failed to save progress:", error);
      // Optionally, revert the UI update here
    }
  };
  
  const handleSelectCategory = (category: CategoryType) => {
    setCurrentCategory(category);
    setViewState('category');
  };

  const handleSelectModule = (moduleId: string) => {
    setCurrentModuleId(moduleId);
    setViewState('module');
  };

  const handleGoToInnovationZone = () => {
    setViewState('innovation-zone');
  };

  const handleBackToTree = () => {
    setCurrentCategory(null);
    setViewState('tree');
  };

  const handleBackToCategory = () => {
    setCurrentModuleId(null);
    if (currentCategory) {
      setViewState('category');
    } else {
      setViewState('tree');
    }
  };

  const categoryTitles: Record<CategoryType, string> = {
    'architecture-mindset': 'The Architecture of your Mindset',
    'science-growth': 'The Science of Growth',
    'learning-cheat-codes': 'The Science of Learning Effectively',
    'the-shield': 'The Shield',
    'the-launchpad': 'The Launchpad',
    'exam-zone': 'Exam Strategy and Points Maximisation',
    'subject-specific-science': 'Subject Specific Science'
  };
  
  const renderContent = () => {
    if (isLoadingAuth) {
        return <LoadingSpinner />;
    }

    if (!user) {
      return (
        <div className="flex flex-col items-center justify-center min-h-screen text-center p-8 relative">
           <h1 className="font-serif text-6xl md:text-8xl text-black dark:text-white tracking-tighter leading-none italic font-bold dark:drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]">
            Learning Lab
          </h1>
          <p className="mt-4 text-stone-500 dark:text-stone-400">Please log in to access the modules.</p>
           
           <button 
            onClick={() => handleLoginSuccess({ uid: 'dev-student', name: 'Dev User', avatar: 'Casper', isAdmin: false })}
            className="fixed bottom-4 left-4 px-3 py-1 bg-red-600/20 text-red-400 border border-red-600/30 rounded-full text-xs font-mono hover:bg-red-600/40"
          >
            DEV: Skip Login
          </button>
        </div>
      );
    }
    
    if (user.isAdmin) {
      return <AdminDashboard allCourses={ALL_COURSES} />;
    }

    if (viewState === 'tree') {
      return <KnowledgeTree 
        onSelectCategory={handleSelectCategory} 
        onGoToInnovationZone={handleGoToInnovationZone} 
        allCourses={ALL_COURSES}
        onSelectModule={handleSelectModule}
        categoryTitles={categoryTitles}
        userProgress={userProgress}
      />;
    }

    if (viewState === 'category' && currentCategory) {
      const categoryCourses = ALL_COURSES.filter(c => c.category === currentCategory);
      return (
        <Library 
          title={categoryTitles[currentCategory]}
          courses={categoryCourses} 
          onSelectCourse={handleSelectModule}
          onBack={handleBackToTree}
          userProgress={userProgress}
        />
      );
    }
    
    if (viewState === 'innovation-zone') {
        return (
          <Suspense fallback={<LoadingSpinner />}>
            <InnovationZone onBack={handleBackToTree} />
          </Suspense>
        );
    }

    if (viewState === 'module' && currentModuleId) {
      const ModuleComponent = moduleComponents[currentModuleId];
      if (ModuleComponent) {
        return (
          <Suspense fallback={<LoadingSpinner />}>
            <ModuleComponent 
              onBack={handleBackToCategory} 
              progress={userProgress[currentModuleId] || { unlockedSection: 0 }}
              onProgressUpdate={(p) => handleProgressUpdate(currentModuleId, p)}
            />
          </Suspense>
        );
      }
      return null;
    }

    return null;
  };

  return (
    <div className="min-h-screen bg-[#FDFCFB] dark:bg-[radial-gradient(ellipse_at_center,_#111_0%,#0A0A0B_80%)] transition-colors duration-500">
      <div className="fixed top-6 right-6 z-[100]">
        {user ? (
          <UserProfile user={user} onLogout={handleLogout} darkMode={darkMode} setDarkMode={setDarkMode} />
        ) : !isLoadingAuth ? (
          <Auth onLoginSuccess={handleLoginSuccess} />
        ) : null}
      </div>
      
      {renderContent()}
    </div>
  );
};

export default App;
