/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  TrendingDown, Calculator, BarChart3, Scale, GitBranch, Layers, Target,
  ChevronDown, ChevronUp, AlertTriangle, CheckCircle2, ArrowRight, Minus, Plus
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { redTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useModuleResponses } from '../hooks/useModuleResponses';

const theme = redTheme;
const MotionDiv = motion.div as any;

// ─── DATA ────────────────────────────────────────────────────────────────────

const GRADES = ['H1','H2','H3','H4','H5','H6','H7','H8'] as const;
const GRADE_POINTS: Record<string, number> = { H1:100, H2:88, H3:77, H4:66, H5:56, H6:46, H7:37, H8:0 };

const SUBJECTS_DATA = [
  { name: 'Applied Maths', h1Rate: 27, objectivity: 95, group: 'maths', synergies: ['Mathematics','Physics'] },
  { name: 'Physics', h1Rate: 20, objectivity: 90, group: 'stem', synergies: ['Mathematics','Applied Maths','Chemistry'] },
  { name: 'Chemistry', h1Rate: 19, objectivity: 88, group: 'stem', synergies: ['Physics','Biology','Ag Science'] },
  { name: 'Accounting', h1Rate: 16, objectivity: 85, group: 'business', synergies: ['Business','Economics'] },
  { name: 'Mathematics', h1Rate: 16, objectivity: 95, group: 'maths', synergies: ['Applied Maths','Physics','Economics'], isMaths: true },
  { name: 'Biology', h1Rate: 15, objectivity: 75, group: 'life-science', synergies: ['Chemistry','Ag Science','Home Economics'] },
  { name: 'Spanish', h1Rate: 14, objectivity: 60, group: 'language', synergies: ['French','German'] },
  { name: 'Economics', h1Rate: 13, objectivity: 70, group: 'business', synergies: ['Mathematics','Business','Accounting'] },
  { name: 'German', h1Rate: 12, objectivity: 60, group: 'language', synergies: ['French','Spanish'] },
  { name: 'Ag Science', h1Rate: 12, objectivity: 70, group: 'life-science', synergies: ['Biology','Chemistry','Geography'] },
  { name: 'French', h1Rate: 11, objectivity: 60, group: 'language', synergies: ['Spanish','German'] },
  { name: 'Home Economics', h1Rate: 10, objectivity: 55, group: 'practical', synergies: ['Biology'] },
  { name: 'Business', h1Rate: 10, objectivity: 65, group: 'business', synergies: ['Economics','Accounting'] },
  { name: 'Construction Studies', h1Rate: 9, objectivity: 72, group: 'practical', synergies: ['DCG','Engineering'] },
  { name: 'DCG', h1Rate: 9, objectivity: 78, group: 'practical', synergies: ['Construction Studies','Engineering'] },
  { name: 'Music', h1Rate: 8, objectivity: 50, group: 'creative', synergies: [] },
  { name: 'Irish', h1Rate: 8, objectivity: 55, group: 'language', synergies: [] },
  { name: 'Politics & Society', h1Rate: 7, objectivity: 40, group: 'humanities', synergies: ['History','Geography'] },
  { name: 'History', h1Rate: 6, objectivity: 35, group: 'humanities', synergies: ['Politics & Society','English'] },
  { name: 'English', h1Rate: 7, objectivity: 25, group: 'humanities', synergies: ['History'] },
  { name: 'Geography', h1Rate: 5, objectivity: 40, group: 'humanities', synergies: ['Ag Science','Biology'] },
  { name: 'Art', h1Rate: 4, objectivity: 20, group: 'creative', synergies: [] },
];

// ─── INTERACTIVE 1: Grade Waterfall Calculator ──────────────────────────────

const GradeWaterfall = () => {
  const defaultGrades = ['H1','H1','H1','H1','H1','H1','H1'];
  const defaultSubjects = ['Mathematics','English','Irish','Physics','Chemistry','Biology','French'];
  const [grades, setGrades] = useState<string[]>(defaultGrades);

  const subjectPoints = grades.map((grade, i) => {
    let pts = GRADE_POINTS[grade] || 0;
    if (i === 0 && ['H1','H2','H3','H4','H5','H6'].includes(grade)) pts += 25; // Maths bonus
    return pts;
  });

  const sorted = [...subjectPoints].sort((a, b) => b - a);
  const bestSix = sorted.slice(0, 6);
  const total = bestSix.reduce((sum, p) => sum + p, 0);
  const maxTotal = 625;

  const setGrade = (idx: number, grade: string) => {
    const next = [...grades];
    next[idx] = grade;
    setGrades(next);
  };

  return (
    <div className="my-10 p-6 md:p-8 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">Grade Waterfall Calculator</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Change the grades below and watch your points total respond. Notice how steep the H1→H2 cliff is.</p>

      <div className="space-y-3 mb-8">
        {defaultSubjects.map((subj, idx) => {
          const pts = subjectPoints[idx];
          const isInBestSix = bestSix.includes(pts) && bestSix.indexOf(pts) !== -1;
          const isH1 = grades[idx] === 'H1';
          const isMaths = idx === 0;

          return (
            <div key={subj} className="flex items-center gap-3">
              <span className="w-28 text-xs font-semibold text-zinc-500 dark:text-zinc-400 shrink-0 truncate">{subj}{isMaths ? ' *' : ''}</span>
              <select
                value={grades[idx]}
                onChange={(e) => setGrade(idx, e.target.value)}
                className="px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-sm font-medium text-zinc-900 dark:text-white"
              >
                {GRADES.map(g => <option key={g} value={g}>{g}</option>)}
              </select>
              <div className="flex-grow h-8 bg-zinc-100 dark:bg-zinc-800 rounded-lg overflow-hidden relative">
                <motion.div
                  className={`h-full rounded-lg ${isH1 ? 'bg-emerald-500' : grades[idx] === 'H2' ? 'bg-amber-400' : 'bg-red-400'}`}
                  animate={{ width: `${(pts / 125) * 100}%` }}
                  transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                />
                <span className="absolute inset-0 flex items-center justify-end pr-3 text-xs font-bold text-zinc-700 dark:text-zinc-300">
                  {pts} pts{isMaths && grades[idx] !== 'H7' && grades[idx] !== 'H8' ? ' (incl. +25)' : ''}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="flex items-center justify-between p-5 rounded-xl bg-zinc-900 dark:bg-white text-white dark:text-zinc-900">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-wider opacity-60">Best 6 Total</p>
          <p className="text-3xl font-bold font-mono">{total}<span className="text-lg opacity-50">/{maxTotal}</span></p>
        </div>
        <div className="text-right">
          <p className="text-[10px] font-semibold uppercase tracking-wider opacity-60">Points Lost</p>
          <p className={`text-3xl font-bold font-mono ${total < maxTotal ? 'text-red-400' : 'text-emerald-400'}`}>
            {total < maxTotal ? `-${maxTotal - total}` : '0'}
          </p>
        </div>
      </div>
      <p className="text-[10px] text-zinc-400 mt-3 text-center">* Mathematics includes the 25-point Higher Level bonus for grades H1–H6.</p>
    </div>
  );
};

// ─── INTERACTIVE 2: Maths Bonus Amplifier ───────────────────────────────────

const MathsBonusVisualizer = () => {
  const [mathsGrade, setMathsGrade] = useState('H6');
  const [otherGrade, setOtherGrade] = useState('H3');

  const mathsPts = (GRADE_POINTS[mathsGrade] || 0) + (['H1','H2','H3','H4','H5','H6'].includes(mathsGrade) ? 25 : 0);
  const otherPts = GRADE_POINTS[otherGrade] || 0;

  return (
    <div className="my-10 p-6 md:p-8 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">The Maths Bonus Amplifier</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Compare HL Maths (with bonus) to any other subject. See how the 25-point bonus warps the economics.</p>

      <div className="grid grid-cols-2 gap-6">
        <div className="text-center">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 mb-3">HL Mathematics</p>
          <select value={mathsGrade} onChange={e => setMathsGrade(e.target.value)}
            className="w-full px-4 py-3 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-lg font-bold text-center text-zinc-900 dark:text-white mb-4">
            {GRADES.map(g => <option key={g} value={g}>{g}</option>)}
          </select>
          <motion.div
            className="mx-auto w-24 h-24 rounded-2xl bg-emerald-500 text-white flex flex-col items-center justify-center"
            animate={{ scale: [1, 1.05, 1] }}
            transition={{ duration: 0.3 }}
            key={mathsGrade}
          >
            <span className="text-2xl font-bold font-mono">{mathsPts}</span>
            <span className="text-[9px] font-semibold opacity-70">POINTS</span>
          </motion.div>
          <p className="text-xs text-zinc-400 mt-3">{GRADE_POINTS[mathsGrade]} + 25 bonus</p>
        </div>

        <div className="text-center">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 mb-3">Any Other Subject</p>
          <select value={otherGrade} onChange={e => setOtherGrade(e.target.value)}
            className="w-full px-4 py-3 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-lg font-bold text-center text-zinc-900 dark:text-white mb-4">
            {GRADES.map(g => <option key={g} value={g}>{g}</option>)}
          </select>
          <motion.div
            className="mx-auto w-24 h-24 rounded-2xl bg-zinc-200 dark:bg-zinc-700 text-zinc-900 dark:text-white flex flex-col items-center justify-center"
            key={otherGrade}
          >
            <span className="text-2xl font-bold font-mono">{otherPts}</span>
            <span className="text-[9px] font-semibold opacity-70">POINTS</span>
          </motion.div>
          <p className="text-xs text-zinc-400 mt-3">{GRADE_POINTS[otherGrade]} points (no bonus)</p>
        </div>
      </div>

      <div className={`mt-6 p-4 rounded-xl text-center text-sm font-medium ${mathsPts >= otherPts ? 'bg-emerald-50 text-emerald-800 dark:bg-emerald-900/20 dark:text-emerald-300' : 'bg-red-50 text-red-800 dark:bg-red-900/20 dark:text-red-300'}`}>
        {mathsPts >= otherPts
          ? `A ${mathsGrade} in Maths (${mathsPts} pts) is worth ${mathsPts - otherPts > 0 ? `${mathsPts - otherPts} points MORE than` : 'the same as'} a ${otherGrade} in any other subject (${otherPts} pts).`
          : `A ${otherGrade} in another subject (${otherPts} pts) beats a ${mathsGrade} in Maths (${mathsPts} pts) by ${otherPts - mathsPts} points.`
        }
      </div>
    </div>
  );
};

// ─── INTERACTIVE 3: Subject H1 Rate Dashboard ──────────────────────────────

const H1RateDashboard = () => {
  const [sortBy, setSortBy] = useState<'h1Rate' | 'objectivity' | 'name'>('h1Rate');
  const [showAll, setShowAll] = useState(false);

  const sorted = useMemo(() => {
    const copy = [...SUBJECTS_DATA];
    if (sortBy === 'h1Rate') return copy.sort((a, b) => b.h1Rate - a.h1Rate);
    if (sortBy === 'objectivity') return copy.sort((a, b) => b.objectivity - a.objectivity);
    return copy.sort((a, b) => a.name.localeCompare(b.name));
  }, [sortBy]);

  const displayed = showAll ? sorted : sorted.slice(0, 10);
  const maxRate = Math.max(...SUBJECTS_DATA.map(s => s.h1Rate));

  const getRiskColor = (rate: number) => {
    if (rate >= 15) return 'bg-emerald-500';
    if (rate >= 10) return 'bg-amber-400';
    return 'bg-red-400';
  };

  const getRiskLabel = (rate: number) => {
    if (rate >= 15) return { text: 'High Yield', color: 'text-emerald-600 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-900/20' };
    if (rate >= 10) return { text: 'Moderate', color: 'text-amber-600 bg-amber-50 dark:text-amber-400 dark:bg-amber-900/20' };
    return { text: 'Low Yield', color: 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/20' };
  };

  return (
    <div className="my-10 p-6 md:p-8 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">Subject H1 Rate Dashboard</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Real H1 percentages from recent Leaving Cert data. Sort to find the highest-probability subjects.</p>

      <div className="flex justify-center gap-2 mb-6">
        {[
          { key: 'h1Rate', label: 'H1 Rate' },
          { key: 'objectivity', label: 'Objectivity' },
          { key: 'name', label: 'A–Z' },
        ].map(opt => (
          <button key={opt.key} onClick={() => setSortBy(opt.key as any)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${sortBy === opt.key ? 'bg-zinc-900 dark:bg-white text-white dark:text-zinc-900' : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400'}`}>
            {opt.label}
          </button>
        ))}
      </div>

      <div className="space-y-2">
        {displayed.map((subj, idx) => {
          const risk = getRiskLabel(subj.h1Rate);
          return (
            <MotionDiv
              key={subj.name}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.02 }}
              className="flex items-center gap-3 py-2"
            >
              <span className="w-32 text-xs font-semibold text-zinc-700 dark:text-zinc-300 shrink-0 truncate">{subj.name}</span>
              <div className="flex-grow h-6 bg-zinc-100 dark:bg-zinc-800 rounded-md overflow-hidden relative">
                <motion.div
                  className={`h-full rounded-md ${getRiskColor(subj.h1Rate)}`}
                  initial={{ width: 0 }}
                  animate={{ width: `${(subj.h1Rate / maxRate) * 100}%` }}
                  transition={{ duration: 0.5, delay: idx * 0.02 }}
                />
                <span className="absolute inset-0 flex items-center pl-2 text-[11px] font-bold text-white mix-blend-difference">{subj.h1Rate}%</span>
              </div>
              <span className={`px-2 py-0.5 rounded text-[9px] font-semibold shrink-0 ${risk.color}`}>{risk.text}</span>
            </MotionDiv>
          );
        })}
      </div>

      {!showAll && (
        <button onClick={() => setShowAll(true)} className="mt-4 w-full py-2 text-xs font-semibold text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 flex items-center justify-center gap-1 transition-colors">
          Show all {SUBJECTS_DATA.length} subjects <ChevronDown size={14} />
        </button>
      )}
    </div>
  );
};

// ─── INTERACTIVE 4: Objectivity Spectrum ────────────────────────────────────

const ObjectivitySpectrum = () => {
  const [revealed, setRevealed] = useState(false);
  const sorted = [...SUBJECTS_DATA].sort((a, b) => b.objectivity - a.objectivity);

  return (
    <div className="my-10 p-6 md:p-8 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">The Objectivity Spectrum</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Where does each subject fall between "right/wrong" and "examiner's discretion"?</p>

      {!revealed ? (
        <div className="text-center py-8">
          <p className="text-sm text-zinc-500 mb-4">Before you see the data — think about your own subjects. Which do you think have the most objective marking?</p>
          <button onClick={() => setRevealed(true)}
            className="px-6 py-3 bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 rounded-lg text-sm font-semibold hover:opacity-90 transition-opacity">
            Reveal the Spectrum
          </button>
        </div>
      ) : (
        <div className="space-y-1.5">
          <div className="flex justify-between text-[9px] font-semibold uppercase tracking-wider text-zinc-400 mb-3 px-1">
            <span>Pure Objective (Right/Wrong)</span>
            <span>Pure Subjective (Discretion)</span>
          </div>
          {sorted.map((subj, idx) => (
            <MotionDiv
              key={subj.name}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.03 }}
              className="relative h-8 bg-zinc-100 dark:bg-zinc-800 rounded-md overflow-hidden"
            >
              <div className="absolute inset-0 flex items-center px-3 justify-between z-10">
                <span className="text-[11px] font-semibold text-zinc-700 dark:text-zinc-300">{subj.name}</span>
                <span className="text-[10px] font-bold text-zinc-500">{subj.objectivity}%</span>
              </div>
              <motion.div
                className="h-full bg-gradient-to-r from-emerald-400/30 to-transparent"
                initial={{ width: 0 }}
                animate={{ width: `${subj.objectivity}%` }}
                transition={{ duration: 0.6, delay: idx * 0.03 }}
              />
            </MotionDiv>
          ))}
          <div className="mt-4 p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800 text-xs text-zinc-600 dark:text-zinc-400 leading-relaxed">
            <strong className="text-zinc-900 dark:text-white">The pattern is clear:</strong> STEM subjects and Maths cluster at the objective end — a correct answer must be awarded full marks. Humanities and Arts cluster at the subjective end, where examiner discretion creates variance. For the risk-averse 625 strategy, objective subjects reduce exam-day volatility.
          </div>
        </div>
      )}
    </div>
  );
};

// ─── INTERACTIVE 5: Subject Synergy Map ─────────────────────────────────────

const SynergyMap = ({ savedSubjects, onSave }: { savedSubjects?: string[]; onSave?: (subjects: string[]) => void }) => {
  const [selected, setSelected] = useState<string[]>(savedSubjects || []);

  useEffect(() => {
    if (savedSubjects) setSelected(savedSubjects);
  }, [savedSubjects]);

  const toggleSubject = (name: string) => {
    let next: string[];
    if (selected.includes(name)) {
      next = selected.filter(s => s !== name);
    } else if (selected.length < 7) {
      next = [...selected, name];
    } else {
      return;
    }
    setSelected(next);
    onSave?.(next);
  };

  const activeSynergies = useMemo(() => {
    const links: { from: string; to: string }[] = [];
    selected.forEach(subj => {
      const data = SUBJECTS_DATA.find(s => s.name === subj);
      if (data) {
        data.synergies.forEach(syn => {
          if (selected.includes(syn) && !links.find(l => (l.from === syn && l.to === subj))) {
            links.push({ from: subj, to: syn });
          }
        });
      }
    });
    return links;
  }, [selected]);

  const groupColors: Record<string, string> = {
    'maths': 'bg-blue-100 text-blue-700 border-blue-200 dark:bg-blue-900/20 dark:text-blue-400 dark:border-blue-800',
    'stem': 'bg-emerald-100 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800',
    'life-science': 'bg-lime-100 text-lime-700 border-lime-200 dark:bg-lime-900/20 dark:text-lime-400 dark:border-lime-800',
    'language': 'bg-purple-100 text-purple-700 border-purple-200 dark:bg-purple-900/20 dark:text-purple-400 dark:border-purple-800',
    'business': 'bg-amber-100 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800',
    'humanities': 'bg-rose-100 text-rose-700 border-rose-200 dark:bg-rose-900/20 dark:text-rose-400 dark:border-rose-800',
    'practical': 'bg-orange-100 text-orange-700 border-orange-200 dark:bg-orange-900/20 dark:text-orange-400 dark:border-orange-800',
    'creative': 'bg-pink-100 text-pink-700 border-pink-200 dark:bg-pink-900/20 dark:text-pink-400 dark:border-pink-800',
  };

  return (
    <div className="my-10 p-6 md:p-8 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">Subject Synergy Map</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Select up to 7 subjects and see which share overlapping content — study one, benefit in another.</p>
      <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">{selected.length}/7 selected</p>

      <div className="flex flex-wrap justify-center gap-2 mb-6">
        {SUBJECTS_DATA.map(subj => {
          const isSelected = selected.includes(subj.name);
          const group = groupColors[subj.group] || 'bg-zinc-100 text-zinc-600 border-zinc-200';
          return (
            <button
              key={subj.name}
              onClick={() => toggleSubject(subj.name)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                isSelected ? group : 'bg-zinc-50 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-500 border-zinc-200 dark:border-zinc-700 hover:border-zinc-300 dark:hover:border-zinc-600'
              }`}
            >
              {subj.name}{subj.isMaths ? ' *' : ''}
            </button>
          );
        })}
      </div>

      {selected.length > 0 && (
        <div className="p-5 rounded-xl bg-zinc-50 dark:bg-zinc-800">
          <div className="flex items-center justify-between mb-3">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Synergy Connections</p>
            <p className="text-sm font-bold text-zinc-900 dark:text-white">{activeSynergies.length} found</p>
          </div>
          {activeSynergies.length > 0 ? (
            <div className="space-y-2">
              {activeSynergies.map((link, i) => (
                <MotionDiv key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
                  className="flex items-center gap-2 text-sm">
                  <span className="font-semibold text-zinc-700 dark:text-zinc-300">{link.from}</span>
                  <span className="text-zinc-300 dark:text-zinc-600">↔</span>
                  <span className="font-semibold text-zinc-700 dark:text-zinc-300">{link.to}</span>
                  <CheckCircle2 size={14} className="text-emerald-500 ml-auto shrink-0" />
                </MotionDiv>
              ))}
            </div>
          ) : (
            <p className="text-xs text-zinc-400 text-center py-4">No synergies between your selected subjects yet. Try adding STEM or language pairs.</p>
          )}
        </div>
      )}
    </div>
  );
};

// ─── INTERACTIVE 6: SRP Surplus Calculator ──────────────────────────────────

const SurplusCalculator = () => {
  const [questionMarks, setQuestionMarks] = useState(30);
  const [marksPerPoint, setMarksPerPoint] = useState(3);
  const [pointsWritten, setPointsWritten] = useState(10);

  const requiredPoints = Math.ceil(questionMarks / marksPerPoint);
  const surplusPoints = pointsWritten - requiredPoints;
  const safetyMargin = surplusPoints > 0 ? Math.round((surplusPoints / requiredPoints) * 100) : 0;

  return (
    <div className="my-10 p-6 md:p-8 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">The Surplus Rule Calculator</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Marking schemes often accept more valid points than required. Calculate your safety margin.</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div>
          <label className="block text-[10px] font-semibold uppercase tracking-wider text-zinc-500 mb-2">Question Worth</label>
          <div className="flex items-center gap-2">
            <button onClick={() => setQuestionMarks(Math.max(5, questionMarks - 5))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Minus size={14} /></button>
            <span className="text-2xl font-bold font-mono text-zinc-900 dark:text-white w-16 text-center">{questionMarks}</span>
            <button onClick={() => setQuestionMarks(Math.min(100, questionMarks + 5))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Plus size={14} /></button>
            <span className="text-xs text-zinc-400">marks</span>
          </div>
        </div>
        <div>
          <label className="block text-[10px] font-semibold uppercase tracking-wider text-zinc-500 mb-2">Marks per Point</label>
          <div className="flex items-center gap-2">
            <button onClick={() => setMarksPerPoint(Math.max(1, marksPerPoint - 1))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Minus size={14} /></button>
            <span className="text-2xl font-bold font-mono text-zinc-900 dark:text-white w-16 text-center">{marksPerPoint}</span>
            <button onClick={() => setMarksPerPoint(Math.min(10, marksPerPoint + 1))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Plus size={14} /></button>
            <span className="text-xs text-zinc-400">each</span>
          </div>
        </div>
        <div>
          <label className="block text-[10px] font-semibold uppercase tracking-wider text-zinc-500 mb-2">Points You Write</label>
          <div className="flex items-center gap-2">
            <button onClick={() => setPointsWritten(Math.max(1, pointsWritten - 1))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Minus size={14} /></button>
            <span className="text-2xl font-bold font-mono text-zinc-900 dark:text-white w-16 text-center">{pointsWritten}</span>
            <button onClick={() => setPointsWritten(Math.min(20, pointsWritten + 1))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Plus size={14} /></button>
            <span className="text-xs text-zinc-400">SRPs</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800 text-center">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 mb-1">Required</p>
          <p className="text-xl font-bold text-zinc-900 dark:text-white">{requiredPoints} SRPs</p>
        </div>
        <div className={`p-4 rounded-xl text-center ${surplusPoints > 0 ? 'bg-emerald-50 dark:bg-emerald-900/20' : 'bg-red-50 dark:bg-red-900/20'}`}>
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 mb-1">Surplus</p>
          <p className={`text-xl font-bold ${surplusPoints > 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>
            {surplusPoints > 0 ? `+${surplusPoints}` : surplusPoints}
          </p>
        </div>
        <div className="p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800 text-center">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 mb-1">Safety</p>
          <p className="text-xl font-bold text-zinc-900 dark:text-white">{safetyMargin}%</p>
        </div>
      </div>

      {surplusPoints >= 2 && (
        <p className="mt-4 text-xs text-emerald-600 dark:text-emerald-400 text-center font-medium">
          Strong surplus. Even if {surplusPoints} of your points are rejected, you still get full marks.
        </p>
      )}
      {surplusPoints >= 0 && surplusPoints < 2 && (
        <p className="mt-4 text-xs text-amber-600 dark:text-amber-400 text-center font-medium">
          Thin margin. Add {2 - surplusPoints} more points to build a safe buffer.
        </p>
      )}
      {surplusPoints < 0 && (
        <p className="mt-4 text-xs text-red-600 dark:text-red-400 text-center font-medium">
          You're writing fewer points than required. You will lose marks. Write at least {requiredPoints + 2} SRPs.
        </p>
      )}
    </div>
  );
};

// ─── INTERACTIVE 7: Portfolio Optimizer ──────────────────────────────────────

const DEFAULT_PORTFOLIO = [
  { subject: 'Mathematics', confidence: 'H2' },
  { subject: 'English', confidence: 'H2' },
  { subject: 'Irish', confidence: 'H3' },
  { subject: '', confidence: 'H2' },
  { subject: '', confidence: 'H2' },
  { subject: '', confidence: 'H2' },
  { subject: '', confidence: 'H3' },
];

const PortfolioOptimizer = ({ savedPortfolio, onSave }: { savedPortfolio?: { subject: string; confidence: string }[]; onSave?: (portfolio: { subject: string; confidence: string }[]) => void }) => {
  const [portfolio, setPortfolio] = useState<{ subject: string; confidence: string }[]>(savedPortfolio || DEFAULT_PORTFOLIO);

  useEffect(() => {
    if (savedPortfolio) setPortfolio(savedPortfolio);
  }, [savedPortfolio]);

  const updateSubject = (idx: number, subject: string) => {
    const next = [...portfolio];
    next[idx] = { ...next[idx], subject };
    setPortfolio(next);
    onSave?.(next);
  };

  const updateConfidence = (idx: number, confidence: string) => {
    const next = [...portfolio];
    next[idx] = { ...next[idx], confidence };
    setPortfolio(next);
    onSave?.(next);
  };

  const analysis = useMemo(() => {
    const filled = portfolio.filter(p => p.subject);
    const points = filled.map(p => {
      let pts = GRADE_POINTS[p.confidence] || 0;
      const data = SUBJECTS_DATA.find(s => s.name === p.subject);
      if (data?.isMaths && ['H1','H2','H3','H4','H5','H6'].includes(p.confidence)) pts += 25;
      return { ...p, pts, data };
    });

    const sorted = [...points].sort((a, b) => b.pts - a.pts);
    const bestSix = sorted.slice(0, 6);
    const totalPts = bestSix.reduce((s, p) => s + p.pts, 0);

    const avgObjectivity = filled.length > 0
      ? Math.round(filled.reduce((s, p) => s + (SUBJECTS_DATA.find(d => d.name === p.subject)?.objectivity || 50), 0) / filled.length)
      : 0;

    const h1Count = filled.filter(p => p.confidence === 'H1').length;
    const riskSubjects = filled.filter(p => {
      const d = SUBJECTS_DATA.find(d => d.name === p.subject);
      return d && d.objectivity < 50;
    });

    return { totalPts, avgObjectivity, h1Count, riskSubjects, filledCount: filled.length };
  }, [portfolio]);

  const availableSubjects = SUBJECTS_DATA.map(s => s.name);

  return (
    <div className="my-10 p-6 md:p-8 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">Your Portfolio Optimizer</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Enter your 7 subjects and your current realistic grade expectation. Get a personalized risk report.</p>

      <div className="space-y-3 mb-8">
        {portfolio.map((item, idx) => (
          <div key={idx} className="flex items-center gap-3">
            <span className="text-xs font-bold text-zinc-400 w-4 shrink-0">{idx + 1}</span>
            <select value={item.subject} onChange={e => updateSubject(idx, e.target.value)}
              className="flex-grow px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-sm font-medium text-zinc-900 dark:text-white">
              <option value="">Select subject...</option>
              {availableSubjects.map(s => <option key={s} value={s}>{s}{s === 'Mathematics' ? ' (+ bonus)' : ''}</option>)}
            </select>
            <select value={item.confidence} onChange={e => updateConfidence(idx, e.target.value)}
              className="w-20 px-2 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-sm font-bold text-center text-zinc-900 dark:text-white">
              {GRADES.map(g => <option key={g} value={g}>{g}</option>)}
            </select>
          </div>
        ))}
      </div>

      {analysis.filledCount >= 4 && (
        <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="p-6 rounded-xl bg-zinc-900 dark:bg-white text-white dark:text-zinc-900">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center">
              <p className="text-[9px] font-semibold uppercase tracking-wider opacity-60">Projected Points</p>
              <p className="text-2xl font-bold font-mono">{analysis.totalPts}<span className="text-sm opacity-40">/625</span></p>
            </div>
            <div className="text-center">
              <p className="text-[9px] font-semibold uppercase tracking-wider opacity-60">Objectivity</p>
              <p className="text-2xl font-bold font-mono">{analysis.avgObjectivity}%</p>
            </div>
            <div className="text-center">
              <p className="text-[9px] font-semibold uppercase tracking-wider opacity-60">H1 Confident</p>
              <p className="text-2xl font-bold font-mono">{analysis.h1Count}/{analysis.filledCount}</p>
            </div>
            <div className="text-center">
              <p className="text-[9px] font-semibold uppercase tracking-wider opacity-60">Gap to 625</p>
              <p className={`text-2xl font-bold font-mono ${analysis.totalPts >= 625 ? 'text-emerald-400' : 'text-red-400'}`}>
                {analysis.totalPts >= 625 ? '0' : `-${625 - analysis.totalPts}`}
              </p>
            </div>
          </div>

          {analysis.riskSubjects.length > 0 && (
            <div className="flex items-start gap-2 p-3 rounded-lg bg-white/10 dark:bg-zinc-900/10">
              <AlertTriangle size={16} className="shrink-0 mt-0.5 text-amber-400" />
              <p className="text-xs leading-relaxed opacity-80">
                <strong>High-variance subjects:</strong> {analysis.riskSubjects.map(s => s.subject).join(', ')}. These have subjective marking — your grade may vary between examiners. Consider investing extra time in exam technique for these.
              </p>
            </div>
          )}
        </MotionDiv>
      )}
    </div>
  );
};

// ─── MODULE COMPONENT ───────────────────────────────────────────────────────

const PointsOptimizationModule: React.FC<{
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}> = ({ onBack, progress, onProgressUpdate }) => {
  const { responses, saveResponse, isLoaded } = useModuleResponses('the-625-blueprint');

  const sections = [
    { id: 'the-cliff', title: 'The 12-Point Cliff', eyebrow: '01 // Grade Economics', icon: TrendingDown },
    { id: 'maths-multiplier', title: 'The Maths Multiplier', eyebrow: '02 // The Bonus Anomaly', icon: Calculator },
    { id: 'h1-probability', title: 'H1 Probability Map', eyebrow: '03 // The Data', icon: BarChart3 },
    { id: 'objectivity-advantage', title: 'The Objectivity Advantage', eyebrow: '04 // Risk Reduction', icon: Scale },
    { id: 'synergy-blocks', title: 'Cross-Curricular Synergy', eyebrow: '05 // Study Smarter', icon: GitBranch },
    { id: 'surplus-rule', title: 'The Surplus Rule', eyebrow: '06 // Mark Banking', icon: Layers },
    { id: 'your-blueprint', title: 'Your 625 Blueprint', eyebrow: '07 // Personal Optimizer', icon: Target },
  ];

  return (
    <ModuleLayout
      moduleNumber="09"
      moduleTitle="The 625 Blueprint"
      moduleSubtitle="The Statistical Optimization Guide"
      moduleDescription="Treat the Leaving Cert as a mathematical optimization problem. Use real H1 rate data, grade economics, and marking scheme mechanics to engineer your maximum possible score."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Complete Module"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The 12-Point Cliff." eyebrow="Step 1" icon={TrendingDown} theme={theme}>
              <p>Here is the single most important number in the Leaving Certificate: <Highlight description="The difference between an H1 (100 points) and an H2 (88 points) is 12 points — the single largest drop between any two passing grades in the system." theme={theme}>12</Highlight>. That's the number of points you lose the moment you drop from an H1 to an H2. It's the steepest cliff in the entire grading system.</p>
              <p>Think about what that means. The difference between 89% and 90% in a single exam is not 1 point — it's <strong>12 points</strong> on the CAO scale. No other grade boundary has this kind of leverage. The drop from H2 to H3 is 11 points. From H3 to H4, it's also 11. But H1 to H2? That 12-point cliff means that for a student targeting 625, the margin for error is essentially zero. You cannot afford a single H2 in your best six subjects.</p>
              <p>This isn't about perfectionism — it's about understanding the mathematics of the system you're operating in. The grading architecture was designed in 2017 to reduce the pressure of marginal gains, but paradoxically, at the very top, it created the most punishing boundary in the entire scale. A student scoring 89% and a student scoring 90% are separated by a single percentage point in achievement but <strong>12 points</strong> in CAO currency.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>I went from failing my Junior Cert to nearly 600 points in the Leaving Cert. If someone had shown me this data — the grade economics, the maths bonus, the H1 rates — when I was in 4th year, I would have saved months of wasted effort. The system has rules, and once you understand them, you stop feeling like the game is rigged against you and start playing it strategically. That's what this module is for.</p>
              </PersonalStory>
              <p>The strategic response? You don't aim for 90%. You aim for 93-95% in practice — building a buffer that absorbs exam-day volatility, unfamiliar questions, and marking variance. Use the calculator below to see exactly how each grade drop cascades through your total.</p>
              <GradeWaterfall />
              <MicroCommitment theme={theme}>
                <p>Enter your current realistic grades into the calculator above. What's your projected total? Now change just ONE subject from H2 to H1 — notice the 12-point jump. That's the subject to prioritise this week.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 1 && (
            <ReadingSection title="The Maths Multiplier." eyebrow="Step 2" icon={Calculator} theme={theme}>
              <p>Higher Level Mathematics carries a secret weapon that no other subject has: the <Highlight description="The SEC awards an additional 25 CAO points to any student who achieves a grade of H6 or higher in Higher Level Maths. This was introduced to incentivize uptake of the subject." theme={theme}>25-point bonus</Highlight>. This single policy decision makes HL Maths the most economically valuable subject on the Leaving Cert curriculum — by a significant margin.</p>
              <p>Let's do the maths on the Maths. An H1 in Higher Level Maths yields <strong>125 points</strong> (100 + 25 bonus). That's 25% more than the maximum possible in any other subject. But the bonus doesn't just reward top performers. An H6 in HL Maths (that's 40-49%, barely a pass) yields 46 + 25 = <strong>71 points</strong>. That's nearly equivalent to an H3 (77 points) in any other subject — where you'd need 70-79% to earn the same reward.</p>
              <p>The implication is mathematical and unavoidable: <strong>every hour invested in HL Maths has a higher point-per-hour yield than the same hour invested in any other subject</strong>. Even if Maths is your weakest subject, the bonus points provide a buffer that justifies the additional effort. For the 625-point candidate, HL Maths isn't optional — it's the linchpin of the entire calculation.</p>
              <MathsBonusVisualizer />
              <MicroCommitment theme={theme}>
                <p>Use the tool above. Set Maths to H6 (a bare pass) and compare it to an H3 in another subject. The fact that near-equal points come from radically different percentages should change how you allocate study time this week.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 2 && (
            <ReadingSection title="H1 Probability Map." eyebrow="Step 3" icon={BarChart3} theme={theme}>
              <p>Not all H1s are created equal. The SEC's own data reveals dramatic differences in the percentage of students who achieve H1 grades across subjects. This isn't necessarily because some subjects are "easier" — it's because the <Highlight description="The proportion of students achieving H1 is influenced by syllabus scope, marking objectivity, cohort self-selection, and assessment structure." theme={theme}>statistical probability</Highlight> of an H1 varies based on syllabus design, marking scheme structure, and cohort composition.</p>
              <p>Applied Maths consistently sees H1 rates exceeding 25-28%. The syllabus is concise, the exam is purely problem-solving, and there is zero subjectivity in marking. The cohort is self-selecting (strong mathematicians choose it), which contributes to the high rates — but for a strong candidate, it's among the highest-probability H1s available.</p>
              <p>Physics and Chemistry hover around 18-22%. These subjects reward precision: exact definitions, correct formulae, and mathematical accuracy. The marking schemes are rigid. Meanwhile, English — a compulsory subject — historically sits at just 3-5% pre-pandemic (rising to 7-11% recently due to grade adjustments). Geography can be as low as 3-4%. The subjectivity of essay-based marking creates variance that pure ability cannot fully control.</p>
              <p>This data should inform your subject selection and, critically, your <strong>effort allocation</strong>. If you're already taking a high-yield subject, protect that advantage. If you're in a low-yield subject, you need to invest disproportionately more time in exam technique to compensate for marking variance.</p>
              <H1RateDashboard />
              <MicroCommitment theme={theme}>
                <p>Sort the dashboard by H1 Rate. Find your own subjects in the list. Are you investing the most study time in your highest-yield or lowest-yield subjects? The answer might surprise you.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 3 && (
            <ReadingSection title="The Objectivity Advantage." eyebrow="Step 4" icon={Scale} theme={theme}>
              <p>There's a hidden variable that determines how much control you have over your grade: the <Highlight description="The degree to which a subject's marking scheme allows only one correct answer (objective) versus allowing examiner interpretation (subjective)." theme={theme}>objectivity</Highlight> of the marking scheme. In Maths, a correct answer is a correct answer — the examiner cannot withhold marks. In English, a brilliant essay might not resonate with a particular examiner's interpretation.</p>
              <p>This isn't a criticism of subjective subjects — they test different and equally valuable skills. But from a pure points-maximization perspective, the distinction matters enormously. In objective subjects (Maths, Physics, Chemistry, Applied Maths, Accounting), the relationship between knowledge and grade is almost deterministic: <strong>if you know it, you get the marks</strong>. In subjective subjects (English, History, Art, Geography), there's an irreducible element of variance.</p>
              <p>The risk-averse 625 strategy therefore favours a subject portfolio weighted towards the objective end of the spectrum. This doesn't mean avoiding subjective subjects entirely — English and Irish are compulsory, and some students genuinely excel in the humanities. But it means understanding that for every subjective subject in your portfolio, you carry more exam-day risk, and you need to compensate with superior exam technique.</p>
              <ObjectivitySpectrum />
              <MicroCommitment theme={theme}>
                <p>Count how many of your subjects sit above 70% objectivity and how many sit below 50%. If you're heavy on the subjective side, your priority this term should be mastering the specific marking criteria (like PCLM for English) to reduce that variance.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 4 && (
            <ReadingSection title="Cross-Curricular Synergy." eyebrow="Step 5" icon={GitBranch} theme={theme}>
              <p>The smartest students don't just study seven separate subjects — they exploit the <Highlight description="When two subjects share overlapping content, studying one simultaneously reinforces the other, effectively giving you a 2-for-1 return on study time." theme={theme}>hidden connections</Highlight> between them. The Leaving Cert curriculum is full of overlapping content, and a strategically chosen subject combination can dramatically reduce your total cognitive load.</p>
              <p>Consider the "Maths Block": Higher Maths, Applied Maths, and Physics. The mechanics section of Physics overlaps significantly with Applied Maths. Calculus in Maths supports both. A student studying all three is effectively getting a 3-for-1 return on certain topics. The "Life Science Block" (Biology, Chemistry, Ag Science) has similar overlaps — organic chemistry appears in both Chemistry and Biology, soil science in Ag Science relies on chemical concepts.</p>
              <p>Even languages create synergies — the grammar structures and essay techniques used in French transfer to Spanish and German. The critical question isn't just "what subjects do I like?" but "what subjects compound each other's value when studied together?"</p>
              <SynergyMap savedSubjects={responses['synergy-subjects']} onSave={(s) => saveResponse('synergy-subjects', s)} />
              <MicroCommitment theme={theme}>
                <p>Select your actual subjects in the tool above. How many synergy connections light up? If you're getting zero connections, think about whether your study schedule could be restructured to study synergistic subjects back-to-back in the same session.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 5 && (
            <ReadingSection title="The Surplus Rule." eyebrow="Step 6" icon={Layers} theme={theme}>
              <p>Here's something most students don't know: in many subjects, the marking scheme contains <Highlight description="When a marking scheme lists 20 valid points for a question that only requires 10, a student can write 12-13 points. If the first few are rejected, the examiner keeps reading until full marks are reached." theme={theme}>more potential marks than the question total</Highlight>. This is the Surplus Rule, and it's the closest thing to a guaranteed-marks strategy in the Leaving Cert.</p>
              <p>Here's how it works. A 30-mark question in Biology might require 10 Significant Relevant Points (SRPs) at 3 marks each. The marking scheme might list 20 valid points. If you write exactly 10 points and the examiner rejects 2 of them as incomplete or off-topic, you score 24/30. But if you write 13 points, you have a 3-point buffer. The examiner reads until they've awarded 30 marks, then stops. There's no penalty for extra correct information.</p>
              <p>This applies across Biology, Geography, History, Business, and many other subjects with SRP-based marking. The H1 student doesn't write the minimum — they write the minimum plus a calculated surplus. The exact surplus depends on the question structure.</p>
              <SurplusCalculator />
              <MicroCommitment theme={theme}>
                <p>Pick your most SRP-heavy subject. Find a past paper question and its marking scheme. Count the required SRPs. Now practice answering with a surplus of +3. Time yourself — the surplus should cost you less than 2 extra minutes per question.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 6 && (
            <ReadingSection title="Your 625 Blueprint." eyebrow="Step 7" icon={Target} theme={theme}>
              <p>You now have the data. You understand the grade economics, the maths bonus multiplier, the H1 probability landscape, the objectivity advantage, the synergy between subjects, and the surplus rule. The final step is to synthesise this into a <Highlight description="A personalized analysis of your specific subject combination that identifies your projected points total, risk profile, and priority areas for improvement." theme={theme}>personal optimization plan</Highlight>.</p>
              <p>Use the Portfolio Optimizer below to input your actual seven subjects and your honest, current grade expectations. Not your target grades — your realistic prediction based on how you're performing right now. The tool will calculate your projected total, objectivity score, and identify your highest-risk subjects.</p>
              <p>The output isn't a judgment — it's a diagnostic. If your projected total is 560, you're not "failing." You're 65 points away, which means you need to flip approximately 5-6 subjects from H2 to H1. That's your project plan for the year. Each H2→H1 flip is worth 12 points. Focus on the subjects where the flip is most achievable — typically your highest-yield, most objective subjects first.</p>
              <p>The post-pandemic landscape is shifting. The generous Post-Marking Adjustments of 2022-2024 are being tapered. You should prepare for 2019-standard marking rigour. That means aiming for 93-95% in practice to safely clear the 90% H1 threshold on exam day. The buffer is your insurance policy.</p>
              <PortfolioOptimizer savedPortfolio={responses['portfolio']} onSave={(p) => saveResponse('portfolio', p)} />
              <MicroCommitment theme={theme}>
                <p>Complete the Portfolio Optimizer with your real subjects and honest grade expectations. Screenshot the result. This is your 625 Blueprint — the gap between your projected total and 625 is the exact project you need to manage between now and June.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default PointsOptimizationModule;
