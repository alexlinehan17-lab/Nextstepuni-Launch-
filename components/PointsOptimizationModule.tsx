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
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Compare HL Maths (with bonus) to any other subject. See how much difference the 25-point bonus actually makes.</p>

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
          <p className="text-xs text-zinc-400 mt-3">{GRADE_POINTS[mathsGrade]}{['H1','H2','H3','H4','H5','H6'].includes(mathsGrade) ? ' + 25 bonus' : ''}</p>
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
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Real H1 percentages from recent Leaving Cert results. Sort to see which subjects have the highest H1 rates.</p>

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
            <strong className="text-zinc-900 dark:text-white">The pattern is clear:</strong> STEM subjects and Maths sit at the objective end — a right answer gets full marks, no question. Humanities and Arts sit at the subjective end, where different examiners might give different marks. If you want to reduce surprise on exam day, having more objective subjects in your mix helps.
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
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">Subject Overlap Map</h4>
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
            <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">Overlapping Subjects</p>
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
            <p className="text-xs text-zinc-400 text-center py-4">No overlap between your selected subjects yet. Try adding STEM or language pairs.</p>
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
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Marking schemes often accept more valid answers than the question needs. Calculate your safety margin.</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div>
          <label className="block text-[10px] font-semibold uppercase tracking-wider text-zinc-500 mb-2">Question Worth</label>
          <div className="flex items-center gap-2">
            <button aria-label="Decrease" onClick={() => setQuestionMarks(Math.max(5, questionMarks - 5))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Minus size={14} /></button>
            <span className="text-2xl font-bold font-mono text-zinc-900 dark:text-white w-16 text-center">{questionMarks}</span>
            <button aria-label="Increase" onClick={() => setQuestionMarks(Math.min(100, questionMarks + 5))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Plus size={14} /></button>
            <span className="text-xs text-zinc-400">marks</span>
          </div>
        </div>
        <div>
          <label className="block text-[10px] font-semibold uppercase tracking-wider text-zinc-500 mb-2">Marks per Point</label>
          <div className="flex items-center gap-2">
            <button aria-label="Decrease" onClick={() => setMarksPerPoint(Math.max(1, marksPerPoint - 1))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Minus size={14} /></button>
            <span className="text-2xl font-bold font-mono text-zinc-900 dark:text-white w-16 text-center">{marksPerPoint}</span>
            <button aria-label="Increase" onClick={() => setMarksPerPoint(Math.min(10, marksPerPoint + 1))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Plus size={14} /></button>
            <span className="text-xs text-zinc-400">each</span>
          </div>
        </div>
        <div>
          <label className="block text-[10px] font-semibold uppercase tracking-wider text-zinc-500 mb-2">Points You Write</label>
          <div className="flex items-center gap-2">
            <button aria-label="Decrease" onClick={() => setPointsWritten(Math.max(1, pointsWritten - 1))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Minus size={14} /></button>
            <span className="text-2xl font-bold font-mono text-zinc-900 dark:text-white w-16 text-center">{pointsWritten}</span>
            <button aria-label="Increase" onClick={() => setPointsWritten(Math.min(20, pointsWritten + 1))} className="p-2 rounded-lg bg-zinc-100 dark:bg-zinc-800"><Plus size={14} /></button>
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
      const d = SUBJECTS_DATA.find(subj => subj.name === p.subject);
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
                <strong>Watch out for these:</strong> {analysis.riskSubjects.map(s => s.subject).join(', ')}. These have subjective marking — your grade could depend on which examiner reads your paper. Put extra time into learning exactly what the marking scheme rewards for these subjects.
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
    { id: 'the-cliff', title: 'The 12-Point Cliff', eyebrow: '01 // How Points Really Work', icon: TrendingDown },
    { id: 'maths-multiplier', title: 'The Maths Multiplier', eyebrow: '02 // The 25-Point Bonus', icon: Calculator },
    { id: 'h1-probability', title: 'H1 Probability Map', eyebrow: '03 // The Data', icon: BarChart3 },
    { id: 'objectivity-advantage', title: 'The Objectivity Advantage', eyebrow: '04 // Reducing Exam-Day Risk', icon: Scale },
    { id: 'synergy-blocks', title: 'Subject Overlap', eyebrow: '05 // Study Smarter', icon: GitBranch },
    { id: 'surplus-rule', title: 'The Surplus Rule', eyebrow: '06 // Banking Extra Marks', icon: Layers },
    { id: 'your-blueprint', title: 'Your 625 Blueprint', eyebrow: '07 // Your Personal Plan', icon: Target },
  ];

  return (
    <ModuleLayout
      moduleNumber="09"
      moduleTitle="The 625 Blueprint"
      moduleSubtitle="How to Maximise Your Points"
      moduleDescription="The Leaving Cert is a points game — and there are smart ways to play it. Use real data on H1 rates, how points really work, and marking scheme tricks to get the most points you can."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Maximise Your Points"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The 12-Point Cliff." eyebrow="Step 1" icon={TrendingDown} theme={theme}>
              <p>Here is the single most important number in the Leaving Cert: <Highlight description="Going from an H1 (100 points) to an H2 (88 points) costs you 12 points — that's the biggest single drop between any two passing grades." theme={theme}>12</Highlight>. That's how many points you lose the moment you drop from an H1 to an H2. It's the steepest cliff in the entire grading system.</p>
              <p>Think about what that means. The difference between 89% and 90% in a single exam is not 1 point — it's <strong>12 points</strong> on the CAO scale. No other grade boundary hits this hard. The drop from H2 to H3 is 11 points. From H3 to H4, it's also 11. But H1 to H2? That 12-point cliff means that if you're chasing 625, there's almost no room for error. You can't afford a single H2 in your best six subjects.</p>
              <p>This isn't about being a perfectionist — it's about understanding how the system actually works. The grading system was redesigned in 2017, but at the very top, it accidentally created the most punishing boundary on the entire scale. A student scoring 89% and a student scoring 90% are separated by a single percentage point — but <strong>12 CAO points</strong>.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>I went from failing my Junior Cert to nearly 600 points in the Leaving Cert. If someone had shown me this data — how the points really work, the maths bonus, the H1 rates — when I was in 4th year, I would have saved months of wasted effort. The system has rules, and once you understand them, you stop feeling like the game is rigged against you and start playing it smart. That's what this module is for.</p>
              </PersonalStory>
              <p>So what do you do about it? You don't just aim for 90%. You aim for 93-95% in practice — building a buffer that protects you from a bad day, unexpected questions, or tough marking. Use the calculator below to see exactly how each grade drop affects your total.</p>
              <GradeWaterfall />
              <MicroCommitment theme={theme}>
                <p>Enter your current realistic grades into the calculator above. What's your projected total? Now change just ONE subject from H2 to H1 — notice the 12-point jump. That's the subject to prioritise this week.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 1 && (
            <ReadingSection title="The Maths Multiplier." eyebrow="Step 2" icon={Calculator} theme={theme}>
              <p>Higher Level Maths has a secret weapon that no other subject has: the <Highlight description="You get an extra 25 CAO points just for doing Higher Level Maths, as long as you get at least an H6. No other subject gives you this." theme={theme}>25-point bonus</Highlight>. This single rule makes HL Maths the most valuable subject on the Leaving Cert — by a long way.</p>
              <p>Let's do the maths on the Maths. An H1 in Higher Level Maths gives you <strong>125 points</strong> (100 + 25 bonus). That's 25% more than the max in any other subject. But the bonus isn't just for top students. An H6 in HL Maths (that's 40-49%, barely a pass) gives you 46 + 25 = <strong>71 points</strong>. That's nearly the same as an H3 (77 points) in any other subject — where you'd need 70-79% to earn a similar reward.</p>
              <p>The bottom line: <strong>every hour you put into HL Maths is worth more points than the same hour in any other subject</strong>. Even if Maths is your weakest subject, the bonus points give you a cushion that makes the extra effort worth it. If you're chasing 625, HL Maths isn't optional — it's the foundation of the whole plan.</p>
              <MathsBonusVisualizer />
              <MicroCommitment theme={theme}>
                <p>Use the tool above. Set Maths to H6 (a bare pass) and compare it to an H3 in another subject. The fact that similar points come from very different percentages should change how you spend your study time this week.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 2 && (
            <ReadingSection title="H1 Probability Map." eyebrow="Step 3" icon={BarChart3} theme={theme}>
              <p>Not all H1s are created equal. The SEC's own data shows huge differences in the percentage of students who get H1s across different subjects. This isn't necessarily because some subjects are "easier" — it's because your <Highlight description="Your chances of getting an H1 depend on the subject itself — how it's marked, how big the course is, and who else takes it. Some subjects just have way higher H1 rates than others." theme={theme}>chances of getting an H1</Highlight> depend on the subject, how it's marked, and who else takes it.</p>
              <p>Applied Maths consistently sees H1 rates above 25%. The course is focused, the exam is pure problem-solving, and the marking is black and white — you either got it right or you didn't. The students who pick it tend to be strong at maths already, which pushes the rates up — but for anyone decent at maths, it's one of the easiest H1s to get.</p>
              <p>Physics and Chemistry sit around 18-22%. These subjects reward precision: exact definitions, correct formulae, and mathematical accuracy. The marking schemes are strict. Meanwhile, English — which everyone has to do — historically sits at just 3-5% for H1s (rising to 7-11% recently with grade adjustments). Geography can be as low as 3-4%. When marking is more subjective, your grade depends partly on which examiner reads your paper.</p>
              <p>This data should shape both your subject choices and, just as importantly, <strong>where you spend your study time</strong>. If you're already taking a subject with a high H1 rate, protect that advantage. If you're in a subject where H1s are rare, you'll need to put extra time into nailing the exam technique to make up for the tougher marking.</p>
              <H1RateDashboard />
              <MicroCommitment theme={theme}>
                <p>Sort the dashboard by H1 Rate. Find your own subjects in the list. Are you spending the most study time on the subjects where H1s are easiest or hardest to get? The answer might surprise you.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 3 && (
            <ReadingSection title="The Objectivity Advantage." eyebrow="Step 4" icon={Scale} theme={theme}>
              <p>There's a hidden factor that affects how much control you actually have over your grade: the <Highlight description="How much the marking is black-and-white (right or wrong answers) versus up to the examiner's judgement. In Maths, if you get the answer right, you get the marks. In English, two examiners might give the same essay different marks." theme={theme}>objectivity</Highlight> of the marking scheme. In Maths, a correct answer is a correct answer — the examiner can't withhold marks. In English, a brilliant essay might not click with a particular examiner.</p>
              <p>This isn't a dig at subjective subjects — they test different and equally valuable skills. But when it comes to getting the most points possible, the difference matters a lot. In objective subjects (Maths, Physics, Chemistry, Applied Maths, Accounting), there's a simple rule: <strong>if you know it, you get the marks</strong>. In subjective subjects (English, History, Art, Geography), there's always some element of luck on the day.</p>
              <p>If you're trying to maximise your points, it helps to have more objective subjects in your mix. That doesn't mean avoiding subjective subjects — English and Irish are compulsory, and plenty of students do brilliantly in the humanities. But it means knowing that for every subjective subject you take, there's more exam-day risk, and you need to put extra work into nailing the marking criteria.</p>
              <ObjectivitySpectrum />
              <MicroCommitment theme={theme}>
                <p>Count how many of your subjects sit above 70% objectivity and how many sit below 50%. If most of yours are on the subjective side, your priority this term should be learning exactly what the examiner is looking for — check the marking scheme and practise giving them exactly that.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 4 && (
            <ReadingSection title="Subject Overlap." eyebrow="Step 5" icon={GitBranch} theme={theme}>
              <p>The smartest students don't just study seven separate subjects — they take advantage of the <Highlight description="When two subjects cover similar material, studying for one helps you in the other. It's like a 2-for-1 deal on study time." theme={theme}>hidden connections</Highlight> between them. The Leaving Cert curriculum is full of overlapping content, and picking the right combination of subjects can seriously cut down on how much you need to learn overall.</p>
              <p>Take the "Maths Block": Higher Maths, Applied Maths, and Physics. The mechanics section of Physics overlaps massively with Applied Maths. Calculus in Maths helps with both. If you're doing all three, you're basically getting a 3-for-1 deal on certain topics. The "Life Science Block" (Biology, Chemistry, Ag Science) works the same way — organic chemistry shows up in both Chemistry and Biology, and Ag Science leans on chemical concepts too.</p>
              <p>Even languages help each other — grammar structures and essay techniques from French carry over to Spanish and German. The key question isn't just "what subjects do I like?" but "which of my subjects help each other when I study them together?"</p>
              <SynergyMap savedSubjects={responses['synergy-subjects']} onSave={(s) => saveResponse('synergy-subjects', s)} />
              <MicroCommitment theme={theme}>
                <p>Select your actual subjects in the tool above. How many connections light up? If you're getting zero, think about whether you could rearrange your study timetable to study overlapping subjects back-to-back in the same session.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 5 && (
            <ReadingSection title="The Surplus Rule." eyebrow="Step 6" icon={Layers} theme={theme}>
              <p>Here's something most students don't know: in many subjects, the marking scheme has <Highlight description="The marking scheme often lists way more valid points than the question actually needs. So you can write extra points as a safety net — if a couple get rejected, the examiner keeps reading until you hit full marks." theme={theme}>more valid answers than the question requires</Highlight>. This is the Surplus Rule, and it's the closest thing to a guaranteed-marks trick in the Leaving Cert.</p>
              <p>Here's how it works. A 30-mark question in Biology might need 10 Significant Relevant Points (SRPs) at 3 marks each. But the marking scheme might list 20 valid points. If you write exactly 10 and the examiner rejects 2 as incomplete or off-topic, you score 24/30. But if you write 13 points, you've built in a safety net. The examiner reads until they've given you 30 marks, then stops. There's no penalty for writing extra correct information.</p>
              <p>This works in Biology, Geography, History, Business, and loads of other subjects that use SRP-based marking. Students who get H1s don't just write the minimum — they write the minimum plus a few extra points as insurance. The exact number depends on the question.</p>
              <SurplusCalculator />
              <MicroCommitment theme={theme}>
                <p>Pick your most SRP-heavy subject. Find a past paper question and its marking scheme. Count the required SRPs. Now practice answering with a surplus of +3. Time yourself — the surplus should cost you less than 2 extra minutes per question.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 6 && (
            <ReadingSection title="Your 625 Blueprint." eyebrow="Step 7" icon={Target} theme={theme}>
              <p>You now have the data. You understand how the points really work, the maths bonus, where H1s are easiest and hardest to get, the objectivity advantage, how subjects overlap, and the surplus rule. The final step is to pull it all together into a <Highlight description="A personalised look at your specific subjects, your projected points total, where you're at risk, and what to focus on to improve." theme={theme}>personal plan</Highlight>.</p>
              <p>Use the Portfolio Optimizer below to enter your actual seven subjects and your honest, current grade expectations. Not your target grades — your realistic prediction based on how you're actually doing right now. The tool will calculate your projected total, objectivity score, and flag your highest-risk subjects.</p>
              <p>The result isn't a judgement — it's a starting point. If your projected total is 560, you're not "failing." You're 65 points away, which means you need to bump roughly 5-6 subjects from H2 to H1. That's your plan for the year. Each H2-to-H1 jump is worth 12 points. Focus on the subjects where the jump is most realistic — usually your subjects with the highest H1 rates and most objective marking.</p>
              <PersonalStory name="Ciara" role="6th Year, Galway">
                <p>I was doing seven subjects and putting equal time into all of them. When I actually sat down and looked at the H1 rates and how objective each subject was, I realised I was spending hours on English essays that might get me 2 extra points, while ignoring Applied Maths where the same effort could have got me 12. Once I shifted my study time around, my mock results jumped by nearly 40 points.</p>
              </PersonalStory>
              <p>One more thing: marking standards are tightening. The generous adjustments from 2022-2024 are being phased out. You should prepare for tougher marking. That means aiming for 93-95% in practice to safely clear the 90% H1 threshold on exam day. The buffer is your safety net.</p>
              <PortfolioOptimizer savedPortfolio={responses['portfolio']} onSave={(p) => saveResponse('portfolio', p)} />
              <MicroCommitment theme={theme}>
                <p>Complete the Portfolio Optimizer with your real subjects and honest grade expectations. Screenshot the result. This is your 625 Blueprint — the gap between your projected total and 625 is exactly what you need to close between now and June.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default PointsOptimizationModule;
