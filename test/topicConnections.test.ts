import { beforeEach, describe, expect, it } from 'vitest';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { attemptNs, allMarks, setMark } from '../components/PaperTrail/attemptStore';
import { browseTopicIdsForQuestion, topicsForSubject } from '../components/PaperTrail/topics';
import { masteryForSubject } from '../components/PaperTrail/topicMastery';
import { evidenceForCurriculumNode } from '../components/PaperTrail/topicEvidence';
import { resolveCurriculumSpecification, resolveSubjectId } from '../curriculumRegistry';
import { SUBJECTS, loadCards, levelsFor } from '../components/MarkBank/deck';
import { cardsForCurriculumNode, markBankCurriculumMenu } from '../components/MarkBank/curriculumMenu';
import { LC_SUBJECTS, JC_SUBJECTS } from '../components/subjectData';

beforeEach(() => localStorage.clear());
describe('topic connections', () => {
  it('makes the Accounting 2020 Q1 score visible in the actual Atlas rows', () => {
    const paper = PAPER_TOPIC_TAGS.find(item => item.subjectId === 'accounting' && item.year === 2020 && item.level === 'higher' && item.lang === 'ev' && item.q.some(question => question.n === '1'))!;
    const question = paper.q.find(item => item.n === '1')!;
    const browseIds = browseTopicIdsForQuestion(paper, question);
    const visibleIds = new Set(topicsForSubject('accounting').map(item => item.subtopicId));
    setMark(attemptNs('audit', paper.subjectId, paper.year, paper.level, paper.lang, paper.fileid), '1', { score: 8, max: 10, ts: 123 });
    expect(browseIds.length).toBeGreaterThan(0);
    expect(browseIds.every(id => visibleIds.has(id))).toBe(true);
    for (const id of browseIds) expect(masteryForSubject('audit', 'accounting').find(item => item.subtopicId === id)?.accuracy).toBe(80);
    const evidence = evidenceForCurriculumNode('audit', resolveCurriculumSpecification('Accounting', 2027)!);
    expect(evidence.marks).toHaveLength(1);
    expect(evidence.accuracy).toBe(80);
    expect(allMarks('audit')).toHaveLength(1);
  });
  it('consolidates subject choices without losing saved aliases', () => {
    expect(resolveSubjectId('Politics & Society')).toBe('politics-and-society');
    expect(resolveSubjectId('Design & Communication Graphics')).toBe('design-and-communication-graphics');
    expect(LC_SUBJECTS.filter(item => resolveSubjectId(item.name) === 'design-and-communication-graphics')).toHaveLength(1);
    for (const id of ['accounting', 'music', 'politics-and-society', 'physics-and-chemistry']) expect(SUBJECTS.some(subject => subject.id === id)).toBe(true);
    for (const name of ['Latin', 'Ancient Greek', 'Arabic', 'Climate Action and Sustainable Development', 'Drama, Film and Theatre Studies', 'Physics & Chemistry']) {
      expect(LC_SUBJECTS.some(item => item.name === name)).toBe(true);
      expect(resolveCurriculumSpecification(name, 2027)?.status).toBe('verified');
    }
    for (const name of ['Climate Action and Sustainable Development', 'Drama, Film and Theatre Studies']) expect(JC_SUBJECTS.some(item => item.name === name)).toBe(false);
  });
  it('keeps every Latin card accessible beside the 2027 syllabus menu', async () => {
    const cards = await loadCards('latin', 'higher');
    const menu = markBankCurriculumMenu('latin', 'higher', '2027-06-02', cards);
    expect(menu.spec?.id).toBe('latin:2027');
    expect(menu.strands.some(strand => strand.label === 'Original paper topics')).toBe(true);
    const reachable = new Set(menu.strands.flatMap(strand => strand.topics.flatMap(topic => cardsForCurriculumNode(topic.id, cards, menu.spec).map(card => card.id))));
    expect(reachable.size).toBe(cards.length);
  });
  it('keeps all original card IDs reachable in old and current cohort menus', async () => {
    for (const subject of SUBJECTS) {
      for (const level of levelsFor(subject.id)) {
        const cards = await loadCards(subject.id, level);
        for (const year of [2026, 2027, 2029]) {
          const menu = markBankCurriculumMenu(subject.id, level, `${year}-06-02`, cards);
          const reachable = new Set(menu.strands.flatMap(strand => strand.topics.flatMap(topic => cardsForCurriculumNode(topic.id, cards, menu.spec).map(card => card.id))));
          expect(cards.filter(card => !reachable.has(card.id)).map(card => card.id), `${subject.id}/${level}/${year}`).toEqual([]);
        }
      }
    }
  }, 120000);
  it('joins the Home Economics archive identity through its curriculum metadata', () => {
    const spec = resolveCurriculumSpecification('Home Economics', 2027)!;
    const evidence = evidenceForCurriculumNode('audit', spec, undefined, 'higher');
    expect(evidence.practiceSubjectId).toBe('home-economics-s-and-s');
    expect(evidence.topics.some(topic => topic.count > 0)).toBe(true);
  });

});
