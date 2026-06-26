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

export interface AccreditationSnapshot {
  governingRule: string;
  methodology: string[];
  coverage: CoverageGroup[];
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
      accredited: 2,
      total: 37,
      basis: 'each subject’s own SEC Chief Examiner report / marking scheme',
    },
  ],

  limitations: [
    {
      title: '35 subject modules not yet presented as verified',
      detail:
        'Subject modules are accredited only once that subject’s own SEC report is in hand. Business and Mathematics are complete (and both had factual exam-structure errors corrected against the official marking schemes). The remaining 35 await their reports — examinations.ie blocks automated downloads, so these are sourced as the reports are supplied, and are not claimed as verified until then.',
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
    claimsChecked: 0,
    modulesClean: 0,
    issuesUpheld: 0,
    method:
      'One independent reviewer per module re-checked every cited claim against its source; each issue raised was then re-tested by a second reviewer instructed to refute it, and only genuine, surviving issues were upheld.',
    date: '2026-06-26',
  },

  asOf: '2026-06-26',
};
