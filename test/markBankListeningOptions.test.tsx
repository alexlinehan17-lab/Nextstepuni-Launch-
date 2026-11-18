/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A listening question's printed options sit under it, one to a line, as the paper sets them (ListeningPromptOptions).
 */
import { render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CARDS as FOUNDATION } from '../components/MarkBank/cards/irish/foundation';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import SessionScreen, { listeningQuestionGroups } from '../components/MarkBank/SessionScreen';
import { listeningPromptParts } from '../components/MarkBank/ListeningPromptOptions';

const withOptions = FOUNDATION.filter(card => card.audioMaterial && /\n\n\S/.test(card.questionText));

describe('listening options on their own lines', () => {
  it('cuts every Foundation listening question with printed options into the question and its options', () => {
    expect(withOptions).toHaveLength(148);
    for (const card of withOptions) {
      const [question, block] = card.questionText.split(/\n\n/);
      const prompts = listeningQuestionGroups(card.questionText).flatMap(group => group.prompts);
      expect(prompts, card.id).toHaveLength(1);
      const { options } = listeningPromptParts(prompts[0].text);
      expect(options, card.id).toEqual(block.split('\n'));
      expect(prompts[0].text.startsWith(question.replace(/^\d+\.\s+(\([ab]\)\s+)?/, '')), card.id).toBe(true);
    }
  });

  it('leaves every other listening prompt as it was: no other prompt prints options after a blank line', () => {
    const others = [...HIGHER, ...ORDINARY, ...FOUNDATION.filter(card => !withOptions.includes(card))]
      .filter(card => card.audioMaterial);
    for (const card of others) for (const group of listeningQuestionGroups(card.questionText)) {
      for (const prompt of group.prompts) expect(listeningPromptParts(prompt.text).options, card.id).toEqual([]);
    }
  });

  it('renders the options as separate lines under the question', () => {
    const card = FOUNDATION.find(entry => entry.id === 'irish-2011-fl-a-1b')!;
    render(<SessionScreen cards={[card]} subjectLabel="Irish" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    const prompt = screen.getByTestId('mark-bank-listening-questions').querySelector('[data-listening-prompt]')!;
    const options = prompt.querySelector('[data-listening-options]')!;
    expect([...options.children].map(line => line.textContent)).toEqual(['Droichead Átha', 'Dún Dealgan', 'Faoin tuath']);
    expect(within(prompt as HTMLElement).getByText(/Cá háit a bhfuil Breandán ina chónaí faoi láthair\?/)).toBeInTheDocument();
  });
});
