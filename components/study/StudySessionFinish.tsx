/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The debrief after a session, then the study receipt (r5-post-session,
 * agreed 26 Nov 2026). The debrief lies on the page in the one typeface:
 * Quick debrief or Write a reflection in the selection bar, the feelings as
 * choices with the ink outline, and Save session pinned at the bottom saying
 * what is still to choose. The receipt is unchanged, markup and study-crew.css
 * rules alike (Alex, 25 Oct: "this is really cool and we can't lose it").
 */
import React, { useEffect, useId, useRef, useState } from 'react';
import KobraScope from '../approved-ui-runtime';
import CrewIllustration from '../CrewIllustration';
import { QUICK_DEBRIEF_POINTS, FULL_REFLECTION_POINTS } from '../ReflectionModal';
import type { StudyTopicAllocation, StudyTopicSelection } from '../../types/studyTopics';
import { equalTopicAllocations } from '../../services/studyTopicHistory';
import { CURRICULUM_SPECIFICATIONS } from '../../curriculumRegistry';
import { PinnedFooter, TopBar } from '../ui/Bars';
import { Button, TextButton, type MissingStep } from '../ui/Button';
import { ChoiceTile, SelectionBar, useRovingRadios } from '../ui/Choice';
import { useFrameTask } from '../ui/Frame';
import TopicTimeCard from './TopicTimeCard';
import './study-crew.css';
import './study-post-session.css';
import './study-after.css';

export { formatStudyTime } from '../../utils/studyTime';
import { formatStudyTime } from '../../utils/studyTime';

interface Props {
  subject: string; elapsedSeconds: number; plannedSeconds: number; practice: string;
  character?: string; strategies: string[]; basePoints: number; isSaving: boolean;
  /** JP for finishing the time added with "Keep going". */
  extensionBonus?: number;
  mode: 'quick' | 'full'; onModeChange: (mode: 'quick' | 'full') => void;
  topicSelection?: StudyTopicSelection;
  onSave: (reflection: string, allocations?: StudyTopicAllocation[]) => Promise<void>; onSkip: (allocations?: StudyTopicAllocation[]) => Promise<void>;
}

const CONFIDENCE = ['Lost', 'Shaky', 'Okay', 'Good', 'Confident'];

export default function StudySessionFinish({ subject, elapsedSeconds, plannedSeconds, practice, character, strategies, basePoints, extensionBonus = 0, isSaving, mode, onModeChange, onSave, onSkip, topicSelection }: Props) {
  const id = useId();
  const formId = useId();
  const feelRef = useRef<HTMLDivElement>(null);
  const reflectionRef = useRef<HTMLTextAreaElement>(null);
  // A task: the tab bar steps aside; and it opens at the top, on its headline.
  useFrameTask(true);
  useEffect(() => { try { window.scrollTo({ top: 0 }); } catch { /* no window to scroll */ } }, []);

  const [topicTimeOpen, setTopicTimeOpen] = useState(false);
  const [allocations, setAllocations] = useState(() => equalTopicAllocations(topicSelection?.topicIds ?? [], elapsedSeconds));
  const spec = CURRICULUM_SPECIFICATIONS.find(item => item.id === topicSelection?.specificationId);
  const topicNames = new Map(spec?.groups.flatMap(group => [[group.id, group.title], ...group.topics.map(topic => [topic.id, topic.title])]) as [string, string][]);
  const [confidence, setConfidence] = useState('');
  const [reflection, setReflection] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [date] = useState(() => new Date());
  const inFlight = useRef(false);
  const busy = isSaving || submitting;
  const valid = Boolean(confidence) && (mode === 'quick' || reflection.trim().length >= 15);
  const bonus = mode === 'quick' ? QUICK_DEBRIEF_POINTS : FULL_REFLECTION_POINTS;
  const early = elapsedSeconds < plannedSeconds;
  const submit = async (skip: boolean) => {
    if (busy || inFlight.current || (!skip && !valid)) return;
    inFlight.current = true; setSubmitting(true); setError('');
    try {
      const text = mode === 'quick' ? confidence : `${confidence}|${reflection.trim()}`;
      if (skip) await (topicSelection ? onSkip(allocations) : onSkip());
      else await (topicSelection ? onSave(text, allocations) : onSave(text));
    }
    catch { setError('Your session couldn’t be saved. Please try again. Your debrief is still here.'); }
    finally { inFlight.current = false; setSubmitting(false); }
  };
  const feelings = useRovingRadios(CONFIDENCE.length, CONFIDENCE.findIndex(label => label.toLowerCase() === confidence), index => setConfidence(CONFIDENCE[index].toLowerCase()));
  const missing: MissingStep | undefined = !confidence
    ? { sentence: `Still to choose: how ${subject} feels.`, goTo: feelRef }
    : !valid ? { sentence: 'Still to write: a sentence or two for your reflection.', goTo: reflectionRef } : undefined;
  const chosen = CONFIDENCE.find(label => label.toLowerCase() === confidence);
  return <KobraScope className="nsu-post-session"><div className="sps-page sps-flow">
    <TopBar className="sps-bar" placeLabel={early ? 'Session ended early' : 'Session complete'} />
    <section className="sps-finish sps-finish-flow" aria-labelledby="study-finish-title">
    <div className="sps-debrief-flow">
      <h1 id="study-finish-title" className="t-display">You showed up.<br />That counts.</h1>
      <p className="t-sub">{early ? 'The work still counts. ' : ''}A little record of the work you put in. And a clear place to pick up next time.</p>
      <form id={formId} className="sps-form" onSubmit={event => { event.preventDefault(); void submit(false); }}>
        <fieldset className="sps-fieldset" disabled={busy}>
          <legend id={`${id}-look-back`} className="t-heading sps-legend">A moment to look back</legend>
          <SelectionBar label="A moment to look back" size="md" className="sps-modes-bar" value={mode} onChange={value => onModeChange(value === 'full' ? 'full' : 'quick')}
            options={[
              { value: 'quick', label: <><span>Quick debrief</span><small>+{QUICK_DEBRIEF_POINTS} JP</small></> },
              { value: 'full', label: <><span>Write a reflection</span><small>+{FULL_REFLECTION_POINTS} JP</small></> },
            ]} />
          <p id="confidence-question" className="t-row sps-question">How does {subject} feel after this session?</p>
          <div ref={feelRef} className="sps-feelings" role="radiogroup" aria-labelledby="confidence-question">
            {CONFIDENCE.map((label, index) => <ChoiceTile key={label} chosen={confidence === label.toLowerCase()} label={label}
              ref={element => { feelings.refs.current[index] = element; }} tabIndex={feelings.tabIndexOf(index)} onKeyDown={event => feelings.onKeyDown(event, index)}
              onClick={() => setConfidence(label.toLowerCase())} />)}
          </div>
          {mode === 'full' && <div className="sps-field">
            <label htmlFor={`${id}-reflection`} className="t-row">What worked, and what will you try next time?</label>
            <textarea ref={reflectionRef} id={`${id}-reflection`} className="sps-area" value={reflection} onChange={event => setReflection(event.target.value)} minLength={15} maxLength={2000} rows={3} placeholder="A thought worth keeping…" aria-describedby="reflection-help" />
            <p id="reflection-help" className="t-meta">At least 15 characters. A sentence or two is enough.</p>
          </div>}
        </fieldset>
        {error && <p className="sps-error" role="alert">{error}</p>}
        <p className="t-meta sps-note">Saved sessions appear in your progress. Your debrief stays in your study journal.</p>
      </form>
    </div>
    <article className="study-receipt" aria-label="Your study receipt">
      <header><p className="study-crew-eyebrow">Nextstepuni / Your study receipt</p><CrewIllustration character={character} /><h2>A good little session.</h2><p>{date.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' })}</p></header>
      <dl><div><dt>Subject</dt><dd>{subject}</dd></div><div><dt>Time studied</dt><dd>{formatStudyTime(elapsedSeconds)}</dd></div><div><dt>Practice</dt><dd>{practice}</dd></div>{strategies.length > 0 && <div><dt>Strategies</dt><dd>{strategies.join(', ')}</dd></div>}{confidence && <div><dt>Feeling</dt><dd className="study-receipt-confidence">{confidence}</dd></div>}<div><dt>JP on saving</dt><dd>{basePoints}{extensionBonus > 0 && <> + {extensionBonus} kept going</>}{valid && <> + {bonus} debrief</>}</dd></div></dl>
      <div className="study-receipt-topics">{allocations.length ? <><p className="study-crew-eyebrow">Topic time</p><ul>{allocations.map(item => <li key={item.topicId}><span>{topicNames.get(item.topicId) ?? item.topicId}</span><strong>{formatStudyTime(item.seconds)}</strong></li>)}</ul><button type="button" className="crew-link" disabled={busy} onClick={() => setTopicTimeOpen(true)}>Review topic time</button></> : <p>Topics not recorded · subject time is saved.</p>}</div>
      <div className="study-receipt-next"><span>{mode === 'full' && reflection.trim() ? 'A note to take with you' : 'Next time'}</span><p>{mode === 'full' && reflection.trim() ? reflection.trim() : 'Pick up where you left off. One step at a time.'}</p></div>
      <footer><span>One step taken.</span><span>Your step.</span></footer><p className="study-receipt-signoff">Small steps, on the record.</p>
    </article>
    {topicTimeOpen && topicSelection && <TopicTimeCard selection={topicSelection} seconds={elapsedSeconds} allocations={allocations} onClose={() => setTopicTimeOpen(false)} onApply={value => { setAllocations(value); setTopicTimeOpen(false); }} />}
    </section>
    <PinnedFooter ruled className="sps-foot">
      {!missing && chosen && <p className="sps-ready">{chosen} · +{bonus} JP for your debrief</p>}
      <Button kind="main" size="lg" block arrow="forward" type="submit" form={formId} className="sps-main" missing={busy ? undefined : missing} aria-disabled={busy || undefined}>{busy ? 'Saving your session…' : 'Save session'}</Button>
      <TextButton tone="quiet" className="sps-quiet" aria-disabled={busy || undefined} onClick={() => void submit(true)}>Save without a debrief</TextButton>
    </PinnedFooter>
  </div></KobraScope>;
}
