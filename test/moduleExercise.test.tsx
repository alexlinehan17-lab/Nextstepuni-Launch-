/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 5b of the design build: the pieces an exercise in a module is made of (boards c-read-flow,
 * c-read-choices, c-read-write). An answer you choose has the right role and aria-checked, a chosen
 * one carries the module's own words for it on an ink line with a green tick, arrow keys move within
 * a group (and choose, in a one-of group), the count is read from the answers; an answer line is ink;
 * a card you press turns over and back; a written answer is a labelled field.
 */
import React, { useState } from 'react';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, test, vi } from 'vitest';
import { ChoiceTile } from '@/components/ui/Choice';
import { AreaField } from '@/components/ui/Field';
import { AnswerGroup, AnswerLine, ExercisePart, ExerciseSheet, RevealCard } from '@/components/learning/Exercise';

afterEach(cleanup);

const REASONS = [
  { text: "I didn't use the right study method.", control: true },
  { text: "I'm just naturally bad at this subject.", control: false },
  { text: 'The test was unfairly hard.', control: false },
];

/** A module's own state, as AttributionSorter keeps it: a map from the answer to chosen. */
function Several() {
  const [choice, setChoice] = useState<Record<string, boolean>>({});
  return (
    <ExerciseSheet title="Control Panel" sub="Scenario: You fail a test.">
      <AnswerGroup kind="several" count>
        {REASONS.map(r => (
          <ChoiceTile key={r.text} kind="several" chosen={!!choice[r.text]} label={r.text}
            note={choice[r.text] ? (r.control ? '(CONTROLLABLE)' : '(UNCONTROLLABLE)') : undefined}
            noteTone={r.control ? 'ok' : 'plain'}
            onClick={() => setChoice({ ...choice, [r.text]: !choice[r.text] })} />
        ))}
      </AnswerGroup>
    </ExerciseSheet>
  );
}

function One({ onPick, chooseOnArrow }: { onPick: (i: number) => void; chooseOnArrow?: boolean }) {
  const [at, setAt] = useState<number | null>(null);
  return (
    <AnswerGroup kind="one" legend="When I fail at something..." chooseOnArrow={chooseOnArrow}>
      {['A) I feel like I\'m a failure.', 'B) I feel like I need to try a new strategy.'].map((t, i) => (
        <ChoiceTile key={t} chosen={at === i} label={t} onClick={() => { setAt(i); onPick(i); }} />
      ))}
    </AnswerGroup>
  );
}

describe('an answer you choose', () => {
  test('any-of: checkboxes named by the exercise, a count, and the answer line under a chosen answer', () => {
    render(<Several />);
    const group = screen.getByRole('group', { name: 'Control Panel' });
    const boxes = screen.getAllByRole('checkbox');
    expect(boxes).toHaveLength(3);
    expect(group).toContainElement(boxes[0]);
    expect(screen.getByText('0 of 3 chosen')).toBeInTheDocument();
    fireEvent.click(boxes[0]);
    fireEvent.click(boxes[2]);
    expect(boxes[0]).toHaveAttribute('aria-checked', 'true');
    expect(boxes[1]).toHaveAttribute('aria-checked', 'false');
    expect(screen.getByText('2 of 3 chosen')).toBeInTheDocument();
    // the module's own words, unchanged, on the line under the chosen answer
    const ok = screen.getByText('(CONTROLLABLE)').closest('.ui-choice-note')!;
    expect(ok).toHaveClass('ui-choice-note--ok');
    expect(ok.querySelector('svg.ui-tick')).not.toBeNull();
    const plain = screen.getByText('(UNCONTROLLABLE)').closest('.ui-choice-note')!;
    expect(plain).not.toHaveClass('ui-choice-note--ok');
    expect(plain.querySelector('svg.ui-tick')).toBeNull();
    // the mark is the square one: pick several
    expect(boxes[0].querySelector('.ui-mark--square.ui-mark--on')).not.toBeNull();
  });

  test('any-of: arrow keys move between the answers without choosing them', () => {
    render(<Several />);
    const boxes = screen.getAllByRole('checkbox');
    boxes[0].focus();
    fireEvent.keyDown(boxes[0], { key: 'ArrowDown' });
    expect(boxes[1]).toHaveFocus();
    fireEvent.keyDown(boxes[1], { key: 'End' });
    expect(boxes[2]).toHaveFocus();
    fireEvent.keyDown(boxes[2], { key: 'ArrowDown' });
    expect(boxes[0]).toHaveFocus();
    expect(boxes.every(b => b.getAttribute('aria-checked') === 'false')).toBe(true);
  });

  test('one-of: a radio group named by its question; arrow keys move and choose, as radios do', () => {
    const onPick = vi.fn();
    render(<One onPick={onPick} />);
    const group = screen.getByRole('radiogroup', { name: 'When I fail at something...' });
    const radios = screen.getAllByRole('radio');
    expect(group).toContainElement(radios[1]);
    fireEvent.click(radios[0]);
    expect(radios[0]).toHaveAttribute('aria-checked', 'true');
    fireEvent.keyDown(radios[0], { key: 'ArrowRight' });
    expect(radios[1]).toHaveFocus();
    expect(radios[1]).toHaveAttribute('aria-checked', 'true');
    expect(onPick).toHaveBeenLastCalledWith(1);
    expect(radios[1].querySelector('.ui-mark--on:not(.ui-mark--square)')).not.toBeNull();
  });

  test('one-of where choosing locks the answer in: arrow keys only move', () => {
    const onPick = vi.fn();
    render(<One onPick={onPick} chooseOnArrow={false} />);
    const radios = screen.getAllByRole('radio');
    radios[0].focus();
    fireEvent.keyDown(radios[0], { key: 'ArrowDown' });
    expect(radios[1]).toHaveFocus();
    expect(onPick).not.toHaveBeenCalled();
  });

  test('every answer is a 44px target or more: the tile is at least 56 tall, inside a module too', () => {
    const css = readFileSync(resolve(__dirname, '..', 'components/ui/parts.css'), 'utf8');
    expect(css).toMatch(/\.ui-choice \{[^}]*min-height: 56px/);
    const ex = readFileSync(resolve(__dirname, '..', 'components/learning/exercise.css'), 'utf8');
    expect(ex).toMatch(/\.nsu-module-reader \.ui-part\.ui-choice \{ min-height: 56px; \}/);
  });
});

describe('the answer line', () => {
  test('ink words with a green tick: the words carry no green, by class and by stylesheet', () => {
    render(<AnswerLine><b>Reframe complete.</b> You've opened up the possibility of future growth.</AnswerLine>);
    const words = screen.getByText(/opened up the possibility/);
    expect(words).toHaveClass('ex-line-words');
    const line = words.closest('p')!;
    expect(line).toHaveClass('ex-line', 'ex-line--ok');
    expect(line.querySelector('svg.ui-tick')).not.toBeNull();
    const ex = readFileSync(resolve(__dirname, '..', 'components/learning/exercise.css'), 'utf8');
    const parts = readFileSync(resolve(__dirname, '..', 'components/ui/parts.css'), 'utf8');
    expect(ex).toMatch(/\.ex-line \{[^}]*color: var\(--ink-primary\)/);
    expect(parts).toMatch(/\.ui-choice-note--ok \{ color: var\(--ink-primary\); \}/);
    expect(parts).toMatch(/\.ui-tick \{[^}]*stroke: var\(--success-hex\)/);
    // no rule in the exercise pieces paints words green or fills an answer with a tint
    expect(ex + parts).not.toMatch(/success-tint|module-success|accent-tint|danger-tint\)|--nsu-orange/);
  });

  test('a note line has no tick', () => {
    render(<AnswerLine tone="note">Result: You're leaning towards Growth.</AnswerLine>);
    const line = screen.getByText(/leaning towards Growth/).closest('p')!;
    expect(line).not.toHaveClass('ex-line--ok');
    expect(line.querySelector('svg')).toBeNull();
  });
});

describe('a card you press to turn it over', () => {
  function Card({ keepBefore, toggles }: { keepBefore?: boolean; toggles?: boolean }) {
    const [on, setOn] = useState(false);
    return <RevealCard revealed={on} onPress={() => setOn(!on)} keepBefore={keepBefore} toggles={toggles}
      before={'"I\'m just naturally bad at Maths."'} after={'"I haven\'t found an effective way to learn Maths yet."'}
      hint="Tap to reframe" done="Reframed" />;
  }
  test('turns over and back; the old words stay, struck through, beside the new ones; the state is said in words', () => {
    render(<Card />);
    const card = screen.getByRole('button', { pressed: false });
    expect(card).toHaveTextContent('Tap to reframe');
    fireEvent.click(card);
    expect(card).toHaveAttribute('aria-pressed', 'true');
    expect(card).toHaveTextContent('"I\'m just naturally bad at Maths."');
    expect(card).toHaveTextContent('"I haven\'t found an effective way to learn Maths yet."');
    expect(card).toHaveTextContent('Reframed');
    expect(card).not.toHaveTextContent('Tap to reframe');
    expect(card.querySelector('.ex-reveal-state--done svg.ui-tick')).not.toBeNull();
    expect(card.querySelector('.ex-reveal-turn')).not.toBeNull();
    fireEvent.click(card);
    expect(card).toHaveAttribute('aria-pressed', 'false');
  });
  test('a card that turns once can hide its first words and has no turn-back mark', () => {
    render(<Card keepBefore={false} toggles={false} />);
    const card = screen.getByRole('button');
    fireEvent.click(card);
    expect(card).not.toHaveTextContent('naturally bad');
    expect(card.querySelector('.ex-reveal-turn')).toBeNull();
  });
});

describe('the sheet and an answer you write', () => {
  test('the sheet carries its label, title and what to do; a second exercise sits on the same sheet', () => {
    render(
      <ExerciseSheet label="Growth Mindset Activity" title={'The "Yet" Reframe Challenge'} sub="Upgrade this fixed thought.">
        <ExercisePart title="Control Panel"><p>Second</p></ExercisePart>
      </ExerciseSheet>,
    );
    expect(screen.getByRole('region', { name: 'The "Yet" Reframe Challenge' })).toHaveClass('ex-sheet');
    expect(screen.getByText('Growth Mindset Activity')).toHaveClass('ex-label');
    expect(screen.getByRole('heading', { level: 4, name: 'Control Panel' }).closest('.ex-part')).not.toBeNull();
  });
  test('a written answer: a labelled field that keeps the module in charge of its value', () => {
    function Write() {
      const [v, setV] = useState('');
      const [saved, setSaved] = useState('');
      return <>
        <AreaField label="Your Reframe" value={v} onChange={e => setV(e.target.value)} onBlur={() => setSaved(v)} placeholder="Rewrite this using the word 'yet'..." />
        {v.toLowerCase().includes('yet') ? <AnswerLine><b>Reframe complete.</b> You've opened up the possibility of future growth.</AnswerLine> : null}
        <output>{saved}</output>
      </>;
    }
    render(<Write />);
    const field = screen.getByRole('textbox', { name: 'Your Reframe' });
    expect(field).toHaveClass('ui-field-input--area');
    fireEvent.change(field, { target: { value: "I'm not a maths person yet." } });
    expect(screen.getByText('Reframe complete.')).toBeInTheDocument();
    fireEvent.blur(field);
    expect(screen.getByRole('status')).toHaveTextContent("I'm not a maths person yet.");
  });
});
