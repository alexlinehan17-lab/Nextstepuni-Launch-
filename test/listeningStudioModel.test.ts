/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Listening Studio's sittings are read off Mark Bank's own cards.
 *
 * Nothing is authored for the Studio: components/ListeningStudio/model.ts places
 * every card that carries a recording into a sitting, a section and an extract
 * from fields the card already has, and puts the parts in printed order. These
 * tests pin that reading against real papers and hold every deck to it, so a
 * new sitting, or a subject carded later, cannot leave a recording card
 * unplaced or a subject with listenings missing from the Studio.
 */
import { describe, expect, it } from 'vitest';
import { builtDecks, loadCards } from '../components/MarkBank/deck';
import { CARDS as GERMAN_HIGHER } from '../components/MarkBank/cards/german/higher';
import { CARDS as IRISH_HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as MUSIC_HIGHER } from '../components/MarkBank/cards/music/higher';
import {
  LISTENING_SUBJECT_IDS, SEC_SUBJECT_CODES, hostedRecordingCount, listeningSittings, partLabel, type StudioSitting,
} from '../components/ListeningStudio/model';
import HOSTED_AUDIO from '../components/MarkBank/hostedAudio.json';

const sitting = (sittings: StudioSitting[], year: number, deferred = false) =>
  sittings.find(candidate => candidate.year === year && candidate.deferred === deferred) as StudioSitting;

describe('one paper becomes its questions, and a question its excerpts', () => {
  const music = listeningSittings(MUSIC_HIGHER);

  it('Music 2025 Higher is the six questions the paper numbers', () => {
    const paper = sitting(music, 2025);
    expect(paper.title).toBe('2025 Higher');
    expect(paper.sections.map(section => section.title)).toEqual([
      'Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6',
    ]);
    // Two sound files a year: Questions 1 to 4 on the first, 5 and 6 on the second.
    const files = paper.sections.map(section => new Set(section.cards.map(card => card.audioMaterial.secFileid)));
    expect(files.every(set => set.size === 1)).toBe(true);
    expect(new Set(files.map(set => [...set][0])).size).toBe(2);
  });

  it('Question 5 is three excerpts with their parts in printed order', () => {
    const question = sitting(music, 2025).sections[4];
    expect(question.marks).toBe(15);
    expect(question.extracts.map(extract => [extract.title, extract.cards.map(card => partLabel(card))])).toEqual([
      ['Excerpt 1', ['(a)', '(b)', '(c)']],
      ['Excerpt 2', ['(d)', '(e)']],
      ['Excerpt 3', ['(f)']],
    ]);
    expect(question.cards.map(card => card.id)).toEqual(
      ['a', 'b', 'c', 'd', 'e', 'f'].map(part => `mus-2025-hl-l-q5-a-${part}`),
    );
  });

  it('a question heard as one excerpt goes by the question\'s own name', () => {
    // 2024 Higher Question 2 is one excerpt; 2025 has none like it.
    const single = sitting(music, 2024).sections.find(section => section.extracts.length === 1);
    expect(single).toBeDefined();
    expect(single?.extracts[0].title).toBe(single?.title);
  });

  it('newest paper first, and a deferred sitting after its June paper', () => {
    const years = music.map(paper => paper.year);
    expect(years).toEqual([...years].sort((a, b) => b - a));
    expect(music.every(paper => paper.sections.length === 6)).toBe(true);
  });
});

describe('printed order is read from the reference, not from the deck', () => {
  it('Irish 2024 Higher runs Cuid A, B, C, and a hAon before a Dó', () => {
    const paper = sitting(listeningSittings(IRISH_HIGHER), 2024);
    expect(paper.sections.map(section => section.title)).toEqual(['Cuid A', 'Cuid B', 'Cuid C']);
    expect(paper.sections.map(section => section.extracts.map(extract => extract.title))).toEqual([
      ['Fógra a hAon', 'Fógra a Dó'],
      ['Comhrá a hAon', 'Comhrá a Dó'],
      ['Píosa a hAon', 'Píosa a Dó'],
    ]);
    // The deck files this sitting Cuid A, C, B.
    const deckOrder = IRISH_HIGHER.filter(card => card.year === 2024 && card.audioMaterial
      && !card.audioMaterial.canonicalUrl.includes('deferredexams')).map(card => card.id);
    expect(paper.sections.flatMap(section => section.cards.map(card => card.id))).not.toEqual(deckOrder);
    // Within a conversation, An Chéad Mhír comes before An Dara Mír.
    expect(paper.sections[1].extracts[0].cards.map(card => card.audioMaterial.label)).toEqual([
      'Cuid B · Comhrá a hAon · An Chéad Mhír', 'Cuid B · Comhrá a hAon · An Dara Mír',
    ]);
  });

  it('German Fourth Part is heard as its four items', () => {
    const paper = sitting(listeningSittings(GERMAN_HIGHER), 2024);
    expect(paper.sections.map(section => section.title)).toEqual(['First Part', 'Second Part', 'Third Part', 'Fourth Part']);
    expect(paper.sections[3].extracts.map(extract => extract.title)).toEqual([
      'Item 1', 'Item 2', 'Item 3', 'Item 4: Weather forecast',
    ]);
    // A part's number is kept where the section is not itself the question.
    expect(paper.sections[3].extracts[0].cards.map(card => partLabel(card))).toEqual(['1(i)', '1(ii)']);
    // One piece: the section's name, with the interview's printed title beside it.
    expect(paper.sections[0].extracts).toHaveLength(1);
    expect(paper.sections[0].extracts[0].title).toBe('First Part');
    expect(paper.sections[0].extracts[0].piece).toMatch(/^Interview with /);
  });
});

describe('every deck', () => {
  it('places each recording card once, in a subject the Studio lists', async () => {
    const withRecordings = new Set<string>();
    const problems: string[] = [];
    let sittings = 0;
    for (const deck of builtDecks()) {
      const cards = await loadCards(deck.subjectId, deck.level);
      const recorded = cards.filter(card => card.audioMaterial).map(card => card.id).sort();
      const papers = listeningSittings(cards);
      if (!recorded.length) {
        if (papers.length) problems.push(`${deck.label}: sittings without recording cards`);
        continue;
      }
      withRecordings.add(deck.subjectId);
      sittings += papers.length;
      const placed = papers.flatMap(paper => paper.sections.flatMap(section => section.extracts.flatMap(extract => extract.cards)));
      if (JSON.stringify(placed.map(card => card.id).sort()) !== JSON.stringify(recorded)) {
        problems.push(`${deck.label}: ${recorded.length} recording cards, ${placed.length} placed`);
      }
      // The front page counts a subject's hosted recordings by the SEC's subject code in the file id.
      const code = (SEC_SUBJECT_CODES as Record<string, string | undefined>)[deck.subjectId];
      for (const card of placed) {
        if (!code || !card.audioMaterial.secFileid.startsWith(`LC${code}`)) {
          problems.push(`${card.id}: file id ${card.audioMaterial.secFileid} does not carry the subject code LC${code}`);
        }
      }
      for (const paper of papers) {
        if (!paper.sections.length) problems.push(`${paper.key}: no sections`);
        if (paper.recordings.total < 1 || paper.recordings.held > paper.recordings.total
          || paper.playsInApp !== (paper.recordings.held === paper.recordings.total)) {
          problems.push(`${paper.key}: recordings ${paper.recordings.held} of ${paper.recordings.total}`);
        }
        for (const section of paper.sections) {
          if (!section.title || !section.extracts.length) problems.push(`${section.key}: empty section`);
          if (section.cards.length !== section.extracts.reduce((count, extract) => count + extract.cards.length, 0)) {
            problems.push(`${section.key}: its cards are not its extracts' cards`);
          }
          for (const extract of section.extracts) {
            if (!extract.title || !extract.cards.length) problems.push(`${extract.key}: empty extract`);
            // One extract is heard on one recording: the sitting plays a single file for it.
            if (new Set(extract.cards.map(card => card.audioMaterial.canonicalUrl)).size !== 1) {
              problems.push(`${extract.key}: more than one recording`);
            }
          }
        }
      }
    }
    expect(problems).toEqual([]);
    // A deck with recording cards whose subject is not listed has no way into
    // the Studio: add the subject to LISTENING_SUBJECT_IDS (and give it a
    // grouping rule if the general one does not suit its paper).
    expect([...withRecordings].sort()).toEqual([...LISTENING_SUBJECT_IDS].sort());
    expect(sittings).toBeGreaterThanOrEqual(297);
    // Every hosted recording is counted under exactly one subject.
    const audio = (HOSTED_AUDIO as string[]).filter(path => path.startsWith('audio/'));
    expect(LISTENING_SUBJECT_IDS.reduce((sum, id) => sum + hostedRecordingCount(id), 0)).toBe(audio.length);
    expect(hostedRecordingCount('french')).toBeGreaterThanOrEqual(17);
    expect(hostedRecordingCount('biology')).toBe(0);
  }, 240_000);
});
