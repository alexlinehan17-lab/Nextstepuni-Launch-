/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Your term so far" — a Duolingo year-in-review-style summary the student
 * can save as an image. The on-screen card and the exported PNG are drawn
 * from the same numbers; the export is painted by hand on a canvas so it
 * needs no extra dependencies.
 */

import React, { useMemo, useState } from 'react';
import { Download } from 'lucide-react';
import { type StreakData } from '../../hooks/useStreak';
import { type StudySessionRecord } from '../../utils/strategyRegistry';

interface Props {
  sessions: StudySessionRecord[];
  streak: StreakData;
}

/** The school term starts on 1 September; before September we look back to
 *  the previous year's 1 September so the card never renders empty in May. */
const termStart = (now: Date): Date => {
  const year = now.getMonth() >= 8 ? now.getFullYear() : now.getFullYear() - 1;
  return new Date(year, 8, 1);
};

const TermReviewCard: React.FC<Props> = ({ sessions, streak }) => {
  const [saving, setSaving] = useState(false);

  const stats = useMemo(() => {
    const start = termStart(new Date()).getTime();
    const inTerm = sessions.filter(s => (s.startedAt || 0) >= start);
    let seconds = 0;
    const bySubject = new Map<string, number>();
    for (const s of inTerm) {
      seconds += s.actualSeconds || 0;
      bySubject.set(s.subject, (bySubject.get(s.subject) ?? 0) + (s.actualSeconds || 0));
    }
    const top = [...bySubject.entries()].sort((a, b) => b[1] - a[1])[0];
    const hours = seconds / 3600;
    return {
      hours: hours >= 10 ? String(Math.round(hours)) : (Math.round(hours * 10) / 10).toString(),
      sessions: inTerm.length,
      topSubject: top ? top[0] : '—',
      bestStreak: streak.longestStreak,
      startLabel: termStart(new Date()).toLocaleDateString('en-IE', { day: 'numeric', month: 'long' }),
    };
  }, [sessions, streak.longestStreak]);

  const saveImage = () => {
    setSaving(true);
    try {
      const scale = 2;
      const W = 620, H = 420;
      const canvas = document.createElement('canvas');
      canvas.width = W * scale; canvas.height = H * scale;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      ctx.scale(scale, scale);
      // Ground
      ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, W, H);
      ctx.strokeStyle = '#383838'; ctx.lineWidth = 2; ctx.strokeRect(6, 6, W - 12, H - 12);
      // Masthead
      ctx.fillStyle = '#A0968D';
      ctx.font = '700 11px "DM Sans", sans-serif';
      ctx.fillText('N E X T S T E P U N I   ·   T E R M   I N   R E V I E W', 36, 48);
      ctx.fillStyle = '#1A1A1A';
      ctx.font = '700 34px "Source Serif 4", Georgia, serif';
      ctx.fillText('The work is adding up.', 36, 92);
      ctx.fillStyle = '#78716C';
      ctx.font = '400 13px "DM Sans", sans-serif';
      ctx.fillText(`Since ${stats.startLabel}`, 36, 116);
      // Stat cells
      const cells = [
        { v: `${stats.hours}h`, l: 'FOCUSED TIME' },
        { v: String(stats.sessions), l: 'SESSIONS' },
        { v: stats.topSubject.length > 14 ? stats.topSubject.slice(0, 13) + '…' : stats.topSubject, l: 'TOP SUBJECT' },
        { v: String(stats.bestStreak), l: 'BEST STREAK' },
      ];
      cells.forEach((cell, i) => {
        const x = 36 + (i % 2) * 290;
        const y = 178 + Math.floor(i / 2) * 96;
        ctx.fillStyle = '#1A1A1A';
        ctx.font = '600 40px "Source Serif 4", Georgia, serif';
        ctx.fillText(cell.v, x, y);
        ctx.fillStyle = '#A0968D';
        ctx.font = '700 10px "DM Sans", sans-serif';
        ctx.fillText(cell.l.split('').join(' '), x + 2, y + 22);
      });
      // The apricot signature strip
      const barY = H - 58;
      for (let i = 0; i < 24; i++) {
        ctx.fillStyle = `rgba(242, 107, 31, ${0.25 + 0.5 * Math.abs(Math.sin(i * 1.7))})`;
        ctx.fillRect(36 + i * 12, barY - 4 - 14 * Math.abs(Math.sin(i * 1.7)), 7, 14 * Math.abs(Math.sin(i * 1.7)) + 4);
      }
      ctx.fillStyle = '#A0968D';
      ctx.font = '400 11px "DM Sans", sans-serif';
      ctx.fillText('nextstepuni-app.web.app', W - 190, H - 28);

      canvas.toBlob(blob => {
        if (!blob) return;
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'nextstepuni-term-in-review.png';
        document.body.appendChild(a);
        a.click();
        a.remove();
      }, 'image/png');
    } finally {
      setSaving(false);
    }
  };

  return (
    <article className="lg:col-span-12 rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-5 py-4 sm:px-6 sm:py-5">
      <div className="flex flex-wrap items-end justify-between gap-x-8 gap-y-4">
        <div className="min-w-0">
          <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Term in review · since {stats.startLabel}</p>
          <div className="mt-3 flex flex-wrap items-end gap-x-8 gap-y-3">
            {[
              { v: `${stats.hours}h`, l: 'Focused time' },
              { v: String(stats.sessions), l: 'Sessions' },
              { v: stats.topSubject, l: 'Top subject' },
              { v: String(stats.bestStreak), l: 'Best streak' },
            ].map(cell => (
              <div key={cell.l} className="min-w-0">
                <p className="truncate font-serif text-[26px] font-semibold leading-none tabular-nums text-[var(--ink-primary)]">{cell.v}</p>
                <p className="mt-1.5 text-[9px] font-bold uppercase tracking-[0.15em] text-[var(--ink-muted)]">{cell.l}</p>
              </div>
            ))}
          </div>
        </div>
        <button
          onClick={saveImage}
          disabled={saving || stats.sessions === 0}
          className="inline-flex min-h-10 shrink-0 items-center gap-1.5 rounded-xl border border-[var(--outline-soft)] px-4 text-xs font-bold text-[var(--ink-secondary)] transition-colors hover:border-[var(--outline-strong)] disabled:opacity-40"
        >
          <Download size={13} /> Save as image
        </button>
      </div>
    </article>
  );
};

export default TermReviewCard;
