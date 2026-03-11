/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useToast } from './Toast';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Clock, Map, TrendingUp, Target, Plus, X, ChevronDown,
  AlertTriangle, CheckCircle, Circle, Minus, Calendar,
} from 'lucide-react';
import { db } from '../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import {
  type StudentSubjectProfile, type Grade, type TimetableCompletions,
  getPointsForGrade, getGradeIndex, getGradesForLevel,
  HIGHER_GRADES, ORDINARY_GRADES,
} from './subjectData';
import {
  computeSubjectPriorities, allocateSessions, computeWeeksUntilExam,
} from './timetableAlgorithm';
import { getSubjectColor, getSubjectStroke, SUBJECT_STROKE_COLORS, getDistinctSubjectHex } from '../studySessionData';
import { type StudySessionRecord } from '../studySessionData';

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

interface WarRoomData {
  topicMap: TopicMap;
  mockResults: MockResult[];
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

function gradeToPoints(grade: string): number {
  if (grade.startsWith('H')) return getPointsForGrade(grade as Grade, false);
  if (grade.startsWith('O')) return getPointsForGrade(grade as Grade, false);
  return 0;
}

// ── Main Component ─────────────────────────────────────────

const WarRoom: React.FC<WarRoomProps> = ({ uid, profile, timetableCompletions }) => {
  const { showToast } = useToast();
  const [activePanel, setActivePanel] = useState(0);
  const [warRoomData, setWarRoomData] = useState<WarRoomData>({ topicMap: {}, mockResults: [] });
  const [studySessions, setStudySessions] = useState<StudySessionRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load data from Firestore
  useEffect(() => {
    if (!uid) return;
    (async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        const data = snap.data() || {};
        if (data.warRoom) {
          setWarRoomData({
            topicMap: data.warRoom.topicMap || {},
            mockResults: data.warRoom.mockResults || [],
          });
        }
        if (data.studySessions) {
          setStudySessions(data.studySessions as StudySessionRecord[]);
        }
      } catch (e) {
        console.error('Failed to load War Room data:', e);
      }
      setIsLoading(false);
    })();
  }, [uid]);

  // Persist helpers
  const saveTopicMap = useCallback((topicMap: TopicMap) => {
    setWarRoomData(prev => {
      const next = { ...prev, topicMap };
      setDoc(doc(db, 'progress', uid), { warRoom: next }, { merge: true })
        .catch(e => { console.error('Failed to save topic map:', e); showToast('Couldn\'t save — check your connection', 'error'); });
      return next;
    });
  }, [uid]);

  const saveMockResults = useCallback((mockResults: MockResult[]) => {
    setWarRoomData(prev => {
      const next = { ...prev, mockResults };
      setDoc(doc(db, 'progress', uid), { warRoom: next }, { merge: true })
        .catch(e => { console.error('Failed to save mock results:', e); showToast('Couldn\'t save — check your connection', 'error'); });
      return next;
    });
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
              className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-lg text-xs font-bold transition-all ${
                isActive
                  ? 'bg-white dark:bg-zinc-900 text-zinc-800 dark:text-white shadow-sm'
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
            />
          )}
          {activePanel === 1 && (
            <CoveragePanel
              subjects={subjects}
              topicMap={warRoomData.topicMap}
              onUpdateTopicMap={saveTopicMap}
            />
          )}
          {activePanel === 2 && (
            <TrajectoryPanel
              subjects={subjects}
              mockResults={warRoomData.mockResults}
              onUpdateMockResults={saveMockResults}
              daysUntilExam={daysUntilExam}
            />
          )}
          {activePanel === 3 && (
            <BriefingPanel
              subjects={subjects}
              topicMap={warRoomData.topicMap}
              mockResults={warRoomData.mockResults}
              allocations={allocations}
              hoursStudiedMap={hoursStudiedMap}
              weeksUntilExam={weeksUntilExam}
              blockDuration={blockDuration}
              daysUntilExam={daysUntilExam}
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
}

const CountdownPanel: React.FC<CountdownPanelProps> = ({ daysUntilExam, subjects, allocations, weeksUntilExam, hoursStudiedMap, blockDuration }) => {
  const subjectBudgets = useMemo(() => {
    return subjects.map(s => {
      const alloc = allocations.find(a => a.subjectName === s.subjectName);
      const sessionsPerWeek = alloc?.sessions ?? 1;
      const hoursRemaining = (sessionsPerWeek * weeksUntilExam * blockDuration) / 60;
      const hoursStudied = hoursStudiedMap[s.subjectName] || 0;
      const totalHours = hoursStudied + hoursRemaining;
      const pct = totalHours > 0 ? Math.min(100, Math.round((hoursStudied / totalHours) * 100)) : 0;
      return { subjectName: s.subjectName, hoursStudied, hoursRemaining, totalHours, pct };
    });
  }, [subjects, allocations, weeksUntilExam, hoursStudiedMap, blockDuration]);

  const totalStudied = subjectBudgets.reduce((sum, s) => sum + s.hoursStudied, 0);
  const totalRemaining = subjectBudgets.reduce((sum, s) => sum + s.hoursRemaining, 0);

  return (
    <div className="space-y-6">
      {/* Hero countdown */}
      <div className="text-center py-8 bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-2xl">
        <motion.p
          className="text-6xl font-bold text-zinc-800 dark:text-white tabular-nums"
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

      {/* Per-subject time budgets */}
      <div className="space-y-3">
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Time Budget by Subject</p>
        {subjectBudgets.map(s => {
          const color = getSubjectColor(s.subjectName);
          return (
            <div key={s.subjectName} className="space-y-1.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className={`w-2.5 h-2.5 rounded-full ${color.dot} shrink-0`} />
                  <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">{s.subjectName}</span>
                </div>
                <span className="text-xs text-zinc-400 dark:text-zinc-500 tabular-nums">
                  {Math.round(s.hoursStudied)}h / {Math.round(s.totalHours)}h
                </span>
              </div>
              <div className="h-2 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden">
                <motion.div
                  className={`h-full rounded-full ${color.dot.replace('bg-', 'bg-')}`}
                  initial={{ width: 0 }}
                  animate={{ width: `${s.pct}%` }}
                  transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                />
              </div>
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
  topicMap: TopicMap;
  onUpdateTopicMap: (topicMap: TopicMap) => void;
}

const CoveragePanel: React.FC<CoveragePanelProps> = ({ subjects, topicMap, onUpdateTopicMap }) => {
  const [selectedSubject, setSelectedSubject] = useState(subjects[0]?.subjectName ?? '');
  const [newTopicName, setNewTopicName] = useState('');

  const topics = topicMap[selectedSubject] || [];

  const addTopic = () => {
    const trimmed = newTopicName.trim();
    if (!trimmed || trimmed.length < 2) return;
    const entry: TopicEntry = {
      id: genId(),
      name: trimmed,
      confidence: 'not-started',
      updatedAt: Date.now(),
    };
    const updated = { ...topicMap, [selectedSubject]: [...topics, entry] };
    onUpdateTopicMap(updated);
    setNewTopicName('');
  };

  const cycleConfidence = (topicId: string) => {
    const updated = {
      ...topicMap,
      [selectedSubject]: topics.map(t =>
        t.id === topicId
          ? { ...t, confidence: CONFIDENCE_CYCLE[t.confidence], updatedAt: Date.now() }
          : t
      ),
    };
    onUpdateTopicMap(updated);
  };

  const removeTopic = (topicId: string) => {
    const updated = {
      ...topicMap,
      [selectedSubject]: topics.filter(t => t.id !== topicId),
    };
    onUpdateTopicMap(updated);
  };

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
          className="px-4 py-2.5 rounded-xl bg-[var(--accent-hex)] text-white text-sm font-bold disabled:opacity-40 hover:shadow-md active:scale-[0.97] transition-all"
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
          <span className="ml-auto font-bold text-zinc-600 dark:text-zinc-300">{currentStats.pct}% covered</span>
        </div>
      )}

      {/* Topic grid */}
      {topics.length > 0 ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
          {topics.map(topic => (
            <div
              key={topic.id}
              className="group relative p-3 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06] cursor-pointer hover:shadow-sm transition-all"
              onClick={() => cycleConfidence(topic.id)}
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
                onClick={(e) => { e.stopPropagation(); removeTopic(topic.id); }}
                className="absolute top-1 right-1 w-5 h-5 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 text-zinc-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 transition-all"
              >
                <X size={10} />
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-10 text-zinc-400 dark:text-zinc-500">
          <Map size={32} className="mx-auto mb-3 opacity-40" />
          <p className="text-sm font-medium">No topics yet for {selectedSubject}</p>
          <p className="text-xs mt-1">Add topics you're studying and rate your confidence</p>
        </div>
      )}

      {/* Coverage heatmap overview (all subjects) */}
      {allSubjectStats.some(s => s.total > 0) && (
        <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-4 space-y-3">
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
                  <span className="text-[10px] font-bold text-zinc-500 dark:text-zinc-400">{s.pct}%</span>
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
  onUpdateMockResults: (results: MockResult[]) => void;
  daysUntilExam: number;
}

const TrajectoryPanel: React.FC<TrajectoryPanelProps> = ({ subjects, mockResults, onUpdateMockResults, daysUntilExam }) => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [formSubject, setFormSubject] = useState(subjects[0]?.subjectName ?? '');
  const [formGrade, setFormGrade] = useState('');
  const [formDate, setFormDate] = useState(new Date().toISOString().split('T')[0]);
  const [formLabel, setFormLabel] = useState('');

  const formSubjectData = subjects.find(s => s.subjectName === formSubject);
  const gradeOptions = formSubjectData ? getGradesForLevel(formSubjectData.level) : HIGHER_GRADES;

  const addResult = () => {
    if (!formSubject || !formGrade || !formDate) return;
    const result: MockResult = {
      id: genId(),
      subject: formSubject,
      grade: formGrade,
      date: formDate,
      label: formLabel.trim() || undefined,
      timestamp: Date.now(),
    };
    onUpdateMockResults([...mockResults, result]);
    setShowAddForm(false);
    setFormGrade('');
    setFormLabel('');
  };

  const removeResult = (id: string) => {
    onUpdateMockResults(mockResults.filter(r => r.id !== id));
  };

  // Group results by subject
  const resultsBySubject = useMemo(() => {
    const map: Record<string, MockResult[]> = {};
    for (const r of mockResults) {
      if (!map[r.subject]) map[r.subject] = [];
      map[r.subject].push(r);
    }
    // Sort each group by date
    for (const key of Object.keys(map)) {
      map[key].sort((a, b) => a.date.localeCompare(b.date));
    }
    return map;
  }, [mockResults]);

  // SVG chart data
  const chartSubjects = subjects.filter(s => resultsBySubject[s.subjectName]?.length);

  return (
    <div className="space-y-5">
      {/* Add result button */}
      <div className="flex items-center justify-between">
        <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Mock & Test Results</p>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[rgba(var(--accent),0.08)] text-[var(--accent-hex)] text-xs font-bold hover:bg-[rgba(var(--accent),0.15)] transition-colors"
        >
          {showAddForm ? <X size={12} /> : <Plus size={12} />}
          {showAddForm ? 'Cancel' : 'Log Result'}
        </button>
      </div>

      {/* Add result form */}
      <AnimatePresence>
        {showAddForm && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-4 space-y-3">
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
                className="w-full py-2.5 rounded-xl text-sm font-bold bg-[var(--accent-hex)] text-white disabled:opacity-40 hover:shadow-md active:scale-[0.98] transition-all"
              >
                Save Result
              </button>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* SVG Chart */}
      {chartSubjects.length > 0 && (
        <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-4">
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
          const targetPts = getPointsForGrade(s.targetGrade, s.subjectName === 'Mathematics');
          const currentPts = latest ? gradeToPoints(latest.grade) : null;
          const hexColor = getDistinctSubjectHex(s.subjectName, sIdx);
          const gap = currentPts !== null ? targetPts - currentPts : null;

          return (
            <div key={s.subjectName} className="flex items-center gap-3 px-4 py-3 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06]">
              <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: hexColor }} />
              <div className="flex-1 min-w-0">
                <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">{s.subjectName}</span>
                {latest ? (
                  <span className="text-xs text-zinc-400 dark:text-zinc-500 ml-2">
                    Latest: {latest.grade} ({currentPts} pts)
                    {latest.label && ` — ${latest.label}`}
                  </span>
                ) : (
                  <span className="text-xs text-zinc-400 dark:text-zinc-500 ml-2">No results logged</span>
                )}
              </div>
              <div className="text-right shrink-0">
                <span className="text-[10px] text-zinc-400 dark:text-zinc-500">Target: {s.targetGrade}</span>
                {gap !== null && (
                  <p className={`text-xs font-bold ${gap <= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
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
          {[...mockResults].reverse().slice(0, 20).map(r => {
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
        <div className="text-center py-10 text-zinc-400 dark:text-zinc-500">
          <TrendingUp size={32} className="mx-auto mb-3 opacity-40" />
          <p className="text-sm font-medium">No results logged yet</p>
          <p className="text-xs mt-1">Log mock exams and test results to track your trajectory</p>
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

  const dates = allResults.map(r => new Date(r.date).getTime());
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
          const targetPts = getPointsForGrade(s.targetGrade, s.subjectName === 'Mathematics');

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
}

interface Recommendation {
  subject: string;
  priority: number; // 0-100
  concerns: string[];
  action: string;
}

const BriefingPanel: React.FC<BriefingPanelProps> = ({
  subjects, topicMap, mockResults, allocations, hoursStudiedMap, weeksUntilExam, blockDuration, daysUntilExam,
}) => {
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
        .filter(r => r.subject === s.subjectName)
        .sort((a, b) => a.date.localeCompare(b.date));
      if (results.length > 0) {
        const latest = results[results.length - 1];
        const latestPts = gradeToPoints(latest.grade);
        const targetPts = getPointsForGrade(s.targetGrade, s.subjectName === 'Mathematics');
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
        recs.push({ subject: s.subjectName, priority, concerns, action });
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
      const results = mockResults.filter(r => r.subject === s.subjectName).sort((a, b) => a.date.localeCompare(b.date));
      const latest = results[results.length - 1];
      if (!latest) continue;
      const surplus = gradeToPoints(latest.grade) - getPointsForGrade(s.targetGrade, s.subjectName === 'Mathematics');
      if (!best || surplus > best.surplus) {
        best = { name: s.subjectName, surplus };
      }
    }
    return best;
  }, [subjectsWithResults, mockResults]);

  const hasData = topicMap && Object.values(topicMap).some(t => t.length > 0) || mockResults.length > 0;

  return (
    <div className="space-y-5">
      {/* Countdown reminder */}
      <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-red-50 dark:bg-red-900/15 border border-red-200 dark:border-red-800/30">
        <Clock size={16} className="text-red-500 shrink-0" />
        <p className="text-sm font-semibold text-red-700 dark:text-red-300">
          {daysUntilExam} days remaining — {weeksUntilExam} weeks of study
        </p>
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
                  className={`p-4 rounded-xl border ${
                    isUrgent
                      ? 'bg-rose-50 dark:bg-rose-900/10 border-rose-200 dark:border-rose-800/30'
                      : 'bg-white dark:bg-zinc-900 border-zinc-200/60 dark:border-white/[0.06]'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`w-2.5 h-2.5 rounded-full ${color.dot}`} />
                    <span className="text-sm font-bold text-zinc-800 dark:text-white">{rec.subject}</span>
                    {isUrgent && <AlertTriangle size={12} className="text-rose-500" />}
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
                    <p className="text-xs font-semibold text-[var(--accent-hex)]">{rec.action}</p>
                  )}
                </div>
              );
            })}
          </div>

          {/* Overall summary */}
          {bestSubject && (
            <div className="px-4 py-3 rounded-xl bg-emerald-50 dark:bg-emerald-900/15 border border-emerald-200 dark:border-emerald-800/30">
              <div className="flex items-center gap-2">
                <CheckCircle size={14} className="text-emerald-500" />
                <p className="text-xs font-semibold text-emerald-700 dark:text-emerald-300">
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
