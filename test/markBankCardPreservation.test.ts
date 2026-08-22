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
  ['biology:higher', BIO_HIGHER, 596, '670cf324f232ae79e3b649c0d4d783f0b41e3b4714cbae101f258150310b9795'],
  ['biology:ordinary', BIO_ORDINARY, 615, '807385b2c17207ef063d59471e5f6eb832119e49fb941e5eb6b08935c1cdedba'],
  ['chemistry:higher', CHEM_HIGHER, 443, '713b7ef8560702e78ed246adca8800057ca9eafd6e4e45ed583404be169709ae'],
  ['chemistry:ordinary', CHEM_ORDINARY, 334, 'd62186f4410f0516f01d6a902e07bfe8544d770095c8abd7e4ffdf9f24ab6f2c'],
  ['physics:higher', PHYS_HIGHER, 431, '9dbc270b7795a1d6008aa02af1d79553852335f38f9a056ebab66e0def805998'],
  ['physics:ordinary', PHYS_ORDINARY, 446, '8bb5ca7515ba7ecadf44bc5cb1994be4ac89710a671addbea578af241710fb82'],
  ['agricultural-science:higher', AGSCI_HIGHER, 431, 'c2e321cb19421d130ecd89bf6f248ecb974fea94f1c54c69387800a8edf1c06d'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 424, '8601d3986cb259f847742099ddbfa63b00c662cea1680ba1ffe733c8d7b52a5b'],
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
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(5_283);
  });
});
