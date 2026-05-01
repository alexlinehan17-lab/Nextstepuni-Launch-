/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Settings, Star, RotateCcw, ChevronDown, ChevronUp, TrendingUp, Info, Compass,
} from 'lucide-react';
import {
  type StudentSubjectProfile, type Grade, type Level,
  LC_SUBJECTS, getPointsForGrade, getGradesForLevel,
} from './subjectData';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useInnovationData } from '../contexts/InnovationDataContext';

// ─── Subject Colours ─────────────────────────────────────────────────────────

const SUBJECT_HEX: Record<string, string> = {
  'English': '#3b82f6', 'Irish': '#10b981', 'Mathematics': '#6366f1',
  'French': '#0ea5e9', 'German': '#eab308', 'Spanish': '#f97316',
  'Italian': '#ef4444', 'Japanese': '#ec4899', 'Physics': '#06b6d4',
  'Chemistry': '#14b8a6', 'Biology': '#84cc16', 'Applied Maths': '#8b5cf6',
  'Computer Science': '#d946ef', 'Ag Science': '#22c55e', 'Accounting': '#f59e0b',
  'Business': '#d97706', 'Economics': '#ca8a04', 'History': '#a855f7',
  'Geography': '#059669', 'Politics & Society': '#f43f5e',
  'Religious Education': '#71717a', 'Classical Studies': '#78716c',
  'Home Economics': '#fb923c', 'Construction Studies': '#64748b',
  'Engineering': '#6b7280', 'Art': '#fb7185', 'Music': '#f472b6',
  'Applied Mathematics': '#8b5cf6',
};
function getSubjectHex(name: string): string {
  return SUBJECT_HEX[name] || '#71717a';
}

// ─── Types ───────────────────────────────────────────────────────────────────

interface CAOPointsSimulatorProps {
  profile: StudentSubjectProfile;
  uid?: string;
  onOpenSettings: () => void;
}

export interface WhatIfScenario {
  subjectName: string;
  currentGrade: Grade;
  whatIfGrade: Grade;
  pointsGain: number;
  isMaths: boolean;
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

// ─── Points Summary Card (Mercury-style: commanding numbers) ─────────────────

const PointsCard: React.FC<{
  label: string;
  points: number;
  maxPoints: number;
  delta?: number;
  accentColor?: string;
  variant?: 'current' | 'target' | 'whatif';
  basePoints?: number;
}> = ({ label, points, maxPoints, delta, accentColor = '#2A7D6F', variant = 'current', basePoints }) => {
  const pct = maxPoints > 0 ? Math.min(100, (points / maxPoints) * 100) : 0;

  // Typography sizing by variant
  const isTarget = variant === 'target';
  const isWhatIf = variant === 'whatif';
  const numberSize = isTarget ? 'text-5xl' : 'text-4xl';
  // Label: teal for target, muted for others
  const labelColorClass = isTarget ? '' : 'text-[#A8A29E] dark:text-zinc-500';
  const labelColorStyle = isTarget ? { color: '#2A7D6F' } : undefined;

  // What-If number colour reacts to changes
  let numberColorClass = 'text-[#1A1A1A] dark:text-white';
  let numberColorStyle: React.CSSProperties | undefined = undefined;
  if (isWhatIf && basePoints !== undefined) {
    if (points > basePoints) { numberColorClass = ''; numberColorStyle = { color: '#2A7D6F' }; }
    else if (points < basePoints) { numberColorClass = ''; numberColorStyle = { color: '#DC2626' }; }
    // else stays dark — no change
  }

  return (
    <div>
      <p className={`text-xs font-semibold uppercase tracking-wider mb-1.5 ${labelColorClass}`} style={labelColorStyle}>{label}</p>
      <div className="flex items-baseline gap-1.5">
        <span className={`${numberSize} font-apercu font-black ${numberColorClass}`} style={{ ...numberColorStyle, letterSpacing: '-0.02em' }}>{points}</span>
        <span className="text-sm font-medium" style={{ color: '#C4C0BC' }}>/625</span>
      </div>
      <div className="w-full h-[6px] rounded-full mt-3 overflow-hidden bg-[#EDEBE8] dark:bg-zinc-800">
        <MotionDiv
          className="h-full rounded-full"
          style={{ backgroundColor: accentColor }}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      </div>
      {delta !== undefined && delta !== 0 && (
        <span
          className="inline-block mt-2 text-xs font-bold"
          style={{ color: delta > 0 ? '#2A7D6F' : '#DC2626' }}
        >
          {delta > 0 ? '+' : ''}{delta} pts
        </span>
      )}
    </div>
  );
};

// ─── CAOPointsSimulator ──────────────────────────────────────────────────────

const CAOPointsSimulator: React.FC<CAOPointsSimulatorProps> = ({ profile, uid, onOpenSettings }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'what-if'>('overview');
  const [showGains, setShowGains] = useState(true);
  const [simSubjects, setSimSubjects] = useState<SimSubject[]>([]);
  const saveTimerRef = useRef<ReturnType<typeof setTimeout>>();

  // Shared data from InnovationDataContext
  const { mockResults: mockResultsCtx, futureFinderPicks: ffPicks } = useInnovationData();
  const mocks = mockResultsCtx.mocks;
  const [mockBannerDismissed, setMockBannerDismissed] = useState(false);

  const latestMockGrades = useMemo(() => {
    if (mocks.length === 0) return null;
    const latest = mocks[0]; // mocks are sorted newest first
    const gradeMap: Record<string, string> = {};
    for (const entry of latest.entries) {
      gradeMap[entry.subjectName] = entry.grade;
    }
    return gradeMap;
  }, [mocks]);

  const mockUpdatesAvailable = useMemo(() => {
    if (!latestMockGrades || mockBannerDismissed) return [];
    return simSubjects.filter(s => {
      const mockGrade = latestMockGrades[s.subjectName];
      return mockGrade && mockGrade !== s.currentGrade;
    }).map(s => ({
      subjectName: s.subjectName,
      currentGrade: s.currentGrade,
      mockGrade: latestMockGrades[s.subjectName] as Grade,
    }));
  }, [simSubjects, latestMockGrades, mockBannerDismissed]);

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

  // Save computed points to Firestore so other components (ComebackEngine) can read them
  useEffect(() => {
    if (!uid || simSubjects.length === 0) return;
    const timer = setTimeout(() => {
      setDoc(doc(db, 'progress', uid), {
        computedPoints: { current: currentAnalysis.total, target: targetAnalysis.total },
      }, { merge: true }).catch(() => {});
    }, 2000);
    return () => clearTimeout(timer);
  }, [uid, currentAnalysis.total, targetAnalysis.total, simSubjects.length]);

  const hasMathsHL = simSubjects.some(s => s.isMaths && s.level === 'higher');

  const handleWhatIfGradeChange = (subjectName: string, grade: Grade) => {
    setSimSubjects(prev => {
      const next = prev.map(s =>
        s.subjectName === subjectName ? { ...s, whatIfGrade: grade } : s
      );
      // Debounced save to Firestore
      if (uid) {
        clearTimeout(saveTimerRef.current);
        saveTimerRef.current = setTimeout(() => {
          const scenarios: WhatIfScenario[] = next
            .filter(s => s.whatIfGrade !== s.currentGrade)
            .map(s => ({
              subjectName: s.subjectName,
              currentGrade: s.currentGrade,
              whatIfGrade: s.whatIfGrade,
              pointsGain: getPointsForGrade(s.whatIfGrade, s.isMaths) - getPointsForGrade(s.currentGrade, s.isMaths),
              isMaths: s.isMaths,
            }));
          setDoc(doc(db, 'progress', uid), {
            caoSimulator: { whatIfScenarios: scenarios, updatedAt: new Date().toISOString() },
          }, { merge: true }).catch(() => {});
        }, 1500);
      }
      return next;
    });
  };

  const handleResetAll = () => {
    setSimSubjects(prev => prev.map(s => ({ ...s, whatIfGrade: s.currentGrade })));
    // Clear saved scenarios
    if (uid) {
      setDoc(doc(db, 'progress', uid), {
        caoSimulator: { whatIfScenarios: [], updatedAt: new Date().toISOString() },
      }, { merge: true }).catch(() => {});
    }
  };

  const bestSixCount = Math.min(6, simSubjects.length);
  const bestSixLabel = simSubjects.length < 6 ? `Best ${bestSixCount}` : 'Best 6';

  if (simSubjects.length === 0) {
    return (
      <div className="text-center py-16 space-y-4">
        <div className="w-16 h-16 mx-auto rounded-2xl bg-zinc-100 dark:bg-zinc-900/30 flex items-center justify-center">
          <Settings size={32} className="text-zinc-400" />
        </div>
        <h3 className="text-lg font-medium text-zinc-800 dark:text-white">Explore how grade changes affect your points</h3>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 max-w-sm mx-auto leading-relaxed">
          Adjust any subject to see the impact on your best-six total. Find the biggest gains with the least effort.
        </p>
        <button
          onClick={onOpenSettings}
          className="px-6 py-3 rounded-xl text-white text-sm font-medium transition-colors"
          style={{ backgroundColor: '#2A7D6F' }}
        >
          Set up subjects
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-end">
        <button
          onClick={onOpenSettings}
          className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-50 dark:hover:bg-zinc-800"
          title="Edit subjects"
        >
          <Settings size={16} className="text-zinc-500 dark:text-zinc-400" />
        </button>
      </div>

      {/* B. Points Summary — Mercury style: white card, confident type, no decoration */}
      <div
        className="rounded-2xl px-6 py-5 bg-[#FAF7F4] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800"
        style={{ boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}
      >
        <div className={`grid gap-6 ${activeTab === 'what-if' ? 'grid-cols-3' : 'grid-cols-2'}`}>
          <PointsCard label="Current" points={currentAnalysis.total} maxPoints={625} accentColor="#C4C0BC" variant="current" />
          <PointsCard label="Target" points={targetAnalysis.total} maxPoints={625} delta={targetAnalysis.total - currentAnalysis.total} accentColor="#2A7D6F" variant="target" />
          {activeTab === 'what-if' && (
            <PointsCard label="What-If" points={whatIfAnalysis.total} maxPoints={625} delta={whatIfAnalysis.total - currentAnalysis.total} accentColor="#3b82f6" variant="whatif" basePoints={currentAnalysis.total} />
          )}
        </div>
        {/* Target course from Future Finder */}
        {ffPicks.length > 0 && (
          <div className="mt-4 pt-4 flex items-center justify-between border-t border-[#EDEBE8] dark:border-zinc-800">
            <div className="flex-1 min-w-0">
              <p className="text-[10px] font-bold uppercase tracking-widest text-[#A8A29E] dark:text-zinc-500">Your #1 pick</p>
              <p className="text-sm font-semibold truncate text-[#1A1A1A] dark:text-white">{ffPicks[0].title}</p>
              <p className="text-[10px] text-[#A8A29E] dark:text-zinc-500">{ffPicks[0].institution} · {ffPicks[0].typicalPoints} pts</p>
            </div>
            <div className="text-right shrink-0 ml-3">
              {currentAnalysis.total >= ffPicks[0].typicalPoints ? (
                <span className="text-[10px] font-bold px-2.5 py-1 rounded-full" style={{ backgroundColor: '#DEF7EC', color: '#276749' }}>On track</span>
              ) : (
                <span className="text-[10px] font-bold px-2.5 py-1 rounded-full" style={{ backgroundColor: '#FDE8E8', color: '#C53030' }}>
                  {ffPicks[0].typicalPoints - currentAnalysis.total}pt gap
                </span>
              )}
            </div>
          </div>
        )}
        {/* Gap indicator */}
        {targetAnalysis.total > currentAnalysis.total && !ffPicks.length && (
          <div className="mt-4 pt-4 flex items-center justify-between border-t border-[#EDEBE8] dark:border-zinc-800">
            <span className="text-xs font-medium text-[#78716C] dark:text-zinc-400">Gap to target</span>
            <div className="flex items-center gap-2">
              <span className="text-base font-black" style={{ color: '#2A7D6F' }}>+{targetAnalysis.total - currentAnalysis.total} pts</span>
              <span className="text-xs font-medium text-[#A8A29E] dark:text-zinc-500">{Math.round((currentAnalysis.total / targetAnalysis.total) * 100)}% there</span>
            </div>
          </div>
        )}
      </div>

      {/* Mock Results Banner */}
      {mockUpdatesAvailable.length > 0 && (
        <div
          className="rounded-xl p-4 space-y-3"
          style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <TrendingUp size={16} className="text-zinc-500" />
              <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200">Mock results available</p>
            </div>
            <button
              onClick={() => setMockBannerDismissed(true)}
              className="text-xs text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
            >
              Dismiss
            </button>
          </div>
          <p className="text-xs text-zinc-500">
            Your latest mock shows different grades for {mockUpdatesAvailable.length} subject{mockUpdatesAvailable.length > 1 ? 's' : ''}. Update your what-if explorer to match?
          </p>
          <div className="space-y-1">
            {mockUpdatesAvailable.slice(0, 3).map(u => (
              <p key={u.subjectName} className="text-xs text-zinc-500">
                {u.subjectName}: {u.currentGrade} → <span className="font-medium" style={{ color: '#2A7D6F' }}>{u.mockGrade}</span> (mock)
              </p>
            ))}
          </div>
          <button
            onClick={() => {
              for (const u of mockUpdatesAvailable) {
                handleWhatIfGradeChange(u.subjectName, u.mockGrade);
              }
              setMockBannerDismissed(true);
            }}
            className="px-4 py-2 rounded-lg text-xs font-medium text-white transition-colors"
            style={{ backgroundColor: '#2A7D6F' }}
          >
            Apply mock grades to What-If
          </button>
        </div>
      )}

      {/* C. Tab Switcher */}
      <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit">
        <button
          onClick={() => setActiveTab('overview')}
          className={`py-2 px-4 rounded-lg text-sm transition-all ${
            activeTab === 'overview'
              ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-medium shadow-sm'
              : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
          }`}
        >
          Overview
        </button>
        <button
          onClick={() => setActiveTab('what-if')}
          className={`py-2 px-4 rounded-lg text-sm transition-all ${
            activeTab === 'what-if'
              ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-medium shadow-sm'
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
            className="space-y-0"
          >
            {/* Best 6 header */}
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">
              {bestSixLabel} Subjects
            </p>

            {/* Best 6 ranked subjects */}
            {currentAnalysis.bestSix.map((sub, idx) => {
              const profileSub = simSubjects.find(s => s.subjectName === sub.subjectName);
              const targetSub = targetAnalysis.bestSix.find(s => s.subjectName === sub.subjectName)
                || targetAnalysis.outside.find(s => s.subjectName === sub.subjectName);
              const targetPoints = targetSub?.points ?? 0;
              const targetGrade = profileSub?.targetGrade ?? sub.grade;
              const isMaths = profileSub?.isMaths ?? false;
              const mathsBonus = isMaths && sub.grade.startsWith('H') && getPointsForGrade(sub.grade, false) >= 46;

              const maxBestSixPts = Math.max(...currentAnalysis.bestSix.map(s => s.points), 1);
              const barPct = (sub.points / maxBestSixPts) * 100;

              return (
                <MotionDiv
                  key={sub.subjectName}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: idx * 0.04 }}
                  className={`py-3 px-1 ${idx < currentAnalysis.bestSix.length - 1 ? 'border-b border-[#EDEBE8] dark:border-zinc-800' : ''}`}
                >
                  <div className="flex items-center gap-3 mb-1.5">
                    <span className="text-[11px] font-bold w-4 text-right" style={{ color: '#C4C0BC' }}>{idx + 1}</span>
                    <div className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: getSubjectHex(sub.subjectName) }} />
                    <p className="text-sm font-semibold flex-1 min-w-0 truncate text-[#1A1A1A] dark:text-white">{sub.subjectName}</p>
                    {mathsBonus && (
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full" style={{ backgroundColor: '#EDF5F3', color: '#2A7D6F' }}>+25</span>
                    )}
                    <div className="flex items-center gap-1.5 flex-shrink-0">
                      <span className="text-xs text-[#A8A29E] dark:text-zinc-500">{sub.grade} → {targetGrade}</span>
                      <span className="text-sm font-bold font-mono text-[#1A1A1A] dark:text-white">{sub.points}</span>
                    </div>
                    {targetPoints !== sub.points && (
                      <span className="text-xs font-semibold flex-shrink-0" style={{ color: targetPoints > sub.points ? '#2A7D6F' : '#ef4444' }}>
                        {targetPoints > sub.points ? '+' : ''}{targetPoints - sub.points}
                      </span>
                    )}
                  </div>
                  {/* Contribution bar */}
                  <div className="ml-[30px] h-1 rounded-full overflow-hidden bg-[#EDEBE8] dark:bg-zinc-800">
                    <MotionDiv
                      className="h-full rounded-full"
                      style={{ backgroundColor: getSubjectHex(sub.subjectName), opacity: 0.6 }}
                      initial={{ width: 0 }}
                      animate={{ width: `${barPct}%` }}
                      transition={{ duration: 0.5, delay: idx * 0.05, ease: 'easeOut' }}
                    />
                  </div>
                </MotionDiv>
              );
            })}

            {/* Outside best 6 */}
            {currentAnalysis.outside.length > 0 && (
              <>
                <div className="flex items-center gap-3 py-3 px-1">
                  <div className="flex-1 h-px bg-zinc-200 dark:bg-zinc-800" />
                  <p className="text-[10px] text-zinc-300 dark:text-zinc-600 uppercase tracking-widest">Outside {bestSixLabel}</p>
                  <div className="flex-1 h-px bg-zinc-200 dark:bg-zinc-800" />
                </div>
                {currentAnalysis.outside.map((sub, idx) => {
                  const profileSub = simSubjects.find(s => s.subjectName === sub.subjectName);
                  const targetGrade = profileSub?.targetGrade ?? sub.grade;

                  return (
                    <MotionDiv
                      key={sub.subjectName}
                      initial={{ opacity: 0, x: -12 }}
                      animate={{ opacity: 0.5, x: 0 }}
                      transition={{ delay: (currentAnalysis.bestSix.length + idx) * 0.04 }}
                      className="flex items-center gap-3 py-3 px-1 border-b border-zinc-50 dark:border-zinc-800/50"
                    >
                      <span className="text-xs text-zinc-300 dark:text-zinc-600 w-5 text-center">{currentAnalysis.bestSix.length + idx + 1}</span>
                      <div className="w-1.5 h-1.5 rounded-full flex-shrink-0 bg-zinc-300" />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-zinc-500 dark:text-zinc-500 truncate">{sub.subjectName}</p>
                        <p className="text-xs text-zinc-300 dark:text-zinc-600">
                          {sub.grade} → {targetGrade}
                        </p>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <p className="text-sm font-medium text-zinc-400 dark:text-zinc-600">{sub.points}</p>
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
            className="space-y-0"
          >
            {/* Reset button */}
            <div className="flex items-center justify-between mb-4">
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
                Adjust grades to explore scenarios
              </p>
              <button
                onClick={handleResetAll}
                className="flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
              >
                <RotateCcw size={12} /> Reset All
              </button>
            </div>

            {/* Per-subject grade rows */}
            {simSubjects.map((sub, idx) => {
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
                  className="py-4 border-b border-zinc-100 dark:border-zinc-800"
                >
                  <div className="flex items-center gap-2 mb-3">
                    <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200 flex-1">{sub.subjectName}</p>
                    {isInBestSix && <Star size={14} className="text-zinc-400 flex-shrink-0" />}
                    <span className="text-sm font-medium text-zinc-800 dark:text-zinc-200 font-mono">{subjectPoints} pts</span>
                    {mathsBonus && (
                      <span className="text-[9px] font-medium text-zinc-400">+25</span>
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
                          className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                            isSelected
                              ? 'shadow-sm'
                              : isCurrent
                                ? 'text-[#A8A29E] dark:text-zinc-500 ring-1 ring-zinc-300 dark:ring-zinc-600'
                                : 'text-[#A8A29E] dark:text-zinc-500 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                          }`}
                          style={{
                            backgroundColor: isSelected ? getSubjectHex(sub.subjectName) : 'rgba(0,0,0,0.04)',
                            ...(isSelected ? { color: '#fff' } : {}),
                          }}
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
        <div
          className="rounded-xl overflow-hidden"
          style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}
        >
          <button
            onClick={() => setShowGains(!showGains)}
            className="w-full flex items-center justify-between px-4 py-3 text-left"
          >
            <div className="flex items-center gap-2">
              <TrendingUp size={16} className="text-zinc-400" />
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">Biggest Gains Available</p>
            </div>
            {showGains ? <ChevronUp size={16} className="text-zinc-400" /> : <ChevronDown size={16} className="text-zinc-400" />}
          </button>
          <AnimatePresence>
            {showGains && (
              <MotionDiv
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="overflow-hidden"
              >
                <div className="px-4 pb-4 space-y-0">
                  <p className="text-[10px] text-zinc-400 mb-3">
                    Top improvements ranked by net {bestSixLabel} total gain from one grade up.
                  </p>
                  {biggestGains.map((gain, idx) => (
                    <div
                      key={gain.subjectName}
                      className={`flex items-center gap-3 py-2.5 ${idx < biggestGains.length - 1 ? 'border-b border-[#EDEBE8] dark:border-zinc-800' : ''}`}
                    >
                      {idx === 0 ? (
                        <span className="text-[9px] font-bold uppercase px-1.5 py-0.5 rounded" style={{ backgroundColor: '#EDF5F3', color: '#2A7D6F' }}>Best</span>
                      ) : (
                        <span className="text-[11px] font-bold w-8 text-center" style={{ color: '#C4C0BC' }}>{idx + 1}</span>
                      )}
                      <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: getSubjectHex(gain.subjectName) }} />
                      <p className="text-sm font-medium flex-1 text-[#1A1A1A] dark:text-white">{gain.subjectName}</p>
                      <p className="text-xs text-[#A8A29E] dark:text-zinc-500">
                        {gain.fromGrade} → {gain.toGrade}
                      </p>
                      <span className="text-sm font-bold" style={{ color: '#2A7D6F' }}>
                        +{gain.netGain}
                      </span>
                    </div>
                  ))}
                </div>
              </MotionDiv>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* G. FutureFinder Course Picks with Gap Analysis */}
      {ffPicks.length > 0 && (
        <div
          className="rounded-xl p-4 space-y-3"
          style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}
        >
          <div className="flex items-center gap-2">
            <Compass size={16} className="text-zinc-400" />
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">Your Future Finder Picks</p>
          </div>
          <div className="space-y-0">
            {ffPicks.map(course => {
              const gap = Math.max(0, course.typicalPoints - whatIfAnalysis.total);
              const isReachable = gap === 0;
              return (
                <div key={course.code} className="flex items-center gap-3 py-2.5 border-b border-zinc-100 dark:border-zinc-800 last:border-b-0">
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-zinc-800 dark:text-zinc-200 truncate">{course.title}</p>
                    <p className="text-[10px] text-zinc-400">{course.institution} — {course.typicalPoints} pts</p>
                  </div>
                  {isReachable ? (
                    <span className="text-xs font-medium text-emerald-600">
                      On track
                    </span>
                  ) : (
                    <span className="text-xs font-medium" style={{ color: '#2A7D6F' }}>
                      {gap} pts to go
                    </span>
                  )}
                </div>
              );
            })}
          </div>
          {biggestGains.length > 0 && ffPicks.some(c => c.typicalPoints > whatIfAnalysis.total) && (
            <p className="text-[10px] text-zinc-400 italic">
              Quick win: upgrade {biggestGains[0].subjectName} from {biggestGains[0].fromGrade} to {biggestGains[0].toGrade} for +{biggestGains[0].netGain} points
            </p>
          )}
        </div>
      )}

      {/* H. Maths Bonus Explainer */}
      {hasMathsHL && (
        <div className="flex items-start gap-3 pl-4" style={{ borderLeft: '2px solid #e4e4e7' }}>
          <Info size={16} className="text-zinc-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-xs font-medium text-zinc-500 italic">Maths HL Bonus</p>
            <p className="text-xs text-zinc-500 leading-relaxed mt-1 italic">
              Students taking Higher Level Mathematics receive an additional 25 CAO points for grades H1 through H6. This bonus is automatically included in all calculations above.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default CAOPointsSimulator;
