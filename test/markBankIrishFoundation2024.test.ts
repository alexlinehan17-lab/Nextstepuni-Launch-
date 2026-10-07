import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import authored from '../components/MarkBank/cards/irish/foundation-2024-authored.json';
import { builtDecks, cardsForTopic, loadCards } from '../components/MarkBank/deck';
import { levelsForSubject } from '../components/MarkBank/levels';
import { readChoice, writeChoice } from '../components/MarkBank/store';
import { combinedListeningAssessment, irishMarks, irishScoreId, listeningQuestionGroups } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import { tariffReconciles } from '../types/markBank';

const CARDS = ALL_CARDS.filter(c => c.year === 2024);

describe('reviewed 2024 Irish Foundation tasks', () => {
  it('loads and remembers Foundation without changing other subjects’ available levels', async () => {
    expect(await loadCards('irish', 'foundation')).toHaveLength(921);
    expect(builtDecks()).toContainEqual({ subjectId: 'irish', level: 'foundation', label: 'Irish Foundation' });
    expect(levelsForSubject('irish', 2024)).toEqual(['higher', 'ordinary', 'foundation']);
    expect(levelsForSubject('biology', 2024)).toEqual(['higher', 'ordinary']);
    writeChoice('foundation-review', { subjectId: 'irish', level: 'foundation' });
    expect(readChoice('foundation-review')).toEqual({ subjectId: 'irish', level: 'foundation' });
  });

  it('keeps every reviewed task at its published boundary and on the canonical curriculum', () => {
    expect(CARDS).toHaveLength(78);
    expect(new Set(CARDS.map(c => c.id)).size).toBe(78);
    for (const card of CARDS) {
      expect(tariffReconciles(card), card.id).toBe(true);
      expect(card.specVersion).toBe(resolveCurriculumSpecification('irish', 2024)!.id);
      expect(card.sourceMaterial?.pages.length, card.id).toBeGreaterThan(0);
      expect(card.schemeRegion?.schemeFileid).toBe('LC001BLP000IV.pdf');
    }
    expect(CARDS.filter(c => /-r-1-\d+$/.test(c.id))).toHaveLength(10);
    expect(CARDS.filter(c => /-r-[23][abc]-\d+$/.test(c.id))).toHaveLength(30);
    expect(CARDS.filter(c => /-r-2[abc]-\d+$/.test(c.id)).every(c => c.totalMarks === 5)).toBe(true);
    expect(CARDS.filter(c => /-r-3[abc]-\d+$/.test(c.id)).every(c => c.totalMarks === 6)).toBe(true);
  });

  it('expands every pair and the form’s internal date choice with its full context', () => {
    for (const question of [2, 3]) {
      const routes = CARDS.filter(c => new RegExp(`-r-${question}-[abc]{2}$`).test(c.id));
      expect(routes.map(c => c.id.split('-').at(-1))).toEqual(['ab', 'ac', 'bc']);
      for (const route of routes) {
        expect(route.totalMarks).toBe(question === 2 ? 50 : 60);
        expect(route.sourceMaterial?.pages).toHaveLength(2);
        if (route.rubric.system !== 'irish') throw new Error('Wrong rubric');
        expect(route.rubric.criteria).toHaveLength(10);
        expect(new Set(route.rubric.criteria.map(c => c.id)).size).toBe(10);
      }
    }
    const forms = CARDS.filter(c => /-w-4b-(25|27|3)-/.test(c.id));
    expect(forms).toHaveLength(3);
    expect(forms.map(c => c.questionText.split('An rogha don chárta seo: ')[1]))
      .toEqual(['25 Meitheamh.', '27 Meitheamh.', '3 Iúil.']);
    for (const form of forms) {
      expect(form.totalMarks).toBe(45);
      expect(form.questionText).toContain('Síle Ní Cheallaigh');
      expect(form.questionText).toContain('timpeall 40 focal');
      expect(form.sourceMaterial?.pages).toEqual([15]);
    }
    const pairs = CARDS.filter(c => /-w-[45][ab]-[45][ab]/.test(c.id));
    expect(pairs).toHaveLength(12);
    for (const pair of pairs) {
      expect(pair.totalMarks).toBe(90);
      expect(pair.sourceMaterial?.pages).toHaveLength(2);
      if (pair.rubric.system !== 'irish') throw new Error('Wrong rubric');
      expect(pair.rubric.criteria.filter(c => c.id.endsWith('-gaeilge'))).toHaveLength(2);
    }
    const mixed = CARDS.find(c => c.id === 'irish-2024-fl-w-4a-4b-25-meitheamh')!;
    expect(cardsForTopic('irish-9-0', CARDS)).toContain(mixed);
    expect(cardsForTopic('irish-9-3', CARDS)).toContain(mixed);
  });

  it('never lets a short response deduct marks from another response or its language award', () => {
    const card = CARDS.find(c => c.id === 'irish-2024-fl-w-5a-5b')!;
    if (card.rubric.system !== 'irish') throw new Error('Wrong rubric');
    const scores = Object.fromEntries(card.rubric.criteria.map(c => [irishScoreId(c.id), c.kind === 'award' ? c.maxMarks : 0]));
    expect(irishMarks(card, scores)).toBe(90);
    scores['irish:w-5a-cumarsaid'] = 0;
    scores['irish:w-5a-length'] = 4;
    expect(irishMarks(card, scores)).toBe(56); // 11 language + the other complete 45-mark response.
  });

  it('keeps all listening pictures and choices with the official Foundation recording', () => {
    const listening = CARDS.filter(c => Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined = combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([3, 4, 5]);
    expect(combined.audioMaterial.secFileid).toBe('LC001BLP017IV.mp3');
    const prompts = listening.flatMap(c => listeningQuestionGroups(c.questionText).flatMap(g => g.prompts));
    expect(prompts).toHaveLength(14);
    expect(prompts.find(p => p.label === '7(a)')?.text).toContain('Sa tSeapáin\nSa Fhrainc\nSa Ghréig');
    expect(combined.questionText).not.toContain('Reáchtálaim féin agus mo theaghlach');
  });

  it('joins every card to a correctly tagged Atlas entry with all source and scheme pages', () => {
    const map = JSON.parse(readFileSync('public/paper-answers/2024/LC001BLP000IV.pdf.json', 'utf8'));
    expect(map.paperOnly).toBeUndefined();
    for (const card of authored.cards) {
      const ids = examTopicIdsForQuestion('irish', 'foundation', 2024, 'main', card.atlasQuestionId, 'single', 'iv', 'LC001BLP000IV.pdf');
      expect(ids.length, card.id).toBeGreaterThan(0);
      const canonical = ids.flatMap(curriculumNodeIdsForExamTopic);
      expect(canonical, card.id).toContain(card.topicId);
      const anchor = map.q.find((q: { n: string }) => q.n === card.atlasQuestionId);
      expect(anchor.paperRegion.map((r: { p: number }) => r.p), card.id).toEqual(card.sourceMaterial.pages);
      expect(anchor.region.map((r: { p: number }) => r.p), card.id).toEqual(card.schemePages);
      if ('audioMaterial' in card) expect(anchor.audioMaterial).toEqual(card.audioMaterial);
    }
    expect(examTopicIdsForQuestion('irish', 'foundation', 2024, 'main', 'W-4B', 'single', 'iv', 'LC001BLP000IV.pdf'))
      .toEqual(['irish-foundation-fill-in-a-form']);
    expect(examTopicIdsForQuestion('irish', 'foundation', 2024, 'main', 'R-2C', 'single', 'iv', 'LC001BLP000IV.pdf'))
      .toEqual(['irish-foundation-reading-extract']);
  });
});


describe('2024 Foundation independent source reconciliation', () => {
  const get = (key: string) => authored.cards.find(c => c.atlasQuestionId === key)!;
  it('uses the exact 2024 answers and published part tariffs', () => {
    expect(authored.cards.filter(c => c.atlasQuestionId.startsWith('A-')).map(c => [c.totalMarks,c.criteria[0].guidance[0]]))
      .toEqual([
        [7,'Feirm = an tríú pictiúr'],[7,'Deirdre'],[7,'Óstán = an dara pictiúr'],[7,'I siopaí éadaí'],
        [8,'Siopa ceoil = an ceathrú pictiúr'],[8,'An bosca ag an mbun ar dheis (tic nó saighead sa bhosca)'],
        [8,'Cluiche sacair = an dara pictiúr'],[8,'Na daltaí ó bhliain a sé'],
        [10,'Aindí agus Órla'],[10,'Dáiríre'],[10,'Sa Fhrainc'],[10,'€400 an duine'],
        [10,'Ceithre phointe'],[10,'Club óige áitiúil'],
      ]);
    expect(authored.cards.filter(c => /^R-1-/.test(c.atlasQuestionId)).map(c => c.criteria[0].guidance[0]).join('')).toBe('EAJICBDHFG');
    const expected = [
      ['29 Bealtaine','Na Buachaillí Dána','Dé hAoine','Rac-cheol','A trí a chlog'],
      ['I ndeisceart Phort Láirge','Deich gciliméadar','Nioclás Tóibín','Sa mheánscoil áitiúil','Rian Glas na nDéise'],
      ['Ar scoil','A naoi a chlog','A dhaid','Rang Béarla','Ina phóca'],
      ['Dhá bhliain déag d’aois','2023','Céim sa Ghaeilge agus sa Chorpoideachas','In Minnesota','Céim i Síceolaíocht an Spóirt'],
      ['Ráth Chairn','2018','Ciarraí','An deireadh seachtaine sin','Díomá'],
      ['Go dtí an ghealach','Culaith spásaire','Picnic / Bia','Go rachaidh sé ar strae','Ina leaba'],
    ];
    for (const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) {
      for(let i=1;i<=5;i++) {
        const card=get(`R-${slot}-${i}`);
        expect(card.criteria[0].guidance[0],card.id).toBe(expected[j][i-1]);
        expect(card.criteria[0].permittedMarks).toEqual([0,j<3?5:6]);
        expect(card.sourceMaterial.pages).toEqual([j+7]);
      }
    }
  });

  it('keeps whole writing responses and the 2024 deductions with their shared language award', () => {
    const notice=get('W-4A');
    expect(notice.criteria.map(c=>c.maxMarks)).toEqual([1,10,13,5,5,11]);
    expect(notice.criteria.find(c=>c.id==='pictiur3')!.guidance.join(' ')).toContain('Patrick Kielty');
    expect(notice.criteria.find(c=>c.id==='pictiur4')!.guidance.join(' ')).toContain('Giomnáisiam');
    const form=get('W-4B-25-meitheamh');
    expect(form.criteria.map(c=>[c.id,c.maxMarks])).toEqual([['fields',19],['paragraph',15],['length',3],['gaeilge',11]]);
    expect(form.criteria.find(c=>c.id==='length')!.guidance.join(' ')).toContain('35–40 focal: 0; 25–34 focal: −1; 10–24 focal: −2; <10 focal: −3');
    expect(form.criteria.find(c=>c.id==='length')).toMatchObject({kind:'deduction',deductFrom:'paragraph'});
    expect(form.questionText).toContain('post samhraidh mar fhreastalaí sa bhialann seo');
    for(const slot of ['5A','5B']) {
      const story=get('W-'+slot);
      expect(story.criteria.filter(c=>c.kind==='award').map(c=>c.maxMarks)).toEqual([34,11]);
      expect(story.criteria.find(c=>c.id==='cumarsaid')!.guidance.join(' ')).toContain('34, 30, 26, 22, 18 nó 14');
      expect(story.criteria.find(c=>c.id==='length')).toMatchObject({kind:'deduction',deductFrom:'cumarsaid',maxMarks:4});
      expect(story.questionText).toContain('timpeall 90 focal');
    }
    expect(get('W-5A').questionText).toContain('Saoire go Páras na Fraince');
    expect(get('W-5B').questionText).toContain('siopadóireacht le do chara tar éis na scoile');
  });

  it('fails unknown directives even on a reviewed page and rejects stale decisions', () => {
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2024 import selection_decisions
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for decision in review['selectionDecisions']: pages[decision['page']-1].text+=decision['raw']+'\n'
assert len(selection_decisions(pages))==24
original=pages[14].text
for edited in [original+'\nRoghnaigh ceann amháin den dá cheann seo.\n',original.replace('Ainmnigh','Liostaigh')]:
 pages[14].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(authored)});
    expect(result).toContain('source guard passed');
  });

  it('retains the original section crop fields and uses additive reviewed regions', () => {
    const map=JSON.parse(readFileSync('public/paper-answers/2024/LC001BLP000IV.pdf.json','utf8'));
    const listening=map.q.find((q: {n:string})=>q.n==='1');
    expect(listening.region).toEqual([{p:3,r:[0,0.1265,1,1]},{p:4,r:[0,0,1,0.0682]}]);
    expect(listening.schemeRegion).toEqual([{p:3,r:[0,0,1,1]}]);
    expect(listening.audioMaterial.secFileid).toBe('LC001BLP017IV.mp3');
    const writing=map.q.find((q: {n:string})=>q.n==='3');
    expect(writing.region.map((r:{p:number})=>r.p)).toEqual([7,8,9,10,11,12]);
    expect(writing.schemeRegion.map((r:{p:number})=>r.p)).toEqual([7,8,9,10,11,12,13,14,15]);
  });

  it('records the full visual sweep without claiming the remaining archive complete', () => {
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(authored.review.reviewedSchemePages).toEqual(Array.from({length:24},(_,i)=>i+1));
    expect(authored.review.selectionDecisions).toHaveLength(24);
    expect(authored.review.atomicPracticeCardIds).toHaveLength(60);
    expect(authored.review.pairedRouteCardIds).toHaveLength(18);
    expect(authored.review.examStructure.total).toBe(360);
    expect(authored.review.openIssues).toEqual([]);
    const row=inventory.papers.find(p=>p.key==='2024|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(CARDS.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.indexedCards).toBe(1372);
    expect(inventory.summary.papersPendingFullReview).toBe(77);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
