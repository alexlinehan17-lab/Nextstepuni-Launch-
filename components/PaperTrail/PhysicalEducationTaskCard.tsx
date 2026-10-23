/** @license SPDX-License-Identifier: Apache-2.0 */
import React, { useState } from 'react';
import { REVIEWED_CARDS } from '../MarkBank/cards/physical-education/factory';
import SourceMaterialReader from '../MarkBank/SourceMaterialReader';
import PhysicalEducationRubricPanel from '../MarkBank/PhysicalEducationRubricPanel';
import type { PhysicalEducationScoreId } from '../MarkBank/physicalEducationScoring';
import type { PhysicalEducationTask } from './physicalEducationTasks';
import './physical-education-tasks.css';

interface Props {
  task: PhysicalEducationTask;
  saved: boolean;
  onToggleReview: () => void;
  onOpenInPaper: () => void;
}

/** Same task, source pages and marking criteria as Mark Bank. Its distinct
 * identity also survives saving to daily review or a custom practice set. */
export default function PhysicalEducationTaskCard({ task, saved, onToggleReview, onOpenInPaper }: Props) {
  const [revealed, setRevealed] = useState(false);
  const [scores, setScores] = useState<Partial<Record<PhysicalEducationScoreId, number>>>({});
  const card = REVIEWED_CARDS.find(item => item.id === task.cardId);
  if (!card || !card.sourceMaterial || !card.paperFileid) return <button onClick={onOpenInPaper}>Open {task.questionRef} in the full paper</button>;
  return (
    <article className="pt-pe-task mark-bank-theme" aria-label={`${card.questionRef} · ${task.n}`}>
      <header className="pt-pe-task-heading">
        <p><strong>{task.year}</strong> · {task.level === 'higher' ? 'Higher' : 'Ordinary'} · Question {task.n}</p>
        <span>{card.totalMarks} marks</span>
      </header>
      <div className="pt-pe-task-body">
        {card.stem && <p className="pt-pe-task-context">{card.stem}</p>}
        <p className="pt-pe-task-prompt">{card.questionText}</p>
        <SourceMaterialReader source={card.sourceMaterial} subjectId={card.subjectId} year={card.year} paperFileid={card.paperFileid} />
        <div className="pt-pe-task-actions">
          <button type="button" onClick={onToggleReview} aria-pressed={saved}>{saved ? 'Saved to daily review' : 'Add to daily review'}</button>
          <button type="button" onClick={onOpenInPaper}>Full paper</button>
        </div>
        <button type="button" className="pt-pe-task-reveal" aria-expanded={revealed} onClick={() => setRevealed(value => !value)}>
          {revealed ? 'Hide marking scheme' : 'Show marking scheme'}
        </button>
        {revealed && <PhysicalEducationRubricPanel card={card} scores={scores} onScore={(id, marks) => setScores(current => ({ ...current, [id]:marks }))} />}
      </div>
    </article>
  );
}
