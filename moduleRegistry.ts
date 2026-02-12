/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { lazy } from 'react';
import { ModuleProgress } from './types';

type ModuleComponent = React.LazyExoticComponent<React.FC<{
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}>>;

export const InnovationZone = lazy(() => import('./components/InnovationZone'));

export const moduleComponents: { [key: string]: ModuleComponent } = {
  'agency-protocol': lazy(() => import('./components/AgencyProtocolModule')),
  'hope-protocol': lazy(() => import('./components/HopeProtocolModule')),
  'affirming-values-protocol': lazy(() => import('./components/AffirmingValuesModule')),
  'best-possible-self-protocol': lazy(() => import('./components/BestPossibleSelfModule')),
  'grammar-of-grit-protocol': lazy(() => import('./components/TheGrammarOfGritModule')),
  'social-capital-protocol': lazy(() => import('./components/SocialCapitalModule')),
  'agency-architecture-protocol': lazy(() => import('./components/AgencyArchitectureModule')),
  'strategic-advantage-protocol': lazy(() => import('./components/StrategicAdvantageModule')),
  'self-efficacy-protocol': lazy(() => import('./components/SelfEfficacyModule')),
  'illusion-of-competence-protocol': lazy(() => import('./components/IllusionOfCompetenceModule')),
  'procrastination-protocol': lazy(() => import('./components/ProcrastinationModule')),
  'neuroplasticity-protocol': lazy(() => import('./components/NeuroplasticityProtocolModule')),
  'myelin-manual-protocol': lazy(() => import('./components/TheMyelinManualModule')),
  'praise-protocol': lazy(() => import('./components/ThePraiseProtocolModule')),
  'effective-struggle-protocol': lazy(() => import('./components/EffectiveStruggleAndGrowthModule')),
  'science-of-making-mistakes-protocol': lazy(() => import('./components/TheScienceOfMakingMistakesModule')),
  'autodidact-engine-protocol': lazy(() => import('./components/TheAutodidactsEngineModule')),
  'power-of-yet-protocol': lazy(() => import('./components/ThePowerOfYetModule')),
  'cognitive-baseline-protocol': lazy(() => import('./components/TheCognitiveBaselineModule')),
  'mastering-active-recall-protocol': lazy(() => import('./components/MasteringActiveRecallModule')),
  'mastering-spaced-repetition-protocol': lazy(() => import('./components/MasteringSpacedRepetitionModule')),
  'mastering-interleaving-protocol': lazy(() => import('./components/MasteringInterleavingModule')),
  'cognitive-architecture-protocol': lazy(() => import('./components/TheCognitiveArchitectureModule')),
  'elaborative-interrogation-protocol': lazy(() => import('./components/ElaborativeInterrogationModule')),
  'cognitive-endurance-protocol': lazy(() => import('./components/CognitiveEnduranceModule')),
  'mental-modelling-protocol': lazy(() => import('./components/MentalModellingModule')),
  'bimodal-brain-protocol': lazy(() => import('./components/BimodalBrainModule')),
  'leaving-cert-strategy-protocol': lazy(() => import('./components/LeavingCertStrategyModule')),
  'reverse-engineering-protocol': lazy(() => import('./components/ReverseEngineeringModule')),
  'achieving-effective-learning-outcomes-protocol': lazy(() => import('./components/AchievingEffectiveLearningOutcomesModule')),
  'exam-hall-strategies-protocol': lazy(() => import('./components/ExamHallStrategiesModule')),
  'exam-crisis-management-protocol': lazy(() => import('./components/ExamCrisisManagementModule')),
  'growth-mindset-protocol': lazy(() => import('./components/GrowthMindsetModule')),
  'controllable-variables-protocol': lazy(() => import('./components/ControllableVariablesModule')),
  'reframing-progress-protocol': lazy(() => import('./components/ReframingProgressModule')),
  'learning-math-protocol': lazy(() => import('./components/LearningMathModule')),
  'linking-study-future-goals-protocol': lazy(() => import('./components/LinkingStudyFutureGoalsModule')),
  'game-day-protocol': lazy(() => import('./components/GameDayModule')),
  'reframing-catastrophic-thoughts-protocol': lazy(() => import('./components/CatastrophicThinkingModule')),
  'mastering-foreign-languages-protocol': lazy(() => import('./components/LanguageMasteryModule')),
  'emotional-intelligence-protocol': lazy(() => import('./components/EmotionalIntelligenceModule')),
  'connecting-education-to-goals-protocol': lazy(() => import('./components/ConnectingEducationToGoalsModule')),
  'mastering-the-sciences-protocol': lazy(() => import('./components/MasteringTheSciencesModule')),
  'mastering-the-humanities-protocol': lazy(() => import('./components/MasteringTheHumanitiesModule')),
  'mastering-english-protocol': lazy(() => import('./components/MasteringEnglishModule')),
  'mastering-business-protocol': lazy(() => import('./components/MasteringBusinessModule')),
  'applied-sciences-protocol': lazy(() => import('./components/AppliedSciencesModule')),
  'digital-distraction-protocol': lazy(() => import('./components/DigitalDistractionModule')),
  'mastering-the-creatives-protocol': lazy(() => import('./components/MasteringTheCreativesModule')),
  'points-optimization-protocol': lazy(() => import('./components/PointsOptimizationModule')),
};
