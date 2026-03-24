/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo } from 'react';
import { useToast } from './Toast';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Clock, Map, TrendingUp, Target, Plus, X, ChevronDown,
  AlertTriangle, CheckCircle, Minus, Activity, BookOpen, Shield,
} from 'lucide-react';
import { db } from '../firebase';
import { doc, getDoc } from 'firebase/firestore';
import {
  type StudentSubjectProfile, type Grade, type TimetableCompletions,
  getPointsForGrade, getGradeIndex, getGradesForLevel,
  HIGHER_GRADES, ORDINARY_GRADES, LC_SUBJECTS,
} from './subjectData';
import {
  computeSubjectPriorities, allocateSessions, computeWeeksUntilExam,
} from './timetableAlgorithm';
import { getSubjectColor, getSubjectStroke, SUBJECT_STROKE_COLORS, getDistinctSubjectHex } from '../studySessionData';
import { getSubjectGuidance, type SubjectGuidance } from './subjectGuidance';
import { getSyllabusTopics } from './syllabusTopics';
import { getSyllabusForSubject, getQuadrant, QUADRANT_LABELS, computeEfficiency } from './syllabusData';
import { type DebriefEntry } from './StudyDebrief';
import { type StudySessionRecord } from '../studySessionData';
import { type CAOCourse, hydrateCourses } from './futureFinderData';
import { useTopicMastery } from '../hooks/useTopicMastery';
import { useMockResults } from '../hooks/useMockResults';
import { type TopicMasteryEntry, type UnifiedConfidence } from '../types';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

// ── Types ──────────────────────────────────────────────────

interface TopicEntry {
  id: string;
  name: string;
  confidence: 'solid' | 'shaky' | 'not-started';
  updatedAt: number;
}

type TopicMap = Record<string, TopicEntry[]>;

interface MockResult {
  id: string;
  subject: string;
  grade: string;
  date: string;
  label?: string;
  timestamp: number;
}

interface WarRoomProps {
  uid: string;
  profile: StudentSubjectProfile;
  timetableCompletions: TimetableCompletions;
}

// ── Helpers ────────────────────────────────────────────────

function genId(): string {
  return Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
}

// ── Design System Styles ────────────────────────────────────
// Light: warm cream #FAF7F4, Dark: rgba(255,255,255,0.04)
// We use a CSS custom property set on the root for dark mode toggling.
// For inline hex colors, we apply light mode by default.
const CARD_STYLE: React.CSSProperties = {
  backgroundColor: '#FAF7F4',
  border: '0.5px solid rgba(0,0,0,0.07)',
  borderRadius: 12,
};
const CARD_CLASS = 'dark:!bg-[rgba(255,255,255,0.04)] dark:!border-[rgba(255,255,255,0.08)]';

const CONFIDENCE_COLORS = {
  'solid': 'bg-emerald-500 dark:bg-emerald-600',
  'shaky': 'bg-amber-400 dark:bg-amber-500',
  'not-started': 'bg-zinc-300 dark:bg-zinc-600',
} as const;

const CONFIDENCE_TEXT_COLORS = {
  'solid': 'text-emerald-700 dark:text-emerald-300',
  'shaky': 'text-amber-700 dark:text-amber-300',
  'not-started': 'text-zinc-500 dark:text-zinc-400',
} as const;

const CONFIDENCE_LABELS: Record<string, string> = {
  'solid': 'Solid',
  'shaky': 'Shaky',
  'not-started': 'Not Started',
};

const CONFIDENCE_CYCLE: Record<string, TopicEntry['confidence']> = {
  'not-started': 'shaky',
  'shaky': 'solid',
  'solid': 'not-started',
};

const PANEL_TABS = [
  { id: 0, label: 'Countdown', icon: Clock },
  { id: 1, label: 'Coverage', icon: Map },
  { id: 2, label: 'Trajectory', icon: TrendingUp },
  { id: 3, label: 'Briefing', icon: Target },
] as const;

function gradeToPoints(grade: string | undefined | null): number {
  if (!grade || typeof grade !== 'string') return 0;
  if (grade.startsWith('H')) return getPointsForGrade(grade as Grade, false);
  if (grade.startsWith('O')) return getPointsForGrade(grade as Grade, false);
  return 0;
}

function computeCurrentTotal(subjects: StudentSubjectProfile['subjects']): number {
  const all = subjects.map(s => {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths ?? false;
    return getPointsForGrade(s.currentGrade as Grade, isMaths);
  }).sort((a, b) => b - a);
  return all.slice(0, 6).reduce((sum, p) => sum + p, 0);
}

// ── Main Component ─────────────────────────────────────────

const WarRoom: React.FC<WarRoomProps> = ({ uid, profile, timetableCompletions }) => {
  const { showToast } = useToast();
  const [activePanel, setActivePanel] = useState(0);
  const [studySessions, setStudySessions] = useState<StudySessionRecord[]>([]);
  const [debriefs, setDebriefs] = useState<DebriefEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [targetCourse, setTargetCourse] = useState<CAOCourse | null>(null);

  // Shared hooks for topic mastery and mock results
  const topicMastery = useTopicMastery(uid);
  const mockResultsHook = useMockResults(uid);

  // Derive a TopicMap from unified mastery for legacy sub-components that still expect TopicMap
  const derivedTopicMap: TopicMap = useMemo(() => {
    const map: TopicMap = {};
    for (const [subject, topics] of Object.entries(topicMastery.mastery)) {
      map[subject] = Object.entries(topics).map(([name, entry]) => ({
        id: `${subject}-${name}`,
        name,
        confidence: entry.confidence as TopicEntry['confidence'],
        updatedAt: entry.updatedAt,
      }));
    }
    return map;
  }, [topicMastery.mastery]);

  // Derive legacy MockResult[] from unified mock results for sub-components
  const derivedMockResults: MockResult[] = useMemo(() => {
    const results: MockResult[] = [];
    for (const mock of mockResultsHook.mocks) {
      for (const entry of mock.entries) {
        results.push({
          id: `${mock.id}-${entry.subjectName}`,
          subject: entry.subjectName,
          grade: entry.grade,
          date: mock.date,
          label: mock.label,
          timestamp: mock.timestamp,
        });
      }
    }
    return results;
  }, [mockResultsHook.mocks]);

  // Load remaining data from Firestore (study sessions, debriefs, future finder)
  useEffect(() => {
    if (!uid) return;
    let cancelled = false;
    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        if (cancelled) return;
        const data = snap.data() || {};
        if (data.studySessions) {
          setStudySessions(data.studySessions as StudySessionRecord[]);
        }
        if (data.studyDebriefs) {
          setDebriefs(data.studyDebriefs as DebriefEntry[]);
        }
        // Load Future Finder top pick for target course banner
        if (data.futureFinder?.topPicks) {
          const hydrated = hydrateCourses(data.futureFinder.topPicks);
          if (hydrated.length > 0) setTargetCourse(hydrated[0]);
        }
      } catch (e) {
        console.error('Failed to load War Room data:', e);
      }
      if (!cancelled) setIsLoading(false);
    };
    load();
    return () => { cancelled = true; };
  }, [uid]);

  // Shared computations
  const subjects = profile.subjects;
  const daysUntilExam = useMemo(() => {
    const examDate = new Date(profile.examStartDate);
    return Math.max(0, Math.ceil((examDate.getTime() - Date.now()) / 86400000));
  }, [profile.examStartDate]);

  const weeksUntilExam = useMemo(() => computeWeeksUntilExam(profile.examStartDate), [profile.examStartDate]);
  const blockDuration = profile.defaultBlockDuration ?? 45;

  const allocations = useMemo(() => {
    const priorities = computeSubjectPriorities(subjects);
    return allocateSessions(priorities, weeksUntilExam);
  }, [subjects, weeksUntilExam]);

  // Hours studied per subject from study sessions
  const hoursStudiedMap = useMemo(() => {
    const map: Record<string, number> = {};
    for (const s of studySessions) {
      map[s.subject] = (map[s.subject] || 0) + s.actualSeconds / 3600;
    }
    // Also count timetable completions as approximate study time
    for (const [, blockIds] of Object.entries(timetableCompletions)) {
      for (const blockId of blockIds) {
        const parts = blockId.split('|');
        const subjectName = parts[0];
        if (subjectName) {
          map[subjectName] = (map[subjectName] || 0) + blockDuration / 60;
        }
      }
    }
    return map;
  }, [studySessions, timetableCompletions, blockDuration]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-6 h-6 border-2 border-zinc-300 dark:border-zinc-600 border-t-[var(--accent-hex)] rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Panel tabs */}
      <div className="flex gap-1 bg-zinc-100 dark:bg-zinc-800/50 rounded-xl p-1">
        {PANEL_TABS.map(tab => {
          const Icon = tab.icon;
          const isActive = activePanel === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActivePanel(tab.id)}
              className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm'
                  : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
              }`}
            >
              <Icon size={14} />
              <span className="hidden sm:inline">{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Panel content */}
      <AnimatePresence mode="wait">
        <MotionDiv
          key={activePanel}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.2 }}
        >
          {activePanel === 0 && (
            <CountdownPanel
              daysUntilExam={daysUntilExam}
              subjects={subjects}
              allocations={allocations}
              weeksUntilExam={weeksUntilExam}
              hoursStudiedMap={hoursStudiedMap}
              blockDuration={blockDuration}
              mockResults={derivedMockResults}
              targetCourse={targetCourse}
              currentPoints={computeCurrentTotal(subjects)}
            />
          )}
          {activePanel === 1 && (
            <CoveragePanel
              subjects={subjects}
              topicMastery={topicMastery}
              debriefs={debriefs}
            />
          )}
          {activePanel === 2 && (
            <TrajectoryPanel
              subjects={subjects}
              mockResults={derivedMockResults}
              mockResultsHook={mockResultsHook}
              daysUntilExam={daysUntilExam}
            />
          )}
          {activePanel === 3 && (
            <BriefingPanel
              subjects={subjects}
              topicMap={derivedTopicMap}
              mockResults={derivedMockResults}
              allocations={allocations}
              hoursStudiedMap={hoursStudiedMap}
              weeksUntilExam={weeksUntilExam}
              blockDuration={blockDuration}
              daysUntilExam={daysUntilExam}
              timetableCompletions={timetableCompletions}
            />
          )}
        </MotionDiv>
      </AnimatePresence>
    </div>
  );
};

// ── Panel 0: Countdown & Time Budget ───────────────────────

interface CountdownPanelProps {
  daysUntilExam: number;
  subjects: StudentSubjectProfile['subjects'];
  allocations: { subjectName: string; sessions: number }[];
  weeksUntilExam: number;
  hoursStudiedMap: Record<string, number>;
  blockDuration: number;
  mockResults: MockResult[];
  targetCourse?: CAOCourse | null;
  currentPoints?: number;
}

const CountdownPanel: React.FC<CountdownPanelProps> = ({ daysUntilExam, subjects, allocations, weeksUntilExam, hoursStudiedMap, blockDuration, mockResults, targetCourse, currentPoints }) => {
  // Derive effective current grade from latest mock results (falls back to profile)
  const latestGradeMap = useMemo(() => {
    const map: Record<string, string> = {};
    const sorted = [...mockResults].filter(r => r.grade && r.date).sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
    for (const r of sorted) {
      map[r.subject] = r.grade; // last one wins (sorted ascending)
    }
    return map;
  }, [mockResults]);

  const subjectBudgets = useMemo(() => {
    return subjects.map(s => {
      const alloc = allocations.find(a => a.subjectName === s.subjectName);
      const sessionsPerWeek = alloc?.sessions ?? 1;
      const hoursRemaining = (sessionsPerWeek * weeksUntilExam * blockDuration) / 60;
      const hoursStudied = hoursStudiedMap[s.subjectName] || 0;
      const totalHours = hoursStudied + hoursRemaining;
      const pct = totalHours > 0 ? Math.min(100, Math.round((hoursStudied / totalHours) * 100)) : 0;
      const latestGrade = latestGradeMap[s.subjectName];
      const targetPts = gradeToPoints(s.targetGrade);
      const currentPts = latestGrade ? gradeToPoints(latestGrade) : gradeToPoints(s.currentGrade);
      const gap = targetPts - currentPts;
      return {
        subjectName: s.subjectName, hoursStudied, hoursRemaining, totalHours, pct,
        latestGrade: latestGrade || s.currentGrade, targetGrade: s.targetGrade, gap, sessionsPerWeek,
      };
    });
  }, [subjects, allocations, weeksUntilExam, hoursStudiedMap, blockDuration, latestGradeMap]);

  const totalStudied = subjectBudgets.reduce((sum, s) => sum + s.hoursStudied, 0);
  const totalRemaining = subjectBudgets.reduce((sum, s) => sum + s.hoursRemaining, 0);

  return (
    <div className="space-y-6">
      {/* Hero countdown */}
      <div className={`text-center py-8 backdrop-blur-2xl ${CARD_CLASS}`} style={CARD_STYLE}>
        <motion.p
          className="text-6xl font-bold tabular-nums"
          style={{ color: '#2A7D6F' }}
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        >
          {daysUntilExam}
        </motion.p>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1 font-medium">days until exams</p>
        <div className="flex items-center justify-center gap-4 mt-4 text-xs text-zinc-400 dark:text-zinc-500">
          <span>{Math.round(totalStudied)}h studied</span>
          <span className="w-1 h-1 rounded-full bg-zinc-300 dark:bg-zinc-600" />
          <span>~{Math.round(totalRemaining)}h remaining</span>
        </div>
      </div>

      {/* Target Course banner (from Future Finder) */}
      {targetCourse && currentPoints !== undefined && (
        <div className={`px-4 py-3.5 ${CARD_CLASS}`} style={CARD_STYLE}>
          <div className="flex items-center justify-between">
            <div className="min-w-0">
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-0.5">Target Course</p>
              <p className="text-sm font-semibold truncate" style={{ color: '#2A7D6F' }}>{targetCourse.title}</p>
              <p className="text-[10px] text-zinc-500 dark:text-zinc-400">{targetCourse.institution} &middot; {targetCourse.typicalPoints} pts required</p>
            </div>
            <div className="text-right shrink-0 ml-3">
              {currentPoints >= targetCourse.typicalPoints ? (
                <span className="text-xs font-bold px-2.5 py-1 rounded-full" style={{ backgroundColor: 'rgba(107,143,113,0.12)', color: '#6B8F71' }}>On target</span>
              ) : (
                <span className="text-xs font-bold px-2.5 py-1 rounded-full" style={{ backgroundColor: '#FDF3E7', color: '#8B5E2A' }}>
                  {targetCourse.typicalPoints - currentPoints}pt gap
                </span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Per-subject status — time budget + grade status */}
      <div className="space-y-3">
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Subject Status</p>
        {[...subjectBudgets].sort((a, b) => b.gap - a.gap).map(s => {
          const color = getSubjectColor(s.subjectName);
          return (
            <div key={s.subjectName} className={`px-4 py-3 ${CARD_CLASS}`} style={CARD_STYLE}>
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <div className={`w-2.5 h-2.5 rounded-full ${color.dot} shrink-0`} />
                  <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">{s.subjectName}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-zinc-400 dark:text-zinc-500">{s.latestGrade} → {s.targetGrade}</span>
                  {s.gap <= 0 ? (
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full" style={{ backgroundColor: 'rgba(107,143,113,0.12)', color: '#6B8F71' }}>On target</span>
                  ) : (
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full" style={{ backgroundColor: '#FDF3E7', color: '#8B5E2A' }}>{s.gap}pt gap</span>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="flex-1 h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: '#EDEAE6' }}>
                  <motion.div
                    className="h-full rounded-full"
                    style={{ backgroundColor: '#2A7D6F' }}
                    initial={{ width: 0 }}
                    animate={{ width: `${s.pct}%` }}
                    transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                  />
                </div>
                <span className="text-[10px] text-zinc-400 dark:text-zinc-500 tabular-nums w-20 text-right">
                  {Math.round(s.hoursStudied)}h / {Math.round(s.totalHours)}h
                </span>
              </div>
              <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1">{s.sessionsPerWeek} session{s.sessionsPerWeek !== 1 ? 's' : ''}/week</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ── Panel 1: Subject Coverage Map ──────────────────────────

interface CoveragePanelProps {
  subjects: StudentSubjectProfile['subjects'];
  topicMastery: ReturnType<typeof useTopicMastery>;
  debriefs?: DebriefEntry[];
}

const CoveragePanel: React.FC<CoveragePanelProps> = ({ subjects, topicMastery, debriefs }) => {
  const [selectedSubject, setSelectedSubject] = useState(subjects[0]?.subjectName ?? '');
  const [newTopicName, setNewTopicName] = useState('');

  // Auto-import syllabus topics when subject changes
  useEffect(() => {
    if (selectedSubject) {
      topicMastery.importSyllabusTopics(selectedSubject);
    }
  }, [selectedSubject]);

  // Derive TopicEntry[] from the unified mastery for the selected subject
  const topics: TopicEntry[] = useMemo(() => {
    const subjectTopics = topicMastery.getSubjectTopics(selectedSubject);
    return Object.entries(subjectTopics).map(([name, entry]) => ({
      id: `${selectedSubject}-${name}`,
      name,
      confidence: entry.confidence as TopicEntry['confidence'],
      updatedAt: entry.updatedAt,
    }));
  }, [topicMastery, selectedSubject]);

  const addTopic = () => {
    const trimmed = newTopicName.trim();
    if (!trimmed || trimmed.length < 2) return;
    topicMastery.setTopicConfidence(selectedSubject, trimmed, 'not-started', 'manual');
    setNewTopicName('');
  };

  const cycleConfidence = (topicName: string) => {
    const current = topicMastery.getTopicConfidence(selectedSubject, topicName);
    const next = CONFIDENCE_CYCLE[current] as UnifiedConfidence;
    topicMastery.setTopicConfidence(selectedSubject, topicName, next, 'manual');
  };

  const removeTopic = (_topicName: string) => {
    // The unified hook doesn't support removal, so set to not-started as equivalent
    // (topics from syllabus should stay; this is a no-op effectively)
    topicMastery.setTopicConfidence(selectedSubject, _topicName, 'not-started', 'manual');
  };

  // Syllabus suggestions (enriched with SXR data)
  const syllabusTopics = getSyllabusTopics(selectedSubject);
  const syllabusData = getSyllabusForSubject(selectedSubject);
  const existingNames = new Set(topics.map(t => t.name.toLowerCase()));
  const unaddedSyllabus = syllabusTopics.filter(t => !existingNames.has(t.toLowerCase()));

  // Sort unadded syllabus by quadrant priority
  const QUADRANT_ORDER: Record<string, number> = { 'start-here': 0, 'high-value': 1, 'worth-knowing': 2, 'only-if-time': 3 };
  const sortedUnaddedSyllabus = useMemo(() => {
    if (!syllabusData) return unaddedSyllabus;
    return [...unaddedSyllabus].sort((a, b) => {
      const topicA = syllabusData.topics.find(t => t.name === a);
      const topicB = syllabusData.topics.find(t => t.name === b);
      if (!topicA || !topicB) return 0;
      return (QUADRANT_ORDER[getQuadrant(topicA)] ?? 3) - (QUADRANT_ORDER[getQuadrant(topicB)] ?? 3);
    });
  }, [unaddedSyllabus, syllabusData]);

  // Debrief-seeded topics: unique hardestTopic entries for this subject not already in topicMap
  const debriefTopics = useMemo(() => {
    if (!debriefs || debriefs.length === 0) return [];
    const seen = new Set<string>();
    const result: string[] = [];
    for (const d of debriefs) {
      if (d.subject !== selectedSubject) continue;
      if (!d.hardestTopic || d.hardestTopic === 'Not specified') continue;
      const key = d.hardestTopic.toLowerCase();
      if (existingNames.has(key) || seen.has(key)) continue;
      seen.add(key);
      result.push(d.hardestTopic);
    }
    return result;
  }, [debriefs, selectedSubject, existingNames]);

  const addDebriefTopics = (topicNames: string[]) => {
    for (const name of topicNames) {
      topicMastery.setTopicConfidence(selectedSubject, name, 'shaky', 'debrief');
    }
  };

  const addSyllabusTopics = (topicNames: string[]) => {
    for (const name of topicNames) {
      topicMastery.setTopicConfidence(selectedSubject, name, 'not-started', 'import');
    }
  };

  // Build a derived topicMap for all subjects (for stats and heatmap)
  const topicMap: TopicMap = useMemo(() => {
    const map: TopicMap = {};
    for (const s of subjects) {
      const subjectTopics = topicMastery.getSubjectTopics(s.subjectName);
      map[s.subjectName] = Object.entries(subjectTopics).map(([name, entry]) => ({
        id: `${s.subjectName}-${name}`,
        name,
        confidence: entry.confidence as TopicEntry['confidence'],
        updatedAt: entry.updatedAt,
      }));
    }
    return map;
  }, [subjects, topicMastery]);

  // Coverage stats for all subjects
  const allSubjectStats = useMemo(() => {
    return subjects.map(s => {
      const t = topicMap[s.subjectName] || [];
      const total = t.length;
      const solid = t.filter(x => x.confidence === 'solid').length;
      const shaky = t.filter(x => x.confidence === 'shaky').length;
      const notStarted = t.filter(x => x.confidence === 'not-started').length;
      const pct = total > 0 ? Math.round(((solid + shaky * 0.5) / total) * 100) : 0;
      return { subjectName: s.subjectName, total, solid, shaky, notStarted, pct };
    });
  }, [subjects, topicMap]);

  const currentStats = allSubjectStats.find(s => s.subjectName === selectedSubject);

  return (
    <div className="space-y-5">
      {/* Subject selector */}
      <div className="flex flex-wrap gap-2">
        {subjects.map(s => {
          const color = getSubjectColor(s.subjectName);
          const isActive = selectedSubject === s.subjectName;
          const stats = allSubjectStats.find(x => x.subjectName === s.subjectName);
          return (
            <button
              key={s.subjectName}
              onClick={() => setSelectedSubject(s.subjectName)}
              className={`inline-flex items-center gap-1.5 px-3 py-2 rounded-full text-[12px] font-semibold transition-all ${
                isActive
                  ? `${color.bg} ${color.text} ring-1 ring-inset ${color.border}`
                  : 'bg-white dark:bg-zinc-900 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
              }`}
            >
              <span className={`w-2 h-2 rounded-full ${color.dot}`} />
              {s.subjectName}
              {stats && stats.total > 0 && (
                <span className="text-[10px] opacity-60">{stats.pct}%</span>
              )}
            </button>
          );
        })}
      </div>

      {/* Add topic */}
      <div className="flex gap-2">
        <input
          type="text"
          value={newTopicName}
          onChange={(e) => setNewTopicName(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && addTopic()}
          placeholder="Add a topic..."
          maxLength={60}
          className="flex-1 px-4 py-2.5 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none focus:ring-2 focus:ring-[rgba(var(--accent),0.3)]"
        />
        <button
          onClick={addTopic}
          disabled={newTopicName.trim().length < 2}
          className="px-4 py-2.5 text-white text-sm font-bold disabled:opacity-40 hover:shadow-md active:scale-[0.97] transition-all"
          style={{ backgroundColor: '#2A7D6F', borderRadius: 12 }}
        >
          <Plus size={16} />
        </button>
      </div>

      {/* Summary stats */}
      {currentStats && currentStats.total > 0 && (
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
            <span className="text-zinc-500 dark:text-zinc-400">{currentStats.solid} solid</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400" />
            <span className="text-zinc-500 dark:text-zinc-400">{currentStats.shaky} shaky</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-zinc-300 dark:bg-zinc-600" />
            <span className="text-zinc-500 dark:text-zinc-400">{currentStats.notStarted} not started</span>
          </span>
          <span className="ml-auto font-bold" style={{ color: '#2A7D6F' }}>{currentStats.pct}% covered</span>
        </div>
      )}

      {/* Topic grid */}
      {topics.length > 0 ? (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {topics.map(topic => (
              <div
                key={topic.id}
                className={`group relative p-3 cursor-pointer hover:shadow-sm transition-all ${CARD_CLASS}`}
                style={CARD_STYLE}
                onClick={() => cycleConfidence(topic.name)}
              >
                <div className="flex items-start gap-2">
                  <div className={`w-3 h-3 rounded-full mt-0.5 shrink-0 ${CONFIDENCE_COLORS[topic.confidence]}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 truncate">{topic.name}</p>
                    <p className={`text-[10px] font-medium ${CONFIDENCE_TEXT_COLORS[topic.confidence]}`}>
                      {CONFIDENCE_LABELS[topic.confidence]}
                    </p>
                  </div>
                </div>
                <button
                  onClick={(e) => { e.stopPropagation(); removeTopic(topic.name); }}
                  className="absolute top-1 right-1 w-5 h-5 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 text-zinc-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 transition-all"
                >
                  <X size={10} />
                </button>
              </div>
            ))}
          </div>
          {/* Debrief-seeded topic suggestions */}
          {debriefTopics.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <p className="text-[10px] font-bold uppercase tracking-widest text-amber-500 dark:text-amber-400">From Your Debriefs</p>
                <button
                  onClick={() => addDebriefTopics(debriefTopics)}
                  className="text-[10px] font-bold text-amber-600 dark:text-amber-400 hover:underline"
                >
                  Add all ({debriefTopics.length})
                </button>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {debriefTopics.map(name => (
                  <button
                    key={name}
                    onClick={() => addDebriefTopics([name])}
                    className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-900/15 border border-dashed border-amber-300 dark:border-amber-700/50 hover:border-amber-500 text-[10px] font-medium text-amber-700 dark:text-amber-400 transition-colors"
                  >
                    <AlertTriangle size={9} className="shrink-0" />
                    {name}
                  </button>
                ))}
              </div>
            </div>
          )}
          {/* Show remaining syllabus topics as suggestions */}
          {sortedUnaddedSyllabus.length > 0 && (
            <button
              onClick={() => addSyllabusTopics(sortedUnaddedSyllabus)}
              className="w-full flex items-center justify-center gap-2 py-2 rounded-lg border border-dashed border-zinc-300 dark:border-zinc-700 text-[10px] font-semibold text-zinc-400 dark:text-zinc-500 hover:border-[var(--accent-hex)] hover:text-[var(--accent-hex)] transition-colors"
            >
              <Plus size={10} />
              Add {sortedUnaddedSyllabus.length} remaining syllabus topic{sortedUnaddedSyllabus.length > 1 ? 's' : ''}
            </button>
          )}
        </>
      ) : sortedUnaddedSyllabus.length > 0 || debriefTopics.length > 0 ? (
        /* Topic suggestions when no topics exist */
        <div className="space-y-4">
          {/* Debrief topics */}
          {debriefTopics.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <p className="text-[10px] font-bold uppercase tracking-widest text-amber-500 dark:text-amber-400">From Your Debriefs</p>
                <button
                  onClick={() => addDebriefTopics(debriefTopics)}
                  className="text-[10px] font-bold text-amber-600 dark:text-amber-400 hover:underline"
                >
                  Add all ({debriefTopics.length})
                </button>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {debriefTopics.map(name => (
                  <button
                    key={name}
                    onClick={() => addDebriefTopics([name])}
                    className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-900/15 border border-dashed border-amber-300 dark:border-amber-700/50 hover:border-amber-500 text-[10px] font-medium text-amber-700 dark:text-amber-400 transition-colors"
                  >
                    <AlertTriangle size={9} className="shrink-0" />
                    {name}
                  </button>
                ))}
              </div>
            </div>
          )}
          {/* Syllabus topics with quadrant info */}
          {sortedUnaddedSyllabus.length > 0 && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Syllabus Topics</p>
                <button
                  onClick={() => addSyllabusTopics(sortedUnaddedSyllabus)}
                  className="text-[10px] font-bold text-[var(--accent-hex)] hover:underline"
                >
                  Add all ({sortedUnaddedSyllabus.length})
                </button>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {sortedUnaddedSyllabus.map(name => {
                  const sxrTopic = syllabusData?.topics.find(t => t.name === name);
                  const quadrant = sxrTopic ? getQuadrant(sxrTopic) : null;
                  const qStyle = quadrant ? QUADRANT_LABELS[quadrant] : null;
                  return (
                    <button
                      key={name}
                      onClick={() => addSyllabusTopics([name])}
                      className="flex items-start gap-2 p-3 rounded-xl bg-white dark:bg-zinc-900 border border-dashed border-zinc-300 dark:border-zinc-700 hover:border-[var(--accent-hex)] hover:bg-[rgba(var(--accent),0.03)] transition-all text-left"
                    >
                      <Plus size={12} className="text-zinc-400 shrink-0 mt-0.5" />
                      <div className="flex-1 min-w-0">
                        <span className="text-xs font-medium text-zinc-600 dark:text-zinc-400">{name}</span>
                        {sxrTopic && (
                          <div className="flex items-center gap-2 mt-1">
                            {qStyle && (
                              <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full ${qStyle.bg} ${qStyle.color}`}>
                                {qStyle.label}
                              </span>
                            )}
                            <span className="text-[9px] text-zinc-400 dark:text-zinc-500">
                              ~{sxrTopic.markWeight}% · {sxrTopic.examFrequency}/10 yrs
                            </span>
                          </div>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-8 space-y-3">
          <div className="w-12 h-12 mx-auto rounded-2xl bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
            <Shield size={24} className="text-amber-500" />
          </div>
          <p className="text-sm font-bold text-zinc-700 dark:text-zinc-300">No topics mapped yet</p>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 max-w-xs mx-auto">
            Topics auto-import from Syllabus X-Ray when available. You can also add topics manually below.
          </p>
        </div>
      )}

      {/* Coverage heatmap overview (all subjects) */}
      {allSubjectStats.some(s => s.total > 0) && (
        <div className={`p-4 space-y-3 ${CARD_CLASS}`} style={CARD_STYLE}>
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">All Subjects Overview</p>
          {allSubjectStats.filter(s => s.total > 0).map(s => {
            const color = getSubjectColor(s.subjectName);
            return (
              <div key={s.subjectName} className="space-y-1">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${color.dot}`} />
                    <span className="text-xs font-semibold text-zinc-600 dark:text-zinc-400">{s.subjectName}</span>
                  </div>
                  <span className="text-[10px] font-bold" style={{ color: '#2A7D6F' }}>{s.pct}%</span>
                </div>
                {/* Mini heatmap row */}
                <div className="flex gap-0.5">
                  {(topicMap[s.subjectName] || []).map(t => (
                    <div
                      key={t.id}
                      className={`h-2.5 rounded-sm flex-1 ${CONFIDENCE_COLORS[t.confidence]}`}
                      title={`${t.name}: ${CONFIDENCE_LABELS[t.confidence]}`}
                    />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

// ── Panel 2: Grade Trajectory ──────────────────────────────

interface TrajectoryPanelProps {
  subjects: StudentSubjectProfile['subjects'];
  mockResults: MockResult[];
  mockResultsHook: ReturnType<typeof useMockResults>;
  daysUntilExam: number;
}

const MOCK_PRESETS = ['Christmas Mocks', 'February Mocks', 'Pre-LC Mocks', 'Practice Exam'];

interface MockFeedback {
  improved: { subject: string; from: string; to: string; ptsDiff: number }[];
  declined: { subject: string; from: string; to: string; ptsDiff: number }[];
  unchanged: string[];
  totalPtsDiff: number;
}

const TrajectoryPanel: React.FC<TrajectoryPanelProps> = ({ subjects, mockResults, mockResultsHook, daysUntilExam }) => {
  const [showAddForm, setShowAddForm] = useState<false | 'single' | 'full'>(false);
  const [formSubject, setFormSubject] = useState(subjects[0]?.subjectName ?? '');
  const [formGrade, setFormGrade] = useState('');
  const [formDate, setFormDate] = useState(new Date().toISOString().split('T')[0]);
  const [formLabel, setFormLabel] = useState('');
  // Full mock form
  const [fullMockGrades, setFullMockGrades] = useState<Record<string, string>>({});
  const [fullMockLabel, setFullMockLabel] = useState('');
  const [fullMockDate, setFullMockDate] = useState(new Date().toISOString().split('T')[0]);
  // Mock feedback after saving
  const [mockFeedback, setMockFeedback] = useState<MockFeedback | null>(null);

  const formSubjectData = subjects.find(s => s.subjectName === formSubject);
  const gradeOptions = formSubjectData ? getGradesForLevel(formSubjectData.level) : HIGHER_GRADES;

  const initFullMockForm = () => {
    const grades: Record<string, string> = {};
    subjects.forEach(s => { grades[s.subjectName] = s.currentGrade; });
    setFullMockGrades(grades);
    setFullMockLabel('');
    setFullMockDate(new Date().toISOString().split('T')[0]);
    setShowAddForm('full');
  };

  const addResult = () => {
    if (!formSubject || !formGrade || !formDate) return;
    const subjectData = subjects.find(s => s.subjectName === formSubject);
    mockResultsHook.addMockResult({
      label: formLabel.trim() || 'Single Result',
      date: formDate,
      entries: [{ subjectName: formSubject, grade: formGrade, level: subjectData?.level || 'Higher' }],
      totalPoints: gradeToPoints(formGrade),
    });
    setShowAddForm(false);
    setFormGrade('');
    setFormLabel('');
  };

  const addFullMock = () => {
    if (!fullMockDate) return;
    const label = fullMockLabel.trim() || 'Mock Exam';

    // Build entries for unified mock
    const entries = subjects.map(s => ({
      subjectName: s.subjectName,
      grade: fullMockGrades[s.subjectName] || s.currentGrade,
      level: s.level,
    }));

    // Compute feedback vs previous results (using derived mockResults for comparison)
    const improved: MockFeedback['improved'] = [];
    const declined: MockFeedback['declined'] = [];
    const unchanged: string[] = [];
    for (const entry of entries) {
      const prev = mockResults
        .filter(r => r.subject === entry.subjectName && r.grade && r.date)
        .sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
      const prevResult = prev[prev.length - 1];
      if (!prevResult) continue;
      const prevPts = gradeToPoints(prevResult.grade);
      const newPts = gradeToPoints(entry.grade);
      const diff = newPts - prevPts;
      if (diff > 0) improved.push({ subject: entry.subjectName, from: prevResult.grade, to: entry.grade, ptsDiff: diff });
      else if (diff < 0) declined.push({ subject: entry.subjectName, from: prevResult.grade, to: entry.grade, ptsDiff: diff });
      else unchanged.push(entry.subjectName);
    }
    const totalPtsDiff = improved.reduce((s, x) => s + x.ptsDiff, 0) + declined.reduce((s, x) => s + x.ptsDiff, 0);
    if (improved.length > 0 || declined.length > 0 || unchanged.length > 0) {
      setMockFeedback({ improved, declined, unchanged, totalPtsDiff });
    }

    // Compute total points (best 6)
    const scored = entries.map(e => {
      const isMaths = LC_SUBJECTS.find(lc => lc.name === e.subjectName)?.isMaths ?? false;
      return getPointsForGrade(e.grade as Grade, isMaths);
    }).sort((a, b) => b - a);
    const totalPoints = scored.slice(0, 6).reduce((sum, p) => sum + p, 0);

    mockResultsHook.addMockResult({ label, date: fullMockDate, entries, totalPoints });
    setShowAddForm(false);
  };

  const removeResult = (derivedId: string) => {
    // Derived IDs are formatted as `${mock.id}-${subjectName}`.
    // Find the parent unified mock by checking if derivedId starts with mock.id.
    for (const mock of mockResultsHook.mocks) {
      if (derivedId.startsWith(mock.id + '-')) {
        mockResultsHook.removeMockResult(mock.id);
        return;
      }
    }
  };

  // Group results by subject
  const resultsBySubject = useMemo(() => {
    const map: Record<string, MockResult[]> = {};
    for (const r of mockResults) {
      if (!r.subject || !r.grade || !r.date) continue; // skip corrupted entries
      if (!map[r.subject]) map[r.subject] = [];
      map[r.subject].push(r);
    }
    // Sort each group by date
    for (const key of Object.keys(map)) {
      map[key].sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
    }
    return map;
  }, [mockResults]);

  // SVG chart data
  const chartSubjects = subjects.filter(s => resultsBySubject[s.subjectName]?.length);

  return (
    <div className="space-y-5">
      {/* Add result buttons */}
      <div className="flex items-center justify-between">
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Mock & Test Results</p>
        <div className="flex gap-2">
          {showAddForm ? (
            <button onClick={() => setShowAddForm(false)} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-zinc-500 text-xs font-bold hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors">
              <X size={12} /> Cancel
            </button>
          ) : (
            <>
              <button onClick={initFullMockForm} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-white text-xs font-bold hover:shadow-md transition-colors" style={{ backgroundColor: '#2A7D6F' }}>
                <Plus size={12} /> Full Mock
              </button>
              <button onClick={() => setShowAddForm('single')} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-zinc-600 dark:text-zinc-400 text-xs font-bold hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
                <Plus size={12} /> Single
              </button>
            </>
          )}
        </div>
      </div>

      {/* Add result form */}
      <AnimatePresence>
        {showAddForm === 'full' && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className={`p-4 space-y-3 ${CARD_CLASS}`} style={CARD_STYLE}>
              <p className="text-xs font-bold text-zinc-600 dark:text-zinc-300">Log Full Mock — all subjects at once</p>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Label</label>
                  <div className="flex flex-wrap gap-1.5 mt-1 mb-1">
                    {MOCK_PRESETS.map(p => (
                      <button key={p} onClick={() => setFullMockLabel(p)} className={`px-2 py-1 rounded-md text-[10px] font-semibold transition-colors ${fullMockLabel === p ? 'text-white' : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 hover:bg-zinc-200 dark:hover:bg-zinc-700'}`} style={fullMockLabel === p ? { backgroundColor: '#2A7D6F' } : undefined}>
                        {p}
                      </button>
                    ))}
                  </div>
                  <input type="text" value={fullMockLabel} onChange={(e) => setFullMockLabel(e.target.value)} placeholder="Or type your own..." maxLength={30} className="w-full px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none" />
                </div>
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Date</label>
                  <input type="date" value={fullMockDate} onChange={(e) => setFullMockDate(e.target.value)} className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white outline-none" />
                </div>
              </div>
              <div className="space-y-2">
                {subjects.map(s => {
                  const grades = getGradesForLevel(s.level);
                  const color = getSubjectColor(s.subjectName);
                  return (
                    <div key={s.subjectName} className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${color.dot} shrink-0`} />
                      <span className="text-xs font-semibold text-zinc-600 dark:text-zinc-400 w-28 truncate">{s.subjectName}</span>
                      <select
                        value={fullMockGrades[s.subjectName] || s.currentGrade}
                        onChange={(e) => setFullMockGrades(prev => ({ ...prev, [s.subjectName]: e.target.value }))}
                        className="flex-1 px-2 py-1.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-xs text-zinc-800 dark:text-white outline-none"
                      >
                        {grades.map(g => <option key={g} value={g}>{g}</option>)}
                      </select>
                    </div>
                  );
                })}
              </div>
              <button onClick={addFullMock} className="w-full py-2.5 text-sm font-bold text-white hover:shadow-md active:scale-[0.98] transition-all" style={{ backgroundColor: '#2A7D6F', borderRadius: 12 }}>
                Save Full Mock
              </button>
            </div>
          </MotionDiv>
        )}
        {showAddForm === 'single' && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className={`p-4 space-y-3 ${CARD_CLASS}`} style={CARD_STYLE}>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Subject</label>
                  <select
                    value={formSubject}
                    onChange={(e) => { setFormSubject(e.target.value); setFormGrade(''); }}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white outline-none"
                  >
                    {subjects.map(s => (
                      <option key={s.subjectName} value={s.subjectName}>{s.subjectName}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Grade</label>
                  <select
                    value={formGrade}
                    onChange={(e) => setFormGrade(e.target.value)}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white outline-none"
                  >
                    <option value="">Select...</option>
                    {gradeOptions.map(g => (
                      <option key={g} value={g}>{g} ({gradeToPoints(g)} pts)</option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Date</label>
                  <input
                    type="date"
                    value={formDate}
                    onChange={(e) => setFormDate(e.target.value)}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white outline-none"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-bold text-zinc-400 uppercase tracking-wider">Label (optional)</label>
                  <input
                    type="text"
                    value={formLabel}
                    onChange={(e) => setFormLabel(e.target.value)}
                    placeholder="e.g. Mock 1"
                    maxLength={30}
                    className="w-full mt-1 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none"
                  />
                </div>
              </div>
              <button
                onClick={addResult}
                disabled={!formGrade}
                className="w-full py-2.5 text-sm font-bold text-white disabled:opacity-40 hover:shadow-md active:scale-[0.98] transition-all"
                style={{ backgroundColor: '#2A7D6F', borderRadius: 12 }}
              >
                Save Result
              </button>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Mock feedback card */}
      <AnimatePresence>
        {mockFeedback && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div
              className={`p-4 ${CARD_CLASS}`}
              style={{
                ...CARD_STYLE,
                backgroundColor: mockFeedback.totalPtsDiff > 0 ? 'rgba(107,143,113,0.08)' : mockFeedback.totalPtsDiff < 0 ? 'rgba(42,125,111,0.06)' : '#FAF7F4',
              }}
            >
              <div className="flex items-center justify-between mb-3">
                <p className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                  {mockFeedback.totalPtsDiff > 0 ? 'Progress since last mock' : mockFeedback.totalPtsDiff < 0 ? 'Changes since last mock' : 'Compared to last mock'}
                </p>
                <button onClick={() => setMockFeedback(null)} className="text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300">
                  <X size={14} />
                </button>
              </div>
              {mockFeedback.improved.length > 0 && (
                <div className="mb-2">
                  <p className="text-[10px] font-bold mb-1" style={{ color: '#6B8F71' }}>Improved</p>
                  {mockFeedback.improved.map(s => (
                    <p key={s.subject} className="text-xs text-zinc-600 dark:text-zinc-400 flex items-center gap-1.5">
                      <TrendingUp size={10} style={{ color: '#6B8F71' }} />
                      {s.subject}: {s.from} → {s.to} <span className="font-bold" style={{ color: '#6B8F71' }}>(+{s.ptsDiff}pts)</span>
                    </p>
                  ))}
                </div>
              )}
              {mockFeedback.declined.length > 0 && (
                <div className="mb-2">
                  <p className="text-[10px] font-bold mb-1" style={{ color: '#B85C4A' }}>Needs attention</p>
                  {mockFeedback.declined.map(s => (
                    <p key={s.subject} className="text-xs text-zinc-600 dark:text-zinc-400 flex items-center gap-1.5">
                      <AlertTriangle size={10} style={{ color: '#B85C4A' }} />
                      {s.subject}: {s.from} → {s.to} <span className="font-bold" style={{ color: '#B85C4A' }}>({s.ptsDiff}pts)</span>
                    </p>
                  ))}
                </div>
              )}
              {mockFeedback.unchanged.length > 0 && (
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                  Unchanged: {mockFeedback.unchanged.join(', ')}
                </p>
              )}
              {mockFeedback.totalPtsDiff !== 0 && (
                <div className="mt-2 pt-2 border-t border-zinc-200/50 dark:border-white/[0.06]">
                  <p className="text-xs font-bold" style={{ color: mockFeedback.totalPtsDiff > 0 ? '#6B8F71' : '#B85C4A' }}>
                    Net change: {mockFeedback.totalPtsDiff > 0 ? '+' : ''}{mockFeedback.totalPtsDiff} CAO points
                  </p>
                </div>
              )}
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* SVG Chart */}
      {chartSubjects.length > 0 && (
        <div className={`p-4 ${CARD_CLASS}`} style={CARD_STYLE}>
          <TrajectoryChart
            subjects={subjects}
            resultsBySubject={resultsBySubject}
          />
        </div>
      )}

      {/* Gap analysis per subject */}
      <div className="space-y-2">
        {subjects.map((s, sIdx) => {
          const results = resultsBySubject[s.subjectName] || [];
          const latest = results[results.length - 1];
          const targetPts = getPointsForGrade(s.targetGrade, false);
          const currentPts = latest ? gradeToPoints(latest.grade) : null;
          const hexColor = getDistinctSubjectHex(s.subjectName, sIdx);
          const gap = currentPts !== null ? targetPts - currentPts : null;

          return (
            <div key={s.subjectName} className={`flex items-center gap-3 px-4 py-3 ${CARD_CLASS}`} style={CARD_STYLE}>
              <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: hexColor }} />
              <div className="flex-1 min-w-0">
                <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">{s.subjectName}</span>
                {latest ? (
                  <span className="text-xs text-zinc-400 dark:text-zinc-500 ml-2">
                    Latest: {latest.grade} (<span style={{ color: '#2A7D6F' }}>{currentPts} pts</span>)
                    {latest.label && ` — ${latest.label}`}
                  </span>
                ) : (
                  <span className="text-xs text-zinc-400 dark:text-zinc-500 ml-2">No results logged</span>
                )}
              </div>
              <div className="text-right shrink-0">
                <span className="text-[10px] text-zinc-400 dark:text-zinc-500">Target: {s.targetGrade}</span>
                {gap !== null && (
                  <p className="text-xs font-bold" style={{ color: gap <= 0 ? '#6B8F71' : '#C4873B' }}>
                    {gap <= 0 ? 'On target' : `${gap} pts gap`}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Results history */}
      {mockResults.length > 0 && (
        <div className="space-y-2">
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">History</p>
          {[...mockResults].filter(r => r.subject && r.grade && r.date).reverse().slice(0, 20).map(r => {
            const subjectIdx = subjects.findIndex(s => s.subjectName === r.subject);
            const hexColor = getDistinctSubjectHex(r.subject, subjectIdx >= 0 ? subjectIdx : 0);
            return (
              <div key={r.id} className="group flex items-center gap-3 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800/50">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: hexColor }} />
                <span className="text-xs font-semibold text-zinc-600 dark:text-zinc-400 w-24 truncate">{r.subject}</span>
                <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">{r.grade}</span>
                <span className="text-[10px] text-zinc-400 dark:text-zinc-500">{r.date}</span>
                {r.label && <span className="text-[10px] text-zinc-400 dark:text-zinc-500 italic">{r.label}</span>}
                <button
                  onClick={() => removeResult(r.id)}
                  className="ml-auto opacity-0 group-hover:opacity-100 text-zinc-400 hover:text-red-500 transition-all"
                >
                  <X size={12} />
                </button>
              </div>
            );
          })}
        </div>
      )}

      {mockResults.length === 0 && (
        <div className="text-center py-12 space-y-4">
          <div className="w-14 h-14 mx-auto rounded-2xl flex items-center justify-center" style={{ backgroundColor: 'rgba(42,125,111,0.1)' }}>
            <TrendingUp size={28} style={{ color: '#2A7D6F' }} />
          </div>
          <h3 className="text-base font-bold text-zinc-800 dark:text-white">Track your mock exam trajectory</h3>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 max-w-xs mx-auto leading-relaxed">
            Log mock results to see your points climb over time and identify the subjects worth targeting.
          </p>
        </div>
      )}
    </div>
  );
};

// ── SVG Trajectory Chart ───────────────────────────────────

interface TrajectoryChartProps {
  subjects: StudentSubjectProfile['subjects'];
  resultsBySubject: Record<string, MockResult[]>;
}

const TrajectoryChart: React.FC<TrajectoryChartProps> = ({ subjects, resultsBySubject }) => {
  const [hoveredLine, setHoveredLine] = useState<string | null>(null);
  const [hoveredDot, setHoveredDot] = useState<{ id: string; cx: number; cy: number; label: string; subject: string; grade: string } | null>(null);

  const W = 400;
  const H = 200;
  const PAD = { top: 15, right: 15, bottom: 25, left: 35 };
  const plotW = W - PAD.left - PAD.right;
  const plotH = H - PAD.top - PAD.bottom;

  // Collect all dates and find range
  const allResults = Object.values(resultsBySubject).flat();
  if (allResults.length === 0) return null;

  const dates = allResults.map(r => new Date(r.date).getTime()).filter(t => !isNaN(t));
  if (dates.length === 0) return null;
  const minDate = Math.min(...dates);
  const maxDate = Math.max(...dates);
  const dateRange = maxDate - minDate || 86400000; // at least 1 day

  const maxPts = 100; // H1 = 100 CAO points
  const minPts = 0;

  const scaleX = (date: string) => {
    const t = new Date(date).getTime();
    return PAD.left + ((t - minDate) / dateRange) * plotW;
  };
  const scaleY = (pts: number) => {
    return PAD.top + plotH - ((pts - minPts) / (maxPts - minPts)) * plotH;
  };

  // Y-axis labels
  const yLabels = [0, 25, 50, 75, 100];

  // Build subject index for distinct colors
  const subjectsWithResults = subjects.filter(s => resultsBySubject[s.subjectName]?.length);
  const subjectIndexMap: Record<string, number> = {};
  subjects.forEach((s, i) => { subjectIndexMap[s.subjectName] = i; });

  return (
    <div className="space-y-3">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="w-full"
        style={{ maxHeight: 220 }}
        onMouseLeave={() => { setHoveredLine(null); setHoveredDot(null); }}
      >
        {/* Grid lines */}
        {yLabels.map(pts => (
          <g key={pts}>
            <line
              x1={PAD.left} y1={scaleY(pts)}
              x2={W - PAD.right} y2={scaleY(pts)}
              stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5"
            />
            <text x={PAD.left - 5} y={scaleY(pts) + 3} textAnchor="end" className="text-zinc-400 dark:text-zinc-500 fill-current" fontSize="8">
              {pts}
            </text>
          </g>
        ))}

        {/* Subject lines */}
        {subjects.map(s => {
          const results = resultsBySubject[s.subjectName];
          if (!results || results.length < 1) return null;
          const hexColor = getDistinctSubjectHex(s.subjectName, subjectIndexMap[s.subjectName] ?? 0);
          const points = results.map(r => `${scaleX(r.date)},${scaleY(gradeToPoints(r.grade))}`).join(' ');
          const isHovered = hoveredLine === s.subjectName;
          const isFaded = hoveredLine !== null && !isHovered;

          // Target line
          const targetPts = getPointsForGrade(s.targetGrade, false);

          return (
            <g key={s.subjectName} style={{ opacity: isFaded ? 0.15 : 1, transition: 'opacity 0.2s' }}>
              {/* Target dashed line */}
              <line
                x1={PAD.left} y1={scaleY(targetPts)}
                x2={W - PAD.right} y2={scaleY(targetPts)}
                stroke={hexColor} strokeWidth="1" strokeDasharray="4 3" opacity="0.3"
              />
              {/* Invisible wide hit area for hover */}
              {results.length > 1 && (
                <polyline
                  points={points}
                  fill="none"
                  stroke="transparent"
                  strokeWidth="12"
                  strokeLinecap="round"
                  onMouseEnter={() => setHoveredLine(s.subjectName)}
                  style={{ cursor: 'pointer' }}
                />
              )}
              {/* Visible data polyline */}
              {results.length > 1 && (
                <polyline
                  points={points}
                  fill="none"
                  stroke={hexColor}
                  strokeWidth={isHovered ? 3 : 2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  style={{ pointerEvents: 'none', transition: 'stroke-width 0.2s' }}
                />
              )}
              {/* Data points */}
              {results.map(r => {
                const cx = scaleX(r.date);
                const cy = scaleY(gradeToPoints(r.grade));
                const dotLabel = r.label || `${r.grade} — ${r.date}`;
                return (
                  <circle
                    key={r.id}
                    cx={cx} cy={cy} r={hoveredDot?.id === r.id ? 6 : 4}
                    stroke={hexColor}
                    fill="white"
                    strokeWidth="2"
                    style={{ cursor: 'pointer', transition: 'r 0.15s' }}
                    onMouseEnter={() => setHoveredDot({ id: r.id, cx, cy, label: dotLabel, subject: s.subjectName, grade: r.grade })}
                    onMouseLeave={() => setHoveredDot(null)}
                  />
                );
              })}
            </g>
          );
        })}

        {/* Hover tooltip for line */}
        {hoveredLine && !hoveredDot && (() => {
          const results = resultsBySubject[hoveredLine];
          if (!results?.length) return null;
          const lastR = results[results.length - 1];
          const tx = scaleX(lastR.date);
          const ty = scaleY(gradeToPoints(lastR.grade));
          return (
            <g style={{ pointerEvents: 'none' }}>
              <rect x={tx + 6} y={ty - 12} width={hoveredLine.length * 5.5 + 12} height={16} rx="4" fill="rgba(0,0,0,0.8)" />
              <text x={tx + 12} y={ty - 1} fontSize="9" fill="white" fontWeight="600">{hoveredLine}</text>
            </g>
          );
        })()}

        {/* Hover tooltip for dot */}
        {hoveredDot && (() => {
          const label = hoveredDot.label;
          const tooltipW = label.length * 5 + 16;
          // Position tooltip above the dot, flip if near top
          const above = hoveredDot.cy > 40;
          const ty = above ? hoveredDot.cy - 20 : hoveredDot.cy + 10;
          return (
            <g style={{ pointerEvents: 'none' }}>
              <rect
                x={hoveredDot.cx - tooltipW / 2}
                y={ty}
                width={tooltipW} height={16} rx="4"
                fill="rgba(0,0,0,0.85)"
              />
              <text
                x={hoveredDot.cx}
                y={ty + 11}
                fontSize="8" fill="white" fontWeight="600" textAnchor="middle"
              >{label}</text>
            </g>
          );
        })()}
      </svg>

      {/* Legend */}
      {subjectsWithResults.length > 1 && (
        <div className="flex flex-wrap gap-x-4 gap-y-1.5 px-1">
          {subjectsWithResults.map(s => {
            const hexColor = getDistinctSubjectHex(s.subjectName, subjectIndexMap[s.subjectName] ?? 0);
            return (
              <div
                key={s.subjectName}
                className="flex items-center gap-1.5 cursor-pointer"
                onMouseEnter={() => setHoveredLine(s.subjectName)}
                onMouseLeave={() => setHoveredLine(null)}
              >
                <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: hexColor }} />
                <span className="text-[10px] font-semibold text-zinc-600 dark:text-zinc-400">{s.subjectName}</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

// ── Helpers for study pattern charts ───────────────────────

function getMonday(d: Date): Date {
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  const m = new Date(d);
  m.setDate(diff);
  m.setHours(0, 0, 0, 0);
  return m;
}

function toISODateKey(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

// ── Panel 3: Strategic Briefing ────────────────────────────

interface BriefingPanelProps {
  subjects: StudentSubjectProfile['subjects'];
  topicMap: TopicMap;
  mockResults: MockResult[];
  allocations: { subjectName: string; sessions: number }[];
  hoursStudiedMap: Record<string, number>;
  weeksUntilExam: number;
  blockDuration: number;
  daysUntilExam: number;
  timetableCompletions: TimetableCompletions;
}

interface Recommendation {
  subject: string;
  priority: number; // 0-100
  concerns: string[];
  action: string;
  guidance?: SubjectGuidance;
  latestGrade?: string;
}

const BriefingPanel: React.FC<BriefingPanelProps> = ({
  subjects, topicMap, mockResults, allocations, hoursStudiedMap, weeksUntilExam, blockDuration, daysUntilExam, timetableCompletions,
}) => {
  const [showStudyPatterns, setShowStudyPatterns] = useState(false);

  // ── Study pattern data (merged from Insights) ──
  const weeklyData = useMemo(() => {
    const weeks: { label: string; startDate: Date; totalBlocks: number; subjectBlocks: Record<string, number> }[] = [];
    const today = new Date();
    for (let w = 7; w >= 0; w--) {
      const weekStart = getMonday(new Date(today.getTime() - w * 7 * 86400000));
      const subjectBlocks: Record<string, number> = {};
      let total = 0;
      for (let d = 0; d < 7; d++) {
        const dayDate = new Date(weekStart);
        dayDate.setDate(weekStart.getDate() + d);
        const key = toISODateKey(dayDate);
        const blocks = timetableCompletions[key] || [];
        total += blocks.length;
        for (const blockId of blocks) {
          const subName = blockId.split('|')[0];
          if (subName) subjectBlocks[subName] = (subjectBlocks[subName] || 0) + 1;
        }
      }
      const label = `${weekStart.getDate()}/${weekStart.getMonth() + 1}`;
      weeks.push({ label, startDate: weekStart, totalBlocks: total, subjectBlocks });
    }
    return weeks;
  }, [timetableCompletions]);

  const heatmapData = useMemo(() => {
    const days: { date: string; blocks: number }[] = [];
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    for (let i = 27; i >= 0; i--) {
      const d = new Date(today.getTime() - i * 86400000);
      const key = toISODateKey(d);
      const blocks = (timetableCompletions[key] || []).length;
      days.push({ date: key, blocks });
    }
    return days;
  }, [timetableCompletions]);

  const maxDayBlocks = Math.max(1, ...heatmapData.map(d => d.blocks));
  const maxWeekBlocks = Math.max(1, ...weeklyData.map(w => w.totalBlocks));
  const currentWeekSubjects = weeklyData[weeklyData.length - 1]?.subjectBlocks ?? {};
  const currentWeekTotal = Object.values(currentWeekSubjects).reduce((a, b) => a + b, 0);
  const SPW = 360; const SPH = 120;
  const SPAD = { top: 10, right: 10, bottom: 20, left: 30 };
  const spPlotW = SPW - SPAD.left - SPAD.right;
  const spPlotH = SPH - SPAD.top - SPAD.bottom;

  const recommendations = useMemo((): Recommendation[] => {
    const recs: Recommendation[] = [];

    for (const s of subjects) {
      const concerns: string[] = [];
      let priority = 0;

      // Coverage analysis
      const topics = topicMap[s.subjectName] || [];
      if (topics.length > 0) {
        const notStarted = topics.filter(t => t.confidence === 'not-started').length;
        const shaky = topics.filter(t => t.confidence === 'shaky').length;
        const weakPct = (notStarted + shaky * 0.5) / topics.length;
        if (notStarted > 0) {
          concerns.push(`${notStarted} topic${notStarted > 1 ? 's' : ''} not started`);
          priority += weakPct * 40;
        }
        if (shaky > 0 && notStarted === 0) {
          concerns.push(`${shaky} shaky topic${shaky > 1 ? 's' : ''}`);
          priority += weakPct * 25;
        }
      }

      // Trajectory analysis
      const results = mockResults
        .filter(r => r.subject === s.subjectName && r.grade && r.date)
        .sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
      if (results.length > 0) {
        const latest = results[results.length - 1];
        const latestPts = gradeToPoints(latest.grade);
        const targetPts = getPointsForGrade(s.targetGrade, false);
        const gap = targetPts - latestPts;
        if (gap > 0) {
          concerns.push(`${gap} point gap to target (${latest.grade} → ${s.targetGrade})`);
          priority += Math.min(40, (gap / targetPts) * 60);
        }
        // Declining trend
        if (results.length >= 2) {
          const prev = results[results.length - 2];
          const prevPts = gradeToPoints(prev.grade);
          if (latestPts < prevPts) {
            concerns.push('grade declining');
            priority += 15;
          }
        }
      }

      // Time allocation relative to need
      const alloc = allocations.find(a => a.subjectName === s.subjectName);
      const sessionsPerWeek = alloc?.sessions ?? 1;

      if (concerns.length === 0 && topics.length === 0 && results.length === 0) {
        // No data — gentle nudge
        concerns.push('no coverage data or test results logged yet');
        priority += 5;
      }

      // Generate action text
      let action = '';
      if (concerns.length > 0) {
        const weakTopics = topics.filter(t => t.confidence === 'not-started').slice(0, 2).map(t => t.name);
        if (weakTopics.length > 0) {
          action = `Prioritise: ${weakTopics.join(', ')}. You have ${sessionsPerWeek} session${sessionsPerWeek > 1 ? 's' : ''} allocated this week.`;
        } else if (topics.filter(t => t.confidence === 'shaky').length > 0) {
          const shakyNames = topics.filter(t => t.confidence === 'shaky').slice(0, 2).map(t => t.name);
          action = `Strengthen: ${shakyNames.join(', ')}.`;
        } else {
          action = `${sessionsPerWeek} session${sessionsPerWeek > 1 ? 's' : ''} allocated this week.`;
        }
      }

      if (concerns.length > 0) {
        // Derive latest grade for subject guidance
        const latestGrade = results.length > 0
          ? results[results.length - 1].grade
          : (s.currentGrade as string | undefined);
        const guidance = latestGrade ? getSubjectGuidance(s.subjectName, latestGrade) : undefined;
        recs.push({ subject: s.subjectName, priority, concerns, action, guidance, latestGrade });
      }
    }

    recs.sort((a, b) => b.priority - a.priority);
    return recs;
  }, [subjects, topicMap, mockResults, allocations]);

  // Best and worst subjects
  const subjectsWithResults = subjects.filter(s =>
    mockResults.some(r => r.subject === s.subjectName)
  );

  const bestSubject = useMemo(() => {
    let best: { name: string; surplus: number } | null = null;
    for (const s of subjectsWithResults) {
      const results = mockResults.filter(r => r.subject === s.subjectName && r.grade && r.date).sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));
      const latest = results[results.length - 1];
      if (!latest) continue;
      const surplus = gradeToPoints(latest.grade) - getPointsForGrade(s.targetGrade, false);
      if (!best || surplus > best.surplus) {
        best = { name: s.subjectName, surplus };
      }
    }
    return best;
  }, [subjectsWithResults, mockResults]);

  const hasData = topicMap && Object.values(topicMap).some(t => t.length > 0) || mockResults.length > 0;

  const [expandedGuidance, setExpandedGuidance] = useState<string | null>(null);

  return (
    <div className="space-y-5">
      {/* Countdown reminder */}
      <div className={`flex items-center gap-3 px-4 py-3 ${CARD_CLASS}`} style={CARD_STYLE}>
        <Clock size={16} style={{ color: '#2A7D6F' }} className="shrink-0" />
        <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
          <span style={{ color: '#2A7D6F' }}>{daysUntilExam}</span> days remaining — {weeksUntilExam} weeks of study
        </p>
      </div>

      {/* Study Patterns — collapsible */}
      <div className={`overflow-hidden ${CARD_CLASS}`} style={CARD_STYLE}>
        <button
          onClick={() => setShowStudyPatterns(!showStudyPatterns)}
          className="w-full flex items-center justify-between px-4 py-3 text-left"
        >
          <div className="flex items-center gap-2">
            <Activity size={14} style={{ color: '#2A7D6F' }} />
            <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">Study Patterns</span>
            {currentWeekTotal > 0 && (
              <span className="text-[10px] text-zinc-400 dark:text-zinc-500">{currentWeekTotal} sessions this week</span>
            )}
          </div>
          <ChevronDown size={14} className={`text-zinc-400 transition-transform ${showStudyPatterns ? 'rotate-180' : ''}`} />
        </button>
        <AnimatePresence>
          {showStudyPatterns && (
            <MotionDiv
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.25 }}
              className="overflow-hidden"
            >
              <div className="px-4 pb-4 space-y-5">
                {/* Weekly volume bar chart */}
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Weekly Volume</p>
                  <svg viewBox={`0 0 ${SPW} ${SPH}`} className="w-full" style={{ maxHeight: 140 }}>
                    {[0, 0.5, 1].map(frac => {
                      const y = SPAD.top + spPlotH * (1 - frac);
                      const val = Math.round(maxWeekBlocks * frac);
                      return (
                        <g key={frac}>
                          <line x1={SPAD.left} y1={y} x2={SPW - SPAD.right} y2={y} stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5" />
                          {frac > 0 && <text x={SPAD.left - 4} y={y + 3} textAnchor="end" className="text-zinc-400 dark:text-zinc-500 fill-current" fontSize="7">{val}</text>}
                        </g>
                      );
                    })}
                    {weeklyData.map((w, i) => {
                      const barW = Math.max(8, spPlotW / weeklyData.length - 4);
                      const x = SPAD.left + (i / weeklyData.length) * spPlotW + 2;
                      const barH = maxWeekBlocks > 0 ? (w.totalBlocks / maxWeekBlocks) * spPlotH : 0;
                      const isCurrentWeek = i === weeklyData.length - 1;
                      return (
                        <g key={i}>
                          <rect x={x} y={SPAD.top + spPlotH - barH} width={barW} height={Math.max(0, barH)} rx="3" fill={isCurrentWeek ? '#2A7D6F' : undefined} className={isCurrentWeek ? '' : 'fill-zinc-300 dark:fill-zinc-600'} opacity={isCurrentWeek ? 1 : 0.7} />
                          <text x={x + barW / 2} y={SPH - 4} textAnchor="middle" className="fill-current text-zinc-400 dark:text-zinc-500" fontSize="7">{w.label}</text>
                          {w.totalBlocks > 0 && <text x={x + barW / 2} y={SPAD.top + spPlotH - barH - 3} textAnchor="middle" className="fill-current text-zinc-500 dark:text-zinc-400" fontSize="7" fontWeight="600">{w.totalBlocks}</text>}
                        </g>
                      );
                    })}
                  </svg>
                </div>

                {/* Daily consistency heatmap */}
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Daily Consistency (28 days)</p>
                  <div className="flex flex-wrap gap-1 justify-center">
                    {heatmapData.map(d => {
                      const intensity = d.blocks / maxDayBlocks;
                      const bgColor = d.blocks === 0
                        ? '#EDEAE6'
                        : intensity > 0.66
                          ? '#2A7D6F'
                          : intensity > 0.33
                            ? '#D4907D'
                            : '#E8C4B8';
                      return <div key={d.date} className="w-5 h-5 rounded-sm" style={{ backgroundColor: bgColor }} title={`${d.date}: ${d.blocks} session${d.blocks !== 1 ? 's' : ''}`} />;
                    })}
                  </div>
                  <div className="flex items-center justify-center gap-2 mt-2 text-[10px] text-zinc-400 dark:text-zinc-500">
                    <span>Less</span>
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#EDEAE6' }} />
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#E8C4B8' }} />
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#D4907D' }} />
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#2A7D6F' }} />
                    <span>More</span>
                  </div>
                </div>

                {/* Subject balance — this week */}
                {currentWeekTotal > 0 && (
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Subject Balance — This Week</p>
                    <div className="flex h-3.5 rounded-full overflow-hidden">
                      {subjects.map((s, i) => {
                        const count = currentWeekSubjects[s.subjectName] || 0;
                        if (count === 0) return null;
                        const pct = (count / currentWeekTotal) * 100;
                        const hexColor = getDistinctSubjectHex(s.subjectName, i);
                        return <div key={s.subjectName} style={{ width: `${pct}%`, backgroundColor: hexColor }} className="h-full" title={`${s.subjectName}: ${count} sessions`} />;
                      })}
                    </div>
                    <div className="flex flex-wrap gap-x-3 gap-y-1 mt-2">
                      {subjects.map((s, i) => {
                        const count = currentWeekSubjects[s.subjectName] || 0;
                        if (count === 0) return null;
                        const hexColor = getDistinctSubjectHex(s.subjectName, i);
                        return (
                          <div key={s.subjectName} className="flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: hexColor }} />
                            <span className="text-[10px] text-zinc-500 dark:text-zinc-400">{s.subjectName}</span>
                            <span className="text-[10px] font-bold text-zinc-600 dark:text-zinc-300">{count}</span>
                          </div>
                        );
                      })}
                    </div>
                    {subjects.filter(s => !currentWeekSubjects[s.subjectName]).length > 0 && (
                      <div className="mt-2 flex items-start gap-2 px-3 py-2 rounded-lg bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-800/30">
                        <AlertTriangle size={12} className="text-amber-500 mt-0.5 shrink-0" />
                        <p className="text-[10px] text-amber-700 dark:text-amber-300">
                          <strong>Not studied this week:</strong>{' '}
                          {subjects.filter(s => !currentWeekSubjects[s.subjectName]).map(s => s.subjectName).join(', ')}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </MotionDiv>
          )}
        </AnimatePresence>
      </div>

      {hasData ? (
        <>
          {/* Recommendations */}
          <div className="space-y-3">
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Priority Actions</p>
            {recommendations.slice(0, 5).map((rec, i) => {
              const color = getSubjectColor(rec.subject);
              const isUrgent = rec.priority >= 30;
              return (
                <div
                  key={rec.subject}
                  className={`p-4 ${CARD_CLASS}`}
                  style={{
                    ...CARD_STYLE,
                    backgroundColor: isUrgent ? 'rgba(42,125,111,0.06)' : '#FAF7F4',
                  }}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`w-2.5 h-2.5 rounded-full ${color.dot}`} />
                    <span className="text-sm font-bold text-zinc-800 dark:text-white">{rec.subject}</span>
                    {isUrgent && <AlertTriangle size={12} style={{ color: '#B85C4A' }} />}
                  </div>
                  <ul className="space-y-1 mb-2">
                    {rec.concerns.map((c, ci) => (
                      <li key={ci} className="flex items-start gap-2 text-xs text-zinc-600 dark:text-zinc-400">
                        <Minus size={8} className="mt-1 shrink-0 text-zinc-400" />
                        {c}
                      </li>
                    ))}
                  </ul>
                  {rec.action && (
                    <p className="text-xs font-semibold" style={{ color: '#2A7D6F' }}>{rec.action}</p>
                  )}

                  {/* Examiner Insights — expandable subject guidance */}
                  {rec.guidance && (
                    <div className="mt-3 border-t border-zinc-200/50 dark:border-white/[0.06] pt-3">
                      <button
                        onClick={() => setExpandedGuidance(expandedGuidance === rec.subject ? null : rec.subject)}
                        className="flex items-center gap-2 text-xs font-semibold transition-colors"
                        style={{ color: '#2A7D6F' }}
                      >
                        <BookOpen size={12} />
                        Examiner Insights {rec.latestGrade && <span className="font-normal text-zinc-400">({rec.latestGrade})</span>}
                        <ChevronDown size={12} className={`transition-transform ${expandedGuidance === rec.subject ? 'rotate-180' : ''}`} />
                      </button>
                      <AnimatePresence>
                        {expandedGuidance === rec.subject && (
                          <MotionDiv
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.25 }}
                            className="overflow-hidden"
                          >
                            <div className="mt-3 space-y-3 text-xs">
                              {/* Common Struggles */}
                              <div>
                                <p className="font-bold text-zinc-700 dark:text-zinc-300 mb-1.5">Why students struggle here</p>
                                <ul className="space-y-1.5">
                                  {rec.guidance.commonStruggles.map((s, si) => (
                                    <li key={si} className="flex items-start gap-2 text-zinc-600 dark:text-zinc-400">
                                      <span className="mt-1.5 w-1 h-1 rounded-full shrink-0" style={{ backgroundColor: '#B85C4A' }} />
                                      {s}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                              {/* Actions */}
                              <div>
                                <p className="font-bold text-zinc-700 dark:text-zinc-300 mb-1.5">What to do</p>
                                <ul className="space-y-1.5">
                                  {rec.guidance.actions.map((a, ai) => (
                                    <li key={ai} className="flex items-start gap-2 text-zinc-600 dark:text-zinc-400">
                                      <span className="mt-1.5 w-1 h-1 rounded-full shrink-0" style={{ backgroundColor: '#6B8F71' }} />
                                      {a}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                              {/* Exam Trap */}
                              <div className="p-3 rounded-lg" style={{ backgroundColor: '#FDF3E7', border: '0.5px solid rgba(196,135,59,0.2)', borderRadius: 12 }}>
                                <p className="font-bold mb-1" style={{ color: '#8B5E2A' }}>Exam trap</p>
                                <p style={{ color: '#C4873B' }}>{rec.guidance.examTrap}</p>
                              </div>
                              {/* Mindset Shift */}
                              <div className="p-3 rounded-lg" style={{ backgroundColor: 'rgba(42,125,111,0.06)', border: '0.5px solid rgba(42,125,111,0.15)', borderRadius: 12 }}>
                                <p className="font-bold mb-1" style={{ color: '#2A7D6F' }}>Mindset shift</p>
                                <p className="text-zinc-600 dark:text-zinc-400">{rec.guidance.mindsetShift}</p>
                              </div>
                            </div>
                          </MotionDiv>
                        )}
                      </AnimatePresence>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Overall summary */}
          {bestSubject && (
            <div className={`px-4 py-3 ${CARD_CLASS}`} style={{ ...CARD_STYLE, backgroundColor: 'rgba(107,143,113,0.08)' }}>
              <div className="flex items-center gap-2">
                <CheckCircle size={14} style={{ color: '#6B8F71' }} />
                <p className="text-xs font-semibold" style={{ color: '#6B8F71' }}>
                  {bestSubject.surplus >= 0
                    ? `Strongest: ${bestSubject.name} — above target`
                    : `Closest to target: ${bestSubject.name}`
                  }
                </p>
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-12 text-zinc-400 dark:text-zinc-500 space-y-3">
          <Target size={36} className="mx-auto opacity-40" />
          <p className="text-sm font-medium">No strategic data yet</p>
          <div className="text-xs space-y-1">
            <p>Add topics in the <strong>Coverage</strong> tab to track what you've studied</p>
            <p>Log test results in the <strong>Trajectory</strong> tab to track your grades</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default WarRoom;
