/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The heading for Ask the papers. The word
 * "guesswork" erodes under the visitor's pointer or finger into orange dust
 * and, once mostly gone, re-forms (fx-i/GuessworkWord + guessworkField).
 * A small mono hint says what to do and goes once they have.
 */

import React, { useState } from 'react';
import { Display } from '../primitives';
import { FONT, L } from '../theme';
import GuessworkWord from '../fx-i/GuessworkWord';
import '../fx-i/fx-i.css';

const TEXT = {
  before: 'Less ',
  word: 'guesswork',
  after: '.',
  hint: 'Rub the word out',
} as const;

const Guesswork: React.FC = () => {
  const [ready, setReady] = useState(false);
  const [touched, setTouched] = useState(false);
  return (
    <div id="guesswork" style={{ scrollMarginTop: 110 }}>
      <Display id="ask-heading" size="section" as="h2" style={{ fontSize: 'clamp(34px, 4vw, 48px)', overflow: 'visible' }}>
        {TEXT.before}
        <GuessworkWord word={TEXT.word} onReady={() => setReady(true)} onTouch={() => setTouched(true)} />
        {TEXT.after}
      </Display>
      {ready && <div
        aria-hidden="true"
        className="mt-4"
        style={{ fontFamily: FONT.mono, fontSize: 10, letterSpacing: '0.12em', textTransform: 'uppercase', color: L.faint, lineHeight: 1.4, opacity: touched ? 0 : 1, transition: 'opacity 400ms ease' }}
      >
        {TEXT.hint}
      </div>}
    </div>
  );
};

export default Guesswork;
