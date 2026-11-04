/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * History's printed extracts keep the paper's own breaks.
 *
 * An Ordinary Part A prints the SEC's instruction ("... Read it and answer the
 * questions which follow."), leaves a gap, and then prints the extract. The
 * stems used to arrive as one run of words, so the instruction ran straight
 * into the extract and the extract's paragraphs into each other. The reader
 * (hist_paper.paragraphs) now returns the breaks the page prints: a blank line
 * for the gap, a new line where the paper starts one. The words are untouched;
 * the cards under test are the SHIPPED cards, so a regeneration that moves a
 * break shows up here, and the cases the layout rules had to tell apart are
 * pinned by name.
 */
import { describe, expect, it, vi } from 'vitest';
import { render } from '@testing-library/react';
import { CARDS as HISTORY_ORDINARY } from '../components/MarkBank/cards/history/ordinary';
import { CARDS as HISTORY_HIGHER } from '../components/MarkBank/cards/history/higher';
import { CARDS as AGSCI_ORDINARY } from '../components/MarkBank/cards/agricultural-science/ordinary';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { stemWithListBreaks, stemWithPrintedBreaks } from '../components/MarkBank/stemText';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const stemOf = (id: string) => {
  const card = HISTORY_ORDINARY.find(c => c.id === id);
  if (!card?.stem) throw new Error(`no stem on ${id}`);
  return card.stem;
};
const lines = (id: string) => stemOf(id).split('\n\n')[1].split('\n');

describe('the printed breaks in a History stem', () => {
  it('sets the instruction apart from the extract, and each indented paragraph on its own line', () => {
    expect(stemOf('hist-2026-ol-lm-s2t1a-q1')).toBe(
      'In this edited extract, The Freeman’s Journal (August, 1850) describes the opening procession of the Synod of Thurles. Read it and answer the questions which follow.'
      + '\n\nEvery window in the neighbouring houses was crowded with spectators during the procession of bishops and priests.'
      + '\nThe large bell of the chapel and the chimes of the convent were heard at intervals.'
      + '\nDespite the immense crowds, so complete was the respectful silence that, even at a considerable distance, the organ of the chapel could be heard.',
    );
  });

  it('gives every Ordinary Part A stem one gap, after a finished instruction sentence', () => {
    const partA = HISTORY_ORDINARY.filter(c => /-s(?:2|3)t\d+a-q\d$|-xa-q\d$/.test(c.id) && c.stem);
    expect(partA.length).toBeGreaterThan(600);
    for (const card of partA) {
      const parts = card.stem!.split('\n\n');
      expect(parts, card.id).toHaveLength(2);
      expect(parts[0], card.id).toMatch(/[.?!:]$/);
      expect(card.stem, card.id).not.toMatch(/ \n|\n |\n{3}/);
    }
  });

  it('keeps a dated diary entry whole: its hanging indent is the rest of the entry', () => {
    expect(lines('hist-2025-ol-lm-s2t1a-q1')).toEqual([
      '03/02/1829: I have been appointed parish warden, Callan, Co. Kilkenny, in the Catholic Association, to collect the Catholic Rent.',
      '08/07/1829: Every window in town is full of candles to celebrate Daniel O’Connell’s victory in the Clare Election.',
      '28/09/1829: A drum calls O’Connell’s followers to march through Callan, wearing ribbons of green and other colours.',
    ]);
  });

  it('reads a diary’s times of day as the extract, never as question numbers', () => {
    // 2020 OL: "4.30 House filling quickly." once read as question 4, and "6.40 Parnell up." as a question 6.
    expect(lines('hist-2020-ol-lm-s2t2a-q1')).toEqual([
      '4.30 House filling quickly.',
      '4.45 The Prime Minister just arrived. Great cheering. House full, nearly.',
      '6.40 Parnell up. Very quiet and white. He spoke calmly and effectively. He says you must pass the Bill or you will have to coerce [use force against] us as you never did before.',
      'For: 311. Against: 341. A fearful row in the lobby.',
    ]);
    expect(HISTORY_ORDINARY.filter(c => c.id.startsWith('hist-2020-ol-lm-s2t2a-')).map(c => c.questionText)).toEqual([
      'For what occasion was the writer present?',
      'How was the Prime Minister greeted?',
      'Was the writer impressed by Parnell’s performance? Briefly explain your answer.',
      'After the vote was taken, what took place in the lobby?',
      'Why did the Home Rule Bill fail to pass in the House of Commons?',
    ]);
  });

  it('puts each bulleted item on a line, with its wrapped rest beside it', () => {
    expect(lines('hist-2023-ol-em-s2t4a-q1')).toEqual([
      '• No trader is permitted to block the street with a stall.',
      '• On Fishamble Street, only butchers with shops (kept clean and smart) are permitted – not those who trade on the street.',
      '• The sale of stockings, linen and woollen cloth is permitted in the Crane Market; but the sale of butter, cheese and bacon is not allowed.',
      '• No stalls are permitted in High Street – but those carrying goods for sale in their arms are allowed.',
    ]);
  });

  it('sets verse line by line, the longest line included', () => {
    expect(lines('hist-2025-ol-em-s2t5a-q1')).toEqual([
      'O ‘tis one year tomorrow my home I deserted',
      'And went to Ard Pádraig my hat done [decorated] with laces',
      'The Whiteboys were there tormenting the cattle',
      'Now I’m grieving and lonely in jail in Clonmel',
      'I’m condemned [to die] and won’t live beyond Friday.',
    ]);
  });

  it('runs a line the setter wrapped by hand in mid-sentence on, as one sentence', () => {
    expect(stemOf('hist-2023-ol-lm-s2t6a-q1')).toContain(
      'But with Mr. de Valera watching him [as President] from the Phoenix Park',
    );
    expect(stemOf('hist-2026-ol-lm-s3t2a-q1').split('\n\n')[0]).toBe(
      'In this edited extract, German Chancellor Bernhard von Bülow, in a speech to the Reichstag, 11 December 1899, explains the background to the naval policy of Wilhelm II. Read it and answer the questions which follow.',
    );
  });

  it('leaves the Higher stems, which print no extract, on one line', () => {
    for (const card of HISTORY_HIGHER) expect(card.stem ?? '', card.id).not.toContain('\n');
  });
});

describe('showing a stem', () => {
  it('keeps the breaks History prints, and only those', () => {
    expect(stemWithPrintedBreaks('  A.\n\n\nB \n C\n')).toBe('A.\n\nB\nC');
    // Every other subject: unchanged, a break before a bullet and a space for the rest.
    expect(stemWithListBreaks('A.\n\nB\n• C')).toBe('A. B\n• C');
  });

  // The session renders into a portal on document.body, not into its container.
  const stemParagraph = (opening: string) =>
    [...document.body.querySelectorAll('p')].find(p => p.textContent?.startsWith(opening));

  it('renders a History stem with its printed breaks', () => {
    const card = HISTORY_ORDINARY.find(c => c.id === 'hist-2026-ol-lm-s2t1a-q1')!;
    render(<SessionScreen cards={[card]} subjectLabel="History" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(stemParagraph('In this edited extract')?.textContent).toBe(card.stem);
  });

  it('renders another subject’s stem exactly as before', () => {
    const card = AGSCI_ORDINARY.find(c => c.id === 'agsci-2025-ol-q16b')!;
    expect(card.stem).toContain('\n\n');
    render(<SessionScreen cards={[card]} subjectLabel="Agricultural Science" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(stemParagraph('Winter months')?.textContent).toBe(stemWithListBreaks(card.stem!));
    expect(stemParagraph('Winter months')?.textContent).not.toContain('\n');
  });
});
