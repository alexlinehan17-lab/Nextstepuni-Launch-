import React, { useId, useState } from 'react';
import {
  ArrowRight,
  BookOpen,
  ChevronDown,
  Clock3,
  Volume2,
  VolumeX,
  Check,
} from 'lucide-react';
import type { StudentSubjectProfile } from '../subjectData';
import type { StrategyMasteryMap } from '../../types';
import type { TimetableBlockContext } from './StudySessionView';
import { DURATION_PRESETS, STRATEGY_REGISTRY } from '../../studySessionData';
import { MIN_STUDY_SESSION_MINUTES } from '../../hooks/useStudySession';
import SubjectAvatar from '../SubjectAvatar';
import KobraScope from '../approved-ui-runtime';
import BackButton from '../ui/BackButton';
import { Button } from '../approved-ui-runtime';
import { Input } from '../approved-ui-runtime';
import { Switch } from '../approved-ui-runtime';
import { RadioGroup, RadioGroupItem } from '../approved-ui-runtime';
import { PlanCard, type PlanStep } from '../approved-ui-runtime';
import { setSoundMuted, useSoundMuted } from '../approved-ui-runtime';
import StudySubjectPicker, { StudySubjectArtwork } from './StudySubjectPicker';
import { SessionTodos } from './SessionTodos';
import StudyTopicPicker from './StudyTopicPicker';
import './study-kobra.css';

type SessionType = 'new-learning' | 'practice' | 'revision';
export const STUDY_TYPES: { id: SessionType; label: string; detail: string }[] = [
  { id: 'new-learning', label: 'New Learning', detail: 'Meet it for the first time' },
  { id: 'practice', label: 'Practice', detail: 'Work through questions' },
  { id: 'revision', label: 'Revision', detail: 'Recall what you know' },
];

interface StudySessionSetupProps {
  todos?: PlanStep[] | null;
  onTodosChange?: (steps: PlanStep[]) => void;
  colourfulTimer?: boolean;
  onColourfulTimerChange?: (value: boolean) => void;
  examDate?: string | null;
  topicIds?: string[];
  onTopics?: (ids: string[]) => void;
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
  const {
    subjects,
    selectedSubject,
    selectedType,
    selectedMinutes,
    onSubject,
    onType,
    onMinutes,
    todayBlocks,
    onBlock,
    sessionCount,
    todayMinutes,
    reflectionCount,
    strategyMastery,
    onProgress,
    onReflections,
    onBack,
    onSetUpProfile,
    onStart,
    canStart,
    startHint,
    todos,
    onTodosChange,
  } = props;
  const id = useId();
  const muted = useSoundMuted();
  const [editing, setEditing] = useState(false);
  const [saved, setSaved] = useState(false);
  const [localTodos, setLocalTodos] = useState<PlanStep[] | null>(null);
  const method = STUDY_TYPES.find((type) => type.id === selectedType);
  const steps = todos ??
    localTodos ?? [
      { label: selectedSubject || 'Choose your subject', done: !!selectedSubject },
      { label: method?.detail || 'Choose how you’ll work', done: !!selectedType },
      {
        label:
          selectedMinutes >= MIN_STUDY_SESSION_MINUTES
            ? `${selectedMinutes} minutes of attention`
            : 'Make some time',
        done: selectedMinutes >= MIN_STUDY_SESSION_MINUTES,
      },
    ];
  return (
    <KobraScope className="ks-page">
      <div className="ks-shell">
        <nav className="ks-navigation" aria-label="Study navigation">
          <BackButton onClick={onBack} label="Back to home" />
          <span aria-hidden="true">/</span>
          <span>The Study Room</span>
          <div className="ks-nav-actions">
            <Button variant="ghost" onClick={onReflections}>
              <BookOpen />
              My reflections{reflectionCount > 0 ? ` (${reflectionCount})` : ''}
            </Button>
            <Button
              variant="ghost"
              onClick={() => setSoundMuted(!muted)}
              aria-label={muted ? 'Turn study sound on' : 'Turn study sound off'}
            >
              {muted ? <VolumeX /> : <Volume2 />}
              <span>Sound {muted ? 'off' : 'on'}</span>
            </Button>
          </div>
        </nav>
        <header className="ks-masthead">
          <div>
            <p className="ks-eyebrow">The Study Room</p>
            <h1>
              Study <em>Session.</em>
            </h1>
            <p>
              Choose what to work on. Give it your attention.
            </p>
          </div>
        </header>
        <div className="ks-layout">
          <div className="ks-sections">
            <section className="ks-section" aria-labelledby={`${id}-subjects`}>
              <p className="ks-eyebrow">01 / The study room</p>
              <h2 id={`${id}-subjects`}>What are you studying?</h2>
              <p className="ks-copy">A familiar face for every subject.</p>
              {subjects.length ? (
                <StudySubjectPicker
                  subjects={subjects.map((subject) => subject.subjectName)}
                  selected={selectedSubject}
                  onSelect={onSubject}
                />
              ) : (
                <div className="ks-empty">
                  <h3>Add your subjects to begin.</h3>
                  <p>We use them to tailor sessions, strategies and progress.</p>
                  {onSetUpProfile && (
                    <Button variant="outline" className="nsu-ink-outline" onClick={onSetUpProfile}>
                      Set up subjects <ArrowRight />
                    </Button>
                  )}
                </div>
              )}
              {props.onTopics && <StudyTopicPicker subject={selectedSubject} examDate={props.examDate} level={subjects.find(subject => subject.subjectName === selectedSubject)?.level} selected={props.topicIds ?? []} onChange={props.onTopics} />}
            </section>
            <section className="ks-section" aria-labelledby={`${id}-type`}>
              <p className="ks-eyebrow">02 / The study room</p>
              <h2 id={`${id}-type`}>How will you work?</h2>
              <RadioGroup
                value={selectedType}
                onValueChange={(value) => onType(value as SessionType)}
                aria-label="Study method"
                className="ks-methods"
              >
                {STUDY_TYPES.map((type) => (
                  <label
                    key={type.id}
                    className="ks-choice"
                    data-selected={selectedType === type.id}
                  >
                    <RadioGroupItem value={type.id} />
                    <span>
                      <strong>{type.label}</strong>{' '}
                      <small>{type.detail}</small>
                    </span>
                  </label>
                ))}
              </RadioGroup>
            </section>
            <section className="ks-section" aria-labelledby={`${id}-duration`}>
              <p className="ks-eyebrow">03 / The study room</p>
              <h2 id={`${id}-duration`}>Make some time.</h2>
              <div className="ss-durations">
                {DURATION_PRESETS.map((preset) => (
                  <Button
                    key={preset.minutes}
                    variant="outline"
                    className="nsu-ink-outline"
                    aria-label={`${preset.minutes} min`}
                    aria-pressed={selectedMinutes === preset.minutes}
                    onClick={() => onMinutes(preset.minutes)}
                  >
                    {preset.minutes} min
                  </Button>
                ))}
                <label className="ks-custom-duration" data-selected={selectedMinutes > 0 && !DURATION_PRESETS.some(preset => preset.minutes === selectedMinutes)}>
                  <span>Custom</span>
                  <Input
                    type="number"
                    placeholder="—"
                    inputMode="numeric"
                    min={MIN_STUDY_SESSION_MINUTES}
                    max={180}
                    value={selectedMinutes || ''}
                    aria-label="Custom study duration in minutes"
                    aria-describedby={`${id}-duration-help`}
                    aria-invalid={selectedMinutes > 0 && selectedMinutes < MIN_STUDY_SESSION_MINUTES}
                    onChange={(event) => {
                      const value = Number(event.target.value);
                      if (event.target.value === '') onMinutes(0);
                      else if (Number.isInteger(value) && value >= 1 && value <= 180)
                        onMinutes(value);
                    }}
                  />
                  <span>min</span>
                </label>
              </div>
              <p id={`${id}-duration-help`} className="ss-duration-help">
                {selectedMinutes > 0 && selectedMinutes < MIN_STUDY_SESSION_MINUTES
                  ? `Minimum ${MIN_STUDY_SESSION_MINUTES} minutes`
                  : `Choose a preset or enter ${MIN_STUDY_SESSION_MINUTES}–180 minutes.`}
              </p>
            </section>
          </div>
          <aside className="ks-sidebar" aria-label="Session overview">
            <section className="ks-session-summary">
              <div className="ks-session-intro">
                {selectedSubject && <StudySubjectArtwork subject={selectedSubject} size={64} />}
                <div>
                  <p className="ks-eyebrow">Your session</p>
                  <h2>
                    A little focus.
                    <br /> A little further.
                  </h2>
                </div>
              </div>
              <PlanCard
                className="nsu-plan-card"
                icon={<Clock3 />}
                title={selectedSubject || 'Make a start.'}
                description={`${selectedMinutes > 0 ? `${selectedMinutes} minutes` : 'Choose your duration'} · ${method?.label || 'Choose a method'}`}
                steps={steps}
                visibleSteps={3}
                approveLabel="Start Session"
                approveDisabled={!canStart || editing}
                viewLabel="Edit to-dos"
                onView={() => {
                  setSaved(false);
                  setEditing(true);
                }}
                onApprove={onStart}
              />
              {saved && (
                <p className="ks-save-feedback" role="status">
                  <span className="nsu-success-mark">
                    <Check size={14} />
                  </span>
                  To-dos updated.
                </p>
              )}
              {startHint && <p className="ks-start-hint">{startHint}</p>}
              <p className="ks-today-total">
                {sessionCount
                  ? `${sessionCount} session${sessionCount === 1 ? '' : 's'} today · ${todayMinutes} min total`
                  : 'Your first session of the day.'}
              </p>
            </section>
            {props.onColourfulTimerChange && (
              <div className="ks-appearance-choice">
                <div>
                  <label htmlFor={`${id}-colourful`}>I want my timer to have more colour!</label>
                  <p id={`${id}-appearance-help`}>
                    {props.colourfulTimer
                      ? 'Paper horizon · gentle layers in your subject’s colour.'
                      : 'After hours · a quiet dark study room.'}
                  </p>
                </div>
                <Switch
                  id={`${id}-colourful`}
                  checked={!!props.colourfulTimer}
                  onCheckedChange={props.onColourfulTimerChange}
                  aria-label="I want my timer to have more colour!"
                  aria-describedby={`${id}-appearance-help`}
                />
              </div>
            )}
            {todayBlocks.length > 0 && (
              <section className="ks-timetable" aria-label="Today’s timetable">
                <h2>On your plan today</h2>
                <div>
                  {todayBlocks.map((block) => (
                    <Button
                      variant="ghost"
                      key={block.blockId}
                      onClick={() => onBlock(block)}
                      aria-label={`Set up ${block.subject}, ${block.durationMinutes} minutes`}
                    >
                      <SubjectAvatar subject={block.subject} />
                      <span>
                        <strong>{block.subject}</strong>
                        <small>
                          {STUDY_TYPES.find((type) => type.id === block.sessionType)?.label} ·{' '}
                          {block.durationMinutes} min
                        </small>
                      </span>
                      <ArrowRight />
                    </Button>
                  ))}
                </div>
              </section>
            )}
          </aside>
        </div>
        {strategyMastery && Object.keys(strategyMastery).length > 0 && (
          <details className="ks-mastery">
            <summary>
              <span>Your study strategies</span>
              <ChevronDown size={18} aria-hidden="true" />
            </summary>
            <div>
              {STRATEGY_REGISTRY.map((strategy) => (
                <div key={strategy.moduleId}>
                  <span>{strategy.strategyName}</span>
                  <span>
                    {
                      (
                        {
                          none: 'Not started',
                          learned: 'Read',
                          practiced: 'Practiced',
                          applied: 'Applied',
                          habitual: 'Habitual',
                        } as const
                      )[strategyMastery[strategy.moduleId]?.tier ?? 'none']
                    }
                  </span>
                </div>
              ))}
            </div>
            {onProgress && (
              <Button variant="ghost" onClick={onProgress}>
                View progress and milestones <ArrowRight />
              </Button>
            )}
          </details>
        )}
      </div>
      {editing && (
        <SessionTodos
          steps={steps}
          onClose={() => setEditing(false)}
          onSave={(next) => {
            (onTodosChange ?? setLocalTodos)(next);
            setEditing(false);
            setSaved(true);
          }}
        />
      )}
    </KobraScope>
  );
};
export default StudySessionSetup;
