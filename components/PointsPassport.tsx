/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  TrendingUp, Zap, Plus, Trash2,
  ArrowRight, Star, Calendar, Award, Rocket,
} from 'lucide-react';
import {
  type StudentSubjectProfile, type Grade, type Level,
  LC_SUBJECTS, getPointsForGrade, getGradesForLevel,

  computeBargains,
} from './subjectData';
import { useToast } from './Toast';
import { useMockResults } from '../hooks/useMockResults';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';

// ─── Types ───────────────────────────────────────────────────────────────────

interface PointsPassportProps {
  uid: string;
  profile: StudentSubjectProfile;
}

interface MockResult {
  id: string;
  label: string; // e.g. "Christmas Mocks", "Pre-LC Mocks"
  date: string;  // ISO date
  grades: { subjectName: string; grade: Grade; level: Level }[];
  totalPoints: number;
}

// ─── Constants ───────────────────────────────────────────────────────────────

const MOCK_PRESETS = ['Christmas Mocks', 'February Mocks', 'Pre-LC Mocks', 'Practice Exam'];

// Typical improvement ranges (anonymised, based on general LC patterns)
const TRAJECTORY_DATA = [
  { range: '200-250', typical: '30-60', message: 'Students in this range often gain 30-60 points by focusing on their 3 weakest topics per subject.' },
  { range: '250-300', typical: '30-55', message: 'At this level, targeted practice on exam technique typically yields 30-55 extra points.' },
  { range: '300-350', typical: '25-50', message: 'From here, most gains come from moving 2-3 subjects up one grade each — very achievable with focus.' },
  { range: '350-400', typical: '20-45', message: 'Students here often underestimate their potential. Strategic subject focus can unlock 20-45 more points.' },
  { range: '400-450', typical: '15-35', message: 'You\'re in strong territory. Fine-tuning exam timing and tackling stretch topics can add 15-35 points.' },
  { range: '450-500', typical: '10-25', message: 'At this level, the biggest gains come from eliminating careless errors and perfecting high-mark questions.' },
  { range: '500+', typical: '5-20', message: 'Elite range. Marginal gains come from perfecting your strongest subjects and nailing time management.' },
];

// Motivational micro-stories
const MICRO_STORIES = [
  { from: 310, to: 402, quote: 'I focused on my 3 weakest topics in each subject. I stopped trying to study everything and just attacked the gaps.', label: 'Student, 2024' },
  { from: 275, to: 365, quote: 'I switched from re-reading notes to doing past papers under timed conditions. That one change was everything.', label: 'Student, 2023' },
  { from: 340, to: 421, quote: 'My teacher said points at mocks aren\'t your ceiling — they\'re your floor. I believed her and kept pushing.', label: 'Student, 2024' },
  { from: 380, to: 478, quote: 'I found out that improving Maths from H6 to H5 was worth way more than I thought because of the bonus. That became my mission.', label: 'Student, 2023' },
  { from: 255, to: 345, quote: 'Everyone told me I was a "300 student." I stopped listening and just focused on what I could control.', label: 'Student, 2024' },
];

// ─── Utility ─────────────────────────────────────────────────────────────────

function computeBestSixTotal(
  subjects: { subjectName: string; grade: Grade }[],
): number {
  const scored = subjects.map(s => {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths ?? false;
    return getPointsForGrade(s.grade, isMaths);
  });
  scored.sort((a, b) => b - a);
  return scored.slice(0, 6).reduce((sum, p) => sum + p, 0);
}

function getTrajectoryInfo(points: number) {
  if (points >= 500) return TRAJECTORY_DATA[6];
  if (points >= 450) return TRAJECTORY_DATA[5];
  if (points >= 400) return TRAJECTORY_DATA[4];
  if (points >= 350) return TRAJECTORY_DATA[3];
  if (points >= 300) return TRAJECTORY_DATA[2];
  if (points >= 250) return TRAJECTORY_DATA[1];
  return TRAJECTORY_DATA[0];
}

// ─── Subject Color Map ───────────────────────────────────────────────────────

const SUBJECT_DOT: Record<string, string> = {
  'English': 'bg-blue-500', 'Irish': 'bg-emerald-500', 'Mathematics': 'bg-indigo-500',
  'French': 'bg-sky-500', 'German': 'bg-yellow-500', 'Spanish': 'bg-orange-500',
  'Physics': 'bg-cyan-500', 'Chemistry': 'bg-teal-500', 'Biology': 'bg-lime-500',
  'Applied Maths': 'bg-violet-500', 'Computer Science': 'bg-fuchsia-500', 'Ag Science': 'bg-green-500',
  'Accounting': 'bg-amber-500', 'Business': 'bg-amber-600', 'Economics': 'bg-yellow-600',
  'History': 'bg-purple-500', 'Geography': 'bg-emerald-600', 'Home Economics': 'bg-orange-400',
  'Art': 'bg-rose-400', 'Music': 'bg-pink-400',
};

function getDot(name: string) { return SUBJECT_DOT[name] || 'bg-zinc-500'; }

// ─── Component ───────────────────────────────────────────────────────────────

const PointsPassport: React.FC<PointsPassportProps> = ({ uid, profile }) => {
  const { showToast } = useToast();
  const [activeTab, setActiveTab] = useState<'overview' | 'mocks' | 'bargains'>('overview');

  // Shared mock results hook
  const mockResultsHook = useMockResults(uid);
  const loaded = mockResultsHook.isLoaded;

  // Derive MockResult[] for local display from unified mocks
  const mockResults: MockResult[] = useMemo(() => {
    return mockResultsHook.mocks.map(m => ({
      id: m.id,
      label: m.label,
      date: m.date,
      grades: m.entries.map(e => ({ subjectName: e.subjectName, grade: e.grade as Grade, level: e.level as Level })),
      totalPoints: m.totalPoints,
    }));
  }, [mockResultsHook.mocks]);

  // CAO Simulator data (Connection 4: CAO Simulator → Points Passport)
  const [caoData, setCaoData] = useState<{ whatIfScenarios: any[]; computedPoints?: { current: number; target: number } } | null>(null);

  useEffect(() => {
    if (!uid) return;
    let cancelled = false;
    getDoc(doc(db, 'progress', uid)).then(snap => {
      if (cancelled) return;
      const data = snap.data();
      if (data?.caoSimulator?.whatIfScenarios?.length || data?.computedPoints) {
        setCaoData({
          whatIfScenarios: data?.caoSimulator?.whatIfScenarios || [],
          computedPoints: data?.computedPoints,
        });
      }
    }).catch(() => {});
    return () => { cancelled = true; };
  }, [uid]);

  // Mock entry form state
  const [showMockForm, setShowMockForm] = useState(false);
  const [mockLabel, setMockLabel] = useState('');
  const [mockGrades, setMockGrades] = useState<Record<string, Grade>>({});

  // Current points from profile
  const currentPoints = useMemo(() => {
    return computeBestSixTotal(
      profile.subjects.map(s => ({ subjectName: s.subjectName, grade: s.currentGrade }))
    );
  }, [profile]);

  const targetPoints = useMemo(() => {
    return computeBestSixTotal(
      profile.subjects.map(s => ({ subjectName: s.subjectName, grade: s.targetGrade }))
    );
  }, [profile]);

  const trajectoryInfo = getTrajectoryInfo(currentPoints);
  const bargains = useMemo(() => computeBargains(profile), [profile]);

  // Pick a relevant micro-story
  const relevantStory = useMemo(() => {
    return MICRO_STORIES.reduce((best, story) => {
      const dist = Math.abs(story.from - currentPoints);
      const bestDist = Math.abs(best.from - currentPoints);
      return dist < bestDist ? story : best;
    }, MICRO_STORIES[0]);
  }, [currentPoints]);

  // Mock form handlers
  const initMockForm = () => {
    const grades: Record<string, Grade> = {};
    profile.subjects.forEach(s => { grades[s.subjectName] = s.currentGrade; });
    setMockGrades(grades);
    setMockLabel('');
    setShowMockForm(true);
  };

  const saveMock = async () => {
    const label = mockLabel.trim() || 'Mock Exam';
    const gradeEntries = profile.subjects.map(s => ({
      subjectName: s.subjectName,
      grade: mockGrades[s.subjectName] || s.currentGrade,
      level: s.level,
    }));
    const total = computeBestSixTotal(gradeEntries);
    mockResultsHook.addMockResult({
      label,
      date: new Date().toISOString().split('T')[0],
      entries: gradeEntries,
      totalPoints: total,
    });
    setShowMockForm(false);
    showToast(`${label} saved — ${total} points`, 'success');
  };

  const deleteMock = async (id: string) => {
    mockResultsHook.removeMockResult(id);
  };

  if (!loaded) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-6 h-6 border-2 rounded-full animate-spin" style={{ borderColor: '#2A7D6F', borderTopColor: 'transparent' }} />
      </div>
    );
  }

  return (
    <div className="space-y-6">

      {/* Points overview cards */}
      <div className="grid grid-cols-3 gap-3">
        <div className="rounded-xl p-4 bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
          <p className="text-[10px] font-bold uppercase tracking-widest mb-1 text-[#9A9590] dark:text-zinc-500">Current</p>
          <span className="font-apercu text-3xl font-black" style={{ color: '#2A7D6F' }}>{currentPoints}</span>
          <span className="text-sm ml-1 text-[#9A9590] dark:text-zinc-500">/625</span>
        </div>
        <div className="rounded-xl p-4" style={{ backgroundColor: '#EDF2EE', border: '0.5px solid rgba(0,0,0,0.07)' }}>
          <p className="text-[10px] font-bold uppercase tracking-widest mb-1" style={{ color: '#6B8F71' }}>Target</p>
          <span className="font-apercu text-3xl font-black" style={{ color: '#4A6B4F' }}>{targetPoints}</span>
          <span className="text-sm ml-1" style={{ color: '#6B8F71' }}>/625</span>
        </div>
        <div className="rounded-xl p-4" style={{ backgroundColor: '#FDF3E7', border: '0.5px solid rgba(0,0,0,0.07)' }}>
          <p className="text-[10px] font-bold uppercase tracking-widest mb-1" style={{ color: '#C4873B' }}>Gap</p>
          <span className="font-apercu text-3xl font-black" style={{ color: '#8B5E2A' }}>
            {targetPoints - currentPoints > 0 ? '+' : ''}{targetPoints - currentPoints}
          </span>
          <span className="text-sm ml-1" style={{ color: '#C4873B' }}>pts</span>
        </div>
      </div>

      {/* Identity reframing card */}
      <div className="rounded-xl p-5 bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
        <div className="flex items-start gap-3">
          <TrendingUp size={18} className="shrink-0 mt-0.5" style={{ color: '#2A7D6F' }} />
          <div>
            <p className="text-sm font-bold" style={{ color: '#2A7D6F' }}>
              Students scoring {trajectoryInfo.range} typically improve by {trajectoryInfo.typical} points
            </p>
            <p className="text-xs leading-relaxed mt-1 text-zinc-600 dark:text-zinc-400">
              {trajectoryInfo.message}
            </p>
          </div>
        </div>
      </div>

      {/* Tab switcher */}
      <div className="flex gap-1 p-1 bg-zinc-100 dark:bg-zinc-800/50 rounded-xl">
        {([
          { key: 'overview' as const, label: 'Overview' },
          { key: 'mocks' as const, label: 'Mock Tracker' },
          { key: 'bargains' as const, label: 'Best Bargains' },
        ]).map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`flex-1 py-2.5 px-3 rounded-lg text-sm transition-all ${
              activeTab === tab.key
                ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-medium shadow-sm'
                : 'text-zinc-500'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <AnimatePresence mode="wait">
        {/* ── Overview Tab ── */}
        {activeTab === 'overview' && (
          <MotionDiv
            key="overview"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="space-y-5"
          >
            {/* Subject breakdown */}
            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                Your Subjects
              </p>
              <div className="space-y-1.5">
                {profile.subjects.map(sub => {
                  const isMaths = LC_SUBJECTS.find(lc => lc.name === sub.subjectName)?.isMaths ?? false;
                  const currentPts = getPointsForGrade(sub.currentGrade, isMaths);
                  const targetPts = getPointsForGrade(sub.targetGrade, isMaths);
                  const gap = targetPts - currentPts;
                  return (
                    <div key={sub.subjectName} className="flex items-center gap-3 p-3 rounded-xl bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
                      <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${getDot(sub.subjectName)}`} />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200 truncate">{sub.subjectName}</p>
                        <p className="text-[11px] text-zinc-500 dark:text-zinc-400">
                          {sub.currentGrade} <ArrowRight size={10} className="inline" /> {sub.targetGrade}
                        </p>
                      </div>
                      <div className="text-right shrink-0">
                        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{currentPts} pts</p>
                        {gap > 0 && (
                          <span className="inline-block text-[10px] font-bold px-1.5 py-0.5 rounded-full" style={{ backgroundColor: '#EDF2EE', color: '#4A6B4F' }}>+{gap} possible</span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* CAO Simulator insights (Connection 4: CAO Simulator → Points Passport) */}
            {caoData && caoData.whatIfScenarios && caoData.whatIfScenarios.length > 0 && (
              <div className="rounded-xl p-4 space-y-2 bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
                <p className="text-[10px] font-bold uppercase tracking-widest" style={{ color: '#2A7D6F' }}>From Your Simulator</p>
                {caoData.whatIfScenarios.slice(0, 3).map((s: any, i: number) => (
                  <div key={i} className="flex items-center justify-between text-xs">
                    <span className="text-zinc-600 dark:text-zinc-400">
                      {s.subjectName}: {s.currentGrade} → {s.whatIfGrade}
                    </span>
                    <span className="font-bold" style={{ color: '#2A7D6F' }}>+{s.pointsGain} pts</span>
                  </div>
                ))}
                {caoData.computedPoints && (
                  <p className="text-[10px] pt-1" style={{ color: '#2A7D6F' }}>
                    Current: {caoData.computedPoints.current} pts → Target: {caoData.computedPoints.target} pts
                  </p>
                )}
              </div>
            )}

            {/* Micro-story */}
            <div className="bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-5">
              <div className="flex items-start gap-3">
                <Award size={18} className="text-amber-500 shrink-0 mt-1" />
                <div>
                  <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed italic">
                    "{relevantStory.quote}"
                  </p>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-2">
                    — {relevantStory.label} &middot; {relevantStory.from} → {relevantStory.to} pts
                  </p>
                </div>
              </div>
            </div>
          </MotionDiv>
        )}

        {/* ── Mock Tracker Tab ── */}
        {activeTab === 'mocks' && (
          <MotionDiv
            key="mocks"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="space-y-5"
          >
            {/* Trajectory chart (simple bar visualisation) */}
            {mockResults.length > 0 && (
              <div>
                <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Points Trajectory
                </p>
                <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-4">
                  <div className="flex items-end gap-2 h-32">
                    {mockResults.map((mock, idx) => {
                      const pct = Math.min(100, (mock.totalPoints / 625) * 100);
                      const prevPts = idx > 0 ? mockResults[idx - 1].totalPoints : null;
                      const delta = prevPts !== null ? mock.totalPoints - prevPts : null;
                      return (
                        <div key={mock.id} className="flex-1 flex flex-col items-center gap-1">
                          <span className="text-[10px] font-bold text-zinc-600 dark:text-zinc-400">{mock.totalPoints}</span>
                          {delta !== null && (
                            <span className="text-[9px] font-bold" style={{ color: delta >= 0 ? '#6B8F71' : '#C4873B' }}>
                              {delta >= 0 ? '+' : ''}{delta}
                            </span>
                          )}
                          <MotionDiv
                            className="w-full rounded-t-lg min-h-[4px]"
                            style={{ backgroundColor: '#2A7D6F' }}
                            initial={{ height: 0 }}
                            animate={{ height: `${pct}%` }}
                            transition={{ delay: idx * 0.1, duration: 0.5 }}
                          />
                          <span className="text-[9px] text-zinc-400 dark:text-zinc-500 text-center leading-tight mt-1">
                            {mock.label}
                          </span>
                        </div>
                      );
                    })}
                    {/* Current grade marker */}
                    <div className="flex-1 flex flex-col items-center gap-1">
                      <span className="text-[10px] font-bold" style={{ color: '#2A7D6F' }}>{currentPoints}</span>
                      <MotionDiv
                        className="w-full rounded-t-lg min-h-[4px] border-2 border-dashed"
                        style={{ backgroundColor: '#4DB8A4', borderColor: '#2A7D6F' }}
                        initial={{ height: 0 }}
                        animate={{ height: `${Math.min(100, (currentPoints / 625) * 100)}%` }}
                        transition={{ delay: mockResults.length * 0.1, duration: 0.5 }}
                      />
                      <span className="text-[9px] text-center leading-tight mt-1 font-bold" style={{ color: '#2A7D6F' }}>Now</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Mock results list */}
            {mockResults.length > 0 && (
              <div className="space-y-2">
                <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
                  Recorded Mocks
                </p>
                {mockResults.map((mock) => (
                  <div key={mock.id} className="flex items-center gap-3 p-3 rounded-xl bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}>
                    <Calendar size={14} className="shrink-0 text-[#9A9590] dark:text-zinc-500" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">{mock.label}</p>
                      <p className="text-[11px] text-[#9A9590] dark:text-zinc-500">{mock.date}</p>
                    </div>
                    <span className="text-sm font-bold" style={{ color: '#2A7D6F' }}>{mock.totalPoints} pts</span>
                    <button
                      onClick={() => deleteMock(mock.id)}
                      className="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                    >
                      <Trash2 size={14} className="text-zinc-400" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            {mockResults.length === 0 && !showMockForm && (
              <div className="text-center py-8">
                <Calendar size={32} className="text-zinc-300 dark:text-zinc-600 mx-auto mb-3" />
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-1">No mocks recorded yet</p>
                <p className="text-xs text-zinc-400 dark:text-zinc-500">Track your mock results to see your trajectory over time.</p>
              </div>
            )}

            {/* Add mock button / form */}
            {!showMockForm ? (
              <button
                onClick={initMockForm}
                className="w-full flex items-center justify-center gap-2 py-3 rounded-xl text-sm font-bold text-white transition-colors"
                style={{ backgroundColor: '#2A7D6F' }}
              >
                <Plus size={16} /> Record Mock Results
              </button>
            ) : (
              <MotionDiv
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-5 space-y-4"
              >
                <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">Record Mock Results</p>

                {/* Label selector */}
                <div className="space-y-2">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Exam Name</p>
                  <div className="flex flex-wrap gap-2">
                    {MOCK_PRESETS.map(preset => (
                      <button
                        key={preset}
                        onClick={() => setMockLabel(preset)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                          mockLabel === preset
                            ? 'text-white'
                            : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                        }`}
                        style={mockLabel === preset ? { backgroundColor: '#2A7D6F' } : undefined}
                      >
                        {preset}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Grade inputs per subject */}
                <div className="space-y-3">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Grades</p>
                  {profile.subjects.map(sub => {
                    const grades = getGradesForLevel(sub.level);
                    return (
                      <div key={sub.subjectName} className="space-y-1.5">
                        <div className="flex items-center gap-2">
                          <span className={`w-2 h-2 rounded-full ${getDot(sub.subjectName)}`} />
                          <span className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">{sub.subjectName}</span>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {grades.map(g => (
                            <button
                              key={g}
                              onClick={() => setMockGrades(prev => ({ ...prev, [sub.subjectName]: g }))}
                              className={`px-2 py-1 rounded-md text-xs font-bold transition-all ${
                                mockGrades[sub.subjectName] === g
                                  ? 'text-white shadow-sm'
                                  : 'bg-zinc-50 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-700'
                              }`}
                              style={mockGrades[sub.subjectName] === g ? { backgroundColor: '#2A7D6F' } : undefined}
                            >
                              {g}
                            </button>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Save / Cancel */}
                <div className="flex gap-3">
                  <button
                    onClick={saveMock}
                    className="flex-1 py-2.5 rounded-xl text-sm font-bold text-white transition-colors"
                    style={{ backgroundColor: '#2A7D6F' }}
                  >
                    Save Mock
                  </button>
                  <button
                    onClick={() => setShowMockForm(false)}
                    className="px-4 py-2.5 rounded-xl text-sm font-medium text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </MotionDiv>
            )}
          </MotionDiv>
        )}

        {/* ── Bargains Tab ── */}
        {activeTab === 'bargains' && (
          <MotionDiv
            key="bargains"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="space-y-5"
          >
            <div className="flex items-start gap-3 p-4 bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-800/30 rounded-xl">
              <Zap size={16} className="text-amber-500 shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-bold text-amber-700 dark:text-amber-300">Best Points Bargains</p>
                <p className="text-xs text-amber-600 dark:text-amber-400 leading-relaxed mt-1">
                  These are the grade improvements that give you the most points for the least effort. Focus here first.
                </p>
              </div>
            </div>

            {bargains.length > 0 ? (
              <div className="space-y-2">
                {bargains.map((b, idx) => (
                  <MotionDiv
                    key={b.subjectName}
                    initial={{ opacity: 0, x: -12 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="p-4 rounded-xl bg-white/60 dark:bg-white/5 border border-zinc-200/60 dark:border-white/10"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-lg font-bold text-amber-500 w-6 text-center">#{idx + 1}</span>
                      <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${getDot(b.subjectName)}`} />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{b.subjectName}</p>
                        <p className="text-[11px] text-zinc-500 dark:text-zinc-400">
                          {b.fromGrade} <ArrowRight size={10} className="inline" /> {b.toGrade}
                        </p>
                      </div>
                      <div className="text-right shrink-0">
                        <span className="text-sm font-bold px-2.5 py-1 rounded-full" style={{ backgroundColor: '#EDF2EE', color: '#4A6B4F' }}>
                          +{b.pointsGain} pts
                        </span>
                      </div>
                    </div>
                    <div className="mt-2 ml-9 flex items-center gap-3">
                      <span className="text-[11px] text-zinc-400 dark:text-zinc-500">
                        Estimated effort: {b.effortHint}
                      </span>
                      {b.isMathsBonus && (
                        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400">
                          Unlocks +25 Maths Bonus!
                        </span>
                      )}
                    </div>
                  </MotionDiv>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Star size={32} className="text-zinc-300 dark:text-zinc-600 mx-auto mb-3" />
                <p className="text-sm text-zinc-500 dark:text-zinc-400">
                  You're already at your best grades in every subject. Amazing!
                </p>
              </div>
            )}

            {/* Total potential gain */}
            {bargains.length > 0 && (
              <div className="rounded-xl p-4" style={{ backgroundColor: '#EDF2EE', border: '0.5px solid rgba(0,0,0,0.07)' }}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Rocket size={16} style={{ color: '#6B8F71' }} />
                    <span className="text-sm font-bold" style={{ color: '#4A6B4F' }}>
                      Total potential from top 3 bargains
                    </span>
                  </div>
                  <span className="text-lg font-bold" style={{ color: '#4A6B4F' }}>
                    +{bargains.slice(0, 3).reduce((sum, b) => sum + b.pointsGain, 0)} pts
                  </span>
                </div>
                <p className="text-xs mt-1" style={{ color: '#6B8F71' }}>
                  That would take you from {currentPoints} to {currentPoints + bargains.slice(0, 3).reduce((sum, b) => sum + b.pointsGain, 0)} points.
                </p>
              </div>
            )}
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

export default PointsPassport;
