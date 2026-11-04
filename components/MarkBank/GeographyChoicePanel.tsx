/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of a Geography criterion the scheme prices one of
 * several ways (cards/geography/allocation.ts, `GeographyAllocation.choice`):
 *
 *  - route: a two-column table ("3 @ 20 marks each" / "4 @ 15 marks each",
 *    "Bar Chart" / "Pie Chart"). The student picks the column their answer
 *    followed, then claims that column's rows and SRPs as on any other card.
 *    Where the review split one table over several criteria (2010–2013
 *    Higher options, "Number of aspects") the pick is made once: every
 *    criterion of the table shows the same pill and moves together.
 *  - band: a quality table ("Excellent · 20" … "Poor · 0"). Each band is a
 *    claimable row with its descriptor; claiming one clears the others.
 *  - alternative: one printed answer or another, each at its own price.
 *
 * Every label and descriptor is the scheme's own text; only the option the
 * student picks scores (geographyScoring.ts).
 */
import React from 'react';
import type { GeographyAllocationChoice, GeographyCriterion } from '../../types/markBank';
import HorizontalTabs from '../ui/HorizontalTabs';
import GeographyAllocationPanel from './GeographyAllocationPanel';
import {
  geographyChoiceScoreId,
  geographyOptionCriterionId,
  type GeographyScoreId,
  type GeographyScores,
} from './geographyScoring';
import './geography-choice.css';

interface Props {
  criterion: GeographyCriterion & { allocation: NonNullable<GeographyCriterion['allocation']> & { choice: GeographyAllocationChoice } };
  scores: GeographyScores;
  onScore: (id: GeographyScoreId, marks: number) => void;
}

const Tick: React.FC = () => (
  <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">
    <path d="M2.5 6.2l2.4 2.4L9.5 3.9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export default function GeographyChoicePanel({ criterion, scores, onScore }: Props) {
  const { choice, directions } = criterion.allocation;
  const choiceId = geographyChoiceScoreId(choice.follows ?? criterion.id);
  const pickedIndex = (scores[choiceId] ?? 0) - 1;
  const picked = choice.options[pickedIndex];
  // The criterion's own heading already names it ("Overall coherence").
  const same = (a: string, b: string) => a.toLowerCase().replace(/[^a-z0-9]+/g, '') === b.toLowerCase().replace(/[^a-z0-9]+/g, '');
  const prompt = choice.prompt && !same(choice.prompt, criterion.label) ? choice.prompt : '';

  if (choice.kind === 'route') {
    return (
      <div className="mb-geo-choice">
        {prompt && <p className="mb-geo-choice-prompt">{prompt}</p>}
        <HorizontalTabs
          variant="pill"
          size="sm"
          fill
          label={choice.prompt || `${criterion.label}: the scheme to use`}
          value={picked?.id ?? ''}
          options={choice.options.map(option => ({ value: option.id, label: option.label }))}
          onChange={id => onScore(choiceId, choice.options.findIndex(option => option.id === id) + 1)}
        />
        {picked?.allocation ? (
          <GeographyAllocationPanel
            criterion={{
              ...criterion,
              id: geographyOptionCriterionId(criterion.id, picked.id),
              allocation: picked.allocation,
            }}
            scores={scores}
            onScore={onScore}
          />
        ) : (
          <p className="mb-geo-choice-hint">Choose the scheme that fits your answer, then claim its marks.</p>
        )}
        {directions.length > 0 && (
          <ul className="mb-geo-choice-notes">
            {directions.map((note, index) => <li key={index}>{note}</li>)}
          </ul>
        )}
      </div>
    );
  }

  return (
    <div className="mb-geo-choice">
      {prompt && <p className="mb-geo-choice-prompt">{prompt}</p>}
      <div className="mb-geo-choice-options" role="group" aria-label={choice.prompt || criterion.label}>
        {choice.options.map((option, index) => {
          const claimed = index === pickedIndex;
          const marks = option.marks ?? 0;
          return (
            <button
              key={option.id}
              type="button"
              className="mb-geo-choice-option"
              data-claimed={claimed}
              aria-pressed={claimed}
              aria-label={`${option.label} · ${marks}m`}
              onClick={() => onScore(choiceId, claimed ? 0 : index + 1)}
            >
              <span className="mb-geo-choice-check" aria-hidden="true">{claimed && <Tick />}</span>
              <span className="mb-geo-choice-text">
                <span dir="auto">{option.label}</span>
                {option.note && <small>{option.note}</small>}
              </span>
              <span className="mb-geo-choice-chip">{marks}m</span>
            </button>
          );
        })}
      </div>
      {directions.length > 0 && (
        <ul className="mb-geo-choice-notes">
          {directions.map((note, index) => <li key={index}>{note}</li>)}
        </ul>
      )}
    </div>
  );
}
