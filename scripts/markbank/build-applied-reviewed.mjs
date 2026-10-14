#!/usr/bin/env node
/** Compile visually reviewed Applied Mathematics tasks; never infer coverage
 * from this output. The independent review ledger is the required input. */
import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { paperIndex, paperEntry, resolvePaperFileid } from './paperIndex.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const reviewDir = resolve(root, 'scripts/markbank/authoring/reviewed/applied-maths');
const cards = [];
// Withdrawn IDs still carry saved progress to their consolidated cards.
// Newly separated tasks must use fresh IDs rather than revive an alias key.
const reservedAliasIds = new Set([...readFileSync(resolve(root, 'components/MarkBank/cardAliases.ts'), 'utf8')
  .matchAll(/^  "([^"]+)": "[^"]+"/gm)].map(match => match[1]));
const questionMappings = [];
const taxonomy = JSON.parse(readFileSync(resolve(root, 'data/examTopics/applied-mathematics.json')));
const archiveTopics = JSON.parse(readFileSync(resolve(root, 'data/examTopics/applied-mathematics-archive-topics.json')));
const hash = path => createHash('sha256').update(readFileSync(path)).digest('hex');
const schemeSources = task => task.schemePages
  ? task.schemePages.map((page, index) => ({ page, region: task.schemeRegions[index] }))
  : [{ page: task.schemePage, region: task.schemeRegion }];
for (const filename of readdirSync(reviewDir).filter(name => name.endsWith('.json')).sort()) {
  const review = JSON.parse(readFileSync(resolve(reviewDir, filename)));
  for (const paper of review.papers) {
    const short = paper.level === 'higher' ? 'hl' : 'ol';
    const prefix = `${review.year}-${short}`;
    const originalSource = readFileSync(resolve(root, `components/MarkBank/cards/applied-maths/${paper.level}.ts`), 'utf8');
    const originalBlocks = new Map([...originalSource.matchAll(/  \{\n    \.\.\.base,[\s\S]*?  \} as SecCard,/g)]
      .map(([block]) => [block.match(/^    id: "([^"]+)"/m)?.[1], block]));
    const correctionIds = new Set();
    for (const correction of paper.cardCorrections ?? []) {
      const block = originalBlocks.get(correction.cardId);
      if (!block || createHash('sha256').update(block).digest('hex') !== correction.originalBlockSha256
        || !paper.tasks.some(task => `am-${prefix}-${task.idSuffix}` === correction.cardId)
        || !correction.reason || correctionIds.has(correction.cardId))
        throw new Error(`${prefix}: stale, duplicate or orphan card correction ${correction.cardId}`);
      correctionIds.add(correction.cardId);
    }
    const paperPath = resolve(root, `examiner-reports/applied-maths/papers/${prefix}-paper.pdf`);
    const schemePath = resolve(root, `examiner-reports/applied-maths/schemes/${prefix}.pdf`);
    if (hash(paperPath) !== paper.paperSha256 || hash(schemePath) !== paper.schemeSha256)
      throw new Error(`${prefix}: source PDF changed since review`);
    // Scan the raw paper, not just selected card wording. Exact reviewed hits
    // must still exist, and an added directive must not pass silently.
    const selections = JSON.parse(execFileSync('python3', ['-c', `
import fitz,re,json,sys,unicodedata
hits=[]
for i,p in enumerate(fitz.open(sys.argv[1])):
 for line in p.get_text().splitlines():
  line=' '.join(unicodedata.normalize('NFKC',line).split())
  if re.search(r'\\b(?:choose|one of|any (?:one|two|three|four|five|six|seven|eight|nine|ten|\\d+)|either|or otherwise|answer.*questions|(?:one|two|three|four|five|six|seven|eight|nine|ten|\\d+) questions? (?:to be )?answered)\\b',line,re.I): hits.append({'page':i+1,'text':line})
print(json.dumps(hits))
`, paperPath], { encoding: 'utf8' }));
    if (JSON.stringify(selections) !== JSON.stringify(paper.selectionDirectives?.map(({ page, text }) => ({ page, text }))))
      throw new Error(`${prefix}: unclassified or stale selection directive`);
    if (paper.tasks.length !== paper.practiceTaskCount) throw new Error(`${prefix}: missing reviewed tasks`);
    // Source review still owns diagram boundaries. This additional guard
    // catches an accidentally clipped exponent, force label or tariff at the
    // top/bottom of a reviewed solution crop, including private font glyphs.
    const clipped = JSON.parse(execFileSync('python3', ['-c', `
import fitz,json,sys
doc=fitz.open(sys.argv[1]); clipped=[]
for task in json.load(sys.stdin):
 p=doc[task['schemePage']-1]; r=task['schemeRegion']
 if len(r)!=4 or not (0<=r[0]<r[2]<=1 and 0<=r[1]<r[3]<=1): raise ValueError('Invalid crop: '+task['idSuffix'])
 box=fitz.Rect(r[0]*p.rect.width,r[1]*p.rect.height,r[2]*p.rect.width,r[3]*p.rect.height)
 if not p.get_text(clip=box).strip(): raise ValueError('Empty solution crop: '+task['idSuffix'])
 for b in p.get_text('dict')['blocks']:
  for line in b.get('lines',[]):
   text=''.join(s['text'] for s in line['spans']).strip()
   x0,y0,x1,y1=line['bbox']; y0/=p.rect.height; y1/=p.rect.height
   if text and (y0+.0005<r[1]<y1-.0005 or y0+.0005<r[3]<y1-.0005) and x0<p.rect.width*r[2] and x1>p.rect.width*r[0]: clipped.append(task['idSuffix'])
print(json.dumps(sorted(set(clipped))))
`, schemePath], { input: JSON.stringify(paper.tasks.flatMap(task => {
      if (task.schemePages && (!task.schemePages.length || task.schemePages.length !== task.schemeRegions?.length))
        throw new Error(`${prefix}/${task.ref}: mismatched solution pages and crops`);
      return schemeSources(task).map(({ page, region }) => ({ idSuffix: task.idSuffix, schemePage: page, schemeRegion: region }));
    })), encoding: 'utf8' }));
    if (clipped.length) throw new Error(`${prefix}: clipped source text in ${clipped.join(', ')}`);
    const fileid = resolvePaperFileid('applied-maths', review.year, paper.level, 'B');
    const entry = paperEntry('applied-maths', review.year, paper.level);
    const schemeFileid = entry?.papers.find(item => item.doc.f.replace(/\.pdf$/, '') === fileid)?.scheme?.f;
    if (!fileid || !schemeFileid) throw new Error(`${prefix}: unbound source`);
    const totals = new Map();
    const questions = new Map();
    for (const task of paper.tasks) {
      const id = `am-${prefix}-${task.idSuffix}`;
      if (reservedAliasIds.has(id)) throw new Error(`${prefix}: task revives a redirected progress ID ${id}`);
      if (originalBlocks.has(id) && !correctionIds.has(id))
        throw new Error(`${prefix}: unaudited correction of shipped card ${id}`);
      const totalMarks = task.allocations.reduce((sum, item) => sum + Math.max(...item.credit), 0);
      const solutionSources = schemeSources(task);
      const q = task.ref.match(/^Q(\d+)/)?.[1];
      if (!q || !task.examTopicIds?.length || task.examTopicIds.some(id =>
        ![...taxonomy.levels[paper.level].topics, ...archiveTopics.filter(topic => topic.level === paper.level)]
          .some(topic => topic.id === id)))
        throw new Error(`${prefix}/${task.ref}: missing or unknown reviewed exam topic`);
      totals.set(q, (totals.get(q) ?? 0) + totalMarks);
      const tasks = questions.get(q) ?? [];
      tasks.push(task);
      questions.set(q, tasks);
      const common = {
        attribution: '© State Examinations Commission',
        presentationNote: 'Original SEC examination layout, including mathematical notation and diagrams.',
      };
      cards.push({
        id, source: 'sec', kind: 'rubric', subjectId: 'applied-maths',
        year: review.year, level: paper.level, topicId: task.topicId,
        conceptId: task.topicId, section: 'B',
        questionRef: `${review.year} ${short.toUpperCase()} ${task.ref}`,
        questionText: task.questionText,
        ...(task.stem ? { stem: task.stem } : {}),
        ...(task.practiceFocus ? { practiceFocus: task.practiceFocus } : {}),
        paperFileid: fileid, totalMarks,
        sourceMaterial: { ...common, kind: 'source-paper', label: `${task.ref} · question and context`, title: 'Original question pages', pages: task.paperPages,
          ...(task.paperRegions ? { regions: task.paperRegions } : {}) },
        schemeCitation: `SEC Applied Mathematics ${review.year} ${paper.level === 'higher' ? 'Higher' : 'Ordinary'} Level marking scheme, PDF page${solutionSources.length > 1 ? 's' : ''} ${solutionSources.map(source => source.page).join(', ')} — © State Examinations Commission.`,
        rubric: {
          system: 'applied-mathematics',
          solution: { ...common, kind: 'source-scheme', label: task.ref, title: 'Official worked solution', sourceFileid: schemeFileid, pages: solutionSources.map(source => source.page), regions: solutionSources.map(source => source.region) },
          allocations: task.allocations.map((item, index) => ({ id: `allocation-${index + 1}`, ...item })),
          markingGuideNote: paper.markingGuideNote,
        },
        qa: { gates: ['paper-scheme-visual-review', 'published-tariffs', 'source-hashes', 'selection-review', ...(correctionIds.has(id) ? ['reviewed-card-correction'] : [])], humanReviewedBy: 'Codex source review (not human sign-off)', humanReviewedAt: review.reviewedAt },
      });
    }
    if (JSON.stringify(Object.fromEntries(totals)) !== JSON.stringify(paper.questionMarks)
      || [...totals.values()].reduce((sum, marks) => sum + marks, 0) !== paper.availableMarks)
      throw new Error(`${prefix}: task allocations do not reconcile to the reviewed paper`);
    const fullFileid = `${fileid}.pdf`;
    const originalMapPath = resolve(root, `scripts/paper-trail/answers/${review.year}/${fullFileid}.json`);
    const originalMap = existsSync(originalMapPath) ? JSON.parse(readFileSync(originalMapPath)) : null;
    const answerQuestions = [];
    for (const [n, tasks] of questions) {
      questionMappings.push({ year: review.year, level: paper.level, lang: 'ev',
        fileid: fullFileid, n, topicIds: [...new Set(tasks.flatMap(task => task.examTopicIds))] });
      const pages = [...new Set(tasks.flatMap(task => task.paperPages))].sort((a, b) => a - b);
      const paperRegions = new Map();
      for (const task of tasks) {
        task.paperPages.forEach((page, index) => {
          const rect = task.paperRegions?.[index] ?? [0.05, 0.065, 0.96, 0.92];
          const previous = paperRegions.get(page);
          paperRegions.set(page, previous
            ? [Math.min(previous[0], rect[0]), Math.min(previous[1], rect[1]), Math.max(previous[2], rect[2]), Math.max(previous[3], rect[3])]
            : rect);
        });
      }
      const schemeRegions = new Map();
      for (const task of tasks) {
        for (const { page, region } of schemeSources(task)) {
          const previous = schemeRegions.get(page);
          const [x0, y0, x1, y1] = region;
          schemeRegions.set(page, previous
            ? [Math.min(previous[0], x0), Math.min(previous[1], y0), Math.max(previous[2], x1), Math.max(previous[3], y1)]
            : [x0, y0, x1, y1]);
        }
      }
      const region = [...schemeRegions].sort(([a], [b]) => a - b).map(([p, r]) => ({ p, r }));
      const original = originalMap?.q.find(question => question.n === n);
      answerQuestions.push({
        ...(original ?? { n, label: `Question ${n}`, mode: 'crop', conf: 1, pP: pages[0], pY: [0.065, 1], region }),
        paperRegion: pages.map(p => ({ p, r: paperRegions.get(p) })),
        ...(original ? { schemeRegion: region } : {}),
      });
    }
    if (originalMap?.q.some(question => !questions.has(question.n)))
      throw new Error(`${prefix}: a shipped Atlas question would be lost`);
    const hosted = {
      ...(originalMap ?? { v: 1, paperFileid: fullFileid, schemeFileid, component: '000',
        copyright: '© State Examinations Commission',
        band: [1, Math.max(...paper.tasks.flatMap(task => schemeSources(task).map(source => source.page))) + 1] }),
      maxCropPages: Math.max(...answerQuestions.map(question => question.paperRegion.length)),
      q: answerQuestions,
    };
    const output = resolve(root, `public/paper-answers/${review.year}/${fullFileid}.json`);
    mkdirSync(dirname(output), { recursive: true });
    writeFileSync(output, JSON.stringify(hosted) + '\n');
  }
}
// A translated booklet keeps its native coordinates, but identical tasks share
// the canonical cards. A separate visual review is required before it is added.
const translatedDir = resolve(root, 'scripts/markbank/authoring/translated/applied-maths');
for (const filename of existsSync(translatedDir) ? readdirSync(translatedDir).filter(name => name.endsWith('.json')).sort() : []) {
  const review = JSON.parse(readFileSync(resolve(translatedDir, filename)));
  const canonicalPath = resolve(reviewDir, filename);
  for (const paper of review.papers) {
    const short = paper.level === 'higher' ? 'hl' : 'ol';
    const prefix = `${review.year}-${short}-iv`;
    const entry = paperIndex['applied-mathematics'].find(item => item.year === review.year && item.level === paper.level && item.lang === 'iv');
    const indexed = entry?.papers.find(item => item.doc.f === paper.paperFileid);
    if (!indexed || indexed.scheme?.f !== paper.schemeFileid)
      throw new Error(`${prefix}: translated source is not bound to the index`);
    const paperPath = resolve(root, `examiner-reports/applied-maths/irish/${review.year}-${short}-paper.pdf`);
    const schemePath = resolve(root, paper.schemeLang === 'iv'
      ? `examiner-reports/applied-maths/irish/${review.year}-${short}-scheme.pdf`
      : `examiner-reports/applied-maths/schemes/${review.year}-${short}.pdf`);
    if (hash(paperPath) !== paper.paperSha256 || hash(schemePath) !== paper.schemeSha256 || hash(canonicalPath) !== paper.canonicalReviewSha256)
      throw new Error(`${prefix}: translated or canonical source changed since review`);
    if (paper.distinctAdditionalTasks.length)
      throw new Error(`${prefix}: distinct translated tasks must be authored before compilation`);
    const validation = JSON.parse(execFileSync('python3', [resolve(root, 'scripts/markbank/validate-applied-translation.py'), paperPath, schemePath], {
      input: JSON.stringify(paper), encoding: 'utf8',
    }));
    if (JSON.stringify(validation.selections) !== JSON.stringify(paper.selectionDirectives.map(({ page, text }) => ({ page, text })))
      || paper.selectionDirectives.some(item => !item.classification || !item.reason))
      throw new Error(`${prefix}: unclassified or stale Irish selection directive`);
    const canonicalCards = cards.filter(card => card.year === review.year && card.level === paper.level);
    const mappedIds = paper.questions.flatMap(question => question.canonicalTaskIds);
    if (canonicalCards.length !== paper.practiceTaskCount || new Set(mappedIds).size !== mappedIds.length
      || JSON.stringify([...mappedIds].sort()) !== JSON.stringify(canonicalCards.map(card => card.id).sort()))
      throw new Error(`${prefix}: missing, duplicate or orphan translated task correspondence`);
    const originalMapPath = resolve(root, `scripts/paper-trail/answers/${review.year}/${paper.paperFileid}.json`);
    const originalMap = existsSync(originalMapPath) ? JSON.parse(readFileSync(originalMapPath)) : null;
    const answerQuestions = paper.questions.map(question => {
      const tasks = question.canonicalTaskIds.map(id => canonicalCards.find(card => card.id === id));
      if (tasks.some(task => task.questionRef.match(/Q(\d+)/)?.[1] !== question.n)
        || JSON.stringify(tasks.map(task => task.totalMarks)) !== JSON.stringify(question.taskTariffs))
        throw new Error(`${prefix}/Q${question.n}: translated task boundary or tariff changed`);
      const canonical = questionMappings.find(item => item.year === review.year && item.level === paper.level && item.lang === 'ev' && item.n === question.n);
      if (!canonical) throw new Error(`${prefix}/Q${question.n}: no canonical topic mapping`);
      questionMappings.push({ ...canonical, lang: 'iv', fileid: paper.paperFileid });
      const original = originalMap?.q.find(item => item.n === question.n);
      return {
        ...(original ?? { n: question.n, label: `Question ${question.n}`, mode: 'crop', conf: 1,
          pP: question.paperRegion[0].p, pY: [question.paperRegion[0].r[1], 1], region: question.schemeRegion }),
        paperRegion: question.paperRegion,
        ...(original ? { schemeRegion: question.schemeRegion } : {}),
      };
    });
    if (originalMap?.q.some(question => !paper.questions.some(item => item.n === question.n)))
      throw new Error(`${prefix}: a shipped Irish Atlas question would be lost`);
    const hosted = {
      ...(originalMap ?? { v: 1, paperFileid: paper.paperFileid, schemeFileid: paper.schemeFileid,
        component: '000', copyright: '© State Examinations Commission',
        band: [1, validation.schemePages + 1] }),
      maxCropPages: Math.max(...answerQuestions.map(question => question.paperRegion.length)),
      q: answerQuestions,
    };
    const output = resolve(root, `public/paper-answers/${review.year}/${paper.paperFileid}.json`);
    mkdirSync(dirname(output), { recursive: true });
    writeFileSync(output, JSON.stringify(hosted) + '\n');
  }
}
if (new Set(cards.map(card => card.id)).size !== cards.length) throw new Error('Duplicate task ID');
writeFileSync(resolve(root, 'components/MarkBank/cards/applied-maths/reviewed.json'), JSON.stringify(cards, null, 2) + '\n');
writeFileSync(resolve(root, 'data/examTopics/applied-mathematics-reviewed-questions.json'), JSON.stringify(questionMappings, null, 2) + '\n');
console.log(`Compiled ${cards.length} reviewed tasks. This is not a full-corpus completion claim.`);
