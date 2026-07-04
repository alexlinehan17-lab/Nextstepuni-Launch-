/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail topic revision-pack export (feature C2): the HTML lists
 * every real question with its year/level/paper, carries the SEC attribution,
 * fabricates no answer text, escapes untrusted labels, and slugs a safe filename.
 */
import { describe, it, expect } from 'vitest';
import { buildPackHtml, packFilename } from '../components/PaperTrail/revisionPack';
import { type TopicSibling } from '../components/PaperTrail/topics';

const q = (year: number, level: TopicSibling['level'], paperKey: string, n: string): TopicSibling => ({
  subjectId: 'business', level, lang: 'ev', year, fileid: `f${year}`, paperKey, n,
});

const opts = {
  subjectLabel: 'Business',
  topicLabel: 'Marketing Mix',
  questions: [q(2022, 'higher', 'p1', '3'), q(2021, 'ordinary', 'p2', '7')],
  dateIso: '2026-07-04',
};

describe('Paper Trail — topic revision pack', () => {
  it('lists every question with its year, level and paper', () => {
    const html = buildPackHtml(opts);
    expect(html).toContain('2022');
    expect(html).toContain('Question 3');
    expect(html).toContain('Higher · Paper 1');
    expect(html).toContain('2021');
    expect(html).toContain('Ordinary · Paper 2');
    expect(html).toContain('across 2 years');
  });

  it('carries the SEC attribution and no fabricated answers', () => {
    const html = buildPackHtml(opts);
    expect(html).toContain('State Examinations Commission');
    expect(html).toContain('question references only');
  });

  it('escapes untrusted label characters', () => {
    const html = buildPackHtml({ ...opts, topicLabel: 'A & B <x>' });
    expect(html).toContain('A &amp; B &lt;x&gt;');
    expect(html).not.toContain('<x>');
  });

  it('produces a safe, slugged filename', () => {
    expect(packFilename('Business', 'Marketing Mix')).toBe('business-marketing-mix-revision-pack.html');
    expect(packFilename('Maths (Applied)', 'Calculus & Limits')).toBe('maths-applied-calculus-limits-revision-pack.html');
  });
});
