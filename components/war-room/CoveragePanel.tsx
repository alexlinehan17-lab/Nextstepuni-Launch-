/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo } from 'react';
import { Plus, X, AlertTriangle, Shield } from 'lucide-react';
import { type StudentSubjectProfile } from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import { getSyllabusTopics } from '../syllabusTopics';
import { getSyllabusForSubject, getQuadrant, QUADRANT_LABELS } from '../syllabusData';
import { type DebriefEntry } from '../StudyDebrief';
import { type useTopicMastery } from '../../hooks/useTopicMastery';
import { type UnifiedConfidence } from '../../types';
import {
  CONFIDENCE_LABELS,
  CONFIDENCE_CYCLE,
  CARD_STYLE,
  CARD_CLASS,
  type TopicEntry,
  type TopicMap,
} from './warRoomShared';

// ── Props ───────────────────────────────────────────────────

interface CoveragePanelProps {
  subjects: StudentSubjectProfile['subjects'];
  topicMastery: ReturnType<typeof useTopicMastery>;
  debriefs?: DebriefEntry[];
}

// ── Panel 1: Subject Coverage Map ───────────────────────────

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
      {/* Subject selector — selected pill uses subject colour as fill */}
      <div className="flex flex-wrap gap-1.5">
        {subjects.map((s, sIdx) => {
          const hex = getDistinctSubjectHex(s.subjectName, sIdx);
          const isActive = selectedSubject === s.subjectName;
          const stats = allSubjectStats.find(x => x.subjectName === s.subjectName);
          const showPct = stats && stats.total > 0 && stats.pct > 0;
          return (
            <button
              key={s.subjectName}
              onClick={() => setSelectedSubject(s.subjectName)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[12px] font-semibold transition-all ${
                !isActive ? 'bg-[#F0EDE8] dark:bg-zinc-700 text-[#57534E] dark:text-zinc-300' : ''
              }`}
              style={isActive
                ? { backgroundColor: hex, color: '#fff' }
                : undefined
              }
            >
              {!isActive && <span className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: hex }} />}
              {s.subjectName}
              {showPct && (
                <span className="text-[10px]" style={{ opacity: isActive ? 0.7 : 0.5 }}>{stats.pct}%</span>
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
            <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: '#22c55e' }} />
            <span style={{ color: '#57534E' }}><span className="font-bold" style={{ color: '#276749' }}>{currentStats.solid}</span> solid</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: '#f59e0b' }} />
            <span style={{ color: '#57534E' }}><span className="font-bold" style={{ color: '#92600A' }}>{currentStats.shaky}</span> shaky</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: '#d4d0ca' }} />
            <span style={{ color: '#57534E' }}><span className="font-bold" style={{ color: '#6B6B6B' }}>{currentStats.notStarted}</span> not started</span>
          </span>
          <span className="ml-auto font-bold" style={{ color: currentStats.pct >= 50 ? '#2A7D6F' : currentStats.pct >= 25 ? '#92600A' : '#C53030' }}>
            {currentStats.pct}% covered
          </span>
        </div>
      )}

      {/* Topic grid */}
      {topics.length > 0 ? (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {topics.map(topic => {
              const statusBorder = topic.confidence === 'solid' ? '#22c55e' : topic.confidence === 'shaky' ? '#f59e0b' : '#d4d0ca';
              const isNotStarted = topic.confidence === 'not-started';
              return (
                <div
                  key={topic.id}
                  className="group relative p-3 cursor-pointer hover:shadow-sm transition-all bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800"
                  style={{
                    borderLeft: `4px solid ${statusBorder}`,
                    borderRadius: 10,
                    opacity: isNotStarted ? 0.65 : 1,
                  }}
                  onClick={() => cycleConfidence(topic.name)}
                >
                  <div className="flex items-start gap-2">
                    <div className="w-2.5 h-2.5 rounded-full mt-0.5 shrink-0" style={{ backgroundColor: statusBorder }} />
                    <div className="flex-1 min-w-0">
                      <p className={`text-xs font-semibold truncate ${isNotStarted ? 'text-[#A8A29E] dark:text-zinc-500' : 'text-[#1C1917] dark:text-white'}`}>{topic.name}</p>
                      <p className="text-[10px] font-medium" style={{ color: topic.confidence === 'solid' ? '#276749' : topic.confidence === 'shaky' ? '#92600A' : '#6B6B6B' }}>
                        {CONFIDENCE_LABELS[topic.confidence]}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => { e.stopPropagation(); removeTopic(topic.name); }}
                    className="absolute top-1 right-1 w-5 h-5 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all text-[#A8A29E] dark:text-zinc-500"
                  >
                    <X size={10} />
                  </button>
                </div>
              );
            })}
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
          <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">All Subjects Overview</p>
          {allSubjectStats.filter(s => s.total > 0).map((s, sIdx, arr) => {
            const hex = getDistinctSubjectHex(s.subjectName, subjects.findIndex(sub => sub.subjectName === s.subjectName) ?? sIdx);
            const pctColor = s.pct >= 50 ? '#2A7D6F' : s.pct >= 25 ? '#92600A' : '#C53030';
            const isLast = sIdx === arr.length - 1;
            return (
              <div key={s.subjectName} className={`pb-2.5 mb-2.5 ${isLast ? '' : 'border-b border-[#F0EFED] dark:border-zinc-800'}`}>
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: hex }} />
                    <span className="text-xs font-semibold text-[#1C1917] dark:text-white">{s.subjectName}</span>
                  </div>
                  <span className="text-[10px] font-bold" style={{ color: pctColor }}>{s.pct}%</span>
                </div>
                {/* Mini heatmap row */}
                <div className="flex gap-0.5 ml-5">
                  {(topicMap[s.subjectName] || []).map(t => (
                    <div
                      key={t.id}
                      className="h-2.5 rounded-sm flex-1"
                      style={{
                        backgroundColor: t.confidence === 'solid' ? '#22c55e' : t.confidence === 'shaky' ? '#f59e0b' : '#E0DCD6',
                      }}
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

export default CoveragePanel;
