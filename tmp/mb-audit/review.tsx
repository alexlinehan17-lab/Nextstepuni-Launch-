import React from 'react';
import { createRoot } from 'react-dom/client';
import SessionScreen from '../../components/MarkBank/SessionScreen';
import { loadCards, SUBJECTS } from '../../components/MarkBank/deck';
import '../../index.css';

/* One shipped card in the real session screen: ?subject=&level=&card= */
const q = new URLSearchParams(location.search);
const subject = q.get('subject')!, level = q.get('level') as any, id = q.get('card')!;
const paper = q.get('paper') === '1';
const label = (SUBJECTS as readonly any[]).find(s => s.id === subject)?.title ?? subject;
loadCards(subject, level).then(cards => {
  const selected = cards.find(c => c.id === id);
  if (!selected) { document.body.textContent = 'CARD NOT FOUND'; return; }
  createRoot(document.getElementById('root')!).render(
    <SessionScreen paperLayout={paper} cards={[selected]} subjectLabel={label} onGrade={() => {}} onFinish={() => {}} onExit={() => {}} />);
});
