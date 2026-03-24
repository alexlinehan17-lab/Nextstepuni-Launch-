/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Settings, Star, RotateCcw, ChevronDown, ChevronUp, TrendingUp, Info, ArrowRight, Compass,
} from 'lucide-react';
import {
  type StudentSubjectProfile, type Grade, type Level,
  LC_SUBJECTS, getPointsForGrade, getGradesForLevel,
} from './subjectData';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type CAOCourse, hydrateCourses } from './futureFinderData';
import { useMockResults } from '../hooks/useMockResults';

const MotionDiv = motion.div as any;

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

// ─── Points Summary Card ────────────────────────────────────────────────────

const PointsCard: React.FC<{
  label: string;
  points: number;
  maxPoints: number;
  delta?: number;
}> = ({ label, points, maxPoints, delta }) => {
  const pct = maxPoints > 0 ? Math.min(100, (points / maxPoints) * 100) : 0;
  return (
    <div
      className="rounded-xl p-4"
      style={{
        backgroundColor: '#FAF7F4',
        border: '0.5px solid rgba(0,0,0,0.07)',
      }}
    >
      <div className="dark:hidden">
        <p className="text-[10px] font-medium uppercase tracking-widest text-zinc-400 mb-1">{label}</p>
        <div className="flex items-baseline gap-1.5">
          <span className="text-3xl font-medium" style={{ color: '#2A7D6F' }}>{points}</span>
          <span className="text-sm text-zinc-400 font-medium">/625</span>
        </div>
        <div className="w-full h-1 bg-zinc-200 rounded-full mt-2 overflow-hidden">
          <MotionDiv
            className="h-full rounded-full"
            style={{ backgroundColor: '#2A7D6F' }}
            initial={{ width: 0 }}
            animate={{ width: `${pct}%` }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
          />
        </div>
        {delta !== undefined && delta !== 0 && (
          <span
            className="inline-block mt-2 text-xs font-medium"
            style={{ color: delta > 0 ? '#2A7D6F' : undefined }}
          >
            <span className={delta < 0 ? 'text-rose-500' : ''}>
              {delta > 0 ? '+' : ''}{delta} pts
            </span>
          </span>
        )}
      </div>
      <div className="hidden dark:block">
        <div
          className="rounded-xl p-4 -m-4"
          style={{
            backgroundColor: 'rgba(255,255,255,0.04)',
            border: '0.5px solid rgba(255,255,255,0.08)',
          }}
        >
          <p className="text-[10px] font-medium uppercase tracking-widest text-zinc-400 mb-1">{label}</p>
          <div className="flex items-baseline gap-1.5">
            <span className="text-3xl font-medium" style={{ color: '#4DB8A4' }}>{points}</span>
            <span className="text-sm text-zinc-400 font-medium">/625</span>
          </div>
          <div className="w-full h-1 bg-zinc-200 dark:bg-zinc-700 rounded-full mt-2 overflow-hidden">
            <MotionDiv
              className="h-full rounded-full"
              style={{ backgroundColor: '#4DB8A4' }}
              initial={{ width: 0 }}
              animate={{ width: `${pct}%` }}
              transition={{ duration: 0.6, ease: 'easeOut' }}
            />
          </div>
          {delta !== undefined && delta !== 0 && (
            <span
              className="inline-block mt-2 text-xs font-medium"
              style={{ color: delta > 0 ? '#4DB8A4' : undefined }}
            >
              <span className={delta < 0 ? 'text-rose-500' : ''}>
                {delta > 0 ? '+' : ''}{delta} pts
              </span>
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

// ─── CAOPointsSimulator ──────────────────────────────────────────────────────

const CAOPointsSimulator: React.FC<CAOPointsSimulatorProps> = ({ profile, uid, onOpenSettings }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'what-if'>('overview');
  const [showGains, setShowGains] = useState(true);
  const [simSubjects, setSimSubjects] = useState<SimSubject[]>([]);
  const [ffPicks, setFfPicks] = useState<CAOCourse[]>([]);
  const saveTimerRef = useRef<ReturnType<typeof setTimeout>>();

  // Mock results integration (War Room → CAO Simulator)
  const { mocks } = useMockResults(uid);
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

  // Load FutureFinder picks from Firestore
  useEffect(() => {
    if (!uid) return;
    let cancelled = false;
    getDoc(doc(db, 'progress', uid)).then(snap => {
      if (cancelled) return;
      const data = snap.data();
      if (data?.futureFinder?.topPicks) {
        const hydrated = hydrateCourses(data.futureFinder.topPicks).slice(0, 5);
        setFfPicks(hydrated);
      }
    }).catch(() => {});
    return () => { cancelled = true; };
  }, [uid]);

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
      {/* A. Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-zinc-900 dark:text-white">CAO Points Simulator</h2>
          <p className="text-sm text-zinc-400 mt-1">Explore how grade changes affect your points.</p>
        </div>
        <button
          onClick={onOpenSettings}
          className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-50 dark:hover:bg-zinc-800"
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
        />
        <PointsCard
          label="Target"
          points={targetAnalysis.total}
          maxPoints={625}
          delta={targetAnalysis.total - currentAnalysis.total}
        />
        {activeTab === 'what-if' && (
          <PointsCard
            label="What-If"
            points={whatIfAnalysis.total}
            maxPoints={625}
            delta={whatIfAnalysis.total - currentAnalysis.total}
          />
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

              return (
                <MotionDiv
                  key={sub.subjectName}
                  initial={{ opacity: 0, x: -12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.04 }}
                  className="flex items-center gap-3 py-3 px-1 border-b border-zinc-100 dark:border-zinc-800"
                >
                  <span className="text-xs text-zinc-400 w-5 text-center">{idx + 1}</span>
                  <div className="w-1.5 h-1.5 rounded-full flex-shrink-0 bg-zinc-400" />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200 truncate">{sub.subjectName}</p>
                      {mathsBonus && (
                        <span className="text-[9px] font-medium text-zinc-400">+25</span>
                      )}
                    </div>
                    <p className="text-xs text-zinc-400">
                      {sub.grade} → {targetGrade}
                    </p>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200">{sub.points}</p>
                    {targetPoints !== sub.points && (
                      <p className="text-xs font-medium" style={{ color: targetPoints > sub.points ? '#2A7D6F' : undefined }}>
                        <span className={targetPoints < sub.points ? 'text-rose-500' : ''}>
                          {targetPoints > sub.points ? '+' : ''}{targetPoints - sub.points}
                        </span>
                      </p>
                    )}
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
                              ? 'text-white shadow-sm'
                              : isCurrent
                                ? 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 ring-1 ring-zinc-300 dark:ring-zinc-600'
                                : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                          }`}
                          style={isSelected ? { backgroundColor: '#2A7D6F' } : undefined}
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
                    <div key={gain.subjectName} className="flex items-center gap-3 py-2.5 border-b border-zinc-100 dark:border-zinc-800 last:border-b-0">
                      <span className="text-xs text-zinc-400 w-5 text-center">{idx + 1}</span>
                      <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200 flex-1">{gain.subjectName}</p>
                      <p className="text-xs text-zinc-400">
                        {gain.fromGrade} → {gain.toGrade}
                      </p>
                      <span className="text-xs font-medium" style={{ color: '#2A7D6F' }}>
                        +{gain.netGain} pts
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
