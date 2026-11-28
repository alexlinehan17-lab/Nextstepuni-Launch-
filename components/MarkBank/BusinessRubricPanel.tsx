/** @license SPDX-License-Identifier: Apache-2.0 */
import React from 'react';
import type { BusinessExpectedItem, BusinessRubric, SecRubricCard } from '../../types/markBank';
import { BUSINESS_OTHER_RESPONSE, businessExpectedId, businessExpectedLayout, businessMarks, businessPoolTarget,
  businessResponseFill, businessResponseMarks, businessScoreId, effectiveBusinessScores,
  type BusinessScoreId, type BusinessScores } from './businessRubric';
import { ClaimRow, MarkTick } from './ClaimRows';
import SourceMaterialReader from './SourceMaterialReader';

interface Props {
  card: SecRubricCard & { rubric: BusinessRubric };
  scores: BusinessScores;
  onScore: (id: BusinessScoreId, marks: number) => void;
}

const HEAD: React.CSSProperties = { margin: '0 0 6px', color: 'var(--ink-muted)', font: '400 11px/14px var(--font-ui)', letterSpacing: '.1em', textTransform: 'uppercase' };
const MUTED: React.CSSProperties = { margin: '6px 0 0', color: 'var(--ink-muted)', font: '400 13px/18px var(--font-ui)' };

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
    <div style={{ color: 'var(--ink-primary)', font: '400 15px/21px var(--font-ui)' }}>
      <p style={HEAD}>SEC Business marking scheme</p>
      {rubric.taskRequirements.map(requirement => (
        <p key={requirement} className="mb-scheme-sub">{requirement}</p>
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
        <p key={note} className="mb-scheme-sub">{note}</p>
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
          borderTop: '1px solid var(--hairline)', minWidth: 0,
        }}>
          <legend style={{ paddingRight: 10, font: '400 15px/21px var(--font-ui)' }}>{response.label}</legend>
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
                  <span style={{ color: 'var(--ink-secondary)', font: '400 13px/18px var(--font-ui)' }}>{allocation.label}</span>
                  <div className="mb-mark-buttons">
                    {allocation.permittedMarks.map(mark => (
                      <button key={mark} type="button" className="mb-mark-btn" aria-pressed={selected === mark}
                        aria-label={`Set ${response.label} ${allocation.label} to ${mark} marks`}
                        disabled={Boolean(locked && mark > 0)}
                        onClick={() => onScore(id, mark)}>{selected === mark && <MarkTick />}{mark}</button>
                    ))}
                  </div>
                </div>
                {locked && <p style={MUTED}>
                  A link earns marks only with relevant theory in this response.
                </p>}
              </div>
            );
          })}
        </fieldset>
      ))}
      <p className="mb-scheme-total">
        <span>Your placement</span><strong>{businessMarks(card, scores)} / {card.totalMarks}</strong>
      </p>
      <p className="mb-scheme-sub" style={{ marginTop: 12 }}>{rubric.markingGuideNote}</p>
    </div>
  );
}
