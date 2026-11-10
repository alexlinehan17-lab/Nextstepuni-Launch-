/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import { ArrowRight, ArrowUpRight, Clock3 } from 'lucide-react';
import { Button, PlanCard } from '../approved-ui-runtime';
import CrewIllustration from '../CrewIllustration';
import { formatStudyTime } from '../../utils/studyTime';
import { recordedSubjectActivity } from '../../services/studyTopicHistory';
import type { StudySessionRecord } from '../../utils/strategyRegistry';
import { compactStudyTime } from './learningRecordModel';
import {
  type Grade,
  type StudentSubjectProfile,
  getPointsForGrade,
} from '../subjectData';
import { getSubjectGuidance } from '../subjectGuidance';
import {
  type MockResult,
  type TopicMap,
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
  onOpenRecord: (subject: string) => void;
  studySessions: StudySessionRecord[];
  daysUntilExam: number | null;
  examDate: Date | null;
  currentDate: Date;
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
  onOpenRecord, studySessions, daysUntilExam, examDate, currentDate,
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

  if (!focus) return <div className="wr-empty"><p className="wr-eyebrow">Your daily brief</p><h2>Make room for your next step.</h2><p>Add your subjects in Settings to build your study plan.</p></div>;
  const duration = focusBlock?.durationMinutes ?? blockDuration;
  const recorded = recordedSubjectActivity(studySessions, focus.subject);

  return <>
    <section className="wr-opening">
      <div><p className="wr-eyebrow">{currentDate.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' })} / Your daily brief</p>
        <h2>Make room for<br /><em>your next step.</em></h2><p>You don’t need to do everything today.<br />Start with one good session.</p></div>
      {daysUntilExam !== null && <div className="wr-countdown" role="group" aria-label="Exam countdown"><span>{daysUntilExam}</span><p>{daysUntilExam === 1 ? 'day' : 'days'} to your exams</p><small>{examDate?.toLocaleDateString('en-IE', { day: 'numeric', month: 'long', year: 'numeric' })}</small></div>}
    </section>
    <section className="wr-next-session" aria-labelledby="wr-next-subject">
      <div className="wr-session-copy"><p className="wr-eyebrow">{focusBlock ? 'Next on your plan / 01' : 'A little room to reset / 01'}</p><h3 id="wr-next-subject">{focus.subject}</h3>
        <p className="wr-topic-name">{focus.action}</p>
        <div className="wr-session-meta">{focusBlock ? <><span><Clock3 size={15} />{duration} minutes</span><span>{sessionTypeLabel(focusBlock.sessionType)}</span></> : <span>No sessions left in today’s plan.</span>}</div>
        <div className="wr-session-actions">
          {focusBlock && onStudyNow ? <Button className="wr-orange" size="lg" aria-label={`Start a ${duration}-minute session`} onClick={() => onStudyNow(focusBlock)}>Start studying <ArrowUpRight size={19} /></Button> : <Button variant="outline" className="nsu-ink-outline" onClick={onReviewSubjects}>Choose a subject <ArrowRight size={17} /></Button>}
          <Button variant="link" className="wr-reason-toggle" aria-expanded={showReasoning} aria-controls="wr-session-reason" onClick={() => setShowReasoning(value => !value)}>Why this subject?</Button>
        </div>
        {showReasoning && <div id="wr-session-reason" className="wr-session-reason"><p>{focus.reason}</p><p>{focus.evidenceSummary}</p>{focus.latestGrade && focus.targetGrade && <p>{focus.latestGrade} → {focus.targetGrade}</p>}</div>}
      </div><CrewIllustration subject={focus.subject} className="wr-session-art" />
    </section>
    <div className="wr-brief-bottom">
      <section><header className="wr-section-heading"><span>02</span><h3>A plan you can follow.</h3></header>
        <PlanCard className="nsu-plan-card wr-plan-card" title="Small session. Clear purpose." description={focus.action}
          steps={[{ label: 'Recall what you know before opening your notes.' }, { label: 'Check the gaps and work through one example.' }, { label: 'Finish with your usual session reflection.' }]}
          visibleSteps={3} approveLabel="Prepare session" approveDisabled={!focusBlock || !onStudyNow} onApprove={() => { if (focusBlock) onStudyNow?.(focusBlock); }}
          viewLabel="Learning record" onView={() => onOpenRecord(focus.subject)} />
        <div className="wr-week-queue"><div className="wr-queue-heading"><h4>Your weekly queue</h4><span>{totalCompleted}/{totalPlanned}</span></div>
          <div className="wr-progress" role="progressbar" aria-label="Weekly queue progress" aria-valuemin={0} aria-valuemax={totalPlanned} aria-valuenow={totalCompleted}><span style={{ width: `${totalProgress}%` }} /></div>
          <ol aria-label="Weekly subject queue">{visibleQueue.map((row, index) => <li key={row.subject}><span className="wr-row-number">{String(index + 1).padStart(2, '0')}</span><div><strong>{row.subject}</strong><p>{row.action}</p></div><span>{row.sessionsRemaining === 0 ? 'Complete' : `${row.sessionsRemaining} left`}</span></li>)}</ol>
          {queue.length > 3 && <Button variant="link" onClick={() => setShowAllSubjects(value => !value)} aria-expanded={showAllSubjects}>{showAllSubjects ? 'Show less' : `Show all ${queue.length} subjects`}</Button>}
        </div>
      </section>
      <section className="wr-week-quiet"><header className="wr-section-heading"><span>03</span><h3>The work is adding up.</h3></header><strong aria-label={formatStudyTime(recorded.seconds)}>{compactStudyTime(recorded.seconds)}</strong><p>recorded for {focus.subject} / {recorded.count} saved {recorded.count === 1 ? 'session' : 'sessions'}</p>
        <div className="wr-rule" />
        {focus.latestGrade && focus.targetGrade && <><p>{mockResults.some(result => result.subject === focus.subject) ? 'Latest recorded grade' : 'Your current grade'}</p><div className="wr-grade-path"><span>{focus.latestGrade}</span><ArrowRight size={19} /><span>{focus.targetGrade}</span></div><small>Your target</small></>}
        <p className="wr-week-summary">{focus.sessionsCompleted} of {focus.sessionsPlanned} planned sessions completed this week.</p>
        <div className="wr-progress" role="progressbar" aria-label={`${focus.subject} weekly sessions`} aria-valuemin={0} aria-valuemax={focus.sessionsPlanned} aria-valuenow={focus.sessionsCompleted}><span style={{ width: `${focus.sessionsPlanned ? focus.sessionsCompleted / focus.sessionsPlanned * 100 : 0}%` }} /></div>
        <Button variant="link" onClick={() => onOpenRecord(focus.subject)}>Open your learning record <ArrowRight size={16} /></Button>
      </section>
    </div>
  </>;
};

export default BriefingPanel;
