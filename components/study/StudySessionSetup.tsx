import React, { useEffect, useId, useRef, useState } from 'react';
import {
  BookOpen,
  ChevronDown,
  Volume2,
  VolumeX,
  Check,
} from 'lucide-react';
import type { StudentSubjectProfile } from '../subjectData';
import type { StrategyMasteryMap } from '../../types';
import type { TimetableBlockContext } from './StudySessionView';
import { DURATION_PRESETS, STRATEGY_REGISTRY } from '../../studySessionData';
import { MIN_STUDY_SESSION_MINUTES } from '../../hooks/useStudySession';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';
import SubjectAvatar from '../SubjectAvatar';
import KobraScope from '../approved-ui-runtime';
import type { PlanStep } from '../approved-ui-runtime';
import { setSoundMuted, useSoundMuted } from '../approved-ui-runtime';
import { TopBar, PinnedFooter } from '../ui/Bars';
import { Button, Glyph, IconButton, TextButton, type MissingStep } from '../ui/Button';
import { ChoiceTile, Switch, useRovingRadios } from '../ui/Choice';
import { List, PaperSheet, Row } from '../ui/List';
import { useFrameTask } from '../ui/Frame';
import StudySubjectPicker, { StudySubjectArtwork } from './StudySubjectPicker';
import { SessionTodos } from './SessionTodos';
import StudyTopicPicker from './StudyTopicPicker';
import StudyFocusChoice from './StudyFocusChoice';
import StudyRule, { cardMarks } from './StudyRule';
import { StudyTodoDot } from './StudyTodoDot';
import { formatTime } from './StudySessionTimer';
import './study-kobra.css';
import './study-setup.css';

type SessionType = 'new-learning' | 'practice' | 'revision';
export const STUDY_TYPES: { id: SessionType; label: string; detail: string }[] = [
  { id: 'new-learning', label: 'New Learning', detail: 'Meet it for the first time' },
  { id: 'practice', label: 'Practice', detail: 'Work through questions' },
  { id: 'revision', label: 'Revision', detail: 'Recall what you know' },
];

/** The three to-dos the box writes itself until a student writes their own. */
const PROMPTS = new Set(['Choose your subject', 'Choose how you’ll work', 'Make some time']);

interface StudySessionSetupProps {
  todos?: PlanStep[] | null;
  onTodosChange?: (steps: PlanStep[]) => void;
  colourfulTimer?: boolean;
  onColourfulTimerChange?: (value: boolean) => void;
  /** Quiz on what was studied once the session is saved (settings.studyQuiz). */
  quizAtEnd?: boolean;
  onQuizAtEndChange?: (value: boolean) => void;
  examDate?: string | null;
  topicIds?: string[];
  onTopics?: (ids: string[]) => void;
  subjects: StudentSubjectProfile['subjects'];
  selectedSubject: string;
  selectedType: SessionType | '';
  selectedMinutes: number;
  /** Stopwatch session: no set end, finish when done. */
  openEnded?: boolean;
  onOpenEnded?: () => void;
  onSubject: (subject: string) => void;
  onType: (type: SessionType) => void;
  onMinutes: (minutes: number) => void;
  /** Cancel, at the top left once anything is chosen: clears the choices and brings the tab bar back. */
  onClear?: () => void;
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

function words(list: string[]) {
  return list.length < 2 ? list.join('') : `${list.slice(0, -1).join(', ')} and ${list[list.length - 1]}`;
}

const StudySessionSetup: React.FC<StudySessionSetupProps> = (props) => {
  const {
    subjects,
    selectedSubject,
    selectedType,
    selectedMinutes,
    openEnded = false,
    onOpenEnded,
    onSubject,
    onType,
    onMinutes,
    onClear,
    todayBlocks,
    onBlock,
    sessionCount,
    todayMinutes,
    reflectionCount,
    strategyMastery,
    onProgress,
    onReflections,
    onSetUpProfile,
    onStart,
    canStart,
    todos,
    onTodosChange,
  } = props;
  const id = useId();
  const phone = useMobileAppDesign();
  const muted = useSoundMuted();
  const [editing, setEditing] = useState(false);
  const [saved, setSaved] = useState(false);
  const [localTodos, setLocalTodos] = useState<PlanStep[] | null>(null);
  // The custom field shows its own number; a preset leaves it empty, as drawn.
  const [typing, setTyping] = useState(false);
  const isPreset = DURATION_PRESETS.some(preset => preset.minutes === selectedMinutes);
  const subjectStep = useRef<HTMLDivElement>(null);
  const methodStep = useRef<HTMLDivElement>(null);
  const timeStep = useRef<HTMLDivElement>(null);
  const method = STUDY_TYPES.find((type) => type.id === selectedType);
  const methodKeys = useRovingRadios(STUDY_TYPES.length, STUDY_TYPES.findIndex(type => type.id === selectedType), index => onType(STUDY_TYPES[index].id));
  const timeChosen = openEnded || selectedMinutes >= MIN_STUDY_SESSION_MINUTES;
  const defaults: PlanStep[] = [
    { label: selectedSubject || 'Choose your subject', done: !!selectedSubject },
    { label: method?.detail || 'Choose how you’ll work', done: !!selectedType },
    {
      label: openEnded
        ? 'Open-ended: finish when you’re done'
        : selectedMinutes >= MIN_STUDY_SESSION_MINUTES
          ? `${selectedMinutes} minutes of attention`
          : 'Make some time',
      done: timeChosen,
    },
  ];
  const custom = todos ?? localTodos;
  const steps = custom ?? defaults;
  // A to-do the student wrote is set; one the box wrote is set once it is chosen.
  const isSet = (step: PlanStep) => (custom ? !!step.done || !PROMPTS.has(step.label) : !!step.done);

  // Place, then task: once anything is chosen, the pinned Start takes the tab bar's place (phone).
  const going = Boolean(selectedSubject || selectedType || selectedMinutes || openEnded);
  useFrameTask(phone && going);

  // What is still missing, in words, and where pressing Start early takes the student.
  const missing: { word: string; goTo: MissingStep['goTo'] }[] = [];
  if (!selectedSubject) missing.push({ word: 'your subject', goTo: subjectStep });
  if (!selectedType) missing.push({ word: 'how you’ll work', goTo: methodStep });
  if (!timeChosen) missing.push({ word: 'your time', goTo: timeStep });
  const missingStep: MissingStep | undefined = !canStart
    ? subjects.length === 0
      ? { sentence: 'Add your subjects to begin.', goTo: subjectStep }
      : { sentence: `Still to choose: ${words(missing.map((item) => item.word)) || 'your session'}.`, goTo: missing[0]?.goTo ?? subjectStep }
    : undefined;
  const ready = `${selectedSubject} · ${method?.label ?? ''} · ${openEnded ? 'Open-ended' : `${selectedMinutes} min`}`;

  // The Kobra plan card it replaces started the session on Cmd/Ctrl + Enter: kept.
  const startKeys = useRef({ canStart, editing, onStart });
  startKeys.current = { canStart, editing, onStart };
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key !== 'Enter' || !(event.metaKey || event.ctrlKey)) return;
      const current = startKeys.current;
      if (!current.canStart || current.editing) return;
      event.preventDefault();
      current.onStart();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const soundLabel = muted ? 'Turn study sound on' : 'Turn study sound off';
  const reflectionsLabel = `My reflections${reflectionCount > 0 ? `, ${reflectionCount}` : ''}`;
  const startButton = (
    <Button kind="main" size="lg" block arrow="forward" missing={missingStep} onClick={onStart}>Start session</Button>
  );

  const head = phone ? (
    <>
      <TopBar
        className="sset-bar"
        leave={going && onClear ? { kind: 'cancel', onPress: onClear, label: 'Cancel' } : undefined}
        placeLabel="The Study Room"
        action={
          <span className="sset-bar-actions">
            <IconButton label={reflectionsLabel} icon={<Glyph icon={BookOpen} />} onClick={onReflections} />
            <IconButton label={soundLabel} aria-pressed={!muted} icon={<Glyph icon={muted ? VolumeX : Volume2} />} onClick={() => setSoundMuted(!muted)} />
          </span>
        }
      />
      <header className="sset-head">
        <h1 className="t-display">Study session.</h1>
        <p className="t-sub">Choose what to work on. Give it your attention.</p>
      </header>
    </>
  ) : (
    <header className="sset-head sset-head--desk">
      <div className="sset-head-words">
        <p className="t-label">The Study Room</p>
        <h1 className="t-display">Study session.</h1>
        <p className="t-sub">Choose what to work on. Give it your attention.</p>
      </div>
      <div className="sset-acts">
        <TextButton tone="quiet" onClick={onReflections} aria-label={reflectionsLabel}>
          <BookOpen className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />
          My reflections{reflectionCount > 0 ? <span className="t-readout sset-count">{reflectionCount}</span> : null}
        </TextButton>
        <TextButton tone="quiet" onClick={() => setSoundMuted(!muted)} aria-label={soundLabel} aria-pressed={!muted}>
          {muted ? <VolumeX className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /> : <Volume2 className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}
          Sound {muted ? 'off' : 'on'}
        </TextButton>
      </div>
    </header>
  );

  const session = (
    <section className="sset-session" aria-label="Session overview" data-sec="session">
      <div className="sset-sesshead">
        {selectedSubject && <span className="sset-face"><StudySubjectArtwork subject={selectedSubject} size={104} /></span>}
        <div className="sset-sesswords">
          <p className="t-label">Your session</p>
          <h2 className="t-title">A little focus.<br /> A little further.</h2>
        </div>
      </div>
      <PaperSheet className="sset-card" label={selectedSubject ? `Your session: ${selectedSubject}` : 'Your session'}>
        <div className="sset-cardtop">
          <h3 className="t-name-sm">{selectedSubject || 'Make a start.'}</h3>
          <span className={`t-readout sset-readout${selectedMinutes || openEnded ? '' : ' sset-readout--off'}`}>{formatTime(openEnded ? 0 : selectedMinutes * 60)}</span>
        </div>
        {(selectedMinutes > 0 || openEnded || method) && (
          <p className="t-sub sset-cardmeta">
            {[openEnded ? 'Open-ended' : selectedMinutes > 0 ? `${selectedMinutes} minutes` : null, method?.label].filter(Boolean).join(' · ')}
          </p>
        )}
        <StudyRule size="card" className="sset-rule" marks={cardMarks(openEnded ? 0 : selectedMinutes)} />
        <div className="sset-todohead">
          <h4 className="t-row">To-dos</h4>
          <TextButton tone="quiet" onClick={() => { setSaved(false); setEditing(true); }}>Edit to-dos</TextButton>
        </div>
        <ul className="sset-todos" aria-label="To-dos">
          {steps.map((step, index) => (
            <li key={`${index}-${step.label}`} className={isSet(step) ? 'is-set' : 'is-open'}>
              <StudyTodoDot set={isSet(step)} done={false} />
              <span>{step.label}</span>
            </li>
          ))}
        </ul>
        {saved && (
          <p className="sset-saved" role="status">
            <span className="nsu-success-mark"><Check size={14} aria-hidden="true" /></span>
            To-dos updated.
          </p>
        )}
        {props.onQuizAtEndChange && (
          <div className="sset-switch">
            <div>
              <label htmlFor={`${id}-quiz`} className="t-row">Offer me questions when I finish</label>
              <p id={`${id}-quiz-help`} className="t-meta">
                {props.quizAtEnd
                  ? 'Choose whether to try real exam questions on the topics you studied.'
                  : 'Straight to your points when you log the session.'}
              </p>
            </div>
            <Switch id={`${id}-quiz`} checked={!!props.quizAtEnd} onChange={props.onQuizAtEndChange}
              aria-label="Offer me questions when I finish" aria-describedby={`${id}-quiz-help`} />
          </div>
        )}
        {!phone && (
          <div className="sset-start">
            {canStart && <p className="sset-ready">{ready}</p>}
            {startButton}
          </div>
        )}
      </PaperSheet>
    </section>
  );

  // Today's quieter extras, kept in the look below the box: the timer's colour
  // (the "more colour" room stays), app blocking on iOS, today's total, the
  // plan's rows and the strategies list (none of them is on the agreed board).
  const extras = (
    <div className="sset-extras">
      {props.onColourfulTimerChange && (
        <div className="sset-switch sset-switch--page">
          <div>
            <label htmlFor={`${id}-colourful`} className="t-row">I want my timer to have more colour!</label>
            <p id={`${id}-appearance-help`} className="t-meta">
              {props.colourfulTimer
                ? 'Paper horizon · gentle layers in your subject’s colour.'
                : 'After hours · a quiet dark study room.'}
            </p>
          </div>
          <Switch id={`${id}-colourful`} checked={!!props.colourfulTimer} onChange={props.onColourfulTimerChange}
            aria-label="I want my timer to have more colour!" aria-describedby={`${id}-appearance-help`} />
        </div>
      )}
      <StudyFocusChoice />
      <p className="t-meta sset-today">
        {sessionCount
          ? `${sessionCount} session${sessionCount === 1 ? '' : 's'} today · ${todayMinutes} min total`
          : 'Your first session of the day.'}
      </p>
      {todayBlocks.length > 0 && (
        <section className="sset-plan" aria-label="Today’s timetable">
          <h2 className="t-heading">On your plan today</h2>
          <List>
            {todayBlocks.map((block) => (
              <Row
                key={block.blockId}
                art={<SubjectAvatar subject={block.subject} bare />}
                title={block.subject}
                meta={`${STUDY_TYPES.find((type) => type.id === block.sessionType)?.label} · ${block.durationMinutes} min`}
                label={`Set up ${block.subject}, ${block.durationMinutes} minutes`}
                onPress={() => onBlock(block)}
              />
            ))}
          </List>
        </section>
      )}
      {strategyMastery && Object.keys(strategyMastery).length > 0 && (
        <details className="sset-mastery">
          <summary>
            <span className="t-heading">Your study strategies</span>
            <ChevronDown size={20} strokeWidth={1.75} aria-hidden="true" />
          </summary>
          <div className="sset-mastery-list">
            {STRATEGY_REGISTRY.map((strategy) => (
              <div key={strategy.moduleId}>
                <span>{strategy.strategyName}</span>
                <span className="t-meta">
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
          {onProgress && <TextButton arrow="forward" onClick={onProgress}>View progress and milestones</TextButton>}
        </details>
      )}
    </div>
  );

  return (
    <KobraScope className={`sset${phone ? ' sset--phone' : ' sset--desk'}`}>
      <div className="sset-page" data-going={going || undefined}>
        {head}
        <div className="sset-cols">
          <div className="sset-questions">
            <section className="sset-sec" aria-labelledby={`${id}-subjects`} data-sec="subject">
              <p className="t-label">01 / Subject</p>
              <h2 id={`${id}-subjects`} className="t-title">What are you studying?</h2>
              <p className="t-sub">A familiar face for every subject.</p>
              {subjects.length ? (
                <StudySubjectPicker
                  subjects={subjects.map((subject) => subject.subjectName)}
                  selected={selectedSubject}
                  onSelect={onSubject}
                  namesRef={subjectStep}
                />
              ) : (
                <div ref={subjectStep} className="sset-empty" data-study-step="subject">
                  <h3 className="t-heading">Add your subjects to begin.</h3>
                  <p className="t-sub">We use them to tailor sessions, strategies and progress.</p>
                  {onSetUpProfile && <Button arrow="forward" onClick={onSetUpProfile}>Set up subjects</Button>}
                </div>
              )}
              {props.onTopics && <StudyTopicPicker subject={selectedSubject} examDate={props.examDate} level={subjects.find(subject => subject.subjectName === selectedSubject)?.level} selected={props.topicIds ?? []} onChange={props.onTopics} />}
            </section>
            <section className="sset-sec" aria-labelledby={`${id}-type`} data-sec="method">
              <p className="t-label">02 / How you work</p>
              <h2 id={`${id}-type`} className="t-title">How will you work?</h2>
              <div ref={methodStep} role="radiogroup" aria-labelledby={`${id}-type`} className="sset-step sset-methods" data-study-step="method">
                {STUDY_TYPES.map((type, index) => (
                  <ChoiceTile key={type.id} className="sset-method" chosen={selectedType === type.id}
                    ref={element => { methodKeys.refs.current[index] = element; }}
                    tabIndex={methodKeys.tabIndexOf(index)} onKeyDown={event => methodKeys.onKeyDown(event, index)}
                    label={type.label} meta={type.detail} onClick={() => onType(type.id)} />
                ))}
              </div>
            </section>
            <section className="sset-sec" aria-labelledby={`${id}-duration`} data-sec="time">
              <p className="t-label">03 / Time</p>
              <h2 id={`${id}-duration`} className="t-title">Make some time.</h2>
              <div ref={timeStep} role="radiogroup" aria-labelledby={`${id}-duration`} className="sset-step sset-time" data-study-step="time">
                <div className="sset-presets">
                  {DURATION_PRESETS.map((preset) => (
                    <ChoiceTile key={preset.minutes} className="sset-preset" chosen={!openEnded && selectedMinutes === preset.minutes}
                      label={`${preset.minutes} min`} onClick={() => { setTyping(false); onMinutes(preset.minutes); }} />
                  ))}
                  <label className="sset-custom" data-selected={!openEnded && selectedMinutes > 0 && (typing || !isPreset) || undefined}>
                    <span>Custom</span>
                    <input
                      type="number"
                      placeholder="–"
                      inputMode="numeric"
                      enterKeyHint="done"
                      min={MIN_STUDY_SESSION_MINUTES}
                      max={180}
                      value={openEnded || (isPreset && !typing) ? '' : selectedMinutes || ''}
                      aria-label="Custom study duration in minutes"
                      aria-describedby={`${id}-duration-help`}
                      aria-invalid={selectedMinutes > 0 && selectedMinutes < MIN_STUDY_SESSION_MINUTES}
                      onChange={(event) => {
                        setTyping(true);
                        const value = Number(event.target.value);
                        if (event.target.value === '') onMinutes(0);
                        else if (Number.isInteger(value) && value >= 1 && value <= 180)
                          onMinutes(value);
                      }}
                    />
                    <span>min</span>
                  </label>
                </div>
                {onOpenEnded && (
                  <ChoiceTile className="sset-method sset-open" chosen={openEnded} aria-describedby={`${id}-duration-help`}
                    label="Open-ended" meta="Count up, stop when you’re done" onClick={onOpenEnded} />
                )}
              </div>
              <p id={`${id}-duration-help`} className={`t-meta sset-help${selectedMinutes > 0 && selectedMinutes < MIN_STUDY_SESSION_MINUTES ? ' sset-help--err' : ''}`}>
                {openEnded
                  ? `The clock counts up. Finish whenever you’re done, after ${MIN_STUDY_SESSION_MINUTES} minutes or more.`
                  : selectedMinutes > 0 && selectedMinutes < MIN_STUDY_SESSION_MINUTES
                    ? `Minimum ${MIN_STUDY_SESSION_MINUTES} minutes`
                    : `Choose a preset or enter ${MIN_STUDY_SESSION_MINUTES}–180 minutes.`}
              </p>
            </section>
            {phone && session}
            {extras}
          </div>
          {!phone && <aside className="sset-aside">{session}</aside>}
        </div>
        {phone && going && (
          <PinnedFooter ruled className="sset-foot">
            {canStart && <p className="sset-ready">{ready}</p>}
            {startButton}
          </PinnedFooter>
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
