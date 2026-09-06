/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Resolve browser-audited StudyClix State-exam headings to exact, entitled
 * SEC question cards for subjects whose heading grammar exposes a stable
 * year/level/paper/question identity. Commercial mocks are not inputs.
 */

import fs from 'node:fs';
import path from 'node:path';
import { PAPER_TRAIL_INDEX } from '../../paperTrailData';

const ROOT = path.resolve(process.cwd());
const DATA = path.join(ROOT, 'data/examTopics');
const ANSWERS = path.join(ROOT, 'scripts/paper-trail/answers');

const SUBJECTS = [
  ['english', 'english'],
  ['geography', 'geography'],
  ['home-economics-s-and-s', 'home-economics'],
  ['mathematics', 'mathematics'],
  ['physical-education', 'physical-education'],
] as const;

type Level = 'higher' | 'ordinary' | 'foundation';
type Lang = 'ev' | 'iv';
type Sitting = 'main' | 'deferred' | 'sample';

type ReferenceTopic = {
  id: string;
  label: string;
  sourceUnavailable?: string;
  officialQuestionHeadings: string[];
};

type ReferenceVariant = { label: string; topics: ReferenceTopic[] };
type ReferenceAudit = { subjectId: string; variants: Record<string, ReferenceVariant> };

type AnchorQuestion = { n: string; label?: string };
type LocalTarget = {
  level: Level;
  lang: Lang;
  year: number;
  paperKey: string;
  fileid: string;
  n: string;
  paperLabel: string;
  questionLabel?: string;
};

const readJson = <T>(file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as T;
const writeJson = (file: string, value: unknown) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

const levelForVariant = (variant: string): Level => {
  if (variant.startsWith('higher')) return 'higher';
  if (variant.startsWith('ordinary')) return 'ordinary';
  if (variant.startsWith('foundation')) return 'foundation';
  throw new Error(`Unknown reference variant level: ${variant}`);
};

const paperKeyOf = (label: string) =>
  /\b(two|2|ii)\b/i.test(label) ? 'p2' : /\b(one|1|i)\b/i.test(label) ? 'p1' : 'single';

const localTargetsFor = (subjectId: string) => {
  const targets: LocalTarget[] = [];
  const paperVariants = new Set<string>();
  for (const entry of PAPER_TRAIL_INDEX[subjectId] ?? []) {
    for (const paper of entry.papers) {
      if (paper.answers !== 1) continue;
      const answerFile = path.join(ANSWERS, String(entry.year), `${paper.doc.f}.json`);
      if (!fs.existsSync(answerFile)) {
        throw new Error(`${subjectId}: answers=1 but local answer map is missing: ${answerFile}`);
      }
      const answerMap = readJson<{ q: AnchorQuestion[] }>(answerFile);
      paperVariants.add(`${entry.level}|${entry.lang}|${entry.year}|${paper.doc.f}`);
      for (const question of answerMap.q) {
        targets.push({
          level: entry.level as Level,
          lang: entry.lang,
          year: entry.year,
          paperKey: paperKeyOf(paper.label),
          fileid: paper.doc.f,
          n: question.n,
          paperLabel: paper.label,
          ...(question.label ? { questionLabel: question.label } : {}),
        });
      }
    }
  }
  return { targets, paperVariants: paperVariants.size };
};

const headingIdentity = (heading: string) => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const n = heading.match(/Question\s+(\d+)/i)?.[1];
  if (!year) throw new Error(`Unparseable factual reference year: ${heading}`);
  const sitting: Sitting = /\bSample\b/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main';
  const section = heading.match(/Section\s+([A-D])/i)?.[1]?.toUpperCase();
  const explicitPaper = heading.match(/Paper\s*(One|Two|1|2)\b/i)?.[1]?.toLowerCase();
  const explicitPart = heading.match(/Part\s+(One|Two|1|2)\b/i)?.[1]?.toLowerCase();
  const numbered = explicitPaper ?? explicitPart;
  const paperKey = numbered === 'one' || numbered === '1'
    ? 'p1'
    : numbered === 'two' || numbered === '2'
      ? 'p2'
      : null;
  return { year, n, sitting, section, paperKey, projectMaths: /Project Maths/i.test(heading) };
};

const logicalTargetKey = (target: LocalTarget) => [
  target.level,
  target.year,
  target.paperKey,
  target.fileid.replace(/(?:EV|IV)(?=\.pdf$)/i, 'BV'),
  target.n,
].join('|');

const targetIdentity = (target: LocalTarget) => ({
  level: target.level,
  lang: target.lang,
  year: target.year,
  paperKey: target.paperKey,
  fileid: target.fileid,
  n: target.n,
  ...(target.questionLabel ? { label: target.questionLabel } : {}),
});

const candidatesFor = (
  subjectId: string,
  level: Level,
  heading: string,
  allTargets: LocalTarget[],
  topicId: string,
) => {
  const parsed = headingIdentity(heading);
  if (subjectId === 'english') {
    if (parsed.sitting !== 'main') {
      return { parsed, candidates: [], reason: `${parsed.sitting}-sitting-not-in-local-corpus` };
    }
    const section = Number(heading.match(/Section\s+(\d+)/i)?.[1]);
    let candidates = allTargets.filter(target =>
      target.level === level
      && target.year === parsed.year
      && target.paperKey === parsed.paperKey);

    if (
      parsed.paperKey === 'p1'
      && topicId.endsWith('-composition')
      && parsed.year === 2010
      && /Section\s+1\s*-\s*Question\s+A\s*$/i.test(heading)
    ) {
      // This StudyClix entry is cross-listed on its composition shelf, but its
      // signed-in viewer shows Text 3's Question A from the comprehension paper.
      candidates = candidates.filter(target =>
        target.questionLabel === 'Comprehending · Text 3 · Question A');
      return candidates.length === 1
        ? { parsed, candidates, reason: null }
        : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
    }

    if (parsed.paperKey === 'p1' && topicId.endsWith('-composition')) {
      const range = heading.match(/Question\s+(\d+)\s*-\s*(\d+)/i);
      const first = Number(range?.[1]);
      const last = Number(range?.[2]);
      if (section !== 2 || !first || !last) {
        return { parsed, candidates: [], reason: 'reference-heading-missing-composition-range' };
      }
      candidates = candidates.filter(target => Number(target.n) >= first && Number(target.n) <= last);
      return candidates.length === last - first + 1
        ? { parsed, candidates, reason: null }
        : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
    }

    if (topicId.includes('reading-comprehension')) {
      // StudyClix uses four one-off historical bundle labels which do not follow
      // the later Text 1/2/3 convention. These were checked in the signed-in
      // question viewer against the underlying SEC paper before being mapped.
      if (parsed.year === 2010 && /Section\s+2\s*-\s*Question\s+1\s*-\s*7/i.test(heading)) {
        candidates = candidates.filter(target => Number(target.n) >= 1 && Number(target.n) <= 7);
        return candidates.length === 7
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      if (parsed.year === 2010 && /Section\s+1\s*-\s*Question\s+A\s*&\s*B/i.test(heading)) {
        candidates = candidates.filter(target =>
          target.questionLabel?.startsWith('Comprehending · Text '));
        return candidates.length === 6
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      if (parsed.year === 2011 && /Section\s+1\s*-\s*Question\s+A\s*$/i.test(heading)) {
        candidates = candidates.filter(target =>
          target.questionLabel?.startsWith('Comprehending · Text 2 ·'));
        return candidates.length === 2
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      if (parsed.year === 2012 && /Section\s+1\s*-\s*Question\s+C\s*$/i.test(heading)) {
        candidates = candidates.filter(target =>
          target.questionLabel?.startsWith('Comprehending · Text 3 ·'));
        return candidates.length === 2
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      if (/Section\s+1\s*-\s*Question\s+A\s*-\s*B/i.test(heading)) {
        candidates = candidates.filter(target =>
          target.questionLabel?.startsWith('Comprehending · Text '));
        return candidates.length === 6
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      const textRange = heading.match(/Section\s+1\s*-\s*Question\s+(\d)\s*-\s*(\d)/i);
      if (textRange) {
        const firstText = Number(textRange[1]);
        const lastText = Number(textRange[2]);
        candidates = candidates.filter(target => {
          const textNumber = Number(target.questionLabel?.match(/^Comprehending · Text (\d) ·/)?.[1]);
          return textNumber >= firstText && textNumber <= lastText;
        });
        return candidates.length === (lastText - firstText + 1) * 2
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      const textNumber = Number(
        heading.match(/Section\s+1\s*-\s*Question\s+(?:Text\s+)?(\d)/i)?.[1]
        ?? heading.match(/Question\s+Text\s+(\d)/i)?.[1],
      );
      candidates = textNumber
        ? candidates.filter(target => target.questionLabel?.startsWith(`Comprehending · Text ${textNumber} ·`))
        : [];
      return candidates.length === 2
        ? { parsed, candidates, reason: null }
        : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
    }

    if (parsed.paperKey === 'p2' && level === 'higher') {
      if (topicId.includes('-text-') || /-(?:hamlet|othello)$/.test(topicId)) {
        const rawChoice = (
          heading.match(/Section\s+1\s*-\s*Question\s+\(?([A-I1-9])\)?/i)?.[1]
        )?.toUpperCase();
        const letter = rawChoice && /\d/.test(rawChoice)
          ? String.fromCharCode(64 + Number(rawChoice))
          : rawChoice;
        const part = heading.match(/Part\s+([AB])\s*$/i)?.[1]?.toUpperCase();
        candidates = letter
          ? candidates.filter(target => {
            if (!target.questionLabel?.startsWith(`Single Text ${letter} ·`)) return false;
            if (part === 'A') return target.questionLabel.endsWith('· (i)');
            if (part === 'B') return target.questionLabel.endsWith('· (ii)');
            return true;
          })
          : [];
        const expected = part ? 1 : 2;
        return candidates.length === expected
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      if (topicId.includes('-comparative-')) {
        const modeKey = topicId.endsWith('-cultural-context')
          ? 'cultural-context'
          : topicId.endsWith('-literary-genre')
            ? 'literary-genre'
            : topicId.endsWith('-theme-or-issue')
              ? 'theme-or-issue'
              : topicId.endsWith('-vision-viewpoint')
                ? 'vision-viewpoint'
                : null;
        const numericPart = heading.match(/Question\s+[A-C]\s*-\s*Part\s+([12])\s*$/i)?.[1];
        candidates = modeKey
          ? candidates.filter(target => {
            const label = target.questionLabel?.toLowerCase();
            if (!label?.startsWith('comparative ')) return false;
            const modeMatches = modeKey === 'cultural-context'
              ? label.includes('cultural context')
              : modeKey === 'literary-genre'
                ? label.includes('literary genre')
                : modeKey === 'theme-or-issue'
                  ? label.includes('theme') && label.includes('issue')
                  : label.includes('vision') && label.includes('viewpoint');
            if (!modeMatches) return false;
            return numericPart ? target.questionLabel.endsWith(`· Q${numericPart}`) : true;
          })
          : [];
        const expected = numericPart ? 1 : 2;
        return candidates.length === expected
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      if (topicId.endsWith('-unseen-poetry')) {
        candidates = candidates.filter(target => target.questionLabel?.startsWith('Unseen Poetry · Q'));
        return candidates.length === 2
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      if (topicId.includes('-poetry-')) {
        const option = Number(
          heading.match(/(?:Question|Part)\s+(\d+)\s*$/i)?.[1]
          ?? heading.match(/Question\s+B(\d+)\s*$/i)?.[1]
          ?? (Number(section) === 4 ? heading.match(/Question\s+(\d+)\s*$/i)?.[1] : undefined),
        );
        candidates = option
          ? candidates.filter(target =>
            target.questionLabel?.startsWith('Prescribed Poetry ·')
            && target.questionLabel.endsWith(`· Q${option}`))
          : [];
        return candidates.length === 1
          ? { parsed, candidates, reason: null }
          : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
      }
      return { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
    }

    if (parsed.paperKey === 'p2' && level === 'ordinary') {
      if (topicId.includes('-text-') || /-(?:hamlet|othello)$/.test(topicId)) {
        const rawChoice = heading.match(
          /Section\s+1\s*-\s*Question\s+\(?([A-I1-9])\)?/i,
        )?.[1]?.toUpperCase();
        const letter = rawChoice && /\d/.test(rawChoice)
          ? String.fromCharCode(64 + Number(rawChoice))
          : rawChoice;
        candidates = letter
          ? candidates.filter(target => target.questionLabel?.startsWith(`Single Text ${letter} ·`))
          : [];
      } else if (topicId.includes('-comparative-')) {
        const letter = heading.match(/Section\s+2\s*-\s*Question\s+([A-C])/i)?.[1]?.toUpperCase();
        candidates = letter
          ? candidates.filter(target => target.questionLabel?.startsWith(`Comparative ${letter} ·`))
          : [];
      } else if (topicId.endsWith('-unseen-poetry')) {
        candidates = candidates.filter(target => target.questionLabel === 'Unseen Poetry');
      } else if (topicId.includes('-poetry-') && !topicId.endsWith('-unseen-poetry')) {
        const letter = (
          heading.match(/(?:Part|Question)\s+([A-H])\s*$/i)?.[1]
          ?? heading.match(/Section\s+3\s*-\s*Question\s+([A-H])\b/i)?.[1]
        )?.toUpperCase();
        candidates = letter
          ? candidates.filter(target => target.questionLabel?.startsWith(`Poetry ${letter} ·`))
          : [];
      } else {
        candidates = [];
      }
      return candidates.length === 1
        ? { parsed, candidates, reason: null }
        : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
    }

    return { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
  }
  if (
    subjectId === 'home-economics-s-and-s'
    && level === 'higher'
    && parsed.year === 2016
    && topicId.endsWith('-food-industry-packaging')
    && /Section\s+3\s*-\s*Question\s+c\s*$/i.test(heading)
  ) {
    // The StudyClix heading drops both the paper section letter and question
    // number.  Its source card is the packaging part of SEC Section B Q3(c).
    const candidates = allTargets.filter(target =>
      target.level === level
      && target.year === parsed.year
      && target.questionLabel === 'Section B · Q3');
    return candidates.length === 1
      ? { parsed, candidates, reason: null }
      : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
  }
  if (
    subjectId === 'mathematics'
    && level === 'foundation'
    && parsed.year === 2018
    && /Section\s+1\s*-\s*Question\s+A\s*$/i.test(heading)
  ) {
    // The signed-in StudyClix viewer labels this as "Question A", but the
    // image itself is the official Foundation paper's Question 1 (the ages
    // line plot). Map the verified image, not the malformed heading.
    const candidates = allTargets.filter(target =>
      target.level === level
      && target.year === parsed.year
      && target.fileid === 'LC003BLP100EV.pdf'
      && target.n === '1');
    return candidates.length === 1
      ? { parsed, candidates, reason: null }
      : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
  }
  if (!parsed.n) return { parsed, candidates: [], reason: 'reference-heading-missing-question-number' };
  if (parsed.sitting !== 'main') return { parsed, candidates: [], reason: `${parsed.sitting}-sitting-not-in-local-corpus` };
  if (subjectId === 'physical-education' && level === 'ordinary' && parsed.year === 2020) {
    // StudyClix displays a distinct Ordinary paper (for example, Q4 is the
    // head/neck lever diagram), but the corresponding LC225GLP000 paper and
    // scheme are absent from the SEC's authoritative 2020 archive and the
    // direct official file URLs return 404.  The available Higher paper is
    // visibly different, so never attach these headings by question number.
    return { parsed, candidates: [], reason: 'reference-state-tag-not-found-in-sec-archive' };
  }
  let candidates = allTargets.filter(target =>
    target.level === level
    && target.year === parsed.year);

  if (subjectId === 'geography') {
    let paperKey = parsed.paperKey;
    if (!paperKey && parsed.year >= 2020 && /Question\s+\d+\s*-\s*Part\s+[ABC]\b/i.test(heading)) {
      // A/B/C sub-parts exist on the structured Part Two questions.  Part One
      // is the separate short-answer booklet and has no such sub-part labels.
      paperKey = 'p2';
    }
    if (!paperKey && parsed.year >= 2020 && parsed.section) paperKey = parsed.section === 'A' || parsed.section === 'B'
      ? null
      : parsed.section === 'C' || parsed.section === 'D'
        ? 'p2'
        : null;
    // The published headings use Section 1 for Part 1 and Sections 2–4 for
    // Part 2 in the 2020+ split-paper format.
    const numberedSection = heading.match(/Section\s+(\d+)/i)?.[1];
    if (!paperKey && parsed.year >= 2020 && numberedSection) paperKey = numberedSection === '1' ? 'p1' : 'p2';
    if (parsed.year < 2020) paperKey = 'single';
    if (paperKey) candidates = candidates.filter(target => target.paperKey === paperKey);
  } else if (subjectId === 'home-economics-s-and-s') {
    if (!parsed.section) return { parsed, candidates: [], reason: 'reference-heading-missing-section' };
    if (parsed.year >= 2020) {
      candidates = candidates.filter(target => parsed.section === 'A'
        ? /^Section A$/i.test(target.paperLabel)
        : /^Section B&C$/i.test(target.paperLabel));
    } else {
      candidates = candidates.filter(target => {
        const match = target.questionLabel?.match(/Section\s+([ABC])\s*·\s*Q(\d+)/i);
        return match?.[1]?.toUpperCase() === parsed.section && match?.[2] === parsed.n;
      });
    }
  } else if (subjectId === 'mathematics') {
    if (
      level === 'foundation'
      && parsed.year === 2012
      && !parsed.projectMaths
      && !parsed.paperKey
      && (
        /Section\s+A\s*-\s*Question\s+[2-6]\b/i.test(heading)
        || /Section\s+B\s*-\s*Question\s+7\s*-\s*Part\s+[bc]\b/i.test(heading)
      )
    ) {
      // These seven images form a separate 2012-style Foundation paper, but
      // they do not match any of the eight Mathematics papers in the SEC's
      // authoritative 2012 archive. StudyClix also exposes no scheme for the
      // checked entries. Keep them explicitly blocked instead of attaching
      // them to a same-numbered but different official question.
      return { parsed, candidates: [], reason: 'reference-state-tag-not-found-in-sec-archive' };
    }
    if (
      level === 'ordinary'
      && parsed.year === 2011
      && /Paper\s*-\s*Section\s+A\s*-\s*Question\s+8\s*$/i.test(heading)
    ) {
      // The viewer shows f(x)=1/(x+2), followed by its value table and graph.
      // That is Q8 of the ordinary Paper One file LC003GLP000, not Q8 of the
      // contemporaneous Project Maths paper (where the same task is Q9).
      candidates = candidates.filter(target =>
        target.fileid === 'LC003GLP000EV.pdf' && target.n === '8');
      return candidates.length === 1
        ? { parsed, candidates, reason: null }
        : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
    }
    if (parsed.paperKey) candidates = candidates.filter(target => target.paperKey === parsed.paperKey);
    if (
      parsed.year === 2010
      && parsed.paperKey === 'p2'
      && parsed.projectMaths
      && parsed.n === '9'
      && level === 'higher'
    ) {
      // The paper offers mutually exclusive Q9A (statistics) and Q9B
      // (geometry/trigonometry).  StudyClix omits the A suffix on its
      // statistics headings but retains 9B on the geometry headings.
      const choice = /Question\s+9B/i.test(heading) ? '10' : '9';
      candidates = candidates.filter(target =>
        /Project Maths/i.test(target.paperLabel) && target.n === choice);
      const logical = new Map<string, LocalTarget[]>();
      for (const candidate of candidates) {
        const key = logicalTargetKey(candidate);
        const editions = logical.get(key) ?? [];
        editions.push(candidate);
        logical.set(key, editions);
      }
      return logical.size === 1
        ? { parsed, candidates: [...logical.values()][0], reason: null }
        : { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
    }
    // All 2014 papers are the Project Maths examination, but StudyClix's
    // Foundation headings inconsistently omit those two words.
    if (parsed.year !== 2014) {
      candidates = candidates.filter(target => parsed.projectMaths
        ? /Project Maths/i.test(target.paperLabel)
        : !/Project Maths/i.test(target.paperLabel));
    }
  } else if (subjectId === 'physical-education') {
    candidates = candidates.filter(target => target.paperKey === 'single');
  }

  if (!(subjectId === 'home-economics-s-and-s' && parsed.year < 2020)) {
    candidates = candidates.filter(target => target.n === parsed.n);
  }
  const logical = new Map<string, LocalTarget[]>();
  for (const candidate of candidates) {
    const key = logicalTargetKey(candidate);
    const editions = logical.get(key) ?? [];
    editions.push(candidate);
    logical.set(key, editions);
  }
  if (logical.size === 1) return { parsed, candidates: [...logical.values()][0], reason: null };
  if (logical.size > 1) return { parsed, candidates: [], reason: 'ambiguous-local-paper-slot' };
  return { parsed, candidates: [], reason: 'answer-anchored-local-card-missing' };
};

for (const [subjectId, fileStem] of SUBJECTS) {
  const reference = readJson<ReferenceAudit>(path.join(DATA, `${fileStem}.json`));
  const runtime = readJson<{ topics: Array<[string, ...unknown[]]> }>(path.join(DATA, `${subjectId}-runtime.json`));
  const topicIndex = new Map(runtime.topics.map((topic, index) => [topic[0], index]));
  const local = localTargetsFor(subjectId);
  const earliestLocalYear = Math.min(...local.targets.map(target => target.year));
  const associations = [];
  const topics = [];
  const runtimeMap = new Map<string, { target: LocalTarget; topicIndexes: Set<number> }>();

  for (const [variant, variantData] of Object.entries(reference.variants)) {
    const level = levelForVariant(variant);
    for (const topic of variantData.topics) {
      topics.push(topic);
      const index = topicIndex.get(topic.id);
      if (index == null) throw new Error(`${subjectId}: runtime omits ${topic.id}`);
      for (const heading of topic.officialQuestionHeadings) {
        const result = candidatesFor(subjectId, level, heading, local.targets, topic.id);
        const reason = result.parsed.year < earliestLocalYear
          ? 'before-local-corpus'
          : result.reason;
        const matched = result.candidates.length > 0;
        associations.push({
          topicId: topic.id,
          heading,
          level,
          variant,
          resolution: matched ? 'matched' : 'source-blocked',
          ...(matched
            ? { targets: result.candidates.map(targetIdentity) }
            : { reason }),
        });
        for (const target of result.candidates) {
          const key = [target.level, target.lang, target.year, target.paperKey, target.fileid, target.n].join('|');
          const row = runtimeMap.get(key) ?? { target, topicIndexes: new Set<number>() };
          row.topicIndexes.add(index);
          runtimeMap.set(key, row);
        }
      }
    }
  }

  const matched = associations.filter(association => association.resolution === 'matched');
  const blocked = associations.filter(association => association.resolution === 'source-blocked');
  const blockedReasons = [...new Set(blocked.map(association => association.reason!))].sort();
  const sourceBlockedByReason = Object.fromEntries(blockedReasons.map(reason => [
    reason,
    blocked.filter(association => association.reason === reason).length,
  ]));
  const questionMappings = [...runtimeMap.values()]
    .sort((a, b) =>
      a.target.level.localeCompare(b.target.level)
      || b.target.year - a.target.year
      || a.target.paperKey.localeCompare(b.target.paperKey)
      || a.target.fileid.localeCompare(b.target.fileid)
      || Number(a.target.n) - Number(b.target.n))
    .map(({ target, topicIndexes }) => [
      target.level === 'higher' ? 'h' : target.level === 'ordinary' ? 'o' : 'f',
      target.lang === 'ev' ? 'e' : 'i',
      target.year,
      target.paperKey,
      target.fileid,
      target.n,
      [...topicIndexes].sort((a, b) => a - b),
    ]);

  writeJson(path.join(DATA, `${subjectId}-local-crosswalk.json`), {
    schemaVersion: 1,
    subjectId,
    generatedAt: new Date().toISOString(),
    status: blocked.length ? 'exact-current-corpus-mapped-source-completion-pending' : 'complete',
    summary: {
      referenceTopics: topics.length,
      referenceOfficialAssociations: associations.length,
      matchedAssociations: matched.length,
      sourceBlockedAssociations: blocked.length,
      sourceBlockedByReason,
      matchedLocalCardLinks: matched.reduce((sum, association) => sum + (association.targets?.length ?? 0), 0),
      exactRuntimeQuestionMappings: questionMappings.length,
      localAnswerAnchoredPaperVariants: local.paperVariants,
      localAnswerAnchoredPhysicalCards: local.targets.length,
      sourceUnavailableTopics: topics.filter(topic => topic.sourceUnavailable).length,
    },
    policy: {
      matchedSource: 'Entitled local State Examinations Commission corpus only.',
      excludedContent: 'No commercial mock question, solution, note, question text, image, media or provider-hosted PDF is copied.',
      crossCoursePractice: 'A historic official question may appear in an outgoing and a replacement-course shelf only when the factual reference associates it with both.',
      completion: 'A heading is matched only to one unambiguous answer-anchored local SEC card identity.',
    },
    associations,
  });
  writeJson(path.join(DATA, `${subjectId}-question-runtime.json`), {
    schemaVersion: 1,
    subjectId,
    topicIds: runtime.topics.map(topic => topic[0]),
    questionMappings,
  });
  console.log(`${subjectId}: ${matched.length}/${associations.length} matched, ${blocked.length} source blocked, ${questionMappings.length} exact runtime mappings`);
}
