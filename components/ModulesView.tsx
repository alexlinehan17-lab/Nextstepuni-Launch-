/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ModulesView — the category overview. Five worlds: Mind, Growth, Learn,
 * Decode, Exam. Hero + satellites; never an equal-weight grid.
 *
 * Hero is dynamic — driven by the most active category from progress data,
 * falling back to Mind. The user can promote any satellite by tapping it.
 *
 * Critical: all five cards are always rendered in a single 12-col grid,
 * each with a stable layoutId. Promotion just toggles which card holds the
 * hero (col-span-12) vs. satellite (col-span-3) class. No card ever
 * unmounts during promotion, so the hero slot is never empty.
 *
 * Visual register: cream ground, radial-focused gradients (focal point
 * varies per category to break repetition), a faint SVG noise grain, a
 * 1px white inner highlight on the top edge for ceramic quality.
 */

import React, { useState } from 'react';
import { motion, LayoutGroup } from 'framer-motion';
import { type CourseData } from './Library';
import { type CategoryType } from './KnowledgeTree';
import { MODULE_SECTIONS } from '../moduleSections';
import { WorldIconBlob, type WorldId } from './WorldIconBlob';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface ModulesViewProps {
  onBack: () => void;
  onSelectCategory: (category: CategoryType) => void;
  onSelectModule: (moduleId: string) => void;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
  userProgress: UserProgress;
}

// ── Inline SVG icons (currentColor) ─────────────────────────────────────

const IconArrowLeft: React.FC<{ size?: number }> = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M19 12H5M12 19l-7-7 7-7" />
  </svg>
);

const IconArrowRight: React.FC<{ size?: number }> = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M5 12h14M12 5l7 7-7 7" />
  </svg>
);

const IconChevronRight: React.FC<{ size?: number }> = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="m9 18 6-6-6-6" />
  </svg>
);

const IconCheck: React.FC<{ size?: number }> = ({ size = 12 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M20 6 9 17l-5-5" />
  </svg>
);

// ── Category configuration ──────────────────────────────────────────────

interface CategoryConfig {
  id: CategoryType;
  worldKey: WorldId;
  number: string;
  name: string;
  worldName: string;
  blurb: string;
  description: string;
  /** Soft blob colour — used for the faint card tint and the 25%-alpha border. */
  blob: string;
  /** Saturated mid-tone — italic sub-headline, primary button, progress fill. */
  mid: string;
  /** Deeper shade for emphasis text. */
  deep: string;
  /** Tint focal — varies per world so cards don't read as the same gradient. */
  tintFocal: string;
}

const CATEGORIES: CategoryConfig[] = [
  {
    id: 'architecture-mindset',
    worldKey: 'mind',
    number: '01',
    name: 'Mind',
    worldName: 'The Architecture',
    blurb: 'Psychological foundations',
    description: 'Identity, beliefs, and emotional regulation — the foundation everything else stands on.',
    blob: '#B8C9E5',
    mid: '#5B7DB0',
    deep: '#1e3a5f',
    tintFocal: 'at 0% 0%',
  },
  {
    id: 'science-growth',
    worldKey: 'growth',
    number: '02',
    name: 'Growth',
    worldName: 'The Garden',
    blurb: 'How effort changes the brain',
    description: 'The neuroscience of mastery — neuroplasticity, deliberate practice, the cost and reward of struggle.',
    blob: '#F5C9A8',
    mid: '#C4873B',
    deep: '#7c4a14',
    tintFocal: 'at 100% 100%',
  },
  {
    id: 'learning-cheat-codes',
    worldKey: 'learn',
    number: '03',
    name: 'Learn',
    worldName: 'The Cheat Codes',
    blurb: 'Techniques that compound',
    description: 'Active recall, spaced repetition, interleaving — the practical strategies that separate high performers.',
    blob: '#B8DDC8',
    mid: '#2A7D6F',
    deep: '#115e4f',
    tintFocal: 'at 100% 0%',
  },
  {
    id: 'subject-specific-science',
    worldKey: 'decode',
    number: '04',
    name: 'Decode',
    worldName: 'The Decoder',
    blurb: 'Subject by subject',
    description: 'How each Leaving Cert paper actually works — marking schemes, examiner patterns, hidden curriculum.',
    blob: '#F0BFCE',
    mid: '#C76489',
    deep: '#8a2860',
    tintFocal: 'at 0% 100%',
  },
  {
    id: 'exam-zone',
    worldKey: 'exam',
    number: '05',
    name: 'Exam',
    worldName: 'The Arena',
    blurb: 'Performance under pressure',
    description: 'Pacing, nerves, recovery — the psychology and strategy of executing on the day.',
    blob: '#F5BFB0',
    mid: '#D4564E',
    deep: '#7f1d1d',
    tintFocal: 'at 50% 100%',
  },
];

const FALLBACK_HERO_ID: CategoryType = 'architecture-mindset';

// ── Stats / next-up helpers ─────────────────────────────────────────────

interface CategoryStats {
  completed: number;
  total: number;
  percent: number;
  hasAnyProgress: boolean;
}

function getStats(catId: CategoryType, allCourses: CourseData[], userProgress: UserProgress): CategoryStats {
  const courses = allCourses.filter(c => c.category === catId);
  const total = courses.length;
  let completed = 0;
  let hasAnyProgress = false;
  for (const c of courses) {
    const p = userProgress[c.id];
    if (!p) continue;
    if (p.unlockedSection > 0) hasAnyProgress = true;
    if (p.unlockedSection >= c.sectionsCount) completed += 1;
  }
  return {
    completed,
    total,
    percent: total > 0 ? (completed / total) * 100 : 0,
    hasAnyProgress,
  };
}

interface NextUp {
  course: CourseData;
  /** 1-indexed section number to start/continue at. */
  sectionNumber: number;
  /** Title of that specific section, falling back to "Section N". */
  sectionTitle: string;
  isContinue: boolean;
}

function getNextUp(catId: CategoryType, allCourses: CourseData[], userProgress: UserProgress): NextUp | null {
  const inCat = allCourses.filter(c => c.category === catId);
  if (inCat.length === 0) return null;

  const inProgress = inCat.find(c => {
    const p = userProgress[c.id];
    return p && p.unlockedSection > 0 && p.unlockedSection < c.sectionsCount;
  });
  if (inProgress) {
    const p = userProgress[inProgress.id];
    const sectionNumber = Math.min(p.unlockedSection + 1, inProgress.sectionsCount);
    const sectionTitle = MODULE_SECTIONS[inProgress.id]?.[sectionNumber - 1]?.title ?? `Section ${sectionNumber}`;
    return { course: inProgress, sectionNumber, sectionTitle, isContinue: true };
  }

  const firstIncomplete = inCat.find(c => {
    const p = userProgress[c.id];
    return !p || p.unlockedSection < c.sectionsCount;
  });
  const target = firstIncomplete ?? inCat[0];
  const sectionTitle = MODULE_SECTIONS[target.id]?.[0]?.title ?? 'Section 1';
  return { course: target, sectionNumber: 1, sectionTitle, isContinue: false };
}

function pickHeroId(allCourses: CourseData[], userProgress: UserProgress): CategoryType {
  let bestId: CategoryType = FALLBACK_HERO_ID;
  let bestScore = 0;
  for (const cat of CATEGORIES) {
    const courses = allCourses.filter(c => c.category === cat.id);
    let score = 0;
    for (const c of courses) {
      const p = userProgress[c.id];
      if (!p) continue;
      if (p.unlockedSection > 0 && p.unlockedSection < c.sectionsCount) {
        score += 100 + p.unlockedSection;
      } else if (p.unlockedSection >= c.sectionsCount) {
        score += 1;
      }
    }
    if (score > bestScore) {
      bestScore = score;
      bestId = cat.id;
    }
  }
  return bestId;
}

// ── Progress ring ───────────────────────────────────────────────────────

const ProgressRing: React.FC<{
  completed: number;
  total: number;
  mid: string;
  deep: string;
  size?: number;
}> = ({ completed, total, mid, deep, size = 92 }) => {
  const stroke = 6;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const pct = total > 0 ? completed / total : 0;
  const isComplete = total > 0 && completed === total;

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={deep}
          strokeOpacity={0.15}
          strokeWidth={stroke}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={mid}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          animate={{ strokeDashoffset: c - c * pct }}
          transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        {isComplete ? (
          <span className="inline-flex items-center justify-center w-7 h-7 rounded-full" style={{ background: mid, color: 'white' }}>
            <IconCheck size={16} />
          </span>
        ) : (
          <span className="font-serif text-[28px] font-semibold leading-none tabular-nums" style={{ color: deep }}>
            {completed}
          </span>
        )}
      </div>
    </div>
  );
};

// ── Card wrapper ────────────────────────────────────────────────────────
//
// Cream card with a faint world-colour tint at one corner (no hard
// gradient), 1px world-colour border at 25% opacity, soft warm shadow.
// Same recipe for hero and satellites — only sizing differs.

interface CardWrapperProps {
  config: CategoryConfig;
  isHero: boolean;
  children: React.ReactNode;
  onClick: () => void;
  ariaLabel: string;
}

const CardWrapper: React.FC<CardWrapperProps> = ({ config, isHero, children, onClick, ariaLabel }) => {
  const { blob, tintFocal, worldKey } = config;

  // Cream + soft world-colour tint at one corner (radial fade, no hard edge).
  // The tint is alpha-mixed (~22% blob colour) onto the cream baseline.
  // Mind opts out — its pale blue tint reads cold against the cream and the
  // user wanted the card flat for that world.
  const background =
    worldKey === 'mind'
      ? '#FDF8F0'
      : `radial-gradient(ellipse 60% 55% ${tintFocal}, ${blob}38 0%, transparent 70%), #FDF8F0`;
  const border = `1px solid ${blob}66`; // ~40% — visible but soft.
  const boxShadow = isHero
    ? '0 4px 18px rgba(0,0,0,0.05), 0 1px 4px rgba(0,0,0,0.04)'
    : '0 2px 8px rgba(0,0,0,0.04)';

  return (
    <motion.div
      layoutId={`category-card-${config.id}`}
      layout
      transition={{ type: 'spring', stiffness: 220, damping: 30 }}
      className={`relative ${isHero ? 'col-span-1 md:col-span-12' : 'col-span-1 md:col-span-3'}`}
    >
      <motion.div
        layout="position"
        onClick={onClick}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onClick(); } }}
        aria-label={ariaLabel}
        whileHover={isHero ? undefined : { y: -2 }}
        className={`relative h-full overflow-hidden cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-4 focus-visible:ring-offset-[#FDF8F0] ${isHero ? 'rounded-[28px] md:rounded-[32px]' : 'rounded-2xl md:rounded-[22px]'}`}
        style={{ background, border, boxShadow }}
      >
        <div className="relative">{children}</div>
      </motion.div>
    </motion.div>
  );
};

// ── Hero inner content ──────────────────────────────────────────────────

interface HeroInnerProps {
  config: CategoryConfig;
  stats: CategoryStats;
  nextUp: NextUp | null;
  onContinue: (moduleId: string) => void;
  onOpenCategory: () => void;
}

const HeroInner: React.FC<HeroInnerProps> = ({ config, stats, nextUp, onContinue, onOpenCategory }) => {
  const { mid, deep, worldKey } = config;
  const eyebrow = stats.hasAnyProgress ? 'Continue where you left off' : 'Start here';

  return (
    <div className="grid grid-cols-1 md:grid-cols-12 gap-6 md:gap-8 p-6 md:p-9 lg:p-10">
      {/* Left — identity */}
      <div className="md:col-span-7 flex flex-col">
        <div className="flex items-center gap-4 mb-3 md:mb-4">
          <WorldIconBlob world={worldKey} size={140} />
          <div className="flex items-center gap-3 min-w-0">
            <span className="font-mono text-[11px] font-bold tracking-[0.25em]" style={{ color: deep }}>
              {config.number}
            </span>
            <span className="h-px w-8 shrink-0" style={{ background: `${deep}40` }} />
            <span className="font-mono text-[10px] uppercase tracking-[0.22em]" style={{ color: `${deep}AA` }}>
              {config.worldName}
            </span>
          </div>
        </div>

        <h1
          className="font-serif font-medium tracking-[-0.03em] leading-[0.95] text-[#1A1A1A]"
          style={{ fontSize: 'clamp(52px, 7vw, 84px)' }}
        >
          {config.name}
        </h1>

        <p className="font-serif italic text-[18px] md:text-[20px] mt-3" style={{ color: mid }}>
          {config.blurb}
        </p>

        <p className="text-[14px] leading-relaxed mt-4 max-w-[44ch]" style={{ color: 'rgba(0,0,0,0.62)' }}>
          {config.description}
        </p>

        <div className="mt-6 md:mt-8 flex items-center gap-5">
          <ProgressRing
            completed={stats.completed}
            total={stats.total}
            mid={mid}
            deep={deep}
            size={72}
          />
          <div className="text-[13px] leading-snug" style={{ color: `${deep}CC` }}>
            <p className="font-semibold">
              {stats.completed === 0 ? 'Not started yet' : stats.completed === stats.total ? 'World complete' : `${Math.round(stats.percent)}% complete`}
            </p>
            <p className="mt-0.5" style={{ color: `${deep}99` }}>
              {stats.total} module{stats.total === 1 ? '' : 's'} in this world
            </p>
          </div>
        </div>
      </div>

      {/* Right — continue panel, separated by hairline rule in world's colour */}
      <div className="md:col-span-5 md:pl-8 md:border-l flex flex-col" style={{ borderColor: `${mid}4D` }}>
        {nextUp ? (
          <>
            <p className="font-mono text-[10px] font-bold uppercase tracking-[0.22em]" style={{ color: `${deep}AA` }}>
              {eyebrow}
            </p>
            <h3 className="font-serif text-[24px] md:text-[28px] font-medium leading-tight tracking-tight text-[#1A1A1A] mt-3">
              {nextUp.course.title}
            </h3>
            {nextUp.course.subtitle && (
              <p className="font-serif italic text-[14px] mt-1.5" style={{ color: `${mid}` }}>
                {nextUp.course.subtitle}
              </p>
            )}
            <p className="text-[13px] mt-4 leading-relaxed line-clamp-3" style={{ color: 'rgba(0,0,0,0.62)' }}>
              {nextUp.course.description}
            </p>

            {/* Section preview */}
            <div className="mt-5 md:mt-6 pl-3 border-l-2" style={{ borderColor: mid }}>
              <p className="font-mono text-[10px] font-bold uppercase tracking-[0.22em]" style={{ color: `${deep}AA` }}>
                {nextUp.isContinue
                  ? `Up next · Section ${nextUp.sectionNumber} of ${nextUp.course.sectionsCount}`
                  : `Begins with · Section 1 of ${nextUp.course.sectionsCount}`}
              </p>
              <p className="font-serif text-[16px] md:text-[17px] font-medium mt-1.5 leading-snug" style={{ color: '#1A1A1A' }}>
                {nextUp.sectionTitle}
              </p>
            </div>

            <div className="mt-5 md:mt-6 flex flex-col items-start gap-3">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  if (nextUp.isContinue) {
                    onContinue(nextUp.course.id);
                  } else {
                    onOpenCategory();
                  }
                }}
                className="group/cta inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full text-white text-[14px] font-semibold transition-all duration-300 hover:gap-3.5"
                style={{
                  background: mid,
                  boxShadow: `0 6px 16px ${mid}55`,
                }}
              >
                {nextUp.isContinue ? 'Continue' : 'Begin'}
                <IconArrowRight size={16} />
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); onOpenCategory(); }}
                className="inline-flex items-center gap-1 px-3 py-1.5 rounded-full text-[12px] font-semibold transition-colors duration-200 hover:gap-1.5"
                style={{ color: mid, border: `1px solid ${mid}55` }}
              >
                Browse all {stats.total}
                <IconChevronRight size={12} />
              </button>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center">
            <p className="text-[14px]" style={{ color: `${deep}AA` }}>
              No modules available in this world yet.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

// ── Satellite inner content ─────────────────────────────────────────────

interface SatelliteInnerProps {
  config: CategoryConfig;
  stats: CategoryStats;
}

const SatelliteInner: React.FC<SatelliteInnerProps> = ({ config, stats }) => {
  const { mid, deep, worldKey } = config;
  const isComplete = stats.total > 0 && stats.completed === stats.total;

  return (
    <div className="flex flex-col h-full p-5 md:p-6">
      <div className="flex justify-center -mb-4 -mt-10">
        <WorldIconBlob world={worldKey} size={180} />
      </div>

      <span className="font-mono text-[11px] font-medium tracking-[0.15em]" style={{ color: mid }}>
        {config.number}
      </span>

      <h3 className="font-serif text-[28px] md:text-[36px] font-medium tracking-tight leading-[1.0] mt-1" style={{ color: '#1A1A1A' }}>
        {config.name}
      </h3>

      <p className="text-[13px] mt-2 leading-snug" style={{ color: 'rgba(0,0,0,0.55)' }}>
        {config.blurb}
      </p>

      <div className="mt-6 pt-4 flex items-center justify-between gap-3">
        <span className="text-[12px] font-mono font-bold tabular-nums" style={{ color: deep }}>
          {stats.completed}<span style={{ opacity: 0.5 }}> / {stats.total}</span>
        </span>
        {isComplete ? (
          <span className="inline-flex items-center justify-center w-5 h-5 rounded-full" style={{ background: mid, color: 'white' }}>
            <IconCheck size={11} />
          </span>
        ) : (
          <span
            className="h-1 rounded-full overflow-hidden flex-1 max-w-[80px]"
            style={{ background: `${deep}1F` }}
          >
            <span
              className="block h-full rounded-full transition-all duration-700"
              style={{ width: `${stats.percent}%`, background: mid }}
            />
          </span>
        )}
      </div>
    </div>
  );
};

// ── Main view ───────────────────────────────────────────────────────────

export const ModulesView: React.FC<ModulesViewProps> = ({
  onBack,
  onSelectCategory,
  onSelectModule,
  allCourses,
  userProgress,
}) => {
  // Synchronous initialiser — no useEffect race. Hero is set on the first
  // render. If the auto-detected hero isn't resolvable for any reason,
  // useState's lazy init falls back to Mind via FALLBACK_HERO_ID.
  const [heroId, setHeroId] = useState<CategoryType>(() =>
    pickHeroId(allCourses, userProgress),
  );

  // Order: hero first, satellites in their original order. This keeps the
  // hero in the first row (col-span-12) and the four satellites in the
  // second row (4 × col-span-3 = 12). Promotion just shuffles this array.
  const ordered = [
    CATEGORIES.find(c => c.id === heroId)!,
    ...CATEGORIES.filter(c => c.id !== heroId),
  ];

  return (
    <div className="min-h-screen bg-[#FDF8F0] dark:bg-zinc-950">
      {/* Header — left side only. Right side intentionally empty so the
          App-level top-right cluster (TrainingPulse + bell + profile)
          owns that real estate without any leakage. */}
      <header
        className="fixed top-0 left-0 z-40 px-4 md:px-10 bg-[#FDF8F0]/85 dark:bg-zinc-950/90 backdrop-blur-md"
        style={{ paddingTop: 'calc(16px + var(--sat, 0px))', paddingBottom: '16px' }}
      >
        <div className="flex items-center gap-4">
          <button
            onClick={onBack}
            className="p-2.5 rounded-xl transition-colors hover:bg-white/60 dark:hover:bg-zinc-800/60 text-[#1A1A1A] dark:text-white"
            style={{ border: '1px solid rgba(0,0,0,0.06)' }}
            aria-label="Back to home"
          >
            <IconArrowLeft size={18} />
          </button>
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-[#A8A29E] dark:text-zinc-500">
              The Programme
            </p>
            <h1 className="font-serif text-base md:text-lg font-semibold text-[#1A1A1A] dark:text-white">
              Modules
            </h1>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="pt-24 md:pt-28 pb-16 px-4 md:px-10">
        <div className="max-w-7xl mx-auto">
          <LayoutGroup>
            <div className="grid grid-cols-1 md:grid-cols-12 gap-4 md:gap-5 auto-rows-min">
              {ordered.map(cat => {
                const isHero = cat.id === heroId;
                const stats = getStats(cat.id, allCourses, userProgress);
                return (
                  <CardWrapper
                    key={cat.id}
                    config={cat}
                    isHero={isHero}
                    onClick={() => isHero ? onSelectCategory(cat.id) : setHeroId(cat.id)}
                    ariaLabel={isHero ? `Open ${cat.name} world` : `Promote ${cat.name} to hero`}
                  >
                    {isHero ? (
                      <HeroInner
                        config={cat}
                        stats={stats}
                        nextUp={getNextUp(cat.id, allCourses, userProgress)}
                        onContinue={onSelectModule}
                        onOpenCategory={() => onSelectCategory(cat.id)}
                      />
                    ) : (
                      <SatelliteInner config={cat} stats={stats} />
                    )}
                  </CardWrapper>
                );
              })}
            </div>
          </LayoutGroup>
        </div>
      </main>
    </div>
  );
};

export default ModulesView;
