/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { ArrowRight, ChevronDown } from 'lucide-react';
import { MotionDiv } from '../Motion';
import {
  type Grade,
  type StudentSubjectProfile,
  getPointsForGrade,
} from '../subjectData';
import { getDistinctSubjectHex } from '../../studySessionData';
import { getSubjectGuidance } from '../subjectGuidance';
import {
  type MockResult,
  type TopicMap,
  mutedSubjectHex,
} from './warRoomShared';
import { type WarRoomStudyBlock } from '../WarRoom';

interface Recommendation {
  subject: string;
  priority: number;
  hasEvidence: boolean;
  reason: string;
  action: string;
  evidenceSummary: string;
  examinerCue?: string;
  latestGrade?: string;
  targetGrade?: string;
  sessionsPlanned: number;
  sessionsCompleted: number;
  sessionsRemaining: number;
  topicsTotal: number;
  notStarted: number;
  shaky: number;
  solid: number;
  coveragePct: number | null;
}

interface BriefingPanelProps {
  subjects: StudentSubjectProfile['subjects'];
  topicMap: TopicMap;
  mockResults: MockResult[];
  allocations: { subjectName: string; sessions: number }[];
  blockDuration: number;
  completedThisWeek: Record<string, number>;
  todayBlocks?: WarRoomStudyBlock[];
  onStudyNow?: (block: WarRoomStudyBlock) => void;
  onReviewSubjects?: () => void;
}

function sessionTypeLabel(sessionType: WarRoomStudyBlock['sessionType']): string {
  if (sessionType === 'new-learning') return 'New learning';
  if (sessionType === 'practice') return 'Practice';
  return 'Revision';
}

const BriefingPanel: React.FC<BriefingPanelProps> = ({
  subjects,
  topicMap,
  mockResults,
  allocations,
  blockDuration,
  completedThisWeek,
  todayBlocks = [],
  onStudyNow,
  onReviewSubjects,
}) => {
  const [showReasoning, setShowReasoning] = useState(false);
  const [showAllSubjects, setShowAllSubjects] = useState(false);

  const recommendations = useMemo((): Recommendation[] => {
    const rows = subjects.map((subject, subjectIndex) => {
      const topics = topicMap[subject.subjectName] ?? [];
      const notStartedTopics = topics.filter(topic => topic.confidence === 'not-started');
      const shakyTopics = topics.filter(topic => topic.confidence === 'shaky');
      const solidTopics = topics.filter(topic => topic.confidence === 'solid');
      const coveragePct = topics.length > 0
        ? Math.round(((solidTopics.length + shakyTopics.length * 0.5) / topics.length) * 100)
        : null;

      const results = mockResults
        .filter(result => result.subject === subject.subjectName && result.grade && result.date)
        .sort((a, b) => a.date.localeCompare(b.date));
      const latestResult = results.at(-1);
      const latestGrade = latestResult?.grade ?? subject.currentGrade;
      const isHigherMaths = subject.subjectName === 'Mathematics' && subject.level === 'higher';
      const latestPoints = getPointsForGrade(latestResult?.grade as Grade | undefined, isHigherMaths);
      const targetPoints = getPointsForGrade(subject.targetGrade, isHigherMaths);
      const gradeGap = latestResult ? Math.max(0, targetPoints - latestPoints) : 0;
      const allocation = allocations.find(item => item.subjectName === subject.subjectName);
      const sessionsPlanned = allocation?.sessions ?? 1;
      const sessionsCompleted = Math.min(
        sessionsPlanned,
        completedThisWeek[subject.subjectName] ?? 0,
      );
      const sessionsRemaining = Math.max(0, sessionsPlanned - sessionsCompleted);
      const hasEvidence = topics.length > 0 || results.length > 0;

      let priority = sessionsPlanned * 4;
      if (topics.length > 0) {
        priority += (notStartedTopics.length / topics.length) * 50;
        priority += (shakyTopics.length / topics.length) * 24;
      }
      if (latestResult && targetPoints > 0) {
        priority += Math.min(40, (gradeGap / targetPoints) * 60);
        if (results.length >= 2) {
          const previousPoints = getPointsForGrade(results.at(-2)?.grade as Grade | undefined, isHigherMaths);
          if (latestPoints < previousPoints) priority += 12;
        }
      }

      let action = `Complete one focused ${subject.subjectName} session.`;
      if (notStartedTopics[0]) {
        action = `Start ${notStartedTopics[0].name}.`;
      } else if (shakyTopics[0]) {
        action = `Strengthen ${shakyTopics[0].name} with retrieval practice.`;
      } else if (latestResult && gradeGap > 0) {
        action = 'Use one timed question to work on the gap to your target.';
      } else if (!hasEvidence) {
        action = 'Map your coverage, then complete one focused session.';
      }

      const signals: string[] = [];
      if (notStartedTopics.length > 0) {
        signals.push(`${notStartedTopics.length} topic${notStartedTopics.length === 1 ? '' : 's'} not started`);
      } else if (shakyTopics.length > 0) {
        signals.push(`${shakyTopics.length} topic${shakyTopics.length === 1 ? '' : 's'} still shaky`);
      }
      if (latestResult && gradeGap > 0 && subject.targetGrade) {
        signals.push(`${latestResult.grade} to ${subject.targetGrade} target`);
      }

      const reason = signals.length > 0
        ? `${signals.slice(0, 2).join(' · ')}.`
        : hasEvidence
          ? 'Your current evidence makes this the clearest place to use the next session.'
          : `${sessionsPlanned} session${sessionsPlanned === 1 ? '' : 's'} planned here this week.`;

      const evidenceSummary = coveragePct === null
        ? 'Coverage has not been mapped yet.'
        : `${coveragePct}% weighted coverage across ${topics.length} topic${topics.length === 1 ? '' : 's'}.`;
      const guidance = latestGrade ? getSubjectGuidance(subject.subjectName, latestGrade) : undefined;

      return {
        subject: subject.subjectName,
        subjectIndex,
        priority,
        hasEvidence,
        reason,
        action,
        evidenceSummary,
        examinerCue: guidance?.actions[0],
        latestGrade,
        targetGrade: subject.targetGrade,
        sessionsPlanned,
        sessionsCompleted,
        sessionsRemaining,
        topicsTotal: topics.length,
        notStarted: notStartedTopics.length,
        shaky: shakyTopics.length,
        solid: solidTopics.length,
        coveragePct,
      };
    });

    return rows.sort((a, b) => {
      if ((a.sessionsRemaining === 0) !== (b.sessionsRemaining === 0)) {
        return a.sessionsRemaining === 0 ? 1 : -1;
      }
      if (b.priority !== a.priority) return b.priority - a.priority;
      if (b.sessionsRemaining !== a.sessionsRemaining) return b.sessionsRemaining - a.sessionsRemaining;
      return a.subjectIndex - b.subjectIndex;
    });
  }, [allocations, completedThisWeek, mockResults, subjects, topicMap]);

  const scheduledSubjects = useMemo(
    () => new Set(todayBlocks.map(block => block.subject)),
    [todayBlocks],
  );
  const scheduledRecommendations = recommendations.filter(row => scheduledSubjects.has(row.subject));
  const focus = scheduledRecommendations[0] ?? recommendations[0];
  const focusBlock = focus
    ? todayBlocks.find(block => block.subject === focus.subject)
    : undefined;
  const queue = focus
    ? recommendations.filter(row => row.subject !== focus.subject)
    : recommendations;
  const visibleQueue = showAllSubjects ? queue : queue.slice(0, 3);
  const totalPlanned = recommendations.reduce((total, row) => total + row.sessionsPlanned, 0);
  const totalCompleted = recommendations.reduce((total, row) => total + row.sessionsCompleted, 0);
  const totalProgress = totalPlanned > 0 ? Math.min(100, (totalCompleted / totalPlanned) * 100) : 0;

  if (!focus) {
    return (
      <div className="mx-auto max-w-[880px]">
        <header>
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--ink-muted)]">Focus</p>
          <h2 className="mt-2 font-serif text-[30px] font-semibold leading-tight text-[var(--ink-primary)] sm:text-[36px]">
            What matters now
          </h2>
        </header>
        <div className="mt-7 border-y border-[var(--outline-soft)] py-8">
          <p className="text-sm text-[var(--ink-secondary)]">Add your subjects to build a clear weekly focus.</p>
          {onReviewSubjects && (
            <button
              type="button"
              onClick={onReviewSubjects}
              className="mt-5 inline-flex min-h-11 items-center gap-2 rounded-[9px] bg-[#F26B1F] px-5 text-sm font-bold text-[var(--ink-on-accent)] transition-transform hover:-translate-y-0.5"
            >
              Review subjects <ArrowRight size={15} aria-hidden="true" />
            </button>
          )}
        </div>
      </div>
    );
  }

  const focusIndex = subjects.findIndex(subject => subject.subjectName === focus.subject);
  const focusColor = mutedSubjectHex(
    getDistinctSubjectHex(focus.subject, Math.max(0, focusIndex)),
    0.12,
  );
  const focusAction = focusBlock && !focus.hasEvidence
    ? `Complete today’s ${sessionTypeLabel(focusBlock.sessionType).toLowerCase()} session.`
    : focus.action;
  const reasoningId = 'war-room-focus-reasoning';

  return (
    <div className="mx-auto max-w-[880px]">
      <header>
        <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--ink-muted)]">Focus</p>
        <h2 className="mt-2 font-serif text-[30px] font-semibold leading-tight text-[var(--ink-primary)] sm:text-[36px]">
          What matters now
        </h2>
        <p className="mt-2 hidden max-w-xl text-sm leading-relaxed text-[var(--ink-secondary)] sm:block">
          One useful next move. The detail can wait until you need it.
        </p>
      </header>

      <section
        className="mt-5 overflow-hidden rounded-[14px] border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] sm:mt-7"
        aria-labelledby="war-room-focus-subject"
      >
        <div className="p-5 sm:p-7 lg:p-8">
          <div className="flex flex-wrap items-center gap-2.5">
            <span
              className="h-2.5 w-2.5 shrink-0 rounded-full border border-black/10"
              style={{ background: focusColor }}
              aria-hidden="true"
            />
            <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">
              {focus.hasEvidence ? 'Highest impact' : 'Start here'}
            </span>
            {focusBlock && (
              <>
                <span className="text-[var(--outline-strong)]" aria-hidden="true">·</span>
                <span className="text-[10px] font-bold uppercase tracking-[0.15em] text-[var(--ink-muted)]">
                  Today’s {sessionTypeLabel(focusBlock.sessionType).toLowerCase()}
                </span>
              </>
            )}
          </div>

          <h3 id="war-room-focus-subject" className="mt-4 font-serif text-[32px] font-semibold leading-none text-[var(--ink-primary)] sm:text-[40px]">
            {focus.subject}
          </h3>
          <p className="mt-4 max-w-2xl text-[17px] font-semibold leading-snug text-[var(--ink-primary)] sm:text-[19px]">
            {focusAction}
          </p>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--ink-secondary)]">
            {focus.reason}
          </p>

          <div className="mt-7 max-w-xl">
            <div className="flex items-center justify-between gap-4 text-xs">
              <span className="font-medium text-[var(--ink-secondary)]">This week</span>
              <span className="font-mono text-[11px] font-semibold text-[var(--ink-muted)]">
                {focus.sessionsCompleted} of {focus.sessionsPlanned} complete
              </span>
            </div>
            <div
              className="mt-2 h-1.5 overflow-hidden rounded-full bg-[var(--outline-soft)]"
              role="progressbar"
              aria-label={`${focus.subject} weekly sessions`}
              aria-valuemin={0}
              aria-valuemax={focus.sessionsPlanned}
              aria-valuenow={focus.sessionsCompleted}
            >
              <div
                className="h-full rounded-full bg-[var(--ink-primary)] transition-[width] duration-500"
                style={{ width: `${focus.sessionsPlanned > 0 ? (focus.sessionsCompleted / focus.sessionsPlanned) * 100 : 0}%` }}
              />
            </div>
          </div>

          <div className="mt-7 flex flex-col items-start gap-3 sm:flex-row sm:items-center">
            {focusBlock && onStudyNow ? (
              <button
                type="button"
                onClick={() => onStudyNow(focusBlock)}
                className="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-[9px] bg-[#F26B1F] px-5 text-sm font-bold text-[var(--ink-on-accent)] shadow-[0_2px_0_rgba(26,26,26,.75)] transition-[transform,box-shadow] hover:-translate-y-0.5 hover:shadow-[0_3px_0_rgba(26,26,26,.75)] active:translate-y-0 active:shadow-none sm:w-auto"
              >
                Start a {focusBlock.durationMinutes}-minute session
                <ArrowRight size={15} aria-hidden="true" />
              </button>
            ) : onReviewSubjects ? (
              <button
                type="button"
                onClick={onReviewSubjects}
                className="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-[9px] bg-[#F26B1F] px-5 text-sm font-bold text-[var(--ink-on-accent)] shadow-[0_2px_0_rgba(26,26,26,.75)] transition-[transform,box-shadow] hover:-translate-y-0.5 hover:shadow-[0_3px_0_rgba(26,26,26,.75)] active:translate-y-0 active:shadow-none sm:w-auto"
              >
                Review subject coverage
                <ArrowRight size={15} aria-hidden="true" />
              </button>
            ) : null}

            {focusBlock && onReviewSubjects && (
              <button
                type="button"
                onClick={onReviewSubjects}
                className="min-h-10 px-1 text-xs font-semibold text-[var(--ink-secondary)] underline decoration-[var(--outline-soft)] underline-offset-4 transition-colors hover:text-[var(--ink-primary)]"
              >
                Review subject coverage
              </button>
            )}
          </div>
        </div>

        <div className="border-t border-[var(--outline-soft)] px-5 py-1 sm:px-7 lg:px-8">
          <button
            type="button"
            aria-expanded={showReasoning}
            aria-controls={reasoningId}
            onClick={() => setShowReasoning(value => !value)}
            className="flex min-h-12 w-full items-center justify-between gap-4 text-left text-xs font-semibold text-[var(--ink-secondary)] transition-colors hover:text-[var(--ink-primary)]"
          >
            Why this subject?
            <ChevronDown
              size={15}
              aria-hidden="true"
              className={`shrink-0 transition-transform duration-200 ${showReasoning ? 'rotate-180' : ''}`}
            />
          </button>
          <AnimatePresence initial={false}>
            {showReasoning && (
              <MotionDiv
                id={reasoningId}
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
                className="overflow-hidden"
              >
                <div className="grid gap-4 border-t border-[var(--outline-soft)] py-5 text-xs sm:grid-cols-2">
                  <div>
                    <p className="font-semibold text-[var(--ink-primary)]">Evidence</p>
                    <p className="mt-1.5 leading-relaxed text-[var(--ink-secondary)]">{focus.evidenceSummary}</p>
                    {focus.latestGrade && focus.targetGrade && (
                      <p className="mt-1.5 text-[var(--ink-secondary)]">
                        Grade path: <span className="font-mono font-semibold text-[var(--ink-primary)]">{focus.latestGrade} → {focus.targetGrade}</span>
                      </p>
                    )}
                  </div>
                  <div>
                    <p className="font-semibold text-[var(--ink-primary)]">Plan</p>
                    <p className="mt-1.5 leading-relaxed text-[var(--ink-secondary)]">
                      {focus.sessionsPlanned} × {blockDuration} minutes this week. {focus.sessionsRemaining} remaining.
                    </p>
                    {focus.examinerCue && (
                      <p className="mt-1.5 line-clamp-3 leading-relaxed text-[var(--ink-secondary)]">
                        Suggested approach: {focus.examinerCue}
                      </p>
                    )}
                  </div>
                </div>
              </MotionDiv>
            )}
          </AnimatePresence>
        </div>
      </section>

      <section className="mt-10" aria-labelledby="war-room-week-title">
        <div className="flex items-end justify-between gap-5 border-b border-[var(--outline-strong)] pb-3">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--ink-muted)]">This week</p>
            <h3 id="war-room-week-title" className="mt-1.5 font-serif text-[24px] font-semibold text-[var(--ink-primary)]">
              Your queue
            </h3>
          </div>
          <p className="shrink-0 font-mono text-[11px] font-semibold text-[var(--ink-muted)]">
            {totalCompleted}/{totalPlanned}
          </p>
        </div>

        <div
          className="h-1 bg-[var(--outline-soft)]"
          role="progressbar"
          aria-label="Weekly queue progress"
          aria-valuemin={0}
          aria-valuemax={totalPlanned}
          aria-valuenow={totalCompleted}
        >
          <div className="h-full bg-[#F26B1F] transition-[width] duration-500" style={{ width: `${totalProgress}%` }} />
        </div>

        <ol className="divide-y divide-[var(--outline-soft)]" aria-label="Weekly subject queue">
          {visibleQueue.map((row, index) => {
            const subjectIndex = subjects.findIndex(subject => subject.subjectName === row.subject);
            const color = mutedSubjectHex(getDistinctSubjectHex(row.subject, Math.max(0, subjectIndex)), 0.12);
            return (
              <li key={row.subject} className="grid grid-cols-[auto_1fr_auto] items-center gap-3 py-4 sm:gap-4">
                <span className="w-5 font-mono text-[10px] text-[var(--ink-muted)]">{String(index + 1).padStart(2, '0')}</span>
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="h-2 w-2 shrink-0 rounded-full border border-black/10" style={{ background: color }} aria-hidden="true" />
                    <p className="truncate text-sm font-semibold text-[var(--ink-primary)]">{row.subject}</p>
                  </div>
                  <p className="mt-1 line-clamp-1 text-xs text-[var(--ink-muted)]">{row.action}</p>
                </div>
                <p className={`shrink-0 text-right text-[11px] font-semibold ${
                  row.sessionsRemaining === 0 ? 'text-[var(--success-hex)]' : 'text-[var(--ink-secondary)]'
                }`}>
                  {row.sessionsRemaining === 0
                    ? 'Complete'
                    : `${row.sessionsRemaining} left`}
                </p>
              </li>
            );
          })}
        </ol>

        {queue.length === 0 && (
          <p className="border-b border-[var(--outline-soft)] py-5 text-sm text-[var(--ink-secondary)]">
            Nothing else is competing for attention this week.
          </p>
        )}

        {queue.length > 3 && (
          <button
            type="button"
            onClick={() => setShowAllSubjects(value => !value)}
            aria-expanded={showAllSubjects}
            className="mt-4 min-h-10 text-xs font-semibold text-[var(--ink-secondary)] underline decoration-[var(--outline-soft)] underline-offset-4 transition-colors hover:text-[var(--ink-primary)]"
          >
            {showAllSubjects ? 'Show less' : `Show all ${queue.length} subjects`}
          </button>
        )}
      </section>
    </div>
  );
};

export default BriefingPanel;
