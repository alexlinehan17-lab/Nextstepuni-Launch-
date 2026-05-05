/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo } from 'react';
import { useToast } from './Toast';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { db } from '../firebase';
import { doc, getDoc } from 'firebase/firestore';
import {
  type StudentSubjectProfile, type TimetableCompletions,
} from './subjectData';
import {
  computeSubjectPriorities, allocateSessions, computeWeeksUntilExam,
} from './timetableAlgorithm';
import { type DebriefEntry } from './StudyDebrief';
import { type StudySessionRecord } from '../utils/strategyRegistry';
import { useInnovationData } from '../contexts/InnovationDataContext';
import {
  type TopicEntry, type TopicMap, type MockResult, computeCurrentTotal,
  INK, INK_MUTE, ACCENT,
} from './war-room/warRoomShared';
import {
  Overline,
} from './war-room/warRoomPrimitives';
import CountdownPanel from './war-room/CountdownPanel';
import CoveragePanel from './war-room/CoveragePanel';
import TrajectoryPanel from './war-room/TrajectoryPanel';
import BriefingPanel from './war-room/BriefingPanel';

// ── Types ──────────────────────────────────────────────────

interface WarRoomProps {
  uid: string;
  profile: StudentSubjectProfile;
  timetableCompletions: TimetableCompletions;
}

// Hand-drawn tab icons supplied as transparent PNGs.
const PANEL_TABS = [
  { id: 0, label: 'Countdown',  iconSrc: '/assets/war-room-icons/countdown.png' },
  { id: 1, label: 'Coverage',   iconSrc: '/assets/war-room-icons/coverage.png' },
  { id: 2, label: 'Trajectory', iconSrc: '/assets/war-room-icons/trajectory.png' },
  { id: 3, label: 'Briefing',   iconSrc: '/assets/war-room-icons/briefing.png' },
] as const;

// ── Hand-drawn sketch tab ──────────────────────────────────
// Inactive: single thin charcoal border. Active: double-stroke outline + 3 small orange spark lines at top-left.

const SketchTab: React.FC<{
  label: string;
  iconSrc: string;
  isActive: boolean;
  onClick: () => void;
}> = ({ label, iconSrc, isActive, onClick }) => (
  <button
    type="button"
    role="tab"
    aria-selected={isActive}
    onClick={onClick}
    className="relative inline-flex items-center gap-2.5 px-5 sm:px-6 py-2.5 transition-all"
    style={{
      background: '#FFFFFF',
      borderRadius: 14,
      border: `1.5px solid ${INK}`,
      boxShadow: isActive
        ? `0 0 0 3px #FFFFFF, 0 0 0 4.5px ${INK}, 0 6px 16px rgba(31,27,23,0.06)`
        : '0 1px 0 rgba(31,27,23,0.04), 0 4px 12px rgba(31,27,23,0.04)',
      color: INK,
      transform: isActive ? 'rotate(-0.4deg)' : 'rotate(0deg)',
    }}
  >
    {/* Active spark marks — three orange dashes radiating up-and-left from the top-left corner */}
    {isActive && (
      <span
        className="absolute pointer-events-none"
        style={{ top: -16, left: -4 }}
        aria-hidden
      >
        <svg width="26" height="22" viewBox="0 0 26 22" fill="none">
          <path d="M14 2 L 11 9" stroke={ACCENT} strokeWidth={1.8} strokeLinecap="round" />
          <path d="M8 1 L 7 9" stroke={ACCENT} strokeWidth={1.8} strokeLinecap="round" />
          <path d="M2 4 L 4 10" stroke={ACCENT} strokeWidth={1.8} strokeLinecap="round" />
        </svg>
      </span>
    )}
    <img src={iconSrc} alt="" aria-hidden style={{ width: 34, height: 34, objectFit: 'contain' }} />
    <span
      className="font-serif"
      style={{
        fontSize: 17,
        fontWeight: isActive ? 700 : 500,
        color: INK,
        letterSpacing: '-0.005em',
      }}
    >
      {label}
    </span>
  </button>
);

// ── Main Component ─────────────────────────────────────────

const WarRoom: React.FC<WarRoomProps> = ({ uid, profile, timetableCompletions }) => {
  const { showToast: _showToast } = useToast();
  const [activePanel, setActivePanel] = useState(0);
  const [studySessions, setStudySessions] = useState<StudySessionRecord[]>([]);
  const [debriefs, setDebriefs] = useState<DebriefEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const { topicMastery, mockResults: mockResultsHook, futureFinderPicks } = useInnovationData();
  const targetCourse = futureFinderPicks.length > 0 ? futureFinderPicks[0] : null;

  const derivedTopicMap: TopicMap = useMemo(() => {
    const map: TopicMap = {};
    for (const [subject, topics] of Object.entries(topicMastery.mastery)) {
      map[subject] = Object.entries(topics).map(([name, entry]) => ({
        id: `${subject}-${name}`,
        name,
        confidence: entry.confidence as TopicEntry['confidence'],
        updatedAt: entry.updatedAt,
      }));
    }
    return map;
  }, [topicMastery.mastery]);

  const derivedMockResults: MockResult[] = useMemo(() => {
    const results: MockResult[] = [];
    for (const mock of mockResultsHook.mocks) {
      for (const entry of mock.entries) {
        results.push({
          id: `${mock.id}-${entry.subjectName}`,
          subject: entry.subjectName,
          grade: entry.grade,
          date: mock.date,
          label: mock.label,
          timestamp: mock.timestamp,
        });
      }
    }
    return results;
  }, [mockResultsHook.mocks]);

  useEffect(() => {
    if (!uid) return;
    let cancelled = false;
    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        if (cancelled) return;
        const data = snap.data() || {};
        if (data.studySessions) setStudySessions(data.studySessions as StudySessionRecord[]);
        if (data.studyDebriefs) setDebriefs(data.studyDebriefs as DebriefEntry[]);
      } catch (err) {
        console.error('Failed to load War Room data:', err);
      }
      if (!cancelled) setIsLoading(false);
    };
    load();
    return () => { cancelled = true; };
  }, [uid]);

  const subjects = profile.subjects;
  const daysUntilExam = useMemo(() => {
    const examDate = new Date(profile.examStartDate);
    return Math.max(0, Math.ceil((examDate.getTime() - Date.now()) / 86400000));
  }, [profile.examStartDate]);

  const weeksUntilExam = useMemo(() => computeWeeksUntilExam(profile.examStartDate), [profile.examStartDate]);
  const blockDuration = profile.defaultBlockDuration ?? 45;

  const allocations = useMemo(() => {
    const priorities = computeSubjectPriorities(subjects);
    return allocateSessions(priorities, weeksUntilExam);
  }, [subjects, weeksUntilExam]);

  const hoursStudiedMap = useMemo(() => {
    const map: Record<string, number> = {};
    for (const s of studySessions) {
      map[s.subject] = (map[s.subject] || 0) + s.actualSeconds / 3600;
    }
    for (const [, blockIds] of Object.entries(timetableCompletions)) {
      for (const blockId of blockIds) {
        const parts = blockId.split('|');
        const subjectName = parts[0];
        if (subjectName) {
          map[subjectName] = (map[subjectName] || 0) + blockDuration / 60;
        }
      }
    }
    return map;
  }, [studySessions, timetableCompletions, blockDuration]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-6 h-6 border-2 rounded-full animate-spin"
             style={{ borderColor: `${INK}22`, borderTopColor: ACCENT }} />
      </div>
    );
  }

  // ── Editorial header ─────────────────────────────────────
  // Cream paper banner — small overline, serif title, hand-drawn horizon, days badge.
  // Replaces the previous heavy coloured banner.

  return (
    <div
      className="relative"
      style={{
        // Break out to viewport width so the cream surface reaches the page edges.
        position: 'relative',
        left: '50%',
        right: '50%',
        marginLeft: '-50vw',
        marginRight: '-50vw',
        width: '100vw',
        background: '#FAFBF6',
        minHeight: '100vh',
      }}
    >
      {/* War Room target crest — anchored top-right of the page */}
      <img
        src="/assets/war-room-crest.png"
        alt=""
        aria-hidden
        className="absolute z-10"
        style={{
          top: 'clamp(16px, 2.5vw, 32px)',
          right: 'clamp(16px, 3vw, 40px)',
          width: 'clamp(75px, 8.6vw, 112px)',
          height: 'clamp(75px, 8.6vw, 112px)',
          objectFit: 'contain',
        }}
      />

      <div className="max-w-5xl mx-auto px-4 sm:px-8 pt-10 sm:pt-14 pb-16">
        {/* ── Centered editorial hero ── */}
        <header className="relative mb-2 text-center">
          {/* Title — large, centred serif */}
          <h1
            className="font-serif font-bold leading-[1.0]"
            style={{
              color: INK,
              fontSize: 'clamp(48px, 9vw, 96px)',
              letterSpacing: '-0.022em',
            }}
          >
            Strategy Briefing
          </h1>

          {/* Subtitle */}
          <p
            className="font-sans mt-5 mx-auto leading-relaxed"
            style={{
              color: INK_MUTE,
              fontSize: 'clamp(15px, 1.5vw, 18px)',
              maxWidth: 560,
            }}
          >
            An editorial overview of the road to your Leaving Cert.
          </p>
        </header>

        {/* Hand-drawn path illustration spanning the hero */}
        <div className="relative -mx-4 sm:-mx-8 mt-2 mb-6 select-none pointer-events-none">
          <img
            src="/assets/war-room-path.png"
            alt=""
            aria-hidden
            className="w-full block"
            style={{ maxHeight: 220, objectFit: 'contain', objectPosition: 'center' }}
          />
        </div>

        {/* ── Tab navigation ── */}
        {/* Hand-drawn rounded-rectangle buttons; active state adds a sketchy double border + orange spark marks. */}
        <nav role="tablist" className="relative mb-8 flex items-center justify-center" aria-label="War Room tabs">
          <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-4">
            {PANEL_TABS.map(tab => {
              const isActive = activePanel === tab.id;
              return (
                <SketchTab
                  key={tab.id}
                  label={tab.label}
                  iconSrc={tab.iconSrc}
                  isActive={isActive}
                  onClick={() => setActivePanel(tab.id)}
                />
              );
            })}
          </div>
        </nav>

        {/* ── Active panel ── */}
        <AnimatePresence mode="wait">
          <MotionDiv
            key={activePanel}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.22 }}
          >
            {activePanel === 0 && (
              <CountdownPanel
                daysUntilExam={daysUntilExam}
                subjects={subjects}
                allocations={allocations}
                weeksUntilExam={weeksUntilExam}
                hoursStudiedMap={hoursStudiedMap}
                blockDuration={blockDuration}
                mockResults={derivedMockResults}
                targetCourse={targetCourse}
                currentPoints={computeCurrentTotal(subjects)}
              />
            )}
            {activePanel === 1 && (
              <CoveragePanel subjects={subjects} topicMastery={topicMastery} debriefs={debriefs} />
            )}
            {activePanel === 2 && (
              <TrajectoryPanel subjects={subjects} mockResults={derivedMockResults} mockResultsHook={mockResultsHook} daysUntilExam={daysUntilExam} />
            )}
            {activePanel === 3 && (
              <BriefingPanel
                subjects={subjects} topicMap={derivedTopicMap} mockResults={derivedMockResults}
                allocations={allocations} hoursStudiedMap={hoursStudiedMap}
                weeksUntilExam={weeksUntilExam} blockDuration={blockDuration}
                daysUntilExam={daysUntilExam} timetableCompletions={timetableCompletions}
              />
            )}
          </MotionDiv>
        </AnimatePresence>
      </div>
    </div>
  );
};

export default WarRoom;
