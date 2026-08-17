import type { SecCard } from '../../types/markBank';
import { figureUrl } from '../../utils/figureUrl';
import type { WaysInQuestionSource } from './types';

const rowIdeaCount = (row: SecCard['rows'][number]): number =>
  row.kind === 'anyN' && row.group ? row.group.claimMax : 1;

/**
 * Count only the answer spaces the student can actually use.
 * Alternative SEC routes are mutually exclusive, so their rows must not be
 * added together. The marking-row wording itself never leaves Mark Bank.
 */
export function markBankAnswerIdeaCount(card: SecCard): number {
  if (card.tariffModel.kind === 'bestNofParts') return card.tariffModel.answer;

  const common = card.rows
    .filter(row => !row.route)
    .reduce((total, row) => total + rowIdeaCount(row), 0);
  const byRoute = new Map<string, number>();
  for (const row of card.rows) {
    if (!row.route) continue;
    byRoute.set(row.route, (byRoute.get(row.route) ?? 0) + rowIdeaCount(row));
  }
  const route = byRoute.size ? Math.max(...byRoute.values()) : 0;
  return Math.max(1, common + route);
}

export function waysInSourceFromMarkBank(card: SecCard, subjectLabel: string): WaysInQuestionSource {
  const choice = card.tariffModel.kind === 'bestNofParts'
    ? { answer: card.tariffModel.answer, available: card.tariffModel.ofParts }
    : undefined;
  return {
    id: `mark-bank:${card.id}`,
    origin: 'mark-bank',
    subjectLabel,
    levelLabel: card.level === 'higher' ? 'Higher Level' : 'Ordinary Level',
    year: card.year,
    questionRef: card.questionRef,
    questionText: card.questionText,
    stem: card.stem,
    figure: 'figure' in card && card.figure ? {
      src: figureUrl(card.figure.src),
      alt: card.figure.alt,
      attribution: card.figure.attribution,
    } : undefined,
    answerShape: {
      points: markBankAnswerIdeaCount(card),
      totalMarks: card.totalMarks,
      choice,
      alternativeRoutes: card.rows.some(row => Boolean(row.route)),
    },
    textConfidence: 'verified',
    sourceLabel: `${card.year} ${card.level === 'higher' ? 'HL' : 'OL'} · ${card.questionRef}`,
    sourceCopyright: 'Question wording © State Examinations Commission',
  };
}
