/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The 2010 Foundation listening paper has no published recording (its ledger records the audio as 'unavailable'): its
 * 22 cards, and only those, say so in one plain line above the source reader.
 */
import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CARDS as FOUNDATION } from '../components/MarkBank/cards/irish/foundation';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { RECORDING_UNPUBLISHED } from '../components/MarkBank/SourceMaterialReader';

const flagged = (cards: typeof FOUNDATION) => cards.filter(card => card.sourceMaterial?.recordingUnpublished);
const renderCard = (id: string) => render(<SessionScreen cards={[FOUNDATION.find(card => card.id === id)!]}
  subjectLabel="Irish" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);

describe('the 2010 Foundation listening note', () => {
  it('is the approved wording', () => {
    expect(RECORDING_UNPUBLISHED).toBe('The SEC has not published the recording for this paper. The question and the scheme’s answer are shown as printed.');
  });

  it('is set on the 22 cards of the 2010 Foundation aural paper and on no other card', () => {
    expect(flagged(FOUNDATION).map(card => card.id).sort()).toEqual(
      FOUNDATION.filter(card => card.year === 2010 && card.paperFileid === 'LC001BLPA00IV').map(card => card.id).sort());
    expect(flagged(FOUNDATION)).toHaveLength(22);
    expect(flagged(FOUNDATION).every(card => !card.audioMaterial)).toBe(true);
    expect(flagged([...HIGHER, ...ORDINARY] as typeof FOUNDATION)).toEqual([]);
  });

  it('renders as one plain line above the reader on a 2010 card, and not on a 2011 card with its recording', () => {
    const { unmount } = renderCard('irish-2010-fl-a-1b');
    expect(screen.getByTestId('mb-recording-unpublished')).toHaveTextContent(RECORDING_UNPUBLISHED);
    expect(screen.getByTestId('mb-recording-unpublished').tagName).toBe('P');
    unmount();
    renderCard('irish-2011-fl-a-1b');
    expect(screen.queryByTestId('mb-recording-unpublished')).not.toBeInTheDocument();
  });
});
