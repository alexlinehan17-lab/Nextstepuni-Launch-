/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — topic revision-pack export (feature C2). Turns "every past
 * question on this topic" into a clean, printable HTML sheet the student can
 * save, print, or work offline. It lists only real SEC questions (year, level,
 * paper, question number) — there is no fabricated answer text; the marking
 * scheme in Paper Trail (or on examinations.ie) is the check. Pure string build
 * so it can be unit-tested; the DOM download is a thin wrapper.
 */

import { type TopicSibling } from './topics';

const LVL: Record<string, string> = { higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common' };
const paperAbbr = (k: string) => (k === 'p1' ? 'Paper 1' : k === 'p2' ? 'Paper 2' : '');

const esc = (s: string) =>
  s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]!));

export interface PackOptions {
  subjectLabel: string;
  topicLabel: string;
  questions: TopicSibling[];
  /** ISO date stamp (YYYY-MM-DD) — passed in, never read from the clock here. */
  dateIso: string;
}

/** A safe, print-friendly filename for the pack. */
export function packFilename(subjectLabel: string, topicLabel: string): string {
  const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  return `${slug(subjectLabel)}-${slug(topicLabel)}-revision-pack.html`;
}

/** Build the self-contained HTML for a topic revision pack. Pure. */
export function buildPackHtml(o: PackOptions): string {
  const years = new Set(o.questions.map(q => q.year));
  const rows = o.questions
    .map(q => {
      const bits = [LVL[q.level] ?? q.level, paperAbbr(q.paperKey), q.lang === 'iv' ? 'Gaeilge' : ''].filter(Boolean);
      return `      <tr><td class="yr">${q.year}</td><td>${esc(bits.join(' · '))}</td><td>Question ${esc(q.n)}</td><td class="chk"></td></tr>`;
    })
    .join('\n');

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(o.subjectLabel)} · ${esc(o.topicLabel)} — Revision pack</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: 'DM Sans', -apple-system, system-ui, sans-serif; color: #1a1a1a; max-width: 720px; margin: 32px auto; padding: 0 20px; }
  h1 { font-family: 'Source Serif 4', Georgia, serif; font-size: 24px; margin: 0 0 4px; }
  .sub { color: #7a7068; font-size: 13px; margin: 0 0 20px; }
  .intro { background: #FDEEDF; border-left: 3px solid #F26B1F; border-radius: 0 8px 8px 0; padding: 12px 14px; font-size: 13.5px; color: #8C3A0E; margin-bottom: 20px; }
  table { border-collapse: collapse; width: 100%; font-size: 13.5px; }
  th { text-align: left; text-transform: uppercase; font-size: 10.5px; letter-spacing: 0.08em; color: #9e9186; border-bottom: 2px solid #1a1a1a; padding: 6px 8px; }
  td { padding: 8px; border-bottom: 1px solid #e0dbd4; }
  td.yr { font-family: 'Source Serif 4', Georgia, serif; font-weight: 700; width: 60px; }
  td.chk { width: 28px; }
  td.chk::before { content: ''; display: inline-block; width: 15px; height: 15px; border: 1.5px solid #d0cdc8; border-radius: 4px; vertical-align: middle; }
  footer { margin-top: 24px; font-size: 11px; color: #9e9186; line-height: 1.5; }
  @media print { body { margin: 0; } .intro { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
</style>
</head>
<body>
  <h1>${esc(o.topicLabel)}</h1>
  <p class="sub">${esc(o.subjectLabel)} · revision pack · generated ${esc(o.dateIso)}</p>
  <div class="intro">
    Every past-paper question on <b>${esc(o.topicLabel)}</b> — ${o.questions.length} question${o.questions.length === 1 ? '' : 's'} across ${years.size} year${years.size === 1 ? '' : 's'}.
    Work each one, then check yourself against its marking scheme in Paper Trail. Tick the box when you can answer it cold.
  </div>
  <table>
    <thead><tr><th>Year</th><th>Level / paper</th><th>Question</th><th></th></tr></thead>
    <tbody>
${rows}
    </tbody>
  </table>
  <footer>
    Examination material © State Examinations Commission, reproduced with attribution.
    This sheet lists question references only — open each paper and its official marking scheme to study it.
  </footer>
</body>
</html>`;
}

/** Build the pack and trigger a browser download. Browser-only. */
export function downloadPack(o: PackOptions): void {
  const html = buildPackHtml(o);
  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = packFilename(o.subjectLabel, o.topicLabel);
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
