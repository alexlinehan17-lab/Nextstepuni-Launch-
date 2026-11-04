/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The debrief after a session, beside the study receipt. The debrief is a
 * Kobra paper card (approved review, 25 Oct 2026): Tabs for the mode, the
 * confidence scale as hairline options with an ink ring when chosen, the
 * runtime's Textarea and Buttons (study-post-session.css). The receipt is
 * unchanged, markup and study-crew.css rules alike (Alex, 25 Oct: "this is
 * really cool and we can't lose it").
 */
import React, { useId, useRef, useState } from 'react';
import { ArrowUpRight } from 'lucide-react';
import KobraScope, { Alert, AlertDescription, Button, Tabs, TabsList, TabsTrigger, Textarea } from '../approved-ui-runtime';
import CrewIllustration from '../CrewIllustration';
import { QUICK_DEBRIEF_POINTS, FULL_REFLECTION_POINTS } from '../ReflectionModal';
import type { StudyTopicAllocation, StudyTopicSelection } from '../../types/studyTopics';
import { equalTopicAllocations } from '../../services/studyTopicHistory';
import { CURRICULUM_SPECIFICATIONS } from '../../curriculumRegistry';
import TopicTimeCard from './TopicTimeCard';
import './study-crew.css';
import './study-post-session.css';

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
  return <KobraScope className="nsu-post-session"><div className="sps-page"><section className="sps-finish" aria-labelledby="study-finish-title">
    <div className="sps-card sps-debrief nsu-paper-card">
      <p className="sps-kicker">{early ? 'Session ended early' : 'Session complete'}</p>
      <h1 id="study-finish-title" className="sps-title">You showed up.<br />That counts.</h1>
      <p className="sps-lede">{early ? 'The work still counts. ' : ''}A little record of the work you put in. And a clear place to pick up next time.</p>
      <form className="sps-form" onSubmit={event => { event.preventDefault(); void submit(false); }}>
        <fieldset className="sps-fieldset" disabled={busy}>
          <legend id={`${id}-look-back`} className="sps-legend">A moment to look back</legend>
          <Tabs className="sps-modes" value={mode} onValueChange={value => onModeChange(value === 'full' ? 'full' : 'quick')}>
            <TabsList aria-labelledby={`${id}-look-back`}>
              <TabsTrigger value="quick">Quick debrief <small>+{QUICK_DEBRIEF_POINTS} JP</small></TabsTrigger>
              <TabsTrigger value="full">Write a reflection <small>+{FULL_REFLECTION_POINTS} JP</small></TabsTrigger>
            </TabsList>
          </Tabs>
          <p id="confidence-question" className="sps-question">How does {subject} feel after this session?</p>
          <div className="sps-feel" role="group" aria-labelledby="confidence-question">
            {CONFIDENCE.map(label => <button type="button" key={label} className="sps-feel-option" aria-pressed={confidence === label.toLowerCase()} onClick={() => setConfidence(label.toLowerCase())}><span className="sps-feel-mark" aria-hidden="true" />{label}</button>)}
          </div>
          {mode === 'full' && <div className="sps-field">
            <label htmlFor={`${id}-reflection`}>What worked, and what will you try next time?</label>
            <Textarea id={`${id}-reflection`} className="sps-textarea" value={reflection} onChange={event => setReflection(event.target.value)} minLength={15} maxLength={2000} rows={3} placeholder="A thought worth keeping…" aria-describedby="reflection-help" />
            <p id="reflection-help" className="sps-help">At least 15 characters. A sentence or two is enough.</p>
          </div>}
        </fieldset>
        {error && <Alert variant="error" className="sps-alert"><AlertDescription>{error}</AlertDescription></Alert>}
        <div className="sps-actions">
          <Button type="submit" className="sps-primary" disabled={busy || !valid}>{busy ? 'Saving your session…' : 'Save session'}<ArrowUpRight aria-hidden="true" /></Button>
          <Button type="button" variant="ghost" className="sps-quiet" disabled={busy} onClick={() => void submit(true)}>Save without a debrief</Button>
          <p className="sps-note">Saved sessions appear in your progress. Your debrief stays in your study journal.</p>
        </div>
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
  </section></div></KobraScope>;
}
