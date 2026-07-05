/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — learning milestones (feature E5). Daily practice stays quiet;
 * this reserves a real, animated, shareable celebration for the moments that
 * actually matter — a streak tier reached, or a count of topics genuinely taken
 * to mastery. Each milestone fires once: acknowledged ids are remembered per uid
 * so a moment never repeats.
 */

import { getStreak } from './streakStore';
import { masteredCount } from './topicMastery';

export interface Milestone {
  id: string;
  kind: 'streak' | 'mastery';
  value: number;
  title: string;
  blurb: string;
}

const STREAK_TIERS = [7, 14, 30, 50, 100];
const MASTERY_TIERS = [1, 5, 10, 25];

const streakMilestone = (t: number): Milestone => ({
  id: `streak-${t}`,
  kind: 'streak',
  value: t,
  title: `${t}-day streak`,
  blurb: t >= 30 ? 'That is real, durable habit — the thing that moves grades.' : 'Consistency compounds. Keep the run going.',
});
const masteryMilestone = (t: number): Milestone => ({
  id: `mastery-${t}`,
  kind: 'mastery',
  value: t,
  title: t === 1 ? 'First topic mastered' : `${t} topics mastered`,
  blurb: 'Proven by accuracy and retention — not just seen, but owned.',
});

/** Pure: which milestones are newly reached given the current stats and the set
 *  of already-acknowledged ids. Biggest first. */
export function newMilestones(streakLongest: number, mastered: number, seen: Set<string>): Milestone[] {
  const out: Milestone[] = [];
  for (const t of STREAK_TIERS) if (streakLongest >= t && !seen.has(`streak-${t}`)) out.push(streakMilestone(t));
  for (const t of MASTERY_TIERS) if (mastered >= t && !seen.has(`mastery-${t}`)) out.push(masteryMilestone(t));
  return out.sort((a, b) => b.value - a.value);
}

// ─── acknowledgement store ──────────────────────────────────

const PREFIX = 'pt:milestones:';
const readSeen = (uid?: string): Set<string> => {
  try {
    const raw = localStorage.getItem(PREFIX + (uid || 'anon'));
    return new Set(raw ? (JSON.parse(raw) as string[]) : []);
  } catch {
    return new Set();
  }
};
const writeSeen = (uid: string | undefined, seen: Set<string>) => {
  try {
    localStorage.setItem(PREFIX + (uid || 'anon'), JSON.stringify([...seen]));
  } catch {
    /* private mode — degrade silently */
  }
};

/** Milestones reached but not yet celebrated (live stats vs acknowledged ids). */
export function pendingMilestones(uid: string | undefined, now: number): Milestone[] {
  return newMilestones(getStreak(uid, now).longest, masteredCount(uid), readSeen(uid));
}

export function acknowledgeMilestone(uid: string | undefined, id: string): void {
  const seen = readSeen(uid);
  seen.add(id);
  writeSeen(uid, seen);
}

// ─── shareable card ─────────────────────────────────────────

const esc = (s: string) =>
  s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]!));

export function buildMilestoneCardHtml(m: Milestone, dateIso: string): string {
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(m.title)} — Nextstepuni</title>
<style>
  body { margin:0; min-height:100vh; display:grid; place-items:center; background:#efece6; font-family:system-ui,-apple-system,sans-serif; }
  .card { width:min(92vw,420px); background:#fff; border:2px solid #1a1a1a; border-radius:20px; box-shadow:6px 6px 0 0 #1a1a1a; padding:34px 30px; text-align:center; }
  .badge { width:64px; height:64px; margin:0 auto 16px; border-radius:18px; background:#FDEEDF; display:grid; place-items:center; font-size:30px; }
  .eyebrow { font-size:11px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#9a8f82; }
  h1 { font-family:Georgia,serif; font-size:28px; margin:8px 0 10px; color:#1a1a1a; }
  p { font-size:14.5px; line-height:1.5; color:#5a5550; margin:0 0 18px; }
  .foot { font-size:11px; color:#9e9186; border-top:1px solid #e0dbd4; padding-top:12px; }
  .brand { font-weight:700; color:#F26B1F; }
</style></head>
<body><div class="card">
  <div class="badge">${m.kind === 'streak' ? '🔥' : '🎯'}</div>
  <div class="eyebrow">Milestone reached</div>
  <h1>${esc(m.title)}</h1>
  <p>${esc(m.blurb)}</p>
  <div class="foot"><span class="brand">Nextstepuni</span> · Paper Trail · ${esc(dateIso)}</div>
</div></body></html>`;
}

export function downloadMilestoneCard(m: Milestone, dateIso: string): void {
  const blob = new Blob([buildMilestoneCardHtml(m, dateIso)], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `nextstepuni-${m.id}.html`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
