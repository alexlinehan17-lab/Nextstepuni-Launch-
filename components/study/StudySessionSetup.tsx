import React, { useId } from 'react';
import { ArrowLeft, ArrowRight, BookOpen, ChevronDown, Play } from 'lucide-react';
import type { StudentSubjectProfile } from '../subjectData';
import type { StrategyMasteryMap } from '../../types';
import type { TimetableBlockContext } from './StudySessionView';
import { DURATION_PRESETS, STRATEGY_REGISTRY } from '../../studySessionData';
import { MIN_STUDY_SESSION_MINUTES } from '../../hooks/useStudySession';
import { getSubjectFill } from '../../utils/subjectColors';
import '../launchpad/launchpad.css';
import './study-session.css';

type SessionType = 'new-learning' | 'practice' | 'revision';
export const STUDY_TYPES: { id: SessionType; label: string; detail: string }[] = [
  { id: 'new-learning', label: 'New Learning', detail: 'Meet it for the first time' },
  { id: 'practice', label: 'Practice', detail: 'Work through questions' },
  { id: 'revision', label: 'Revision', detail: 'Recall what you know' },
];

interface StudySessionSetupProps {
  subjects: StudentSubjectProfile['subjects'];
  selectedSubject: string;
  selectedType: SessionType | '';
  selectedMinutes: number;
  onSubject: (subject: string) => void;
  onType: (type: SessionType) => void;
  onMinutes: (minutes: number) => void;
  todayBlocks: TimetableBlockContext[];
  onBlock: (block: TimetableBlockContext) => void;
  sessionCount: number;
  todayMinutes: number;
  reflectionCount: number;
  lastNote?: string;
  strategyMastery?: StrategyMasteryMap;
  onProgress?: () => void;
  onReflections: () => void;
  onBack: () => void;
  onSetUpProfile?: () => void;
  onStart: () => void;
  canStart: boolean;
  startHint: string | null;
}

const StudySessionSetup: React.FC<StudySessionSetupProps> = (props) => {
  const { subjects, selectedSubject, selectedType, selectedMinutes, onSubject, onType, onMinutes, todayBlocks, onBlock, sessionCount, todayMinutes, reflectionCount, lastNote, strategyMastery, onProgress, onReflections, onBack, onSetUpProfile, onStart, canStart, startHint } = props;
  const id = useId();
  const custom = !DURATION_PRESETS.some(preset => preset.minutes === selectedMinutes) && selectedMinutes > 0;
  return (
    <div className="study-session-page">
      <div className="ss-shell">
        <nav className="ss-navigation" aria-label="Study navigation">
          <button type="button" onClick={onBack} aria-label="Back"><ArrowLeft size={18} aria-hidden="true" /><span>Back</span></button>
          <button type="button" onClick={onReflections}><BookOpen size={17} aria-hidden="true" />My reflections{reflectionCount > 0 ? ` (${reflectionCount})` : ''}</button>
        </nav>
        <header className="lp-masthead ss-masthead">
          <div className="lp-masthead-copy">
            <p className="lp-eyebrow">The study room</p>
            <h1>Study Session.</h1>
            <p className="lp-masthead-subtitle">Choose what to work on. Give it your attention.</p>
          </div>
          <svg className="lp-artwork ss-study-art" viewBox="150 150 724 724" aria-hidden="true">
            <image href="/assets/study/study-session-v2.png" width="1024" height="1024" />
          </svg>
        </header>
        <div className="ss-layout">
          <div className="ss-choices">
            <section className="ss-section" aria-labelledby={`${id}-subjects`}>
              <div className="ss-section-title"><span aria-hidden="true">01</span><h2 id={`${id}-subjects`}>What are you studying?</h2></div>
              {subjects.length > 0 ? <div className="ss-subjects">
                {subjects.map(subject => <button type="button" key={subject.subjectName} aria-pressed={selectedSubject === subject.subjectName} onClick={() => onSubject(subject.subjectName)}>
                  <i style={{ backgroundColor: getSubjectFill(subject.subjectName) }} aria-hidden="true" /><span>{subject.subjectName}</span>
                </button>)}
              </div> : <div className="ss-empty"><h3>Add your subjects to begin.</h3><p>We use them to tailor sessions, strategies and progress.</p>{onSetUpProfile && <button type="button" className="ss-text-action" onClick={onSetUpProfile}>Set up subjects <ArrowRight size={17} /></button>}</div>}
              {lastNote && selectedSubject && <div className="ss-last-note"><p className="ss-eyebrow">Last time you studied {selectedSubject}</p><blockquote>{lastNote}</blockquote></div>}
            </section>
            <section className="ss-section" aria-labelledby={`${id}-type`}>
              <div className="ss-section-title"><span aria-hidden="true">02</span><h2 id={`${id}-type`}>How will you work?</h2></div>
              <div className="ss-types">
                {STUDY_TYPES.map(type => <button type="button" key={type.id} aria-label={`${type.label} ${type.detail}`} aria-pressed={selectedType === type.id} onClick={() => onType(type.id)}><span className="ss-choice-indicator" aria-hidden="true" /><span><strong>{type.label}</strong><small>{type.detail}</small></span></button>)}
              </div>
            </section>
            <section className="ss-section" aria-labelledby={`${id}-duration`}>
              <div className="ss-section-title"><span aria-hidden="true">03</span><h2 id={`${id}-duration`}>Make some time.</h2></div>
              <div className="ss-durations">
                {DURATION_PRESETS.map(preset => <button type="button" key={preset.minutes} aria-label={`${preset.minutes} min`} aria-pressed={selectedMinutes === preset.minutes} onClick={() => onMinutes(preset.minutes)}>{preset.minutes}<span>min</span></button>)}
                <label className="ss-custom-duration" data-selected={custom || undefined}><span className="sr-only">Custom study duration in minutes</span><input type="number" min={MIN_STUDY_SESSION_MINUTES} max={180} placeholder="Custom" value={custom ? selectedMinutes : ''} aria-label="Custom study duration in minutes" aria-describedby={`${id}-duration-help`} aria-invalid={selectedMinutes > 0 && selectedMinutes < MIN_STUDY_SESSION_MINUTES} onChange={event => {
                  const value = parseInt(event.target.value, 10);
                  if (!isNaN(value) && value >= 1 && value <= 180) onMinutes(value);
                  else if (event.target.value === '') onMinutes(0);
                }} /><span aria-hidden="true">min</span></label>
              </div>
              <p id={`${id}-duration-help`} className="ss-duration-help">{selectedMinutes > 0 && selectedMinutes < MIN_STUDY_SESSION_MINUTES ? `Minimum ${MIN_STUDY_SESSION_MINUTES} minutes` : `Choose a preset, or enter ${MIN_STUDY_SESSION_MINUTES}–180 minutes.`}</p>
            </section>
          </div>
          <aside className="ss-sidebar" aria-label="Session overview">
            <section className="ss-session-summary">
              <p className="ss-eyebrow">Your session</p>
              <h2>{selectedSubject || 'Make a start.'}</h2>
              <p className="ss-summary-time"><strong>{selectedMinutes > 0 ? selectedMinutes : '—'}</strong><span>minutes</span></p>
              <p className="ss-summary-type">{STUDY_TYPES.find(type => type.id === selectedType)?.label || 'Choose how you’ll work'}</p>
              <button type="button" className="ss-start" onClick={onStart} disabled={!canStart}>Start Session <Play size={17} fill="currentColor" aria-hidden="true" /></button>
              {startHint && <p className="ss-start-hint">{startHint}</p>}
              <p className="ss-today-total">{sessionCount > 0 ? `${sessionCount} session${sessionCount === 1 ? '' : 's'} today · ${todayMinutes} min total` : 'Your first session of the day.'}</p>
            </section>
            {todayBlocks.length > 0 && <section className="ss-timetable" aria-label="Today’s timetable"><h2>On your plan today</h2><div>{todayBlocks.map(block => <button type="button" key={block.blockId} onClick={() => onBlock(block)} aria-label={`Set up ${block.subject}, ${block.durationMinutes} minutes`}>
              <i style={{ backgroundColor: getSubjectFill(block.subject) }} aria-hidden="true" /><span><strong>{block.subject}</strong><small>{STUDY_TYPES.find(type => type.id === block.sessionType)?.label} · {block.durationMinutes} min</small></span><ArrowRight size={18} aria-hidden="true" />
            </button>)}</div></section>}
          </aside>
        </div>
        {strategyMastery && Object.keys(strategyMastery).length > 0 && <details className="ss-mastery"><summary><span>Your study strategies</span><ChevronDown size={18} aria-hidden="true" /></summary><div className="ss-mastery-list">{STRATEGY_REGISTRY.map(strategy => <div key={strategy.moduleId}><span>{strategy.strategyName}</span><span>{({ none: 'Not started', learned: 'Learned', practiced: 'Practiced', applied: 'Applied', habitual: 'Habitual' } as const)[strategyMastery[strategy.moduleId]?.tier ?? 'none']}</span></div>)}</div>{onProgress && <button type="button" className="ss-text-action" onClick={onProgress}>View progress and milestones <ArrowRight size={16} /></button>}</details>}
      </div>
    </div>
  );
};

export default StudySessionSetup;
