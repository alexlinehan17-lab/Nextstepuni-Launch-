import { execFileSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { expect, it } from 'vitest';

it('includes supplemental subject waves while preserving other published subjects', () => {
  const directory = mkdtempSync(join(tmpdir(), 'topic-tags-scoped-'));
  try {
    const waves = join(directory, 'scripts/paper-trail/topic-tags/tags');
    const data = join(directory, 'data/paperTrail');
    mkdirSync(waves, { recursive: true });
    mkdirSync(data, { recursive: true });
    const paper = (subjectId: string, year: number, n: string) => ({
      subjectId, level: 'higher', lang: 'ev', year, fileid: `${subjectId}-${year}.pdf`,
      paperKey: 'single', q: [{ n, primary: `${subjectId}-1` }],
    });
    const current = paper('japanese', 2026, '1');
    const supplemental = paper('japanese', 2022, '2');
    const other = paper('physics', 2025, 'published');
    writeFileSync(join(waves, 'japanese.json'), JSON.stringify([current]));
    writeFileSync(join(waves, 'japanese-written-2019-2022.json'), JSON.stringify([supplemental]));
    writeFileSync(join(waves, 'physics.json'), JSON.stringify([paper('physics', 2025, 'unpublished')]));
    writeFileSync(join(data, 'paperTopicTags.json'), JSON.stringify([other, current, supplemental]));
    writeFileSync(join(data, 'topicLabels.json'), JSON.stringify({ 'japanese-1': 'Old label', 'physics-1': 'Published label' }));
    writeFileSync(join(directory, 'curriculum.ts'), 'CURRICULUM: CurriculumSubject[] = [{"strands":[{"subtopics":[{"id":"japanese-1","name":"Japanese label"},{"id":"physics-1","name":"Unpublished label"}]}]}];');
    const script = resolve(__dirname, '../scripts/paper-trail/topic-tags/build-tags.mjs');
    execFileSync(process.execPath, [script, '--subject', 'japanese'], { cwd: directory });
    const published = JSON.parse(readFileSync(join(data, 'paperTopicTags.json'), 'utf8'));
    expect(published).toEqual([current, supplemental, other]);
    expect(JSON.parse(readFileSync(join(data, 'topicLabels.json'), 'utf8'))).toEqual({
      'japanese-1': 'Japanese label', 'physics-1': 'Published label',
    });
    const runtime = JSON.parse(readFileSync(join(data, 'paperTopicTags-runtime.json'), 'utf8'));
    expect(runtime.papers).toHaveLength(3);
    expect(runtime.papers.map((row: [number, string, string, number]) => [runtime.subjects[row[0]], row[3]])).toEqual([
      ['japanese', 2026], ['japanese', 2022], ['physics', 2025],
    ]);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});
