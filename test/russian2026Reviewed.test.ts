import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/russian/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/russian/ordinary';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import legacy from '../scripts/markbank/authored/russian.json';
import sources from '../scripts/markbank/authoring/russian-reviewed-sources.json';
import audio from '../data/russianAudio.json';
import { languageMarks, languageScoreId, languageLengthId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
import { HOSTED_ANSWER_OVERRIDES } from '../components/PaperTrail/vaultResolve';
import { reviewedRussianJointTask } from '../scripts/markbank/russianJointTasks.mjs';

const get = (suffix: string) => {
  const card = REVIEWED_CARDS.find(card=>card.id===`ru-2026-hl-${suffix}`);
  if (!card) throw new Error(suffix);
  return card;
};
const reviewedHigher = REVIEWED_CARDS.filter(card => card.year === 2026 && card.level === 'higher');

describe('Russian 2026 Higher independent source review', () => {
  it('preserves all199 prior IDs and covers46 complete reviewed tasks', () => {
    const runtime = new Set([...HIGHER,...ORDINARY].map(card=>card.id));
    expect(legacy.every(card=>runtime.has(card.id))).toBe(true);
    expect(HIGHER.length).toBeGreaterThanOrEqual(129);
    expect(ORDINARY.length).toBeGreaterThanOrEqual(116);
    expect(reviewedHigher).toHaveLength(46);
    expect(reviewedHigher.every(tariffReconciles)).toBe(true);
    expect(reviewedHigher.reduce((sum,card)=>sum+card.totalMarks,0)).toBe(320);
    expect(reviewedHigher.filter(card=>card.audioMaterial).reduce((sum,card)=>sum+card.totalMarks,0)).toBe(80);
  });
  it('keeps the full printed pools and never invents a grammar tariff', () => {
    const winter=get('la1-ii'), grammar=get('gr');
    expect(winter.kind==='question' && winter.rows[0].group?.options).toHaveLength(19);
    expect(grammar.kind==='question' && grammar.tariffModel.kind).toBe('questionTotal');
    expect(grammar.kind==='question' && grammar.rows).toHaveLength(14);
    expect(grammar.kind==='question' && grammar.rows.every(row=>row.marks===null)).toBe(true);
    expect(get('gw').questionRef).toBe('2026 HL Section GW Q3');
    expect(get('gw').sourceMaterial?.pages).toEqual([13,14]);
    expect(get('gw').questionText).toContain('to college.');
    expect(get('se').questionText.split('\n').filter(line=>line.startsWith('• '))).toHaveLength(5);
  });
  it('scores partial listening answers within the printed two-answer quota', () => {
    const card=get('l3-2-ii');
    if(!isRubricCard(card))throw new Error('Missing listening rubric');
    const scores={
      [languageGroupId('answer-2')]:1,[languageRowId('answer-2','partial-1')]:1,
      [languageGroupId('answer-4')]:1,[languageRowId('answer-4','full')]:1,
    };
    expect(languageMarks(card,scores)).toBe(3);
    expect(languageMarks(card,{...scores,[languageRowId('answer-2','full')]:1})).toBe(4);
  });
  it('applies the actual essay threshold before its title deduction', () => {
    const card=get('se');
    if(!isRubricCard(card))throw new Error('Missing essay rubric');
    const scores={ [languageScoreId('content')]:6,[languageScoreId('title-penalty')]:1,
      [languageScoreId('expression')]:20,[languageLengthId('words')]:50 };
    expect(languageMarks(card,scores)).toBe(25);
    expect(languageMarks(card,{...scores,[languageScoreId('content')]:4})).toBe(17);
    expect(languageMarks(card,{...scores,[languageLengthId('words')]:24})).toBe(19);
    expect(languageMarks(card,{...scores,[languageScoreId('content')]:0})).toBe(0);
  });
  it('includes separately assessed summary skills', () => {
    const card=get('c2-1');
    if(!isRubricCard(card))throw new Error('Missing summary rubric');
    const scores:Record<string,number>={ [languageScoreId('summary-skills')]:2 };
    for(const n of [1,2,3,4]) {
      scores[languageGroupId(`answer-${n}`)]=1;
      scores[languageRowId(`answer-${n}`,'full')]=2;
    }
    expect(languageMarks(card,scores)).toBe(10);
  });
  it('applies the Higher zero-language rule only to mandated answers', () => {
    expect(reviewedHigher.filter(card=>card.answerLanguageRule)).toHaveLength(18);
    for(const card of reviewedHigher.filter(card=>card.answerLanguageRule)) {
      expect(card.answerLanguageRule?.otherLanguageMultiplier).toBe(0);
      expect(card.answerLanguageRule?.schemePages).toEqual([3]);
    }
    for(const suffix of ['la2-i','la2-ii','sd','gr','l1-1-i']) expect(get(suffix).answerLanguageRule).toBeUndefined();
    expect(ORDINARY.every(card=>!card.answerLanguageRule)).toBe(true);
    const comprehension=get('c1-1-i'), grammar=get('gr');
    expect(comprehension.kind==='question' && comprehension.rows[0].contextNote).toContain('English or Irish');
    expect(grammar.kind==='question' && grammar.rows[0].contextNote).toContain('does not print separate marks for individual forms');
    const card=get('c2-1');
    if(!isRubricCard(card)) throw new Error('Missing summary rubric');
    const scores={ [languageGroupId('answer-1')]:1,[languageRowId('answer-1','full')]:2,
      [languageGroupId('answer-2')]:1,[languageRowId('answer-2','full')]:2 };
    expect(languageMarks(card,scores)).toBe(4);
    expect(languageMarks(card,{...scores,[languageOtherLanguageId('row:answer-1:full')]:1})).toBe(2);
  });
  it('binds every task to reachable original-paper and scheme anchors', () => {
    for(const source of sources) {
      const card=REVIEWED_CARDS.find(card=>card.id===source.id);
      if(!card)throw new Error(`Missing reviewed Russian task ${source.id}`);
      const joint=reviewedRussianJointTask(source,card);
      const questions=joint??[{n:source.id.replace(/^ru-\d+-[a-z]+-/,''),
        questionPages:source.questionPages??source.paperPages,schemePages:source.schemePages}];
      const file=`${source.year}/${source.paperFileid}.json`;
      const map=JSON.parse(readFileSync(resolve(__dirname,'../public/paper-answers',file),'utf8'));
      for(const original of questions) {
        const matching=map.q.filter((q:{n:string})=>q.n===original.n);
        expect(matching).toHaveLength(1);
        const question=matching[0];
        expect(question.paperRegion.map((region:{p:number})=>region.p)).toEqual(source.paperPages);
        expect(question.region.map((region:{p:number})=>region.p)).toEqual(original.schemePages);
        expect(question.pP).toBe(original.questionPages[0]);
        if(joint)expect(question.markBankCardId).toBe(source.id);
        expect(PAPER_TOPIC_TAGS.find(p=>p.subjectId==='russian'&&p.year===source.year&&p.fileid===source.paperFileid)?.q.some(q=>q.n===original.n&&q.primary===source.topicId)).toBe(true);
      }
      expect(map.schemeFileid).toBe(source.schemeFileid);
      expect(HOSTED_ANSWER_OVERRIDES.has(`russian|${source.year}|${source.paperFileid}`)).toBe(true);
      expect(PAPER_TRAIL_INDEX.russian.find(p=>p.year===source.year&&p.level===source.level&&p.lang==='ev')?.papers.find(p=>p.doc.f===source.paperFileid)?.answers).toBe(1);
    }
  });
  it('uses only verified audio while retaining the playback-QA limitation', () => {
    expect(audio).toHaveLength(17);
    expect(audio.every(record=>record.verification.status==='full-file-verified' && record.verification.sha256.length===64)).toBe(true);
    expect(audio.every(record=>record.verification.browserPlayback===false)).toBe(true);
    for(const card of reviewedHigher.filter(card=>card.audioMaterial)) {
      expect(card.paperFileid).toBe('LC099ALPA00BV');
      expect(card.audioMaterial?.canonicalUrl).toBe(audio.find(record=>record.year===2026)?.source.canonicalUrl);
    }
  });
});
