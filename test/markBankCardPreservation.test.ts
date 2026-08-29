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
  /* 2026-08-29 (tenth wave): economics 325/259 -> 335/263. Fourteen cards, none
   * removed. The backfill run proper: a drafter proposes a tariff from the
   * scheme's own cells and a figure from the ref hierarchy, and every proposal
   * is checked before it is used. Coverage 538/658 -> 552/658, exclusions
   * 120 -> 106. */
  /* 2026-08-29 (ninth wave): economics 323/259 -> 325/259. Two cards added,
   * both unblocked by a TOOL fix rather than by new authoring: a crop is
   * catalogued against whatever ref the inspecting agent judged it to belong
   * to, and that is usually the parent question, so the scout's ref matching
   * had to walk the whole hierarchy instead of one level. It had been
   * reporting 43 asks as needing a crop that was never taken; the real number
   * is far smaller. Coverage 536/658 -> 538/658, exclusions 122 -> 120. */
  /* 2026-08-29 (eighth wave): economics 322/259 -> 323/259. One card added:
   * 2022 HL Section A Q7(a)(ii), the justification half of a "which chart"
   * pair. Part (i) is deliberately NOT carded — the paper prints Figure A and
   * Figure B side by side and only Figure B is catalogued, so a student would
   * be asked to choose between two charts while seeing one. Its exclusion
   * reason now says that rather than calling it a tick question. */
  /* 2026-08-29 (seventh wave): economics 320/257 -> 322/259. Four more tick
   * tables, none removed. Two of them carry a Reason column, where the scheme
   * prints prose AND states the categorisation with a drawn ✔ — extraction
   * interleaves the two into "Farmers in This is a visible export. Ireland
   * selling The money leaves Germany", so the crop is the only faithful form.
   * Coverage 531/658 -> 535/658, exclusions 127 -> 123. */
  /* 2026-08-29 (sixth wave): economics 319/253 -> 320/257. Five more tick
   * tables, none removed. Each is the scheme's completed table cropped and
   * bound as a solution figure, because the ✔ is drawn and extraction loses the
   * column it sits in. Coverage 526/658 -> 531/658, exclusions 132 -> 127. */
  /* 2026-08-29 (fifth wave): economics 317/252 -> 319/253. Three cards ADDED,
   * none removed — the first tick tables in the deck. Their ✔ is DRAWN, not set
   * in the text layer, so extraction keeps the tick and loses the column it
   * sits in, and the column is the whole answer. The scheme's completed table
   * is cropped and bound as a SOLUTION figure instead (the mechanism the Maths
   * deck already uses for 819 printed model solutions: hidden until reveal,
   * rendered large). Coverage 523/658 -> 526/658, exclusions 135 -> 132. */
  /* 2026-08-29 (fourth wave): economics 316/251 -> 317/252. Two cards ADDED,
   * none removed. Diagram parts where the paper also says "Explain" and the
   * scheme prints that explanation as prose — the drawing was never the whole
   * ask. Coverage 521/658 -> 523/658, exclusions 137 -> 135. */
  /* 2026-08-29 (third wave): economics 314/250 -> 316/251. Three cards ADDED,
   * none removed. Worked calculations whose scheme sets the fraction as a
   * stacked 2-D layout — extraction flattens it, putting the denominator after
   * the answer, so each card's note says how to read the order rather than
   * pretending the layout survived. Coverage 518/658 -> 521/658, exclusions
   * 140 -> 137. Two pre-existing cards also gained the figure they had always
   * referred to ("The diagram shows...") and card lint is now clean. */
  /* 2026-08-29 (second wave): economics 303/247 -> 314/250. Fourteen cards
   * ADDED, none removed or renamed. All thirteen came out of the exclusion
   * list, where they had been recorded as "answered by reading the chart" or
   * "the response is the worked calculation" — descriptions of the answer, not
   * blockers. The charts were already catalogued; the schemes print formula,
   * substitution and result in full. Coverage 504/658 -> 517/658, exclusions
   * 154 -> 140. The fourteenth is 2024 OL Q14(b)(ii), a tick question whose
   * paper ALSO says "explain your choice": the tick was never the whole ask,
   * and the scheme prints the explanation as ordinary prose. */
  /* 2026-08-29: economics 301/243 -> 303/247. Six cards ADDED, none removed or
   * renamed. All six are parts that had been excluded as "answered by reading
   * the chart printed with it" — which described the response and was never a
   * reason to leave the ask out, because the chart itself was already
   * catalogued with verified alt text and an md5 the build re-checks. Binding
   * it gives the student what the candidate in the hall had:
   *   econ-2021-hl-q16-a-i-trend  air passenger numbers 2017-2020
   *   econ-2023-hl-q14-a-i        monthly unemployment rate, Mar 21 - Sep 22
   *   econ-2023-ol-q14-a-i        petrol prices, Apr - Sep 2022
   *   econ-2021-ol-q14-c-i        income tax on €18,000 across five countries
   *   econ-2022-ol-seca-q6-i      peak months of unemployment, Nov 20 - Nov 21
   *   econ-2024-ol-q12-c-i        overall trend in Irish unemployment, 2022
   * The -trend suffix on the first is forced: econ-2021-hl-q16-a-i is taken by
   * a card whose citation econ_refs.py corrects to Q16(c)(i), and an id is
   * never renamed because it keys a student's review history. */
  ['economics:higher', ECON_HIGHER, 335, 'a058097cc9ebf6f2b32353bcf5e148e7b44cf8628970ee9cc7d48c796a75a114'],
  ['economics:ordinary', ECON_ORDINARY, 263, 'f4cc9b993c3b278f93dbc2d693831fcebba9ecd14602592c1eb292b914200c5e'],
  /* 2026-08-23: the two newest subjects had shipped with NO identity baseline
   * at all — found by the ratchet-soundness review, which means every earlier
   * count in this file was guarding seven decks while two rode along
   * unprotected. First recorded at their current shipped state. */
  /* 2026-08-23 (same day): maths 389/396 -> 391/398. The user caught a card
   * with no context ("find the probability..." with nothing saying 15% or 11
   * players) — the fix ships every part's paper stem, and four cards whose
   * question texts previously collided as duplicates are disambiguated by
   * their stems and now ship. Nothing was removed; all prior ids remain. */
  ['maths:higher', MATHS_HIGHER, 387, 'e5daea14329527050997f6c7d02d838919bb8c72efb236fadaa02b69fd369bc5'],
  ['maths:ordinary', MATHS_ORDINARY, 397, 'feb0fc8f67372bcef789bbe1616dd3241c6c42b9fd8f4d12a3204c84a49b5c74'],
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
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(7270);
  });
});
