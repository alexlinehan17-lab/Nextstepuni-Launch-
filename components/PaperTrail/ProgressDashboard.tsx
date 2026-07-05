/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — progress dashboard (feature C1). One screen that pulls the whole
 * study loop together: streak + daily goal, self-mark accuracy overall and by
 * subject, weakest topics (one tap to drill), where marks are lost, and the
 * review-deck status. Every number comes from the student's own practice — no
 * inflation, and it reads empty honestly until they've done something.
 */

import React, { useMemo } from 'react';
import { ArrowLeft, ArrowRight, Award, Download, Flame, Repeat, Target, TrendingDown } from 'lucide-react';
import { computeProgress } from './progressStats';
import { masteredCount } from './topicMastery';
import { downloadReport } from './progressReport';
import GuardianConsent from './GuardianConsent';
import { siblingsFor, topicLabel, type TopicSibling } from './topics';
import { type GapKind } from './attemptStore';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const SUCCESS = '#3A8D5F';

const GAP_LABEL: Record<GapKind, string> = {
  content: 'Didn’t know it',
  process: 'Wrong method',
  careless: 'Careless slips',
  timing: 'Ran out of time',
};
const GAP_NUDGE: Record<GapKind, string> = {
  content: 'Revision gaps — go back to the notes.',
  process: 'Revisit the method, not just the facts.',
  careless: 'Slow down and check your working.',
  timing: 'Practise against the clock (Exam mode).',
};

/** Accuracy → token colour: red is never used; healthy is success, below is accent. */
const accColour = (avg: number) => (avg >= 66 ? SUCCESS : ACCENT);

interface Props {
  uid?: string;
  now: number;
  subjectLabel: (id: string) => string;
  onDrill: (t: TopicSibling) => void;
  onBack: () => void;
}

const Stat: React.FC<{ icon: React.ReactNode; value: string; label: string }> = ({ icon, value, label }) => (
  <div className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-3">
    <span className="flex items-center gap-1.5 mb-1" style={{ color: '#9e9186' }}>{icon}</span>
    <span className="block text-[22px] font-bold leading-none tabular-nums" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{value}</span>
    <span className="block text-[11px] mt-1" style={{ color: '#7a7068' }}>{label}</span>
  </div>
);

const ProgressDashboard: React.FC<Props> = ({ uid, now, subjectLabel, onDrill, onBack }) => {
  const p = useMemo(() => computeProgress(uid, now), [uid, now]);
  const mastered = useMemo(() => masteredCount(uid), [uid, now]);

  const topGap = (Object.entries(p.gaps) as [GapKind, number][])
    .filter(([, c]) => c > 0)
    .sort((a, b) => b[1] - a[1])[0];
  const gapTotal = Object.values(p.gaps).reduce((a, b) => a + b, 0);

  const drill = (subjectId: string, subtopicId: string) => {
    const sib = siblingsFor(subjectId, subtopicId)[0];
    if (sib) onDrill(sib);
  };

  const header = (
    <button onClick={onBack} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
      <ArrowLeft size={15} /> Paper Trail
    </button>
  );

  const nothingYet = p.totalMarks === 0 && p.deck.total === 0 && p.streak.longest === 0;

  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      {header}
      <h2 className="text-2xl font-semibold mb-1 flex items-center gap-2" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
        <Target size={20} style={{ color: ACCENT }} /> Your progress
      </h2>
      <p className="text-[13.5px] leading-relaxed mb-4" style={{ color: '#5a5550' }}>
        Everything you’ve practised, in one place — built entirely from your own self-marks and reviews.
      </p>

      {!nothingYet && (
        <button
          onClick={() => downloadReport({ stats: p, subjectName: subjectLabel, topicName: topicLabel, dateIso: new Date(now).toISOString().slice(0, 10) })}
          className="inline-flex items-center gap-1.5 mb-5 rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold border-2 transition-transform active:translate-y-0.5"
          style={{ borderColor: 'rgba(242,107,31,0.35)', color: ACCENT }}
        >
          <Download size={14} /> Export report
        </button>
      )}

      {nothingYet ? (
        <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
          Nothing to show yet. Open a paper and self-mark a few questions, or start a daily review — your accuracy, weak topics and streak will build here.
        </p>
      ) : (
        <>
          {/* Stat band */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mb-6">
            <Stat icon={<Flame size={14} />} value={`${p.streak.current}`} label={`day streak${p.streak.longest > p.streak.current ? ` · best ${p.streak.longest}` : ''}`} />
            <Stat icon={<Target size={14} />} value={p.totalMarks ? `${p.overallAvg}%` : '—'} label={`avg over ${p.totalMarks} self-mark${p.totalMarks === 1 ? '' : 's'}`} />
            <Stat icon={<TrendingDown size={14} />} value={`${p.papersPractised}`} label={`paper${p.papersPractised === 1 ? '' : 's'} practised`} />
            <Stat icon={<Repeat size={14} />} value={`${p.deck.due}`} label={`due · ${p.deck.total} in deck`} />
          </div>

          {mastered > 0 && (
            <p className="text-[13px] -mt-3 mb-6 flex items-center gap-1.5" style={{ color: SUCCESS }}>
              <Award size={15} /> <b style={{ color: '#1F5F3E' }}>{mastered}</b>&nbsp;topic{mastered === 1 ? '' : 's'} taken to mastery so far — proven by accuracy and retention.
            </p>
          )}

          {/* Accuracy by subject */}
          {p.subjects.length > 0 && (
            <section className="mb-6">
              <h3 className="text-[11px] font-bold uppercase tracking-[0.12em] mb-2.5" style={{ color: '#9e9186' }}>Accuracy by subject</h3>
              <div className="space-y-2">
                {p.subjects.map(s => (
                  <div key={s.subjectId} className="flex items-center gap-3">
                    <span className="w-28 shrink-0 text-[12.5px] font-medium truncate" style={{ color: INK }}>{subjectLabel(s.subjectId)}</span>
                    <span className="flex-1 h-2.5 rounded-full overflow-hidden" style={{ backgroundColor: '#e0dbd4' }}>
                      <span className="block h-full rounded-full" style={{ width: `${s.avg}%`, backgroundColor: accColour(s.avg) }} />
                    </span>
                    <span className="w-16 shrink-0 text-right text-[12px] tabular-nums" style={{ color: '#7a7068' }}>
                      <b style={{ color: INK }}>{s.avg}%</b> · {s.n}
                    </span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Weakest topics */}
          {p.weakestTopics.length > 0 && (
            <section className="mb-6">
              <h3 className="text-[11px] font-bold uppercase tracking-[0.12em] mb-2.5" style={{ color: '#9e9186' }}>Weakest topics — tap to drill</h3>
              <div className="space-y-1.5">
                {p.weakestTopics.slice(0, 6).map(t => (
                  <button
                    key={`${t.subjectId}-${t.subtopicId}`}
                    onClick={() => drill(t.subjectId, t.subtopicId)}
                    className="w-full flex items-center gap-3 rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3 py-2 text-left transition-transform active:translate-y-0.5 hover:border-[#F26B1F]"
                  >
                    <span className="shrink-0 w-11 text-[14px] font-bold tabular-nums" style={{ color: t.avg < 50 ? ACCENT : INK, fontFamily: "'Source Serif 4', serif" }}>{t.avg}%</span>
                    <span className="flex-1 min-w-0">
                      <span className="block text-[13px] font-semibold truncate" style={{ color: INK }}>{topicLabel(t.subtopicId)}</span>
                      <span className="block text-[11px] truncate" style={{ color: '#7a7068' }}>{subjectLabel(t.subjectId)} · {t.count} attempt{t.count === 1 ? '' : 's'}</span>
                    </span>
                    <ArrowRight size={15} className="shrink-0" style={{ color: ACCENT }} />
                  </button>
                ))}
              </div>
            </section>
          )}

          {/* Where marks are lost */}
          {gapTotal > 0 && (
            <section className="mb-2">
              <h3 className="text-[11px] font-bold uppercase tracking-[0.12em] mb-2.5" style={{ color: '#9e9186' }}>Where you lose marks</h3>
              <div className="space-y-2">
                {(Object.entries(p.gaps) as [GapKind, number][])
                  .filter(([, c]) => c > 0)
                  .sort((a, b) => b[1] - a[1])
                  .map(([g, c]) => (
                    <div key={g} className="flex items-center gap-3">
                      <span className="w-28 shrink-0 text-[12.5px] font-medium truncate" style={{ color: INK }}>{GAP_LABEL[g]}</span>
                      <span className="flex-1 h-2.5 rounded-full overflow-hidden" style={{ backgroundColor: '#e0dbd4' }}>
                        <span className="block h-full rounded-full" style={{ width: `${Math.round((c / gapTotal) * 100)}%`, backgroundColor: ACCENT }} />
                      </span>
                      <span className="w-10 shrink-0 text-right text-[12px] tabular-nums" style={{ color: '#7a7068' }}>{c}×</span>
                    </div>
                  ))}
              </div>
              {topGap && (
                <p className="mt-3 text-[11.5px]" style={{ color: '#5a5550' }}>
                  Biggest leak: <b style={{ color: '#8C3A0E' }}>{GAP_LABEL[topGap[0]]}</b>. {GAP_NUDGE[topGap[0]]}
                </p>
              )}
            </section>
          )}

          {/* Opt-in weekly guardian summary (E10) — gated; renders null until live. */}
          <GuardianConsent
            uid={uid}
            preview={{
              weekMinutes: 0,
              cardsReviewed: p.totalMarks,
              currentStreak: p.streak.current,
              focusTopic: p.weakestTopics[0] ? topicLabel(p.weakestTopics[0].subtopicId) : undefined,
            }}
          />
        </>
      )}
    </div>
  );
};

export default ProgressDashboard;
