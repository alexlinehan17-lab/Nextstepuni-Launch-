import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const tasks = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/examTopics/french-reviewed-tasks.json'), 'utf8'));

/** Apply only reviewed geometry. Task identities are stable and additive. */
export function addFrenchReviewedAnchors(map, year) {
  const paperTasks = tasks.filter(task => task.year === year && task.fileid === map.paperFileid);
  // Rebuild supplemental ordering when another reviewed category is added later.
  // The original archive questions retain their existing order and geometry.
  const childIds = new Set(paperTasks.filter(task => task.n !== task.parent).map(task => task.n));
  const existingChildren = new Map(map.q.filter(question => childIds.has(question.n)).map(question => [question.n, question]));
  map.q = map.q.filter(question => !childIds.has(question.n));
  for (const task of paperTasks) {
    if (existingChildren.has(task.n)) map.q.push({ ...existingChildren.get(task.n), printOrder: map.q.length + 1 });
    const existing = map.q.find(question => question.n === task.n);
    const parent = map.q.find(question => question.n === task.parent);
    if (!parent) throw new Error(`Missing French parent ${year}/${task.fileid}/${task.parent}`);
    const geometry = {
      paperRegion: task.pages.map(p => ({ p, r: [0, 0, 1, 1] })),
    };
    if (existing) Object.assign(existing, geometry, task.n === task.parent ? {} : { label: task.label });
    else map.q.push({ ...parent, ...geometry, n: task.n, label: task.label, printOrder: map.q.length + 1 });
    map.maxCropPages = Math.max(map.maxCropPages ?? 3, task.pages.at(-1) - task.pages[0]);
  }
  return map;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  for (const key of new Set(tasks.map(task => `${task.year}/${task.fileid}.json`))) {
    const file = path.join(ROOT, 'public/paper-anchors', key);
    const map = addFrenchReviewedAnchors(JSON.parse(fs.readFileSync(file, 'utf8')), Number(key.split('/')[0]));
    fs.writeFileSync(file, `${JSON.stringify(map)}\n`);
  }
}
