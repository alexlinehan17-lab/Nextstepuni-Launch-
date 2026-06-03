/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * FutureFinderResults — a self-contained, reusable copy of the original Future
 * Finder's results layer (cards / per-course detail / compare / saved picks /
 * "How this works" explainer). The JSX and logic are copied VERBATIM from
 * components/FutureFinder.tsx so the look is byte-identical; the original file
 * is left untouched. This component is currently consumed ONLY by the revamped
 * (RIASEC) tool — a temporary duplication that will be resolved when the
 * original Future Finder is retired.
 *
 * Two small additions over the original:
 *  1. An optional `reach` badge per result (DisplayResult.reach), rendered in
 *     the badge row of ResultCard and DetailPhase next to the Level pill.
 *  2. Configurable score-bar labels + an overridable "How this works" modal,
 *     so the revamped tool can relabel the three bars (Interest / Values /
 *     Points reach) and swap in its own RIASEC explainer.
 *
 * When `reach` is absent and the defaults are used, the rendered output is
 * identical to the original — keeping the legacy shape unaffected.
 */
import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import {
  ChevronLeft, SlidersHorizontal,
  MapPin, Briefcase, Heart, Star, RotateCcw,
  BookmarkPlus, Check, ArrowUpRight, TrendingUp, X, Clock, Eye,
  type LucideIcon,
} from 'lucide-react';
import { COLORS } from '../design/tokens';
import { INSTITUTIONS, REGIONS, type CAOCourse, getCoursePageUrl } from './futureFinderData';
import { type RecommendationResult } from './futureFinderAlgorithm';

// ─── Types ──────────────────────────────────────────────────────────────────

export type SortMode = 'match' | 'points' | 'institution';

/**
 * A result row for the shared UI. Extends the legacy RecommendationResult with
 * an OPTIONAL points-reach badge. When `reach` is present, an extra pill is
 * rendered next to the Level pill in the card + detail header; when absent the
 * shape is exactly the legacy one.
 */
export type DisplayResult = RecommendationResult & {
  reach?: { label: string; color: string; bg: string };
};

interface ScoreBreakdownLabels {
  interest: string;
  values: string;
  feasibility: string;
}

const DEFAULT_SCORE_LABELS: ScoreBreakdownLabels = {
  interest: 'Interest match',
  values: 'Values alignment',
  feasibility: 'Practical fit',
};

interface FutureFinderResultsProps {
  results: DisplayResult[];
  autoPoints: number;
  sortMode: SortMode;
  onSortChange: (m: SortMode) => void;
  regionFilter: string;
  onRegionFilterChange: (r: string) => void;
  savedPicks: string[];
  compareCourses: DisplayResult[];
  onToggleSave: (code: string) => void;
  onToggleCompare: (r: DisplayResult) => void;
  onRemoveCompare: (code: string) => void;
  onRetake: () => void;
  onOpenCareerPaths?: (careerStrings: string[]) => void;
  explainer?: React.ComponentType<{ onClose: () => void }>;
  scoreBreakdownLabels?: ScoreBreakdownLabels;
}

// ─── Helpers ────────────────────────────────────────────────────────────────

/** Get match label from percentage */
function getMatchLabel(pct: number): string {
  if (pct >= 75) return 'Strong match';
  if (pct >= 55) return 'Good fit';
  if (pct >= 40) return 'Worth exploring';
  return 'Stretch';
}

// ─── Component ──────────────────────────────────────────────────────────────

const FutureFinderResults: React.FC<FutureFinderResultsProps> = ({
  results, autoPoints, sortMode, onSortChange, regionFilter, onRegionFilterChange,
  savedPicks, compareCourses, onToggleSave, onToggleCompare, onRemoveCompare,
  onRetake, onOpenCareerPaths, explainer, scoreBreakdownLabels,
}) => {
  const [phase, setPhase] = useState<'results' | 'detail' | 'compare'>('results');
  const [selectedCourse, setSelectedCourse] = useState<DisplayResult | null>(null);
  const labels = scoreBreakdownLabels ?? DEFAULT_SCORE_LABELS;

  return (
    <AnimatePresence mode="wait">
      {phase === 'results' && (
        <ResultsPhase
          key="results"
          results={results}
          autoPoints={autoPoints}
          sortMode={sortMode}
          onSortChange={onSortChange}
          regionFilter={regionFilter}
          onRegionFilterChange={onRegionFilterChange}
          savedPicks={savedPicks}
          compareCourses={compareCourses}
          onToggleSave={onToggleSave}
          onToggleCompare={onToggleCompare}
          onSelectCourse={(r) => { setSelectedCourse(r); setPhase('detail'); }}
          onCompare={() => setPhase('compare')}
          onRetake={onRetake}
          onOpenCareerPaths={onOpenCareerPaths}
          explainer={explainer}
        />
      )}
      {phase === 'detail' && selectedCourse && (
        <DetailPhase
          key="detail"
          result={selectedCourse}
          autoPoints={autoPoints}
          isSaved={savedPicks.includes(selectedCourse.course.code)}
          isCompared={!!compareCourses.find(c => c.course.code === selectedCourse.course.code)}
          onToggleSave={() => onToggleSave(selectedCourse.course.code)}
          onToggleCompare={() => onToggleCompare(selectedCourse)}
          onBack={() => setPhase('results')}
          scoreBreakdownLabels={labels}
        />
      )}
      {phase === 'compare' && (
        <ComparePhase
          key="compare"
          courses={compareCourses}
          onBack={() => setPhase('results')}
          onRemove={onRemoveCompare}
        />
      )}
    </AnimatePresence>
  );
};

export default FutureFinderResults;

// ─── Phase Components ───────────────────────────────────────────────────────

/** Phase 3: Results */
function ResultsPhase({
  results, autoPoints, sortMode, onSortChange, regionFilter, onRegionFilterChange,
  savedPicks, compareCourses, onToggleSave, onToggleCompare, onSelectCourse, onCompare, onRetake, onOpenCareerPaths,
  explainer: Explainer,
}: {
  results: DisplayResult[];
  autoPoints: number;
  sortMode: SortMode;
  onSortChange: (m: SortMode) => void;
  regionFilter: string;
  onRegionFilterChange: (r: string) => void;
  savedPicks: string[];
  compareCourses: DisplayResult[];
  onToggleSave: (code: string) => void;
  onToggleCompare: (r: DisplayResult) => void;
  onSelectCourse: (r: DisplayResult) => void;
  onCompare: () => void;
  onRetake: () => void;
  onOpenCareerPaths?: (careerStrings: string[]) => void;
  explainer?: React.ComponentType<{ onClose: () => void }>;
}) {
  const [explainerOpen, setExplainerOpen] = useState(false);
  const ExplainerModal = Explainer ?? ScoringExplainerModal;
  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }}>
      {/* Header */}
      <div className="flex items-start justify-between mb-6 gap-3">
        <div className="min-w-0">
          <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Your Top Matches</h2>
          <p className="text-sm text-zinc-400 dark:text-zinc-500 mt-1">Courses ranked by how well they fit you</p>
          {autoPoints > 0 && (
            <p className="text-xs font-medium mt-1" style={{ color: COLORS.accent }}>
              Based on your current grades, you're at {autoPoints} points
            </p>
          )}
        </div>
        <div className="flex items-center gap-3 shrink-0 pt-1">
          <button
            onClick={() => setExplainerOpen(true)}
            className="flex items-center gap-1.5 text-xs font-semibold text-zinc-400 dark:text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 transition-colors"
            aria-label="How are these results calculated?"
          >
            <Eye size={14} /> How this works
          </button>
          <button onClick={onRetake} className="flex items-center gap-1.5 text-xs font-semibold text-zinc-400 dark:text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 transition-colors">
            <RotateCcw size={14} /> Retake
          </button>
        </div>
      </div>

      {onOpenCareerPaths && (
        <button
          onClick={() => onOpenCareerPaths(results.flatMap((r) => r.course.careerPaths))}
          className="w-full mb-6 flex items-center gap-3 rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 p-4 text-left transition-transform active:translate-y-0.5 hover:shadow-md"
        >
          <span className="w-11 h-11 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: '#0E7C6B' }}>
            <Briefcase size={20} className="text-white" />
          </span>
          <span className="flex-1 min-w-0">
            <span className="block text-sm font-semibold text-zinc-900 dark:text-white">Explore these as careers</span>
            <span className="block text-xs text-zinc-500 dark:text-zinc-400">What they pay, the day-to-day, and the routes in — for the careers your results point to.</span>
          </span>
          <ArrowUpRight size={18} className="text-zinc-400 shrink-0" />
        </button>
      )}

      <AnimatePresence>
        {explainerOpen && <ExplainerModal onClose={() => setExplainerOpen(false)} />}
      </AnimatePresence>

      {/* Sort & Filter controls */}
      <div className="flex flex-wrap gap-2 mb-4">
        <div className="flex items-center gap-1 bg-zinc-100 dark:bg-zinc-800 rounded-lg p-0.5">
          {([['match', 'Match %'], ['points', 'Points'], ['institution', 'College']] as const).map(([key, label]) => (
            <button
              key={key}
              onClick={() => onSortChange(key)}
              className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors ${
                sortMode === key ? 'bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white shadow-sm' : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
        <select
          value={regionFilter}
          onChange={e => onRegionFilterChange(e.target.value)}
          className="px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-xs font-semibold text-zinc-700 dark:text-zinc-300 border-none focus:outline-none focus:ring-2 focus:ring-zinc-400/50"
        >
          <option value="">All regions</option>
          {Object.entries(REGIONS).map(([key, label]) => (
            <option key={key} value={key}>{label}</option>
          ))}
        </select>
      </div>

      {/* Compare bar */}
      {compareCourses.length > 0 && (
        <div className="mb-4 p-3 rounded-xl border flex items-center justify-between bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(242,107,31,0.2)' }}>
          <span className="text-xs font-semibold" style={{ color: COLORS.accent }}>
            {compareCourses.length} course{compareCourses.length > 1 ? 's' : ''} selected for comparison
          </span>
          <button
            onClick={onCompare}
            disabled={compareCourses.length < 2}
            className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-colors ${
              compareCourses.length >= 2 ? 'text-white' : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400 cursor-not-allowed'
            }`}
            style={compareCourses.length >= 2 ? { backgroundColor: COLORS.accent } : undefined}
          >
            Compare
          </button>
        </div>
      )}

      {/* Result cards */}
      <div className="space-y-3">
        {results.map((r, i) => (
          <ResultCard
            key={r.course.code}
            result={r}
            rank={i + 1}
            isSaved={savedPicks.includes(r.course.code)}
            isCompared={!!compareCourses.find(c => c.course.code === r.course.code)}
            onToggleSave={() => onToggleSave(r.course.code)}
            onToggleCompare={() => onToggleCompare(r)}
            onClick={() => onSelectCourse(r)}
          />
        ))}
      </div>

      {results.length === 0 && (
        <div className="text-center py-16">
          <p className="text-zinc-400 dark:text-zinc-500">No courses match your filters. Try broadening your region or study duration preferences.</p>
        </div>
      )}
    </MotionDiv>
  );
}

/** Result Card */
function ResultCard({
  result, rank, isSaved, isCompared, onToggleSave, onToggleCompare, onClick,
}: {
  result: DisplayResult;
  rank: number;
  isSaved: boolean;
  isCompared: boolean;
  onToggleSave: () => void;
  onToggleCompare: () => void;
  onClick: () => void;
}) {
  const matchPct = Math.round(result.score * 100);
  const matchLabel = getMatchLabel(matchPct);
  const c = result.course;

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: rank * 0.04, duration: 0.3 }}
      className="group rounded-xl border hover:shadow-md cursor-pointer overflow-hidden transition-all bg-[#FAF7F4] dark:bg-zinc-900"
      style={{ borderColor: 'rgba(0,0,0,0.07)' }}
      onClick={onClick}
    >
      <div className="h-[2px] opacity-0 group-hover:opacity-100 transition-opacity" style={{ backgroundColor: COLORS.accent }} />
      <div className="p-4 md:p-5">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span className="text-xs font-bold" style={{ color: COLORS.accent }}>#{rank}</span>
              <span className="text-xs font-mono text-zinc-400 dark:text-zinc-500">{c.code}</span>
              <span className="px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-xs font-semibold text-zinc-500 dark:text-zinc-400">Level {c.level}</span>
              {result.reach && (
                <span className="px-2 py-0.5 rounded-full text-xs font-semibold" style={{ backgroundColor: result.reach.bg, color: result.reach.color }}>{result.reach.label}</span>
              )}
              {c.pathwayType === 'plc' && (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold" style={{ backgroundColor: '#EDF2EE', color: '#4A6B4F' }}>PLC</span>
              )}
              {c.pathwayType === 'apprenticeship' && (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold" style={{ backgroundColor: '#FDF3E7', color: '#8B5E2A' }}>Apprenticeship</span>
              )}
              {result.subjectAlignment === 'strong' && (
                <span className="px-2 py-0.5 rounded-full text-xs font-semibold" style={{ backgroundColor: '#E8F0E8', color: '#4A6B4F' }}>Subjects align</span>
              )}
              {result.subjectAlignment === 'none' && c.subjectBonus.length > 0 && (
                <span className="px-2 py-0.5 rounded-full text-xs font-semibold" style={{ backgroundColor: '#FEF3C7', color: '#92400E' }}>Check requirements</span>
              )}
            </div>
            <h4 className="font-serif font-semibold text-base text-zinc-900 dark:text-white truncate">{c.title}</h4>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{INSTITUTIONS[c.institution] || c.institution} {'—'} {REGIONS[c.region] || c.region}</p>
          </div>
          <div className="flex flex-col items-center shrink-0">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-sm ${
              matchPct < 50 ? 'bg-zinc-100 text-zinc-500' : ''
            }`}
              style={matchPct >= 70 ? { backgroundColor: '#EDF2EE', color: '#4A6B4F' } : matchPct >= 50 ? { backgroundColor: '#FDF3E7', color: '#8B5E2A' } : undefined}
            >
              {matchPct}%
            </div>
            <span className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1">{matchLabel}</span>
          </div>
        </div>

        {/* Points */}
        <div className="flex items-center gap-3 mb-3">
          <span className="text-xs font-semibold text-zinc-500 dark:text-zinc-400">
            {c.typicalPoints === 0 ? (c.pathwayType === 'apprenticeship' ? 'Employer-based' : 'Open entry') : `~${c.typicalPoints} points`}
          </span>
          <span className="text-xs text-zinc-400 dark:text-zinc-500">{'•'}</span>
          <span className="text-xs text-zinc-500 dark:text-zinc-400">{c.duration} years</span>
          {c.salaryBand === 'high' && (
            <>
              <span className="text-xs text-zinc-400 dark:text-zinc-500">{'•'}</span>
              <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400">High salary</span>
            </>
          )}
        </div>

        {/* Reason pills — show up to 5 */}
        <div className="flex flex-wrap gap-1.5 mb-3">
          {result.reasons.slice(0, 5).map((reason, i) => (
            <span key={i} className="px-2.5 py-1 rounded-full text-xs font-medium" style={{ backgroundColor: '#EDF2EE', color: '#4A6B4F' }}>
              {reason}
            </span>
          ))}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2" onClick={e => e.stopPropagation()}>
          <button
            onClick={onToggleSave}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-colors border ${
              isSaved ? 'bg-transparent border-zinc-300 dark:border-zinc-600' : 'bg-transparent border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800'
            }`}
            style={isSaved ? { color: COLORS.accent } : undefined}
          >
            {isSaved ? <Check size={12} /> : <BookmarkPlus size={12} />}
            {isSaved ? 'Saved' : 'Save'}
          </button>
          <button
            onClick={onToggleCompare}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-colors border ${
              isCompared ? 'bg-transparent border-zinc-300 dark:border-zinc-600' : 'bg-transparent border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800'
            }`}
            style={isCompared ? { color: COLORS.accent } : undefined}
          >
            <SlidersHorizontal size={12} />
            {isCompared ? 'Comparing' : 'Compare'}
          </button>
          <a
            href={getCoursePageUrl(c)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-transparent border border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
          >
            <ArrowUpRight size={12} />
            College page
          </a>
        </div>
      </div>
    </MotionDiv>
  );
}

/** Phase 4: Detail View */
function DetailPhase({
  result, autoPoints, isSaved, isCompared, onToggleSave, onToggleCompare, onBack, scoreBreakdownLabels,
}: {
  result: DisplayResult;
  autoPoints: number;
  isSaved: boolean;
  isCompared: boolean;
  onToggleSave: () => void;
  onToggleCompare: () => void;
  onBack: () => void;
  scoreBreakdownLabels: ScoreBreakdownLabels;
}) {
  const c = result.course;
  const matchPct = Math.round(result.score * 100);
  const matchLabel = getMatchLabel(matchPct);
  const pointsGap = c.typicalPoints - autoPoints;

  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }}>
      <button onClick={onBack} className="flex items-center gap-1.5 text-sm font-semibold text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300 mb-4 transition-colors">
        <ChevronLeft size={16} /> Back to results
      </button>

      <div className="bg-[#FAF7F4] dark:bg-zinc-900 overflow-hidden" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: '12px' }}>
        {/* Header */}
        <div className="p-6" style={{ backgroundColor: COLORS.accent }}>
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-xs font-bold">{c.code}</span>
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-xs font-bold">Level {c.level}</span>
            {result.reach && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold" style={{ backgroundColor: result.reach.bg, color: result.reach.color }}>{result.reach.label}</span>
            )}
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-xs font-bold">{matchPct}% {matchLabel}</span>
            {c.pathwayType === 'plc' && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold" style={{ backgroundColor: 'rgba(255,255,255,0.25)', color: 'white' }}>PLC</span>
            )}
            {c.pathwayType === 'apprenticeship' && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold" style={{ backgroundColor: 'rgba(255,255,255,0.25)', color: 'white' }}>Apprenticeship</span>
            )}
            {result.subjectAlignment === 'strong' && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold" style={{ backgroundColor: 'rgba(255,255,255,0.25)', color: 'white' }}>Subjects align</span>
            )}
            {result.subjectAlignment === 'none' && c.subjectBonus.length > 0 && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold" style={{ backgroundColor: 'rgba(254,243,199,0.3)', color: '#FEF3C7' }}>Check requirements</span>
            )}
          </div>
          <h3 className="font-serif text-2xl font-bold text-white mb-1">{c.title}</h3>
          <p className="text-white/80 text-sm">{INSTITUTIONS[c.institution] || c.institution}</p>
        </div>

        <div className="p-6 space-y-6">
          {/* Description */}
          <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">{c.description}</p>

          {/* Key info grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <InfoTile icon={TrendingUp} label="Typical Points" value={c.typicalPoints === 0 ? (c.pathwayType === 'apprenticeship' ? 'Employer-based' : 'Open entry') : `~${c.typicalPoints}`} />
            <InfoTile icon={Clock} label="Duration" value={`${c.duration} years`} />
            <InfoTile icon={MapPin} label="Region" value={REGIONS[c.region] || c.region} />
            <InfoTile icon={Briefcase} label="Salary Band" value={c.salaryBand.charAt(0).toUpperCase() + c.salaryBand.slice(1)} />
          </div>

          {/* Your Points section */}
          {c.typicalPoints === 0 ? (
            <div className="p-4 rounded-xl border bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(242,107,31,0.15)' }}>
              <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">Entry Requirements</h4>
              <p className="text-sm text-zinc-700 dark:text-zinc-300">
                {c.pathwayType === 'apprenticeship'
                  ? 'Apply directly to an employer. No CAO points required. You will earn a wage from day one while training on the job.'
                  : 'No CAO points required. This is an open-entry QQI Level 5 course. Apply directly through the college.'}
              </p>
            </div>
          ) : autoPoints > 0 ? (
            <div className="p-4 rounded-xl border bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(242,107,31,0.15)' }}>
              <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">Your Points</h4>
              <div className="grid grid-cols-3 gap-3 text-center">
                <div>
                  <p className="text-2xl font-bold" style={{ color: COLORS.accent }}>{autoPoints}</p>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Your current points</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-zinc-600 dark:text-zinc-400">{c.typicalPoints}</p>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Typical entry</p>
                </div>
                <div>
                  {pointsGap > 0 ? (
                    <>
                      <p className="text-2xl font-bold" style={{ color: '#D97706' }}>{pointsGap}</p>
                      <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Points gap</p>
                    </>
                  ) : (
                    <>
                      <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{Math.abs(pointsGap)}</p>
                      <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Points ahead</p>
                    </>
                  )}
                </div>
              </div>
            </div>
          ) : null}

          {/* Employability */}
          <div>
            <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Employability</h4>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map(n => (
                <div key={n} className={`h-2 flex-1 rounded-full ${n <= c.employability ? 'bg-emerald-500' : 'bg-zinc-200 dark:bg-zinc-700'}`} />
              ))}
            </div>
          </div>

          {/* Career paths */}
          <div>
            <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Career Paths</h4>
            <div className="flex flex-wrap gap-2">
              {c.careerPaths.map(cp => (
                <span key={cp} className="px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-sm text-zinc-700 dark:text-zinc-300 font-medium">{cp}</span>
              ))}
            </div>
          </div>

          {/* Subject bonus */}
          <div>
            <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Subjects That Help</h4>
            <div className="flex flex-wrap gap-2">
              {c.subjectBonus.map(sub => (
                <span key={sub} className="px-3 py-1.5 rounded-lg text-sm font-medium bg-[#FAF7F4] dark:bg-zinc-900" style={{ color: COLORS.accent }}>{sub}</span>
              ))}
            </div>
          </div>

          {/* Why this suits you — show up to 5 reasons */}
          <div className="p-4 rounded-xl border bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(242,107,31,0.15)' }}>
            <h4 className="text-sm font-bold mb-3 flex items-center gap-2" style={{ color: COLORS.accent }}>
              <Heart size={16} style={{ color: COLORS.accent }} /> Why This Suits You
            </h4>
            <ul className="space-y-2">
              {result.reasons.slice(0, 5).map((reason, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-zinc-700 dark:text-zinc-300">
                  <Star size={14} className="mt-0.5 shrink-0" style={{ color: COLORS.accent }} />
                  {reason}
                </li>
              ))}
            </ul>
          </div>

          {/* How we scored this */}
          <div className="p-4 rounded-xl border border-zinc-200 dark:border-zinc-800">
            <h4 className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-4">How We Scored This</h4>
            <div className="space-y-3">
              <ScoreBar label={scoreBreakdownLabels.interest} score={result.scoreBreakdown.interestScore} />
              <ScoreBar label={scoreBreakdownLabels.values} score={result.scoreBreakdown.valuesScore} />
              <ScoreBar label={scoreBreakdownLabels.feasibility} score={result.scoreBreakdown.feasibilityScore} />
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-wrap gap-2 pt-2">
            <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onToggleSave}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-colors border ${
                isSaved ? 'text-white' : 'bg-transparent border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800'
              }`}
              style={isSaved ? { backgroundColor: COLORS.accent, borderColor: COLORS.accent } : undefined}>
              {isSaved ? <Check size={16} /> : <BookmarkPlus size={16} />}
              {isSaved ? 'Saved to Picks' : 'Save to Picks'}
            </MotionButton>
            <MotionButton whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={onToggleCompare}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-colors border ${
                isCompared ? 'text-white' : 'bg-transparent border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800'
              }`}
              style={isCompared ? { backgroundColor: COLORS.accent, borderColor: COLORS.accent } : undefined}>
              <SlidersHorizontal size={16} />
              {isCompared ? 'Added to Compare' : 'Add to Compare'}
            </MotionButton>
            <a
              href={getCoursePageUrl(c)}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-transparent border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
            >
              <ArrowUpRight size={16} />
              Visit {c.institution} course page
            </a>
          </div>
        </div>
      </div>
    </MotionDiv>
  );
}

/** Score progress bar for the "How we scored this" section */
function ScoreBar({ label, score }: { label: string; score: number }) {
  const pct = Math.round(score * 100);
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs font-medium text-zinc-600 dark:text-zinc-400 w-32 shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${pct}%`, backgroundColor: COLORS.accent }}
        />
      </div>
      <span className="text-xs font-bold text-zinc-600 dark:text-zinc-400 w-10 text-right">{pct}%</span>
    </div>
  );
}

/** Info Tile (for detail view) */
function InfoTile({ icon: Icon, label, value }: { icon: LucideIcon; label: string; value: string }) {
  return (
    <div className="p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 text-center">
      <Icon size={16} className="mx-auto text-zinc-400 dark:text-zinc-500 mb-1" />
      <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-0.5">{label}</p>
      <p className="text-sm font-bold text-zinc-900 dark:text-white">{value}</p>
    </div>
  );
}

/** Phase 5: Compare View */
function ComparePhase({
  courses, onBack, onRemove,
}: {
  courses: DisplayResult[];
  onBack: () => void;
  onRemove: (code: string) => void;
}) {
  const fields: { label: string; render: (c: CAOCourse, r: DisplayResult) => string }[] = [
    { label: 'Institution', render: c => INSTITUTIONS[c.institution] || c.institution },
    { label: 'Level', render: c => `Level ${c.level}` },
    { label: 'Typical Points', render: c => c.typicalPoints === 0 ? (c.pathwayType === 'apprenticeship' ? 'Employer-based' : 'Open entry') : `~${c.typicalPoints}` },
    { label: 'Duration', render: c => `${c.duration} years` },
    { label: 'Region', render: c => REGIONS[c.region] || c.region },
    { label: 'Salary Band', render: c => c.salaryBand.charAt(0).toUpperCase() + c.salaryBand.slice(1) },
    { label: 'Employability', render: c => `${'★'.repeat(c.employability)}${'☆'.repeat(5 - c.employability)}` },
    { label: 'Career Paths', render: c => c.careerPaths.join(', ') },
    { label: 'Match', render: (_c, r) => `${Math.round(r.score * 100)}%` },
  ];

  return (
    <MotionDiv initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.35 }}>
      <button onClick={onBack} className="flex items-center gap-1.5 text-sm font-semibold text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300 mb-4 transition-colors">
        <ChevronLeft size={16} /> Back to results
      </button>

      <div className="flex items-start justify-between gap-4 mb-6">
        <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Compare Courses</h2>
        <img
          src="/assets/future-finder-compare.png"
          alt=""
          aria-hidden
          className="shrink-0"
          style={{ width: 'clamp(56px, 7vw, 88px)', height: 'auto', objectFit: 'contain' }}
        />
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr>
              <th className="text-left p-3 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider" />
              {courses.map(r => (
                <th key={r.course.code} className="p-3 text-left min-w-[180px]">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-serif font-semibold text-zinc-900 dark:text-white text-sm">{r.course.title}</p>
                      <p className="text-xs text-zinc-400 dark:text-zinc-500 font-normal">{r.course.code}</p>
                    </div>
                    <button onClick={() => onRemove(r.course.code)} className="p-1 rounded-md hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                      <X size={14} className="text-zinc-400" />
                    </button>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {fields.map(field => (
              <tr key={field.label} className="border-t border-zinc-100 dark:border-zinc-800">
                <td className="p-3 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider whitespace-nowrap">{field.label}</td>
                {courses.map(r => (
                  <td key={r.course.code} className="p-3 text-zinc-700 dark:text-zinc-300">
                    {field.render(r.course, r)}
                  </td>
                ))}
              </tr>
            ))}
            <tr className="border-t border-zinc-100 dark:border-zinc-800">
              <td className="p-3 text-xs font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Why It Fits</td>
              {courses.map(r => (
                <td key={r.course.code} className="p-3">
                  <ul className="space-y-1">
                    {r.reasons.slice(0, 5).map((reason, i) => (
                      <li key={i} className="flex items-start gap-1 text-xs text-zinc-700 dark:text-zinc-300">
                        <Star size={10} className="mt-0.5 shrink-0" style={{ color: COLORS.accent }} /> {reason}
                      </li>
                    ))}
                  </ul>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>

      {courses.length < 2 && (
        <p className="text-center text-sm text-zinc-400 dark:text-zinc-500 mt-8">
          Add at least 2 courses to compare. Go back and use the Compare button on result cards.
        </p>
      )}
    </MotionDiv>
  );
}

// ── Scoring explainer modal ────────────────────────────────────────────────
// Surfaces what's actually happening behind the match %, how the salary band
// is derived, and how the employability number is sourced. The intent is to
// be honest with the student about what's a real algorithm vs. what's a
// hand-curated reference value — so they can use the result as a guide
// without treating it as a prediction.
function ScoringExplainerModal({ onClose }: { onClose: () => void }) {
  // Portalled to document.body so the modal escapes ResultsPhase's Framer
  // `<MotionDiv>` transform context. Without the portal, `position: fixed`
  // is positioned relative to the transformed ancestor instead of the
  // viewport, and the modal spills off the top of the screen.
  return createPortal(
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[200] flex items-center justify-center bg-black/55 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <MotionDiv
        initial={{ opacity: 0, scale: 0.96, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.96, y: 12 }}
        transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] as number[] }}
        className="bg-[#FAFBF6] dark:bg-zinc-900 rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[6px_6px_0_0_#1A1A1A] dark:shadow-[6px_6px_0_0_#3f3f46] max-w-xl w-full max-h-[90vh] flex flex-col overflow-hidden"
        onClick={(e: React.MouseEvent) => e.stopPropagation()}
      >
        {/* Header (fixed) */}
        <div className="flex items-start justify-between p-6 pb-4 shrink-0">
          <div className="flex items-start gap-3 min-w-0">
            <div className="w-11 h-11 rounded-xl flex items-center justify-center bg-[rgba(242,107,31,0.12)] shrink-0">
              <Eye size={20} className="text-[#F26B1F]" />
            </div>
            <div className="min-w-0">
              <h2 className="font-serif text-xl font-bold text-[#1A1A1A] dark:text-white">How your results are calculated</h2>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">A quick look behind the match percentage</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-black/5 dark:hover:bg-white/10 transition-colors shrink-0"
            aria-label="Close"
          >
            <X size={18} className="text-zinc-500" />
          </button>
        </div>

        {/* Body (scrolls when content exceeds the viewport-capped modal) */}
        <div className="px-6 pb-6 space-y-5 overflow-y-auto flex-1 min-h-0">
          {/* Matching */}
          <section>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">The match score</p>
            <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed mb-3">
              Every course gets a 0–100% score made of three parts:
            </p>
            <div className="space-y-2.5">
              <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
                <div className="flex items-baseline justify-between mb-1">
                  <p className="text-sm font-bold text-[#1A1A1A] dark:text-white">Interest fit</p>
                  <span className="text-xs font-bold" style={{ color: COLORS.accent }}>45%</span>
                </div>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  How well your interest tags and the scenarios you picked overlap with the course's own tags. Full credit at 3+ matching interests, with a bonus for matching scenarios.
                </p>
              </div>
              <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
                <div className="flex items-baseline justify-between mb-1">
                  <p className="text-sm font-bold text-[#1A1A1A] dark:text-white">Values alignment</p>
                  <span className="text-xs font-bold" style={{ color: COLORS.accent }}>30%</span>
                </div>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  Your salary, job-security, and helping-others sliders weighted against the course's salary band and employability rating. Plus your work-style picks (analytical / hands-on / etc.) and team preference.
                </p>
              </div>
              <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
                <div className="flex items-baseline justify-between mb-1">
                  <p className="text-sm font-bold text-[#1A1A1A] dark:text-white">Feasibility</p>
                  <span className="text-xs font-bold" style={{ color: COLORS.accent }}>25%</span>
                </div>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  Does your preferred study length match the course's NFQ level, and are your current points realistic for the course's typical entry threshold. Geographic preferences nudge the final score up or down.
                </p>
              </div>
            </div>
          </section>

          {/* Salary */}
          <section>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Salary band</p>
            <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
              <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed mb-2">
                Every course carries a <span className="font-bold">Low / Mid / High</span> salary band. These are <span className="font-bold">informed reference values</span>, not predictions for you personally — they reflect roughly where typical mid-career graduate earnings sit in Ireland for that pathway, based on the general patterns visible across publicly-available labour-market and graduate-outcome reporting.
              </p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed italic">
                Two students in the same course will end up in very different bands depending on specialisation, region, and employer. The band is a useful first signal — not a number to bank on.
              </p>
            </div>
          </section>

          {/* Employability */}
          <section>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Employability rating</p>
            <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
              <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed mb-2">
                A <span className="font-bold">1 to 5 rating</span> per course, also informed-but-curated. Higher means the path from this course to substantive employment or further study tends to be more predictable in the Irish market.
              </p>
              <ul className="text-xs text-zinc-600 dark:text-zinc-400 space-y-1 leading-relaxed">
                <li><span className="font-bold text-[#1A1A1A] dark:text-white">5</span> — Very strong outcomes (medicine, nursing, education, accounting)</li>
                <li><span className="font-bold text-[#1A1A1A] dark:text-white">4</span> — Strong (engineering, computer science, most business)</li>
                <li><span className="font-bold text-[#1A1A1A] dark:text-white">3</span> — Solid (general degrees, sciences, social sciences)</li>
                <li><span className="font-bold text-[#1A1A1A] dark:text-white">1–2</span> — Niche or competitive fields where placement is less predictable</li>
              </ul>
            </div>
          </section>

          {/* Disclaimer */}
          <section className="rounded-xl p-3" style={{ backgroundColor: 'rgba(242,107,31,0.10)' }}>
            <p className="text-xs text-[#8C3A0E] dark:text-[#FDEEDF] leading-relaxed">
              <span className="font-bold">Treat the result as a guide, not a verdict.</span> The algorithm reflects fit between you and a course, not how your career will go. Use it to surface options you hadn't thought about — then go talk to people doing the job.
            </p>
          </section>
        </div>

        {/* Footer CTA (fixed below the scrolling body) */}
        <div className="px-6 pb-6 pt-2 shrink-0 border-t border-black/[0.04] dark:border-white/[0.06]">
          <button
            onClick={onClose}
            className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-sans font-bold text-sm shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-[0px_0px_0_0_#1A1A1A] transition-all duration-150"
          >
            Got it
          </button>
        </div>
      </MotionDiv>
    </MotionDiv>,
    document.body
  );
}
