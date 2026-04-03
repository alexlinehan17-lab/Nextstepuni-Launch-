/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo } from 'react';
import { useToast } from './Toast';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Clock, Map, TrendingUp, Target } from 'lucide-react';
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
import { type TopicEntry, type TopicMap, type MockResult, computeCurrentTotal } from './war-room/warRoomShared';
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

const PANEL_TABS = [
  { id: 0, label: 'Countdown', icon: Clock },
  { id: 1, label: 'Coverage', icon: Map },
  { id: 2, label: 'Trajectory', icon: TrendingUp },
  { id: 3, label: 'Briefing', icon: Target },
] as const;

// ── Main Component ─────────────────────────────────────────

const WarRoom: React.FC<WarRoomProps> = ({ uid, profile, timetableCompletions }) => {
  const { showToast } = useToast();
  const [activePanel, setActivePanel] = useState(0);
  const [studySessions, setStudySessions] = useState<StudySessionRecord[]>([]);
  const [debriefs, setDebriefs] = useState<DebriefEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Shared data from InnovationDataContext
  const { topicMastery, mockResults: mockResultsHook, futureFinderPicks } = useInnovationData();
  const targetCourse = futureFinderPicks.length > 0 ? futureFinderPicks[0] : null;

  // Derive a TopicMap from unified mastery for legacy sub-components that still expect TopicMap
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

  // Derive legacy MockResult[] from unified mock results for sub-components
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

  // Load remaining data from Firestore (study sessions, debriefs)
  useEffect(() => {
    if (!uid) return;
    let cancelled = false;
    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        if (cancelled) return;
        const data = snap.data() || {};
        if (data.studySessions) {
          setStudySessions(data.studySessions as StudySessionRecord[]);
        }
        if (data.studyDebriefs) {
          setDebriefs(data.studyDebriefs as DebriefEntry[]);
        }
      } catch (e) {
        console.error('Failed to load War Room data:', e);
      }
      if (!cancelled) setIsLoading(false);
    };
    load();
    return () => { cancelled = true; };
  }, [uid]);

  // Shared computations
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

  // Hours studied per subject from study sessions
  const hoursStudiedMap = useMemo(() => {
    const map: Record<string, number> = {};
    for (const s of studySessions) {
      map[s.subject] = (map[s.subject] || 0) + s.actualSeconds / 3600;
    }
    // Also count timetable completions as approximate study time
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
        <div className="w-6 h-6 border-2 border-zinc-300 dark:border-zinc-600 border-t-[var(--accent-hex)] rounded-full animate-spin" />
      </div>
    );
  }

  const phaseColorMain = daysUntilExam > 180 ? '#2A7D6F' : daysUntilExam > 90 ? '#D4891C' : daysUntilExam > 30 ? '#D4564E' : '#C5981A';

  // Shared tab row component (rendered inside colour or on cream)
  const tabRow = (onColor: boolean) => (
    <div className="flex justify-center gap-1 px-4">
      {PANEL_TABS.map(tab => {
        const Icon = tab.icon;
        const isActive = activePanel === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => setActivePanel(tab.id)}
            className={`flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg text-[13px] transition-all ${
              !onColor
                ? isActive
                  ? 'bg-[#FEFDFB] dark:bg-zinc-900 text-[#1C1917] dark:text-white border border-[#EDEBE8] dark:border-zinc-800'
                  : 'text-[#A8A29E] dark:text-zinc-500 border border-transparent'
                : ''
            }`}
            style={onColor ? {
              backgroundColor: isActive ? 'rgba(255,255,255,0.18)' : 'transparent',
              color: isActive ? '#fff' : 'rgba(255,255,255,0.55)',
              fontWeight: isActive ? 700 : 500,
            } : {
              fontWeight: isActive ? 700 : 500,
              boxShadow: isActive ? '0 1px 3px rgba(28,25,23,0.04)' : 'none',
            }}
          >
            <Icon size={13} />
            <span className="hidden sm:inline">{tab.label}</span>
          </button>
        );
      })}
    </div>
  );

  return (
    <div>
      {/* ── Colour header with integrated tabs ── */}
      {activePanel === 0 ? (
        /* Countdown: full hero with tabs inside */
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
          tabRow={tabRow(true)}
          phaseColor={phaseColorMain}
        />
      ) : (
        /* Other tabs: short colour strip with tabs, then cream content */
        <>
          <div
            className="relative overflow-hidden"
            style={{
              backgroundColor: phaseColorMain,
              position: 'relative',
              left: '50%',
              right: '50%',
              marginLeft: '-50vw',
              marginRight: '-50vw',
              width: '100vw',
            }}
          >
            <div className="relative z-10 pt-16 md:pt-20 pb-5 max-w-4xl mx-auto">
              {tabRow(true)}
            </div>
            {/* Wavy edge */}
            <div className="absolute bottom-0 left-0 right-0" style={{ transform: 'translateY(1px)' }}>
              <svg viewBox="0 0 1440 24" preserveAspectRatio="none" className="block w-full" style={{ height: 20 }}>
                <path d="M0,12 C360,24 720,4 1080,16 C1260,22 1360,10 1440,14 L1440,24 L0,24 Z" className="fill-[#FDF8F0] dark:fill-zinc-950" />
              </svg>
            </div>
          </div>

          <div className="pt-5">
            <AnimatePresence mode="wait">
              <MotionDiv
                key={activePanel}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.2 }}
              >
                {activePanel === 1 && (
                  <CoveragePanel subjects={subjects} topicMastery={topicMastery} debriefs={debriefs} />
                )}
                {activePanel === 2 && (
                  <TrajectoryPanel subjects={subjects} mockResults={derivedMockResults} mockResultsHook={mockResultsHook} daysUntilExam={daysUntilExam} />
                )}
                {activePanel === 3 && (
                  <BriefingPanel subjects={subjects} topicMap={derivedTopicMap} mockResults={derivedMockResults} allocations={allocations} hoursStudiedMap={hoursStudiedMap} weeksUntilExam={weeksUntilExam} blockDuration={blockDuration} daysUntilExam={daysUntilExam} timetableCompletions={timetableCompletions} />
                )}
              </MotionDiv>
            </AnimatePresence>
          </div>
        </>
      )}
    </div>
  );
};

export default WarRoom;
