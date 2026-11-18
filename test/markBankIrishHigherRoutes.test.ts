import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/irish/higher';
import authored from '../components/MarkBank/cards/irish/authored.json';
import reviews from '../scripts/markbank/authored/irish-higher-route-review.json';
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import { curriculumNodeIdsForExamTopic, examTopicIdsForQuestion } from '../data/examTopics/registry';
import { topicsForPaper } from '../components/PaperTrail/topics';
import { irishMarks } from '../components/MarkBank/SessionScreen';
import { resolveSibling, answerMapUrls } from '../components/PaperTrail/vaultResolve';
import { tariffReconciles } from '../types/markBank';
import { irishFullScores } from './fixtures/irishScores';

const byId = new Map(CARDS.map(card => [card.id,card]));
const routeIds = new Set(reviews.flatMap(review => review.cardIds));
const reviewed = authored.cards.filter(card => routeIds.has(card.id));

describe('visually reviewed Higher Irish prose and optional poetry routes', () => {
  it('keeps both prescribed works apart and one optional film-or-play card with both printed alternatives', () => {
    for (const year of [2022,2024]) {
      const base = `irish-${year}-hl-p2-`;
      const film = byId.get(base+'prose-2a-a')!;
      const drama = byId.get(base+'prose-2a-a-an-lasair-choille')!;
      expect(film.topicId).toBe('irish-4-6');
      expect(drama.topicId).toBe('irish-4-8');
      expect(film.questionText).toContain('Cáca Milis');
      expect(film.questionText).not.toContain('An Lasair Choille');
      expect(drama.questionText).toContain(year === 2022 ? 'chuairt Mhíoda' : 'Is siombail é Binncheol');
      expect(drama.questionText).not.toContain('Cáca Milis');
      // The optional film and the optional play share one grid and one Atlas heading (irish-4-7),
      // so the live 2B(a) card carries both printed alternatives (choose-one refinement).
      expect(byId.has(base+'prose-2b-a-drama')).toBe(false);
      const optionalA = byId.get(base+'prose-2b-a')!;
      for (const text of ['scannán roghnach', 'an scannáin', 'dráma roghnach', 'an dráma', 'hainm an scríbhneora']) {
        expect(optionalA.questionText).toContain(text);
      }
      expect(optionalA.questionRef).toBe(`${year} HL Paper 2 Prós 2B(a) · Scannán nó dráma roghnach`);
      expect(optionalA.totalMarks).toBe(30);
      expect(optionalA.rubric.system).toBe('irish');
      if (optionalA.rubric.system !== 'irish') throw new Error('Wrong rubric');
      expect(optionalA.rubric.taskRequirements.join(' ')).toContain('Níl cead');
      expect(optionalA.rubric.criteria.map(c => c.maxMarks)).toEqual(year === 2022 ? [25,5] : [2,23,5]);
      expect([film,drama].every(c => c.totalMarks === 30 && tariffReconciles(c))).toBe(true);
      const prescribedB = byId.get(base+'prose-2a-b')!;
      expect(prescribedB.questionText.startsWith(year === 2022 ? 'Hurlamaboc' : 'Dís')).toBe(true);
      expect(prescribedB.questionText).not.toContain('Cáca Milis');
      const optionalB = byId.get(base+'prose-2b-b')!;
      expect(optionalB.questionText.startsWith('Maidir')).toBe(true);
      expect(optionalB.questionText).not.toContain('scannán roghnach');
    }
  });

  it('keeps 2022 3B(a) as one card: the device (íomhánna, codarsnacht nó mothúcháin) is the student\'s choice inside one question', () => {
    // Decision 4 (2026-11-04): the three device cards were branch-only and are withdrawn; no aliases.
    expect(CARDS.filter(c => /^irish-2022-hl-p2-poetry-3b-a-/.test(c.id))).toEqual([]);
    const card = byId.get('irish-2022-hl-p2-poetry-3b-a')!;
    expect(card.questionText).toContain('íomhánna, codarsnacht nó mothúcháin');
    expect(card.questionText).toMatch(/\(i\).*\(ii\).*\(iii\)/);
    expect(card.questionText.startsWith('(a) (i)')).toBe(true);
    expect(card.questionText).not.toContain('An rogha don chárta seo');
    expect(card.totalMarks).toBe(30);
    if (card.rubric.system !== 'irish') throw new Error('Wrong rubric');
    expect(card.rubric.criteria.map(c => [c.id,c.maxMarks])).toEqual([
      ['eolas-i',13],['eolas-ii',5],['eolas-iii',7],['gaeilge',5],
    ]);
    expect(card.rubric.criteria[0].guidance.join(' ')).toContain('ar a laghad');
    expect(card.rubric.criteria[2].guidance.join(' ')).toContain('bronn 0 ar an mír ar fad');
    expect(irishMarks(card,irishFullScores(card))).toBe(30);
    const review = reviews.find(r => r.year === 2022)!;
    expect(review.withdrawnCardIds).toEqual(['irish-2022-hl-p2-poetry-3b-a-codarsnacht','irish-2022-hl-p2-poetry-3b-a-iomhanna','irish-2022-hl-p2-poetry-3b-a-mothuchain']);
  });

  it('joins all fourteen reviewed responses to exact Atlas task, topic and paper/scheme regions', () => {
    expect(reviewed).toHaveLength(14);
    for (const raw of reviewed) {
      if (!('atlasQuestionId' in raw) || !('reviewedPaperPages' in raw) || !('schemePages' in raw)) throw new Error('Missing reviewed identity');
      const card = byId.get(raw.id)!;
      if (/-prose-2b-|-poetry-3b-/.test(card.id)) {
        // Printed under the section heading, before (a): the card's lead-in, never a sentence of its last part.
        expect(card.stem).toMatch(/^Níl cead aon ábhar a bhaineann le (?:Prós|Filíocht) Ainmnithe a úsáid i bhfreagra ar an (?:bPrós|bhFilíocht) Roghnach\.$/);
        expect(card.questionText).not.toContain('Níl cead');
      }
      if (card.id.includes('-poetry-3b-')) {
        expect(card.questionText).not.toMatch(/thíos\. Níl cead|\(a\) nó \(b\)/);
        for (const part of ['i','ii','iii']) {
          expect(card.questionText.split(`(${part})`)).toHaveLength(2);
        }
      }
      const n = raw.atlasQuestionId as string;
      expect(card.specVersion).toBe(resolveCurriculumSpecification('irish',raw.year)!.id);
      const topics = examTopicIdsForQuestion('irish','higher',raw.year,'main',n,'p2','iv',raw.paperFileid+'.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic),card.id).toContain(raw.topicId);
      expect(topicsForPaper('irish',raw.year,'higher','iv',raw.paperFileid+'.pdf')?.q.find(q => q.n === n)?.primary).toBe(raw.topicId);
      const map = JSON.parse(readFileSync(`public/paper-answers/${raw.year}/${raw.paperFileid}.pdf.json`,'utf8'));
      const q = map.q.find((q: { n: string }) => q.n === n);
      expect(map.schemeFileid).toBe('LC001ALP000IV.pdf');
      expect(q.paperRegion.map((r: { p: number }) => r.p)).toEqual(raw.reviewedPaperPages);
      expect(q.region.map((r: { p: number }) => r.p)).toEqual(raw.schemePages);
      expect(q.label,card.id).toBe(card.questionRef.replace(/^\d{4} HL Paper 2 /,''));
      expect(q.practiceInstruction).toContain(q.label);
      if (n.startsWith('P-2A-')) expect(topics).toEqual(['irish-higher-prescribed-prose-archive']);
    }
  });

  it('serves partial verified scheme maps while preserving the unreviewed anchors', () => {
    for (const year of [2022,2024]) {
      const resolved = resolveSibling({subjectId:'irish',year,level:'higher',lang:'iv',paperKey:'p2',fileid:'LC001ALP200IV.pdf',n:'P-2A-a-an-lasair-choille'})!;
      expect(answerMapUrls(resolved)[0]).toBe(`/paper-answers/${year}/LC001ALP200IV.pdf.json`);
      const map = JSON.parse(readFileSync(`public/paper-answers/${year}/LC001ALP200IV.pdf.json`,'utf8'));
      // The twelve shipped reading anchors stay byte-identical; the literature questions the paper
      // prints (Ceist 2 Prós, Ceist 3 Filíocht, Ceist 4 Litríocht Bhreise) are added after them as the reviewed
      // tasks' parents (2022's Ceist 4 since its paper review, 2026-11-04).
      const legacy = map.q.filter((q: { n: string }) => /^\d+$/.test(q.n) && Number(q.n) <= 12)
        .map(({paperRegion: _paperRegion,schemeRegion: _schemeRegion,printOrder: _printOrder,...original}: Record<string, unknown>) => original);
      expect(legacy).toHaveLength(12);
      expect(map.q.filter((q: { n: string }) => /^\d+$/.test(q.n) && Number(q.n) > 12)
        .map((q: { n: string; label: string }) => [q.n, q.label]))
        .toEqual([['13', 'Ceist 2 · Prós'], ['14', 'Ceist 3 · Filíocht'], ['15', 'Ceist 4 · Litríocht Bhreise']]);
      for (const task of map.q.filter((q: { n: string }) => /^[PF]-/.test(q.n))) {
        expect(task.parentN, task.n).toBe(task.n.startsWith('P-') ? '13' : '14');
      }
      expect(createHash('sha256').update(JSON.stringify(legacy)).digest('hex')).toBe(year === 2022
        ? '1e563fe88d83be836a4a4d3d02b9fa50d8db754d0f2e59218720173f5c47fdef'
        : '59c189047fa108b5f2e66888a2557ae388efc65e48fda35fd7cd44070ccf589e');
      // 2022: ten until decision 4 withdrew the three 3B(a) device tasks, then nine once its paper review
      // joined 3A(a) and 3A(b) (2026-11-04).
      expect(map.q.filter((q: { n: string }) => /^[PF]-/.test(q.n))).toHaveLength(9);
      expect(map.q.some((q: { n: string }) => q.n === 'R-A')).toBe(false);
      const anchors = JSON.parse(readFileSync(`public/paper-anchors/${year}/LC001ALP200IV.pdf.json`,'utf8'));
      expect(anchors.paperOnly).toBe(1);
      expect(anchors.q.length).toBeGreaterThan(map.q.length);
      expect(reviews.find(r => r.year === year)?.scope).toContain(year === 2022 ? 'irish_higher_2022_p2.py' : 'full-paper status is recorded separately');
    }
  });
});
