/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A question from the SEC's deferred sitting says so wherever Paper Trail and
 * the Topic Atlas name its paper. Engineering 2022 Higher deferred Question 3
 * read "2022 · Higher · Question 3", exactly as June's Question 3 does.
 */

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render } from '@testing-library/react';

import VaultQuestionCard from '@/components/PaperTrail/VaultQuestionCard';
import { buildPackHtml } from '@/components/PaperTrail/revisionPack';
import { isDeferredFileid, sittingLabel } from '@/components/PaperTrail/sitting';
import { logicalQuestionIdentity, type TopicSibling } from '@/components/PaperTrail/topics';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
vi.mock('@/components/PaperTrail/CropView', () => ({ default: () => <div>Official PDF page</div> }));

const engineering2022 = (fileid: string): TopicSibling => ({
  subjectId: 'engineering', year: 2022, level: 'higher', lang: 'ev', fileid, paperKey: 'single', n: '3',
});

beforeEach(() => {
  delete (window as unknown as Record<string, unknown>).IntersectionObserver;
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, json: async () => ({}) })));
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

const header = (sibling: TopicSibling) => {
  const { container } = render(<VaultQuestionCard sibling={sibling} saved={false} onToggleReview={vi.fn()} onOpenInPaper={vi.fn()} />);
  const row = container.querySelector('.rounded-2xl > div')!;
  return [...row.querySelectorAll('span')].slice(0, 2).map(span => span.textContent);
};

describe('the deferred sitting is named', () => {
  it('the Atlas card for Engineering 2022 Higher deferred Q3 says "Deferred sitting"', () => {
    expect(header(engineering2022('LC027ALP000EV-deferred.pdf'))).toEqual(['2022', 'Higher · Deferred sitting · Question 3']);
  });

  it("June's Question 3 is unchanged", () => {
    expect(header(engineering2022('LC027ALP000EV.pdf'))).toEqual(['2022', 'Higher · Question 3']);
  });

  it('the revision pack names it too', () => {
    const html = buildPackHtml({
      subjectLabel: 'Engineering', topicLabel: 'Testing of Materials and Products', dateIso: '2026-11-13',
      questions: [engineering2022('LC027ALP000EV-deferred.pdf'), engineering2022('LC027ALP000EV.pdf')],
    });
    expect(html).toContain('<td>Higher · Deferred sitting</td><td>Question 3</td>');
    expect(html).toContain('<td>Higher</td><td>Question 3</td>');
  });

  it('one helper decides, and the Atlas identity still keeps the two sittings apart', () => {
    expect(isDeferredFileid('LC027ALP000EV-deferred.pdf')).toBe(true);
    expect(isDeferredFileid('LC027ALP000EV.pdf')).toBe(false);
    expect(sittingLabel('LC001ALP100IV-deferred.pdf')).toBe('Deferred sitting');
    expect(sittingLabel('LC001ALP100IV.pdf')).toBeNull();
    expect(logicalQuestionIdentity(engineering2022('LC027ALP000EV-deferred.pdf')))
      .not.toBe(logicalQuestionIdentity(engineering2022('LC027ALP000EV.pdf')));
  });
});
