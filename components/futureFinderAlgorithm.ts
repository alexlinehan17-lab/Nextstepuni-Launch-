/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type CAOCourse, CAO_COURSES } from './futureFinderData';
import { type StudentSubjectProfile } from './subjectData';

// ─── Assessment Types ───────────────────────────────────────────────────────

export interface FutureFinderAnswers {
  // Q1: Interest areas (merged from old Q1+Q2)
  interestTags: string[];         // pick up to 5

  // Q2: Job scenarios (replaces dream job text)
  scenarioChoices: string[];      // pick 2-3 from 10 scenarios

  // Q3-5: Values (moved earlier, pills not sliders)
  salaryImportance: number;       // 1-5
  jobSecurityImportance: number;  // 1-5
  helpingOthersImportance: number;// 1-5

  // Q6-7: Work style
  workStyleTags: string[];        // pick 2-3
  teamPreference: 'team' | 'solo' | 'mix';

  // Q8: Study duration (replaces level)
  studyDuration: string[];        // '2' | '3' | '4+'

  // Q9-10: Location
  willingToRelocate: boolean;
  preferredRegions: string[];

  // Keep estimatedPoints for backward compat but don't ask for it
  estimatedPoints: number;
}

export interface RecommendationResult {
  course: CAOCourse;
  score: number;
  reasons: string[];
  scoreBreakdown: {
    interestScore: number;
    valuesScore: number;
    feasibilityScore: number;
  };
  subjectAlignment: 'strong' | 'partial' | 'none';
}

// ─── Scenario-to-Tag Mapping ────────────────────────────────────────────────

const SCENARIO_TAG_MAP: Record<string, string[]> = {
  'design-product': ['design', 'engineering', 'technology'],
  'investigate-science': ['science', 'healthcare', 'environment'],
  'help-difficult': ['healthcare', 'social-care', 'psychology'],
  'argue-case': ['law', 'politics', 'arts'],
  'build-fix': ['engineering', 'technology', 'agriculture'],
  'run-business': ['business', 'finance', 'leadership'],
  'create-content': ['media', 'design', 'arts'],
  'protect-environment': ['environment', 'science', 'agriculture'],
  'analyse-data': ['finance', 'technology', 'science'],
  'teach-inspire': ['education', 'sport', 'social-care'],
};

// ─── Scoring Helpers ────────────────────────────────────────────────────────

/** Sigmoid-like feasibility: 1 at target, drops off for unrealistic courses */
function feasibilitySigmoid(estimatedPoints: number, typicalPoints: number): number {
  // If course has no points requirement (PLC, apprenticeship), feasibility = 1.0
  if (typicalPoints === 0) return 1.0;
  const diff = estimatedPoints - typicalPoints;
  // Student has more than enough points — high score
  if (diff >= 0) return 1;
  // Stretch goal: within 50 points below — still decent
  if (diff >= -50) return 0.7 + (diff + 50) * (0.3 / 50);
  // Within 100 points — possible but challenging
  if (diff >= -100) return 0.3 + (diff + 100) * (0.4 / 50);
  // More than 100 below — unlikely but don't zero out
  return Math.max(0.05, 0.3 + (diff + 100) * (0.25 / 100));
}

/** Calculate how many student LC subjects match the course's subject bonus list */
function _subjectFitScore(profile: StudentSubjectProfile | null, course: CAOCourse): number {
  if (!profile || profile.subjects.length === 0 || course.subjectBonus.length === 0) return 0;
  const studentSubjects = new Set(profile.subjects.map(s => s.subjectName));
  let matches = 0;
  for (const bonus of course.subjectBonus) {
    if (studentSubjects.has(bonus)) matches++;
  }
  return matches / course.subjectBonus.length;
}

/** Determine subject alignment level */
function getSubjectAlignment(profile: StudentSubjectProfile | null, course: CAOCourse): 'strong' | 'partial' | 'none' {
  if (!profile || profile.subjects.length === 0 || course.subjectBonus.length === 0) return 'none';
  const studentSubjects = new Set(profile.subjects.map(s => s.subjectName));
  let matches = 0;
  for (const bonus of course.subjectBonus) {
    if (studentSubjects.has(bonus)) matches++;
  }
  const ratio = matches / course.subjectBonus.length;
  if (ratio >= 0.5) return 'strong';
  if (matches >= 1) return 'partial';
  return 'none';
}

/** Interest score: tag overlap + scenario bonus (45% weight) */
function computeInterestScore(answers: FutureFinderAnswers, course: CAOCourse): number {
  const userInterests = answers.interestTags;
  const courseTags = course.interestTags;

  // Tag overlap (weighted, not Jaccard — give more credit per match)
  const matchCount = userInterests.filter(t => courseTags.includes(t)).length;
  const interestBase = Math.min(matchCount / 3, 1); // 3+ matches = full score

  // Scenario bonus: map chosen scenarios to tags, check overlap with course
  const scenarioTags = new Set(answers.scenarioChoices.flatMap(s => SCENARIO_TAG_MAP[s] || []));
  const scenarioOverlap = courseTags.filter(t => scenarioTags.has(t)).length;
  const scenarioBonus = Math.min(scenarioOverlap / 2, 1) * 0.4; // up to 40% bonus

  const interestScore = Math.min(interestBase + scenarioBonus, 1);
  return interestScore;
}

/** Values alignment: maps user slider values to course properties (30% weight) */
function computeValuesScore(answers: FutureFinderAnswers, course: CAOCourse): number {
  let score = 0;
  let weights = 0;

  // Salary importance vs salary band
  const salaryW = answers.salaryImportance / 5;
  const salaryMatch = course.salaryBand === 'high' ? 1 : course.salaryBand === 'mid' ? 0.5 : 0.2;
  score += salaryW * salaryMatch;
  weights += salaryW;

  // Job security -> employability
  const securityW = answers.jobSecurityImportance / 5;
  const securityMatch = course.employability / 5;
  score += securityW * securityMatch;
  weights += securityW;

  // Helping others -> people-focused or social-care tags
  const helpW = answers.helpingOthersImportance / 5;
  const helpMatch = (
    course.workStyleTags.includes('people-focused') ||
    course.interestTags.includes('social-care') ||
    course.interestTags.includes('healthcare') ||
    course.interestTags.includes('education')
  ) ? 1 : 0.2;
  score += helpW * helpMatch;
  weights += helpW;

  // Work style alignment (weighted overlap, not Jaccard)
  if (answers.workStyleTags.length > 0) {
    const workMatches = answers.workStyleTags.filter(t => course.workStyleTags.includes(t)).length;
    const workStyleOverlap = Math.min(workMatches / 2, 1); // 2+ matches = full score
    score += workStyleOverlap;
    weights += 1;
  }

  // Team preference
  const teamMatch = (() => {
    if (answers.teamPreference === 'team') return course.workStyleTags.includes('team-based') ? 1 : 0.5;
    if (answers.teamPreference === 'solo') return course.workStyleTags.includes('independent') ? 1 : 0.5;
    return 0.7; // mix — moderate match for everything
  })();
  score += teamMatch * 0.5;
  weights += 0.5;

  return weights > 0 ? score / weights : 0;
}

/** Feasibility score: study duration match + points feasibility (25% weight) */
function computeFeasibilityScore(
  answers: FutureFinderAnswers,
  course: CAOCourse,
  autoPoints: number,
): number {
  // Study duration: map '1' -> [5], '2' -> [5, 6], '3' -> [7], '4+' -> [8]
  let durationScore = 1; // default: no penalty if nothing selected
  if (answers.studyDuration.length > 0) {
    const levelMap: Record<string, number[]> = {
      '1': [5],
      '2': [5, 6],
      '3': [7],
      '4+': [8],
    };
    const acceptedLevels = new Set(answers.studyDuration.flatMap(d => levelMap[d] || []));
    if (acceptedLevels.size > 0) {
      durationScore = acceptedLevels.has(course.level) ? 1 : 0.3;
    }
  }

  // Points: use auto-computed points from profile, NOT user-entered
  const pointsToUse = autoPoints > 0 ? autoPoints : answers.estimatedPoints;
  const pointsScore = feasibilitySigmoid(pointsToUse, course.typicalPoints);

  // Combine: 50% duration, 50% points
  return durationScore * 0.5 + pointsScore * 0.5;
}

// ─── Reason Generation ──────────────────────────────────────────────────────

function generateReasons(
  answers: FutureFinderAnswers,
  profile: StudentSubjectProfile | null,
  course: CAOCourse,
  autoPoints: number,
  subjectAlignment: 'strong' | 'partial' | 'none',
): string[] {
  const reasons: string[] = [];

  // Interest match — specific tags
  const matchingInterests = answers.interestTags.filter(t => course.interestTags.includes(t));
  if (matchingInterests.length >= 2) {
    const formatted = matchingInterests.slice(0, 3).map(t => t.replace(/-/g, ' ')).join(', ');
    reasons.push(`Strong match with your interest in ${formatted} \u2014 this course covers all of them`);
  } else if (matchingInterests.length === 1) {
    const formatted = matchingInterests[0].replace(/-/g, ' ');
    reasons.push(`Matches your interest in ${formatted}`);
  }

  // Scenario match
  const scenarioTags = new Set(answers.scenarioChoices.flatMap(s => SCENARIO_TAG_MAP[s] || []));
  const scenarioOverlap = course.interestTags.filter(t => scenarioTags.has(t)).length;
  if (scenarioOverlap >= 2) {
    reasons.push('Closely aligned with the work scenarios you chose');
  }

  // Salary / values
  if (answers.salaryImportance >= 4 && course.salaryBand === 'high') {
    reasons.push('You said earning well matters \u2014 graduates from this course earn above average');
  }
  if (answers.jobSecurityImportance >= 4 && course.employability >= 4) {
    reasons.push('High employability and job security, which you ranked highly');
  }
  if (answers.helpingOthersImportance >= 4 &&
    (course.interestTags.includes('healthcare') || course.interestTags.includes('social-care') || course.interestTags.includes('education'))) {
    reasons.push('Aligned with your desire to help others and make a difference');
  }

  // Work style
  const matchingStyles = answers.workStyleTags.filter(t => course.workStyleTags.includes(t));
  if (matchingStyles.length >= 2) {
    const formatted = matchingStyles.slice(0, 2).map(t => t.replace(/-/g, ' ')).join(' and ');
    reasons.push(`Suits your ${formatted} work style`);
  } else if (matchingStyles.length === 1) {
    const formatted = matchingStyles[0].replace(/-/g, ' ');
    reasons.push(`Suits your ${formatted} work style`);
  }

  // Pathway type reasons
  if (course.pathwayType === 'plc') {
    reasons.push('No CAO points required \u2014 open entry with QQI certification');
  }
  if (course.pathwayType === 'apprenticeship') {
    reasons.push('Earn while you learn \u2014 paid from day one');
  }

  // Study duration
  if (answers.studyDuration.length > 0) {
    const levelMap: Record<string, number[]> = { '1': [5], '2': [5, 6], '3': [7], '4+': [8] };
    const acceptedLevels = new Set(answers.studyDuration.flatMap(d => levelMap[d] || []));
    if (acceptedLevels.has(course.level)) {
      const durationLabel = course.level === 5 ? '1 year' : course.level === 6 ? '1\u20132 years' : course.level === 7 ? '3 years' : '4+ years';
      reasons.push(`At ${durationLabel}, this fits your preferred study length`);
    }
  }

  // Points feasibility (skip for open-entry courses)
  if (course.typicalPoints > 0) {
    const pointsToUse = autoPoints > 0 ? autoPoints : answers.estimatedPoints;
    const pointsDiff = pointsToUse - course.typicalPoints;
    if (pointsDiff >= 50) {
      reasons.push('Well within your points range');
    } else if (pointsDiff >= 0) {
      reasons.push('Within your points range');
    } else if (pointsDiff >= -30) {
      reasons.push('A reachable stretch goal for your points');
    } else if (pointsDiff >= -60) {
      reasons.push('An ambitious target \u2014 achievable with strong results');
    }
  }

  // Region
  if (answers.preferredRegions.length > 0 && answers.preferredRegions.includes(course.region)) {
    const regionLabel = course.region.charAt(0).toUpperCase() + course.region.slice(1);
    reasons.push(`Located in ${regionLabel}, one of your preferred regions`);
  }

  // Subject alignment — informational, not scored
  if (profile && profile.subjects.length > 0 && course.subjectBonus.length > 0) {
    const studentSubjects = new Set(profile.subjects.map(s => s.subjectName));
    const matchingSubs = course.subjectBonus.filter(s => studentSubjects.has(s));
    if (subjectAlignment === 'strong' && matchingSubs.length >= 2) {
      reasons.push(`Your ${matchingSubs.slice(0, 2).join(' and ')} subjects are a strong foundation for this`);
    } else if (subjectAlignment === 'strong' && matchingSubs.length === 1) {
      reasons.push(`Your ${matchingSubs[0]} background is a strong foundation for this`);
    } else if (subjectAlignment === 'partial' && matchingSubs.length >= 1) {
      reasons.push(`Builds on your ${matchingSubs[0]} studies`);
    }
  }

  // Career paths (add only if we have room)
  if (reasons.length < 5 && course.careerPaths.length > 0) {
    reasons.push(`Career paths include ${course.careerPaths.slice(0, 2).join(' and ')}`);
  }

  // Return up to 6 most specific reasons
  return reasons.slice(0, 6);
}

// ─── Main Algorithm ─────────────────────────────────────────────────────────

export function runFutureFinderAssessment(
  answers: FutureFinderAnswers,
  profile: StudentSubjectProfile | null,
  autoPoints?: number,
): RecommendationResult[] {
  const results: RecommendationResult[] = [];
  const pts = autoPoints || answers.estimatedPoints || 350;

  for (const course of CAO_COURSES) {
    // Study duration filter: map '1' -> [5], '2' -> [5, 6], '3' -> [7], '4+' -> [8]
    if (answers.studyDuration && answers.studyDuration.length > 0) {
      const levelMap: Record<string, number[]> = { '1': [5], '2': [5, 6], '3': [7], '4+': [8] };
      const acceptedLevels = new Set(answers.studyDuration.flatMap(d => levelMap[d] || []));
      // Only filter if student didn't select all options (which means "show all")
      if (acceptedLevels.size > 0 && acceptedLevels.size < 4 && !acceptedLevels.has(course.level)) {
        continue;
      }
    }

    // Interest score (45%)
    const interestScore = computeInterestScore(answers, course);

    // Values alignment (30%)
    const valuesScoreVal = computeValuesScore(answers, course);

    // Feasibility (25%)
    const feasibilityScore = computeFeasibilityScore(answers, course, pts);

    // Subject alignment (informational, not scored)
    const subjectAlignment = getSubjectAlignment(profile, course);

    // Weighted total
    let totalScore = (
      interestScore * 0.45 +
      valuesScoreVal * 0.30 +
      feasibilityScore * 0.25
    );

    // Geographic modifier
    if (answers.preferredRegions.length > 0 && !answers.willingToRelocate) {
      if (answers.preferredRegions.includes(course.region)) {
        totalScore *= 1.2;
      } else {
        totalScore *= 0.7;
      }
    } else if (answers.preferredRegions.length > 0 && answers.willingToRelocate) {
      // Mild boost for preferred regions even when willing to relocate
      if (answers.preferredRegions.includes(course.region)) {
        totalScore *= 1.1;
      }
    }

    // Cap at 1
    totalScore = Math.min(totalScore, 1);

    const reasons = generateReasons(answers, profile, course, pts, subjectAlignment);

    results.push({
      course,
      score: totalScore,
      reasons,
      scoreBreakdown: {
        interestScore,
        valuesScore: valuesScoreVal,
        feasibilityScore,
      },
      subjectAlignment,
    });
  }

  // Sort by score descending
  results.sort((a, b) => b.score - a.score);

  return results;
}

// ─── Assessment Questions ───────────────────────────────────────────────────

export interface AssessmentQuestion {
  id: string;
  dimension: string;
  question: string;
  subtitle?: string;
  type: 'multi-select' | 'single-select' | 'slider' | 'text' | 'rank' | 'boolean' | 'number';
  options?: { value: string; label: string }[];
  min?: number;
  max?: number;
  maxSelections?: number;
}

export const ASSESSMENT_QUESTIONS: AssessmentQuestion[] = [
  // Q1: Interests (merged)
  {
    id: 'interestTags', dimension: 'Interest', type: 'multi-select', maxSelections: 5,
    question: 'Which areas genuinely interest you?',
    subtitle: 'Pick up to 5 \u2014 go with your gut.',
    options: [
      { value: 'technology', label: 'Technology & Computing' },
      { value: 'science', label: 'Science & Discovery' },
      { value: 'healthcare', label: 'Healthcare & Medicine' },
      { value: 'business', label: 'Business & Enterprise' },
      { value: 'finance', label: 'Finance & Numbers' },
      { value: 'engineering', label: 'Engineering & Building' },
      { value: 'arts', label: 'Arts & Humanities' },
      { value: 'media', label: 'Media & Communication' },
      { value: 'education', label: 'Teaching & Education' },
      { value: 'law', label: 'Law & Justice' },
      { value: 'environment', label: 'Environment & Sustainability' },
      { value: 'sport', label: 'Sport & Fitness' },
      { value: 'psychology', label: 'Psychology & Mind' },
      { value: 'social-care', label: 'Social Care & Community' },
      { value: 'design', label: 'Design & Visual' },
    ],
  },

  // Q2: Scenarios (replaces dream job)
  {
    id: 'scenarioChoices', dimension: 'Interest', type: 'multi-select', maxSelections: 3,
    question: 'Which of these sound like something you\'d enjoy?',
    subtitle: 'Pick 2\u20133 that appeal to you.',
    options: [
      { value: 'design-product', label: 'Designing something people use every day' },
      { value: 'investigate-science', label: 'Investigating how things work at a molecular level' },
      { value: 'help-difficult', label: 'Helping someone through a really difficult time' },
      { value: 'argue-case', label: 'Arguing a case and changing someone\'s mind' },
      { value: 'build-fix', label: 'Building or fixing something with your hands' },
      { value: 'run-business', label: 'Running your own business or project' },
      { value: 'create-content', label: 'Creating content that thousands of people see' },
      { value: 'protect-environment', label: 'Protecting the environment or wildlife' },
      { value: 'analyse-data', label: 'Analysing data to spot patterns others miss' },
      { value: 'teach-inspire', label: 'Teaching or coaching someone to be their best' },
    ],
  },

  // Q3: Salary (pill, not slider)
  {
    id: 'salaryImportance', dimension: 'Values', type: 'slider', min: 1, max: 5,
    question: 'How important is earning well?',
    subtitle: 'There\'s no wrong answer.',
  },

  // Q4: Job security (pill)
  {
    id: 'jobSecurityImportance', dimension: 'Values', type: 'slider', min: 1, max: 5,
    question: 'How important is job security?',
    subtitle: 'Knowing you\'ll always have work.',
  },

  // Q5: Helping others (pill)
  {
    id: 'helpingOthersImportance', dimension: 'Values', type: 'slider', min: 1, max: 5,
    question: 'How important is helping others or making a difference?',
  },

  // Q6: Work style
  {
    id: 'workStyleTags', dimension: 'Work Style', type: 'multi-select', maxSelections: 3,
    question: 'How do you like to work?',
    subtitle: 'Pick 2\u20133 that feel right.',
    options: [
      { value: 'hands-on', label: 'Hands-on \u2014 building, making, doing' },
      { value: 'analytical', label: 'Analytical \u2014 solving problems with logic' },
      { value: 'creative', label: 'Creative \u2014 imagining new ideas' },
      { value: 'people-focused', label: 'People-focused \u2014 communicating, helping' },
      { value: 'research-driven', label: 'Research-driven \u2014 deep investigation' },
      { value: 'structured', label: 'Structured \u2014 clear rules and processes' },
      { value: 'flexible', label: 'Flexible \u2014 variety and freedom' },
      { value: 'leadership', label: 'Leadership \u2014 organising and leading' },
    ],
  },

  // Q7: Team preference
  {
    id: 'teamPreference', dimension: 'Work Style', type: 'single-select',
    question: 'Do you prefer working in a team or on your own?',
    options: [
      { value: 'team', label: 'In a team \u2014 I thrive with others around' },
      { value: 'solo', label: 'On my own \u2014 I do my best work solo' },
      { value: 'mix', label: 'A mix of both' },
    ],
  },

  // Q8: Study duration (replaces level — removes hierarchy)
  {
    id: 'studyDuration', dimension: 'Practical', type: 'multi-select',
    question: 'How long would you like to study for?',
    subtitle: 'You can pick more than one.',
    options: [
      { value: '1', label: '1 year \u2014 fast-track to a career or progression' },
      { value: '2', label: '1\u20132 years \u2014 get working sooner' },
      { value: '3', label: '3 years \u2014 a solid foundation' },
      { value: '4+', label: '4+ years \u2014 deep specialist knowledge' },
    ],
  },

  // Q9: Location
  {
    id: 'willingToRelocate', dimension: 'Location', type: 'boolean',
    question: 'Are you open to studying anywhere in Ireland?',
  },

  // Q10: Regions (conditional)
  {
    id: 'preferredRegions', dimension: 'Location', type: 'multi-select', maxSelections: 3,
    question: 'Which areas would you prefer?',
    subtitle: 'Pick up to 3.',
    options: [
      { value: 'dublin', label: 'Dublin' },
      { value: 'cork', label: 'Cork' },
      { value: 'galway', label: 'Galway' },
      { value: 'limerick', label: 'Limerick' },
      { value: 'midlands', label: 'Midlands' },
      { value: 'southeast', label: 'South East' },
      { value: 'northwest', label: 'North West' },
      { value: 'southwest', label: 'South West' },
    ],
  },
];
