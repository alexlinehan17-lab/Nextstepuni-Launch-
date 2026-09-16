import React, { useRef, useState } from 'react';
import { ArrowUpRight } from 'lucide-react';
import CrewIllustration from '../CrewIllustration';
import { QUICK_DEBRIEF_POINTS, FULL_REFLECTION_POINTS } from '../ReflectionModal';
import './study-crew.css';

export function formatStudyTime(seconds: number) {
  const minutes = Math.floor(Math.max(0, seconds) / 60);
  const remainder = Math.floor(Math.max(0, seconds) % 60);
  return remainder ? `${minutes} min ${remainder} sec` : `${minutes} minute${minutes === 1 ? '' : 's'}`;
}

interface Props {
  subject: string; elapsedSeconds: number; plannedSeconds: number; practice: string;
  character?: string; strategies: string[]; basePoints: number; isSaving: boolean;
  mode: 'quick' | 'full'; onModeChange: (mode: 'quick' | 'full') => void;
  onSave: (reflection: string) => Promise<void>; onSkip: () => Promise<void>;
}

export default function StudySessionFinish({ subject, elapsedSeconds, plannedSeconds, practice, character, strategies, basePoints, isSaving, mode, onModeChange, onSave, onSkip }: Props) {
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
    try { await (skip ? onSkip() : onSave(mode === 'quick' ? confidence : `${confidence}|${reflection.trim()}`)); }
    catch { setError('Your session couldn’t be saved. Please try again. Your debrief is still here.'); }
    finally { inFlight.current = false; setSubmitting(false); }
  };
  return <section className="study-finish" aria-labelledby="study-finish-title">
    <div className="study-debrief">
      <p className="study-crew-eyebrow">{early ? 'Session ended early' : 'Session complete'}</p>
      <h1 id="study-finish-title">You showed up.<br />That counts.</h1>
      <p className="study-crew-intro">{early ? 'The work still counts. ' : ''}A little record of the work you put in. And a clear place to pick up next time.</p>
      <form onSubmit={event => { event.preventDefault(); void submit(false); }}>
        <fieldset disabled={busy}>
          <legend>A moment to look back</legend>
          <div className="study-debrief-modes"><button type="button" aria-pressed={mode === 'quick'} onClick={() => onModeChange('quick')}>Quick debrief <span>+{QUICK_DEBRIEF_POINTS} JP</span></button><button type="button" aria-pressed={mode === 'full'} onClick={() => onModeChange('full')}>Write a reflection <span>+{FULL_REFLECTION_POINTS} JP</span></button></div>
          <p id="confidence-question">How does {subject} feel after this session?</p>
          <div className="study-confidence" role="group" aria-labelledby="confidence-question">{['Lost', 'Shaky', 'Okay', 'Good', 'Confident'].map(label => <button type="button" key={label} aria-pressed={confidence === label.toLowerCase()} onClick={() => setConfidence(label.toLowerCase())}>{label}</button>)}</div>
          {mode === 'full' && <label className="study-reflection-label">What worked, and what will you try next time?<textarea value={reflection} onChange={event => setReflection(event.target.value)} minLength={15} maxLength={2000} rows={3} placeholder="A thought worth keeping…" aria-describedby="reflection-help" /><small id="reflection-help">At least 15 characters. A sentence or two is enough.</small></label>}
        </fieldset>
        {error && <p role="alert" className="study-save-error">{error}</p>}
        <button type="submit" className="crew-primary study-keep" disabled={busy || !valid}>{busy ? 'Saving your session…' : 'Keep this session'}<ArrowUpRight size={21} aria-hidden="true" /></button>
        <button type="button" className="crew-link study-skip" disabled={busy} onClick={() => void submit(true)}>Save without a debrief</button>
        <p className="study-save-note">Saved sessions appear in your progress. Your debrief stays in your study journal.</p>
      </form>
    </div>
    <article className="study-receipt" aria-label="Your study receipt">
      <header><p className="study-crew-eyebrow">Nextstepuni / Your study receipt</p><CrewIllustration character={character} /><h2>A good little session.</h2><p>{date.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' })}</p></header>
      <dl><div><dt>Subject</dt><dd>{subject}</dd></div><div><dt>Time studied</dt><dd>{formatStudyTime(elapsedSeconds)}</dd></div><div><dt>Practice</dt><dd>{practice}</dd></div>{strategies.length > 0 && <div><dt>Strategies</dt><dd>{strategies.join(', ')}</dd></div>}{confidence && <div><dt>Feeling</dt><dd className="study-receipt-confidence">{confidence}</dd></div>}<div><dt>JP on saving</dt><dd>{basePoints}{valid && <> + {bonus} debrief</>}</dd></div></dl>
      <div className="study-receipt-next"><span>{mode === 'full' && reflection.trim() ? 'A note to take with you' : 'Next time'}</span><p>{mode === 'full' && reflection.trim() ? reflection.trim() : 'Pick up where you left off. One step at a time.'}</p></div>
      <footer><span>One step taken.</span><span>Your step.</span></footer><p className="study-receipt-signoff">Small steps, on the record.</p>
    </article>
  </section>;
}
