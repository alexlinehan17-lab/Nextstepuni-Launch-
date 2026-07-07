/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Classroom pilot kit — the one-pager builder is pure; assert the content a
 * teacher (and the accreditation review) depends on is actually in the sheet.
 */
import { describe, expect, it } from 'vitest';
import { buildPilotKitHtml } from '../components/ExaminersChair/pilotKit';

describe('buildPilotKitHtml', () => {
  const html = buildPilotKitHtml();

  it('is a self-contained printable document', () => {
    expect(html).toContain('<!DOCTYPE html>');
    expect(html).toContain('@media print');
    expect(html).not.toMatch(/src=|href="http/);
  });

  it('walks the five steps of a marking class', () => {
    expect(html).toContain('Pick a class code');
    expect(html).toContain('Send');
    expect(html).toContain('Teacher view');
    expect(html).toMatch(/moderation/i);
    expect(html).toContain('Daily Mark');
  });

  it('states the privacy guarantee in plain words', () => {
    expect(html).toMatch(/only anonymous counts/i);
    expect(html).toMatch(/No names/i);
  });

  it('carries the content-honesty note', () => {
    expect(html).toMatch(/cited to a filed SEC marking scheme/i);
    expect(html).toMatch(/never real candidate work/i);
  });
});
