/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The exam-topic overlay must remain complete and non-destructive.  StudyClix
 * is a reference for browse metadata only; official curriculum ids continue to
 * resolve locally and every existing NextStepUni question remains reachable.
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import accountingQuestionBaselineJson from './fixtures/accountingTopicQuestionBaseline.json';
import { topicsForPaper } from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
  retainedLocalExamTopicAssociations,
} from '../data/examTopics/registry';

const higherLabels = [
  'Budgeting - Cash',
  'Budgeting - Flexible',
  'Budgeting - Production',
  'Cash Flow Statements',
  'Club Accounts',
  'Control Accounts',
  'Correction of Errors/Suspense',
  'Costing - Job, Product, Stock Valuation & O/H Apportionment',
  'Costing - Marginal',
  'Depreciation of Fixed Assets',
  'Farm Accounts',
  'Final Accounts - Company',
  'Final Accounts - Manufacturing',
  'Final Accounts - Sole Trader',
  'Fixed Assets Valuation',
  'Incomplete Records A',
  'Incomplete Records B',
  'Interpretation of Accounts',
  'Published Accounts',
  'Revaluation of Fixed Assets',
  'Service Firms',
  'Tabular Statements',
];

const ordinaryLabels = [
  'Bank Reconciliation Statement',
  'Budgeting - Cash',
  'Budgeting - Production',
  'Cash Flow Statements',
  'Club Accounts',
  'Company Profit & Loss',
  'Control Accounts',
  'Correction of Errors/Suspense',
  'Costing - Absorption',
  'Costing - Marginal',
  'Farm Accounts',
  'Final Accounts - Company',
  'Final Accounts - Departmental',
  'Final Accounts - Manufacturing',
  'Final Accounts - Sole Trader',
  'Fixed Assets - Depreciation & Revaluation',
  'Incomplete Records - Control Account',
  'Incomplete Records - Net Worth',
  'Interpretation of Accounts',
  'Service Firms',
  'Tabular Statements',
];

describe('Accounting exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('accounting')!;
  const accountingQuestionBaseline = accountingQuestionBaselineJson as Array<{
    level: 'higher' | 'ordinary';
    lang: 'ev' | 'iv';
    year: number;
    fileid: string;
    questions: string[];
  }>;

  it('pins the audited, level-aware topic structure', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => group.label)).toEqual(['Higher Level', 'Ordinary Level']);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label)).toEqual(higherLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label)).toEqual(ordinaryLabels);
    expect(new Set(taxonomy.topics.map(topic => topic.id)).size).toBe(43);
  });

  it('crosswalks every exam topic to real canonical curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM.flatMap(subject => subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id))),
    );
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids.length, `${topic.id} has no curriculum crosswalk`).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned curriculum ids`).toEqual([]);
    }
  });

  it('covers every main-paper Accounting question in the local 2010–2026 corpus', () => {
    for (const level of ['higher', 'ordinary'] as const) {
      for (let year = 2010; year <= 2026; year++) {
        for (let number = 1; number <= 9; number++) {
          expect(
            examTopicIdsForQuestion('accounting', level, year, 'main', String(number)),
            `${level}|${year}|Q${number}`,
          ).not.toEqual([]);
        }
      }
    }
  });

  it('keeps every already-tagged Accounting question reachable through the new browse taxonomy', () => {
    for (const paper of PAPER_TOPIC_TAGS.filter(item => item.subjectId === 'accounting')) {
      for (const question of paper.q) {
        expect(
          examTopicIdsForQuestion('accounting', paper.level, paper.year, 'main', question.n),
          `${paper.level}|${paper.year}|${paper.lang}|${question.n}`,
        ).not.toEqual([]);
      }
    }
  });

  it('preserves every exact pre-migration Accounting paper/question identity', () => {
    for (const baseline of accountingQuestionBaseline) {
      const live = topicsForPaper(
        'accounting',
        baseline.year,
        baseline.level,
        baseline.lang,
        baseline.fileid,
      );
      expect(live, `${baseline.level}|${baseline.lang}|${baseline.year}|${baseline.fileid}`).not.toBeNull();
      const liveNumbers = new Set(live!.q.map(question => question.n));
      for (const number of baseline.questions) {
        expect(liveNumbers.has(number), `${baseline.level}|${baseline.lang}|${baseline.year}|Q${number}`).toBe(true);
      }
    }
  });

  it('records reference omissions as explicit preservation exceptions', () => {
    expect(retainedLocalExamTopicAssociations
      .filter(item => item.subjectId === 'accounting')
      .map(item => `${item.level}|${item.year}|${item.n}`)).toEqual([
      'higher|2017|4',
      'ordinary|2017|5',
    ]);
  });

  it('stores no commercial mock question content', () => {
    for (const topic of taxonomy.topics) {
      expect(topic.mockQuestionCount).toBeGreaterThanOrEqual(0);
      expect(Object.keys(topic).sort()).toEqual([
        'curriculumNodeIds',
        'id',
        'label',
        'level',
        'mockQuestionCount',
        'officialQuestionKeys',
        'sourcePath',
      ]);
    }
  });
});
