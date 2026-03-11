/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type CAOCourse, CAO_COURSES } from './futureFinderData';
import { type StudentSubjectProfile, LC_SUBJECTS } from './subjectData';

// ─── Assessment Types ───────────────────────────────────────────────────────

export interface FutureFinderAnswers {
  // Interest / passion (Q1-3)
  interestTags: string[];         // Q1: pick up to 5 interest areas
  activityRankings: string[];     // Q2: rank top 3 activities
  dreamJobKeywords: string;       // Q3: free-text dream job description

  // Work style (Q4-5)
  workStyleTags: string[];        // Q4: pick 2-3 work styles
  teamPreference: 'team' | 'solo' | 'mix'; // Q5: team vs solo

  // Career values (Q6-8)
  salaryImportance: number;       // Q6: 1-5 slider
  jobSecurityImportance: number;  // Q7: 1-5 slider
  helpingOthersImportance: number;// Q8: 1-5 slider

  // Geographic preference (Q9-10)
  willingToRelocate: boolean;     // Q9: yes/no
  preferredRegions: string[];     // Q10: pick preferred regions

  // Course level & feasibility (Q11-12)
  preferredLevels: (6 | 7 | 8)[]; // Q11: which NFQ levels
  estimatedPoints: number;         // Q12: realistic points estimate
}

export interface RecommendationResult {
  course: CAOCourse;
  score: number;
  reasons: string[];
}

// ─── Scoring Helpers ────────────────────────────────────────────────────────

/** Jaccard-like overlap: |A ∩ B| / |A ∪ B|, returns 0-1 */
function tagOverlap(userTags: string[], courseTags: string[]): number {
  if (userTags.length === 0 && courseTags.length === 0) return 0;
  const setA = new Set(userTags);
  const setB = new Set(courseTags);
  let intersection = 0;
  for (const tag of setA) {
    if (setB.has(tag)) intersection++;
  }
  const union = new Set([...setA, ...setB]).size;
  return union === 0 ? 0 : intersection / union;
}

/** Sigmoid-like feasibility: 1 at target, drops off for unrealistic courses */
function feasibilitySigmoid(estimatedPoints: number, typicalPoints: number): number {
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
function subjectFitScore(profile: StudentSubjectProfile | null, course: CAOCourse): number {
  if (!profile || profile.subjects.length === 0 || course.subjectBonus.length === 0) return 0;
  const studentSubjects = new Set(profile.subjects.map(s => s.subjectName));
  let matches = 0;
  for (const bonus of course.subjectBonus) {
    if (studentSubjects.has(bonus)) matches++;
  }
  return matches / course.subjectBonus.length;
}

/** Values alignment: maps user slider values to course properties */
function valuesScore(answers: FutureFinderAnswers, course: CAOCourse): number {
  let score = 0;
  let weights = 0;

  // Salary importance vs salary band
  const salaryW = answers.salaryImportance / 5;
  const salaryMatch = course.salaryBand === 'high' ? 1 : course.salaryBand === 'mid' ? 0.5 : 0.2;
  score += salaryW * salaryMatch;
  weights += salaryW;

  // Job security → employability
  const securityW = answers.jobSecurityImportance / 5;
  const securityMatch = course.employability / 5;
  score += securityW * securityMatch;
  weights += securityW;

  // Helping others → people-focused or social-care tags
  const helpW = answers.helpingOthersImportance / 5;
  const helpMatch = (
    course.workStyleTags.includes('people-focused') ||
    course.interestTags.includes('social-care') ||
    course.interestTags.includes('healthcare') ||
    course.interestTags.includes('education')
  ) ? 1 : 0.2;
  score += helpW * helpMatch;
  weights += helpW;

  // Work style alignment
  const workStyleOverlap = tagOverlap(answers.workStyleTags, course.workStyleTags);
  score += workStyleOverlap;
  weights += 1;

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

/** Extract keywords from dream job text and check against course data */
function dreamJobBonus(dreamJob: string, course: CAOCourse): number {
  if (!dreamJob.trim()) return 0;
  const words = dreamJob.toLowerCase().split(/\s+/).filter(w => w.length > 2);
  const courseText = [
    course.title, course.description, ...course.careerPaths, ...course.interestTags
  ].join(' ').toLowerCase();
  let matches = 0;
  for (const word of words) {
    if (courseText.includes(word)) matches++;
  }
  return words.length > 0 ? Math.min(matches / words.length, 1) : 0;
}

// ─── Reason Generation ──────────────────────────────────────────────────────

function generateReasons(
  answers: FutureFinderAnswers,
  profile: StudentSubjectProfile | null,
  course: CAOCourse,
): string[] {
  const reasons: string[] = [];

  // Interest match
  const matchingInterests = answers.interestTags.filter(t => course.interestTags.includes(t));
  if (matchingInterests.length > 0) {
    const formatted = matchingInterests.slice(0, 2).map(t => t.replace(/-/g, ' ')).join(' and ');
    reasons.push(`Matches your interest in ${formatted}`);
  }

  // Subject fit
  if (profile) {
    const studentSubjects = new Set(profile.subjects.map(s => s.subjectName));
    const matchingSubs = course.subjectBonus.filter(s => studentSubjects.has(s));
    if (matchingSubs.length >= 2) {
      reasons.push(`Strong fit with your ${matchingSubs.slice(0, 2).join(' and ')} background`);
    } else if (matchingSubs.length === 1) {
      reasons.push(`Builds on your ${matchingSubs[0]} studies`);
    }
  }

  // Points feasibility
  const pointsDiff = answers.estimatedPoints - course.typicalPoints;
  if (pointsDiff >= 50) {
    reasons.push('Well within your points range');
  } else if (pointsDiff >= 0) {
    reasons.push('Within your points range');
  } else if (pointsDiff >= -30) {
    reasons.push('A reachable stretch goal for you');
  } else if (pointsDiff >= -60) {
    reasons.push('An ambitious target — achievable with strong results');
  }

  // Salary / employability
  if (answers.salaryImportance >= 4 && course.salaryBand === 'high') {
    reasons.push('Strong salary prospects, which you ranked highly');
  }
  if (answers.jobSecurityImportance >= 4 && course.employability >= 4) {
    reasons.push('High employability and job security');
  }

  // Helping others
  if (answers.helpingOthersImportance >= 4 &&
    (course.interestTags.includes('healthcare') || course.interestTags.includes('social-care') || course.interestTags.includes('education'))) {
    reasons.push('Aligned with your desire to help others');
  }

  // Work style
  const matchingStyles = answers.workStyleTags.filter(t => course.workStyleTags.includes(t));
  if (matchingStyles.length > 0) {
    const formatted = matchingStyles.slice(0, 2).map(t => t.replace(/-/g, ' ')).join(' and ');
    reasons.push(`Suits your ${formatted} work style`);
  }

  // Region
  if (answers.preferredRegions.length > 0 && answers.preferredRegions.includes(course.region)) {
    const regionLabel = course.region.charAt(0).toUpperCase() + course.region.slice(1);
    reasons.push(`Located in your preferred ${regionLabel} region`);
  }

  // Dream job
  if (answers.dreamJobKeywords.trim()) {
    const bonus = dreamJobBonus(answers.dreamJobKeywords, course);
    if (bonus > 0.3) {
      reasons.push('Closely related to your dream career description');
    }
  }

  // Career paths
  if (course.careerPaths.length > 0) {
    reasons.push(`Career paths include ${course.careerPaths.slice(0, 2).join(' and ')}`);
  }

  // Return top 3 most specific reasons
  return reasons.slice(0, 3);
}

// ─── Main Algorithm ─────────────────────────────────────────────────────────

export function runFutureFinderAssessment(
  answers: FutureFinderAnswers,
  profile: StudentSubjectProfile | null,
): RecommendationResult[] {
  const results: RecommendationResult[] = [];

  for (const course of CAO_COURSES) {
    // Level filter: exclude courses outside preferred levels
    if (answers.preferredLevels.length > 0 && !answers.preferredLevels.includes(course.level)) {
      continue;
    }

    // Interest score (Jaccard overlap + activity ranking bonus + dream job bonus)
    const interestOverlap = tagOverlap(answers.interestTags, course.interestTags);
    const activityBonus = tagOverlap(answers.activityRankings, course.interestTags) * 0.3;
    const dreamBonus = dreamJobBonus(answers.dreamJobKeywords, course) * 0.3;
    const interestScore = Math.min(interestOverlap + activityBonus + dreamBonus, 1);

    // Subject fit
    const subFit = subjectFitScore(profile, course);

    // Values alignment
    const valScore = valuesScore(answers, course);

    // Feasibility
    const feasScore = feasibilitySigmoid(answers.estimatedPoints, course.typicalPoints);

    // Weighted total
    let totalScore = (
      interestScore * 0.35 +
      subFit * 0.25 +
      valScore * 0.20 +
      feasScore * 0.20
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

    const reasons = generateReasons(answers, profile, course);

    results.push({ course, score: totalScore, reasons });
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
  type: 'multi-select' | 'single-select' | 'slider' | 'text' | 'rank' | 'boolean' | 'number';
  options?: { value: string; label: string }[];
  min?: number;
  max?: number;
  maxSelections?: number;
}

export const ASSESSMENT_QUESTIONS: AssessmentQuestion[] = [
  // Interest / passion
  {
    id: 'interestTags', dimension: 'Interest', type: 'multi-select', maxSelections: 5,
    question: 'Which areas genuinely interest you? Pick up to 5.',
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
      { value: 'languages', label: 'Languages & Culture' },
      { value: 'design', label: 'Design & Visual' },
      { value: 'agriculture', label: 'Agriculture & Land' },
      { value: 'music', label: 'Music & Performance' },
      { value: 'politics', label: 'Politics & Society' },
      { value: 'food', label: 'Food & Hospitality' },
    ],
  },
  {
    id: 'activityRankings', dimension: 'Interest', type: 'multi-select', maxSelections: 3,
    question: 'Which activities do you enjoy most? Pick your top 3.',
    options: [
      { value: 'technology', label: 'Coding or building things with tech' },
      { value: 'science', label: 'Experiments and figuring out how things work' },
      { value: 'healthcare', label: 'Helping people who are unwell or injured' },
      { value: 'business', label: 'Running a project or starting something new' },
      { value: 'arts', label: 'Reading, writing or debating ideas' },
      { value: 'design', label: 'Drawing, designing or making things look good' },
      { value: 'sport', label: 'Training, coaching or competing' },
      { value: 'social-care', label: 'Volunteering or looking after people' },
      { value: 'media', label: 'Creating content, filming or photography' },
      { value: 'environment', label: 'Being outdoors or working with nature' },
    ],
  },
  {
    id: 'dreamJobKeywords', dimension: 'Interest', type: 'text',
    question: 'Describe your dream job in a few words — even if it seems unrealistic.',
  },

  // Work style
  {
    id: 'workStyleTags', dimension: 'Work Style', type: 'multi-select', maxSelections: 3,
    question: 'How do you like to work? Pick 2-3 styles.',
    options: [
      { value: 'hands-on', label: 'Hands-on — building, making, doing' },
      { value: 'analytical', label: 'Analytical — solving problems with logic' },
      { value: 'creative', label: 'Creative — imagining new ideas' },
      { value: 'people-focused', label: 'People-focused — communicating, helping' },
      { value: 'research-driven', label: 'Research-driven — deep investigation' },
      { value: 'structured', label: 'Structured — clear rules and processes' },
      { value: 'flexible', label: 'Flexible — variety and freedom' },
      { value: 'leadership', label: 'Leadership — organising and leading' },
    ],
  },
  {
    id: 'teamPreference', dimension: 'Work Style', type: 'single-select',
    question: 'Do you prefer working in a team or independently?',
    options: [
      { value: 'team', label: 'In a team — I thrive with others around me' },
      { value: 'solo', label: 'Independently — I do my best work alone' },
      { value: 'mix', label: 'A mix of both' },
    ],
  },

  // Career values
  {
    id: 'salaryImportance', dimension: 'Values', type: 'slider', min: 1, max: 5,
    question: 'How important is a high salary to you?',
  },
  {
    id: 'jobSecurityImportance', dimension: 'Values', type: 'slider', min: 1, max: 5,
    question: 'How important is job security and employability?',
  },
  {
    id: 'helpingOthersImportance', dimension: 'Values', type: 'slider', min: 1, max: 5,
    question: 'How important is helping others or making a difference?',
  },

  // Geographic
  {
    id: 'willingToRelocate', dimension: 'Location', type: 'boolean',
    question: 'Are you open to studying anywhere in Ireland, or do you have a preference?',
  },
  {
    id: 'preferredRegions', dimension: 'Location', type: 'multi-select', maxSelections: 3,
    question: 'Which regions would you prefer? Pick up to 3.',
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

  // Feasibility
  {
    id: 'preferredLevels', dimension: 'Feasibility', type: 'multi-select',
    question: 'What type of course are you interested in?',
    options: [
      { value: '8', label: 'Level 8 — Honours Degree (4 years)' },
      { value: '7', label: 'Level 7 — Ordinary Degree (3 years)' },
      { value: '6', label: 'Level 6 — Higher Certificate (2 years)' },
    ],
  },
  {
    id: 'estimatedPoints', dimension: 'Feasibility', type: 'number', min: 100, max: 625,
    question: 'What CAO points do you realistically expect? (Use the CAO Simulator if unsure)',
  },
];
