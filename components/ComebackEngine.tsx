/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useToast } from './Toast';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import {
  Rocket, ChevronRight, ChevronLeft, Trophy, TrendingUp, Zap, Target,
  CheckCircle, Circle, ArrowUpRight, Flame, Star, RotateCcw, Sparkles,
  GraduationCap, BookOpen, Wrench, DoorOpen, Compass,
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
import { type CAOCourse } from './futureFinderData';
import { useInnovationData } from '../contexts/InnovationDataContext';

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

type AnchorType = 'course' | 'apprenticeship' | 'plc' | 'options' | 'prove-them-wrong' | 'custom' | 'future-finder';

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
  trending?: 'up' | 'down' | 'stable';
}

interface ComebackEngineProps {
  uid: string;
  profile: StudentSubjectProfile;
}

// ── Constants ──────────────────────────────────────────────

const ANCHOR_OPTIONS: { type: AnchorType; label: string; icon: React.ElementType; prompt: string }[] = [
  { type: 'future-finder', icon: Compass, label: 'My Future Finder pick', prompt: '' },
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

function calculateQuickWins(subjects: StudentSubjectProfile['subjects'], mockTrends?: Record<string, 'up' | 'down' | 'stable'>): QuickWin[] {
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
        if (gradeIdx >= 5) effort = 'low';
        else if (gradeIdx <= 2) effort = 'high';

        const trending = mockTrends?.[s.subjectName];

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
          trending,
        });
      }
    }
  }

  // Sort: highest gain per effort first, but trending-down subjects get priority boost
  const effortWeight = { low: 3, medium: 2, high: 1 };
  const trendWeight = (t?: string) => t === 'down' ? 1.3 : t === 'up' ? 0.8 : 1;
  wins.sort((a, b) => (b.gain * effortWeight[b.effort] * trendWeight(b.trending)) - (a.gain * effortWeight[a.effort] * trendWeight(a.trending)));

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
  whatIfScenarios?: { subjectName: string; currentGrade: Grade; whatIfGrade: Grade; pointsGain: number }[],
  topicMastery?: Record<string, Record<string, { confidence: string }>>,
): WeeklyMission[] {
  const missions: WeeklyMission[] = [];
  const topWins = quickWins.slice(0, 3); // Focus on top 3 quickest wins
  const missionSubjects = new Set<string>();

  for (const win of topWins) {
    missionSubjects.add(win.subject);
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

  // Add missions from CAO Simulator what-if scenarios (subjects not already covered)
  if (whatIfScenarios && whatIfScenarios.length > 0) {
    const newWhatIfs = whatIfScenarios
      .filter(s => s.pointsGain > 0 && !missionSubjects.has(s.subjectName))
      .sort((a, b) => b.pointsGain - a.pointsGain)
      .slice(0, 2);
    for (const wif of newWhatIfs) {
      missionSubjects.add(wif.subjectName);
      missions.push({
        id: genId(),
        subject: wif.subjectName,
        action: `Focus session: work toward your ${wif.whatIfGrade} target in ${wif.subjectName}`,
        reason: `Your simulator shows ${wif.currentGrade} → ${wif.whatIfGrade} is worth +${wif.pointsGain} points`,
        pointsImpact: wif.pointsGain,
        done: false,
      });
    }
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

  // Add topic-specific missions from mastery data (War Room integration)
  if (topicMastery) {
    for (const win of topWins) {
      const subjectTopics = topicMastery[win.subject];
      if (!subjectTopics) continue;
      const shakyTopics = Object.entries(subjectTopics)
        .filter(([, t]) => t.confidence === 'shaky')
        .map(([name]) => name);
      if (shakyTopics.length > 0 && !missions.some(m => m.subject === win.subject && m.action.includes('weakest topic'))) {
        // Replace the generic "review weakest topic" mission with a specific one
        const idx = missions.findIndex(m => m.subject === win.subject && m.action.includes('weakest topic'));
        const specificTopic = shakyTopics[0];
        const newMission: WeeklyMission = {
          id: genId(),
          subject: win.subject,
          action: `Focus on "${specificTopic}" in ${win.subject} — it's marked as shaky`,
          reason: `${shakyTopics.length} topic${shakyTopics.length > 1 ? 's' : ''} still shaky in ${win.subject}`,
          pointsImpact: 0,
          done: false,
        };
        if (idx >= 0) {
          missions[idx] = newMission;
        } else if (missions.length < 7) {
          missions.push(newMission);
        }
      }
    }
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
  const { showToast } = useToast();
  const [comebackData, setComebackData] = useState<ComebackData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [phase, setPhase] = useState<'anchor' | 'gap' | 'wins' | 'plan' | 'progress'>('anchor');

  // Anchor form state
  const [selectedAnchor, setSelectedAnchor] = useState<AnchorType | null>(null);
  const [anchorText, setAnchorText] = useState('');
  const [customPoints, setCustomPoints] = useState('');

  // NorthStar integration
  const [northStar, setNorthStar] = useState<{ category: string; statement: string } | null>(null);

  // Computed points from CAO Simulator
  const [computedPoints, setComputedPoints] = useState<number | null>(null);

  // Future Finder integration (from shared context)
  const { futureFinderPicks: ffPicks } = useInnovationData();
  const [selectedFfPick, setSelectedFfPick] = useState<CAOCourse | null>(null);

  // CAO Simulator what-if scenarios
  const [whatIfScenarios, setWhatIfScenarios] = useState<{ subjectName: string; currentGrade: Grade; whatIfGrade: Grade; pointsGain: number }[]>([]);

  // Topic mastery data (War Room integration — Connection 2)
  const [topicMasteryData, setTopicMasteryData] = useState<Record<string, Record<string, { confidence: string }>>>({});

  // Timetable completions (Spaced Rep Timetable integration — Connection 3 & 5)
  const [timetableCompletions, setTimetableCompletions] = useState<Record<string, string[]>>({});

  const subjects = profile.subjects;
  const daysUntilExam = useMemo(() => {
    const exam = new Date(profile.examStartDate);
    return Math.max(0, Math.ceil((exam.getTime() - Date.now()) / 86400000));
  }, [profile.examStartDate]);

  const projectedPoints = useMemo(() => computeProjectedPoints(subjects), [subjects]);
  const maxRealisticPoints = useMemo(() => computeMaxRealisticPoints(subjects), [subjects]);

  // Compute mock trends: compare last two mocks per subject
  const { mockResults: mockResultsCtx, subjectPriorities } = useInnovationData();
  const mockTrends = useMemo(() => {
    const trends: Record<string, 'up' | 'down' | 'stable'> = {};
    for (const s of subjects) {
      const subjectMocks = mockResultsCtx.mocks
        .flatMap(m => m.entries.filter(e => e.subjectName === s.subjectName).map(e => ({ grade: e.grade, date: m.date })))
        .sort((a, b) => a.date.localeCompare(b.date));
      if (subjectMocks.length >= 2) {
        const prev = getGradeIndex(subjectMocks[subjectMocks.length - 2].grade as Grade);
        const latest = getGradeIndex(subjectMocks[subjectMocks.length - 1].grade as Grade);
        trends[s.subjectName] = latest < prev ? 'up' : latest > prev ? 'down' : 'stable';
      }
    }
    return trends;
  }, [subjects, mockResultsCtx.mocks]);

  const quickWins = useMemo(() => calculateQuickWins(subjects, mockTrends), [subjects, mockTrends]);

  // Load from Firestore
  useEffect(() => {
    if (!uid) return;
    let cancelled = false;
    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        if (cancelled) return;
        const data = snap.data();
        if (data?.comebackEngine) {
          setComebackData(data.comebackEngine);
          setPhase('progress');
        }
        // Load CAO Simulator what-if scenarios
        if (data?.caoSimulator?.whatIfScenarios?.length) {
          setWhatIfScenarios(data.caoSimulator.whatIfScenarios);
        }
        // Load NorthStar data
        if (data?.northStar?.statement) {
          setNorthStar({ category: data.northStar.category, statement: data.northStar.statement });
        }
        // Load computed points from CAO Simulator
        if (data?.computedPoints?.current) {
          setComputedPoints(data.computedPoints.current);
        }
        // Load topic mastery data (War Room integration)
        if (data?.topicMastery) {
          setTopicMasteryData(data.topicMastery);
        }
        // Load timetable completions (Spaced Rep Timetable integration)
        if (data?.timetableCompletions) {
          setTimetableCompletions(data.timetableCompletions);
        }
      } catch (e) {
        console.error('Failed to load Comeback Engine data:');
      }
      if (!cancelled) setIsLoading(false);
    };
    load();
    return () => { cancelled = true; };
  }, [uid]);

  const saveData = useCallback((data: ComebackData) => {
    setComebackData(data);
    setDoc(doc(db, 'progress', uid), { comebackEngine: data }, { merge: true })
      .catch(e => { console.error('Failed to save comeback data:'); showToast('Couldn\'t save — check your connection', 'error'); });
  }, [uid]);

  // ── Anchor Setup ───────────────────────────────────────

  const handleSetAnchor = () => {
    if (!selectedAnchor) return;

    let targetPts: number | null = null;
    if (selectedAnchor === 'future-finder' && selectedFfPick) {
      targetPts = selectedFfPick.typicalPoints;
    } else if (customPoints && !isNaN(Number(customPoints))) {
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

    const missions = generateMissions(quickWins, daysUntilExam, whatIfScenarios, topicMasteryData);
    const today = new Date().toISOString().split('T')[0];

    const anchorLabel = selectedAnchor === 'future-finder' && selectedFfPick
      ? `${selectedFfPick.title} (${selectedFfPick.institution})`
      : anchorText || ANCHOR_OPTIONS.find(a => a.type === selectedAnchor)?.label || '';

    const data: ComebackData = {
      anchor: anchorLabel,
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
    const missions = generateMissions(quickWins, daysUntilExam, whatIfScenarios, topicMasteryData);
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
      .catch(e => { console.error('Failed to reset comeback data:'); showToast('Couldn\'t save — check your connection', 'error'); });
  };

  // ── Derived values ─────────────────────────────────────

  const targetPoints = comebackData?.targetPoints ?? null;
  const gap = targetPoints !== null ? Math.max(0, targetPoints - projectedPoints) : null;
  const completedCount = comebackData?.weeklyMissions.filter(m => m.done).length ?? 0;
  const totalMissions = comebackData?.weeklyMissions.length ?? 0;

  // Progress since start
  const startingPoints = comebackData?.history?.[0]?.projectedPoints ?? projectedPoints;
  const pointsGained = projectedPoints - startingPoints;

  // Connection 3: Weekly timetable completion rate
  const weeklyCompletionRate = useMemo(() => {
    const now = new Date();
    let totalBlocks = 0;
    let completedBlocks = 0;
    for (let i = 0; i < 7; i++) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const key = d.toISOString().split('T')[0];
      const dayCompletions = timetableCompletions[key];
      if (dayCompletions) {
        completedBlocks += dayCompletions.length;
      }
      totalBlocks += 2; // assume ~2 blocks expected per day
    }
    if (totalBlocks === 0) return null;
    return Math.round((completedBlocks / totalBlocks) * 100);
  }, [timetableCompletions]);

  // Connection 5: Auto-completable missions based on timetable activity
  const autoCompletableMissions = useMemo(() => {
    if (!comebackData || Object.keys(timetableCompletions).length === 0) return new Set<string>();
    const today = new Date().toISOString().split('T')[0];
    const todayCompletions = timetableCompletions[today] || [];
    if (todayCompletions.length === 0) return new Set<string>();

    // Check if any incomplete missions match subjects studied today
    const ids = new Set<string>();
    for (const mission of comebackData.weeklyMissions) {
      if (mission.done) continue;
      // Check if today's completions include this mission's subject
      const subjectStudiedToday = todayCompletions.some(blockId =>
        blockId.toLowerCase().includes(mission.subject.toLowerCase())
      );
      if (subjectStudiedToday) {
        ids.add(mission.id);
      }
    }
    return ids;
  }, [comebackData, timetableCompletions]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-6 h-6 border-2 border-zinc-300 dark:border-zinc-600 rounded-full animate-spin" style={{ borderTopColor: '#2A7D6F' }} />
      </div>
    );
  }

  // ── Phase: Anchor ──────────────────────────────────────

  if (phase === 'anchor' && !comebackData) {
    return (
      <div className="space-y-6">
        {/* Intro */}
        <div className="text-center space-y-3 py-4">
          <div className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto bg-[#FAF7F4] dark:bg-zinc-900">
            <Rocket className="w-7 h-7" style={{ color: '#2A7D6F' }} />
          </div>
          <h2 className="text-xl font-bold text-zinc-800 dark:text-white">Let's be real for a second.</h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 max-w-md mx-auto leading-relaxed">
            Forget grades for a minute. Forget what anyone else thinks.
            What do <span className="font-semibold text-zinc-700 dark:text-zinc-300">you</span> actually want?
          </p>
          {northStar && (
            <div className="dark:border rounded-lg px-4 py-3 max-w-sm mx-auto bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(0,0,0,0.07)' }}>
              <p className="text-[10px] font-bold uppercase tracking-wider mb-1" style={{ color: '#2A7D6F' }}>Your North Star</p>
              <p className="text-sm italic" style={{ color: '#2A7D6F' }}>"{northStar.statement}"</p>
            </div>
          )}
        </div>

        {/* Anchor selection */}
        <div className="space-y-2">
          {ANCHOR_OPTIONS.map(opt => {
            const isFf = opt.type === 'future-finder';
            const ffDisabled = isFf && ffPicks.length === 0;
            return (
              <button
                key={opt.type}
                onClick={() => !ffDisabled && setSelectedAnchor(opt.type)}
                disabled={ffDisabled}
                className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl border text-left transition-all ${
                  ffDisabled
                    ? 'border-zinc-200 dark:border-zinc-700/50 bg-zinc-100 dark:bg-zinc-800/50 opacity-50 cursor-not-allowed'
                    : selectedAnchor === opt.type
                    ? 'shadow-sm bg-[#FAF7F4] dark:bg-zinc-900'
                    : 'border-zinc-200 dark:border-zinc-700/50 bg-white dark:bg-zinc-900 hover:border-zinc-300 dark:hover:border-zinc-600'
                }`}
                style={!ffDisabled && selectedAnchor === opt.type ? { borderColor: '#2A7D6F' } : undefined}
              >
                <opt.icon size={18} className={selectedAnchor === opt.type && !ffDisabled ? '' : 'text-zinc-400 dark:text-zinc-500'} style={selectedAnchor === opt.type && !ffDisabled ? { color: '#2A7D6F' } : undefined} />
                <div className="flex-1 min-w-0">
                  <span className={`text-sm font-semibold ${
                    selectedAnchor === opt.type && !ffDisabled ? '' : 'text-zinc-700 dark:text-zinc-300'
                  }`} style={selectedAnchor === opt.type && !ffDisabled ? { color: '#2A7D6F' } : undefined}>{opt.label}</span>
                  {ffDisabled && (
                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5">Complete Future Finder first</p>
                  )}
                </div>
                {selectedAnchor === opt.type && !ffDisabled && (
                  <CheckCircle size={16} className="ml-auto" style={{ color: '#2A7D6F' }} />
                )}
              </button>
            );
          })}
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
              {/* Future Finder picks dropdown */}
              {selectedAnchor === 'future-finder' && ffPicks.length > 0 && (
                <div className="space-y-2">
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">
                    Pick your target course
                  </label>
                  {ffPicks.map(course => (
                    <button
                      key={course.code}
                      onClick={() => {
                        setSelectedFfPick(course);
                        setAnchorText(`${course.title} (${course.institution})`);
                        setCustomPoints(String(course.typicalPoints));
                      }}
                      className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-all border ${
                        selectedFfPick?.code === course.code
                          ? 'bg-[#FAF7F4] dark:bg-zinc-900'
                          : 'bg-zinc-50 dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700'
                      }`}
                      style={selectedFfPick?.code === course.code ? { borderColor: '#2A7D6F' } : undefined}
                    >
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-semibold text-zinc-800 dark:text-zinc-200 truncate">{course.title}</p>
                        <p className="text-[10px] text-zinc-400 dark:text-zinc-500">{course.institution}</p>
                      </div>
                      <span className="text-xs font-bold text-zinc-600 dark:text-zinc-300 shrink-0">{course.typicalPoints} pts</span>
                      {selectedFfPick?.code === course.code && (
                        <CheckCircle size={14} className="shrink-0" style={{ color: '#2A7D6F' }} />
                      )}
                    </button>
                  ))}
                </div>
              )}

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
                    className="w-full mt-1 px-3 py-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none focus:border-[#2A7D6F] dark:focus:border-[#4DB8A4] transition-colors"
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
                    className="w-full mt-1 px-3 py-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none focus:border-[#2A7D6F] dark:focus:border-[#4DB8A4] transition-colors"
                  />
                </div>
              )}

              <button
                onClick={handleSetAnchor}
                disabled={selectedAnchor === 'future-finder' && !selectedFfPick}
                className="w-full py-3 rounded-xl text-sm font-bold text-white active:scale-[0.98] transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                style={{ backgroundColor: '#2A7D6F', boxShadow: '0 10px 15px -3px rgba(42,125,111,0.2)' }}
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
          {northStar && (
            <p className="text-xs text-zinc-500 dark:text-zinc-400 italic max-w-sm mx-auto">
              Remember: "{northStar.statement}"
            </p>
          )}
          <p className="text-xs text-zinc-400 dark:text-zinc-500">No judgement. Just the facts.</p>
        </div>

        {/* Current projection */}
        <div className="rounded-2xl p-5 text-center space-y-1 bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Your projected CAO points</p>
          <p className="text-5xl font-black" style={{ color: '#2A7D6F' }}>{projectedPoints}</p>
          <p className="text-xs text-zinc-400 dark:text-zinc-500">Based on your best 6 subjects right now</p>
        </div>

        {/* Target & gap */}
        {targetPoints !== null && gap !== null && (
          <div className="rounded-2xl p-5 text-center space-y-2 border"
            style={gap === 0
              ? { backgroundColor: '#EDF2EE', borderColor: '#6B8F71' }
              : { backgroundColor: '#FDF3E7', borderColor: '#C4873B' }
            }
          >
            {gap === 0 ? (
              <>
                <p className="text-sm font-bold" style={{ color: '#4A6B4F' }}>You're already there.</p>
                <p className="text-xs" style={{ color: '#6B8F71' }}>Your current grades already meet your target. Now it's about holding the line.</p>
              </>
            ) : (
              <>
                <p className="text-[10px] font-bold uppercase tracking-widest" style={{ color: '#C4873B' }}>The gap</p>
                <p className="text-4xl font-black" style={{ color: '#2A7D6F' }}>{gap} points</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">
                  You need <span className="font-bold">{targetPoints}</span> points.
                  That's <span className="font-bold">{gap}</span> to close.
                </p>
                {gap <= 50 && (
                  <p className="text-xs font-semibold pt-1" style={{ color: '#2A7D6F' }}>
                    That's smaller than you think. One or two grade jumps could close it.
                  </p>
                )}
                {gap > 50 && gap <= 120 && (
                  <p className="text-xs font-semibold pt-1" style={{ color: '#2A7D6F' }}>
                    That's doable. A few smart moves in the right subjects and you're there.
                  </p>
                )}
                {gap > 120 && (
                  <p className="text-xs font-semibold pt-1" style={{ color: '#2A7D6F' }}>
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
              That's <span className="font-bold" style={{ color: '#6B8F71' }}>+{maxRealisticPoints - projectedPoints} points</span>.
            </p>
          </div>
        )}

        <button
          onClick={() => setPhase('wins')}
          className="w-full py-3 rounded-xl text-sm font-bold text-white active:scale-[0.98] transition-all flex items-center justify-center gap-2"
          style={{ backgroundColor: '#2A7D6F', boxShadow: '0 10px 15px -3px rgba(42,125,111,0.2)' }}
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
                className="rounded-xl p-4 bg-[#FAF7F4] dark:bg-zinc-900"
                style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: '12px' }}
              >
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 text-white font-black text-sm" style={{ backgroundColor: hexColor }}>
                    {i + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-zinc-800 dark:text-white">{win.subject}</span>
                      <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full"
                        style={
                          win.effort === 'low' ? { backgroundColor: '#EDF2EE', color: '#4A6B4F' }
                            : win.effort === 'medium' ? { backgroundColor: '#FDF3E7', color: '#8B5E2A' }
                            : { backgroundColor: '#ECF5F3', color: '#1F5F54' }
                        }
                      >
                        {win.effort === 'low' ? 'Easiest' : win.effort === 'medium' ? 'Moderate' : 'Harder'}
                      </span>
                      {win.trending === 'up' && <TrendingUp size={13} style={{ color: '#276749' }} />}
                      {win.trending === 'down' && <TrendingUp size={13} style={{ color: '#DC2626', transform: 'scaleY(-1)' }} />}
                      {win.trending === 'stable' && <span className="text-[10px] text-[#A8A29E] dark:text-zinc-500">—</span>}
                    </div>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                      {win.currentGrade} → {win.targetGrade}
                    </p>
                  </div>
                  <div className="text-right shrink-0">
                    <p className="text-lg font-black" style={{ color: '#6B8F71' }}>+{win.gain}</p>
                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500">CAO pts</p>
                  </div>
                </div>
              </MotionDiv>
            );
          })}
        </div>

        {/* Total potential */}
        <div className="rounded-xl p-4 text-center" style={{ backgroundColor: '#EDF2EE', border: '0.5px solid rgba(107,143,113,0.3)' }}>
          <p className="text-xs" style={{ color: '#4A6B4F' }}>
            Just these {top5.length} moves alone could be worth up to <span className="font-black text-lg">+{totalPossible}</span> CAO points
          </p>
          <p className="text-[10px] mt-1" style={{ color: '#6B8F71' }}>
            {projectedPoints} → {projectedPoints + totalPossible} projected
          </p>
        </div>

        <button
          onClick={() => setPhase('plan')}
          className="w-full py-3 rounded-xl text-sm font-bold text-white active:scale-[0.98] transition-all flex items-center justify-center gap-2"
          style={{ backgroundColor: '#2A7D6F', boxShadow: '0 10px 15px -3px rgba(42,125,111,0.2)' }}
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
                className={`w-full flex items-start gap-3 px-4 py-3.5 rounded-xl border text-left transition-all ${m.done ? '' : 'bg-[#FAF7F4] dark:bg-zinc-900'}`}
                style={m.done
                  ? { backgroundColor: '#EDF2EE', borderColor: 'rgba(107,143,113,0.3)' }
                  : { border: '0.5px solid rgba(0,0,0,0.07)' }
                }
              >
                <div className="mt-0.5 shrink-0">
                  {m.done ? (
                    <CheckCircle size={18} style={{ color: '#6B8F71' }} />
                  ) : (
                    <Circle size={18} className="text-[#9A9590] dark:text-zinc-500" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-semibold ${m.done ? 'line-through' : 'text-zinc-700 dark:text-zinc-300'}`} style={m.done ? { color: '#4A6B4F' } : undefined}>
                    {m.action}
                    {!m.done && autoCompletableMissions.has(m.id) && (
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full ml-1" style={{ color: '#4A6B4F', backgroundColor: '#EDF2EE' }}>
                        studied today
                      </span>
                    )}
                  </p>
                  <p className="text-[11px] text-zinc-400 dark:text-zinc-500 mt-0.5">
                    {m.reason}
                    {(() => {
                      const priority = subjectPriorities.find(p => p.subjectName === m.subject);
                      if (!priority) return null;
                      const label = priority.sessions >= 3 ? 'High' : priority.sessions >= 2 ? 'Med' : 'Low';
                      const color = label === 'High' ? '#C4873B' : label === 'Med' ? '#2A7D6F' : '#A8A29E';
                      return <span className="ml-1.5 text-[9px] font-bold" style={{ color }}>{label} priority</span>;
                    })()}
                  </p>
                </div>
                {m.pointsImpact > 0 && (
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full shrink-0" style={{ color: '#4A6B4F', backgroundColor: '#EDF2EE' }}>
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
          <div className="h-2 rounded-full overflow-hidden bg-[#9A9590] dark:bg-zinc-700">
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{ width: `${totalMissions > 0 ? (completedCount / totalMissions) * 100 : 0}%`, backgroundColor: '#2A7D6F' }}
            />
          </div>
        </div>

        {completedCount === totalMissions && totalMissions > 0 && (
          <MotionDiv
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="rounded-xl p-4 text-center space-y-2 border bg-[#FAF7F4] dark:bg-zinc-900"
            style={{ borderColor: 'rgba(42,125,111,0.3)' }}
          >
            <Flame className="w-8 h-8 mx-auto" style={{ color: '#2A7D6F' }} />
            <p className="text-sm font-bold" style={{ color: '#2A7D6F' }}>All missions complete. Comeback is happening.</p>
            <button
              onClick={() => { handleNewWeek(); }}
              className="px-4 py-2 rounded-lg text-xs font-bold text-white transition-colors"
              style={{ backgroundColor: '#2A7D6F' }}
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
        <div className="rounded-xl p-4 text-center bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: '12px' }}>
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Projected</p>
          <p className="text-3xl font-black" style={{ color: '#2A7D6F' }}>{projectedPoints}</p>
          <p className="text-[10px] text-zinc-400 dark:text-zinc-500">CAO points</p>
        </div>
        {targetPoints !== null && gap !== null ? (
          <div className={`border rounded-xl p-4 text-center ${gap === 0 ? '' : 'bg-[#FAF7F4] dark:bg-zinc-900'}`}
            style={gap === 0
              ? { backgroundColor: '#EDF2EE', borderColor: '#6B8F71', borderRadius: '12px' }
              : { borderColor: 'rgba(196,135,59,0.3)', borderRadius: '12px' }
            }
          >
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
              {gap === 0 ? 'Status' : 'Gap to close'}
            </p>
            <p className="text-3xl font-black"
              style={gap === 0 ? { color: '#6B8F71' } : { color: '#C4873B' }}
            >
              {gap === 0 ? <CheckCircle size={28} className="mx-auto" style={{ color: '#6B8F71' }} /> : gap}
            </p>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
              {gap === 0 ? 'On target' : `Need ${targetPoints}`}
            </p>
          </div>
        ) : (
          <div className="rounded-xl p-4 text-center bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: '12px' }}>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Potential</p>
            <p className="text-3xl font-black" style={{ color: '#6B8F71' }}>{maxRealisticPoints}</p>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500">If each up 1 grade</p>
          </div>
        )}
      </div>

      {/* Momentum indicator */}
      {comebackData && comebackData.history.length > 1 && (
        <div className={`rounded-xl p-4 text-center border ${pointsGained === 0 ? 'bg-[#FAF7F4] dark:bg-zinc-900' : ''}`}
          style={pointsGained > 0
            ? { backgroundColor: '#EDF2EE', borderColor: 'rgba(107,143,113,0.3)' }
            : pointsGained === 0
            ? { borderColor: 'rgba(0,0,0,0.07)' }
            : { backgroundColor: '#ECF5F3', borderColor: 'rgba(42,125,111,0.3)' }
          }
        >
          <div className="flex items-center justify-center gap-2">
            {pointsGained > 0 ? (
              <TrendingUp size={18} style={{ color: '#6B8F71' }} />
            ) : pointsGained === 0 ? (
              <Target size={18} className="text-[#9A9590] dark:text-zinc-500" />
            ) : (
              <TrendingUp size={18} className="rotate-180" style={{ color: '#B85C4A' }} />
            )}
            <span className={`text-sm font-bold ${pointsGained === 0 ? 'text-[#9A9590] dark:text-zinc-500' : ''}`}
              style={pointsGained > 0
                ? { color: '#4A6B4F' }
                : pointsGained === 0
                ? undefined
                : { color: '#B85C4A' }
              }
            >
              {pointsGained > 0 ? `+${pointsGained} points since you started`
                : pointsGained === 0 ? 'Holding steady — keep going'
                : `${pointsGained} points — time to refocus`}
            </span>
          </div>
        </div>
      )}

      {/* Timetable completion rate (Connection 3: Spaced Rep → Comeback Engine) */}
      {weeklyCompletionRate !== null && weeklyCompletionRate < 50 && (
        <div className="rounded-xl p-4 text-center space-y-1 border" style={{ backgroundColor: '#FDF3E7', borderColor: 'rgba(196,135,59,0.3)' }}>
          <p className="text-xs font-bold" style={{ color: '#8B5E2A' }}>
            {weeklyCompletionRate}% timetable completion this week
          </p>
          <p className="text-[10px]" style={{ color: '#C4873B' }}>
            {weeklyCompletionRate === 0
              ? "You haven't hit any timetable blocks this week. Start with just one today."
              : "Try completing just one more block per day — small wins compound."}
          </p>
        </div>
      )}

      {/* The Anchor — their goal */}
      {comebackData && (
        <div className="rounded-xl p-4 bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: '12px' }}>
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1">Your anchor</p>
          <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
            {comebackData.anchor}
          </p>
        </div>
      )}

      {/* NorthStar motivation connector */}
      {northStar && (
        <div className="rounded-xl p-4 space-y-2 border bg-[#FAF7F4] dark:bg-zinc-900" style={{ borderColor: 'rgba(42,125,111,0.2)' }}>
          <p className="text-[10px] font-bold uppercase tracking-widest" style={{ color: '#2A7D6F' }}>Your Why</p>
          <p className="text-sm font-semibold italic" style={{ color: '#2A7D6F' }}>"{northStar.statement}"</p>
          {targetPoints !== null && gap !== null && gap > 0 && (
            <p className="text-xs" style={{ color: '#2A7D6F' }}>
              {gap <= 30
                ? `You're so close — just ${gap} points from making this real.`
                : gap <= 80
                ? `${gap} points to go. A few focused weeks could change everything.`
                : `${gap} points to close. Every session gets you closer to this.`
              }
            </p>
          )}
          {targetPoints !== null && gap !== null && gap === 0 && (
            <p className="text-xs font-medium" style={{ color: '#6B8F71' }}>
              You're on track to make this happen. Keep going.
            </p>
          )}
        </div>
      )}

      {/* Quick wins summary */}
      <div className="space-y-2">
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Quickest wins</p>
        {quickWins.slice(0, 3).map((win, i) => {
          const hexColor = getDistinctSubjectHex(win.subject, i);
          return (
            <div key={win.subject} className="flex items-center gap-3 px-4 py-2.5 rounded-xl bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: '12px' }}>
              <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: hexColor }} />
              <span className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 flex-1">{win.subject}</span>
              <span className="text-xs text-zinc-400 dark:text-zinc-500">{win.currentGrade} → {win.targetGrade}</span>
              <span className="text-xs font-bold" style={{ color: '#6B8F71' }}>+{win.gain}</span>
            </div>
          );
        })}
      </div>

      {/* Weekly missions */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">This week's missions</p>
          <span className="text-xs font-bold" style={{ color: '#2A7D6F' }}>{completedCount}/{totalMissions}</span>
        </div>
        {comebackData?.weeklyMissions.map(m => (
          <button
            key={m.id}
            onClick={() => handleToggleMission(m.id)}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg border text-left transition-all ${m.done ? '' : 'bg-[#FAF7F4] dark:bg-zinc-900'}`}
            style={m.done
              ? { backgroundColor: '#EDF2EE', borderColor: 'rgba(107,143,113,0.3)' }
              : { border: '0.5px solid rgba(0,0,0,0.07)' }
            }
          >
            {m.done ? (
              <CheckCircle size={14} className="shrink-0" style={{ color: '#6B8F71' }} />
            ) : (
              <Circle size={14} className="shrink-0 text-[#9A9590] dark:text-zinc-500" />
            )}
            <span className={`text-xs font-medium flex-1 ${m.done ? 'line-through' : 'text-zinc-600 dark:text-zinc-400'}`} style={m.done ? { color: '#4A6B4F' } : undefined}>
              {m.action}
              {!m.done && autoCompletableMissions.has(m.id) && (
                <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full ml-1" style={{ color: '#4A6B4F', backgroundColor: '#EDF2EE' }}>
                  studied today
                </span>
              )}
            </span>
          </button>
        ))}
        {completedCount === totalMissions && totalMissions > 0 && (
          <button
            onClick={handleNewWeek}
            className="w-full py-2 rounded-lg text-xs font-bold transition-colors border bg-[#FAF7F4] dark:bg-zinc-900"
            style={{ color: '#2A7D6F', borderColor: 'rgba(42,125,111,0.3)' }}
          >
            Generate next week's missions
          </button>
        )}
      </div>

      {/* Days remaining */}
      <div className="text-center py-2">
        <p className="text-xs text-zinc-400 dark:text-zinc-500">
          <span className="font-bold" style={{ color: '#2A7D6F' }}>{daysUntilExam}</span> days until exam — every day counts
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
