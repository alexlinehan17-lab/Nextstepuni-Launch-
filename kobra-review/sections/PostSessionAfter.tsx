/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Kobra review, section 01 (dev only, 24 Oct 2026): the three steps a student
 * sees after every study session, rebuilt on the Kobra runtime. Every word is
 * the current screens' (StrategyPickerStep, StudySessionFinish and
 * StudySessionSaved), on the same Chemistry session the BEFORE pane mounts.
 *
 * The steps share state so the flow reads end to end: a ticked strategy
 * reaches the receipt, the debrief sets the points on the saved card, and the
 * saved card's buttons start the flow again (as the BEFORE harness does).
 */
import { useEffect, useId, useRef, useState, type CSSProperties } from 'react';
import { ArrowUpRight } from 'lucide-react';
import { Button, Checkbox, RadioGroup, RadioGroupItem, Tabs, TabsList, TabsTrigger } from '../../components/approved-ui-runtime';
import CrewIllustration from '../../components/CrewIllustration';
import { FULL_REFLECTION_POINTS, QUICK_DEBRIEF_POINTS } from '../../components/ReflectionModal';
import { STRATEGY_REGISTRY } from '../../utils/strategyRegistry';
import { getSubjectFill } from '../../utils/subjectColors';
import { formatStudyTime } from '../../utils/studyTime';
import './post-session.css';

// ── Demo session: the BEFORE harness's Chemistry session ─────────
const SUBJECT = 'Chemistry';
const ELAPSED_SECONDS = 2700;
const PLANNED_SECONDS = 2700;
const BASE_POINTS = 40;
const PRACTICE = 'Past paper questions';
const CHARACTER = 'star-crew:maker';
const AUTO_TRACKED = ['mastering-active-recall-protocol', 'mastering-spaced-repetition-protocol'];
const AUTO_SET = new Set(AUTO_TRACKED);
/** Long enough to show "Saving your session…" and the runtime's disabled faces. */
const DEMO_SAVE_MS = 700;

// ── Strategy categories, as StrategyPickerStep groups them ───────
const CATEGORIES: { label: string; ids: string[] }[] = [
  {
    label: 'Recall and retention',
    ids: [
      'mastering-active-recall-protocol',
      'mastering-spaced-repetition-protocol',
      'mastering-interleaving-protocol',
      'elaborative-interrogation-protocol',
    ],
  },
  {
    label: 'Mindset and focus',
    ids: [
      'agency-protocol',
      'growth-mindset-protocol',
      'digital-distraction-protocol',
      'learning-radar-protocol',
    ],
  },
  {
    label: 'Exam prep',
    ids: ['exam-hall-strategies-protocol'],
  },
];
const STRATEGY_BY_ID = new Map(STRATEGY_REGISTRY.map(strategy => [strategy.moduleId, strategy]));
const CONFIDENCE = ['Lost', 'Shaky', 'Okay', 'Good', 'Confident'];

type Mode = 'quick' | 'full';

export default function PostSessionAfter() {
  const id = useId();
  // Step 1
  const [selected, setSelected] = useState<Set<string>>(() => new Set(AUTO_TRACKED));
  const [strategiesSkipped, setStrategiesSkipped] = useState(false);
  // Step 2
  const [mode, setMode] = useState<Mode>('quick');
  const [confidence, setConfidence] = useState('');
  const [reflection, setReflection] = useState('');
  const [busy, setBusy] = useState(false);
  const [withoutDebrief, setWithoutDebrief] = useState(false);
  const [date] = useState(() => new Date());

  const stepOne = useRef<HTMLHeadingElement>(null);
  const stepTwo = useRef<HTMLHeadingElement>(null);
  const stepThree = useRef<HTMLHeadingElement>(null);
  const saveTimer = useRef<number | undefined>(undefined);
  useEffect(() => () => window.clearTimeout(saveTimer.current), []);

  const count = selected.size;
  const valid = Boolean(confidence) && (mode === 'quick' || reflection.trim().length >= 15);
  const bonus = mode === 'quick' ? QUICK_DEBRIEF_POINTS : FULL_REFLECTION_POINTS;
  const early = ELAPSED_SECONDS < PLANNED_SECONDS;
  const note = mode === 'full' ? reflection.trim() : '';
  const strategies = strategiesSkipped
    ? []
    : STRATEGY_REGISTRY.filter(strategy => selected.has(strategy.moduleId)).map(strategy => strategy.strategyName);
  // As StudySessionView: the session's points, plus the debrief bonus when one is saved.
  const savedPoints = BASE_POINTS + (!withoutDebrief && valid ? bonus : 0);

  const toggle = (moduleId: string) => {
    if (AUTO_SET.has(moduleId)) return;
    setStrategiesSkipped(false);
    setSelected(current => {
      const next = new Set(current);
      if (next.has(moduleId)) next.delete(moduleId);
      else next.add(moduleId);
      return next;
    });
  };

  const leaveStepOne = (skip: boolean) => {
    setStrategiesSkipped(skip);
    stepTwo.current?.focus();
  };

  /** Any change to the debrief means it will be saved with one. */
  const editDebrief = () => setWithoutDebrief(false);

  const save = (skip: boolean) => {
    if (busy || (!skip && !valid)) return;
    setBusy(true);
    saveTimer.current = window.setTimeout(() => {
      setBusy(false);
      setWithoutDebrief(skip);
      stepThree.current?.focus();
    }, DEMO_SAVE_MS);
  };

  const startAgain = () => {
    window.clearTimeout(saveTimer.current);
    setSelected(new Set(AUTO_TRACKED));
    setStrategiesSkipped(false);
    setMode('quick');
    setConfidence('');
    setReflection('');
    setBusy(false);
    setWithoutDebrief(false);
    stepOne.current?.focus();
  };

  return (
    <section className="kr-section kr-ps">
      <div className="kr-ps-grid">
        {/* ── Step 1: what helped you focus ── */}
        <section className="kr-ps-card nsu-paper-card" aria-labelledby={`${id}-one`}>
          <header className="kr-ps-head">
            <p className="kr-ps-step">Step 1 of 3 · Strategies</p>
            <span className="kr-ps-subject" style={{ '--kr-ps-subject': getSubjectFill(SUBJECT) } as CSSProperties}>
              <span className="kr-ps-subject-dot" aria-hidden="true" />
              {SUBJECT}
            </span>
          </header>
          <p className="kr-ps-kicker">Before your results</p>
          <h3 id={`${id}-one`} ref={stepOne} tabIndex={-1} className="kr-ps-title">What helped you focus?</h3>
          <p className="kr-ps-lede">Select the strategies you used.</p>

          <dl className="kr-ps-stats">
            <div><dt>Duration</dt><dd>{Math.round(ELAPSED_SECONDS / 60)}m</dd></div>
            <div><dt>Tracked</dt><dd>{AUTO_TRACKED.length}</dd></div>
            <div><dt>JP earned</dt><dd className="kr-ps-accent">+{BASE_POINTS}</dd></div>
          </dl>

          {CATEGORIES.map(category => (
            <fieldset key={category.label} className="kr-ps-group">
              <legend className="kr-ps-group-label">{category.label}</legend>
              <div className="kr-ps-choices">
                {category.ids.map(moduleId => {
                  const strategy = STRATEGY_BY_ID.get(moduleId);
                  if (!strategy) return null;
                  const on = selected.has(moduleId);
                  const auto = AUTO_SET.has(moduleId);
                  return (
                    <label key={moduleId} className="kr-ps-choice" data-checked={on || undefined} data-locked={auto || undefined}>
                      <Checkbox checked={on} disabled={auto} onCheckedChange={() => toggle(moduleId)} />
                      <span className="kr-ps-choice-label">{strategy.strategyName}</span>
                      {auto && <span className="kr-ps-tracked">Tracked</span>}
                    </label>
                  );
                })}
              </div>
            </fieldset>
          ))}

          <div className="kr-ps-actions">
            <Button className="kr-ps-primary" disabled={count === 0} onClick={() => leaveStepOne(false)}>
              {count > 0
                ? `Continue with ${count} ${count === 1 ? 'strategy' : 'strategies'}`
                : 'Select strategies to continue'}
            </Button>
            {count > 0 && <p className="kr-ps-bonus"><em>+5</em> bonus JP for reflecting</p>}
            <Button variant="ghost" className="kr-ps-quiet" onClick={() => leaveStepOne(true)}>Skip this step</Button>
          </div>
        </section>

        {/* ── Step 2: the debrief and the study receipt ── */}
        <section className="kr-ps-card nsu-paper-card" aria-labelledby={`${id}-two`}>
          <header className="kr-ps-head">
            <p className="kr-ps-step">Step 2 of 3 · Debrief</p>
          </header>
          <p className="kr-ps-kicker">{early ? 'Session ended early' : 'Session complete'}</p>
          <h3 id={`${id}-two`} ref={stepTwo} tabIndex={-1} className="kr-ps-title">You showed up.<br />That counts.</h3>
          <p className="kr-ps-lede">{early ? 'The work still counts. ' : ''}A little record of the work you put in. And a clear place to pick up next time.</p>

          <form className="kr-ps-form" onSubmit={event => { event.preventDefault(); save(false); }}>
            <fieldset className="kr-ps-fieldset" disabled={busy}>
              <legend id={`${id}-look-back`} className="kr-ps-legend">A moment to look back</legend>
              <Tabs className="kr-ps-modes" value={mode} onValueChange={value => { setMode(value === 'full' ? 'full' : 'quick'); editDebrief(); }}>
                <TabsList aria-labelledby={`${id}-look-back`}>
                  <TabsTrigger value="quick">Quick debrief <small>+{QUICK_DEBRIEF_POINTS} JP</small></TabsTrigger>
                  <TabsTrigger value="full">Write a reflection <small>+{FULL_REFLECTION_POINTS} JP</small></TabsTrigger>
                </TabsList>
              </Tabs>

              <p id={`${id}-feel`} className="kr-ps-question">How does {SUBJECT} feel after this session?</p>
              <RadioGroup
                className="kr-ps-feel"
                aria-labelledby={`${id}-feel`}
                value={confidence}
                disabled={busy}
                onValueChange={value => { setConfidence(String(value)); editDebrief(); }}
              >
                {CONFIDENCE.map(label => {
                  const value = label.toLowerCase();
                  return (
                    <label key={label} className="kr-ps-feel-option" data-checked={confidence === value || undefined}>
                      <RadioGroupItem value={value} />
                      <span>{label}</span>
                    </label>
                  );
                })}
              </RadioGroup>

              {mode === 'full' && (
                <div className="kr-ps-field">
                  <label htmlFor={`${id}-reflection`}>What worked, and what will you try next time?</label>
                  <textarea
                    id={`${id}-reflection`}
                    className="kr-ps-textarea"
                    value={reflection}
                    onChange={event => { setReflection(event.target.value); editDebrief(); }}
                    minLength={15}
                    maxLength={2000}
                    rows={3}
                    placeholder="A thought worth keeping…"
                    aria-describedby={`${id}-reflection-help`}
                  />
                  <p id={`${id}-reflection-help`} className="kr-ps-help">At least 15 characters. A sentence or two is enough.</p>
                </div>
              )}
            </fieldset>

            <div className="kr-ps-actions">
              <Button type="submit" className="kr-ps-primary" disabled={busy || !valid}>
                {busy ? 'Saving your session…' : 'Save session'}
                <ArrowUpRight aria-hidden="true" />
              </Button>
              <Button type="button" variant="ghost" className="kr-ps-quiet" disabled={busy} onClick={() => save(true)}>
                Save without a debrief
              </Button>
              <p className="kr-ps-note">Saved sessions appear in your progress. Your debrief stays in your study journal.</p>
            </div>
          </form>

          <article className="kr-ps-receipt" aria-label="Your study receipt">
            <header className="kr-ps-receipt-head">
              <div>
                <p className="kr-ps-eyebrow">Nextstepuni / Your study receipt</p>
                <h4 className="kr-ps-receipt-title">A good little session.</h4>
                <p className="kr-ps-detail">{date.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' })}</p>
              </div>
              <span className="kr-ps-art"><CrewIllustration character={CHARACTER} /></span>
            </header>
            <dl className="kr-ps-rows">
              <div><dt>Subject</dt><dd>{SUBJECT}</dd></div>
              <div><dt>Time studied</dt><dd>{formatStudyTime(ELAPSED_SECONDS)}</dd></div>
              <div><dt>Practice</dt><dd>{PRACTICE}</dd></div>
              {strategies.length > 0 && <div><dt>Strategies</dt><dd>{strategies.join(', ')}</dd></div>}
              {confidence && <div><dt>Feeling</dt><dd className="kr-ps-cap">{confidence}</dd></div>}
              <div><dt>JP on saving</dt><dd>{BASE_POINTS}{valid && <> + {bonus} debrief</>}</dd></div>
            </dl>
            <p className="kr-ps-topics">Topics not recorded · subject time is saved.</p>
            <div className="kr-ps-next">
              <span>{note ? 'A note to take with you' : 'Next time'}</span>
              <p>{note || 'Pick up where you left off. One step at a time.'}</p>
            </div>
            <footer className="kr-ps-receipt-foot kr-ps-eyebrow"><span>One step taken.</span><span>Your step.</span></footer>
            <p className="kr-ps-signoff">Small steps, on the record.</p>
          </article>
        </section>

        {/* ── Step 3: saved, and the points to spend ── */}
        <section className="kr-ps-card nsu-paper-card" aria-labelledby={`${id}-three`}>
          <header className="kr-ps-head">
            <p className="kr-ps-step">Step 3 of 3 · Saved</p>
          </header>
          <div className="kr-ps-saved-top">
            <div>
              <p className="kr-ps-eyebrow">Session saved</p>
              <h3 id={`${id}-three`} ref={stepThree} tabIndex={-1} className="kr-ps-points">
                <em>+{savedPoints}</em> <small>JP</small>
              </h3>
            </div>
            <span className="kr-ps-art kr-ps-art-lg"><CrewIllustration character={CHARACTER} /></span>
          </div>
          <p className="kr-ps-lede">{formatStudyTime(ELAPSED_SECONDS)} of {SUBJECT} is on the record. Your Journey Points are ready to spend.</p>
          <div className="kr-ps-actions">
            <Button className="kr-ps-primary" onClick={startAgain}>
              Spend them on your island <ArrowUpRight aria-hidden="true" />
            </Button>
            <Button variant="ghost" className="kr-ps-quiet" onClick={startAgain}>Back to the study room</Button>
          </div>
        </section>
      </div>
    </section>
  );
}
