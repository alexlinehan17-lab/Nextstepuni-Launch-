/** @license SPDX-License-Identifier: Apache-2.0 */
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import authoredJson from '../components/MarkBank/cards/irish/authored.json';
import {
  irishMarks,
  irishScoreId,
  listeningQuestionGroups,
  suggestRubricGrade,
} from '../components/MarkBank/SessionScreen';
import { sessionExerciseCount } from '../components/MarkBank/sessionPlanning';
import {
  isRubricCard,
  tariffReconciles,
  type CardAudioMaterial,
  type CardSourceMaterial,
  type IrishRubric,
  type SecRubricCard,
} from '../types/markBank';

interface CensusAsk {
  id: string;
  year: number;
  level: 'hl' | 'ol';
  paper: 1 | 2;
  questionRef: string;
  status: 'authored' | 'queued';
}

interface IrishCensus {
  paperCount: number;
  cardUnitCount: number;
  authoredCount: number;
  queuedCount: number;
  papers: Array<{
    year: number;
    level: 'hl' | 'ol';
    paper: 1 | 2;
    cardUnits: number;
    authored: number;
    queued: number;
  }>;
  asks: CensusAsk[];
}

interface AuthoredCard {
  id: string;
  year: number;
  level: 'higher' | 'ordinary';
  paper: 1 | 2;
  section: '1' | '2';
  questionRef: string;
  questionText: string;
  totalMarks: number;
  topicId: string;
  paperFileid: string;
  paperPage: number;
  paperTraceScore: number;
  schemePage: number;
  schemeTraceScore: number;
  criteria: IrishRubric['criteria'];
  sourceMaterial?: CardSourceMaterial;
  audioMaterial?: CardAudioMaterial;
}

interface IrishManifest {
  cardCount: number;
  cards: AuthoredCard[];
}

const census = JSON.parse(readFileSync(resolve(
  __dirname, '../scripts/markbank/authored/irish-census.json'), 'utf8')) as IrishCensus;
const manifest = authoredJson as unknown as IrishManifest;
const ALL: SecRubricCard[] = [...HIGHER, ...ORDINARY];
const byId = new Map(ALL.map(card => [card.id, card]));

const irishRubric = (card: SecRubricCard): IrishRubric => {
  if (card.rubric.system !== 'irish') throw new Error(`${card.id} is not an Irish rubric`);
  return card.rubric;
};

const family = (card: { id: string }) => {
  if (card.id.includes('-listening-')) return 'listening';
  if (card.id.includes('-composition-')) return 'composition';
  if (card.id.includes('-reading-')) return 'reading';
  return 'literature';
};

describe('Irish all-question census', () => {
  it('accounts for every selectable response on all twenty written papers', () => {
    expect(census.paperCount).toBe(20);
    expect(census.cardUnitCount).toBe(400);
    expect(census.authoredCount).toBe(400);
    expect(census.queuedCount).toBe(0);
    expect(census.asks).toHaveLength(400);
    expect(new Set(census.asks.map(ask => ask.id)).size).toBe(400);
    expect(census.papers.every(paper =>
      paper.cardUnits === paper.authored + paper.queued)).toBe(true);
  });

  it('pins the independently audited count for every paper', () => {
    const expected = new Map([
      ['hl-1', 17], ['hl-2', 26], ['ol-1', 15], ['ol-2', 22],
    ]);
    for (const year of [2021, 2022, 2023, 2024, 2025]) {
      for (const [key, count] of expected) {
        const [level, paper] = key.split('-');
        expect(census.asks.filter(ask => ask.year === year
          && ask.level === level && ask.paper === Number(paper)), `${year} ${key}`)
          .toHaveLength(count);
      }
    }
  });

  it('maps the census and generated manifest one-to-one to the live decks', () => {
    expect(HIGHER).toHaveLength(215);
    expect(ORDINARY).toHaveLength(185);
    expect(ALL).toHaveLength(400);
    expect(manifest.cardCount).toBe(400);
    expect(new Set(ALL.map(card => card.id)).size).toBe(400);
    expect(ALL.map(card => card.id).sort()).toEqual(census.asks.map(ask => ask.id).sort());
    expect(manifest.cards.map(card => card.id).sort())
      .toEqual(census.asks.map(ask => ask.id).sort());
  });
});
describe('Irish prompt, paper and source integrity', () => {
  it('preserves every generated prompt and its paper/scheme trace', () => {
    const furniture = /Scrúdú na hArdteistiméireachta|Leathanach Bán|Níl (?:aon )?ábhar scrúdaithe|Cuid II\s+An Cheapadóireacht|(?:2A|2B|3A|3B)\s*[–—-]\s*(?:PRÓS|FILÍOCHT)/i;
    for (const authored of manifest.cards) {
      const runtime = byId.get(authored.id);
      expect(runtime, authored.id).toBeDefined();
      expect(runtime?.questionText, authored.id).toBe(authored.questionText);
      expect(runtime?.questionRef, authored.id).toBe(authored.questionRef);
      expect(runtime?.totalMarks, authored.id).toBe(authored.totalMarks);
      expect(runtime?.topicId, authored.id).toBe(authored.topicId);
      expect(runtime?.paperFileid, authored.id).toBe(authored.paperFileid);
      expect(runtime?.section, authored.id).toBe(authored.section);
      expect(runtime?.schemeCitation, authored.id)
        .toContain(`p.${authored.schemePage}`);
      expect(authored.paperPage, authored.id).toBeGreaterThan(0);
      expect(authored.paperTraceScore, authored.id).toBeGreaterThan(0);
      expect(authored.schemePage, authored.id).toBeGreaterThan(0);
      expect(authored.schemeTraceScore, authored.id).toBeGreaterThan(0);
      expect(authored.questionText.length, authored.id).toBeGreaterThanOrEqual(40);
      expect(authored.questionText, authored.id).not.toMatch(furniture);
      if (family(authored) === 'reading') {
        expect(authored.questionText.length, authored.id).toBeLessThan(900);
      }
    }
  });

  it('resolves every card to the real Paper Trail question paper', async () => {
    const { resolvePaperFileid } = await import('../scripts/markbank/paperIndex.mjs');
    const bad = ALL.filter(card => card.paperFileid !== resolvePaperFileid(
      card.subjectId, card.year, card.level, card.section));
    expect(bad.map(card => `${card.id}: ${card.paperFileid}`)).toEqual([]);
    expect(byId.get('irish-2022-ol-p1-listening-a-f1')?.paperFileid)
      .toBe('LC001GLP000IV');
  });

  it('attaches every required reading passage and printed poem as real PDF pages', () => {
    const sourced = ALL.filter(card => card.sourceMaterial);
    expect(sourced).toHaveLength(140);
    expect(sourced.filter(card => family(card) === 'reading')).toHaveLength(110);
    expect(sourced.filter(card => card.id.includes('-poetry-3a-'))).toHaveLength(25);
    expect(sourced.filter(card => card.id.includes('-literature-4-'))).toHaveLength(5);

    for (const card of sourced) {
      const source = card.sourceMaterial!;
      expect(source.kind, card.id).toBe('source-text');
      expect(source.title.trim().length, card.id).toBeGreaterThan(2);
      expect(source.pages.length, card.id).toBeGreaterThan(0);
      expect(source.pages, card.id).toEqual([...source.pages].sort((a, b) => a - b));
      expect(new Set(source.pages).size, card.id).toBe(source.pages.length);
      expect(source.presentationNote, card.id).toContain('official examination paper');
    }

    const additional = sourced.filter(card => card.id.includes('-literature-4-'));
    expect(additional.map(card => card.sourceMaterial?.title)).toEqual([
      'Éiceolaí', 'Caoineadh Airt Uí Laoghaire', 'A Chlann', 'Fill Arís',
      'Caoineadh Airt Uí Laoghaire',
    ]);
    expect(additional.map(card => card.sourceMaterial?.pages)).toEqual([
      [13], [14, 15], [13], [13], [13, 14],
    ]);
  });

  it('keeps every Ordinary prescribed-poetry choice whole and on its own page', () => {
    const ordinaryPoetry = ORDINARY.filter(card => card.id.includes('-poetry-3a-'));
    expect(ordinaryPoetry).toHaveLength(15);
    for (const card of ordinaryPoetry) {
      expect(card.questionText, card.id).toMatch(/\(i\).*\(ii\).*\(iii\)/);
      expect(card.sourceMaterial?.title, card.id).not.toBe('Dán Ainmnithe');
      expect(card.sourceMaterial?.pages, card.id).toHaveLength(1);
    }

    const repairedChoices = [
      ['irish-2022-ol-p2-poetry-3a-a', 'An tEarrach Thiar', 11],
      ['irish-2022-ol-p2-poetry-3a-b', 'Colscaradh', 12],
      ['irish-2022-ol-p2-poetry-3a-c', 'An Spailpín Fánach', 13],
      ['irish-2024-ol-p2-poetry-3a-a', 'Colscaradh', 10],
      ['irish-2024-ol-p2-poetry-3a-b', 'An Spailpín Fánach', 11],
      ['irish-2024-ol-p2-poetry-3a-c', 'Géibheann', 12],
      ['irish-2025-ol-p2-poetry-3a-a', 'Mo Ghrá-Sa', 10],
      ['irish-2025-ol-p2-poetry-3a-b', 'An tEarrach Thiar', 11],
      ['irish-2025-ol-p2-poetry-3a-c', 'Colscaradh', 12],
    ] as const;
    for (const [id, title, page] of repairedChoices) {
      const card = byId.get(id);
      expect(card?.sourceMaterial?.title, id).toBe(title);
      expect(card?.sourceMaterial?.pages, id).toEqual([page]);
      expect(card?.totalMarks, id).toBe(25);
    }
  });

  it('retains printed part labels and removes continuation furniture', () => {
    const hurlamaboc = byId.get('irish-2021-ol-p2-prose-2a-a');
    expect(hurlamaboc?.questionText).toMatch(/\(i\).*\(ii\).*\(iii\).*\(iv\).*\(v\)/);

    const furniture = ALL.filter(card =>
      /Cuid\s+[ABC]\s+ar\s+leanúint|Freagair\s+do\s+rogha\s+ceann\s+amháin\s+as\s*$/i
        .test(card.questionText));
    expect(furniture.map(card => card.id)).toEqual([]);
  });

  it('puts the official listening recording on every listening card and nowhere else', () => {
    const listening = ALL.filter(card => family(card) === 'listening');
    expect(listening).toHaveLength(70);
    expect(listening.every(card => card.audioMaterial)).toBe(true);
    expect(ALL.filter(card => family(card) !== 'listening' && card.audioMaterial))
      .toEqual([]);

    for (const card of listening) {
      const audio = card.audioMaterial!;
      expect(audio.kind, card.id).toBe('source-audio');
      expect(audio.secFileid, card.id).toBe('LC001ZLP017IV.mp3');
      expect(audio.canonicalUrl, card.id).toBe(
        `https://www.examinations.ie/archive/exampapers/${card.year}/LC001ZLP017IV.mp3`);
      expect(audio.playbackUrl, card.id).toMatch(/^https:\/\/educateplus\.ie\//);
      expect(audio.attribution, card.id).toContain('State Examinations Commission');
    }
    const grid = byId.get('irish-2021-ol-p1-listening-a-f1')!;
    expect(irishRubric(grid).criteria[0].guidance.join(' ')).toContain('oifig@gaeilge.ie');
  });

  it('keeps every prompt for an audio extract together with that recording', () => {
    const listening = ALL.filter(card => family(card) === 'listening');
    const groups = listening.map(card => ({
      id: card.id,
      groups: listeningQuestionGroups(card.questionText),
    }));

    expect(groups.every(card => card.groups.length > 0)).toBe(true);
    const malformed = groups.filter(card => !card.groups.every(group =>
      group.prompts.length > 0
      && group.prompts.every(prompt => Boolean(prompt.label && prompt.text))));
    expect(malformed.map(card => card.id)).toEqual([]);

    // These are 218 prompts backed by 70 separately scored card ids, but shown
    // inside only 30 listening exercises. The recording and the question sheet
    // must not restart merely because the SEC scheme has another scoring block.
    expect(groups.reduce((total, card) => total + card.groups.reduce(
      (subtotal, group) => subtotal + group.prompts.length, 0), 0)).toBe(218);
    expect(sessionExerciseCount(listening)).toBe(30);

    const grid = groups.find(card => card.id === 'irish-2021-ol-p1-listening-a-f1')!;
    expect(grid.groups[0].instruction).toMatch(/Líon isteach an t-eolas/i);
    expect(grid.groups[0].prompts).toHaveLength(4);

    const conversation = groups.find(card => card.id === 'irish-2025-ol-p1-listening-b-c1')!;
    expect(conversation.groups.map(group => group.label)).toEqual([
      'An Chéad Mhír', 'An Dara Mír',
    ]);
    expect(conversation.groups.flatMap(group => group.prompts)).toHaveLength(4);
  });
});

describe('Irish marking grammar', () => {
  it('uses only Irish rubric cards and reconciles every published total', () => {
    expect(ALL.every(isRubricCard)).toBe(true);
    expect(ALL.every(card => card.rubric.system === 'irish')).toBe(true);
    expect(ALL.every(card => !('rows' in card))).toBe(true);
    expect(ALL.filter(card => !tariffReconciles(card)).map(card => card.id)).toEqual([]);
  });

  it('keeps exact answers distinct from indicative and quality guidance', () => {
    const exact = ALL.filter(card => ['listening', 'reading'].includes(family(card)));
    expect(exact).toHaveLength(180);
    for (const card of exact) {
      const criteria = irishRubric(card).criteria;
      expect(criteria).toHaveLength(1);
      expect(criteria[0].guidanceKind, card.id).toBe('exact');
      expect(criteria[0].guidance.length, card.id).toBeGreaterThan(0);
      expect(criteria[0].guidance.join(' '), card.id)
        .not.toMatch(/Siombailí Anótála|Stíl chuí scríbhneoireachta|An Cumas Gaeilge \((?:40|80) marc/i);
    }

    const literature = ALL.filter(card => family(card) === 'literature');
    expect(literature).toHaveLength(130);
    expect(literature.every(card => irishRubric(card).criteria[0].guidanceKind === 'indicative'))
      .toBe(true);
    expect(literature.every(card =>
      irishRubric(card).markingGuideNote.includes('indicative rather than exhaustive')))
      .toBe(true);
  });

  it('models Higher and Ordinary composition exactly as published', () => {
    const higher = HIGHER.filter(card => family(card) === 'composition');
    const ordinary = ORDINARY.filter(card => family(card) === 'composition');
    expect(higher).toHaveLength(45);
    expect(ordinary).toHaveLength(45);
    for (const card of higher) {
      expect(irishRubric(card).criteria.map(criterion =>
        [criterion.id, criterion.maxMarks])).toEqual([
        ['stil', 5], ['abhar', 15], ['gaeilge', 80],
      ]);
    }
    for (const card of ordinary) {
      const criteria = irishRubric(card).criteria;
      expect(criteria.map(criterion => [criterion.id, criterion.maxMarks])).toEqual([
        ['tasc', 2], ['abhar', 8], ['gaeilge', 40],
      ]);
      expect(criteria[2].permittedMarks).toEqual([
        0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20,
        22, 24, 26, 28, 30, 32, 34, 36, 38, 40,
      ]);
    }
  });

  it('awards Higher literature language marks but subtracts the Ordinary penalty', () => {
    const higher = HIGHER.filter(card => family(card) === 'literature');
    const ordinary = ORDINARY.filter(card => family(card) === 'literature');
    expect(higher).toHaveLength(70);
    expect(ordinary).toHaveLength(60);
    expect(higher.every(card => irishRubric(card).criteria.at(-1)?.kind === 'award'))
      .toBe(true);
    expect(ordinary.every(card => {
      const deduction = irishRubric(card).criteria.at(-1);
      return deduction?.id === 'gaeilge-deduction'
        && deduction.kind === 'deduction' && deduction.maxMarks === 4;
    })).toBe(true);

    const ordinaryCard = ordinary[0];
    expect(irishMarks(ordinaryCard, {
      [irishScoreId('eolas')]: 25,
      [irishScoreId('gaeilge-deduction')]: 4,
    })).toBe(21);
    expect(suggestRubricGrade(ordinaryCard, {
      [irishScoreId('eolas')]: 25,
      [irishScoreId('gaeilge-deduction')]: 4,
    })).toBe('got');
    expect(irishMarks(ordinaryCard, {
      [irishScoreId('eolas')]: 0,
      [irishScoreId('gaeilge-deduction')]: 4,
    })).toBe(0);
  });
});
