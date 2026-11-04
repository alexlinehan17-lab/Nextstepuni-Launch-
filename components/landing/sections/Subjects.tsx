import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, ArrowUpRight } from 'lucide-react';
import CrewIllustration from '../../CrewIllustration';
import catalogue from '../subjectShowcase.json';
import type { ShowcaseSubject } from '../subjectShowcaseSource';
import type { PaperCycle } from '../../../types/paperTrail';
import { Container, Eyebrow, SectionRule } from '../primitives';
import { APP_URL, SPACE } from '../theme';
import './subjects-crew.css';

const subjects = catalogue as ShowcaseSubject[];
const cycles: { id: PaperCycle; label: string }[] = [
  { id: 'lc', label: 'Leaving Certificate' }, { id: 'jc', label: 'Junior Cycle' }, { id: 'lca', label: 'Leaving Certificate Applied' },
];
const count = (value: number) => value ? value.toLocaleString('en-IE') : '—';
export const wrapSubjectIndex = (index: number, length: number) => ((index % length) + length) % length;

export default function Subjects() {
  const [cycle, setCycle] = useState<PaperCycle>('lc');
  const [selectedId, setSelectedId] = useState('music');
  const startPointer = useRef<{ x: number; y: number } | null>(null);
  const suppressClick = useRef(false);
  const wheelGate = useRef(0);
  const carousel = useRef<HTMLDivElement>(null);
  const available = useMemo(() => subjects.filter(subject => subject.cycle === cycle), [cycle]);
  const selectedIndex = Math.max(0, available.findIndex(subject => subject.id === selectedId));
  const selected = available[selectedIndex];
  const move = (delta: number) => setSelectedId(available[wrapSubjectIndex(selectedIndex + delta, available.length)].id);
  const selectCycle = (value: PaperCycle) => { setCycle(value); setSelectedId(subjects.find(s => s.cycle === value)!.id); };
  useEffect(() => {
    const element = carousel.current;
    if (!element) return;
    let travel = 0, lastWheel = 0;
    const onWheel = (event: WheelEvent) => {
      if (Math.abs(event.deltaX) <= Math.abs(event.deltaY)) return;
      event.preventDefault(); // Keep horizontal trackpad flicks inside the carousel.
      const now = Date.now();
      if (now - lastWheel > 180) travel = 0;
      lastWheel = now;
      if (now - wheelGate.current < 420) return;
      travel += event.deltaX;
      if (Math.abs(travel) < 35) return;
      const direction = travel > 0 ? 1 : -1;
      travel = 0; wheelGate.current = now;
      setSelectedId(current => available[wrapSubjectIndex(Math.max(0, available.findIndex(subject => subject.id === current)) + direction, available.length)].id);
    };
    element.addEventListener('wheel', onWheel, { passive: false });
    return () => element.removeEventListener('wheel', onWheel);
  }, [available]);
  const slots = [-3, -2, -1, 0, 1, 2, 3];
  const years = selected.firstYear === null ? '—' : selected.firstYear === selected.lastYear ? String(selected.firstYear) : `${selected.firstYear}–${selected.lastYear}`;
  return <section id="subjects" className={`${SPACE.section} landing-subject-crew`}>
    <SectionRule />
    <Container>
      <div className="lsc-heading"><Eyebrow className="justify-center">YOUR SUBJECTS. THEIR OWN PERSONALITY.</Eyebrow><h2>A crew for every curiosity.</h2><p>Find your subject. See what’s waiting inside.</p></div>
      <div className="lsc-tools"><label>Exam programme<select value={cycle} onChange={event => selectCycle(event.target.value as PaperCycle)}>{cycles.map(item => <option key={item.id} value={item.id}>{item.label}</option>)}</select></label><label>Jump to a subject<select value={selected.id} onChange={event => setSelectedId(event.target.value)}>{[...available].sort((a, b) => a.name.localeCompare(b.name)).map(subject => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select></label></div>
      <div ref={carousel} className="lsc-carousel" role="region" aria-roledescription="carousel" aria-label="Explore subjects" tabIndex={0}
        onKeyDown={event => { if (event.target !== event.currentTarget) return; if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1); } if (event.key === 'Home') { event.preventDefault(); setSelectedId(available[0].id); } if (event.key === 'End') { event.preventDefault(); setSelectedId(available.at(-1)!.id); } }}
        onPointerDown={event => { startPointer.current = { x: event.clientX, y: event.clientY }; suppressClick.current = false; }}
        onPointerMove={event => { const start = startPointer.current; if (start && Math.abs(event.clientX - start.x) > 42 && Math.abs(event.clientX - start.x) > Math.abs(event.clientY - start.y)) event.currentTarget.setPointerCapture?.(event.pointerId); }}
        onPointerCancel={() => { startPointer.current = null; }}
        onPointerUp={event => { const start = startPointer.current; startPointer.current = null; if (!start) return; const dx = event.clientX - start.x, dy = event.clientY - start.y; if (Math.abs(dx) > 42 && Math.abs(dx) > Math.abs(dy)) { suppressClick.current = true; move(dx < 0 ? 1 : -1); } }}>
        {slots.map(offset => { const subject = available[wrapSubjectIndex(selectedIndex + offset, available.length)]; const edge = Math.abs(offset) === 3; return <button key={subject.id} type="button" className={`lsc-card${edge ? ' lsc-peek' : ''}`} data-offset={offset} aria-label={`Explore ${subject.name}`} aria-pressed={offset === 0} tabIndex={edge ? -1 : 0}
          style={{ '--slot': offset, '--turn': `${offset * 5}deg`, '--drop': `${Math.abs(offset) * 10}px` } as React.CSSProperties}
          onKeyDown={event => { if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); event.currentTarget.parentElement?.focus(); move(event.key === 'ArrowLeft' ? -1 : 1); } }}
          onClick={() => { if (suppressClick.current) { suppressClick.current = false; return; } setSelectedId(subject.id); }}>
          <CrewIllustration subject={subject.artworkSubject} /><span>{subject.name}</span>
        </button>; })}
      </div>
      <div className="lsc-selection"><button type="button" onClick={() => move(-1)} aria-label="Previous subject"><ArrowLeft size={21} /></button><div aria-live="polite" aria-atomic="true"><h3>{selected.name}</h3><p>{selectedIndex + 1} / {available.length} subjects · Swipe or use the arrows</p></div><button type="button" onClick={() => move(1)} aria-label="Next subject"><ArrowRight size={21} /></button></div>
      <dl className="lsc-stats" aria-label={`${selected.name} resources`} key={selected.id}>
        <div><dd>{count(selected.markBankCards)}</dd><dt>Mark Bank cards</dt><p>{selected.markBankCards ? 'Practice from the marking schemes' : 'Not yet available for this subject'}</p></div>
        <div><dd>{count(selected.atlasQuestions)}</dd><dt>Topic Atlas questions</dt><p>{selected.atlasQuestions ? `Across ${selected.atlasTopics.toLocaleString('en-IE')} topic groups` : 'Not yet available for this subject'}</p></div>
        <div><dd>{count(selected.paperCount)}</dd><dt>Paper Trail PDFs</dt><p>{selected.paperCount ? 'Available levels and language editions' : 'No papers available yet'}</p></div>
        <div><dd>{years}</dd><dt>Exam years in the library</dt><p>{selected.firstYear ? 'Availability varies by year and level' : 'New material added as it becomes available'}</p></div>
      </dl>
      <div className="lsc-footer"><p>Counts reflect the current library. Topic Atlas questions and Mark Bank cards are different practice resources.</p><a href={APP_URL}>Find your next step <ArrowUpRight size={19} /></a></div>
    </Container>
  </section>;
}
