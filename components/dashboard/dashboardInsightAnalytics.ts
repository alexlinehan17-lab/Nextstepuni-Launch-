/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import type { UnifiedMockResult } from '../../types';
import { resolveMockResultKind } from '../../services/mockResultsRepository';
import { getGradeIndex, getPointsForGrade, type Grade } from '../subjectData';
import {
  CONFIDENCE_LABELS,
  type ActivityBucket,
  type ActivityMetric,
  type ConfidenceObservation,
  startOfLocalDay,
  toLocalDateKey,
} from './dashboardAnalytics';

export type DashboardTrend = 'upward' | 'downward' | 'steady' | 'varied' | 'building';

export interface DashboardInsightItem {
  id: string;
  title: string;
  trend: DashboardTrend;
  evidence: string;
  guidance: string;
}

interface SeriesReading {
  trend: DashboardTrend;
  earlyAverage: number;
  recentAverage: number;
  range: number;
}

interface SeriesAverages {
  earlyAverage: number;
  recentAverage: number;
}

const average = (values: number[]): number => (
  values.reduce((sum, value) => sum + value, 0) / Math.max(values.length, 1)
);

function compareSeriesEdges(values: number[]): SeriesAverages {
  if (values.length < 2) {
    const onlyValue = values[0] ?? 0;
    return { earlyAverage: onlyValue, recentAverage: onlyValue };
  }
  const windowSize = values.length === 2 ? 1 : Math.min(3, Math.floor(values.length / 2));
  return {
    earlyAverage: average(values.slice(0, windowSize)),
    recentAverage: average(values.slice(-windowSize)),
  };
}

function projectedSeriesChange(values: number[]): number {
  if (values.length < 2) return 0;
  const xAverage = (values.length - 1) / 2;
  const yAverage = average(values);
  let numerator = 0;
  let denominator = 0;

  values.forEach((value, index) => {
    const xDelta = index - xAverage;
    numerator += xDelta * (value - yAverage);
    denominator += xDelta ** 2;
  });

  return denominator === 0 ? 0 : (numerator / denominator) * (values.length - 1);
}

function readSeries(
  values: number[],
  meaningfulChange: number,
  variedRange: number,
): SeriesReading {
  if (values.length < 2) {
    const onlyValue = values[0] ?? 0;
    return { trend: 'building', earlyAverage: onlyValue, recentAverage: onlyValue, range: 0 };
  }

  const { earlyAverage, recentAverage } = compareSeriesEdges(values);
  const shift = recentAverage - earlyAverage;
  const range = Math.max(...values) - Math.min(...values);
  const changes = values.slice(1).map((value, index) => value - values[index]);
  const hasIncrease = changes.some(change => change > 0);
  const hasDecrease = changes.some(change => change < 0);
  const projectedChange = projectedSeriesChange(values);

  const oscillatesWithoutDirection = hasIncrease
    && hasDecrease
    && range >= variedRange
    && Math.abs(projectedChange) <= Math.max(variedRange, meaningfulChange * 2);

  if (oscillatesWithoutDirection) return { trend: 'varied', earlyAverage, recentAverage, range };
  if (shift >= meaningfulChange) return { trend: 'upward', earlyAverage, recentAverage, range };
  if (shift <= -meaningfulChange) return { trend: 'downward', earlyAverage, recentAverage, range };
  if (hasIncrease && hasDecrease && range >= variedRange) return { trend: 'varied', earlyAverage, recentAverage, range };
  return { trend: 'steady', earlyAverage, recentAverage, range };
}

function formatNumber(value: number): string {
  return Number.isInteger(value) ? String(value) : value.toFixed(1);
}

function formatSignedNumber(value: number): string {
  return `${value > 0 ? '+' : ''}${formatNumber(value)}`;
}

function confidenceGuidance(trend: DashboardTrend, recentAverage: number, subject: string): string {
  if (trend === 'upward') {
    return 'Keep the approach behind the recent lift, then check it with a short closed-book task so the feeling is backed by recall.';
  }
  if (trend === 'downward') {
    return `Choose one ${subject} topic behind the lower rating and make the next block a small diagnose-and-fix session.`;
  }
  if (trend === 'varied') {
    return 'Compare the topic and method used in the strongest and weakest sessions, then repeat the stronger setup once.';
  }
  if (trend === 'building') {
    return `Add another debrief after your next ${subject} session before treating this as a trend.`;
  }
  if (recentAverage >= 4) {
    return 'Confidence is consistently high. Use one marked or closed-book task to check that it matches performance.';
  }
  if (recentAverage <= 2.5) {
    return 'Narrow the next block to one topic and one achievable check, then debrief again.';
  }
  return 'Change one variable next time—topic, method or question type—and see whether the next rating moves.';
}

export function buildConfidenceInsights(
  observations: ConfidenceObservation[],
  subjectNames: string[] = [],
): DashboardInsightItem[] {
  const grouped = new Map<string, ConfidenceObservation[]>();
  for (const observation of observations) {
    const points = grouped.get(observation.subject) ?? [];
    points.push(observation);
    grouped.set(observation.subject, points);
  }
  for (const subject of subjectNames) {
    if (!grouped.has(subject)) grouped.set(subject, []);
  }

  return [...grouped.entries()]
    .sort((a, b) => b[1].length - a[1].length)
    .map(([subject, unsortedPoints]) => {
      const points = [...unsortedPoints].sort((a, b) => a.timestamp - b.timestamp);
      if (points.length === 0) {
        return {
          id: `confidence-${subject}`,
          title: subject,
          trend: 'building',
          evidence: 'No confidence debriefs fall inside the selected period yet.',
          guidance: `Choose a confidence rating after your next ${subject} session and the trend will begin here.`,
        };
      }
      const values = points.map(point => point.score);
      const reading = readSeries(values, 0.5, 1);
      const latest = values.at(-1) ?? 0;
      const latestLabel = CONFIDENCE_LABELS[Math.max(0, latest - 1)] ?? 'Unknown';
      const countLabel = `${points.length} debrief${points.length === 1 ? '' : 's'}`;
      let evidence = `${countLabel} · latest ${latestLabel}`;

      if (reading.trend === 'upward' || reading.trend === 'downward') {
        const shift = Math.abs(reading.recentAverage - reading.earlyAverage);
        evidence = `${countLabel} · recent ratings are ${formatNumber(shift)} level${shift === 1 ? '' : 's'} ${reading.trend === 'upward' ? 'higher' : 'lower'} than earlier ratings.`;
      } else if (reading.trend === 'varied') {
        evidence = `${countLabel} · ratings span ${formatNumber(reading.range)} confidence level${reading.range === 1 ? '' : 's'}.`;
      }

      return {
        id: `confidence-${subject}`,
        title: subject,
        trend: reading.trend,
        evidence,
        guidance: confidenceGuidance(reading.trend, reading.recentAverage, subject),
      };
    });
}

function formatActivityValue(value: number, metric: ActivityMetric): string {
  if (metric === 'sessions') return `${value} session${value === 1 ? '' : 's'}`;
  return `${value} minute${value === 1 ? '' : 's'}`;
}

export function buildActivityInsights(
  buckets: ActivityBucket[],
  metric: ActivityMetric,
  subjectLabel: string,
  now = new Date(),
): DashboardInsightItem[] {
  const today = startOfLocalDay(now).getTime();
  const completed = buckets.filter(bucket => bucket.end <= today);
  const windowSize = Math.min(3, Math.floor(completed.length / 2));
  const title = subjectLabel === 'All subjects' ? 'Study momentum' : `${subjectLabel} momentum`;

  if (windowSize === 0) {
    const currentTotal = buckets.reduce((sum, bucket) => sum + bucket[metric], 0);
    return [{
      id: 'activity-momentum',
      title,
      trend: 'building',
      evidence: currentTotal > 0
        ? `${formatActivityValue(currentTotal, metric)} recorded so far in this period.`
        : 'There is not enough completed time in this period to compare yet.',
      guidance: 'Complete one more focused block and this comparison will begin to take shape.',
    }];
  }

  const previous = completed.slice(-(windowSize * 2), -windowSize);
  const recent = completed.slice(-windowSize);
  const previousTotal = previous.reduce((sum, bucket) => sum + bucket[metric], 0);
  const recentTotal = recent.reduce((sum, bucket) => sum + bucket[metric], 0);
  const meaningfulChange = metric === 'sessions' ? 1 : 10;
  let trend: DashboardTrend = 'steady';

  if (previousTotal === 0 && recentTotal > 0) trend = 'upward';
  else if (recentTotal - previousTotal >= meaningfulChange && recentTotal >= previousTotal * 1.2) trend = 'upward';
  else if (previousTotal - recentTotal >= meaningfulChange && recentTotal <= previousTotal * 0.8) trend = 'downward';
  else if (previousTotal === 0 && recentTotal === 0) trend = 'building';

  const periodNoun = buckets[0]?.key.length === 7 ? 'months' : 'days';
  const evidence = `${formatActivityValue(recentTotal, metric)} across the latest ${windowSize} completed ${periodNoun}, compared with ${formatActivityValue(previousTotal, metric)} in the preceding ${windowSize}.`;
  const guidance = trend === 'upward'
    ? 'Protect the pattern by deciding the next small block before this one ends.'
    : trend === 'downward'
      ? 'Restart with one manageable block rather than trying to recover the whole gap at once.'
      : trend === 'building'
        ? 'Choose one short block on the next available day to create a fresh signal.'
        : 'The volume is holding steady; improve the next block by making its outcome more specific.';

  return [{ id: 'activity-momentum', title, trend, evidence, guidance }];
}

function isGrade(value: string): value is Grade {
  return /^(H|O)[1-8]$/.test(value);
}

function gradePosition(grade: Grade): number {
  return 8 - getGradeIndex(grade);
}

function gradeLevel(grade: Grade): 'Higher' | 'Ordinary' {
  return grade.startsWith('H') ? 'Higher' : 'Ordinary';
}

function formatCaoPointComparison(values: number[]): string {
  const { earlyAverage, recentAverage } = compareSeriesEdges(values);
  const shift = recentAverage - earlyAverage;
  if (shift === 0) return `CAO subject points remain at ${formatNumber(recentAverage)}.`;
  return `CAO subject points move from ${formatNumber(earlyAverage)} to ${formatNumber(recentAverage)} (${formatSignedNumber(shift)}).`;
}

interface GradePoint {
  grade: Grade;
}

interface LevelTransition {
  from: Grade;
  to: Grade;
}

function getCurrentLevelSegment<T extends GradePoint>(points: T[]): {
  current: T[];
  transitions: LevelTransition[];
} {
  const transitions: LevelTransition[] = [];
  let currentLevelStart = 0;
  for (let index = 1; index < points.length; index += 1) {
    if (points[index].grade[0] === points[index - 1].grade[0]) continue;
    transitions.push({ from: points[index - 1].grade, to: points[index].grade });
    currentLevelStart = index;
  }
  return { current: points.slice(currentLevelStart), transitions };
}

function sortMocks(mocks: UnifiedMockResult[]): UnifiedMockResult[] {
  return [...mocks].sort((a, b) => a.date.localeCompare(b.date) || a.timestamp - b.timestamp);
}

function buildMockSubjectMovement(mocks: UnifiedMockResult[]): DashboardInsightItem | null {
  if (mocks.length < 2) return null;
  const latest = mocks.at(-1);
  if (!latest) return null;
  const histories = new Map<string, { grade: Grade }[]>();
  for (const mock of mocks) {
    for (const entry of mock.entries) {
      if (!isGrade(entry.grade)) continue;
      const history = histories.get(entry.subjectName) ?? [];
      history.push({ grade: entry.grade });
      histories.set(entry.subjectName, history);
    }
  }
  const movements = latest.entries.flatMap(entry => {
    if (!isGrade(entry.grade)) return [];
    const history = histories.get(entry.subjectName) ?? [];
    const { current, transitions } = getCurrentLevelSegment(history);
    const latestCurrent = current.at(-1);
    if (!latestCurrent) return [];
    const latestTransition = transitions.at(-1);
    if (current.length < 2 && !latestTransition) return [];
    const earlierGrade = current.length >= 2 ? current[0].grade : latestTransition?.from;
    if (!earlierGrade) return [];
    const maths = entry.subjectName === 'Mathematics';
    return [{
      subject: entry.subjectName,
      earlierGrade,
      latestGrade: latestCurrent.grade,
      levelTransition: current.length < 2 ? latestTransition : undefined,
      rebased: transitions.length > 0 && current.length >= 2,
      gradeChange: current.length >= 2
        ? gradePosition(latestCurrent.grade) - gradePosition(earlierGrade)
        : null,
      pointChange: getPointsForGrade(latestCurrent.grade, maths) - getPointsForGrade(earlierGrade, maths),
    }];
  });
  if (movements.length === 0) return null;

  const comparable = movements.filter((movement): movement is typeof movement & { gradeChange: number } => (
    movement.gradeChange !== null
  ));
  const levelChanges = movements.filter(movement => movement.gradeChange === null);
  const strongest = [...comparable].sort((a, b) => b.gradeChange - a.gradeChange)[0];
  const weakest = [...comparable].sort((a, b) => a.gradeChange - b.gradeChange)[0];
  const hasLift = (strongest?.gradeChange ?? 0) > 0;
  const hasDrop = (weakest?.gradeChange ?? 0) < 0;
  const trend: DashboardTrend = levelChanges.length > 0
    ? (hasLift || hasDrop ? 'varied' : 'building')
    : hasLift && hasDrop ? 'varied' : hasLift ? 'upward' : hasDrop ? 'downward' : 'steady';
  const evidenceParts: string[] = [];
  const pointChangeLabel = (change: number) => change === 0
    ? 'no CAO-point change'
    : `${formatSignedNumber(change)} CAO points`;
  if (hasLift && strongest) {
    const context = strongest.rebased ? '; since latest level change' : '';
    evidenceParts.push(`Largest lift: ${strongest.subject} ${strongest.earlierGrade} → ${strongest.latestGrade} (${pointChangeLabel(strongest.pointChange)}${context})`);
  }
  if (hasDrop && weakest) {
    const context = weakest.rebased ? '; since latest level change' : '';
    evidenceParts.push(`Watch: ${weakest.subject} ${weakest.earlierGrade} → ${weakest.latestGrade} (${pointChangeLabel(weakest.pointChange)}${context})`);
  }
  if (!hasLift && !hasDrop && levelChanges.length === 0) {
    evidenceParts.push('Subject grades are unchanged between the first and latest result in view');
  }
  for (const movement of levelChanges.slice(0, 2)) {
    const transition = movement.levelTransition;
    evidenceParts.push(`Level change: ${movement.subject} ${transition?.from ?? movement.earlierGrade} → ${transition?.to ?? movement.latestGrade} (not compared as a direction)`);
  }

  let guidance = 'Use the next marked practice to create movement in one subject rather than spreading effort across all of them.';
  if (levelChanges.length > 0) {
    const changed = levelChanges[0];
    guidance = `Treat ${changed.subject} ${changed.latestGrade} as a new ${gradeLevel(changed.latestGrade).toLowerCase()}-level baseline, then compare its next result at the same level.`;
  } else if (hasLift && hasDrop && strongest && weakest) {
    guidance = `Keep a light maintenance block for ${strongest.subject}, and make ${weakest.subject} the next subject you diagnose.`;
  } else if (hasLift && strongest) {
    guidance = `Note what changed in ${strongest.subject} and reuse that setup for one subject that has not moved yet.`;
  } else if (hasDrop && weakest) {
    guidance = `Start with one question set in ${weakest.subject}, then use the marking evidence to choose the exact gap to fix.`;
  }

  return {
    id: 'mock-subject-movement',
    title: 'Subject movement',
    trend,
    evidence: `${evidenceParts.join(' · ')}.`,
    guidance,
  };
}

function buildSubjectMockInsight(mocks: UnifiedMockResult[], subject: string): DashboardInsightItem {
  const points = sortMocks(mocks).flatMap(mock => mock.entries.flatMap(entry => {
    if (entry.subjectName !== subject || !isGrade(entry.grade)) return [];
    return [{
      id: `${mock.id}-${subject}`,
      grade: entry.grade,
      date: mock.date,
      position: gradePosition(entry.grade),
      caoPoints: getPointsForGrade(entry.grade, subject === 'Mathematics'),
    }];
  }));

  if (points.length === 0) {
    return {
      id: `mock-${subject}`,
      title: `${subject} results`,
      trend: 'building',
      evidence: `No ${subject} grades fall inside the selected period yet.`,
      guidance: `Add a ${subject} result after your next marked paper and this comparison will begin here.`,
    };
  }

  const latest = points.at(-1) ?? points[0];
  const { current: currentLevelPoints, transitions: levelTransitions } = getCurrentLevelSegment(points);
  if (levelTransitions.length > 0 && currentLevelPoints.length < 2) {
    const latestTransition = levelTransitions.at(-1) ?? levelTransitions[0];
    const transitionEvidence = levelTransitions.length === 1
      ? `level changed from ${gradeLevel(latestTransition.from)} to ${gradeLevel(latestTransition.to)}`
      : `level changed ${levelTransitions.length} times`;
    return {
      id: `mock-${subject}`,
      title: `${subject} results`,
      trend: 'building',
      evidence: `${points.length} results · ${transitionEvidence}. Latest grade ${latest.grade} is the new ${gradeLevel(latest.grade).toLowerCase()}-level baseline.`,
      guidance: `Keep the next ${subject} result at ${gradeLevel(latest.grade)} level so it can be compared with ${latest.grade}.`,
    };
  }

  const analyzedPoints = levelTransitions.length > 0 ? currentLevelPoints : points;
  const countLabel = levelTransitions.length > 0
    ? `${analyzedPoints.length} ${gradeLevel(latest.grade).toLowerCase()}-level results since the latest level change`
    : `${points.length} results`;
  const values = analyzedPoints.map(point => point.position);
  const reading = readSeries(values, 0.5, 1);
  const caoPointValues = analyzedPoints.map(point => point.caoPoints);
  let evidence = `One result recorded · latest grade ${latest.grade} (${latest.caoPoints} CAO subject points).`;

  if (reading.trend === 'varied') {
    const ordered = [...analyzedPoints].sort((a, b) => a.position - b.position);
    evidence = `${countLabel}, ranging from ${ordered[0].grade} to ${ordered.at(-1)?.grade ?? latest.grade}, with no consistent direction yet. ${formatCaoPointComparison(caoPointValues)}`;
  } else if (analyzedPoints.length > 1) {
    const shift = reading.recentAverage - reading.earlyAverage;
    const direction = shift > 0 ? 'higher' : shift < 0 ? 'lower' : 'unchanged';
    const gradeComparison = shift === 0
      ? 'grade position is holding steady'
      : `recent grades average ${formatNumber(Math.abs(shift))} grade step${Math.abs(shift) === 1 ? '' : 's'} ${direction} than earlier results`;
    evidence = `${countLabel} · ${gradeComparison}. Latest grade ${latest.grade}. ${formatCaoPointComparison(caoPointValues)}`;
  }

  const guidance = reading.trend === 'upward'
    ? `Note what changed before the stronger ${subject} results and reuse that setup for the next marked practice.`
    : reading.trend === 'downward'
      ? `Use the latest ${subject} paper as a diagnosis and trace the lower grade to one topic or question type.`
      : reading.trend === 'varied'
        ? `Compare the strongest and weakest ${subject} result for differences in topic, timing and preparation, then repeat one condition.`
        : reading.trend === 'steady'
          ? `Choose one specific ${subject} gap for the next marked practice, then compare the result under similar conditions.`
          : `A second ${subject} result will show direction; keep the paper conditions similar so the comparison is useful.`;

  return {
    id: `mock-${subject}`,
    title: `${subject} results`,
    trend: reading.trend,
    evidence,
    guidance,
  };
}

export function buildMockInsights(
  mocks: UnifiedMockResult[],
  subject = 'all',
  todayKey = toLocalDateKey(new Date()),
): DashboardInsightItem[] {
  const eligible = sortMocks(mocks.filter(mock => mock.date <= todayKey));
  if (subject !== 'all') return [buildSubjectMockInsight(eligible, subject)];

  const fullMocks = eligible.filter(mock => resolveMockResultKind(mock) === 'full');
  if (fullMocks.length === 0) {
    return [{
      id: 'mock-trajectory',
      title: 'Total points',
      trend: 'building',
      evidence: 'No full mock sittings fall inside the selected period yet.',
      guidance: 'Add a full mock in Points Passport and the total-points comparison will begin here.',
    }];
  }

  const values = fullMocks.map(mock => mock.totalPoints);
  const reading = readSeries(values, 5, 20);
  let evidence = `One full mock sitting recorded at ${values[0]} points.`;
  if (reading.trend === 'varied') {
    evidence = `${fullMocks.length} full mock sittings spanning ${reading.range} points, with no consistent direction yet.`;
  } else if (fullMocks.length > 1) {
    const shift = reading.recentAverage - reading.earlyAverage;
    evidence = `${fullMocks.length} full mock sittings · earlier average ${formatNumber(reading.earlyAverage)} points, recent average ${formatNumber(reading.recentAverage)} (${formatSignedNumber(shift)}).`;
  }

  const guidance = reading.trend === 'upward'
    ? 'Compare the earlier and recent subject grades, keep what improved, and choose one remaining gap for the next marked practice.'
    : reading.trend === 'downward'
      ? 'Use the latest full mock as a diagnosis: choose one subject-grade drop and trace it to a specific topic or question type.'
      : reading.trend === 'varied'
        ? 'Compare the strongest and weakest full sitting for differences in subject grades, timing and preparation, then repeat one condition.'
        : reading.trend === 'steady'
          ? 'Choose one subject where a single grade step would matter, and make that the focus of the next marked practice.'
          : 'A second full mock will show direction; keep the paper conditions similar so the comparison is useful.';

  const insights: DashboardInsightItem[] = [{
    id: 'mock-trajectory',
    title: 'Total points',
    trend: reading.trend,
    evidence,
    guidance,
  }];
  const subjectMovement = buildMockSubjectMovement(fullMocks);
  if (subjectMovement) insights.push(subjectMovement);
  return insights;
}
