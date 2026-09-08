/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Less guesswork. One display line after the examiner section. The word
 * "guesswork" erodes under the visitor's pointer or finger into orange dust
 * and, once mostly gone, re-forms (fx-i/GuessworkWord + guessworkField).
 * A small mono hint says what to do and goes once they have.
 */

import React, { useState } from 'react';
import { Container, Display } from '../primitives';
import { FONT, L, SPACE } from '../theme';
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
    <section id="guesswork" className={SPACE.sectionTight} aria-label={`${TEXT.before}${TEXT.word}${TEXT.after}`} style={{ scrollMarginTop: 70 }}>
      <Container>
        <Display size="hero" as="p" style={{ overflow: 'visible' }}>
          {TEXT.before}
          <GuessworkWord word={TEXT.word} onReady={() => setReady(true)} onTouch={() => setTouched(true)} />
          {TEXT.after}
        </Display>
        <div
          aria-hidden="true"
          className="mt-5"
          style={{ fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.16em', textTransform: 'uppercase', color: L.faint, lineHeight: 1, opacity: ready && !touched ? 1 : 0, transition: 'opacity 400ms ease', minHeight: 11 }}
        >
          {TEXT.hint}
        </div>
      </Container>
    </section>
  );
};

export default Guesswork;
