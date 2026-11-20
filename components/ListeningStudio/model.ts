/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How Mark Bank's listening cards become Listening Studio sittings.
 *
 * Nothing is authored for the Studio. Every card that carries a recording
 * (`audioMaterial`) is placed by fields it already has:
 *
 *   sitting   one paper: its year, its level, and June or the deferred sitting
 *   section   what the paper itself numbers: Question 5, Section B, Cuid A,
 *             Erster Teil; a student sits one section at a time
 *   extract   what is heard as one piece inside a section: Excerpt 2,
 *             Fógra a hAon, Dialogue 1, Item 3; one extract is on the sheet
 *             at a time, with all of its questions in view
 *
 * The rules were read off all 6,755 recording cards on 20 Nov 2026 (ten
 * subjects, 297 sittings, no card unplaced). A subject carded later falls to
 * the general rule (its `section`, one extract a section) until it is given its
 * own; test/listeningStudioModel.test.ts fails if a deck has recording cards
 * and its subject is missing from LISTENING_SUBJECT_IDS, so that is a decision
 * someone makes, never something that happens silently.
 *
 * Cards are put in printed order by reading `questionRef`, not by deck order:
 * eighteen Irish sittings are filed Cuid A, C, B, and a few Japanese, Italian
 * and Russian cards sit out of place in their decks.
 */

import type { CardAudioMaterial, MarkBankLevel, SecCard } from '../../types/markBank';
import { MARK_BANK_LEVEL_LABELS } from '../../types/markBank';
import { hostedAudioPath } from '../MarkBank/audioStorage';

/** Subjects with recording cards, in the order the Studio offers them. */
export const LISTENING_SUBJECT_IDS = [
  'irish', 'french', 'german', 'spanish', 'italian', 'music',
  'japanese', 'russian', 'polish', 'portuguese',
] as const;

export type ListeningCard = SecCard & { audioMaterial: CardAudioMaterial };
export const isListeningCard = (card: SecCard): card is ListeningCard => Boolean(card.audioMaterial);

export interface StudioExtract {
  key: string;
  /** What the stepper and the sheet call it: "Excerpt 2", "Dialogue 1", or the section's own name. */
  title: string;
  /** The piece's printed name, where the paper gives one: "Boa Forma", "EL TIEMPO". */
  piece?: string;
  /** The recording these questions are heard on. */
  audio: CardAudioMaterial;
  cards: ListeningCard[];
}

export interface StudioSection {
  key: string;
  title: string;
  extracts: StudioExtract[];
  /** Every card of the section, in printed order. */
  cards: ListeningCard[];
  /** The printed tariff of those cards. */
  marks: number;
}

export interface StudioSitting {
  key: string;
  subjectId: string;
  year: number;
  level: MarkBankLevel;
  deferred: boolean;
  /** "2025 Higher", "2023 Ordinary · deferred sitting". */
  title: string;
  sections: StudioSection[];
  /** Every recording of the sitting has a copy the app can play. */
  playsInApp: boolean;
}

/* ------------------------------------------------------------- reading ---- */

const isDeferred = (card: ListeningCard) => card.audioMaterial.canonicalUrl.includes('/archive/deferredexams/');
const refOf = (card: SecCard) => card.questionRef.replace(/\s+—\s+Deferred sitting$/, '');
const sectionLabel = (card: ListeningCard) => card.audioMaterial.label.replace(/\s+·\s+listening$/i, '').trim();
const questionNumber = (ref: string): number => {
  const match = /\bQ(\d+)/.exec(ref);
  return match ? Number(match[1]) : 0;
};
/** The bracketed part labels after the question number: "(e)(i)" -> ["e", "i"]. */
const partTokens = (ref: string): string[] => {
  const question = /\bQ\d*/.exec(ref);
  const tail = question ? ref.slice(question.index + question[0].length) : ref;
  return [...tail.matchAll(/\(([a-z]+|\d+)\)/gi)].map(match => match[1].toLowerCase());
};

const ROMAN: Record<string, number> = {
  i: 1, ii: 2, iii: 3, iv: 4, v: 5, vi: 6, vii: 7, viii: 8, ix: 9, x: 10, xi: 11, xii: 12, xiii: 13, xiv: 14, xv: 15,
};
/** "(i)" is the ninth letter where its siblings run (a), (b), (c), and one where they run (i), (ii), (iii). */
const lettersInUse = (tokens: string[]) => tokens.some(token => /^[a-z]$/.test(token) && !'ivx'.includes(token));
const tokenRank = (token: string, letters: boolean): number => {
  if (/^\d+$/.test(token)) return Number(token);
  if (!letters && ROMAN[token]) return ROMAN[token];
  return token.length === 1 ? token.charCodeAt(0) - 96 : 100 + (ROMAN[token] ?? 0);
};

const compareKeys = (a: number[], b: number[]): number => {
  for (let i = 0; i < Math.max(a.length, b.length); i += 1) {
    const difference = (a[i] ?? 0) - (b[i] ?? 0);
    if (difference) return difference;
  }
  return 0;
};

const IRISH_ORDINALS: Record<string, number> = { haon: 1, dó: 2, trí: 3, ceathair: 4, cúig: 5, sé: 6 };
const irishOrdinal = (text: string): number => {
  // No trailing \b: it does not hold after an accented letter (Dó, Trí).
  const match = /\ba\s+(hAon|Dó|Trí|Ceathair|Cúig|Sé)(?=\s|·|$)/i.exec(text);
  return match ? IRISH_ORDINALS[match[1].toLowerCase()] ?? 0 : 0;
};

/* ------------------------------------------------------------ placement ---- */

interface Placement {
  sectionKey: string;
  sectionTitle: string;
  sectionOrder: number;
  /** Null: the extract is found afterwards, from runs of one printed instruction. */
  extractKey: string | null;
  /** Null: the section's own title. */
  extractTitle: string | null;
  extractOrder: number;
  /** Ahead of the question number when ordering cards inside an extract. */
  lead: number[];
}

const letterOrder = (text: string) => [...text].reduce((order, char) => order * 40 + (char.charCodeAt(0) % 40), 0);
const pieceAfterDash = (title: string | undefined): string | null => {
  const piece = title?.split(/\s+—\s+/)[1]?.trim();
  return piece && !/^Question\s+\d+/i.test(piece) ? piece : null;
};

const place = (card: ListeningCard): Placement => {
  const ref = refOf(card);
  const question = questionNumber(ref);
  const label = sectionLabel(card);
  const whole = { extractKey: 'all', extractTitle: null, extractOrder: 0, lead: [] };

  switch (card.subjectId) {
    case 'music': {
      // "Excerpt 2" in the reference (to 2018) or in the recording's label
      // (from 2019). A part that compares two excerpts sits with the later one.
      const inRef = /\bExcerpt (\d+)/.exec(ref);
      const pair = /\bExcerpt (\d+) and Excerpt (\d+)/.exec(card.audioMaterial.label);
      const inLabel = /·\s*Excerpt (\d+)\s*$/.exec(card.audioMaterial.label);
      const excerpt = inRef ? Number(inRef[1])
        : pair ? Math.max(Number(pair[1]), Number(pair[2]))
        : inLabel ? Number(inLabel[1]) : 0;
      const bars = /\bBars (\d+)/.exec(ref);
      return {
        sectionKey: `Q${question}`, sectionTitle: `Question ${question}`, sectionOrder: question,
        extractKey: `X${excerpt}`, extractTitle: excerpt ? `Excerpt ${excerpt}` : null, extractOrder: excerpt,
        lead: [bars ? Number(bars[1]) : 0],
      };
    }
    case 'spanish': {
      // The paper has no level above the question: each question is one piece.
      // The weather question's title is only in its instruction ("EL TIEMPO: ...").
      const piece = pieceAfterDash(card.sourceMaterial?.title)
        ?? (/^(el tiempo)\s*:/i.exec(card.stem ?? '')?.[1].toUpperCase() ?? null);
      return {
        ...whole, sectionKey: `Q${question}`, sectionTitle: `Question ${question}`, sectionOrder: question,
        extractTitle: piece,
      };
    }
    case 'italian': {
      const section = /\bSection L([AB])(\d)?/.exec(ref);
      const letter = section?.[1] ?? 'A';
      const dialogue = Number(section?.[2] ?? 0);
      return {
        sectionKey: `L${letter}`, sectionTitle: `Section ${letter}`, sectionOrder: letter === 'A' ? 1 : 2,
        extractKey: dialogue ? `D${dialogue}` : 'all', extractTitle: dialogue ? `Dialogue ${dialogue}` : null,
        extractOrder: dialogue, lead: [],
      };
    }
    case 'irish': {
      const [first, second = '', third = ''] = card.audioMaterial.label.split(/\s+·\s+/);
      const cuid = /^Cuid ([ABC])$/.exec(first);
      const ceist = /\bCeist (\d+)/.exec(ref);
      if (!cuid) {
        // Foundation names no Cuid: each Ceist stands alone.
        const number = Number(/\bCeist (\d+)/.exec(card.audioMaterial.label)?.[1] ?? ceist?.[1] ?? 0);
        return { ...whole, sectionKey: `Ceist ${number}`, sectionTitle: `Ceist ${number}`, sectionOrder: number };
      }
      const ordinal = irishOrdinal(second);
      return {
        sectionKey: first, sectionTitle: first, sectionOrder: cuid[1].charCodeAt(0) - 64,
        extractKey: second || 'all', extractTitle: second || null, extractOrder: ordinal,
        lead: [/Dara/.test(third) ? 2 : third ? 1 : 0, ceist ? Number(ceist[1]) : 0],
      };
    }
    case 'german':
    case 'polish':
      return {
        sectionKey: card.section, sectionTitle: label, sectionOrder: letterOrder(card.section),
        extractKey: null, extractTitle: null, extractOrder: 0, lead: [],
      };
    case 'japanese': {
      // 2010 Higher prints C1 and C2; both are Section C, heard as two pieces.
      const letter = card.section.charAt(0);
      return {
        sectionKey: letter, sectionTitle: `Section ${letter}`, sectionOrder: letterOrder(letter),
        extractKey: null, extractTitle: null, extractOrder: 0, lead: [Number(card.section.charAt(1)) || 0],
      };
    }
    case 'portuguese': {
      const piece = /^Parte [A-E]:?\s*(.*?)\s+—\s+Question/.exec(card.sourceMaterial?.title ?? '')?.[1].trim();
      return {
        ...whole, sectionKey: card.section, sectionTitle: label, sectionOrder: letterOrder(card.section),
        extractTitle: piece || null,
      };
    }
    default: {
      // French, Russian, and any subject without a rule of its own: the card's
      // section, heard as one piece. A recording label that only names the
      // subject ("Russian listening") gives way to the section itself.
      const printed = /\bSection (?:L)?([A-Z]{1,3}|\d+)\b/.exec(ref)?.[1];
      const generic = /^\S+ listening$/i.test(card.audioMaterial.label.trim());
      const title = !generic && label ? label : printed ? `Section ${printed}` : `Section ${card.section}`;
      return { ...whole, sectionKey: card.section, sectionTitle: title, sectionOrder: letterOrder(card.section) };
    }
  }
};

/** The piece a printed instruction introduces, where it names one. */
const stemTitle = (card: ListeningCard): string | null => {
  const stem = (card.stem ?? '').trim();
  const item = /\(?\bItem\s*(\d+)(?::\s*([^)]+))?\)?\s*$/.exec(stem);
  if (item) return item[2] ? `Item ${item[1]}: ${item[2].trim()}` : `Item ${item[1]}`;
  if (card.subjectId === 'german') {
    const heading = /^\(([^)]{3,60})\)/.exec(stem)?.[1];
    if (heading) return heading;
  }
  if (card.subjectId === 'polish') {
    const heading = /^(.{2,50}?)\s+You will hear\b/.exec(stem)?.[1];
    if (heading) return heading;
  }
  if (card.subjectId === 'japanese') {
    const heading = /(?:^|\n|\.\s)(\d+)\.\s*\(?([^()\n]{2,60})\)?\s*$/.exec(stem);
    if (heading) return `${heading[1]}. ${heading[2].trim()}`;
  }
  return null;
};

/* -------------------------------------------------------------- sittings ---- */

interface Placed { card: ListeningCard; placement: Placement; ref: string; question: number; tokens: string[]; deckIndex: number }

/** Every recording card of one subject and level, as the sittings a student can sit. Newest first. */
export function listeningSittings(cards: SecCard[]): StudioSitting[] {
  const sittings = new Map<string, { first: ListeningCard; deferred: boolean; placed: Placed[] }>();
  cards.forEach((card, deckIndex) => {
    if (!isListeningCard(card)) return;
    const deferred = isDeferred(card);
    const key = `${card.subjectId}:${card.year}:${card.level}:${deferred ? 'deferred' : 'june'}`;
    const sitting = sittings.get(key) ?? { first: card, deferred, placed: [] };
    const ref = refOf(card);
    sitting.placed.push({ card, placement: place(card), ref, question: questionNumber(ref), tokens: partTokens(ref), deckIndex });
    sittings.set(key, sitting);
  });

  return [...sittings.entries()].map(([key, { first, deferred, placed }]) => {
    const bySection = new Map<string, Placed[]>();
    for (const item of placed) {
      const list = bySection.get(item.placement.sectionKey) ?? [];
      list.push(item);
      bySection.set(item.placement.sectionKey, list);
    }

    const sections = [...bySection.entries()]
      .sort(([, a], [, b]) => a[0].placement.sectionOrder - b[0].placement.sectionOrder)
      .map(([sectionKey, items]): StudioSection => {
        // Whether "(i)" is a letter is settled per question and per depth.
        const letters = new Map<string, boolean>();
        const depthKey = (item: Placed, depth: number) => `${item.question}:${depth}`;
        for (const item of items) {
          item.tokens.forEach((token, depth) => {
            const k = depthKey(item, depth);
            letters.set(k, Boolean(letters.get(k)) || lettersInUse([token]));
          });
        }
        const orderOf = (item: Placed) => [
          item.placement.extractOrder, ...item.placement.lead, item.question,
          ...item.tokens.map((token, depth) => tokenRank(token, Boolean(letters.get(depthKey(item, depth))))),
        ];
        const sorted = [...items].sort((a, b) =>
          compareKeys(orderOf(a), orderOf(b))
          // Fewer part labels first ("Q3" before "Q3(i)"), then the deck's own order.
          || a.tokens.length - b.tokens.length || a.deckIndex - b.deckIndex);
        const sectionTitle = sorted[0].placement.sectionTitle;

        const groups: { key: string; title: string | null; items: Placed[] }[] = [];
        for (const item of sorted) {
          const stemRun = item.placement.extractKey === null;
          const runKey = stemRun ? `${item.card.section}:${(item.card.stem ?? '').trim()}` : item.placement.extractKey as string;
          const last = groups[groups.length - 1];
          if (last && last.key === runKey) last.items.push(item);
          else if (!stemRun && groups.some(group => group.key === runKey)) groups.find(group => group.key === runKey)?.items.push(item);
          else groups.push({ key: runKey, title: item.placement.extractTitle, items: [item] });
        }
        const extracts = groups.map((group, position): StudioExtract => {
          const lead = group.items[0];
          const named = lead.placement.extractKey === null ? stemTitle(lead.card) : group.title;
          // One extract: it goes by the section's name, with the piece beside it.
          // Several: each goes by its own name, or by its place in the section.
          const title = groups.length === 1 ? sectionTitle : named ?? `${sectionTitle} · ${position + 1}`;
          return {
            key: `${key}:${sectionKey}:${position}`,
            title,
            ...(groups.length === 1 && named && named !== sectionTitle ? { piece: named } : {}),
            audio: lead.card.audioMaterial,
            cards: group.items.map(item => item.card),
          };
        });
        const sectionCards = extracts.flatMap(extract => extract.cards);
        return {
          key: `${key}:${sectionKey}`,
          title: sectionTitle,
          extracts,
          cards: sectionCards,
          marks: sectionCards.reduce((sum, card) => sum + card.totalMarks, 0),
        };
      });

    return {
      key,
      subjectId: first.subjectId,
      year: first.year,
      level: first.level,
      deferred,
      title: `${first.year} ${MARK_BANK_LEVEL_LABELS[first.level]}${deferred ? ' · deferred sitting' : ''}`,
      sections,
      playsInApp: placed.every(item => {
        const url = item.card.audioMaterial.canonicalUrl;
        return hostedAudioPath(url) !== null || !/^https?:\/\/(www\.)?examinations\.ie\//i.test(url);
      }),
    };
  }).sort((a, b) => b.year - a.year || Number(a.deferred) - Number(b.deferred));
}

/**
 * What the sheet prints beside a part: "(a)", "(e)(i)", "2(b)", "3". Where the
 * section is itself the question (Music, Spanish) the number is left off.
 */
export function partLabel(card: SecCard): string {
  const ref = refOf(card);
  if (card.subjectId === 'irish') {
    // Foundation's section is the Ceist itself, so only its letter is left to
    // print; 2026 prints a Ceist number inside each Fógra, Comhrá and Píosa.
    const ceist = /\bCeist (\d+)(\([a-z]+\))?/i.exec(ref);
    if (!ceist) return '';
    return /Cluastuiscint · Ceist/.test(ref) ? ceist[2] ?? '' : `${ceist[1]}${ceist[2] ?? ''}`;
  }
  const question = /\bQ(\d*)/.exec(ref);
  if (!question) return '';
  const tail = ref.slice(question.index + question[0].length);
  const bracket = tail.indexOf('(');
  const parts = bracket >= 0 ? tail.slice(bracket).trim() : '';
  const sectionIsQuestion = card.subjectId === 'music' || card.subjectId === 'spanish';
  return sectionIsQuestion ? parts : `${question[1]}${parts}`;
}
