import type { SecCard } from '../../types/markBank';
import { figureUrl } from '../../utils/figureUrl';
import type { WaysInQuestionSource } from './types';

export function waysInSourceFromMarkBank(card: SecCard, subjectLabel: string): WaysInQuestionSource {
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
    // The total is printed on the question paper. Rows, routes, answer counts
    // and tariff mechanics come from the marking scheme and deliberately do
    // not cross this pre-reveal boundary—not even as anonymous numbers.
    answerShape: {
      totalMarks: card.totalMarks,
    },
    textConfidence: 'verified',
    sourceLabel: `${card.year} ${card.level === 'higher' ? 'HL' : 'OL'} · ${card.questionRef}`,
    sourceCopyright: 'Question wording © State Examinations Commission',
  };
}
