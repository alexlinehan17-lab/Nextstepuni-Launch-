/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Rocket, ChevronRight, ChevronLeft, Trophy, TrendingUp, Zap, Target,
  CheckCircle, Circle, ArrowUpRight, Flame, Star, RotateCcw, Sparkles,
  GraduationCap, BookOpen, Wrench, DoorOpen,
} from 'lucide-react';
import { db } from '../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import {
  type StudentSubjectProfile, type Grade, type Level,
  getPointsForGrade, getGradeIndex, getGradesForLevel,
  HIGHER_GRADES, ORDINARY_GRADES, HIGHER_POINTS, ORDINARY_POINTS,
  LC_SUBJECTS,
} from './subjectData';
import { getDistinctSubjectHex } from '../studySessionData';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

// ── Types ──────────────────────────────────────────────────

interface ComebackData {
  anchor: string;           // Their real-life goal text
  anchorType: AnchorType;
  targetPoints: number | null; // CAO/PLC points they need (null = "just want options")
  weeklyMissions: WeeklyMission[];
  weekStartDate: string;    // ISO date of current plan week start
  completedMissions: string[]; // mission IDs completed this cycle
  history: ProgressSnapshot[];
}

type AnchorType = 'course' | 'apprenticeship' | 'plc' | 'options' | 'prove-them-wrong' | 'custom';

interface WeeklyMission {
  id: string;
  subject: string;
  action: string;
  reason: string;
  pointsImpact: number; // potential CAO points gained
  done: boolean;
}

interface ProgressSnapshot {
  date: string;
  projectedPoints: number;
}

interface QuickWin {
  subject: string;
  currentGrade: Grade;
  targetGrade: Grade; // one realistic step up
  currentPoints: number;
  newPoints: number;
  gain: number;
  effort: 'low' | 'medium' | 'high';
  isMaths: boolean;
  level: Level;
}

interface ComebackEngineProps {
  uid: string;
  profile: StudentSubjectProfile;
}

// ── Constants ──────────────────────────────────────────────

const ANCHOR_OPTIONS: { type: AnchorType; label: string; icon: React.ElementType; prompt: string }[] = [
  { type: 'course', icon: GraduationCap, label: 'A specific course', prompt: 'What course? (We\'ll figure out the points)' },
  { type: 'plc', icon: BookOpen, label: 'A PLC / Further Ed course', prompt: 'Which PLC or area?' },
  { type: 'apprenticeship', icon: Wrench, label: 'An apprenticeship or trade', prompt: 'What trade or area?' },
  { type: 'options', icon: DoorOpen, label: 'I just want options', prompt: '' },
  { type: 'prove-them-wrong', icon: Flame, label: 'Prove someone wrong', prompt: '' },
  { type: 'custom', icon: Sparkles, label: 'Something else', prompt: 'What\'s your goal?' },
];

// Common PLC/apprenticeship thresholds — not exact, but good motivational targets
const POINTS_THRESHOLDS: Record<string, number> = {
  'plc-general': 200,
  'apprenticeship': 200,
  'options-decent': 300,
  'options-good': 350,
};

function genId(): string {
  return Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
}

// ── Quickest Wins Calculator ───────────────────────────────

function getOneGradeUp(grade: Grade): Grade | null {
  const idx = getGradeIndex(grade);
  if (idx <= 0) return null; // already at top
  if (grade.startsWith('H')) return HIGHER_GRADES[idx - 1];
  return ORDINARY_GRADES[idx - 1];
}

function getTwoGradesUp(grade: Grade): Grade | null {
  const idx = getGradeIndex(grade);
  if (idx <= 1) return getOneGradeUp(grade);
  if (grade.startsWith('H')) return HIGHER_GRADES[idx - 2];
  return ORDINARY_GRADES[idx - 2];
}

function calculateQuickWins(subjects: StudentSubjectProfile['subjects']): QuickWin[] {
  const wins: QuickWin[] = [];

  for (const s of subjects) {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths || false;
    const currentPts = getPointsForGrade(s.currentGrade, isMaths);
    const gradeIdx = getGradeIndex(s.currentGrade);

    // Try one grade up
    const oneUp = getOneGradeUp(s.currentGrade);
    if (oneUp) {
      const newPts = getPointsForGrade(oneUp, isMaths);
      const gain = newPts - currentPts;
      if (gain > 0) {
        // Effort estimation: bottom grades are easier to improve
        let effort: QuickWin['effort'] = 'medium';
        if (gradeIdx >= 5) effort = 'low';     // H6/H7/O6/O7 → easiest to improve
        else if (gradeIdx <= 2) effort = 'high'; // H1/H2/H3 → hard to improve further

        wins.push({
          subject: s.subjectName,
          currentGrade: s.currentGrade,
          targetGrade: oneUp,
          currentPoints: currentPts,
          newPoints: newPts,
          gain,
          effort,
          isMaths,
          level: s.level,
        });
      }
    }
  }

  // Sort: highest gain per effort first
  const effortWeight = { low: 3, medium: 2, high: 1 };
  wins.sort((a, b) => (b.gain * effortWeight[b.effort]) - (a.gain * effortWeight[a.effort]));

  return wins;
}

function computeProjectedPoints(subjects: StudentSubjectProfile['subjects']): number {
  // Best 6 subjects by points (standard CAO calculation)
  const allPoints = subjects.map(s => {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths || false;
    return getPointsForGrade(s.currentGrade, isMaths);
  }).sort((a, b) => b - a);

  return allPoints.slice(0, 6).reduce((sum, p) => sum + p, 0);
}

function computeMaxRealisticPoints(subjects: StudentSubjectProfile['subjects']): number {
  // If each subject improved by 1 grade
  const allPoints = subjects.map(s => {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths || false;
    const oneUp = getOneGradeUp(s.currentGrade);
    const grade = oneUp || s.currentGrade;
    return getPointsForGrade(grade, isMaths);
  }).sort((a, b) => b - a);

  return allPoints.slice(0, 6).reduce((sum, p) => sum + p, 0);
}

// ── Generate Weekly Missions ───────────────────────────────

function generateMissions(
  quickWins: QuickWin[],
  daysUntilExam: number,
): WeeklyMission[] {
  const missions: WeeklyMission[] = [];
  const topWins = quickWins.slice(0, 3); // Focus on top 3 quickest wins

  for (const win of topWins) {
    // Study mission
    missions.push({
      id: genId(),
      subject: win.subject,
      action: `Do one ${win.level === 'higher' ? 'HL' : 'OL'} ${win.subject} past paper question`,
      reason: `Going ${win.currentGrade} → ${win.targetGrade} is worth +${win.gain} CAO points`,
      pointsImpact: win.gain,
      done: false,
    });
  }

  // Add a general mission based on biggest win
  if (topWins.length > 0) {
    const biggest = topWins[0];
    missions.push({
      id: genId(),
      subject: biggest.subject,
      action: `Spend 20 minutes reviewing your weakest topic in ${biggest.subject}`,
      reason: `${biggest.subject} has the highest return on your time right now`,
      pointsImpact: 0,
      done: false,
    });
  }

  // Add one mindset mission
  if (daysUntilExam > 30) {
    missions.push({
      id: genId(),
      subject: 'General',
      action: 'Write down one reason you want to do better — keep it somewhere you can see it',
      reason: 'Students who write their goals down are 42% more likely to achieve them',
      pointsImpact: 0,
      done: false,
    });
  }

  return missions;
}

// ── Main Component ─────────────────────────────────────────

const ComebackEngine: React.FC<ComebackEngineProps> = ({ uid, profile }) => {
  const [comebackData, setComebackData] = useState<ComebackData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [phase, setPhase] = useState<'anchor' | 'gap' | 'wins' | 'plan' | 'progress'>('anchor');

  // Anchor form state
  const [selectedAnchor, setSelectedAnchor] = useState<AnchorType | null>(null);
  const [anchorText, setAnchorText] = useState('');
  const [customPoints, setCustomPoints] = useState('');

  const subjects = profile.subjects;
  const daysUntilExam = useMemo(() => {
    const exam = new Date(profile.examStartDate);
    return Math.max(0, Math.ceil((exam.getTime() - Date.now()) / 86400000));
  }, [profile.examStartDate]);

  const projectedPoints = useMemo(() => computeProjectedPoints(subjects), [subjects]);
  const maxRealisticPoints = useMemo(() => computeMaxRealisticPoints(subjects), [subjects]);
  const quickWins = useMemo(() => calculateQuickWins(subjects), [subjects]);

  // Load from Firestore
  useEffect(() => {
    if (!uid) return;
    (async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        const data = snap.data();
        if (data?.comebackEngine) {
          setComebackData(data.comebackEngine);
          setPhase('progress');
        }
      } catch (e) {
        console.error('Failed to load Comeback Engine data:', e);
      }
      setIsLoading(false);
    })();
  }, [uid]);

  const saveData = useCallback((data: ComebackData) => {
    setComebackData(data);
    setDoc(doc(db, 'progress', uid), { comebackEngine: data }, { merge: true })
      .catch(e => console.error('Failed to save comeback data:', e));
  }, [uid]);

  // ── Anchor Setup ───────────────────────────────────────

  const handleSetAnchor = () => {
    if (!selectedAnchor) return;

    let targetPts: number | null = null;
    if (customPoints && !isNaN(Number(customPoints))) {
      targetPts = Number(customPoints);
    } else if (selectedAnchor === 'course') {
      targetPts = Number(customPoints) || null;
    } else if (selectedAnchor === 'plc' || selectedAnchor === 'apprenticeship') {
      targetPts = POINTS_THRESHOLDS['plc-general'];
    } else if (selectedAnchor === 'options') {
      targetPts = POINTS_THRESHOLDS['options-decent'];
    } else if (selectedAnchor === 'prove-them-wrong') {
      targetPts = null;
    }

    const missions = generateMissions(quickWins, daysUntilExam);
    const today = new Date().toISOString().split('T')[0];

    const data: ComebackData = {
      anchor: anchorText || ANCHOR_OPTIONS.find(a => a.type === selectedAnchor)?.label || '',
      anchorType: selectedAnchor,
      targetPoints: targetPts,
      weeklyMissions: missions,
      weekStartDate: today,
      completedMissions: [],
      history: [{ date: today, projectedPoints }],
    };

    saveData(data);
    setPhase('gap');
  };

  const handleToggleMission = (missionId: string) => {
    if (!comebackData) return;
    const updated = { ...comebackData };
    const mission = updated.weeklyMissions.find(m => m.id === missionId);
    if (mission) {
      mission.done = !mission.done;
      if (mission.done && !updated.completedMissions.includes(missionId)) {
        updated.completedMissions.push(missionId);
      } else if (!mission.done) {
        updated.completedMissions = updated.completedMissions.filter(id => id !== missionId);
      }
    }
    saveData(updated);
  };

  const handleNewWeek = () => {
    if (!comebackData) return;
    const missions = generateMissions(quickWins, daysUntilExam);
    const today = new Date().toISOString().split('T')[0];
    const updated: ComebackData = {
      ...comebackData,
      weeklyMissions: missions,
      weekStartDate: today,
      completedMissions: [],
      history: [...comebackData.history, { date: today, projectedPoints }],
    };
    saveData(updated);
  };

  const handleReset = () => {
    setComebackData(null);
    setPhase('anchor');
    setSelectedAnchor(null);
    setAnchorText('');
    setCustomPoints('');
    setDoc(doc(db, 'progress', uid), { comebackEngine: null }, { merge: true })
      .catch(e => console.error('Failed to reset comeback data:', e));
  };

  // ── Derived values ─────────────────────────────────────

  const targetPoints = comebackData?.targetPoints ?? null;
  const gap = targetPoints !== null ? Math.max(0, targetPoints - projectedPoints) : null;
  const completedCount = comebackData?.weeklyMissions.filter(m => m.done).length ?? 0;
  const totalMissions = comebackData?.weeklyMissions.length ?? 0;

  // Progress since start
  const startingPoints = comebackData?.history?.[0]?.projectedPoints ?? projectedPoints;
  const pointsGained = projectedPoints - startingPoints;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-6 h-6 border-2 border-zinc-300 dark:border-zinc-600 border-t-orange-500 rounded-full animate-spin" />
      </div>
    );
  }

  // ── Phase: Anchor ──────────────────────────────────────

  if (phase === 'anchor' && !comebackData) {
    return (
      <div className="space-y-6">
        {/* Intro */}
        <div className="text-center space-y-3 py-4">
          <div className="w-14 h-14 rounded-2xl bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center mx-auto">
            <Rocket className="w-7 h-7 text-orange-600 dark:text-orange-400" />
          </div>
          <h2 className="text-xl font-bold text-zinc-800 dark:text-white">Let's be real for a second.</h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 max-w-md mx-auto leading-relaxed">
            Forget grades for a minute. Forget what anyone else thinks.
            What do <span className="font-semibold text-zinc-700 dark:text-zinc-300">you</span> actually want?
          </p>
        </div>

        {/* Anchor selection */}
        <div className="space-y-2">
          {ANCHOR_OPTIONS.map(opt => (
            <button
              key={opt.type}
              onClick={() => setSelectedAnchor(opt.type)}
              className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl border text-left transition-all ${
                selectedAnchor === opt.type
                  ? 'border-orange-400 dark:border-orange-500 bg-orange-50 dark:bg-orange-900/20 shadow-sm'
                  : 'border-zinc-200 dark:border-zinc-700/50 bg-white dark:bg-zinc-900 hover:border-zinc-300 dark:hover:border-zinc-600'
              }`}
            >
              <opt.icon size={18} className={selectedAnchor === opt.type ? 'text-orange-500' : 'text-zinc-400 dark:text-zinc-500'} />
              <span className={`text-sm font-semibold ${
                selectedAnchor === opt.type ? 'text-orange-700 dark:text-orange-300' : 'text-zinc-700 dark:text-zinc-300'
              }`}>{opt.label}</span>
              {selectedAnchor === opt.type && (
                <CheckCircle size={16} className="ml-auto text-orange-500" />
              )}
            </button>
          ))}
        </div>

        {/* Follow-up input */}
        <AnimatePresence>
          {selectedAnchor && (
            <MotionDiv
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden space-y-3"
            >
              {/* Text input for goal */}
              {(selectedAnchor === 'course' || selectedAnchor === 'plc' || selectedAnchor === 'apprenticeship' || selectedAnchor === 'custom') && (
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">
                    {ANCHOR_OPTIONS.find(a => a.type === selectedAnchor)?.prompt}
                  </label>
                  <input
                    type="text"
                    value={anchorText}
                    onChange={e => setAnchorText(e.target.value)}
                    placeholder="Type here..."
                    maxLength={100}
                    className="w-full mt-1 px-3 py-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none focus:border-orange-400 dark:focus:border-orange-500 transition-colors"
                  />
                </div>
              )}

              {/* Points input for course */}
              {selectedAnchor === 'course' && (
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">
                    CAO points needed (if you know — leave blank if not)
                  </label>
                  <input
                    type="number"
                    value={customPoints}
                    onChange={e => setCustomPoints(e.target.value)}
                    placeholder="e.g. 350"
                    min={0}
                    max={625}
                    className="w-full mt-1 px-3 py-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none focus:border-orange-400 dark:focus:border-orange-500 transition-colors"
                  />
                </div>
              )}

              <button
                onClick={handleSetAnchor}
                className="w-full py-3 rounded-xl text-sm font-bold bg-orange-500 hover:bg-orange-600 text-white shadow-lg shadow-orange-500/20 active:scale-[0.98] transition-all"
              >
                Show me what's possible
              </button>
            </MotionDiv>
          )}
        </AnimatePresence>
      </div>
    );
  }

  // ── Phase: Gap ─────────────────────────────────────────

  if (phase === 'gap') {
    return (
      <div className="space-y-6">
        <div className="text-center space-y-2 py-2">
          <h2 className="text-lg font-bold text-zinc-800 dark:text-white">Here's where you stand.</h2>
          <p className="text-xs text-zinc-400 dark:text-zinc-500">No judgement. Just the facts.</p>
        </div>

        {/* Current projection */}
        <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-5 text-center space-y-1">
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Your projected CAO points</p>
          <p className="text-5xl font-black text-zinc-800 dark:text-white">{projectedPoints}</p>
          <p className="text-xs text-zinc-400 dark:text-zinc-500">Based on your best 6 subjects right now</p>
        </div>

        {/* Target & gap */}
        {targetPoints !== null && gap !== null && (
          <div className={`rounded-2xl p-5 text-center space-y-2 ${
            gap === 0
              ? 'bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800/40'
              : 'bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800/40'
          }`}>
            {gap === 0 ? (
              <>
                <p className="text-sm font-bold text-emerald-700 dark:text-emerald-300">You're already there.</p>
                <p className="text-xs text-emerald-600 dark:text-emerald-400">Your current grades already meet your target. Now it's about holding the line.</p>
              </>
            ) : (
              <>
                <p className="text-[10px] font-bold uppercase tracking-widest text-orange-500 dark:text-orange-400">The gap</p>
                <p className="text-4xl font-black text-orange-600 dark:text-orange-400">{gap} points</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">
                  You need <span className="font-bold">{targetPoints}</span> points.
                  That's <span className="font-bold">{gap}</span> to close.
                </p>
                {gap <= 50 && (
                  <p className="text-xs font-semibold text-orange-700 dark:text-orange-300 pt-1">
                    That's smaller than you think. One or two grade jumps could close it.
                  </p>
                )}
                {gap > 50 && gap <= 120 && (
                  <p className="text-xs font-semibold text-orange-700 dark:text-orange-300 pt-1">
                    That's doable. A few smart moves in the right subjects and you're there.
                  </p>
                )}
                {gap > 120 && (
                  <p className="text-xs font-semibold text-orange-700 dark:text-orange-300 pt-1">
                    It's a stretch — but every single point you close matters. Let's find your quickest wins.
                  </p>
                )}
              </>
            )}
          </div>
        )}

        {/* No target set — show what's possible */}
        {targetPoints === null && (
          <div className="bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700/50 rounded-2xl p-5 text-center space-y-2">
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">What's realistically possible</p>
            <p className="text-3xl font-black text-zinc-800 dark:text-white">{projectedPoints} → {maxRealisticPoints}</p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              If you improve each subject by just one grade, you go from {projectedPoints} to {maxRealisticPoints}.
              That's <span className="font-bold text-emerald-600 dark:text-emerald-400">+{maxRealisticPoints - projectedPoints} points</span>.
            </p>
          </div>
        )}

        <button
          onClick={() => setPhase('wins')}
          className="w-full py-3 rounded-xl text-sm font-bold bg-orange-500 hover:bg-orange-600 text-white shadow-lg shadow-orange-500/20 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
        >
          Show me the quickest wins <ChevronRight size={16} />
        </button>
      </div>
    );
  }

  // ── Phase: Quickest Wins ───────────────────────────────

  if (phase === 'wins') {
    const top5 = quickWins.slice(0, 5);
    const totalPossible = top5.reduce((sum, w) => sum + w.gain, 0);

    return (
      <div className="space-y-5">
        <div className="space-y-1">
          <button onClick={() => setPhase('gap')} className="flex items-center gap-1 text-xs font-bold text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors">
            <ChevronLeft size={14} /> Back
          </button>
          <h2 className="text-lg font-bold text-zinc-800 dark:text-white">Your quickest wins</h2>
          <p className="text-xs text-zinc-400 dark:text-zinc-500">
            These are the subjects where the smallest effort gives you the biggest jump.
          </p>
        </div>

        <div className="space-y-3">
          {top5.map((win, i) => {
            const hexColor = getDistinctSubjectHex(win.subject, i);
            return (
              <MotionDiv
                key={win.subject}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
                className="bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06] rounded-xl p-4"
              >
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 text-white font-black text-sm" style={{ backgroundColor: hexColor }}>
                    {i + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-zinc-800 dark:text-white">{win.subject}</span>
                      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-full ${
                        win.effort === 'low' ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400'
                          : win.effort === 'medium' ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400'
                          : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                      }`}>
                        {win.effort === 'low' ? 'Easiest' : win.effort === 'medium' ? 'Moderate' : 'Harder'}
                      </span>
                    </div>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                      {win.currentGrade} → {win.targetGrade}
                    </p>
                  </div>
                  <div className="text-right shrink-0">
                    <p className="text-lg font-black text-emerald-600 dark:text-emerald-400">+{win.gain}</p>
                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500">CAO pts</p>
                  </div>
                </div>
              </MotionDiv>
            );
          })}
        </div>

        {/* Total potential */}
        <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800/40 rounded-xl p-4 text-center">
          <p className="text-xs text-emerald-600 dark:text-emerald-400">
            Just these {top5.length} moves alone could be worth up to <span className="font-black text-lg">+{totalPossible}</span> CAO points
          </p>
          <p className="text-[10px] text-emerald-500 dark:text-emerald-500 mt-1">
            {projectedPoints} → {projectedPoints + totalPossible} projected
          </p>
        </div>

        <button
          onClick={() => setPhase('plan')}
          className="w-full py-3 rounded-xl text-sm font-bold bg-orange-500 hover:bg-orange-600 text-white shadow-lg shadow-orange-500/20 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
        >
          Give me a plan <ChevronRight size={16} />
        </button>
      </div>
    );
  }

  // ── Phase: Plan (30-Day / Weekly Missions) ─────────────

  if (phase === 'plan') {
    return (
      <div className="space-y-5">
        <div className="space-y-1">
          <button onClick={() => setPhase('wins')} className="flex items-center gap-1 text-xs font-bold text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors">
            <ChevronLeft size={14} /> Back
          </button>
          <h2 className="text-lg font-bold text-zinc-800 dark:text-white">This week's missions</h2>
          <p className="text-xs text-zinc-400 dark:text-zinc-500">
            Not a full year plan. Just this week. Tick them off as you go.
          </p>
        </div>

        {/* Missions */}
        <div className="space-y-2">
          {comebackData?.weeklyMissions.map((m, i) => (
            <MotionDiv
              key={m.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.06 }}
            >
              <button
                onClick={() => handleToggleMission(m.id)}
                className={`w-full flex items-start gap-3 px-4 py-3.5 rounded-xl border text-left transition-all ${
                  m.done
                    ? 'bg-emerald-50 dark:bg-emerald-900/10 border-emerald-200 dark:border-emerald-800/30'
                    : 'bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700'
                }`}
              >
                <div className="mt-0.5 shrink-0">
                  {m.done ? (
                    <CheckCircle size={18} className="text-emerald-500" />
                  ) : (
                    <Circle size={18} className="text-zinc-300 dark:text-zinc-600" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-semibold ${m.done ? 'text-emerald-700 dark:text-emerald-400 line-through' : 'text-zinc-700 dark:text-zinc-300'}`}>
                    {m.action}
                  </p>
                  <p className="text-[11px] text-zinc-400 dark:text-zinc-500 mt-0.5">{m.reason}</p>
                </div>
                {m.pointsImpact > 0 && (
                  <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/30 px-2 py-0.5 rounded-full shrink-0">
                    +{m.pointsImpact} pts
                  </span>
                )}
              </button>
            </MotionDiv>
          ))}
        </div>

        {/* Progress bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
            <span>This week</span>
            <span>{completedCount}/{totalMissions} done</span>
          </div>
          <div className="h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-orange-500 rounded-full transition-all duration-500"
              style={{ width: `${totalMissions > 0 ? (completedCount / totalMissions) * 100 : 0}%` }}
            />
          </div>
        </div>

        {completedCount === totalMissions && totalMissions > 0 && (
          <MotionDiv
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800/40 rounded-xl p-4 text-center space-y-2"
          >
            <Flame className="w-8 h-8 text-orange-500 mx-auto" />
            <p className="text-sm font-bold text-orange-700 dark:text-orange-300">All missions complete. Comeback is happening.</p>
            <button
              onClick={() => { handleNewWeek(); }}
              className="px-4 py-2 rounded-lg text-xs font-bold bg-orange-500 text-white hover:bg-orange-600 transition-colors"
            >
              Generate next week's missions
            </button>
          </MotionDiv>
        )}

        <button
          onClick={() => setPhase('progress')}
          className="w-full py-3 rounded-xl text-sm font-bold bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-700 dark:text-zinc-300 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
        >
          See overall progress <ChevronRight size={16} />
        </button>
      </div>
    );
  }

  // ── Phase: Progress (Overview Dashboard) ───────────────

  return (
    <div className="space-y-5">
      {/* Top stats row */}
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06] rounded-xl p-4 text-center">
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Projected</p>
          <p className="text-3xl font-black text-zinc-800 dark:text-white">{projectedPoints}</p>
          <p className="text-[10px] text-zinc-400 dark:text-zinc-500">CAO points</p>
        </div>
        {targetPoints !== null && gap !== null ? (
          <div className={`border rounded-xl p-4 text-center ${
            gap === 0
              ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800/40'
              : 'bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800/40'
          }`}>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
              {gap === 0 ? 'Status' : 'Gap to close'}
            </p>
            <p className={`text-3xl font-black ${
              gap === 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-orange-600 dark:text-orange-400'
            }`}>
              {gap === 0 ? <CheckCircle size={28} className="mx-auto" /> : gap}
            </p>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
              {gap === 0 ? 'On target' : `Need ${targetPoints}`}
            </p>
          </div>
        ) : (
          <div className="bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700/50 rounded-xl p-4 text-center">
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Potential</p>
            <p className="text-3xl font-black text-emerald-600 dark:text-emerald-400">{maxRealisticPoints}</p>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500">If each up 1 grade</p>
          </div>
        )}
      </div>

      {/* Momentum indicator */}
      {comebackData && comebackData.history.length > 1 && (
        <div className={`rounded-xl p-4 text-center border ${
          pointsGained > 0
            ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800/40'
            : pointsGained === 0
            ? 'bg-zinc-50 dark:bg-zinc-800/50 border-zinc-200 dark:border-zinc-700/50'
            : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800/40'
        }`}>
          <div className="flex items-center justify-center gap-2">
            {pointsGained > 0 ? (
              <TrendingUp size={18} className="text-emerald-500" />
            ) : pointsGained === 0 ? (
              <Target size={18} className="text-zinc-400" />
            ) : (
              <TrendingUp size={18} className="text-red-500 rotate-180" />
            )}
            <span className={`text-sm font-bold ${
              pointsGained > 0 ? 'text-emerald-700 dark:text-emerald-300'
                : pointsGained === 0 ? 'text-zinc-600 dark:text-zinc-400'
                : 'text-red-700 dark:text-red-300'
            }`}>
              {pointsGained > 0 ? `+${pointsGained} points since you started`
                : pointsGained === 0 ? 'Holding steady — keep going'
                : `${pointsGained} points — time to refocus`}
            </span>
          </div>
        </div>
      )}

      {/* The Anchor — their goal */}
      {comebackData && (
        <div className="bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06] rounded-xl p-4">
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1">Your anchor</p>
          <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
            {comebackData.anchor}
          </p>
        </div>
      )}

      {/* Quick wins summary */}
      <div className="space-y-2">
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Quickest wins</p>
        {quickWins.slice(0, 3).map((win, i) => {
          const hexColor = getDistinctSubjectHex(win.subject, i);
          return (
            <div key={win.subject} className="flex items-center gap-3 px-4 py-2.5 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06]">
              <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: hexColor }} />
              <span className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 flex-1">{win.subject}</span>
              <span className="text-xs text-zinc-400 dark:text-zinc-500">{win.currentGrade} → {win.targetGrade}</span>
              <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400">+{win.gain}</span>
            </div>
          );
        })}
      </div>

      {/* Weekly missions */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">This week's missions</p>
          <span className="text-xs font-bold text-orange-500">{completedCount}/{totalMissions}</span>
        </div>
        {comebackData?.weeklyMissions.map(m => (
          <button
            key={m.id}
            onClick={() => handleToggleMission(m.id)}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg border text-left transition-all ${
              m.done
                ? 'bg-emerald-50/50 dark:bg-emerald-900/10 border-emerald-200/50 dark:border-emerald-800/20'
                : 'bg-white dark:bg-zinc-900 border-zinc-200/60 dark:border-white/[0.06]'
            }`}
          >
            {m.done ? (
              <CheckCircle size={14} className="text-emerald-500 shrink-0" />
            ) : (
              <Circle size={14} className="text-zinc-300 dark:text-zinc-600 shrink-0" />
            )}
            <span className={`text-xs font-medium flex-1 ${m.done ? 'text-emerald-600 dark:text-emerald-400 line-through' : 'text-zinc-600 dark:text-zinc-400'}`}>
              {m.action}
            </span>
          </button>
        ))}
        {completedCount === totalMissions && totalMissions > 0 && (
          <button
            onClick={handleNewWeek}
            className="w-full py-2 rounded-lg text-xs font-bold text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800/40 hover:bg-orange-100 dark:hover:bg-orange-900/30 transition-colors"
          >
            Generate next week's missions
          </button>
        )}
      </div>

      {/* Days remaining */}
      <div className="text-center py-2">
        <p className="text-xs text-zinc-400 dark:text-zinc-500">
          <span className="font-bold text-zinc-600 dark:text-zinc-300">{daysUntilExam}</span> days until exam — every day counts
        </p>
      </div>

      {/* Reset */}
      <button
        onClick={handleReset}
        className="flex items-center gap-1.5 mx-auto text-[10px] font-bold text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
      >
        <RotateCcw size={10} /> Start over
      </button>
    </div>
  );
};

export default ComebackEngine;
