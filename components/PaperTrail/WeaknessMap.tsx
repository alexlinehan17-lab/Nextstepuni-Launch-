/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — "Your practice" weakness map (Tier 3). Aggregates the student's
 * self-marks (attemptStore) by curriculum topic, surfaces the weakest topics,
 * and offers a one-tap drill into that topic across years. Closes the loop:
 * sit → self-mark → see your weak spots → drill them.
 *
 * Renders nothing until the student has self-marked at least one question.
 */

import React, { useMemo } from 'react';
import { TrendingDown, ArrowRight } from 'lucide-react';
import { allMarks, type GapKind } from './attemptStore';
import { siblingsFor, topicLabel, topicsForPaper, type TopicSibling } from './topics';
import { type PaperLang, type PaperLevel } from '../../types/paperTrail';

const GAP_LABEL: Record<GapKind, string> = {
  content: 'Didn’t know it',
  process: 'Wrong method',
  careless: 'Careless slips',
  timing: 'Ran out of time',
};

interface TopicAgg {
  subjectId: string;
  subtopicId: string;
  label: string;
  count: number;
  avg: number; // 0-100
}

const WeaknessMap: React.FC<{
  uid?: string;
  subjectName: (id: string) => string;
  onDrill: (t: TopicSibling) => void;
}> = ({ uid, subjectName, onDrill }) => {
  const { topics, overall, gaps } = useMemo(() => {
    const marks = allMarks(uid);
    const byTopic = new Map<string, { subjectId: string; subtopicId: string; sum: number; n: number }>();
    const gapCount: Record<GapKind, number> = { content: 0, process: 0, careless: 0, timing: 0 };
    let sum = 0;
    for (const m of marks) {
      if (m.gap) gapCount[m.gap]++;
      const pct = m.max ? (m.score / m.max) * 100 : m.score;
      sum += pct;
      const tags = topicsForPaper(m.subjectId, m.year, m.level as PaperLevel, m.lang as PaperLang, m.fileid);
      const tag = tags?.q.find(q => q.n === m.n);
      if (!tag) continue;
      const key = `${m.subjectId}|${tag.primary}`;
      const cur = byTopic.get(key) ?? { subjectId: m.subjectId, subtopicId: tag.primary, sum: 0, n: 0 };
      cur.sum += pct;
      cur.n += 1;
      byTopic.set(key, cur);
    }
    const aggs: TopicAgg[] = [...byTopic.values()].map(v => ({
      subjectId: v.subjectId,
      subtopicId: v.subtopicId,
      label: topicLabel(v.subtopicId),
      count: v.n,
      avg: Math.round(v.sum / v.n),
    }));
    // weakest first; only topics with a real attempt
    aggs.sort((a, b) => a.avg - b.avg || b.count - a.count);
    return {
      topics: aggs.slice(0, 6),
      overall: { n: marks.length, avg: marks.length ? Math.round(sum / marks.length) : 0 },
      gaps: gapCount,
    };
  }, [uid]);

  if (overall.n === 0) return null;

  const topGap = (Object.entries(gaps) as [GapKind, number][])
    .filter(([, c]) => c > 0)
    .sort((a, b) => b[1] - a[1])[0];

  const drill = (t: TopicAgg) => {
    const sib = siblingsFor(t.subjectId, t.subtopicId)[0];
    if (sib) onDrill(sib);
  };

  return (
    <div className="mb-6 rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-4">
      <div className="flex items-center justify-between gap-2 mb-3">
        <h3 className="text-[15px] font-semibold flex items-center gap-1.5" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
          <TrendingDown size={16} style={{ color: '#F26B1F' }} /> Your practice
        </h3>
        <span className="text-[11px]" style={{ color: '#7a7068' }}>
          {overall.n} self-marked · avg {overall.avg}%
        </span>
      </div>

      {topics.length > 0 ? (
        <>
          <p className="text-[11px] font-bold uppercase tracking-[0.1em] mb-2" style={{ color: '#9e9186' }}>
            Weakest topics — tap to drill
          </p>
          <div className="space-y-1.5">
            {topics.map(t => (
              <button
                key={`${t.subjectId}-${t.subtopicId}`}
                onClick={() => drill(t)}
                className="w-full flex items-center gap-3 rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-2 text-left transition-transform active:translate-y-0.5 hover:border-[#F26B1F]"
              >
                <span className="shrink-0 w-11 text-[14px] font-bold tabular-nums" style={{ color: t.avg < 50 ? '#F26B1F' : '#1a1a1a', fontFamily: "'Source Serif 4', serif" }}>
                  {t.avg}%
                </span>
                <span className="flex-1 min-w-0">
                  <span className="block text-[13px] font-semibold truncate" style={{ color: '#1a1a1a' }}>{t.label}</span>
                  <span className="block text-[11px] truncate" style={{ color: '#7a7068' }}>
                    {subjectName(t.subjectId)} · {t.count} attempt{t.count === 1 ? '' : 's'}
                  </span>
                </span>
                <ArrowRight size={15} className="shrink-0" style={{ color: '#F26B1F' }} />
              </button>
            ))}
          </div>
        </>
      ) : (
        <p className="text-[12px]" style={{ color: '#7a7068' }}>
          Self-mark questions in a tagged subject to see your weak topics here.
        </p>
      )}

      {topGap && (
        <p className="mt-3 text-[11.5px]" style={{ color: '#5a5550' }}>
          Most common gap: <b style={{ color: '#8C3A0E' }}>{GAP_LABEL[topGap[0]]}</b> ({topGap[1]}×).
          {topGap[0] === 'careless' && ' Slow down and check your working.'}
          {topGap[0] === 'process' && ' Revisit the method, not just the facts.'}
          {topGap[0] === 'content' && ' These are revision gaps — go back to the notes.'}
          {topGap[0] === 'timing' && ' Practise against the clock (Exam mode).'}
        </p>
      )}
    </div>
  );
};

export default WeaknessMap;
