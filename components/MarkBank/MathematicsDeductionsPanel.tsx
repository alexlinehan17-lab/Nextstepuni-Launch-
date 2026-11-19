import React from 'react';
import type { MathematicsDeductionComponent, MathematicsDeductionMethod } from '../../types/markBank';

export type MathematicsComponentScores = Partial<Record<`mathematics:${string}`, number>>;

export function deductionAwards(component: MathematicsDeductionComponent): number[] {
  if (component.permittedMarks) return component.permittedMarks;
  return component.attempt === 0 ? [0, component.maximum]
    : [0, ...Array.from({ length: component.maximum - component.attempt + 1 }, (_, i) => component.attempt + i)];
}

export function deductionTotal(methods: MathematicsDeductionMethod[], scores: MathematicsComponentScores): number {
  const index = scores['mathematics:method'] ?? 0;
  if (!Number.isInteger(index) || !methods[index]) return 0;
  const method = methods[index];
  return method.components.reduce((total, component) => {
    const award = scores[`mathematics:${method.id}:${component.id}`];
    return total + (award !== undefined && deductionAwards(component).includes(award) ? award : 0);
  }, 0);
}

/** Older SEC schemes award named steps after deductions, not credit bands.
 * The learner compares their work with the complete official notes; this UI
 * does not infer which errors they made or stack incompatible methods. */
const MathematicsDeductionsPanel: React.FC<{
  cardId: string;
  methods: MathematicsDeductionMethod[];
  totalMarks: number;
  markingNote?: string;
  scores: MathematicsComponentScores;
  onSelect?: (id: string, marks: number) => void;
}> = ({ cardId, methods, totalMarks, markingNote, scores, onSelect }) => {
  const methodIndex = scores['mathematics:method'] ?? 0;
  const method = methods[methodIndex] ?? methods[0];
  const hasDeductions = method.components.some(component => component.attempt > 0 && !component.permittedMarks);
  return <div className="mb-maths-deductions">
    <h3>Mark the steps in your working.</h3>
    {hasDeductions && <><p>Use the printed marking notes for each step. A mathematical error normally loses 3 marks;
      a numerical slip or permitted misreading loses 1. Apply the task’s specific rules first.</p>
    <p>A correct, relevant step earns at least its attempt mark. An answer with no creditworthy work earns 0.
      Do not deduct for the same error twice in the same section.</p></>}
    {markingNote && <p className="mb-maths-scale-note">{markingNote}</p>}
    {methods.length > 1 && <fieldset className="mb-maths-methods">
      <legend>Choose the method you used</legend>
      {methods.map((candidate, index) => <label key={candidate.id} className={methodIndex === index ? 'is-selected' : ''}>
        <input type="radio" name={`maths-method-${cardId}`} checked={methodIndex === index}
          onChange={() => onSelect?.('method', index)} />
        <span>{candidate.label}</span>
      </label>)}
    </fieldset>}
    {method.components.map(component => {
      const selected = scores[`mathematics:${method.id}:${component.id}`];
      return <fieldset key={`${method.id}:${component.id}`} className="mb-maths-step">
        <legend>{component.label} · {component.maximum} marks</legend>
        <p>{component.permittedMarks ? `The scheme awards only ${component.permittedMarks.join(', ')} marks for this step.`
          : component.attempt === 0 ? 'All or nothing: the SEC awards full marks or 0 for this step.'
          : `Attempt mark: ${component.attempt}. Apply deductions, but never award between 0 and ${component.attempt}.`}</p>
        <div className="mb-maths-step-awards">
          {deductionAwards(component).map(award => <label key={award} className={selected === award ? 'is-selected' : ''}>
            <input type="radio" name={`maths-step-${cardId}-${method.id}-${component.id}`}
              aria-label={`${component.label}: ${award} of ${component.maximum} marks`}
              checked={selected === award} onChange={() => onSelect?.(`${method.id}:${component.id}`, award)} />
            <strong>{award}</strong>
            <span>{award === 0 ? 'No credit' : award === component.maximum ? 'Full' : award === component.attempt ? 'Attempt' : 'marks'}</span>
          </label>)}
        </div>
      </fieldset>;
    })}
    <p className="mb-maths-scale-total" aria-live="polite"><strong>Total: {deductionTotal(methods, scores)} / {totalMarks} marks</strong></p>
  </div>;
};

export default MathematicsDeductionsPanel;
