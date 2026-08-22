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
  ['biology:higher', BIO_HIGHER, 590, 'f1426a89703b0c720f0b11af4de86ee7caacac751876903d1fb6d0359fa37372'],
  ['biology:ordinary', BIO_ORDINARY, 609, '74c1263a0a74f4a3937b9019e30a552b5e2b1e2a2ece3c1d46210761a1172be9'],
  ['chemistry:higher', CHEM_HIGHER, 442, '0d4d7d1d3507f1ec87d9ba100bf172199a2e65dc37e837a093a6a52895f31196'],
  ['chemistry:ordinary', CHEM_ORDINARY, 333, 'e39a8fd08acd5d0849ab0d254cf27b15a237fc1edf1afac85131e2ba278b9884'],
  ['physics:higher', PHYS_HIGHER, 418, '27c1c75ce7134b6b1a3fc465cb7160428b38dd146764b6a1e67b36cf6197441a'],
  ['physics:ordinary', PHYS_ORDINARY, 433, '7738533efb264bec603952b08ca889fed98dde34ed54e8dae222fef95c30b695'],
  ['agricultural-science:higher', AGSCI_HIGHER, 424, '35a36a5589a926442af3f27b3697ef088d3eb2c49b708d9c54f39927a9b89173'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 420, '6ef8d5b819d337906e787c0944f19a175cb6cc1b38994f71ddfef85929fb7491'],
  ['business:higher', BUSINESS_HIGHER, 267, 'f77da5157334a615111f7a5bd160306fef346c9eac49d8ad41b0dc6e4629a2b3'],
  ['business:ordinary', BUSINESS_ORDINARY, 317, '460e27935f41becdf381904c05fa4fa041c9c906fe0ded058a77638f3a3c2e80'],
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
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(5_210);
  });
});
