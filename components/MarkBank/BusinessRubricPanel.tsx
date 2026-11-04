/** @license SPDX-License-Identifier: Apache-2.0 */
import React from 'react';
import type { BusinessExpectedItem, BusinessRubric, SecRubricCard } from '../../types/markBank';
import { BUSINESS_OTHER_RESPONSE, businessExpectedId, businessExpectedLayout, businessMarks, businessPoolTarget,
  businessResponseFill, businessResponseMarks, businessScoreId, effectiveBusinessScores,
  type BusinessScoreId, type BusinessScores } from './businessRubric';
import { ClaimRow } from './ClaimRows';
import SourceMaterialReader from './SourceMaterialReader';

interface Props {
  card: SecRubricCard & { rubric: BusinessRubric };
  scores: BusinessScores;
  onScore: (id: BusinessScoreId, marks: number) => void;
}

const HEAD: React.CSSProperties = { fontSize: 10, fontWeight: 700, letterSpacing: '.1em', textTransform: 'uppercase', margin: '0 0 6px' };
const MUTED: React.CSSProperties = { margin: '6px 0 0', fontSize: 11, lineHeight: 1.45, color: 'var(--mb-muted)' };

/**
 * The SEC's response allocations, with the responses the scheme printed as
 * rows the student claims. A claimed row places the response's full marks on
 * the response it answers (the one it names, or the next empty one in a pool);
 * the component buttons under each response keep part marks honest. The
 * scheme calls its list a sample, so a row for another valid response stays.
 */
export default function BusinessRubricPanel({ card, scores, onScore }: Props) {
  const { rubric } = card;
  const effective = effectiveBusinessScores(rubric, scores);
  const layout = businessExpectedLayout(rubric);
  const worth = businessResponseMarks(rubric);
  const claimed = (itemId: string) => (scores[businessExpectedId(itemId)] ?? 0) > 0;
  const toggle = (itemId: string, responseId?: string) => {
    const next = !claimed(itemId);
    onScore(businessExpectedId(itemId), next ? 1 : 0);
    const target = responseId ?? businessPoolTarget(rubric, scores, next);
    if (target) for (const [id, marks] of businessResponseFill(rubric, target, next)) onScore(id, marks);
  };
  const row = (item: BusinessExpectedItem, responseId?: string) => (
    <ClaimRow key={item.id} text={item.text} note={item.detail?.join(' ')} marks={worth.marks} tag={worth.tag}
      claimed={claimed(item.id)} onToggle={() => toggle(item.id, responseId)} />
  );
  return (
    <div style={{ color: 'var(--mb-ink)', fontFamily: 'inherit' }}>
      <p style={HEAD}>SEC Business marking scheme</p>
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
        paperFileid={rubric.schemeFileid} documentKind="scheme" inline labelNamesMaterial
      />
      {rubric.guidance.map(note => (
        <p key={note} style={{ fontSize: 12, lineHeight: 1.5, color: 'var(--mb-muted)' }}>{note}</p>
      ))}
      {layout?.kind === 'pool' && (
        <section aria-label={`Scheme responses, page ${rubric.expected!.page}`} style={{ margin: '14px 0' }}>
          <p style={HEAD}>What the scheme printed · page {rubric.expected!.page}</p>
          {layout.items.map(item => row(item))}
          <ClaimRow text="Another valid response" tag={worth.marks === undefined ? worth.tag : undefined} marks={worth.marks}
            note="The scheme prints a sample of possible responses, never the only answers that score."
            claimed={claimed(BUSINESS_OTHER_RESPONSE)} onToggle={() => toggle(BUSINESS_OTHER_RESPONSE)} />
          <p style={MUTED}>A claimed response takes the full marks of the next response below; use its buttons for part marks.</p>
        </section>
      )}
      {rubric.responses.map(response => (
        <fieldset key={response.id} style={{
          margin: '14px 0', padding: '11px 0', border: 0,
          borderTop: '1px solid var(--mb-border)', minWidth: 0,
        }}>
          <legend style={{ paddingRight: 10, fontSize: 13, fontWeight: 650 }}>{response.label}</legend>
          {layout?.kind === 'per-response' && layout.items.has(response.id) && row(layout.items.get(response.id)!, response.id)}
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
