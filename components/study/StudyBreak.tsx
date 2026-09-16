import React, { useEffect, useState } from 'react';
import { ArrowUpRight } from 'lucide-react';
import CrewIllustration from '../CrewIllustration';
import { formatStudyTime } from './StudySessionFinish';
import './study-crew.css';

export default function StudyBreak({ subject, elapsedSeconds, onResume, onLeave }: { subject: string; elapsedSeconds: number; onResume: () => void; onLeave: () => void }) {
  const [breathing, setBreathing] = useState(false);
  const [inhale, setInhale] = useState(true);
  useEffect(() => {
    if (!breathing) return;
    const timer = setInterval(() => setInhale(value => !value), 4000);
    return () => clearInterval(timer);
  }, [breathing]);
  return <section className="study-break" aria-labelledby="study-break-title">
    <p className="study-crew-eyebrow">A little room to breathe</p>
    <div className={`study-break-art${breathing ? ' is-breathing' : ''}`}><CrewIllustration character="star-crew:snoozer" /></div>
    <h1 id="study-break-title">Even stars take a moment.</h1>
    <p>Look away. Stretch a little. Come back when you’re ready.</p>
    <div className="study-break-context"><strong>{subject}</strong><span>{formatStudyTime(elapsedSeconds)} studied · Timer paused</span></div>
    <button type="button" className="crew-primary" onClick={onResume} autoFocus>Back to study<ArrowUpRight size={21} aria-hidden="true" /></button>
    <button type="button" className="crew-link study-breathe-toggle" aria-pressed={breathing} onClick={() => { setBreathing(value => !value); setInhale(true); }}>{breathing ? 'Stop breathing guide' : 'Take a few slow breaths'}</button>
    <p className="study-breath-prompt" aria-live="off">{breathing ? inhale ? 'Breathe in, gently…' : 'Breathe out, slowly…' : 'Your place is right here.'}</p>
    <button type="button" className="crew-link study-break-leave" onClick={onLeave}>Finish for now</button>
  </section>;
}
