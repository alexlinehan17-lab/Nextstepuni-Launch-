/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Brain, CheckCircle, ArrowRight, BookOpen, Target, RotateCcw,
  Lightbulb, Sparkles, BarChart3,
} from 'lucide-react';

// ─── Types ───────────────────────────────────────────────────────────────────

export interface DebriefEntry {
  id: string;
  date: string;
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  hardestTopic: string;
  topicsCovered?: string[];   // topics the student worked on this session
  strategy: string;
  confidenceBefore: number;   // 1-5
  confidenceAfter: number;    // 1-5
  whatWorked: string;         // short free text
}

// ─── Constants ───────────────────────────────────────────────────────────────

export const STRATEGY_OPTIONS = [
  { id: 'past-papers', label: 'Past papers / practice questions', icon: Target },
  { id: 'active-recall', label: 'Active recall / self-testing', icon: Brain },
  { id: 're-reading', label: 'Re-reading notes', icon: BookOpen },
  { id: 'summarising', label: 'Summarising / mind maps', icon: Lightbulb },
  { id: 'teaching', label: 'Teaching / explaining it', icon: Sparkles },
  { id: 'videos', label: 'Videos / online resources', icon: BarChart3 },
  { id: 'flashcards', label: 'Flashcards', icon: RotateCcw },
  { id: 'other', label: 'Other', icon: CheckCircle },
];

const _CONFIDENCE_LABELS = ['Very Low', 'Low', 'Medium', 'High', 'Very High'];

// ─── StudyDebrief Modal ──────────────────────────────────────────────────────

interface StudyDebriefProps {
  isOpen: boolean;
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  syllabusTopics?: string[];
  onSubmit: (entry: Omit<DebriefEntry, 'id' | 'date'>) => void;
  onSkip: () => void;
}

const StudyDebrief: React.FC<StudyDebriefProps> = ({
  isOpen, subject, sessionType, durationMinutes, syllabusTopics, onSubmit, onSkip,
}) => {
  const [step, setStep] = useState(0);
  const [hardestTopic, setHardestTopic] = useState('');
  const [topicsCovered, setTopicsCovered] = useState<string[]>([]);
  const [strategy, setStrategy] = useState('');
  const [confidenceBefore, setConfidenceBefore] = useState(3);
  const [confidenceAfter, setConfidenceAfter] = useState(3);
  const [whatWorked, setWhatWorked] = useState('');
  // The saved entry is held for one screen so the session ends on a debrief
  // moment (ring + confidence shift) rather than the modal vanishing mid-tap.
  const [saved, setSaved] = useState<Omit<DebriefEntry, 'id' | 'date'> | null>(null);
  const [ringIn, setRingIn] = useState(false);

  useEffect(() => {
    if (!saved) { setRingIn(false); return; }
    const raf = requestAnimationFrame(() => setRingIn(true));
    return () => cancelAnimationFrame(raf);
  }, [saved]);

  const buildEntry = (): Omit<DebriefEntry, 'id' | 'date'> => {
    // Build topics covered: include hardest topic + any additionally selected
    const cleanHardest = (hardestTopic === '__other__' ? '' : hardestTopic).trim();
    const allTopics = [...new Set([
      ...(cleanHardest && cleanHardest !== 'Not specified' ? [cleanHardest] : []),
      ...topicsCovered,
    ])];
    return {
      subject,
      sessionType,
      durationMinutes,
      hardestTopic: cleanHardest || 'Not specified',
      topicsCovered: allTopics.length > 0 ? allTopics : undefined,
      strategy: strategy || 'other',
      confidenceBefore,
      confidenceAfter,
      whatWorked: whatWorked.trim(),
    };
  };

  const handleFinish = () => {
    if (!saved) return;
    onSubmit(saved);
    // Reset for next use
    setSaved(null);
    setStep(0);
    setHardestTopic('');
    setTopicsCovered([]);
    setStrategy('');
    setConfidenceBefore(3);
    setConfidenceAfter(3);
    setWhatWorked('');
  };

  if (!isOpen) return null;

  if (saved) {
    const pct = Math.max(0, Math.min(1, saved.confidenceAfter / 5));
    const C = 2 * Math.PI * 50;
    const covered = (saved.topicsCovered ?? []).filter(t => t !== saved.hardestTopic);
    const shaky = saved.hardestTopic !== 'Not specified' ? saved.hardestTopic : '';
    return (
      <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm px-4">
        <MotionDiv
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="w-full max-w-md overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-2xl dark:border-zinc-800 dark:bg-zinc-900"
        >
          <div className="px-6 pt-6 pb-2">
            <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[#A0968D] dark:text-zinc-500">
              Session complete · {saved.subject} · {saved.durationMinutes} min
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-6 px-6 py-5">
            <div className="relative h-[116px] w-[116px] shrink-0">
              <svg width="116" height="116" viewBox="0 0 116 116" className="-rotate-90">
                <circle cx="58" cy="58" r="50" fill="none" stroke="#ECE8E3" strokeWidth="7" className="dark:stroke-zinc-700" />
                <circle
                  cx="58" cy="58" r="50" fill="none" strokeWidth="7" strokeLinecap="round"
                  stroke="rgba(242,107,31,0.62)"
                  strokeDasharray={C}
                  strokeDashoffset={ringIn ? C * (1 - pct) : C}
                  className="motion-reduce:transition-none"
                  style={{ transition: 'stroke-dashoffset 900ms cubic-bezier(0.16, 1, 0.3, 1)' }}
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-apercu text-[22px] font-black tabular-nums leading-none text-[#1A1A1A] dark:text-white">{saved.confidenceAfter}/5</span>
                <span className="mt-1 text-[9px] font-bold uppercase tracking-[0.14em] text-[#A0968D] dark:text-zinc-500">Confidence</span>
              </div>
            </div>
            <div className="min-w-[180px] flex-1">
              <p className="font-serif text-[19px] font-bold text-[#1A1A1A] dark:text-white">
                Confidence {saved.confidenceBefore} <span className="text-[#F26B1F]">→</span> {saved.confidenceAfter}
              </p>
              <div className="mt-3 space-y-1.5 text-[12.5px] text-[#3A3530] dark:text-zinc-300">
                {covered.length > 0 && (
                  <p className="flex items-baseline gap-2">
                    <span aria-hidden="true" className="h-[9px] w-[9px] shrink-0 self-center rounded-full bg-[#3A8D5F]" />
                    <span><b className="font-bold text-[#1A1A1A] dark:text-white">Covered</b> — {covered.join(', ')}</span>
                  </p>
                )}
                {shaky && (
                  <p className="flex items-baseline gap-2">
                    <span aria-hidden="true" className="h-[9px] w-[9px] shrink-0 self-center rounded-full border-[1.5px] border-[#D6D3D0] dark:border-zinc-500" />
                    <span><b className="font-bold text-[#1A1A1A] dark:text-white">Still shaky</b> — {shaky}</span>
                  </p>
                )}
                <p className="pt-1 text-[11.5px] text-[#A8A29E] dark:text-zinc-500">
                  {saved.confidenceAfter > saved.confidenceBefore
                    ? 'Feeling surer isn’t the same as remembering — test yourself on this in a day or two.'
                    : 'Logged. Tomorrow’s plan can pick this up where you left it.'}
                </p>
              </div>
            </div>
          </div>
          <div className="px-6 pb-6">
            <button
              onClick={handleFinish}
              className="w-full rounded-xl bg-[#1A1A1A] py-3 text-sm font-bold text-white transition-transform hover:-translate-y-0.5 dark:bg-white dark:text-zinc-900"
            >
              Done
            </button>
          </div>
        </MotionDiv>
      </div>
    );
  }

  const steps = [
    // Step 0: What was hardest?
    <MotionDiv key="step-0" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
      <div>
        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">What felt hardest today?</p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">
          {syllabusTopics && syllabusTopics.length > 0 ? 'Pick a topic or type your own.' : 'Name a specific topic, concept, or question type.'}
        </p>
      </div>
      {syllabusTopics && syllabusTopics.length > 0 ? (
        <div className="space-y-2">
          <div className="max-h-40 overflow-y-auto space-y-1 pr-1">
            {syllabusTopics.map(t => (
              <button
                key={t}
                onClick={() => setHardestTopic(t)}
                className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                  hardestTopic === t
                    ? 'bg-[#F26B1F] text-white'
                    : 'bg-zinc-50 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-700'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
          <button
            onClick={() => setHardestTopic('__other__')}
            className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium transition-all ${
              hardestTopic === '__other__' || (hardestTopic !== '' && !syllabusTopics.includes(hardestTopic))
                ? 'bg-[#F26B1F] text-white'
                : 'bg-zinc-50 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-700'
            }`}
          >
            Other (type your own)
          </button>
          {(hardestTopic === '__other__' || (hardestTopic !== '' && !syllabusTopics.includes(hardestTopic))) && (
            <input
              type="text"
              value={hardestTopic === '__other__' ? '' : hardestTopic}
              onChange={(e) => setHardestTopic(e.target.value || '__other__')}
              placeholder="Type a topic..."
              className="w-full px-4 py-3 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-zinc-200 placeholder:text-zinc-400 outline-none focus:ring-2 focus:ring-[#F26B1F]/30"
              autoFocus
            />
          )}
        </div>
      ) : (
        <>
          <input
            type="text"
            value={hardestTopic}
            onChange={(e) => setHardestTopic(e.target.value)}
            placeholder={`e.g. "Organic chemistry reactions" or "Integration by parts"`}
            className="w-full px-4 py-3 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-zinc-200 placeholder:text-zinc-400 outline-none focus:ring-2 focus:ring-[#F26B1F]/30"
            autoFocus
          />
        </>
      )}

      {/* Also covered? — quick topic multi-select */}
      {syllabusTopics && syllabusTopics.length > 0 && hardestTopic && hardestTopic !== '__other__' && (
        <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800">
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">Also covered?</p>
          <div className="flex flex-wrap gap-1.5">
            {syllabusTopics
              .filter(t => t !== hardestTopic)
              .slice(0, 8)
              .map(t => {
                const isSelected = topicsCovered.includes(t);
                return (
                  <button
                    key={t}
                    onClick={() => setTopicsCovered(prev =>
                      isSelected ? prev.filter(x => x !== t) : [...prev, t]
                    )}
                    className={`px-2.5 py-1 rounded-md text-[10px] font-medium transition-all ${
                      isSelected
                        ? 'bg-[#F26B1F] text-white'
                        : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                    }`}
                  >
                    {t}
                  </button>
                );
              })}
          </div>
        </div>
      )}
    </MotionDiv>,

    // Step 1: What strategy did you use?
    <MotionDiv key="step-1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
      <div>
        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">What strategy did you mainly use?</p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">Pick the one that best describes your session.</p>
      </div>
      <div className="grid grid-cols-2 gap-2">
        {STRATEGY_OPTIONS.map(opt => {
          const Icon = opt.icon;
          return (
            <button
              key={opt.id}
              onClick={() => setStrategy(opt.id)}
              className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-xs font-medium transition-all text-left ${
                strategy === opt.id
                  ? 'bg-[#F26B1F] text-white shadow-sm'
                  : 'bg-zinc-50 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-700'
              }`}
            >
              <Icon size={14} />
              {opt.label}
            </button>
          );
        })}
      </div>
    </MotionDiv>,

    // Step 2: Confidence before & after
    <MotionDiv key="step-2" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-5">
      <div>
        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">Confidence check</p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">How confident did you feel before vs after this session?</p>
      </div>

      <div className="space-y-4">
        <div>
          <p className="text-[11px] font-semibold text-zinc-500 dark:text-zinc-400 mb-2">Before the session</p>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map(n => (
              <button
                key={n}
                onClick={() => setConfidenceBefore(n)}
                className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
                  confidenceBefore === n
                    ? 'bg-zinc-700 dark:bg-zinc-300 text-white dark:text-zinc-900'
                    : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                }`}
              >
                {n}
              </button>
            ))}
          </div>
          <div className="flex justify-between mt-1">
            <span className="text-[9px] text-zinc-400">Very Low</span>
            <span className="text-[9px] text-zinc-400">Very High</span>
          </div>
        </div>

        <div>
          <p className="text-[11px] font-semibold text-zinc-500 dark:text-zinc-400 mb-2">After the session</p>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map(n => (
              <button
                key={n}
                onClick={() => setConfidenceAfter(n)}
                className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
                  confidenceAfter === n
                    ? 'bg-[#F26B1F] text-white'
                    : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                }`}
              >
                {n}
              </button>
            ))}
          </div>
          <div className="flex justify-between mt-1">
            <span className="text-[9px] text-zinc-400">Very Low</span>
            <span className="text-[9px] text-zinc-400">Very High</span>
          </div>
        </div>

        {confidenceAfter > confidenceBefore && (
          <p className="text-xs font-medium" style={{ color: '#1F5F3E' }}>
            +{confidenceAfter - confidenceBefore} confidence. Good — but feeling sure isn’t the same as remembering. Lock it in by testing yourself on this, book closed, in a day or two.
          </p>
        )}
        {confidenceAfter < confidenceBefore && (
          <p className="text-xs text-amber-600 dark:text-amber-400 font-medium">
            Confidence dropped — that's okay. It means you found what you don't know yet. That's progress.
          </p>
        )}
      </div>
    </MotionDiv>,

    // Step 3: What worked? (optional short note)
    <MotionDiv key="step-3" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
      <div>
        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">Anything you want to remember?</p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">Optional. A quick note about what clicked or what to revisit.</p>
      </div>
      <textarea
        value={whatWorked}
        onChange={(e) => setWhatWorked(e.target.value)}
        placeholder="e.g. 'The worked examples in ch. 5 really helped' or 'Need to revisit trigonometric identities'"
        rows={3}
        className="w-full px-4 py-3 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-zinc-200 placeholder:text-zinc-400 outline-none focus:ring-2 focus:ring-[#F26B1F]/30 resize-none"
      />
    </MotionDiv>,
  ];

  const isLastStep = step === steps.length - 1;

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm px-4">
      <MotionDiv
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-2xl w-full max-w-md overflow-hidden"
      >
        {/* Header */}
        <div className="px-5 pt-5 pb-3">
          <div className="flex items-center gap-2 mb-3">
            <Brain size={18} className="text-[#F26B1F]" />
            <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200">Quick Debrief</span>
            <span className="text-[10px] text-zinc-400 dark:text-zinc-500 ml-auto">{step + 1} / {steps.length}</span>
          </div>
          {/* Step progress */}
          <div className="flex gap-1">
            {steps.map((_, i) => (
              <div key={i} className={`flex-1 h-1 rounded-full transition-all ${i <= step ? 'bg-[#F26B1F]' : 'bg-zinc-200 dark:bg-zinc-700'}`} />
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="px-5 py-4 min-h-[200px]">
          <AnimatePresence mode="wait">
            {steps[step]}
          </AnimatePresence>
        </div>

        {/* Actions */}
        <div className="px-5 pb-5 flex items-center gap-3">
          {step > 0 && (
            <button
              onClick={() => setStep(step - 1)}
              className="px-4 py-2.5 rounded-xl text-sm font-medium text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-all"
            >
              Back
            </button>
          )}
          <button
            onClick={onSkip}
            className="text-sm text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
          >
            Skip
          </button>
          <div className="flex-1" />
          <button
            onClick={isLastStep ? () => setSaved(buildEntry()) : () => setStep(step + 1)}
            disabled={step === 1 && !strategy}
            className="px-5 py-2.5 rounded-xl text-sm font-bold text-white bg-[#F26B1F] hover:bg-[#B54D14] shadow-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5"
          >
            {isLastStep ? 'Save Debrief' : 'Next'}
            <ArrowRight size={14} />
          </button>
        </div>
      </MotionDiv>
    </div>
  );
};

export default StudyDebrief;

// ─── Shared Utility: Per-subject best strategy ──────────────────────────────

export interface SubjectStrategyHint {
  strategy: string;
  label: string;
  avgGain: number;
}

/**
 * Computes the best study strategy per subject from debrief data.
 * Returns a map of subjectName → best strategy with avg confidence gain.
 * Only includes strategies used 2+ times with positive gain.
 */
export function computeStrategyHints(debriefs: DebriefEntry[]): Record<string, SubjectStrategyHint> {
  const bySubject = new Map<string, Map<string, number[]>>();

  for (const d of debriefs) {
    if (!bySubject.has(d.subject)) bySubject.set(d.subject, new Map());
    const stratMap = bySubject.get(d.subject)!;
    if (!stratMap.has(d.strategy)) stratMap.set(d.strategy, []);
    stratMap.get(d.strategy)!.push(d.confidenceAfter - d.confidenceBefore);
  }

  const result: Record<string, SubjectStrategyHint> = {};
  bySubject.forEach((stratMap, subject) => {
    let bestStrat: string | null = null;
    let bestAvg = 0;
    stratMap.forEach((gains, strat) => {
      if (gains.length >= 2) {
        const avg = gains.reduce((s, g) => s + g, 0) / gains.length;
        if (avg > bestAvg) {
          bestAvg = avg;
          bestStrat = strat;
        }
      }
    });
    if (bestStrat && bestAvg > 0) {
      const label = STRATEGY_OPTIONS.find(o => o.id === bestStrat)?.label ?? bestStrat;
      // Shorten label for display
      const shortLabel = label.split(' / ')[0].split(' (')[0];
      result[subject] = { strategy: bestStrat, label: shortLabel, avgGain: Math.round(bestAvg * 10) / 10 };
    }
  });

  return result;
}
