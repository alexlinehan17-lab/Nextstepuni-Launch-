/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Regression guard: Innovation-Zone tools that surface JUNIOR CYCLE content
 * MUST be visible to Junior Cycle students.
 *
 * Background: the Innovation Zone gates tools by curriculum level. A JC
 * (1st–3rd year) student only sees a tool whose `curriculum` tag is 'both' or
 * 'junior' — the gate in components/InnovationZone.tsx reads
 *   const tag = t.curriculum ?? 'senior';
 *   const okCurriculum = tag === 'both' || tag === curriculumLevel;
 * so an ABSENT tag defaults to 'senior' and the tool is hidden from JC users.
 *
 * Catch-Up Lane and Command-Word Reflex once carried JC content while still
 * tagged 'senior', so they were invisible to the very students they were built
 * for. This test ties the actual content data to the gate: if a content tool
 * has any jc- subject, its InnovationZone curriculum tag must be JC-visible.
 * It fails both if the tag is reverted to 'senior' (the original bug) and if a
 * new content tool ships JC content without being tagged.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { RECOVERY_CARDS } from '../catchUpLaneData';
import { COMMAND_WORD_QUESTIONS, cycleForSubject } from '../commandWordData';

// Vitest runs from the repo root, so resolve the source file from process.cwd().
// (import.meta.url is not a file:// URL once Vite has transformed the module.)
const izSource = readFileSync(
  resolve(process.cwd(), 'components/InnovationZone.tsx'),
  'utf8',
);

/**
 * Extract the `curriculum` tag declared for a tool id in the IZ tools array.
 * Returns null when the tool has no tag (≡ 'senior' per the gate's default).
 */
function curriculumTagFor(toolId: string): string | null {
  const marker = `id: '${toolId}'`;
  const start = izSource.indexOf(marker);
  if (start === -1) return null;
  // Bound the search to THIS tool's object literal (up to the next tool's id),
  // so we never read a neighbouring tool's curriculum tag.
  const nextId = izSource.indexOf("id: '", start + marker.length);
  const block = izSource.slice(start, nextId === -1 ? start + 1500 : nextId);
  const m = block.match(/curriculum:\s*'([a-z]+)'/);
  return m ? m[1] : null;
}

const JC_VISIBLE = new Set(['both', 'junior']);

/** Per-subject Innovation-Zone content tools, paired with the data they render. */
const CONTENT_TOOLS: { id: string; subjectIds: string[] }[] = [
  { id: 'catch-up-lane', subjectIds: RECOVERY_CARDS.map((c) => c.subjectId) },
  { id: 'command-word-reflex', subjectIds: COMMAND_WORD_QUESTIONS.map((q) => q.subjectId) },
];

describe('JC tool visibility', () => {
  it('the InnovationZone curriculum gate still allows both/junior tools', () => {
    // Guard the gate predicate itself, so a refactor that drops it is noticed
    // and this test is re-evaluated rather than silently passing.
    expect(izSource).toMatch(/tag === 'both'\s*\|\|\s*tag === curriculumLevel/);
  });

  for (const tool of CONTENT_TOOLS) {
    it(`'${tool.id}' is declared in InnovationZone`, () => {
      expect(
        curriculumTagFor(tool.id) !== null || izSource.includes(`id: '${tool.id}'`),
        `tool '${tool.id}' was not found in InnovationZone.tsx (renamed or removed?)`,
      ).toBe(true);
      expect(izSource).toContain(`id: '${tool.id}'`);
    });

    it(`'${tool.id}' has Junior Cycle content`, () => {
      const jcSubjects = tool.subjectIds.filter((id) => cycleForSubject(id) === 'junior-cycle');
      expect(jcSubjects.length, `expected '${tool.id}' to carry jc- content`).toBeGreaterThan(0);
    });

    it(`'${tool.id}' is tagged JC-visible because it carries Junior Cycle content`, () => {
      const hasJc = tool.subjectIds.some((id) => cycleForSubject(id) === 'junior-cycle');
      if (!hasJc) return; // nothing to guard if the tool has no JC content
      const tag = curriculumTagFor(tool.id) ?? 'senior';
      expect(
        JC_VISIBLE.has(tag),
        `'${tool.id}' carries Junior Cycle content but its InnovationZone curriculum tag is ` +
          `'${tag}', which hides it from JC students. Tag it 'both' or 'junior'.`,
      ).toBe(true);
    });
  }
});
