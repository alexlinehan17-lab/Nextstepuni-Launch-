/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Subject Explorer (JC mode of Future Finder) ────────────────────────────
//
// JC variant of Future Finder. Instead of matching the student to CAO courses
// (which JC kids have no use for), this matches their interest-quiz answers
// to clusters of LC subjects they're likely to enjoy in senior cycle.
//
// The matcher consumes the same FutureFinderAnswers shape produced by the
// shared 10-question assessment, but only reads the age-agnostic
// dimensions (interestTags, scenarioChoices, workStyleTags, value sliders,
// teamPreference). It ignores studyDuration / willingToRelocate /
// preferredRegions — those are CAO-flavoured and inapplicable to JC.

import type { FutureFinderAnswers } from './futureFinderAlgorithm';

// ─── Cluster definitions ────────────────────────────────────────────────────

export interface SubjectCluster {
  id: string;
  label: string;
  blurb: string; // 1-2 sentences shown alongside the cluster on the result card
  // Subjects to suggest. Names are LC subject names; JC equivalents map
  // 1:1 for English/Irish/Maths/History/Geography/Music/Art/Religion and
  // diverge for some practical/STEM subjects. We surface LC names here
  // since the framing is "subjects you'd enjoy in senior cycle".
  subjects: string[];
  // Soft career callout — "people who study these often go on to do..."
  // Kept low-prescription, JC-voice. No "your future career" language.
  careerHint: string;
  // Things to try in TY / electives — concrete, low-stakes exploration.
  thingsToTry: string[];
  // Which quiz signals this cluster responds to. Higher weight = stronger
  // pull. The matcher sums weights across tag matches and ranks clusters.
  interestTags: string[];      // matches answers.interestTags
  scenarioTags: string[];      // matches answers.scenarioChoices
  workStyleTags: string[];     // matches answers.workStyleTags
}

export const SUBJECT_CLUSTERS: SubjectCluster[] = [
  {
    id: 'stem-analytical',
    label: 'STEM — analytical',
    blurb: 'You\'re drawn to how things work and like solving problems with logic and numbers. These subjects reward that kind of thinking.',
    subjects: ['Mathematics', 'Applied Maths', 'Physics', 'Chemistry', 'Computer Science', 'Engineering'],
    careerHint: 'People who study these often go on to do engineering, computer science, physics, finance, or research.',
    thingsToTry: [
      'Try a coding tutorial — Scratch, Python or Replit are good starting points',
      'Build something physical — a robotics kit, electronics project, or DIY repair',
      'Sign up for a maths or science Olympiad — even just to see what the questions are like',
      'Watch some 3Blue1Brown or Veritasium videos and notice which topics make you want to know more',
    ],
    interestTags: ['technology', 'science', 'engineering', 'finance'],
    scenarioTags: ['investigate-science', 'build-fix', 'analyse-data', 'design-product'],
    workStyleTags: ['analytical', 'hands-on', 'research-driven'],
  },
  {
    id: 'stem-biological',
    label: 'STEM — life and earth',
    blurb: 'You like understanding living systems and how the natural world fits together. These subjects let you explore that at depth.',
    subjects: ['Biology', 'Chemistry', 'Ag Science', 'Geography'],
    careerHint: 'People who study these often go on to do medicine, nursing, veterinary, environmental science, or agriculture.',
    thingsToTry: [
      'Volunteer with a local animal shelter or wildlife group',
      'Try a citizen-science project (BioBlitz, bird counts, water-quality monitoring)',
      'Grow something — herbs on a windowsill, a vegetable patch, or a hydroponic kit',
      'Read or watch about a biology topic that fascinates you (genetics, ecology, the brain)',
    ],
    interestTags: ['science', 'healthcare', 'environment', 'sport'],
    scenarioTags: ['investigate-science', 'help-difficult', 'protect-environment'],
    workStyleTags: ['analytical', 'research-driven', 'hands-on'],
  },
  {
    id: 'humanities-analytical',
    label: 'Humanities — analytical',
    blurb: 'You enjoy understanding why things happen and how systems shape people\'s lives. These subjects train that kind of reasoning.',
    subjects: ['History', 'Geography', 'Politics & Society', 'Economics'],
    careerHint: 'People who study these often go on to do law, journalism, policy, international relations, or teaching.',
    thingsToTry: [
      'Read a long-form article or watch a documentary on a current event that\'s confused you',
      'Listen to a history or politics podcast — even one episode',
      'Join your school\'s debating club or write for a school newspaper',
      'Visit a museum or historic site and notice what questions come to mind',
    ],
    interestTags: ['law', 'environment', 'business'],
    scenarioTags: ['argue-case', 'analyse-data', 'protect-environment'],
    workStyleTags: ['analytical', 'research-driven', 'leadership'],
  },
  {
    id: 'humanities-creative',
    label: 'Humanities — creative and reflective',
    blurb: 'You\'re drawn to stories, ideas and how people see the world. These subjects let you go deep on that.',
    subjects: ['English', 'History', 'Art', 'Music', 'Religious Education', 'Classical Studies'],
    careerHint: 'People who study these often go on to do writing, journalism, teaching, the arts, or the screen industry.',
    thingsToTry: [
      'Start writing — a journal, a short story, a film review, or anything you don\'t have to show',
      'Read a book outside your usual range (a classic, a memoir, or a graphic novel)',
      'Visit a gallery, theatre, or live music venue',
      'Try a creative writing or film-making club at school',
    ],
    interestTags: ['arts', 'media', 'education', 'social-care'],
    scenarioTags: ['create-content', 'teach-inspire', 'help-difficult'],
    workStyleTags: ['creative', 'people-focused', 'flexible'],
  },
  {
    id: 'business-practical',
    label: 'Business and money',
    blurb: 'You\'re interested in how organisations work, how decisions get made, and how value gets created. These subjects open that up.',
    subjects: ['Business', 'Accounting', 'Economics', 'Mathematics'],
    careerHint: 'People who study these often go on to do business, finance, accounting, marketing, or entrepreneurship.',
    thingsToTry: [
      'Run a small project that makes money (selling something at a school fair, tutoring younger kids, mowing lawns)',
      'Follow a public company in the news for a few weeks and notice what moves the share price',
      'Join Junior Achievement or a Young Entrepreneurs programme if your school offers one',
      'Read a short business book aimed at teens — "Rich Dad Poor Dad" or similar is a starting point',
    ],
    interestTags: ['business', 'finance', 'law'],
    scenarioTags: ['run-business', 'analyse-data', 'argue-case'],
    workStyleTags: ['leadership', 'analytical', 'structured'],
  },
  {
    id: 'languages-and-culture',
    label: 'Languages and culture',
    blurb: 'You like communicating, picking up other languages, and getting under the skin of how people live elsewhere. These subjects fit that.',
    subjects: ['French', 'German', 'Spanish', 'Irish', 'English', 'Classical Studies', 'History'],
    careerHint: 'People who study these often go on to do translation, journalism, diplomacy, teaching, tourism, or international business.',
    thingsToTry: [
      'Use Duolingo or a similar app on a language you\'ve never tried',
      'Watch a film or TV show in another language with subtitles for two weeks',
      'Sign up for a language exchange or pen-pal scheme',
      'Read in a second language — comic books or short stories are a good way in',
    ],
    interestTags: ['arts', 'media', 'education'],
    scenarioTags: ['teach-inspire', 'create-content', 'help-difficult'],
    workStyleTags: ['people-focused', 'creative', 'flexible'],
  },
  {
    id: 'creative-expression',
    label: 'Creative and expressive',
    blurb: 'You think in images, sounds, or made things. These subjects let you build that into how you work.',
    subjects: ['Art', 'Music', 'Design & Communication Graphics', 'English', 'Construction Studies'],
    careerHint: 'People who study these often go on to do design, architecture, music, film, animation, or the games industry.',
    thingsToTry: [
      'Start a creative practice you do weekly — sketching, making beats, photography, writing songs',
      'Share something you made (a friend, a school competition, a small online community)',
      'Visit a design studio, gallery, or workshop on an open day',
      'Try a 30-day creative challenge (Inktober, FAWM, NaNoWriMo)',
    ],
    interestTags: ['arts', 'design', 'media'],
    scenarioTags: ['create-content', 'design-product', 'build-fix'],
    workStyleTags: ['creative', 'hands-on', 'flexible'],
  },
  {
    id: 'practical-applied',
    label: 'Practical and applied',
    blurb: 'You like doing over reading-about-doing. You learn fastest with your hands or in a workshop. These subjects let you build, make, and apply.',
    subjects: ['Construction Studies', 'Engineering', 'Design & Communication Graphics', 'Ag Science', 'Home Economics'],
    careerHint: 'People who study these often go on to do trades, apprenticeships, engineering, architecture, or running their own practical business.',
    thingsToTry: [
      'Take on a real project — building, repairing, restoring, or making something for your home',
      'Shadow a tradesperson for a day (carpentry, plumbing, electrical, mechanics)',
      'Try a community workshop or men\'s shed if there\'s one near you',
      'Watch a few "how it\'s made" or trade-school videos and notice which techniques you want to try',
    ],
    interestTags: ['engineering', 'environment', 'sport'],
    scenarioTags: ['build-fix', 'design-product', 'protect-environment'],
    workStyleTags: ['hands-on', 'structured', 'creative'],
  },
  {
    id: 'people-and-society',
    label: 'People and society',
    blurb: 'You\'re drawn to understanding people — what makes them tick, what they need, how they grow. These subjects open that up.',
    subjects: ['Psychology (TY only)', 'Politics & Society', 'Religious Education', 'Home Economics', 'English'],
    careerHint: 'People who study these often go on to do psychology, social work, teaching, nursing, or the helping professions.',
    thingsToTry: [
      'Volunteer somewhere that puts you with people who aren\'t your usual circle',
      'Sign up for a peer-mentoring or buddy programme at school',
      'Read about a psychology or sociology topic that interests you (sleep, motivation, friendship)',
      'Try a basic first-aid or mental-health-first-aid course',
    ],
    interestTags: ['psychology', 'social-care', 'healthcare', 'education'],
    scenarioTags: ['help-difficult', 'teach-inspire'],
    workStyleTags: ['people-focused', 'creative', 'flexible'],
  },
];

// ─── Matcher ────────────────────────────────────────────────────────────────

export interface ClusterMatchResult {
  cluster: SubjectCluster;
  score: number;
  matchedSignals: string[]; // human-readable list of why this matched (e.g. "you picked Investigate science", "you like analytical work")
}

/**
 * Score a cluster against the student's quiz answers.
 *
 * The score is a weighted sum:
 *   - interest tag overlap: 2 points each (strongest signal — explicit interest)
 *   - scenario overlap: 1.5 points each (concrete preference)
 *   - work-style overlap: 1 point each
 * Value sliders (salary/jobSecurity/helping) and teamPreference are not
 * read directly — they vary too widely to dominate clustering. They influence
 * the senior CAO course matcher because individual courses carry those tags;
 * clusters at this resolution don't.
 */
export function scoreCluster(cluster: SubjectCluster, answers: FutureFinderAnswers): ClusterMatchResult {
  const signals: string[] = [];
  let score = 0;

  for (const tag of answers.interestTags) {
    if (cluster.interestTags.includes(tag)) {
      score += 2;
      signals.push(`you picked ${tag.replace(/-/g, ' ')}`);
    }
  }
  for (const choice of answers.scenarioChoices) {
    if (cluster.scenarioTags.includes(choice)) {
      score += 1.5;
      // Don't spam signals — keep the most distinctive ones
      if (signals.length < 4) signals.push(choice.replace(/-/g, ' '));
    }
  }
  for (const style of answers.workStyleTags) {
    if (cluster.workStyleTags.includes(style)) {
      score += 1;
      if (signals.length < 5) signals.push(`${style.replace(/-/g, ' ')} work suits you`);
    }
  }

  return { cluster, score, matchedSignals: signals };
}

export function runSubjectExplorerMatch(answers: FutureFinderAnswers): ClusterMatchResult[] {
  return SUBJECT_CLUSTERS
    .map(c => scoreCluster(c, answers))
    .filter(r => r.score > 0)  // drop zero-score clusters — no positive signal
    .sort((a, b) => b.score - a.score);
}
