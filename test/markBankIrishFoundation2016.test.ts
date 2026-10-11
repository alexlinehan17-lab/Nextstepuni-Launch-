import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2016-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { combinedListeningAssessment, irishMarks } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2016);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2016 Foundation independently reviewed boundaries',()=>{
  it('requires one Q4 and one Q5 and expands all three internal form jobs',()=>{
    expect(cards).toHaveLength(74);
    expect(new Set(cards.map(c=>c.id)).size).toBe(74);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    expect(authored.review.examStructure).toEqual({listening:120,matching:40,readingQ2:50,readingQ3:60,writingQ4:40,writingQ5:50,writing:90,total:360});
    expect(authored.review.atomicPracticeCardIds).toHaveLength(60);
    expect(authored.review.pairedRouteCardIds).toHaveLength(14);
    const routes=authored.cards.filter(c=>/^W-.*-5[AB]$/.test(c.atlasQuestionId));
    expect(routes.map(c=>c.atlasQuestionId)).toEqual([
      'W-4A-5A','W-4A-5B','W-4B-glantoir-5A','W-4B-glantoir-5B',
      'W-4B-garraiodoir-5A','W-4B-garraiodoir-5B','W-4B-freastalai-5A','W-4B-freastalai-5B',
    ]);
    for(const c of routes) {
      expect(c.totalMarks).toBe(90);
      expect(c.questionText).toContain('FREAGAIR GACH CEIST (4 AGUS 5)');
      expect(c.memberCardIds).toHaveLength(2);
      expect(c.sourceMaterial.pages).toEqual([c.atlasQuestionId.includes('4A')?14:15,c.atlasQuestionId.endsWith('5A')?16:17]);
    }
    for(const n of [2,3]) {
      const pairs=authored.cards.filter(c=>new RegExp(`^R-${n}-[ABC]{2}$`).test(c.atlasQuestionId));
      expect(pairs.map(c=>c.atlasQuestionId)).toEqual(['AB','AC','BC'].map(p=>`R-${n}-${p}`));
      for(const c of pairs) {
        expect(c.totalMarks).toBe(n===2?50:60);
        expect(c.criteria).toHaveLength(10);
        expect(c.sourceMaterial.pages).toHaveLength(2);
      }
    }
  });

  it('keeps the fourteen listening answers, full map and complete official recording',()=>{
    const listening=cards.filter(c=>Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined=combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([2,3,4]);
    expect(combined.audioMaterial.playbackUrl).toContain('/2016/LC001BLP017IV.mp3');
    const tasks=authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-'));
    tasks.forEach(c=>expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]));
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'Craoltóir Raidió = an tríú pictiúr','T-léine agus jíons','Iascaire trálaera = an ceathrú pictiúr','Sos breá',
      'Siopa seodóra = an chéad phictiúr','An bosca ag an mbarr ar chlé (tic nó saighead sa bhosca)',
      'Grianmhar, te = an dara pictiúr','Seanbhean','I siopa leabhar','A deich a chlog',
      'Dé Sathairn','Péinteáil','Chun bille a íoc','Ar an mbord',
    ]);
  });

  it('retains the full poem and every published partial-credit answer',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('CHEGJIABFD');
    const expected=[
      ['29 Feabhra','Grád B','Peil','Foirm iarratais','Stiúrthóir'],
      ['I measc na gcnoc','Baile Bhuirne','Ar bharr na gcnoc','Cór Chúil Aodha','Amhránaíocht ar an sean-nós'],
      ['Mí an Mhárta','Na tuismitheoirí','Sa seomra suí','D’imir siad cártaí','An bothán adhmaid'],
      ['Henry Shefflin','2000','Deich n-uaire','Bhris sé cnámh ina chos chlé','Ar theilifís RTÉ'],
      ['Northampton','Snámh','Ceoltóir','Chun clú agus cáil a bhaint amach mar amhránaí','Foden'],
      ['Sionnach','I lár na cathrach','Bia blasta','Bia dóite','I rith an lae'],
    ];
    const partials:Record<string,number[]>={'3A-4':[0,2,3,4,5,6],'3B-4':[0,2,3,6],'3C-3':[0,4,6]};
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual(partials[`${slot}-${i}`]??[0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+6]);
      expect(c.schemePages).toEqual([j<3?5:j===5?7:6]);
    }
    expect(get('R-3A-4').criteria[0].guidance).toContain('5 mharc: Bhris sé cnámh ina chos; Ghortaigh sé cnámh ina chos chlé.');
    expect(get('R-3A-4').criteria[0].guidance).toContain('2 mharc: An t-alt ar fad: “Bronnadh ... 2012”.');
    expect(get('R-3B-4').criteria[0].guidance).toContain('2 mharc: Mar amhránaí. “Amhránaí” leis féin = 0.');
    expect(get('R-3C-3').criteria[0].guidance).toContain('4 mharc: Véarsa3 ar fad mar fhreagra.');
    for(const [part,scores] of Object.entries(partials)) {
      for(const pair of ['AB','AC','BC'].filter(p=>p.includes(part[1]))) {
        expect(get('R-3-'+pair).criteria.find(c=>c.id==='r-'+part.toLowerCase()+'-answer')!.permittedMarks).toEqual(scores);
      }
    }
  });

  it('keeps the notice submarks and each whole form with one language award',()=>{
    const notice=get('W-4A');
    expect(notice.criteria.map(c=>c.maxMarks)).toEqual([1,8,13,4,4,10]);
    expect(notice.criteria.find(c=>c.id==='pictiur3')!.guidance.join(' ')).toContain('Paul O’Connell');
    expect(notice.criteria.find(c=>c.id==='pictiur2')!.guidance.join(' ')).toContain('3ú – 5ú (gan an mhí)');
    expect(notice.criteria.find(c=>c.id==='pictiur4')!.guidance.join(' ')).toContain('Peataí ar Strae');
    const forms=authored.cards.filter(c=>/^W-4B-(glantoir|garraiodoir|freastalai)$/.test(c.atlasQuestionId));
    expect(forms).toHaveLength(3);
    for(const [i,form] of forms.entries()) {
      expect(form.totalMarks).toBe(40);
      expect(form.questionText).toContain('Tadhg de Brún');
      expect(form.questionText).toContain('post samhraidh sa chumann gailf seo');
      expect(form.questionText).toContain('An rogha don chárta seo: '+['Glantóir','Garraíodóir','Freastalaí'][i]+'.');
      expect(form.questionText).toContain('Ainmnigh cúig ábhar scoile');
      expect(form.questionText).toContain('Luaigh trí chaitheamh aimsire');
      expect(form.criteria.map(c=>[c.id,c.maxMarks])).toEqual([['fields',15],['paragraph',15],['gaeilge',10]]);
      expect(form.sourceMaterial.pages).toEqual([15]);
      expect(form.schemePages).toEqual([12,13]);
      const fields=form.criteria[0].guidance.join(' ');
      expect(fields).toContain('21 ÷ 2 = 10½ → 11');
      expect(fields).toContain('Do not round each half-mark field separately');
      expect(fields).toContain('Cén post ba mhaith leat?');
      expect(fields).toContain('Glac le tic amháin');
      expect(fields).toContain('tarracóir');
      const paragraph=form.criteria[1].guidance.join(' ');
      expect(paragraph).toContain('marc níos airde ná 8 as 15');
      expect(paragraph).toContain('(5) mura bhfuil an t-alt');
      expect(paragraph).toContain('25%');
      expect(paragraph).toContain('paragraph award only');
      expect(paragraph).not.toContain('35–40 focal: 0');
    }
    expect(forms[0].criteria).toEqual(forms[2].criteria);
  });

  it('confines paragraph and story length adjustments to their own awards in paired practice',()=>{
    for(const key of ['W-5A','W-5B']) {
      const story=get(key);
      expect(story.totalMarks).toBe(50);
      expect(story.criteria).toHaveLength(1);
      expect(story.criteria[0].label).toBe('Freagra iomlán · Cumarsáid 37 + Gaeilge 13');
      const guide=story.criteria[0].guidance.join(' ');
      expect(guide).toContain('50%');
      expect(guide).not.toContain('80–90 focal: 0');
      expect(guide).not.toContain('Sármhaith 9–11');
      expect(guide).toContain('belongs only to the modified marking scheme');
    }
    expect(get('W-5A').schemePages).toEqual([14]);
    expect(get('W-5B').schemePages).toEqual([15,16]);
    expect(get('W-5A').questionText).toContain('Cóisir Lá Breithe');
    expect(get('W-5B').questionText).toContain('stáisiún traenach');
    const pair=cards.find(c=>c.id==='irish-2016-fl-w-4b-glantoir-5b')!;
    if(pair.rubric.system!=='irish') throw new Error('wrong rubric');
    // Questions 21/30 -> 11/15; paragraph awarded12 reduced25% ->9;
    // language10 stays intact; 45-word story50 reduced50% ->25.
    const scores={'irish:w-4b-glantoir-fields':11,'irish:w-4b-glantoir-paragraph':9,
      'irish:w-4b-glantoir-gaeilge':10,'irish:w-5b-freagra':25};
    expect(irishMarks(pair,scores)).toBe(55);
  });

  it('joins every task and the restored whole sections to full Atlas paper/scheme regions',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2016/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2016,'main',n,'single','iv','LC001BLP000IV.pdf');
    for(const c of authored.cards) {
      expect(topics(c.atlasQuestionId).flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      const q=map.q.find((q:{n:string})=>q.n===c.atlasQuestionId);
      expect(q.paperRegion.map((r:{p:number})=>r.p),c.id).toEqual(c.sourceMaterial.pages);
      expect((q.schemeRegion??q.region).map((r:{p:number})=>r.p),c.id).toEqual(c.schemePages);
      if('audioMaterial' in c) expect(q.audioMaterial).toEqual(c.audioMaterial);
    }
    for(const [n,pages] of [['1',[2,3,4]],['2',[5,6,7,8,9,10,11]],['3',[13,14,15,16,17]]] as const) {
      expect(map.q.find((q:{n:string})=>q.n===n).paperRegion.map((r:{p:number})=>r.p)).toEqual(pages);
    }
    for(const n of ['W-4B','W-4B-glantoir','W-4B-garraiodoir','W-4B-freastalai']) expect(topics(n)).toEqual(['irish-foundation-fill-in-a-form']);
    expect(map.q.find((q:{n:string})=>q.n==='W-4B-freastalai').practiceInstruction).toContain('Freastalaí');
    expect(topics('R-2C')).toEqual(['irish-foundation-reading-newspaper-article']);
    expect(topics('3')).not.toContain('irish-foundation-write-a-letter');
    expect((map.q.find((q:{n:string})=>q.n==='3').schemeRegion??map.q.find((q:{n:string})=>q.n==='3').region).map((r:{p:number})=>r.p)).toEqual([8,9,10,11,12,13,14,15,16]);
    expect(map.band).toEqual([3,17]);
  });

  it('rejects unknown or stale raw selections and retains readable scheme glyphs',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json,fitz
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2016 import selection_decisions,scheme_page_text
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==25
original=pages[14].text
for edited in [original+'\nRoghnaigh dhá cheann.\n',original.replace('Glantóir','Cócaire')]:
 pages[14].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale selection')
doc=fitz.open('paper-trail-corpus/markingschemes/2016/LC001BLP000IV.pdf')
decoded=[scheme_page_text(p) for p in doc]
assert 'Craoltóir Raidió' in decoded[2]
assert 'Véarsa 3 ar fad mar fhreagra = 4 mharc' in decoded[6]
assert '21 ÷ 2 = 11 mharc' in decoded[11]
assert '25%' in decoded[12] and '50%' in decoded[13]
print('source guards passed')
`],{encoding:'utf8',input:JSON.stringify(authored)});
    expect(result).toContain('source guards passed');
    for(const card of authored.cards) for(const c of card.criteria) expect(c.guidance.join(' ')).not.toMatch(/[\uE000-\uF8FF]/);
    expect(authored.review.reviewedPaperPages).toHaveLength(20);
    expect(authored.review.reviewedSchemePages).toHaveLength(24);
    const row=inventory.papers.find(p=>p.key==='2016|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(72);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
