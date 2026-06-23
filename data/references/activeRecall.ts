/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';

// ─── Mastering Active Recall — verified reference set ────────────────────────
//
// Every DOI below was confirmed to resolve via CrossRef during the
// pre-accreditation review (2026-06). The per-claim verification record and any
// reframed/cut content are documented in compliance/evidence/active-recall.md.

const REFERENCES = {
  rk2006: {
    id: 'rk2006',
    authors: 'Roediger, H. L., & Karpicke, J. D.',
    year: 2006,
    title: 'Test-enhanced learning: Taking memory tests improves long-term retention',
    source: 'Psychological Science',
    doi: '10.1111/j.1467-9280.2006.01693.x',
  },
  kr2008: {
    id: 'kr2008',
    authors: 'Karpicke, J. D., & Roediger, H. L.',
    year: 2008,
    title: 'The critical importance of retrieval for learning',
    source: 'Science',
    doi: '10.1126/science.1152408',
  },
  sb2015: {
    id: 'sb2015',
    authors: 'Soderstrom, N. C., & Bjork, R. A.',
    year: 2015,
    title: 'Learning versus performance: An integrative review',
    source: 'Perspectives on Psychological Science',
    doi: '10.1177/1745691615569000',
  },
  butler2010: {
    id: 'butler2010',
    authors: 'Butler, A. C.',
    year: 2010,
    title: 'Repeated testing produces superior transfer of learning relative to repeated studying',
    source: 'Journal of Experimental Psychology: Learning, Memory, and Cognition',
    doi: '10.1037/a0019902',
  },
  kb2011: {
    id: 'kb2011',
    authors: 'Karpicke, J. D., & Blunt, J. R.',
    year: 2011,
    title: 'Retrieval practice produces more learning than elaborative studying with concept mapping',
    source: 'Science',
    doi: '10.1126/science.1199327',
  },
  agarwal2014: {
    id: 'agarwal2014',
    authors: "Agarwal, P. K., D'Antonio, L., Roediger, H. L., McDermott, K. B., & McDaniel, M. A.",
    year: 2014,
    title: "Classroom-based programs of retrieval practice reduce middle school and high school students' test anxiety",
    source: 'Journal of Applied Research in Memory and Cognition',
    doi: '10.1016/j.jarmac.2014.07.002',
  },
} satisfies Record<string, Reference>;

export const ACTIVE_RECALL_REFERENCES = REFERENCES;

// Per-section reference lists. The order here defines the superscript numbering
// shown in each section (the <Cite n={…}/> markers map to this order).
export const AR_SECTION_REFS: Record<string, Reference[]> = {
  s1: [REFERENCES.rk2006],
  s2: [REFERENCES.rk2006, REFERENCES.sb2015],
  s3: [REFERENCES.kr2008],
  s4: [REFERENCES.butler2010, REFERENCES.kb2011],
  s5: [REFERENCES.agarwal2014],
  s6: [REFERENCES.sb2015],
};
