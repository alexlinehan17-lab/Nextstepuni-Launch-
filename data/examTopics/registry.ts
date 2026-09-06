/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Student-facing exam-topic taxonomy.
 *
 * The canonical curriculum registry remains the authority for Syllabus X-Ray.
 * This layer records the flatter, level-aware question groupings students use
 * when browsing exam practice.  Keeping the two identities separate prevents
 * a commercial site's browse menu from erasing official syllabus nodes, while
 * the crosswalk lets the two surfaces link to each other.
 */

import type { PaperLang, PaperLevel } from '../../types/paperTrail';
import { PAPER_TOPIC_TAGS } from '../paperTrail/topicTags';
import accountingAuditJson from './accounting.json';
import agriculturalScienceAuditJson from './agricultural-science.json';
import appliedMathematicsAuditJson from './applied-mathematics.json';
import artRuntimeJson from './art-runtime.json';
import biologyRuntimeJson from './biology-runtime.json';
import businessRuntimeJson from './business-runtime.json';
import chemistryRuntimeJson from './chemistry-runtime.json';
import classicalStudiesAuditJson from './classical-studies.json';
import computerScienceRuntimeJson from './computer-science-runtime.json';
import constructionStudiesRuntimeJson from './construction-studies-runtime.json';
import designAndCommunicationGraphicsRuntimeJson from './design-and-communication-graphics-runtime.json';
import directQuestionRuntimeJson from './direct-question-runtime.json';
import economicsRuntimeJson from './economics-runtime.json';
import engineeringRuntimeJson from './engineering-runtime.json';
import englishQuestionRuntimeJson from './english-question-runtime.json';
import englishRuntimeJson from './english-runtime.json';
import frenchRuntimeJson from './french-runtime.json';
import geographyQuestionRuntimeJson from './geography-question-runtime.json';
import geographyRuntimeJson from './geography-runtime.json';
import germanRuntimeJson from './german-runtime.json';
import historyRuntimeJson from './history-runtime.json';
import homeEconomicsQuestionRuntimeJson from './home-economics-s-and-s-question-runtime.json';
import homeEconomicsRuntimeJson from './home-economics-s-and-s-runtime.json';
import irishRuntimeJson from './irish-runtime.json';
import italianRuntimeJson from './italian-runtime.json';
import japaneseAuditJson from './japanese.json';
import japaneseRuntimeJson from './japanese-runtime.json';
import linkModulesAuditJson from './link-modules.json';
import mathematicsQuestionRuntimeJson from './mathematics-question-runtime.json';
import mathematicsRuntimeJson from './mathematics-runtime.json';
import musicRuntimeJson from './music-runtime.json';
import physicalEducationQuestionRuntimeJson from './physical-education-question-runtime.json';
import physicalEducationRuntimeJson from './physical-education-runtime.json';
import physicsRuntimeJson from './physics-runtime.json';
import physicsAndChemistryRuntimeJson from './physics-and-chemistry-runtime.json';
import politicsAndSocietyAuditJson from './politics-and-society.json';
import religiousEducationRuntimeJson from './religious-education-runtime.json';
import spanishRuntimeJson from './spanish-runtime.json';
import technologyRuntimeJson from './technology-runtime.json';

export type ExamSitting = 'main' | 'deferred' | 'sample';

export interface ExamTopicDefinition {
  id: string;
  label: string;
  level: PaperLevel;
  /** Public page path used to re-audit the classification. */
  sourcePath: string;
  /** Official State-exam question identities; never commercial question text. */
  officialQuestionKeys: string[];
  /** Count only. Commercial mock content is deliberately excluded. */
  mockQuestionCount: number;
  /** Canonical curriculum nodes covered by this exam-practice bucket. */
  curriculumNodeIds: string[];
  /** Course identity where a subject exposes overlapping specifications. */
  course?: 'new' | 'old';
  /** Total items shown by the audited reference page. */
  reportedQuestionCount?: number;
  /** Count only. Provider-owned sample content is never copied or mapped. */
  providerSampleQuestionCount?: number;
  /** True when the linked reference page itself was unavailable during audit. */
  referenceUnavailable?: boolean;
}

export interface ExamTopicGroup {
  id: string;
  label: string;
  level: PaperLevel;
  topicIds: string[];
  course?: 'new' | 'old';
}

export interface ExamTopicTaxonomy {
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  groups: ExamTopicGroup[];
  topics: ExamTopicDefinition[];
}

export interface ExamQuestionPartReference {
  subjectId: string;
  level: PaperLevel;
  year: number;
  sitting: ExamSitting;
  /** Stable Paper Trail slot (`single`, `p1`, `p2`, `aural`, …). */
  paperKey: string;
  /** Exact booklet where independently selectable Art components reuse Q1. */
  fileid?: string;
  /** Top-level number printed on the official paper. */
  n: string;
  /** Factual heading only (section/part/roman-numeral range); never question text. */
  subdivision?: string;
  topicId: string;
}

interface AccountingAuditTopic {
  id: string;
  label: string;
  sourcePath: string;
  officialQuestions: string[];
  mockQuestionCount: number;
}

interface AccountingAudit {
  subjectId: string;
  capturedAt: string;
  reference: { provider: string };
  levels: Record<'higher' | 'ordinary', {
    label: string;
    topics: AccountingAuditTopic[];
  }>;
}

interface AppliedMathematicsAuditTopic {
  id: string;
  label: string;
  sourcePath: string;
  officialQuestionHeadings: string[];
  mockQuestionCount: number;
  empty?: boolean;
}

interface AppliedMathematicsAudit {
  subjectId: string;
  capturedAt: string;
  reference: { provider: string };
  levels: Record<'higher' | 'ordinary', {
    label: string;
    topics: AppliedMathematicsAuditTopic[];
  }>;
}

interface LinkModulesAudit {
  subjectId: string;
  capturedAt: string;
  reference: { provider: string };
  levels: {
    common: {
      label: string;
      topics: AppliedMathematicsAuditTopic[];
    };
  };
}

interface JapaneseAudit {
  subjectId: string;
  capturedAt: string;
  reference: { provider: string };
  levels: {
    common: {
      label: string;
      topics: AppliedMathematicsAuditTopic[];
    };
  };
}

interface JapaneseRuntime {
  v: 1;
  /** [topic index, year, h/o/common, single/aural/oral, printed question, factual heading] */
  partReferences: Array<[number, number, 'h' | 'o' | 'c', 's' | 'a' | 'r', string, string]>;
  /** [h/o, e/i, year, single/aural, printed question, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, 's' | 'a', string, number[]]>;
}

interface ItalianRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, display label, topic indexes] */
  groups: Array<['h' | 'o', string, number[]]>;
  /** [id, label, source path, mock count, provider-sample count, curriculum ids, h/o, reported total] */
  topics: Array<[string, string, string, number, number, string[], 'h' | 'o', number]>;
  /** [topic index, year-2000, h/o, single/aural, local card number, factual heading] */
  partReferences: Array<[number, number, 'h' | 'o', 's' | 'a', string, string]>;
  /** [h/o, e/i, year-2000, single/aural, local card number, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, 's' | 'a', string, number[]]>;
}

interface FrenchRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, exact level label, topic indexes] */
  groups: Array<['h' | 'o', string, number[]]>;
  /** [id, label, source path, mock count, provider-sample count, curriculum ids, h/o, reported total] */
  topics: Array<[string, string, string, number, number, string[], 'h' | 'o', number]>;
  /** [topic index, year-2000, h/o, single/aural/oral, main/deferred, local number, factual heading] */
  partReferences: Array<[number, number, 'h' | 'o', 's' | 'a' | 'o', 'm' | 'd', string, string]>;
  /** [h/o, e/i, year-2000, single/aural, local card number, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, 's' | 'a', string, number[]]>;
}

interface GermanRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, stable group id, exact display label, topic indexes] */
  groups: Array<['h' | 'o', string, string, number[]]>;
  /** [id, label, source path, mock count, provider-sample count, curriculum ids, h/o, reported total] */
  topics: Array<[string, string, string, number, number, string[], 'h' | 'o', number]>;
  /** [topic index, year-2000, h/o, single/aural, main/deferred, local number, factual heading] */
  partReferences: Array<[number, number, 'h' | 'o', 's' | 'a', 'm' | 'd', string, string]>;
  /** [h/o, e/i, year-2000, single/aural, local card number, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, 's' | 'a', string, number[]]>;
}

interface MusicRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, stable group id, display label, topic indexes] */
  groups: Array<['h' | 'o', string, string, number[]]>;
  /** [id, label, source path, mock count, provider-sample count, curriculum ids, h/o, reported total, reference/archive] */
  topics: Array<[string, string, string, number, number, string[], 'h' | 'o', number, 0 | 1]>;
  /** [topic index, year-2000, h/o, sitting, SEC component, local number, factual heading, matched fileid] */
  partReferences: Array<[
    number,
    number,
    'h' | 'o',
    'm' | 'd' | 'x',
    '6' | '7' | '8' | 'u',
    string,
    string,
    string,
  ]>;
  /** [h/o, e/i, year-2000, SEC component, local card number, topic indexes] */
  questionMappings: Array<[
    'h' | 'o',
    'e' | 'i',
    number,
    '6' | '7' | '8' | 'u',
    string,
    number[],
  ]>;
}

interface IrishRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o/f, stable group id, exact level label, topic indexes] */
  groups: Array<['h' | 'o' | 'f', string, string, number[]]>;
  /** [id, label, source path, mock count, provider-sample count, curriculum ids, h/o/f, reported total, reference/local] */
  topics: Array<[string, string, string, number, number, string[], 'h' | 'o' | 'f', number, 0 | 1]>;
  /** [topic index, year-2000, h/o/f, paper key, sitting, local number, factual heading] */
  partReferences: Array<[
    number,
    number,
    'h' | 'o' | 'f',
    's' | '1' | '2' | 'a' | 'o',
    'm' | 'd' | 'x',
    string,
    string,
  ]>;
  /** [h/o/f, e/i, year-2000, paper key, local card number, topic indexes] */
  questionMappings: Array<[
    'h' | 'o' | 'f',
    'e' | 'i',
    number,
    's' | '1' | '2' | 'a',
    string,
    number[],
  ]>;
}

interface SpanishRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, stable group id, exact display label, topic indexes] */
  groups: Array<['h' | 'o', string, string, number[]]>;
  /** [id, label, source path, mock count, provider-sample count, curriculum ids, h/o, reported total] */
  topics: Array<[string, string, string, number, number, string[], 'h' | 'o', number]>;
  /** [topic index, year-2000, h/o, written/aural/oral, main/deferred, local number, factual heading] */
  partReferences: Array<[number, number, 'h' | 'o', 'w' | 'a' | 'o', 'm' | 'd', string, string]>;
  /** [h/o, e/i, year-2000, written/aural, local card number, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, 'w' | 'a', string, number[]]>;
}

interface HistoryRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, group label, topic indexes] */
  groups: Array<['h' | 'o', string, number[]]>;
  /** [topic id, label, source path, mock count, canonical curriculum ids, h/o] */
  topics: Array<[string, string, string, number, string[], 'h' | 'o']>;
  /** [topic index, year, main/deferred, local-or-reference number, factual heading] */
  partReferences: Array<[number, number, 'm' | 'd', string, string]>;
  /** [h/o, e/i, year, local card number, topic index] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, string, number]>;
}

interface EconomicsRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, group label, topic indexes] */
  groups: Array<['h' | 'o', string, number[]]>;
  /** [topic id, label, source path, mock count, canonical curriculum ids, h/o] */
  topics: Array<[string, string, string, number, string[], 'h' | 'o']>;
  /** [topic index, year, main/deferred/sample, local-or-reference number, factual heading] */
  partReferences: Array<[number, number, 'm' | 'd' | 's', string, string]>;
  /** [h/o, e/i, year, local card number, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, string, number[]]>;
}

interface ArtRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, stable group id, exact display label, topic indexes] */
  groups: Array<['h' | 'o', string, string, number[]]>;
  /** [id, label, source path, mock count, provider-sample count, curriculum ids, h/o, reported total] */
  topics: Array<[string, string, string, number, number, string[], 'h' | 'o', number]>;
  /** [topic index, year-2000, main/deferred/sample, component code or blank, printed number, heading] */
  partReferences: Array<[number, number, 'm' | 'd' | 's', string, string, string]>;
  /** [h/o, e/i, year-2000, component code, printed number, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, string, string, number[]]>;
}

interface ComputerScienceRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, group label, topic indexes] */
  groups: Array<['h' | 'o', string, number[]]>;
  /** [topic id, label, source path, mock count, canonical curriculum ids, h/o] */
  topics: Array<[string, string, string, number, string[], 'h' | 'o']>;
  /** [topic index, year, main/sample, local-or-reference number, factual heading] */
  partReferences: Array<[number, number, 'm' | 's', string, string]>;
  /** [h/o, e/i, year, local card number, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, string, number[]]>;
}

interface BiologyRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, new/old, stable id, display label, topic indexes] */
  groups: Array<['h' | 'o', 'n' | 'o', string, string, number[]]>;
  /**
   * [terminal slug, label, mock count, provider-sample count,
   *  curriculum ids, reported total]. Identity fields are reconstructed from
   *  the exact group membership.
   */
  topics: Array<[
    string,
    string,
    number,
    number,
    string[],
    number,
  ]>;
  headingPrefixes: string[];
  headingTails: string[];
  /** [topic index, year-2000, prefix index, printed question, tail index] */
  partReferences: Array<[number, number, number, string, number]>;
  /** [h/o, year-2000, printed question, topic indexes] */
  questionMappings: Array<['h' | 'o', number, string, number[]]>;
}

interface BusinessRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, new/old, stable id, display label, topic indexes] */
  groups: Array<['h' | 'o', 'n' | 'o', string, string, number[]]>;
  /** [terminal slug, label, mock count, provider-sample count, curriculum ids, reported total] */
  topics: Array<[string, string, number, number, string[], number]>;
  headingPrefixes: string[];
  headingTails: string[];
  /** [topic index, year-2000, prefix index, printed token, tail index, paper key, stable card number] */
  partReferences: Array<[
    number,
    number,
    number,
    string,
    number,
    's' | '1' | '2',
    string,
  ]>;
  /** [h/o, year-2000, paper key, stable card number, topic indexes] */
  questionMappings: Array<['h' | 'o', number, 's' | '1' | '2', string, number[]]>;
}

interface ConstructionStudiesRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, new/outgoing, stable id, display label, topic indexes] */
  groups: Array<['h' | 'o', 'n' | 'o', string, string, number[]]>;
  /** [terminal slug, label, mock count, provider-sample count, curriculum ids, reported total] */
  topics: Array<[string, string, number, number, string[], number]>;
  headingPrefixes: string[];
  headingTails: string[];
  /** [topic index, year-2000, prefix index, printed token, tail index, stable card number] */
  partReferences: Array<[number, number, number, string, number, string]>;
  /** [h/o, year-2000, stable card number, topic indexes] */
  questionMappings: Array<['h' | 'o', number, string, number[]]>;
}

interface EngineeringRuntime extends ConstructionStudiesRuntime {}

interface TechnologyRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, stable group id, exact display label, topic indexes] */
  groups: Array<['h' | 'o', string, string, number[]]>;
  /** [terminal slug, label, mock count, provider-sample count, curriculum ids, reported total] */
  topics: Array<[string, string, number, number, string[], number]>;
  headingPrefixes: string[];
  headingTails: string[];
  files: string[];
  /** [topic index, year-2000, prefix index, printed token, tail index, card number, file index/-1, main/deferred] */
  partReferences: Array<[
    number,
    number,
    number,
    string,
    number,
    string,
    number,
    'm' | 'd',
  ]>;
  /** [h/o, year-2000, stable card number, topic indexes] */
  questionMappings: Array<['h' | 'o', number, string, number[]]>;
}

interface ChemistryRuntime extends BiologyRuntime {}

interface PhysicsRuntime extends BiologyRuntime {}

interface DesignAndCommunicationGraphicsRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, group label, topic indexes] */
  groups: Array<['h' | 'o', string, number[]]>;
  /** [topic id, label, source path, mock count, canonical curriculum ids, h/o] */
  topics: Array<[string, string, string, number, string[], 'h' | 'o']>;
  /** [topic index, year, main/deferred, B-C/Section-A, local card number, heading] */
  partReferences: Array<[number, number, 'm' | 'd', 's' | 'a', string, string]>;
  /** [h/o, e/i, year, B-C/Section-A, local card number, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, 's' | 'a', string, number[]]>;
}

interface PhysicsAndChemistryRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  groupLabel: string;
  /** [topic id, label, source path, mock count, canonical curriculum ids] */
  topics: Array<[string, string, string, number, string[]]>;
  /** [topic index, year, printed question, factual reference heading] */
  partReferences: Array<[number, number, string, string]>;
  /** [h/o, e/i, year, printed question, topic indexes] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, string, number[]]>;
}

interface ReligiousEducationRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, group label, topic indexes] */
  groups: Array<['h' | 'o', string, number[]]>;
  /** [topic id, label, source path, mock count, canonical curriculum ids, h/o] */
  topics: Array<[string, string, string, number, string[], 'h' | 'o']>;
  /** [topic index, year, local section-card number, factual reference heading] */
  partReferences: Array<[number, number, string, string]>;
  /** [h/o, e/i, year, local section-card number, topic index] */
  questionMappings: Array<['h' | 'o', 'e' | 'i', number, string, number]>;
}

interface BrowserAuditedRuntime {
  v: 1;
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  /** [h/o, new/outgoing/current, stable id, exact display label, topic indexes] */
  groups: Array<['h' | 'o' | 'f', 'n' | 'o' | 'c', string, string, number[]]>;
  /** [id, label, path, mock, provider, curriculum ids, h/o, reported, new/outgoing/current] */
  topics: Array<[
    string,
    string,
    string,
    number,
    number,
    string[],
    'h' | 'o' | 'f',
    number,
    'n' | 'o' | 'c',
    (0 | 1)?,
  ]>;
}

interface BrowserQuestionRuntime {
  schemaVersion: 1;
  subjectId: string;
  topicIds: string[];
  /** [level, language, year, paper slot, exact SEC booklet, card number, topic indexes] */
  questionMappings: Array<[
    'h' | 'o' | 'f',
    'e' | 'i',
    number,
    string,
    string,
    string,
    number[],
  ]>;
}

interface DirectQuestionRuntime {
  v: 1;
  subjects: Array<{
    subjectId: string;
    topicIds: string[];
    /** [level, language, year, paper slot, exact SEC booklet, card number, topic indexes] */
    questionMappings: Array<[
      PaperLevel,
      PaperLang,
      number,
      string,
      string,
      string,
      number[],
    ]>;
  }>;
}

const accountingAudit = accountingAuditJson as AccountingAudit;
const agriculturalScienceAudit = agriculturalScienceAuditJson as AppliedMathematicsAudit;
const appliedMathematicsAudit = appliedMathematicsAuditJson as AppliedMathematicsAudit;
const artRuntime = artRuntimeJson as unknown as ArtRuntime;
const biologyRuntime = biologyRuntimeJson as unknown as BiologyRuntime;
const businessRuntime = businessRuntimeJson as unknown as BusinessRuntime;
const chemistryRuntime = chemistryRuntimeJson as unknown as ChemistryRuntime;
const classicalStudiesAudit = classicalStudiesAuditJson as AppliedMathematicsAudit;
const computerScienceRuntime = computerScienceRuntimeJson as unknown as ComputerScienceRuntime;
const constructionStudiesRuntime = constructionStudiesRuntimeJson as unknown as ConstructionStudiesRuntime;
const designAndCommunicationGraphicsRuntime = designAndCommunicationGraphicsRuntimeJson as unknown as DesignAndCommunicationGraphicsRuntime;
const directQuestionRuntime = directQuestionRuntimeJson as unknown as DirectQuestionRuntime;
const economicsRuntime = economicsRuntimeJson as unknown as EconomicsRuntime;
const engineeringRuntime = engineeringRuntimeJson as unknown as EngineeringRuntime;
const englishQuestionRuntime = englishQuestionRuntimeJson as unknown as BrowserQuestionRuntime;
const englishRuntime = englishRuntimeJson as unknown as BrowserAuditedRuntime;
const frenchRuntime = frenchRuntimeJson as unknown as FrenchRuntime;
const geographyQuestionRuntime = geographyQuestionRuntimeJson as unknown as BrowserQuestionRuntime;
const geographyRuntime = geographyRuntimeJson as unknown as BrowserAuditedRuntime;
const germanRuntime = germanRuntimeJson as unknown as GermanRuntime;
const historyRuntime = historyRuntimeJson as HistoryRuntime;
const homeEconomicsQuestionRuntime = homeEconomicsQuestionRuntimeJson as unknown as BrowserQuestionRuntime;
const homeEconomicsRuntime = homeEconomicsRuntimeJson as unknown as BrowserAuditedRuntime;
const irishRuntime = irishRuntimeJson as unknown as IrishRuntime;
const italianRuntime = italianRuntimeJson as unknown as ItalianRuntime;
const japaneseAudit = japaneseAuditJson as JapaneseAudit;
const japaneseRuntime = japaneseRuntimeJson as JapaneseRuntime;
const linkModulesAudit = linkModulesAuditJson as LinkModulesAudit;
const mathematicsQuestionRuntime = mathematicsQuestionRuntimeJson as unknown as BrowserQuestionRuntime;
const mathematicsRuntime = mathematicsRuntimeJson as unknown as BrowserAuditedRuntime;
const musicRuntime = musicRuntimeJson as unknown as MusicRuntime;
const physicalEducationQuestionRuntime = physicalEducationQuestionRuntimeJson as unknown as BrowserQuestionRuntime;
const physicalEducationRuntime = physicalEducationRuntimeJson as unknown as BrowserAuditedRuntime;
const physicsRuntime = physicsRuntimeJson as unknown as PhysicsRuntime;
const physicsAndChemistryRuntime = physicsAndChemistryRuntimeJson as PhysicsAndChemistryRuntime;
const politicsAndSocietyAudit = politicsAndSocietyAuditJson as AppliedMathematicsAudit;
const religiousEducationRuntime = religiousEducationRuntimeJson as ReligiousEducationRuntime;
const spanishRuntime = spanishRuntimeJson as unknown as SpanishRuntime;
const technologyRuntime = technologyRuntimeJson as unknown as TechnologyRuntime;

const browserAuditLevel = (levelCode: 'h' | 'o' | 'f'): PaperLevel => (
  levelCode === 'h' ? 'higher' : levelCode === 'f' ? 'foundation' : 'ordinary'
);

const browserAuditedTaxonomy = (runtime: BrowserAuditedRuntime): ExamTopicTaxonomy => ({
  subjectId: runtime.subjectId,
  capturedAt: runtime.capturedAt,
  referenceProvider: runtime.referenceProvider,
  groups: runtime.groups.map(([levelCode, courseCode, id, label, topicIndexes]) => ({
    id,
    label,
    level: browserAuditLevel(levelCode),
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = runtime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`${runtime.subjectId}: unknown topic index ${topicIndex}`);
      return topicId;
    }),
    ...(courseCode === 'c' ? {} : { course: courseCode === 'n' ? 'new' as const : 'old' as const }),
  })),
  topics: runtime.topics.map(([
    id,
    label,
    sourcePath,
    mockQuestionCount,
    providerSampleQuestionCount,
    curriculumNodeIds,
    levelCode,
    reportedQuestionCount,
    courseCode,
    referenceUnavailable,
  ]) => ({
    id,
    label,
    sourcePath,
    officialQuestionKeys: [],
    mockQuestionCount,
    providerSampleQuestionCount,
    curriculumNodeIds,
    level: browserAuditLevel(levelCode),
    reportedQuestionCount,
    ...(referenceUnavailable ? { referenceUnavailable: true } : {}),
    ...(courseCode === 'c' ? {} : { course: courseCode === 'n' ? 'new' as const : 'old' as const }),
  })),
});

const ENGLISH_TAXONOMY = browserAuditedTaxonomy(englishRuntime);
const GEOGRAPHY_TAXONOMY = browserAuditedTaxonomy(geographyRuntime);
const HOME_ECONOMICS_TAXONOMY = browserAuditedTaxonomy(homeEconomicsRuntime);
const MATHEMATICS_TAXONOMY = browserAuditedTaxonomy(mathematicsRuntime);
const PHYSICAL_EDUCATION_TAXONOMY = browserAuditedTaxonomy(physicalEducationRuntime);

/**
 * Many-to-many bridge into the official Accounting syllabus.  The order is
 * not a primary/secondary ranking: a StudyClix-style exam bucket can span more
 * than one canonical node, while a question can sit in several exam buckets.
 */
const ACCOUNTING_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'accounting-higher-budgeting-cash': ['accounting-9-6'],
  'accounting-higher-budgeting-flexible': ['accounting-9-5'],
  'accounting-higher-budgeting-production': ['accounting-9-7'],
  'accounting-higher-cash-flow-statements': ['accounting-7-5'],
  'accounting-higher-club-accounts': ['accounting-5-2'],
  'accounting-higher-control-accounts': ['accounting-2-2'],
  'accounting-higher-correction-of-errorssuspense': ['accounting-2-3', 'accounting-2-4'],
  'accounting-higher-costing-job-product-stock-valuation-oh-apportionment': ['accounting-9-2', 'accounting-5-1', 'accounting-9-1'],
  'accounting-higher-costing-marginal': ['accounting-9-3'],
  'accounting-higher-depreciation-of-fixed-assets': ['accounting-2-5'],
  'accounting-higher-farm-accounts': ['accounting-5-4'],
  'accounting-higher-final-accounts-company': ['accounting-4-1'],
  'accounting-higher-final-accounts-manufacturing': ['accounting-5-0'],
  'accounting-higher-final-accounts-sole-trader': ['accounting-3-1'],
  'accounting-higher-fixed-assets-valuation': ['accounting-2-5'],
  'accounting-higher-incomplete-records-a': ['accounting-6-1', 'accounting-6-2', 'accounting-6-3', 'accounting-6-0'],
  'accounting-higher-incomplete-records-b': ['accounting-6-2', 'accounting-6-1', 'accounting-6-3', 'accounting-6-0'],
  'accounting-higher-interpretation-of-accounts': ['accounting-8-1', 'accounting-8-4', 'accounting-8-5', 'accounting-8-6', 'accounting-8-7', 'accounting-8-8', 'accounting-8-9', 'accounting-8-10'],
  'accounting-higher-published-accounts': ['accounting-4-2'],
  'accounting-higher-revaluation-of-fixed-assets': ['accounting-2-5'],
  'accounting-higher-service-firms': ['accounting-5-5'],
  'accounting-higher-tabular-statements': ['accounting-2-6'],

  'accounting-ordinary-bank-reconciliation-statement': ['accounting-2-1'],
  'accounting-ordinary-budgeting-cash': ['accounting-9-6'],
  'accounting-ordinary-budgeting-production': ['accounting-9-7'],
  'accounting-ordinary-cash-flow-statements': ['accounting-7-5'],
  'accounting-ordinary-club-accounts': ['accounting-5-2'],
  'accounting-ordinary-company-profit-loss': ['accounting-4-1'],
  'accounting-ordinary-control-accounts': ['accounting-2-2'],
  'accounting-ordinary-correction-of-errorssuspense': ['accounting-2-3', 'accounting-2-4'],
  'accounting-ordinary-costing-absorption': ['accounting-9-2', 'accounting-9-1'],
  'accounting-ordinary-costing-marginal': ['accounting-9-3'],
  'accounting-ordinary-farm-accounts': ['accounting-5-4'],
  'accounting-ordinary-final-accounts-company': ['accounting-4-1'],
  'accounting-ordinary-final-accounts-departmental': ['accounting-5-3'],
  'accounting-ordinary-final-accounts-manufacturing': ['accounting-5-0'],
  'accounting-ordinary-final-accounts-sole-trader': ['accounting-3-1'],
  'accounting-ordinary-fixed-assets-depreciation-revaluation': ['accounting-2-5'],
  'accounting-ordinary-incomplete-records-control-account': ['accounting-6-1'],
  'accounting-ordinary-incomplete-records-net-worth': ['accounting-6-2'],
  'accounting-ordinary-interpretation-of-accounts': ['accounting-8-1', 'accounting-8-4', 'accounting-8-5', 'accounting-8-6', 'accounting-8-7', 'accounting-8-9'],
  'accounting-ordinary-service-firms': ['accounting-5-5'],
  'accounting-ordinary-tabular-statements': ['accounting-2-6'],
};

const accountingLevels = ['higher', 'ordinary'] as const;
const accountingTopics: ExamTopicDefinition[] = accountingLevels.flatMap((level) =>
  accountingAudit.levels[level].topics.map((topic) => ({
    id: topic.id,
    label: topic.label,
    level,
    sourcePath: topic.sourcePath,
    officialQuestionKeys: topic.officialQuestions,
    mockQuestionCount: topic.mockQuestionCount,
    curriculumNodeIds: ACCOUNTING_CURRICULUM_CROSSWALK[topic.id] ?? [],
  })),
);

const ACCOUNTING_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: accountingAudit.subjectId,
  capturedAt: accountingAudit.capturedAt,
  referenceProvider: accountingAudit.reference.provider,
  groups: accountingLevels.map((level) => ({
    id: `accounting-${level}`,
    label: accountingAudit.levels[level].label,
    level,
    topicIds: accountingAudit.levels[level].topics.map((topic) => topic.id),
  })),
  topics: accountingTopics,
};

/**
 * The official specification remains the canonical mastery model. These links
 * only explain which syllabus ideas can surface inside each student-facing
 * exam-practice bucket. Several of the reference buckets intentionally overlap.
 */
const APPLIED_MATHEMATICS_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'applied-mathematics-higher-circular-motion': ['applied-mathematics-2-7'],
  'applied-mathematics-higher-difference-equations': ['applied-mathematics-3-0', 'applied-mathematics-3-1', 'applied-mathematics-3-2'],
  'applied-mathematics-higher-differential-equations': ['applied-mathematics-3-3', 'applied-mathematics-3-4'],
  'applied-mathematics-higher-further-integration-u-substitution-integration-by-parts': ['applied-mathematics-2-1', 'applied-mathematics-3-4'],
  'applied-mathematics-higher-hookes-law': ['applied-mathematics-2-13'],
  'applied-mathematics-higher-impacts-collisions': ['applied-mathematics-2-4'],
  'applied-mathematics-higher-integration': ['applied-mathematics-2-1', 'applied-mathematics-3-4'],
  'applied-mathematics-higher-mathematical-modelling-project': ['applied-mathematics-0-0', 'applied-mathematics-0-1', 'applied-mathematics-0-2', 'applied-mathematics-0-3', 'applied-mathematics-0-4'],
  'applied-mathematics-higher-networks-and-graphs': ['applied-mathematics-1-0', 'applied-mathematics-1-1', 'applied-mathematics-1-2', 'applied-mathematics-1-3', 'applied-mathematics-1-4'],
  'applied-mathematics-higher-newtons-laws-connected-particles': ['applied-mathematics-2-3', 'applied-mathematics-2-5', 'applied-mathematics-2-10', 'applied-mathematics-2-11'],
  'applied-mathematics-higher-optimal-critical-paths': ['applied-mathematics-1-3', 'applied-mathematics-1-4', 'applied-mathematics-1-5'],
  'applied-mathematics-higher-projectiles': ['applied-mathematics-2-2'],
  'applied-mathematics-higher-uniform-accelerated-motion': ['applied-mathematics-2-0', 'applied-mathematics-2-1'],
  'applied-mathematics-higher-vectors': ['applied-mathematics-2-2', 'applied-mathematics-2-9'],
  'applied-mathematics-higher-work-power-energy-momentum': ['applied-mathematics-2-4', 'applied-mathematics-2-6', 'applied-mathematics-2-12'],

  'applied-mathematics-ordinary-centre-of-gravity': ['applied-mathematics-2-10'],
  'applied-mathematics-ordinary-circular-motion': ['applied-mathematics-2-7'],
  'applied-mathematics-ordinary-difference-equations': ['applied-mathematics-3-0', 'applied-mathematics-3-1', 'applied-mathematics-3-2'],
  'applied-mathematics-ordinary-differential-equations': ['applied-mathematics-3-3', 'applied-mathematics-3-4'],
  'applied-mathematics-ordinary-dimensional-analysis': ['applied-mathematics-2-8'],
  'applied-mathematics-ordinary-hydrostatics': ['applied-mathematics-2-11'],
  'applied-mathematics-ordinary-impacts-collisions': ['applied-mathematics-2-4'],
  'applied-mathematics-ordinary-linear-motion': ['applied-mathematics-2-0', 'applied-mathematics-2-1'],
  'applied-mathematics-ordinary-mathematical-modelling-project': ['applied-mathematics-0-0', 'applied-mathematics-0-1', 'applied-mathematics-0-2', 'applied-mathematics-0-3', 'applied-mathematics-0-4'],
  'applied-mathematics-ordinary-networks-graphs': ['applied-mathematics-1-0', 'applied-mathematics-1-1', 'applied-mathematics-1-2', 'applied-mathematics-1-3', 'applied-mathematics-1-4'],
  'applied-mathematics-ordinary-newtons-laws-connected-particles': ['applied-mathematics-2-3', 'applied-mathematics-2-5'],
  'applied-mathematics-ordinary-optimal-critical-paths': ['applied-mathematics-1-3', 'applied-mathematics-1-4', 'applied-mathematics-1-5'],
  'applied-mathematics-ordinary-projectiles': ['applied-mathematics-2-2'],
  'applied-mathematics-ordinary-relative-velocity': ['applied-mathematics-2-9'],
  'applied-mathematics-ordinary-statics': ['applied-mathematics-2-10'],
  'applied-mathematics-ordinary-uniform-accelerated-motion': ['applied-mathematics-2-0', 'applied-mathematics-2-1'],
  'applied-mathematics-ordinary-vectors': ['applied-mathematics-2-2', 'applied-mathematics-2-9'],
  'applied-mathematics-ordinary-work-energy-power-momentum': ['applied-mathematics-2-4', 'applied-mathematics-2-6', 'applied-mathematics-2-12'],
};

const parseAppliedMathematicsHeading = (heading: string): {
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision?: string;
} => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const question = heading.match(/Question\s+(\d+)/i);
  if (!year || !question) throw new Error(`Unparseable Applied Mathematics reference heading: ${heading}`);
  const sitting: ExamSitting = /Sample Paper/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main';
  const afterQuestion = heading.slice((question.index ?? 0) + question[0].length)
    .replace(/^\s*-\s*/, '')
    .trim();
  const beforeQuestion = heading.slice(4, question.index)
    .replace(/(?:Sample Paper|Deferred Exam Paper|Paper)/gi, '')
    .replace(/^\s*-\s*|\s*-\s*$/g, '')
    .trim();
  const subdivision = [beforeQuestion, afterQuestion].filter(Boolean).join(' · ') || undefined;
  return { year, sitting, paperKey: 'single', n: question[1], subdivision };
};

const appliedMathematicsLevels = ['higher', 'ordinary'] as const;
const appliedMathematicsPartReferences: ExamQuestionPartReference[] = [];
const appliedMathematicsTopics: ExamTopicDefinition[] = appliedMathematicsLevels.flatMap((level) =>
  appliedMathematicsAudit.levels[level].topics.map((topic) => {
    const officialQuestionKeys = new Set<string>();
    for (const heading of topic.officialQuestionHeadings) {
      const parsed = parseAppliedMathematicsHeading(heading);
      officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
      appliedMathematicsPartReferences.push({
        subjectId: appliedMathematicsAudit.subjectId,
        level,
        ...parsed,
        topicId: topic.id,
      });
    }
    return {
      id: topic.id,
      label: topic.label,
      level,
      sourcePath: topic.sourcePath,
      officialQuestionKeys: [...officialQuestionKeys],
      mockQuestionCount: topic.mockQuestionCount,
      curriculumNodeIds: APPLIED_MATHEMATICS_CURRICULUM_CROSSWALK[topic.id] ?? [],
    };
  }),
);

const APPLIED_MATHEMATICS_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: appliedMathematicsAudit.subjectId,
  capturedAt: appliedMathematicsAudit.capturedAt,
  referenceProvider: appliedMathematicsAudit.reference.provider,
  groups: appliedMathematicsLevels.map((level) => ({
    id: `applied-mathematics-${level}`,
    label: appliedMathematicsAudit.levels[level].label,
    level,
    topicIds: appliedMathematicsAudit.levels[level].topics.map((topic) => topic.id),
  })),
  topics: appliedMathematicsTopics,
};

const AGRICULTURAL_SCIENCE_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'agricultural-science-higher-animal-diseases': ['agricultural-science-3-5'],
  'agricultural-science-higher-animal-physiology-digestive-system': ['agricultural-science-3-0'],
  'agricultural-science-higher-animal-physiology-reproductive-systems': ['agricultural-science-3-0', 'agricultural-science-3-6'],
  'agricultural-science-higher-beef-cattle': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-higher-classification-of-animals-plants': ['agricultural-science-2-1', 'agricultural-science-3-1'],
  'agricultural-science-higher-coursework-project-2025': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-higher-coursework-project-2026': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-higher-crop-production': ['agricultural-science-2-2', 'agricultural-science-2-3', 'agricultural-science-2-4', 'agricultural-science-2-5'],
  'agricultural-science-higher-dairy-cattle': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-higher-energy-crop-catch-crop': ['agricultural-science-2-2', 'agricultural-science-2-3', 'agricultural-science-2-4', 'agricultural-science-2-5'],
  'agricultural-science-higher-fertilisers-pollution-environment-cycles': ['agricultural-science-1-6'],
  'agricultural-science-higher-genetics': ['agricultural-science-3-6'],
  'agricultural-science-higher-grassland': ['agricultural-science-2-6'],
  'agricultural-science-higher-innovation-and-biotechnology-in-agriculture': ['agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-3-6'],
  'agricultural-science-higher-pigs': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-higher-plant-physiology': ['agricultural-science-2-0'],
  'agricultural-science-higher-scientific-practices-experiments-investigations': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-higher-sheep': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-higher-soil-science': ['agricultural-science-1-0', 'agricultural-science-1-1', 'agricultural-science-1-2', 'agricultural-science-1-3', 'agricultural-science-1-4', 'agricultural-science-1-5', 'agricultural-science-1-6'],

  'agricultural-science-ordinary-animal-diseases': ['agricultural-science-3-5'],
  'agricultural-science-ordinary-animal-physiology': ['agricultural-science-3-0', 'agricultural-science-3-6'],
  'agricultural-science-ordinary-animal-production': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-ordinary-classification-of-organisms': ['agricultural-science-2-1', 'agricultural-science-3-1'],
  'agricultural-science-ordinary-coursework-project-2021': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-ordinary-coursework-project-2022': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-ordinary-coursework-project-2023': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-ordinary-crop-production': ['agricultural-science-2-2', 'agricultural-science-2-3', 'agricultural-science-2-4', 'agricultural-science-2-5'],
  'agricultural-science-ordinary-fertilisers-pollution-the-environment': ['agricultural-science-1-6'],
  'agricultural-science-ordinary-genetics': ['agricultural-science-3-6'],
  'agricultural-science-ordinary-grassland': ['agricultural-science-2-6'],
  'agricultural-science-ordinary-health-safety': ['agricultural-science-0-4'],
  'agricultural-science-ordinary-innovation-and-biotechnology-in-agriculture': ['agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-3-6'],
  'agricultural-science-ordinary-plant-physiology': ['agricultural-science-2-0'],
  'agricultural-science-ordinary-scientific-practices-experiments-investigations': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-ordinary-soil-science': ['agricultural-science-1-0', 'agricultural-science-1-1', 'agricultural-science-1-2', 'agricultural-science-1-3', 'agricultural-science-1-4', 'agricultural-science-1-5', 'agricultural-science-1-6'],
};

const parseAgriculturalScienceHeading = (heading: string, level: PaperLevel): {
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision?: string;
} => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const question = heading.match(/Question\s+([A-Z]|\d+)/i);
  if (!year || !question) throw new Error(`Unparseable Agricultural Science reference heading: ${heading}`);
  const sitting: ExamSitting = /Sample Paper/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main';
  const printedQuestion = question[1];
  // Former-course Higher Section 1 printed its short items A–J inside the
  // single locally anchored Q1 region. Retain the letter as subdivision data.
  const isShortItem = level === 'higher' && /^[A-Z]$/i.test(printedQuestion);
  const n = isShortItem ? '1' : printedQuestion;
  const beforeQuestion = heading.slice(4, question.index)
    .replace(/(?:Sample Paper|Deferred Exam Paper|Paper)/gi, '')
    .replace(/^\s*-\s*|\s*-\s*$/g, '')
    .trim();
  const afterQuestion = heading.slice((question.index ?? 0) + question[0].length)
    .replace(/^\s*-\s*/, '')
    .trim();
  const subdivision = [
    beforeQuestion,
    isShortItem ? `Short question ${printedQuestion.toUpperCase()}` : '',
    afterQuestion,
  ].filter(Boolean).join(' · ') || undefined;
  return { year, sitting, paperKey: 'single', n, subdivision };
};

const agriculturalScienceLevels = ['higher', 'ordinary'] as const;
const agriculturalSciencePartReferences: ExamQuestionPartReference[] = [];
const agriculturalScienceTopics: ExamTopicDefinition[] = agriculturalScienceLevels.flatMap((level) =>
  agriculturalScienceAudit.levels[level].topics.map((topic) => {
    const officialQuestionKeys = new Set<string>();
    for (const heading of topic.officialQuestionHeadings) {
      const parsed = parseAgriculturalScienceHeading(heading, level);
      officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
      agriculturalSciencePartReferences.push({
        subjectId: agriculturalScienceAudit.subjectId,
        level,
        ...parsed,
        topicId: topic.id,
      });
    }
    return {
      id: topic.id,
      label: topic.label,
      level,
      sourcePath: topic.sourcePath,
      officialQuestionKeys: [...officialQuestionKeys],
      mockQuestionCount: topic.mockQuestionCount,
      curriculumNodeIds: AGRICULTURAL_SCIENCE_CURRICULUM_CROSSWALK[topic.id] ?? [],
    };
  }),
);

const AGRICULTURAL_SCIENCE_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: agriculturalScienceAudit.subjectId,
  capturedAt: agriculturalScienceAudit.capturedAt,
  referenceProvider: agriculturalScienceAudit.reference.provider,
  groups: agriculturalScienceLevels.map((level) => ({
    id: `agricultural-science-${level}`,
    label: agriculturalScienceAudit.levels[level].label,
    level,
    topicIds: agriculturalScienceAudit.levels[level].topics.map((topic) => topic.id),
  })),
  topics: agriculturalScienceTopics,
};

const LINK_MODULES_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'link-modules-common-1-career-investigation': ['lcvp-link-modules-0-2'],
  'link-modules-common-1-introduction-to-working-life': ['lcvp-link-modules-0-0'],
  'link-modules-common-1-job-seeking-skills': ['lcvp-link-modules-0-1', 'lcvp-link-modules-0-4'],
  'link-modules-common-1-work-placement': ['lcvp-link-modules-0-3', 'lcvp-link-modules-1-4'],
  'link-modules-common-2-an-enterprise-activity': ['lcvp-link-modules-1-3'],
  'link-modules-common-2-enterprise-skills': ['lcvp-link-modules-1-0'],
  'link-modules-common-2-local-business-enterprises': ['lcvp-link-modules-1-1'],
  'link-modules-common-2-local-voluntarycommunity-enterprises': ['lcvp-link-modules-1-2'],
  // These are assessment-format buckets whose source material can draw on any
  // unit; they are deliberately excluded from the inverse content fallback.
  'link-modules-common-audio-visual': [
    'lcvp-link-modules-0-0', 'lcvp-link-modules-0-1', 'lcvp-link-modules-0-2',
    'lcvp-link-modules-0-3', 'lcvp-link-modules-0-4', 'lcvp-link-modules-1-0',
    'lcvp-link-modules-1-1', 'lcvp-link-modules-1-2', 'lcvp-link-modules-1-3',
    'lcvp-link-modules-1-4',
  ],
  'link-modules-common-case-study': [
    'lcvp-link-modules-0-0', 'lcvp-link-modules-0-1', 'lcvp-link-modules-0-2',
    'lcvp-link-modules-0-3', 'lcvp-link-modules-0-4', 'lcvp-link-modules-1-0',
    'lcvp-link-modules-1-1', 'lcvp-link-modules-1-2', 'lcvp-link-modules-1-3',
    'lcvp-link-modules-1-4',
  ],
};

const parseLinkModulesHeading = (heading: string): Array<{
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision: string;
}> => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const section = heading.match(/Section\s+([ABC])/i)?.[1]?.toUpperCase();
  if (!year || !section) throw new Error(`Unparseable Link Modules reference heading: ${heading}`);
  const sitting: ExamSitting = /Deferred Exam Paper/i.test(heading) ? 'deferred' : 'main';
  const listed = heading.match(/Questions?\s+((?:\d+\s*,\s*)+\d+)/i);
  const range = heading.match(/Questions?\s+(\d+)(?:-(\d+))?/i);
  let printedNumbers: number[];
  if (listed) {
    printedNumbers = listed[1].split(',').map(value => Number(value.trim()));
  } else if (range) {
    const lo = Number(range[1]);
    const hi = Number(range[2] ?? range[1]);
    printedNumbers = Array.from({ length: hi - lo + 1 }, (_, index) => lo + index);
  } else if (section === 'A') {
    // The 2022 reference heading names the whole section rather than spelling
    // out its printed 1–8 range.
    printedNumbers = [1, 2, 3, 4, 5, 6, 7, 8];
  } else if (section === 'B') {
    printedNumbers = [1, 2, 3];
  } else {
    throw new Error(`Link Modules Section C heading has no question number: ${heading}`);
  }
  const offset = section === 'A' ? 0 : section === 'B' ? 8 : 11;
  const subdivision = heading.replace(/^\d{4}\s*-\s*/, '').trim();
  return printedNumbers.map(number => ({
    year,
    sitting,
    paperKey: 'single',
    n: String(offset + number),
    subdivision,
  }));
};

const linkModulesPartReferences: ExamQuestionPartReference[] = [];
const linkModulesTopics: ExamTopicDefinition[] = linkModulesAudit.levels.common.topics.map((topic) => {
  const officialQuestionKeys = new Set<string>();
  for (const heading of topic.officialQuestionHeadings) {
    for (const parsed of parseLinkModulesHeading(heading)) {
      officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
      linkModulesPartReferences.push({
        subjectId: linkModulesAudit.subjectId,
        level: 'common',
        ...parsed,
        topicId: topic.id,
      });
    }
  }
  return {
    id: topic.id,
    label: topic.label,
    level: 'common',
    sourcePath: topic.sourcePath,
    officialQuestionKeys: [...officialQuestionKeys],
    mockQuestionCount: topic.mockQuestionCount,
    curriculumNodeIds: LINK_MODULES_CURRICULUM_CROSSWALK[topic.id] ?? [],
  };
});

const LINK_MODULES_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: linkModulesAudit.subjectId,
  capturedAt: linkModulesAudit.capturedAt,
  referenceProvider: linkModulesAudit.reference.provider,
  groups: [{
    id: 'link-modules-common',
    label: linkModulesAudit.levels.common.label,
    level: 'common',
    topicIds: linkModulesAudit.levels.common.topics.map(topic => topic.id),
  }],
  topics: linkModulesTopics,
};

/**
 * History exposes the twelve official Later Modern topics separately at each
 * level. The generated bridge preserves the four DQB subquestion cards, adds
 * every independently selectable Ireland/Europe topic block, and retains the
 * Ordinary-level Alternative Part A cards printed from 2023 to 2026.
 */
const historyPartReferences: ExamQuestionPartReference[] = [];
const historyOfficialKeys = new Map<string, Set<string>>();
for (const [topicIndex, year, sittingCode, n, heading] of historyRuntime.partReferences) {
  const runtimeTopic = historyRuntime.topics[topicIndex];
  if (!runtimeTopic) throw new Error(`Unknown History runtime topic index: ${topicIndex}`);
  const [topicId, , , , , levelCode] = runtimeTopic;
  const sitting = sittingCode === 'd' ? 'deferred' : 'main';
  const keys = historyOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|${sitting}|single|${n}`);
  historyOfficialKeys.set(topicId, keys);
  historyPartReferences.push({
    subjectId: historyRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId,
  });
}

const historyTopics: ExamTopicDefinition[] = historyRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  curriculumNodeIds,
  levelCode,
]) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  officialQuestionKeys: [...(historyOfficialKeys.get(id) ?? [])],
  mockQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const HISTORY_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: historyRuntime.subjectId,
  capturedAt: historyRuntime.capturedAt,
  referenceProvider: historyRuntime.referenceProvider,
  groups: historyRuntime.groups.map(([levelCode, label, topicIndexes]) => ({
    id: `history-${levelCode === 'h' ? 'higher' : 'ordinary'}`,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = historyRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown History group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: historyTopics,
};

/**
 * Economics keeps the flat, level-specific exam-practice menu while the
 * official five-strand curriculum remains canonical underneath it. The
 * generated join also preserves all 32 entitled local questions omitted from
 * the factual reference snapshot.
 */
const economicsPartReferences: ExamQuestionPartReference[] = [];
const economicsOfficialKeys = new Map<string, Set<string>>();
for (const [topicIndex, year, sittingCode, n, heading] of economicsRuntime.partReferences) {
  const runtimeTopic = economicsRuntime.topics[topicIndex];
  if (!runtimeTopic) throw new Error(`Unknown Economics runtime topic index: ${topicIndex}`);
  const [topicId, , , , , levelCode] = runtimeTopic;
  const sitting: ExamSitting = sittingCode === 'd'
    ? 'deferred'
    : sittingCode === 's'
      ? 'sample'
      : 'main';
  const keys = economicsOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|${sitting}|single|${n}`);
  economicsOfficialKeys.set(topicId, keys);
  economicsPartReferences.push({
    subjectId: economicsRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId,
  });
}

const economicsTopics: ExamTopicDefinition[] = economicsRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  curriculumNodeIds,
  levelCode,
]) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  officialQuestionKeys: [...(economicsOfficialKeys.get(id) ?? [])],
  mockQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const ECONOMICS_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: economicsRuntime.subjectId,
  capturedAt: economicsRuntime.capturedAt,
  referenceProvider: economicsRuntime.referenceProvider,
  groups: economicsRuntime.groups.map(([levelCode, label, topicIndexes]) => ({
    id: `economics-${levelCode === 'h' ? 'higher' : 'ordinary'}`,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = economicsRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Economics group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: economicsTopics,
};

/**
 * Art keeps the exact level-specific Visual Studies section hierarchy while
 * retaining every independently selectable legacy practical card. Component
 * code is part of the local identity because those booklets restart at Q1.
 */
const artFileid = (
  levelCode: 'h' | 'o',
  langCode: 'e' | 'i',
  componentCode: string,
): string => `LC014${levelCode === 'h' ? 'A' : 'G'}LP${componentCode}${
  langCode === 'e' ? 'EV' : 'IV'
}.pdf`;

const artPartReferences: ExamQuestionPartReference[] = [];
const artOfficialKeys = new Map<string, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  sittingCode,
  componentCode,
  n,
  heading,
] of artRuntime.partReferences) {
  const runtimeTopic = artRuntime.topics[topicIndex];
  if (!runtimeTopic) throw new Error(`Unknown Art runtime topic index: ${topicIndex}`);
  const [topicId, , , , , , levelCode] = runtimeTopic;
  const sitting: ExamSitting = sittingCode === 'd'
    ? 'deferred'
    : sittingCode === 's'
      ? 'sample'
      : 'main';
  const year = yearOffset + 2000;
  const keys = artOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|${sitting}|single|${n}`);
  artOfficialKeys.set(topicId, keys);
  artPartReferences.push({
    subjectId: artRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    fileid: componentCode ? artFileid(levelCode, 'e', componentCode) : undefined,
    n,
    subdivision: heading,
    topicId,
  });
}

const artTopics: ExamTopicDefinition[] = artRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  levelCode,
  reportedQuestionCount,
]) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  officialQuestionKeys: [...(artOfficialKeys.get(id) ?? [])],
  mockQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
  reportedQuestionCount,
  providerSampleQuestionCount,
}));

const ART_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: artRuntime.subjectId,
  capturedAt: artRuntime.capturedAt,
  referenceProvider: artRuntime.referenceProvider,
  groups: artRuntime.groups.map(([levelCode, id, label, topicIndexes]) => ({
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = artRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Art group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: artTopics,
};

/**
 * Computer Science uses the reference provider's flat, level-specific browse
 * menu over the official three-strand curriculum. Part-level factual headings
 * remain attached even when several headings resolve to one SEC question.
 */
const computerSciencePartReferences: ExamQuestionPartReference[] = [];
const computerScienceOfficialKeys = new Map<string, Set<string>>();
for (const [topicIndex, year, sittingCode, n, heading] of computerScienceRuntime.partReferences) {
  const runtimeTopic = computerScienceRuntime.topics[topicIndex];
  if (!runtimeTopic) throw new Error(`Unknown Computer Science runtime topic index: ${topicIndex}`);
  const [topicId, , , , , levelCode] = runtimeTopic;
  const sitting: ExamSitting = sittingCode === 's' ? 'sample' : 'main';
  const keys = computerScienceOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|${sitting}|${n}`);
  computerScienceOfficialKeys.set(topicId, keys);
  computerSciencePartReferences.push({
    subjectId: computerScienceRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId,
  });
}

const computerScienceTopics: ExamTopicDefinition[] = computerScienceRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  curriculumNodeIds,
  levelCode,
]) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  officialQuestionKeys: [...(computerScienceOfficialKeys.get(id) ?? [])],
  mockQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const COMPUTER_SCIENCE_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: computerScienceRuntime.subjectId,
  capturedAt: computerScienceRuntime.capturedAt,
  referenceProvider: computerScienceRuntime.referenceProvider,
  groups: computerScienceRuntime.groups.map(([levelCode, label, topicIndexes]) => ({
    id: `computer-science-${levelCode === 'h' ? 'higher' : 'ordinary'}`,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = computerScienceRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Computer Science group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: computerScienceTopics,
};

/**
 * Biology is the first audited subject with two overlapping course structures.
 * The exact Higher/Ordinary × New/Old hierarchy remains visible for practice,
 * while every bucket bridges to the appropriate canonical specification.
 * Provider-owned sample exams contribute counts only and never question data.
 */
interface BiologyTopicIdentity {
  id: string;
  sourcePath: string;
  levelCode: 'h' | 'o';
  courseCode: 'n' | 'o';
}

const biologyTopicIdentities: Array<BiologyTopicIdentity | undefined> =
  Array.from({ length: biologyRuntime.topics.length });
for (const [levelCode, courseCode, groupId, , topicIndexes] of biologyRuntime.groups) {
  const variant = `${levelCode === 'h' ? 'higher' : 'ordinary'}-${
    courseCode === 'n' ? 'new-course' : 'old-course'
  }`;
  const groupPrefix = `biology-${variant}`;
  const groupSlug = groupId === groupPrefix
    ? ''
    : groupId.slice(`${groupPrefix}-`.length);
  for (const topicIndex of topicIndexes) {
    const slug = biologyRuntime.topics[topicIndex]?.[0];
    if (!slug || biologyTopicIdentities[topicIndex]) {
      throw new Error(`Invalid Biology group topic index: ${topicIndex}`);
    }
    biologyTopicIdentities[topicIndex] = {
      id: `${groupPrefix}-${slug}`,
      sourcePath: [
        '',
        'leaving-certificate',
        'biology',
        variant,
        groupSlug,
        slug,
      ].filter((segment, index) => index === 0 || segment).join('/'),
      levelCode,
      courseCode,
    };
  }
}

const biologyTopicIdentity = (topicIndex: number): BiologyTopicIdentity => {
  const identity = biologyTopicIdentities[topicIndex];
  if (!identity) throw new Error(`Unknown Biology runtime topic index: ${topicIndex}`);
  return identity;
};

const biologyPartReferences: ExamQuestionPartReference[] = [];
const biologyOfficialKeys = new Map<string, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  prefixIndex,
  n,
  tailIndex,
] of biologyRuntime.partReferences) {
  const runtimeTopic = biologyRuntime.topics[topicIndex];
  const identity = biologyTopicIdentity(topicIndex);
  const prefix = biologyRuntime.headingPrefixes[prefixIndex];
  const tail = biologyRuntime.headingTails[tailIndex];
  if (!runtimeTopic || prefix === undefined || tail === undefined) {
    throw new Error(`Unknown Biology compact part reference: ${[
      topicIndex,
      yearOffset,
      prefixIndex,
      n,
      tailIndex,
    ].join('|')}`);
  }
  const { id: topicId, levelCode } = identity;
  const year = yearOffset + 2000;
  const sitting: ExamSitting = /Deferred Exam Paper/i.test(prefix)
    ? 'deferred'
    : /Sample Paper/i.test(prefix)
      ? 'sample'
      : 'main';
  const heading = `${year} - ${prefix}${n}${tail}`;
  const keys = biologyOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|${sitting}|single|${n}`);
  biologyOfficialKeys.set(topicId, keys);
  biologyPartReferences.push({
    subjectId: biologyRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId,
  });
}

const biologyTopics: ExamTopicDefinition[] = biologyRuntime.topics.map(([
  ,
  label,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  reportedQuestionCount,
], topicIndex) => {
  const { id, sourcePath, levelCode, courseCode } = biologyTopicIdentity(topicIndex);
  return {
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    sourcePath,
    officialQuestionKeys: [...(biologyOfficialKeys.get(id) ?? [])],
    mockQuestionCount,
    curriculumNodeIds: [...curriculumNodeIds],
    course: courseCode === 'n' ? 'new' : 'old',
    reportedQuestionCount,
    providerSampleQuestionCount,
  };
});

const BIOLOGY_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: biologyRuntime.subjectId,
  capturedAt: biologyRuntime.capturedAt,
  referenceProvider: biologyRuntime.referenceProvider,
  groups: biologyRuntime.groups.map(([
    levelCode,
    courseCode,
    id,
    label,
    topicIndexes,
  ]) => ({
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    course: courseCode === 'n' ? 'new' : 'old',
    topicIds: topicIndexes.map(topicIndex => biologyTopicIdentity(topicIndex).id),
  })),
  topics: biologyTopics,
};

/**
 * Business exposes two overlapping specifications and a paper structure that
 * changed in 2020. Stable paper keys and additive ABQ/section identifiers keep
 * every pre-existing card intact while retaining the exact audited hierarchy.
 */
interface BusinessTopicIdentity {
  id: string;
  sourcePath: string;
  levelCode: 'h' | 'o';
  courseCode: 'n' | 'o';
}

const businessTopicIdentities: Array<BusinessTopicIdentity | undefined> =
  Array.from({ length: businessRuntime.topics.length });
for (const [levelCode, courseCode, groupId, , topicIndexes] of businessRuntime.groups) {
  const variant = `${levelCode === 'h' ? 'higher' : 'ordinary'}-${
    courseCode === 'n' ? 'new-course' : 'old-course'
  }`;
  const groupPrefix = `business-${variant}`;
  const groupSlug = groupId === groupPrefix
    ? ''
    : groupId.slice(`${groupPrefix}-`.length);
  for (const topicIndex of topicIndexes) {
    const slug = businessRuntime.topics[topicIndex]?.[0];
    if (!slug || businessTopicIdentities[topicIndex]) {
      throw new Error(`Invalid Business group topic index: ${topicIndex}`);
    }
    businessTopicIdentities[topicIndex] = {
      id: `${groupPrefix}-${slug}`,
      sourcePath: [
        '',
        'leaving-certificate',
        'business',
        variant,
        groupSlug,
        slug,
      ].filter((segment, index) => index === 0 || segment).join('/'),
      levelCode,
      courseCode,
    };
  }
}

const businessTopicIdentity = (topicIndex: number): BusinessTopicIdentity => {
  const identity = businessTopicIdentities[topicIndex];
  if (!identity) throw new Error(`Unknown Business runtime topic index: ${topicIndex}`);
  return identity;
};

const businessPaperKey = (code: 's' | '1' | '2'): 'single' | 'p1' | 'p2' => (
  code === 's' ? 'single' : code === '1' ? 'p1' : 'p2'
);

const businessPartReferences: ExamQuestionPartReference[] = [];
const businessOfficialKeys = new Map<string, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  prefixIndex,
  questionToken,
  tailIndex,
  paperKeyCode,
  n,
] of businessRuntime.partReferences) {
  const runtimeTopic = businessRuntime.topics[topicIndex];
  const identity = businessTopicIdentity(topicIndex);
  const prefix = businessRuntime.headingPrefixes[prefixIndex];
  const tail = businessRuntime.headingTails[tailIndex];
  if (!runtimeTopic || prefix === undefined || tail === undefined) {
    throw new Error(`Unknown Business compact part reference: ${[
      topicIndex,
      yearOffset,
      prefixIndex,
      questionToken,
      tailIndex,
      paperKeyCode,
      n,
    ].join('|')}`);
  }
  const { id: topicId, levelCode } = identity;
  const year = yearOffset + 2000;
  const sitting: ExamSitting = /Deferred Exam Paper/i.test(prefix)
    ? 'deferred'
    : /Sample Paper/i.test(prefix)
      ? 'sample'
      : 'main';
  const paperKey = businessPaperKey(paperKeyCode);
  const heading = `${year} - ${prefix}${questionToken}${tail}`;
  const keys = businessOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|${sitting}|${paperKey}|${n}`);
  businessOfficialKeys.set(topicId, keys);
  businessPartReferences.push({
    subjectId: businessRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey,
    n,
    subdivision: heading,
    topicId,
  });
}

const businessTopics: ExamTopicDefinition[] = businessRuntime.topics.map(([
  ,
  label,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  reportedQuestionCount,
], topicIndex) => {
  const { id, sourcePath, levelCode, courseCode } = businessTopicIdentity(topicIndex);
  return {
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    sourcePath,
    officialQuestionKeys: [...(businessOfficialKeys.get(id) ?? [])],
    mockQuestionCount,
    curriculumNodeIds: [...curriculumNodeIds],
    course: courseCode === 'n' ? 'new' : 'old',
    reportedQuestionCount,
    providerSampleQuestionCount,
  };
});

const BUSINESS_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: businessRuntime.subjectId,
  capturedAt: businessRuntime.capturedAt,
  referenceProvider: businessRuntime.referenceProvider,
  groups: businessRuntime.groups.map(([
    levelCode,
    courseCode,
    id,
    label,
    topicIndexes,
  ]) => ({
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    course: courseCode === 'n' ? 'new' : 'old',
    topicIds: topicIndexes.map(topicIndex => businessTopicIdentity(topicIndex).id),
  })),
  topics: businessTopics,
};

/**
 * Construction Studies keeps the outgoing course and the incoming
 * Construction Technology hierarchy side by side. The official curriculum
 * records remain canonical; these level-aware buckets are the audited exam
 * practice navigation layer.
 */
interface ConstructionStudiesTopicIdentity {
  id: string;
  sourcePath: string;
  levelCode: 'h' | 'o';
  courseCode: 'n' | 'o';
}

const constructionStudiesTopicIdentities: Array<
  ConstructionStudiesTopicIdentity | undefined
> = Array.from({ length: constructionStudiesRuntime.topics.length });
for (const [
  levelCode,
  courseCode,
  groupId,
  ,
  topicIndexes,
] of constructionStudiesRuntime.groups) {
  const variant = `${levelCode === 'h' ? 'higher' : 'ordinary'}${
    courseCode === 'n' ? '-new-course' : ''
  }`;
  const groupPrefix = `construction-studies-${variant}`;
  const groupSlug = groupId === groupPrefix
    ? ''
    : groupId.slice(`${groupPrefix}-`.length);
  for (const topicIndex of topicIndexes) {
    const slug = constructionStudiesRuntime.topics[topicIndex]?.[0];
    if (!slug || constructionStudiesTopicIdentities[topicIndex]) {
      throw new Error(`Invalid Construction Studies group topic index: ${topicIndex}`);
    }
    constructionStudiesTopicIdentities[topicIndex] = {
      id: `${groupPrefix}-${slug}`,
      sourcePath: [
        '',
        'leaving-certificate',
        'construction-studies',
        variant,
        groupSlug,
        slug,
      ].filter((segment, index) => index === 0 || segment).join('/'),
      levelCode,
      courseCode,
    };
  }
}

const constructionStudiesTopicIdentity = (
  topicIndex: number,
): ConstructionStudiesTopicIdentity => {
  const identity = constructionStudiesTopicIdentities[topicIndex];
  if (!identity) {
    throw new Error(`Unknown Construction Studies runtime topic index: ${topicIndex}`);
  }
  return identity;
};

const constructionStudiesPartReferences: ExamQuestionPartReference[] = [];
const constructionStudiesOfficialKeys = new Map<string, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  prefixIndex,
  questionToken,
  tailIndex,
  n,
] of constructionStudiesRuntime.partReferences) {
  const runtimeTopic = constructionStudiesRuntime.topics[topicIndex];
  const identity = constructionStudiesTopicIdentity(topicIndex);
  const prefix = constructionStudiesRuntime.headingPrefixes[prefixIndex];
  const tail = constructionStudiesRuntime.headingTails[tailIndex];
  if (!runtimeTopic || prefix === undefined || tail === undefined) {
    throw new Error(`Unknown Construction Studies compact part reference: ${[
      topicIndex,
      yearOffset,
      prefixIndex,
      questionToken,
      tailIndex,
      n,
    ].join('|')}`);
  }
  const year = yearOffset + 2000;
  const heading = `${year}${prefix}${questionToken}${tail}`;
  const sitting: ExamSitting = /Deferred Exam Paper/i.test(heading)
    ? 'deferred'
    : /Sample Paper/i.test(heading)
      ? 'sample'
      : 'main';
  const keys = constructionStudiesOfficialKeys.get(identity.id) ?? new Set<string>();
  keys.add(`${year}|${sitting}|single|${n}`);
  constructionStudiesOfficialKeys.set(identity.id, keys);
  constructionStudiesPartReferences.push({
    subjectId: constructionStudiesRuntime.subjectId,
    level: identity.levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId: identity.id,
  });
}

const constructionStudiesTopics: ExamTopicDefinition[] = (
  constructionStudiesRuntime.topics.map(([
    ,
    label,
    mockQuestionCount,
    providerSampleQuestionCount,
    curriculumNodeIds,
    reportedQuestionCount,
  ], topicIndex) => {
    const {
      id,
      sourcePath,
      levelCode,
      courseCode,
    } = constructionStudiesTopicIdentity(topicIndex);
    return {
      id,
      label,
      level: levelCode === 'h' ? 'higher' : 'ordinary',
      sourcePath,
      officialQuestionKeys: [...(constructionStudiesOfficialKeys.get(id) ?? [])],
      mockQuestionCount,
      curriculumNodeIds: [...curriculumNodeIds],
      course: courseCode === 'n' ? 'new' : 'old',
      reportedQuestionCount,
      providerSampleQuestionCount,
    };
  })
);

const CONSTRUCTION_STUDIES_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: constructionStudiesRuntime.subjectId,
  capturedAt: constructionStudiesRuntime.capturedAt,
  referenceProvider: constructionStudiesRuntime.referenceProvider,
  groups: constructionStudiesRuntime.groups.map(([
    levelCode,
    courseCode,
    id,
    label,
    topicIndexes,
  ]) => ({
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    course: courseCode === 'n' ? 'new' : 'old',
    topicIds: topicIndexes.map(topicIndex => (
      constructionStudiesTopicIdentity(topicIndex).id
    )),
  })),
  topics: constructionStudiesTopics,
};

/**
 * Engineering keeps its outgoing and replacement specifications side by
 * side. The four replacement strands remain canonical curriculum structure;
 * these level-aware groups are the audited exam-practice navigation layer.
 */
interface EngineeringTopicIdentity {
  id: string;
  sourcePath: string;
  levelCode: 'h' | 'o';
  courseCode: 'n' | 'o';
}

const engineeringTopicIdentities: Array<EngineeringTopicIdentity | undefined> =
  Array.from({ length: engineeringRuntime.topics.length });
for (const [
  levelCode,
  courseCode,
  groupId,
  ,
  topicIndexes,
] of engineeringRuntime.groups) {
  const variant = `${levelCode === 'h' ? 'higher' : 'ordinary'}${
    courseCode === 'n' ? '-new-course' : ''
  }`;
  const groupPrefix = `engineering-${variant}`;
  const groupSlug = groupId === groupPrefix
    ? ''
    : groupId.slice(`${groupPrefix}-`.length);
  for (const topicIndex of topicIndexes) {
    const slug = engineeringRuntime.topics[topicIndex]?.[0];
    if (!slug || engineeringTopicIdentities[topicIndex]) {
      throw new Error(`Invalid Engineering group topic index: ${topicIndex}`);
    }
    engineeringTopicIdentities[topicIndex] = {
      id: `${groupPrefix}-${slug}`,
      sourcePath: [
        '',
        'leaving-certificate',
        'engineering',
        variant,
        groupSlug,
        slug,
      ].filter((segment, index) => index === 0 || segment).join('/'),
      levelCode,
      courseCode,
    };
  }
}

const engineeringTopicIdentity = (topicIndex: number): EngineeringTopicIdentity => {
  const identity = engineeringTopicIdentities[topicIndex];
  if (!identity) throw new Error(`Unknown Engineering runtime topic index: ${topicIndex}`);
  return identity;
};

const engineeringPartReferences: ExamQuestionPartReference[] = [];
const engineeringOfficialKeys = new Map<string, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  prefixIndex,
  questionToken,
  tailIndex,
  n,
] of engineeringRuntime.partReferences) {
  const runtimeTopic = engineeringRuntime.topics[topicIndex];
  const identity = engineeringTopicIdentity(topicIndex);
  const prefix = engineeringRuntime.headingPrefixes[prefixIndex];
  const tail = engineeringRuntime.headingTails[tailIndex];
  if (!runtimeTopic || prefix === undefined || tail === undefined) {
    throw new Error(`Unknown Engineering compact part reference: ${[
      topicIndex,
      yearOffset,
      prefixIndex,
      questionToken,
      tailIndex,
      n,
    ].join('|')}`);
  }
  const year = yearOffset + 2000;
  const heading = `${year}${prefix}${questionToken}${tail}`;
  const sitting: ExamSitting = /Deferred Exam Paper/i.test(heading)
    ? 'deferred'
    : /Sample Paper/i.test(heading)
      ? 'sample'
      : 'main';
  const keys = engineeringOfficialKeys.get(identity.id) ?? new Set<string>();
  keys.add(`${year}|${sitting}|single|${n}`);
  engineeringOfficialKeys.set(identity.id, keys);
  engineeringPartReferences.push({
    subjectId: engineeringRuntime.subjectId,
    level: identity.levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId: identity.id,
  });
}

const engineeringTopics: ExamTopicDefinition[] = engineeringRuntime.topics.map(([
  ,
  label,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  reportedQuestionCount,
], topicIndex) => {
  const { id, sourcePath, levelCode, courseCode } = engineeringTopicIdentity(topicIndex);
  return {
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    sourcePath,
    officialQuestionKeys: [...(engineeringOfficialKeys.get(id) ?? [])],
    mockQuestionCount,
    curriculumNodeIds: [...curriculumNodeIds],
    course: courseCode === 'n' ? 'new' : 'old',
    reportedQuestionCount,
    providerSampleQuestionCount,
  };
});

const ENGINEERING_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: engineeringRuntime.subjectId,
  capturedAt: engineeringRuntime.capturedAt,
  referenceProvider: engineeringRuntime.referenceProvider,
  groups: engineeringRuntime.groups.map(([
    levelCode,
    courseCode,
    id,
    label,
    topicIndexes,
  ]) => ({
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    course: courseCode === 'n' ? 'new' : 'old',
    topicIds: topicIndexes.map(topicIndex => engineeringTopicIdentity(topicIndex).id),
  })),
  topics: engineeringTopics,
};

/**
 * Technology exposes a flat Higher/Ordinary practice menu. The factual
 * reference headings stay separate from the canonical NCCA syllabus nodes,
 * while exact booklet ids distinguish Section A from the separately supplied
 * Section B/C papers.
 */
interface TechnologyTopicIdentity {
  id: string;
  sourcePath: string;
  levelCode: 'h' | 'o';
}

const technologyTopicIdentities: Array<TechnologyTopicIdentity | undefined> =
  Array.from({ length: technologyRuntime.topics.length });
for (const [levelCode, groupId, , topicIndexes] of technologyRuntime.groups) {
  const level = levelCode === 'h' ? 'higher' : 'ordinary';
  for (const topicIndex of topicIndexes) {
    const slug = technologyRuntime.topics[topicIndex]?.[0];
    if (!slug || technologyTopicIdentities[topicIndex]) {
      throw new Error(`Invalid Technology group topic index: ${topicIndex}`);
    }
    technologyTopicIdentities[topicIndex] = {
      id: `${groupId}-${slug}`,
      sourcePath: `/leaving-certificate/technology/${level}/${slug}`,
      levelCode,
    };
  }
}

const technologyTopicIdentity = (topicIndex: number): TechnologyTopicIdentity => {
  const identity = technologyTopicIdentities[topicIndex];
  if (!identity) throw new Error(`Unknown Technology runtime topic index: ${topicIndex}`);
  return identity;
};

const technologyPartReferences: ExamQuestionPartReference[] = [];
const technologyOfficialKeys = new Map<string, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  prefixIndex,
  questionToken,
  tailIndex,
  n,
  fileIndex,
  sittingCode,
] of technologyRuntime.partReferences) {
  const runtimeTopic = technologyRuntime.topics[topicIndex];
  const identity = technologyTopicIdentity(topicIndex);
  const prefix = technologyRuntime.headingPrefixes[prefixIndex];
  const tail = technologyRuntime.headingTails[tailIndex];
  const fileid = fileIndex >= 0 ? technologyRuntime.files[fileIndex] : undefined;
  if (
    !runtimeTopic
    || prefix === undefined
    || tail === undefined
    || (fileIndex >= 0 && !fileid)
  ) {
    throw new Error(`Unknown Technology compact part reference: ${[
      topicIndex,
      yearOffset,
      prefixIndex,
      questionToken,
      tailIndex,
      n,
      fileIndex,
      sittingCode,
    ].join('|')}`);
  }
  const year = yearOffset + 2000;
  const sitting: ExamSitting = sittingCode === 'd' ? 'deferred' : 'main';
  const heading = `${year}${prefix}${questionToken}${tail}`;
  const keys = technologyOfficialKeys.get(identity.id) ?? new Set<string>();
  keys.add(`${year}|${sitting}|single|${n}`);
  technologyOfficialKeys.set(identity.id, keys);
  technologyPartReferences.push({
    subjectId: technologyRuntime.subjectId,
    level: identity.levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    ...(fileid ? { fileid } : {}),
    n,
    subdivision: heading,
    topicId: identity.id,
  });
}

const technologyTopics: ExamTopicDefinition[] = technologyRuntime.topics.map(([
  ,
  label,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  reportedQuestionCount,
], topicIndex) => {
  const { id, sourcePath, levelCode } = technologyTopicIdentity(topicIndex);
  return {
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    sourcePath,
    officialQuestionKeys: [...(technologyOfficialKeys.get(id) ?? [])],
    mockQuestionCount,
    curriculumNodeIds: [...curriculumNodeIds],
    reportedQuestionCount,
    providerSampleQuestionCount,
  };
});

const TECHNOLOGY_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: technologyRuntime.subjectId,
  capturedAt: technologyRuntime.capturedAt,
  referenceProvider: technologyRuntime.referenceProvider,
  groups: technologyRuntime.groups.map(([levelCode, id, label, topicIndexes]) => ({
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => technologyTopicIdentity(topicIndex).id),
  })),
  topics: technologyTopics,
};

/**
 * Chemistry shares Biology's overlapping-course shape: factual practice
 * buckets remain exact to the audited Higher/Ordinary × New/Old hierarchy,
 * while canonical curriculum identities stay specification-specific.
 */
interface ChemistryTopicIdentity {
  id: string;
  sourcePath: string;
  levelCode: 'h' | 'o';
  courseCode: 'n' | 'o';
}

const chemistryTopicIdentities: Array<ChemistryTopicIdentity | undefined> =
  Array.from({ length: chemistryRuntime.topics.length });
for (const [levelCode, courseCode, groupId, , topicIndexes] of chemistryRuntime.groups) {
  const variant = `${levelCode === 'h' ? 'higher' : 'ordinary'}-${
    courseCode === 'n' ? 'new-course' : 'old-course'
  }`;
  const groupPrefix = `chemistry-${variant}`;
  const groupSlug = groupId === groupPrefix
    ? ''
    : groupId.slice(`${groupPrefix}-`.length);
  for (const topicIndex of topicIndexes) {
    const slug = chemistryRuntime.topics[topicIndex]?.[0];
    if (!slug || chemistryTopicIdentities[topicIndex]) {
      throw new Error(`Invalid Chemistry group topic index: ${topicIndex}`);
    }
    chemistryTopicIdentities[topicIndex] = {
      id: `${groupPrefix}-${slug}`,
      sourcePath: [
        '',
        'leaving-certificate',
        'chemistry',
        variant,
        groupSlug,
        slug,
      ].filter((segment, index) => index === 0 || segment).join('/'),
      levelCode,
      courseCode,
    };
  }
}

const chemistryTopicIdentity = (topicIndex: number): ChemistryTopicIdentity => {
  const identity = chemistryTopicIdentities[topicIndex];
  if (!identity) throw new Error(`Unknown Chemistry runtime topic index: ${topicIndex}`);
  return identity;
};

const chemistryPartReferences: ExamQuestionPartReference[] = [];
const chemistryOfficialKeys = new Map<string, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  prefixIndex,
  questionToken,
  tailIndex,
] of chemistryRuntime.partReferences) {
  const runtimeTopic = chemistryRuntime.topics[topicIndex];
  const identity = chemistryTopicIdentity(topicIndex);
  const prefix = chemistryRuntime.headingPrefixes[prefixIndex];
  const tail = chemistryRuntime.headingTails[tailIndex];
  if (!runtimeTopic || prefix === undefined || tail === undefined) {
    throw new Error(`Unknown Chemistry compact part reference: ${[
      topicIndex,
      yearOffset,
      prefixIndex,
      questionToken,
      tailIndex,
    ].join('|')}`);
  }
  const { id: topicId, levelCode } = identity;
  const year = yearOffset + 2000;
  const sitting: ExamSitting = /Deferred Exam Paper/i.test(prefix)
    ? 'deferred'
    : /Sample Paper/i.test(prefix)
      ? 'sample'
      : 'main';
  const n = /^[A-Za-z]$/.test(questionToken)
    ? /Section\s+11\b/i.test(prefix) ? '11' : '4'
    : questionToken;
  const heading = `${year} - ${prefix}${questionToken}${tail}`;
  const keys = chemistryOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|${sitting}|single|${n}`);
  chemistryOfficialKeys.set(topicId, keys);
  chemistryPartReferences.push({
    subjectId: chemistryRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId,
  });
}

const chemistryTopics: ExamTopicDefinition[] = chemistryRuntime.topics.map(([
  ,
  label,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  reportedQuestionCount,
], topicIndex) => {
  const { id, sourcePath, levelCode, courseCode } = chemistryTopicIdentity(topicIndex);
  return {
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    sourcePath,
    officialQuestionKeys: [...(chemistryOfficialKeys.get(id) ?? [])],
    mockQuestionCount,
    curriculumNodeIds: [...curriculumNodeIds],
    course: courseCode === 'n' ? 'new' : 'old',
    reportedQuestionCount,
    providerSampleQuestionCount,
  };
});

const CHEMISTRY_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: chemistryRuntime.subjectId,
  capturedAt: chemistryRuntime.capturedAt,
  referenceProvider: chemistryRuntime.referenceProvider,
  groups: chemistryRuntime.groups.map(([
    levelCode,
    courseCode,
    id,
    label,
    topicIndexes,
  ]) => ({
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    course: courseCode === 'n' ? 'new' : 'old',
    topicIds: topicIndexes.map(topicIndex => chemistryTopicIdentity(topicIndex).id),
  })),
  topics: chemistryTopics,
};

/**
 * Physics uses the same overlapping-course runtime shape.  The exact audited
 * practice hierarchy stays separate from the outgoing syllabus and the
 * redeveloped 2027 specification, with a many-to-many bridge between them.
 */
interface PhysicsTopicIdentity {
  id: string;
  sourcePath: string;
  levelCode: 'h' | 'o';
  courseCode: 'n' | 'o';
}

const physicsTopicIdentities: Array<PhysicsTopicIdentity | undefined> =
  Array.from({ length: physicsRuntime.topics.length });
for (const [levelCode, courseCode, groupId, , topicIndexes] of physicsRuntime.groups) {
  const variant = `${levelCode === 'h' ? 'higher' : 'ordinary'}-${
    courseCode === 'n' ? 'new-course' : 'old-course'
  }`;
  const groupPrefix = `physics-${variant}`;
  const groupSlug = groupId === groupPrefix
    ? ''
    : groupId.slice(`${groupPrefix}-`.length);
  for (const topicIndex of topicIndexes) {
    const slug = physicsRuntime.topics[topicIndex]?.[0];
    if (!slug || physicsTopicIdentities[topicIndex]) {
      throw new Error(`Invalid Physics group topic index: ${topicIndex}`);
    }
    physicsTopicIdentities[topicIndex] = {
      id: `${groupPrefix}-${slug}`,
      sourcePath: [
        '',
        'leaving-certificate',
        'physics',
        variant,
        groupSlug,
        slug,
      ].filter((segment, index) => index === 0 || segment).join('/'),
      levelCode,
      courseCode,
    };
  }
}

const physicsTopicIdentity = (topicIndex: number): PhysicsTopicIdentity => {
  const identity = physicsTopicIdentities[topicIndex];
  if (!identity) throw new Error(`Unknown Physics runtime topic index: ${topicIndex}`);
  return identity;
};

const physicsPartReferences: ExamQuestionPartReference[] = [];
const physicsOfficialKeys = new Map<string, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  prefixIndex,
  questionToken,
  tailIndex,
] of physicsRuntime.partReferences) {
  const runtimeTopic = physicsRuntime.topics[topicIndex];
  const identity = physicsTopicIdentity(topicIndex);
  const prefix = physicsRuntime.headingPrefixes[prefixIndex];
  const tail = physicsRuntime.headingTails[tailIndex];
  if (!runtimeTopic || prefix === undefined || tail === undefined) {
    throw new Error(`Unknown Physics compact part reference: ${[
      topicIndex,
      yearOffset,
      prefixIndex,
      questionToken,
      tailIndex,
    ].join('|')}`);
  }
  const { id: topicId, levelCode } = identity;
  const year = yearOffset + 2000;
  const sitting: ExamSitting = /Deferred Exam Paper/i.test(prefix)
    ? 'deferred'
    : /Sample Paper/i.test(prefix)
      ? 'sample'
      : 'main';
  const n = /^[A-Za-z]$/.test(questionToken)
    ? /Section\s+11\b/i.test(prefix) ? '11' : questionToken
    : questionToken;
  const heading = `${year} - ${prefix}${questionToken}${tail}`;
  const keys = physicsOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|${sitting}|single|${n}`);
  physicsOfficialKeys.set(topicId, keys);
  physicsPartReferences.push({
    subjectId: physicsRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId,
  });
}

const physicsTopics: ExamTopicDefinition[] = physicsRuntime.topics.map(([
  ,
  label,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  reportedQuestionCount,
], topicIndex) => {
  const { id, sourcePath, levelCode, courseCode } = physicsTopicIdentity(topicIndex);
  return {
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    sourcePath,
    officialQuestionKeys: [...(physicsOfficialKeys.get(id) ?? [])],
    mockQuestionCount,
    curriculumNodeIds: [...curriculumNodeIds],
    course: courseCode === 'n' ? 'new' : 'old',
    reportedQuestionCount,
    providerSampleQuestionCount,
  };
});

const PHYSICS_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: physicsRuntime.subjectId,
  capturedAt: physicsRuntime.capturedAt,
  referenceProvider: physicsRuntime.referenceProvider,
  groups: physicsRuntime.groups.map(([
    levelCode,
    courseCode,
    id,
    label,
    topicIndexes,
  ]) => ({
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    course: courseCode === 'n' ? 'new' : 'old',
    topicIds: topicIndexes.map(topicIndex => physicsTopicIdentity(topicIndex).id),
  })),
  topics: physicsTopics,
};

/**
 * DCG keeps its flat, level-specific drawing-topic menu separate from the
 * official three-strand curriculum. Section A has its own paper key because
 * A1–A4 coexist with the stable B1–B3/C1–C5 card run in each sitting.
 */
const dcgPaperKey = (code: 's' | 'a'): string => code === 'a' ? 'section-a' : 'single';
const designAndCommunicationGraphicsPartReferences: ExamQuestionPartReference[] = [];
const designAndCommunicationGraphicsOfficialKeys = new Map<string, Set<string>>();
for (const [topicIndex, year, sittingCode, paperKeyCode, n, heading] of (
  designAndCommunicationGraphicsRuntime.partReferences
)) {
  const runtimeTopic = designAndCommunicationGraphicsRuntime.topics[topicIndex];
  if (!runtimeTopic) throw new Error(`Unknown DCG runtime topic index: ${topicIndex}`);
  const [topicId, , , , , levelCode] = runtimeTopic;
  const sitting: ExamSitting = sittingCode === 'd' ? 'deferred' : 'main';
  const paperKey = dcgPaperKey(paperKeyCode);
  const keys = designAndCommunicationGraphicsOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|${sitting}|${paperKey}|${n}`);
  designAndCommunicationGraphicsOfficialKeys.set(topicId, keys);
  designAndCommunicationGraphicsPartReferences.push({
    subjectId: designAndCommunicationGraphicsRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey,
    n,
    subdivision: heading,
    topicId,
  });
}

const designAndCommunicationGraphicsTopics: ExamTopicDefinition[] = (
  designAndCommunicationGraphicsRuntime.topics.map(([
    id,
    label,
    sourcePath,
    mockQuestionCount,
    curriculumNodeIds,
    levelCode,
  ]) => ({
    id,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    sourcePath,
    officialQuestionKeys: [...(designAndCommunicationGraphicsOfficialKeys.get(id) ?? [])],
    mockQuestionCount,
    curriculumNodeIds: [...curriculumNodeIds],
  }))
);

const DESIGN_AND_COMMUNICATION_GRAPHICS_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: designAndCommunicationGraphicsRuntime.subjectId,
  capturedAt: designAndCommunicationGraphicsRuntime.capturedAt,
  referenceProvider: designAndCommunicationGraphicsRuntime.referenceProvider,
  groups: designAndCommunicationGraphicsRuntime.groups.map(([levelCode, label, topicIndexes]) => ({
    id: `design-and-communication-graphics-${levelCode === 'h' ? 'higher' : 'ordinary'}`,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = designAndCommunicationGraphicsRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown DCG group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: designAndCommunicationGraphicsTopics,
};

/**
 * French keeps the exact flat Higher and Ordinary practice menus while its
 * generated join distinguishes written and aural cards. Factual sub-question
 * headings are retained for later Mark Bank work; the official curriculum
 * remains the Syllabus X-Ray authority.
 */
const frenchRuntimePaperKey = (code: 's' | 'a' | 'o'): string => (
  code === 'a' ? 'aural' : code === 'o' ? 'oral' : 'single'
);

const frenchPartReferences: ExamQuestionPartReference[] = [];
const frenchOfficialQuestionKeys = new Map<number, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  levelCode,
  paperKeyCode,
  sittingCode,
  n,
  heading,
] of frenchRuntime.partReferences) {
  const topic = frenchRuntime.topics[topicIndex];
  if (!topic) throw new Error(`Unknown French runtime topic index: ${topicIndex}`);
  const year = yearOffset + 2000;
  const sitting: ExamSitting = sittingCode === 'd' ? 'deferred' : 'main';
  const paperKey = frenchRuntimePaperKey(paperKeyCode);
  const keys = frenchOfficialQuestionKeys.get(topicIndex) ?? new Set<string>();
  keys.add(`${year}|${sitting}|${paperKey}|${n}`);
  frenchOfficialQuestionKeys.set(topicIndex, keys);
  frenchPartReferences.push({
    subjectId: frenchRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey,
    n,
    subdivision: heading,
    topicId: topic[0],
  });
}

const frenchTopics: ExamTopicDefinition[] = frenchRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  levelCode,
  reportedQuestionCount,
], topicIndex) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  officialQuestionKeys: [...(frenchOfficialQuestionKeys.get(topicIndex) ?? [])],
  mockQuestionCount,
  providerSampleQuestionCount,
  reportedQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const FRENCH_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: frenchRuntime.subjectId,
  capturedAt: frenchRuntime.capturedAt,
  referenceProvider: frenchRuntime.referenceProvider,
  groups: frenchRuntime.groups.map(([levelCode, label, topicIndexes]) => ({
    id: `french-${levelCode === 'h' ? 'higher' : 'ordinary'}`,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = frenchRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown French group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: frenchTopics,
};

/**
 * German keeps the exact Higher/Ordinary Aural and Written shelves captured
 * from the reference. The generated join uses stable semantic paper slots so
 * legacy reading-card numbers cannot collide with grammar or short writing.
 */
const germanRuntimePaperKey = (code: 's' | 'a'): 'single' | 'aural' => (
  code === 'a' ? 'aural' : 'single'
);

const germanPartReferences: ExamQuestionPartReference[] = [];
const germanOfficialQuestionKeys = new Map<number, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  levelCode,
  paperKeyCode,
  sittingCode,
  n,
  heading,
] of germanRuntime.partReferences) {
  const topic = germanRuntime.topics[topicIndex];
  if (!topic) throw new Error(`Unknown German runtime topic index: ${topicIndex}`);
  const year = yearOffset + 2000;
  const sitting: ExamSitting = sittingCode === 'd' ? 'deferred' : 'main';
  const paperKey = germanRuntimePaperKey(paperKeyCode);
  const keys = germanOfficialQuestionKeys.get(topicIndex) ?? new Set<string>();
  keys.add(`${year}|${sitting}|${paperKey}|${n}`);
  germanOfficialQuestionKeys.set(topicIndex, keys);
  germanPartReferences.push({
    subjectId: germanRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey,
    n,
    subdivision: heading,
    topicId: topic[0],
  });
}

const germanTopics: ExamTopicDefinition[] = germanRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  levelCode,
  reportedQuestionCount,
], topicIndex) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  officialQuestionKeys: [...(germanOfficialQuestionKeys.get(topicIndex) ?? [])],
  mockQuestionCount,
  providerSampleQuestionCount,
  reportedQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const GERMAN_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: germanRuntime.subjectId,
  capturedAt: germanRuntime.capturedAt,
  referenceProvider: germanRuntime.referenceProvider,
  groups: germanRuntime.groups.map(([levelCode, groupId, label, topicIndexes]) => ({
    id: `german-${levelCode === 'h' ? 'higher' : 'ordinary'}-${groupId}`,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = germanRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown German group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: germanTopics,
};

/**
 * Music retains the flat Higher and Ordinary reference menus while appending
 * explicit archive shelves for retired set works and the Higher listening
 * elective. Factual headings remain file-aware metadata: Music's four SEC
 * components all restart at Question 1 under the same legacy paper key, so
 * they must never populate the generic question-key map.
 */
const musicComponent = (code: '6' | '7' | '8' | 'u'): '006' | '007' | '008' | 'U00' => ({
  '6': '006',
  '7': '007',
  '8': '008',
  u: 'U00',
})[code] as '006' | '007' | '008' | 'U00';

const musicFileid = (
  levelCode: 'h' | 'o',
  langCode: 'e' | 'i',
  componentCode: '6' | '7' | '8' | 'u',
) => `LC067${levelCode === 'h' ? 'A' : 'G'}LP${musicComponent(componentCode)}${langCode === 'e' ? 'EV' : 'IV'}.pdf`;

const musicPartReferences: ExamQuestionPartReference[] = musicRuntime.partReferences.map(([
  topicIndex,
  yearOffset,
  levelCode,
  sittingCode,
  _componentCode,
  n,
  heading,
  fileid,
]) => {
  const topic = musicRuntime.topics[topicIndex];
  if (!topic) throw new Error(`Unknown Music runtime topic index: ${topicIndex}`);
  const sitting: ExamSitting = sittingCode === 'd'
    ? 'deferred'
    : sittingCode === 'x'
      ? 'sample'
      : 'main';
  return {
    subjectId: musicRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year: yearOffset + 2000,
    sitting,
    paperKey: 'single',
    ...(fileid ? { fileid } : {}),
    n,
    subdivision: heading,
    topicId: topic[0],
  };
});

const musicTopics: ExamTopicDefinition[] = musicRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  levelCode,
  reportedQuestionCount,
]) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  // Deliberately empty. Exact component/file joins below are authoritative.
  officialQuestionKeys: [],
  mockQuestionCount,
  providerSampleQuestionCount,
  reportedQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const MUSIC_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: musicRuntime.subjectId,
  capturedAt: musicRuntime.capturedAt,
  referenceProvider: musicRuntime.referenceProvider,
  groups: musicRuntime.groups.map(([levelCode, groupId, label, topicIndexes]) => ({
    id: groupId,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = musicRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Music group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: musicTopics,
};

/**
 * Irish keeps the exact flat Higher, Ordinary and Foundation menus captured
 * from the reference. Two explicitly labelled archive topics are appended so
 * the migration cannot erase Higher additional literature or Foundation
 * listening that exists in the entitled local SEC corpus.
 */
const irishLevel = (code: 'h' | 'o' | 'f'): PaperLevel => (
  code === 'h' ? 'higher' : code === 'o' ? 'ordinary' : 'foundation'
);
const irishRuntimePaperKey = (
  code: 's' | '1' | '2' | 'a' | 'o',
): 'single' | 'p1' | 'p2' | 'aural' | 'oral' => ({
  s: 'single',
  '1': 'p1',
  '2': 'p2',
  a: 'aural',
  o: 'oral',
})[code] as 'single' | 'p1' | 'p2' | 'aural' | 'oral';

const irishPartReferences: ExamQuestionPartReference[] = [];
const irishOfficialQuestionKeys = new Map<number, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  levelCode,
  paperKeyCode,
  sittingCode,
  n,
  heading,
] of irishRuntime.partReferences) {
  const topic = irishRuntime.topics[topicIndex];
  if (!topic) throw new Error(`Unknown Irish runtime topic index: ${topicIndex}`);
  const year = yearOffset + 2000;
  const sitting: ExamSitting = sittingCode === 'd'
    ? 'deferred'
    : sittingCode === 'x'
      ? 'sample'
      : 'main';
  const paperKey = irishRuntimePaperKey(paperKeyCode);
  const keys = irishOfficialQuestionKeys.get(topicIndex) ?? new Set<string>();
  keys.add(`${year}|${sitting}|${paperKey}|${n}`);
  irishOfficialQuestionKeys.set(topicIndex, keys);
  irishPartReferences.push({
    subjectId: irishRuntime.subjectId,
    level: irishLevel(levelCode),
    year,
    sitting,
    paperKey,
    n,
    subdivision: heading,
    topicId: topic[0],
  });
}

const irishTopics: ExamTopicDefinition[] = irishRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  levelCode,
  reportedQuestionCount,
], topicIndex) => ({
  id,
  label,
  level: irishLevel(levelCode),
  sourcePath,
  officialQuestionKeys: [...(irishOfficialQuestionKeys.get(topicIndex) ?? [])],
  mockQuestionCount,
  providerSampleQuestionCount,
  reportedQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const IRISH_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: irishRuntime.subjectId,
  capturedAt: irishRuntime.capturedAt,
  referenceProvider: irishRuntime.referenceProvider,
  groups: irishRuntime.groups.map(([levelCode, groupId, label, topicIndexes]) => ({
    id: groupId,
    label,
    level: irishLevel(levelCode),
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = irishRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Irish group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: irishTopics,
};

/**
 * Italian keeps the exact flat Higher and Ordinary practice menus captured
 * from the reference while resolving them onto the complete, level-aware SEC
 * corpus. Current title-specific literature buckets and historical prescribed
 * cards remain distinct through the generated crosswalk.
 */
const italianRuntimePaperKey = (code: 's' | 'a'): 'single' | 'aural' => (
  code === 'a' ? 'aural' : 'single'
);

const italianPartReferences: ExamQuestionPartReference[] = [];
const italianOfficialQuestionKeys = new Map<number, Set<string>>();
for (const [topicIndex, yearOffset, levelCode, paperKeyCode, n, heading] of italianRuntime.partReferences) {
  const topic = italianRuntime.topics[topicIndex];
  if (!topic) throw new Error(`Unknown Italian runtime topic index: ${topicIndex}`);
  const paperKey = italianRuntimePaperKey(paperKeyCode);
  const keys = italianOfficialQuestionKeys.get(topicIndex) ?? new Set<string>();
  keys.add(`${yearOffset + 2000}|main|${paperKey}|${n}`);
  italianOfficialQuestionKeys.set(topicIndex, keys);
  italianPartReferences.push({
    subjectId: italianRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year: yearOffset + 2000,
    sitting: 'main',
    paperKey,
    n,
    subdivision: heading,
    topicId: topic[0],
  });
}

const italianTopics: ExamTopicDefinition[] = italianRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  levelCode,
  reportedQuestionCount,
], topicIndex) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  officialQuestionKeys: [...(italianOfficialQuestionKeys.get(topicIndex) ?? [])],
  mockQuestionCount,
  providerSampleQuestionCount,
  reportedQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const ITALIAN_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: italianRuntime.subjectId,
  capturedAt: italianRuntime.capturedAt,
  referenceProvider: italianRuntime.referenceProvider,
  groups: italianRuntime.groups.map(([levelCode, label, topicIndexes]) => ({
    id: `italian-${levelCode === 'h' ? 'higher' : 'ordinary'}`,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = italianRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Italian group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: italianTopics,
};

/**
 * Spanish keeps StudyClix's exact Higher/Ordinary Aural, Oral and Written
 * shelves. The local join is file-aware because the preserved Spanish corpus
 * historically used `single` for both written and aural cards, whose printed
 * numbers restart independently. Superseded prescribed texts remain in one
 * explicit local extension instead of being mislabeled as the current novel.
 */
const spanishFileid = (
  levelCode: 'h' | 'o',
  langCode: 'e' | 'i',
  kindCode: 'w' | 'a',
): string => (
  `LC012${levelCode === 'h' ? 'A' : 'G'}L${kindCode === 'a' ? 'PA00' : 'P000'}${langCode === 'e' ? 'E' : 'I'}V.pdf`
);

const spanishPaperKey = (kindCode: 'w' | 'a' | 'o'): string => (
  kindCode === 'o' ? 'oral' : 'single'
);

const spanishPartReferences: ExamQuestionPartReference[] = [];
const spanishOfficialQuestionKeys = new Map<number, Set<string>>();
for (const [
  topicIndex,
  yearOffset,
  levelCode,
  kindCode,
  sittingCode,
  n,
  heading,
] of spanishRuntime.partReferences) {
  const topic = spanishRuntime.topics[topicIndex];
  if (!topic) throw new Error(`Unknown Spanish runtime topic index: ${topicIndex}`);
  const year = yearOffset + 2000;
  const sitting: ExamSitting = sittingCode === 'd' ? 'deferred' : 'main';
  const paperKey = spanishPaperKey(kindCode);
  const keys = spanishOfficialQuestionKeys.get(topicIndex) ?? new Set<string>();
  keys.add(`${year}|${sitting}|${paperKey}|${n}`);
  spanishOfficialQuestionKeys.set(topicIndex, keys);
  spanishPartReferences.push({
    subjectId: spanishRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting,
    paperKey,
    ...(year >= 2010 && sitting === 'main' && kindCode !== 'o'
      ? { fileid: spanishFileid(levelCode, 'e', kindCode) }
      : {}),
    n,
    subdivision: heading,
    topicId: topic[0],
  });
}

const spanishTopics: ExamTopicDefinition[] = spanishRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  providerSampleQuestionCount,
  curriculumNodeIds,
  levelCode,
  reportedQuestionCount,
], topicIndex) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  officialQuestionKeys: [...(spanishOfficialQuestionKeys.get(topicIndex) ?? [])],
  mockQuestionCount,
  providerSampleQuestionCount,
  reportedQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const SPANISH_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: spanishRuntime.subjectId,
  capturedAt: spanishRuntime.capturedAt,
  referenceProvider: spanishRuntime.referenceProvider,
  groups: spanishRuntime.groups.map(([levelCode, groupId, label, topicIndexes]) => ({
    id: `spanish-${levelCode === 'h' ? 'higher' : 'ordinary'}-${groupId}`,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = spanishRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Spanish group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: spanishTopics,
};

/**
 * StudyClix exposes one shared Japanese practice menu even though the written
 * and aural papers in the SEC corpus retain Higher/Ordinary identities. The
 * generated compact runtime resolves each factual reference heading to stable
 * Paper Trail cards, while Syllabus X-Ray continues to use the official nodes.
 */
const JAPANESE_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'japanese-common-aural-conversation': ['japanese-6-0'],
  'japanese-common-aural-interviewspeech': ['japanese-6-1'],
  'japanese-common-aural-radionews': ['japanese-6-2'],
  'japanese-common-comprehension-general-reading': [
    'japanese-5-0', 'japanese-5-1', 'japanese-5-2', 'japanese-5-6',
  ],
  'japanese-common-comprehension-website': ['japanese-5-0'],
  'japanese-common-grammar': ['japanese-5-5'],
  'japanese-common-kanji': ['japanese-5-4'],
  'japanese-common-oral-exam': [
    'japanese-4-0',
    'japanese-0-0', 'japanese-0-1', 'japanese-0-2', 'japanese-0-3',
    'japanese-0-4', 'japanese-0-5', 'japanese-0-6', 'japanese-0-7',
    'japanese-0-8', 'japanese-0-9', 'japanese-0-10',
  ],
  'japanese-common-personal-writing-all': ['japanese-5-7'],
  'japanese-common-translation-japanese-to-english': ['japanese-5-3'],
  'japanese-common-writing-holidays-abroad-events': ['japanese-5-7'],
  'japanese-common-writing-home-ireland': ['japanese-5-7'],
  'japanese-common-writing-me-my-family': ['japanese-5-7'],
  'japanese-common-writing-school-studying-japanese-future-plans': ['japanese-5-7'],
};

const japaneseRuntimePaperKey = (code: 's' | 'a' | 'r'): 'single' | 'aural' | 'oral' => {
  if (code === 's') return 'single';
  if (code === 'a') return 'aural';
  return 'oral';
};

const japanesePartReferences: ExamQuestionPartReference[] = [];
const japaneseOfficialQuestionKeys = new Map<number, Set<string>>();
for (const [topicIndex, year, levelCode, paperKeyCode, n, heading] of japaneseRuntime.partReferences) {
  const topic = japaneseAudit.levels.common.topics[topicIndex];
  if (!topic) throw new Error(`Unknown Japanese runtime topic index: ${topicIndex}`);
  const paperKey = japaneseRuntimePaperKey(paperKeyCode);
  const officialQuestionKeys = japaneseOfficialQuestionKeys.get(topicIndex) ?? new Set<string>();
  officialQuestionKeys.add(`${year}|main|${paperKey}|${n}`);
  japaneseOfficialQuestionKeys.set(topicIndex, officialQuestionKeys);
  japanesePartReferences.push({
    subjectId: japaneseAudit.subjectId,
    level: levelCode === 'c' ? 'common' : levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting: 'main',
    paperKey,
    n,
    subdivision: heading,
    topicId: topic.id,
  });
}

const japaneseTopics: ExamTopicDefinition[] = japaneseAudit.levels.common.topics.map((topic, topicIndex) => {
  return {
    id: topic.id,
    label: topic.label,
    level: 'common',
    sourcePath: topic.sourcePath,
    officialQuestionKeys: [...(japaneseOfficialQuestionKeys.get(topicIndex) ?? [])],
    mockQuestionCount: topic.mockQuestionCount,
    curriculumNodeIds: JAPANESE_CURRICULUM_CROSSWALK[topic.id] ?? [],
  };
});

const JAPANESE_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: japaneseAudit.subjectId,
  capturedAt: japaneseAudit.capturedAt,
  referenceProvider: japaneseAudit.reference.provider,
  groups: [{
    id: 'japanese-common',
    label: japaneseAudit.levels.common.label,
    level: 'common',
    topicIds: japaneseAudit.levels.common.topics.map(topic => topic.id),
  }],
  topics: japaneseTopics,
};

/**
 * StudyClix exposes a single Physics & Chemistry menu, but its factual cards
 * resolve to Higher Level SEC papers. The generated bridge keeps that exact
 * flat menu while preserving Higher/Ordinary and English/Irish local paper
 * identities. Syllabus X-Ray continues to use the canonical curriculum nodes.
 */
const physicsAndChemistryPartReferences: ExamQuestionPartReference[] = [];
const physicsAndChemistryOfficialKeys = new Map<string, Set<string>>();
for (const [topicIndex, year, n, heading] of physicsAndChemistryRuntime.partReferences) {
  const topicId = physicsAndChemistryRuntime.topics[topicIndex]?.[0];
  if (!topicId) throw new Error(`Unknown Physics & Chemistry runtime topic index: ${topicIndex}`);
  const keys = physicsAndChemistryOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|main|single|${n}`);
  physicsAndChemistryOfficialKeys.set(topicId, keys);
  physicsAndChemistryPartReferences.push({
    subjectId: physicsAndChemistryRuntime.subjectId,
    level: 'higher',
    year,
    sitting: 'main',
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId,
  });
}

const physicsAndChemistryTopics: ExamTopicDefinition[] = physicsAndChemistryRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  curriculumNodeIds,
]) => ({
  id,
  label,
  level: 'common',
  sourcePath,
  officialQuestionKeys: [...(physicsAndChemistryOfficialKeys.get(id) ?? [])],
  mockQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const PHYSICS_AND_CHEMISTRY_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: physicsAndChemistryRuntime.subjectId,
  capturedAt: physicsAndChemistryRuntime.capturedAt,
  referenceProvider: physicsAndChemistryRuntime.referenceProvider,
  groups: [{
    id: 'physics-and-chemistry-common',
    label: physicsAndChemistryRuntime.groupLabel,
    level: 'common',
    topicIds: physicsAndChemistryTopics.map(topic => topic.id),
  }],
  topics: physicsAndChemistryTopics,
};

/**
 * Religious Education uses the official ten syllabus sections as its flat
 * practice menu at each level. The generated bridge retains the reference
 * site's part-level headings while each local card remains the complete
 * printed SEC section, preserving the paper's real answer-choice boundary.
 */
const religiousEducationPartReferences: ExamQuestionPartReference[] = [];
const religiousEducationOfficialKeys = new Map<string, Set<string>>();
for (const [topicIndex, year, n, heading] of religiousEducationRuntime.partReferences) {
  const runtimeTopic = religiousEducationRuntime.topics[topicIndex];
  if (!runtimeTopic) throw new Error(`Unknown Religious Education runtime topic index: ${topicIndex}`);
  const [topicId, , , , , levelCode] = runtimeTopic;
  const keys = religiousEducationOfficialKeys.get(topicId) ?? new Set<string>();
  keys.add(`${year}|main|single|${n}`);
  religiousEducationOfficialKeys.set(topicId, keys);
  religiousEducationPartReferences.push({
    subjectId: religiousEducationRuntime.subjectId,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    year,
    sitting: 'main',
    paperKey: 'single',
    n,
    subdivision: heading,
    topicId,
  });
}

const religiousEducationTopics: ExamTopicDefinition[] = religiousEducationRuntime.topics.map(([
  id,
  label,
  sourcePath,
  mockQuestionCount,
  curriculumNodeIds,
  levelCode,
]) => ({
  id,
  label,
  level: levelCode === 'h' ? 'higher' : 'ordinary',
  sourcePath,
  officialQuestionKeys: [...(religiousEducationOfficialKeys.get(id) ?? [])],
  mockQuestionCount,
  curriculumNodeIds: [...curriculumNodeIds],
}));

const RELIGIOUS_EDUCATION_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: religiousEducationRuntime.subjectId,
  capturedAt: religiousEducationRuntime.capturedAt,
  referenceProvider: religiousEducationRuntime.referenceProvider,
  groups: religiousEducationRuntime.groups.map(([levelCode, label, topicIndexes]) => ({
    id: `religious-education-${levelCode === 'h' ? 'higher' : 'ordinary'}`,
    label,
    level: levelCode === 'h' ? 'higher' : 'ordinary',
    topicIds: topicIndexes.map(topicIndex => {
      const topicId = religiousEducationRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Religious Education group topic index: ${topicIndex}`);
      return topicId;
    }),
  })),
  topics: religiousEducationTopics,
};

const CLASSICAL_STUDIES_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'classical-studies-higher-funerary-practices': ['classical-studies-3-2'],
  'classical-studies-higher-greek-drama': ['classical-studies-1-0', 'classical-studies-1-1', 'classical-studies-1-2'],
  'classical-studies-higher-mythology': ['classical-studies-0-2', 'classical-studies-3-0'],
  'classical-studies-higher-philosophy': ['classical-studies-3-3'],
  'classical-studies-higher-power-and-identity': ['classical-studies-2-0', 'classical-studies-2-1', 'classical-studies-2-2', 'classical-studies-2-3', 'classical-studies-2-4'],
  'classical-studies-higher-roman-spectacle': ['classical-studies-1-3'],
  'classical-studies-higher-temples': ['classical-studies-3-1'],
  'classical-studies-higher-world-of-heroes': ['classical-studies-0-0', 'classical-studies-0-1', 'classical-studies-0-2', 'classical-studies-0-3', 'classical-studies-0-4'],

  'classical-studies-ordinary-funerary-practices': ['classical-studies-3-2'],
  'classical-studies-ordinary-greek-drama': ['classical-studies-1-0', 'classical-studies-1-1', 'classical-studies-1-2'],
  'classical-studies-ordinary-mythology': ['classical-studies-0-2', 'classical-studies-3-0'],
  'classical-studies-ordinary-philosophy': ['classical-studies-3-3'],
  'classical-studies-ordinary-power-and-identity': ['classical-studies-2-0', 'classical-studies-2-1', 'classical-studies-2-2', 'classical-studies-2-3', 'classical-studies-2-4'],
  'classical-studies-ordinary-roman-spectacle': ['classical-studies-1-3'],
  'classical-studies-ordinary-temples': ['classical-studies-3-1'],
  'classical-studies-ordinary-world-of-heroes': ['classical-studies-0-0', 'classical-studies-0-1', 'classical-studies-0-2', 'classical-studies-0-3', 'classical-studies-0-4'],
};

const parseClassicalStudiesHeading = (heading: string): {
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision?: string;
} => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const question = heading.match(/Question\s+(\d+)/i);
  if (!year || !question) throw new Error(`Unparseable Classical Studies reference heading: ${heading}`);
  const sitting: ExamSitting = /Sample Paper/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main';
  const subdivision = heading.slice((question.index ?? 0) + question[0].length)
    .replace(/^\s*-\s*/, '')
    .trim() || undefined;
  return { year, sitting, paperKey: 'single', n: question[1], subdivision };
};

const classicalStudiesLevels = ['higher', 'ordinary'] as const;
const classicalStudiesPartReferences: ExamQuestionPartReference[] = [];
const classicalStudiesTopics: ExamTopicDefinition[] = classicalStudiesLevels.flatMap((level) =>
  classicalStudiesAudit.levels[level].topics.map((topic) => {
    const officialQuestionKeys = new Set<string>();
    for (const heading of topic.officialQuestionHeadings) {
      const parsed = parseClassicalStudiesHeading(heading);
      officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
      classicalStudiesPartReferences.push({
        subjectId: classicalStudiesAudit.subjectId,
        level,
        ...parsed,
        topicId: topic.id,
      });
    }
    return {
      id: topic.id,
      label: topic.label,
      level,
      sourcePath: topic.sourcePath,
      officialQuestionKeys: [...officialQuestionKeys],
      mockQuestionCount: topic.mockQuestionCount,
      curriculumNodeIds: CLASSICAL_STUDIES_CURRICULUM_CROSSWALK[topic.id] ?? [],
    };
  }),
);

const CLASSICAL_STUDIES_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: classicalStudiesAudit.subjectId,
  capturedAt: classicalStudiesAudit.capturedAt,
  referenceProvider: classicalStudiesAudit.reference.provider,
  groups: classicalStudiesLevels.map((level) => ({
    id: `classical-studies-${level}`,
    label: classicalStudiesAudit.levels[level].label,
    level,
    topicIds: classicalStudiesAudit.levels[level].topics.map(topic => topic.id),
  })),
  topics: classicalStudiesTopics,
};

/**
 * Politics & Society has eight content themes plus two deliberately overlapping
 * assessment lenses. The official curriculum tree remains intact; these links
 * only power the simpler exam-practice menu students browse in Topic Atlas.
 */
const POLITICS_AND_SOCIETY_CONTENT_CROSSWALK: Record<string, string[]> = {
  '1-power-and-decision-making-at-national-and-european-level': [
    'politics-and-society-0-4', 'politics-and-society-0-5', 'politics-and-society-0-6',
    'politics-and-society-0-7', 'politics-and-society-0-8', 'politics-and-society-0-9',
    'politics-and-society-0-10', 'politics-and-society-0-12',
  ],
  '1-power-and-decision-making-in-the-school': [
    'politics-and-society-0-0', 'politics-and-society-0-1', 'politics-and-society-0-2',
    'politics-and-society-0-3', 'politics-and-society-0-11',
  ],
  '2-effectively-contributing-to-communities': [
    'politics-and-society-1-0', 'politics-and-society-1-1', 'politics-and-society-1-2',
    'politics-and-society-1-3', 'politics-and-society-1-4', 'politics-and-society-1-5',
    'politics-and-society-1-11',
  ],
  '2-rights-and-responsibilities-in-communication-with-others': [
    'politics-and-society-1-6', 'politics-and-society-1-7', 'politics-and-society-1-8',
    'politics-and-society-1-9', 'politics-and-society-1-10', 'politics-and-society-1-12',
  ],
  '3-human-rights-and-responsibilities-in-europe-and-the-wider-world': [
    'politics-and-society-2-7', 'politics-and-society-2-8', 'politics-and-society-2-9',
    'politics-and-society-2-11',
  ],
  '3-human-rights-and-responsibilities-in-ireland': [
    'politics-and-society-2-0', 'politics-and-society-2-1', 'politics-and-society-2-2',
    'politics-and-society-2-3', 'politics-and-society-2-4', 'politics-and-society-2-5',
    'politics-and-society-2-6', 'politics-and-society-2-10',
  ],
  '4-globalisation-and-identity': [
    'politics-and-society-3-0', 'politics-and-society-3-1', 'politics-and-society-3-2',
    'politics-and-society-3-3', 'politics-and-society-3-4', 'politics-and-society-3-5',
    'politics-and-society-3-6', 'politics-and-society-3-10',
  ],
  '4-sustainable-development': [
    'politics-and-society-3-7', 'politics-and-society-3-8', 'politics-and-society-3-9',
    'politics-and-society-3-11',
  ],
};

const POLITICS_AND_SOCIETY_ALL_CONTENT_NODES = [...new Set(
  Object.values(POLITICS_AND_SOCIETY_CONTENT_CROSSWALK).flat(),
)];
const POLITICS_AND_SOCIETY_CROSSWALK: Record<string, string[]> = {};
for (const level of ['higher', 'ordinary'] as const) {
  for (const [slug, ids] of Object.entries(POLITICS_AND_SOCIETY_CONTENT_CROSSWALK)) {
    POLITICS_AND_SOCIETY_CROSSWALK[`politics-and-society-${level}-${slug}`] = ids;
  }
  // Data-based questions are an assessment format which may draw on any of
  // the eight official themes, so the bridge is intentionally broad.
  POLITICS_AND_SOCIETY_CROSSWALK[`politics-and-society-${level}-data-based-questions`] =
    POLITICS_AND_SOCIETY_ALL_CONTENT_NODES;
  POLITICS_AND_SOCIETY_CROSSWALK[`politics-and-society-${level}-key-thinkers`] = [
    'politics-and-society-0-10',
    'politics-and-society-2-6',
    'politics-and-society-3-6',
    'politics-and-society-3-9',
  ];
}

const parsePoliticsAndSocietyHeading = (
  level: 'higher' | 'ordinary',
  heading: string,
): Array<{
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision: string;
}> => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const section = heading.match(/Section\s+([A-Za-z]\d?)/i)?.[1]?.toUpperCase();
  if (!year || !section) throw new Error(`Unparseable Politics and Society reference heading: ${heading}`);
  const sitting: ExamSitting = /Sample Paper/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main';
  let numbers: string[];
  if (section.startsWith('A')) {
    // The reference lists individual lettered short-answer parts while Paper
    // Trail deliberately exposes the complete Section A as one question card.
    numbers = ['1'];
  } else if (section === 'B') {
    // Higher exposes the complete DBQ as Q2. Ordinary exposes its three
    // printed questions as cards 2–4, even when the reference heading shortens
    // the whole section to just "Question 2".
    numbers = level === 'ordinary' ? ['2', '3', '4'] : ['2'];
  } else if (section === 'C') {
    const number = heading.match(/Question\s+(\d+)/i)?.[1];
    if (!number) throw new Error(`Politics and Society Section C heading has no question number: ${heading}`);
    numbers = [number];
  } else {
    throw new Error(`Unknown Politics and Society section in reference heading: ${heading}`);
  }
  const subdivision = heading.replace(/^\d{4}\s*-\s*/, '').trim();
  return numbers.map(n => ({ year, sitting, paperKey: 'single', n, subdivision }));
};

const politicsAndSocietyLevels = ['higher', 'ordinary'] as const;
const politicsAndSocietyPartReferences: ExamQuestionPartReference[] = [];
const politicsAndSocietyTopics: ExamTopicDefinition[] = politicsAndSocietyLevels.flatMap((level) =>
  politicsAndSocietyAudit.levels[level].topics.map((topic) => {
    const officialQuestionKeys = new Set<string>();
    for (const heading of topic.officialQuestionHeadings) {
      for (const parsed of parsePoliticsAndSocietyHeading(level, heading)) {
        officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
        politicsAndSocietyPartReferences.push({
          subjectId: politicsAndSocietyAudit.subjectId,
          level,
          ...parsed,
          topicId: topic.id,
        });
      }
    }
    return {
      id: topic.id,
      label: topic.label,
      level,
      sourcePath: topic.sourcePath,
      officialQuestionKeys: [...officialQuestionKeys],
      mockQuestionCount: topic.mockQuestionCount,
      curriculumNodeIds: POLITICS_AND_SOCIETY_CROSSWALK[topic.id] ?? [],
    };
  }),
);

const POLITICS_AND_SOCIETY_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: politicsAndSocietyAudit.subjectId,
  capturedAt: politicsAndSocietyAudit.capturedAt,
  referenceProvider: politicsAndSocietyAudit.reference.provider,
  groups: politicsAndSocietyLevels.map(level => ({
    id: `politics-and-society-${level}`,
    label: politicsAndSocietyAudit.levels[level].label,
    level,
    topicIds: politicsAndSocietyAudit.levels[level].topics.map(topic => topic.id),
  })),
  topics: politicsAndSocietyTopics,
};

const TAXONOMIES = new Map<string, ExamTopicTaxonomy>([
  [ACCOUNTING_TAXONOMY.subjectId, ACCOUNTING_TAXONOMY],
  [AGRICULTURAL_SCIENCE_TAXONOMY.subjectId, AGRICULTURAL_SCIENCE_TAXONOMY],
  [APPLIED_MATHEMATICS_TAXONOMY.subjectId, APPLIED_MATHEMATICS_TAXONOMY],
  [ART_TAXONOMY.subjectId, ART_TAXONOMY],
  [BIOLOGY_TAXONOMY.subjectId, BIOLOGY_TAXONOMY],
  [BUSINESS_TAXONOMY.subjectId, BUSINESS_TAXONOMY],
  [CHEMISTRY_TAXONOMY.subjectId, CHEMISTRY_TAXONOMY],
  [CLASSICAL_STUDIES_TAXONOMY.subjectId, CLASSICAL_STUDIES_TAXONOMY],
  [COMPUTER_SCIENCE_TAXONOMY.subjectId, COMPUTER_SCIENCE_TAXONOMY],
  [CONSTRUCTION_STUDIES_TAXONOMY.subjectId, CONSTRUCTION_STUDIES_TAXONOMY],
  [DESIGN_AND_COMMUNICATION_GRAPHICS_TAXONOMY.subjectId, DESIGN_AND_COMMUNICATION_GRAPHICS_TAXONOMY],
  [ECONOMICS_TAXONOMY.subjectId, ECONOMICS_TAXONOMY],
  [ENGINEERING_TAXONOMY.subjectId, ENGINEERING_TAXONOMY],
  [ENGLISH_TAXONOMY.subjectId, ENGLISH_TAXONOMY],
  [FRENCH_TAXONOMY.subjectId, FRENCH_TAXONOMY],
  [GERMAN_TAXONOMY.subjectId, GERMAN_TAXONOMY],
  [GEOGRAPHY_TAXONOMY.subjectId, GEOGRAPHY_TAXONOMY],
  [HISTORY_TAXONOMY.subjectId, HISTORY_TAXONOMY],
  [HOME_ECONOMICS_TAXONOMY.subjectId, HOME_ECONOMICS_TAXONOMY],
  [IRISH_TAXONOMY.subjectId, IRISH_TAXONOMY],
  [ITALIAN_TAXONOMY.subjectId, ITALIAN_TAXONOMY],
  [JAPANESE_TAXONOMY.subjectId, JAPANESE_TAXONOMY],
  [LINK_MODULES_TAXONOMY.subjectId, LINK_MODULES_TAXONOMY],
  [MATHEMATICS_TAXONOMY.subjectId, MATHEMATICS_TAXONOMY],
  [MUSIC_TAXONOMY.subjectId, MUSIC_TAXONOMY],
  [PHYSICAL_EDUCATION_TAXONOMY.subjectId, PHYSICAL_EDUCATION_TAXONOMY],
  [PHYSICS_TAXONOMY.subjectId, PHYSICS_TAXONOMY],
  [PHYSICS_AND_CHEMISTRY_TAXONOMY.subjectId, PHYSICS_AND_CHEMISTRY_TAXONOMY],
  [POLITICS_AND_SOCIETY_TAXONOMY.subjectId, POLITICS_AND_SOCIETY_TAXONOMY],
  [RELIGIOUS_EDUCATION_TAXONOMY.subjectId, RELIGIOUS_EDUCATION_TAXONOMY],
  [SPANISH_TAXONOMY.subjectId, SPANISH_TAXONOMY],
  [TECHNOLOGY_TAXONOMY.subjectId, TECHNOLOGY_TAXONOMY],
]);

const TOPICS_BY_ID = new Map<string, ExamTopicDefinition>();
const QUESTION_TOPICS = new Map<string, string[]>();
const FILE_QUESTION_TOPICS = new Map<string, string[]>();

// Geography and Physical Education already expose their replacement-course
// menus, but the local SEC archive currently ends before those courses' first
// examination. Keep the factual headings in the taxonomy while preventing an
// outgoing paper card from appearing in a future-course shelf.
const REPLACEMENT_COURSE_FIRST_EXAM: Partial<Record<string, number>> = {
  geography: 2028,
  'physical-education': 2028,
};

const topicAppliesToExamYear = (
  subjectId: string,
  topic: Pick<ExamTopicDefinition, 'course'>,
  year: number,
): boolean => {
  const firstExam = REPLACEMENT_COURSE_FIRST_EXAM[subjectId];
  if (!firstExam || !topic.course) return true;
  return year >= firstExam ? topic.course === 'new' : topic.course === 'old';
};

const questionKey = (
  subjectId: string,
  level: PaperLevel,
  year: number,
  sitting: ExamSitting,
  n: string,
  paperKey = 'single',
  lang: PaperLang | 'any' = 'any',
) => `${subjectId}|${level}|${year}|${sitting}|${paperKey}|${lang}|${n}`;

const fileQuestionKey = (
  subjectId: string,
  level: PaperLevel,
  year: number,
  sitting: ExamSitting,
  fileid: string,
  n: string,
  paperKey = 'single',
  lang: PaperLang | 'any' = 'any',
) => `${subjectId}|${level}|${year}|${sitting}|${paperKey}|${lang}|${fileid}|${n}`;

for (const taxonomy of TAXONOMIES.values()) {
  for (const topic of taxonomy.topics) {
    TOPICS_BY_ID.set(topic.id, topic);
    for (const officialKey of topic.officialQuestionKeys) {
      const [year, sitting, ...identity] = officialKey.split('|');
      if (!topicAppliesToExamYear(taxonomy.subjectId, topic, Number(year))) continue;
      const paperKey = identity.length === 1 ? 'single' : identity[0];
      const n = identity.length === 1 ? identity[0] : identity[1];
      const key = questionKey(
        taxonomy.subjectId,
        topic.level,
        Number(year),
        sitting as ExamSitting,
        n,
        paperKey,
      );
      const ids = QUESTION_TOPICS.get(key) ?? [];
      if (!ids.includes(topic.id)) ids.push(topic.id);
      QUESTION_TOPICS.set(key, ids);
    }
  }
}

// Technology's Section A and Section B/C booklets both restart their printed
// numbering. The compact factual references carry the exact SEC booklet id;
// register it as the primary lookup (for both official language editions) so
// a Section B card can never be attached to the Section A document.
for (const reference of technologyPartReferences) {
  if (!reference.fileid) continue;
  const fileids = new Set([
    reference.fileid,
    reference.fileid.replace(/EV(?=\.pdf$)/i, 'IV'),
    reference.fileid.replace(/IV(?=\.pdf$)/i, 'EV'),
  ]);
  for (const fileid of fileids) {
    // A small number of StudyClix headings intentionally group two printed
    // short questions (for example "Question 5,6"). The viewer cards remain
    // the independently selectable Q5 and Q6 tasks.
    for (const number of reference.n.split(/\s*,\s*/)) {
      const key = fileQuestionKey(
        reference.subjectId,
        reference.level,
        reference.year,
        // Paper Trail's selectable archive slot represents the published
        // sitting. This also covers the November 2020 paper, whose factual
        // heading is classified as deferred because the summer exam was
        // cancelled, but which is the only official 2020 paper in the slot.
        'main',
        fileid,
        number,
        reference.paperKey,
      );
      FILE_QUESTION_TOPICS.set(
        key,
        [...new Set([...(FILE_QUESTION_TOPICS.get(key) ?? []), reference.topicId])],
      );
    }
  }
}

// The six taxonomies parsed directly in this module also ship an exact,
// answer-sidecar-derived booklet bridge. Keeping this evidence file-scoped
// lets Paper Trail add verified cards without merging same-numbered booklets,
// and avoids deriving card existence from the generated crosswalk itself.
for (const runtime of directQuestionRuntime.subjects) {
  for (const [level, lang, year, paperKey, fileid, n, topicIndexes] of runtime.questionMappings) {
    const topicIds = topicIndexes.map(topicIndex => {
      const topicId = runtime.topicIds[topicIndex];
      if (!topicId) throw new Error(`${runtime.subjectId}: unknown direct-question topic index ${topicIndex}`);
      return topicId;
    });
    FILE_QUESTION_TOPICS.set(
      fileQuestionKey(runtime.subjectId, level, year, 'main', fileid, n, paperKey, lang),
      [...new Set(topicIds)],
    );
  }
}

/**
 * Exact question-level evidence for the large browser-audited subjects. The
 * booklet id is part of the key because split and pilot papers can restart at
 * Q1. Records are emitted only for StudyClix State-exam headings that join
 * unambiguously to a local, answer-anchored SEC card.
 */
const registerBrowserQuestionRuntime = (runtime: BrowserQuestionRuntime) => {
  for (const [
    levelCode,
    langCode,
    year,
    paperKey,
    fileid,
    n,
    topicIndexes,
  ] of runtime.questionMappings) {
    const topicIds = topicIndexes.map(topicIndex => {
      const topicId = runtime.topicIds[topicIndex];
      if (!topicId) {
        throw new Error(`${runtime.subjectId}: unknown exact-question topic index ${topicIndex}`);
      }
      return topicId;
    }).filter(topicId => topicAppliesToExamYear(
      runtime.subjectId,
      TOPICS_BY_ID.get(topicId)!,
      year,
    ));
    if (!topicIds.length) continue;
    FILE_QUESTION_TOPICS.set(
      fileQuestionKey(
        runtime.subjectId,
        browserAuditLevel(levelCode),
        year,
        'main',
        fileid,
        n,
        paperKey,
        langCode === 'e' ? 'ev' : 'iv',
      ),
      [...new Set(topicIds)],
    );
  }
};

registerBrowserQuestionRuntime(englishQuestionRuntime);
registerBrowserQuestionRuntime(geographyQuestionRuntime);
registerBrowserQuestionRuntime(homeEconomicsQuestionRuntime);
registerBrowserQuestionRuntime(mathematicsQuestionRuntime);
registerBrowserQuestionRuntime(physicalEducationQuestionRuntime);

/**
 * These browser-audited subjects entered the exam hierarchy after their
 * canonical SEC-card tag waves. Bridge those frozen tags into the new level-
 * aware browse topics without rewriting the source tags. Replacement-course
 * nodes remain distinct, so outgoing cards cannot leak into future groups.
 */
const registerCanonicalTagBridge = (taxonomy: ExamTopicTaxonomy) => {
  const topicsByCanonicalNode = new Map<string, string[]>();
  for (const topic of taxonomy.topics) {
    for (const curriculumNodeId of topic.curriculumNodeIds) {
      const scopedKey = `${topic.level}|${curriculumNodeId}`;
      const ids = topicsByCanonicalNode.get(scopedKey) ?? [];
      if (!ids.includes(topic.id)) ids.push(topic.id);
      topicsByCanonicalNode.set(scopedKey, ids);
    }
  }

  for (const paper of PAPER_TOPIC_TAGS) {
    if (paper.subjectId !== taxonomy.subjectId) continue;
    for (const question of paper.q) {
      const topicIds = [...new Set(
        [question.primary, question.secondary]
          .filter((id): id is string => Boolean(id))
          .flatMap(id => topicsByCanonicalNode.get(`${paper.level}|${id}`) ?? [])
          .filter(topicId => topicAppliesToExamYear(
            taxonomy.subjectId,
            TOPICS_BY_ID.get(topicId)!,
            paper.year,
          )),
      )];
      if (!topicIds.length) {
        throw new Error(
          `${taxonomy.subjectId}: no audited topic for ${paper.level} ${paper.year} ${paper.paperKey} Q${question.n}`,
        );
      }
      const key = questionKey(
        paper.subjectId,
        paper.level,
        paper.year,
        'main',
        question.n,
        paper.paperKey,
      );
      const exactFileKey = fileQuestionKey(
        paper.subjectId,
        paper.level,
        paper.year,
        'main',
        paper.fileid,
        question.n,
        paper.paperKey,
        paper.lang,
      );
      // Exact StudyClix-to-SEC evidence wins. The canonical bridge exists only
      // to retain valid local cards absent from those reference pages.
      if (FILE_QUESTION_TOPICS.has(exactFileKey)) continue;
      QUESTION_TOPICS.set(key, [...new Set([...(QUESTION_TOPICS.get(key) ?? []), ...topicIds])]);
    }
  }
};

registerCanonicalTagBridge(ENGLISH_TAXONOMY);
registerCanonicalTagBridge(GEOGRAPHY_TAXONOMY);
registerCanonicalTagBridge(HOME_ECONOMICS_TAXONOMY);
registerCanonicalTagBridge(MATHEMATICS_TAXONOMY);
registerCanonicalTagBridge(PHYSICAL_EDUCATION_TAXONOMY);

// History keeps the StudyClix-equivalent Later Modern hierarchy level-aware,
// while this generated join covers every English and Irish SEC card—including
// the local cards that the reference menu omits or classifies incorrectly.
for (const [levelCode, langCode, year, n, topicIndex] of historyRuntime.questionMappings) {
  const topicId = historyRuntime.topics[topicIndex]?.[0];
  if (!topicId) throw new Error(`Unknown History runtime topic index: ${topicIndex}`);
  QUESTION_TOPICS.set(
    questionKey(
      historyRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      year,
      'main',
      n,
      'single',
      langCode === 'e' ? 'ev' : 'iv',
    ),
    [topicId],
  );
}

// Economics uses exact reference joins where available and reviewed canonical
// fallbacks for the 32 entitled SEC questions absent from the reference menu.
// The same logical mapping is emitted for both official language editions.
for (const [levelCode, langCode, year, n, topicIndexes] of economicsRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      economicsRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      year,
      'main',
      n,
      'single',
      langCode === 'e' ? 'ev' : 'iv',
    ),
    topicIndexes.map(topicIndex => {
      const topicId = economicsRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Economics runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// Art must join on the exact booklet as well as the printed number: legacy
// practical components and the Visual Studies paper all restart at Q1. The
// file-aware mapping therefore takes precedence over the generic factual key.
for (const [
  levelCode,
  langCode,
  yearOffset,
  componentCode,
  n,
  topicIndexes,
] of artRuntime.questionMappings) {
  const level = levelCode === 'h' ? 'higher' : 'ordinary';
  const lang = langCode === 'e' ? 'ev' : 'iv';
  FILE_QUESTION_TOPICS.set(
    fileQuestionKey(
      artRuntime.subjectId,
      level,
      yearOffset + 2000,
      'main',
      artFileid(levelCode, langCode, componentCode),
      n,
      'single',
      lang,
    ),
    topicIndexes.map(topicIndex => {
      const topicId = artRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Art runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// Computer Science exposes all 208 English student-facing questions and their
// Irish-language twins. Exact factual joins take precedence; five valid local
// cards absent from the reference pages retain their reviewed curriculum tags.
for (const [levelCode, langCode, year, n, topicIndexes] of computerScienceRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      computerScienceRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      year,
      'main',
      n,
      'single',
      langCode === 'e' ? 'ev' : 'iv',
    ),
    topicIndexes.map(topicIndex => {
      const topicId = computerScienceRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Computer Science runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// Biology's generated join is shared by both official-language editions. Exact
// factual matches take precedence, while 49 real local questions absent from
// the snapshot—including all 34 from 2026—retain reviewed mappings.
for (const [levelCode, yearOffset, n, topicIndexes] of biologyRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      biologyRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      'single',
    ),
    topicIndexes.map(topicIndex => biologyTopicIdentity(topicIndex).id),
  );
}

// Business uses the exact audited joins for both official-language editions.
// Additive ABQ/S2Q/S3Q identities preserve historical cards without colliding
// with the numbered questions in later split-paper formats.
for (const [levelCode, yearOffset, paperKeyCode, n, topicIndexes] of (
  businessRuntime.questionMappings
)) {
  QUESTION_TOPICS.set(
    questionKey(
      businessRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      businessPaperKey(paperKeyCode),
    ),
    topicIndexes.map(topicIndex => businessTopicIdentity(topicIndex).id),
  );
}

// Construction Studies uses the exact audited joins for both official-
// language editions. Twenty-one genuine SEC questions absent from the
// reference menu remain visible through their direct paper-review mappings.
for (const [levelCode, yearOffset, n, topicIndexes] of (
  constructionStudiesRuntime.questionMappings
)) {
  QUESTION_TOPICS.set(
    questionKey(
      constructionStudiesRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      'single',
    ),
    topicIndexes.map(topicIndex => constructionStudiesTopicIdentity(topicIndex).id),
  );
}

// Engineering maps every entitled written-paper question, including all four
// 2026 level/language editions. The outgoing and replacement topic sets can
// both classify historical questions without collapsing their course identity.
for (const [levelCode, yearOffset, n, topicIndexes] of engineeringRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      engineeringRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      'single',
    ),
    topicIndexes.map(topicIndex => engineeringTopicIdentity(topicIndex).id),
  );
}

// Technology maps the complete SEC Section A and Section B/C corpus. Reference
// omissions remain available through reviewed or existing canonical mappings;
// the paper-prefixed B/C card ids prevent collisions with Section A numbers.
for (const [levelCode, yearOffset, n, topicIndexes] of technologyRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      technologyRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      'single',
    ),
    topicIndexes.map(topicIndex => technologyTopicIdentity(topicIndex).id),
  );
}

// Chemistry shares the audited mapping between both official-language
// editions. Exact factual joins cover 342 cards; the 32 reference omissions
// are retained from direct SEC-paper review, including every 2026 task.
for (const [levelCode, yearOffset, n, topicIndexes] of chemistryRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      chemistryRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      'single',
    ),
    topicIndexes.map(topicIndex => chemistryTopicIdentity(topicIndex).id),
  );
}

// Physics shares the audited mapping between both official-language editions.
// Exact factual joins cover 391 logical cards; 41 valid local questions absent
// from the snapshot are retained from direct SEC-paper review.
for (const [levelCode, yearOffset, n, topicIndexes] of physicsRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      physicsRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      'single',
    ),
    topicIndexes.map(topicIndex => physicsTopicIdentity(topicIndex).id),
  );
}

// DCG's generated join covers both official-language editions and keeps the
// separately published A-sheet cards distinct from B1–B3/C1–C5.
for (const [levelCode, langCode, year, paperKeyCode, n, topicIndexes] of (
  designAndCommunicationGraphicsRuntime.questionMappings
)) {
  QUESTION_TOPICS.set(
    questionKey(
      designAndCommunicationGraphicsRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      year,
      'main',
      n,
      dcgPaperKey(paperKeyCode),
      langCode === 'e' ? 'ev' : 'iv',
    ),
    topicIndexes.map(topicIndex => {
      const topicId = designAndCommunicationGraphicsRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown DCG runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// French has two level-specific menus over written and aural cards. The
// generated join is language-aware so the translated legacy editions retain
// their frozen card granularity while bilingual editions remain singular.
for (const [levelCode, langCode, yearOffset, paperKeyCode, n, topicIndexes] of frenchRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      frenchRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      frenchRuntimePaperKey(paperKeyCode),
      langCode === 'e' ? 'ev' : 'iv',
    ),
    topicIndexes.map(topicIndex => {
      const topicId = frenchRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown French runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// German Storage sidecars use several incompatible historic number runs. The
// generated semantic join and matching hosted anchors preserve all legacy card
// identities while keeping reading, grammar, short writing and aural distinct.
for (const [levelCode, langCode, yearOffset, paperKeyCode, n, topicIndexes] of germanRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      germanRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      germanRuntimePaperKey(paperKeyCode),
      langCode === 'e' ? 'ev' : 'iv',
    ),
    topicIndexes.map(topicIndex => {
      const topicId = germanRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown German runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// Music composing, listening, elective and unprepared-test booklets all use
// the historical `single` paper key and restart their printed question runs.
// Decode the generated SEC component into an exact file-id join so Q1 in one
// booklet cannot leak into Q1 in another.
for (const [
  levelCode,
  langCode,
  yearOffset,
  componentCode,
  n,
  topicIndexes,
] of musicRuntime.questionMappings) {
  const level = levelCode === 'h' ? 'higher' : 'ordinary';
  const lang = langCode === 'e' ? 'ev' : 'iv';
  FILE_QUESTION_TOPICS.set(
    fileQuestionKey(
      musicRuntime.subjectId,
      level,
      yearOffset + 2000,
      'main',
      musicFileid(levelCode, langCode, componentCode),
      n,
      'single',
      lang,
    ),
    topicIndexes.map(topicIndex => {
      const topicId = musicRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Music runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// Irish spans three levels and four live paper slots. The generated join is
// authoritative for all 979 local cards, including the frozen reading cards
// and the two preservation-only archive shelves.
for (const [levelCode, langCode, yearOffset, paperKeyCode, n, topicIndexes] of irishRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      irishRuntime.subjectId,
      irishLevel(levelCode),
      yearOffset + 2000,
      'main',
      n,
      irishRuntimePaperKey(paperKeyCode),
      langCode === 'e' ? 'ev' : 'iv',
    ),
    topicIndexes.map(topicIndex => {
      const topicId = irishRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Irish runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// Italian has two level-specific menus over written and aural cards. The
// generated join is language-aware because translated legacy maps sometimes
// use different card granularity for the same printed paper.
for (const [levelCode, langCode, yearOffset, paperKeyCode, n, topicIndexes] of italianRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      italianRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      yearOffset + 2000,
      'main',
      n,
      italianRuntimePaperKey(paperKeyCode),
      langCode === 'e' ? 'ev' : 'iv',
    ),
    topicIndexes.map(topicIndex => {
      const topicId = italianRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Italian runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// Spanish written and aural cards both retain the historical `single` paper
// key, so the exact booklet id is part of the authoritative join. This prevents
// Written Q1 and Aural Q1 from contaminating one another while preserving every
// pre-existing public question identity.
for (const [
  levelCode,
  langCode,
  yearOffset,
  kindCode,
  n,
  topicIndexes,
] of spanishRuntime.questionMappings) {
  const level = levelCode === 'h' ? 'higher' : 'ordinary';
  const lang = langCode === 'e' ? 'ev' : 'iv';
  FILE_QUESTION_TOPICS.set(
    fileQuestionKey(
      spanishRuntime.subjectId,
      level,
      yearOffset + 2000,
      'main',
      spanishFileid(levelCode, langCode, kindCode),
      n,
      'single',
      lang,
    ),
    topicIndexes.map(topicIndex => {
      const topicId = spanishRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Spanish runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// Japanese uses a single common browse taxonomy over level- and
// language-specific SEC cards. The generated crosswalk is the authoritative
// join; it preserves all 1,329 existing local card identities and gives exact
// reference matches precedence over canonical-tag fallbacks.
for (const [levelCode, langCode, year, paperKeyCode, n, topicIndexes] of japaneseRuntime.questionMappings) {
  const topicIds = topicIndexes.map(topicIndex => {
    const topic = japaneseAudit.levels.common.topics[topicIndex];
    if (!topic) throw new Error(`Unknown Japanese runtime topic index: ${topicIndex}`);
    return topic.id;
  });
  QUESTION_TOPICS.set(
    questionKey(
      japaneseAudit.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      year,
      'main',
      n,
      japaneseRuntimePaperKey(paperKeyCode),
      langCode === 'e' ? 'ev' : 'iv',
    ),
    topicIds,
  );
}

// Physics & Chemistry uses one shared browse taxonomy over exact level- and
// language-specific SEC cards. The generated crosswalk owns this join so the
// 28-topic menu can never erase a retained Ordinary, translated or newer card.
for (const [levelCode, langCode, year, n, topicIndexes] of physicsAndChemistryRuntime.questionMappings) {
  QUESTION_TOPICS.set(
    questionKey(
      physicsAndChemistryRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      year,
      'main',
      n,
      'single',
      langCode === 'e' ? 'ev' : 'iv',
    ),
    topicIndexes.map(topicIndex => {
      const topicId = physicsAndChemistryRuntime.topics[topicIndex]?.[0];
      if (!topicId) throw new Error(`Unknown Physics & Chemistry runtime topic index: ${topicIndex}`);
      return topicId;
    }),
  );
}

// Religious Education joins every paper edition to exactly one level-specific
// syllabus-section bucket. Hosted paper-only anchors use the same generated
// section-card numbering, so even legacy sidecar omissions remain accessible.
for (const [levelCode, langCode, year, n, topicIndex] of religiousEducationRuntime.questionMappings) {
  const topicId = religiousEducationRuntime.topics[topicIndex]?.[0];
  if (!topicId) throw new Error(`Unknown Religious Education runtime topic index: ${topicIndex}`);
  QUESTION_TOPICS.set(
    questionKey(
      religiousEducationRuntime.subjectId,
      levelCode === 'h' ? 'higher' : 'ordinary',
      year,
      'main',
      n,
      'single',
      langCode === 'e' ? 'ev' : 'iv',
    ),
    [topicId],
  );
}

/**
 * Verified local questions omitted from the reference site's topic pages.
 * Retaining these explicit exceptions is safer than silently making a valid
 * SEC question disappear merely to make two headline counts agree.
 */
const RETAINED_LOCAL_ASSOCIATIONS: Array<{
  subjectId: string;
  level: PaperLevel;
  year: number;
  sitting: ExamSitting;
  paperKey?: string;
  /** Only needed where translated answer-map anchors are not structurally aligned. */
  lang?: PaperLang;
  n: string;
  topicIds: string[];
  reason?: string;
}> = [
  {
    subjectId: 'accounting',
    level: 'higher',
    year: 2017,
    sitting: 'main',
    n: '4',
    // The paper itself titles this "Departmental Final Accounts of a Sole
    // Trader". Higher has no separate Departmental bucket in the reference.
    topicIds: ['accounting-higher-final-accounts-sole-trader'],
  },
  {
    subjectId: 'accounting',
    level: 'ordinary',
    year: 2017,
    sitting: 'main',
    n: '5',
    topicIds: ['accounting-ordinary-interpretation-of-accounts'],
  },
];

/**
 * The reference pages omit 113 valid 2010–2022 questions from the former
 * Applied Mathematics course. Map only those omissions through their existing,
 * frozen canonical tags. This keeps the exact current reference menu while
 * retaining every local question; it never overwrites a reference association.
 */
const appliedTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of APPLIED_MATHEMATICS_TAXONOMY.topics) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const scopedKey = `${topic.level}|${curriculumNodeId}`;
    const ids = appliedTopicsByCanonicalNode.get(scopedKey) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    appliedTopicsByCanonicalNode.set(scopedKey, ids);
  }
}

const agriculturalTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of AGRICULTURAL_SCIENCE_TAXONOMY.topics) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const scopedKey = `${topic.level}|${curriculumNodeId}`;
    const ids = agriculturalTopicsByCanonicalNode.get(scopedKey) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    agriculturalTopicsByCanonicalNode.set(scopedKey, ids);
  }
}

const linkModuleContentTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of LINK_MODULES_TAXONOMY.topics.filter(topic =>
  !topic.id.endsWith('-audio-visual') && !topic.id.endsWith('-case-study'))) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const ids = linkModuleContentTopicsByCanonicalNode.get(curriculumNodeId) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    linkModuleContentTopicsByCanonicalNode.set(curriculumNodeId, ids);
  }
}

for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'applied-mathematics') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const topicIds = [...new Set(
      [question.primary, question.secondary]
        .filter((id): id is string => Boolean(id))
        .flatMap(id => appliedTopicsByCanonicalNode.get(`${paper.level}|${id}`) ?? []),
    )];
    if (!topicIds.length) continue;
    QUESTION_TOPICS.set(key, topicIds);
    if (!RETAINED_LOCAL_ASSOCIATIONS.some(item =>
      item.subjectId === paper.subjectId
      && item.level === paper.level
      && item.year === paper.year
      && item.sitting === 'main'
      && item.n === question.n)) {
      RETAINED_LOCAL_ASSOCIATIONS.push({
        subjectId: paper.subjectId,
        level: paper.level,
        year: paper.year,
        sitting: 'main',
        n: question.n,
        topicIds,
        reason: 'Valid local question omitted from the reference topic pages; retained via its verified canonical tag.',
      });
    }
  }
}

for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'agricultural-science') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const topicIds = [...new Set(
      [question.primary, question.secondary]
        .filter((id): id is string => Boolean(id))
        .flatMap(id => agriculturalTopicsByCanonicalNode.get(`${paper.level}|${id}`) ?? []),
    )];
    if (!topicIds.length) continue;
    QUESTION_TOPICS.set(key, topicIds);
    if (!RETAINED_LOCAL_ASSOCIATIONS.some(item =>
      item.subjectId === paper.subjectId
      && item.level === paper.level
      && item.year === paper.year
      && item.sitting === 'main'
      && item.n === question.n)) {
      RETAINED_LOCAL_ASSOCIATIONS.push({
        subjectId: paper.subjectId,
        level: paper.level,
        year: paper.year,
        sitting: 'main',
        n: question.n,
        topicIds,
        reason: 'Valid local question omitted from the reference topic pages; retained via its verified canonical tag.',
      });
    }
  }
}

// The 2021 Higher Q4 anchor predates the committed canonical tag wave and is
// also absent from the reference pages. Its official stem is about farm energy
// efficiency and environmental sustainability, so retain it explicitly in the
// environment bucket rather than allowing it to disappear from Topic Atlas.
if (!QUESTION_TOPICS.has(questionKey('agricultural-science', 'higher', 2021, 'main', '4'))) {
  RETAINED_LOCAL_ASSOCIATIONS.push({
    subjectId: 'agricultural-science',
    level: 'higher',
    year: 2021,
    sitting: 'main',
    n: '4',
    topicIds: ['agricultural-science-higher-fertilisers-pollution-environment-cycles'],
    reason: 'Valid local question omitted from both the reference topic pages and the earlier tag wave; retained from its official SEC stem.',
  });
}

for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'link-modules') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const number = Number(question.n);
    const topicIds = number <= 8
      ? ['link-modules-common-audio-visual']
      : number <= 11
        ? ['link-modules-common-case-study']
        : [...new Set(
          [question.primary, question.secondary]
            .filter((id): id is string => Boolean(id))
            .flatMap(id => linkModuleContentTopicsByCanonicalNode.get(id) ?? []),
        )];
    if (!topicIds.length) continue;
    QUESTION_TOPICS.set(key, topicIds);
    if (!RETAINED_LOCAL_ASSOCIATIONS.some(item =>
      item.subjectId === paper.subjectId
      && item.year === paper.year
      && item.n === question.n)) {
      RETAINED_LOCAL_ASSOCIATIONS.push({
        subjectId: paper.subjectId,
        level: paper.level,
        year: paper.year,
        sitting: 'main',
        n: question.n,
        topicIds,
        reason: 'Valid local question omitted from the reference topic pages; retained by assessment section and verified canonical tag.',
      });
    }
  }
}

const classicalTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of CLASSICAL_STUDIES_TAXONOMY.topics) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const scopedKey = `${topic.level}|${curriculumNodeId}`;
    const ids = classicalTopicsByCanonicalNode.get(scopedKey) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    classicalTopicsByCanonicalNode.set(scopedKey, ids);
  }
}

for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'classical-studies') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const topicIds = [...new Set(
      [question.primary, question.secondary]
        .filter((id): id is string => Boolean(id))
        .flatMap(id => classicalTopicsByCanonicalNode.get(`${paper.level}|${id}`) ?? []),
    )];
    if (!topicIds.length) continue;
    RETAINED_LOCAL_ASSOCIATIONS.push({
      subjectId: paper.subjectId,
      level: paper.level,
      year: paper.year,
      sitting: 'main',
      n: question.n,
      topicIds,
      reason: 'Valid local question omitted from the reference topic pages; retained via its verified canonical tag.',
    });
  }
}

const classicalTopicIds = (
  level: 'higher' | 'ordinary',
  slugs: string[],
) => slugs.map(slug => `classical-studies-${level}-${slug}`);

// The reference retains useful fragments of the retired ten-topic course but
// omits whole valid questions when their former topic has no exact modern
// equivalent. Keep the eight-bucket menu intact and conservatively cross-list
// those questions in the closest surviving practice buckets.
const CLASSICAL_LEGACY_FALLBACKS: Record<string, string[]> = {
  '1': ['power-and-identity'],
  '2': ['power-and-identity'],
  '3': ['power-and-identity', 'philosophy'],
  '4': ['power-and-identity'],
  '5': ['greek-drama'],
  '6': ['world-of-heroes'],
  '7': ['philosophy', 'world-of-heroes'],
  '8': ['temples', 'funerary-practices', 'mythology'],
  '9': ['philosophy'],
  '10': ['temples', 'roman-spectacle', 'funerary-practices'],
};

for (const level of classicalStudiesLevels) {
  for (let year = 2010; year <= 2022; year++) {
    if (level === 'ordinary' && year === 2020) continue;
    for (let n = 1; n <= 10; n++) {
      const number = String(n);
      const key = questionKey('classical-studies', level, year, 'main', number);
      if (QUESTION_TOPICS.has(key)) continue;
      RETAINED_LOCAL_ASSOCIATIONS.push({
        subjectId: 'classical-studies',
        level,
        year,
        sitting: 'main',
        n: number,
        topicIds: classicalTopicIds(level, CLASSICAL_LEGACY_FALLBACKS[number]),
        reason: 'Valid retired-course question omitted from the reference topic pages; retained in the closest surviving exam buckets from its official course topic.',
      });
    }
  }
}

const CLASSICAL_2026_TOPICS: Record<'higher' | 'ordinary', Record<string, string[]>> = {
  higher: {
    '1': ['temples'],
    '2': ['temples'],
    '3': ['mythology'],
    '4': ['world-of-heroes'],
    '5': ['greek-drama'],
    '6': ['greek-drama'],
    '7': ['power-and-identity'],
    '8': ['power-and-identity'],
    '9': ['funerary-practices'],
    '10': ['philosophy'],
    '11': ['world-of-heroes'],
    '12': ['philosophy'],
    '13': ['greek-drama'],
    '14': ['power-and-identity'],
    '15': ['temples'],
    '16': ['roman-spectacle'],
  },
  ordinary: {
    '1': ['mythology'],
    '2': ['world-of-heroes'],
    '3': ['temples'],
    '4': ['funerary-practices'],
    '5': ['philosophy'],
    '6': ['greek-drama'],
    '7': ['roman-spectacle'],
    '8': ['roman-spectacle'],
    '9': ['power-and-identity'],
    '10': ['power-and-identity'],
    '11': ['world-of-heroes'],
    '12': ['power-and-identity'],
    '13': ['temples'],
    '14': ['greek-drama'],
    '15': ['philosophy'],
    '16': ['funerary-practices'],
  },
};

for (const level of classicalStudiesLevels) {
  for (const [n, slugs] of Object.entries(CLASSICAL_2026_TOPICS[level])) {
    RETAINED_LOCAL_ASSOCIATIONS.push({
      subjectId: 'classical-studies',
      level,
      year: 2026,
      sitting: 'main',
      n,
      topicIds: classicalTopicIds(level, slugs),
      reason: 'Official 2026 SEC question published after the captured reference topic pages; retained from direct paper inspection.',
    });
  }
}

const politicsTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of POLITICS_AND_SOCIETY_TAXONOMY.topics.filter(topic =>
  !topic.id.endsWith('-data-based-questions'))) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const scopedKey = `${topic.level}|${curriculumNodeId}`;
    const ids = politicsTopicsByCanonicalNode.get(scopedKey) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    politicsTopicsByCanonicalNode.set(scopedKey, ids);
  }
}

// The reference menu omits Higher 2018 Q4. Retain it from the existing
// hand-verified canonical tag instead of sacrificing a valid SEC card for
// headline parity.
for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'politics-and-society') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const topicIds = [...new Set(
      [question.primary, question.secondary]
        .filter((id): id is string => Boolean(id))
        .flatMap(id => politicsTopicsByCanonicalNode.get(`${paper.level}|${id}`) ?? []),
    )];
    if (!topicIds.length) continue;
    RETAINED_LOCAL_ASSOCIATIONS.push({
      subjectId: paper.subjectId,
      level: paper.level,
      year: paper.year,
      sitting: 'main',
      n: question.n,
      topicIds,
      reason: 'Valid local question omitted from the reference topic pages; retained via its verified canonical tag.',
    });
  }
}

// The reference has no 2024 Higher data-based heading even though the SEC
// paper and our verified answer map both contain Q2. The documents concern
// women in Irish political representation and gender quotas, so preserve the
// assessment-format bucket plus the two directly relevant content themes.
if (!QUESTION_TOPICS.has(questionKey('politics-and-society', 'higher', 2024, 'main', '2'))) {
  RETAINED_LOCAL_ASSOCIATIONS.push({
    subjectId: 'politics-and-society',
    level: 'higher',
    year: 2024,
    sitting: 'main',
    n: '2',
    topicIds: [
      'politics-and-society-higher-data-based-questions',
      'politics-and-society-higher-1-power-and-decision-making-at-national-and-european-level',
      'politics-and-society-higher-3-human-rights-and-responsibilities-in-ireland',
    ],
    reason: 'Valid local data-based question omitted from the reference topic pages; retained from direct inspection of the official SEC paper.',
  });
}

for (const association of RETAINED_LOCAL_ASSOCIATIONS) {
  QUESTION_TOPICS.set(
    questionKey(
      association.subjectId,
      association.level,
      association.year,
      association.sitting,
      association.n,
      association.paperKey,
      association.lang,
    ),
    association.topicIds,
  );
}

export function examTopicTaxonomyFor(subjectId: string): ExamTopicTaxonomy | null {
  return TAXONOMIES.get(subjectId) ?? null;
}

export function examTopicDefinition(topicId: string): ExamTopicDefinition | null {
  return TOPICS_BY_ID.get(topicId) ?? null;
}

export function examTopicLabel(topicId: string): string | null {
  return TOPICS_BY_ID.get(topicId)?.label ?? null;
}

export function examTopicIdsForQuestion(
  subjectId: string,
  level: PaperLevel,
  year: number,
  sitting: ExamSitting,
  n: string,
  paperKey = 'single',
  lang?: PaperLang,
  fileid?: string,
): string[] {
  if (fileid) {
    const fileShared = FILE_QUESTION_TOPICS.get(fileQuestionKey(
      subjectId,
      level,
      year,
      sitting,
      fileid,
      n,
      paperKey,
    )) ?? [];
    const fileLocalised = lang
      ? FILE_QUESTION_TOPICS.get(fileQuestionKey(
        subjectId,
        level,
        year,
        sitting,
        fileid,
        n,
        paperKey,
        lang,
      )) ?? []
      : [];
    const exact = [...new Set([...fileShared, ...fileLocalised])];
    if (exact.length) return exact;
  }
  const shared = QUESTION_TOPICS.get(questionKey(subjectId, level, year, sitting, n, paperKey)) ?? [];
  const localised = lang
    ? QUESTION_TOPICS.get(questionKey(subjectId, level, year, sitting, n, paperKey, lang)) ?? []
    : [];
  return [...new Set([...shared, ...localised])];
}

export function curriculumNodeIdsForExamTopic(topicId: string): string[] {
  return [...(TOPICS_BY_ID.get(topicId)?.curriculumNodeIds ?? [])];
}

/** Part-aware factual references retained for card-level Mark Bank mapping. */
export function examQuestionPartReferencesForSubject(subjectId: string): ExamQuestionPartReference[] {
  return [
    ...appliedMathematicsPartReferences,
    ...agriculturalSciencePartReferences,
    ...artPartReferences,
    ...biologyPartReferences,
    ...businessPartReferences,
    ...chemistryPartReferences,
    ...classicalStudiesPartReferences,
    ...computerSciencePartReferences,
    ...constructionStudiesPartReferences,
    ...designAndCommunicationGraphicsPartReferences,
    ...economicsPartReferences,
    ...engineeringPartReferences,
    ...frenchPartReferences,
    ...germanPartReferences,
    ...historyPartReferences,
    ...irishPartReferences,
    ...italianPartReferences,
    ...japanesePartReferences,
    ...linkModulesPartReferences,
    ...musicPartReferences,
    ...physicsPartReferences,
    ...physicsAndChemistryPartReferences,
    ...politicsAndSocietyPartReferences,
    ...religiousEducationPartReferences,
    ...spanishPartReferences,
    ...technologyPartReferences,
  ]
    .filter(reference => reference.subjectId === subjectId)
    .map(reference => ({ ...reference }));
}

export interface ExamQuestionTopicMapping {
  subjectId: string;
  level: PaperLevel;
  year: number;
  sitting: ExamSitting;
  paperKey: string;
  lang: PaperLang | 'any';
  fileid?: string;
  n: string;
  topicIds: string[];
}

/** All audited question associations for a subject, newest first. */
export function examQuestionTopicMappingsForSubject(subjectId: string): ExamQuestionTopicMapping[] {
  const prefix = `${subjectId}|`;
  const mappings: ExamQuestionTopicMapping[] = [];
  for (const [key, topicIds] of QUESTION_TOPICS) {
    if (!key.startsWith(prefix)) continue;
    const [, level, year, sitting, paperKey, lang, n] = key.split('|');
    mappings.push({
      subjectId,
      level: level as PaperLevel,
      year: Number(year),
      sitting: sitting as ExamSitting,
      paperKey,
      lang: lang as PaperLang | 'any',
      n,
      topicIds: [...topicIds],
    });
  }
  for (const [key, topicIds] of FILE_QUESTION_TOPICS) {
    if (!key.startsWith(prefix)) continue;
    const [, level, year, sitting, paperKey, lang, fileid, n] = key.split('|');
    mappings.push({
      subjectId,
      level: level as PaperLevel,
      year: Number(year),
      sitting: sitting as ExamSitting,
      paperKey,
      lang: lang as PaperLang | 'any',
      fileid,
      n,
      topicIds: [...topicIds],
    });
  }
  return mappings.sort((a, b) =>
    b.year - a.year
    || a.level.localeCompare(b.level)
    || Number(Boolean(b.fileid)) - Number(Boolean(a.fileid))
    || (a.fileid ?? '').localeCompare(b.fileid ?? '')
    || Number(a.n) - Number(b.n));
}

/** Canonical syllabus nodes touched by an audited exam question. */
export function curriculumNodeIdsForExamQuestion(
  subjectId: string,
  level: PaperLevel,
  year: number,
  sitting: ExamSitting,
  n: string,
  paperKey = 'single',
  lang?: PaperLang,
  fileid?: string,
): string[] {
  const ids = examTopicIdsForQuestion(subjectId, level, year, sitting, n, paperKey, lang, fileid)
    .flatMap(topicId => curriculumNodeIdsForExamTopic(topicId));
  return [...new Set(ids)];
}

export const retainedLocalExamTopicAssociations = RETAINED_LOCAL_ASSOCIATIONS;
