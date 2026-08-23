/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { describe, expect, it } from 'vitest';

import { SHOP_CATALOG } from '@/islandShopData';
import { getJourneyV2BasePrice } from '@/journeyEconomyConfig';
import { KUDOS_MESSAGES } from '@/kudosData';
import {
  GIFTABLE_ITEM_PRICES,
  KUDOS_MESSAGE_IDS,
  giftPrice,
  isKudosMessageId,
} from '@/functions/src/peerInteractionPolicy';
import {
  MAX_PASSWORD_LENGTH as SERVER_MAX_PASSWORD_LENGTH,
  MIN_PASSWORD_LENGTH as SERVER_MIN_PASSWORD_LENGTH,
  RESET_LIFETIME_SECONDS,
  hashTemporaryPassword,
  resetSessionIsEligible,
  validateNewPassword,
} from '@/functions/src/passwordResetPolicy';
import {
  MAX_PASSWORD_LENGTH as CLIENT_MAX_PASSWORD_LENGTH,
  MIN_PASSWORD_LENGTH as CLIENT_MIN_PASSWORD_LENGTH,
  passwordLengthError,
} from '@/utils/passwordPolicy';
import { clearLocalSessionData } from '@/utils/sessionPrivacy';

describe('password-reset policy', () => {
  it('keeps the client and callable length policy aligned', () => {
    expect(CLIENT_MIN_PASSWORD_LENGTH).toBe(SERVER_MIN_PASSWORD_LENGTH);
    expect(CLIENT_MAX_PASSWORD_LENGTH).toBe(SERVER_MAX_PASSWORD_LENGTH);
    expect(validateNewPassword('a'.repeat(SERVER_MIN_PASSWORD_LENGTH - 1))).toBeTruthy();
    expect(passwordLengthError('a'.repeat(CLIENT_MIN_PASSWORD_LENGTH - 1))).toBeTruthy();
    expect(validateNewPassword('a'.repeat(SERVER_MIN_PASSWORD_LENGTH))).toBeNull();
    expect(passwordLengthError('a'.repeat(CLIENT_MIN_PASSWORD_LENGTH))).toBeNull();
    expect(validateNewPassword('a'.repeat(SERVER_MAX_PASSWORD_LENGTH + 1))).toBeTruthy();
  });

  it('accepts only the reset session that was issued and has not expired', () => {
    const resetAt = 1_000;
    const expiresAt = resetAt + RESET_LIFETIME_SECONDS;
    expect(resetSessionIsEligible(resetAt, expiresAt, resetAt, expiresAt)).toBe(true);
    expect(resetSessionIsEligible(resetAt, expiresAt, resetAt - 1, resetAt + 1)).toBe(false);
    expect(resetSessionIsEligible(resetAt, expiresAt, resetAt, expiresAt + 1)).toBe(false);
    expect(resetSessionIsEligible('1000', expiresAt, resetAt, resetAt)).toBe(false);
  });

  it('stores only a deterministic hash for temporary-password reuse detection', () => {
    const hash = hashTemporaryPassword('temporary-password');
    expect(hash).toMatch(/^[a-f0-9]{64}$/);
    expect(hash).not.toContain('temporary-password');
    expect(hashTemporaryPassword('temporary-password')).toBe(hash);
    expect(hashTemporaryPassword('different-password')).not.toBe(hash);
  });
});

describe('server-owned peer interaction catalogues', () => {
  it('accepts exactly the kudos choices shown by the student UI', () => {
    expect([...KUDOS_MESSAGE_IDS].sort()).toEqual(KUDOS_MESSAGES.map(message => message.id).sort());
    for (const message of KUDOS_MESSAGES) expect(isKudosMessageId(message.id)).toBe(true);
    expect(isKudosMessageId('custom-message')).toBe(false);
  });

  it('accepts exactly the non-exclusive low-cost decorations shown as giftable', () => {
    const clientGiftable = SHOP_CATALOG
      .filter(item => item.type === 'decoration'
        && getJourneyV2BasePrice(item) <= 50
        && !item.exclusiveTo)
      .map(item => [item.id, getJourneyV2BasePrice(item)] as const)
      .sort(([left], [right]) => left.localeCompare(right));
    const serverGiftable = Object.entries(GIFTABLE_ITEM_PRICES)
      .sort(([left], [right]) => left.localeCompare(right));

    expect(serverGiftable).toEqual(clientGiftable);
    for (const [itemId, price] of serverGiftable) expect(giftPrice(itemId)).toBe(price);
    expect(giftPrice('building-castle')).toBeNull();
    expect(giftPrice('__proto__')).toBeNull();
  });
});

describe('shared-device privacy', () => {
  it('removes browser-persistent and tab-persistent account state on exit', async () => {
    window.localStorage.setItem('student-draft', 'private');
    window.sessionStorage.setItem('student-session', 'private');

    await clearLocalSessionData();

    expect(window.localStorage.length).toBe(0);
    expect(window.sessionStorage.length).toBe(0);
  });
});
