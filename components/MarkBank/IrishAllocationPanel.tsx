/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of an Irish exact criterion whose scheme has been cut
 * into sub-questions and rows (cards/irish/answers.ts): each sub-question
 * carries the scheme's own prompt and tariff, each answer is a button with
 * its marks, a ladder prices a list by how many are right, and the scheme's
 * rule sentences are a short list underneath.
 */
import React from 'react';
import type { IrishAllocation, IrishAnswerPart } from '../../types/markBank';
import { irishPartCount, irishPartMarks, irishRowClaimed, irishRowScoreId, type IrishScores } from './irishScoring';
import { ClaimDirections, ClaimPart, ClaimRow, marksChip } from './ClaimRows';
import './irish-allocation.css';

interface Props {
  criterionId: string;
  allocation: IrishAllocation;
  scores: IrishScores;
  onScore: (id: string, marks: number) => void;
}

const partCaption = (part: IrishAnswerPart): string => {
  if (part.ladder) return part.ladder.map((marks, index) => `${index + 1} ceart · ${marks}m`).join(' · ');
  const count = irishPartCount(part);
  return count > 1 ? `${count} freagra · ${part.tariff}m` : `${part.tariff}m`;
};

export default function IrishAllocationPanel({ criterionId, allocation, scores, onScore }: Props) {
  return (
    <div className="mb-irish-alloc">
      {allocation.parts.map(part => {
        const claimed = part.rows.filter(row => irishRowClaimed(criterionId, part, row.id, scores)).length;
        const full = claimed >= irishPartCount(part);
        return (
          <section className="mb-irish-part" key={part.id} aria-label={part.prompt ?? `Cuid ${part.id}`}>
            <div className="mb-irish-part-head">
              {part.prompt ? <ClaimPart prompt={part.prompt} /> : <span />}
              <span className="mb-claim-chip mb-irish-part-chip" aria-label={`Marks for this sub-question: ${partCaption(part)}`}>{partCaption(part)}</span>
            </div>
            {part.rows.map(row => {
              const id = irishRowScoreId(criterionId, part.id, row.id);
              const isClaimed = irishRowClaimed(criterionId, part, row.id, scores);
              return (
                <ClaimRow
                  key={id}
                  text={row.text}
                  marks={part.ladder ? undefined : row.marks}
                  claimed={isClaimed}
                  tone={!part.ladder && row.marks < part.tariff ? 'partial' : 'full'}
                  disabled={full && !isClaimed}
                  onToggle={() => onScore(id, isClaimed ? 0 : 1)}
                />
              );
            })}
            <div className="mb-irish-part-total">
              <span>An chuid seo</span>
              <strong>{marksChip(irishPartMarks(criterionId, part, scores))}</strong>
            </div>
          </section>
        );
      })}
      <ClaimDirections title="Treoracha an scrúdaitheora" notes={allocation.directions} />
    </div>
  );
}
