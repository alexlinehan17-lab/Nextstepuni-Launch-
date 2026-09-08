import { describe, expect, it } from 'vitest';
import { markAnswer, needed, squares, tokens } from '../components/landing/marking/marker';

describe('landing marker', () => {
  it('tokenises with light stemming and keeps formulae', () => {
    expect(tokens('The cells were digested')).toEqual(['the', 'cell', 'were', 'digest']);
    expect(tokens('Cx(H2O)y')).toEqual(['cx', 'h2o', 'y']);
  });
  it('earns a point when most content words are present', () => {
    const points = [{ id: 'a', verbatim: 'Oesophagus', marks: 3 }, { id: 'b', verbatim: 'Peristalsis (muscular contraction)', marks: 3 }];
    const r = markAnswer('A is the oesophagus and food moves by peristalsis', points);
    expect(r.hits.map(h => h.matched)).toEqual([true, true]);
    expect(r.earned).toBe(6);
    expect(squares(r)).toBe('\u{1F7E7}\u{1F7E7}');
  });
  it('misses when the answer says something else, and never on an empty answer', () => {
    const points = [{ id: 'a', verbatim: 'Stomach', marks: 3 }];
    expect(markAnswer('the small intestine', points).earned).toBe(0);
    expect(markAnswer('', points).hits[0].matched).toBe(false);
  });
  it('ignores sentence punctuation at the end of a word but keeps decimals', () => {
    expect(markAnswer('it is the cathode.', [{ id: 'c', verbatim: 'cathode', marks: 3 }]).earned).toBe(3);
    expect(markAnswer('The speed is 0.', [{ id: 'z', verbatim: '0', marks: 3, accept: [['0']] }]).earned).toBe(3);
    expect(tokens('about 3.5 m this.')).toEqual(['about', '3.5', 'm', 'thi']);
  });
  it('uses explicit accept alternatives when given', () => {
    const points = [{ id: 'f', verbatim: 'Cx(H2O)y', marks: 4, accept: [['cx', 'h2o', 'y'], ['cn', 'h2o', 'n']] }];
    expect(markAnswer('the formula is Cn(H2O)n', points).earned).toBe(4);
    expect(markAnswer('carbon and water', points).earned).toBe(0);
  });
  it('needs every token of a short line and three of five for a long one', () => {
    expect(needed(2)).toBe(2);
    expect(needed(5)).toBe(3);
    expect(needed(10)).toBe(6);
  });
});
