/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The claimable-row vocabulary every rubric subject shares once its scheme is
 * cut into rows (Geography since #265, French since this file): a row is a
 * button carrying the scheme's answer and its marks, a stepped row offers the
 * printed values it can take, a mark strip places a criterion on its permitted
 * marks, and the examiner's directions are a short list underneath, never the
 * thing a student has to read to find the answer.
 */
import React from 'react';
import './claim-rows.css';

const Tick: React.FC = () => (
  <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">
    <path d="M2.5 6.2l2.4 2.4L9.5 3.9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

/** "3m", "−1m" for a deduction, "0m" for an answer the scheme prices at zero. */
export const marksChip = (marks: number) => (marks < 0 ? `−${-marks}m` : `${marks}m`);

export type ClaimTone = 'full' | 'partial' | 'deduction';

export const ClaimRow: React.FC<{
  text: string;
  /** The row's price; left out when a ladder prices the list as a whole. */
  marks?: number;
  /** Printed values the row can take instead of one price (cloze: 3 or 2). */
  steps?: number[];
  claimed: boolean;
  /** The step a stepped row sits on, 0 when unclaimed. */
  value?: number;
  /** A line under the answer: a scheme fact about the row, never an example. */
  note?: string;
  tag?: string;
  tone?: ClaimTone;
  disabled?: boolean;
  onToggle: () => void;
  onStep?: (step: number) => void;
}> = ({ text, marks, steps, claimed, value = 0, note, tag, tone = 'full', disabled, onToggle, onStep }) => {
  if (steps && onStep) {
    return (
      <div className="mb-claim-row mb-claim-row--stepped" data-claimed={claimed} data-tone={tone}>
        <span className="mb-claim-text">
          {tag && <span className="mb-claim-tag">{tag}</span>}
          <span dir="auto">{text}</span>
          {note && <small>{note}</small>}
        </span>
        <span className="mb-claim-steps" role="group" aria-label={`Marks for ${text}`}>
          {steps.map(step => (
            <button
              key={step}
              type="button"
              disabled={disabled}
              aria-pressed={value === step}
              aria-label={`${value === step ? 'Clear' : 'Claim'} ${step} marks for ${text}`}
              onClick={() => onStep(step)}
            >
              {step}m
            </button>
          ))}
        </span>
      </div>
    );
  }
  return (
    <button
      type="button"
      className="mb-claim-row"
      data-claimed={claimed}
      data-tone={tone}
      aria-pressed={claimed}
      aria-label={marks === undefined ? text : `${text} · ${marksChip(marks)}`}
      disabled={disabled && !claimed}
      onClick={onToggle}
    >
      <span className="mb-claim-check" aria-hidden="true">{claimed && <Tick />}</span>
      <span className="mb-claim-text">
        {tag && <span className="mb-claim-tag">{tag}</span>}
        <span dir="auto">{text}</span>
        {note && <small>{note}</small>}
      </span>
      {marks !== undefined && <span className="mb-claim-chip">{marksChip(marks)}</span>}
    </button>
  );
};

/** A sub-part heading over a run of rows: the scheme's "(a)" or "(ii) Restaurant", the paper's sub-question. */
export const ClaimPart: React.FC<{ label?: string; prompt?: string }> = ({ label, prompt }) => (
  <h4 className="mb-claim-part">
    {label && <span>{label}</span>}
    {prompt && <span>{prompt}</span>}
  </h4>
);

/** The permitted marks of one criterion as buttons; the selected one is ink. */
export const MarkStrip: React.FC<{
  label: string;
  marks: readonly number[];
  selected: number;
  disabled?: boolean;
  onSelect: (mark: number) => void;
}> = ({ label, marks, selected, disabled, onSelect }) => (
  <div className="mb-claim-marks" role="group" aria-label={`${label} mark`}>
    {marks.map(mark => (
      <button
        key={mark}
        type="button"
        disabled={disabled}
        aria-pressed={selected === mark}
        aria-label={`Set ${label} to ${mark} marks`}
        onClick={() => onSelect(mark)}
      >
        {mark}
      </button>
    ))}
  </div>
);

export const ClaimDirections: React.FC<{ title?: string; notes: readonly string[] }> = ({ title = 'Examiner directions', notes }) => (
  notes.length === 0 ? null : (
    <aside className="mb-claim-directions">
      <strong>{title}</strong>
      <ul>
        {notes.map((note, index) => <li key={index}>{note}</li>)}
      </ul>
    </aside>
  )
);
