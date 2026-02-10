/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Settings, Star, RotateCcw, ChevronDown, ChevronUp, TrendingUp, Info, ArrowRight,
} from 'lucide-react';
import {
  type StudentSubjectProfile, type Grade, type Level,
  LC_SUBJECTS, getPointsForGrade, getGradesForLevel,
} from './subjectData';

const MotionDiv = motion.div as any;

// ─── Types ───────────────────────────────────────────────────────────────────

interface CAOPointsSimulatorProps {
  profile: StudentSubjectProfile;
  onOpenSettings: () => void;
}

interface SimSubject {
  subjectName: string;
  level: Level;
  currentGrade: Grade;
  targetGrade: Grade;
  whatIfGrade: Grade;
  isMaths: boolean;
}

interface BestSixResult {
  total: number;
  bestSix: { subjectName: string; points: number; grade: Grade }[];
  outside: { subjectName: string; points: number; grade: Grade }[];
}

// ─── Subject Color Map (literal Tailwind strings for CDN constraint) ────────

const SUBJECT_COLORS: Record<string, { dot: string; bg: string; border: string; text: string }> = {
  'English': { dot: 'bg-blue-500', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300' },
  'Irish': { dot: 'bg-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Mathematics': { dot: 'bg-indigo-500', bg: 'bg-indigo-50 dark:bg-indigo-900/20', border: 'border-indigo-200 dark:border-indigo-800/40', text: 'text-indigo-700 dark:text-indigo-300' },
  'French': { dot: 'bg-sky-500', bg: 'bg-sky-50 dark:bg-sky-900/20', border: 'border-sky-200 dark:border-sky-800/40', text: 'text-sky-700 dark:text-sky-300' },
  'German': { dot: 'bg-yellow-500', bg: 'bg-yellow-50 dark:bg-yellow-900/20', border: 'border-yellow-200 dark:border-yellow-800/40', text: 'text-yellow-700 dark:text-yellow-300' },
  'Spanish': { dot: 'bg-orange-500', bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300' },
  'Italian': { dot: 'bg-red-500', bg: 'bg-red-50 dark:bg-red-900/20', border: 'border-red-200 dark:border-red-800/40', text: 'text-red-700 dark:text-red-300' },
  'Japanese': { dot: 'bg-pink-500', bg: 'bg-pink-50 dark:bg-pink-900/20', border: 'border-pink-200 dark:border-pink-800/40', text: 'text-pink-700 dark:text-pink-300' },
  'Physics': { dot: 'bg-cyan-500', bg: 'bg-cyan-50 dark:bg-cyan-900/20', border: 'border-cyan-200 dark:border-cyan-800/40', text: 'text-cyan-700 dark:text-cyan-300' },
  'Chemistry': { dot: 'bg-teal-500', bg: 'bg-teal-50 dark:bg-teal-900/20', border: 'border-teal-200 dark:border-teal-800/40', text: 'text-teal-700 dark:text-teal-300' },
  'Biology': { dot: 'bg-lime-500', bg: 'bg-lime-50 dark:bg-lime-900/20', border: 'border-lime-200 dark:border-lime-800/40', text: 'text-lime-700 dark:text-lime-300' },
  'Applied Maths': { dot: 'bg-violet-500', bg: 'bg-violet-50 dark:bg-violet-900/20', border: 'border-violet-200 dark:border-violet-800/40', text: 'text-violet-700 dark:text-violet-300' },
  'Computer Science': { dot: 'bg-fuchsia-500', bg: 'bg-fuchsia-50 dark:bg-fuchsia-900/20', border: 'border-fuchsia-200 dark:border-fuchsia-800/40', text: 'text-fuchsia-700 dark:text-fuchsia-300' },
  'Ag Science': { dot: 'bg-green-500', bg: 'bg-green-50 dark:bg-green-900/20', border: 'border-green-200 dark:border-green-800/40', text: 'text-green-700 dark:text-green-300' },
  'Accounting': { dot: 'bg-amber-500', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300' },
  'Business': { dot: 'bg-amber-600', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300' },
  'Economics': { dot: 'bg-yellow-600', bg: 'bg-yellow-50 dark:bg-yellow-900/20', border: 'border-yellow-200 dark:border-yellow-800/40', text: 'text-yellow-700 dark:text-yellow-300' },
  'History': { dot: 'bg-purple-500', bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800/40', text: 'text-purple-700 dark:text-purple-300' },
  'Geography': { dot: 'bg-emerald-600', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Politics & Society': { dot: 'bg-rose-500', bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300' },
  'Religious Education': { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' },
  'Classical Studies': { dot: 'bg-stone-500', bg: 'bg-stone-50 dark:bg-stone-800/40', border: 'border-stone-200 dark:border-stone-700/40', text: 'text-stone-700 dark:text-stone-300' },
  'Home Economics': { dot: 'bg-orange-400', bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300' },
  'Construction Studies': { dot: 'bg-slate-500', bg: 'bg-slate-50 dark:bg-slate-800/40', border: 'border-slate-200 dark:border-slate-700/40', text: 'text-slate-700 dark:text-slate-300' },
  'Engineering': { dot: 'bg-gray-500', bg: 'bg-gray-50 dark:bg-gray-800/40', border: 'border-gray-200 dark:border-gray-700/40', text: 'text-gray-700 dark:text-gray-300' },
  'DCG': { dot: 'bg-neutral-500', bg: 'bg-neutral-50 dark:bg-neutral-800/40', border: 'border-neutral-200 dark:border-neutral-700/40', text: 'text-neutral-700 dark:text-neutral-300' },
  'Technology': { dot: 'bg-blue-600', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300' },
  'Art': { dot: 'bg-rose-400', bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300' },
  'Music': { dot: 'bg-pink-400', bg: 'bg-pink-50 dark:bg-pink-900/20', border: 'border-pink-200 dark:border-pink-800/40', text: 'text-pink-700 dark:text-pink-300' },
  'Design & Communication Graphics': { dot: 'bg-indigo-400', bg: 'bg-indigo-50 dark:bg-indigo-900/20', border: 'border-indigo-200 dark:border-indigo-800/40', text: 'text-indigo-700 dark:text-indigo-300' },
};

const DEFAULT_COLOR = { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' };

function getSubjectColor(name: string) {
  return SUBJECT_COLORS[name] || DEFAULT_COLOR;
}

// ─── Core Logic ──────────────────────────────────────────────────────────────

function computeBestSix(
  subjects: { subjectName: string; grade: Grade; isMaths: boolean }[]
): BestSixResult {
  const scored = subjects.map(s => ({
    subjectName: s.subjectName,
    points: getPointsForGrade(s.grade, s.isMaths),
    grade: s.grade,
  }));
  scored.sort((a, b) => b.points - a.points);
  const count = Math.min(6, scored.length);
  return {
    total: scored.slice(0, count).reduce((sum, s) => sum + s.points, 0),
    bestSix: scored.slice(0, count),
    outside: scored.slice(count),
  };
}

// ─── Points Summary Card ────────────────────────────────────────────────────

const PointsCard: React.FC<{
  label: string;
  points: number;
  maxPoints: number;
  delta?: number;
  bgClass: string;
  borderClass: string;
  textClass: string;
  barClass: string;
}> = ({ label, points, maxPoints, delta, bgClass, borderClass, textClass, barClass }) => {
  const pct = maxPoints > 0 ? Math.min(100, (points / maxPoints) * 100) : 0;
  return (
    <div className={`rounded-xl p-4 border ${bgClass} ${borderClass}`}>
      <p className={`text-[10px] font-bold uppercase tracking-widest ${textClass} mb-1`}>{label}</p>
      <div className="flex items-baseline gap-1.5">
        <span className={`font-serif text-3xl font-bold ${textClass}`}>{points}</span>
        <span className="text-sm text-zinc-400 dark:text-zinc-500 font-medium">/625</span>
      </div>
      <div className="w-full h-1.5 bg-zinc-200 dark:bg-white/10 rounded-full mt-2 overflow-hidden">
        <MotionDiv
          className={`h-full rounded-full ${barClass}`}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      </div>
      {delta !== undefined && delta !== 0 && (
        <span className={`inline-block mt-2 text-[10px] font-bold px-2 py-0.5 rounded-full ${
          delta > 0
            ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400'
            : 'bg-rose-100 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400'
        }`}>
          {delta > 0 ? '+' : ''}{delta} pts
        </span>
      )}
    </div>
  );
};

// ─── CAOPointsSimulator ──────────────────────────────────────────────────────

const CAOPointsSimulator: React.FC<CAOPointsSimulatorProps> = ({ profile, onOpenSettings }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'what-if'>('overview');
  const [showGains, setShowGains] = useState(true);
  const [simSubjects, setSimSubjects] = useState<SimSubject[]>([]);

  // Initialize / re-initialize from profile
  useEffect(() => {
    const subs = profile.subjects.map(s => {
      const lcSubject = LC_SUBJECTS.find(lc => lc.name === s.subjectName);
      return {
        subjectName: s.subjectName,
        level: s.level,
        currentGrade: s.currentGrade,
        targetGrade: s.targetGrade,
        whatIfGrade: s.currentGrade,
        isMaths: !!lcSubject?.isMaths,
      };
    });
    setSimSubjects(subs);
  }, [profile]);

  // Analysis computations
  const currentAnalysis = useMemo(() => {
    return computeBestSix(simSubjects.map(s => ({ subjectName: s.subjectName, grade: s.currentGrade, isMaths: s.isMaths })));
  }, [simSubjects]);

  const targetAnalysis = useMemo(() => {
    return computeBestSix(simSubjects.map(s => ({ subjectName: s.subjectName, grade: s.targetGrade, isMaths: s.isMaths })));
  }, [simSubjects]);

  const whatIfAnalysis = useMemo(() => {
    return computeBestSix(simSubjects.map(s => ({ subjectName: s.subjectName, grade: s.whatIfGrade, isMaths: s.isMaths })));
  }, [simSubjects]);

  const whatIfBestSixNames = useMemo(() => {
    return new Set(whatIfAnalysis.bestSix.map(s => s.subjectName));
  }, [whatIfAnalysis]);

  // Biggest gains: for each subject, compute net best-6 total gain from a one-grade improvement
  const biggestGains = useMemo(() => {
    const gains: { subjectName: string; fromGrade: Grade; toGrade: Grade; netGain: number }[] = [];
    for (const sub of simSubjects) {
      const grades = getGradesForLevel(sub.level);
      const currentIdx = grades.indexOf(sub.whatIfGrade);
      if (currentIdx <= 0) continue; // already at best grade
      const betterGrade = grades[currentIdx - 1];
      // Compute current best-6 total
      const currentTotal = whatIfAnalysis.total;
      // Compute new best-6 total with this one subject improved
      const modifiedSubjects = simSubjects.map(s =>
        s.subjectName === sub.subjectName
          ? { subjectName: s.subjectName, grade: betterGrade, isMaths: s.isMaths }
          : { subjectName: s.subjectName, grade: s.whatIfGrade, isMaths: s.isMaths }
      );
      const newTotal = computeBestSix(modifiedSubjects).total;
      const netGain = newTotal - currentTotal;
      if (netGain > 0) {
        gains.push({ subjectName: sub.subjectName, fromGrade: sub.whatIfGrade, toGrade: betterGrade, netGain });
      }
    }
    gains.sort((a, b) => b.netGain - a.netGain);
    return gains.slice(0, 5);
  }, [simSubjects, whatIfAnalysis.total]);

  const hasMathsHL = simSubjects.some(s => s.isMaths && s.level === 'higher');

  const handleWhatIfGradeChange = (subjectName: string, grade: Grade) => {
    setSimSubjects(prev => prev.map(s =>
      s.subjectName === subjectName ? { ...s, whatIfGrade: grade } : s
    ));
  };

  const handleResetAll = () => {
    setSimSubjects(prev => prev.map(s => ({ ...s, whatIfGrade: s.currentGrade })));
  };

  const bestSixCount = Math.min(6, simSubjects.length);
  const bestSixLabel = simSubjects.length < 6 ? `Best ${bestSixCount}` : 'Best 6';

  return (
    <div className="space-y-6">
      {/* A. Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">CAO Points Simulator</h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">Explore how grade changes affect your points.</p>
        </div>
        <button
          onClick={onOpenSettings}
          className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800"
          title="Edit subjects"
        >
          <Settings size={16} className="text-zinc-500 dark:text-zinc-400" />
        </button>
      </div>

      {/* B. Points Summary Cards */}
      <div className={`grid gap-3 ${activeTab === 'what-if' ? 'grid-cols-3' : 'grid-cols-2'}`}>
        <PointsCard
          label="Current"
          points={currentAnalysis.total}
          maxPoints={625}
          bgClass="bg-zinc-50 dark:bg-zinc-800/40"
          borderClass="border-zinc-200 dark:border-zinc-700/40"
          textClass="text-zinc-700 dark:text-zinc-300"
          barClass="bg-zinc-400 dark:bg-zinc-500"
        />
        <PointsCard
          label="Target"
          points={targetAnalysis.total}
          maxPoints={625}
          delta={targetAnalysis.total - currentAnalysis.total}
          bgClass="bg-emerald-50 dark:bg-emerald-900/15"
          borderClass="border-emerald-200 dark:border-emerald-800/40"
          textClass="text-emerald-700 dark:text-emerald-300"
          barClass="bg-emerald-500"
        />
        {activeTab === 'what-if' && (
          <PointsCard
            label="What-If"
            points={whatIfAnalysis.total}
            maxPoints={625}
            delta={whatIfAnalysis.total - currentAnalysis.total}
            bgClass="bg-purple-50 dark:bg-purple-900/15"
            borderClass="border-purple-200 dark:border-purple-800/40"
            textClass="text-purple-700 dark:text-purple-300"
            barClass="bg-purple-500"
          />
        )}
      </div>

      {/* C. Tab Switcher */}
      <div className="flex gap-1 p-1 bg-zinc-100 dark:bg-white/5 rounded-xl">
        <button
          onClick={() => setActiveTab('overview')}
          className={`flex-1 py-2.5 px-4 rounded-lg text-sm font-bold transition-all ${
            activeTab === 'overview'
              ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm'
              : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
          }`}
        >
          Overview
        </button>
        <button
          onClick={() => setActiveTab('what-if')}
          className={`flex-1 py-2.5 px-4 rounded-lg text-sm font-bold transition-all ${
            activeTab === 'what-if'
              ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm'
              : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
          }`}
        >
          What-If Explorer
        </button>
      </div>

      {/* D. Overview Tab */}
      <AnimatePresence mode="wait">
        {activeTab === 'overview' && (
          <MotionDiv
            key="overview"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="space-y-1"
          >
            {/* Best 6 header */}
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">
              {bestSixLabel} Subjects
            </p>

            {/* Best 6 ranked subjects */}
            {currentAnalysis.bestSix.map((sub, idx) => {
              const color = getSubjectColor(sub.subjectName);
              const profileSub = simSubjects.find(s => s.subjectName === sub.subjectName);
              const targetSub = targetAnalysis.bestSix.find(s => s.subjectName === sub.subjectName)
                || targetAnalysis.outside.find(s => s.subjectName === sub.subjectName);
              const targetPoints = targetSub?.points ?? 0;
              const targetGrade = profileSub?.targetGrade ?? sub.grade;
              const isMaths = profileSub?.isMaths ?? false;
              const mathsBonus = isMaths && sub.grade.startsWith('H') && getPointsForGrade(sub.grade, false) >= 46;

              return (
                <MotionDiv
                  key={sub.subjectName}
                  initial={{ opacity: 0, x: -12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.04 }}
                  className="flex items-center gap-3 p-3 rounded-xl bg-white/60 dark:bg-white/5 border border-zinc-200/60 dark:border-white/10"
                >
                  <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500 w-5 text-center">{idx + 1}</span>
                  <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${color.dot}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200 truncate">{sub.subjectName}</p>
                      {mathsBonus && (
                        <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400">+25</span>
                      )}
                    </div>
                    <p className="text-[11px] text-zinc-500 dark:text-zinc-400">
                      {sub.grade} <ArrowRight size={10} className="inline" /> {targetGrade}
                    </p>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{sub.points}</p>
                    {targetPoints !== sub.points && (
                      <p className={`text-[10px] font-bold ${targetPoints > sub.points ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                        {targetPoints > sub.points ? '+' : ''}{targetPoints - sub.points}
                      </p>
                    )}
                  </div>
                </MotionDiv>
              );
            })}

            {/* Outside best 6 */}
            {currentAnalysis.outside.length > 0 && (
              <>
                <div className="flex items-center gap-3 py-2 px-3">
                  <div className="flex-1 h-px bg-zinc-200 dark:bg-white/10" />
                  <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Outside {bestSixLabel}</p>
                  <div className="flex-1 h-px bg-zinc-200 dark:bg-white/10" />
                </div>
                {currentAnalysis.outside.map((sub, idx) => {
                  const color = getSubjectColor(sub.subjectName);
                  const profileSub = simSubjects.find(s => s.subjectName === sub.subjectName);
                  const targetGrade = profileSub?.targetGrade ?? sub.grade;

                  return (
                    <MotionDiv
                      key={sub.subjectName}
                      initial={{ opacity: 0, x: -12 }}
                      animate={{ opacity: 0.5, x: 0 }}
                      transition={{ delay: (currentAnalysis.bestSix.length + idx) * 0.04 }}
                      className="flex items-center gap-3 p-3 rounded-xl"
                    >
                      <span className="text-xs font-bold text-zinc-300 dark:text-zinc-600 w-5 text-center">{currentAnalysis.bestSix.length + idx + 1}</span>
                      <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${color.dot} opacity-50`} />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-zinc-500 dark:text-zinc-500 truncate">{sub.subjectName}</p>
                        <p className="text-[11px] text-zinc-400 dark:text-zinc-600">
                          {sub.grade} <ArrowRight size={10} className="inline" /> {targetGrade}
                        </p>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <p className="text-sm font-bold text-zinc-400 dark:text-zinc-600">{sub.points}</p>
                      </div>
                    </MotionDiv>
                  );
                })}
              </>
            )}
          </MotionDiv>
        )}

        {/* E. What-If Tab */}
        {activeTab === 'what-if' && (
          <MotionDiv
            key="what-if"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="space-y-4"
          >
            {/* Reset button */}
            <div className="flex items-center justify-between">
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
                Adjust grades to explore scenarios
              </p>
              <button
                onClick={handleResetAll}
                className="flex items-center gap-1.5 text-xs font-bold text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 transition-colors px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-white/5"
              >
                <RotateCcw size={12} /> Reset All
              </button>
            </div>

            {/* Per-subject grade cards */}
            {simSubjects.map((sub, idx) => {
              const color = getSubjectColor(sub.subjectName);
              const grades = getGradesForLevel(sub.level);
              const subjectPoints = getPointsForGrade(sub.whatIfGrade, sub.isMaths);
              const isInBestSix = whatIfBestSixNames.has(sub.subjectName);
              const mathsBonus = sub.isMaths && sub.whatIfGrade.startsWith('H') && getPointsForGrade(sub.whatIfGrade, false) >= 46;

              return (
                <MotionDiv
                  key={sub.subjectName}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.03 }}
                  className={`rounded-xl border p-4 ${color.bg} ${color.border}`}
                >
                  <div className="flex items-center gap-2 mb-3">
                    <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${color.dot}`} />
                    <p className={`text-sm font-bold flex-1 ${color.text}`}>{sub.subjectName}</p>
                    {isInBestSix && <Star size={14} className="text-amber-500 flex-shrink-0" />}
                    <span className={`text-sm font-bold font-mono ${color.text}`}>{subjectPoints} pts</span>
                    {mathsBonus && (
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400">+25</span>
                    )}
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {grades.map(g => {
                      const isSelected = sub.whatIfGrade === g;
                      const isCurrent = sub.currentGrade === g;
                      return (
                        <button
                          key={g}
                          onClick={() => handleWhatIfGradeChange(sub.subjectName, g)}
                          className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all ${
                            isSelected
                              ? 'bg-purple-500 text-white shadow-sm'
                              : isCurrent
                                ? 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 ring-2 ring-zinc-300 dark:ring-zinc-600'
                                : 'bg-white/60 dark:bg-white/5 text-zinc-500 dark:text-zinc-400 hover:bg-white dark:hover:bg-white/10'
                          }`}
                        >
                          {g}
                        </button>
                      );
                    })}
                  </div>
                </MotionDiv>
              );
            })}
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* F. Biggest Gains Panel */}
      {biggestGains.length > 0 && (
        <div className="bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-700/30 rounded-xl overflow-hidden">
          <button
            onClick={() => setShowGains(!showGains)}
            className="w-full flex items-center justify-between px-4 py-3 text-left"
          >
            <div className="flex items-center gap-2">
              <TrendingUp size={16} className="text-amber-600 dark:text-amber-400" />
              <p className="text-sm font-bold text-amber-700 dark:text-amber-300">Biggest Gains Available</p>
            </div>
            {showGains ? <ChevronUp size={16} className="text-amber-500" /> : <ChevronDown size={16} className="text-amber-500" />}
          </button>
          <AnimatePresence>
            {showGains && (
              <MotionDiv
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="overflow-hidden"
              >
                <div className="px-4 pb-4 space-y-2">
                  <p className="text-[10px] text-amber-600 dark:text-amber-400 mb-2">
                    Top improvements ranked by net {bestSixLabel} total gain from one grade up.
                  </p>
                  {biggestGains.map((gain, idx) => {
                    const color = getSubjectColor(gain.subjectName);
                    return (
                      <div key={gain.subjectName} className="flex items-center gap-3 p-2.5 rounded-lg bg-white/60 dark:bg-white/5">
                        <span className="text-xs font-bold text-amber-500 w-5 text-center">{idx + 1}</span>
                        <div className={`w-2 h-2 rounded-full ${color.dot}`} />
                        <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200 flex-1">{gain.subjectName}</p>
                        <p className="text-[11px] text-zinc-500 dark:text-zinc-400">
                          {gain.fromGrade} <ArrowRight size={10} className="inline" /> {gain.toGrade}
                        </p>
                        <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-900/30 px-2 py-0.5 rounded-full">
                          +{gain.netGain} pts
                        </span>
                      </div>
                    );
                  })}
                </div>
              </MotionDiv>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* G. Maths Bonus Explainer */}
      {hasMathsHL && (
        <div className="flex items-start gap-3 p-4 bg-indigo-50 dark:bg-indigo-900/15 border border-indigo-200 dark:border-indigo-700/30 rounded-xl">
          <Info size={16} className="text-indigo-500 dark:text-indigo-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-bold text-indigo-700 dark:text-indigo-300">Maths HL Bonus</p>
            <p className="text-xs text-indigo-600 dark:text-indigo-400 leading-relaxed mt-1">
              Students taking Higher Level Mathematics receive an additional 25 CAO points for grades H1 through H6. This bonus is automatically included in all calculations above.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default CAOPointsSimulator;
