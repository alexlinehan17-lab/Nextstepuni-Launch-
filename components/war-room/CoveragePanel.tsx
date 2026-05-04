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
  CONFIDENCE_HEX,
  PAPER, PAPER_SOFT, INK, INK_SOFT, INK_MUTE, INK_FAINT, ACCENT,
  STATUS_SOLID, STATUS_SHAKY, STATUS_GAP, STATUS_GAP_DEEP,
  STATUS_SOLID_TINT, STATUS_SHAKY_TINT, STATUS_GAP_TINT, STATUS_SOLID_DEEP,
  mutedSubjectHex,
  type TopicEntry,
  type TopicMap,
} from './warRoomShared';
import {
  Overline, SectionHeader, EditorialCard, MutedProgress, Pill, ConfidenceDot,
  fieldClass, fieldStyle,
} from './warRoomPrimitives';

interface CoveragePanelProps {
  subjects: StudentSubjectProfile['subjects'];
  topicMastery: ReturnType<typeof useTopicMastery>;
  debriefs?: DebriefEntry[];
}

const CoveragePanel: React.FC<CoveragePanelProps> = ({ subjects, topicMastery, debriefs }) => {
  const [selectedSubject, setSelectedSubject] = useState(subjects[0]?.subjectName ?? '');
  const [newTopicName, setNewTopicName] = useState('');

  useEffect(() => {
    if (selectedSubject) topicMastery.importSyllabusTopics(selectedSubject);
  }, [selectedSubject]);

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
    topicMastery.setTopicConfidence(selectedSubject, _topicName, 'not-started', 'manual');
  };

  const syllabusTopics = getSyllabusTopics(selectedSubject);
  const syllabusData = getSyllabusForSubject(selectedSubject);
  const existingNames = new Set(topics.map(t => t.name.toLowerCase()));
  const unaddedSyllabus = syllabusTopics.filter(t => !existingNames.has(t.toLowerCase()));

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
    for (const name of topicNames) topicMastery.setTopicConfidence(selectedSubject, name, 'shaky', 'debrief');
  };

  const addSyllabusTopics = (topicNames: string[]) => {
    for (const name of topicNames) topicMastery.setTopicConfidence(selectedSubject, name, 'not-started', 'import');
  };

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
    <div className="space-y-7">
      {/* ── Subject chips ── */}
      <section>
        <SectionHeader overline="The map" title="Subject coverage" rule />
        <div className="mt-4 flex flex-wrap gap-2">
          {subjects.map((s, sIdx) => {
            const rawHex = getDistinctSubjectHex(s.subjectName, sIdx);
            const hex = mutedSubjectHex(rawHex, 0.22);
            const isActive = selectedSubject === s.subjectName;
            const stats = allSubjectStats.find(x => x.subjectName === s.subjectName);
            const showPct = stats && stats.total > 0 && stats.pct > 0;
            return (
              <button
                key={s.subjectName}
                onClick={() => setSelectedSubject(s.subjectName)}
                className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-[12px] font-semibold transition-colors"
                style={isActive
                  ? { background: '#fff', color: INK, border: `1.5px solid ${INK}` }
                  : { background: '#fff', color: INK_SOFT, border: `1px solid ${INK}1A` }}
              >
                <span className="w-2 h-2 rounded-full shrink-0"
                      style={{ background: hex }} />
                {s.subjectName}
                {showPct && (
                  <span className="font-mono text-[10px]"
                        style={{ opacity: isActive ? 0.85 : 0.55 }}>{stats.pct}%</span>
                )}
              </button>
            );
          })}
        </div>
      </section>

      {/* ── Add topic ── */}
      <div className="flex gap-2">
        <input
          type="text"
          value={newTopicName}
          onChange={(e) => setNewTopicName(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && addTopic()}
          placeholder="Add a topic…"
          maxLength={60}
          className={fieldClass}
          style={{ ...fieldStyle, flex: 1 }}
        />
        <button
          onClick={addTopic}
          disabled={newTopicName.trim().length < 2}
          className="px-4 rounded-lg disabled:opacity-40 transition-all flex items-center justify-center"
          style={{
            background: INK,
            color: PAPER,
            boxShadow: '0 2px 0 rgba(31,27,23,0.18)',
          }}
        >
          <Plus size={16} />
        </button>
      </div>

      {/* ── Status counters ── */}
      {currentStats && currentStats.total > 0 && (
        <div className="flex items-center flex-wrap gap-x-5 gap-y-2">
          <span className="flex items-center gap-1.5 text-[12px]" style={{ color: INK_SOFT }}>
            <ConfidenceDot confidence="solid" />
            <span className="font-bold" style={{ color: STATUS_SOLID_DEEP }}>{currentStats.solid}</span> solid
          </span>
          <span className="flex items-center gap-1.5 text-[12px]" style={{ color: INK_SOFT }}>
            <ConfidenceDot confidence="shaky" />
            <span className="font-bold" style={{ color: '#8C6022' }}>{currentStats.shaky}</span> shaky
          </span>
          <span className="flex items-center gap-1.5 text-[12px]" style={{ color: INK_SOFT }}>
            <ConfidenceDot confidence="not-started" />
            <span className="font-bold" style={{ color: INK_MUTE }}>{currentStats.notStarted}</span> not started
          </span>
          <span className="ml-auto font-mono text-[12px] font-bold tabular-nums"
                style={{ color: currentStats.pct >= 50 ? STATUS_SOLID_DEEP : currentStats.pct >= 25 ? '#8C6022' : STATUS_GAP_DEEP }}>
            {currentStats.pct}% covered
          </span>
        </div>
      )}

      {/* ── Topic tiles ── */}
      {topics.length > 0 ? (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
            {topics.map(topic => {
              const conf = CONFIDENCE_HEX[topic.confidence];
              const isNotStarted = topic.confidence === 'not-started';
              return (
                <div
                  key={topic.id}
                  role="button"
                  tabIndex={0}
                  className="group relative px-3.5 py-3 cursor-pointer transition-all"
                  style={{
                    background: '#FFFFFF',
                    border: `1px solid ${INK}14`,
                    borderRadius: 12,
                    boxShadow: '0 1px 0 rgba(31,27,23,0.03), 0 4px 12px rgba(31,27,23,0.04)',
                    opacity: isNotStarted ? 0.78 : 1,
                  }}
                  onClick={() => cycleConfidence(topic.name)}
                  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') cycleConfidence(topic.name); }}
                >
                  <div className="flex items-start gap-2">
                    <ConfidenceDot confidence={topic.confidence} />
                    <div className="flex-1 min-w-0">
                      <p className="font-serif text-[13px] font-semibold leading-snug truncate"
                         style={{ color: isNotStarted ? INK_MUTE : INK }}>
                        {topic.name}
                      </p>
                      <p className="font-sans text-[10px] uppercase tracking-[0.18em] mt-0.5"
                         style={{ color: conf.deep, fontWeight: 700 }}>
                        {CONFIDENCE_LABELS[topic.confidence]}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => { e.stopPropagation(); removeTopic(topic.name); }}
                    className="absolute top-1.5 right-1.5 w-5 h-5 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                    style={{ color: INK_MUTE }}
                    aria-label="Reset to not started"
                  >
                    <X size={11} />
                  </button>
                </div>
              );
            })}
          </div>

          {/* Debrief-seeded topic suggestions */}
          {debriefTopics.length > 0 && (
            <section className="space-y-2">
              <div className="flex items-center justify-between">
                <Overline color="#8C6022">From your debriefs</Overline>
                <button
                  onClick={() => addDebriefTopics(debriefTopics)}
                  className="text-[10px] font-bold hover:underline"
                  style={{ color: '#8C6022' }}
                >
                  Add all ({debriefTopics.length})
                </button>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {debriefTopics.map(name => (
                  <button
                    key={name}
                    onClick={() => addDebriefTopics([name])}
                    className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg transition-colors text-[10px] font-medium"
                    style={{ background: STATUS_SHAKY_TINT, border: `1px dashed ${STATUS_SHAKY}66`, color: '#8C6022' }}
                  >
                    <AlertTriangle size={9} className="shrink-0" />
                    {name}
                  </button>
                ))}
              </div>
            </section>
          )}

          {/* Show remaining syllabus topics as suggestions */}
          {sortedUnaddedSyllabus.length > 0 && (
            <button
              onClick={() => addSyllabusTopics(sortedUnaddedSyllabus)}
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-[11px] font-semibold transition-colors"
              style={{ border: `1px dashed ${INK}33`, color: INK_MUTE, background: 'transparent' }}
            >
              <Plus size={11} />
              Add {sortedUnaddedSyllabus.length} remaining syllabus topic{sortedUnaddedSyllabus.length > 1 ? 's' : ''}
            </button>
          )}
        </>
      ) : sortedUnaddedSyllabus.length > 0 || debriefTopics.length > 0 ? (
        <div className="space-y-5">
          {/* Debrief topics */}
          {debriefTopics.length > 0 && (
            <section className="space-y-2">
              <div className="flex items-center justify-between">
                <Overline color="#8C6022">From your debriefs</Overline>
                <button
                  onClick={() => addDebriefTopics(debriefTopics)}
                  className="text-[10px] font-bold hover:underline"
                  style={{ color: '#8C6022' }}
                >
                  Add all ({debriefTopics.length})
                </button>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {debriefTopics.map(name => (
                  <button
                    key={name}
                    onClick={() => addDebriefTopics([name])}
                    className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg transition-colors text-[10px] font-medium"
                    style={{ background: STATUS_SHAKY_TINT, border: `1px dashed ${STATUS_SHAKY}66`, color: '#8C6022' }}
                  >
                    <AlertTriangle size={9} className="shrink-0" />
                    {name}
                  </button>
                ))}
              </div>
            </section>
          )}
          {/* Syllabus topics with quadrant info */}
          {sortedUnaddedSyllabus.length > 0 && (
            <section className="space-y-3">
              <div className="flex items-center justify-between">
                <Overline>Syllabus topics</Overline>
                <button
                  onClick={() => addSyllabusTopics(sortedUnaddedSyllabus)}
                  className="text-[10px] font-bold hover:underline"
                  style={{ color: ACCENT }}
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
                      className="flex items-start gap-2 p-3 transition-all text-left"
                      style={{
                        background: '#FFFFFF',
                        border: `1px dashed ${INK}33`,
                        borderRadius: 10,
                      }}
                    >
                      <Plus size={12} className="shrink-0 mt-0.5" style={{ color: INK_MUTE }} />
                      <div className="flex-1 min-w-0">
                        <span className="font-serif text-[13px] font-semibold" style={{ color: INK }}>{name}</span>
                        {sxrTopic && (
                          <div className="flex items-center gap-2 mt-1">
                            {qStyle && (
                              <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full ${qStyle.bg} ${qStyle.color}`}>
                                {qStyle.label}
                              </span>
                            )}
                            <span className="font-mono text-[9px]" style={{ color: INK_FAINT }}>
                              ~{sxrTopic.markWeight}% · {sxrTopic.examFrequency}/10 yrs
                            </span>
                          </div>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            </section>
          )}
        </div>
      ) : (
        <div className="text-center py-10 space-y-3">
          <div className="w-12 h-12 mx-auto rounded-2xl flex items-center justify-center"
               style={{ background: STATUS_SHAKY_TINT, border: `1px solid ${STATUS_SHAKY}33` }}>
            <Shield size={22} style={{ color: '#8C6022' }} />
          </div>
          <p className="font-serif text-[15px] font-semibold" style={{ color: INK }}>No topics mapped yet</p>
          <p className="font-sans text-[12px] max-w-xs mx-auto leading-relaxed" style={{ color: INK_MUTE }}>
            Topics auto-import from Syllabus X-Ray when available. You can also add topics manually above.
          </p>
        </div>
      )}

      {/* ── All-subjects overview ── */}
      {allSubjectStats.some(s => s.total > 0) && (
        <section>
          <SectionHeader overline="The wider field" title="All subjects overview" rule />
          <div className="mt-3">
            <EditorialCard tone="soft">
              <div className="space-y-2">
                {allSubjectStats.filter(s => s.total > 0).map((s, sIdx, arr) => {
                  const idx = subjects.findIndex(sub => sub.subjectName === s.subjectName);
                  const rawHex = getDistinctSubjectHex(s.subjectName, idx >= 0 ? idx : sIdx);
                  const hex = mutedSubjectHex(rawHex, 0.22);
                  const pctColor = s.pct >= 50 ? STATUS_SOLID_DEEP : s.pct >= 25 ? '#8C6022' : STATUS_GAP_DEEP;
                  const isLast = sIdx === arr.length - 1;
                  const subjectTopics = topicMap[s.subjectName] || [];
                  return (
                    <div
                      key={s.subjectName}
                      className="pb-2"
                      style={isLast ? undefined : { borderBottom: `1px solid ${INK}10` }}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <span className="w-3 h-3 rounded-full shrink-0"
                                style={{ background: hex, border: `1px solid ${INK}33` }} />
                          <span className="font-serif text-[14px] font-semibold" style={{ color: INK }}>
                            {s.subjectName}
                          </span>
                        </div>
                        <span className="font-mono text-[11px] font-bold tabular-nums" style={{ color: pctColor }}>
                          {s.pct}%
                        </span>
                      </div>
                      {/* Refined segmented bar — proportional, soft fills */}
                      <div className="ml-5 flex gap-[2px] overflow-hidden rounded-full"
                           style={{ height: 5, background: `${INK}10` }}>
                        {subjectTopics.map(t => {
                          const conf = CONFIDENCE_HEX[t.confidence];
                          return (
                            <div key={t.id}
                                 className="h-full"
                                 style={{ flex: 1, background: conf.fill, opacity: t.confidence === 'not-started' ? 0.45 : 1 }}
                                 title={`${t.name}: ${CONFIDENCE_LABELS[t.confidence]}`} />
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            </EditorialCard>
          </div>
        </section>
      )}
    </div>
  );
};

export default CoveragePanel;
