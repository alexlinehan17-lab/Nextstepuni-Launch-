/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo } from 'react';
import { Plus, X, AlertTriangle } from 'lucide-react';
import { type StudentSubjectProfile } from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import { getSyllabusTopicRefs } from '../syllabusTopics';
import { getSyllabusForSubject, getQuadrant, QUADRANT_LABELS } from '../syllabusData';
import { examinationYearFromDate, resolveCurriculumSpecification } from '../../curriculumRegistry';
import { type DebriefEntry } from '../StudyDebrief';
import { type useTopicMastery } from '../../hooks/useTopicMastery';
import { type UnifiedConfidence } from '../../types';
import {
  CONFIDENCE_LABELS,
  CONFIDENCE_CYCLE,
  CONFIDENCE_HEX,
  STATUS_SHAKY,
  mutedSubjectHex,
  type TopicEntry,
  type TopicMap,
} from './warRoomShared';
import { ConfidenceDot, fieldClass, fieldStyle } from './warRoomPrimitives';

interface CoveragePanelProps {
  subjects: StudentSubjectProfile['subjects'];
  topicMastery: ReturnType<typeof useTopicMastery>;
  debriefs?: DebriefEntry[];
  examDate?: string | null;
}

const CoveragePanel: React.FC<CoveragePanelProps> = ({ subjects, topicMastery, debriefs, examDate }) => {
  const [selectedSubject, setSelectedSubject] = useState(subjects[0]?.subjectName ?? '');
  const [newTopicName, setNewTopicName] = useState('');

  useEffect(() => {
    if (subjects.some(subject => subject.subjectName === selectedSubject)) return;
    setSelectedSubject(subjects[0]?.subjectName ?? '');
  }, [selectedSubject, subjects]);

  useEffect(() => {
    if (selectedSubject) topicMastery.importSyllabusTopics(selectedSubject, examDate);
  }, [selectedSubject, examDate]);

  const topics: TopicEntry[] = useMemo(() => {
    const subjectTopics = topicMastery.getSubjectTopics(selectedSubject);
    const canonical = topicMastery.getCanonicalSubjectTopics(selectedSubject);
    const refs = getSyllabusTopicRefs(selectedSubject, examDate);
    const canonicalNames = new Set(refs.map((ref) => ref.name.toLowerCase()));
    const curriculumTopics = refs.map((ref) => {
      const entry = canonical[ref.id] ?? subjectTopics[ref.name];
      return {
        id: ref.id,
        name: ref.name,
        confidence: (entry?.confidence ?? 'not-started') as TopicEntry['confidence'],
        updatedAt: entry?.updatedAt ?? 0,
      };
    });
    const customTopics = Object.entries(subjectTopics)
      .filter(([name]) => !canonicalNames.has(name.toLowerCase()))
      .map(([name, entry]) => ({
        id: `custom:${selectedSubject}:${name}`,
        name,
        confidence: entry.confidence as TopicEntry['confidence'],
        updatedAt: entry.updatedAt,
      }));
    return [...curriculumTopics, ...customTopics];
  }, [topicMastery, selectedSubject, examDate]);

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

  const syllabusTopics = getSyllabusTopicRefs(selectedSubject, examDate).map((topic) => topic.name);
  const curriculumSpecification = resolveCurriculumSpecification(
    selectedSubject,
    examinationYearFromDate(examDate),
  );
  const syllabusData = getSyllabusForSubject(selectedSubject, examDate);
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
    <div className="war-room-coverage space-y-8">
      <style>{`
        .war-room-coverage .coverage-subject-control:focus-visible {
          outline: 2px solid var(--outline-strong) !important;
          outline-offset: 2px !important;
        }
        .war-room-coverage .coverage-topic-tile:focus-within {
          outline: 2px solid var(--outline-strong) !important;
          outline-offset: 2px !important;
        }
        .war-room-coverage .coverage-topic-cycle:focus-visible {
          outline: none !important;
        }
        .war-room-coverage .coverage-topic-reset:focus-visible {
          opacity: 1 !important;
          outline: 2px solid var(--outline-strong) !important;
          outline-offset: -3px !important;
        }
        @media (pointer: coarse) {
          .war-room-coverage .coverage-topic-reset {
            opacity: 1 !important;
          }
        }
      `}</style>
      <section aria-labelledby="coverage-heading">
        <div className="border-b border-[var(--outline-soft)] pb-4">
          <h3 id="coverage-heading" className="text-lg font-semibold tracking-[-0.01em] text-[var(--ink-primary)]">
            Coverage and confidence
          </h3>
          <p className="mt-1.5 max-w-2xl text-[13px] leading-5 text-[var(--ink-secondary)]">
            Choose a subject, then mark each topic as not started, shaky or solid.
          </p>
        </div>

        <div className="mt-4 grid grid-cols-2 gap-2 sm:flex sm:flex-wrap" aria-label="Choose a subject">
          {subjects.map((subject, subjectIndex) => {
            const color = mutedSubjectHex(getDistinctSubjectHex(subject.subjectName, subjectIndex), 0.22);
            const isActive = selectedSubject === subject.subjectName;
            const stats = allSubjectStats.find(item => item.subjectName === subject.subjectName);
            const showPercentage = Boolean(stats && stats.total > 0);
            return (
              <button
                key={subject.subjectName}
                type="button"
                onClick={() => setSelectedSubject(subject.subjectName)}
                aria-pressed={isActive}
                className={`coverage-subject-control inline-flex min-h-10 items-center gap-2 rounded-[7px] border px-3 py-1.5 text-left text-xs font-semibold transition-[border-color,background-color,color] ${
                  isActive
                    ? 'border-[var(--outline-strong)] bg-[var(--surface-paper)] text-[var(--ink-primary)]'
                    : 'border-[var(--outline-soft)] bg-transparent text-[var(--ink-secondary)] hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)]'
                }`}
                style={isActive ? { border: '1.5px solid var(--outline-strong)' } : undefined}
              >
                <span
                  className="h-2 w-2 shrink-0 rounded-full border border-black/10"
                  style={{ background: color }}
                  aria-hidden="true"
                />
                <span className="min-w-0 truncate">{subject.subjectName}</span>
                {showPercentage && (
                  <span className="ml-auto text-[10px] font-medium tabular-nums text-[var(--ink-muted)]">
                    {stats?.pct}%
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {curriculumSpecification?.selectionRules?.length ? (
          <p className="mt-4 border-y border-[var(--outline-soft)] py-3 text-xs leading-5 text-[var(--ink-secondary)]">
            <span className="font-semibold text-[var(--ink-primary)]">Subject choices: </span>
            {curriculumSpecification.selectionRules.map(rule => rule.description).join(' ')}
          </p>
        ) : null}
      </section>

      <section aria-labelledby="selected-subject-heading">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Topic map</p>
            <h4 id="selected-subject-heading" className="mt-1 text-sm font-semibold text-[var(--ink-primary)]">
              {selectedSubject || 'No subject selected'}
            </h4>
          </div>

          <div className="flex w-full gap-2 sm:max-w-sm">
            <input
              type="text"
              value={newTopicName}
              onChange={event => setNewTopicName(event.target.value)}
              onKeyDown={event => event.key === 'Enter' && addTopic()}
              placeholder="Add a topic"
              aria-label="New topic name"
              maxLength={60}
              className={`${fieldClass} min-h-10 rounded-[7px] text-xs focus:outline focus:outline-2 focus:outline-offset-1 focus:outline-[var(--outline-strong)]`}
              style={{ ...fieldStyle, flex: 1, boxShadow: 'none' }}
            />
            <button
              type="button"
              onClick={addTopic}
              disabled={newTopicName.trim().length < 2}
              aria-label="Add topic"
              className="flex min-h-10 min-w-10 items-center justify-center rounded-[7px] bg-[var(--ink-primary)] px-3 text-[var(--surface-paper)] transition-opacity disabled:cursor-not-allowed disabled:opacity-35 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
            >
              <Plus size={15} aria-hidden="true" />
            </button>
          </div>
        </div>

        {currentStats && currentStats.total > 0 && (
          <div className="mt-4 flex flex-wrap items-center gap-x-5 gap-y-2 border-y border-[var(--outline-soft)] py-3" aria-label={`${selectedSubject} coverage summary`}>
            <span className="flex items-center gap-1.5 text-xs text-[var(--ink-secondary)]">
              <ConfidenceDot confidence="solid" size={8} />
              <span className="font-semibold text-[var(--ink-primary)]">{currentStats.solid}</span> solid
            </span>
            <span className="flex items-center gap-1.5 text-xs text-[var(--ink-secondary)]">
              <ConfidenceDot confidence="shaky" size={8} />
              <span className="font-semibold text-[var(--ink-primary)]">{currentStats.shaky}</span> shaky
            </span>
            <span className="flex items-center gap-1.5 text-xs text-[var(--ink-secondary)]">
              <ConfidenceDot confidence="not-started" size={8} />
              <span className="font-semibold text-[var(--ink-primary)]">{currentStats.notStarted}</span> not started
            </span>
            <span className="ml-auto text-[11px] font-semibold tabular-nums text-[var(--ink-primary)]">
              {currentStats.pct}% covered
            </span>
          </div>
        )}

        <div className="mt-4">
          {topics.length > 0 ? (
            <>
              <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                {topics.map(topic => {
                  const isNotStarted = topic.confidence === 'not-started';
                  return (
                    <div
                      key={topic.id}
                      className="coverage-topic-tile group relative rounded-[8px] border bg-[var(--surface-paper)] transition-[border-color,box-shadow]"
                      style={{ borderColor: 'var(--outline-soft)' }}
                    >
                      <button
                        type="button"
                        onClick={() => cycleConfidence(topic.name)}
                        aria-label={`${topic.name}: ${CONFIDENCE_LABELS[topic.confidence]}. Change confidence`}
                        className="coverage-topic-cycle min-h-[58px] w-full rounded-[7px] px-3 py-2.5 pr-10 text-left focus:outline-none"
                      >
                        <span className="flex items-start gap-2.5">
                          <span className="pt-0.5"><ConfidenceDot confidence={topic.confidence} size={9} /></span>
                          <span className="min-w-0 flex-1">
                            <span className={`block break-words text-[13px] font-semibold leading-5 ${isNotStarted ? 'text-[var(--ink-secondary)]' : 'text-[var(--ink-primary)]'}`}>
                              {topic.name}
                            </span>
                            <span className="mt-0.5 block text-[10px] font-semibold uppercase tracking-[0.12em] text-[var(--ink-secondary)]">
                              {CONFIDENCE_LABELS[topic.confidence]}
                            </span>
                          </span>
                        </span>
                      </button>
                      <button
                        type="button"
                        onClick={event => { event.stopPropagation(); removeTopic(topic.name); }}
                        className="coverage-topic-reset absolute right-2 top-2 flex h-7 w-7 items-center justify-center rounded-[6px] text-[var(--ink-muted)] opacity-0 transition-[opacity,background-color,color] hover:bg-[var(--surface-soft)] hover:text-[var(--ink-primary)] focus:opacity-100 focus:outline-none group-hover:opacity-100"
                        aria-label={`Reset ${topic.name} to not started`}
                      >
                        <X size={12} aria-hidden="true" />
                      </button>
                    </div>
                  );
                })}
              </div>

              {debriefTopics.length > 0 && (
                <section className="mt-6 border-t border-[var(--outline-soft)] pt-5" aria-labelledby="debrief-suggestions-heading">
                  <div className="flex items-center justify-between gap-4">
                    <h5 id="debrief-suggestions-heading" className="text-xs font-semibold text-[var(--ink-primary)]">From your debriefs</h5>
                    <button
                      type="button"
                      onClick={() => addDebriefTopics(debriefTopics)}
                      className="min-h-8 text-[11px] font-semibold text-[var(--ink-secondary)] underline decoration-[var(--outline-soft)] underline-offset-4 hover:text-[var(--ink-primary)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
                    >
                      Add all ({debriefTopics.length})
                    </button>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {debriefTopics.map(name => (
                      <button
                        key={name}
                        type="button"
                        onClick={() => addDebriefTopics([name])}
                        className="inline-flex min-h-9 items-center gap-1.5 rounded-[7px] border border-[var(--outline-soft)] bg-transparent px-2.5 py-1.5 text-[11px] font-medium text-[var(--ink-secondary)] hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
                      >
                        <AlertTriangle size={10} className="shrink-0" style={{ color: STATUS_SHAKY }} aria-hidden="true" />
                        {name}
                      </button>
                    ))}
                  </div>
                </section>
              )}

              {sortedUnaddedSyllabus.length > 0 && (
                <button
                  type="button"
                  onClick={() => addSyllabusTopics(sortedUnaddedSyllabus)}
                  className="mt-6 flex min-h-10 w-full items-center justify-center gap-2 rounded-[7px] border border-[var(--outline-soft)] bg-transparent px-4 py-2 text-[11px] font-semibold text-[var(--ink-secondary)] hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
                >
                  <Plus size={12} aria-hidden="true" />
                  Add {sortedUnaddedSyllabus.length} remaining syllabus topic{sortedUnaddedSyllabus.length > 1 ? 's' : ''}
                </button>
              )}
            </>
          ) : sortedUnaddedSyllabus.length > 0 || debriefTopics.length > 0 ? (
            <div className="border-y border-[var(--outline-soft)]">
              {debriefTopics.length > 0 && (
                <section className="py-4" aria-labelledby="empty-debrief-suggestions-heading">
                  <div className="flex items-center justify-between gap-4 px-1">
                    <h5 id="empty-debrief-suggestions-heading" className="text-xs font-semibold text-[var(--ink-primary)]">From your debriefs</h5>
                    <button
                      type="button"
                      onClick={() => addDebriefTopics(debriefTopics)}
                      className="min-h-8 text-[11px] font-semibold text-[var(--ink-secondary)] underline decoration-[var(--outline-soft)] underline-offset-4 hover:text-[var(--ink-primary)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
                    >
                      Add all ({debriefTopics.length})
                    </button>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {debriefTopics.map(name => (
                      <button
                        key={name}
                        type="button"
                        onClick={() => addDebriefTopics([name])}
                        className="inline-flex min-h-9 items-center gap-1.5 rounded-[7px] border border-[var(--outline-soft)] px-2.5 py-1.5 text-[11px] font-medium text-[var(--ink-secondary)] hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
                      >
                        <AlertTriangle size={10} className="shrink-0" style={{ color: STATUS_SHAKY }} aria-hidden="true" />
                        {name}
                      </button>
                    ))}
                  </div>
                </section>
              )}

              {sortedUnaddedSyllabus.length > 0 && (
                <section className={debriefTopics.length > 0 ? 'border-t border-[var(--outline-soft)] py-4' : 'py-4'} aria-labelledby="syllabus-suggestions-heading">
                  <div className="flex items-center justify-between gap-4 px-1">
                    <div>
                      <h5 id="syllabus-suggestions-heading" className="text-xs font-semibold text-[var(--ink-primary)]">Syllabus topics</h5>
                      <p className="mt-0.5 text-[11px] text-[var(--ink-muted)]">Select a topic to add it to your map.</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => addSyllabusTopics(sortedUnaddedSyllabus)}
                      className="min-h-8 shrink-0 text-[11px] font-semibold text-[var(--ink-secondary)] underline decoration-[var(--outline-soft)] underline-offset-4 hover:text-[var(--ink-primary)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
                    >
                      Add all ({sortedUnaddedSyllabus.length})
                    </button>
                  </div>
                  <div className="mt-3 border-t border-[var(--outline-soft)]">
                    {sortedUnaddedSyllabus.map(name => {
                      const syllabusTopic = syllabusData?.topics.find(topic => topic.name === name);
                      const quadrant = syllabusTopic ? getQuadrant(syllabusTopic) : null;
                      const quadrantLabel = quadrant ? QUADRANT_LABELS[quadrant].label : null;
                      return (
                        <button
                          key={name}
                          type="button"
                          onClick={() => addSyllabusTopics([name])}
                          className="group flex min-h-12 w-full items-center gap-3 border-b border-[var(--outline-soft)] px-1 py-2.5 text-left hover:bg-[var(--surface-soft)] focus-visible:z-10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--outline-strong)]"
                        >
                          <Plus size={12} className="shrink-0 text-[var(--ink-muted)] group-hover:text-[var(--ink-primary)]" aria-hidden="true" />
                          <span className="min-w-0 flex-1">
                            <span className="block text-xs font-semibold text-[var(--ink-primary)]">{name}</span>
                            {syllabusTopic && (
                              <span className="mt-0.5 flex flex-wrap items-center gap-x-2 gap-y-0.5 text-[10px] text-[var(--ink-muted)]">
                                {quadrantLabel && <span className="font-semibold">{quadrantLabel}</span>}
                                <span className="tabular-nums">~{syllabusTopic.markWeight}% · {syllabusTopic.examFrequency}/10 yrs</span>
                              </span>
                            )}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                </section>
              )}
            </div>
          ) : (
            <div className="border-y border-[var(--outline-soft)] py-6">
              <p className="text-sm font-semibold text-[var(--ink-primary)]">No topics mapped yet</p>
              <p className="mt-1 max-w-lg text-xs leading-5 text-[var(--ink-secondary)]">
                Add a topic above. Syllabus topics will appear here automatically when they are available.
              </p>
            </div>
          )}
        </div>
      </section>

      {allSubjectStats.some(subject => subject.total > 0) && (
        <section className="border-t border-[var(--outline-soft)] pt-6" aria-labelledby="all-subjects-heading">
          <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-[var(--ink-muted)]">Overview</p>
          <h4 id="all-subjects-heading" className="mt-1 text-sm font-semibold text-[var(--ink-primary)]">All subjects</h4>
          <div className="mt-3 border-y border-[var(--outline-soft)]">
            {allSubjectStats.filter(subject => subject.total > 0).map((subject, subjectIndex) => {
              const index = subjects.findIndex(item => item.subjectName === subject.subjectName);
              const color = mutedSubjectHex(getDistinctSubjectHex(subject.subjectName, index >= 0 ? index : subjectIndex), 0.22);
              const subjectTopics = topicMap[subject.subjectName] || [];
              return (
                <div key={subject.subjectName} className="border-b border-[var(--outline-soft)] py-3 last:border-b-0">
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex min-w-0 items-center gap-2.5">
                      <span className="h-2 w-2 shrink-0 rounded-full border border-black/10" style={{ background: color }} aria-hidden="true" />
                      <span className="truncate text-xs font-semibold text-[var(--ink-primary)]">{subject.subjectName}</span>
                    </div>
                    <span className="text-[11px] font-semibold tabular-nums text-[var(--ink-secondary)]">{subject.pct}%</span>
                  </div>
                  <div className="ml-[18px] mt-2 flex h-1 gap-px overflow-hidden bg-[var(--outline-soft)]" aria-hidden="true">
                    {subjectTopics.map(topic => (
                      <span
                        key={topic.id}
                        className="h-full"
                        style={{
                          flex: 1,
                          background: CONFIDENCE_HEX[topic.confidence].fill,
                          opacity: topic.confidence === 'not-started' ? 0.35 : 1,
                        }}
                        title={`${topic.name}: ${CONFIDENCE_LABELS[topic.confidence]}`}
                      />
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      )}
    </div>
  );
};

export default CoveragePanel;
