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
import { CARDS as MATHS_HIGHER } from '../components/MarkBank/cards/maths/higher';
import { CARDS as MATHS_ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import { CARDS as CONS_HIGHER } from '../components/MarkBank/cards/construction-studies/higher';
import { CARDS as CONS_ORDINARY } from '../components/MarkBank/cards/construction-studies/ordinary';

const decks = [
  ['biology:higher', BIO_HIGHER, 673, '45f278ef15f8d35a8a4393a0e8d01d7e5484e73a881844880dc090daeb9ce836'],
  ['biology:ordinary', BIO_ORDINARY, 686, '5792567a2b95584be782d44956c9fe7961eeec2e061683c83f32096fdf4de55e'],
  ['chemistry:higher', CHEM_HIGHER, 482, 'bea03a9e78691b0024ae64eb02526840fde6c4e51a586b1e4bc9387dd24112b5'],
  ['chemistry:ordinary', CHEM_ORDINARY, 364, '7c52a09853d6d24715537428d4a09ada8bbe3ece0a43a841c25c4dd129481172'],
  /* 2026-08-23: physics drops from 487/477 to 486/475. Three cards -- one
   * Higher (2021 q13a(v)) and two Ordinary (2022 q3(ii) and q3(viii)) -- quote
   * a stacked fraction the scheme's font renders as a diagonal slash whose
   * operands extract out of order, so "1/l" arrived as "1 l⁄". They were
   * shipping that text. build-deck.mjs now refuses any card still carrying a
   * glyph no font table resolves, and refusing beats printing the wrong
   * expression in front of a student. Recoverable once the fraction reader
   * covers the Physics papers; not a deletion of content that was correct. */
  /* 2026-08-24: physics 486/475 -> 567/563 — the backfill fleet's second
   * subject. Ten agents closed every open paper ask (card, exclusion with
   * scheme evidence, figure-needed, or named refusal); the ledger reads 95.1%
   * with the residue catalogued by kind. Two defective 2024 OL cards were
   * repaired IN PLACE (same ids): q1-v now lifts the clockwise-moments line
   * its question asks for, q10-iv the closed-pipe harmonic instead of another
   * part's answer. Nothing removed. */
  ['physics:higher', PHYS_HIGHER, 569, '463dd2324556ac2c286ed7c722602a9bf5e4f83a9ee43fdd03bcf8b13d97e6fd'],
  ['physics:ordinary', PHYS_ORDINARY, 563, '67dee7bc4ede4f829b03a569374b5cf94de35dd92bed3af580263667cf2a5f40'],
  ['agricultural-science:higher', AGSCI_HIGHER, 438, '31e25662626e35ca1db55e96e1cdfe0492648666c6cd35365f2c1e6d92c35f6a'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 431, '2dbd6e7635bb73941a16773ce9d3c654741a863280c002f783fc45cd0d7e8dbd'],
  ['business:higher', BUSINESS_HIGHER, 272, 'a61655818cee2ce61307eb08fe6dad282193791674b4e5e8a893e203b64af976'],
  ['business:ordinary', BUSINESS_ORDINARY, 334, '6d62fbc00d4b0f4c411cd23c17d76ddaa63cb066325bb2974c881c8b81073b18'],
  ['home-economics:higher', HOME_EC_HIGHER, 298, '0993532438e360013ca6930c425db0b9c398b886673a4029ad6df0c9c467b49d'],
  ['home-economics:ordinary', HOME_EC_ORDINARY, 273, '5b15bc2e07a475191deb82613d27459fa2e776a0b10a2249aaff4f11f7a7e787'],
  /* 2026-08-24: economics 234/152 -> 301/243 — the backfill campaign's
   * first subject. A ten-agent fleet authored every open paper ask; the ledger
   * (reconcile.py) now reads 100.0%: 498 covered + 160 excluded-with-evidence
   * = all 658 asks the 2021-2025 papers print. Nothing removed; all prior ids
   * remain. */
  ['economics:higher', ECON_HIGHER, 301, 'f69039b493aa5aac10f0f263f9f26fcba18afc9f10003c43960980f667ad852f'],
  ['economics:ordinary', ECON_ORDINARY, 243, 'be7ff725dc954485c6b54c0db7e680881473129a79ef08f33f8338b53af0a44f'],
  /* 2026-08-23: the two newest subjects had shipped with NO identity baseline
   * at all — found by the ratchet-soundness review, which means every earlier
   * count in this file was guarding seven decks while two rode along
   * unprotected. First recorded at their current shipped state. */
  /* 2026-08-23 (same day): maths 389/396 -> 391/398. The user caught a card
   * with no context ("find the probability..." with nothing saying 15% or 11
   * players) — the fix ships every part's paper stem, and four cards whose
   * question texts previously collided as duplicates are disambiguated by
   * their stems and now ship. Nothing was removed; all prior ids remain. */
  ['maths:higher', MATHS_HIGHER, 390, '23beae5a41188a29cd14fad10d9051270d53455c9df02f6e225d57fd87e2d6e0'],
  ['maths:ordinary', MATHS_ORDINARY, 400, 'd3b547c999646ea314ffaa9e5090df989d0e0dba10203f92d0937bd4a2f54031'],
  ['construction-studies:higher', CONS_HIGHER, 255, 'b74a39fd589f1082d6378190aee778d528eff0968d7af0ee9144525f2e40d57b'],
  ['construction-studies:ordinary', CONS_ORDINARY, 250, 'f56985e32cc1f02a2e2f7a7eb300a44646b75cf3604a12b5a478bde2a520d2da'],
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
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(7222);
  });
});
