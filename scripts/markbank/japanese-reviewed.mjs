/** Publish only source-pinned Japanese reviews; preserve legacy authored cards. */
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { resolvePaperFileid } from './paperIndex.mjs';
import { audioMaterialFault, audioQuestionPaperFileid } from './audioMaterial.mjs';
import { comparableScheme, claimMatches, LIGATURES } from './schemeText.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const reviewsDir = resolve(root, 'scripts/markbank/authoring/reviews');
const figures = JSON.parse(readFileSync(resolve(root, 'components/MarkBank/figures-japanese.json'), 'utf8'));
const audio = JSON.parse(readFileSync(resolve(root, 'data/japaneseAudio.json'), 'utf8'));
const glyphs = JSON.parse(readFileSync(resolve(root, 'scripts/markbank/authoring/glyphmap.json'), 'utf8'));
const repair = value => typeof value === 'string'
  ? [...value].map(character => LIGATURES[character] ?? glyphs[character] ?? character).join('').replace(/\u00a0/g, ' ')
  : Array.isArray(value) ? value.map(repair)
    : value && typeof value === 'object' ? Object.fromEntries(Object.entries(value).map(([key, value]) => [key, repair(value)])) : value;
const hash = (path, kind = 'sha256') => createHash(kind).update(readFileSync(path)).digest('hex');
const unprintedAnswer = readFileSync(resolve(root, 'types/markBank.ts'), 'utf8').match(/export const UNPRINTED_ANSWER = '([^']+)'/)[1];
const criterionGuidance = criterion => [
  ...(criterion.guidance ?? []), ...(criterion.bands ?? []).flatMap(band => band.guidance),
  ...(criterion.limits ?? []).flatMap(limit => [...limit.guidance, ...(limit.bands ?? []).flatMap(band => band.guidance)]),
];
const cards = [];

for (const name of readdirSync(reviewsDir).filter(name => /^japanese-\d{4}-(?:hl|ol)\.json$/.test(name)).sort()) {
  const review = JSON.parse(readFileSync(resolve(reviewsDir, name), 'utf8'));
  for (const source of review.sources) {
    if (hash(resolve(root, source.path)) !== source.sha256) throw new Error(`${name}: source changed: ${source.path}`);
  }
  const schemePath = review.sources.find(source => source.document === 'scheme').path.replace(/\.pdf$/, '.md');
  if (!existsSync(resolve(root, schemePath))) throw new Error(`Extract original scheme first: ${schemePath}`);
  const scheme = comparableScheme(readFileSync(resolve(root, schemePath), 'utf8'));
  // Original PDF columns are read in different orders by whole-page extraction.
  // The pinned authoring selectors preserve the inspected column sequence.
  const selectedScheme = comparableScheme(review.selectors.filter(selector => selector.document === 'scheme').map(selector => selector.text).join('\n'));
  for (const original of review.cards) {
    const card = structuredClone(original);
    const evidence = card.sourceEvidence;
    if (card.answerLanguageRule) {
      const rule = card.answerLanguageRule;
      const sourceBound = review.selectors.some(selector => selector.document === 'scheme'
        && rule.schemePages.includes(selector.page) && selector.text === rule.sourceText);
      if (![0, 0.5].includes(rule.otherLanguageMultiplier) || !sourceBound
        || !rule.schemePages.every(page => evidence.generalSchemePages?.includes(page))) {
        throw new Error(`${card.id}: answer-language rule is not bound to its reviewed scheme selector`);
      }
    }
    if (evidence.component === 'aural') {
      const recording = audio.find(record => record.year === card.year);
      if (!recording || recording.verification.status !== 'full-file-verified') throw new Error(`${card.id}: recording not fully verified`);
      card.audioMaterial = recording.source;
      const fault = audioMaterialFault(card, 'japanese');
      if (fault) throw new Error(`${card.id}: ${fault}`);
    }
    card.paperFileid = card.audioMaterial ? audioQuestionPaperFileid(card, 'japanese') : resolvePaperFileid('japanese', card.year, card.level, card.section);
    if (!card.paperFileid) throw new Error(`${card.id}: no indexed original paper`);
    if (card.sourceMaterial) {
      const { _component, ...material } = card.sourceMaterial;
      card.sourceMaterial = { ...material, sourceFileid: card.paperFileid, sourceYear: card.year };
    }
    if (card.questionFigureKey) {
      const key = card.questionFigureKey;
      const figure = figures[key];
      if (!figure || hash(resolve(root, 'public', figure.src.replace(/^\//, '')), 'md5') !== figure.md5) throw new Error(`${card.id}: question crop changed`);
      card.questionFigure = { candId: key, src: figure.src, srcHash: figure.md5, alt: figure.alt, attribution: figure.attribution, lettersVisible: [], includesPrompt: true };
      delete card.questionFigureKey;
    }
    const answers = (card.rows ?? []).flatMap(row => {
      if (row.unprinted) {
        if (row.verbatim !== unprintedAnswer) throw new Error(`${card.id}: unprinted row invents an answer`);
        return [];
      }
      return row.kind === 'anyN' ? row.group.options : [row.verbatim];
    });
    const guidance = [];
    if (card.rubric?.system === 'language-points') {
      answers.push(...card.rubric.groups.flatMap(group => group.rows.map(row => row.text)));
      guidance.push(...card.rubric.groups.flatMap(group => (group.criteria ?? []).flatMap(criterionGuidance)));
    }
    if (['language-points', 'language-writing'].includes(card.rubric?.system)) guidance.push(...(card.rubric.criteria ?? []).flatMap(criterionGuidance));
    const unsupported = answers.filter(answer => !claimMatches(scheme, answer));
    if (unsupported.length) throw new Error(`${card.id}: answer not found in original scheme: ${JSON.stringify(unsupported)}`);
    const unsupportedGuidance = guidance.filter(text => !claimMatches(scheme, text) && !claimMatches(selectedScheme, text));
    if (unsupportedGuidance.length) throw new Error(`${card.id}: rubric guidance not found in original scheme selectors: ${JSON.stringify(unsupportedGuidance)}`);
    cards.push(repair(card));
  }
}
if (new Set(cards.map(card => card.id)).size !== cards.length) throw new Error('Duplicate Japanese reviewed identity');
writeFileSync(resolve(root, 'components/MarkBank/cards/japanese/reviewed.json'), JSON.stringify(cards, null, 2) + '\n');
console.log(`Japanese reviewed tasks: ${cards.length}; ${cards.reduce((sum, card) => sum + card.totalMarks, 0)} offered marks.`);
