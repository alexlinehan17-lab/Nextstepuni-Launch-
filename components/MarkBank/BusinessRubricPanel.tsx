/** @license SPDX-License-Identifier: Apache-2.0 */
import React from 'react';
import type { BusinessRubric, SecRubricCard } from '../../types/markBank';
import { businessMarks, businessScoreId, effectiveBusinessScores,
  type BusinessScoreId, type BusinessScores } from './businessRubric';
import SourceMaterialReader from './SourceMaterialReader';

interface Props {
  card: SecRubricCard & { rubric: BusinessRubric };
  scores: BusinessScores;
  onScore: (id: BusinessScoreId, marks: number) => void;
}

/** Render the SEC's response allocations without making indicative answers ticks. */
export default function BusinessRubricPanel({ card, scores, onScore }: Props) {
  const { rubric } = card;
  const effective = effectiveBusinessScores(rubric, scores);
  return (
    <div style={{ color: 'var(--mb-ink)', fontFamily: 'inherit' }}>
      <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '.1em', textTransform: 'uppercase' }}>
        SEC Business marking scheme
      </p>
      {rubric.taskRequirements.map(requirement => (
        <p key={requirement} style={{ fontSize: 13, lineHeight: 1.5 }}>{requirement}</p>
      ))}
      <SourceMaterialReader
        source={{
          kind: 'source-text', label: 'OFFICIAL MARKING SCHEME',
          title: `${card.questionRef} · answers and allocation`,
          pages: rubric.schemePages,
          attribution: card.schemeCitation,
          presentationNote: 'Read the published possible responses and mark allocation, then compare them with your own answer.',
        }}
        subjectId={card.subjectId} year={card.year}
        paperFileid={rubric.schemeFileid} documentKind="scheme" inline
      />
      {rubric.guidance.map(note => (
        <p key={note} style={{ fontSize: 12, lineHeight: 1.5, color: 'var(--mb-muted)' }}>{note}</p>
      ))}
      {rubric.responses.map(response => (
        <fieldset key={response.id} style={{
          margin: '14px 0', padding: '11px 0', border: 0,
          borderTop: '1px solid var(--mb-border)', minWidth: 0,
        }}>
          <legend style={{ paddingRight: 10, fontSize: 13, fontWeight: 650 }}>{response.label}</legend>
          {response.allocations.map(allocation => {
            const id = businessScoreId(response.id, allocation.id);
            const selected = scores[id] === undefined ? undefined : effective[id] ?? 0;
            const locked = allocation.requiresAnyOf
              && !allocation.requiresAnyOf.some(required =>
                (effective[businessScoreId(response.id, required)] ?? 0) > 0);
            return (
              <div key={id} style={{ margin: '8px 0' }}>
                <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                  <span style={{ fontSize: 12 }}>{allocation.label}</span>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
                    {allocation.permittedMarks.map(mark => (
                      <button key={mark} type="button" aria-pressed={selected === mark}
                        aria-label={`Set ${response.label} ${allocation.label} to ${mark} marks`}
                        disabled={Boolean(locked && mark > 0)}
                        onClick={() => onScore(id, mark)}
                        style={{
                          minWidth: 34, minHeight: 34, padding: '4px 9px', borderRadius: 7,
                          border: '1.5px solid var(--mb-ink)',
                          background: selected === mark ? '#f59c4c' : 'var(--mb-paper)',
                          color: selected === mark ? '#202020' : 'var(--mb-ink)',
                          opacity: locked && mark > 0 ? .45 : 1,
                          fontWeight: 700, cursor: locked && mark > 0 ? 'not-allowed' : 'pointer',
                        }}>{mark}</button>
                    ))}
                  </div>
                </div>
                {locked && <p style={{ margin: '5px 0 0', fontSize: 11, lineHeight: 1.4, color: 'var(--mb-muted)' }}>
                  A link earns marks only with relevant theory in this response.
                </p>}
              </div>
            );
          })}
        </fieldset>
      ))}
      <p style={{ display: 'flex', justifyContent: 'space-between', gap: 12, borderTop: '1px solid var(--mb-border)', paddingTop: 14 }}>
        <span>Your placement</span><strong>{businessMarks(card, scores)} / {card.totalMarks}</strong>
      </p>
      <p style={{ fontSize: 12, lineHeight: 1.5, color: 'var(--mb-muted)' }}>{rubric.markingGuideNote}</p>
    </div>
  );
}
