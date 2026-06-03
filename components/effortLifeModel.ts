/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Effort → Life model — the only net-new computation behind "Your Possible
 * Life". Two small, pure, source-grounded functions plus thin reuse helpers:
 *
 *   irishNetPay(gross)            — 2026 PAYE + USC + PRSI → take-home
 *   lifestyleFromNet(net, region) — take-home → a tangible, honest life picture
 *   bestSixPoints(profile, which) — best-6 CAO points on current OR target grades
 *   careerReach(courses, ...)     — points feasibility of a career's routes
 *
 * Everything upstream (grades → points → reachable careers → salary) reuses the
 * existing engine (getPointsForGrade, reachBucket, CAREERS/matchStrings). These
 * functions translate a salary into what a life actually looks like, authored
 * the same way careerPathsData's salary bands were: source-grounded, verified,
 * with the honesty caveats baked into the copy.
 *
 * ── Tax sources (2026, single PAYE employee, no special reliefs) ──
 *  • Income tax: 20% standard band to €44,000, 40% above; tax credits
 *    €2,000 personal + €2,000 PAYE = €4,000, applied after, floored at €0.
 *    (revenue.ie "Tax rates, bands and reliefs"; Budget 2026.)
 *  • USC: exempt if total income ≤ €13,000 (a cliff — cross it and the bands
 *    apply from €0); otherwise 0.5% ≤ €12,012 · 2% to €28,700 · 3% to €70,044
 *    · 8% above. (revenue.ie USC.)
 *  • PRSI: Class A employee 4.2% of gross once weekly pay > €352 (≈ €18,304/yr;
 *    a credit tapers €352.01–€424/wk but that range sits below every career
 *    here, so a flat 4.2% is exact for our salary range). (gov.ie /
 *    citizensinformation.ie — rate rose to 4.2% from Oct 2025.)
 *  Worked check: €50,000 → €39,667.18 net (~€3,305.60/mo).
 *
 * ── Cost-of-living sources ──
 *  Daft.ie Q4 2025 Rent Report (room / 1-bed / 2-bed by area); CSO; Numbeo;
 *  OUTsurance 2025 car-cost; gradireland grad salaries. The real divider is
 *  share-vs-alone, not city — modelled below. 1-bed euro figures are derived
 *  (≈0.8× the local 2-bed) where Daft publishes only 2-bed standardised rents.
 */

import { type StudentSubjectProfile, LC_SUBJECTS, getPointsForGrade } from './subjectData';
import { reachBucket, type Reach } from './futureFinderRiasec';
import { type CAOCourse } from './futureFinderData';

const round2 = (n: number) => Math.round(n * 100) / 100;
const pct = (x: number) => `${Math.round(x * 100)}%`;

// ─── Irish take-home pay (2026) ──────────────────────────────────────────────

const STANDARD_BAND = 44000;
const RATE_LOW = 0.2;
const RATE_HIGH = 0.4;
const TAX_CREDITS = 4000;

const USC_EXEMPTION = 13000; // total income at/under this → no USC at all
/** Marginal bands: each rate applies to income up to `upTo`. */
const USC_BANDS: { upTo: number; rate: number }[] = [
  { upTo: 12012, rate: 0.005 },
  { upTo: 28700, rate: 0.02 },
  { upTo: 70044, rate: 0.03 },
  { upTo: Infinity, rate: 0.08 },
];

const PRSI_RATE = 0.042;
const PRSI_WEEKLY_FLOOR = 352; // PRSI applies once weekly pay exceeds this

export interface NetPayBreakdown {
  gross: number;
  incomeTax: number;
  usc: number;
  prsi: number;
  /** Annual take-home. */
  net: number;
  /** net / 12. */
  netMonthly: number;
}

/** 2026 PAYE + USC + PRSI for a single employee. See file header for sources. */
export function irishNetPay(gross: number, _year: number = 2026): NetPayBreakdown {
  const g = Math.max(0, gross);

  // Income tax with credits applied after.
  const grossTax = RATE_LOW * Math.min(g, STANDARD_BAND) + RATE_HIGH * Math.max(0, g - STANDARD_BAND);
  const incomeTax = Math.max(0, grossTax - TAX_CREDITS);

  // USC — exempt under the cliff, else marginal bands from €0.
  let usc = 0;
  if (g > USC_EXEMPTION) {
    let prev = 0;
    for (const band of USC_BANDS) {
      if (g <= prev) break;
      const slice = Math.min(g, band.upTo) - prev;
      if (slice > 0) usc += slice * band.rate;
      prev = band.upTo;
    }
  }

  // PRSI — flat 4.2% once weekly pay clears the floor.
  const prsi = g / 52 > PRSI_WEEKLY_FLOOR ? g * PRSI_RATE : 0;

  const net = g - incomeTax - usc - prsi;
  return {
    gross: g,
    incomeTax: round2(incomeTax),
    usc: round2(usc),
    prsi: round2(prsi),
    net: round2(net),
    netMonthly: round2(net / 12),
  };
}

// ─── Take-home → a tangible life ─────────────────────────────────────────────

export type LifeRegion = 'dublin' | 'city' | 'regional';

export const LIFE_REGIONS: LifeRegion[] = ['dublin', 'city', 'regional'];
export const LIFE_REGION_LABELS: Record<LifeRegion, string> = {
  dublin: 'Dublin',
  city: 'Cork · Galway · Limerick',
  regional: 'A town or regional area',
};

/**
 * Monthly €, modelled from Daft Q4 2025 + Numbeo. `share` = a room in a shared
 * house (the realistic option for most new grads): national double room ~€775,
 * Dublin ~€876, regional ~€450-600. `alone` = a 1-bed, set to the midpoint of
 * the researched per-area ranges (Dublin ~€2,000-2,100 / Numbeo median; Cork/
 * Galway/Limerick ~€1,600-1,800; regional ~€1,200-1,400) — NOT a flat 0.8× of
 * the 2-bed, which would understate Dublin. Flagged modelled, not official.
 */
const REGION_RENT: Record<LifeRegion, { share: number; alone: number }> = {
  dublin: { share: 880, alone: 2050 },
  city: { share: 600, alone: 1650 },
  regional: { share: 450, alone: 1300 },
};
/** Utilities + groceries + transport + phone, one person (Numbeo/CSO ~€600-900). */
const ESSENTIALS = 750;
/**
 * A young driver's USED car, all-in/mo — a conservative estimate: insurance
 * ~€140 (the big one for under-25s) + fuel ~€130 + motor tax ~€35 + maintenance
 * ~€60 + NCT/incidentals ≈ €500. A NEW car runs ~€864/mo all-in (OUTsurance
 * 2025); a high-insurance year can push a young driver toward €700-1,000. Kept
 * conservative so the tool never overstates how affordable a car is.
 */
const CAR_COST = 500;

export type LifeTier = 'Getting by' | 'Independent-lite' | 'Comfortable' | 'Thriving';

export interface LifestylePicture {
  netMonthly: number;
  region: LifeRegion;
  tier: LifeTier;
  /** Shared-housing rent used as the realistic baseline. */
  shareRent: number;
  /** Shared-baseline rent as a share of net (0..1). */
  rentShareOfNet: number;
  /** Disposable after shared rent + essentials. */
  disposable: number;
  /** A 1-bed alone here under ~45% of net (stretched-but-doable)? */
  canRentAlone: boolean;
  /** A 1-bed alone here ≤ ~35% of net (comfortable)? */
  aloneComfortable: boolean;
  housing: string;
  housingDetail: string;
  transport: string;
  saving: string;
  /** Headline "could save up to" figure if you skip the car (€/mo). */
  savingMonthly: number;
  travel: string;
  /** One warm second-person line — plural, non-deterministic. */
  vignette: string;
  /** Honesty line shown alongside the picture. */
  caveat: string;
}

/** Take-home → an honest, qualitative life picture. See file header for sources. */
export function lifestyleFromNet(netMonthly: number, region: LifeRegion = 'city'): LifestylePicture {
  const net = Math.max(0, netMonthly);
  const rent = REGION_RENT[region];
  const shareRent = rent.share;
  const rentShareOfNet = net > 0 ? shareRent / net : 1;
  const disposable = Math.max(0, net - shareRent - ESSENTIALS);

  const aloneShare = net > 0 ? rent.alone / net : 1;
  const canRentAlone = aloneShare <= 0.45;
  const aloneComfortable = aloneShare <= 0.35;

  const tier: LifeTier =
    net < 2200 ? 'Getting by' :
    net < 2900 ? 'Independent-lite' :
    net < 3600 ? 'Comfortable' : 'Thriving';

  const regionName =
    region === 'dublin' ? 'Dublin' :
    region === 'city' ? 'a city like Cork or Galway' :
    'a town outside the cities';

  const housing = aloneComfortable
    ? `Your own place in ${regionName}`
    : canRentAlone
      ? `Sharing — or your own small place if you stretch`
      : `A room in a shared house in ${regionName}`;
  const housingDetail = aloneComfortable
    ? `Renting alone here is around ${pct(aloneShare)} of your take-home — comfortable.`
    : canRentAlone
      ? `A 1-bed alone would be ~${pct(aloneShare)} of take-home — doable but tight. Sharing keeps it easy.`
      : `Sharing keeps rent near ${pct(rentShareOfNet)} of take-home. Your own place here isn't realistic on this yet.`;

  // Car vs saving is genuinely a trade-off at typical grad incomes. Round the
  // displayed "save" figures DOWN to the nearest €50 so the copy never overstates
  // what's actually spare (the honesty rule), and gate the message on real
  // disposable, not the rounded value.
  const saveIfNoCar = Math.max(0, Math.floor(disposable / 50) * 50);
  const canAffordCar = disposable >= CAR_COST;
  const saveWithCar = Math.max(0, Math.floor((disposable - CAR_COST) / 50) * 50);

  const transport = canAffordCar
    ? (saveWithCar >= 300 ? 'A used car, and still money left over' : 'A used car — though it takes most of the slack')
    : 'Public transport for now — a car would be a stretch';

  const saving = disposable >= 100
    ? `Put roughly €${saveIfNoCar.toLocaleString()} a month aside${canAffordCar ? ' (less if you run a car)' : ''}`
    : 'Saving would be tight at first';

  const travel = disposable >= 900 ? 'A couple of trips away a year, comfortably'
    : disposable >= 400 ? 'A trip away once or twice a year'
    : 'The odd budget trip if you plan ahead';

  const vignette = aloneComfortable
    ? `You could have a place of your own in ${regionName}, with room to breathe at the end of the month.`
    : tier === 'Getting by'
      ? `You'd be starting out — sharing a place and watching the budget, but standing on your own feet.`
      : `You'd share a place in ${regionName}, cover your own way, and have something left over for what you want.`;

  const caveat = 'A possibility, not a forecast — salaries here are typical, not promised, and rents are tight right now.';

  return {
    netMonthly: round2(net),
    region,
    tier,
    shareRent,
    rentShareOfNet: round2(rentShareOfNet),
    disposable: round2(disposable),
    canRentAlone,
    aloneComfortable,
    housing,
    housingDetail,
    transport,
    saving,
    savingMonthly: saveIfNoCar,
    travel,
    vignette,
    caveat,
  };
}

// ─── Reuse helpers (thin wrappers over the existing points engine) ───────────

/**
 * Best-6 CAO points on the student's CURRENT grades, or on their TARGET grades
 * (falling back to current where no target is set). Same math as the original
 * Future Finder's computeCurrentPoints — the single source of truth is
 * getPointsForGrade — just applied to whichever grade column.
 */
export function bestSixPoints(profile: StudentSubjectProfile, which: 'current' | 'target'): number {
  const pts = profile.subjects
    .map((s) => {
      const isMaths = LC_SUBJECTS.find((lc) => lc.name === s.subjectName)?.isMaths ?? false;
      const grade = which === 'target' ? (s.targetGrade ?? s.currentGrade) : s.currentGrade;
      return getPointsForGrade(grade, isMaths);
    })
    .sort((a, b) => b - a);
  return pts.slice(0, 6).reduce((sum, p) => sum + p, 0);
}

export interface CareerReach {
  /** Lowest typical points among the career's CAO degree routes (>0), or null if none. */
  entryPoints: number | null;
  /** A no-points route exists (apprenticeship / PLC / 0-point course). */
  hasOpenRoute: boolean;
  reachNow: Reach;
  reachTarget: Reach;
  /** Points still needed from current to clear the entry threshold (0 if there / open). */
  gapFromCurrent: number;
  /** Points still needed from target to clear it (0 if there / open). */
  gapFromTarget: number;
}

/**
 * Points feasibility of a career, given the CAO courses that lead to it. Reach
 * is an independent axis from interest fit (reused verbatim from reachBucket) —
 * a points stretch is shown as exactly that, never hidden.
 */
export function careerReach(courses: CAOCourse[], currentPoints: number, targetPoints: number): CareerReach {
  const cao = courses.filter((c) => (c.typicalPoints ?? 0) > 0 && c.pathwayType !== 'apprenticeship');
  const hasOpenRoute = courses.some(
    (c) => (c.typicalPoints ?? 0) <= 0 || c.pathwayType === 'apprenticeship' || c.pathwayType === 'plc',
  );
  const entryPoints = cao.length ? Math.min(...cao.map((c) => c.typicalPoints)) : null;
  const reachNow: Reach = entryPoints == null ? 'open' : reachBucket(currentPoints, entryPoints);
  const reachTarget: Reach = entryPoints == null ? 'open' : reachBucket(targetPoints, entryPoints);
  const gapFromCurrent = entryPoints == null ? 0 : Math.max(0, entryPoints - currentPoints);
  const gapFromTarget = entryPoints == null ? 0 : Math.max(0, entryPoints - targetPoints);
  return { entryPoints, hasOpenRoute, reachNow, reachTarget, gapFromCurrent, gapFromTarget };
}
