/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — printable progress report (feature D2). Turns a student's own
 * practice (self-mark accuracy, weakest topics, where marks are lost, streak)
 * into a clean HTML sheet they can print or hand to a teacher — useful in the
 * DEIS/school context. Every figure is the student's own self-assessment against
 * the official SEC marking schemes; nothing is fabricated or inferred. Pure
 * string build so it can be unit-tested; the DOM download is a thin wrapper.
 */

import { type ProgressStats } from './progressStats';
import { type GapKind } from './attemptStore';

const GAP_LABEL: Record<GapKind, string> = {
  content: 'Didn’t know it',
  process: 'Wrong method',
  careless: 'Careless slips',
  timing: 'Ran out of time',
};

const esc = (s: string) =>
  s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]!));

export interface ReportOptions {
  stats: ProgressStats;
  subjectName: (id: string) => string;
  topicName: (id: string) => string;
  /** ISO date stamp (YYYY-MM-DD) — passed in, never read from the clock here. */
  dateIso: string;
}

export function reportFilename(dateIso: string): string {
  return `practice-report-${dateIso}.html`;
}

/** Build the self-contained HTML for a practice report. Pure. */
export function buildReportHtml(o: ReportOptions): string {
  const p = o.stats;
  const gapTotal = Object.values(p.gaps).reduce((a, b) => a + b, 0);

  const subjectRows = p.subjects
    .map(s => `      <tr><td>${esc(o.subjectName(s.subjectId))}</td><td class="num">${s.avg}%</td><td class="num">${s.n}</td></tr>`)
    .join('\n');

  const topicRows = p.weakestTopics
    .slice(0, 8)
    .map(t => `      <tr><td>${esc(o.topicName(t.subtopicId))}</td><td>${esc(o.subjectName(t.subjectId))}</td><td class="num">${t.avg}%</td><td class="num">${t.count}</td></tr>`)
    .join('\n');

  const gapRows = (Object.entries(p.gaps) as [GapKind, number][])
    .filter(([, c]) => c > 0)
    .sort((a, b) => b[1] - a[1])
    .map(([g, c]) => `      <tr><td>${esc(GAP_LABEL[g])}</td><td class="num">${c}</td><td class="num">${Math.round((c / gapTotal) * 100)}%</td></tr>`)
    .join('\n');

  const section = (title: string, head: string, rows: string) =>
    rows ? `  <h2>${title}</h2>\n  <table>\n    <thead><tr>${head}</tr></thead>\n    <tbody>\n${rows}\n    </tbody>\n  </table>\n` : '';

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Practice report — ${esc(o.dateIso)}</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: 'DM Sans', -apple-system, system-ui, sans-serif; color: #1a1a1a; max-width: 720px; margin: 32px auto; padding: 0 20px; }
  h1 { font-family: 'Source Serif 4', Georgia, serif; font-size: 24px; margin: 0 0 4px; }
  h2 { font-family: 'Source Serif 4', Georgia, serif; font-size: 16px; margin: 24px 0 8px; }
  .sub { color: #7a7068; font-size: 13px; margin: 0 0 20px; }
  .band { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 8px; }
  .stat { flex: 1 1 120px; border: 2px solid #1a1a1a; border-radius: 12px; padding: 10px 12px; }
  .stat .v { font-family: 'Source Serif 4', Georgia, serif; font-size: 22px; font-weight: 700; }
  .stat .l { font-size: 11px; color: #7a7068; }
  table { border-collapse: collapse; width: 100%; font-size: 13px; margin-top: 4px; }
  th { text-align: left; text-transform: uppercase; font-size: 10px; letter-spacing: 0.07em; color: #9e9186; border-bottom: 2px solid #1a1a1a; padding: 6px 8px; }
  td { padding: 7px 8px; border-bottom: 1px solid #e0dbd4; }
  td.num { text-align: right; font-variant-numeric: tabular-nums; }
  footer { margin-top: 24px; font-size: 11px; color: #9e9186; line-height: 1.5; }
  @media print { body { margin: 0; } .stat { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
</style>
</head>
<body>
  <h1>Practice report</h1>
  <p class="sub">Generated ${esc(o.dateIso)} · from the student’s own self-marks in Paper Trail</p>
  <div class="band">
    <div class="stat"><div class="v">${p.streak.current}</div><div class="l">day streak (best ${p.streak.longest})</div></div>
    <div class="stat"><div class="v">${p.totalMarks ? `${p.overallAvg}%` : '—'}</div><div class="l">avg over ${p.totalMarks} self-mark${p.totalMarks === 1 ? '' : 's'}</div></div>
    <div class="stat"><div class="v">${p.papersPractised}</div><div class="l">paper${p.papersPractised === 1 ? '' : 's'} practised</div></div>
    <div class="stat"><div class="v">${p.deck.total}</div><div class="l">in spaced-review deck</div></div>
  </div>
${section('Accuracy by subject', '<th>Subject</th><th class="num">Avg</th><th class="num">Attempts</th>', subjectRows)}${section('Weakest topics', '<th>Topic</th><th>Subject</th><th class="num">Avg</th><th class="num">Attempts</th>', topicRows)}${section('Where marks are lost', '<th>Reason</th><th class="num">Count</th><th class="num">Share</th>', gapRows)}
  <footer>
    Figures reflect the student’s self-assessment against the official State Examinations Commission marking schemes, recorded as they practised.
    Examination material © State Examinations Commission.
  </footer>
</body>
</html>`;
}

/** Build the report and trigger a browser download. Browser-only. */
export function downloadReport(o: ReportOptions): void {
  const html = buildReportHtml(o);
  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = reportFilename(o.dateIso);
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
