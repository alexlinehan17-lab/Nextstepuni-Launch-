/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of an unseen-translation card: the passage as the scheme
 * cuts it, unit by unit, with the marks the scheme writes after each unit.
 *
 * The scheme prints no model translation, so there is no answer to show. What
 * it does print is where each unit of meaning ends, what it is worth, and the
 * rule for full and partial marks. The student reads each unit beside their
 * own translation and marks it: Full, Partial (then a whole mark below full),
 * or None. Every unit's words, every mark and every line of the rule are the
 * scheme's own; the only words that are NextStepUni's are the button labels
 * and TRANSLATION_NO_MODEL.
 */
import React, { useEffect, useState } from 'react';
import { TRANSLATION_NO_MODEL, type SecRubricCard, type TranslationRubric, type TranslationUnit } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import { marksChip, marksLabel } from './ClaimRows';
import {
  partialSteps,
  translationMarks,
  translationTally,
  translationUnitId,
  translationUnitMark,
  type TranslationScoreId,
  type TranslationScores,
} from './translationScoring';
import './translation.css';

interface Props {
  card: SecRubricCard & { rubric: TranslationRubric };
  scores: TranslationScores;
  onScore: (id: TranslationScoreId, marks: number) => void;
}

const Tick: React.FC = () => (
  <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">
    <path d="M2.5 6.2l2.4 2.4L9.5 3.9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const UnitRow: React.FC<{
  unit: TranslationUnit;
  index: number;
  lang: string;
  mark: number | null;
  onScore: Props['onScore'];
}> = ({ unit, index, lang, mark, onScore }) => {
  const isPartial = mark !== null && mark > 0 && mark < unit.marks;
  // "Partial" opens the whole marks below full; it stays open while a partial
  // mark is placed, and closes when Full or None is chosen instead.
  const [partialOpen, setPartialOpen] = useState(isPartial);
  useEffect(() => { if (isPartial) setPartialOpen(true); }, [isPartial]);
  const id = translationUnitId(unit);
  const set = (value: number) => onScore(id, mark === value ? -1 : value);
  const name = `unit ${index + 1}`;
  return (
    <li className="mb-tr-unit" data-marked={mark !== null}>
      <div className="mb-tr-unit-head">
        <span className="mb-tr-unit-name">Unit {index + 1}</span>
        <span className="mb-claim-chip">{marksLabel(unit.marks)}</span>
      </div>
      <p className="mb-tr-unit-text" lang={lang} dir="auto">{unit.text}</p>
      <div className="mb-tr-choices" role="group" aria-label={`Marks for ${name}`}>
        <button type="button" aria-pressed={mark === unit.marks}
          aria-label={`${mark === unit.marks ? 'Clear' : 'Claim'} full marks, ${unit.marks}, for ${name}`}
          onClick={() => { setPartialOpen(false); set(unit.marks); }}>
          {mark === unit.marks && <Tick />}Full · {marksChip(unit.marks)}
        </button>
        {unit.marks > 1 && (
          <button type="button" aria-pressed={partialOpen || isPartial} aria-expanded={partialOpen || isPartial}
            aria-label={`Partial marks for ${name}`}
            onClick={() => {
              if (isPartial) { onScore(id, -1); setPartialOpen(false); } else setPartialOpen(open => !open);
            }}>
            {isPartial && <Tick />}{isPartial ? `Partial · ${marksChip(mark!)}` : 'Partial'}
          </button>
        )}
        <button type="button" aria-pressed={mark === 0}
          aria-label={`${mark === 0 ? 'Clear' : 'Claim'} no marks for ${name}`}
          onClick={() => { setPartialOpen(false); set(0); }}>
          {mark === 0 && <Tick />}None · 0m
        </button>
      </div>
      {(partialOpen || isPartial) && unit.marks > 1 && (
        <div className="mb-tr-partial">
          <span>How many of the {unit.marks} marks?</span>
          <div className="mb-claim-steps" role="group" aria-label={`Partial marks for ${name}`}>
            {partialSteps(unit).map(step => (
              <button key={step} type="button" aria-pressed={mark === step}
                aria-label={`${mark === step ? 'Clear' : 'Claim'} ${step} marks for ${name}`}
                onClick={() => set(step)}>
                {mark === step && <Tick />}{step}m
              </button>
            ))}
          </div>
        </div>
      )}
    </li>
  );
};

const TranslationPanel: React.FC<Props> = ({ card, scores, onScore }) => {
  const { rubric } = card;
  const tally = translationTally(rubric, scores);
  return (
    <div className="mb-tr">
      <p className="mb-tr-eyebrow">SEC marking scheme · unit by unit</p>
      <h3>Mark your translation one unit at a time.</h3>

      <section className="mb-tr-rule" aria-label="How the scheme marks this translation">
        <strong>{TRANSLATION_NO_MODEL}</strong>
        <p>It cuts the passage into units of meaning and writes a mark after each one. Its rule for marking a unit:</p>
        <ul>
          {rubric.schemeGuidance.map((line, index) => <li key={index}>{line}</li>)}
        </ul>
      </section>

      <div className="mb-tr-progress" aria-live="polite">
        <span>{tally.marked} of {tally.units} units marked</span>
      </div>

      <ol className="mb-tr-units">
        {rubric.units.map((unit, index) => (
          <UnitRow key={unit.id} unit={unit} index={index} lang={rubric.sourceLanguage}
            mark={translationUnitMark(unit, scores)} onScore={onScore} />
        ))}
      </ol>

      <div className="mb-tr-total" aria-live="polite">
        <span>Your marks · {tally.marked} of {tally.units} units marked</span>
        <strong>{translationMarks(card, scores)} / {card.totalMarks}</strong>
      </div>
      <p className="mb-tr-note">{rubric.markingGuideNote}</p>
      <SourceMaterialReader
        subjectId={card.subjectId}
        year={card.year}
        paperFileid={rubric.schemeFileid}
        documentKind="scheme"
        source={{
          kind: 'source-data', label: 'the official scheme', title: card.questionRef,
          pages: rubric.schemePages,
          attribution: '© State Examinations Commission',
          presentationNote: 'The units and marks for this passage, as the scheme prints them.',
        }}
      />
    </div>
  );
};

export default TranslationPanel;
