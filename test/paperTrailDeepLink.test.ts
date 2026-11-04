import { describe, expect, it } from 'vitest';
import { resolvePaperDeepLink } from '../components/PaperTrail/paperDeepLink';

const read = (values: Record<string, string>) => (name: string) => values[name] ?? null;

describe('Paper Trail document links', () => {
  it('preserves the selected year, level, language and scheme side', () => {
    const result = resolvePaperDeepLink('accounting', read({
      year: '2025', level: 'ordinary', lang: 'iv', paper: 'LC032GLP000IV.pdf', side: 'scheme',
    }));
    expect(result?.entry).toMatchObject({ year: 2025, level: 'ordinary', lang: 'iv' });
    expect(result?.item.scheme?.f).toBe('LC032GLP000IV.pdf');
    expect(result?.side).toBe('scheme');
  });

  it('opens the paper by default and retains its answer map capability', () => {
    const result = resolvePaperDeepLink('accounting', read({
      year: '2026', level: 'higher', lang: 'ev', paper: 'LC032ALP000EV.pdf',
    }));
    expect(result?.side).toBe('paper');
    expect(result?.item.answers).toBe(1);
    expect(result?.item.scheme).toBeDefined();
  });

  it('rejects missing, mismatched and arbitrary document targets', () => {
    const identity = { year: '2026', level: 'higher', lang: 'ev', paper: 'LC032ALP000EV.pdf' };
    expect(resolvePaperDeepLink('accounting', read({ year: '2026' }))).toBeNull();
    expect(resolvePaperDeepLink('accounting', read({ ...identity, level: 'ordinary' }))).toBeNull();
    expect(resolvePaperDeepLink('accounting', read({ ...identity, paper: 'https://example.com/file.pdf' }))).toBeNull();
    expect(resolvePaperDeepLink('biology', read(identity))).toBeNull();
  });
});
