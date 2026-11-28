/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import LaunchpadSelect from './launchpad/LaunchpadSelect';
import React, { useState, useMemo, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { TrendingUp, Plus, Trash2, ArrowRight, Shield, Target, Pencil } from 'lucide-react';
import {
  type StudentSubjectProfile, type Grade, type Level,
  LC_SUBJECTS, getPointsForGrade, getGradesForLevel, targetGradesFor,

  computeBargains,
} from './subjectData';
import {
  type ScenarioSlot, type ScenarioMap, type ScenarioGradeEntry,
  SCENARIO_SLOTS, loadScenarios, saveScenario, clearScenario,
  computeBestSixTotal, bestLeverToward,
} from './pointsScenarioStore';
import { useToast } from './Toast';
import { useInnovationData } from '../contexts/InnovationDataContext';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { logError } from '../utils/logError';
import { LoadingState } from './ui/SystemState';
import { Confirm } from './ui/Sheet';
import { Button, Glyph, IconButton, TextButton } from './ui/Button';
import { Menu } from './ui/Menu';
import { List, PaperSheet, Row } from './ui/List';
import { ChoiceRuler, ChoiceTile } from './ui/Choice';
import './points-passport-7.css';
import { useProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';

// ─── Types ───────────────────────────────────────────────────────────────────

interface PointsPassportProps {
  uid: string;
  profile: StudentSubjectProfile;
  onOpenSettings?: () => void;
  initialTab?: PassportTab;
  /** Landing preview: use My subjects for the overview and keep the simulator focused on What If. */
  lockSimulatorOverview?: boolean;
  onProfileChange?: (profile: StudentSubjectProfile) => void;
}

type PassportTab = 'overview' | 'mocks' | 'planner' | 'scenarios' | 'bargains';

const CAOPointsSimulator = React.lazy(() => import('./CAOPointsSimulator'));

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


// Motivational micro-stories


// Scenario runway slot metadata (feature F7). computeBestSixTotal lives in
// pointsScenarioStore so the pure math is unit-testable.
const SLOT_META: Record<ScenarioSlot, { label: string; description: string; Icon: typeof Shield }> = {
  safe: { label: 'Safe', description: 'Grades you\'re confident of', Icon: Shield },
  target: { label: 'Target', description: 'Your realistic goal', Icon: Target },
  stretch: { label: 'Stretch', description: 'If everything clicks', Icon: TrendingUp },
};

// ─── Utility ─────────────────────────────────────────────────────────────────

// ─── Component ───────────────────────────────────────────────────────────────

const PointsPassport: React.FC<PointsPassportProps> = ({ uid, profile, onOpenSettings, onProfileChange, initialTab = 'overview', lockSimulatorOverview = false }) => {
  const { showToast } = useToast();
  const { rawProgressDoc } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const [activeTab, setActiveTab] = useState<PassportTab>(initialTab);

  // One app-wide academic record. War Zone, the CAO Simulator and Points
  // Passport must never instantiate competing copies of mock history.
  const { mockResults: mockResultsHook } = useInnovationData();
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
    if (isDemo) {
      const simulator = rawProgressDoc.caoSimulator as { whatIfScenarios?: any[] } | undefined;
      const computedPoints = rawProgressDoc.computedPoints as { current: number; target: number } | undefined;
      setCaoData(simulator?.whatIfScenarios?.length || computedPoints
        ? {
            whatIfScenarios: simulator?.whatIfScenarios || [],
            computedPoints,
          }
        : null);
      return;
    }
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
    }).catch((e) => logError('PointsPassport.loadCao', e));
    return () => { cancelled = true; };
  }, [uid, isDemo, rawProgressDoc.caoSimulator, rawProgressDoc.computedPoints]);

  // Mock entry form state
  const [showMockForm, setShowMockForm] = useState(false);
  const [mockLabel, setMockLabel] = useState('');
  const [mockGrades, setMockGrades] = useState<Record<string, Grade>>({});
  const [pendingDeleteMock, setPendingDeleteMock] = useState<MockResult | null>(null);

  // Scenario runway state (feature F7) — local-only, per uid
  const [scenarios, setScenarios] = useState<ScenarioMap>({});
  const [editingSlot, setEditingSlot] = useState<ScenarioSlot | null>(null);
  const [scenarioGrades, setScenarioGrades] = useState<Record<string, Grade>>({});

  useEffect(() => {
    setScenarios(loadScenarios(uid));
    setEditingSlot(null);
  }, [uid]);

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


  // Re-rank the authored effort hints using the only gain that matters to the
  // student: the change to their actual best-six total. A raw subject increase
  // can be worth zero CAO points when that subject remains outside the best six.
  const bargains = useMemo(() => {
    const baselineEntries = profile.subjects.map(s => ({ subjectName: s.subjectName, grade: s.currentGrade }));
    const baselineTotal = computeBestSixTotal(baselineEntries);
    return computeBargains(profile)
      .map(bargain => {
        const changed = baselineEntries.map(entry => entry.subjectName === bargain.subjectName
          ? { ...entry, grade: bargain.toGrade }
          : entry);
        return { ...bargain, pointsGain: computeBestSixTotal(changed) - baselineTotal };
      })
      .filter(bargain => bargain.pointsGain > 0)
      .sort((a, b) => b.pointsGain - a.pointsGain);
  }, [profile]);

  const topThreePotential = useMemo(() => {
    const changedGrades = new Map(bargains.slice(0, 3).map(b => [b.subjectName, b.toGrade]));
    const changed = profile.subjects.map(s => ({
      subjectName: s.subjectName,
      grade: changedGrades.get(s.subjectName) ?? s.currentGrade,
    }));
    return computeBestSixTotal(changed) - currentPoints;
  }, [bargains, profile, currentPoints]);

  // Pick a relevant micro-story


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
      resultKind: 'full',
    });
    setShowMockForm(false);
    showToast(`${label} saved — ${total} points`, 'success');
  };

  const deleteMock = () => {
    if (!pendingDeleteMock) return;
    mockResultsHook.removeMockResult(pendingDeleteMock.id);
    showToast(`${pendingDeleteMock.label} removed`, 'success');
    setPendingDeleteMock(null);
  };

  // ── Scenario runway (feature F7) ──
  // Baseline = the student's latest recorded mock (mocks are stored
  // newest-first). Their own data, never a prediction. Falls back to the
  // profile's current grades when no mocks are recorded yet.
  const scenarioBaseline = useMemo(() => {
    const latestMock = mockResults.length > 0 ? mockResults[0] : null;
    if (latestMock) {
      return {
        entries: latestMock.grades as ScenarioGradeEntry[],
        total: latestMock.totalPoints,
        label: latestMock.label,
        isMock: true,
      };
    }
    return {
      entries: profile.subjects.map(s => ({ subjectName: s.subjectName, grade: s.currentGrade, level: s.level })) as ScenarioGradeEntry[],
      total: currentPoints,
      label: 'your current grades',
      isMock: false,
    };
  }, [mockResults, profile, currentPoints]);

  const startEditScenario = (slot: ScenarioSlot) => {
    const existing = scenarios[slot];
    const grades: Record<string, Grade> = {};
    profile.subjects.forEach(s => {
      const saved = existing?.grades.find(g => g.subjectName === s.subjectName)?.grade;
      grades[s.subjectName] = saved || s.currentGrade;
    });
    setScenarioGrades(grades);
    setEditingSlot(slot);
  };

  const scenarioEntriesFromForm = (): ScenarioGradeEntry[] =>
    profile.subjects.map(s => ({
      subjectName: s.subjectName,
      grade: scenarioGrades[s.subjectName] || s.currentGrade,
      level: s.level,
    }));

  const saveScenarioForm = () => {
    if (!editingSlot) return;
    const grades = scenarioEntriesFromForm();
    setScenarios(saveScenario(uid, {
      slot: editingSlot,
      grades,
      savedAt: new Date().toISOString().split('T')[0],
    }));
    setEditingSlot(null);
    showToast(`${SLOT_META[editingSlot].label} scenario saved — ${computeBestSixTotal(grades)} points`, 'success');
  };

  const cloneScenarioFromCurrent = (slot: ScenarioSlot) => {
    const grades: ScenarioGradeEntry[] = profile.subjects.map(s => ({
      subjectName: s.subjectName,
      grade: s.currentGrade,
      level: s.level,
    }));
    setScenarios(saveScenario(uid, {
      slot,
      grades,
      savedAt: new Date().toISOString().split('T')[0],
    }));
    showToast(`${SLOT_META[slot].label} scenario started from your current grades`, 'success');
  };

  const deleteScenario = (slot: ScenarioSlot) => {
    setScenarios(clearScenario(uid, slot));
    if (editingSlot === slot) setEditingSlot(null);
  };

  if (!loaded) {
    return <LoadingState label="Loading your points passport" />;
  }

  return (
    <>
    <div className="pp7">

      {/* The one sheet: the total written "465 / 625", the target, the gap and the bar with its
          tick (boards c-tools1-passport, r5-points-passport). Not on What if?, which pins its own. */}
      {activeTab !== 'planner' && <PaperSheet className="pp7-hero" label="Your points">
        <div className="pp7-hero-total"><p className="t-label pp7-label">Based on your current grades</p><p className="pp7-total"><span>{currentPoints}</span><span className="pp7-of"> / 625</span></p><p className="t-meta">Your best six, with the maths bonus where eligible.</p></div>
        <div className="pp7-hero-side"><div className="pp7-target"><span>Your target <b>{targetPoints}</b></span><span>Gap <b>{Math.max(0,targetPoints-currentPoints)} points</b></span></div>
          <div className="pp7-bar"><span style={{width:`${Math.min(100,currentPoints/625*100)}%`}} /><i style={{left:`${Math.min(99,targetPoints/625*100)}%`}} aria-label={`Target ${targetPoints}`} /></div><p className="t-meta">Your target is a goal you set, not a prediction.</p>
        </div>
      </PaperSheet>}
      {/* The five parts in one menu: "My subjects · 1 of 5". */}
      <Menu label="Points Passport sections" count block className="pp7-parts" value={activeTab} onChange={next => setActiveTab(next)}
        options={[{ value: 'overview' as PassportTab, label: 'My subjects' }, { value: 'planner' as PassportTab, label: 'What if?' }, { value: 'scenarios' as PassportTab, label: 'Scenarios' }, { value: 'mocks' as PassportTab, label: 'Mock Tracker' }, { value: 'bargains' as PassportTab, label: 'Best Moves' }]} />
      {/* Tab content */}
      <AnimatePresence mode="wait">
        {activeTab === 'planner' && (
          <MotionDiv
            key="planner"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
          >
            <React.Suspense fallback={<LoadingState label="Loading your grade planner" />}>
              <CAOPointsSimulator
                profile={profile}
                uid={uid}
                initialTab="what-if"
                overviewLocked={lockSimulatorOverview}
                passport
                onOpenSettings={onOpenSettings ?? (() => setActiveTab('overview'))}
              />
            </React.Suspense>
          </MotionDiv>
        )}
        {/* ── Overview Tab ── */}
        {activeTab === 'overview' && (
          <MotionDiv
            key="overview"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="space-y-5"
          >
            <div className="pp7-split">
              <section className="pp7-subjects"><div className="pp7-head"><h2 className="t-heading">Your subject contributions</h2>{onOpenSettings && <TextButton onClick={onOpenSettings}>Edit subjects</TextButton>}</div>
                <div className="pp7-grades"><div className="pp7-grade pp7-grade--head t-label"><span>Subject</span><span>Current</span><span>Target</span><span>Gain</span></div>
                {profile.subjects.map(sub => {
                  const isMaths = LC_SUBJECTS.find(lc => lc.name === sub.subjectName)?.isMaths ?? false;
                  const currentPts = getPointsForGrade(sub.currentGrade, isMaths);
                  const targetPts = getPointsForGrade(sub.targetGrade, isMaths);
                  const update = (field: 'currentGrade' | 'targetGrade', grade: Grade) => onProfileChange?.({...profile, subjects:profile.subjects.map(s => s.subjectName === sub.subjectName ? {...s,[field]:grade} : s)});
                  return <div className="pp7-grade" key={sub.subjectName}><div className="pp7-grade-name"><span>{sub.subjectName}</span><div className="pp7-grade-bar"><span style={{width:`${currentPts/125*100}%`}} /></div></div>
                    <LaunchpadSelect aria-label={`${sub.subjectName} current grade`} value={sub.currentGrade} disabled={!onProfileChange} onChange={e => update('currentGrade',e.target.value as Grade)}>{getGradesForLevel(sub.level).map(g => <option key={g}>{g}</option>)}</LaunchpadSelect>
                    <LaunchpadSelect aria-label={`${sub.subjectName} target grade`} value={sub.targetGrade} disabled={!onProfileChange} onChange={e => update('targetGrade',e.target.value as Grade)}>{targetGradesFor(sub.level).map(g => <option key={g}>{g}</option>)}</LaunchpadSelect>
                    <span className="pp7-gain t-readout">{targetPts-currentPts > 0 ? '+' : ''}{targetPts-currentPts}</span>
                  </div>;
                })}</div><p className="t-meta pp7-note">Subject gains are before best-six selection. Your total counts only your best six.</p>
              </section>
              <aside className="pp7-try"><p className="t-label pp7-label">Try a possibility</p><h2 className="t-title pp7-try-title">What would one grade change?</h2><p className="t-sub">Use What if? to explore a different set of grades without changing your current grades.</p><Button kind="main" size="lg" block arrow="forward" onClick={() => setActiveTab('planner')}>Explore What If?</Button></aside>
            </div>
            {/* CAO Simulator insights (Connection 4: CAO Simulator → Points Passport) */}
            {caoData && caoData.whatIfScenarios && caoData.whatIfScenarios.length > 0 && (
              <div className="pp7-section">
                <p className="t-label pp7-label">From your simulator</p>
                {caoData.whatIfScenarios.slice(0, 3).map((s: any, i: number) => (
                  <div key={i} className="flex items-center justify-between text-xs">
                    <span className="t-sub">
                      {s.subjectName}: {s.currentGrade} → {s.whatIfGrade}
                    </span>
                    <span className="t-readout">+{s.pointsGain} pts</span>
                  </div>
                ))}
                {caoData.computedPoints && (
                  <p className="t-meta">
                    Current: {caoData.computedPoints.current} pts → Target: {caoData.computedPoints.target} pts
                  </p>
                )}
              </div>
            )}

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
            {/* The points trajectory: the student's own totals drawn (orange is their own value). */}
            {mockResults.length > 0 && (
              <section className="pp7-section" aria-label="Points trajectory">
                <p className="t-label pp7-label">Points trajectory</p>
                <div className="pp7-chart">
                  {/* mockResults is newest-first: oldest to newest left to right, each delta against the previous. */}
                  {[...mockResults].reverse().map((mock, idx, chrono) => {
                    const pct = Math.min(100, (mock.totalPoints / 625) * 100);
                    const prevPts = idx > 0 ? chrono[idx - 1].totalPoints : null;
                    const delta = prevPts !== null ? mock.totalPoints - prevPts : null;
                    return (
                      <div key={mock.id}>
                        <span className="t-readout">{mock.totalPoints}</span>
                        {delta !== null && <span className="t-meta">{delta >= 0 ? '+' : ''}{delta}</span>}
                        <MotionDiv className="pp7-chart-bar" initial={{ height: 0 }} animate={{ height: `${pct}%` }} transition={{ delay: idx * 0.1, duration: 0.5 }} />
                        <span className="t-meta">{mock.label}</span>
                      </div>
                    );
                  })}
                  <div>
                    <span className="t-readout">{currentPoints}</span>
                    <MotionDiv className="pp7-chart-bar pp7-chart-bar--now" initial={{ height: 0 }} animate={{ height: `${Math.min(100, (currentPoints / 625) * 100)}%` }} transition={{ delay: mockResults.length * 0.1, duration: 0.5 }} />
                    <span className="t-meta">Now</span>
                  </div>
                </div>
              </section>
            )}

            {mockResults.length > 0 && (
              <section className="pp7-section" aria-label="Recorded mocks">
                <p className="t-label pp7-label">Recorded mocks</p>
                {mockResults.map((mock) => (
                  <div key={mock.id} className="pp7-mock-row">
                    <div><span>{mock.label}</span><span className="t-meta">{mock.date}</span></div>
                    <span className="t-readout">{mock.totalPoints} points</span>
                    <IconButton label={`Remove ${mock.label}`} icon={<Glyph icon={Trash2} size={20} />} onClick={() => setPendingDeleteMock(mock)} />
                  </div>
                ))}
              </section>
            )}

            {mockResults.length === 0 && !showMockForm && (
              <div className="pp7-section">
                <h3 className="t-heading">No mocks recorded yet</h3>
                <p className="t-sub">Track your mock results to see your trajectory over time.</p>
              </div>
            )}

            {!showMockForm ? (
              <Button kind="main" size="lg" block onClick={initMockForm}><span className="pp7-inline"><Plus size={20} aria-hidden="true" />Record mock results</span></Button>
            ) : (
              <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="pp7-form">
                <h3 className="t-heading">Record mock results</h3>
                <div className="pp7-section">
                  <p className="t-label pp7-label">Exam name</p>
                  <div className="pp7-presets" role="group" aria-label="Exam name">
                    {MOCK_PRESETS.map(preset => <ChoiceTile key={preset} compact kind="toggle" chosen={mockLabel === preset} label={preset} onClick={() => setMockLabel(preset)} />)}
                  </div>
                </div>
                <div className="pp7-section">
                  <p className="t-label pp7-label">Grades</p>
                  {profile.subjects.map(sub => (
                    <div key={sub.subjectName} className="pp7-wsub">
                      <span className="pp7-wsub-name">{sub.subjectName}</span>
                      <ChoiceRuler label={`${sub.subjectName} mock grade`} value={mockGrades[sub.subjectName] ?? ''} onChange={g => setMockGrades(prev => ({ ...prev, [sub.subjectName]: g as Grade }))}
                        options={getGradesForLevel(sub.level).map(g => ({ value: g, label: g, name: `${sub.subjectName} ${g}` }))} />
                    </div>
                  ))}
                </div>
                <div className="pp7-actions">
                  <Button kind="main" size="lg" block onClick={saveMock}>Save mock</Button>
                  <TextButton tone="quiet" onClick={() => setShowMockForm(false)}>Cancel</TextButton>
                </div>
              </MotionDiv>
            )}
          </MotionDiv>
        )}

        {/* ── Scenarios Tab (feature F7: Safe / Target / Stretch runway) ── */}
        {activeTab === 'scenarios' && (
          <MotionDiv
            key="scenarios"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="space-y-5"
          >
            {/* Honesty framing: deltas compare against the student's own mocks */}
            <section className="pp7-section" aria-label="Scenario runway">
              <h3 className="t-heading">Scenario runway</h3>
              <p className="t-sub">
                Sketch a Safe, Target and Stretch grade set and compare them side by side.
                Each delta is measured against {scenarioBaseline.isMock
                  ? <>your latest recorded mock ({scenarioBaseline.label})</>
                  : 'your current self-assessed grades'} — that&apos;s your own results so far, not a prediction of how the real exam will go.
              </p>
              <div className="pp7-mock-row">
                <div><span className="t-sub">{scenarioBaseline.isMock ? `Latest recorded mock · ${scenarioBaseline.label}` : 'Current grades from your subject profile'}</span></div>
                <span className="t-readout">{scenarioBaseline.total} points</span>
              </div>
            </section>

            <div className="pp7-slots">
              {SCENARIO_SLOTS.map(slot => {
                const meta = SLOT_META[slot];
                const SlotIcon = meta.Icon;
                const sc = scenarios[slot];
                const total = sc ? computeBestSixTotal(sc.grades) : null;
                const delta = total !== null ? total - scenarioBaseline.total : null;
                const lever = sc ? bestLeverToward(scenarioBaseline.entries, sc.grades) : null;
                return (
                  <section key={slot} className="pp7-slot" aria-label={`${meta.label} scenario`}>
                    <div className="pp7-slot-head">
                      <SlotIcon size={16} aria-hidden="true" />
                      <span className="t-label">{meta.label}</span>
                      {sc && <>
                        <IconButton label={`Edit ${meta.label} scenario`} icon={<Glyph icon={Pencil} size={20} />} onClick={() => startEditScenario(slot)} />
                        <IconButton label={`Clear ${meta.label} scenario`} icon={<Glyph icon={Trash2} size={20} />} onClick={() => deleteScenario(slot)} />
                      </>}
                    </div>
                    <p className="t-meta">{meta.description}</p>
                    {sc && total !== null && delta !== null ? (
                      <>
                        <p className="pp7-slot-total">{total}<span className="pp7-of"> / 625</span></p>
                        <p className="t-sub">
                          {delta > 0
                            ? `+${delta} vs ${scenarioBaseline.isMock ? 'latest mock' : 'current'}`
                            : delta === 0
                              ? `Level with your ${scenarioBaseline.isMock ? 'latest mock' : 'current grades'}`
                              : `Already ${-delta} ahead on your ${scenarioBaseline.isMock ? 'mocks' : 'grades'}`}
                        </p>
                        {lever && (
                          <p className="t-meta">
                            Biggest single step: {lever.subjectName} {lever.fromGrade} <ArrowRight size={12} className="inline" aria-label="to" /> {lever.toGrade} +{lever.pointsGain} points
                          </p>
                        )}
                      </>
                    ) : (
                      <div className="pp7-actions">
                        <Button block onClick={() => startEditScenario(slot)}>Set grades</Button>
                        <TextButton tone="quiet" onClick={() => cloneScenarioFromCurrent(slot)}>Start from current grades</TextButton>
                      </div>
                    )}
                  </section>
                );
              })}
            </div>

            {/* Scenario grade editor */}
            {editingSlot && (
              <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="pp7-form">
                <div className="pp7-head">
                  <h3 className="t-heading">{SLOT_META[editingSlot].label} scenario — pick a grade per subject</h3>
                  <span className="t-readout">{computeBestSixTotal(scenarioEntriesFromForm())} points</span>
                </div>
                {profile.subjects.map(sub => (
                  <div key={sub.subjectName} className="pp7-wsub">
                    <span className="pp7-wsub-name">{sub.subjectName}</span>
                    <ChoiceRuler label={`${sub.subjectName} scenario grade`} value={scenarioGrades[sub.subjectName] ?? ''} onChange={g => setScenarioGrades(prev => ({ ...prev, [sub.subjectName]: g as Grade }))}
                      options={getGradesForLevel(sub.level).map(g => ({ value: g, label: g, name: `${sub.subjectName} ${g}` }))} />
                  </div>
                ))}
                <div className="pp7-actions">
                  <Button kind="main" size="lg" block onClick={saveScenarioForm}>Save {SLOT_META[editingSlot].label} scenario</Button>
                  <TextButton tone="quiet" onClick={() => setEditingSlot(null)}>Cancel</TextButton>
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
            <header className="pp7-section">
              <p className="t-label pp7-label">Where points move</p>
              <h3 className="t-title">Best points bargains</h3>
              <p className="t-sub">Grade moves with a strong points return for the effort involved. Use these as priorities, not promises.</p>
            </header>

            {bargains.length > 0 ? (
              <List label="Best points bargains" className="pp7-moves">
                {bargains.map((b, idx) => (
                  <Row key={b.subjectName} lead={`#${idx + 1}`} title={b.subjectName}
                    meta={`${b.fromGrade} → ${b.toGrade} · Estimated effort: ${b.effortHint}${b.isMathsBonus ? ' · Unlocks the +25 maths bonus' : ''}`}
                    value={`+${b.pointsGain} points`} />
                ))}
              </List>
            ) : (
              <div className="pp7-section">
                <p className="t-sub">You're already at your best grades in every subject. Amazing!</p>
              </div>
            )}

            {bargains.length > 0 && (
              <section className="pp7-section" aria-label="Three-move preview">
                <div className="pp7-head"><div><p className="t-label pp7-label">Three-move preview</p><p className="t-body">Total potential from the top three</p></div><span className="t-readout">+{topThreePotential} points</span></div>
                <p className="t-meta">That would take you from {currentPoints} to {currentPoints + topThreePotential} points.</p>
              </section>
            )}
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
    <Confirm open={pendingDeleteMock !== null} sentence="Remove this mock result?"
      detail={pendingDeleteMock ? `${pendingDeleteMock.label} and its subject grades will be removed from your mock history. This cannot be undone. Your current grades and saved scenarios will not change.` : undefined}
      keepLabel="Keep result" onKeep={() => setPendingDeleteMock(null)} dangerLabel="Remove result" onDanger={deleteMock} />
    </>
  );
};

export default PointsPassport;
