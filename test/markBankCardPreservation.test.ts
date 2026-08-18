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
  ['chemistry:higher', CHEM_HIGHER, 410, 'db8ca35c632ea4933c32853b3eea315f87843200ae1e4787be4dff0362f0de01'],
  ['chemistry:ordinary', CHEM_ORDINARY, 308, '72fa1bb1dbc6717cd949865acc5fa6f2c203ad2cc605ef98a11fe226799407e9'],
  ['physics:higher', PHYS_HIGHER, 392, '5fdc64850f6aed01bf9aa5d1553b7ef05559ba17aedd5f896cd9dd6fd81a6e9a'],
  ['physics:ordinary', PHYS_ORDINARY, 415, 'e9fde53ea139add180d5fa3b6bb11d63053981988738b789842b937504bfe54b'],
  ['agricultural-science:higher', AGSCI_HIGHER, 401, '62a6fe4e88d3740af0b96a5a403622cb237f583eafa65fd199638b0e320379a4'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 389, 'd964ad3c5b7f8933d947c1fc18c593098b3928d20c22d7ff8de8473e6e243a0e'],
  ['business:higher', BUSINESS_HIGHER, 261, '756f439b344b3f5ad492baf96d2bde14e4991d225d8fadbf4a0234beef9290a7'],
  ['business:ordinary', BUSINESS_ORDINARY, 314, '9aa889406a38da3c7c143cc2aa84af34e33b1a901ee8482493ad58105c20af38'],
  ['home-economics:higher', HOME_EC_HIGHER, 191, 'e44f64afe2c876977224023822d95d01069ee2d7be2d4c35e1e9d1fff5c21298'],
  ['home-economics:ordinary', HOME_EC_ORDINARY, 152, 'c14dd035ebac19598d87342ddc8512b63dbcfe69b92c1808aebaf132303e8755'],
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
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(4_345);
  });
});
