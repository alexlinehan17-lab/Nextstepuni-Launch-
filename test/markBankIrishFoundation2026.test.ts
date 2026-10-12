import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2026-authored.json';
import sourceReview from '../scripts/markbank/authored/irish-foundation-2026-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { cardsForTopic } from '../components/MarkBank/deck';
import { combinedListeningAssessment, irishMarks, irishScoreId } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2026);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;
const guide=(key:string,id:string)=>get(key).criteria.find(c=>c.id===id)!.guidance.join(' ');

describe('2026 Foundation source reconciliation',()=>{
  it('retains every published boundary and carries both closed choose-two instructions on their options',()=>{
    expect(cards).toHaveLength(58);
    expect(new Set(cards.map(c=>c.id)).size).toBe(58);
    for(const card of cards) expect(tariffReconciles(card),card.id).toBe(true);
    for(const card of cards) expect(card.schemeRegion?.schemeFileid).toBe('LC001BLP100IV.pdf');
    expect(authored.review.atomicPracticeCardIds).toHaveLength(58);
    // Choice is not a route: no per-combination cards for either choose-two pool.
    expect(authored.review).not.toHaveProperty('pairedRouteCardIds');
    expect(authored.cards.filter(c=>/^R-[23]-[ABC]{2}$|^W-[45][AB]-[45][AB]$/.test(c.atlasQuestionId))).toEqual([]);
    for(const n of [2,3]) {
      const parts=authored.cards.filter(c=>new RegExp(`^R-${n}[ABC]-\\d$`).test(c.atlasQuestionId));
      expect(parts).toHaveLength(15);
      for(const c of parts) expect(c.taskRequirements[0],c.id).toBe(`Ceist ${n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.`);
    }
    for(const key of ['W-4A','W-4B','W-5A','W-5B']) {
      expect(get(key).taskRequirements[0],key).toBe('Freagair dhá cheist ar bith as na ceithre cinn seo a leanas: 4 (a), 4 (b), 5 (a) nó 5 (b).');
    }
  });

  it('keeps the unequal published listening tariffs and the official 2026 recording',()=>{
    const listening=cards.filter(c=>Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined=combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([3,4,5]);
    expect(combined.audioMaterial.playbackUrl).toBe('https://www.examinations.ie/archive/exampapers/2026/LC001BLP017IV.mp3');
    expect(authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-')).map(c=>[c.totalMarks,c.criteria[0].guidance[0]])).toEqual([
      [10,'Rugbaí = an chéad phictiúr'],[4,'Sasana'],[10,'Seó damhsa = an ceathrú pictiúr'],[4,'I mí Eanáir'],
      [8,'Oifig turasóireachta = an tríú pictiúr'],[8,'An ceathrú bosca ag an mbarr (tic nó saighead sa bhosca)'],
      [8,'Go hálainn = an chéad phictiúr'],[8,'6 chéim Celsius'],[15,'Ar a seacht a chlog'],[5,'€490'],
      [10,'Dé hAoine'],[10,'Trí bhréag'],[10,'Damhsa an Séú Bliain'],[10,'I gcarrchlós na Scoile'],
    ]);
    for(const c of authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-'))) {
      expect(c.schemePages).toEqual([2]);
      expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);
    }
    expect(get('A-6b').questionText).toContain('€90\n€245\n€490');
  });

  it('uses every reading key at its own printed tariff, including the 1- and 2-mark parts',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('HGFBIJECDA');
    expect(guide('R-1-1','answer')).toContain('uimhir an phictiúir in ionad litir an phictiúir');
    const expected:[string,number][][]=[
      [['I mí Feabhra',1],['Is eagarthóir é',6],['Ailt a scríobh sé féin',6],['A spéis i gcúrsaí polaitíochta',6],['Scoláirí eile',6]],
      [['Ceithre chéad acra',6],['Tá sé suite i lár na tíre',6],['Tá sé saor ó charranna',6],['Ar an bpáirc uisce',6],['Ní féidir',1]],
      [['Mí ó shin',6],['Ina sheomra codlata',1],['Briseadh croí',6],['Comórtas amhránaíochta',6],['Meangadh mór gáire',6]],
      [['Go raibh siad geallta',7],['Is realta cheoil í.',7],['Ceithre bliana déag d’aois/14',7],['Podchraoladh ráthúil',2],['Ar an 13 Meitheamh 2026',7]],
      [['San Iaráin',6],['Bhí an-trua acu dó / chun aire a thabhairt dó',6],['I bpuball',6],['Sa bhliain 1947',6],['Compórdach',6]],
      [['Taibhsín bídeach',7],['Múinteoirí',7],['Doras',7],['Eilifint',7],['Ríl',2]],
    ];
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) {
      for(let i=1;i<=5;i++) {
        const c=get(`R-${slot}-${i}`);
        expect([c.criteria[0].guidance[0],c.totalMarks],c.id).toEqual(expected[j][i-1]);
        expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);
        expect(c.sourceMaterial.pages).toEqual([j+7]);
        expect(c.schemePages).toEqual([j<3?4:5]);
      }
      expect(expected[j].reduce((sum,[,marks])=>sum+marks,0)).toBe(j<3?25:30);
    }
    expect(guide('R-3A-4','answer')).toContain('rathúil on the paper');
    expect(get('R-3C-1').questionText).toContain('“Taibhse mór”\n“Taibhsín bídeach”\n“Teach dhá stór”');
  });

  it('keeps the notice and London letter whole with the 2026 language table',()=>{
    expect(get('W-4A').criteria.map(c=>c.maxMarks)).toEqual([1,10,13,5,5,11]);
    expect(guide('W-4A','pictiur1')).toContain('dioscó ciúin');
    expect(guide('W-4A','pictiur3')).toContain('Calvin Harris');
    expect(guide('W-4A','pictiur4')).toContain('callairí nua');
    expect(guide('W-4A','pictiur4')).not.toContain('`');
    expect(guide('W-4A','pictiur2')).toContain('Beidh pionós -1');
    const letter=get('W-4B');
    expect(letter.criteria.map(c=>[c.id,c.maxMarks])).toEqual([
      ['seoladh',2],['data',1],['beannu',1],['crioch',2],['pictiur1',7],['pictiur2',7],['pictiur3',7],['pictiur4',7],['gaeilge',11],
    ]);
    expect(letter.schemePages).toEqual([10,11]);
    expect(letter.questionText.match(/dhá phointe eolais/g)).toHaveLength(4);
    expect(letter.questionText).toContain('Turas go Londain\nDé hAoine 9 Meitheamh – Dé Domhnaigh 11 Meitheamh\nCostas €200');
    expect(letter.sourceDiscrepancyNotice).toContain('Foirm Iarratais');
    for(const key of ['W-4A','W-4B','W-5A','W-5B']) {
      expect(guide(key,'gaeilge')).toContain('An-mhaith 6–8; Maith / Maith go leor 3–5; Lag / An-lag 0–2');
      expect(guide(key,'gaeilge')).not.toContain('An-mhaith 7–8');
    }
    expect(cardsForTopic('irish-2-8',cards)).toContain(cards.find(c=>c.id==='irish-2026-fl-w-4b')!);
    expect(cardsForTopic('irish-9-4',cards)).toContain(cards.find(c=>c.id==='irish-2026-fl-w-5a')!);
  });

  it('applies the missing-reference caps and the length table only to the story communication award',()=>{
    for(const slot of ['5A','5B']) {
      const c=get('W-'+slot);
      expect(c.criteria.filter(r=>r.kind==='award').map(r=>r.maxMarks)).toEqual([34,11]);
      expect(c.criteria.find(r=>r.id==='length')).toMatchObject({kind:'deduction',maxMarks:4,deductFrom:'cumarsaid'});
      expect(guide('W-'+slot,'cumarsaid')).toContain('30, 26, 22, 18 or 14');
      expect(guide('W-'+slot,'length')).toContain('Fad = −0');
    }
    expect(get('W-5A').sourceDiscrepancyNotice).toContain('Féile cheoil');
    expect(guide('W-5B','cumarsaid')).toContain('An madra caillte');
    expect(get('W-5B').questionText).toContain('2. Ar strae / Trína chéile');
    const story=cards.find(c=>c.id==='irish-2026-fl-w-5a')!;
    if(story.rubric.system!=='irish') throw new Error('Wrong rubric');
    const scores=Object.fromEntries(story.rubric.criteria.map(c=>[irishScoreId(c.id),c.kind==='award'?c.maxMarks:0]));
    expect(irishMarks(story,scores)).toBe(45);
    scores['irish:cumarsaid']=26;
    scores['irish:length']=3;
    expect(irishMarks(story,scores)).toBe(34); // 26 − 3 communication + 11 language; the deduction never reaches the language award.
  });

  it('joins all 58 cards to Atlas with the right pages, topics and disclosed scheme carry-overs',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2026/LC001BLP100IV.pdf.json','utf8'));
    const q=(n:string)=>map.q.find((q:{n:string})=>q.n===n);
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2026,'main',n,'p1','iv','LC001BLP100IV.pdf');
    expect(map.schemeFileid).toBe('LC001BLP100IV.pdf');
    for(const c of authored.cards) {
      expect(topics(c.atlasQuestionId).flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      expect(q(c.atlasQuestionId).paperRegion.map((r:{p:number})=>r.p),c.id).toEqual(c.sourceMaterial.pages);
      expect(q(c.atlasQuestionId).region.map((r:{p:number})=>r.p),c.id).toEqual(c.schemePages);
      if('audioMaterial' in c) expect(q(c.atlasQuestionId).audioMaterial).toEqual(c.audioMaterial);
    }
    expect(topics('W-4B')).toEqual(['irish-foundation-write-a-letter']);
    expect(topics('3')).not.toContain('irish-foundation-fill-in-a-form');
    expect(q('1').audioMaterial.playbackUrl).toContain('/2026/LC001BLP017IV.mp3');
    for(const n of ['W-4B','W-5A','3']) expect(q(n).practiceInstruction,n).toContain('Nóta foinse');
    expect(map.q.some((q:{n:string})=>/^W-[45][AB]-[45][AB]$|^R-[23]-[ABC]{2}$/.test(q.n))).toBe(false);
    expect(q('W-4B').practiceInstruction.match(/Foirm Iarratais/g)).toHaveLength(1);
    expect(q('3').practiceInstruction.match(/Nóta foinse/g)).toHaveLength(2);
  });

  it('rejects unknown and stale raw selection directives',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2026 import selection_decisions
review=json.load(sys.stdin)
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==32
original=pages[14].text
for edited in [original+'\nRoghnaigh ceann amháin den dá cheann seo.\n',original.replace('Faoin bpóstaer','Maidir leis an bpóstaer')]:
 pages[14].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(sourceReview)});
    expect(result).toContain('source guard passed');
  });

  it('records all visually reviewed pages and reconciles the paper without claiming archive completion',()=>{
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(authored.review.reviewedSchemePages).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(authored.review.examStructure).toEqual({listening:120,matching:40,readingQ2:50,readingQ3:60,writing:90,total:360});
    expect(authored.review.openIssues).toEqual([]);
    const row=inventory.papers.find(p=>p.key==='2026|foundation|LC001BLP100IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(63);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
