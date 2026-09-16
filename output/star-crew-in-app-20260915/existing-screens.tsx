import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import HomeNextStep from '../../components/HomeNextStep';
import StudySessionSetup from '../../components/study/StudySessionSetup';
import type { StudyBlock, StudentSubject } from '../../components/subjectData';
import type { TimetableBlockContext } from '../../components/study/StudySessionView';
import '../../index.css';
import './existing-screens.css';

interface Artwork {
  id: string;
  name: string;
  file: string;
  frame: { width: number; left: number; top: number };
}
interface Context {
  selected: string[];
  subject: string;
}
const catalogue: Artwork[] = await fetch('../star-crew-subjects-20260915/gallery.json').then(response => response.json());
const byId = new Map(catalogue.map(item => [item.id, item]));
const initial = ['english', 'irish', 'mathematics', 'ancient-greek', 'music', 'biology', 'history'];
const screen = new URLSearchParams(location.search).get('screen') === 'home' ? 'home' : 'study';
const send = (message: Record<string, unknown>) => parent.postMessage(message, location.origin);

/** Preview-only decoration of existing icon slots; product components are unmodified. */
function placeArtwork(slot: HTMLElement, artwork: Artwork, size: number) {
  slot.classList.add('existing-subject-avatar');
  slot.style.setProperty('--crew-size', `${size}px`);
  slot.dataset.crewSubject = artwork.id;
  slot.setAttribute('aria-hidden', 'true');
  const image = document.createElement('img');
  image.src = new URL(`../star-crew-subjects-20260915/${artwork.file}`, import.meta.url).href;
  image.alt = '';
  image.style.cssText = `width:${artwork.frame.width}%;height:${artwork.frame.width}%;left:${artwork.frame.left}%;top:${artwork.frame.top}%;`;
  slot.replaceChildren(image);
}

function ExistingScreens() {
  const [context, setContext] = useState<Context>({ selected: initial, subject: 'ancient-greek' });
  const [selectedSubject, setSelectedSubject] = useState('Ancient Greek');
  const [selectedType, setSelectedType] = useState<StudyBlock['sessionType']>('revision');
  const [minutes, setMinutes] = useState(25);
  const [colourful, setColourful] = useState(false);
  const root = useRef<HTMLDivElement>(null);
  const artworks = context.selected.map(id => byId.get(id)).filter((item): item is Artwork => Boolean(item));
  const subjectProfile: StudentSubject[] = artworks.map(item => ({ subjectName: item.name, level: 'higher' }));
  const ordered = ['irish', 'music', ...context.selected].filter((id, index, all) => context.selected.includes(id) && all.indexOf(id) === index);
  const blocks: StudyBlock[] = ordered.slice(0, 3).map((id, index) => ({
    subjectName: byId.get(id)!.name,
    sessionType: index === 0 ? 'revision' : 'practice',
    durationMinutes: index === 0 ? 25 : 20,
  }));
  const timetable: TimetableBlockContext[] = blocks.map((block, index) => ({ subject: block.subjectName, sessionType: block.sessionType, durationMinutes: block.durationMinutes, dateKey: '2026-09-15', blockId: `preview-${index}` }));

  useEffect(() => {
    const receive = (event: MessageEvent) => {
      if (event.origin !== location.origin || event.source !== parent || event.data?.type !== 'crew-context') return;
      const selected = Array.isArray(event.data.selected) ? event.data.selected.filter((id: unknown): id is string => typeof id === 'string' && byId.has(id)) : initial;
      const subject = selected.includes(event.data.subject) ? event.data.subject : selected[0];
      setContext({ selected, subject });
      setSelectedSubject(byId.get(subject)?.name || '');
    };
    window.addEventListener('message', receive);
    send({ type: 'crew-ready' });
    return () => window.removeEventListener('message', receive);
  }, []);

  useLayoutEffect(() => {
    const content = root.current;
    if (!content) return;
    if (screen === 'home') {
      content.querySelectorAll<HTMLElement>('.home-plan-row').forEach(row => {
        const label = row.querySelector('.home-plan-copy strong')?.textContent;
        const artwork = artworks.find(item => item.name === label);
        const slot = row.querySelector<HTMLElement>('.home-subject-code');
        if (slot && artwork) placeArtwork(slot, artwork, 44);
      });
    } else {
      content.querySelectorAll<HTMLElement>('.ss-subjects button').forEach(button => {
        const label = button.querySelector(':scope > span')?.textContent;
        const artwork = artworks.find(item => item.name === label);
        const slot = button.querySelector<HTMLElement>(':scope > i');
        if (slot && artwork) placeArtwork(slot, artwork, 64);
      });
      content.querySelectorAll<HTMLElement>('.ss-timetable button').forEach(button => {
        const artwork = artworks.find(item => item.name === button.querySelector('strong')?.textContent);
        const slot = button.querySelector<HTMLElement>(':scope > i');
        if (slot && artwork) placeArtwork(slot, artwork, 36);
      });
    }
    const measure = () => send({ type: 'crew-height', height: Math.ceil(content.getBoundingClientRect().height) });
    const observer = new ResizeObserver(measure);
    observer.observe(content);
    measure();
    return () => observer.disconnect();
  }, [context, selectedSubject, selectedType, minutes, colourful]);

  const navigateToSubject = (subjectName: string) => {
    const artwork = artworks.find(item => item.name === subjectName);
    if (artwork) send({ type: 'crew-open-subject', subject: artwork.id });
  };
  const existingAction = (action: string) => send({ type: 'crew-existing-action', action });

  return <div ref={root} className={`existing-screen existing-screen-${screen}`}>
    {screen === 'home' ? <div className="existing-home-section">
      <HomeNextStep blocks={blocks} completions={[]} hasProfile={artworks.length > 0} onStudy={() => navigateToSubject(blocks[0]?.subjectName)} onPlannedStudy={block => navigateToSubject(block.subjectName)} onPlan={() => existingAction('The existing plan opens from this control.')} onProgress={() => existingAction('The existing progress screen opens from this control.')} />
    </div> : <StudySessionSetup
      subjects={subjectProfile}
      selectedSubject={selectedSubject}
      selectedType={selectedType}
      selectedMinutes={minutes}
      onSubject={setSelectedSubject}
      onType={setSelectedType}
      onMinutes={setMinutes}
      todayBlocks={timetable}
      onBlock={block => { setSelectedSubject(block.subject); setSelectedType(block.sessionType); setMinutes(block.durationMinutes); }}
      sessionCount={0}
      todayMinutes={0}
      reflectionCount={0}
      onReflections={() => existingAction('The existing reflections screen opens from this control.')}
      onBack={() => send({ type: 'crew-go-home' })}
      onSetUpProfile={() => send({ type: 'crew-go-subjects' })}
      onStart={() => existingAction('The existing study timer follows this step. This preview is for the subject cards.')}
      canStart={Boolean(selectedSubject && selectedType && minutes >= 5)}
      startHint={selectedSubject ? null : 'Choose a subject to begin.'}
      colourfulTimer={colourful}
      onColourfulTimerChange={setColourful}
    />}
  </div>;
}

createRoot(document.getElementById('existingRoot')!).render(<ExistingScreens />);
