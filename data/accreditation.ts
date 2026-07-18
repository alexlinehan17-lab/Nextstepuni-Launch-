/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Accreditation snapshot ──────────────────────────────────────────────────
//
// Content for the in-app Accreditation page (the cover document for the
// pre-accreditation review with DCU / Brian MacCraith). This is the curated
// point-in-time summary; the per-module evidence lives in
// compliance/evidence/<module>.md and the change audit trail in
// data/cutContent.ts (the in-app "Cut Content" page).
//
// Update the coverage counts and the `verification` block as the review
// progresses. `asOf` stamps the snapshot.

export interface CoverageGroup {
  name: string;
  accredited: number;
  total: number;
  basis: string; // what the claims are grounded in
}

export interface AccreditationLimitation {
  title: string;
  detail: string;
}

export interface VerificationSummary {
  /** Modules put through the independent adversarial re-check. */
  modulesAudited: number;
  /** Cited claims re-examined against their sources. */
  claimsChecked: number;
  /** Modules where every citation held with no issue raised. */
  modulesClean: number;
  /** Issues that survived an independent second-reviewer refutation attempt. */
  issuesUpheld: number;
  method: string;
  date: string;
}

export interface ExamEngine {
  /** Headline stats for the exam-preparation engine (Paper Trail). */
  stats: { value: string; label: string }[];
  /** How the exam data was held to the same evidence standard. */
  provenance: string;
  /** What a student can do with it — the study loop. */
  capabilities: { title: string; detail: string }[];
}

export interface AccreditationSnapshot {
  governingRule: string;
  methodology: string[];
  coverage: CoverageGroup[];
  examEngine: ExamEngine;
  limitations: AccreditationLimitation[];
  verification: VerificationSummary;
  asOf: string;
}

export const ACCREDITATION: AccreditationSnapshot = {
  // The single rule every claim is held to (verbatim from the project standard).
  governingRule:
    'We only state or advise something where a real, locatable source genuinely supports the specific claim — ' +
    'peer-reviewed literature for the learning-science content, and official State Examinations Commission and CAO ' +
    'documents for the exam content. Any claim that could not be verified was reframed to non-prescriptive language ' +
    'or removed outright. A citation was never invented to keep a claim.',

  methodology: [
    'Every peer-reviewed citation is checked to resolve to a real paper via its DOI on CrossRef; abstracts and open-access checks use PubMed, Europe PMC and Unpaywall.',
    'Exam-strategy and subject content is grounded in official sources — SEC marking schemes and Chief Examiner’s Reports, and the CAO common points scale — not psychology journals.',
    'In-app, sources surface as faint inline citation markers plus a module-wide References list; the full reference set is typed and ordered per module.',
    'Every removal, reframe or factual correction is recorded verbatim in the Cut Content audit trail, with the original wording, the replacement, and the reason.',
    'Each module carries a claim-by-claim evidence dossier recording how every source was verified.',
    'The whole accredited set was then put through an independent, adversarial re-verification pass: a separate reviewer per module re-checked that each citation supports its specific claim, and every issue raised was independently re-tested before being upheld.',
  ],

  coverage: [
    {
      name: 'Learning science & psychology',
      accredited: 38,
      total: 38,
      basis: 'peer-reviewed literature (verified DOIs)',
    },
    {
      name: 'Exam Zone (strategy)',
      accredited: 8,
      total: 8,
      basis: 'SEC marking schemes / Chief Examiner reports + CAO points scale',
    },
    {
      name: 'Subject-specific',
      accredited: 3,
      total: 37,
      basis: 'each subject’s own SEC Chief Examiner report / marking scheme',
    },
  ],

  examEngine: {
    stats: [
      { value: '23', label: 'Subjects topic-tagged' },
      { value: '5,306', label: 'Questions tagged to topics' },
      { value: '1,121', label: 'Papers with per-question answers' },
      { value: '100%', label: 'Independent-audit agreement' },
    ],
    provenance:
      'The exam-preparation engine (Paper Trail) is held to the same verify-don’t-guess standard as the learning content. ' +
      'Every past-paper question is mapped to its own marking-scheme region from the real State Examinations Commission scheme (coordinates only, © SEC), ' +
      'and every one of 5,306 questions across 23 subjects is classified to its curriculum topic and re-checked by an independent adversarial verifier. ' +
      'A separate read-only audit re-classified a fresh sample of 120 questions spanning all 23 subjects and agreed with the committed tag 100% of the time, with zero clear errors.',
    capabilities: [
      { title: 'Every paper with its scheme', detail: 'Each of ~1,121 papers opens beside its official marking scheme, per-question — so a student sees exactly how the marks are awarded.' },
      { title: 'Practise a topic across years', detail: 'Because questions are tagged to curriculum topics, a student weak on (say) Calculus can drill every Calculus question across every year in one tap, with a frequency chip showing how often it comes up.' },
      { title: 'Exam technique on the real paper', detail: 'Live overlays show minute-by-question time budgets, decode each command word, and surface the Chief Examiner’s own “where marks are lost” for the subject — all on the actual exam.' },
      { title: 'A full, personal study loop', detail: 'Students score themselves against the scheme and tag why a mark was lost; from that, the app builds a progress dashboard, ranks their weakest topics, schedules spaced recall over the questions they got wrong, lets them assemble custom mock sets, counts down to their exam date, and exports a printable revision pack — every item a real SEC question, never fabricated content.' },
    ],
  },

  limitations: [
    {
      title: '34 subject modules not yet presented as verified',
      detail:
        'Subject modules are accredited only once that subject’s own SEC report is in hand. Business, Mathematics and English are complete (and all three had factual exam-structure errors corrected against the official marking schemes). The remaining 34 are worked through as their reports are supplied and verified, and are not claimed as verified until then.',
    },
    {
      title: 'Two figures await a paywalled primary source',
      detail:
        'Two statements were reframed conservatively only because their primary paper is paywalled and the exact wording could not be confirmed. They are flagged in the Cut Content log and can be restored verbatim once the paper is supplied.',
    },
    {
      title: 'Points-optimisation H1 rates labelled approximate',
      detail:
        'The per-subject H1-rate figures derive from SEC annual statistics that could not be re-downloaded this cycle; they are cited to the SEC statistics, shown as approximate in-app, and flagged for re-checking against the published tables.',
    },
  ],

  // Filled from the independent re-verification pass.
  verification: {
    modulesAudited: 48,
    claimsChecked: 297,
    modulesClean: 26,
    issuesUpheld: 13,
    method:
      'One independent reviewer per module re-checked every cited claim against its source; each issue raised was then re-tested by a second reviewer instructed to refute it, and only genuine, surviving issues were upheld. 13 genuine issues were upheld across 11 modules — and all 13 have since been resolved (sources re-attributed to the paper that supports the claim, or the claim reframed to what the evidence establishes), each recorded in the Cut Content log.',
    date: '2026-06-26',
  },

  asOf: '2026-07-18',
};
