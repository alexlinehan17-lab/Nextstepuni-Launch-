/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Canonical curriculum registry.
 *
 * This is the public gateway for curriculum data.  A subject name alone is not
 * enough to identify a syllabus: specifications overlap while cohorts move
 * from an outgoing syllabus to a redeveloped one.  Consumers must resolve a
 * subject together with the student's examination year.
 *
 * `curriculum.ts` is retained as the legacy data adapter while content is
 * migrated.  Mark Bank's verified redeveloped taxonomies are also adapted here.
 * New product code should use this registry rather than importing either data
 * set directly.
 */
import {
  CURRICULUM,
  type CurriculumCategory,
  type CurriculumLevel,
} from './curriculum';
import { SUBJECTS as MARK_BANK_SUBJECTS } from './components/MarkBank/deck';

export type CurriculumAuthority = 'Curriculum Online' | 'NCCA' | 'SEC';
export type CurriculumAuditStatus = 'verified' | 'provisional' | 'audit-required';
export type CurriculumProgramme =
  | 'leaving-certificate-established'
  | 'leaving-certificate-applied'
  | 'junior-cycle'
  | 'lcvp'
  | 'recognised-non-curricular-language'
  | 'retired';

export interface CurriculumSource {
  authority: CurriculumAuthority;
  title: string;
  url: string;
  role: 'content' | 'assessment' | 'transition';
}

export interface CanonicalCurriculumTopic {
  id: string;
  code?: string;
  title: string;
  aliases?: string[];
}

export interface CanonicalCurriculumGroup {
  id: string;
  code?: string;
  title: string;
  label?: string;
  topics: CanonicalCurriculumTopic[];
}

export interface CurriculumSelectionRule {
  id: string;
  description: string;
  requiredGroupIds?: string[];
  choose?: number;
  fromGroupIds?: string[];
  appliesTo: 'written-examination' | 'coursework' | 'programme';
}

export type CurriculumAssessmentKind =
  | 'written-examination'
  | 'project'
  | 'coursework'
  | 'practical-examination'
  | 'oral-examination'
  | 'aural-examination';

export interface CurriculumAssessmentComponent {
  id: string;
  title: string;
  kind: CurriculumAssessmentKind;
  weighting: number;
  levels: CurriculumLevel[];
  required: boolean;
  durationMinutes?: number;
  notes?: string[];
}

export interface CanonicalCurriculumSpecification {
  id: string;
  subjectId: string;
  subjectName: string;
  programme: CurriculumProgramme;
  category: CurriculumCategory;
  levels: CurriculumLevel[];
  title: string;
  firstExamYear?: number;
  lastExamYear?: number;
  status: CurriculumAuditStatus;
  sources: CurriculumSource[];
  groups: CanonicalCurriculumGroup[];
  /** The node granularity students track as syllabus coverage. */
  coverageNodeLevel: 'group' | 'topic';
  selectionRules?: CurriculumSelectionRule[];
  assessmentComponents?: CurriculumAssessmentComponent[];
  recommendedClassHours?: number;
  notes?: string[];
}

const OFFICIAL = {
  curriculumOverview: 'https://www.curriculumonline.ie/senior-cycle/curriculum/',
  biology: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/biology/',
  chemistry: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/chemistry/',
  physics: 'https://curriculumonline.ie/senior-cycle/senior-cycle-subjects/physics/',
  business: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/business/',
  agriculturalScience: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/agricultural-science/',
  appliedMathematics: 'https://curriculumonline.ie/senior-cycle/senior-cycle-subjects/applied-mathematics/',
  appliedMathematicsSpecification: 'https://curriculumonline.ie/getmedia/1d61d7b6-573d-4e2a-83ea-037ef17b083b/Leaving-Certificate-Specification-Applied-Mathematics_EN.pdf',
  geography: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/geography/',
  geographyGuidelines: 'https://www.curriculumonline.ie/getmedia/e7c30be5-df65-4d0b-8377-7bed94697978/SCSEC17_Geography_guidelines_eng.pdf',
  geographySpecification: 'https://www.curriculumonline.ie/getmedia/837bf939-b559-4b45-8c94-5590d8710083/SC-Geography-Spec-ENG-INT.pdf',
  history: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/history/',
  historySyllabus: 'https://www.curriculumonline.ie/getmedia/da556505-f5fb-4921-869f-e0983fd80e50/SCSEC20_History_syllabus_eng.pdf',
  homeEconomics: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/home-economics/',
  homeEconomicsSyllabus: 'https://www.curriculumonline.ie/getmedia/b9bc688f-3a5d-48a7-90f1-b60063f49c74/SCSEC21_Home_Economics_syllabus_eng.pdf',
  english: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/english/',
  gaeilge: 'https://curriculumonline.ie/senior-cycle/senior-cycle-subjects/gaeilge/',
  mathematics: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/mathematics/',
  french: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/french/',
  accounting: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/accounting/',
  constructionStudies: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/construction-studies/',
  constructionTechnologySpecification: 'https://curriculumonline.ie/getmedia/8a5f525f-b3d4-4d0d-ae60-11fed5c4076c/SC-Construction-Technology-Spec-ENG.pdf',
  engineering: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/engineering/',
  physicalEducation: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/physical-education-specification/',
  computerScience: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/computer-science/',
  computerScienceAssessment: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/computer-science/assessment/',
  economics: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/economics/',
  economicsSpecification: 'https://www.curriculumonline.ie/getmedia/3342d8a2-1e22-4f17-b82b-a8134fe16eb3/LCEconomics_0219_EN.pdf',
  politicsAndSociety: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/politics-and-society/',
  politicsAndSocietyAssessment: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/politics-and-society/assessment/',
  art: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/art/',
  artAssessment: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/art/assessment%20for%20certification/',
  lcvp: 'https://www.curriculumonline.ie/senior-cycle/leaving-certificate-vocational-programme-%28lcvp%29/',
  religiousEducation: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/religious-education/',
  religiousEducationSyllabus: 'https://curriculumonline.ie/getmedia/55900bde-5836-4eef-b94c-d569b31d5b70/SCSEC29_Religious_Ed_syllabus_eng.pdf',
  ancientGreek: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/ancient-greek/',
  ancientGreekSyllabus: 'https://www.curriculumonline.ie/getmedia/ea4356e5-c4da-4fc3-958d-257552d72f15/SCSEC03_Ancient-Greek_Syllabus_English.pdf',
  latin: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/latin/',
  latinSyllabus: 'https://www.curriculumonline.ie/getmedia/632b5943-aa68-4758-b2b8-d6390a6636de/SCSEC24_Latin_syllabus_Eng.pdf',
  arabic: 'https://curriculumonline.ie/senior-cycle/senior-cycle-subjects/arabic/',
  arabicSyllabus: 'https://www.curriculumonline.ie/getmedia/f9c08339-ef8a-4096-b5d4-8862d02efe9b/SCSEC05_Arabic_Syllabus_English.pdf',
  classicalStudies: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/classical-studies/',
  classicalStudiesSpecification: 'https://www.curriculumonline.ie/getmedia/4f756b6f-29c2-4651-bf1e-06739dee2106/Leaving_Certificate_Specification-Classical_Studies_EN.pdf',
  dcg: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/design-and-communication-graphics/',
  dcgSyllabus: 'https://curriculumonline.ie/getmedia/c288dafe-12a9-4641-b5bb-382b99871423/SCSEC33_Design_Comm_Graphics_syllabus_eng.pdf',
  technology: 'https://curriculumonline.ie/senior-cycle/senior-cycle-subjects/technology/',
  technologySyllabus: 'https://curriculumonline.ie/getmedia/da63d79a-b84f-4b8c-ba06-a4cb1fd21e07/SCSEC34_Technology_syllabus_eng.pdf',
  music: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/music/',
  musicSyllabus: 'https://www.curriculumonline.ie/getmedia/85bfed8e-207e-4fbc-b8ed-3120cd979a4b/SCSEC26_Music_syllabus_eng.pdf',
  german: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/german/',
  spanish: 'https://www.curriculumonline.ie/Senior-Cycle/Senior-Cycle-Subjects/Spanish/',
  italian: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/italian/',
  japanese: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/japanese/',
  russian: 'https://curriculumonline.ie/senior-cycle/senior-cycle-subjects/russian/',
  hebrewStudies: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/hebrew-studies/',
  hebrewStudiesSyllabus: 'https://www.curriculumonline.ie/getmedia/7c6e16cb-4582-4836-b329-89e3e5f0f1c6/SCSEC19_Hebrew_syllabus_eng.pdf',
  physicsAndChemistry: 'https://curriculumonline.ie/senior-cycle/senior-cycle-subjects/physics-and-chemistry/',
  physicsAndChemistrySyllabus: 'https://www.curriculumonline.ie/getmedia/a3c83bc8-6b45-4076-bd09-5f25a07c5c98/SCSEC28_physicsChem_syllabus_eng.pdf',
  polish: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/polish/',
  lithuanian: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/lithuanian/',
  portuguese: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/portuguese/',
  mandarinChinese: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/mandarin-chinese/',
} as const;

const RECOGNISED_NON_CURRICULAR_LANGUAGE_IDS = new Set([
  'bulgarian', 'croatian', 'czech', 'danish', 'dutch', 'estonian', 'finnish',
  'hungarian', 'latvian', 'maltese', 'modern-greek', 'romanian', 'slovakian',
  'slovenian', 'swedish', 'ukrainian',
]);

function programmeForSubjectId(subjectId: string): CurriculumProgramme {
  if (subjectId.startsWith('jc-')) return 'junior-cycle';
  if (subjectId.startsWith('lca-')) return 'leaving-certificate-applied';
  if (subjectId === 'lcvp-link-modules') return 'lcvp';
  if (RECOGNISED_NON_CURRICULAR_LANGUAGE_IDS.has(subjectId)) return 'recognised-non-curricular-language';
  if (subjectId === 'agricultural-economics' || subjectId === 'history-early-modern') return 'retired';
  return 'leaving-certificate-established';
}

const legacySpecifications: CanonicalCurriculumSpecification[] = CURRICULUM.map((subject) => ({
  id: `${subject.id}:legacy-current`,
  subjectId: subject.id,
  subjectName: subject.name,
  programme: programmeForSubjectId(subject.id),
  category: subject.category,
  levels: subject.levels,
  title: `${subject.name} — legacy/current taxonomy`,
  status: 'audit-required',
  sources: [{
    authority: 'Curriculum Online',
    title: 'Senior Cycle curriculum overview',
    url: OFFICIAL.curriculumOverview,
    role: 'content',
  }],
  groups: subject.strands.map((strand) => ({
    id: strand.id,
    title: strand.name,
    topics: strand.subtopics
      .filter((topic): topic is { id: string; name: string } => Boolean(topic.id))
      .map((topic) => ({ id: topic.id, title: topic.name })),
  })),
  coverageNodeLevel: 'group',
  notes: ['Imported from the pre-registry taxonomy; official subject-level verification is still required.'],
}));

const transitionSubjects: Record<string, {
  firstExamYear: number;
  source: string;
  title: string;
}> = {
  biology: { firstExamYear: 2027, source: OFFICIAL.biology, title: 'Leaving Certificate Biology' },
  chemistry: { firstExamYear: 2027, source: OFFICIAL.chemistry, title: 'Leaving Certificate Chemistry' },
  physics: { firstExamYear: 2027, source: OFFICIAL.physics, title: 'Leaving Certificate Physics' },
  business: { firstExamYear: 2027, source: OFFICIAL.business, title: 'Leaving Certificate Business' },
  'agricultural-science': { firstExamYear: 2021, source: OFFICIAL.agriculturalScience, title: 'Leaving Certificate Agricultural Science' },
};

const redevelopedSpecifications: CanonicalCurriculumSpecification[] = MARK_BANK_SUBJECTS.map((subject) => {
  const transition = transitionSubjects[subject.id];
  const legacy = CURRICULUM.find((entry) => entry.id === subject.id);
  return {
    id: `${subject.id}:${transition.firstExamYear}`,
    subjectId: subject.id,
    subjectName: subject.title,
    programme: 'leaving-certificate-established',
    category: legacy?.category ?? 'other',
    levels: legacy?.levels ?? ['higher', 'ordinary'],
    title: `${transition.title} — specification examined from ${transition.firstExamYear}`,
    firstExamYear: transition.firstExamYear,
    status: 'verified',
    sources: [{
      authority: 'Curriculum Online',
      title: transition.title,
      url: transition.source,
      role: 'content',
    }],
    groups: subject.strands.map((strand) => ({
      id: `${subject.id}:${strand.id}`,
      title: strand.title,
      label: strand.label,
      topics: strand.topics.map((topic) => ({
        id: topic.id,
        code: topic.code,
        title: topic.title,
      })),
    })),
    coverageNodeLevel: 'topic',
  };
});

const constructionTechnologySpecification: CanonicalCurriculumSpecification = {
  id: 'construction-technology:2028',
  // Keep the established subject identity stable so historic selections and mastery survive the rename.
  subjectId: 'construction-studies',
  subjectName: 'Construction Technology',
  programme: 'leaving-certificate-established',
  category: 'practical-applied',
  levels: ['higher', 'ordinary'],
  title: 'Leaving Certificate Construction Technology — specification examined from 2028',
  firstExamYear: 2028,
  status: 'verified',
  sources: [
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Construction Technology curriculum specification',
      url: OFFICIAL.constructionTechnologySpecification,
      role: 'content',
    },
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Construction Technology assessment for certification',
      url: OFFICIAL.constructionTechnologySpecification,
      role: 'assessment',
    },
  ],
  recommendedClassHours: 180,
  groups: [
    {
      id: 'construction-technology-built-environment',
      code: '1',
      title: 'Built Environment',
      topics: [
        ['design-principles', 'Design principles of a domestic dwelling'],
        ['architectural-heritage', 'Environmental and architectural heritage of dwellings'],
        ['urban-rural-design', 'Urban and rural design of a dwelling'],
        ['health-safety', 'Personal safety and safety on a construction site'],
        ['universal-design', 'Universal Design applied to a domestic dwelling'],
      ].map(([suffix, title], index) => ({
        id: `construction-technology-1-${suffix}`,
        code: `1.${index + 1}`,
        title,
      })),
    },
    {
      id: 'construction-technology-design-materials-craft',
      code: '2',
      title: 'Design, Materials, and Craft Skills',
      topics: [
        ['sustainable-materials', 'Sustainable use of materials'],
        ['material-properties', 'Materials properties and use'],
        ['design-skills', 'Design skills'],
        ['project-management', 'Project management'],
        ['craft-skills', 'Craft skills, processes and techniques'],
        ['graphical-communication', 'Graphical communication'],
        ['communication-skills', 'Communication skills'],
        ['personal-reflection', 'Personal reflection'],
      ].map(([suffix, title], index) => ({
        id: `construction-technology-2-${suffix}`,
        code: `2.${index + 1}`,
        title,
      })),
    },
    {
      id: 'construction-technology-building-fabric',
      code: '3',
      title: 'Building Fabric',
      topics: [
        ['construction-principles', 'Construction principles for a domestic dwelling'],
        ['fabric-functions', 'Functions of the building fabric in a domestic dwelling'],
        ['substructure-superstructure', 'Substructure and superstructure'],
        ['passive-design', 'Passive design'],
        ['resilient-design', 'Resilient design'],
        ['health-wellness-comfort', 'Design for health, wellness and comfort'],
        ['ecological-design', 'Ecological building design'],
        ['regulations-standards', 'Building regulations and standards'],
      ].map(([suffix, title], index) => ({
        id: `construction-technology-3-${suffix}`,
        code: `3.${index + 1}`,
        title,
      })),
    },
    {
      id: 'construction-technology-services-control',
      code: '4',
      title: 'Services and Control Technology',
      topics: [
        ['indoor-environment', 'Indoor dwelling environment'],
        ['heat-energy', 'Heat energy and scientific calculations in dwellings'],
        ['operational-carbon', 'Operational carbon of a domestic dwelling'],
        ['airtightness', 'Airtightness in a domestic dwelling'],
        ['ventilation', 'Ventilation in a domestic dwelling'],
        ['energy-heating', 'Energy sources and space heating systems in domestic houses'],
        ['water-supply', 'Water supply in a domestic dwelling'],
        ['electricity', 'Electricity in a domestic dwelling'],
        ['drainage', 'Drainage systems for a domestic dwelling'],
        ['smart-home', 'Smart home technologies'],
      ].map(([suffix, title], index) => ({
        id: `construction-technology-4-${suffix}`,
        code: `4.${index + 1}`,
        title,
      })),
    },
  ],
  coverageNodeLevel: 'topic',
  assessmentComponents: [
    {
      id: 'construction-technology-constructed-environment',
      title: 'Exploring the Constructed Environment',
      kind: 'project',
      weighting: 30,
      levels: ['higher', 'ordinary'],
      required: true,
      notes: ['Completed in response to a common brief issued annually by the SEC.'],
    },
    {
      id: 'construction-technology-craft-skills',
      title: 'Craft Skills Assessment',
      kind: 'practical-examination',
      weighting: 20,
      levels: ['higher', 'ordinary'],
      required: true,
      notes: ['Common prescribed task.'],
    },
    {
      id: 'construction-technology-written-examination',
      title: 'Written examination',
      kind: 'written-examination',
      weighting: 50,
      levels: ['higher', 'ordinary'],
      required: true,
    },
  ],
  notes: [
    'Introduced to fifth-year students in September 2026.',
    'The topic nodes reproduce the official “Students learn about” headings rather than the outgoing Construction Studies taxonomy.',
  ],
};

const geography2028Specification: CanonicalCurriculumSpecification = {
  id: 'geography:2028',
  subjectId: 'geography',
  subjectName: 'Geography',
  programme: 'leaving-certificate-established',
  category: 'social-environmental',
  levels: ['higher', 'ordinary'],
  title: 'Leaving Certificate Geography — specification examined from 2028',
  firstExamYear: 2028,
  status: 'verified',
  sources: [
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Geography curriculum specification',
      url: OFFICIAL.geographySpecification,
      role: 'content',
    },
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Geography assessment for certification',
      url: OFFICIAL.geographySpecification,
      role: 'assessment',
    },
  ],
  recommendedClassHours: 180,
  groups: [
    {
      id: 'geography-2028-applying-thinking-skills',
      code: 'U',
      title: 'Applying geographical thinking and skills',
      label: 'Unifying strand',
      topics: [
        ['value-importance', 'The value and importance of geography'],
        ['key-concepts', 'Key concepts in geography'],
        ['inquiry-skills', 'Geographical inquiry and skills'],
      ].map(([suffix, title], index) => ({
        id: `geography-2028-u-${suffix}`,
        code: `U.${index + 1}`,
        title,
      })),
    },
    {
      id: 'geography-2028-physical-environment',
      code: '1',
      title: 'The physical environment',
      topics: [
        ['tectonics', 'Tectonics'],
        ['rock-cycle', 'Rock cycle'],
        ['surface-processes', 'Surface processes'],
        ['atmosphere-weather', 'Atmosphere and weather'],
        ['climate', 'Climate'],
      ].map(([suffix, title], index) => ({
        id: `geography-2028-1-${suffix}`,
        code: `1.${index + 1}`,
        title,
      })),
    },
    {
      id: 'geography-2028-human-environment',
      code: '2',
      title: 'The human environment',
      topics: [
        ['human-settlement', 'Human settlement'],
        ['population-migration', 'Population and migration'],
      ].map(([suffix, title], index) => ({
        id: `geography-2028-2-${suffix}`,
        code: `2.${index + 1}`,
        title,
      })),
    },
    {
      id: 'geography-2028-global-environment',
      code: '3',
      title: 'The global environment',
      topics: [
        ['agriculture-fisheries', 'Agriculture and fisheries'],
        ['tourism', 'Tourism'],
        ['globalisation', 'Globalisation'],
        ['development-assistance', 'Development assistance and cooperation'],
        ['geopolitics', 'Geopolitics'],
      ].map(([suffix, title], index) => ({
        id: `geography-2028-3-${suffix}`,
        code: `3.${index + 1}`,
        title,
      })),
    },
  ],
  coverageNodeLevel: 'topic',
  assessmentComponents: [
    {
      id: 'geography-2028-applied-project',
      title: 'Applied Geography Project',
      kind: 'project',
      weighting: 40,
      levels: ['higher', 'ordinary'],
      required: true,
      notes: ['Completed in response to a common brief issued annually by the SEC.'],
    },
    {
      id: 'geography-2028-written-examination',
      title: 'Written examination',
      kind: 'written-examination',
      weighting: 60,
      levels: ['higher', 'ordinary'],
      required: true,
    },
  ],
  notes: [
    'Introduced to fifth-year students in September 2026.',
    'The topic nodes reproduce the official “Students learn about” headings rather than the outgoing Geography taxonomy.',
  ],
};

function canonicalGroup(
  id: string,
  title: string,
  topicTitles: Array<[id: string, title: string]>,
): CanonicalCurriculumGroup {
  return {
    id,
    title,
    topics: topicTitles.map(([topicId, topicTitle]) => ({ id: topicId, title: topicTitle })),
  };
}

function patchLegacySpecification(spec: CanonicalCurriculumSpecification): CanonicalCurriculumSpecification {
  if (spec.subjectId === 'ancient-greek') {
    return {
      ...spec,
      id: 'ancient-greek:outgoing-2026',
      title: 'Leaving Certificate Ancient Greek syllabus — examination to June 2026',
      lastExamYear: 2026,
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Ancient Greek transition information', url: OFFICIAL.ancientGreek, role: 'transition' },
        { authority: 'NCCA', title: 'Leaving Certificate Ancient Greek syllabus', url: OFFICIAL.ancientGreekSyllabus, role: 'content' },
      ],
      groups: [
        canonicalGroup('ancient-greek-2026-language-texts', 'Language and texts', [
          ['ancient-greek-2026-composition-comprehension', 'Composition or comprehension'],
          ['ancient-greek-2026-scansion', 'Scansion'],
          ['ancient-greek-2026-prescribed-texts', 'Prescribed texts'],
          ['ancient-greek-2026-unprescribed-prose', 'Unprescribed prose'],
          ['ancient-greek-2026-unprescribed-verse', 'Unprescribed verse'],
        ]),
        canonicalGroup('ancient-greek-2026-history', 'Greek history', [
          ['ancient-greek-2026-peloponnesian-war-alexander', 'From the Peloponnesian War to the death of Alexander'],
          ['ancient-greek-2026-athens-sparta', 'Athenian and Spartan constitutional history'],
        ]),
        canonicalGroup('ancient-greek-2026-literature', 'Greek literature', [
          ['ancient-greek-2026-authors', 'Greek authors from Homer to Aristotle'],
        ]),
        canonicalGroup('ancient-greek-2026-art-architecture', 'Greek art and architecture', [
          ['ancient-greek-2026-sculpture', 'Greek sculpture'],
          ['ancient-greek-2026-temple-architecture', 'Greek temple architecture'],
          ['ancient-greek-2026-vase-painting', 'Attic vase painting'],
        ]),
      ],
      coverageNodeLevel: 'topic',
      notes: [
        'This is the outgoing syllabus sat by the 2026 examination cohort.',
        'The specification introduced to fifth-year students in September 2025 is deliberately excluded from this record.',
        'Prescribed texts are set for each examination year by the State Examinations Commission.',
      ],
    };
  }
  if (spec.subjectId === 'latin') {
    return {
      ...spec,
      id: 'latin:outgoing-2026',
      title: 'Leaving Certificate Latin syllabus — examination to June 2026',
      lastExamYear: 2026,
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Latin transition information', url: OFFICIAL.latin, role: 'transition' },
        { authority: 'NCCA', title: 'Leaving Certificate Latin syllabus', url: OFFICIAL.latinSyllabus, role: 'content' },
      ],
      groups: [
        canonicalGroup('latin-2026-language-texts', 'Language and texts', [
          ['latin-2026-composition-comprehension', 'Composition or comprehension'],
          ['latin-2026-grammar-scansion', 'Grammar and scansion'],
          ['latin-2026-prescribed-texts', 'Prescribed texts'],
          ['latin-2026-unprescribed-prose', 'Unprescribed prose'],
          ['latin-2026-unprescribed-verse', 'Unprescribed verse'],
        ]),
        canonicalGroup('latin-2026-history', 'Roman history', [
          ['latin-2026-caesar-trajan', 'From the death of Caesar to the death of Trajan'],
        ]),
        canonicalGroup('latin-2026-literature', 'Latin literature', [
          ['latin-2026-authors', 'Prescribed Latin authors and literary context'],
        ]),
        canonicalGroup('latin-2026-art-architecture', 'Roman art and architecture', [
          ['latin-2026-art', 'Roman art'],
          ['latin-2026-architecture', 'Roman architecture'],
        ]),
      ],
      coverageNodeLevel: 'topic',
      notes: [
        'This is the outgoing syllabus sat by the 2026 examination cohort.',
        'The specification introduced to fifth-year students in September 2025 is deliberately excluded from this record.',
        'Prescribed texts are set for each examination year by the State Examinations Commission.',
      ],
    };
  }
  if (spec.subjectId === 'arabic') {
    return {
      ...spec,
      id: 'arabic:outgoing-2026',
      title: 'Leaving Certificate Arabic syllabus — examination to June 2026',
      lastExamYear: 2026,
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Arabic transition information', url: OFFICIAL.arabic, role: 'transition' },
        { authority: 'NCCA', title: 'Leaving Certificate Arabic syllabus', url: OFFICIAL.arabicSyllabus, role: 'content' },
      ],
      groups: [
        canonicalGroup('arabic-2026-reading-directed-writing', 'Reading and directed writing', [
          ['arabic-2026-reading-comprehension', 'Reading comprehension'],
          ['arabic-2026-directed-writing', 'Directed writing'],
          ['arabic-2026-prescribed-literature', 'Prescribed literary texts'],
        ]),
        canonicalGroup('arabic-2026-continuous-writing', 'Continuous writing', [
          ['arabic-2026-experience-ideas', 'Articulating experience and ideas'],
          ['arabic-2026-audience-structure', 'Audience, structure and paragraphing'],
        ]),
        canonicalGroup('arabic-2026-use-language', 'Use of language', [
          ['arabic-2026-grammar-syntax', 'Grammar and syntax'],
          ['arabic-2026-vocabulary-register', 'Vocabulary, register and style'],
          ['arabic-2026-punctuation', 'Paragraphing and punctuation'],
        ]),
      ],
      coverageNodeLevel: 'topic',
      notes: [
        'This is the outgoing syllabus sat by the 2026 examination cohort.',
        'The redeveloped specification examined from 2027 is deliberately excluded from this record.',
      ],
    };
  }
  if (['biology', 'chemistry', 'physics', 'business'].includes(spec.subjectId)) {
    const officialSubjectSources = {
      biology: OFFICIAL.biology,
      chemistry: OFFICIAL.chemistry,
      physics: OFFICIAL.physics,
      business: OFFICIAL.business,
    } as const;
    return {
      ...spec,
      // This ID has already been written into mastery records. Keep it stable
      // while making its outgoing-cohort boundary and provenance explicit.
      lastExamYear: 2026,
      title: `Leaving Certificate ${spec.subjectName} syllabus — examination to June 2026`,
      status: 'verified',
      sources: [{
        authority: 'Curriculum Online',
        title: `Leaving Certificate ${spec.subjectName} syllabus (for examination to June 2026)`,
        url: officialSubjectSources[spec.subjectId as keyof typeof officialSubjectSources],
        role: 'transition',
      }],
      notes: [
        'The canonical IDs remain unchanged so existing Mark Bank cards and student mastery retain their identity.',
        'A redeveloped specification applies from the 2027 examination cohort.',
      ],
    };
  }
  if (spec.subjectId === 'religious-education') {
    return {
      ...spec,
      id: 'religious-education:2003',
      title: 'Leaving Certificate Religious Education syllabus',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Religious Education', url: OFFICIAL.religiousEducation, role: 'content' },
        { authority: 'NCCA', title: 'Leaving Certificate Religious Education syllabus', url: OFFICIAL.religiousEducationSyllabus, role: 'assessment' },
      ],
      selectionRules: [
        {
          id: 're-written-section-a',
          description: 'Section A is compulsory in the written examination.',
          requiredGroupIds: ['religious-education-0'],
          appliesTo: 'written-examination',
        },
        {
          id: 're-written-parts-two',
          description: 'Study two sections from B, C and D for the written examination.',
          choose: 2,
          fromGroupIds: ['religious-education-1', 'religious-education-2', 'religious-education-3'],
          appliesTo: 'written-examination',
        },
        {
          id: 're-written-parts-three',
          description: 'Study one section from E to J for the written examination.',
          choose: 1,
          fromGroupIds: [
            'religious-education-4', 'religious-education-5', 'religious-education-6',
            'religious-education-7', 'religious-education-8', 'religious-education-9',
          ],
          appliesTo: 'written-examination',
        },
      ],
    };
  }
  if (spec.subjectId === 'irish') {
    return {
      ...spec,
      id: 'irish:current',
      title: 'Leaving Certificate Gaeilge syllabus',
      status: 'verified',
      sources: [{ authority: 'Curriculum Online', title: 'Gaeilge', url: OFFICIAL.gaeilge, role: 'assessment' }],
      assessmentComponents: [
        {
          id: 'irish-oral-examination',
          title: 'Oral examination',
          kind: 'oral-examination',
          weighting: 40,
          levels: ['higher', 'ordinary', 'foundation'],
          required: true,
        },
        {
          id: 'irish-june-examinations',
          title: 'Aural and written examinations',
          kind: 'written-examination',
          weighting: 60,
          levels: ['higher', 'ordinary', 'foundation'],
          required: true,
          notes: ['Aggregate of the remaining three language skills assessed in June.'],
        },
      ],
    };
  }
  if (spec.subjectId === 'mathematics') {
    return {
      ...spec,
      id: 'mathematics:2015',
      title: 'Leaving Certificate Mathematics syllabus for examination from 2015',
      status: 'verified',
      sources: [{ authority: 'Curriculum Online', title: 'Mathematics', url: OFFICIAL.mathematics, role: 'assessment' }],
      notes: [
        'Higher and Ordinary levels have two examination papers; Foundation level has one examination paper.',
      ],
    };
  }
  if (spec.subjectId === 'french') {
    return {
      ...spec,
      id: 'french:current',
      title: 'Leaving Certificate French syllabus',
      status: 'verified',
      sources: [{ authority: 'Curriculum Online', title: 'French', url: OFFICIAL.french, role: 'assessment' }],
      notes: ['Assessment comprises written, aural and oral examinations at Higher and Ordinary levels.'],
    };
  }
  if (spec.subjectId === 'accounting') {
    return {
      ...spec,
      id: 'accounting:outgoing',
      title: 'Leaving Certificate Accounting syllabus — examination to June 2028',
      lastExamYear: 2028,
      status: 'verified',
      sources: [{ authority: 'Curriculum Online', title: 'Accounting', url: OFFICIAL.accounting, role: 'transition' }],
      notes: [
        'The replacement specification will not be introduced earlier than September 2027 and requires a separate canonical record.',
      ],
    };
  }
  if (spec.subjectId === 'applied-mathematics') {
    return {
      ...spec,
      id: 'applied-mathematics:current',
      title: 'Leaving Certificate Applied Mathematics specification',
      status: 'verified',
      sources: [
        {
          authority: 'Curriculum Online',
          title: 'Applied Mathematics',
          url: OFFICIAL.appliedMathematics,
          role: 'content',
        },
        {
          authority: 'NCCA',
          title: 'Leaving Certificate Applied Mathematics specification',
          url: OFFICIAL.appliedMathematicsSpecification,
          role: 'assessment',
        },
      ],
      recommendedClassHours: 180,
      assessmentComponents: [
        {
          id: 'applied-mathematics-modelling-project',
          title: 'Modelling project',
          kind: 'project',
          weighting: 20,
          levels: ['higher', 'ordinary'],
          required: true,
          notes: ['Based on an annual brief issued by the State Examinations Commission.'],
        },
        {
          id: 'applied-mathematics-written-examination',
          title: 'Written examination',
          kind: 'written-examination',
          weighting: 80,
          levels: ['higher', 'ordinary'],
          required: true,
          durationMinutes: 150,
        },
      ],
      notes: [
        'The four official strands are represented directly; Mathematical Modelling is a unifying strand.',
      ],
    };
  }
  if (spec.subjectId === 'history') {
    return {
      ...spec,
      id: 'history:current',
      title: 'Leaving Certificate History syllabus',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'History', url: OFFICIAL.history, role: 'content' },
        { authority: 'NCCA', title: 'Leaving Certificate History syllabus', url: OFFICIAL.historySyllabus, role: 'assessment' },
      ],
      assessmentComponents: [
        {
          id: 'history-research-study-report',
          title: 'Research study report',
          kind: 'coursework',
          weighting: 20,
          levels: ['higher', 'ordinary'],
          required: true,
          notes: ['Completed under teacher guidance and submitted before the written examination.'],
        },
        {
          id: 'history-written-examination',
          title: 'Written examination',
          kind: 'written-examination',
          weighting: 80,
          levels: ['higher', 'ordinary'],
          required: true,
        },
      ],
      notes: [
        'The March–May 2026 public-consultation draft is not an enacted specification and is not used here.',
      ],
    };
  }
  if (spec.subjectId === 'geography') {
    return {
      ...spec,
      id: 'geography:outgoing',
      title: 'Leaving Certificate Geography syllabus — examination to June 2027',
      lastExamYear: 2027,
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Geography', url: OFFICIAL.geography, role: 'transition' },
        { authority: 'NCCA', title: 'Leaving Certificate Geography guidelines', url: OFFICIAL.geographyGuidelines, role: 'assessment' },
      ],
      assessmentComponents: [
        {
          id: 'geography-investigation-report',
          title: 'Report on the geographical investigation',
          kind: 'coursework',
          weighting: 20,
          levels: ['higher', 'ordinary'],
          required: true,
        },
        {
          id: 'geography-written-examination',
          title: 'Written examination',
          kind: 'written-examination',
          weighting: 80,
          levels: ['higher', 'ordinary'],
          required: true,
          durationMinutes: 150,
        },
      ],
      notes: [
        'This outgoing syllabus must not be resolved for examinations after June 2027.',
        'The replacement specification introduced to fifth-year students in September 2026 requires a separate canonical record.',
      ],
    };
  }
  if (spec.subjectId === 'home-economics') {
    return {
      ...spec,
      id: 'home-economics:current',
      title: 'Leaving Certificate Home Economics — Scientific and Social syllabus',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Home Economics', url: OFFICIAL.homeEconomics, role: 'content' },
        { authority: 'NCCA', title: 'Home Economics — Scientific and Social syllabus', url: OFFICIAL.homeEconomicsSyllabus, role: 'assessment' },
      ],
      assessmentComponents: [
        {
          id: 'home-economics-practical-coursework',
          title: 'Practical coursework',
          kind: 'coursework',
          weighting: 20,
          levels: ['higher', 'ordinary'],
          required: true,
          notes: ['The form of practical coursework is governed by the selected elective and SEC instructions.'],
        },
        {
          id: 'home-economics-written-examination',
          title: 'Written examination',
          kind: 'written-examination',
          weighting: 80,
          levels: ['higher', 'ordinary'],
          required: true,
        },
      ],
    };
  }
  if (spec.subjectId === 'computer-science') {
    return {
      ...spec,
      id: 'computer-science:2025',
      title: 'Leaving Certificate Computer Science — updated specification for examination in 2025 and beyond',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Computer Science', url: OFFICIAL.computerScience, role: 'content' },
        { authority: 'NCCA', title: 'Computer Science assessment', url: OFFICIAL.computerScienceAssessment, role: 'assessment' },
      ],
      assessmentComponents: [
        {
          id: 'computer-science-end-of-course-examination',
          title: 'End-of-course examination',
          kind: 'written-examination',
          weighting: 70,
          levels: ['higher', 'ordinary'],
          required: true,
          notes: ['Includes written and computer-based assessment.'],
        },
        {
          id: 'computer-science-coursework',
          title: 'Coursework assessment',
          kind: 'coursework',
          weighting: 30,
          levels: ['higher', 'ordinary'],
          required: true,
          notes: ['One computational artefact with an accompanying report.'],
        },
      ],
    };
  }
  if (spec.subjectId === 'economics') {
    return {
      ...spec,
      id: 'economics:current',
      title: 'Leaving Certificate Economics specification',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Economics', url: OFFICIAL.economics, role: 'content' },
        { authority: 'NCCA', title: 'Leaving Certificate Economics specification', url: OFFICIAL.economicsSpecification, role: 'assessment' },
      ],
      assessmentComponents: [
        {
          id: 'economics-research-study',
          title: 'Research study',
          kind: 'coursework',
          weighting: 20,
          levels: ['higher', 'ordinary'],
          required: true,
        },
        {
          id: 'economics-written-examination',
          title: 'Written examination',
          kind: 'written-examination',
          weighting: 80,
          levels: ['higher', 'ordinary'],
          required: true,
        },
      ],
    };
  }
  if (spec.subjectId === 'politics-and-society') {
    return {
      ...spec,
      id: 'politics-and-society:current',
      title: 'Leaving Certificate Politics and Society specification',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Politics and Society', url: OFFICIAL.politicsAndSociety, role: 'content' },
        { authority: 'NCCA', title: 'Politics and Society assessment', url: OFFICIAL.politicsAndSocietyAssessment, role: 'assessment' },
      ],
      assessmentComponents: [
        {
          id: 'politics-and-society-citizenship-project',
          title: 'Citizenship project',
          kind: 'project',
          weighting: 20,
          levels: ['higher', 'ordinary'],
          required: true,
        },
        {
          id: 'politics-and-society-written-examination',
          title: 'Written examination',
          kind: 'written-examination',
          weighting: 80,
          levels: ['higher', 'ordinary'],
          required: true,
        },
      ],
    };
  }
  if (spec.subjectId === 'art') {
    return {
      ...spec,
      id: 'art:current',
      title: 'Leaving Certificate Art specification',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Art', url: OFFICIAL.art, role: 'content' },
        { authority: 'NCCA', title: 'Art assessment for certification', url: OFFICIAL.artAssessment, role: 'assessment' },
      ],
      assessmentComponents: [
        {
          id: 'art-practical-coursework',
          title: 'Practical coursework',
          kind: 'coursework',
          weighting: 50,
          levels: ['higher', 'ordinary'],
          required: true,
        },
        {
          id: 'art-practical-examination',
          title: 'Invigilated practical examination',
          kind: 'practical-examination',
          weighting: 20,
          levels: ['higher', 'ordinary'],
          required: true,
        },
        {
          id: 'art-written-examination',
          title: 'Written examination',
          kind: 'written-examination',
          weighting: 30,
          levels: ['higher', 'ordinary'],
          required: true,
        },
      ],
    };
  }
  if (spec.subjectId === 'classical-studies') {
    return {
      ...spec,
      id: 'classical-studies:current',
      title: 'Leaving Certificate Classical Studies specification',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Classical Studies', url: OFFICIAL.classicalStudies, role: 'content' },
        { authority: 'NCCA', title: 'Leaving Certificate Classical Studies specification', url: OFFICIAL.classicalStudiesSpecification, role: 'assessment' },
      ],
      recommendedClassHours: 180,
      assessmentComponents: [
        {
          id: 'classical-studies-research-study', title: 'Research study', kind: 'coursework',
          weighting: 20, levels: ['higher', 'ordinary'], required: true,
        },
        {
          id: 'classical-studies-written-examination', title: 'Written examination', kind: 'written-examination',
          weighting: 80, levels: ['higher', 'ordinary'], required: true,
        },
      ],
      notes: ['The four strand groups reproduce the official specification structure.'],
    };
  }
  if (spec.subjectId === 'design-and-communication-graphics') {
    return {
      ...spec,
      id: 'design-and-communication-graphics:current',
      title: 'Leaving Certificate Design and Communication Graphics syllabus',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Design and Communication Graphics', url: OFFICIAL.dcg, role: 'content' },
        { authority: 'NCCA', title: 'Design and Communication Graphics syllabus', url: OFFICIAL.dcgSyllabus, role: 'assessment' },
      ],
      assessmentComponents: [
        {
          id: 'dcg-student-assignment', title: 'Student assignment', kind: 'project',
          weighting: 40, levels: ['higher', 'ordinary'], required: true,
        },
        {
          id: 'dcg-terminal-examination', title: 'Terminal examination', kind: 'written-examination',
          weighting: 60, levels: ['higher', 'ordinary'], required: true,
        },
      ],
    };
  }
  if (spec.subjectId === 'technology') {
    return {
      ...spec,
      id: 'technology:current',
      title: 'Leaving Certificate Technology syllabus',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Technology', url: OFFICIAL.technology, role: 'content' },
        { authority: 'NCCA', title: 'Leaving Certificate Technology syllabus', url: OFFICIAL.technologySyllabus, role: 'assessment' },
      ],
      selectionRules: [{
        id: 'technology-two-options',
        description: 'Study two of the five optional areas in addition to the mandatory core.',
        requiredGroupIds: ['technology-0', 'technology-1', 'technology-2', 'technology-3', 'technology-4', 'technology-5', 'technology-6'],
        choose: 2,
        fromGroupIds: ['technology-7', 'technology-8', 'technology-9', 'technology-10', 'technology-11'],
        appliesTo: 'programme',
      }],
      assessmentComponents: [
        {
          id: 'technology-project', title: 'Project', kind: 'project',
          weighting: 50, levels: ['higher', 'ordinary'], required: true,
        },
        {
          id: 'technology-terminal-examination', title: 'Terminal examination paper', kind: 'written-examination',
          weighting: 50, levels: ['higher', 'ordinary'], required: true,
          notes: ['Two hours at Ordinary level and two and a half hours at Higher level.'],
        },
      ],
    };
  }
  if (spec.subjectId === 'music') {
    return {
      ...spec,
      id: 'music:current',
      title: 'Leaving Certificate Music syllabus',
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: 'Music', url: OFFICIAL.music, role: 'content' },
        { authority: 'NCCA', title: 'Leaving Certificate Music syllabus', url: OFFICIAL.musicSyllabus, role: 'assessment' },
      ],
      recommendedClassHours: 180,
      selectionRules: [{
        id: 'music-elective',
        description: 'Choose Performing, Composing or Listening as the elective activity worth the remaining 25%.',
        choose: 1,
        fromGroupIds: ['music-0', 'music-1', 'music-2'],
        appliesTo: 'programme',
      }],
      notes: [
        'Performing, Composing and Listening each account for 25%; the chosen elective adds a further 25% in that activity.',
        'The elective structure is retained as a selection rule rather than represented as misleading fixed assessment percentages.',
      ],
    };
  }
  const verifiedCurrent: Record<string, { id: string; title: string; source: string; syllabus?: string; notes?: string[] }> = {
    german: {
      id: 'german:current', title: 'Leaving Certificate German syllabus', source: OFFICIAL.german,
      notes: ['Assessment comprises written, aural and oral examinations at Higher and Ordinary levels.'],
    },
    spanish: {
      id: 'spanish:current', title: 'Leaving Certificate Spanish syllabus', source: OFFICIAL.spanish,
      notes: ['Assessment comprises written, aural and oral examinations at Higher and Ordinary levels.'],
    },
    italian: {
      id: 'italian:current', title: 'Leaving Certificate Italian syllabus', source: OFFICIAL.italian,
      notes: ['Assessment comprises written, aural and oral examinations at Higher and Ordinary levels.'],
    },
    japanese: {
      id: 'japanese:current', title: 'Leaving Certificate Japanese syllabus', source: OFFICIAL.japanese,
      notes: ['Assessment comprises written, aural and oral examinations at Higher and Ordinary levels.'],
    },
    russian: {
      id: 'russian:current', title: 'Leaving Certificate Russian syllabus', source: OFFICIAL.russian,
      notes: ['Assessment comprises written, aural and oral examinations at Higher and Ordinary levels.'],
    },
    'hebrew-studies': {
      id: 'hebrew-studies:current', title: 'Leaving Certificate Hebrew Studies syllabus',
      source: OFFICIAL.hebrewStudies, syllabus: OFFICIAL.hebrewStudiesSyllabus,
      notes: ['Sections A to D and their paired major topics reproduce the official syllabus structure.'],
    },
    'physics-and-chemistry': {
      id: 'physics-and-chemistry:current', title: 'Leaving Certificate Physics and Chemistry syllabus',
      source: OFFICIAL.physicsAndChemistry, syllabus: OFFICIAL.physicsAndChemistrySyllabus,
      notes: ['This is a discrete combined subject and must not be treated as the separate Physics and Chemistry subjects.'],
    },
    polish: {
      id: 'polish:current', title: 'Leaving Certificate Polish specification', source: OFFICIAL.polish,
      notes: ['The two official competence strands are represented directly.'],
    },
    lithuanian: {
      id: 'lithuanian:current', title: 'Leaving Certificate Lithuanian specification', source: OFFICIAL.lithuanian,
      notes: ['The two official competence strands are represented directly.'],
    },
    portuguese: {
      id: 'portuguese:current', title: 'Leaving Certificate Portuguese specification', source: OFFICIAL.portuguese,
      notes: ['Oral, aural and written weightings differ by level; consumers must use the official assessment table rather than infer one shared split.'],
    },
    'mandarin-chinese': {
      id: 'mandarin-chinese:current', title: 'Leaving Certificate Mandarin Chinese specification', source: OFFICIAL.mandarinChinese,
      notes: ['Oral, aural and written weightings differ by level; consumers must use the official assessment table rather than infer one shared split.'],
    },
  };
  const current = verifiedCurrent[spec.subjectId];
  if (current) {
    return {
      ...spec,
      id: current.id,
      title: current.title,
      status: 'verified',
      sources: [
        { authority: 'Curriculum Online', title: current.title, url: current.source, role: 'content' },
        ...(current.syllabus ? [{
          authority: 'NCCA' as const,
          title: current.title,
          url: current.syllabus,
          role: 'assessment' as const,
        }] : []),
      ],
      notes: current.notes,
    };
  }
  const verifiedOutgoing: Record<string, { id: string; title: string; lastExamYear: number; source: string; note: string }> = {
    english: {
      id: 'english:outgoing', title: 'Leaving Certificate English syllabus — examination to June 2028',
      lastExamYear: 2028, source: OFFICIAL.english,
      note: 'The replacement specification will not be introduced earlier than September 2027 and needs a separate canonical record.',
    },
    'construction-studies': {
      id: 'construction-studies:outgoing', title: 'Leaving Certificate Construction Studies syllabus — examination to June 2027',
      lastExamYear: 2027, source: OFFICIAL.constructionStudies,
      note: 'Construction Technology is introduced to fifth-year students in September 2026 and needs a separate canonical record.',
    },
    engineering: {
      id: 'engineering:outgoing', title: 'Leaving Certificate Engineering syllabus — examination to June 2027',
      lastExamYear: 2027, source: OFFICIAL.engineering,
      note: 'The replacement Engineering specification introduced in September 2026 needs a separate canonical record.',
    },
    'physical-education': {
      id: 'physical-education:outgoing', title: 'Leaving Certificate Physical Education specification — examination to June 2027',
      lastExamYear: 2027, source: OFFICIAL.physicalEducation,
      note: 'The replacement Physical Education specification introduced in September 2026 needs a separate canonical record.',
    },
    'lcvp-link-modules': {
      id: 'lcvp-link-modules:outgoing', title: 'LCVP Link Modules programme statement — examination to June 2027',
      lastExamYear: 2027, source: OFFICIAL.lcvp,
      note: 'Life, Community and Work is introduced in September 2026 and needs a separate canonical record.',
    },
  };
  const outgoing = verifiedOutgoing[spec.subjectId];
  if (outgoing) {
    return {
      ...spec,
      id: outgoing.id,
      title: outgoing.title,
      lastExamYear: outgoing.lastExamYear,
      status: 'verified',
      sources: [{ authority: 'Curriculum Online', title: outgoing.title, url: outgoing.source, role: 'transition' }],
      notes: [outgoing.note],
    };
  }
  return spec;
}

export const CURRICULUM_SPECIFICATIONS: CanonicalCurriculumSpecification[] = [
  ...legacySpecifications.map(patchLegacySpecification),
  ...redevelopedSpecifications,
  constructionTechnologySpecification,
  geography2028Specification,
];

const normalise = (value: string) => value.trim().toLowerCase().replace(/\s+/g, ' ');

const SUBJECT_ALIASES: Record<string, string> = {
  maths: 'mathematics', math: 'mathematics',
  'applied maths': 'applied-mathematics',
  bio: 'biology', chem: 'chemistry', phys: 'physics',
  'ag science': 'agricultural-science', 'agricultural science': 'agricultural-science',
  re: 'religious-education', religion: 'religious-education',
  gaeilge: 'irish', irish: 'irish',
  dcg: 'design-and-communication-graphics',
  'design communication graphics': 'design-and-communication-graphics',
  'computer studies': 'computer-science', cs: 'computer-science',
  'home ec': 'home-economics', 'home economics': 'home-economics',
  lcpe: 'physical-education', pe: 'physical-education',
  'construction technology': 'construction-studies',
  'life community and work': 'lcvp-link-modules', lcvp: 'lcvp-link-modules',
};

export function resolveSubjectId(subject: string): string | undefined {
  const key = normalise(subject);
  const direct = CURRICULUM.find((entry) => normalise(entry.id) === key || normalise(entry.name) === key);
  return direct?.id ?? SUBJECT_ALIASES[key];
}

export function examinationYearFromDate(examDate?: string | null): number {
  if (examDate) {
    const parsed = new Date(examDate);
    if (!Number.isNaN(parsed.getTime())) return parsed.getFullYear();
  }
  const today = new Date();
  return today.getMonth() > 5 ? today.getFullYear() + 1 : today.getFullYear();
}

export function specificationsForSubject(subject: string): CanonicalCurriculumSpecification[] {
  const subjectId = resolveSubjectId(subject);
  if (!subjectId) return [];
  return CURRICULUM_SPECIFICATIONS.filter((spec) => spec.subjectId === subjectId);
}

export interface CanonicalCurriculumSubjectSummary {
  id: string;
  name: string;
  category: CurriculumCategory;
  levels: CurriculumLevel[];
  specificationId: string;
  groups: CanonicalCurriculumGroup[];
  programme: CurriculumProgramme;
}

/** Cohort-safe subject catalogue for pickers and other enumerating surfaces. */
export function curriculumSubjectsForYear(
  examYear = examinationYearFromDate(),
  programmes?: CurriculumProgramme[],
): CanonicalCurriculumSubjectSummary[] {
  const subjectIds = [...new Set(CURRICULUM_SPECIFICATIONS.map((specification) => specification.subjectId))];
  return subjectIds.flatMap((subjectId) => {
    const specification = resolveCurriculumSpecification(subjectId, examYear);
    return specification && (!programmes || programmes.includes(specification.programme)) ? [{
      id: specification.subjectId,
      name: specification.subjectName,
      category: specification.category,
      levels: specification.levels,
      specificationId: specification.id,
      groups: specification.groups,
      programme: specification.programme,
    }] : [];
  });
}

export function resolveCurriculumSpecification(
  subject: string,
  examYear = examinationYearFromDate(),
): CanonicalCurriculumSpecification | undefined {
  const candidates = specificationsForSubject(subject)
    .filter((spec) => (spec.firstExamYear ?? -Infinity) <= examYear && (spec.lastExamYear ?? Infinity) >= examYear)
    .sort((a, b) => (b.firstExamYear ?? -Infinity) - (a.firstExamYear ?? -Infinity));
  return candidates[0];
}

export function findCanonicalTopic(
  specification: CanonicalCurriculumSpecification,
  topicId: string,
): CanonicalCurriculumTopic | undefined {
  return specification.groups.flatMap((group) => group.topics).find((topic) => topic.id === topicId);
}

export function specificationContainsId(
  specification: CanonicalCurriculumSpecification,
  nodeId: string,
): boolean {
  return specification.groups.some((group) =>
    group.id === nodeId || group.topics.some((topic) => topic.id === nodeId),
  );
}
