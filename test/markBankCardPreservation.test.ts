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

const decks = [
  ['biology:higher', BIO_HIGHER, 548, '142c8d8fbb638cd62fe5f142c121ce82b93d796a204020ada6465f54dd53ea06'],
  ['biology:ordinary', BIO_ORDINARY, 564, '33cfab25e5fac59895767cd764e79c2116a8e1076f31a9f8db324ecb8e5d49f8'],
  ['chemistry:higher', CHEM_HIGHER, 416, 'e51984a5a0244bb597d3b578ab6f4f0f2f16903f5ca0d81dc753228e3dc5b5ca'],
  ['chemistry:ordinary', CHEM_ORDINARY, 311, '4cec647fec1f52160bef4c5eef3d7400b887081a27732999c7bb6a6c2a6cd7c2'],
  ['physics:higher', PHYS_HIGHER, 396, '7b1675bfd8052f4a0070fa8f659b5114a70044b7aa33e297d4d51691b809e266'],
  ['physics:ordinary', PHYS_ORDINARY, 418, '994814c0fff6456591e97479b8580a862639c6a89d2317037f767848d5a5fb21'],
  ['agricultural-science:higher', AGSCI_HIGHER, 401, '62a6fe4e88d3740af0b96a5a403622cb237f583eafa65fd199638b0e320379a4'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 389, 'd964ad3c5b7f8933d947c1fc18c593098b3928d20c22d7ff8de8473e6e243a0e'],
  ['business:higher', BUSINESS_HIGHER, 267, 'f77da5157334a615111f7a5bd160306fef346c9eac49d8ad41b0dc6e4629a2b3'],
  ['business:ordinary', BUSINESS_ORDINARY, 317, '460e27935f41becdf381904c05fa4fa041c9c906fe0ded058a77638f3a3c2e80'],
  ['home-economics:higher', HOME_EC_HIGHER, 296, '719eab895a58debff56d6beb0abc9d89d995dfe68f19989125fbb6f8f972a2f6'],
  ['home-economics:ordinary', HOME_EC_ORDINARY, 273, '5b15bc2e07a475191deb82613d27459fa2e776a0b10a2249aaff4f11f7a7e787'],
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
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(4_596);
  });
});
