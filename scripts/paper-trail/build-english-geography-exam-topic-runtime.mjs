#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Build compact, student-facing runtime taxonomies from the browser-audited
 * StudyClix metadata snapshots. The source snapshots retain the full factual
 * heading evidence; the runtime deliberately carries hierarchy, counts and
 * the canonical-curriculum bridge only.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const DATA = path.join(ROOT, 'data/examTopics');

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const writeJson = (file, value, pretty = false) => fs.writeFileSync(
  file,
  `${JSON.stringify(value, null, pretty ? 2 : 0)}\n`,
);

const ENGLISH_POETS = {
  adcock: 'english-11-24',
  bishop: 'english-11-0',
  brooks: 'english-11-25',
  browning: 'english-11-26',
  bryce: 'english-11-27',
  dickinson: 'english-11-2',
  donne: 'english-11-3',
  dove: 'english-11-29',
  duffy: 'english-11-30',
  france: 'english-11-31',
  french: 'english-11-51',
  heaney: 'english-11-8',
  hopkins: 'english-11-9',
  hughes: 'english-11-50',
  joseph: 'english-11-32',
  kavanagh: 'english-11-10',
  mahon: 'english-11-15',
  meehan: 'english-11-16',
  morrissey: 'english-11-33',
  muldoon: 'english-11-34',
  'ni chuilleanain': 'english-11-18',
  olusanya: 'english-11-37',
  plath: 'english-11-19',
  rich: 'english-11-20',
  robinson: 'english-11-39',
  seibles: 'english-11-40',
  shakespeare: 'english-11-41',
  shelley: 'english-11-42',
  yeats: 'english-11-23',
};

const ENGLISH_TEXTS = {
  '1984': 'english-12-5',
  "a doll's house": 'english-12-6',
  'a raisin in the sun': 'english-12-7',
  dracula: 'english-12-11',
  'girl on an altar': 'english-12-13',
  hamnet: 'english-12-14',
  room: 'english-12-18',
  'silas marner': 'english-12-31',
  sive: 'english-12-19',
  'the cove': 'english-12-20',
  'the great gatsby': 'english-12-22',
  'the spinning heart': 'english-12-27',
  'the tenant of wildfell hall': 'english-12-28',
  // Preserve the spelling published in the audited reference menu.
  'the tenant of windfell hall': 'english-12-28',
  'the underground railroad': 'english-12-29',
  'wuthering heights': 'english-12-30',
};

const normalise = value => value
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .toLowerCase()
  .trim();

// These IDs are constructed from suffix tuples in curriculumRegistry.ts, so
// the complete strings do not occur literally in that source file.
const GENERATED_CANONICAL_IDS = new Set([
  'geography-2028-1-tectonics',
  'geography-2028-1-rock-cycle',
  'geography-2028-1-surface-processes',
  'geography-2028-1-atmosphere-weather',
  'geography-2028-1-climate',
  'geography-2028-2-human-settlement',
  'geography-2028-2-population-migration',
  'geography-2028-3-agriculture-fisheries',
  'geography-2028-3-tourism',
  'geography-2028-3-globalisation',
  'geography-2028-3-development-assistance',
  'geography-2028-3-geopolitics',
  'geography-2028-u-inquiry-skills',
]);

const englishCurriculumIds = (topic, variant) => {
  const label = normalise(topic.label).replace(/^1 /, '');
  const levelPoetry = variant === 'higher' ? 'english-8-0' : 'english-8-1';
  const direct = {
    'comparative - cultural context': ['english-7-3'],
    'comparative - literary genre': ['english-7-2'],
    'comparative - theme or issue': ['english-7-0'],
    'comparative - theme': ['english-7-0'],
    'comparative - vision & viewpoint': ['english-7-4'],
    'comparative - hero, heroine, villain': ['english-7-5'],
    'comparative - relationships': ['english-7-6'],
    'comparative - social setting': ['english-7-7'],
    composition: ['english-9-1'],
    'reading comprehension': ['english-10-0', 'english-10-1'],
    'unseen poetry': ['english-8-2'],
    hamlet: ['english-6-0', 'english-6-1', 'english-12-0'],
    othello: ['english-6-0', 'english-6-1', 'english-12-3'],
  }[label];
  if (direct) return direct;
  if (label.startsWith('poetry - ')) {
    const poet = label.slice('poetry - '.length);
    return [levelPoetry, ENGLISH_POETS[poet]].filter(Boolean);
  }
  if (label.startsWith('text - ')) {
    const title = label.slice('text - '.length);
    return ['english-6-0', ENGLISH_TEXTS[title]].filter(Boolean);
  }
  throw new Error(`English crosswalk missing: ${topic.label}`);
};

const ENGLISH_ARCHIVE_TOPICS = [
  ['comparative-relationships', 'Comparative - Relationships', ['english-7-6']],
  ['poetry-boland', 'Poetry - Boland', ['english-8-0', 'english-11-1']],
  ['poetry-durcan', 'Poetry - Durcan', ['english-8-0', 'english-11-4']],
  ['poetry-eliot', 'Poetry - Eliot', ['english-8-0', 'english-11-5']],
  ['poetry-frost', 'Poetry - Frost', ['english-8-0', 'english-11-6']],
  ['poetry-hardy', 'Poetry - Hardy', ['english-8-0', 'english-11-7']],
  ['poetry-keats', 'Poetry - Keats', ['english-8-0', 'english-11-11']],
  ['poetry-larkin', 'Poetry - Larkin', ['english-8-0', 'english-11-13']],
  ['poetry-montague', 'Poetry - Montague', ['english-8-0', 'english-11-17']],
  ['poetry-smith', 'Poetry - Smith', ['english-8-0', 'english-11-21']],
  ['poetry-wordsworth', 'Poetry - Wordsworth', ['english-8-0', 'english-11-22']],
];

const OLD_GEOGRAPHY = {
  'Aerial Photos': ['geography-2-8'],
  'Earthquakes & Volcanoes': ['geography-0-7'],
  'Economic - Developing Economies': ['geography-3-1'],
  'Economic - Energy': ['geography-3-5'],
  'Economic - Environmental Impact': ['geography-3-4'],
  'Economic - European Union': ['geography-3-3'],
  'Economic - Ireland & the EU': ['geography-3-3'],
  'Economic - Multinationals & Globalisation': ['geography-3-2'],
  'Elective - Economic': ['geography-3-0', 'geography-3-1', 'geography-3-2', 'geography-3-3', 'geography-3-4', 'geography-3-5'],
  'Elective - Human': ['geography-4-0', 'geography-4-1', 'geography-4-2', 'geography-4-3', 'geography-4-4', 'geography-4-5'],
  Glaciation: ['geography-0-11'],
  'Graph-Style Questions': ['geography-2-0'],
  'Human - Population': ['geography-4-0', 'geography-4-1', 'geography-4-2'],
  'Human - Urban Geography': ['geography-4-3', 'geography-4-4', 'geography-4-5'],
  'Karst Regions': ['geography-0-3'],
  Mapwork: ['geography-2-6'],
  'Option - Atmosphere & Ocean': ['geography-8-0', 'geography-8-1', 'geography-8-2', 'geography-8-3', 'geography-8-4', 'geography-8-5'],
  'Option - Culture & Identity': ['geography-7-0', 'geography-7-1', 'geography-7-2'],
  'Option - Geoecology': ['geography-6-0', 'geography-6-1', 'geography-6-2', 'geography-6-3'],
  'Option - Global Interdependence': ['geography-5-0', 'geography-5-1', 'geography-5-2', 'geography-5-3'],
  'Plate Tectonics': ['geography-0-0'],
  'PROJECT - Investigation': ['geography-2-1', 'geography-2-2', 'geography-2-3', 'geography-2-4', 'geography-2-5'],
  'Regions - Continental': ['geography-1-0', 'geography-1-1', 'geography-1-2', 'geography-1-3', 'geography-1-6'],
  'Regions - European': ['geography-1-0', 'geography-1-1', 'geography-1-2', 'geography-1-3', 'geography-1-5'],
  'Regions - Ireland': ['geography-1-0', 'geography-1-1', 'geography-1-2', 'geography-1-3', 'geography-1-4'],
  Rivers: ['geography-0-4', 'geography-0-5', 'geography-0-6', 'geography-0-9'],
  'Rocks, Weathering & Mass Movement': ['geography-0-1', 'geography-0-2', 'geography-0-4', 'geography-0-5', 'geography-0-6', 'geography-0-8'],
  'Tables/Graphs Questions': ['geography-2-0'],
  'The Sea': ['geography-0-4', 'geography-0-5', 'geography-0-6', 'geography-0-10'],
  'Urban Land Uses': ['geography-4-4'],
  'Weather & Climate': ['geography-2-7'],
};

const newGeographyCurriculumIds = (label) => {
  const value = label.replace(/^S?(?:1|2|3)\.[0-9]+\s+/, '').replace(/^U[1-4]\s+/, '');
  if (/^(Tectonics|Fold Mountains|Volcanic Activity|Earthquakes)$/.test(value)) {
    return ['geography-2028-1-tectonics'];
  }
  if (value === 'Rock Cycle') return ['geography-2028-1-rock-cycle'];
  if (value.startsWith('Surface Processes')) return ['geography-2028-1-surface-processes'];
  if (value === 'Atmosphere and Weather') return ['geography-2028-1-atmosphere-weather'];
  if (value === 'Climate') return ['geography-2028-1-climate'];
  if (value === 'Human Settlement') return ['geography-2028-2-human-settlement'];
  if (value === 'Population' || value === 'Migration') return ['geography-2028-2-population-migration'];
  if (value === 'Agriculture and Fisheries in Ireland') return ['geography-2028-3-agriculture-fisheries'];
  if (value === 'Tourism') return ['geography-2028-3-tourism'];
  if (value === 'Globalisation') return ['geography-2028-3-globalisation'];
  if (value === 'Development, Assistance and Cooperation') return ['geography-2028-3-development-assistance'];
  if (value === 'Geopolitics') return ['geography-2028-3-geopolitics'];
  if (/^(Aerial Photography|Ordnance Survey Mapwork|Graphical Interpretation and Analysis|Applied Geography Project)/.test(value)) {
    return ['geography-2028-u-inquiry-skills'];
  }
  throw new Error(`New Geography crosswalk missing: ${label}`);
};

const geographyCurriculumIds = (topic, variant) => {
  if (variant.endsWith('new-course')) return newGeographyCurriculumIds(topic.label);
  const ids = OLD_GEOGRAPHY[topic.label];
  if (!ids) throw new Error(`Outgoing Geography crosswalk missing: ${topic.label}`);
  return ids;
};

const HOME_ECONOMICS = {
  'Consumer Studies': ['home-economics-1-2'],
  'Diet & Health': ['home-economics-0-0', 'home-economics-0-1'],
  'Elective 1: Energy & Emissions': ['home-economics-1-5', 'home-economics-3-6'],
  'Elective 1: Heating, Water, Lighting...': ['home-economics-1-3', 'home-economics-3-5'],
  'Elective 1: Housing (Planning, Building...)': ['home-economics-3-0', 'home-economics-3-3'],
  'Elective 1: Irish Housing': ['home-economics-3-0', 'home-economics-3-3'],
  'Elective 1: Interior Design': ['home-economics-3-0', 'home-economics-3-4'],
  'Elective 2: Fabrics': ['home-economics-1-4', 'home-economics-3-1', 'home-economics-3-7'],
  'Elective 2: Patterns & Fashion': ['home-economics-3-1', 'home-economics-3-8'],
  'Elective 3: (Un)employment & Poverty': ['home-economics-2-2', 'home-economics-3-2', 'home-economics-3-9'],
  'Elective 3: Education in Ireland': ['home-economics-2-2', 'home-economics-3-2', 'home-economics-3-10'],
  'Elective 3: Family Life & Leisure': ['home-economics-2-0', 'home-economics-2-2', 'home-economics-3-2', 'home-economics-3-11'],
  Energy: ['home-economics-1-3'],
  Environment: ['home-economics-1-5'],
  'Food Assignments': ['home-economics-0-0', 'home-economics-0-3'],
  'Food Industry & Packaging': ['home-economics-0-11'],
  'Food Spoilage & Food Safety': ['home-economics-0-4'],
  'Foods: Meat, Fish, Cereal, Fruit/Veg, Dairy, Eggs': ['home-economics-0-2', 'home-economics-0-9'],
  'Household Appliances': ['home-economics-1-3'],
  'Household Finances': ['home-economics-1-0', 'home-economics-1-1'],
  'Marriage & Family Law': ['home-economics-2-1'],
  'Meal Planning & Preparation': ['home-economics-0-3', 'home-economics-0-10'],
  'Nutrition: Carbohydrates': ['home-economics-0-6'],
  'Nutrition: Lipids': ['home-economics-0-7'],
  'Nutrition: Protein': ['home-economics-0-5'],
  'Nutrition: Vitamins and Minerals': ['home-economics-0-8'],
  'Older Persons': ['home-economics-2-3'],
  Textiles: ['home-economics-1-4', 'home-economics-3-1'],
  'The Family': ['home-economics-2-0', 'home-economics-2-1'],
};

const homeEconomicsCurriculumIds = (topic) => {
  const ids = HOME_ECONOMICS[topic.label];
  if (!ids) throw new Error(`Home Economics crosswalk missing: ${topic.label}`);
  return ids;
};

const MATHEMATICS = {
  'Algebra - Cubics': ['mathematics-3-0', 'mathematics-3-1'],
  'Algebra - Expressions & Factorising': ['mathematics-3-0'],
  'Algebra - Inequalities': ['mathematics-3-2'],
  'Algebra - Quadratics': ['mathematics-3-0', 'mathematics-3-1'],
  'Algebra - Simultaneous Equations': ['mathematics-3-1'],
  'Algebra - Solving Equations': ['mathematics-3-1'],
  Algebra: ['mathematics-2-1', 'mathematics-2-4', 'mathematics-3-0', 'mathematics-3-1', 'mathematics-3-2'],
  'Algebra - Equations': ['mathematics-3-1'],
  'Area & Volume': ['mathematics-2-3'],
  Arithmetic: ['mathematics-2-2', 'mathematics-2-5'],
  'Co-Ordinate Geometry of the Circle': ['mathematics-1-1'],
  'Co-Ordinate Geometry of the Line': ['mathematics-1-1'],
  'Co-Ordinate Geometry the Circle': ['mathematics-1-1'],
  'Complex Numbers': ['mathematics-3-3'],
  Counting: ['mathematics-0-0'],
  'Data & Statistics': ['mathematics-0-3', 'mathematics-0-4', 'mathematics-0-5', 'mathematics-0-6'],
  'Differentiation - Applications': ['mathematics-4-1'],
  'Differentiation - Rules': ['mathematics-4-1'],
  Differentiation: ['mathematics-4-1'],
  'Financial Maths': ['mathematics-2-2', 'mathematics-2-5'],
  Functions: ['mathematics-4-0'],
  'Graphing Functions': ['mathematics-4-0'],
  'Graphs of Functions': ['mathematics-4-0'],
  Geometry: ['mathematics-1-0', 'mathematics-1-3'],
  'Geometry - Constructions & Proofs': ['mathematics-1-0'],
  'Geometry (Proofs and Constructions)': ['mathematics-1-0'],
  Indices: ['mathematics-2-1'],
  'Indices and Logs': ['mathematics-2-0', 'mathematics-2-1'],
  Induction: ['mathematics-3-4'],
  Integration: ['mathematics-4-1'],
  'Number Systems': ['mathematics-2-0'],
  Probability: ['mathematics-0-0', 'mathematics-0-1', 'mathematics-0-2'],
  'Sequences & Series': ['mathematics-2-4'],
  Statistics: ['mathematics-0-3', 'mathematics-0-4', 'mathematics-0-5', 'mathematics-0-6'],
  'Statistics - Descriptive Statistics': ['mathematics-0-3', 'mathematics-0-4', 'mathematics-0-5', 'mathematics-0-6'],
  'Statistics - Inferential Statistics': ['mathematics-0-3', 'mathematics-0-6'],
  'Statistics - Z Scores': ['mathematics-0-3', 'mathematics-0-6'],
  Trigonometry: ['mathematics-1-2'],
  'Trigonometry - Functions & Identities': ['mathematics-1-2'],
  'Trigonometry - Triangles': ['mathematics-1-2'],
};

const mathematicsCurriculumIds = (topic) => {
  const ids = MATHEMATICS[topic.label];
  if (!ids) throw new Error(`Mathematics crosswalk missing: ${topic.label}`);
  return ids;
};

const PE_OUTGOING = {
  '1. Learning and Improving Skill & Technique: Ability and Skilled Performance': ['physical-education-0-0', 'physical-education-0-1', 'physical-education-0-3'],
  '1. Learning and Improving Skill & Technique: Biomechanics': ['physical-education-0-2'],
  '1. Learning and Improving Skill & Technique': ['physical-education-0-0', 'physical-education-0-1', 'physical-education-0-2', 'physical-education-0-3'],
  '2. Physical Demands of Performance': ['physical-education-0-4', 'physical-education-0-5', 'physical-education-0-6', 'physical-education-0-7', 'physical-education-0-8', 'physical-education-0-9'],
  '2. Physical/Psychological Demands of Performance: Diet, Nutrition, Hydration and Energy Systems': ['physical-education-0-12'],
  '2. Physical/Psychological Demands of Performance: Training Methods and Fitness Planning': ['physical-education-0-5', 'physical-education-0-6', 'physical-education-0-7', 'physical-education-0-8', 'physical-education-0-9', 'physical-education-0-10'],
  '2. Psychological Demands of Performance': ['physical-education-0-11'],
  '2. Physical & Psychological Demands of Performance': ['physical-education-0-4', 'physical-education-0-5', 'physical-education-0-6', 'physical-education-0-7', 'physical-education-0-8', 'physical-education-0-9', 'physical-education-0-10', 'physical-education-0-11', 'physical-education-0-12'],
  '3. Structures, Strategies, Roles & Conventions': ['physical-education-0-13', 'physical-education-0-14', 'physical-education-0-15', 'physical-education-0-16', 'physical-education-0-17', 'physical-education-0-18', 'physical-education-0-19', 'physical-education-2-0', 'physical-education-2-1', 'physical-education-2-2', 'physical-education-2-3', 'physical-education-2-4', 'physical-education-2-5'],
  '4. Planning for Optimum Performance': ['physical-education-0-20', 'physical-education-0-21', 'physical-education-0-22', 'physical-education-0-23', 'physical-education-0-24', 'physical-education-2-0', 'physical-education-2-1', 'physical-education-2-2', 'physical-education-2-3', 'physical-education-2-4', 'physical-education-2-5'],
  '5. Promoting Physical Activity': ['physical-education-1-0', 'physical-education-1-1', 'physical-education-1-2', 'physical-education-1-3', 'physical-education-1-4'],
  '6. Ethics & Fair Play': ['physical-education-1-5', 'physical-education-1-6', 'physical-education-1-7', 'physical-education-1-8', 'physical-education-1-9', 'physical-education-1-10'],
  '7. Physical Activity & Inclusion': ['physical-education-1-11', 'physical-education-1-12', 'physical-education-1-13', 'physical-education-1-14', 'physical-education-1-15'],
  '8. Technology, Media & Sport': ['physical-education-1-16', 'physical-education-1-17', 'physical-education-1-18'],
  '9. Gender & Physical Activity': ['physical-education-1-19', 'physical-education-1-20', 'physical-education-1-21', 'physical-education-1-22'],
  'Business & Enterprise in Physical Activity & Sport': ['physical-education-1-23', 'physical-education-1-24', 'physical-education-1-25', 'physical-education-1-26', 'physical-education-1-27'],
};

const physicalEducationCurriculumIds = (topic, variant) => {
  if (variant.endsWith('new-course')) {
    if (topic.groupId?.startsWith('strand-1-')) return ['physical-education-2028-skill-performance'];
    if (topic.groupId?.startsWith('strand-2-')) return ['physical-education-2028-demands-performance'];
    if (topic.groupId?.startsWith('strand-3-')) return ['physical-education-2028-participation-factors'];
    throw new Error(`New Physical Education group missing: ${topic.id}`);
  }
  const ids = PE_OUTGOING[topic.label];
  if (!ids) throw new Error(`Outgoing Physical Education crosswalk missing: ${topic.label}`);
  return ids;
};

const build = ({ subjectId, referenceFile = `${subjectId}.json`, curriculumIds, archives = [] }) => {
  const reference = readJson(path.join(DATA, referenceFile));
  const variants = Object.entries(reference.variants);
  const topicRows = [];
  const groups = [];
  const crosswalk = {};

  for (const [variant, source] of variants) {
    const levelCode = variant.startsWith('higher') ? 'h' : variant.startsWith('foundation') ? 'f' : 'o';
    const courseCode = variant.endsWith('new-course') ? 'n'
      : variants.some(([name]) => name.endsWith('new-course')) ? 'o' : 'c';
    const indexes = [];
    for (const topic of source.topics) {
      const ids = curriculumIds(topic, variant);
      if (!ids.length) throw new Error(`${topic.id}: empty curriculum crosswalk`);
      crosswalk[topic.id] = ids;
      indexes.push(topicRows.length);
      topicRows.push([
        topic.id,
        topic.label,
        topic.sourcePath,
        topic.mockQuestionCount,
        topic.providerSampleQuestionCount,
        ids,
        levelCode,
        topic.reportedQuestionCount,
        courseCode,
        topic.sourceUnavailable ? 1 : 0,
      ]);
    }
    if (source.groups.length) {
      for (const group of source.groups) {
        groups.push([
          levelCode,
          courseCode,
          group.id,
          `${source.label} · ${group.label}`,
          group.topicIds.map(id => {
            const index = topicRows.findIndex(row => row[0] === id);
            if (index < 0) throw new Error(`${group.id}: unknown topic ${id}`);
            return index;
          }),
        ]);
      }
    } else {
      groups.push([levelCode, courseCode, `${subjectId}-${variant}`, source.label, indexes]);
    }
  }

  if (archives.length) {
    const indexes = [];
    for (const [slug, label, ids] of archives) {
      const id = `${subjectId}-higher-${slug}-archive`;
      crosswalk[id] = ids;
      indexes.push(topicRows.length);
      topicRows.push([
        id,
        label,
        `/nextstepuni-preservation/${subjectId}/higher/${slug}`,
        0,
        0,
        ids,
        'h',
        0,
        'c',
      ]);
    }
    groups.push([
      'h',
      'c',
      `${subjectId}-higher-local-archive`,
      'Higher Level · Historical local archive',
      indexes,
    ]);
  }

  const sourceText = [
    fs.readFileSync(path.join(ROOT, 'curriculum.ts'), 'utf8'),
    fs.readFileSync(path.join(ROOT, 'curriculumRegistry.ts'), 'utf8'),
  ].join('\n');
  for (const [topicId, ids] of Object.entries(crosswalk)) {
    for (const id of ids) {
      if (!sourceText.includes(id) && !GENERATED_CANONICAL_IDS.has(id)) {
        throw new Error(`${topicId}: unknown canonical node ${id}`);
      }
    }
  }
  if (Object.keys(crosswalk).length !== topicRows.length) {
    throw new Error(`${subjectId}: crosswalk/topic count mismatch`);
  }

  const runtime = {
    v: 1,
    subjectId,
    capturedAt: reference.capturedAt,
    referenceProvider: reference.reference.provider,
    groups,
    topics: topicRows,
  };
  writeJson(path.join(DATA, `${subjectId}-runtime.json`), runtime);
  writeJson(path.join(DATA, `${subjectId}-curriculum-crosswalk.json`), crosswalk, true);
  return {
    subjectId,
    referenceTopics: variants.reduce((sum, [, source]) => sum + source.topics.length, 0),
    archiveTopics: archives.length,
    runtimeTopics: topicRows.length,
    groups: groups.length,
  };
};

const summaries = [
  build({
    subjectId: 'english',
    curriculumIds: englishCurriculumIds,
    archives: ENGLISH_ARCHIVE_TOPICS,
  }),
  build({
    subjectId: 'geography',
    curriculumIds: geographyCurriculumIds,
  }),
  build({
    subjectId: 'home-economics-s-and-s',
    referenceFile: 'home-economics.json',
    curriculumIds: homeEconomicsCurriculumIds,
  }),
  build({
    subjectId: 'mathematics',
    curriculumIds: mathematicsCurriculumIds,
  }),
  build({
    subjectId: 'physical-education',
    curriculumIds: physicalEducationCurriculumIds,
  }),
];

console.log(JSON.stringify(summaries, null, 2));
