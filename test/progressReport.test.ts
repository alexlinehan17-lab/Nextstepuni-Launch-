/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail progress-report export (feature D2): the HTML reflects
 * the real figures, includes only sections with data, carries the SEC / self-
 * assessment provenance, and never fabricates numbers.
 */
import { describe, it, expect } from 'vitest';
import { buildReportHtml, reportFilename } from '../components/PaperTrail/progressReport';
import { type ProgressStats } from '../components/PaperTrail/progressStats';

const stats: ProgressStats = {
  totalMarks: 4,
  overallAvg: 62,
  papersPractised: 2,
  subjects: [{ subjectId: 'business', n: 3, avg: 55 }, { subjectId: 'mathematics', n: 1, avg: 80 }],
  weakestTopics: [{ subjectId: 'business', subtopicId: 'biz.marketing-mix', count: 2, avg: 40 }],
  gaps: { content: 0, process: 1, careless: 2, timing: 0 },
  gapLoss: { content: 0, process: 20, careless: 30, timing: 0 },
  deck: { total: 5, due: 1, fresh: 3 },
  streak: { current: 3, longest: 7, todayCount: 2, goal: 10, goalMet: false, activeToday: true, freezes: 0, protectedNow: false },
};

const opts = {
  stats,
  subjectName: (id: string) => (id === 'business' ? 'Business' : 'Mathematics'),
  topicName: (id: string) => (id === 'biz.marketing-mix' ? 'Marketing Mix' : id),
  dateIso: '2026-07-04',
};

describe('Paper Trail — progress report', () => {
  it('shows the headline figures', () => {
    const html = buildReportHtml(opts);
    expect(html).toContain('62%');
    expect(html).toContain('day streak (best 7)');
    expect(html).toContain('papers practised');
    expect(html).toContain('in spaced-review deck');
  });

  it('includes the accuracy, weak-topic and gap sections with real values', () => {
    const html = buildReportHtml(opts);
    expect(html).toContain('Accuracy by subject');
    expect(html).toContain('Business');
    expect(html).toContain('Weakest topics');
    expect(html).toContain('Marketing Mix');
    expect(html).toContain('Where marks are lost');
    expect(html).toContain('Careless slips');
  });

  it('omits sections with no data', () => {
    const empty: ProgressStats = { ...stats, subjects: [], weakestTopics: [], gaps: { content: 0, process: 0, careless: 0, timing: 0 } };
    const html = buildReportHtml({ ...opts, stats: empty });
    expect(html).not.toContain('Accuracy by subject');
    expect(html).not.toContain('Where marks are lost');
  });

  it('carries the self-assessment / SEC provenance and a dated filename', () => {
    expect(buildReportHtml(opts)).toContain('State Examinations Commission');
    expect(buildReportHtml(opts)).toContain('self-assessment');
    expect(reportFilename('2026-07-04')).toBe('practice-report-2026-07-04.html');
  });
});
