import type { CurriculumLevel } from './authUtils';

// Shared by the Launchpad and its nested tool boundary to avoid a copy flash.
const TOOL_LOADING_LABELS: Record<string, string> = {
  journey: 'Opening your academic journey',
  'cao-simulator': 'Opening Points Passport',
  planner: 'Opening your planner',
  'war-room': 'Opening War Room',
  comeback: 'Opening Comeback Engine',
  'future-finder': 'Opening Future Finder',
  'future-finder-revamped': 'Opening Future Finder',
  'syllabus-xray': 'Opening War Room',
  'points-passport': 'Opening Points Passport',
  'college-compass': 'Opening College Compass',
  'catch-up-lane': 'Opening Catch-Up Lane',
  'mark-bank': 'Opening Mark Bank',
  'paper-trail': 'Opening Paper Trail',
  'topic-atlas': 'Opening Topic Atlas',
  'diagram-vault': 'Opening Diagram Vault',
  'answer-architect': 'Opening Answer Architect',
  'definition-drill': 'Opening Definition Drill',
  'coursework-companion': 'Opening Coursework Companion',
  'oral-trainer': 'Opening Irish Oral Trainer',
  'examiners-chair': 'Opening The Examiner’s Chair',
  'command-word-reflex': 'Opening Command-Word Reflex',
  'how-they-did-it': 'Opening How They Did It',
  'your-possible-life': 'Opening Your Possible Life',
  'career-paths': 'Opening Your Possible Life',
};

export function getToolLoadingLabel(tool?: string | null, curriculumLevel?: CurriculumLevel): string {
  if (tool === 'future-finder' && curriculumLevel === 'junior') return 'Opening Subject Explorer';
  return tool && Object.prototype.hasOwnProperty.call(TOOL_LOADING_LABELS, tool) ? TOOL_LOADING_LABELS[tool] : 'Opening Launchpad';
}
