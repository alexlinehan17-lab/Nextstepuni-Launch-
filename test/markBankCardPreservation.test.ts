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
  ['biology:higher', BIO_HIGHER, 583, '4b0c49aea5360d4df0b659aa5d8e75720b2844f1368973505b057cfa90af629f'],
  ['biology:ordinary', BIO_ORDINARY, 588, '3093dc5c029971485a25dfdaec1fabc1e303e977213f94e4c0cebd3ec06d563f'],
  ['chemistry:higher', CHEM_HIGHER, 440, 'b4a96e7c169bbbdf4abdfd2f9ed231e62363d9edfe37744861fc71e84ff3fe24'],
  ['chemistry:ordinary', CHEM_ORDINARY, 326, '7eec5589fab5e1cf2b028baed4995f14a80296951f35ed4cf68f33a503f6a89a'],
  ['physics:higher', PHYS_HIGHER, 409, '0e7e9c27d6c23caec9b38f234b73df42aff985b2f8f45e9df8bb8a96e1ab6d34'],
  ['physics:ordinary', PHYS_ORDINARY, 425, '5a35010adf532cba57deadced11f2818ee841324b1615098962974b9e2f67a39'],
  ['agricultural-science:higher', AGSCI_HIGHER, 419, 'b747e371eef2908cf53f8fcbf7ed9552baed0b7afc71a0d86bbde71b94284411'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 418, '28fa2c01786e0b65b2a6ebcfb66788b4b5ce7bb7726d808bc00214bd323ec671'],
  ['business:higher', BUSINESS_HIGHER, 267, 'f77da5157334a615111f7a5bd160306fef346c9eac49d8ad41b0dc6e4629a2b3'],
  ['business:ordinary', BUSINESS_ORDINARY, 317, '460e27935f41becdf381904c05fa4fa041c9c906fe0ded058a77638f3a3c2e80'],
  ['home-economics:higher', HOME_EC_HIGHER, 298, '0993532438e360013ca6930c425db0b9c398b886673a4029ad6df0c9c467b49d'],
  ['home-economics:ordinary', HOME_EC_ORDINARY, 273, '5b15bc2e07a475191deb82613d27459fa2e776a0b10a2249aaff4f11f7a7e787'],
  ['economics:higher', ECON_HIGHER, 204, '593142d16898d5f6803372f25b77dc206bb9406fb7a87eaae23ebf75999b8a56'],
  ['economics:ordinary', ECON_ORDINARY, 132, '5fa4f72fcd19dc4bfb3cddfd0c3faf48dd864b1e5223d79adbceb4291e907e53'],
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
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(5_099);
  });
});
