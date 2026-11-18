import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as ordinary } from '../components/MarkBank/cards/japanese/ordinary';
import reviewed from '../components/MarkBank/cards/japanese/reviewed.json';
import aliases from '../components/MarkBank/cards/japanese/aliases.json';
import census from '../scripts/markbank/authoring/reviews/japanese-2015-ol-census.json';
import review from '../scripts/markbank/authoring/reviews/japanese-2015-ol.json';
import { languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';

const cards = ordinary.filter(card => card.year === 2015);
const idFor = (key: (string | number | null)[]) => `ja-2015-ol-${key.filter(part => part !== null).join('-').toLowerCase()}`;
const card = (suffix: string) => cards.find(card => card.id === `ja-2015-ol-${suffix}`)!;
const point = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'question') throw new Error(`Expected point card: ${suffix}`);
  return found;
};
const points = (suffix: string) => {
  const found = card(suffix);
  if (found.kind !== 'rubric' || found.rubric.system !== 'language-points') throw new Error(`Expected grouped rubric: ${suffix}`);
  return found.rubric;
};
const map = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/2015/${fileid}.json`), 'utf8'));

describe('Japanese 2015 Ordinary independent source review', () => {
  it('covers all 51 independent tasks and all 40 original physical pages', () => {
    expect(cards).toHaveLength(51);
    expect(cards.map(card => card.id).sort()).toEqual(census.tasks.map(task => idFor(task.key)).sort());
    for (const task of census.tasks) {
      const found = cards.find(card => card.id === idFor(task.key))!;
      expect(found.totalMarks, found.id).toBe(task.marks);
      expect(tariffReconciles(found), found.id).toBe(true);
      expect(reviewed.find(card => card.id === found.id)!.sourceEvidence).toMatchObject({ component: task.component, paperPages: task.paperPages, schemePages: task.schemePages });
    }
    const total = (selected: typeof cards) => selected.reduce((sum, card) => sum + card.totalMarks, 0);
    expect(total(cards.filter(card => !card.audioMaterial && !['4', 'Q5'].includes(card.section!)))).toBe(120);
    expect(total(cards.filter(card => ['4', 'Q5'].includes(card.section!)))).toBe(80);
    expect(total(cards.filter(card => card.audioMaterial))).toBe(100);
    expect(total(cards)).toBe(300);
    expect(census.candidateMaximum).toMatchObject({ written: 200, listening: 100, total: 300 });
    expect(Object.values(census.pageRoles).map(pages => Object.keys(pages).length)).toEqual([16, 8, 16]);
    expect(review.sources.map(source => ({ component: source.document, path: source.path, sha256: source.sha256 }))).toEqual(census.sources);
    expect(review.sources.map(source => source.sha256)).toEqual([
      'f879d2104da262a0d71d0b35fe4e8b96663005919a79de7e985437311ddbaae4',
      '4182135287021fe369c51c80cdb12a9c1d87b8bcbdf6b859995a005c6d72ca91',
      'a61a77888865f54df92faadfbde180cf052ab549a5f17a255856961808da22e8',
    ]);
    for (const source of review.sources) expect(source.pagesReviewed).toEqual(Object.keys(census.pageRoles[source.document as keyof typeof census.pageRoles]).map(Number));
  });

  it('adds 51 independently reviewed cards without inventing original aliases', () => {
    const original = readFileSync(resolve(__dirname, '../components/MarkBank/cards/japanese/ordinary.ts'), 'utf8');
    expect(createHash('sha256').update(original).digest('hex')).toBe('83a3b57745ae80882d11a3346ab34cefba7b70d801701b87202493e0650983ef');
    const originalIds = [...original.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
    expect(originalIds).toHaveLength(261);
    expect(originalIds.some(id => id.startsWith('ja-2015-'))).toBe(false);
    expect(cards.every(card => !originalIds.includes(card.id))).toBe(true);
    expect(review.consolidations).toEqual([]);
    expect(Object.keys(aliases)).toHaveLength(391);
    expect(Object.keys(aliases).filter(id => id.startsWith('ja-2015-'))).toEqual([]);
  });

  it('retains the full required link/profile tasks and the published component tariffs', () => {
    expect(point('1-1').rows.map(row => row.verbatim)).toEqual(['6', '4', '2', '7', '3']);
    const profile = point('1-2');
    expect(profile.rows).toHaveLength(6);
    expect(profile.rows[0].group?.options).toEqual(['Morita', 'Morida']);
    expect(profile.rows[1]).toMatchObject({ verbatim: 'Minako', marks: 1 });
    expect(profile.rows[4].group?.options).toEqual(['Pasta', 'Ice cream']);
    expect(marksClaimed(profile, { 'r-2': 1, 'r-3': 2, 'r-4': 2, 'r-6': 2 }, { 'r-1': [0, 1], 'r-5': [0, 1] })).toBe(10);
    expect(point('2a-1').rows.map(row => row.verbatim)).toEqual(['Ronan', 'Marie / Mary', 'Paul']);
    expect(point('1-4-i').rows[0].verbatim).toBe('2,000 yen');
    expect(point('1-4-ii').rows[0].verbatim).toBe('3,000 yen');
  });

  it('preserves every finite response and Japan partial credit within the two-country quota', () => {
    expect(point('1-3').rows[0].group).toEqual({ claimMax: 2, perOption: 2, options: ['Yoga', 'cooking', 'jogging'] });
    expect(point('2a-3').rows[0].group?.options).toEqual(['Name is Sudou Genki', 'manager of college wrestling club', 'actor', 'interesting']);
    const rubric = points('2a-2');
    expect(rubric.groups.map(group => group.rows[0].text)).toEqual(['France', 'America', 'Russia', 'Korea', 'Japan']);
    expect(rubric.groups.map(group => group.rows[0].marks)).toEqual([2, 2, 2, 2, 1]);
    const scores: LanguageScores = { 'language:group:item-1': 1, 'language:row:item-1:answer': 1, 'language:group:item-5': 1, 'language:row:item-5:answer': 1 };
    expect(languagePointsMarks(rubric, scores)).toBe(3);
    scores['language:group:item-2'] = 1;
    scores['language:row:item-2:answer'] = 1;
    expect(languagePointsMarks(rubric, scores)).toBe(4);
    expect(point('3a-1').rows[0]).toMatchObject({ verbatim: 'Judo', marks: 2 });
    expect(point('3a-1').rows[1].group?.options.map(text => text.trim())).toEqual(['Aikido', 'rugby']);
    expect(point('3a-2').rows[0]).toMatchObject({ verbatim: 'Kendo', marks: 2 });
    expect(point('3a-2').rows[1].group?.options).toEqual(['Badminton', 'shopping']);
    expect(marksClaimed(point('3a-1'), {}, { 'r-2': [0, 1] })).toBe(2);
    const culture = point('2d');
    expect(culture.rows[0]).toMatchObject({ verbatim: UNPRINTED_ANSWER, unprinted: true, permittedMarks: [0, 2, 4] });
    expect(culture.rows[0].parts?.map(part => part.marks)).toEqual([2, 2]);
    expect(marksClaimed(culture, { 'r-1:point-1': 2, 'r-1:point-2': 2 })).toBe(4);
  });

  it('keeps all true/false evidence, kanji distractors and required grammar forms', () => {
    for (const [suffix, count, total] of [['2b', 5, 15], ['2c', 10, 10], ['3b-1', 5, 10], ['3b-2', 5, 10]] as const) {
      const rubric = points(suffix);
      expect(rubric.count).toBe(count);
      expect(rubric.groups).toHaveLength(count);
      const scores: LanguageScores = {};
      for (const group of rubric.groups) {
        scores[`language:group:${group.id}`] = 1;
        for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 1;
      }
      expect(languagePointsMarks(rubric, scores)).toBe(total);
    }
    expect(points('2b').groups.map(group => group.rows.map(row => row.marks))).toEqual(Array(5).fill([1, 2]));
    expect(points('2b').groups.map(group => group.rows[0].text)).toEqual(['False', 'False', 'True', 'True', 'False']);
    expect(points('2b').groups[4].rows[1].text).toContain('ロンドンのコンサートに行きます。');
    expect(points('2c').groups.map(group => group.rows[0].text)).toEqual(['a', 'b', 'c', 'c', 'a', 'd', 'a', 'd', 'b', 'c']);
    expect(card('2c').questionText).toContain('(d) month');
    expect(points('3b-1').groups.map(group => group.rows[0].text)).toEqual(['行きません。', 'おもしろいです。', 'じゃありません./じゃないです。', 'します。', '食べます。']);
    expect(points('3b-2').groups.map(group => group.rows[0].text)).toEqual(['b. の', 'c. は', 'c. と', 'a. まで', 'c. から']);
    expect(point('3a-4-i').rows[0].verbatim).toBe('(ちょっと) むじかしいです。');
    expect(point('3a-4-i').rows[0].contextNote).toContain('むずかしい');
  });

  it('retains all ten cloze blanks and exact conditional alternatives under one word-use rule', () => {
    const found = point('4');
    expect(found.rows).toHaveLength(10);
    expect(found.taskGroups?.map(group => [group.label, group.marks, group.rowIds])).toEqual(
      ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'].map((roman, index) => [`(${roman})`, 3, [`r-${index + 1}`]]),
    );
    expect(found.rows.every(row => row.kind === 'anyN' && row.group?.claimMax === 1 && row.group.perOption === 3)).toBe(true);
    expect(found.rows.map(row => row.group?.options)).toEqual([
      ['日本りょうり', '学校'], ['バスで'], ['二十分'], ['おいしい', '大好き', '日本りょうり'], ['飲みます'],
      ['見ます'], ['大好き'], ['うちに', 'バスで'], ['とても'], ['学校'],
    ]);
    expect(found.questionText).toContain('A word should be used only once.');
    expect(found.questionText).toContain('20 分');
    expect(found.questionText).toContain('たのしい');
    expect(found.rows[0].contextNote).toContain('（学校 accepted if not used elsewhere）');
    expect(found.rows[3].contextNote).toContain('（大好き/日本料理  accepted if not used elsewhere）');
    expect(found.rows[7].contextNote).toContain('(バスで  accepted if not used elsewhere）');
    for (const row of [found.rows[0], found.rows[3]]) {
      expect(row.contextNote).toContain('日本りようり');
      expect(row.contextNote).toContain('日本料理');
    }
    expect(marksClaimed(found, {}, Object.fromEntries(found.rows.map(row => [row.id, [0]])))).toBe(30);
  });

  it('keeps a whole four-mark telephone response and the explicit two-mark illness partial', () => {
    const phone = point('lb-1-iii');
    expect(phone.rows).toHaveLength(1);
    expect(phone.rows[0]).toMatchObject({ verbatim: '03-6576-8180', marks: 4 });
    expect(phone.rows[0].contextNote).toContain('no per-digit tariff');
    expect(phone.questionFigure).toBeDefined();
    expect(phone.audioMaterial).toBeDefined();
    const illness = point('lc-2-i');
    expect(illness.rows[0].permittedMarks).toEqual([0, 2, 4]);
    expect(illness.rows[0].verbatim).toContain('38');
    expect(illness.rows[0].verbatim).toContain('sore throat');
    expect(illness.rows[0].contextNote).toContain('feels sick');
    expect(marksClaimed(illness, { 'r-1': 2 })).toBe(2);
    expect(marksClaimed(illness, { 'r-1': 4 })).toBe(4);
    expect(cards.filter(card => card.audioMaterial)).toHaveLength(26);
  });
  it('keeps all seven place/weekend prompts and independent five-response expression caps', () => {
    const rubric = points('5');
    expect(rubric.count).toBe(5);
    expect(rubric.groups).toHaveLength(7);
    expect(rubric.markingGuideNote).toContain('どうやった');
    expect(rubric.groups[4].label).toContain('どうやって');
    expect(rubric.groups[6].label).toContain('すみたいですか。');
    expect(rubric.groups[0].criteria?.[1].bands?.[0].guidance.join(' ')).toContain('Vocabulary very inadequate');
    expect(rubric.groups[0].criteria?.[1].bands?.[2].guidance.join(' ')).toContain('Good use of Genkouyoushi');
    const scores: LanguageScores = {};
    for (const group of rubric.groups) {
      expect(group.criteria?.map(criterion => criterion.maxMarks)).toEqual([5, 5]);
      scores[`language:group:${group.id}`] = 1;
      for (const criterion of group.criteria ?? []) scores[`language:${criterion.id}`] = 5;
    }
    expect(languagePointsMarks(rubric, scores)).toBe(50);
    for (const group of rubric.groups.slice(5)) scores[`language:group:${group.id}`] = 0;
    scores['language:item-1-content'] = 3;
    expect(languagePointsMarks(rubric, scores)).toBe(46);
    scores['language:item-2-content'] = 3;
    expect(languagePointsMarks(rubric, scores)).toBe(42);
    scores['language:item-1-content'] = 4;
    expect(languagePointsMarks(rubric, scores)).toBe(45);
    scores['language:group:item-2'] = 0;
    expect(languagePointsMarks(rubric, scores)).toBe(39);
  });

  it('binds exactly23 reading and26 listening conditions to the original source selectors', () => {
    expect(cards.filter(card => card.answerLanguageRule)).toHaveLength(49);
    expect(cards.filter(card => card.answerLanguageRule?.penalizedLanguage === 'Japanese')).toHaveLength(26);
    for (const found of cards.filter(card => card.answerLanguageRule)) {
      const rule = found.answerLanguageRule!;
      expect(review.selectors.some(selector => selector.document === 'scheme' && selector.text === rule.sourceText && rule.schemePages.includes(selector.page))).toBe(true);
      expect(rule.otherLanguageMultiplier).toBe(0.5);
      expect(rule.sourceText).toBe(found.audioMaterial ? '(1/2 marks if answered in Japanese, romaji or Japanese script)' : '(Half marks if not answered in the appropriate language)');
    }
    expect(cards.some(card => card.extraneousMaterialRule)).toBe(false);
    expect(card('4').answerLanguageRule).toBeUndefined();
    expect(card('5').answerLanguageRule).toBeUndefined();
  });

  it('retains all19 written and14 aural Atlas anchors and seven full source crops', () => {
    expect(cards.filter(card => 'questionFigure' in card && card.questionFigure)).toHaveLength(7);
    const tags = JSON.parse(readFileSync(resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'), 'utf8'));
    for (const task of census.tasks) {
      const sidecar = map(task.atlas.fileid);
      const group = sidecar.q.find(question => question.n === task.atlas.questionNumber)!;
      const runtime = cards.find(card => card.id === idFor(task.key))!;
      expect(task.paperPages, runtime.id).toContain(group.pP);
      expect(task.schemePages.every(page => group.region.some(region => region.p === page)), runtime.id).toBe(true);
      const tagged = tags.find((paper: { year: number; fileid: string }) => paper.year === 2015 && paper.fileid === task.atlas.fileid);
      expect(tagged.q.find((question: { n: string }) => question.n === task.atlas.questionNumber).primary, runtime.id).toBe(runtime.topicId);
      expect(sidecar.band).toEqual([1, 16]);
    }
    expect(map('LC058GLP000EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 19 }, (_, i) => String(i + 1)));
    expect(map('LC058GLPA00EV.pdf').q.map(question => question.n)).toEqual(Array.from({ length: 14 }, (_, i) => String(i + 1)));
  });
});
