/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Propose the SEC's own wording for a marking point that fails provenance.
 *
 *     node scripts/markbank/suggest-verbatim.mjs <subject> [card-id]
 *
 * The commonest reason a physics or chemistry card fails is that the scheme
 * prints slash-separated ALTERNATIVES and the author wrote out one of them:
 * the scheme says "a control rod absorbs/stops/blocks neutrons" and the card
 * says "a control rod absorbs neutrons". Restoring the scheme's form is more
 * faithful, not less — it also shows the student which answers are accepted.
 *
 * SAFETY RULE, and the reason this can be applied semi-automatically: a
 * candidate is only proposed when it contains EVERY word of the card's claim,
 * in order. The scheme's text can therefore only ever be a superset of what the
 * card already said, so meaning is restored, never changed or dropped. Anything
 * that fails that test is printed as "no candidate" for a human to author.
 */
import { readFileSync } from 'node:fs';
import { normalise } from './schemeText.mjs';

const subj = process.argv[2];
const only = process.argv[3];
const cards = JSON.parse(readFileSync(`scripts/markbank/authored/${subj}.json`, 'utf8'));
const cache = new Map();

const schemeFor = (c) => {
  const stem = `${c.year}-${c.level === 'higher' ? 'hl' : 'ol'}`;
  const f = `examiner-reports/${subj}/schemes/${stem}.md`;
  if (!cache.has(f)) {
    const raw = readFileSync(f, 'utf8');
    const flat = [], at = [];
    for (let i = 0; i < raw.length; i++) {
      for (const ch of normalise(raw[i])) { flat.push(ch); at.push(i); }
    }
    cache.set(f, { raw, flat: flat.join(''), at });
  }
  return cache.get(f);
};

const words = (s) => (String(s).toLowerCase().match(/[a-z0-9]+/g) ?? []);

/** Every word of `claim`, in order, inside `text`. */
function covers(text, claim) {
  const t = words(text), c = words(claim);
  let i = 0;
  for (const w of c) {
    i = t.indexOf(w, i);
    if (i === -1) return false;
    i++;
  }
  return true;
}

const claimsOf = (r) => r.kind === 'anyN' && r.group ? r.group.options
                                                    : [String(r.verbatim).split(/\s[—-]\s/).pop()];
let proposed = 0, unresolved = 0;
for (const c of cards) {
  if (only && c.id !== only) continue;
  let s;
  try { s = schemeFor(c); } catch { continue; }
  for (const r of c.rows ?? []) {
    for (const claim of claimsOf(r)) {
      if (s.flat.includes(normalise(claim))) continue;
      // Anchor on the claim's first three words, then widen a window to the
      // right until it covers the whole claim.
      const cw = words(claim);
      // The anchor must be long enough to identify a place. "a = (-)w2s"
      // normalises to a couple of characters and matched the title page, so
      // take leading words until the anchor is substantial.
      let anchor = '';
      for (const w of cw) { anchor += normalise(w); if (anchor.length >= 8) break; }
      if (anchor.length < 8) { unresolved++; console.log(`${c.id}\t${r.id}\t${JSON.stringify(claim)}\tNO CANDIDATE`); continue; }
      let best = null;
      for (let i = s.flat.indexOf(anchor); i !== -1 && !best; i = s.flat.indexOf(anchor, i + 1)) {
        const from = s.at[i];
        for (const span of [120, 200, 300, 420]) {
          const to = Math.min(s.raw.length, from + span);
          const text = s.raw.slice(from, to).replace(/\s+/g, ' ').trim();
          if (!covers(text, claim)) continue;
          let cut = text;
          // Trim from the LEFT while the claim is still covered, so a candidate
          // that begins with the question text or a neighbouring marking point
          // narrows to the SEC's wording of this one.
          {
            const toks = cut.split(/\s+/);
            for (let k = 0; k < toks.length; k++) {
              const t2 = toks.slice(k).join(' ');
              if (covers(t2, claim)) cut = t2; else break;
            }
          }
          // Then to the shortest prefix that still covers, and drop trailing
          // mark annotations -- "[6]", "(4", "4 p" -- which are not the point.
          for (let k = cut.length; k > 0; k -= 3) {
            const t2 = cut.slice(0, k).trim();
            if (covers(t2, claim)) cut = t2; else break;
          }
          cut = cut.replace(/[\s\[(]*\d+[\s\])]*$/, '').replace(/[\s/(\[]+$/, '').trim();
          if (!covers(cut, claim)) continue;
          best = cut;
          break;
        }
      }
      if (best) { proposed++; console.log(`${c.id}\t${r.id}\t${JSON.stringify(claim)}\t${JSON.stringify(best)}`); }
      else { unresolved++; console.log(`${c.id}\t${r.id}\t${JSON.stringify(claim)}\tNO CANDIDATE`); }
    }
  }
}
console.error(`\n${proposed} candidate(s), ${unresolved} with none`);
