import React from 'react';
import type { SecPointCardBase } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';

export type MathematicsScaleCard = SecPointCardBase & {
  mathematicsScale: NonNullable<SecPointCardBase['mathematicsScale']>;
};

export function mathematicsScaleMarks(card: MathematicsScaleCard, selected?: number): number {
  if (selected === undefined) return 0;
  const scale = card.mathematicsScale;
  return scale.marks.includes(selected)
    || (scale.fullCreditMinusOne && selected === card.totalMarks - 1)
    ? selected : 0;
}

/** A scale awards one band for the whole response. Its examples are not points
 * that can be added together, and Full Credit −1 has specific SEC conditions. */
const MathematicsScalePanel: React.FC<{
  card: MathematicsScaleCard;
  selected?: number;
  onSelect: (marks: number) => void;
}> = ({ card, selected, onSelect }) => {
  const scale = card.mathematicsScale;
  const labels = scale.marks.length === 2 ? ['No credit', 'Full credit']
    : scale.marks.length === 3 ? ['No credit', 'Partial credit', 'Full credit']
      : scale.marks.length === 4 ? ['No credit', 'Low partial credit', 'High partial credit', 'Full credit']
        : ['No credit', 'Low partial credit', 'Mid partial credit', 'High partial credit', 'Full credit'];
  const choices = scale.marks.map((marks, index) => ({ marks, label: labels[index] }));
  if (scale.fullCreditMinusOne && !scale.marks.includes(card.totalMarks - 1)) {
    choices.splice(-1, 0, { marks: card.totalMarks - 1, label: 'Full credit −1' });
  }
  return (
    <section className="mb-maths-scale" aria-label={`SEC scale ${scale.code}`}>
      <h3>Select the credit your working earns.</h3>
      <p>Read the worked solution and marking notes, then choose one award on scale {scale.code}.</p>
      <SourceMaterialReader
        subjectId={card.subjectId} year={card.year} paperFileid={card.paperFileid ?? scale.schemeFileid}
        source={{
          kind: 'source-scheme', documentKind: 'scheme',
          label: `SEC SCALE ${scale.code}`, title: 'Worked solution and marking notes',
          pages: [...new Set([...scale.schemePages, ...scale.generalNotesPages])],
          sourceFileid: scale.schemeFileid, attribution: card.schemeCitation,
          presentationNote: 'The task-specific solution and credit notes come first, followed by the general marking rules.',
        }}
      />
      <fieldset>
        <legend>Credit awarded</legend>
        {choices.map(choice => (
          <label key={choice.marks} className={selected === choice.marks ? 'is-selected' : ''}>
            <input type="radio" name={`maths-scale-${card.id}`} value={choice.marks}
              aria-label={`${choice.label}, ${choice.marks} of ${card.totalMarks} marks`}
              checked={selected === choice.marks} onChange={() => onSelect(choice.marks)} />
            <span>{choice.label}</span><strong>{choice.marks} / {card.totalMarks}</strong>
          </label>
        ))}
      </fieldset>
      {scale.fullCreditMinusOne && (
        <p className="mb-maths-scale-note">Full Credit −1 follows the task-specific and general SEC notes. It can cover a minor error or an explicitly listed omission. Check those notes before selecting {card.totalMarks - 1} marks.</p>
      )}
    </section>
  );
};

export default MathematicsScalePanel;
