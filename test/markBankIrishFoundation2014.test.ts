import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2014-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { combinedListeningAssessment, irishMarks } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2014);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2014 Foundation independently reviewed boundaries',()=>{
  it('requires one Q4 and one Q5 and carries each printed choice on its options',()=>{
    expect(cards).toHaveLength(60);
    expect(new Set(cards.map(c=>c.id)).size).toBe(60);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    expect(authored.review.examStructure).toEqual({listening:120,matching:40,readingQ2:50,readingQ3:60,writingQ4:40,writingQ5:50,writing:90,total:360});
    expect(authored.review.atomicPracticeCardIds).toHaveLength(60);
    // Choice is not a route: no reading pairs and no writing combinations.
    expect(authored.review).not.toHaveProperty('pairedRouteCardIds');
    expect(authored.cards.filter(c=>'memberCardIds' in c)).toEqual([]);
    for(const n of [2,3]) for(const c of authored.cards.filter(c=>new RegExp(`^R-${n}[ABC]-\\d$`).test(c.atlasQuestionId))) {
      expect(c.taskRequirements[0],c.id).toBe(`Ceist ${n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.`);
    }
    for(const c of authored.cards.filter(c=>/^W-[45]/.test(c.atlasQuestionId))) expect(c.taskRequirements[0],c.id).toBe("FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).");
  });
  it('keeps the fourteen listening answers, full map and complete official recording',()=>{
    const listening=cards.filter(c=>Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined=combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([2,3,4]);
    expect(combined.audioMaterial.playbackUrl).toContain('/2014/LC001BLP017IV.mp3');
    const tasks=authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-'));
    tasks.forEach(c=>expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]));
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'Garda Síochána = an dara pictiúr','Cill Chainnigh','Lúthchleasaíocht = an ceathrú pictiúr','Scoláireacht',
      'An bhunscoil = an tríú pictiúr','An bosca ag an mbarr ar dheis (tic nó saighead)',
      'Fliuch = an chéad phictiúr','Tráthnóna amárach','Maidin Dé hAoine','Sa charr',
      'Seachtain ó shin','Printíseacht mar mheicneoir','Ag staidéar','Ag comórtas snámha',
    ]);
  });

  it('retains the full poem and every published partial-credit answer',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('DCIHAGEJFB');
    const expected=[
      ['Co. An Chabháin','Grád C','Obair pháirtaimseartha','€9','Bainisteoir'],
      ['An Charraig Fhinn','Carr','Trá ghainmheach','Machairí gailf','Siúlóidí breátha'],
      ['Deartháireacha','Corcaigh','Go barr an tsléibhe','A chos','An fhoireann tarrthála'],
      ['Páistí bunscoile','Sa Ghaeltacht','Sa mheánscoil','Éadaí faiseanta','Ar stíl imeartha rugbaí'],
      ['I gContae Mhaigh Eo','(chun) ( tús) an fhómhair a cheiliúradh','Bhí sé ag guí','Séipéal beag','Líon na gcuairteoirí'],
      ['70','Nach mbeidh sí óg arís','An croí istigh','Éisteann sí','Grá'],
    ];
    const partials:Record<string,number[]>={'3B-2':[0,3,6],'3C-2':[0,2,4,6]};
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual(partials[`${slot}-${i}`]??[0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+6]);
      expect(c.schemePages).toEqual([j<3?5:j===5?7:6]);
    }
    expect(get('R-3A-4').criteria[0].guidance.join(' ')).toContain('Caitheann sí éadaí faiseanta');
    expect(get('R-3B-2').criteria[0].guidance.join(' ')).toContain('ómós don ghrian');
    expect(get('R-3C-2').criteria[0].guidance.join(' ')).toContain('an véarsa ar fad: pionós −4');
    // Choice is not a route: each part keeps its own partial tariff; no pair card repeats it.
    expect(authored.cards.some(c=>/^R-[23]-[ABC]{2}$/.test(c.atlasQuestionId))).toBe(false);
  });

  it('keeps the notice submarks and each whole form with one language award',()=>{
    const notice=get('W-4A');
    expect(notice.criteria.map(c=>c.maxMarks)).toEqual([1,8,13,4,4,10]);
    expect(notice.criteria.find(c=>c.id==='pictiur3')!.guidance.join(' ')).toContain('Sharon Shannon');
    expect(notice.criteria.find(c=>c.id==='pictiur2')!.guidance.join(' ')).toContain('Cead isteach');
    expect(notice.criteria.find(c=>c.id==='pictiur4')!.guidance.join(' ')).toContain('Halla Spóirt Nua');
    const forms=authored.cards.filter(c=>/^W-4B-(cocaire|doirseoir|freastalai)$/.test(c.atlasQuestionId));
    expect(forms).toHaveLength(3);
    for(const [i,form] of forms.entries()) {
      expect(form.totalMarks).toBe(40);
      expect(form.questionText).toContain('Séamas Ó Néill');
      expect(form.questionText).toContain('post samhraidh san óstán seo');
      expect(form.questionText).toContain('An rogha don chárta seo: '+['Cócaire','Doirseoir','Freastalaí'][i]+'.');
      expect(form.questionText).toContain('Ainmnigh cúig ábhar scoile');
      expect(form.questionText).toContain('Luaigh trí chaitheamh aimsire');
      expect(form.criteria.map(c=>[c.id,c.maxMarks])).toEqual([['fields',15],['paragraph',15],['gaeilge',10]]);
      expect(form.sourceMaterial.pages).toEqual([15]);
      expect(form.schemePages).toEqual([13,14]);
      const fields=form.criteria[0].guidance.join(' ');
      expect(fields).toContain('21 ÷ 2 = 10½ → 11');
      expect(fields).toContain('Do not round each half-mark field separately');
      expect(fields).toContain('Cén post ba mhaith leat?');
      expect(form.questionText).toContain('Cuir tic le ceann amháin');
      expect(fields).toContain('Bebo');
      expect(fields).toContain('Meánteist');
      const paragraph=form.criteria[1].guidance.join(' ');
      expect(paragraph).not.toContain('marc níos airde ná 8');
      expect(paragraph).toContain('as (5) mura bhfuil sé');
      expect(paragraph).toContain('25%');
      expect(paragraph).toContain('paragraph award only');
      expect(paragraph).not.toContain('35–40 focal: 0');
    }
    expect(forms[0].criteria).toEqual(forms[2].criteria);
  });

  it('confines paragraph and story length adjustments to their own awards on separate cards',()=>{
    for(const key of ['W-5A','W-5B']) {
      const story=get(key);
      expect(story.totalMarks).toBe(50);
      expect(story.criteria).toHaveLength(1);
      expect(story.criteria[0].label).toBe('Freagra iomlán · Cumarsáid 37 + Gaeilge 13');
      const guide=story.criteria[0].guidance.join(' ');
      expect(guide).toContain('50%');
      expect(guide).not.toContain('80–90 focal: 0');
      expect(guide).not.toContain('Sármhaith 9–11');
      expect(guide).toContain('Do not apply that conversion to the standard rubric');
    }
    expect(get('W-5A').schemePages).toEqual([15]);
    expect(get('W-5B').schemePages).toEqual([16]);
    expect(get('W-5A').questionText).toContain('Féile Cheoil');
    expect(get('W-5B').questionText).toContain('amuigh ag siúl le do chara');
    const form=cards.find(c=>c.id==='irish-2014-fl-w-4b-cocaire')!;
    const story=cards.find(c=>c.id==='irish-2014-fl-w-5b')!;
    if(form.rubric.system!=='irish'||story.rubric.system!=='irish') throw new Error('wrong rubric');
    // Choice is not a route: form and story are marked on their own cards.
    // Questions 21/30 -> 11/15; paragraph awarded12 reduced25% ->9;
    // language10 stays intact; 45-word story50 reduced50% ->25.
    expect(irishMarks(form,{'irish:fields':11,'irish:paragraph':9,'irish:gaeilge':10})).toBe(30);
    expect(irishMarks(story,{'irish:freagra':25})).toBe(25);
  });

  it('joins every task and the restored whole sections to full Atlas paper/scheme regions',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2014/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2014,'main',n,'single','iv','LC001BLP000IV.pdf');
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
    for(const n of ['W-4B','W-4B-cocaire','W-4B-doirseoir','W-4B-freastalai']) expect(topics(n)).toEqual(['irish-foundation-fill-in-a-form']);
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
from irish_foundation_2014 import selection_decisions,scheme_page_text
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==23
original=pages[14].text
for edited in [original+'\nRoghnaigh dhá cheann.\n',original.replace('ceann amháin','dhá cheann')]:
 pages[14].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale selection')
doc=fitz.open('paper-trail-corpus/markingschemes/2014/LC001BLP000IV.pdf')
decoded=[scheme_page_text(p) for p in doc]
assert 'Garda Síochána' in decoded[2]
assert 'An véarsa ar fad (-4)' in decoded[6]
assert '21 ÷ 2 = 10½  = 11 mharc' in decoded[12]
assert '25%' in decoded[13] and '50%' in decoded[14]
for i in range(2,22): assert f'Lch {i-1}' in decoded[i],i
assert 'Tasc  →' in decoded[8]
class UnknownPage:
 number=0
 def get_text(self,mode): return {'blocks':[{'lines':[{'spans':[{'font':'Cambria','text':'X'}]}]}]}
try: scheme_page_text(UnknownPage())
except AssertionError: pass
else: raise AssertionError('Unreviewed font glyph accepted')
print('source guards passed')
`],{encoding:'utf8',input:JSON.stringify(authored)});
    expect(result).toContain('source guards passed');
    for(const card of authored.cards) for(const c of card.criteria) expect(c.guidance.join(' ')).not.toMatch(/[\uE000-\uF8FF]/);
    expect(authored.review.reviewedPaperPages).toHaveLength(20);
    expect(authored.review.reviewedSchemePages).toHaveLength(24);
    const row=inventory.papers.find(p=>p.key==='2014|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(65);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
