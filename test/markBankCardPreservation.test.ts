/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Frozen card-identity baseline. Curriculum migrations may remap topic metadata
 * but must never silently remove or replace a Mark Bank card. The hash is over
 * sorted stable card IDs, not topic IDs, so a legitimate canonical-topic
 * migration leaves this test green.
 *
 * When genuinely adding cards, update the affected count/hash only after
 * checking that all previous IDs remain present. Never refresh this baseline to
 * conceal a deletion.
 */
import { createHash } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import { CARDS as BIO_HIGHER } from '../components/MarkBank/cards/biology/higher';
import { CARDS as BIO_ORDINARY } from '../components/MarkBank/cards/biology/ordinary';
import { CARDS as CHEM_HIGHER } from '../components/MarkBank/cards/chemistry/higher';
import { CARDS as CHEM_ORDINARY } from '../components/MarkBank/cards/chemistry/ordinary';
import { CARDS as PHYS_HIGHER } from '../components/MarkBank/cards/physics/higher';
import { CARDS as PHYS_ORDINARY } from '../components/MarkBank/cards/physics/ordinary';
import { CARDS as AGSCI_HIGHER } from '../components/MarkBank/cards/agricultural-science/higher';
import { CARDS as AGSCI_ORDINARY } from '../components/MarkBank/cards/agricultural-science/ordinary';
import { CARDS as BUSINESS_HIGHER } from '../components/MarkBank/cards/business/higher';
import { CARDS as BUSINESS_ORDINARY } from '../components/MarkBank/cards/business/ordinary';
import { CARDS as HOME_EC_HIGHER } from '../components/MarkBank/cards/home-economics/higher';
import { CARDS as HOME_EC_ORDINARY } from '../components/MarkBank/cards/home-economics/ordinary';
import { CARDS as ECON_HIGHER } from '../components/MarkBank/cards/economics/higher';
import { CARDS as ECON_ORDINARY } from '../components/MarkBank/cards/economics/ordinary';

const decks = [
  ['biology:higher', BIO_HIGHER, 604, '0463b882c88149b96f94d709918f3a4c0aa86f385d947f036324de072d9f36da'],
  ['biology:ordinary', BIO_ORDINARY, 621, '449975186cd8a84f7f89d1cf0709515a09d6561592091e3f692e774f8d58746c'],
  ['chemistry:higher', CHEM_HIGHER, 443, '713b7ef8560702e78ed246adca8800057ca9eafd6e4e45ed583404be169709ae'],
  ['chemistry:ordinary', CHEM_ORDINARY, 335, 'b57490d8dce4b1bbcfa072e614f0078b29983dc95debe9cb56b559f10c5cfa2b'],
  ['physics:higher', PHYS_HIGHER, 485, 'b55030d87561dabe648528b960c74cc1def7c2fcbafbfbdd2ae63552b20b076b'],
  ['physics:ordinary', PHYS_ORDINARY, 476, 'ee2ae321c9ef21cb3fe8f041067268dba805c9fb5eb587ba70dd976171428f0a'],
  ['agricultural-science:higher', AGSCI_HIGHER, 438, '31e25662626e35ca1db55e96e1cdfe0492648666c6cd35365f2c1e6d92c35f6a'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 429, '338c18162213c261ee39334c32c7e864011a2f25c5a6fc3be8e17400df147a39'],
  ['business:higher', BUSINESS_HIGHER, 272, 'a61655818cee2ce61307eb08fe6dad282193791674b4e5e8a893e203b64af976'],
  ['business:ordinary', BUSINESS_ORDINARY, 334, '6d62fbc00d4b0f4c411cd23c17d76ddaa63cb066325bb2974c881c8b81073b18'],
  ['home-economics:higher', HOME_EC_HIGHER, 298, '0993532438e360013ca6930c425db0b9c398b886673a4029ad6df0c9c467b49d'],
  ['home-economics:ordinary', HOME_EC_ORDINARY, 273, '5b15bc2e07a475191deb82613d27459fa2e776a0b10a2249aaff4f11f7a7e787'],
  ['economics:higher', ECON_HIGHER, 234, '5bf329cc43896d7ae5dcb46ffc413255cc72a23f403068be83cc804fce6fecdb'],
  ['economics:ordinary', ECON_ORDINARY, 152, 'f07a279c83d1a53cf923d42344612cfbaa1c33e324b114a4a6173b872536b6a8'],
] as const;

const identityHash = (cards: readonly { id: string }[]) => createHash('sha256')
  .update(cards.map((card) => card.id).sort().join('\n'))
  .digest('hex');

describe('Mark Bank card preservation', () => {
  it.each(decks)('%s retains its complete stable card set', (name, cards, count, hash) => {
    expect(cards.length, `${name}: card count changed`).toBe(count);
    expect(new Set(cards.map((card) => card.id)).size, `${name}: duplicate card IDs`).toBe(count);
    expect(identityHash(cards), `${name}: a card ID was removed or replaced`).toBe(hash);
  });

  it('protects the complete current bank', () => {
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(5_394);
  });
});
