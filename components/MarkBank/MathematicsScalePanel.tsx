import React from 'react';
import type { CardFigure, SecPointCardBase } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import MathematicsWorkedSolution from './MathematicsWorkedSolution';
import MathematicsDeductionsPanel, { deductionTotal } from './MathematicsDeductionsPanel';

export type MathematicsScaleCard = SecPointCardBase & {
  mathematicsScale: NonNullable<SecPointCardBase['mathematicsScale']>;
  figure?: CardFigure;
};
type ComponentScores = Partial<Record<`mathematics:${string}`, number>>;

export function mathematicsScaleMarks(card: MathematicsScaleCard, selected?: number, scores: ComponentScores = {}): number {
  const scale = card.mathematicsScale;
  if (scale.methods) return deductionTotal(scale.methods, scores);
  if (scale.components) {
    const total = scale.components.reduce((sum, component) => {
      const award = scores[`mathematics:${component.id}`];
      const valid = award !== undefined && (component.marks.includes(award)
        || (component.fullCreditMinusOne && award === component.marks.at(-1)! - 1));
      return sum + (valid ? award! : 0);
    }, 0);
    // The 2015 general notes allow one deduction per printed part, never one
    // per component. Full Credit −1 only applies to an otherwise full response.
    return total - (scale.fullCreditMinusOne && total === card.totalMarks && scores['mathematics:deduction'] === 1 ? 1 : 0);
  }
  if (selected === undefined) return 0;
  return scale.marks.includes(selected)
    || (scale.fullCreditMinusOne && selected === card.totalMarks - 1)
    ? selected : 0;
}

const creditChoices = (marks: number[], fullCreditMinusOne: boolean) => {
  const labels = marks.length === 2 ? ['No credit', 'Full credit']
    : marks.length === 3 ? ['No credit', 'Partial credit', 'Full credit']
      : marks.length === 4 ? ['No credit', 'Low partial credit', 'High partial credit', 'Full credit']
        : marks.length === 5 ? ['No credit', 'Low partial credit', 'Mid partial credit', 'High partial credit', 'Full credit']
          : ['No credit', 'Low partial credit', 'Low mid partial credit', 'High mid partial credit', 'High partial credit', 'Full credit'];
  const choices = marks.map((award, index) => ({ marks: award, label: labels[index] }));
  const maximum = marks.at(-1)!;
  if (fullCreditMinusOne && !marks.includes(maximum - 1)) choices.splice(-1, 0, { marks: maximum - 1, label: 'Full credit −1' });
  return choices;
};

/** One band per published scale. Examples within a band are not extra points. */
const MathematicsScalePanel: React.FC<{
  card: MathematicsScaleCard;
  selected?: number;
  onSelect: (marks: number) => void;
  componentScores?: ComponentScores;
  onComponentSelect?: (id: string, marks: number) => void;
}> = ({ card, selected, onSelect, componentScores = {}, onComponentSelect }) => {
  const scale = card.mathematicsScale;
  if (scale.methods) return <section className="mb-maths-scale" aria-label="SEC step marks and deductions">
    {card.figure?.solution && <MathematicsWorkedSolution figure={card.figure} />}
    <SourceMaterialReader subjectId={card.subjectId} year={card.year} paperFileid={card.paperFileid ?? scale.schemeFileid}
      source={{kind: 'source-scheme', documentKind: 'scheme', label: 'SEC STEP MARKS', title: 'Worked solution and marking notes',
        pages: [...new Set([...scale.schemePages, ...scale.generalNotesPages])], sourceFileid: scale.schemeFileid,
        attribution: card.schemeCitation, presentationNote: 'The complete official methods, step allocations and deductions, followed by the general marking rules.'}} />
    <MathematicsDeductionsPanel cardId={card.id} methods={scale.methods} totalMarks={card.totalMarks}
      markingNote={scale.markingNote} scores={componentScores} onSelect={onComponentSelect} />
  </section>;
  const componentMode = !!scale.components;
  const bands = scale.components ?? [{ id: 'whole', label: 'Credit awarded', code: scale.code, marks: scale.marks, fullCreditMinusOne: scale.fullCreditMinusOne }];
  const fullyAwarded = scale.components?.every(component => componentScores[`mathematics:${component.id}`] === component.marks.at(-1));
  return (
    <section className="mb-maths-scale" aria-label={componentMode ? 'SEC component scales' : `SEC scale ${scale.code}`}>
      {card.figure?.solution && <MathematicsWorkedSolution figure={card.figure} />}
      <h3>Select the credit your working earns.</h3>
      <p>{componentMode ? 'This is one complete question. Choose the credit earned for each component; the awards add to your total.'
        : `Read the worked solution and marking notes, then choose one award on scale ${scale.code}.`}</p>
      <SourceMaterialReader
        subjectId={card.subjectId} year={card.year} paperFileid={card.paperFileid ?? scale.schemeFileid}
        source={{
          kind: 'source-scheme', documentKind: 'scheme',
          label: componentMode ? 'SEC COMPONENT SCALES' : `SEC SCALE ${scale.code}`, title: 'Worked solution and marking notes',
          pages: [...new Set([...scale.schemePages, ...scale.generalNotesPages])],
          sourceFileid: scale.schemeFileid, attribution: card.schemeCitation,
          presentationNote: 'The task-specific solution and credit notes come first, followed by the general marking rules.',
        }}
      />
      {scale.markingNote && <p className="mb-maths-scale-note">{scale.markingNote}</p>}
      {bands.map(band => <fieldset key={band.id}>
        <legend>{componentMode ? `${band.label} · ${band.code}` : 'Credit awarded'}</legend>
        {creditChoices(band.marks, componentMode ? !!band.fullCreditMinusOne : scale.fullCreditMinusOne).map(choice => {
          const checked = (componentMode ? componentScores[`mathematics:${band.id}`] : selected) === choice.marks;
          return <label key={choice.marks} className={checked ? 'is-selected' : ''}>
            <input type="radio" name={`maths-scale-${card.id}-${band.id}`} value={choice.marks}
              aria-label={`${choice.label}, ${choice.marks} of ${band.marks.at(-1)} marks`}
              checked={checked} onChange={() => componentMode ? onComponentSelect?.(band.id, choice.marks) : onSelect(choice.marks)} />
            <span>{choice.label}</span><strong>{choice.marks} / {band.marks.at(-1)}</strong>
          </label>;
        })}
        {componentMode && band.fullCreditMinusOne && <p className="mb-maths-scale-note">
          Full Credit −1 applies to this component only. Check its SEC marking notes before selecting {band.marks.at(-1)! - 1} marks.
        </p>}
      </fieldset>)}
      {componentMode && <p className="mb-maths-scale-total" aria-live="polite"><strong>Total: {mathematicsScaleMarks(card, undefined, componentScores)} / {card.totalMarks} marks</strong></p>}
      {componentMode && scale.fullCreditMinusOne && <label className="mb-maths-scale-deduction">
        <input type="checkbox" disabled={!fullyAwarded} checked={!!fullyAwarded && componentScores['mathematics:deduction'] === 1}
          onChange={event => onComponentSelect?.('deduction', event.target.checked ? 1 : 0)} />
        Apply one minor-error deduction (−1), only where the SEC notes allow it.
      </label>}
      {scale.fullCreditMinusOne && (
        <p className="mb-maths-scale-note">{componentMode
          ? 'Full Credit −1 applies to an otherwise full-credit response. Check the task-specific and general SEC notes; apply the deduction once for this whole part, not once per component.'
          : `Full Credit −1 follows the task-specific and general SEC notes. It can cover a minor error or an explicitly listed omission. Check those notes before selecting ${card.totalMarks - 1} marks.`}</p>
      )}
    </section>
  );
};

export default MathematicsScalePanel;
