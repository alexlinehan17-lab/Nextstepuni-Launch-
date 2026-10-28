import React from 'react';
import { createRoot } from 'react-dom/client';
import SessionScreen from '../../../../../components/MarkBank/SessionScreen';
import { CARDS as HIGHER } from '../../../../../components/MarkBank/cards/chemistry/higher';
import { CARDS as ORDINARY } from '../../../../../components/MarkBank/cards/chemistry/ordinary';
import '../../../../../index.css';

/* One shipped Chemistry card in the real session screen, chosen by ?card=. */
const CARDS = [...HIGHER, ...ORDINARY];
const id = new URLSearchParams(location.search).get('card') ?? 'chem-2026-hl-q1-a-i';
const selected = CARDS.find(card => card.id === id)!;
createRoot(document.getElementById('root')!).render(
  <SessionScreen cards={[selected]} subjectLabel="Chemistry" onGrade={() => {}} onFinish={() => {}} onExit={() => {}} />);
