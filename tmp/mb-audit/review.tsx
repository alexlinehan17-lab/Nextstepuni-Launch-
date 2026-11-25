import React from 'react';
import { createRoot } from 'react-dom/client';
import SessionScreen from '../../components/MarkBank/SessionScreen';
import { loadCards, SUBJECTS } from '../../components/MarkBank/deck';
import '../../index.css';

/* One shipped card in the real session screen: ?subject=&level=&card= */
const q = new URLSearchParams(location.search);
const LEVELS = ['higher', 'ordinary', 'foundation', 'common'] as const;
// Only a subject and level the bank really has may reach the deck loader: both come from the address bar.
const known = SUBJECTS.find(s => s.id === q.get('subject'));
const level = LEVELS.find(l => l === q.get('level'));
const id = q.get('card') ?? '';
const paper = q.get('paper') === '1';
const label = known?.title ?? 'Mark Bank';
if (!known || !level) document.body.textContent = 'UNKNOWN SUBJECT OR LEVEL';
else loadCards(known.id, level).then(cards => {
  const selected = cards.find(c => c.id === id);
  if (!selected) { document.body.textContent = 'CARD NOT FOUND'; return; }
  createRoot(document.getElementById('root')!).render(
    <SessionScreen paperLayout={paper} cards={[selected]} subjectLabel={label} onGrade={() => {}} onFinish={() => {}} onExit={() => {}} />);
});
