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

  // Interleaving
  rohrer2007: {
    id: 'rohrer2007',
    authors: 'Rohrer, D., & Taylor, K.',
    year: 2007,
    title: 'The shuffling of mathematics problems improves learning',
    source: 'Instructional Science',
    doi: '10.1007/s11251-007-9015-8',
  },
  rohrer2015: {
    id: 'rohrer2015',
    authors: 'Rohrer, D., Dedrick, R. F., & Stershic, S.',
    year: 2015,
    title: 'Interleaved practice improves mathematics learning',
    source: 'Journal of Educational Psychology',
    doi: '10.1037/edu0000001',
  },
  kornell2008: {
    id: 'kornell2008',
    authors: 'Kornell, N., & Bjork, R. A.',
    year: 2008,
    title: 'Learning concepts and categories: Is spacing the enemy of induction?',
    source: 'Psychological Science',
    doi: '10.1111/j.1467-9280.2008.02127.x',
  },

  // Metacognition / illusions of competence; technique reviews
  koriat2005: {
    id: 'koriat2005',
    authors: 'Koriat, A., & Bjork, R. A.',
    year: 2005,
    title: "Illusions of competence in monitoring one's knowledge during study",
    source: 'Journal of Experimental Psychology: Learning, Memory, and Cognition',
    doi: '10.1037/0278-7393.31.2.187',
  },
  dunlosky2013: {
    id: 'dunlosky2013',
    authors: 'Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T.',
    year: 2013,
    title: "Improving students' learning with effective learning techniques: Promising directions from cognitive and educational psychology",
    source: 'Psychological Science in the Public Interest',
    doi: '10.1177/1529100612453266',
  },

  // Deliberate practice, feedback, error learning, cognitive load, self-explanation
  ericsson1993: {
    id: 'ericsson1993',
    authors: 'Ericsson, K. A., Krampe, R. T., & Tesch-Römer, C.',
    year: 1993,
    title: 'The role of deliberate practice in the acquisition of expert performance',
    source: 'Psychological Review',
    doi: '10.1037/0033-295x.100.3.363',
  },
  hattie2007: {
    id: 'hattie2007',
    authors: 'Hattie, J., & Timperley, H.',
    year: 2007,
    title: 'The power of feedback',
    source: 'Review of Educational Research',
    doi: '10.3102/003465430298487',
  },
  metcalfe2017: {
    id: 'metcalfe2017',
    authors: 'Metcalfe, J.',
    year: 2017,
    title: 'Learning from errors',
    source: 'Annual Review of Psychology',
    doi: '10.1146/annurev-psych-010416-044022',
  },
  sweller1988: {
    id: 'sweller1988',
    authors: 'Sweller, J.',
    year: 1988,
    title: 'Cognitive load during problem solving: Effects on learning',
    source: 'Cognitive Science',
    doi: '10.1207/s15516709cog1202_4',
  },
  chi1989: {
    id: 'chi1989',
    authors: 'Chi, M. T. H., Bassok, M., Lewis, M. W., Reimann, P., & Glaser, R.',
    year: 1989,
    title: 'Self-explanations: How students study and use examples in learning to solve problems',
    source: 'Cognitive Science',
    doi: '10.1016/0364-0213(89)90002-5',
  },

  // Memory architecture (stores, capacity, consolidation)
  atkinson1968: {
    id: 'atkinson1968',
    authors: 'Atkinson, R. C., & Shiffrin, R. M.',
    year: 1968,
    title: 'Human memory: A proposed system and its control processes',
    source: 'Psychology of Learning and Motivation',
    doi: '10.1016/S0079-7421(08)60422-3',
  },
  miller1956: {
    id: 'miller1956',
    authors: 'Miller, G. A.',
    year: 1956,
    title: 'The magical number seven, plus or minus two: Some limits on our capacity for processing information',
    source: 'Psychological Review',
    doi: '10.1037/h0043158',
  },
  cowan2001: {
    id: 'cowan2001',
    authors: 'Cowan, N.',
    year: 2001,
    title: 'The magical number 4 in short-term memory: A reconsideration of mental storage capacity',
    source: 'Behavioral and Brain Sciences',
    doi: '10.1017/s0140525x01003922',
  },
  peterson1959: {
    id: 'peterson1959',
    authors: 'Peterson, L. R., & Peterson, M. J.',
    year: 1959,
    title: 'Short-term retention of individual verbal items',
    source: 'Journal of Experimental Psychology',
    doi: '10.1037/h0049234',
  },
  squire2004: {
    id: 'squire2004',
    authors: 'Squire, L. R.',
    year: 2004,
    title: 'Memory systems of the brain: A brief history and current perspective',
    source: 'Neurobiology of Learning and Memory',
    doi: '10.1016/j.nlm.2004.06.005',
  },
  craik1972: {
    id: 'craik1972',
    authors: 'Craik, F. I. M., & Lockhart, R. S.',
    year: 1972,
    title: 'Levels of processing: A framework for memory research',
    source: 'Journal of Verbal Learning and Verbal Behavior',
    doi: '10.1016/s0022-5371(72)80001-x',
  },
  diekelmann2010: {
    id: 'diekelmann2010',
    authors: 'Diekelmann, S., & Born, J.',
    year: 2010,
    title: 'The memory function of sleep',
    source: 'Nature Reviews Neuroscience',
    doi: '10.1038/nrn2762',
  },
  lupien2009: {
    id: 'lupien2009',
    authors: 'Lupien, S. J., McEwen, B. S., Gunnar, M. R., & Heim, C.',
    year: 2009,
    title: 'Effects of stress throughout the lifespan on the brain, behaviour and cognition',
    source: 'Nature Reviews Neuroscience',
    doi: '10.1038/nrn2639',
  },

  // Elaborative interrogation / elaboration
  stein1979: {
    id: 'stein1979',
    authors: 'Stein, B. S., & Bransford, J. D.',
    year: 1979,
    title: 'Constraints on effective elaboration: Effects of precision and subject generation',
    source: 'Journal of Verbal Learning and Verbal Behavior',
    doi: '10.1016/s0022-5371(79)90481-x',
  },
  pressley1987: {
    id: 'pressley1987',
    authors: 'Pressley, M., McDaniel, M. A., Turnure, J. E., Wood, E., & Ahmad, M.',
    year: 1987,
    title: 'Generation and precision of elaboration: Effects on intentional and incidental learning',
    source: 'Journal of Experimental Psychology: Learning, Memory, and Cognition',
    doi: '10.1037/0278-7393.13.2.291',
  },

  // Cognitive endurance: brain energy, stress, sleep, performance
  raichle2002: {
    id: 'raichle2002',
    authors: 'Raichle, M. E., & Gusnard, D. A.',
    year: 2002,
    title: "Appraising the brain's energy budget",
    source: 'Proceedings of the National Academy of Sciences',
    doi: '10.1073/pnas.172399499',
  },
  mcewen1998: {
    id: 'mcewen1998',
    authors: 'McEwen, B. S.',
    year: 1998,
    title: 'Protective and damaging effects of stress mediators',
    source: 'New England Journal of Medicine',
    doi: '10.1056/nejm199801153380307',
  },
  walker2009: {
    id: 'walker2009',
    authors: 'Walker, M. P., & van der Helm, E.',
    year: 2009,
    title: 'Overnight therapy? The role of sleep in emotional brain processing',
    source: 'Psychological Bulletin',
    doi: '10.1037/a0016570',
  },
  chambers2009: {
    id: 'chambers2009',
    authors: 'Chambers, E. S., Bridge, M. W., & Jones, D. A.',
    year: 2009,
    title: 'Carbohydrate sensing in the human mouth: Effects on exercise performance and brain activity',
    source: 'The Journal of Physiology',
    doi: '10.1113/jphysiol.2008.164285',
  },
  arnsten2009: {
    id: 'arnsten2009',
    authors: 'Arnsten, A. F. T.',
    year: 2009,
    title: 'Stress signalling pathways that impair prefrontal cortex structure and function',
    source: 'Nature Reviews Neuroscience',
    doi: '10.1038/nrn2648',
  },
  balban2023: {
    id: 'balban2023',
    authors: 'Balban, M. Y., Neri, E., Kogon, M. M., Weed, L., Nouriani, B., Jo, B., Holl, G., Zeitzer, J. M., Spiegel, D., & Huberman, A. D.',
    year: 2023,
    title: 'Brief structured respiration practices enhance mood and reduce physiological arousal',
    source: 'Cell Reports Medicine',
    doi: '10.1016/j.xcrm.2022.100895',
  },

  // Spatial cognition / visualisation
  shepard1971: {
    id: 'shepard1971',
    authors: 'Shepard, R. N., & Metzler, J.',
    year: 1971,
    title: 'Mental rotation of three-dimensional objects',
    source: 'Science',
    doi: '10.1126/science.171.3972.701',
  },
  linn1985: {
    id: 'linn1985',
    authors: 'Linn, M. C., & Petersen, A. C.',
    year: 1985,
    title: 'Emergence and characterization of sex differences in spatial ability: A meta-analysis',
    source: 'Child Development',
    doi: '10.2307/1130467',
  },
  uttal2013: {
    id: 'uttal2013',
    authors: 'Uttal, D. H., Meadow, N. G., Tipton, E., Hand, L. L., Alden, A. R., Warren, C., & Newcombe, N. S.',
    year: 2013,
    title: 'The malleability of spatial skills: A meta-analysis of training studies',
    source: 'Psychological Bulletin',
    doi: '10.1037/a0028446',
  },
  sorby2009: {
    id: 'sorby2009',
    authors: 'Sorby, S. A.',
    year: 2009,
    title: 'Educational research in developing 3-D spatial skills for engineering students',
    source: 'International Journal of Science Education',
    doi: '10.1080/09500690802595839',
  },
  rittlejohnson2001: {
    id: 'rittlejohnson2001',
    authors: 'Rittle-Johnson, B., Siegler, R. S., & Alibali, M. W.',
    year: 2001,
    title: 'Developing conceptual understanding and procedural skill in mathematics: An iterative process',
    source: 'Journal of Educational Psychology',
    doi: '10.1037/0022-0663.93.2.346',
  },
} satisfies Record<string, Reference>;
