/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of a History essay card: the SEC's marking of an essay.
 *
 * The scheme prints no model answer for an essay. At Higher Level it marks
 * each paragraph on a band ladder (the Cumulative Mark, up to a printed
 * maximum); at Ordinary Level it counts Core Statements at a printed value
 * each; and it marks the answer as a whole on one band (the Overall
 * Evaluation) where it prints one. So the student adds the paragraphs they
 * actually wrote, one at a time, placing each on one band at one of its marks
 * — or counts their Core Statements — and then places the whole answer. Every
 * band, descriptor and direction on this panel is the scheme's own wording;
 * the rows, chips and directions are the shared claim-row parts
 * (ClaimRows.tsx), so a placed band is the same charcoal selection as a
 * claimed answer anywhere else.
 */
import React, { useEffect, useState } from 'react';
import {
  HISTORY_ESSAY_NO_MODEL_ANSWER,
  type HistoryCoreStatementCm, type HistoryEssayRubric, type HistoryParagraphCm, type SecRubricCard,
} from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import { ClaimDirections, ClaimRow, marksChip } from './ClaimRows';
import {
  bandOf,
  historyAddParagraph,
  historyCap,
  historyCapId,
  historyCmTally,
  historyEssayMarks,
  historyIncompleteId,
  historyOeId,
  historyOeMark,
  historyParagraphId,
  historyRemoveParagraph,
  historySetStatements,
  type HistoryEssayScoreId,
  type HistoryEssayScores,
  type HistoryParagraphTally,
  type HistoryStatementTally,
} from './historyEssayScoring';
import './history-essay.css';

interface Props {
  card: SecRubricCard & { rubric: HistoryEssayRubric };
  scores: HistoryEssayScores;
  onScore: (id: HistoryEssayScoreId, marks: number) => void;
}

type Write = (writes: Array<[HistoryEssayScoreId, number]>) => void;

/** Higher Level: one line per paragraph, one ladder open at a time. */
const ParagraphMarking: React.FC<{
  cm: HistoryParagraphCm;
  cardId: string;
  paragraphs: HistoryParagraphTally[];
  scores: HistoryEssayScores;
  onScore: Props['onScore'];
  write: Write;
}> = ({ cm, cardId, paragraphs, scores, onScore, write }) => {
  // The paragraph whose ladder is open. Placing it closes it again, so the
  // list stays one line per paragraph and only one ladder shows at a time.
  const [open, setOpen] = useState<number | null>(null);
  useEffect(() => { setOpen(null); }, [cardId]);
  const count = paragraphs.length;
  return (
    <>
      {count === 0 && (
        <p className="mb-hist-empty">Add the first paragraph of your answer, then place it on a band.</p>
      )}
      <ol className="mb-hist-paragraphs">
        {paragraphs.map(({ n, placed, counted }) => {
          const band = bandOf(cm.bands, placed);
          const editing = open === n || (placed === null && open === null && n === count);
          return (
            <li key={n} className="mb-hist-paragraph" data-open={editing} data-capped={placed !== null && counted !== placed}>
              <div className="mb-hist-paragraph-head">
                <span className="mb-hist-paragraph-name">Paragraph {n}</span>
                <span className="mb-hist-paragraph-state">
                  {placed === null ? 'Not placed yet'
                    : counted === placed ? `${band?.label} · ${marksChip(placed)}`
                      : counted === 0 ? `${band?.label} · ${marksChip(placed)} · past the CM maximum, counts 0m`
                        : `${band?.label} · ${marksChip(placed)} · counts ${marksChip(counted)} up to the CM maximum`}
                </span>
                <span className="mb-hist-paragraph-actions">
                  {!editing && (
                    <button type="button" onClick={() => setOpen(n)} aria-label={`Change paragraph ${n}`}>Change</button>
                  )}
                  <button
                    type="button"
                    onClick={() => { write(historyRemoveParagraph(scores, n)); setOpen(null); }}
                    aria-label={`Remove paragraph ${n}`}
                  >
                    Remove
                  </button>
                </span>
              </div>
              {editing && (
                <div className="mb-hist-ladder" role="group" aria-label={`Bands for paragraph ${n}`}>
                  {cm.bands.map(item => (
                    <ClaimRow
                      key={item.label}
                      text={item.printed}
                      note={item.descriptor}
                      steps={item.marks}
                      claimed={placed !== null && item.marks.includes(placed)}
                      value={placed ?? -1}
                      onToggle={() => undefined}
                      onStep={step => {
                        onScore(historyParagraphId(n), placed === step ? -1 : step);
                        if (placed !== step) setOpen(null);
                      }}
                    />
                  ))}
                </div>
              )}
            </li>
          );
        })}
      </ol>
      <button
        type="button"
        className="mb-hist-add"
        onClick={() => { write(historyAddParagraph(scores)); setOpen(count + 1); }}
      >
        {count === 0 ? 'Add a paragraph' : 'Add another paragraph'}
      </button>
      <ClaimDirections title="What the scheme counts as a paragraph" notes={[cm.paragraphLead, ...cm.paragraphKinds]} />
    </>
  );
};

/** Ordinary Level: completed Core Statements counted, an incomplete last one placed. */
const CoreStatementMarking: React.FC<{
  cm: HistoryCoreStatementCm;
  statements: HistoryStatementTally;
  onScore: Props['onScore'];
}> = ({ cm, statements, onScore }) => {
  const perStatementLine = cm.procedure.find(line => /Each completed Core Statement is awarded/.test(line)) ?? '';
  const incompleteLine = cm.procedure.find(line => /incomplete Core Statement/.test(line)) ?? '';
  const { completed, incomplete } = statements;
  return (
    <>
      <div className="mb-hist-counter-row" data-claimed={completed > 0}>
        <span className="mb-claim-text">
          <span>{perStatementLine}</span>
          <small>Count the Core Statements you completed.</small>
        </span>
        <span className="mb-hist-counter" role="group" aria-label="Completed Core Statements">
          <button type="button" aria-label="One fewer Core Statement" disabled={completed <= 0}
            onClick={() => onScore(...historySetStatements(completed - 1))}>−</button>
          <output aria-live="polite">{completed}</output>
          <button type="button" aria-label="One more Core Statement"
            onClick={() => onScore(...historySetStatements(completed + 1))}>+</button>
        </span>
        <span className="mb-claim-chip">{marksChip(statements.completedMarks)}</span>
      </div>
      <div className="mb-hist-ladder">
        <ClaimRow
          text={incompleteLine}
          steps={cm.incomplete}
          claimed={incomplete !== null}
          value={incomplete ?? -1}
          onToggle={() => undefined}
          onStep={step => onScore(historyIncompleteId, incomplete === step ? -1 : step)}
        />
      </div>
      <ClaimDirections title="What the scheme counts as a Core Statement" notes={[cm.statementLead, ...cm.statementKinds]} />
      <ClaimDirections title="How the examiner marks by Core Statement" notes={[cm.procedureLead, ...cm.procedure]} />
    </>
  );
};

const HistoryEssayPanel: React.FC<Props> = ({ card, scores, onScore }) => {
  const { rubric } = card;
  const { cm, oe } = rubric;
  const tally = historyCmTally(rubric, scores);
  const oeMark = historyOeMark(rubric, scores);
  const cap = historyCap(rubric, scores);
  const write: Write = writes => writes.forEach(([id, value]) => onScore(id, value));
  const placedAny = tally.paragraphs.length > 0 || (tally.statements?.raw ?? 0) > 0;
  const overCeiling = tally.statements ? tally.statements.raw > tally.ceiling : false;

  return (
    <div className="mb-hist-essay">
      <p className="mb-hist-eyebrow">SEC History marking scheme</p>
      <h3>
        {cm.mode === 'paragraph'
          ? 'Place each paragraph you wrote on the scheme’s bands, then place your whole answer.'
          : oe ? 'Count the Core Statements you wrote, then place your whole answer.'
            : 'Count the Core Statements you wrote.'}
      </h3>

      <section className="mb-hist-nomodel" aria-label="How the scheme marks this answer">
        <strong>{HISTORY_ESSAY_NO_MODEL_ANSWER}</strong>
        {rubric.schemeGuidance.map((line, index) => <p key={index}>{line}</p>)}
      </section>

      {cm.elementRule && (
        <section className="mb-hist-element" aria-label="This question's note">
          <ClaimDirections title="This question’s note in the scheme" notes={[cm.elementRule.note]} />
          {cm.elementRule.caps.map((item, index) => (
            <ClaimRow
              key={item.when}
              text={`In my judgement, the note’s “${item.when}” applies to my answer.`}
              note={`Your call, not the scheme’s. It sets your CM maximum to ${item.max}, as the note says.`}
              claimed={cap === item}
              onToggle={() => onScore(historyCapId, cap === item ? 0 : index + 1)}
            />
          ))}
        </section>
      )}

      <section className="mb-hist-part" aria-label="Cumulative Mark">
        <div className="mb-hist-part-head">
          <h4>
            <span>Cumulative Mark (CM)</span>
            <small>{cm.definition}</small>
          </h4>
          <span className="mb-claim-chip mb-hist-chip">{tally.cm} / {tally.ceiling}</span>
        </div>
        {cm.mode === 'paragraph' ? (
          <ParagraphMarking cm={cm} cardId={card.id} paragraphs={tally.paragraphs} scores={scores} onScore={onScore} write={write} />
        ) : (
          <CoreStatementMarking cm={cm} statements={tally.statements!} onScore={onScore} />
        )}
        {placedAny && tally.cm >= tally.ceiling && (
          <p className="mb-hist-reached">
            Your CM has reached its maximum of {tally.ceiling}.
            {' '}{cm.mode === 'paragraph' ? 'A further paragraph counts 0m.' : 'A further Core Statement counts 0m.'}
            {overCeiling && ` You placed ${marksChip(tally.statements!.raw)}; ${marksChip(tally.ceiling)} counts.`}
          </p>
        )}
        <ClaimDirections notes={cm.directions} />
      </section>

      {oe && (
        <section className="mb-hist-part" aria-label="Overall Evaluation">
          <div className="mb-hist-part-head">
            <h4>
              <span>Overall Evaluation (OE)</span>
              {(oe.definition ?? oe.lead) && <small>{oe.definition ?? oe.lead}</small>}
            </h4>
            <span className="mb-claim-chip mb-hist-chip">{oeMark ?? 0} / {oe.max}</span>
          </div>
          <div className="mb-hist-ladder mb-hist-ladder--stacked" role="group" aria-label="Overall Evaluation bands">
            {oe.bands.map(item => (
              <ClaimRow
                key={item.label}
                text={item.printed}
                note={item.descriptor}
                steps={item.marks}
                claimed={oeMark !== null && item.marks.includes(oeMark)}
                value={oeMark ?? -1}
                onToggle={() => undefined}
                onStep={step => onScore(historyOeId, oeMark === step ? -1 : step)}
              />
            ))}
          </div>
          {oe.directions.length > 0 && (
            <ClaimDirections title={oe.directionsLead ?? 'Examiner directions'} notes={oe.directions} />
          )}
        </section>
      )}

      <div className="mb-hist-total" aria-live="polite">
        <span>Your placement · CM {tally.cm}{oe ? ` + OE ${oeMark ?? 0}` : ''}</span>
        <strong>{historyEssayMarks(card, scores)} / {card.totalMarks}</strong>
      </div>
      <p className="mb-hist-note">{rubric.markingGuideNote}</p>
      <SourceMaterialReader
        subjectId={card.subjectId}
        year={card.year}
        paperFileid={rubric.schemeFileid}
        documentKind="scheme"
        source={{
          kind: 'source-data', label: 'the official scheme', title: card.questionRef,
          pages: rubric.schemePages,
          attribution: '© State Examinations Commission',
          presentationNote: 'The printed marking for this question, as the scheme sets it out.',
        }}
      />
    </div>
  );
};

export default HistoryEssayPanel;
