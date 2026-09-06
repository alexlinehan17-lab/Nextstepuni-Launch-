import { describe, expect, it } from 'vitest';
import { taggedSubjects } from '../components/PaperTrail/topics';
import {
  atlasSubjectIcon,
  hasAtlasSubjectIcon,
} from '../components/PaperTrail/subjectIcons';

describe('Topic Atlas subject icons', () => {
  it('gives every charted subject an intentional visual glyph', () => {
    const missing = taggedSubjects().filter(id => !hasAtlasSubjectIcon(id));
    expect(missing).toEqual([]);
  });

  it('keeps a discipline visually consistent across programmes', () => {
    expect(atlasSubjectIcon('english')).toBe(atlasSubjectIcon('jc-english'));
    expect(atlasSubjectIcon('engineering')).toBe(atlasSubjectIcon('lca-engineering'));
    expect(atlasSubjectIcon('spanish')).toBe(atlasSubjectIcon('jc-spanish'));
  });
});

