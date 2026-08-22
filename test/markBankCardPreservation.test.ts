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
  ['biology:higher', BIO_HIGHER, 562, 'f9278d1b49aa4f4f0eecc1cbbccedc38ea8495e1fb21e3f1f9f1bea90ed5ef27'],
  ['biology:ordinary', BIO_ORDINARY, 581, '2eef24eeb7a62c48562e13ab5c64decb30f4ce855b28af8cc1a47c7d7808d498'],
  ['chemistry:higher', CHEM_HIGHER, 439, '09daf554f99e50dd093bbd10644f7de3beefcc9697f07cbcc943d8880dc937d2'],
  ['chemistry:ordinary', CHEM_ORDINARY, 325, 'e3436c2eb4566c8fc5bc87df1cb00e7e57f322ebee7bb3ef010ee9e9a9652577'],
  ['physics:higher', PHYS_HIGHER, 409, '0e7e9c27d6c23caec9b38f234b73df42aff985b2f8f45e9df8bb8a96e1ab6d34'],
  ['physics:ordinary', PHYS_ORDINARY, 425, '5a35010adf532cba57deadced11f2818ee841324b1615098962974b9e2f67a39'],
  ['agricultural-science:higher', AGSCI_HIGHER, 401, '62a6fe4e88d3740af0b96a5a403622cb237f583eafa65fd199638b0e320379a4'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 389, 'd964ad3c5b7f8933d947c1fc18c593098b3928d20c22d7ff8de8473e6e243a0e'],
  ['business:higher', BUSINESS_HIGHER, 267, 'f77da5157334a615111f7a5bd160306fef346c9eac49d8ad41b0dc6e4629a2b3'],
  ['business:ordinary', BUSINESS_ORDINARY, 317, '460e27935f41becdf381904c05fa4fa041c9c906fe0ded058a77638f3a3c2e80'],
  ['home-economics:higher', HOME_EC_HIGHER, 298, '0993532438e360013ca6930c425db0b9c398b886673a4029ad6df0c9c467b49d'],
  ['home-economics:ordinary', HOME_EC_ORDINARY, 273, '5b15bc2e07a475191deb82613d27459fa2e776a0b10a2249aaff4f11f7a7e787'],
  ['economics:higher', ECON_HIGHER, 189, '11ccb1c5f156112fa0d90b0c64e486086f920eeec72c9ad884aaa7d338ba2db6'],
  ['economics:ordinary', ECON_ORDINARY, 107, 'd48275547928418109d9a10e7c2bbeb62e2a60ea54b15e5932468d97bf463e28'],
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
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(4_982);
  });
});
