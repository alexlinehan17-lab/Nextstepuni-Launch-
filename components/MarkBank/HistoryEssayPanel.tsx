/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of a History essay card: the SEC's marking by paragraph.
 *
 * The scheme prints no model answer for an essay. It marks each paragraph on
 * a band ladder (the Cumulative Mark, up to a printed maximum) and the answer
 * as a whole on one band (the Overall Evaluation). So the student adds the
 * paragraphs they actually wrote, one at a time, places each on one band at
 * one of its marks, and then places the whole answer. Every band, descriptor
 * and direction on this panel is the scheme's own wording; the rows, chips
 * and directions are the shared claim-row parts (ClaimRows.tsx), so a placed
 * band is the same charcoal selection as a claimed answer anywhere else.
 */
import React, { useEffect, useState } from 'react';
import { HISTORY_ESSAY_NO_MODEL_ANSWER, type HistoryEssayRubric, type SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import { ClaimDirections, ClaimRow, marksChip } from './ClaimRows';
import {
  bandOf,
  historyAddParagraph,
  historyCmTally,
  historyEssayMarks,
  historyOeId,
  historyOeMark,
  historyOneElement,
  historyOneElementId,
  historyParagraphId,
  historyRemoveParagraph,
  type HistoryEssayScoreId,
  type HistoryEssayScores,
} from './historyEssayScoring';
import './history-essay.css';

interface Props {
  card: SecRubricCard & { rubric: HistoryEssayRubric };
  scores: HistoryEssayScores;
  onScore: (id: HistoryEssayScoreId, marks: number) => void;
}

const HistoryEssayPanel: React.FC<Props> = ({ card, scores, onScore }) => {
  const { rubric } = card;
  const { cm, oe } = rubric;
  const tally = historyCmTally(rubric, scores);
  const oeMark = historyOeMark(rubric, scores);
  const oneElement = historyOneElement(rubric, scores);
  // The paragraph whose ladder is open. Placing it closes it again, so the
  // list stays one line per paragraph and only one ladder shows at a time.
  const [open, setOpen] = useState<number | null>(null);
  useEffect(() => { setOpen(null); }, [card.id]);
  const write = (writes: Array<[HistoryEssayScoreId, number]>) => writes.forEach(([id, value]) => onScore(id, value));
  const count = tally.paragraphs.length;
  const reached = tally.cm >= tally.ceiling;

  return (
    <div className="mb-hist-essay">
      <p className="mb-hist-eyebrow">SEC History marking scheme</p>
      <h3>Place each paragraph you wrote on the scheme’s bands, then place your whole answer.</h3>

      <section className="mb-hist-nomodel" aria-label="How the scheme marks this answer">
        <strong>{HISTORY_ESSAY_NO_MODEL_ANSWER}</strong>
        {rubric.schemeGuidance.map((line, index) => <p key={index}>{line}</p>)}
      </section>

      {cm.elementRule && (
        <section className="mb-hist-element" aria-label="This question's note">
          <ClaimDirections title="This question’s note in the scheme" notes={[cm.elementRule.note]} />
          <ClaimRow
            text="In my judgement, my answer deals with only one of these elements."
            note={`Your call, not the scheme’s. It sets your CM maximum to ${cm.elementRule.max}, as the note says.`}
            claimed={oneElement}
            onToggle={() => onScore(historyOneElementId, oneElement ? 0 : 1)}
          />
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

        {count === 0 && (
          <p className="mb-hist-empty">Add the first paragraph of your answer, then place it on a band.</p>
        )}
        <ol className="mb-hist-paragraphs">
          {tally.paragraphs.map(({ n, placed, counted }) => {
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

        {reached && count > 0 && (
          <p className="mb-hist-reached">
            Your CM has reached its maximum of {tally.ceiling}. A further paragraph counts 0m.
          </p>
        )}
        <button
          type="button"
          className="mb-hist-add"
          onClick={() => { write(historyAddParagraph(scores)); setOpen(count + 1); }}
        >
          {count === 0 ? 'Add a paragraph' : 'Add another paragraph'}
        </button>

        <ClaimDirections title="What the scheme counts as a paragraph" notes={[cm.paragraphLead, ...cm.paragraphKinds]} />
        <ClaimDirections notes={cm.directions} />
      </section>

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

      <div className="mb-hist-total" aria-live="polite">
        <span>Your placement · CM {tally.cm} + OE {oeMark ?? 0}</span>
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
          presentationNote: 'The printed marking by paragraph for this question, as the scheme sets it out.',
        }}
      />
    </div>
  );
};

export default HistoryEssayPanel;
