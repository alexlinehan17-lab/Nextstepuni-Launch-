import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync } from 'node:fs';
import { CARDS as HIGHER_CARDS } from '../components/MarkBank/cards/economics/higher';
import { CARDS as ORDINARY_CARDS } from '../components/MarkBank/cards/economics/ordinary';
import { isPointCard, type SecDiagramCard, type SecPointCard, type SecQuestionCard } from '../types/markBank';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import { reviewedArchiveEntries } from '../components/PaperTrail/indexLookup';
import { curriculumNodeIdsForExamTopic, examTopicIdsForQuestion } from '../data/examTopics/registry';
import reviews from '../data/examTopics/economics-sec-topic-reviews.json';
import inventory from '../scripts/markbank/authoring/economics-source-inventory.json';
import higher2021Review from '../scripts/markbank/authoring/reviews/economics-2021-hl-ev.json';
import ordinary2021Review from '../scripts/markbank/authoring/reviews/economics-2021-ol-ev.json';
import paperReview from '../scripts/markbank/authoring/reviews/economics-2022-hl-ev.json';
import ordinaryReview from '../scripts/markbank/authoring/reviews/economics-2022-ol-ev.json';
import irishReview from '../scripts/markbank/authoring/reviews/economics-2022-ol-iv.json';
import higherIrishReview from '../scripts/markbank/authoring/reviews/economics-2022-hl-iv.json';
import higher2023Review from '../scripts/markbank/authoring/reviews/economics-2023-hl-ev.json';
import higher2023IrishReview from '../scripts/markbank/authoring/reviews/economics-2023-hl-iv.json';
import ordinary2023Review from '../scripts/markbank/authoring/reviews/economics-2023-ol-ev.json';
import ordinary2023IrishReview from '../scripts/markbank/authoring/reviews/economics-2023-ol-iv.json';
import higher2024Review from '../scripts/markbank/authoring/reviews/economics-2024-hl-ev.json';
import higher2024IrishReview from '../scripts/markbank/authoring/reviews/economics-2024-hl-iv.json';
import ordinary2024Review from '../scripts/markbank/authoring/reviews/economics-2024-ol-ev.json';
import ordinary2024IrishReview from '../scripts/markbank/authoring/reviews/economics-2024-ol-iv.json';
import higher2025Review from '../scripts/markbank/authoring/reviews/economics-2025-hl-ev.json';
import ordinary2025Review from '../scripts/markbank/authoring/reviews/economics-2025-ol-ev.json';
import higher2026Review from '../scripts/markbank/authoring/reviews/economics-2026-hl-ev.json';
import ordinary2026Review from '../scripts/markbank/authoring/reviews/economics-2026-ol-ev.json';
import boundaryCorrections from '../scripts/markbank/authoring/economics-boundary-corrections.json';
import exclusions from '../scripts/markbank/authoring/exclusions/economics.json';

/* The SEC papers and marking schemes are local-only: paper-trail-corpus is
 * gitignored, so CI has none of them. econ_review.py validates every reviewed
 * edition against the PDFs themselves (hashes, printed directives, pages)
 * before a mutation test can run, so those checks run wherever the corpus and
 * PyMuPDF are present and are skipped on CI; everything checkable from
 * committed files keeps running everywhere. The Music tests use the same gate. */
const CORPUS = 'paper-trail-corpus';
const hasEconomicsSources = [2021, 2022, 2023, 2024, 2025, 2026].every(year => (
  ['exampapers', 'markingschemes'].every(folder => {
    const dir = `${CORPUS}/${folder}/${year}`;
    return existsSync(dir) && readdirSync(dir).some(name => name.startsWith('LC034'));
  })
));
const hasPyMuPDF = (() => {
  try {
    execFileSync('python3', ['-c', 'import fitz'], { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
})();
const canReadSecSources = hasEconomicsSources && hasPyMuPDF;

// Every Economics card is a marking-point card (no rubric cards); narrowing
// here keeps the assertions below typed against rows and figures, and the
// length check proves the narrowing drops nothing.
// Question and diagram cards both appear; the assertions read either kind's
// optional fields.
type EconomicsCard = SecPointCard & {
  questionFigure?: SecQuestionCard['questionFigure'];
  labelKey?: SecDiagramCard['labelKey'];
};
const CARDS: EconomicsCard[] = HIGHER_CARDS.filter(isPointCard);
const ORDINARY: EconomicsCard[] = ORDINARY_CARDS.filter(isPointCard);
if (CARDS.length !== HIGHER_CARDS.length || ORDINARY.length !== ORDINARY_CARDS.length) {
  throw new Error('Economics ships a card that is not a marking-point card');
}

const sectionA = CARDS.filter(card => card.year === 2022 && card.section === 'A');

describe('Economics SEC source review (completion remains pending)', () => {
  it('carries 2024 Ordinary Irish labels, field order and the missing tariff explanation', () => {
    const card = (s: string) => ORDINARY.find(c => c.id === `econ-2024-ol-${s}`)!;
    for (const [s,note] of [
      ['sa-q9','OTI = Olltáirge Intíre'], ['sa-q10','É1/É2 are demand curves'],
      ['q11-b-i','Costas Imeallach'], ['q11-b-ii','output label C1'],
      ['q15-a','Fiontraíocht = Enterprise'], ['q15-b-ii','C/Pc/Cc'],
      ['q16-b-ii-adv','second 9-mark cell is absent'], ['q16-c-i-neg','income/social inequality'],
    ]) expect(card(s).rows[0].contextNote,s).toContain(note);
    expect(ordinary2024IrishReview.questions.find(q => q.n === '16')?.allocationEvidence?.schemePages).toEqual([39,40]);
    expect(card('q15-b-i').stem).toContain('12 months to October 2022');
    expect(card('q14-a-i').rows[0].contextNote).toContain('Deduct 1 for omission of € and 1 for omission of bn');
  });

  it('matches the independent 61-route 2024 Ordinary census including marks, context and Atlas topics', () => {
    const cards = ORDINARY.filter(c => c.year === 2024);
    const tasks = ordinary2024Review.questions.flatMap(q => q.tasks);
    expect(tasks).toHaveLength(61);
    expect(cards.map(c => c.id).sort()).toEqual(tasks.map(t => t.cardId).sort());
    expect(cards.filter(c => c.section === 'A')).toHaveLength(13);
    for (const q of ordinary2024Review.questions) {
      const topics = examTopicIdsForQuestion('economics','ordinary',2024,'main',q.n,'single','ev')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const t of q.tasks) {
        const c = cards.find(c => c.id === t.cardId)!;
        expect(c.totalMarks,c.id).toBe(t.marks);
        expect(c.topicId,c.id).toBe(t.topicId);
        expect(c.sourceMaterial?.pages,c.id).toEqual(q.paperPages);
        expect(topics,c.id).toContain(t.topicId);
      }
      if (Number(q.n) > 10) {
        expect(q.tasks.filter(t => !['c/ii/no','b/iii/disagree','c/i/negative'].includes(t.key))
          .reduce((sum,t) => sum+t.marks,0), `2024 OL Q${q.n}`).toBe(75);
      }
    }
  });

  it('preserves 2024 Ordinary required responses and original progress without fixed-side shared tariffs', () => {
    const card = (s: string) => ORDINARY.find(c => c.id === `econ-2024-ol-${s}`)!;
    for (const [old,kept,marks] of [['sa-q1-ii','sa-q1-i',12],['sa-q8-ii','sa-q8-i',12],['q16-b-ii-dis','q16-b-ii-adv',18]] as const) {
      expect(CARD_ID_ALIASES[`econ-2024-ol-${old}`]).toBe(card(kept).id);
      expect(card(old)).toBeUndefined();
      expect(card(kept).totalMarks).toBe(marks);
      expect(card(kept).rows).toHaveLength(2);
    }
    for (const s of ['sa-q1-i','sa-q2-a','sa-q8-i','sa-q9','q11-a-i','q13-b-i','q15-a']) {
      expect(card(s).tariffModel.kind).toBe('questionTotal');
      expect(card(s).rows.every(r => r.marks === null)).toBe(true);
    }
    expect(card('sa-q9').rows.map(r => r.verbatim)).toEqual(['Gross','Product','Gross','National']);
    expect(card('q16-b-ii-adv').rows.map(r => r.marks)).toEqual([9,9]);
    expect(card('q11-b-iii').questionText).toContain('Give one other example of an oligopoly market');
    expect(card('q11-b-iii').rows).toHaveLength(2);
  });

  it('retains every 2024 Ordinary finite stance and both independently priced spending calculations', () => {
    for (const [prefix,choices,marks] of [
      ['q13-c-ii',['yes','no'],10],['q14-b-iii',['agree','disagree'],7],['q16-c-i',['pos','neg'],10],
    ] as const) {
      const cards = ORDINARY.filter(c => c.id.startsWith(`econ-2024-ol-${prefix}-`));
      expect(cards.map(c => c.id).sort()).toEqual(choices.map(x => `econ-2024-ol-${prefix}-${x}`).sort());
      expect(cards.every(c => c.totalMarks === marks)).toBe(true);
      expect(new Set(cards.map(c => c.questionText)).size).toBe(2);
    }
    const total = ORDINARY.find(c => c.id === 'econ-2024-ol-q14-a-i')!;
    const share = ORDINARY.find(c => c.id === 'econ-2024-ol-q14-a-i-education')!;
    expect(total.totalMarks).toBe(12);
    expect(share.totalMarks).toBe(8);
    expect(share.rows[0].contextNote).toContain('€44.22bn total');
    expect(share.rows[0].contextNote).toContain('9.63 ÷ 44.22 × 100 = 21.78%');
  });

  it('restores missing 2024 Ordinary examples and explains official-source inaccuracies', () => {
    const card = (s: string) => ORDINARY.find(c => c.id === `econ-2024-ol-${s}`)!;
    for (const [s,count] of [['sa-q3-b',5],['sa-q6',5],['q12-c-iii',6],['q13-c-ii-no',5],['q13-c-iii',6],['q14-b-iii-agree',4],['q14-b-iii-disagree',6],['q16-c-i-neg',5]] as const) {
      expect(card(s).rows[0].group?.options, s).toHaveLength(count);
    }
    for (const [s,note] of [
      ['q12-c-i','0.1 percentage point'],['q13-a-i','cross at output 2'],
      ['q13-c-iii','symmetric 2%'],['q15-c-i','(−40÷40) × (240÷140)'],
      ['q15-c-ii','price RISES'],['q16-a-i','cannot itself increase the WORLD total'],
      ['q16-a-ii','AGE-BASED dependency ratio'],['q16-b-ii-adv','€750m'],
    ]) expect(card(s).rows.map(r => r.contextNote).join(' '),s).toContain(note);
    expect(card('sa-q1-i').rows[1].verbatim).toContain('Reduce water usage');
    expect(card('sa-q1-i').rows[1].verbatim).toContain('When using these resources');
  });

  it('lifts 2024 Ordinary wording from the paper and hides its solutions until reveal', () => {
    const card = (s: string) => ORDINARY.find(c => c.id === `econ-2024-ol-${s}`)!;
    // A solution in the figure slot takes the whole printed question as the question crop.
    for (const [s, crop] of [['q11-b-ii', 'p11-q11bii'], ['q13-a-i', 'p16-q13ai'], ['q15-a', 'p22-q15a'],
      ['q15-b-i', 'p23-q15b'], ['q15-b-ii', 'p23-q15b'], ['q15-c-i', 'p24-q15ci']] as const) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).questionFigure?.src, s).toContain(`economics-2024-OL-paper-${crop}-question.png`);
    }
    for (const c of ORDINARY.filter(item => item.year === 2024 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
    }
    // The asks the earlier extractors paraphrased now read as the paper prints them.
    expect(card('sa-q8-i').questionText).toContain('From the data given, state in the boxes below');
    expect(card('q16-a-iii').stem).toBe('Ireland’s population is ageing faster than anywhere else in Europe.');
    expect(card('q16-c-ii').questionText).toContain('Revolut becoming a mortgage lender may have on people applying');
    expect(card('seca-q5-ticks').questionText).toContain('Irish tourists staying in hotels in France.');
    expect(card('q15-a').rows.map(r => r.verbatim).slice(0, 3)).toEqual(['Capital', 'Labour', 'Enterprise']);
    expect(card('q11-b-ii').rows.map(r => r.verbatim)).toEqual(['Q1', 'P1']);
    // Figure alts describe printed answer blanks, so the check reads the card's own text.
    const text = ORDINARY.filter(c => c.year === 2024)
      .map(c => JSON.stringify([c.stem, c.questionText, c.rows])).join('\n');
    for (const junk of ['Possible responses', 'P a g e', '⟨', '____', 'the exam’s scenario']) {
      expect(text, junk).not.toContain(junk);
    }
  });

  it('matches all 83 independently counted 2024 Higher routes, tariffs, sources and Atlas topics', () => {
    const cards = CARDS.filter(card => card.year === 2024);
    const tasks = higher2024Review.questions.flatMap(question => question.tasks);
    expect(tasks).toHaveLength(83);
    expect(cards.map(c => c.id).sort()).toEqual(tasks.map(t => t.cardId).sort());
    expect(cards.filter(c => c.section === 'A')).toHaveLength(24);
    for (const question of higher2024Review.questions) {
      const nodes = examTopicIdsForQuestion('economics', 'higher', 2024, 'main', question.n,
        'single', 'ev').flatMap(curriculumNodeIdsForExamTopic);
      for (const task of question.tasks) {
        const card = cards.find(c => c.id === task.cardId)!;
        expect(card.totalMarks, card.id).toBe(task.marks);
        expect(card.topicId, card.id).toBe(task.topicId);
        expect(card.sourceMaterial?.pages, card.id).toEqual(question.paperPages);
        expect(nodes, card.id).toContain(task.topicId);
      }
      if (Number(question.n) > 10) {
        const oneRoute = question.tasks.filter(t => !['a/iii/government', 'a/ii/disagree'].includes(t.key));
        expect(oneRoute.reduce((sum, t) => sum + t.marks, 0), `2024 Q${question.n}`).toBe(75);
      }
    }
  });

  it('preserves 2024 required headings and saved progress, with the published combined tariffs', () => {
    for (const [kept, alias, marks] of [
      ['sa-q6-b-down','sa-q6-b-up',4], ['sa-q9-a-cost','sa-q9-a-benefit',6],
      ['q13-b-iii-pos','q13-b-iii-neg',10], ['q13-c-iii-pos','q13-c-iii-neg',6],
      ['q14-c-i-spending','q14-c-i-debt',8], ['q15-c-ii-economic','q15-c-ii-social',10],
      ['q16-c-ii-cost','q16-c-ii-benefit',10], ['q16-c-iii-advantage','q16-c-iii-disadvantage',12],
    ] as const) {
      const card = CARDS.find(c => c.id === `econ-2024-hl-${kept}`)!;
      expect(card.totalMarks).toBe(marks);
      expect(card.rows).toHaveLength(2);
      expect(CARD_ID_ALIASES[`econ-2024-hl-${alias}`]).toBe(card.id);
      expect(CARDS.some(c => c.id === `econ-2024-hl-${alias}`)).toBe(false);
    }
    for (const suffix of ['q13-b-iii-pos','q15-c-ii-economic']) {
      const c = CARDS.find(c => c.id === `econ-2024-hl-${suffix}`)!;
      expect(c.tariffModel.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null)).toBe(true);
    }
  });

  it('retains every closed 2024 stance and every separately marked drawing/calculation response', () => {
    const byId = new Map(CARDS.map(c => [c.id, c]));
    for (const [prefix, choices, tariff] of [
      ['q12-a-iii',['tax','gov'],4], ['q14-a-ii',['agree','disagree'],6],
    ] as const) {
      const routes = CARDS.filter(c => c.id.startsWith(`econ-2024-hl-${prefix}-`));
      expect(routes.map(c => c.id).sort()).toEqual(choices.map(s => `econ-2024-hl-${prefix}-${s}`).sort());
      expect(new Set(routes.map(c => c.questionText)).size).toBe(2);
      expect(routes.every(c => c.totalMarks === tariff)).toBe(true);
    }
    for (const [suffix, marks] of [
      ['sa-q6-a-diagram',5], ['q11-c-i-diagram',5], ['q11-c-ii-diagram',5],
      ['q11-c-iii-diagram',5], ['q14-b-i',12],
    ] as const) {
      const c = byId.get(`econ-2024-hl-${suffix}`)!;
      expect(c.totalMarks).toBe(marks);
      expect(c.figure?.solution).toBe(true);
      expect(c.figure?.src).toContain('-scheme-');
    }
    for (const [suffix, marks] of [['q11-b-i',12],['q11-b-i-meaning',4],
      ['q14-b-i-explanation',9],['q16-b-ii',9],['q16-b-ii-meaning',4]] as const) {
      expect(byId.get(`econ-2024-hl-${suffix}`)?.totalMarks).toBe(marks);
    }
  });

  it('restores omitted 2024 criteria and separates source mistakes from usable answer guidance', () => {
    const card = (suffix: string) => CARDS.find(c => c.id === `econ-2024-hl-${suffix}`)!;
    expect(card('sa-q8-a').rows.map(r => r.marks)).toEqual([4,2]);
    expect(card('sa-q8-a').rows[0].verbatim).toContain('not due to a difference');
    expect(card('sa-q4-b').rows[0].group?.options).toHaveLength(8);
    expect(card('sa-q7-a').rows[0].group?.options).toHaveLength(4);
    expect(card('sa-q7-b').rows[0].group?.options).toHaveLength(5);
    expect(card('q12-a-iii-tax').rows[0].group?.options).toHaveLength(6);
    expect(card('q14-c-iii').rows[0].group?.options).toHaveLength(5);
    expect(card('q15-c-ii-economic').rows[0].verbatim).toContain('Increase VAT');
    expect(card('q15-c-ii-economic').rows[1].verbatim).toContain('No fry zones');
    expect(card('q15-c-ii-economic').rows[1].verbatim).not.toContain('Increase VAT');
    expect(card('q16-c-ii-cost').rows[0].group?.options.join(' ')).toContain('Loss of natural environment');
    expect(card('q16-c-ii-cost').rows[1].group?.options.join(' ')).toContain('Reduced health care costs');
    expect(card('q16-c-i').rows.map(r => r.marks)).toEqual([4,2]);
    expect(card('q13-c-i').rows.map(r => r.marks)).toEqual([4,4]);
    expect(card('q16-a-i').totalMarks).toBe(10);
    expect(card('q16-a-ii').totalMarks).toBe(10);
    expect(card('q12-b-i').rows[0].contextNote).toContain('percentage points');
    expect(card('q12-b-i').rows[0].contextNote).toContain('Prices are still rising');
    expect(card('q11-b-i').rows[0].contextNote).toContain('1.086956');
    expect(card('q16-b-ii').rows[0].contextNote).toContain('0.81818');
    expect(card('q16-b-iii').rows[0].contextNote).toContain('Expected 2024 sales');
  });

  it('lifts 2024 Higher wording from the paper and hides its solutions until reveal', () => {
    const card = (s: string) => CARDS.find(c => c.id === `econ-2024-hl-${s}`)!;
    // A solution in the figure slot takes the whole printed question as the question crop.
    for (const [s, crop] of [['sa-q3-a', 'p05-q3a'], ['seca-q4-a-ticks', 'p06-q4a'],
      ['sa-q10-a-ii', 'p12-q10a'], ['q12-b-ii', 'p18-q12bii']] as const) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).questionFigure?.src, s).toContain(`economics-2024-HL-paper-${crop}-question.png`);
    }
    for (const c of CARDS.filter(item => item.year === 2024 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
    }
    for (const s of ['seca-q1-a', 'q11-a-iii', 'q13-a-iii', 'q15-a-ii', 'q16-a-i', 'q16-b-ii']) {
      expect(card(s).figure?.src, s).toContain('-paper-');
      expect(card(s).figure?.solution, s).toBeUndefined();
    }
    // The written asks the earlier extractors paraphrased now read as the paper prints them.
    expect(card('sa-q9-a-cost').questionText).toBe('Outline one opportunity cost of this pledge by Coillte and outline one social benefit of this proposal.');
    expect(card('q12-a-iii-tax').stem).toContain('has not been ruled out, according to Taoiseach Leo Varadkar');
    expect(card('q14-c-i-spending').rows.map(r => r.verbatim)).toEqual(['Level of consumer spending', 'Cost of servicing the national debt']);
    expect(card('q15-b-ii').rows.map(r => r.marks)).toEqual([5, 5]);
    expect(card('q15-a-ii').rows[0].group?.options).toHaveLength(4);
    expect(card('sa-q2-b').rows[0].group?.options).toHaveLength(4);
    expect(card('sa-q6-b-down').rows[0].group?.options).toHaveLength(2);
    for (const part of ['i', 'ii', 'iii']) {
      expect(card(`q11-c-${part}`).rows[0].group?.options, part).toHaveLength(4);
      expect(card(`q11-c-${part}-diagram`).rows[0].marks, part).toBe(5);
    }
    const text = CARDS.filter(c => c.year === 2024).map(c => JSON.stringify(c)).join('\n');
    for (const junk of ['Possible Responses', 'P a g e', '⟨', '____']) {
      expect(text, junk).not.toContain(junk);
    }
  });

  it('inventories every indexed paper, including earlier years and Irish editions', () => {
    // The reviewed window: June sittings 2010-2026 (pre-2010 and deferred
    // papers are archive-only).
    const indexed = reviewedArchiveEntries('economics').flatMap(entry => entry.papers.map(paper =>
      [entry.year, entry.level, entry.lang, paper.doc.f].join('|'))).sort();
    const inventoried = inventory.papers.map(paper =>
      [paper.year, paper.level, paper.lang, paper.fileid].join('|')).sort();
    expect(inventoried).toEqual(indexed);
    expect(inventory.complete).toBe(false);
    expect(inventory.summary.paperVariantsWithoutMarkBankCards).toBe(48);
    expect(inventory.summary.paperVariantsWithoutPrimaryMarkBankCards).toBe(54);
    expect(inventory.summary.paperVariantsWithValidatedVisualReview).toBe(18);
    expect(inventory.papers.every(paper => paper.paper.sha256.length === 64
      && paper.scheme.sha256.length === 64 && paper.paper.pages > 0 && paper.scheme.pages > 0)).toBe(true);
  });

  it('retains the reviewed question context for every existing 2022 HL Section A card', () => {
    expect(sectionA).toHaveLength(24);
    for (const card of sectionA) {
      const n = card.questionRef.match(/Q(\d+)/)![1];
      const review = reviews.questions.find(question => question.n === n)!;
      expect(card.paperFileid, card.id).toBe('LC034ALP000EV');
      expect(card.sourceMaterial?.pages, card.id).toEqual(review.pages);
      expect(card.sourceMaterial?.kind, card.id).toBe('source-illustration');
    }
  });

  it('places every reviewed existing card in a corresponding Atlas topic', () => {
    for (const card of sectionA) {
      const n = card.questionRef.match(/Q(\d+)/)![1];
      const topics = examTopicIdsForQuestion('economics', 'higher', 2022, 'main', n, 'single', 'ev');
      const nodes = topics.flatMap(curriculumNodeIdsForExamTopic);
      expect(nodes, `${card.id}: missing ${card.topicId} in Atlas`).toContain(card.topicId);
    }
  });

  it('corrects the demonstrably wrong topics and paper wording without changing IDs', () => {
    const byId = new Map(CARDS.map(card => [card.id, card]));
    expect(byId.get('econ-2022-hl-seca-q7-a-ii')?.topicId).toBe('economics-3-3');
    expect(byId.get('econ-2022-hl-seca-q10-a')?.topicId).toBe('economics-0-1');
    expect(byId.get('econ-2022-hl-seca-q10-a')?.questionText).toContain('Explain your answer.');
    expect(byId.get('econ-2022-hl-sa-q4-b')?.questionText)
      .toBe('In the box below justify each of your choices in part (a) above.');
    expect(byId.get('econ-2022-hl-sa-q7-a-i')?.questionText).toContain('2000 to 2020');
    expect(examTopicIdsForQuestion('economics', 'higher', 2022, 'main', '9', 'single', 'ev'))
      .toEqual(['economics-higher-33-market-failure']);
  });

  it('restores the FDI alternative at its published total without inventing a per-reason split', () => {
    const restored = sectionA.find(card => card.id === 'econ-2022-hl-sa-q4-c')!;
    expect(restored.totalMarks).toBe(7);
    expect(restored.questionText).toContain('Outline two reasons');
    expect(restored.topicId).toBe('economics-4-1');
    expect(restored.kind).toBe('question');
    if (restored.kind !== 'question') throw new Error('Unexpected card kind');
    expect(restored.tariffModel.kind).toBe('questionTotal');
    expect(restored.rows).toHaveLength(1);
    expect(restored.rows[0].marks).toBeNull();
    expect(restored.rows[0].verbatim).toContain('Increased employment opportunities');
    expect(restored.rows[0].verbatim).toContain('Increased tax revenue');
    expect(restored.rows[0].verbatim).toContain('Increased economic growth');
    expect(restored.rows[0].contextNote).toContain('not three compulsory points');
  });

  it('matches the independent visual census, including every reviewed tariff and source page', () => {
    const cards = CARDS.filter(card => card.year === 2022);
    const tasks = paperReview.questions.flatMap(question => question.tasks);
    expect(tasks).toHaveLength(75);
    expect(cards.map(card => card.id).sort()).toEqual(tasks.map(task => task.cardId).sort());
    for (const question of paperReview.questions) {
      for (const task of question.tasks) {
        const card = cards.find(card => card.id === task.cardId)!;
        expect(card.totalMarks, task.cardId).toBe(task.marks);
        expect(card.sourceMaterial?.pages, task.cardId).toEqual(question.paperPages);
        expect(question.canonicalNodeIds, task.cardId).toContain(card.topicId);
      }
      if (Number(question.n) > 10) {
        const compulsory = question.tasks.filter(task => task.key !== 'c/ii/no');
        expect(compulsory.reduce((sum, task) => sum + task.marks, 0), `Q${question.n}`).toBe(75);
      }
    }
  });

  it('matches all 74 independently counted 2023 Higher routes, sources, tariffs and Atlas nodes', () => {
    const cards = CARDS.filter(card => card.year === 2023);
    const tasks = higher2023Review.questions.flatMap(question => question.tasks);
    expect(tasks).toHaveLength(74);
    expect(cards.map(card => card.id).sort()).toEqual(tasks.map(task => task.cardId).sort());
    for (const question of higher2023Review.questions) {
      const nodes = examTopicIdsForQuestion('economics', 'higher', 2023, 'main', question.n, 'single', 'ev')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const task of question.tasks) {
        const card = cards.find(item => item.id === task.cardId)!;
        expect(card.totalMarks, task.cardId).toBe(task.marks);
        expect(card.topicId, task.cardId).toBe(task.topicId);
        expect(card.sourceMaterial?.pages, task.cardId).toEqual(question.paperPages);
        expect(nodes, task.cardId).toContain(task.topicId);
      }
      if (Number(question.n) > 10) {
        const compulsory = question.tasks.filter(task => task.key !== 'b/iii/no');
        expect(compulsory.reduce((sum, task) => sum + task.marks, 0), `2023 Q${question.n}`).toBe(75);
      }
    }
  });

  it('restores 2023 required answer components and preserves consolidated progress', () => {
    const card = (suffix: string) => {
      const found = CARDS.find(item => item.id === `econ-2023-hl-${suffix}`)!;
      if (found.kind !== 'question') throw new Error('Expected question card');
      return found;
    };
    for (const [kept, alias, marks] of [
      ['sa-q2-c-adv', 'sa-q2-c-dis', 6],
      ['q11-a-iii-neg', 'q11-a-iii-pos', 10],
      ['q12-b-iii-adv', 'q12-b-iii-dis', 10],
      ['q16-c-i-for', 'q16-c-i-against', 12],
    ] as const) {
      expect(card(kept).totalMarks).toBe(marks);
      expect(card(kept).rows).toHaveLength(2);
      expect(CARD_ID_ALIASES[`econ-2023-hl-${alias}`]).toBe(`econ-2023-hl-${kept}`);
    }
    for (const suffix of ['sa-q1-a', 'sa-q7-a']) {
      expect(card(suffix).rows.map(row => row.marks)).toEqual([3, 3]);
      expect(card(suffix).figure?.solution).toBe(true);
    }
    expect(card('q12-a-iii').figure?.solution).toBe(true);
    expect(card('sa-q2-a').rows.map(row => row.marks)).toEqual([1, 5]);
    expect(card('q13-a-ii').rows.map(row => row.marks)).toEqual([2, 4, 2, 4]);
    expect(card('q14-b-iii').topicId).toBe('economics-0-1');
    expect(card('q14-b-iii').questionText).toContain('Use a cost');
    expect(card('q14-b-iii').rows.map(row => row.marks)).toEqual([4, 4, 4]);
    expect(card('q14-a-iii').rows[0].group?.options).toHaveLength(5);
    expect(card('q14-a-iii').rows[0].group?.options[0]).toContain('Structural unemployment');
    expect(card('q14-a-ii').rows[0].verbatim).toContain('Award 4 marks to all candidates');
    expect(card('q14-a-ii').questionText).toContain('Quarterly National Household Survey');
    expect(card('q15-a-i').rows).toHaveLength(2);
    expect(card('q15-a-i').rows[0].contextNote).toContain('euro cents per kWh');
    expect(card('q15-a-i').tariffModel.kind).toBe('questionTotal');
    // 1st @ 8, 2 @ 5 across the For/Against table: three arguments from one menu.
    expect(card('q12-c').rows[0].group?.perOptionSteps).toEqual([8, 5, 5]);
    expect(card('q12-c').rows[0].group?.options).toHaveLength(7);
    expect(card('sa-q5-a').tariffModel.kind).toBe('questionTotal');
    expect(card('sa-q5-a').rows.every(row => row.marks === null)).toBe(true);
    // A single 6 cell over an open list of examples is one priced point.
    for (const suffix of ['sa-q4-c', 'sa-q5-b', 'sa-q6-b', 'sa-q7-b', 'sa-q9-b']) {
      expect(card(suffix).rows.map(row => row.marks), suffix).toEqual([6]);
    }
  });

  it('matches all 61 independently reviewed 2023 Ordinary tasks and Atlas associations', () => {
    const cards = ORDINARY.filter(card => card.year === 2023);
    const tasks = ordinary2023Review.questions.flatMap(question => question.tasks);
    expect(tasks).toHaveLength(61);
    expect(cards.map(c => c.id).sort()).toEqual(tasks.map(t => t.cardId).sort());
    for (const question of ordinary2023Review.questions) {
      const nodes = examTopicIdsForQuestion('economics', 'ordinary', 2023, 'main', question.n,
        'single', 'ev').flatMap(curriculumNodeIdsForExamTopic);
      for (const task of question.tasks) {
        const card = cards.find(c => c.id === task.cardId)!;
        expect(card.totalMarks, card.id).toBe(task.marks);
        expect(card.topicId, card.id).toBe(task.topicId);
        expect(nodes, card.id).toContain(task.topicId);
        expect(card.sourceMaterial?.pages, card.id).toEqual(question.paperPages);
        expect(card.paperFileid, card.id).toBe('LC034GLP000EV');
      }
      if (Number(question.n) > 10) {
        const oneRoute = question.tasks;
        expect(oneRoute.reduce((sum, t) => sum + t.marks, 0), `2023 OL Q${question.n}`).toBe(75);
      }
    }
  });

  it('carries any two of the three economic-good terms as one claim-two card', () => {
    const card = ORDINARY.find(c => c.id === 'econ-2023-ol-q16-a-i')!;
    if (card.kind !== 'question') throw new Error('Expected question');
    expect(ORDINARY.filter(c => c.year === 2023 && c.questionRef.startsWith('2023 OL Q16(b)(i)')).map(c => c.id))
      .toEqual(['econ-2023-ol-q16-a-i']);
    expect(card.totalMarks).toBe(14);
    expect(card.tariffModel).toMatchObject({ kind: 'bestNofParts', answer: 2, ofParts: 3, perPart: 7 });
    expect(card.rows[0].group?.claimMax).toBe(2);
    expect(card.rows[0].group?.options.map(o => o.split(':')[0])).toEqual(['Scarce', 'Transferable', 'Utility']);
    expect(card.sourceMaterial?.pages).toEqual([25, 26, 27]);
    for (const id of ['econ-2023-ol-q16-b-i-scarce-utility', 'econ-2023-ol-q16-b-i-transferable-utility']) {
      expect(ORDINARY.some(c => c.id === id), id).toBe(false);
    }
  });

  it('restores Ordinary marked components and retains required headings at their shared tariff', () => {
    const card = (suffix: string) => {
      const c = ORDINARY.find(item => item.id === `econ-2023-ol-${suffix}`)!;
      if (c.kind !== 'question') throw new Error('Expected question');
      return c;
    };
    expect(card('q11-c-i').totalMarks).toBe(10);
    expect(card('q11-c-i').rows.map(r => r.marks)).toEqual([6, 4]);
    expect(card('q11-c-i').rows[1].verbatim).toContain('Teachers doing grinds');
    expect(card('q16-a-ii').rows.map(r => r.marks)).toEqual([2, 4]);
    expect(card('q16-a-ii').rows[0].verbatim).toBe('Yes.');
    expect(card('q13-b-ii').totalMarks).toBe(18);
    expect(card('q13-b-ii-trade').totalMarks).toBe(9);
    expect(card('q13-b-ii-trade').topicId).toBe('economics-4-2');
    for (const [kept, old, marks] of [
      ['sa-q10-private', 'sa-q10-social', 12],
      ['q14-a-ii-reason', 'q14-a-ii-effect', 12],
    ] as const) {
      expect(CARD_ID_ALIASES[`econ-2023-ol-${old}`]).toBe(`econ-2023-ol-${kept}`);
      expect(card(kept).totalMarks).toBe(marks);
      expect(card(kept).rows).toHaveLength(2);
    }
    for (const suffix of ['sa-q9', 'sa-q10-private', 'q11-b-ii', 'q11-c-ii', 'q12-c-iii', 'q13-a-i', 'q14-a-ii-reason']) {
      expect(card(suffix).tariffModel.kind, suffix).toBe('questionTotal');
      expect(card(suffix).rows.every(r => r.marks === null), suffix).toBe(true);
    }
    expect(card('q15-b-ii').rows.map(r => r.marks)).toEqual([6, 3]);
    expect(card('q15-a-i-percentage').topicId).toBe('economics-1-1');
    expect(card('q11-b-ii').figure?.src).toContain('q11bii-equilibrium');
  });

  it('lifts 2023 Ordinary wording from the paper and hides its solutions until reveal', () => {
    const card = (s: string) => ORDINARY.find(c => c.id === `econ-2023-ol-${s}`)!;
    // A solution in the figure slot takes the whole printed question as the question crop.
    for (const [s, crop] of [['q11-b-ii', 'p11-q11bii'], ['q16-a-i-factors', 'p25-q16ai']] as const) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).questionFigure?.src, s).toContain(`economics-2023-OL-paper-${crop}-question.png`);
    }
    for (const c of ORDINARY.filter(item => item.year === 2023 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
    }
    // Data figures are cropped to the data alone, not to neighbouring asks or answer boxes.
    for (const [s, crop] of [['sa-q5', 'p07-q5-diagram'], ['q11-b-i', 'p11-q11b-diagram'],
      ['q11-b-iii', 'p11-q11b-diagram'], ['q14-a-i', 'p19-q14-chart'], ['q14-a-ii-reason', 'p19-q14-chart']] as const) {
      expect(card(s).figure?.solution, s).toBeFalsy();
      expect(card(s).figure?.src, s).toContain(`economics-2023-OL-paper-${crop}.png`);
    }
    // The asks the earlier extractors paraphrased now read as the paper prints them.
    expect(card('sa-q9').questionText).toContain('Capital funding of €2.3bn has been allocated');
    expect(card('q13-b-ii').questionText).toContain('The level of National Income in 2023');
    expect(card('q13-b-ii-trade').questionText).toContain('The Balance of Trade');
    expect(card('q14-a-ii-reason').questionText).toContain('in the line graph above and explain one effect');
    expect(card('sa-q3-a-i').rows[0].group?.options).toContain('Transport.');
    expect(card('q12-c-iii').rows.map(r => r.verbatim)).toEqual(['Economic.', 'Environment.', 'Social.']);
    expect(card('q11-b-ii').rows.map(r => r.verbatim)).toEqual(['Q1', 'P1', 'C1']);
    expect(card('q16-a-i-factors').rows.map(r => r.marks)).toEqual([4, 8, 4, 8]);
    expect(card('sa-q8-ii').rows[1].contextNote).toContain('scheme writes “second” where the paper says eighth');
    const text = ORDINARY.filter(c => c.year === 2023)
      .map(c => JSON.stringify([c.stem, c.questionText, c.rows])).join('\n');
    for (const junk of ['Possible responses', 'P a g e', '⟨', '____', 'the exam’s scenario', 'Adapted from']) {
      expect(text, junk).not.toContain(junk);
    }
  });

  it('keeps both 2023 calculation tasks and both explicitly accepted exchange-rate stances', () => {
    const cards = CARDS.filter(card => card.year === 2023);
    const q10 = cards.filter(card => /^2023 HL Section A Q10\(/.test(card.questionRef));
    expect(q10.map(card => [card.id, card.totalMarks])).toEqual([
      ['econ-2023-hl-sa-q10', 6], ['econ-2023-hl-sa-q10-c', 6],
    ]);
    const routes = cards.filter(card => card.id.startsWith('econ-2023-hl-q15-b-iii-euro'));
    expect(routes).toHaveLength(2);
    expect(routes.map(card => card.totalMarks)).toEqual([8, 8]);
    expect(routes.map(card => card.questionText)).toEqual(expect.arrayContaining([
      expect.stringContaining('Answer for: YES.'), expect.stringContaining('Answer for: NO.'),
    ]));
    const yes = routes.find(card => card.id.endsWith('-euro'))!;
    const no = routes.find(card => card.id.endsWith('-no'))!;
    if (yes.kind !== 'question' || no.kind !== 'question') throw new Error('Expected question cards');
    expect(yes.rows[0].group?.options).toHaveLength(2);
    expect(no.rows[0].group?.options).toHaveLength(2);
    expect(yes.rows[0].group?.options.join(' ')).not.toContain('Reduced inflationary pressures');
    expect(no.rows[0].group?.options.join(' ')).toContain('Reduced inflationary pressures');
  });

  it.skipIf(!canReadSecSources)('rejects changed or out-of-range targeted Irish allocation evidence', () => {
    const script = `
import copy, sys
sys.path.insert(0, 'scripts/markbank/authoring')
from econ_review import reviewed_papers, validate_review
indexed, reviewed = reviewed_papers()
key = (2023, 'higher', 'ev', 'LC034ALP000EV')
for field, value in [('schemeSha256', '0' * 64), ('paperPages', [999]), ('reason', '')]:
    altered = copy.deepcopy(reviewed[key])
    altered['targetedIrishEvidence'][field] = value
    try: validate_review(altered, indexed[key])
    except ValueError: continue
    raise AssertionError('Accepted ' + field)
print('targeted evidence mutations rejected')
`;
    expect(execFileSync('python3', ['-c', script], { encoding: 'utf8' }).trim())
      .toBe('targeted evidence mutations rejected');
  });

  it('retains both complete perfect-competition routes without an inferred diagram split', () => {
    const routes = sectionA.filter(card => /q6-a-[bc]$/.test(card.id));
    expect(routes.map(card => card.id).sort()).toEqual([
      'econ-2022-hl-sa-q6-a-b', 'econ-2022-hl-sa-q6-a-c',
    ]);
    for (const card of routes) {
      expect(card.totalMarks).toBe(15);
      expect(card.questionText).toContain('market equilibrium');
      expect(card.questionText).toContain('individual firm’s price');
      expect(card.figure?.solution).toBe(true);
      if (card.kind !== 'question') throw new Error('Expected question card');
      expect(card.tariffModel.kind).toBe('questionTotal');
      expect(card.rows).toHaveLength(4);
      expect(card.rows.every(row => row.marks === null)).toBe(true);
    }
    expect(routes[0].questionText).toContain('short run');
    expect(routes[1].questionText).toContain('long run');
    for (const old of ['econ-2022-hl-sa-q6-a-i', 'econ-2022-hl-sa-q6-a-ii']) {
      expect(CARD_ID_ALIASES[old]).toBe('econ-2022-hl-sa-q6-a-b');
    }
  });

  it('restores required examples and citizen responses rather than substituting extra government points', () => {
    const card = (id: string) => {
      const found = CARDS.find(value => value.id === id)!;
      if (found.kind !== 'question') throw new Error('Expected question card');
      return found;
    };
    const benefits = card('econ-2022-hl-q13-a-i');
    expect(benefits.rows.map(row => row.marks)).toEqual([5, 4]);
    expect(benefits.rows[0].group?.options).toHaveLength(4);
    expect(benefits.rows[1].verbatim).toContain('unemployment benefit');
    const government = card('econ-2022-hl-q16-b-ii');
    const citizens = card('econ-2022-hl-q16-b-ii-citizens');
    expect(government.totalMarks).toBe(7);
    expect(citizens.totalMarks).toBe(7);
    expect(government.rows[0].group?.options).toHaveLength(7);
    expect(citizens.rows[0].group?.options).toHaveLength(3);
    expect(government.rows[0].group?.options.join(' ')).not.toContain('Citizens:');
    const airports = card('econ-2022-hl-q11-c-iii-for');
    expect(airports.questionText).toContain('for and against');
    expect(airports.rows.map(row => row.marks)).toEqual([6, 6]);
    expect(CARD_ID_ALIASES['econ-2022-hl-q11-c-iii-against']).toBe(airports.id);
    expect(card('econ-2022-hl-q16-c-iii').totalMarks).toBe(5);
    expect(card('econ-2022-hl-sa-q8-b').rows[0].group?.options).toHaveLength(4);
  });

  it('lifts 2022 Higher wording from the paper and hides its solutions until reveal', () => {
    const card = (s: string) => {
      const found = CARDS.find(c => c.id === `econ-2022-hl-${s}`)!;
      if (found.kind !== 'question') throw new Error('Expected question');
      return found;
    };
    // A solution in the figure slot takes the whole printed question as the question crop.
    for (const [s, crop] of [['sa-q1-a', 'p03-q1a'], ['seca-q4-a-ticks', 'p06-q4a'], ['q14-a-ii-ticks', 'p26-q14aii'],
      ['q14-b-i', 'p27-q14b'], ['q14-b-ii', 'p27-q14b'], ['q15-a-iii', 'p31-q15aiii']] as const) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).questionFigure?.src, s).toContain(`economics-2022-HL-paper-${crop}-question.png`);
    }
    for (const c of CARDS.filter(item => item.year === 2022 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
    }
    // Data figures are cropped to the data alone, not to neighbouring asks or answer boxes.
    for (const [s, crop] of [['sa-q1-b', 'p03-q1-graph'], ['seca-q2-a', 'p04-q2-infographic'],
      ['sa-q10-b', 'p13-q10-data'], ['q11-a-i', 'p14-q11-infographic'], ['q12-a-i', 'p18-q12-charts'],
      ['q13-a-i', 'p22-q13-infographic'], ['q14-c-i', 'p28-q14c-chart'], ['q15-a-i', 'p30-q15a-chart'],
      ['q15-b-i', 'p32-q15b-chart'], ['q15-c-i', 'p33-q15c-chart']] as const) {
      expect(card(s).figure?.solution, s).toBeFalsy();
      expect(card(s).figure?.src, s).toContain(`economics-2022-HL-paper-${crop}.png`);
    }
    // The asks and stems the earlier extractors wrote now read as the paper prints them.
    expect(card('sa-q2-b').stem).toBe('The infographic below shows the Quarterly National Accounts for Quarter 2, 2021.');
    expect(card('seca-q7-a-ii').stem).toContain('Only one of the charts below accurately displays');
    expect(card('q11-c-i').questionText).toBe('Explain the term opportunity cost.');
    expect(card('q16-a-i').questionText).toContain('this government intervention on social sustainability');
    expect(card('q14-b-i').conceptId).toBe('total-average-total-and-marginal-cost');
    expect(card('q12-a-i').rows.map(r => r.marks)).toEqual([3, 3, 3]);
    expect(card('q15-a-ii').rows.map(r => r.marks)).toEqual([4, 4]);
    expect(card('sa-q5-a').rows[0].group?.options).toHaveLength(4);
    expect(card('sa-q5-a').rows[0].group?.options.join(' ')).not.toContain('Adapted from');
    expect(card('q11-a-ii').rows[0].group?.options).toHaveLength(5);
    const text = CARDS.filter(c => c.year === 2022)
      .map(c => JSON.stringify([c.stem, c.questionText, c.rows])).join('\n');
    for (const junk of ['Possible responses', 'P a g e', '⟨', '____', 'Adapted from', 'Leaving Certificate']) {
      expect(text, junk).not.toContain(junk);
    }
  });

  it.skipIf(!canReadSecSources)('rejects source changes, omitted directives and stale directive reviews', () => {
    const script = `
import copy, json, sys
sys.path.insert(0, 'scripts/markbank/authoring')
from econ_review import reviewed_papers, validate_review
indexed, reviewed = reviewed_papers()
key = (2022, 'higher', 'ev', 'LC034ALP000EV')
base = reviewed[key]
for mutation in ['source', 'omitted', 'stale']:
    altered = copy.deepcopy(base)
    if mutation == 'source': altered['paperSha256'] = '0' * 64
    if mutation == 'omitted': altered['selections'].pop()
    if mutation == 'stale': altered['selections'][0]['text'] += ' changed'
    try: validate_review(altered, indexed[key])
    except ValueError: continue
    raise AssertionError('Accepted ' + mutation)
print('three invalid reviews rejected')
`;
    expect(execFileSync('python3', ['-c', script], { encoding: 'utf8' }).trim())
      .toBe('three invalid reviews rejected');
  });

  it.skipIf(!canReadSecSources)('classifies Irish yes/no wording as well as explicit either/or choices', () => {
    const script = `
import copy, sys
sys.path.insert(0, 'scripts/markbank/authoring')
from econ_review import reviewed_papers, validate_review
indexed, reviewed = reviewed_papers()
key = (2023, 'higher', 'iv', 'LC034ALP000IV')
base = reviewed[key]
for page in [10, 32, 33, 34]:
    candidates = [x for x in base['selections'] if x['page'] == page and ('Tá:' in x['text'] or 'An dóigh' in x['text'] or 'An léiríonn' in x['text'])]
    assert candidates, page
    assert all(x['classification'] == 'answer-classification' for x in candidates)
    altered = copy.deepcopy(base)
    altered['selections'].remove(candidates[0])
    try: validate_review(altered, indexed[key])
    except ValueError: continue
    raise AssertionError('Accepted omitted Irish yes/no on page ' + str(page))
print('Irish yes/no omissions rejected')
`;
    expect(execFileSync('python3', ['-c', script], { encoding: 'utf8' }).trim())
      .toBe('Irish yes/no omissions rejected');
  });

  it.skipIf(!canReadSecSources)('rejects omission of the Irish any-two instruction inside the economic-goods task', () => {
    const script = `
import copy, sys
sys.path.insert(0, 'scripts/markbank/authoring')
from econ_review import reviewed_papers, validate_review
indexed, reviewed = reviewed_papers()
key = (2023, 'ordinary', 'iv', 'LC034GLP000IV')
base = reviewed[key]
route = [x for x in base['selections'] if 'dhá cheann ar bith' in x['text']]
assert len(route) == 1 and route[0]['classification'] == 'finite-route'
assert route[0]['page'] == 26
altered = copy.deepcopy(base)
altered['selections'].remove(route[0])
try: validate_review(altered, indexed[key])
except ValueError: print('Irish any-two omission rejected')
else: raise AssertionError('accepted omitted Irish choose-two directive')
`;
    expect(execFileSync('python3', ['-c', script], { encoding: 'utf8' }).trim())
      .toBe('Irish any-two omission rejected');
  });

  it('explains Ordinary Irish notation and conflicting scheme cells without changing the task tariff', () => {
    for (const [suffix, text] of [
      ['sa-q6-i', 'T with Táirgeacht and I with Intíre'],
      ['q11-b-i', 'meánchostas (average cost)'],
      ['q11-b-ii', 'C1 for output, P1 for price and Co1 for average cost'],
      ['q12-b-i', 'scheme prints 10 here'],
      ['q13-b-i', 'misprints the C column as P'],
      ['q15-b-i', 'Praghas is price and Méid is quantity'],
    ]) {
      const card = ORDINARY.find(c => c.id === `econ-2023-ol-${suffix}`)!;
      expect(card.rows[0].contextNote, card.id).toContain(text);
      expect(card.questionText, card.id).not.toContain(text);
    }
    const equity = ORDINARY.find(c => c.id === 'econ-2023-ol-q12-b-i')!;
    expect(equity.totalMarks).toBe(8);
    expect(ordinary2023IrishReview.questions.find(q => q.n === '12')?.allocationEvidence?.schemePages)
      .toEqual([16]);
    const percentage = ORDINARY.find(c => c.id === 'econ-2023-ol-q15-a-i-percentage')!;
    if (percentage.kind !== 'question') throw new Error('Expected question');
    expect(percentage.rows[0].verbatim).toBe('81.32%');
    expect(percentage.rows[0].contextNote).toContain('(101,853 + 68,042) ÷ 208,913 × 100 = 81.32%');
  });

  it('retains previously excluded asks at their complete marked boundary', () => {
    const allCards = [...CARDS, ...ORDINARY];
    for (const correction of boundaryCorrections.corrections) {
      const card = allCards.find(item => item.id === correction.cardId)!;
      expect(card.questionRef, card.id).toContain(correction.question);
      expect(card.totalMarks, card.id).toBe(correction.marks);
      expect(card.sourceMaterial?.pages, card.id).toEqual(correction.paperPages);
      const n = card.questionRef.match(/Q(\d+)/)![1];
      const topics = examTopicIdsForQuestion('economics', card.level, card.year, 'main', n, 'single', 'ev');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic), card.id).toContain(card.topicId);
    }
    const kerosene = ORDINARY.find(card => card.id === 'econ-2021-ol-sa-q3-i')!;
    if (kerosene.kind !== 'question') throw new Error('Expected question card');
    expect(kerosene.questionText).toContain('price elastic or price inelastic');
    expect(kerosene.rows.some(row => row.verbatim.includes('It is elastic'))).toBe(true);
    expect(kerosene.tariffModel.kind).toBe('questionTotal');
    const coffee = ORDINARY.find(card => card.id === 'econ-2022-ol-q12-a-i')!;
    expect(coffee.questionText).toContain('market equilibrium price');
    expect(coffee.questionText).toContain('market equilibrium quantity');
    expect(CARD_ID_ALIASES['econ-2022-ol-q12-a-ii']).toBe(coffee.id);
    // Q16(a)(i) definitions (4 + 4) and (a)(ii) diagram and explanation (7 + 8) are separate tasks.
    const definitions = CARDS.find(card => card.id === 'econ-2023-hl-q16-a-i')!;
    const demand = CARDS.find(card => card.id === 'econ-2023-hl-q16-a-ii')!;
    if (demand.kind !== 'question' || definitions.kind !== 'question') throw new Error('Expected question card');
    expect(definitions.rows.map(r => r.marks)).toEqual([4, 4]);
    expect(definitions.rows[0].verbatim).toContain('Individual Demand refers');
    expect(definitions.rows[1].verbatim).toContain('Market Demand refers');
    expect(demand.rows.map(r => r.marks)).toEqual([7, 8]);
    expect(exclusions).toHaveLength(1);
    expect(exclusions[0].ref).toBe('2024 HL Section A Q10(a)(i)');
    expect(exclusions[0].evidence).toContain('Part (i) has been completed for you');
  });

  it('matches the independent Ordinary census, tariffs, source pages and Atlas topics', () => {
    const cards = ORDINARY.filter(card => card.year === 2022);
    const tasks = ordinaryReview.questions.flatMap(question => question.tasks);
    expect(tasks).toHaveLength(62);
    expect(cards.map(card => card.id).sort()).toEqual(tasks.map(task => task.cardId).sort());
    for (const question of ordinaryReview.questions) {
      const atlasNodes = examTopicIdsForQuestion('economics', 'ordinary', 2022, 'main', question.n,
        'single', 'ev').flatMap(curriculumNodeIdsForExamTopic);
      for (const task of question.tasks) {
        const card = cards.find(value => value.id === task.cardId)!;
        expect(card.totalMarks, task.cardId).toBe(task.marks);
        expect(card.topicId, task.cardId).toBe(task.topicId);
        expect(atlasNodes, task.cardId).toContain(task.topicId);
        expect(card.sourceMaterial?.pages, task.cardId).toEqual(question.paperPages);
        expect(card.paperFileid, task.cardId).toBe('LC034GLP000EV');
      }
      if (Number(question.n) > 10) {
        const oneRoute = question.tasks.filter(task => task.key !== 'a/ii/capital');
        expect(oneRoute.reduce((sum, task) => sum + task.marks, 0), `OL Q${question.n}`).toBe(75);
      }
    }
  });

  it('keeps both expenditure routes and requires a definition plus an example in each', () => {
    for (const suffix of ['expenditure', 'capital']) {
      const card = ORDINARY.find(value => value.id === `econ-2022-ol-q13-a-ii-${suffix}`)!;
      if (card.kind !== 'question') throw new Error('Expected question');
      expect(card.totalMarks).toBe(9);
      expect(card.rows.map(row => row.marks)).toEqual([6, 3]);
      expect(card.rows.every(row => row.kind === 'point')).toBe(true);
      expect(card.questionText).toContain('Explain current or capital government expenditure');
      expect(card.questionText).toContain(suffix === 'capital' ? 'Answer for: CAPITAL EXPENDITURE' : 'Answer for: CURRENT EXPENDITURE');
      expect(card.rows[1].verbatim).toContain('Example:');
    }
  });

  it('uses the Irish scheme to resolve separate hidden-economy boundaries without guessing row marks', () => {
    const hidden = ORDINARY.find(card => card.id === 'econ-2022-ol-q16-c-ii')!;
    const effect = ORDINARY.find(card => card.id === 'econ-2022-ol-q16-c-iii')!;
    const indirect = ORDINARY.find(card => card.id === 'econ-2022-ol-q16-c-i')!;
    for (const card of [hidden, indirect]) {
      if (card.kind !== 'question') throw new Error('Expected question');
      expect(card.tariffModel.kind).toBe('questionTotal');
      expect(card.rows.every(row => row.marks === null)).toBe(true);
    }
    expect(hidden.totalMarks).toBe(8);
    expect(hidden.questionText).not.toContain('economic effect');
    expect(hidden.stem).toContain('smuggling of cigarettes');
    expect(effect.totalMarks).toBe(8);
    expect(effect.topicId).toBe('economics-3-0');
    expect(effect.questionText).toContain('one economic effect');
    expect(indirect.totalMarks).toBe(8);
    expect(CARD_ID_ALIASES['econ-2022-ol-q16-c-iii']).toBeUndefined();
    expect(ORDINARY.find(card => card.id === 'econ-2022-ol-q14-b-i')?.totalMarks).toBe(17);
  });

  it('carries the 2022 Ordinary parts priced by one first/second tariff as one card each', () => {
    // Q3, Q8 and Q14(b) each print one 1st x n, 2nd x m beside the stem across (i) and (ii).
    for (const [kept, old, marks] of [
      ['sa-q3-i', 'sa-q3-ii', 15], ['sa-q8-i', 'sa-q8-ii', 15], ['q14-b-i', 'q14-b-ii-water', 17],
    ] as const) {
      const card = ORDINARY.find(c => c.id === `econ-2022-ol-${kept}`)!;
      if (card.kind !== 'question') throw new Error('Expected question');
      expect(card.totalMarks, kept).toBe(marks);
      expect(card.tariffModel.kind, kept).toBe('questionTotal');
      expect(card.rows.map(r => r.marks), kept).toEqual([null, null]);
      expect(CARD_ID_ALIASES[`econ-2022-ol-${old}`]).toBe(card.id);
      expect(ORDINARY.some(c => c.id === `econ-2022-ol-${old}`), old).toBe(false);
    }
  });

  it('lifts 2022 Ordinary wording from the paper and hides its solutions until reveal', () => {
    const card = (s: string) => {
      const found = ORDINARY.find(c => c.id === `econ-2022-ol-${s}`)!;
      if (found.kind !== 'question') throw new Error('Expected question');
      return found;
    };
    // A solution in the figure slot takes the whole printed question as the question crop.
    for (const [s, crop] of [['seca-q4-ticks', 'p05-q4'], ['seca-q7-a-ii-ticks', 'p07-q7aii'],
      ['sa-q7-b-ii', 'p07-q7b'], ['seca-q9-i', 'p08-q9i'], ['q11-b-ii', 'p11-q11bii'], ['q12-a-i', 'p13-q12a'],
      ['q12-b-ii', 'p14-q12b'], ['q12-b-iii', 'p14-q12b'], ['q13-a-i-percentage', 'p16-q13ai'],
      ['q13-b-ii', 'p17-q13bii'], ['q14-a-i', 'p19-q14ai']] as const) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).questionFigure?.src, s).toContain(`economics-2022-OL-paper-${crop}-question.png`);
    }
    for (const c of ORDINARY.filter(item => item.year === 2022 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
    }
    // Data figures are cropped to the data alone.
    for (const [s, crop] of [['sa-q1-i', 'p03-q1-infographic'], ['sa-q10-a', 'p09-q10-chart'],
      ['q11-b-i', 'p11-q11b-diagram'], ['q12-b-i', 'p14-q12b-diagram'], ['q13-a-ii-capital', 'p16-q13-chart'],
      ['q15-a-i-trend', 'p22-q15a-chart'], ['q15-c-i', 'p24-q15c-chart']] as const) {
      const c = ORDINARY.find(item => item.id === `econ-2022-ol-${s}`)!;
      expect(c.figure?.solution, s).toBeFalsy();
      expect(c.figure?.src, s).toContain(`economics-2022-OL-paper-${crop}.png`);
    }
    // The asks and stems the earlier extractors wrote now read as the paper prints them,
    // keeping the Irish label notes the earlier review placed on four asks.
    expect(card('sa-q2-i').questionText).toBe('What do the initials CSO stand for? (POS in the Irish paper)');
    expect(card('q11-a-ii').stem).toBe('The graph below shows the breakdown of streaming services in the US.');
    expect(card('q15-a-i-trend').stem).toContain('The graph below shows the corporation tax received');
    expect(card('q11-b-ii').questionText).toContain('On the Irish paper use C₁ for output');
    expect(card('q12-b-iii').questionText).toContain('On the Irish paper use C₂ for the new quantity');
    expect(card('seca-q4-ticks').rows.map(r => r.verbatim)).toEqual([
      'Substitute — Samsung S21', 'Complementary — iPhone 13 case', 'Complementary — iPhone charging plug',
      'Substitute — Google Pixel 4A smartphone']);
    expect(card('q14-a-i').rows.map(r => r.marks)).toEqual([6, 6, 6, 6]);
    expect(card('q15-c-i').rows.map(r => r.marks)).toEqual([6, 6]);
    expect(card('q15-a-ii').rows.map(r => r.marks)).toEqual([6, 3]);
    const text = ORDINARY.filter(c => c.year === 2022)
      .map(c => JSON.stringify([c.stem, c.questionText, c.rows])).join('\n');
    for (const junk of ['Possible responses', 'P a g e', '⟨', '____', 'Adapted from', 'Leaving Certificate']) {
      expect(text, junk).not.toContain(junk);
    }
  });

  it('matches all 65 independently counted 2021 Higher routes, tariffs, sources and Atlas topics', () => {
    const cards = CARDS.filter(card => card.year === 2021);
    const tasks = higher2021Review.questions.flatMap(question => question.tasks);
    expect(tasks).toHaveLength(65);
    expect(cards.map(card => card.id).sort()).toEqual(tasks.map(task => task.cardId).sort());
    for (const question of higher2021Review.questions) {
      const atlasNodes = examTopicIdsForQuestion('economics', 'higher', 2021, 'main', question.n,
        'single', 'ev').flatMap(curriculumNodeIdsForExamTopic);
      for (const task of question.tasks) {
        const card = cards.find(value => value.id === task.cardId)!;
        expect(card.totalMarks, task.cardId).toBe(task.marks);
        expect(card.topicId, task.cardId).toBe(task.topicId);
        expect(atlasNodes, task.cardId).toContain(task.topicId);
        expect(card.sourceMaterial?.pages, task.cardId).toEqual(question.paperPages);
        expect(card.paperFileid, task.cardId).toBe('LC034ALP000EV');
      }
      // Section A answers (b) or (c) in Q4, Q6 and Q7; each route is counted once.
      const n = Number(question.n);
      const once = question.tasks.filter(task => !(n <= 10 && task.key === 'c'))
        .reduce((sum, task) => sum + task.marks, 0);
      expect(once, `HL Q${question.n}`).toBe(n > 10 ? 75 : 15);
    }
  });

  it('keeps 2021 Higher answers priced across two headings whole and restores the full scheme lists', () => {
    const card = (s: string) => {
      const found = CARDS.find(c => c.id === `econ-2021-hl-${s}`)!;
      if (found.kind !== 'question') throw new Error('Expected question');
      return found;
    };
    // Q12(a)(ii) prints 2 @ 8 and 2 @ 5 beside one ask for two positive AND two negative impacts.
    const impacts = card('q12-a-ii-pos');
    expect(impacts.totalMarks).toBe(26);
    expect(impacts.rows).toHaveLength(1);
    expect(impacts.rows[0].group?.perOptionSteps).toEqual([8, 8, 5, 5]);
    expect(impacts.rows[0].group?.options).toHaveLength(13);
    // Q16(b)(ii) prints one 10 (2 @ 5) cell for one social AND one economic reason.
    const wage = card('q16-b-ii-social');
    expect(wage.totalMarks).toBe(10);
    expect(wage.rows.map(r => [r.marks, r.group?.claimMax, r.group?.options.length])).toEqual([[5, 1, 3], [5, 1, 3]]);
    for (const [old, kept] of [['q12-a-ii-neg', 'q12-a-ii-pos'], ['q16-b-ii-economic', 'q16-b-ii-social']]) {
      expect(CARD_ID_ALIASES[`econ-2021-hl-${old}`]).toBe(`econ-2021-hl-${kept}`);
      expect(CARDS.some(c => c.id === `econ-2021-hl-${old}`), old).toBe(false);
    }
    // The answer is marked as well as its explanation.
    expect(card('q11-a-ii').rows.map(r => r.marks)).toEqual([3, 5]);
    expect(card('q11-b-ii').rows.map(r => r.marks)).toEqual([2, 8]);
    expect(card('q15-a').tariffModel.kind).toBe('questionTotal');
    expect(card('q15-a').rows.every(r => r.marks === null)).toBe(true);
    // Every menu carries the scheme's whole list.
    for (const [s, count] of [['sa-q1-b', 3], ['sa-q3-b', 3], ['sa-q5-b', 6], ['sa-q6-b', 4], ['sa-q6-c', 4],
      ['q11-b-iii', 4], ['q11-c-ii', 8], ['q12-b-i', 5], ['q15-c-iii', 4], ['q16-a-i', 5], ['q16-a-ii', 7]] as const) {
      expect(card(s).rows[0].group?.options, s).toHaveLength(count);
    }
    expect(card('sa-q10-b').rows[0].group?.options.map(o => o.split(' ')[0])).toEqual(['During', 'ECB']);
    expect(card('q14-a-i').rows[0].group?.perOptionSteps).toEqual([6, 3, 3]);
  });

  it('lifts 2021 Higher wording from the paper and hides its solutions until reveal', () => {
    const card = (s: string) => {
      const found = CARDS.find(c => c.id === `econ-2021-hl-${s}`)!;
      if (found.kind !== 'question') throw new Error('Expected question');
      return found;
    };
    // A solution in the figure slot takes the whole printed question as the question crop.
    for (const [s, crop] of [['sa-q2', 'p04-q2'], ['q13-a-i', 'p22-q13a'], ['q13-a-ii', 'p22-q13a']] as const) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).questionFigure?.src, s).toContain(`economics-2021-HL-paper-${crop}-question.png`);
    }
    for (const c of CARDS.filter(item => item.year === 2021 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
    }
    // Calculation workings wait for the reveal; the ask carries every figure they use.
    for (const [s, crop] of [['q13-c-i', 'p24-q13ci-working'], ['q15-c-ii', 'p30-q15cii-working']] as const) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).figure?.src, s).toContain(`economics-2021-HL-scheme-${crop}.png`);
    }
    // Data figures are cropped to the data alone.
    for (const [s, crop] of [['sa-q3-a', 'p04-q3-chart'], ['sa-q3-b', 'p04-q3-chart'], ['seca-q8-a', 'p12-q8-ratios'],
      ['seca-q8-b', 'p12-q8-ratios'], ['q16-b-ii-social', 'p35-i0']] as const) {
      expect(card(s).figure?.solution, s).toBeFalsy();
      expect(card(s).figure?.src, s).toContain(`economics-2021-HL-paper-${crop}.png`);
    }
    // The stems the earlier extractors wrote now read as the paper prints them.
    expect(card('sa-q3-a').stem).toBe('The table below shows the subscription price for a basic Netflix account in '
      + 'different countries. (The prices have been converted into US dollars $ for comparison purposes)');
    expect(card('q11-a-ii').stem).toBe('The pie chart below shows the market share of the Global Aircraft Market in 2018.');
    expect(card('seca-q8-a').stem).toBe('John always spends his income in the following ratio of price to marginal utility:');
    expect(card('q13-a-ii').stem).toContain('Shortages of the PlayStation 5');
    expect(card('sa-q6-b').stem).toBe('The data below has been extracted from the HDI 2020.');
    expect(card('sa-q2').rows.map(r => r.verbatim.split(' — ')[0])).toEqual(['Positive', 'Normative', 'Normative', 'Positive']);
    const text = CARDS.filter(c => c.year === 2021)
      .map(c => JSON.stringify([c.stem, c.questionText, c.rows])).join('\n');
    for (const junk of ['Possible responses', 'Suggested responses', 'P a g e', '⟨', '____', 'Adapted from',
      'Leaving Certificate']) {
      expect(text, junk).not.toContain(junk);
    }
  });

  it('matches all 57 independently counted 2021 Ordinary routes, tariffs, sources and Atlas topics', () => {
    const cards = ORDINARY.filter(card => card.year === 2021);
    const tasks = ordinary2021Review.questions.flatMap(question => question.tasks);
    expect(tasks).toHaveLength(57);
    expect(cards.map(card => card.id).sort()).toEqual(tasks.map(task => task.cardId).sort());
    for (const question of ordinary2021Review.questions) {
      const atlasNodes = examTopicIdsForQuestion('economics', 'ordinary', 2021, 'main', question.n,
        'single', 'ev').flatMap(curriculumNodeIdsForExamTopic);
      for (const task of question.tasks) {
        const card = cards.find(value => value.id === task.cardId)!;
        expect(card.totalMarks, task.cardId).toBe(task.marks);
        expect(card.topicId, task.cardId).toBe(task.topicId);
        expect(atlasNodes, task.cardId).toContain(task.topicId);
        expect(card.sourceMaterial?.pages, task.cardId).toEqual(question.paperPages);
        expect(card.paperFileid, task.cardId).toBe('LC034GLP000EV');
      }
      // Section A answers (a) or (b) in Q6, Q9 and Q10; Q11(b)(i) is an advantage OR a disadvantage.
      const n = Number(question.n);
      const once = question.tasks.filter(task => !(n <= 10 && task.key === 'b') && task.key !== 'b/i/disadvantage')
        .reduce((sum, task) => sum + task.marks, 0);
      expect(once, `OL Q${question.n}`).toBe(n > 10 ? 75 : 15);
    }
  });

  it('prices 2021 Ordinary parts at their printed cells and keeps required headings together', () => {
    const card = (s: string) => {
      const found = ORDINARY.find(c => c.id === `econ-2021-ol-${s}`)!;
      if (found.kind !== 'question') throw new Error('Expected question');
      return found;
    };
    // Q14(b)(ii) prints a separate 1 @ 8 for each objective: two cards, the older one keeping the environment.
    expect(card('q13-c-ii').questionRef).toBe('2021 OL Q14(b)(ii) — care for the environment');
    expect(card('q14-b-ii-services').questionRef).toBe('2021 OL Q14(b)(ii) — maintaining state services');
    expect([card('q13-c-ii').totalMarks, card('q14-b-ii-services').totalMarks]).toEqual([8, 8]);
    expect(card('q13-c-ii').rows[0].group?.options).toHaveLength(5);
    expect(card('q14-b-ii-services').rows[0].group?.options).toHaveLength(4);
    // One cell for two required headings: one card with a row per heading.
    for (const [s, marks] of [['q13-b-i', [7, 7]], ['q14-a-i', [10, 10]], ['q15-a-i', [8, 8]]] as const) {
      expect(card(s).rows.map(r => r.marks), s).toEqual(marks);
    }
    // Printed tariffs: Q6(b) 9 + 6, Q9(b) 9 then 6, Q12(b) 9 then 6 and 6.
    expect(card('sa-q6-b').rows.map(r => r.marks)).toEqual([9, 6]);
    expect(card('sa-q9-b').rows[0].group?.perOptionSteps).toEqual([9, 6]);
    expect(card('q12-b').totalMarks).toBe(21);
    expect(card('q12-b').rows[0].group?.perOptionSteps).toEqual([9, 6, 6]);
    // First-correct tariffs on objective answers are unpriced rows.
    for (const s of ['sa-q2', 'sa-q6-a', 'sa-q9-a', 'sa-q10-a']) {
      expect(card(s).tariffModel.kind, s).toBe('questionTotal');
      expect(card(s).rows.every(r => r.marks === null), s).toBe(true);
    }
    // Every menu carries the scheme's whole list.
    for (const [s, count] of [['sa-q10-b', 8], ['q11-b-i-pos', 8], ['q11-b-i-neg', 4], ['q11-b-iii', 7],
      ['q13-c-iii', 7]] as const) {
      expect(card(s).rows[0].group?.options, s).toHaveLength(count);
    }
    expect(card('q11-a-i').rows.map(r => r.verbatim)).toEqual(['+ 1', '+ 0.2 Years', '+ 0.2', 'Yes']);
  });

  it('lifts 2021 Ordinary wording from the paper and hides its solutions until reveal', () => {
    const card = (s: string) => {
      const found = ORDINARY.find(c => c.id === `econ-2021-ol-${s}`)!;
      if (found.kind !== 'question') throw new Error('Expected question');
      return found;
    };
    // A solution in the figure slot takes the whole printed question as the question crop.
    for (const [s, crop] of [['sa-q2', 'p04-q2'], ['sa-q3-i', 'p04-q3'], ['sa-q4', 'p05-q4'], ['sa-q8', 'p07-q8'],
      ['q12-a-ii', 'p13-q12a']] as const) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).questionFigure?.src, s).toContain(`economics-2021-OL-paper-${crop}-question.png`);
    }
    for (const c of ORDINARY.filter(item => item.year === 2021 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
    }
    expect(card('sa-q8').figure?.src).toContain('economics-2021-OL-scheme-p07-q8-diagram.png');
    // Data figures: both HDI tables in one crop.
    for (const s of ['q11-a-i', 'q11-a-ii']) {
      expect(card(s).figure?.solution, s).toBeFalsy();
      expect(card(s).figure?.src, s).toContain('economics-2021-OL-paper-p10-q11-hdi-tables.png');
    }
    // The asks and stems the earlier extractors wrote now read as the paper prints them.
    expect(card('q13-c-iii-types').questionText).toBe('Explain one possible cause of inflation in Ireland during this time.');
    expect(card('q11-a-ii').stem).toBe('The data below is extracted from the Human Development Index (HDI) in 2019 and 2020.');
    expect(card('q15-b-i').questionText).toContain('had on the demand for Nike products');
    expect(card('sa-q2').rows.map(r => r.verbatim.split(' — ')[0])).toEqual(['Positive', 'Normative']);
    const text = ORDINARY.filter(c => c.year === 2021)
      .map(c => JSON.stringify([c.stem, c.questionText, c.rows])).join('\n');
    for (const junk of ['Possible Responses', 'Suggested responses', 'P a g e', '⟨', '____', 'Adapted from',
      'Leaving Certificate', 'Set on']) {
      expect(text, junk).not.toContain(junk);
    }
  });

  it.each([
    { review: irishReview, cards: ORDINARY, level: 'ordinary' as const, count: 62 },
    { review: higherIrishReview, cards: CARDS, level: 'higher' as const, count: 75 },
    { review: higher2023IrishReview, cards: CARDS, level: 'higher' as const, count: 74 },
    { review: ordinary2023IrishReview, cards: ORDINARY, level: 'ordinary' as const, count: 61 },
    { review: higher2024IrishReview, cards: CARDS, level: 'higher' as const, count: 83 },
    { review: ordinary2024IrishReview, cards: ORDINARY, level: 'ordinary' as const, count: 61 },
  ])('attaches every independently checked $level Irish route to its source and Atlas topic', ({ review, cards, level, count }) => {
    expect(review.questions.flatMap(q => q.tasks)).toHaveLength(count);
    for (const question of review.questions) {
      expect(question.equivalenceReason.length).toBeGreaterThan(20);
      const nodes = examTopicIdsForQuestion('economics', level, review.year, 'main', question.n,
        'single', 'iv').flatMap(curriculumNodeIdsForExamTopic);
      for (const task of question.tasks) {
        const card = cards.find(value => value.id === task.cardId)!;
        expect(card.totalMarks, task.cardId).toBe(task.marks);
        expect(card.topicId, task.cardId).toBe(task.topicId);
        expect(nodes, task.cardId).toContain(task.topicId);
        expect(card.additionalSourceMaterials, task.cardId).toHaveLength(1);
        expect(card.additionalSourceMaterials?.[0].sourceFileid, task.cardId).toBe(review.fileid);
        expect(card.additionalSourceMaterials?.[0].pages, task.cardId).toEqual(question.paperPages);
        expect(card.sourceMaterial?.label, task.cardId).toBe('ENGLISH QUESTION PAGE');
      }
    }
    const record = inventory.papers.find(p => p.year === review.year && p.level === level && p.lang === 'iv')!;
    expect(record.primaryMarkBankCardIds).toHaveLength(0);
    expect(record.equivalentEditionCardIds).toHaveLength(count);
    expect(record.markBankCardIds).toHaveLength(count);
  });

  it('carries the checked 2024 Irish corrections and label meanings into shared answers', () => {
    for (const [suffix, fragment] of [
      ['sa-q1-b', 'export credits exceed import debits'],
      ['sa-q3-a', 'Pc is equilibrium price and Cc is equilibrium quantity'],
      ['sa-q6-a-diagram', 'Costas imeallach is marginal cost'],
      ['sa-q10-a-ii', 'OTI is GDP, OTN is GNP'],
      ['q12-b-i', 'PIT means CPI'],
      ['q14-b-i', 'C1 is equilibrium quantity/output'],
      ['q14-b-i-explanation', 'II/MR denotes marginal revenue'],
    ]) {
      const card = CARDS.find(c => c.id === `econ-2024-hl-${suffix}`)!;
      expect(card.rows[0].contextNote, card.id).toContain(fragment);
    }
    expect(higher2024IrishReview.selections).toHaveLength(35);
    expect(higher2024IrishReview.questions.find(q => q.n === '16')?.equivalenceReason)
      .toContain('scheme stale2021/2022');
  });

  it('explains 2023 Irish translation, diagram, formula and allocation differences after reveal', () => {
    const requiredGuidance = [
      ['sa-q3-a', '1 mark for the correct answer and 1 for correct working'],
      ['sa-q5-a', 'C for efficient, A for inefficient and B for impossible'],
      ['sa-q5-b', 'A is inefficient because it lies inside'],
      ['sa-q6-b', 'accepts discussion of any taxation principles'],
      ['sa-q7-a', 'É denotes demand'],
      ['q11-c-iii', 'matching English scheme gives 9 marks (5 + 4)'],
      ['q12-a-iii', 'horizontal-axis label C denotes quantity/output'],
      ['q13-a-i', 'savings (coigilteas), not spending (caiteachas)'],
      ['q13-a-ii', '12 marks altogether'],
      ['q13-b-ii-multiplier', '1 ÷ (1 − MPC + MPM)'],
      ['q15-c-iii', 'Ní dóigh liom (No)'],
      ['q16-a-ii', 'leftward shift of demand (éileamh)'],
    ];
    for (const [suffix, guidance] of requiredGuidance) {
      const card = CARDS.find(item => item.id === `econ-2023-hl-${suffix}`)!;
      if (card.kind !== 'question') throw new Error('Expected question');
      expect(card.rows[0].contextNote, card.id).toContain(guidance);
      expect(card.questionText, card.id).not.toContain(guidance);
    }
    expect(higher2023IrishReview.questions.find(q => q.n === '6')?.equivalenceReason)
      .toContain('broader Irish acceptance');
    for (const [n, pages] of [['11', [18]], ['13', [23]]] as const) {
      expect(higher2023IrishReview.questions.find(q => q.n === n)?.allocationEvidence?.schemePages)
        .toEqual(pages);
    }
  });

  it('explains Higher edition differences and corrects misleading exchange-rate units', () => {
    const card = (id: string) => {
      const found = CARDS.find(value => value.id === id)!;
      if (found.kind !== 'question') throw new Error('Expected question');
      return found;
    };
    expect(card('econ-2022-hl-sa-q8-a').topicId).toBe('economics-3-0');
    for (const [id, text] of [
      ['econ-2022-hl-seca-q2-a', 'OTN (GNP) falling 6.7%'],
      ['econ-2022-hl-sa-q5-c', '7 marks (4 + 3)'],
      ['econ-2022-hl-sa-q6-a-b', 'assess the complete 15-mark route'],
      ['econ-2022-hl-seca-q10-a', '6 marks'],
      ['econ-2022-hl-q12-b-ii', 'CI = marginal cost (MC)'],
    ]) {
      expect(card(id).rows[0].contextNote, id).toContain(text);
    }
    const exchange = card('econ-2022-hl-q15-b-i');
    expect(exchange.rows[0].contextNote).toContain('pounds per €1 (£/€)');
    expect(exchange.rows[0].contextNote).toContain('83p to 74p');
    expect(exchange.rows[0].group?.options.join(' ')).not.toContain('pence');
    expect(exchange.rows[0].group?.options).toHaveLength(3);
  });

  it('provides a completed official solution for every Higher drawing task', () => {
    for (const id of [
      'econ-2022-hl-sa-q6-a-b', 'econ-2022-hl-sa-q6-a-c',
      'econ-2022-hl-q11-b-i', 'econ-2022-hl-q12-b-ii',
      'econ-2022-hl-q14-b-ii', 'econ-2022-hl-q15-a-iii', 'econ-2022-hl-q16-c-i',
    ]) {
      expect(CARDS.find(card => card.id === id)?.figure?.solution, id).toBe(true);
    }
    const milk = CARDS.find(card => card.id === 'econ-2022-hl-q15-a-iii')!;
    expect(milk.questionFigure?.solution).not.toBe(true);
    expect(milk.questionFigure?.alt).toContain('blank market diagram');
    expect(milk.figure?.alt).toContain('grant aid shifts supply right');
    const floor = CARDS.find(card => card.id === 'econ-2022-hl-q16-c-i')!;
    if (floor.kind !== 'question') throw new Error('Expected question');
    expect(floor.rows[0].verbatim).toBe('Fully labelled diagram');
    expect(floor.rows[1].contextNote).toContain('quantity demanded falls');
  });

  it('keeps Irish organisation and graph labels in revealed guidance', () => {
    for (const [id, wording] of [
      ['econ-2022-ol-sa-q2-i', 'POS stands for Príomhoifig Staidrimh'],
      ['econ-2022-ol-q11-b-ii', 'average cost is Co₁'],
      ['econ-2022-ol-q12-a-i', 'follow the question paper’s P₁/C₁ labels'],
      ['econ-2022-ol-q12-b-iii', 'new quantity C₂'],
    ]) {
      const card = ORDINARY.find(value => value.id === id)!;
      if (card.kind !== 'question') throw new Error('Expected question');
      expect(card.rows[0].contextNote, id).toContain(wording);
      expect(card.additionalSourceMaterials?.[0].presentationNote, id).not.toContain(wording);
    }
  });

  it.skipIf(!canReadSecSources)('scans Irish instructions and refuses a falsely equivalent edition', () => {
    const script = `
import copy, sys
sys.path.insert(0, 'scripts/markbank/authoring')
from econ_review import DIRECTIVE, reviewed_papers, validate_review, validate_equivalences
for text in ['Freagair cúig cheist', 'Roghnaigh dhá cheann', 'ceann amháin de na roghanna', 'Aontaím nó ní aontaím', 'cé acu', 'Ar chóir', 'Ba chóir: Níor chóir']:
    assert DIRECTIVE.search(text), text
assert not DIRECTIVE.search('Stáit Aontaithe'), 'United States is not an agreement choice'
indexed, reviewed = reviewed_papers()
key = (2022, 'ordinary', 'iv', 'LC034GLP000IV')
altered = copy.deepcopy(reviewed[key])
altered['selections'].pop()
try: validate_review(altered, indexed[key])
except ValueError: pass
else: raise AssertionError('accepted unclassified Irish directive')
for mutation in ['marks', 'missing-question', 'missing-task', 'reason', 'circular']:
    changed = copy.deepcopy(reviewed)
    edition = changed[key]
    if mutation == 'marks': edition['questions'][0]['tasks'][0]['marks'] += 1
    if mutation == 'missing-question': edition['questions'].pop()
    if mutation == 'missing-task': edition['questions'][0]['tasks'].pop()
    if mutation == 'reason': edition['questions'][0]['equivalenceReason'] = ''
    if mutation == 'circular': edition['equivalentTo'] = {'lang': 'iv', 'fileid': 'LC034GLP000IV'}
    try: validate_equivalences(changed)
    except ValueError: continue
    raise AssertionError('accepted false equivalence: ' + mutation)
print('Irish directive and five false equivalences rejected')
`;
    expect(execFileSync('python3', ['-c', script], { encoding: 'utf8' }).trim())
      .toBe('Irish directive and five false equivalences rejected');
  });

  it.skipIf(!canReadSecSources)('rejects incorrect cross-edition tariff evidence', () => {
    const script = `
import copy, sys
sys.path.insert(0, 'scripts/markbank/authoring')
from econ_review import reviewed_papers, validate_equivalences
_, reviewed = reviewed_papers()
for mutation in ['file', 'page', 'reason']:
    changed = copy.deepcopy(reviewed)
    evidence = changed[(2022, 'higher', 'iv', 'LC034ALP000IV')]['questions'][4]['allocationEvidence']
    if mutation == 'file': evidence['fileid'] = 'LC034GLP000EV'
    if mutation == 'page': evidence['schemePages'] = [48]
    if mutation == 'reason': evidence['reason'] = ''
    try: validate_equivalences(changed)
    except ValueError: continue
    raise AssertionError('accepted allocation evidence: ' + mutation)
print('three invalid allocation references rejected')
`;
    expect(execFileSync('python3', ['-c', script], { encoding: 'utf8' }).trim())
      .toBe('three invalid allocation references rejected');
  });

  it('refuses to publish when a later build gate drops a reviewed task', () => {
    const script = `
import fs from 'node:fs';
import { assertEconomicsReviewCoverage } from './scripts/markbank/economicsEditions.mjs';

const review = JSON.parse(fs.readFileSync('scripts/markbank/authoring/reviews/economics-2022-hl-ev.json'));
const ids = new Set(review.questions.flatMap(q => q.tasks.map(t => t.cardId)));
assertEconomicsReviewCoverage(ids, [review]);
ids.delete('econ-2022-hl-q15-a-iii');
try { assertEconomicsReviewCoverage(ids, [review]); }
catch (error) {
  if (!error.message.includes('econ-2022-hl-q15-a-iii')) throw error;
  console.log('dropped reviewed task rejected');
  process.exit(0);
}
throw new Error('Accepted incomplete generated deck');
`;
    expect(execFileSync('node', ['--input-type=module', '-e', script], { encoding: 'utf8' }).trim())
      .toBe('dropped reviewed task rejected');
  });

  it('keeps the full sustainable-business example pool without importing the next question', () => {
    const card = ORDINARY.find(value => value.id === 'econ-2022-ol-q12-c-ii')!;
    if (card.kind !== 'question') throw new Error('Expected question');
    expect(card.rows[0].group?.claimMax).toBe(2);
    expect(card.rows[0].group?.options).toHaveLength(8);
    expect(card.rows[0].group?.options.some(value => value.startsWith('Packaging:'))).toBe(true);
    expect(card.rows[0].group?.options.join(' ')).not.toContain('Expenditure');
    for (const id of ['econ-2022-ol-seca-q9-i', 'econ-2022-ol-q13-a-i-percentage']) {
      expect(ORDINARY.find(value => value.id === id)?.figure?.solution, id).toBe(true);
    }
    const meaning = ORDINARY.find(value => value.id === 'econ-2022-ol-q13-b-iii')!;
    if (meaning.kind !== 'question') throw new Error('Expected question');
    expect(meaning.rows[0].verbatim).toContain('increase by €2');
    expect(meaning.rows[0].verbatim).not.toContain('will double');
  });

  it('matches all 82 independently counted 2025 Higher routes, tariffs, sources and Atlas topics', () => {
    const cards = CARDS.filter(c => c.year === 2025);
    const tasks = higher2025Review.questions.flatMap(q => q.tasks);
    expect(tasks).toHaveLength(82);
    expect(cards.map(c => c.id).sort()).toEqual(tasks.map(t => t.cardId).sort());
    expect(cards.filter(c => c.section === 'A')).toHaveLength(24);
    // One route per printed choice: (b) OR (c) in Section A, one side of each tick in Section B.
    const alternative = (n: string, key: string) => (Number(n) <= 10 && /^c/.test(key))
      || /\/(?:disagree|gdp|sport)$/.test(key);
    for (const q of higher2025Review.questions) {
      const nodes = examTopicIdsForQuestion('economics', 'higher', 2025, 'main', q.n, 'single', 'ev')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const t of q.tasks) {
        const c = cards.find(card => card.id === t.cardId)!;
        expect(c.totalMarks, c.id).toBe(t.marks);
        expect(c.topicId, c.id).toBe(t.topicId);
        expect(c.sourceMaterial?.pages, c.id).toEqual(q.paperPages);
        expect(c.paperFileid, c.id).toBe('LC034ALP000EV');
        expect(nodes, c.id).toContain(t.topicId);
      }
      const once = q.tasks.filter(t => !alternative(q.n, t.key)).reduce((sum, t) => sum + t.marks, 0);
      // The scheme prints 6 for each required heading of Q1(a) and Q4(b).
      expect(once, `2025 Q${q.n}`).toBe(Number(q.n) > 10 ? 75 : ['1', '4'].includes(q.n) ? 18 : 12);
    }
  });

  it('keeps 2025 Higher required headings together and saved progress on the combined card', () => {
    const card = (s: string) => CARDS.find(c => c.id === `econ-2025-hl-${s}`)!;
    for (const [kept, withdrawn, marks] of [
      ['sa-q1-a-for', 'sa-q1-a-against', [6, 6]], ['sa-q4-b-gov', 'sa-q4-b-cons', [6, 6]],
      ['q11-b-iii-adv', 'q11-b-iii-dis', [4, 4]], ['q12-a-ii-tax', 'q12-a-ii-gov', [7, 7]],
      ['q12-c-i-employee', 'q12-c-i-employer', [7, 7]], ['q13-a-ii-benefit', 'q13-a-ii-challenge', [7, 7]],
    ] as const) {
      expect(card(kept).rows.map(r => r.marks), kept).toEqual(marks);
      expect(CARD_ID_ALIASES[`econ-2025-hl-${withdrawn}`]).toBe(`econ-2025-hl-${kept}`);
      expect(CARDS.some(c => c.id === `econ-2025-hl-${withdrawn}`), withdrawn).toBe(false);
    }
    expect(CARD_ID_ALIASES['econ-2025-hl-sa-q4-a-bad']).toBe('econ-2025-hl-sa-q4-a-good');
    expect(card('sa-q4-a-good').tariffModel.kind).toBe('questionTotal');
    expect(card('sa-q4-a-good').rows.map(r => r.id)).toEqual(['r-trend', 'r-beneficial']);
    expect(card('q14-c-ii-positive').rows.map(r => r.marks)).toEqual([6, 6]);
    expect(card('q12-b-i').rows.map(r => r.marks)).toEqual([6, 6]);
  });

  it('splits 2025 Higher drawings and calculations only where the scheme prices them apart', () => {
    const card = (s: string) => CARDS.find(c => c.id === `econ-2025-hl-${s}`)!;
    for (const [first, second, a, b] of [
      ['q11-b-i', 'q11-b-i-explanation', 12, 9], ['q14-b-ii', 'q14-b-ii-meaning', 9, 5],
      ['q16-b-ii', 'q16-b-ii-explanation', 8, 8],
    ] as const) {
      expect(card(first).totalMarks, first).toBe(a);
      expect(card(second).totalMarks, second).toBe(b);
    }
    expect(card('q14-b-i').rows.map(r => r.marks)).toEqual([2, 6, 6, 3]);
    expect(card('q16-b-ii').rows.map(r => r.marks)).toEqual([3, 3, 1, 1]);
    for (const s of ['q16-b-i-diseconomies', 'q16-c-ii', 'q12-a-i-gdp']) expect(card(s), s).toBeDefined();
    // Objective ticks stay one card: the scheme credits one answer only.
    for (const [s, answer] of [['sa-q4-c', 'Cost-push'], ['q12-a-iii', 'GNI*'], ['q12-b-ii', 'REGRESSIVE']] as const) {
      expect(JSON.stringify(card(s).rows), s).toContain(answer);
    }
    for (const [prefix, sides, marks] of [
      ['sa-q2-c', ['agree', 'disagree'], 6], ['q12-b-iii', ['agree', 'disagree'], 8],
      ['q14-a-iii', ['agri', 'sport'], 5], ['q15-a-i', ['agree', 'disagree'], 7],
      ['q15-a-i-cash', ['agree', 'disagree'], 6], ['q15-b-iii', ['agree', 'disagree'], 5],
    ] as const) {
      for (const side of sides) expect(card(`${prefix}-${side}`).totalMarks, `${prefix}-${side}`).toBe(marks);
    }
    expect(card('q12-a-i').totalMarks).toBe(6);
    expect(card('q15-a-i-agree').questionRef).toBe('2025 HL Q14(c)(i) — agree');
    expect(card('q16-b-i').questionRef).toBe('2025 HL Q16(c)(i)');
    expect(card('q16-c').questionRef).toBe('2025 HL Q16(c)(iii)');
  });

  it('hides 2025 Higher solutions until reveal and shows the whole printed question where it replaces the ask', () => {
    const card = (s: string) => CARDS.find(c => c.id === `econ-2025-hl-${s}`)!;
    const crops = [['seca-q6-b', 'p08-q6b'], ['q11-a-i', 'p13-q11ai'], ['q13-a-i', 'p21-q13ai'],
      ['q14-b-i', 'p26-q14bi'], ['q15-b-i', 'p30-q15bi'], ['q16-a-i', 'p33-q16ai'],
      ['q16-b-ii', 'p34-q16bii'], ['q16-b-ii-explanation', 'p34-q16bii']] as const;
    for (const [s, crop] of crops) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).questionFigure?.src, s).toContain(`economics-2025-HL-paper-${crop}-question.png`);
    }
    for (const s of ['seca-q2-a', 'q11-b-i', 'q11-b-i-explanation', 'q14-b-ii', 'seca-q5-b']) {
      expect(card(s).figure?.solution, s).toBe(true);
    }
    for (const c of CARDS.filter(item => item.year === 2025 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
    }
    const text = CARDS.filter(c => c.year === 2025).map(c => JSON.stringify(c)).join('\n');
    for (const broken of ['Ireland’s GD ', 'Ireland’s OD ', '( IB)', 'cluster e ect', 'nowledge Development Box ( DB)', '✓✓']) {
      expect(text, broken).not.toContain(broken);
    }
  });

  it('matches all 69 independently counted 2025 Ordinary routes, tariffs, sources and Atlas topics', () => {
    const cards = ORDINARY.filter(c => c.year === 2025);
    const tasks = ordinary2025Review.questions.flatMap(q => q.tasks);
    expect(tasks).toHaveLength(69);
    expect(cards.map(c => c.id).sort()).toEqual(tasks.map(t => t.cardId).sort());
    expect(cards.filter(c => c.section === 'A')).toHaveLength(20);
    // One route per printed choice: (a) OR (b) in Section A and one side of each tick.
    const alternative = (n: string, key: string) => (Number(n) <= 10 && /^b/.test(key) && ['2', '3', '4'].includes(n))
      || /\/(?:no|social|disagree|employers|mr|negative)$/.test(key);
    for (const q of ordinary2025Review.questions) {
      const nodes = examTopicIdsForQuestion('economics', 'ordinary', 2025, 'main', q.n, 'single', 'ev')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const t of q.tasks) {
        const c = cards.find(card => card.id === t.cardId)!;
        expect(c.totalMarks, c.id).toBe(t.marks);
        expect(c.topicId, c.id).toBe(t.topicId);
        expect(c.sourceMaterial?.pages, c.id).toEqual(q.paperPages);
        expect(c.paperFileid, c.id).toBe('LC034GLP000EV');
        expect(nodes, c.id).toContain(t.topicId);
      }
      const once = q.tasks.filter(t => !alternative(q.n, t.key)).reduce((sum, t) => sum + t.marks, 0);
      expect(once, `2025 OL Q${q.n}`).toBe(Number(q.n) > 10 ? 75 : 12);
    }
  });

  it('keeps 2025 Ordinary jointly priced answers whole and expands its finite routes', () => {
    const card = (s: string) => ORDINARY.find(c => c.id === `econ-2025-ol-${s}`)!;
    for (const [kept, withdrawn, marks] of [
      ['sa-q6-private', 'sa-q6-social', 12], ['seca-q8-i-ticks', 'sa-q8-ii', 12], ['q16-b-i-ag', 'q16-b-i-ind', 18],
    ] as const) {
      expect(card(kept).totalMarks, kept).toBe(marks);
      expect(CARD_ID_ALIASES[`econ-2025-ol-${withdrawn}`]).toBe(`econ-2025-ol-${kept}`);
      expect(ORDINARY.some(c => c.id === `econ-2025-ol-${withdrawn}`), withdrawn).toBe(false);
    }
    expect(card('q16-b-i-ag').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    for (const s of ['sa-q6-private', 'seca-q8-i-ticks', 'q11-c-ii', 'q12-c-iii', 'q15-a-i']) {
      expect(card(s).tariffModel.kind, s).toBe('questionTotal');
    }
    // "Any three of the following four labels": one card, all four labels, claim three.
    const labels = ORDINARY.filter(c => c.year === 2025 && c.questionRef.startsWith('2025 OL Q11(b)(i)'));
    expect(labels.map(c => c.id)).toEqual(['econ-2025-ol-q11-b-i']);
    expect(labels[0].totalMarks).toBe(24);
    expect(labels[0].tariffModel).toMatchObject({ kind: 'bestNofParts', answer: 3, ofParts: 4, perPart: 8 });
    expect(labels[0].rows[0].group?.claimMax).toBe(3);
    expect(labels[0].rows[0].group?.options).toHaveLength(4);
    for (const [prefix, sides, marks] of [
      ['sa-q2-a', ['yes', 'no'], 12], ['sa-q3-a', ['private', 'social'], 12], ['sa-q3-b', ['agree', 'disagree'], 12],
      ['q13-a-iii', ['gov', 'emp'], 7], ['q14-b-i', ['positive', 'negative'], 16], ['q15-b-iii', ['pos', 'neg'], 6],
    ] as const) {
      for (const side of sides) expect(card(`${prefix}-${side}`).totalMarks, `${prefix}-${side}`).toBe(marks);
    }
    expect(card('q13-b-ii').totalMarks).toBe(6);
    expect(card('q13-b-ii-mr').totalMarks).toBe(6);
    expect(card('q11-b-iii').totalMarks).toBe(4);
    expect(card('q11-c-i').totalMarks).toBe(10);
    expect(card('q13-c-i').totalMarks).toBe(12);
    expect(card('q13-c').questionRef).toBe('2025 OL Q13(c)(ii)');
    expect(card('q14-c').questionRef).toBe('2025 OL Q14(b)(ii)');
    // One-answer ticks stay one card.
    for (const [s, answer] of [['sa-q4-b', 'YES'], ['q12-a-ii', 'CAPITAL'], ['q14-c-i', 'IMPROVED'],
      ['q15-a-ii', 'AGREE'], ['q16-a-i', 'INDIRECT']] as const) {
      expect(JSON.stringify(card(s).rows), s).toContain(answer);
    }
  });

  it('hides 2025 Ordinary solutions until reveal and prints the whole question where it replaces the ask', () => {
    const card = (s: string) => ORDINARY.find(c => c.id === `econ-2025-ol-${s}`)!;
    for (const [s, crop] of [['seca-q7-i', 'p08-q7i'], ['seca-q8-i-ticks', 'p09-q8'], ['seca-q9-ticks', 'p09-q9'],
      ['q11-b-ii', 'p12-q11bii'], ['q12-a-i', 'p14-q12ai'], ['q13-b-i', 'p18-q13bi'], ['q15-b-i', 'p24-q15bi']] as const) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).questionFigure?.src, s).toContain(`economics-2025-OL-paper-${crop}-question.png`);
    }
    expect(card('q12-b-ii').figure?.solution).toBe(true);
    for (const c of ORDINARY.filter(item => item.year === 2025 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
    }
    for (const s of ['sa-q1-ii', 'sa-q7-ii', 'q14-b-i-positive', 'q16-b-ii', 'q11-b-iii']) {
      expect(card(s).figure?.src, s).toContain('-paper-');
      expect(card(s).figure?.solution, s).toBeUndefined();
    }
    const text = ORDINARY.filter(c => c.year === 2025).map(c => JSON.stringify(c)).join('\n');
    for (const junk of ['Possible Responses', 'continue on the next page', '1st@ 8', '2nd @ 4', '____']) {
      expect(text, junk).not.toContain(junk);
    }
  });

  it('matches all 90 independently counted 2026 Higher routes, tariffs, sources and Atlas topics', () => {
    const cards = CARDS.filter(c => c.year === 2026);
    const tasks = higher2026Review.questions.flatMap(q => q.tasks);
    expect(tasks).toHaveLength(90);
    expect(cards.map(c => c.id).sort()).toEqual(tasks.map(t => t.cardId).sort());
    expect(cards.filter(c => c.section === 'A')).toHaveLength(28);
    expect(new Set(cards.map(c => c.questionRef)).size).toBe(90);
    // One route per printed choice: the stance or alternative counted once.
    const alternative = /\/(?:disagree|streaming|irrational|tax|no|exports|challenge|option-b|widen)$|^c$/;
    for (const q of higher2026Review.questions) {
      const nodes = examTopicIdsForQuestion('economics', 'higher', 2026, 'main', q.n, 'single', 'ev')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const t of q.tasks) {
        const c = cards.find(card => card.id === t.cardId)!;
        expect(c.totalMarks, c.id).toBe(t.marks);
        expect(c.topicId, c.id).toBe(t.topicId);
        expect(c.sourceMaterial?.pages, c.id).toEqual(q.paperPages);
        expect(c.paperFileid, c.id).toBe('LC034ALP000EV');
        expect(nodes, c.id).toContain(t.topicId);
      }
      const once = q.tasks.filter(t => !alternative.test(t.key)).reduce((sum, t) => sum + t.marks, 0);
      expect(once, `2026 Q${q.n}`).toBe(Number(q.n) > 10 ? 75 : 12);
    }
  });

  it('expands every printed 2026 Higher either/or choice into full-tariff routes', () => {
    const route = (s: string) => CARDS.find(c => c.id === `econ-2026-hl-${s}`)!;
    for (const [prefix, sides, marks] of [
      ['sa-q2-a', ['events', 'streaming'], 6], ['sa-q3-a', ['agree', 'disagree'], 6],
      ['sa-q5-a', ['rational', 'irrational'], 6], ['sa-q7-a', ['subsidy', 'tax'], 6],
      ['sa-q7-b', ['yes', 'no'], 6], ['q11-c-ii', ['agree', 'disagree'], 6],
      ['q12-a-i', ['imports', 'exports'], 4], ['q12-a-ii', ['benefit', 'challenge'], 8],
      ['q12-c-ii', ['option-a', 'option-b'], 6], ['q13-c-iii', ['agree', 'disagree'], 5],
      ['q14-b-iii', ['agree', 'disagree'], 5], ['q15-b-iii', ['agree', 'disagree'], 6],
      ['q15-c-iii', ['narrow', 'widen'], 6],
    ] as const) {
      const cards = sides.map(side => route(`${prefix}-${side}`));
      expect(cards.every(c => c?.totalMarks === marks), prefix).toBe(true);
      expect(new Set(cards.map(c => c.questionText)).size, prefix).toBe(2);
      expect(new Set(cards.map(c => c.questionRef)).size, prefix).toBe(2);
    }
    // Section A (b) OR (c) alternatives are separate tasks at their own tariffs.
    for (const q of ['2', '3', '4']) {
      expect(route(`sa-q${q}-b`).totalMarks).toBe(6);
      expect(route(`sa-q${q}-c`).totalMarks).toBe(6);
    }
  });

  it('keeps 2026 Higher required headings together and splits only separately priced boundaries', () => {
    const card = (s: string) => {
      const c = CARDS.find(item => item.id === `econ-2026-hl-${s}`)!;
      if (c.kind === 'question' || c.kind === 'diagram') return c;
      throw new Error('unexpected card kind');
    };
    for (const [s, marks] of [
      ['q11-b-ii', [4, 4]], ['q12-b-iii', [6, 6]], ['q12-c-iii', [5, 5]], ['q13-b-i', [6, 6]],
      ['q13-c-i', [5, 5]], ['q14-a-iii', [5, 5]], ['q15-a-i', [6, 6]], ['q15-c-i', [5, 2, 2]],
      ['q15-c-ii', [6, 6]], ['q16-c-iii', [6, 6]], ['sa-q6-a', [3, 3]], ['q14-b-ii', [4, 8]],
    ] as const) {
      expect(card(s).rows.map(r => r.marks), s).toEqual(marks);
    }
    for (const [diagram, explanation, a, b] of [
      ['q11-b-i', 'q11-b-i-explanation', 12, 9], ['q11-c-i', 'q11-c-i-meaning', 7, 5],
      ['q12-c-i', 'q12-c-i-influence', 7, 4],
    ] as const) {
      expect(card(diagram).totalMarks).toBe(a);
      expect(card(explanation).totalMarks).toBe(b);
    }
    for (const s of ['sa-q9-a', 'q11-c-iii', 'q12-c-i', 'q13-b-iii', 'q14-a-i', 'q14-b-i',
      'q14-c-i', 'q14-c-ii', 'q14-c-iii', 'q16-b-i']) {
      expect(card(s).tariffModel.kind, s).toBe('questionTotal');
      expect(card(s).rows.every(r => r.marks === null), s).toBe(true);
    }
  });

  it('hides every 2026 Higher drawing and fraction working until reveal and shows the paper visuals first', () => {
    const card = (s: string) => CARDS.find(c => c.id === `econ-2026-hl-${s}`)!;
    for (const s of ['q11-b-i', 'q11-b-i-explanation', 'q11-c-i', 'q12-c-i', 'q13-b-ii', 'q14-c-i',
      'q14-c-ii', 'q14-c-iii', 'q16-a-i', 'q16-b-i', 'q16-c-ii']) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).figure?.src, s).toContain('-scheme-');
    }
    // A question crop REPLACES the typed stem and ask, so the paper's data rides
    // beneath them as the figure; only a card whose figure slot holds its solution
    // takes a question crop, and that crop is the whole printed question.
    for (const s of ['sa-q3-a-agree', 'sa-q4-a', 'sa-q7-b-no', 'sa-q9-a', 'sa-q10-b', 'q11-a-i',
      'q12-a-i-exports', 'q12-c-i-influence', 'q13-a-i', 'q13-b-iii', 'q14-b-i', 'q15-a-i', 'q15-c-i']) {
      expect(card(s).figure?.src, s).toContain('-paper-');
      expect(card(s).figure?.solution, s).toBeUndefined();
      expect(card(s).questionFigure, s).toBeUndefined();
    }
    for (const [s, crop] of [['q12-c-i', 'p20-q12ci-question'], ['q13-b-ii', 'p23-q13bii-question'],
      ['q16-a-i', 'p34-q16ai-question'], ['q16-b-i', 'p35-q16bi-question'],
      ['q16-c-ii', 'p36-q16cii-question']] as const) {
      expect(card(s).questionFigure?.src, s).toContain(`economics-2026-HL-paper-${crop}.png`);
      expect(card(s).questionFigure?.alt, s).toContain('The ask reads:');
    }
    const ppf = card('q16-c-i');
    expect(ppf.kind).toBe('diagram');
    expect(ppf.figure?.solution).toBeUndefined();
    expect(ppf.labelKey?.map(k => k.letter)).toEqual(['A', 'B']);
  });

  it('opens every 2026 Higher Q1(b) characteristic with its own heading', () => {
    const options = CARDS.find(c => c.id === 'econ-2026-hl-sa-q1-b')!.rows[0].group!.options;
    expect(options.map(o => o.split(' Early 1950s')[0])).toEqual([
      'Types of goods and services exported', 'Trading partners / Foreign market concentration',
      'Ireland’s trade policy / EU membership', 'Role of multinational corporations (MNCs)',
      'Size of international trade', 'Trade balances']);
    for (const o of options) expect(o).toContain(' Present day');
  });

  it('repairs the 2026 scheme glyphs the text layer reads as spaces', () => {
    const text = CARDS.filter(c => c.year === 2026).map(c => JSON.stringify(c)).join('\n');
    for (const broken of ['G P', '€15 .4', '€18,0 9m', '€2 , m', 'In reases', 'rene able', ' ublin']) {
      expect(text, broken).not.toContain(broken);
    }
    const card = (s: string) => {
      const c = CARDS.find(item => item.id === `econ-2026-hl-${s}`)!;
      if (c.kind !== 'question') throw new Error('Expected question');
      return c;
    };
    expect(card('q14-a-i').rows[1].verbatim).toContain('€153.4bn');
    expect(card('q12-a-i-exports').rows[0].verbatim).toContain('€23,333m');
    expect(card('q12-a-ii-benefit').rows[0].group?.options.join(' ')).toContain('Increases Ireland’s international reputation');
    expect(card('q14-a-ii').rows[0].group?.options.filter(o => o.includes('Ireland’s GDP')).length).toBeGreaterThan(4);
  });

  it('matches all 74 independently counted 2026 Ordinary routes, tariffs, sources and Atlas topics', () => {
    const cards = ORDINARY.filter(c => c.year === 2026);
    const tasks = ordinary2026Review.questions.flatMap(q => q.tasks);
    expect(tasks).toHaveLength(74);
    expect(cards.map(c => c.id).sort()).toEqual(tasks.map(t => t.cardId).sort());
    expect(cards.filter(c => c.section === 'A')).toHaveLength(20);
    expect(new Set(cards.map(c => c.questionRef)).size).toBe(74);
    // One route per printed choice; Section A (a)/(b) alternatives counted once.
    const alternative = /\/(?:social|retailers|government|disadvantage|disagree|negative|economy|no|employer)$|^(?:disadvantage|disagree)$/;
    for (const q of ordinary2026Review.questions) {
      const nodes = examTopicIdsForQuestion('economics', 'ordinary', 2026, 'main', q.n, 'single', 'ev')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const t of q.tasks) {
        const c = cards.find(card => card.id === t.cardId)!;
        expect(c.totalMarks, c.id).toBe(t.marks);
        expect(c.topicId, c.id).toBe(t.topicId);
        expect(c.sourceMaterial?.pages, c.id).toEqual(q.paperPages);
        expect(c.paperFileid, c.id).toBe('LC034GLP000EV');
        expect(nodes, c.id).toContain(t.topicId);
      }
      const once = q.tasks.filter(t => !alternative.test(t.key)
        && !(['2', '3', '4'].includes(q.n) && /^b/.test(t.key))).reduce((sum, t) => sum + t.marks, 0);
      expect(once, `2026 OL Q${q.n}`).toBe(Number(q.n) > 10 ? 75 : 12);
    }
  });

  it('expands every printed 2026 Ordinary either/or choice and keeps objective ticks as one card', () => {
    const route = (s: string) => ORDINARY.find(c => c.id === `econ-2026-ol-${s}`)!;
    for (const [prefix, sides, marks] of [
      ['sa-q2-a', ['private', 'social'], 12], ['sa-q2-b', ['government', 'retailers'], 12],
      ['sa-q4-b', ['advantage', 'disadvantage'], 12], ['sa-q5', ['advantage', 'disadvantage'], 12],
      ['sa-q8', ['agree', 'disagree'], 12], ['q11-c-ii', ['agree', 'disagree'], 6],
      ['q13-a-ii', ['positive', 'negative'], 3], ['q13-b-i', ['households', 'economy'], 8],
      ['q13-b-iii', ['agree', 'disagree'], 8], ['q14-a-ii', ['yes', 'no'], 10],
      ['q14-b-i', ['employee', 'employer'], 12], ['q15-a-ii', ['agree', 'disagree'], 8],
    ] as const) {
      const cards = sides.map(side => route(`${prefix}-${side}`));
      expect(cards.every(c => c?.totalMarks === marks), prefix).toBe(true);
      expect(new Set(cards.map(c => c.questionText)).size, prefix).toBe(2);
    }
    // The scheme ticks one answer only: no invented opposite route.
    expect(route('sa-q4-a').totalMarks).toBe(12);
    expect(ORDINARY.some(c => c.id.startsWith('econ-2026-ol-sa-q4-a-'))).toBe(false);
    expect(route('q11-a-i').rows.map(r => r.marks)).toEqual([4, 5]);
    expect(route('q11-a-i').rows[0].verbatim).toBe('YES');
    // Q13(a)(ii): the trend and the opinion are separately priced.
    expect(route('q13-a-ii').totalMarks).toBe(12);
  });

  it('keeps 2026 Ordinary required pairs whole and shows the paper visuals and solutions', () => {
    const card = (s: string) => {
      const c = ORDINARY.find(item => item.id === `econ-2026-ol-${s}`)!;
      if (c.kind === 'question' || c.kind === 'diagram') return c;
      throw new Error('unexpected card kind');
    };
    for (const s of ['sa-q1-i', 'sa-q1-ii', 'sa-q6', 'sa-q7', 'sa-q9', 'sa-q10-i', 'sa-q10-ii', 'q11-a-ii', 'q15-b-iii']) {
      expect(card(s).tariffModel.kind, s).toBe('questionTotal');
      expect(card(s).rows.every(r => r.marks === null), s).toBe(true);
    }
    for (const [s, marks] of [['q11-b-i', [8, 8, 8]], ['q11-c-i', [8, 8]], ['q15-a-i', [8, 8]],
      ['q15-c-i', [7, 4]], ['q15-c-ii', [6, 6]]] as const) {
      expect(card(s).rows.map(r => r.marks), s).toEqual(marks);
    }
    expect(card('sa-q7').rows.map(r => r.contextNote)).toEqual([
      'B. Certainty matches explanation 3.', 'C. Economy matches explanation 4.', 'D. Equity matches explanation 1.']);
    expect(card('q16-b-i').rows[0].group?.options).toEqual(['Land', 'Labour', 'Capital']);
    for (const s of ['q11-b-ii', 'q15-b-iii']) {
      expect(card(s).figure?.solution, s).toBe(true);
      expect(card(s).figure?.src, s).toContain('-scheme-');
    }
    for (const s of ['sa-q7', 'sa-q9', 'sa-q10-i', 'q11-b-i', 'q11-c-i', 'q13-a-ii', 'q14-a-ii-no', 'q14-b-iii']) {
      expect(card(s).figure?.src, s).toContain('-paper-');
      expect(card(s).figure?.solution, s).toBeUndefined();
      expect(card(s).questionFigure, s).toBeUndefined();
    }
    expect(card('q11-b-ii').questionFigure?.src).toContain('economics-2026-OL-paper-p12-q11bii-question.png');
  });

  it('never lets a 2026 question crop hide the typed ask unless the crop prints that ask', () => {
    for (const c of CARDS.filter(item => item.year === 2026 && item.questionFigure)) {
      expect(c.figure?.solution, c.id).toBe(true);
      expect(c.questionFigure?.src, c.id).toMatch(/-question\.png$/);
    }
  });
});
