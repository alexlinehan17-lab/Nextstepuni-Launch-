/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic Vault deep links — build a shareable URL + restore from the boot
 * snapshot. Pure logic (no history/popstate), so it's fully unit-testable; the
 * boot-param source is mocked. Validation runs against the REAL committed tags.
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';

let bootParams: Record<string, string> = {};
vi.mock('@/utils/bootParams', () => ({ getBootParam: (k: string) => bootParams[k] ?? null }));

import {
  buildVaultLink,
  hasInitialVaultTopic,
  consumeInitialVaultLocation,
  __resetVaultDeepLinkForTest,
} from '@/components/PaperTrail/vaultDeepLink';
import { taggedSubjects, topicsForSubject } from '@/components/PaperTrail/topics';

const sid = taggedSubjects()[0];
const tid = topicsForSubject(sid)[0].subtopicId;

beforeEach(() => {
  bootParams = {};
  __resetVaultDeepLinkForTest();
});

describe('vault deep link', () => {
  it('builds a shareable URL carrying the app nav params + subject/topic', () => {
    const url = buildVaultLink(sid, tid, 'https://app.example', '/');
    const u = new URL(url);
    expect(u.searchParams.get('view')).toBe('innovation-zone');
    expect(u.searchParams.get('tool')).toBe('paper-trail');
    expect(u.searchParams.get('subject')).toBe(sid);
    expect(u.searchParams.get('topic')).toBe(tid);
  });

  it('build → parse round-trips a real (subject, topic)', () => {
    const url = buildVaultLink(sid, tid, 'https://app.example', '/');
    const q = new URL(url).searchParams;
    bootParams = { subject: q.get('subject')!, topic: q.get('topic')! };
    expect(hasInitialVaultTopic()).toBe(true);
    expect(consumeInitialVaultLocation()).toEqual({ subjectId: sid, subtopicId: tid });
  });

  it('consumes the location only once per load', () => {
    bootParams = { subject: sid, topic: tid };
    expect(consumeInitialVaultLocation()).toEqual({ subjectId: sid, subtopicId: tid });
    expect(consumeInitialVaultLocation()).toBeNull(); // second read is null
  });

  it('rejects an unknown subject or a topic that is not on the subject', () => {
    bootParams = { subject: 'not-a-subject', topic: tid };
    expect(hasInitialVaultTopic()).toBe(false);
    bootParams = { subject: sid, topic: 'not-a-real-topic' };
    expect(hasInitialVaultTopic()).toBe(false);
    expect(consumeInitialVaultLocation()).toBeNull();
  });

  it('with no params, restores nothing (normal vault home)', () => {
    expect(hasInitialVaultTopic()).toBe(false);
    expect(consumeInitialVaultLocation()).toBeNull();
  });
});
