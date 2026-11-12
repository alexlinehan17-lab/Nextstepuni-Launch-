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
import { irishPartCount, irishPartMarks, irishRowClaimed, irishRowPoint, irishRowScoreId, type IrishScores } from './irishScoring';
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
        // A point is claimed once any of its rows is: a group of one point's printed alternatives counts once.
        const claimedPoints = new Set(part.rows.filter(row => irishRowClaimed(criterionId, part, row.id, scores)).map(irishRowPoint));
        const full = claimedPoints.size >= irishPartCount(part);
        const members = (group: string) => part.rows.filter(row => row.group === group);
        return (
          <section className="mb-irish-part" key={part.id} aria-label={part.prompt ?? `Cuid ${part.id}`}>
            <div className="mb-irish-part-head">
              {part.prompt ? <ClaimPart prompt={part.prompt} /> : <span />}
              <span className="mb-claim-chip mb-irish-part-chip" aria-label={`Marks for this sub-question: ${partCaption(part)}`}>{partCaption(part)}</span>
            </div>
            {part.rows.map(row => {
              const claimRow = (member: typeof row) => {
                const id = irishRowScoreId(criterionId, part.id, member.id);
                const isClaimed = irishRowClaimed(criterionId, part, member.id, scores);
                return (
                  <ClaimRow
                    key={id}
                    text={member.text}
                    marks={part.ladder ? undefined : member.marks}
                    steps={member.steps}
                    value={member.steps ? scores[id] ?? 0 : undefined}
                    claimed={isClaimed}
                    tone={!part.ladder && member.marks < part.tariff && !member.steps ? 'partial' : 'full'}
                    disabled={!isClaimed && (full || claimedPoints.has(irishRowPoint(member)))}
                    onToggle={() => onScore(id, isClaimed ? 0 : 1)}
                    onStep={member.steps ? step => onScore(id, step) : undefined}
                  />
                );
              };
              if (!row.group) return claimRow(row);
              // The printed alternatives for one point, together: any one of them earns it.
              const group = members(row.group);
              if (group[0] !== row) return null;
              return (
                <div className="mb-irish-group" key={`${part.id}-${row.group}`} role="group"
                  aria-label={`Any one of these: ${group[0].marks} marks`}>
                  <span className="mb-irish-group-head">{`1 freagra · ${group[0].marks}m`}</span>
                  {group.map(claimRow)}
                </div>
              );
            })}
            {part.samples && <ClaimDirections title="Freagraí samplacha — sampla, ní seicliosta" notes={part.samples} />}
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
