import { describe, expect, it } from 'vitest';
import { audioMaterialFault, audioQuestionPaperFileid } from '../scripts/markbank/audioMaterial.mjs';

const card = (subject: 'japanese' | 'russian', year = 2026) => {
  const code = subject === 'japanese' ? '058' : '099';
  const secFileid = `LC${code}ZLP017BV.mp3`;
  const canonicalUrl = `https://www.examinations.ie/archive/exampapers/${year}/${secFileid}`;
  return { id: `${subject}-test`, year, level: 'higher', audioMaterial: {
    kind: 'source-audio', label: 'Listening', title: `${year} listening`,
    secFileid, canonicalUrl, playbackUrl: canonicalUrl,
    attribution: '© State Examinations Commission.', presentationNote: 'Full official recording.',
  } };
};

describe('generated point-card recordings', () => {
  it('binds both languages to the actual aural booklet rather than the written examination', () => {
    for (const subject of ['japanese', 'russian'] as const) {
      const c = card(subject);
      expect(audioMaterialFault(c, subject)).toBeNull();
      expect(audioQuestionPaperFileid(c, subject)).toBe(`LC${subject === 'japanese' ? '058' : '099'}ALPA00BV`);
    }
  });
  it('leaves cards without audio and existing embedded-audio subject resolution unchanged', () => {
    expect(audioQuestionPaperFileid({ year: 2026, level: 'higher' }, 'japanese')).toBeUndefined();
    expect(audioMaterialFault({ year: 2026, level: 'higher' }, 'japanese')).toBeNull();
    expect(audioQuestionPaperFileid(card('japanese'), 'irish')).toBeUndefined();
  });
  it('refuses a missing booklet, another subject, another year or the wrong sitting', () => {
    expect(audioMaterialFault(card('japanese', 2001), 'japanese')).toContain('Aural Paper');
    expect(audioMaterialFault(card('russian'), 'japanese')).toContain('different subject');
    expect(audioMaterialFault({ ...card('japanese'), year: 2025 }, 'japanese')).toContain('examination year');
    expect(audioMaterialFault({ ...card('japanese'), id: 'ja-2026-hl-deferred-test' }, 'japanese')).toContain('sitting');
  });
  it('refuses incomplete metadata and untrusted or mismatched canonical identities', () => {
    const c = card('russian');
    for (const patch of [{ kind: 'source-text' }, { label: '' }, { playbackUrl: 'javascript:alert(1)' },
      { canonicalUrl: c.audioMaterial.canonicalUrl.replace('www.examinations.ie', 'example.com') },
      { secFileid: 'LC099ZLP017EV.mp3' }]) {
      expect(audioMaterialFault({ ...c, audioMaterial: { ...c.audioMaterial, ...patch } }, 'russian')).not.toBeNull();
    }
  });
});
