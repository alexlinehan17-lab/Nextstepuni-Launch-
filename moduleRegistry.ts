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

// Factory for data-driven subject modules (all share a single SubjectModule component)
function createSubjectModule(subjectId: string): ModuleComponent {
  return lazy(async () => {
    const { createSubjectModuleComponent } = await import('./components/SubjectModule');
    return { default: createSubjectModuleComponent(subjectId) as any };
  });
}

export const InnovationZone = lazy(() => import('./components/InnovationZone'));

export const moduleComponents: { [key: string]: ModuleComponent } = {
  'agency-protocol': lazy(() => import('./components/AgencyProtocolModule')),
  'hope-protocol': lazy(() => import('./components/HopeProtocolModule')),
  'affirming-values-protocol': lazy(() => import('./components/AffirmingValuesModule')),
  'best-possible-self-protocol': lazy(() => import('./components/BestPossibleSelfModule')),
  'grammar-of-grit-protocol': lazy(() => import('./components/TheGrammarOfGritModule')),
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
  'mastering-the-sciences-protocol': lazy(() => import('./components/MasteringTheSciencesModule')),
  'mastering-the-humanities-protocol': lazy(() => import('./components/MasteringTheHumanitiesModule')),
  'mastering-english-protocol': lazy(() => import('./components/MasteringEnglishModule')),
  'mastering-business-protocol': lazy(() => import('./components/MasteringBusinessModule')),
  'applied-sciences-protocol': lazy(() => import('./components/AppliedSciencesModule')),
  'digital-distraction-protocol': lazy(() => import('./components/DigitalDistractionModule')),
  'mastering-the-creatives-protocol': lazy(() => import('./components/MasteringTheCreativesModule')),
  'points-optimization-protocol': lazy(() => import('./components/PointsOptimizationModule')),
  'learning-radar-protocol': lazy(() => import('./components/TheLearningRadarModule')),
  'note-taking-paradox-protocol': lazy(() => import('./components/TheNoteTakingParadoxModule')),
  'teaching-effect-protocol': lazy(() => import('./components/TheTeachingEffectModule')),
  'cognitive-load-protocol': lazy(() => import('./components/TheCognitiveLoadModule')),
  'implementation-protocol': lazy(() => import('./components/TheImplementationProtocolModule')),
  'context-effect-protocol': lazy(() => import('./components/TheContextEffectModule')),
  // Per-subject modules (data-driven via SubjectModule.tsx)
  'subject-english-protocol': createSubjectModule('english'),
  'subject-irish-protocol': createSubjectModule('irish'),
  'subject-french-protocol': createSubjectModule('french'),
  'subject-german-protocol': createSubjectModule('german'),
  'subject-spanish-protocol': createSubjectModule('spanish'),
  'subject-italian-protocol': createSubjectModule('italian'),
  'subject-japanese-protocol': createSubjectModule('japanese'),
  'subject-mathematics-protocol': createSubjectModule('mathematics'),
  'subject-applied-maths-protocol': createSubjectModule('applied-maths'),
  'subject-physics-protocol': createSubjectModule('physics'),
  'subject-chemistry-protocol': createSubjectModule('chemistry'),
  'subject-biology-protocol': createSubjectModule('biology'),
  'subject-computer-science-protocol': createSubjectModule('computer-science'),
  'subject-ag-science-protocol': createSubjectModule('ag-science'),
  'subject-accounting-protocol': createSubjectModule('accounting'),
  'subject-business-protocol': createSubjectModule('business'),
  'subject-economics-protocol': createSubjectModule('economics'),
  'subject-history-protocol': createSubjectModule('history'),
  'subject-geography-protocol': createSubjectModule('geography'),
  'subject-politics-and-society-protocol': createSubjectModule('politics-and-society'),
  'subject-religious-education-protocol': createSubjectModule('religious-education'),
  'subject-classical-studies-protocol': createSubjectModule('classical-studies'),
  'subject-home-economics-protocol': createSubjectModule('home-economics'),
  'subject-construction-studies-protocol': createSubjectModule('construction-studies'),
  'subject-engineering-protocol': createSubjectModule('engineering'),
  'subject-dcg-protocol': createSubjectModule('dcg'),
  'subject-technology-protocol': createSubjectModule('technology'),
  'subject-art-protocol': createSubjectModule('art'),
  'subject-music-protocol': createSubjectModule('music'),
};
