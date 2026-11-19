/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One shipped Physics card in the real session screen, chosen by ?card=, in the
 * light theme or, with ?theme=dark, the dark one. Used by browser-cases.mjs.
 */
import React from 'react';
import { createRoot } from 'react-dom/client';
import SessionScreen from '../../../../../components/MarkBank/SessionScreen';
import { CARDS as HIGHER } from '../../../../../components/MarkBank/cards/physics/higher';
import { CARDS as ORDINARY } from '../../../../../components/MarkBank/cards/physics/ordinary';
import '../../../../../index.css';

const CARDS = [...HIGHER, ...ORDINARY];
const params = new URLSearchParams(location.search);
const id = params.get('card') ?? 'phys-2026-hl-q2-i';
if (params.get('theme') === 'dark') document.documentElement.classList.add('dark');
const selected = CARDS.find(card => card.id === id)!;
createRoot(document.getElementById('root')!).render(
  <SessionScreen cards={[selected]} subjectLabel="Physics" onGrade={() => {}} onFinish={() => {}} onExit={() => {}} />);
