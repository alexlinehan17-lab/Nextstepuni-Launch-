/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo } from 'react';
import { MotionDiv } from './Motion';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { type CategoryType } from './KnowledgeTree';
import { type CourseData } from './Library';
import { type StreakData } from '../hooks/useStreak';
import { type FocusRecommendation } from '../hooks/useTodaysFocus';
import MountainLandscape, { type WorldProgress } from './MountainLandscape';
import WorldIconBlob, { type WorldId } from './WorldIconBlob';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface DashboardViewProps {
  userProgress: UserProgress;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
  streak: StreakData;
  recommendation: FocusRecommendation | null;
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
  pointsBalance: number;
}

// Map the five world ids to their backing course categories. The five
// worlds are a subset of the seven categories — 'the-shield' and
// 'the-launchpad' aren't represented as climbs on this page.
const WORLD_TO_CATEGORY: Record<WorldId, CategoryType> = {
  mind:   'architecture-mindset',
  growth: 'science-growth',
  learn:  'learning-cheat-codes',
  decode: 'subject-specific-science',
  exam:   'exam-zone',
};

// Inverse lookup used by Today's Focus to pick the world icon for a
// recommended module's category. Categories that aren't worlds (the-shield,
// the-launchpad) fall back to the learn icon at the call site.
const CATEGORY_TO_WORLD: Partial<Record<CategoryType, WorldId>> = {
  'architecture-mindset':       'mind',
  'science-growth':             'growth',
  'learning-cheat-codes':       'learn',
  'subject-specific-science':   'decode',
  'exam-zone':                  'exam',
};

const WORLD_LABEL: Record<WorldId, string> = {
  mind:   'Mind',
  growth: 'Growth',
  learn:  'Learn',
  decode: 'Decode',
  exam:   'Exam',
};

const WORLD_ORDER: WorldId[] = ['mind', 'growth', 'learn', 'decode', 'exam'];

const SERIF: React.CSSProperties = { fontFamily: "'Source Serif 4', serif" };
const SANS: React.CSSProperties = { fontFamily: "'DM Sans', system-ui, sans-serif" };

interface StatCellProps {
  eyebrow: string;
  value: string;
  meta: string;
  /** Furthest-along uses a smaller serif so the longer composite value fits. */
  smallValue?: boolean;
}
const StatCell: React.FC<StatCellProps> = ({ eyebrow, value, meta, smallValue }) => (
  <div>
    <p
      className="uppercase"
      style={{ ...SANS, fontSize: 11, fontWeight: 500, letterSpacing: '1.5px', color: 'rgba(0,0,0,0.5)', margin: 0 }}
    >
      {eyebrow}
    </p>
    <p
      style={{
        ...SERIF,
        fontSize: smallValue ? 22 : 36,
        fontWeight: 500,
        color: '#1a1a1a',
        margin: 0,
        marginTop: 8,
        lineHeight: 1.05,
      }}
    >
      {value}
    </p>
    <p
      style={{ ...SANS, fontSize: 12, color: 'rgba(0,0,0,0.55)', margin: 0, marginTop: 6 }}
    >
      {meta}
    </p>
  </div>
);

const DashboardView: React.FC<DashboardViewProps> = ({
  userProgress,
  allCourses,
  categoryTitles: _categoryTitles,
  streak,
  recommendation,
  onSelectModule,
  onBack,
  pointsBalance,
}) => {
  // Per-world progress: count modules in each of the five categories and
  // how many are completed. The mountain landscape, the page subtitle,
  // and the "Furthest along" stat all derive from this.
  const worldProgress = useMemo<Record<WorldId, WorldProgress>>(() => {
    const out = {} as Record<WorldId, WorldProgress>;
    for (const w of WORLD_ORDER) {
      const cat = WORLD_TO_CATEGORY[w];
      const courses = allCourses.filter(c => c.category === cat);
      const completed = courses.filter(c => {
        const p = userProgress[c.id];
        return p && p.unlockedSection >= c.sectionsCount;
      }).length;
      out[w] = { completed, total: courses.length };
    }
    return out;
  }, [allCourses, userProgress]);

  const fiveWorldTotal = WORLD_ORDER.reduce((acc, w) => acc + worldProgress[w].total, 0);
  const fiveWorldCompleted = WORLD_ORDER.reduce((acc, w) => acc + worldProgress[w].completed, 0);
  const overallPct = fiveWorldTotal > 0 ? Math.round((fiveWorldCompleted / fiveWorldTotal) * 100) : 0;

  // Furthest along — the world with the highest completion ratio. Ties
  // resolve to the world that appears first in WORLD_ORDER.
  const furthest = useMemo(() => {
    let bestRatio = -1;
    let bestWorld: WorldId = 'mind';
    for (const w of WORLD_ORDER) {
      const wp = worldProgress[w];
      if (wp.total === 0) continue;
      const ratio = wp.completed / wp.total;
      if (ratio > bestRatio) {
        bestRatio = ratio;
        bestWorld = w;
      }
    }
    const wp = worldProgress[bestWorld];
    const pct = wp.total > 0 ? Math.round(bestRatio * 100) : 0;
    return { world: bestWorld, pct, completed: wp.completed };
  }, [worldProgress]);

  const todayLabel = useMemo(
    () => new Date().toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }),
    []
  );

  return (
    <div className="min-h-screen bg-[#FDF8F0] dark:bg-zinc-950">
      {/* Back arrow row */}
      <div className="max-w-5xl mx-auto px-6 pt-6">
        <button
          onClick={onBack}
          aria-label="Back"
          className="w-10 h-10 rounded-xl flex items-center justify-center bg-white border border-[#EDEBE8] hover:bg-[#F8F4EC] transition-colors"
          style={{ boxShadow: '0 1px 2px rgba(28,25,23,0.04)' }}
        >
          <ArrowLeft size={18} className="text-[#1a1a1a]" />
        </button>
      </div>

      {/* Single content card — the new mountain hero */}
      <div className="max-w-5xl mx-auto px-6 pt-6 pb-10">
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] as number[] }}
          className="rounded-3xl bg-white p-7 md:p-10"
          style={{ boxShadow: '0 4px 28px rgba(28,25,23,0.06), 0 1px 3px rgba(28,25,23,0.04)' }}
        >
          {/* 1. Eyebrow row */}
          <div className="flex items-center justify-between">
            <span
              className="uppercase"
              style={{ ...SANS, fontSize: 11, fontWeight: 500, letterSpacing: '1.8px', color: 'rgba(0,0,0,0.5)' }}
            >
              My Progress
            </span>
            <span
              style={{ ...SANS, fontSize: 12, color: 'rgba(0,0,0,0.5)' }}
            >
              {todayLabel}
            </span>
          </div>

          {/* 2. Title */}
          <h1
            style={{
              ...SERIF,
              fontSize: 'clamp(32px, 4.5vw, 44px)',
              fontWeight: 500,
              letterSpacing: '-0.8px',
              lineHeight: 1.05,
              color: '#1a1a1a',
              margin: 0,
              marginTop: 22,
            }}
          >
            Five climbs, all your own.
          </h1>

          {/* 3. Italic sub-headline */}
          <p
            style={{
              ...SERIF,
              fontStyle: 'italic',
              fontSize: 17,
              color: '#2A7D6F',
              margin: 0,
              marginTop: 10,
            }}
          >
            {fiveWorldCompleted} of {fiveWorldTotal} modules · each mountain fills as you progress
          </p>

          {/* 4. The mountain landscape */}
          <div className="mt-8">
            <MountainLandscape progress={worldProgress} />
          </div>

          {/* 5. Hairline rule */}
          <div className="mt-2 mb-7" style={{ borderTop: '1px solid rgba(0,0,0,0.08)' }} />

          {/* 6. Stat row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
            <StatCell
              eyebrow="Overall"
              value={`${overallPct}%`}
              meta={`${fiveWorldCompleted} of ${fiveWorldTotal} modules`}
            />
            <StatCell
              eyebrow="Streak"
              value={String(streak.currentStreak)}
              meta="days running"
            />
            <StatCell
              eyebrow="Journey points"
              value={String(pointsBalance)}
              meta="earned to date"
            />
            <StatCell
              eyebrow="Furthest along"
              value={`${WORLD_LABEL[furthest.world]} · ${furthest.pct}%`}
              meta={`${furthest.completed} module${furthest.completed === 1 ? '' : 's'} complete`}
              smallValue
            />
          </div>
        </MotionDiv>
      </div>

      {/* ── Today's Focus — editorial cream card ── */}
      <div className="max-w-5xl mx-auto px-6 pb-24">
        {recommendation && recommendation.reason !== 'all-complete' && (() => {
          const focusCourse = allCourses.find(c => c.id === recommendation.moduleId);
          const focusWorld: WorldId = (focusCourse && CATEGORY_TO_WORLD[focusCourse.category]) || 'learn';

          return (
            <MotionDiv
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.18, duration: 0.4, ease: [0.16, 1, 0.3, 1] as number[] }}
              className="mt-2"
            >
              <p
                className="uppercase mb-4"
                style={{ ...SANS, fontSize: 11, fontWeight: 500, letterSpacing: '1.8px', color: 'rgba(0,0,0,0.5)' }}
              >
                Today's Focus
              </p>
              <button
                onClick={() => onSelectModule(recommendation.moduleId)}
                className="w-full text-left flex items-center gap-5 px-6 py-5 group transition-shadow hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(42,125,111,0.35)]"
                style={{
                  background: '#FFFFFF',
                  border: '1px solid #E8E2D8',
                  borderRadius: 22,
                  boxShadow: '0 4px 28px rgba(28,25,23,0.06), 0 1px 3px rgba(28,25,23,0.04)',
                }}
              >
                {/* World icon — painted blob behind hand-drawn ink illustration,
                    matching the same recipe used elsewhere in the app. */}
                <WorldIconBlob world={focusWorld} size={72} compact />


                {/* Title + subtext + terracotta accent */}
                <div className="flex-1 min-w-0">
                  <h3
                    style={{
                      ...SERIF,
                      fontSize: 22,
                      fontWeight: 500,
                      letterSpacing: '-0.4px',
                      color: '#1a1a1a',
                      margin: 0,
                      lineHeight: 1.2,
                    }}
                  >
                    {recommendation.title}
                  </h3>
                  <p
                    style={{
                      ...SANS,
                      fontSize: 13,
                      color: 'rgba(0,0,0,0.55)',
                      margin: 0,
                      marginTop: 5,
                    }}
                  >
                    {recommendation.reason === 'in-progress' ? 'Continue where you left off' : 'Start this module'}
                  </p>
                  {/* Terracotta accent — small underline */}
                  <div
                    aria-hidden="true"
                    style={{
                      width: 28,
                      height: 2,
                      background: '#D85F47',
                      borderRadius: 1,
                      marginTop: 8,
                    }}
                  />
                </div>

                {/* Simple charcoal arrow */}
                <div
                  className="shrink-0 transition-transform group-hover:translate-x-1"
                  style={{ color: '#1a1a1a' }}
                >
                  <ArrowRight size={22} strokeWidth={1.6} />
                </div>
              </button>
            </MotionDiv>
          );
        })()}
      </div>
    </div>
  );
};

export default DashboardView;
