/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  ChevronRight, X, ScanSearch,
} from 'lucide-react';
import {
  type SyllabusTopic,
  AVAILABLE_SUBJECTS, getSyllabusForSubject,
  computeEfficiency, getQuadrant, QUADRANT_LABELS,
  fuzzyMatchTopic,
} from './syllabusData';
import { computeSubjectRoi } from './syllabusRoi';
import { db } from '../firebase';
import { doc, getDoc } from 'firebase/firestore';
import { type DebriefEntry } from './StudyDebrief';
import { useTopicMastery } from '../hooks/useTopicMastery';
import { type UnifiedConfidence } from '../types';
import { COLORS } from '../design/tokens';
import { examinationYearFromDate, resolveCurriculumSpecification } from '../curriculumRegistry';

// ── Types ────────────────────────────────────────────────────────────────────

interface SyllabusXRayProps {
  studentSubjects?: string[];
  uid?: string;
  examDate?: string | null;
}

type TopicStatus = 'not-started' | 'in-progress' | 'confident';

type SortKey = 'efficiency' | 'frequency' | 'weight' | 'difficulty';

interface TopicMastery {
  [topicName: string]: TopicStatus;
}

interface SubjectMastery {
  [subject: string]: TopicMastery;
}

// ── Sort control ─────────────────────────────────────────────────────────────

const SORT_OPTIONS: { key: SortKey; label: string }[] = [
  { key: 'efficiency', label: 'Efficiency' },
  { key: 'frequency', label: 'Frequency' },
  { key: 'weight', label: 'Marks' },
  { key: 'difficulty', label: 'Difficulty' },
];

// ── Treemap layout ───────────────────────────────────────────────────────────

// Tiles are sized by mark weight but rendered in the caller-supplied order, so
// the active sort (efficiency / frequency / marks / difficulty) drives the
// reading order while block size always reflects marks.
function computeTreemapLayout(topics: SyllabusTopic[], _totalMarks: number): { topic: SyllabusTopic; cols: number; rows: number }[] {
  return topics.map(topic => {
    const area = Math.max(2, Math.round((topic.markWeight / 100) * 20)); // Scale to ~20 units total

    let cols: number;
    let rows: number;

    if (area >= 8) {
      cols = 5; rows = 2;
    } else if (area >= 5) {
      cols = 5; rows = 1;
    } else if (area >= 4) {
      cols = 4; rows = 1;
    } else if (area >= 3) {
      cols = 3; rows = 1;
    } else {
      cols = 2; rows = 1;
    }

    return { topic, cols, rows };
  });
}

// ── Mapping helpers: unified <-> display ─────────────────────────────────────

/** Map from UnifiedConfidence ('not-started'|'shaky'|'solid') to display TopicStatus */
function unifiedToDisplay(c: UnifiedConfidence): TopicStatus {
  if (c === 'solid') return 'confident';
  if (c === 'shaky') return 'in-progress';
  return 'not-started';
}

/** Map from display TopicStatus to UnifiedConfidence */
function displayToUnified(s: TopicStatus): UnifiedConfidence {
  if (s === 'confident') return 'solid';
  if (s === 'in-progress') return 'shaky';
  return 'not-started';
}

// ── Component ────────────────────────────────────────────────────────────────

const SyllabusXRay: React.FC<SyllabusXRayProps> = ({ studentSubjects, uid, examDate }) => {
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<SortKey>('efficiency');
  const [expandedTopic, setExpandedTopic] = useState<string | null>(null);
  const [debriefs, setDebriefs] = useState<DebriefEntry[]>([]);

  // Shared topic mastery hook
  const topicMastery = useTopicMastery(uid, examDate);

  // Derive a display-friendly SubjectMastery from the unified mastery
  const mastery: SubjectMastery = useMemo(() => {
    const result: SubjectMastery = {};
    for (const [subject, topics] of Object.entries(topicMastery.mastery)) {
      result[subject] = {};
      for (const [topicName, entry] of Object.entries(topics)) {
        result[subject][topicName] = unifiedToDisplay(entry.confidence);
      }
    }
    return result;
  }, [topicMastery.mastery]);

  // Load study debriefs only (mastery is handled by the hook)
  useEffect(() => {
    if (!uid) return;
    let cancelled = false;
    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        if (cancelled) return;
        const data = snap.data();
        if (data?.studyDebriefs) {
          setDebriefs(data.studyDebriefs as DebriefEntry[]);
        }
      } catch (err) { console.error('Failed to load debrief data:', err); }
    };
    load();
    return () => { cancelled = true; };
  }, [uid]);

  // Compute hours per topic for the selected subject via fuzzy matching
  const topicHoursMap = useMemo(() => {
    if (!selectedSubject || debriefs.length === 0) return {};
    const map: Record<string, number> = {};
    for (const d of debriefs) {
      if (d.subject !== selectedSubject) continue;
      const matched = fuzzyMatchTopic(selectedSubject, d.hardestTopic, examDate);
      if (matched) {
        map[matched.name] = (map[matched.name] || 0) + (d.durationMinutes / 60);
      }
    }
    return map;
  }, [selectedSubject, debriefs, examDate]);

  // Determine which subjects to show — prioritise student's subjects
  const availableSubjects = useMemo(() => {
    if (studentSubjects && studentSubjects.length > 0) {
      return AVAILABLE_SUBJECTS.filter(s => studentSubjects.includes(s));
    }
    return AVAILABLE_SUBJECTS;
  }, [studentSubjects]);

  const syllabus = selectedSubject ? getSyllabusForSubject(selectedSubject, examDate) : null;
  const activeSpecification = selectedSubject
    ? resolveCurriculumSpecification(selectedSubject, examinationYearFromDate(examDate))
    : undefined;

  // Personal ROI overlay (F6): historical marks-per-strand × the student's own
  // Paper Trail self-mark accuracy. Null (renders nothing) unless the student
  // has ≥3 self-marks in the subject AND at least one joins onto a strand.
  const roi = useMemo(
    () => (syllabus ? computeSubjectRoi(uid, syllabus) : null),
    [uid, syllabus],
  );

  // Study time stats
  const studyTimeStats = useMemo(() => {
    if (!syllabus || !selectedSubject) return { totalNeeded: 0, totalLogged: 0, remaining: 0 };
    const subjectMastery = mastery[selectedSubject] || {};
    let totalNeeded = 0;
    let totalLogged = 0;
    for (const topic of syllabus.topics) {
      totalNeeded += topic.studyHours;
      totalLogged += topicHoursMap[topic.name] || 0;
    }
    // Only count remaining for topics that aren't confident
    let remaining = 0;
    for (const topic of syllabus.topics) {
      const status = subjectMastery[topic.name] || 'not-started';
      if (status !== 'confident') {
        remaining += Math.max(0, topic.studyHours - (topicHoursMap[topic.name] || 0));
      }
    }
    return { totalNeeded, totalLogged: Math.round(totalLogged * 10) / 10, remaining: Math.round(remaining) };
  }, [syllabus, selectedSubject, topicHoursMap, mastery]);

  // Topics in the active sort order — drives the treemap reading order.
  const sortedTopics = useMemo(() => {
    if (!syllabus) return [];
    const topics = [...syllabus.topics];
    switch (sortBy) {
      case 'frequency':
        return topics.sort((a, b) => b.examFrequency - a.examFrequency);
      case 'weight':
        return topics.sort((a, b) => b.markWeight - a.markWeight);
      case 'difficulty':
        return topics.sort((a, b) => a.difficulty - b.difficulty);
      case 'efficiency':
      default:
        return topics.sort((a, b) => computeEfficiency(b, syllabus.totalMarks) - computeEfficiency(a, syllabus.totalMarks));
    }
  }, [syllabus, sortBy]);

  // Subject-level progress for subject picker (mastery-based)
  const subjectProgress = useMemo(() => {
    const progress: Record<string, number> = {};
    for (const subject of AVAILABLE_SUBJECTS) {
      const data = getSyllabusForSubject(subject, examDate);
      const subjectMastery = mastery[subject] || {};
      if (!data) { progress[subject] = 0; continue; }
      let score = 0;
      for (const topic of data.topics) {
        const s = subjectMastery[topic.name] || 'not-started';
        if (s === 'confident') score += 1;
        else if (s === 'in-progress') score += 0.5;
      }
      progress[subject] = data.topics.length > 0 ? Math.round((score / data.topics.length) * 100) : 0;
    }
    return progress;
  }, [mastery, examDate]);

  // ── Subject Picker (2-column card grid) ──
  if (!selectedSubject) {
    // If no student subjects available at all, show empty state
    if (availableSubjects.length === 0) {
      return (
        <div className="space-y-6">
          <div className="text-center py-16 space-y-4">
            <div className="w-16 h-16 mx-auto rounded-2xl flex items-center justify-center" style={{ backgroundColor: '#FDEEDF' }}>
              <ScanSearch size={32} style={{ color: COLORS.accent }} />
            </div>
            <h3 className="text-lg font-bold text-zinc-800 dark:text-white">See what's really worth marks</h3>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 max-w-sm mx-auto leading-relaxed">
              Every topic weighted by exam frequency and mark value — so you study what actually counts.
            </p>
            <p className="text-xs text-zinc-400 dark:text-zinc-500">Complete your subject profile to get started.</p>
          </div>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <div className="grid grid-cols-2 gap-2.5">
          {availableSubjects.map(subject => {
            const data = getSyllabusForSubject(subject, examDate);
            const progress = subjectProgress[subject] || 0;
            return (
              <button
                key={subject}
                onClick={() => setSelectedSubject(subject)}
                className="rounded-xl p-3.5 text-left transition-colors bg-[#FAF7F4] dark:bg-zinc-900"
                style={{
                  border: '0.5px solid rgba(0,0,0,0.07)',
                }}
              >
                <p className="text-[15px] font-medium text-zinc-800 dark:text-zinc-200">{subject}</p>
                {data && (
                  <p className="text-[11px] text-zinc-400 dark:text-zinc-500 mt-0.5">
                    {data.totalMarks} marks &middot; {data.papers.length} paper{data.papers.length !== 1 ? 's' : ''}
                  </p>
                )}
                {/* Progress bar */}
                <div className="mt-2.5 h-1 rounded-full bg-zinc-200 dark:bg-zinc-700 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all"
                    style={{ width: `${progress}%`, backgroundColor: COLORS.accent }}
                  />
                </div>
                {data && (
                  <p className="text-[11px] text-zinc-400 dark:text-zinc-500 mt-1.5">
                    {data.topics.length} topics
                  </p>
                )}
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  // ── Subject Detail View — Treemap ──
  const subjectMastery = mastery[selectedSubject] || {};
  const treemapLayout = syllabus ? computeTreemapLayout(sortedTopics, syllabus.totalMarks) : [];

  // Selected topic data
  const selectedTopicData = expandedTopic && syllabus
    ? syllabus.topics.find(t => t.name === expandedTopic) || null
    : null;

  return (
    <div className="space-y-5">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => { setSelectedSubject(null); setExpandedTopic(null); }}
            aria-label="Back to subjects"
            className="p-1 -ml-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800/60 transition-colors"
          >
            <ChevronRight size={16} className="text-zinc-400 rotate-180" />
          </button>
          <h2 className="text-[26px] font-medium text-zinc-900 dark:text-white">{selectedSubject}</h2>
        </div>
        {syllabus && (
          <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5 ml-7">
            {syllabus.totalMarks} marks &middot; {syllabus.papers.length} paper{syllabus.papers.length !== 1 ? 's' : ''} &middot; {studyTimeStats.totalNeeded}h estimated
          </p>
        )}
      </div>

      {!syllabus && activeSpecification && (
        <div className="rounded-2xl border-2 border-[#302D29] bg-[#FCFBF8] p-6 space-y-3">
          <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-[#9A8F85]">
            Specification-safe view
          </p>
          <h3 className="font-serif text-xl text-[#211E1B]">Prioritisation is being verified</h3>
          <p className="text-sm leading-6 text-[#6F665E]">
            You are on {activeSpecification.title}. We have paused marks-per-hour rankings for this subject rather than show advice from a different syllabus.
          </p>
          <p className="text-xs text-[#9A8F85]">
            Your coverage and Mark Bank cards remain available and unchanged.
          </p>
        </div>
      )}

      {/* Sort control — reorders the treemap. Efficiency (marks per study hour)
          is the default "where the marks are hiding" view. */}
      {syllabus && (
        <div className="flex items-center gap-1.5 overflow-x-auto -mx-1 px-1 pb-1" role="group" aria-label="Sort topics by">
          <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 shrink-0 mr-1">Sort</span>
          {SORT_OPTIONS.map(opt => {
            const active = sortBy === opt.key;
            return (
              <button
                key={opt.key}
                onClick={() => setSortBy(opt.key)}
                aria-pressed={active}
                className="shrink-0 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors border-2"
                style={active
                  ? { backgroundColor: '#FDEEDF', color: '#8C3A0E', borderColor: COLORS.accent }
                  : { backgroundColor: 'white', color: '#7a7068', borderColor: '#d0cdc8' }}
              >
                {opt.label}
              </button>
            );
          })}
        </div>
      )}

      {/* Treemap Grid */}
      {syllabus && (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(10, 1fr)',
            gridAutoRows: '56px',
            gap: '5px',
          }}
        >
          {treemapLayout.map(({ topic, cols, rows }) => {
            const potentialMarks = Math.round((topic.markWeight / 100) * syllabus.totalMarks);
            const isSelected = expandedTopic === topic.name;
            const hasSelection = expandedTopic !== null;

            // Determine number size based on block size
            let numberSizeClass: string;
            if (rows >= 2) {
              numberSizeClass = 'text-4xl';
            } else if (cols >= 4) {
              numberSizeClass = 'text-2xl';
            } else {
              numberSizeClass = 'text-lg';
            }

            // Determine colors based on selection state
            let bgClass: string;
            let borderColor: string;
            let nameClass: string;
            let markColor: string;

            if (isSelected) {
              bgClass = 'bg-[#FDEEDF] dark:bg-zinc-800';
              borderColor = COLORS.accent;
              nameClass = 'text-zinc-700 dark:text-zinc-300';
              markColor = COLORS.accent;
            } else if (hasSelection) {
              bgClass = 'bg-[#F7F5F2] dark:bg-zinc-800/50';
              borderColor = 'rgba(0,0,0,0.03)';
              nameClass = 'text-zinc-300 dark:text-zinc-600';
              markColor = '#c9c2b8';
            } else {
              bgClass = 'bg-[#FAF7F4] dark:bg-zinc-900';
              borderColor = 'rgba(0,0,0,0.07)';
              nameClass = 'text-zinc-700 dark:text-zinc-300';
              markColor = COLORS.accent;
            }

            return (
              <button
                key={topic.name}
                onClick={() => setExpandedTopic(isSelected ? null : topic.name)}
                className={`rounded-xl p-3 cursor-pointer text-left overflow-hidden ${bgClass} ${rows >= 2 ? 'flex flex-col justify-between h-full' : 'flex flex-row items-center justify-between'}`}
                style={{
                  gridColumn: `span ${cols}`,
                  gridRow: `span ${rows}`,
                  border: `0.5px solid ${borderColor}`,
                }}
              >
                <span className={`text-xs font-medium ${nameClass} ${rows < 2 ? 'truncate mr-2' : ''}`}>
                  {topic.name}
                </span>
                <span
                  className={`${numberSizeClass} font-medium shrink-0`}
                  style={{ color: markColor }}
                >
                  {potentialMarks}
                </span>
              </button>
            );
          })}
        </div>
      )}

      {/* Legend */}
      {syllabus && <p className="text-[11px] text-zinc-400 text-center py-3">
        Block size = mark weight &middot; tap to x-ray a topic
      </p>}

      {/* Detail Panel */}
      <AnimatePresence>
        {selectedTopicData && syllabus && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div
              className="rounded-[14px] p-6 relative bg-[#FAF7F4] dark:bg-zinc-900"
              style={{
                border: '0.5px solid rgba(0,0,0,0.1)',
              }}
            >
              {/* Header + close */}
              <div className="flex items-start justify-between mb-1">
                <h3 className="text-[22px] font-medium text-zinc-900 dark:text-white pr-8">
                  {selectedTopicData.name}
                </h3>
                <button
                  onClick={() => setExpandedTopic(null)}
                  className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors shrink-0"
                >
                  <X size={18} className="text-zinc-400" />
                </button>
              </div>

              {/* Quadrant label */}
              <p className="text-xs text-zinc-400 mb-4">
                {QUADRANT_LABELS[getQuadrant(selectedTopicData)]?.label}
              </p>

              {/* Hero marks */}
              <p className="text-[48px] font-medium leading-none" style={{ color: COLORS.accent }}>
                {Math.round((selectedTopicData.markWeight / 100) * syllabus.totalMarks)}
              </p>
              <p className="text-xs text-zinc-400 mt-1 mb-5">
                {Math.round((selectedTopicData.markWeight / 100) * syllabus.totalMarks)} marks &middot; {selectedTopicData.markWeight}% of your total grade
              </p>

              {/* Status toggle — 3-segment control */}
              {(() => {
                const topicStatus = subjectMastery[selectedTopicData.name] || 'not-started';
                const segments: { key: TopicStatus; label: string; dotClass: string; activeClasses: string }[] = [
                  { key: 'not-started', label: 'Not started', dotClass: 'bg-zinc-400', activeClasses: 'bg-zinc-200 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-200' },
                  { key: 'in-progress', label: 'In progress', dotClass: 'bg-accent', activeClasses: 'bg-accentTint text-accentDarkText' },
                  { key: 'confident', label: 'Confident', dotClass: 'bg-success', activeClasses: 'bg-successTint text-successDarkText' },
                ];
                return (
                  <div className="flex gap-1.5 mb-5 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50">
                    {segments.map(seg => {
                      const isActive = topicStatus === seg.key;
                      return (
                        <button
                          key={seg.key}
                          onClick={(e) => {
                            e.stopPropagation();
                            if (!isActive) {
                              topicMastery.setTopicConfidence(selectedSubject, selectedTopicData.name, displayToUnified(seg.key), 'manual');
                            }
                          }}
                          className={`flex-1 flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
                            isActive
                              ? `${seg.activeClasses} shadow-sm`
                              : 'text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300'
                          }`}
                        >
                          <span className={`block w-2 h-2 rounded-full shrink-0 ${isActive ? seg.dotClass : 'bg-zinc-300 dark:bg-zinc-600'}`} />
                          {seg.label}
                        </button>
                      );
                    })}
                  </div>
                );
              })()}

              {/* Three metric cards */}
              <div className="grid grid-cols-3 gap-3 mb-5">
                <div
                  className="bg-white dark:bg-zinc-900 rounded-[10px] p-3 text-center"
                  style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}
                >
                  <p className="text-xl font-medium text-zinc-800 dark:text-zinc-200">
                    {selectedTopicData.examFrequency}<span className="text-sm text-zinc-400">/10</span>
                  </p>
                  <p className="text-[10px] text-zinc-400 mt-0.5">Exam frequency</p>
                </div>
                <div
                  className="bg-white dark:bg-zinc-900 rounded-[10px] p-3 text-center"
                  style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}
                >
                  <p className="text-xl font-medium text-zinc-800 dark:text-zinc-200">
                    {selectedTopicData.difficulty}<span className="text-sm text-zinc-400">/5</span>
                  </p>
                  <p className="text-[10px] text-zinc-400 mt-0.5">Difficulty</p>
                </div>
                <div
                  className="bg-white dark:bg-zinc-900 rounded-[10px] p-3 text-center"
                  style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}
                >
                  <p className="text-xl font-medium text-zinc-800 dark:text-zinc-200">
                    {computeEfficiency(selectedTopicData, syllabus.totalMarks)}
                  </p>
                  <p className="text-[10px] text-zinc-400 mt-0.5">marks/hour</p>
                </div>
              </div>

              {/* Tip / strategy */}
              <p className="font-serif italic text-sm text-zinc-500 leading-relaxed">
                {selectedTopicData.tip}
              </p>

              {/* Sub-topics — the exact curriculum sub-topics under this strand,
                  the same nodes Catch-Up Lane and Command-Word use (single source of truth) */}
              {selectedTopicData.subtopics.length > 0 && (
                <div className="mt-5 pt-4" style={{ borderTop: '0.5px solid rgba(0,0,0,0.07)' }}>
                  <p className="text-[11px] text-zinc-400 uppercase tracking-wider mb-2">
                    Sub-topics ({selectedTopicData.subtopics.length})
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {selectedTopicData.subtopics.map((st) => (
                      <span
                        key={st.id}
                        className="text-[12px] px-2.5 py-1 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300"
                      >
                        {st.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Personal ROI overlay (F6) — where YOUR next marks are. Only rendered
          when the student has enough self-mark evidence; no empty shell. */}
      {roi && roi.entries.length > 0 && (
        <div
          className="rounded-xl p-5 bg-[#FAF7F4] dark:bg-zinc-900"
          style={{
            border: '0.5px solid rgba(0,0,0,0.07)',
          }}
        >
          <p className="text-[11px] text-zinc-400 uppercase tracking-wider mb-1">Where your next marks are</p>
          <p className="text-[12px] text-zinc-400 dark:text-zinc-500 leading-relaxed mb-3">
            What each topic has historically carried, crossed with your own self-marked accuracy from Paper Trail
            ({roi.totalSelfMarks} question{roi.totalSelfMarks !== 1 ? 's' : ''} so far). Most room to gain first —
            this is not a prediction of what will come up.
          </p>
          <div className="space-y-2">
            {roi.entries.slice(0, 5).map((entry) => (
              <button
                key={entry.topicId}
                onClick={() => setExpandedTopic(entry.topicName)}
                className="w-full flex items-center gap-3 text-left rounded-[10px] p-3 bg-white dark:bg-zinc-800/60 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
                style={{ border: '0.5px solid rgba(0,0,0,0.07)' }}
              >
                <div className="flex-1 min-w-0">
                  <p className="text-[13px] font-medium text-zinc-700 dark:text-zinc-200 truncate">{entry.topicName}</p>
                  <p className="text-[11px] text-zinc-400 mt-0.5">
                    historically carried ~{entry.historicalMarks} marks &middot; your measured accuracy: {entry.accuracy}%
                    (from {entry.sampleSize} self-marked question{entry.sampleSize !== 1 ? 's' : ''})
                  </p>
                </div>
                <div className="text-right shrink-0">
                  <p className="text-xl font-medium leading-none" style={{ color: COLORS.accent }}>{entry.roomToGain}</p>
                  <p className="text-[10px] text-zinc-400 mt-0.5">marks of room</p>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Exam Strategy Box */}
      {syllabus && (
        <div
          className="rounded-xl p-5 bg-[#FAF7F4] dark:bg-zinc-900"
          style={{
            border: '0.5px solid rgba(0,0,0,0.07)',
          }}
        >
          <p className="text-[11px] text-zinc-400 uppercase tracking-wider mb-2">Exam strategy</p>
          <p className="text-[13px] text-zinc-500 dark:text-zinc-400 leading-relaxed">
            {syllabus.keyAdvice}
          </p>
        </div>
      )}
    </div>
  );
};

export default SyllabusXRay;
