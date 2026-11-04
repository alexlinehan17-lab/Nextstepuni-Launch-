/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One Biology Mark Bank card in the real SessionScreen, for the browser check
 * (?id=<card id>, &dark=1 for the dark theme).
 */
import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import '../../../../index.css';
import SessionScreen from '../../../../components/MarkBank/SessionScreen';
import {CARDS as HIGHER} from '../../../../components/MarkBank/cards/biology/higher';
import {CARDS as ORDINARY} from '../../../../components/MarkBank/cards/biology/ordinary';

const CARDS = [...HIGHER, ...ORDINARY];
const params = new URLSearchParams(location.search);
function App() {
  const [id] = useState(params.get('id') ?? 'bio-2026-hl-q1-a');
  const card = CARDS.find(c => c.id === id)!;
  return <div style={{minHeight: '100vh'}}>
    <SessionScreen key={id} cards={[card]} subjectLabel="Biology" onGrade={() => {}} onFinish={() => {}} onExit={() => {}} />
  </div>;
}
if (params.get('dark')) document.documentElement.classList.add('dark');
createRoot(document.getElementById('root')!).render(<App/>);
