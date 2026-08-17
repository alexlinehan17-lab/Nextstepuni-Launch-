/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ExternalLink,
  Plus,
  Search,
  ShieldCheck,
  X,
} from 'lucide-react';
import { type StudentSubjectProfile } from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import { getSyllabusTopicRefs } from '../syllabusTopics';
import {
  examinationYearFromDate,
  getCurriculumCohortNotice,
  resolveCurriculumSpecification,
} from '../../curriculumRegistry';
import { type DebriefEntry } from '../StudyDebrief';
import { type useTopicMastery } from '../../hooks/useTopicMastery';
import { type UnifiedConfidence } from '../../types';
import {
  CONFIDENCE_CYCLE,
  CONFIDENCE_HEX,
  CONFIDENCE_LABELS,
  STATUS_SHAKY,
  mutedSubjectHex,
  type TopicEntry,
} from './warRoomShared';
import {
  ConfidenceDot,
  EditorialCard,
  fieldClass,
  fieldStyle,
} from './warRoomPrimitives';

interface CoveragePanelProps {
  subjects: StudentSubjectProfile['subjects'];
  topicMastery: ReturnType<typeof useTopicMastery>;
  debriefs?: DebriefEntry[];
  examDate?: string | null;
}

type CoverageFilter = 'all' | TopicEntry['confidence'];

interface CoverageStats {
  total: number;
  solid: number;
  shaky: number;
  notStarted: number;
  started: number;
  startedPct: number;
  solidPct: number;
}

interface TopicGroup {
  id: string;
  title: string;
  topics: TopicEntry[];
  isCustom?: boolean;
}

const EMPTY_STATS: CoverageStats = {
  total: 0,
  solid: 0,
  shaky: 0,
  notStarted: 0,
  started: 0,
  startedPct: 0,
  solidPct: 0,
};

function statsFor(topics: TopicEntry[]): CoverageStats {
  if (topics.length === 0) return EMPTY_STATS;
  const solid = topics.filter(topic => topic.confidence === 'solid').length;
  const shaky = topics.filter(topic => topic.confidence === 'shaky').length;
  const notStarted = topics.length - solid - shaky;
  const started = solid + shaky;
  return {
    total: topics.length,
    solid,
    shaky,
    notStarted,
    started,
    startedPct: Math.round((started / topics.length) * 100),
    solidPct: Math.round((solid / topics.length) * 100),
  };
}

const StatusRail: React.FC<{ stats: CoverageStats; height?: number }> = ({ stats, height = 6 }) => {
  if (stats.total === 0) {
    return <div className="w-full rounded-full bg-[var(--outline-soft)]" style={{ height }} aria-hidden="true" />;
  }
  return (
    <div
      className="flex w-full overflow-hidden rounded-full bg-[var(--outline-soft)]"
      style={{ height }}
      aria-hidden="true"
    >
      {stats.solid > 0 && (
        <span style={{ width: `${(stats.solid / stats.total) * 100}%`, background: CONFIDENCE_HEX.solid.fill }} />
      )}
      {stats.shaky > 0 && (
        <span style={{ width: `${(stats.shaky / stats.total) * 100}%`, background: CONFIDENCE_HEX.shaky.fill }} />
      )}
      {stats.notStarted > 0 && (
        <span
          style={{
            width: `${(stats.notStarted / stats.total) * 100}%`,
            background: CONFIDENCE_HEX['not-started'].fill,
            opacity: 0.55,
          }}
        />
      )}
    </div>
  );
};

const CoverageRing: React.FC<{ stats: CoverageStats; subject: string }> = ({ stats, subject }) => {
  const radius = 46;
  const circumference = 2 * Math.PI * radius;
  const solidLength = stats.total ? circumference * (stats.solid / stats.total) : 0;
  const shakyLength = stats.total ? circumference * (stats.shaky / stats.total) : 0;
  const label = stats.total
    ? `${subject}: ${stats.started} of ${stats.total} topics started, ${stats.solid} solid`
    : `${subject}: no verified topics available`;

  return (
    <div className="relative h-[132px] w-[132px] shrink-0" role="img" aria-label={label}>
      <svg className="h-full w-full -rotate-90" viewBox="0 0 120 120" aria-hidden="true">
        <circle cx="60" cy="60" r={radius} fill="none" stroke="var(--outline-soft)" strokeWidth="9" />
        {solidLength > 0 && (
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            stroke={CONFIDENCE_HEX.solid.fill}
            strokeWidth="9"
            strokeLinecap="round"
            strokeDasharray={`${solidLength} ${circumference - solidLength}`}
          />
        )}
        {shakyLength > 0 && (
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            stroke={CONFIDENCE_HEX.shaky.fill}
            strokeWidth="9"
            strokeLinecap="round"
            strokeDasharray={`${shakyLength} ${circumference - shakyLength}`}
            strokeDashoffset={-solidLength}
          />
        )}
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="font-serif text-[29px] font-semibold leading-none text-[var(--ink-primary)]">
          {stats.total ? `${stats.started}/${stats.total}` : '—'}
        </span>
        <span className="mt-1 text-[9px] font-semibold uppercase tracking-[0.16em] text-[var(--ink-muted)]">
          started
        </span>
      </div>
    </div>
  );
};

const CoveragePanel: React.FC<CoveragePanelProps> = ({ subjects, topicMastery, debriefs, examDate }) => {
  const [selectedSubject, setSelectedSubject] = useState(subjects[0]?.subjectName ?? '');
  const [newTopicName, setNewTopicName] = useState('');
  const [filter, setFilter] = useState<CoverageFilter>('all');
  const [query, setQuery] = useState('');

  useEffect(() => {
    if (subjects.some(subject => subject.subjectName === selectedSubject)) return;
    setSelectedSubject(subjects[0]?.subjectName ?? '');
  }, [selectedSubject, subjects]);

  useEffect(() => {
    setFilter('all');
    setQuery('');
    if (selectedSubject) topicMastery.importSyllabusTopics(selectedSubject, examDate);
  }, [selectedSubject, examDate]);

  const examYear = examinationYearFromDate(examDate);
  const curriculumSpecification = resolveCurriculumSpecification(selectedSubject, examYear);
  const verifiedSpecification = curriculumSpecification?.status === 'verified'
    ? curriculumSpecification
    : undefined;
  const cohortNotice = getCurriculumCohortNotice(selectedSubject, examYear);
  const syllabusRefs = useMemo(
    () => getSyllabusTopicRefs(selectedSubject, examDate),
    [selectedSubject, examDate],
  );

  const officialTopics = useMemo<TopicEntry[]>(() => {
    const subjectTopics = topicMastery.getSubjectTopics(selectedSubject);
    const canonical = topicMastery.getCanonicalSubjectTopics(selectedSubject);
    return syllabusRefs.map(ref => {
      const entry = canonical[ref.id] ?? subjectTopics[ref.name];
      return {
        id: ref.id,
        name: ref.name,
        confidence: (entry?.confidence ?? 'not-started') as TopicEntry['confidence'],
        updatedAt: entry?.updatedAt ?? 0,
      };
    });
  }, [topicMastery, selectedSubject, syllabusRefs]);

  const customTopics = useMemo<TopicEntry[]>(() => {
    const subjectTopics = topicMastery.getSubjectTopics(selectedSubject);
    const canonicalNames = new Set(syllabusRefs.map(ref => ref.name.toLowerCase()));
    return Object.entries(subjectTopics)
      .filter(([name, entry]) => !canonicalNames.has(name.toLowerCase()) && entry.source !== 'import')
      .map(([name, entry]) => ({
        id: `custom:${selectedSubject}:${name}`,
        name,
        confidence: entry.confidence as TopicEntry['confidence'],
        updatedAt: entry.updatedAt,
      }));
  }, [topicMastery, selectedSubject, syllabusRefs]);

  const currentStats = useMemo(() => statsFor(officialTopics), [officialTopics]);
  const allTopics = useMemo(() => [...officialTopics, ...customTopics], [officialTopics, customTopics]);

  const allSubjectStats = useMemo(() => subjects.map(subject => {
    const refs = getSyllabusTopicRefs(subject.subjectName, examDate);
    const subjectTopics = topicMastery.getSubjectTopics(subject.subjectName);
    const canonical = topicMastery.getCanonicalSubjectTopics(subject.subjectName);
    const entries = refs.map(ref => {
      const entry = canonical[ref.id] ?? subjectTopics[ref.name];
      return {
        id: ref.id,
        name: ref.name,
        confidence: (entry?.confidence ?? 'not-started') as TopicEntry['confidence'],
        updatedAt: entry?.updatedAt ?? 0,
      };
    });
    return { subjectName: subject.subjectName, ...statsFor(entries) };
  }), [subjects, topicMastery, examDate]);

  const topicGroups = useMemo<TopicGroup[]>(() => {
    if (!verifiedSpecification) return customTopics.length
      ? [{ id: 'custom', title: 'Your own topics', topics: customTopics, isCustom: true }]
      : [];

    const byId = new Map(officialTopics.map(topic => [topic.id, topic]));
    const officialGroups: TopicGroup[] = verifiedSpecification.coverageNodeLevel === 'topic'
      ? verifiedSpecification.groups.map(group => ({
          id: group.id,
          title: group.title,
          topics: group.topics.flatMap(topic => {
            const entry = byId.get(topic.id);
            return entry ? [entry] : [];
          }),
        })).filter(group => group.topics.length > 0)
      : [{
          id: 'official-syllabus-areas',
          title: 'Official syllabus areas',
          topics: curriculumSpecification.groups.flatMap(group => {
            const entry = byId.get(group.id);
            return entry ? [entry] : [];
          }),
        }];

    return customTopics.length
      ? [...officialGroups, { id: 'custom', title: 'Your own topics', topics: customTopics, isCustom: true }]
      : officialGroups;
  }, [verifiedSpecification, officialTopics, customTopics]);

  const visibleGroups = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    return topicGroups.map(group => ({
      ...group,
      topics: group.topics.filter(topic => (
        (filter === 'all' || topic.confidence === filter)
        && (!normalizedQuery || topic.name.toLowerCase().includes(normalizedQuery))
      )),
    })).filter(group => group.topics.length > 0);
  }, [filter, query, topicGroups]);

  const existingNames = useMemo(
    () => new Set(allTopics.map(topic => topic.name.toLowerCase())),
    [allTopics],
  );
  const debriefTopics = useMemo(() => {
    if (!debriefs?.length) return [];
    const seen = new Set<string>();
    return debriefs.flatMap(debrief => {
      if (debrief.subject !== selectedSubject) return [];
      if (!debrief.hardestTopic || debrief.hardestTopic === 'Not specified') return [];
      const key = debrief.hardestTopic.toLowerCase();
      if (existingNames.has(key) || seen.has(key)) return [];
      seen.add(key);
      return [debrief.hardestTopic];
    });
  }, [debriefs, existingNames, selectedSubject]);

  const addTopic = () => {
    const trimmed = newTopicName.trim();
    if (trimmed.length < 2 || existingNames.has(trimmed.toLowerCase())) return;
    topicMastery.setTopicConfidence(selectedSubject, trimmed, 'not-started', 'manual');
    setNewTopicName('');
  };

  const cycleConfidence = (topicName: string) => {
    const current = topicMastery.getTopicConfidence(selectedSubject, topicName);
    const next = CONFIDENCE_CYCLE[current] as UnifiedConfidence;
    topicMastery.setTopicConfidence(selectedSubject, topicName, next, 'manual');
  };

  const resetTopic = (topicName: string) => {
    topicMastery.setTopicConfidence(selectedSubject, topicName, 'not-started', 'manual');
  };

  const addDebriefTopics = (topicNames: string[]) => {
    for (const name of topicNames) topicMastery.setTopicConfidence(selectedSubject, name, 'shaky', 'debrief');
  };

  const primarySource = verifiedSpecification?.sources.find(source => source.role === 'content')
    ?? verifiedSpecification?.sources[0];
  const displayedSubjectName = verifiedSpecification?.subjectName ?? selectedSubject;

  const filters: Array<{ id: CoverageFilter; label: string; count: number }> = [
    { id: 'all', label: 'All', count: allTopics.length },
    { id: 'not-started', label: 'Not started', count: allTopics.filter(topic => topic.confidence === 'not-started').length },
    { id: 'shaky', label: 'Shaky', count: allTopics.filter(topic => topic.confidence === 'shaky').length },
    { id: 'solid', label: 'Solid', count: allTopics.filter(topic => topic.confidence === 'solid').length },
  ];

  return (
    <div className="war-room-coverage space-y-9">
      <style>{`
        .war-room-coverage .coverage-subject-control:focus-visible,
        .war-room-coverage .coverage-topic-tile:focus-within {
          outline: 2px solid var(--outline-strong) !important;
          outline-offset: 2px !important;
        }
        .war-room-coverage .coverage-topic-cycle:focus-visible { outline: none !important; }
        .war-room-coverage .coverage-topic-reset:focus-visible {
          opacity: 1 !important;
          outline: 2px solid var(--outline-strong) !important;
          outline-offset: -3px !important;
        }
        .war-room-coverage .coverage-scroll { scrollbar-width: none; }
        .war-room-coverage .coverage-scroll::-webkit-scrollbar { display: none; }
        @media (pointer: coarse) {
          .war-room-coverage .coverage-topic-reset { opacity: 1 !important; }
        }
      `}</style>

      <section aria-labelledby="coverage-heading">
        <div className="border-b border-[var(--outline-soft)] pb-5">
          <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-[var(--ink-muted)]">Curriculum map</p>
          <h3 id="coverage-heading" className="mt-1.5 font-serif text-[24px] font-semibold tracking-[-0.02em] text-[var(--ink-primary)] sm:text-[28px]">
            Coverage and confidence
          </h3>
          <p className="mt-2 max-w-2xl text-[13px] leading-6 text-[var(--ink-secondary)]">
            One cohort-safe view of the official syllabus, your confidence and the gaps surfaced in study debriefs. Tap a topic to move it from not started to shaky to solid.
          </p>
        </div>

        <div className="coverage-scroll mt-4 overflow-x-auto pb-2" aria-label="Choose a subject">
          <div className="flex min-w-max gap-2.5">
            {subjects.map((subject, subjectIndex) => {
              const color = mutedSubjectHex(getDistinctSubjectHex(subject.subjectName, subjectIndex), 0.18);
              const isActive = selectedSubject === subject.subjectName;
              const stats = allSubjectStats.find(item => item.subjectName === subject.subjectName) ?? EMPTY_STATS;
              return (
                <button
                  key={subject.subjectName}
                  type="button"
                  onClick={() => setSelectedSubject(subject.subjectName)}
                  aria-label={subject.subjectName}
                  aria-pressed={isActive}
                  className={`coverage-subject-control min-h-[74px] w-[164px] rounded-[12px] border px-3.5 py-3 text-left transition-[border-color,background-color,transform] ${
                    isActive
                      ? 'border-[var(--outline-strong)] bg-[var(--surface-paper)]'
                      : 'border-[var(--outline-soft)] bg-[var(--surface-soft)] hover:border-[var(--outline-strong)]'
                  }`}
                  style={isActive ? { borderWidth: 1.5, transform: 'translateY(-1px)' } : undefined}
                >
                  <span className="flex items-center gap-2">
                    <span className="h-2.5 w-2.5 shrink-0 rounded-full border border-black/10" style={{ background: color }} aria-hidden="true" />
                    <span className="truncate text-xs font-semibold text-[var(--ink-primary)]">{subject.subjectName}</span>
                  </span>
                  <span className="mt-2.5 block"><StatusRail stats={stats} height={5} /></span>
                  <span className="mt-1.5 block text-[10px] tabular-nums text-[var(--ink-muted)]">
                    {stats.total ? `${stats.started} of ${stats.total} started` : 'Map being checked'}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </section>

      {selectedSubject && (
        <section className="grid gap-4 lg:grid-cols-[minmax(0,1.45fr)_minmax(280px,.75fr)]" aria-labelledby="selected-subject-heading">
          <EditorialCard className="relative overflow-hidden" style={{ minHeight: 224 }}>
            <div
              className="absolute -right-14 -top-20 h-48 w-48 rounded-full opacity-50"
              style={{ background: 'radial-gradient(circle, color-mix(in srgb, #F26B1F 14%, transparent), transparent 68%)' }}
              aria-hidden="true"
            />
            <div className="relative">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
                  Exam cohort {examYear}
                </span>
                {verifiedSpecification ? (
                  <span className="inline-flex items-center gap-1 rounded-full border border-[var(--outline-soft)] bg-[var(--surface-soft)] px-2 py-1 text-[9px] font-semibold uppercase tracking-[0.12em] text-[var(--ink-secondary)]">
                    <ShieldCheck size={11} aria-hidden="true" /> Official source checked
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 rounded-full border border-[var(--outline-soft)] bg-[var(--surface-soft)] px-2 py-1 text-[9px] font-semibold uppercase tracking-[0.12em] text-[var(--ink-secondary)]">
                    <AlertTriangle size={11} aria-hidden="true" /> Source check in progress
                  </span>
                )}
              </div>
              <h4 id="selected-subject-heading" className="mt-4 max-w-xl font-serif text-[30px] font-semibold leading-[1.05] tracking-[-0.025em] text-[var(--ink-primary)] sm:text-[36px]">
                {displayedSubjectName || 'No subject selected'}
              </h4>
              <p className="mt-3 max-w-xl text-xs leading-5 text-[var(--ink-secondary)]">
                {verifiedSpecification?.title ?? 'We are checking the official specification for this examination cohort.'}
              </p>

              <div className="mt-5 flex flex-wrap items-center gap-x-5 gap-y-2 text-[11px] text-[var(--ink-secondary)]">
                {verifiedSpecification && (
                  <span><strong className="font-semibold text-[var(--ink-primary)]">{officialTopics.length}</strong> trackable syllabus areas</span>
                )}
                {verifiedSpecification?.recommendedClassHours && (
                  <span><strong className="font-semibold text-[var(--ink-primary)]">{verifiedSpecification.recommendedClassHours}</strong> class-contact hours</span>
                )}
                {primarySource && (
                  <a
                    href={primarySource.url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex min-h-8 items-center gap-1 font-semibold text-[var(--ink-primary)] underline decoration-[var(--outline-soft)] underline-offset-4 hover:decoration-[var(--ink-primary)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
                  >
                    Open official specification <ExternalLink size={11} aria-hidden="true" />
                  </a>
                )}
              </div>

              {verifiedSpecification?.selectionRules?.length ? (
                <p className="mt-5 border-t border-[var(--outline-soft)] pt-4 text-xs leading-5 text-[var(--ink-secondary)]">
                  <span className="font-semibold text-[var(--ink-primary)]">Choices that matter: </span>
                  {verifiedSpecification.selectionRules.map(rule => rule.description).join(' ')}
                </p>
              ) : null}
            </div>
          </EditorialCard>

          <EditorialCard className="flex min-h-[224px] flex-col justify-between">
            <div className="flex items-center gap-4">
              <CoverageRing stats={currentStats} subject={displayedSubjectName} />
              <div className="min-w-0 flex-1 space-y-2.5">
                {([
                  ['solid', currentStats.solid, 'Solid'],
                  ['shaky', currentStats.shaky, 'Shaky'],
                  ['not-started', currentStats.notStarted, 'Not started'],
                ] as const).map(([confidence, value, label]) => (
                  <div key={confidence} className="flex items-center gap-2 text-[11px] text-[var(--ink-secondary)]">
                    <ConfidenceDot confidence={confidence} size={8} />
                    <span>{label}</span>
                    <span className="ml-auto font-semibold tabular-nums text-[var(--ink-primary)]">{value}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="border-t border-[var(--outline-soft)] pt-3">
              <p className="text-[10px] leading-4 text-[var(--ink-muted)]">
                This is your self-reported confidence, not a predicted grade or a claim about topic importance.
              </p>
            </div>
          </EditorialCard>
        </section>
      )}

      {cohortNotice && (
        <section
          className="rounded-[14px] border p-4 sm:p-5"
          style={{
            borderColor: 'color-mix(in srgb, #B8843D 55%, var(--outline-soft))',
            background: 'color-mix(in srgb, #B8843D 8%, var(--surface-paper))',
          }}
          aria-labelledby="cohort-notice-heading"
        >
          <div className="flex items-start gap-3">
            <AlertTriangle size={17} className="mt-0.5 shrink-0" style={{ color: STATUS_SHAKY }} aria-hidden="true" />
            <div className="min-w-0">
              <h5 id="cohort-notice-heading" className="text-sm font-semibold text-[var(--ink-primary)]">{cohortNotice.title}</h5>
              <p className="mt-1 text-xs leading-5 text-[var(--ink-secondary)]">{cohortNotice.message}</p>
              <a
                href={cohortNotice.sourceUrl}
                target="_blank"
                rel="noreferrer"
                className="mt-2 inline-flex min-h-8 items-center gap-1 text-[11px] font-semibold text-[var(--ink-primary)] underline decoration-[var(--outline-soft)] underline-offset-4 hover:decoration-[var(--ink-primary)]"
              >
                Check the official transition <ExternalLink size={11} aria-hidden="true" />
              </a>
            </div>
          </div>
        </section>
      )}

      {verifiedSpecification?.assessmentComponents?.length ? (
        <section aria-labelledby="assessment-shape-heading">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Verified assessment structure</p>
              <h4 id="assessment-shape-heading" className="mt-1 font-serif text-xl font-semibold text-[var(--ink-primary)]">How the final result is built</h4>
            </div>
            <p className="max-w-md text-[11px] leading-4 text-[var(--ink-muted)]">Only official published weightings are shown. Annual briefs and prescribed material still need to be checked with the SEC.</p>
          </div>
          <div className="mt-4 overflow-hidden rounded-[12px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]">
            <div className="flex h-3 w-full" aria-hidden="true">
              {verifiedSpecification.assessmentComponents.map((component, index) => (
                <span
                  key={component.id}
                  style={{
                    width: `${component.weighting}%`,
                    background: index % 2 === 0 ? '#F26B1F' : 'color-mix(in srgb, #F26B1F 38%, var(--surface-soft))',
                  }}
                />
              ))}
            </div>
            <div className="grid divide-y divide-[var(--outline-soft)] sm:grid-cols-2 sm:divide-x sm:divide-y-0">
              {verifiedSpecification.assessmentComponents.map(component => (
                <div key={component.id} className="flex items-start justify-between gap-4 p-4">
                  <div>
                    <p className="text-xs font-semibold text-[var(--ink-primary)]">{component.title}</p>
                    <p className="mt-1 text-[10px] capitalize text-[var(--ink-muted)]">{component.kind.replaceAll('-', ' ')}</p>
                  </div>
                  <span className="font-serif text-2xl font-semibold tabular-nums text-[var(--ink-primary)]">{component.weighting}%</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      ) : null}

      <section aria-labelledby="topic-map-heading">
        <div className="flex flex-col gap-4 border-b border-[var(--outline-soft)] pb-5 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Your working map</p>
            <h4 id="topic-map-heading" className="mt-1 font-serif text-xl font-semibold text-[var(--ink-primary)]">Syllabus areas</h4>
          </div>
          <div className="flex w-full gap-2 md:max-w-sm">
            <input
              type="text"
              value={newTopicName}
              onChange={event => setNewTopicName(event.target.value)}
              onKeyDown={event => event.key === 'Enter' && addTopic()}
              placeholder="Add your own topic"
              aria-label="New topic name"
              maxLength={60}
              className={`${fieldClass} min-h-10 rounded-[8px] text-xs focus:outline focus:outline-2 focus:outline-offset-1 focus:outline-[var(--outline-strong)]`}
              style={{ ...fieldStyle, flex: 1, boxShadow: 'none' }}
            />
            <button
              type="button"
              onClick={addTopic}
              disabled={newTopicName.trim().length < 2 || existingNames.has(newTopicName.trim().toLowerCase())}
              aria-label="Add topic"
              className="flex min-h-10 min-w-10 items-center justify-center rounded-[8px] bg-[var(--ink-primary)] px-3 text-[var(--surface-paper)] transition-opacity disabled:cursor-not-allowed disabled:opacity-35 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--outline-strong)]"
            >
              <Plus size={15} aria-hidden="true" />
            </button>
          </div>
        </div>

        <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="coverage-scroll flex gap-1.5 overflow-x-auto pb-1" role="group" aria-label="Filter topics by confidence">
            {filters.map(option => {
              const active = filter === option.id;
              return (
                <button
                  key={option.id}
                  type="button"
                  onClick={() => setFilter(option.id)}
                  aria-pressed={active}
                  className={`shrink-0 rounded-full border px-3 py-1.5 text-[10px] font-semibold transition-colors ${
                    active
                      ? 'border-[var(--outline-strong)] bg-[var(--ink-primary)] text-[var(--surface-paper)]'
                      : 'border-[var(--outline-soft)] bg-[var(--surface-paper)] text-[var(--ink-secondary)] hover:border-[var(--outline-strong)]'
                  }`}
                >
                  {option.label} <span className="ml-1 tabular-nums opacity-70">{option.count}</span>
                </button>
              );
            })}
          </div>
          <label className="relative block w-full sm:w-56">
            <Search size={13} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[var(--ink-muted)]" aria-hidden="true" />
            <span className="sr-only">Search syllabus areas</span>
            <input
              type="search"
              value={query}
              onChange={event => setQuery(event.target.value)}
              placeholder="Find an area"
              className={`${fieldClass} min-h-10 rounded-[8px] pl-9 text-xs focus:outline focus:outline-2 focus:outline-offset-1 focus:outline-[var(--outline-strong)]`}
              style={{ ...fieldStyle, boxShadow: 'none' }}
            />
          </label>
        </div>

        {debriefTopics.length > 0 && (
          <section className="mt-5 rounded-[12px] border border-[var(--outline-soft)] bg-[var(--surface-soft)] p-4" aria-labelledby="debrief-suggestions-heading">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h5 id="debrief-suggestions-heading" className="text-xs font-semibold text-[var(--ink-primary)]">Gaps named in your debriefs</h5>
                <p className="mt-1 text-[10px] text-[var(--ink-muted)]">These are your words, so they stay separate from the official map.</p>
              </div>
              <button
                type="button"
                onClick={() => addDebriefTopics(debriefTopics)}
                className="min-h-8 text-[11px] font-semibold text-[var(--ink-secondary)] underline decoration-[var(--outline-soft)] underline-offset-4 hover:text-[var(--ink-primary)]"
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
                  className="inline-flex min-h-9 items-center gap-1.5 rounded-[7px] border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-2.5 py-1.5 text-[11px] font-medium text-[var(--ink-secondary)] hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)]"
                >
                  <AlertTriangle size={10} className="shrink-0" style={{ color: STATUS_SHAKY }} aria-hidden="true" />
                  {name}
                </button>
              ))}
            </div>
          </section>
        )}

        <div className="mt-6 space-y-7">
          {visibleGroups.map((group, groupIndex) => (
            <section key={group.id} aria-labelledby={`coverage-group-${group.id}`}>
              <div className="mb-3 flex items-center gap-3">
                <span className="font-mono text-[9px] font-semibold tabular-nums text-[var(--ink-muted)]">{String(groupIndex + 1).padStart(2, '0')}</span>
                <h5 id={`coverage-group-${group.id}`} className="text-xs font-semibold text-[var(--ink-primary)]">{group.title}</h5>
                {group.isCustom && (
                  <span className="rounded-full border border-[var(--outline-soft)] px-2 py-0.5 text-[8px] font-semibold uppercase tracking-[0.12em] text-[var(--ink-muted)]">Not official</span>
                )}
                <span className="h-px flex-1 bg-[var(--outline-soft)]" aria-hidden="true" />
              </div>
              <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
                {group.topics.map((topic, topicIndex) => {
                  const isNotStarted = topic.confidence === 'not-started';
                  return (
                    <div
                      key={topic.id}
                      className="coverage-topic-tile group relative overflow-hidden rounded-[11px] border bg-[var(--surface-paper)] transition-[border-color,transform,box-shadow] hover:-translate-y-px hover:border-[var(--outline-strong)] hover:shadow-[0_8px_20px_rgba(38,32,27,.05)]"
                      style={{ borderColor: 'var(--outline-soft)' }}
                    >
                      <span
                        className="absolute inset-y-0 left-0 w-1"
                        style={{
                          background: CONFIDENCE_HEX[topic.confidence].fill,
                          opacity: topic.confidence === 'not-started' ? 0.45 : 1,
                        }}
                        aria-hidden="true"
                      />
                      <button
                        type="button"
                        onClick={() => cycleConfidence(topic.name)}
                        aria-label={`${topic.name}: ${CONFIDENCE_LABELS[topic.confidence]}. Change confidence`}
                        className="coverage-topic-cycle min-h-[76px] w-full px-4 py-3.5 pr-11 text-left focus:outline-none"
                      >
                        <span className="flex items-start gap-3">
                          <span className="pt-0.5 font-mono text-[9px] tabular-nums text-[var(--ink-muted)]">{String(topicIndex + 1).padStart(2, '0')}</span>
                          <span className="min-w-0 flex-1">
                            <span className={`block break-words text-[13px] font-semibold leading-5 ${isNotStarted ? 'text-[var(--ink-secondary)]' : 'text-[var(--ink-primary)]'}`}>
                              {topic.name}
                            </span>
                            <span className="mt-1.5 inline-flex items-center gap-1.5 text-[9px] font-semibold uppercase tracking-[0.12em] text-[var(--ink-muted)]">
                              <ConfidenceDot confidence={topic.confidence} size={7} />
                              {CONFIDENCE_LABELS[topic.confidence]}
                            </span>
                          </span>
                        </span>
                      </button>
                      <button
                        type="button"
                        onClick={event => { event.stopPropagation(); resetTopic(topic.name); }}
                        className="coverage-topic-reset absolute right-2 top-2 flex h-8 w-8 items-center justify-center rounded-[7px] text-[var(--ink-muted)] opacity-0 transition-[opacity,background-color,color] hover:bg-[var(--surface-soft)] hover:text-[var(--ink-primary)] focus:opacity-100 focus:outline-none group-hover:opacity-100"
                        aria-label={`Reset ${topic.name} to not started`}
                      >
                        <X size={12} aria-hidden="true" />
                      </button>
                    </div>
                  );
                })}
              </div>
            </section>
          ))}

          {visibleGroups.length === 0 && (
            <div className="rounded-[12px] border border-dashed border-[var(--outline-soft)] bg-[var(--surface-soft)] px-5 py-8 text-center">
              <p className="text-sm font-semibold text-[var(--ink-primary)]">
                {allTopics.length ? 'No topics match this view' : 'No verified topic map for this cohort yet'}
              </p>
              <p className="mx-auto mt-1 max-w-lg text-xs leading-5 text-[var(--ink-secondary)]">
                {allTopics.length
                  ? 'Try a different confidence filter or clear the search.'
                  : 'The outgoing map is intentionally hidden rather than being shown to the wrong exam cohort. Use the official link above in the meantime.'}
              </p>
            </div>
          )}
        </div>
      </section>

      {allSubjectStats.some(subject => subject.total > 0) && (
        <section className="border-t border-[var(--outline-soft)] pt-7" aria-labelledby="all-subjects-heading">
          <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Across your subjects</p>
          <h4 id="all-subjects-heading" className="mt-1 font-serif text-xl font-semibold text-[var(--ink-primary)]">The whole syllabus at a glance</h4>
          <div className="mt-4 overflow-hidden rounded-[12px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]">
            {allSubjectStats.filter(subject => subject.total > 0).map((subject, subjectIndex) => {
              const profileIndex = subjects.findIndex(item => item.subjectName === subject.subjectName);
              const color = mutedSubjectHex(getDistinctSubjectHex(subject.subjectName, profileIndex >= 0 ? profileIndex : subjectIndex), 0.18);
              return (
                <div key={subject.subjectName} className="grid gap-3 border-b border-[var(--outline-soft)] px-4 py-3.5 last:border-b-0 sm:grid-cols-[180px_1fr_150px] sm:items-center">
                  <div className="flex min-w-0 items-center gap-2.5">
                    <span className="h-2.5 w-2.5 shrink-0 rounded-full border border-black/10" style={{ background: color }} aria-hidden="true" />
                    <span className="truncate text-xs font-semibold text-[var(--ink-primary)]">{subject.subjectName}</span>
                  </div>
                  <StatusRail stats={subject} height={7} />
                  <div className="flex items-center justify-between gap-3 text-[10px] tabular-nums text-[var(--ink-muted)] sm:justify-end">
                    <span>{subject.started}/{subject.total} started</span>
                    <span className="font-semibold text-[var(--ink-primary)]">{subject.solid} solid</span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      )}

      <p className="border-t border-[var(--outline-soft)] pt-4 text-[10px] leading-4 text-[var(--ink-muted)]">
        Curriculum notice: this is a planning and confidence tool, not an official publication. Topic maps and published assessment percentages come from the cohort-specific NCCA / Curriculum Online specification. Prescribed texts, annual briefs, project instructions and temporary SEC assessment arrangements can change; confirm those with your teacher and the SEC for your exam year.
      </p>
    </div>
  );
};

export default CoveragePanel;
