/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search, ChevronRight, ChevronDown, ArrowRight, Clock,
  BarChart3, TrendingUp, Lightbulb, BookOpen, Zap, Info,
  Star, AlertTriangle, CheckCircle,
} from 'lucide-react';
import {
  type SubjectSyllabus, type SyllabusTopic,
  SYLLABUS_DATA, AVAILABLE_SUBJECTS, getSyllabusForSubject,
  computeEfficiency, getQuadrant, QUADRANT_LABELS,
} from './syllabusData';

const MotionDiv = motion.div as any;

// ─── Types ───────────────────────────────────────────────────────────────────

interface SyllabusXRayProps {
  studentSubjects?: string[];
}

// ─── Subject Colors ──────────────────────────────────────────────────────────

const SUBJECT_ACCENT: Record<string, { dot: string; bg: string; border: string; text: string }> = {
  'English': { dot: 'bg-blue-500', bg: 'bg-blue-50 dark:bg-blue-900/15', border: 'border-blue-200 dark:border-blue-800/30', text: 'text-blue-700 dark:text-blue-300' },
  'Mathematics': { dot: 'bg-indigo-500', bg: 'bg-indigo-50 dark:bg-indigo-900/15', border: 'border-indigo-200 dark:border-indigo-800/30', text: 'text-indigo-700 dark:text-indigo-300' },
  'Biology': { dot: 'bg-lime-500', bg: 'bg-lime-50 dark:bg-lime-900/15', border: 'border-lime-200 dark:border-lime-800/30', text: 'text-lime-700 dark:text-lime-300' },
  'Business': { dot: 'bg-amber-500', bg: 'bg-amber-50 dark:bg-amber-900/15', border: 'border-amber-200 dark:border-amber-800/30', text: 'text-amber-700 dark:text-amber-300' },
  'History': { dot: 'bg-purple-500', bg: 'bg-purple-50 dark:bg-purple-900/15', border: 'border-purple-200 dark:border-purple-800/30', text: 'text-purple-700 dark:text-purple-300' },
  'Geography': { dot: 'bg-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-900/15', border: 'border-emerald-200 dark:border-emerald-800/30', text: 'text-emerald-700 dark:text-emerald-300' },
  'Chemistry': { dot: 'bg-teal-500', bg: 'bg-teal-50 dark:bg-teal-900/15', border: 'border-teal-200 dark:border-teal-800/30', text: 'text-teal-700 dark:text-teal-300' },
  'Physics': { dot: 'bg-cyan-500', bg: 'bg-cyan-50 dark:bg-cyan-900/15', border: 'border-cyan-200 dark:border-cyan-800/30', text: 'text-cyan-700 dark:text-cyan-300' },
};

const DEFAULT_ACCENT = { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' };

function getAccent(subject: string) { return SUBJECT_ACCENT[subject] || DEFAULT_ACCENT; }

// ─── Frequency / Difficulty bars ─────────────────────────────────────────────

const FrequencyBar: React.FC<{ value: number; max?: number }> = ({ value, max = 10 }) => (
  <div className="flex gap-0.5">
    {Array.from({ length: max }, (_, i) => (
      <div key={i} className={`w-2 h-3 rounded-sm ${i < value ? 'bg-emerald-500' : 'bg-zinc-200 dark:bg-zinc-700'}`} />
    ))}
  </div>
);

const DifficultyDots: React.FC<{ value: number }> = ({ value }) => (
  <div className="flex gap-1">
    {[1, 2, 3, 4, 5].map(i => (
      <div key={i} className={`w-2 h-2 rounded-full ${i <= value ? 'bg-amber-500' : 'bg-zinc-200 dark:bg-zinc-700'}`} />
    ))}
  </div>
);

// ─── Sort options ────────────────────────────────────────────────────────────

type SortKey = 'efficiency' | 'frequency' | 'weight' | 'difficulty';

const SORT_OPTIONS: { key: SortKey; label: string }[] = [
  { key: 'efficiency', label: 'Efficiency (marks/hour)' },
  { key: 'frequency', label: 'Exam frequency' },
  { key: 'weight', label: 'Mark weight' },
  { key: 'difficulty', label: 'Difficulty (easiest first)' },
];

// ─── Component ───────────────────────────────────────────────────────────────

const SyllabusXRay: React.FC<SyllabusXRayProps> = ({ studentSubjects }) => {
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<SortKey>('efficiency');
  const [expandedTopic, setExpandedTopic] = useState<string | null>(null);

  // Determine which subjects to show — prioritise student's subjects
  const availableSubjects = useMemo(() => {
    if (studentSubjects && studentSubjects.length > 0) {
      return AVAILABLE_SUBJECTS.filter(s => studentSubjects.includes(s));
    }
    return AVAILABLE_SUBJECTS;
  }, [studentSubjects]);

  const syllabus = selectedSubject ? getSyllabusForSubject(selectedSubject) : null;

  const sortedTopics = useMemo(() => {
    if (!syllabus) return [];
    const topics = [...syllabus.topics];
    switch (sortBy) {
      case 'efficiency':
        return topics.sort((a, b) => computeEfficiency(b, syllabus.totalMarks) - computeEfficiency(a, syllabus.totalMarks));
      case 'frequency':
        return topics.sort((a, b) => b.examFrequency - a.examFrequency);
      case 'weight':
        return topics.sort((a, b) => b.markWeight - a.markWeight);
      case 'difficulty':
        return topics.sort((a, b) => a.difficulty - b.difficulty);
      default:
        return topics;
    }
  }, [syllabus, sortBy]);

  const topicsByQuadrant = useMemo(() => {
    if (!syllabus) return {};
    const groups: Record<string, SyllabusTopic[]> = {};
    for (const topic of syllabus.topics) {
      const q = getQuadrant(topic);
      if (!groups[q]) groups[q] = [];
      groups[q].push(topic);
    }
    return groups;
  }, [syllabus]);

  // ── Subject Picker ──
  if (!selectedSubject) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Syllabus X-Ray</h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
            See which topics are worth the most marks, how often they appear, and where to focus your study time.
          </p>
        </div>

        <div className="bg-rose-50 dark:bg-rose-900/15 border border-rose-200 dark:border-rose-800/30 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <Zap size={16} className="text-rose-500 shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-bold text-rose-700 dark:text-rose-300">
                This is the exam intelligence that grind schools charge for.
              </p>
              <p className="text-xs text-rose-600 dark:text-rose-400 leading-relaxed mt-1">
                Stop studying everything equally. Focus on what appears most often, carries the most marks, and suits your study time.
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
            {studentSubjects && studentSubjects.length > 0 ? 'Your Subjects' : 'Available Subjects'}
          </p>
          {availableSubjects.map(subject => {
            const accent = getAccent(subject);
            const data = getSyllabusForSubject(subject);
            return (
              <button
                key={subject}
                onClick={() => setSelectedSubject(subject)}
                className={`w-full flex items-center gap-4 p-4 rounded-xl ${accent.bg} border ${accent.border} hover:shadow-sm active:scale-[0.99] transition-all text-left`}
              >
                <span className={`w-3 h-3 rounded-full shrink-0 ${accent.dot}`} />
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-bold ${accent.text}`}>{subject}</p>
                  {data && (
                    <p className="text-[11px] text-zinc-400 dark:text-zinc-500">
                      {data.totalMarks} marks &middot; {data.papers.length} paper{data.papers.length !== 1 ? 's' : ''} &middot; {data.topics.length} topics
                    </p>
                  )}
                </div>
                <ChevronRight size={16} className="text-zinc-300 dark:text-zinc-600 shrink-0" />
              </button>
            );
          })}

          {availableSubjects.length === 0 && (
            <p className="text-sm text-zinc-400 dark:text-zinc-500 text-center py-8">
              Complete your subject profile to see your subjects here, or browse all available subjects below.
            </p>
          )}

          {/* Show remaining subjects if student has a profile */}
          {studentSubjects && studentSubjects.length > 0 && (
            <>
              <div className="flex items-center gap-3 py-3 px-3">
                <div className="flex-1 h-px bg-zinc-200 dark:bg-white/10" />
                <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Other Subjects</p>
                <div className="flex-1 h-px bg-zinc-200 dark:bg-white/10" />
              </div>
              {AVAILABLE_SUBJECTS.filter(s => !studentSubjects.includes(s)).map(subject => {
                const data = getSyllabusForSubject(subject);
                return (
                  <button
                    key={subject}
                    onClick={() => setSelectedSubject(subject)}
                    className="w-full flex items-center gap-4 p-3 rounded-xl bg-white/40 dark:bg-white/5 border border-zinc-200/40 dark:border-white/5 hover:bg-white dark:hover:bg-white/10 transition-all text-left opacity-60 hover:opacity-100"
                  >
                    <span className="w-3 h-3 rounded-full shrink-0 bg-zinc-400" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-zinc-600 dark:text-zinc-400">{subject}</p>
                      {data && (
                        <p className="text-[11px] text-zinc-400 dark:text-zinc-500">
                          {data.totalMarks} marks &middot; {data.topics.length} topics
                        </p>
                      )}
                    </div>
                    <ChevronRight size={14} className="text-zinc-300 dark:text-zinc-600 shrink-0" />
                  </button>
                );
              })}
            </>
          )}
        </div>
      </div>
    );
  }

  // ── Subject Detail View ──
  const accent = getAccent(selectedSubject);

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => { setSelectedSubject(null); setExpandedTopic(null); }}
          className="p-2 -ml-2 rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800/60 transition-colors"
        >
          <ChevronRight size={18} className="text-zinc-400 rotate-180" />
        </button>
        <div>
          <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">{selectedSubject}</h2>
          {syllabus && (
            <p className="text-xs text-zinc-400 dark:text-zinc-500">
              {syllabus.totalMarks} marks &middot; {syllabus.papers.map(p => p.name).join(' + ')}
            </p>
          )}
        </div>
      </div>

      {/* Paper structure */}
      {syllabus && (
        <div className="flex gap-2">
          {syllabus.papers.map(paper => (
            <div key={paper.name} className={`flex-1 rounded-xl p-3 border ${accent.bg} ${accent.border}`}>
              <p className={`text-[10px] font-bold uppercase tracking-widest ${accent.text} mb-1`}>{paper.name}</p>
              <div className="flex items-baseline gap-1.5">
                <span className={`text-lg font-bold ${accent.text}`}>{paper.marks}</span>
                <span className="text-[11px] text-zinc-400">marks</span>
              </div>
              <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5 flex items-center gap-1">
                <Clock size={10} /> {paper.duration}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Key advice */}
      {syllabus && (
        <div className={`${accent.bg} border ${accent.border} rounded-xl p-4`}>
          <div className="flex items-start gap-3">
            <Lightbulb size={16} className={accent.text.replace('text-', 'text-').split(' ')[0]} style={{ opacity: 0.8 }} />
            <p className="text-xs leading-relaxed text-zinc-600 dark:text-zinc-400">{syllabus.keyAdvice}</p>
          </div>
        </div>
      )}

      {/* Quadrant summary */}
      {syllabus && (
        <div className="grid grid-cols-2 gap-2">
          {(['start-here', 'high-value', 'worth-knowing', 'only-if-time'] as const).map(q => {
            const info = QUADRANT_LABELS[q];
            const topics = topicsByQuadrant[q] || [];
            return (
              <div key={q} className={`rounded-xl p-3 border ${info.bg} border-zinc-200/40 dark:border-white/5`}>
                <p className={`text-[10px] font-bold uppercase tracking-widest ${info.color} mb-1`}>{info.label}</p>
                <p className="text-lg font-bold text-zinc-800 dark:text-zinc-200">{topics.length}</p>
                <p className="text-[10px] text-zinc-400">topic{topics.length !== 1 ? 's' : ''}</p>
              </div>
            );
          })}
        </div>
      )}

      {/* Sort control */}
      <div className="flex items-center gap-2 overflow-x-auto py-1 -mx-1 px-1">
        <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 shrink-0">Sort:</span>
        {SORT_OPTIONS.map(opt => (
          <button
            key={opt.key}
            onClick={() => setSortBy(opt.key)}
            className={`shrink-0 px-3 py-1.5 rounded-lg text-[11px] font-medium transition-all ${
              sortBy === opt.key
                ? 'bg-zinc-800 dark:bg-zinc-200 text-white dark:text-zinc-900'
                : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
            }`}
          >
            {opt.label}
          </button>
        ))}
      </div>

      {/* Topic list */}
      <div className="space-y-2">
        {sortedTopics.map((topic, idx) => {
          const quadrant = getQuadrant(topic);
          const qInfo = QUADRANT_LABELS[quadrant];
          const efficiency = computeEfficiency(topic, syllabus!.totalMarks);
          const isExpanded = expandedTopic === topic.name;
          const potentialMarks = Math.round((topic.markWeight / 100) * syllabus!.totalMarks);

          return (
            <MotionDiv
              key={topic.name}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.03 }}
            >
              <button
                onClick={() => setExpandedTopic(isExpanded ? null : topic.name)}
                className="w-full text-left p-4 rounded-xl bg-white/60 dark:bg-white/5 border border-zinc-200/60 dark:border-white/10 hover:bg-white dark:hover:bg-white/10 transition-all"
              >
                <div className="flex items-start gap-3">
                  <span className="text-xs font-bold text-zinc-300 dark:text-zinc-600 w-5 text-center mt-0.5">
                    {idx + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{topic.name}</p>
                      <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full ${qInfo.bg} ${qInfo.color}`}>
                        {qInfo.label}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-[11px] text-zinc-400 dark:text-zinc-500">
                      <span>~{topic.markWeight}% ({potentialMarks} marks)</span>
                      <span>{topic.studyHours}h study</span>
                      <span className="font-semibold text-emerald-600 dark:text-emerald-400">
                        {efficiency} eff
                      </span>
                    </div>
                  </div>
                  <div className="shrink-0">
                    {isExpanded ? <ChevronDown size={16} className="text-zinc-400" /> : <ChevronRight size={16} className="text-zinc-300" />}
                  </div>
                </div>

                {/* Expanded details */}
                <AnimatePresence>
                  {isExpanded && (
                    <MotionDiv
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden"
                    >
                      <div className="mt-3 ml-8 space-y-3 border-t border-zinc-100 dark:border-zinc-800 pt-3">
                        {/* Section */}
                        <div className="flex items-center gap-2">
                          <BookOpen size={12} className="text-zinc-400" />
                          <span className="text-xs text-zinc-500">{topic.section}</span>
                        </div>

                        {/* Exam frequency */}
                        <div className="space-y-1">
                          <p className="text-[10px] font-bold text-zinc-400 uppercase tracking-widest">Exam Frequency</p>
                          <div className="flex items-center gap-2">
                            <FrequencyBar value={topic.examFrequency} />
                            <span className="text-[10px] text-zinc-400">{topic.examFrequency}/10</span>
                          </div>
                        </div>

                        {/* Difficulty */}
                        <div className="space-y-1">
                          <p className="text-[10px] font-bold text-zinc-400 uppercase tracking-widest">Difficulty</p>
                          <div className="flex items-center gap-2">
                            <DifficultyDots value={topic.difficulty} />
                            <span className="text-[10px] text-zinc-400">{topic.difficulty}/5</span>
                          </div>
                        </div>

                        {/* Tip */}
                        <div className="bg-zinc-50 dark:bg-zinc-800/50 rounded-lg p-3">
                          <div className="flex items-start gap-2">
                            <Lightbulb size={12} className="text-amber-500 shrink-0 mt-0.5" />
                            <p className="text-xs text-zinc-600 dark:text-zinc-400 leading-relaxed">{topic.tip}</p>
                          </div>
                        </div>
                      </div>
                    </MotionDiv>
                  )}
                </AnimatePresence>
              </button>
            </MotionDiv>
          );
        })}
      </div>
    </div>
  );
};

export default SyllabusXRay;
