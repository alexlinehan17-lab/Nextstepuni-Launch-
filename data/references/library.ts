/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';

// ─── Shared verified-reference library ──────────────────────────────────────
//
// Every entry's DOI has been confirmed to resolve via CrossRef. This is the
// single source of truth for citation metadata across all accredited modules —
// per-module files (data/references/<module>.ts) compose ordered lists from
// these. NEVER add an entry whose DOI has not been verified against CrossRef.
//
// `satisfies` keeps each value strongly typed as a Reference while preserving
// the literal keys for autocomplete.
export const REF = {
  // Retrieval practice / testing effect
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

  // Learning vs performance / desirable difficulties
  sb2015: {
    id: 'sb2015',
    authors: 'Soderstrom, N. C., & Bjork, R. A.',
    year: 2015,
    title: 'Learning versus performance: An integrative review',
    source: 'Perspectives on Psychological Science',
    doi: '10.1177/1745691615569000',
  },

  // Forgetting curve / spacing
  murre2015: {
    id: 'murre2015',
    authors: 'Murre, J. M. J., & Dros, J.',
    year: 2015,
    title: "Replication and analysis of Ebbinghaus' forgetting curve",
    source: 'PLOS ONE',
    doi: '10.1371/journal.pone.0120644',
  },
  cepeda2006: {
    id: 'cepeda2006',
    authors: 'Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D.',
    year: 2006,
    title: 'Distributed practice in verbal recall tasks: A review and quantitative synthesis',
    source: 'Psychological Bulletin',
    doi: '10.1037/0033-2909.132.3.354',
  },
  cepeda2008: {
    id: 'cepeda2008',
    authors: 'Cepeda, N. J., Vul, E., Rohrer, D., Wixted, J. T., & Pashler, H.',
    year: 2008,
    title: 'Spacing effects in learning: A temporal ridgeline of optimal retention',
    source: 'Psychological Science',
    doi: '10.1111/j.1467-9280.2008.02209.x',
  },
} satisfies Record<string, Reference>;
