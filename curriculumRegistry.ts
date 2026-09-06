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
  /** Compatibility-only redirects from retired node IDs into this specification. */
  legacyTopicAliases?: Record<string, string>;
  notes?: string[];
}

const OFFICIAL = {
  curriculumOverview: 'https://www.curriculumonline.ie/senior-cycle/curriculum/',
  redevelopmentSchedule: 'https://ncca.ie/en/senior-cycle/senior-cycle-redevelopment/schedule-of-senior-cycle-subjects-for-redevelopment/',
  biology: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/biology/',
  chemistry: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/chemistry/',
  physics: 'https://curriculumonline.ie/senior-cycle/senior-cycle-subjects/physics/',
  business: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/business/',
  businessSpecification: 'https://www.curriculumonline.ie/getmedia/e81ccca9-fdf5-42e9-a291-52e9549820c9/SC-Business-Spec-ENG.pdf',
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
  engineeringSpecification: 'https://www.curriculumonline.ie/getmedia/2e897923-e0dc-4f3b-ac42-f8501226c8ab/SC-Engineering-Spec-ENG-INT.pdf',
  physicalEducation: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/physical-education-specification/',
  physicalEducation2028Specification: 'https://www.curriculumonline.ie/getmedia/e3c33f7c-a88b-4050-bed3-c892ec995ba2/SC-PE-Spec-ENG-INT.pdf',
  lifeCommunityWorkSpecification: 'https://www.curriculumonline.ie/getmedia/f6802fdb-582a-4380-905f-ee47b4edbaf2/SC-LCW-Spec-ENG-INT.pdf',
  computerScience: 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/computer-science/',
  engineeringSyllabus: 'https://www.curriculumonline.ie/getmedia/a2934262-1866-46d6-a156-bbfb629f6306/SCSEC13_Engineering_syllabus_Eng.pdf',
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

export interface CurriculumRedevelopmentTransition {
  /** Year the replacement is introduced to fifth-year students. */
  introductionYear: number;
  /** First examination year implied by the two-year senior-cycle course. */
  firstExamYear: number;
  /** Last cohort for which the outgoing map is valid. */
  outgoingLastExamYear: number;
  replacementName: string;
  sourceUrl: string;
  timing: 'confirmed' | 'not-before';
}

/**
 * Cohort boundaries that materially change the topic map or assessment
 * structure students see in War Room. These are deliberately separate from
 * editorial study advice: every entry is backed by Curriculum Online or the
 * NCCA redevelopment schedule.
 */

/**
 * The Construction Studies syllabus's own ten sections, mirroring
 * CONSTRUCTION_STUDIES_STRANDS in components/MarkBank/deck.ts. Both are needed:
 * deck.ts is what the tool displays, this is what a card's topic must resolve
 * into, and a subject present in one and absent from the other fails the
 * registry check the moment its deck can be loaded.
 */
const CONSTRUCTION_STUDIES_GROUPS = [
  {
    id: 'cs1',
    code: '1',
    title: 'General',
    topics: [
      { id: 'cons-1-1', code: '1.1', title: 'Historical development and appearance of buildings' },
      { id: 'cons-1-2', code: '1.2', title: 'The built environment and controls over it' },
      { id: 'cons-1-3', code: '1.3', title: 'Planning permission, choosing a site, house purchase' },
      { id: 'cons-1-4', code: '1.4', title: 'The construction industry and occupations in it' },
      { id: 'cons-1-5', code: '1.5', title: 'Drawings, documents, scales, symbols and notation' },
      { id: 'cons-1-6', code: '1.6', title: 'Site investigation and site accommodation' },
      { id: 'cons-1-7', code: '1.7', title: 'Structural principles and exposure to the elements' },
      { id: 'cons-1-8', code: '1.8', title: 'Safety precautions on site' },
      { id: 'cons-1-9', code: '1.9', title: 'Building regulations and fire tests on materials' },
    ],
  },
  {
    id: 'cs2',
    code: '2',
    title: 'Substructure',
    topics: [
      { id: 'cons-2-1', code: '2.1', title: 'Excavation, vegetable soil and water in excavations' },
      { id: 'cons-2-2', code: '2.2', title: 'Functions of a foundation and choice of foundation' },
      { id: 'cons-2-3', code: '2.3', title: 'Subsoil movement and foundation materials' },
      { id: 'cons-2-4', code: '2.4', title: 'Strip, slab, short bored pile and pad foundations' },
      { id: 'cons-2-5', code: '2.5', title: 'Steel reinforcement in foundations' },
      { id: 'cons-2-6', code: '2.6', title: 'Concrete materials, storage and batching' },
      { id: 'cons-2-7', code: '2.7', title: 'Water/cement ratio, mixing, site and ready mixed concrete' },
    ],
  },
  {
    id: 'cs3',
    code: '3',
    title: 'Superstructure',
    topics: [
      { id: 'cons-3-1', code: '3.1', title: 'Structural forms and the relationship to substructure' },
      { id: 'cons-3-2', code: '3.2', title: 'The external envelope and its primary functions' },
      { id: 'cons-3-3', code: '3.3', title: 'External walls, bonding, piers and parapet walls' },
      { id: 'cons-3-4', code: '3.4', title: 'Damp proof courses and membranes, lintels and arches' },
      { id: 'cons-3-5', code: '3.5', title: 'Windows: types, components, ironmongery and choice' },
      { id: 'cons-3-6', code: '3.6', title: 'Window details at head, sill and jamb; glass and glazing' },
      { id: 'cons-3-7', code: '3.7', title: 'Doors: types, schedules, sizes and details' },
      { id: 'cons-3-8', code: '3.8', title: 'Roof forms, trusses and trussed rafters' },
      { id: 'cons-3-9', code: '3.9', title: 'Roof coverings, sarking and thermal insulation' },
      { id: 'cons-3-10', code: '3.10', title: 'Flat roofs, finishes, eaves, verges and abutments' },
    ],
  },
  {
    id: 'cs4',
    code: '4',
    title: 'Internal Construction',
    topics: [
      { id: 'cons-4-1', code: '4.1', title: 'Internal walls, openings and wall finishes' },
      { id: 'cons-4-2', code: '4.2', title: 'Ground floors: solid and timber, and their junctions' },
      { id: 'cons-4-3', code: '4.3', title: 'Suspended timber floors, upper floors and strutting' },
      { id: 'cons-4-4', code: '4.4', title: 'Stairs: rise, going, handrail, height and headroom' },
      { id: 'cons-4-5', code: '4.5', title: 'Stud partitions, internal doors and second fixing' },
      { id: 'cons-4-6', code: '4.6', title: 'Dry lining, plastering, painting and defects in finishes' },
    ],
  },
  {
    id: 'cs5',
    code: '5',
    title: 'Services and External Works',
    topics: [
      { id: 'cons-5-1', code: '5.1', title: 'Service entry, materials and protection of installations' },
      { id: 'cons-5-2', code: '5.2', title: 'Hot and cold water systems, cisterns and cylinders' },
      { id: 'cons-5-3', code: '5.3', title: 'Heating systems, temperature control and heat conservation' },
      { id: 'cons-5-4', code: '5.4', title: 'Surface water, eaves gutters and rainwater pipes' },
      { id: 'cons-5-5', code: '5.5', title: 'Underground drainage, septic tanks and laying drains' },
      { id: 'cons-5-6', code: '5.6', title: 'Sanitary fitments and the single stack system' },
      { id: 'cons-5-7', code: '5.7', title: 'Fireplaces and flues to domestic fireplaces' },
      { id: 'cons-5-8', code: '5.8', title: 'Domestic electrical installation, circuits and protection' },
    ],
  },
  {
    id: 'cs6',
    code: '6',
    title: 'Heat and Thermal Effects in Buildings',
    topics: [
      { id: 'cons-6-1', code: '6.1', title: 'Thermal resistance, conductivity and transmittance' },
      { id: 'cons-6-2', code: '6.2', title: 'Thermal bridges and insulating materials' },
      { id: 'cons-6-3', code: '6.3', title: 'Heat loss calculations and running costs' },
      { id: 'cons-6-4', code: '6.4', title: 'Solar heat gain and sources of heat gain' },
      { id: 'cons-6-5', code: '6.5', title: 'Human comfort, humidity and ventilation rates' },
      { id: 'cons-6-6', code: '6.6', title: 'Surface condensation and vapour barriers' },
    ],
  },
  {
    id: 'cs7',
    code: '7',
    title: 'Illumination in Buildings',
    topics: [
      { id: 'cons-7-1', code: '7.1', title: 'The way we see, and the nature of light' },
      { id: 'cons-7-2', code: '7.2', title: 'Units of illumination and the daylight factor' },
      { id: 'cons-7-3', code: '7.3', title: 'Glare, the glare index and control of glare' },
      { id: 'cons-7-4', code: '7.4', title: 'Conditions necessary for good illumination' },
    ],
  },
  {
    id: 'cs8',
    code: '8',
    title: 'Sound in Buildings',
    topics: [
      { id: 'cons-8-1', code: '8.1', title: 'The way we hear, and the nature of sound' },
      { id: 'cons-8-2', code: '8.2', title: 'The decibel, reverberation and reverberation time' },
      { id: 'cons-8-3', code: '8.3', title: 'Airborne and impact sound insulation' },
      { id: 'cons-8-4', code: '8.4', title: 'Hearing loss, noise levels and protection devices' },
    ],
  },
  {
    id: 'cs9',
    code: '9',
    title: 'Tools',
    topics: [
      { id: 'cons-9-1', code: '9.1', title: 'Maintenance and care in the use of tools' },
      { id: 'cons-9-2', code: '9.2', title: 'Woodworking tools, their uses and mechanical principles' },
      { id: 'cons-9-3', code: '9.3', title: 'Grinding, sharpening and workshop equipment' },
      { id: 'cons-9-4', code: '9.4', title: 'Safety with edged tools and electricity' },
    ],
  },
  {
    id: 'cs10',
    code: '10',
    title: 'Processes',
    topics: [
      { id: 'cons-10-1', code: '10.1', title: 'Joints in partitions, floors, stairs, roofs, doors and windows' },
      { id: 'cons-10-2', code: '10.2', title: 'Box and carcase construction and simple fitments' },
      { id: 'cons-10-3', code: '10.3', title: 'Jointing boards and the use of manufactured boards' },
      { id: 'cons-10-4', code: '10.4', title: 'Choice of joint for strength, assembly and decorative effect' },
      { id: 'cons-10-5', code: '10.5', title: 'Cutting lists and the setting-out rod' },
      { id: 'cons-10-6', code: '10.6', title: 'Glues, adhesives, holding work and jigs' },
      { id: 'cons-10-7', code: '10.7', title: 'Measuring for accuracy, surface preparation and finishing' },
    ],
  },
];


/**
 * The Mathematics syllabus's own five strands, mirroring MATHS_STRANDS in
 * components/MarkBank/deck.ts. Titles are the syllabus's, including where it is
 * terser than the usual name for the area -- it writes "Complex", not "Complex
 * numbers".
 */
/* The Engineering syllabus's own headings. Section 1 is Workshop Processes,
 * examined practically; section 2, "Materials and Technology", is what the
 * written paper covers. Its fourteen headings are the topics here, with the
 * mechanisms heading from section 1's TECHNOLOGY ("prime movers, power
 * transmission systems, brakes and other mechanisms") added because the
 * written paper asks about those every year. The syllabus PDF is a SCAN with
 * no text layer, so the headings were read by rendering its pages. */
const ENGINEERING_GROUPS = [
  {
    id: 'eng1',
    code: '1',
    title: 'Materials',
    topics: [
      { id: 'eng-1-2', code: 'M', title: 'Classification and origin of metals' },
      { id: 'eng-1-3', code: 'M', title: 'Structure of metals' },
      { id: 'eng-1-4', code: 'M', title: 'Iron and steel' },
      { id: 'eng-1-5', code: 'M', title: 'Non-ferrous metals' },
      { id: 'eng-1-9', code: 'M', title: 'Plastics' },
    ],
  },
  {
    id: 'eng2',
    code: '2',
    title: 'Processes',
    topics: [
      { id: 'eng-2-6', code: 'P', title: 'Heat treatment of metals' },
      { id: 'eng-2-10', code: 'P', title: 'Joining of materials' },
      { id: 'eng-2-11', code: 'P', title: 'Machining' },
      { id: 'eng-2-13', code: 'P', title: 'Manufacturing processes' },
      { id: 'eng-2-15', code: 'P', title: 'Mechanisms and power transmission' },
      { id: 'eng-2-16', code: 'P', title: 'Control technology and electronics' },
    ],
  },
  {
    id: 'eng3',
    code: '3',
    title: 'Properties and practice',
    topics: [
      { id: 'eng-3-1', code: 'T', title: 'Health and safety' },
      { id: 'eng-3-7', code: 'T', title: 'Corrosion of metals' },
      { id: 'eng-3-8', code: 'T', title: 'Materials testing' },
      { id: 'eng-3-12', code: 'T', title: 'Metrology' },
      { id: 'eng-3-14', code: 'T', title: 'Technology and design' },
    ],
  },
];

const COMPUTER_SCIENCE_GROUPS = [
  {
    id: 'cs1',
    code: '1',
    title: 'Practices and principles',
    topics: [
      { id: 'cs-1-1', code: 'S1', title: 'Computational thinking' },
      { id: 'cs-1-2', code: 'S1', title: 'Computers and society' },
      { id: 'cs-1-3', code: 'S1', title: 'Designing and developing' },
    ],
  },
  {
    id: 'cs2',
    code: '2',
    title: 'Core concepts',
    topics: [
      { id: 'cs-2-1', code: 'S2', title: 'Abstraction' },
      { id: 'cs-2-2', code: 'S2', title: 'Algorithms' },
      { id: 'cs-2-3', code: 'S2', title: 'Computer systems' },
      { id: 'cs-2-4', code: 'S2', title: 'Data' },
      { id: 'cs-2-5', code: 'S2', title: 'Evaluation and testing' },
    ],
  },
  {
    id: 'cs3',
    code: '3',
    title: 'Computer science in practice',
    topics: [
      { id: 'cs-3-1', code: 'ALT1', title: 'Interactive information systems' },
      { id: 'cs-3-2', code: 'ALT2', title: 'Analytics' },
      { id: 'cs-3-3', code: 'ALT3', title: 'Modelling and simulation' },
      { id: 'cs-3-4', code: 'ALT4', title: 'Embedded systems' },
    ],
  },
];

const MATHS_GROUPS = [
  {
    id: 'ms1',
    code: '1',
    title: 'Statistics and Probability',
    topics: [
      { id: 'maths-1-1', code: '1.1', title: 'Counting' },
      { id: 'maths-1-2', code: '1.2', title: 'Concepts of probability' },
      { id: 'maths-1-3', code: '1.3', title: 'Outcomes of simple random processes' },
      { id: 'maths-1-4', code: '1.4', title: 'Statistical reasoning with an aim' },
      { id: 'maths-1-5', code: '1.5', title: 'Finding, collecting and organising data' },
      { id: 'maths-1-6', code: '1.6', title: 'Representing data graphically and numerically' },
      { id: 'maths-1-7', code: '1.7', title: 'Analysing, interpreting and drawing conclusions from data' },
    ],
  },
  {
    id: 'ms2',
    code: '2',
    title: 'Geometry and Trigonometry',
    topics: [
      { id: 'maths-2-1', code: '2.1', title: 'Synthetic geometry' },
      { id: 'maths-2-2', code: '2.2', title: 'Co-ordinate geometry' },
      { id: 'maths-2-3', code: '2.3', title: 'Trigonometry' },
      { id: 'maths-2-4', code: '2.4', title: 'Transformation geometry, enlargements' },
    ],
  },
  {
    id: 'ms3',
    code: '3',
    title: 'Number',
    topics: [
      { id: 'maths-3-1', code: '3.1', title: 'Number systems' },
      { id: 'maths-3-2', code: '3.2', title: 'Indices' },
      { id: 'maths-3-3', code: '3.3', title: 'Arithmetic' },
      { id: 'maths-3-4', code: '3.4', title: 'Length, area and volume' },
    ],
  },
  {
    id: 'ms4',
    code: '4',
    title: 'Algebra',
    topics: [
      { id: 'maths-4-1', code: '4.1', title: 'Expressions' },
      { id: 'maths-4-2', code: '4.2', title: 'Solving equations' },
      { id: 'maths-4-3', code: '4.3', title: 'Inequalities' },
      { id: 'maths-4-4', code: '4.4', title: 'Complex' },
    ],
  },
  {
    id: 'ms5',
    code: '5',
    title: 'Functions',
    topics: [
      { id: 'maths-5-1', code: '5.1', title: 'Functions' },
      { id: 'maths-5-2', code: '5.2', title: 'Calculus' },
    ],
  },
];

export const CURRICULUM_REDEVELOPMENT_TRANSITIONS: Record<string, CurriculumRedevelopmentTransition> = {
  'construction-studies': {
    introductionYear: 2026,
    firstExamYear: 2028,
    outgoingLastExamYear: 2027,
    replacementName: 'Construction Technology',
    sourceUrl: OFFICIAL.constructionStudies,
    timing: 'confirmed',
  },
  engineering: {
    introductionYear: 2026,
    firstExamYear: 2028,
    outgoingLastExamYear: 2027,
    replacementName: 'Engineering',
    sourceUrl: OFFICIAL.engineering,
    timing: 'confirmed',
  },
  geography: {
    introductionYear: 2026,
    firstExamYear: 2028,
    outgoingLastExamYear: 2027,
    replacementName: 'Geography',
    sourceUrl: OFFICIAL.geography,
    timing: 'confirmed',
  },
  'lcvp-link-modules': {
    introductionYear: 2026,
    firstExamYear: 2028,
    outgoingLastExamYear: 2027,
    replacementName: 'Life, Community and Work',
    sourceUrl: OFFICIAL.lcvp,
    timing: 'confirmed',
  },
  'physical-education': {
    introductionYear: 2026,
    firstExamYear: 2028,
    outgoingLastExamYear: 2027,
    replacementName: 'Physical Education',
    sourceUrl: OFFICIAL.physicalEducation,
    timing: 'confirmed',
  },
  // Accounting and English were postponed until at least September 2027.
  accounting: {
    introductionYear: 2027,
    firstExamYear: 2029,
    outgoingLastExamYear: 2028,
    replacementName: 'Accounting',
    sourceUrl: OFFICIAL.accounting,
    timing: 'not-before',
  },
  english: {
    introductionYear: 2027,
    firstExamYear: 2029,
    outgoingLastExamYear: 2028,
    replacementName: 'English',
    sourceUrl: OFFICIAL.english,
    timing: 'not-before',
  },
  // Tranche 3: introduced to fifth year in 2027, so the outgoing
  // specifications remain the correct maps through the 2028 examinations.
  'agricultural-science': {
    introductionYear: 2027, firstExamYear: 2029, outgoingLastExamYear: 2028,
    replacementName: 'Agricultural Science', sourceUrl: OFFICIAL.redevelopmentSchedule, timing: 'confirmed',
  },
  'computer-science': {
    introductionYear: 2027, firstExamYear: 2029, outgoingLastExamYear: 2028,
    replacementName: 'Computer Science', sourceUrl: OFFICIAL.redevelopmentSchedule, timing: 'confirmed',
  },
  'design-and-communication-graphics': {
    introductionYear: 2027, firstExamYear: 2029, outgoingLastExamYear: 2028,
    replacementName: 'Design and Communication Graphics', sourceUrl: OFFICIAL.redevelopmentSchedule, timing: 'confirmed',
  },
  history: {
    introductionYear: 2027, firstExamYear: 2029, outgoingLastExamYear: 2028,
    replacementName: 'History', sourceUrl: OFFICIAL.redevelopmentSchedule, timing: 'confirmed',
  },
  'home-economics': {
    introductionYear: 2027, firstExamYear: 2029, outgoingLastExamYear: 2028,
    replacementName: 'Home Economics', sourceUrl: OFFICIAL.redevelopmentSchedule, timing: 'confirmed',
  },
  mathematics: {
    introductionYear: 2027, firstExamYear: 2029, outgoingLastExamYear: 2028,
    replacementName: 'Mathematics', sourceUrl: OFFICIAL.redevelopmentSchedule, timing: 'confirmed',
  },
  music: {
    introductionYear: 2027, firstExamYear: 2029, outgoingLastExamYear: 2028,
    replacementName: 'Music', sourceUrl: OFFICIAL.redevelopmentSchedule, timing: 'confirmed',
  },
  'physics-and-chemistry': {
    introductionYear: 2027, firstExamYear: 2029, outgoingLastExamYear: 2028,
    replacementName: 'Physics and Chemistry', sourceUrl: OFFICIAL.redevelopmentSchedule, timing: 'confirmed',
  },
};

const redevelopedSpecifications: CanonicalCurriculumSpecification[] = MARK_BANK_SUBJECTS
  /* Not every Mark Bank subject has a redeveloped specification to record.
   * Home Economics is taught and examined on the Scientific and Social
   * syllabus; the NCCA schedule introduces its replacement in 2027 for first
   * examination in 2029, and that specification is not published, so there is
   * nothing here to cite. Its record is `home-economics:current` below.
   * Mapping over every subject regardless would assert a specification that
   * does not exist — and it threw on the missing entry the moment a subject
   * without one was added to the deck. */
  .filter((subject) => transitionSubjects[subject.id] && subject.id !== 'business')
  .map((subject) => {
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

/**
 * Leaving Certificate Business introduced in September 2025 and first
 * examined in 2027. The official specification is not the outgoing seven-unit
 * Mark Bank deck: it has one unifying strand and four contextual strands.
 */
const business2027Specification: CanonicalCurriculumSpecification = {
  id: 'business:2027',
  subjectId: 'business',
  subjectName: 'Business',
  programme: 'leaving-certificate-established',
  category: 'business',
  levels: ['higher', 'ordinary'],
  title: 'Leaving Certificate Business — specification examined from 2027',
  firstExamYear: 2027,
  status: 'verified',
  sources: [
    {
      authority: 'Curriculum Online',
      title: 'Leaving Certificate Business',
      url: OFFICIAL.business,
      role: 'transition',
    },
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Business Specification',
      url: OFFICIAL.businessSpecification,
      role: 'content',
    },
  ],
  groups: [
    {
      id: 'business-2027-unifying',
      title: 'Unifying Strand: Investigating Business',
      topics: [
        { id: 'business-2027-u1', code: 'U1', title: 'Developing questions to research' },
        { id: 'business-2027-u2', code: 'U2', title: 'Managing information' },
        { id: 'business-2027-u3', code: 'U3', title: 'Project planning' },
        { id: 'business-2027-u4', code: 'U4', title: 'Analysing and evaluating information' },
        { id: 'business-2027-u5', code: 'U5', title: 'Presenting findings and perspectives' },
        { id: 'business-2027-u6', code: 'U6', title: 'Acknowledging sources' },
      ],
    },
    {
      id: 'business-2027-strand-1',
      code: '1',
      title: 'Strand 1: Exploring the Business Environment',
      topics: [
        { id: 'business-2027-1-1', code: '1.1', title: 'Key stakeholders in business' },
        { id: 'business-2027-1-2', code: '1.2', title: 'Forms of business, business regulation and governance' },
        { id: 'business-2027-1-3', code: '1.3', title: 'Business and the economy' },
        { id: 'business-2027-1-4', code: '1.4', title: 'The influence of national and EU policy' },
        { id: 'business-2027-1-5', code: '1.5', title: 'Irish business globally and internationally' },
        { id: 'business-2027-1-6', code: '1.6', title: 'Applying my learning' },
      ],
    },
    {
      id: 'business-2027-strand-2',
      code: '2',
      title: 'Strand 2: Understanding enterprise',
      topics: [
        { id: 'business-2027-2-1', code: '2.1', title: 'Enterprise in its broadest sense' },
        { id: 'business-2027-2-2', code: '2.2', title: 'Idea development' },
        { id: 'business-2027-2-3', code: '2.3', title: 'Business planning' },
        { id: 'business-2027-2-4', code: '2.4', title: 'The target market' },
        { id: 'business-2027-2-5', code: '2.5', title: 'Operations and finance' },
        { id: 'business-2027-2-6', code: '2.6', title: 'Growth, development, and expansion' },
        { id: 'business-2027-2-7', code: '2.7', title: 'Managing risk' },
        { id: 'business-2027-2-8', code: '2.8', title: 'Applying my learning' },
      ],
    },
    {
      id: 'business-2027-strand-3',
      code: '3',
      title: 'Strand 3: Leading in Business',
      topics: [
        { id: 'business-2027-3-1', code: '3.1', title: 'Leading and managing an organisation' },
        { id: 'business-2027-3-2', code: '3.2', title: 'Leading and managing people' },
        { id: 'business-2027-3-3', code: '3.3', title: 'The importance of communication' },
        { id: 'business-2027-3-4', code: '3.4', title: 'The rationale for planning' },
        { id: 'business-2027-3-5', code: '3.5', title: 'Applying my learning' },
      ],
    },
    {
      id: 'business-2027-strand-4',
      code: '4',
      title: 'Strand 4: Being Informed and Making Informed Decisions',
      topics: [
        { id: 'business-2027-4-1', code: '4.1', title: 'Making informed decisions as a consumer' },
        { id: 'business-2027-4-2', code: '4.2', title: 'Making informed financial decisions' },
        { id: 'business-2027-4-3', code: '4.3', title: 'Being an informed employee' },
      ],
    },
  ],
  coverageNodeLevel: 'topic',
  recommendedClassHours: 180,
  assessmentComponents: [
    {
      id: 'business-2027-investigative-study',
      title: 'Business Alive Investigative Study',
      kind: 'coursework',
      weighting: 40,
      levels: ['higher', 'ordinary'],
      required: true,
      notes: ['Completed from a common brief and submitted digitally during sixth year.'],
    },
    {
      id: 'business-2027-written-examination',
      title: 'Written examination',
      kind: 'written-examination',
      weighting: 60,
      levels: ['higher', 'ordinary'],
      required: true,
    },
  ],
  legacyTopicAliases: {
    'business-0-12': 'business-2027-1-1',
    'business-0-13': 'business-2027-4-1',
    'business-0-14': 'business-2027-4-3',
    'business-1-5': 'business-2027-2-1',
    'business-2-11': 'business-2027-3-1',
    'business-2-12': 'business-2027-3-3',
    'business-2-13': 'business-2027-3-4',
    'business-3-16': 'business-2027-2-5',
    'business-3-17': 'business-2027-2-7',
    'business-3-18': 'business-2027-1-3',
    'business-3-19': 'business-2027-2-5',
    'business-3-20': 'business-2027-3-2',
    'business-3-21': 'business-2027-3-4',
    'business-4-14': 'business-2027-2-2',
    'business-4-15': 'business-2027-2-3',
    'business-4-16': 'business-2027-2-4',
    'business-4-17': 'business-2027-2-4',
    'business-4-18': 'business-2027-2-6',
    'business-4-19': 'business-2027-u4',
    'business-5-13': 'business-2027-1-2',
    'business-5-14': 'business-2027-1-2',
    'business-5-15': 'business-2027-1-3',
    'business-5-16': 'business-2027-2-1',
    'business-5-17': 'business-2027-1-2',
    'business-6-13': 'business-2027-1-5',
    'business-6-14': 'business-2027-1-4',
    'business-6-15': 'business-2027-1-5',
  },
  notes: [
    'The unifying strand permeates all four contextual strands.',
    'Legacy aliases keep historic Mark Bank mastery resolvable without exposing the outgoing seven-unit map as the 2027 specification.',
  ],
};

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

const engineering2028Specification: CanonicalCurriculumSpecification = {
  id: 'engineering:2028',
  subjectId: 'engineering',
  subjectName: 'Engineering',
  programme: 'leaving-certificate-established',
  category: 'practical-applied',
  levels: ['higher', 'ordinary'],
  title: 'Leaving Certificate Engineering — specification examined from 2028',
  firstExamYear: 2028,
  status: 'verified',
  sources: [
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Engineering curriculum specification',
      url: OFFICIAL.engineeringSpecification,
      role: 'content',
    },
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Engineering assessment for certification',
      url: OFFICIAL.engineeringSpecification,
      role: 'assessment',
    },
  ],
  recommendedClassHours: 180,
  groups: [
    canonicalGroup('engineering-2028-processes', 'Engineering Processes', [
      ['engineering-2028-1-cadcam', 'CAD/CAM'],
      ['engineering-2028-1-engineering-in-society', 'Engineering in society'],
      ['engineering-2028-1-manufacturing-skills', 'Manufacturing skills'],
      ['engineering-2028-1-materials-processing-selection', 'Materials processing and selection'],
      ['engineering-2028-1-measurement-quality-automation', 'Measurement, quality and automation'],
      ['engineering-2028-1-project-planning-evaluation', 'Project planning and evaluation'],
    ]),
    canonicalGroup('engineering-2028-automation-control', 'Automation and Control Systems', [
      ['engineering-2028-2-advanced-autonomous-systems', 'Advanced and autonomous systems'],
      ['engineering-2028-2-communication-programming-debugging', 'Communication, programming and debugging'],
      ['engineering-2028-2-control-system-design', 'Control-system design'],
      ['engineering-2028-2-control-systems', 'Control systems'],
      ['engineering-2028-2-sensors-actuators-energy', 'Sensors, actuators and energy'],
    ]),
    canonicalGroup('engineering-2028-design-capability', 'Design Capability', [
      ['engineering-2028-3-design-process-sustainability', 'Design process and sustainability'],
      ['engineering-2028-3-specification-prototyping', 'Engineering specification and prototyping'],
      ['engineering-2028-3-human-centred-design', 'Functionality and human-centred design'],
      ['engineering-2028-3-sketching-visualisation-communication', 'Sketching, visualisation and communication'],
    ]),
    canonicalGroup('engineering-2028-principles-energy', 'Engineering Principles and Energy', [
      ['engineering-2028-4-electrical-pneumatic-hydraulic', 'Electrical, pneumatic and hydraulic systems'],
      ['engineering-2028-4-energy-power', 'Energy and power'],
      ['engineering-2028-4-materials', 'Materials'],
      ['engineering-2028-4-mechanisms-motion-structures', 'Mechanisms, motion and structures'],
    ]),
  ],
  coverageNodeLevel: 'topic',
  assessmentComponents: [
    {
      id: 'engineering-2028-design-manufacture-project',
      title: 'Design and manufacture project',
      kind: 'project',
      weighting: 50,
      levels: ['common'],
      required: true,
      notes: ['Based on a common brief issued by the State Examinations Commission.'],
    },
    {
      id: 'engineering-2028-written-examination',
      title: 'Written examination',
      kind: 'written-examination',
      weighting: 50,
      levels: ['higher', 'ordinary'],
      required: true,
    },
  ],
  notes: [
    'Introduced to fifth-year students in September 2026.',
    'The four official strands remain canonical. The trackable study areas consolidate the specification learning outcomes into the same practical clusters used by the audited exam-topic menu.',
    'The factual practice label “Advanced and Autonomous System” is retained in Topic Atlas, while this canonical record corrects it to the plural “systems”.',
  ],
};

const physicalEducation2028Specification: CanonicalCurriculumSpecification = {
  id: 'physical-education:2028',
  subjectId: 'physical-education',
  subjectName: 'Physical Education',
  programme: 'leaving-certificate-established',
  category: 'practical-applied',
  levels: ['higher', 'ordinary'],
  title: 'Leaving Certificate Physical Education — specification examined from 2028',
  firstExamYear: 2028,
  status: 'verified',
  sources: [
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Physical Education curriculum specification',
      url: OFFICIAL.physicalEducation2028Specification,
      role: 'content',
    },
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Physical Education assessment for certification',
      url: OFFICIAL.physicalEducation2028Specification,
      role: 'assessment',
    },
  ],
  recommendedClassHours: 180,
  groups: [
    canonicalGroup('physical-education-2028-skill-performance', 'Skill learning, participation and performance', []),
    canonicalGroup('physical-education-2028-demands-performance', 'Physical and psychological demands of performance', []),
    canonicalGroup('physical-education-2028-participation-factors', 'Factors influencing participation in physical activity', []),
  ],
  coverageNodeLevel: 'group',
  assessmentComponents: [
    {
      id: 'physical-education-2028-project',
      title: 'Physical Education project',
      kind: 'project',
      weighting: 50,
      levels: ['common'],
      required: true,
      notes: ['Based on a common brief issued by the State Examinations Commission.'],
    },
    {
      id: 'physical-education-2028-written-examination',
      title: 'Written examination',
      kind: 'written-examination',
      weighting: 50,
      levels: ['higher', 'ordinary'],
      required: true,
    },
  ],
  notes: [
    'Introduced to fifth-year students in September 2026.',
    'Coverage uses the three official strands; the 2018 specification is not carried into the 2028 cohort.',
  ],
};

const lifeCommunityWork2028Specification: CanonicalCurriculumSpecification = {
  id: 'lcvp-link-modules:2028',
  // Keep the established LCVP identity so saved profiles and confidence data survive the replacement.
  subjectId: 'lcvp-link-modules',
  subjectName: 'Life, Community and Work',
  programme: 'lcvp',
  category: 'business',
  levels: ['common'],
  title: 'Leaving Certificate Life, Community and Work — specification examined from 2028',
  firstExamYear: 2028,
  status: 'verified',
  sources: [
    {
      authority: 'NCCA',
      title: 'Leaving Certificate Life, Community and Work curriculum specification',
      url: OFFICIAL.lifeCommunityWorkSpecification,
      role: 'content',
    },
    {
      authority: 'NCCA',
      title: 'Life, Community and Work assessment for certification',
      url: OFFICIAL.lifeCommunityWorkSpecification,
      role: 'assessment',
    },
  ],
  recommendedClassHours: 120,
  groups: [
    canonicalGroup('life-community-work-2028-understanding-myself', 'Understanding Myself', []),
    canonicalGroup('life-community-work-2028-progression', 'Understanding my Progression Opportunities', []),
    canonicalGroup('life-community-work-2028-community', 'Appreciating my Community', []),
    canonicalGroup('life-community-work-2028-workplace', 'Engaging with the Workplace', []),
  ],
  coverageNodeLevel: 'group',
  assessmentComponents: [
    {
      id: 'life-community-work-2028-portfolio',
      title: 'Portfolio in Action',
      kind: 'coursework',
      weighting: 60,
      levels: ['common'],
      required: true,
      notes: ['A multimodal response to an annual brief issued by the State Examinations Commission.'],
    },
    {
      id: 'life-community-work-2028-written-examination',
      title: 'Written examination',
      kind: 'written-examination',
      weighting: 40,
      levels: ['common'],
      required: true,
    },
  ],
  notes: [
    'Introduced to fifth-year students in September 2026, replacing the LCVP programme statement.',
    'The four official strands sit across the integrated modules Me and my Future and Community and Work.',
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
      groups: MATHS_GROUPS,
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
  if (spec.subjectId === 'engineering') {
    return {
      ...spec,
      id: 'engineering:materials-and-technology',
      title: 'Leaving Certificate Engineering — Materials and Technology',
      status: 'verified',
      groups: ENGINEERING_GROUPS,
      sources: [
        { authority: 'Curriculum Online', title: 'Engineering', url: OFFICIAL.engineering, role: 'content' },
        { authority: 'Curriculum Online', title: 'Engineering syllabus', url: OFFICIAL.engineeringSyllabus, role: 'content' },
      ],
      /* 600 marks in total: the written paper 300, the practical examination
       * 150 and the project 150. The Mark Bank cards the WRITTEN paper only —
       * the other two are made in a workshop and have no marking scheme text
       * to lift. */
      assessmentComponents: [
        {
          id: 'engineering-written-examination',
          title: 'Written examination',
          kind: 'written-examination',
          weighting: 50,
          levels: ['higher', 'ordinary'],
          required: true,
        },
        {
          id: 'engineering-practical-examination',
          title: 'Practical examination',
          kind: 'practical-examination',
          weighting: 25,
          levels: ['higher', 'ordinary'],
          required: true,
        },
        {
          id: 'engineering-project',
          title: 'Project',
          kind: 'project',
          weighting: 25,
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
      groups: COMPUTER_SCIENCE_GROUPS,
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
  const verifiedOutgoing: Record<string, { id: string; title: string; lastExamYear: number;
    source: string; note: string; groups?: CanonicalCurriculumSpecification['groups'] }> = {
    english: {
      id: 'english:outgoing', title: 'Leaving Certificate English syllabus — examination to June 2028',
      lastExamYear: 2028, source: OFFICIAL.english,
      note: 'The replacement specification will not be introduced earlier than September 2027 and needs a separate canonical record.',
    },
    'construction-studies': {
      id: 'construction-studies:outgoing', title: 'Leaving Certificate Construction Studies syllabus — examination to June 2027',
      lastExamYear: 2027, source: OFFICIAL.constructionStudies,
      note: 'Construction Technology is introduced to fifth-year students in September 2026 and needs a separate canonical record.',
      groups: CONSTRUCTION_STUDIES_GROUPS,
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
      // An outgoing subject still needs its own groups, or a Mark Bank card
      // tagged to it resolves into a specification that contains no such topic.
      // Construction Studies shipped without them and the check only caught it
      // once the deck could actually be loaded.
      ...(outgoing.groups ? { groups: outgoing.groups } : {}),
    };
  }
  return spec;
}

function applyScheduledOutgoingBoundary(
  specification: CanonicalCurriculumSpecification,
): CanonicalCurriculumSpecification {
  const transition = CURRICULUM_REDEVELOPMENT_TRANSITIONS[specification.subjectId];
  if (!transition) return specification;
  if (specification.firstExamYear && specification.firstExamYear >= transition.firstExamYear) return specification;
  if ((specification.lastExamYear ?? Infinity) <= transition.outgoingLastExamYear) return specification;

  return {
    ...specification,
    lastExamYear: transition.outgoingLastExamYear,
    title: `${specification.title.replace(/\s+— examination to June \d{4}$/, '')} — examination to June ${transition.outgoingLastExamYear}`,
    notes: [
      ...(specification.notes ?? []),
      `${transition.replacementName} is scheduled for introduction to fifth-year students in ${transition.introductionYear}; this outgoing record must not be resolved for the ${transition.firstExamYear} examination cohort.`,
    ],
  };
}

export const CURRICULUM_SPECIFICATIONS: CanonicalCurriculumSpecification[] = [
  ...legacySpecifications.map(patchLegacySpecification).map(applyScheduledOutgoingBoundary),
  ...redevelopedSpecifications,
  business2027Specification,
  constructionTechnologySpecification,
  geography2028Specification,
  engineering2028Specification,
  physicalEducation2028Specification,
  lifeCommunityWork2028Specification,
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

export interface CurriculumCohortNotice {
  kind: 'outgoing' | 'replacement-pending';
  title: string;
  message: string;
  sourceUrl: string;
  replacementExamYear: number;
}

/**
 * Student-facing transition copy for the selected examination cohort. It
 * never guesses a replacement taxonomy: if a future specification has not
 * yet been encoded and verified, the old map stays unavailable.
 */
export function getCurriculumCohortNotice(
  subject: string,
  examYear = examinationYearFromDate(),
): CurriculumCohortNotice | undefined {
  const subjectId = resolveSubjectId(subject);
  if (!subjectId) return undefined;
  const transition = CURRICULUM_REDEVELOPMENT_TRANSITIONS[subjectId];
  if (!transition) return undefined;

  if (examYear <= transition.outgoingLastExamYear) {
    const isFinalOutgoingCohort = examYear === transition.outgoingLastExamYear;
    const title = transition.outgoingLastExamYear === 2027 && isFinalOutgoingCohort
      ? 'For 2027 exam candidates only'
      : `Current specification — exams through ${transition.outgoingLastExamYear}`;
    const timing = transition.timing === 'not-before'
      ? `The replacement has been postponed until at least September ${transition.introductionYear}, so ${transition.firstExamYear} is the earliest possible first examination year.`
      : `${transition.replacementName} is introduced to fifth-year students in September ${transition.introductionYear} and is first examined in ${transition.firstExamYear}.`;
    const cohortContext = isFinalOutgoingCohort
      ? `This topic map follows the outgoing specification for the ${examYear} exam cohort.`
      : `This topic map follows the current outgoing specification for your ${examYear} exam cohort and remains in use through the ${transition.outgoingLastExamYear} exams.`;
    return {
      kind: 'outgoing',
      title,
      message: `${cohortContext} ${timing} Do not use this map for the ${transition.firstExamYear} cohort.`,
      sourceUrl: transition.sourceUrl,
      replacementExamYear: transition.firstExamYear,
    };
  }

  const active = resolveCurriculumSpecification(subjectId, examYear);
  if (active?.firstExamYear && active.firstExamYear >= transition.firstExamYear) return undefined;

  return {
    kind: 'replacement-pending',
    title: `${transition.firstExamYear} specification being verified`,
    message: `The outgoing ${subject} map ended with the ${transition.outgoingLastExamYear} exams. We will not show it for your cohort. Use the official ${transition.replacementName} specification while the new map is checked and added here.`,
    sourceUrl: transition.sourceUrl,
    replacementExamYear: transition.firstExamYear,
  };
}

export function findCanonicalTopic(
  specification: CanonicalCurriculumSpecification,
  topicId: string,
): CanonicalCurriculumTopic | undefined {
  const topics = specification.groups.flatMap((group) => group.topics);
  const canonicalId = specification.legacyTopicAliases?.[topicId] ?? topicId;
  return topics.find((topic) => topic.id === canonicalId);
}

export function specificationContainsId(
  specification: CanonicalCurriculumSpecification,
  nodeId: string,
): boolean {
  if (specification.groups.some((group) =>
    group.id === nodeId || group.topics.some((topic) => topic.id === nodeId),
  )) return true;
  const canonicalId = specification.legacyTopicAliases?.[nodeId];
  return canonicalId
    ? specification.groups.some((group) => group.topics.some((topic) => topic.id === canonicalId))
    : false;
}
