/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the "Show Me One" exemplars: every modelAnswer segment must point at a
 * real ribbon on its card (or the reveal renders a segment with no mark), carry
 * non-empty text, and cite a source.
 */
import { describe, it, expect } from 'vitest';
import { REP_CARDS } from '../examRepsData';

describe('Exam Reps — Show Me One model answers', () => {
  const withModel = REP_CARDS.filter((c) => c.modelAnswer);

  it('at least one card ships an authored model answer', () => {
    expect(withModel.length).toBeGreaterThan(0);
  });

  it('every model-answer segment maps to a real ribbon and has text', () => {
    for (const c of withModel) {
      for (const seg of c.modelAnswer!.segments) {
        expect(c.ribbons[seg.ribbonIndex], `${c.id}: segment ribbonIndex ${seg.ribbonIndex} is out of range`).toBeDefined();
        expect(seg.text.trim().length, `${c.id}: empty segment text`).toBeGreaterThan(0);
      }
    }
  });

  it('every model answer carries a source citation', () => {
    for (const c of withModel) {
      expect(c.modelAnswer!.source.trim().length, `${c.id}: model answer has no source`).toBeGreaterThan(0);
    }
  });

  it('segments use distinct ribbon indices and never target a gate ribbon', () => {
    for (const c of withModel) {
      const idxs = c.modelAnswer!.segments.map((s) => s.ribbonIndex);
      expect(new Set(idxs).size, `${c.id}: duplicate ribbonIndex across segments`).toBe(idxs.length);
      for (const s of c.modelAnswer!.segments) {
        const r = c.ribbons[s.ribbonIndex];
        if (r) expect(r.kind, `${c.id}: a model segment earns a gate ribbon (gates are pass/fail, not earned)`).not.toBe('gate');
      }
    }
  });
});
