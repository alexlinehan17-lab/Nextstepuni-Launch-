export interface JourneyStage {
  id: string;
  name: string;
  minimumModules: number;
  description: string;
}

export const JOURNEY_STAGES: JourneyStage[] = [
  { id: 'trailhead', name: 'Trailhead', minimumModules: 0, description: 'Lay the first foundations.' },
  { id: 'builder', name: 'Builder', minimumModules: 2, description: 'Turn progress into a place of your own.' },
  { id: 'settler', name: 'Settler', minimumModules: 6, description: 'Build a recognisable corner of the island.' },
  { id: 'pathfinder', name: 'Pathfinder', minimumModules: 14, description: 'Open routes and shape a larger settlement.' },
  { id: 'township', name: 'Township', minimumModules: 27, description: 'Grow a thriving, personal landscape.' },
  { id: 'landmark', name: 'Landmark', minimumModules: 40, description: 'Create an island worth returning to.' },
];

export interface JourneyProgressionInput {
  completedModules: number;
  nonStarterPlacements: number;
  claimedRewards: number;
  inventoryItems: number;
}

export interface FoundationStep {
  id: string;
  label: string;
  detail: string;
  complete: boolean;
}

export function getJourneyProgress(input: JourneyProgressionInput) {
  let stageIndex = 0;
  for (let index = JOURNEY_STAGES.length - 1; index >= 0; index -= 1) {
    if (input.completedModules >= JOURNEY_STAGES[index].minimumModules) {
      stageIndex = index;
      break;
    }
  }
  const stage = JOURNEY_STAGES[stageIndex];
  const nextStage = JOURNEY_STAGES[stageIndex + 1] ?? null;
  const range = nextStage ? nextStage.minimumModules - stage.minimumModules : 1;
  const progress = nextStage
    ? Math.min(1, (input.completedModules - stage.minimumModules) / range)
    : 1;

  const foundationSteps: FoundationStep[] = [
    { id: 'arrive', label: 'Find your island', detail: 'Set a North Star and open Journey.', complete: true },
    { id: 'learn', label: 'Make the first move', detail: 'Complete your first learning module.', complete: input.completedModules >= 1 },
    { id: 'reward', label: 'Earn something real', detail: 'Claim your first island reward.', complete: input.claimedRewards >= 1 },
    { id: 'place', label: 'Choose where it belongs', detail: 'Place a new object in Build Mode.', complete: input.nonStarterPlacements >= 1 },
    { id: 'shape', label: 'Make it yours', detail: 'Place three earned or purchased objects.', complete: input.nonStarterPlacements >= 3 },
  ];

  return {
    stage,
    nextStage,
    progress,
    modulesToNext: nextStage ? Math.max(0, nextStage.minimumModules - input.completedModules) : 0,
    foundationSteps,
    foundationComplete: foundationSteps.every(step => step.complete),
    foundationCompletedCount: foundationSteps.filter(step => step.complete).length,
    unplacedCount: input.inventoryItems,
  };
}
