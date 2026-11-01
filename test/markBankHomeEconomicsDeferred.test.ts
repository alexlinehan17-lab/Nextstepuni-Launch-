import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import { reviewedHomeEconomicsSource, homeEconomicsSourceMap } from '../scripts/markbank/homeEconomicsSources.mjs';
import { resolveIndexedPaperFileid } from '../scripts/markbank/paperIndex.mjs';
import review from '../scripts/markbank/authoring/home-economics/2023-hl-deferred-review.json';
import anchors from '../scripts/paper-trail/answers/2023/LC098ALP014EV-deferred.pdf.json';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import { preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';

const cards = CARDS.filter(c => c.id.startsWith('he-2023-hl-deferred-sa-'));
const get = (suffix: string) => {
  const c = cards.find(c => c.id === `he-2023-hl-deferred-sa-${suffix}`);
  if (!c || c.kind !== 'question') throw new Error(suffix);
  return c;
};

describe('Home Economics deferred source boundaries', () => {
  it('separates the two gel tasks while preserving every other required or open response', () => {
    expect(cards).toHaveLength(15);
    expect(cards.reduce((n, c) => n + c.totalMarks, 0)).toBe(84);
    expect(get('q1').totalMarks).toBe(4);
    expect(get('q1-example').totalMarks).toBe(2);
    expect(get('q1-example').stem).toBe('In relation to proteins.');
    for (const c of cards) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.paperFileid).toBe('LC098ALP014EV-deferred');
      expect(c.schemeCitation).toContain('deferred examination');
    }
  });
  it('retains given table context, all six export sectors and exact partial-credit ladders', () => {
    expect(get('q2').questionText).toContain('Secretion: Pancreatic juice');
    expect(get('q2').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
    expect(get('q3').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 2]));
    expect(get('q6').rows).toHaveLength(3);
    expect(get('q6').rows[0].contextNote?.split('\n\n')).toHaveLength(7);
    expect(get('q6').rows[0].contextNote).toContain('Horticulture: Mushrooms; potatoes; vegetables; fruit.');
    expect(get('q6').rows[0].contextNote).toContain('Prepared consumer foods: Cooked meat; pizza; sauces; bakery; confectionary.');
    expect(get('q8').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 4], [0, 2]]);
    expect(get('q8').rows[0].contextNote).toContain('market value and/or a longer shelf life');
    expect(get('q10').rows[0].contextNote).toContain('access to funds');
    expect(get('q11').rows.map(r => r.permittedMarks)).toEqual(Array(2).fill([0, 2, 3]));
    expect(get('q12').rows[0].contextNote).toContain('“Current” refers to this 2023 examination');
    expect(get('q14').rows.map(r => r.verbatim)).toEqual(['Cause', 'Effect', 'Reduction measure']);
  });
  it('fails closed on a June archive, swapped component, changed bytes or undeclared task', () => {
    for (const kind of ['a', 'bc', 'scheme'] as const) {
      const bad = structuredClone(review);
      bad.sources[kind].path = bad.sources[kind].path.replace('deferredexams', 'exampapers').replace('deferredmarkingschemes', 'markingschemes');
      expect(() => homeEconomicsSourceMap(bad)).toThrow(/archive identity/);
    }
    const bad = structuredClone(review); bad.sources.a.fileid = bad.sources.bc.fileid;
    expect(() => homeEconomicsSourceMap(bad)).toThrow(/archive identity/);
    expect(() => homeEconomicsSourceMap(review, () => Buffer.from('wrong document'))).toThrow(/bytes differ/);
    expect(() => reviewedHomeEconomicsSource('he-2023-hl-deferred-sa-q99')).toThrow(/lacks reviewed sources/);
    expect(reviewedHomeEconomicsSource('he-2023-hl-sa-q1')).toBeUndefined();
    expect(resolveIndexedPaperFileid('home-economics', 2023, 'higher', reviewedHomeEconomicsSource(get('q1').id))).toBe('LC098ALP014EV-deferred');
    expect(() => resolveIndexedPaperFileid('home-economics', 2023, 'ordinary', reviewedHomeEconomicsSource(get('q1').id))).toThrow(/No unique indexed/);
  });
  it('maps every new task to its own deferred Atlas question and every canonical topic', () => {
    const file = 'LC098ALP014EV-deferred.pdf';
    const tags = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2023 && p.fileid === file)!;
    expect(tags).toBeDefined();
    expect(anchors.q).toHaveLength(14);
    expect(anchors.schemeFileid).toBe('LC098ALP000EV-deferred.pdf');
    expect(preferredAnswersUrl('home-economics-s-and-s', 2023, file, 'stale')).toBe(`/paper-answers/2023/${file}.json`);
    for (const c of cards) {
      const n = c.questionRef.match(/Q(\d+)/)![1];
      const row = runtime.questionMappings.find(r => r[0] === 'h' && r[1] === 'e' && r[2] === 2023 && r[4] === file && r[5] === n)!;
      expect(row, c.id).toBeDefined();
      const topics = (row[6] as number[]).map(i => runtime.topicIds[i]);
      const expected = Object.entries(crosswalk).filter(([k, nodes]) => k.includes('-higher-') && nodes.includes(c.topicId)).map(([k]) => k);
      expect(topics).toEqual(expect.arrayContaining(expected));
      const question = tags.q.find(q => q.n === n)!;
      expect(browseTopicIdsForQuestion(tags, question)).toEqual(expect.arrayContaining(expected));
    }
  });
});
