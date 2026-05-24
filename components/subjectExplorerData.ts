/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Subject Explorer (JC mode of Future Finder) ────────────────────────────
//
// JC variant of Future Finder. Matches the 7-question intent quiz to clusters
// of LC subjects the student would likely enjoy in senior cycle.
//
// Refined May 2026 against Irish LC subject-choice reality:
//   - Removed Psychology from people-and-society (not an LC subject).
//   - Removed Construction Studies from creative-expression (it's
//     vocational/timber-built work — belongs only in practical-applied).
//   - Removed English from the listed subjects in every humanities cluster
//     and creative-expression — it's universal-mandatory, so the framing
//     copy carries it instead of listing it five times.
//   - Added PE to stem-biological and to the new sport-and-health cluster.
//   - Added Mathematics to practical-applied.
//   - Trimmed languages-and-culture from 7 subjects to a tighter pattern.
//   - Sharpened humanities-creative career callout; added art-track /
//     music-track framing.
//   - Added two new clusters: `sport-and-health` (PE/Bio/Home Ec/Chem) and
//     `balanced-and-broad` (the diffuse / weak-signal fallback).
//   - Wired Q3-Q5 (value sliders) + Q7 (team preference) into the scorer
//     (previously collected but ignored).
//   - Normalised scores by each cluster's max-possible-tag-score to remove
//     the size-of-cluster scoring advantage.
//   - Deterministic tie-break (signal count desc, then cluster id asc).
//   - `balanced-and-broad` surfaces when the signal is diffuse (top-3 within
//     80% of each other) or weak (top normalised score < 0.3).

import type { FutureFinderAnswers } from './futureFinderAlgorithm';

// ─── Cluster definitions ────────────────────────────────────────────────────

export interface SubjectCluster {
  id: string;
  label: string;
  /** 1-3 sentences. Framing notes about universal-English / language picks /
   *  art-vs-music live here so the renderer doesn't need a separate field. */
  blurb: string;
  /** LC subject names. JC equivalents map 1:1 where applicable. English is
   *  intentionally NOT listed (mandatory, covered by the blurb framing) for
   *  humanities clusters and creative-expression. Maths is listed when the
   *  level (HL vs OL) is a meaningful choice for the cluster. */
  subjects: string[];
  /** Soft career callout — "people who study these often go on to do…". JC
   *  voice, no "your future career" language, no vague "great prospects". */
  careerHint: string;
  /** Concrete, doable-for-a-14-year-old exploration ideas. */
  thingsToTry: string[];
  /** Quiz signals this cluster responds to. The scorer sums weighted overlaps
   *  and normalises by max-possible-tag-score so clusters with more tags
   *  don't get an unfair signal-collection advantage. */
  interestTags: string[];      // 2 pts per match (strongest signal)
  scenarioTags: string[];      // 1.5 pts per match
  workStyleTags: string[];     // 1 pt per match
}

export const SUBJECT_CLUSTERS: SubjectCluster[] = [
  {
    id: 'stem-analytical',
    label: 'STEM — analytical',
    blurb: 'You\'re drawn to how things work and like solving problems with logic and numbers. These subjects reward that kind of thinking. LC Engineering is part-theory, part-practical (a metalwork project) — students who pair it with Maths and Physics typically progress to mechanical or electrical engineering at university.',
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
    blurb: 'You like understanding living systems and how the natural world fits together. The canonical pre-med / pre-vet / health-science stack is Biology + Chemistry + HL Maths, with Physics as a strong alternative for engineering-adjacent science paths. PE is a real LC option too if you\'re interested in how the body actually works.',
    subjects: ['Biology', 'Chemistry', 'Mathematics', 'Physics', 'Ag Science', 'Geography', 'PE'],
    careerHint: 'People who study these often go on to do medicine, nursing, veterinary, environmental science, sports science, or agriculture.',
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
    blurb: 'You enjoy understanding why things happen and how systems shape people\'s lives. These subjects train that kind of reasoning. (You\'ll also take English — almost every LC student does — these are your additional choices.)',
    subjects: ['History', 'Geography', 'Politics & Society', 'Economics'],
    careerHint: 'People who study these often go on to do law, journalism, policy, international relations, or teaching.',
    thingsToTry: [
      'Read a long-form article or watch a documentary on a current event that\'s confused you',
      'Listen to a history or politics podcast — even one episode',
      'Join your school\'s debating club or write for a school newspaper',
      'Visit a museum or historic site and notice what questions come to mind',
    ],
    interestTags: ['law', 'environment', 'business', 'history-and-politics'],
    scenarioTags: ['argue-case', 'analyse-data', 'protect-environment'],
    workStyleTags: ['analytical', 'research-driven', 'leadership'],
  },
  {
    id: 'humanities-creative',
    label: 'Humanities — creative and reflective',
    blurb: 'You\'re drawn to stories, ideas and how people see the world. Most students lean into either the art-track (Art + History + RE) or the music-track (Music + History + RE) — few do both. (You\'ll also take English — almost every LC student does — these are your additional choices.)',
    subjects: ['History', 'Art', 'Music', 'Religious Education', 'Classical Studies'],
    careerHint: 'People who study these often go on to publishing, screenwriting, theatre, journalism, teaching, or arts administration.',
    thingsToTry: [
      'Start writing — a journal, a short story, a film review, or anything you don\'t have to show',
      'Read a book outside your usual range (a classic, a memoir, or a graphic novel)',
      'Visit a gallery, theatre, or live music venue',
      'Try a creative writing or film-making club at school',
    ],
    interestTags: ['arts', 'education', 'social-care', 'writing-and-literature'],
    scenarioTags: ['create-content', 'teach-inspire', 'help-difficult'],
    workStyleTags: ['creative', 'people-focused', 'flexible'],
  },
  {
    id: 'business-practical',
    label: 'Business and enterprise',
    blurb: 'You\'re interested in how organisations work, how decisions get made, and how value gets created. These subjects open that up.',
    subjects: ['Business', 'Accounting', 'Economics', 'Mathematics'],
    careerHint: 'People who study these often go on to do business, finance, accounting, marketing, or entrepreneurship.',
    thingsToTry: [
      'Run a small project that makes money (selling something at a school fair, tutoring younger kids, mowing lawns)',
      'Pick a brand you actually use — Spotify, Penneys, BoohooMan, Supermac\'s — and read one news article about how their last quarter went',
      'Join Junior Achievement or a Young Entrepreneurs programme if your school offers one',
      'Follow a public company in the news for a few weeks and notice what moves the share price',
    ],
    interestTags: ['business', 'finance', 'law'],
    scenarioTags: ['run-business', 'analyse-data', 'argue-case'],
    workStyleTags: ['leadership', 'analytical', 'structured'],
  },
  {
    id: 'languages-and-culture',
    label: 'Languages and culture',
    blurb: 'You like communicating, picking up other languages, and getting under the skin of how people live elsewhere. Pick one foreign language you\'ll stick with for two years (French, German, Spanish, or Italian — schools vary) plus History or Classical Studies as the cultural pairing. (You\'ll also take English and Irish — almost everyone does.)',
    subjects: ['French', 'German', 'Spanish', 'Italian', 'Irish', 'History', 'Classical Studies'],
    careerHint: 'People who study these often go on to do translation, journalism, diplomacy, teaching, tourism, or international business.',
    thingsToTry: [
      'Use Duolingo or a similar app on a language you\'ve never tried',
      'Watch a film or TV show in another language with subtitles for two weeks',
      'Sign up for a language exchange or pen-pal scheme',
      'Read in a second language — comic books or short stories are a good way in',
    ],
    interestTags: ['arts', 'education', 'writing-and-literature', 'languages-i-love'],
    scenarioTags: ['teach-inspire', 'create-content', 'help-difficult'],
    workStyleTags: ['people-focused', 'creative', 'flexible'],
  },
  {
    id: 'creative-expression',
    label: 'Creative and expressive',
    blurb: 'You think in images, sounds, or made things. These subjects let you build that into how you work. (You\'ll also take English — almost every LC student does — these are your additional choices.)',
    subjects: ['Art', 'Music', 'Design & Communication Graphics'],
    careerHint: 'People who study these often go on to do design, architecture, music, film, animation, or the games industry.',
    thingsToTry: [
      'Start a creative practice you do weekly — sketching, making beats, photography, writing songs',
      'Share something you made (a friend, a school competition, a small online community)',
      'Visit a design studio, gallery, or workshop on an open day',
      'Try a 30-day creative challenge (Inktober, FAWM, NaNoWriMo)',
    ],
    interestTags: ['arts', 'design'],
    scenarioTags: ['create-content', 'design-product', 'build-fix'],
    workStyleTags: ['creative', 'hands-on', 'flexible'],
  },
  {
    id: 'practical-applied',
    label: 'Practical and applied',
    blurb: 'You like doing over reading-about-doing. You learn fastest with your hands or in a workshop. These subjects let you build, make, and apply. Most students take at least OL Maths; many take HL if they\'re aiming at engineering.',
    subjects: ['Construction Studies', 'Engineering', 'Design & Communication Graphics', 'Ag Science', 'Home Economics', 'Mathematics'],
    careerHint: 'People who study these often go on to do trades, apprenticeships, engineering, architecture, or running their own practical business.',
    thingsToTry: [
      'Take on a real project — building, repairing, restoring, or making something for your home',
      'Shadow a tradesperson for a day (carpentry, plumbing, electrical, mechanics)',
      'Try a community workshop or makerspace if there\'s one near you (your local Men\'s Sheds Association may also run under-18 sessions)',
      'Watch a few "how it\'s made" or trade-school videos and notice which techniques you want to try',
    ],
    interestTags: ['engineering', 'environment', 'sport'],
    scenarioTags: ['build-fix', 'design-product', 'protect-environment'],
    workStyleTags: ['hands-on', 'structured', 'creative'],
  },
  {
    id: 'people-and-society',
    label: 'People and society',
    blurb: 'You\'re drawn to understanding people — what makes them tick, what they need, how they grow. These subjects open that up. (You\'ll also take English — almost every LC student does — these are your additional choices.)',
    subjects: ['Politics & Society', 'Religious Education', 'Home Economics', 'Biology', 'PE'],
    careerHint: 'People who study these often go on to study Psychology, social work, nursing, teaching, or public policy at university.',
    thingsToTry: [
      'Volunteer somewhere that puts you with people who aren\'t your usual circle',
      'Sign up for a peer-mentoring or buddy programme at school',
      'Read about a psychology or sociology topic that interests you (sleep, motivation, friendship)',
      'Listen to a podcast like The Happiness Lab or watch a TED talk on a psychology topic that interests you',
    ],
    interestTags: ['psychology', 'social-care', 'healthcare', 'education', 'history-and-politics'],
    scenarioTags: ['help-difficult', 'teach-inspire'],
    workStyleTags: ['people-focused', 'creative', 'flexible'],
  },

  // ─── New clusters (May 2026 refinement) ──────────────────────────────────

  {
    id: 'sport-and-health',
    label: 'Sport and health',
    blurb: 'You\'re drawn to how the body works, how performance is measured, and how to keep people healthy. PE is now a full LC subject — pair it with Biology and Chemistry for the science side, or Home Economics for the nutrition side.',
    subjects: ['PE', 'Biology', 'Home Economics', 'Chemistry'],
    careerHint: 'People who study these often go on to sports science, physiotherapy, sports management, coaching, dietetics, or nursing.',
    thingsToTry: [
      'Track one thing about yourself for two weeks — resting heart rate, sleep hours, water intake — and notice what changes it',
      'Watch how a pro athlete actually trains (most have YouTube channels) and notice how much is recovery, nutrition and mindset, not just the sport',
      'Help coach a younger team at your local GAA, soccer or hockey club for a season',
      'Read about a sports science topic that interests you — concussion, sleep, periodisation, performance under pressure',
    ],
    // `science` dropped May 2026 — it was pulling STEM-analytical profiles
    // (Lego/Maths kids) into sport-and-health as false positives at 0.5+.
    // {sport, healthcare} is the right signal: the cluster only fires for
    // students who actually like sport AND/OR healthcare.
    interestTags: ['sport', 'healthcare'],
    scenarioTags: ['help-difficult', 'build-fix', 'analyse-data'],
    workStyleTags: ['hands-on', 'people-focused', 'analytical'],
  },
  {
    // The diffuse / weak-signal fallback. Excluded from the normal cluster
    // scoring loop in `runSubjectExplorerMatch` and surfaced via the
    // ratio-and-threshold logic only — see DIFFUSE_RATIO_THRESHOLD and
    // WEAK_SIGNAL_THRESHOLD below. Label deliberately echoes the JC NS
    // theme `future-doors` ("Keep My Future Open").
    id: 'balanced-and-broad',
    label: 'Keep your options open',
    blurb: 'Your interests are wide-ranging, which is a real strength. Here\'s a balanced LC subject set that keeps multiple pathways open — sciences, humanities, and business all stay accessible to you.',
    subjects: ['History', 'Biology', 'Business', 'Geography', 'a foreign language'],
    careerHint: 'Students who take a broad LC subject set often go into general degrees (Arts, Commerce, Social Sciences) where you can specialise later. You don\'t have to know yet.',
    thingsToTry: [
      'Talk to 5 adults about what they actually do day-to-day — not what they studied, what their week looks like',
      'In TY, pick one taster module from each area (science / humanities / business / arts) and notice which one you don\'t want to stop',
      'Read or watch widely — BBC Future, The Conversation, and 99% Invisible all give you 5-minute snapshots of different fields',
      'Listen to a podcast that\'s not aimed at any one career — Stuff You Should Know, The Naked Scientists, or Freakonomics — and notice what catches you',
    ],
    interestTags: [],
    scenarioTags: [],
    workStyleTags: [],
  },
];

// ─── Scoring ────────────────────────────────────────────────────────────────

export interface ClusterMatchResult {
  cluster: SubjectCluster;
  /** Normalised 0-1+ (can exceed 1.0 when Q3-Q7 boosts apply on top of full
   *  tag-overlap — fine for ranking). */
  score: number;
  matchedSignals: string[];
}

// Q3-Q5 (value sliders) + Q7 (team preference) were previously collected
// but did nothing. They now apply additive boosts to clusters aligned with
// the student's stated values + team preference. Thresholds and weights
// per the educator-knowledge corrections that accompanied the audit.
const VALUE_HELPING_CLUSTERS = ['people-and-society', 'stem-biological', 'sport-and-health'];
const VALUE_HELPING_WEIGHT = 1.5;
const VALUE_SALARY_CLUSTERS = ['business-practical', 'stem-analytical'];
const VALUE_SALARY_WEIGHT = 1.5;
const VALUE_SECURITY_CLUSTERS = ['people-and-society', 'practical-applied'];
const VALUE_SECURITY_WEIGHT = 1;
const TEAM_PREF_CLUSTERS: Record<'team' | 'solo', string[]> = {
  team: ['people-and-society', 'business-practical', 'humanities-creative'],
  solo: ['stem-analytical', 'creative-expression', 'humanities-analytical'],
};
const TEAM_PREF_WEIGHT = 0.5;
const VALUE_THRESHOLD = 4;

function computeBoosts(clusterId: string, answers: FutureFinderAnswers): number {
  let boost = 0;
  if (answers.helpingOthersImportance >= VALUE_THRESHOLD && VALUE_HELPING_CLUSTERS.includes(clusterId)) {
    boost += VALUE_HELPING_WEIGHT;
  }
  if (answers.salaryImportance >= VALUE_THRESHOLD && VALUE_SALARY_CLUSTERS.includes(clusterId)) {
    boost += VALUE_SALARY_WEIGHT;
  }
  if (answers.jobSecurityImportance >= VALUE_THRESHOLD && VALUE_SECURITY_CLUSTERS.includes(clusterId)) {
    boost += VALUE_SECURITY_WEIGHT;
  }
  const team = answers.teamPreference;
  if ((team === 'team' || team === 'solo') && TEAM_PREF_CLUSTERS[team].includes(clusterId)) {
    boost += TEAM_PREF_WEIGHT;
  }
  return boost;
}

/** Maximum tag-overlap score this cluster could possibly achieve from Q1/Q2/Q6.
 *  Q3-Q7 boosts are NOT included in this ceiling — a strongly-aligned profile
 *  is allowed to score slightly above 1.0, which is fine for ranking. */
function maxPossibleTagScore(cluster: SubjectCluster): number {
  return (2 * cluster.interestTags.length)
    + (1.5 * cluster.scenarioTags.length)
    + (1 * cluster.workStyleTags.length);
}

export function scoreCluster(cluster: SubjectCluster, answers: FutureFinderAnswers): ClusterMatchResult {
  const signals: string[] = [];
  let rawTagScore = 0;

  for (const tag of answers.interestTags) {
    if (cluster.interestTags.includes(tag)) {
      rawTagScore += 2;
      signals.push(`you picked ${tag.replace(/-/g, ' ')}`);
    }
  }
  for (const choice of answers.scenarioChoices) {
    if (cluster.scenarioTags.includes(choice)) {
      rawTagScore += 1.5;
      if (signals.length < 4) signals.push(choice.replace(/-/g, ' '));
    }
  }
  for (const style of answers.workStyleTags) {
    if (cluster.workStyleTags.includes(style)) {
      rawTagScore += 1;
      if (signals.length < 5) signals.push(`${style.replace(/-/g, ' ')} work suits you`);
    }
  }

  const boost = computeBoosts(cluster.id, answers);
  const max = maxPossibleTagScore(cluster);
  // Clusters with empty tag arrays (only balanced-and-broad) score 0 here
  // and are surfaced separately via the surfacing logic below.
  const score = max > 0 ? (rawTagScore + boost) / max : 0;

  return { cluster, score, matchedSignals: signals };
}

// ─── balanced-and-broad surfacing thresholds ────────────────────────────────
// DIFFUSE: top 3 cluster scores within 80% of each other AND span ≥2 pillars
//   → student's interests are genuinely wide-ranging across the curriculum,
//   not just diffuse across sub-clusters of a single pillar. Surface
//   balanced-and-broad as a strong alternate (#2).
// WEAK: top normalised score is below 0.3 → low overall engagement / unclear
//   signal. Surface balanced-and-broad as the top result instead of leaving
//   the student staring at a thin specialised cluster.
const DIFFUSE_RATIO_THRESHOLD = 0.8;
const WEAK_SIGNAL_THRESHOLD = 0.3;

// Pillar map for the diffuse-AND-pillar-spanning check. A student whose top
// 3 clusters all sit in the same pillar (e.g. three humanities sub-clusters)
// has a *consistent within-pillar* signal — not a broad one — so we don't
// surface "Keep your options open" for them. Surfacing broad requires the
// top 3 to touch at least 2 of these 4 pillars.
const CLUSTER_PILLARS: Record<string, string> = {
  // STEM
  'stem-analytical': 'STEM',
  'stem-biological': 'STEM',
  'sport-and-health': 'STEM',
  // Humanities
  'humanities-analytical': 'Humanities',
  'humanities-creative': 'Humanities',
  'languages-and-culture': 'Humanities',
  'people-and-society': 'Humanities',
  // Business
  'business-practical': 'Business',
  // Practical / Creative
  'practical-applied': 'PracticalCreative',
  'creative-expression': 'PracticalCreative',
};

function countPillarSpan(results: ClusterMatchResult[]): number {
  const pillars = new Set<string>();
  for (const r of results) {
    const p = CLUSTER_PILLARS[r.cluster.id];
    if (p) pillars.add(p);
  }
  return pillars.size;
}

/** Deterministic tie-break: (1) more matched signals wins; (2) alphabetical
 *  by cluster id. Removes array-order luck when scores are equal. */
function compareTie(a: ClusterMatchResult, b: ClusterMatchResult): number {
  if (b.matchedSignals.length !== a.matchedSignals.length) {
    return b.matchedSignals.length - a.matchedSignals.length;
  }
  return a.cluster.id.localeCompare(b.cluster.id);
}

export function runSubjectExplorerMatch(answers: FutureFinderAnswers): ClusterMatchResult[] {
  // Specialised clusters compete on tag matches; balanced-and-broad is
  // reserved for the surfacing logic and excluded from the main ranking.
  const broadCluster = SUBJECT_CLUSTERS.find(c => c.id === 'balanced-and-broad')!;
  const ranked = SUBJECT_CLUSTERS
    .filter(c => c.id !== 'balanced-and-broad')
    .map(c => scoreCluster(c, answers))
    .filter(r => r.score > 0)
    .sort((a, b) => (b.score - a.score) || compareTie(a, b));

  if (ranked.length === 0) {
    // No positive signal at all — surface broad as the standalone result.
    return [{
      cluster: broadCluster,
      score: 0,
      matchedSignals: ['your interests are wide-ranging'],
    }];
  }

  const topScore = ranked[0].score;
  const thirdScore = ranked[2]?.score ?? 0;
  const diffuse = topScore > 0 && (thirdScore / topScore) > DIFFUSE_RATIO_THRESHOLD;
  const pillarSpan = countPillarSpan(ranked.slice(0, 3));
  const weak = topScore < WEAK_SIGNAL_THRESHOLD;

  const broadResult: ClusterMatchResult = {
    cluster: broadCluster,
    score: weak ? 1 : topScore,
    matchedSignals: [weak ? 'your interests are still forming' : 'your interests are wide-ranging'],
  };

  if (weak) {
    // Broad as top; top two specialised clusters keep their alternate slots.
    // (The weak path is a separate concern from the diffuse path — a student
    // who hasn't engaged enough for any strong signal still benefits from
    // seeing broad even if their thin top 3 sit in one pillar.)
    return [broadResult, ...ranked.slice(0, 2)];
  }
  if (diffuse && pillarSpan >= 2) {
    // Genuine cross-pillar breadth. Top specialised stays #1; broad slots in
    // as #2; the next specialised takes #3. The original third drops off —
    // the spread is too wide for it to be a confident match anyway.
    return [ranked[0], broadResult, ...ranked.slice(1, 2)];
  }
  return ranked;
}
