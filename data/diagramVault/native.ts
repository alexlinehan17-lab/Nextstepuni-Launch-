/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — NATIVE figures aggregate. Figures extracted straight from SEC
 * question papers by the extraction pipeline (tools/detect_exam_figures.py →
 * dv_prepare → agent-verify → dv_apply) land in one file per subject under
 * `./figures/`, and this module concatenates them. Each entry is a figure an
 * agent VIEWED and confirmed: a real diagram/graph/map/chart cropped from the
 * paper, with an alt describing only what the figure shows and an SEC `source`
 * naming the exact paper + question.
 *
 * INTEGRITY: every entry is covered by the same gate as the derived half
 * (test/diagramVault.test.ts) — the file at `src` must exist in public/, the
 * source must be SEC-attributed, ids unique. A `src` collision with a derived
 * figure is resolved in index.ts (native wins — it is the primary paper crop).
 *
 * Subject files are added to the imports + spread below as each wave lands.
 */

import type { DiagramEntry } from './index';
import { BIOLOGY_FIGURES } from './figures/biology';
import { GEOGRAPHY_FIGURES } from './figures/geography';
import { PHYSICS_FIGURES } from './figures/physics';
import { CHEMISTRY_FIGURES } from './figures/chemistry';
import { BUSINESS_FIGURES } from './figures/business';
import { MATHEMATICS_FIGURES } from './figures/mathematics';
import { APPLIED_MATHEMATICS_FIGURES } from './figures/applied-mathematics';
import { DESIGN_AND_COMMUNICATION_GRAPHICS_FIGURES } from './figures/design-and-communication-graphics';
import { CONSTRUCTION_STUDIES_FIGURES } from './figures/construction-studies';
import { ENGINEERING_FIGURES } from './figures/engineering';
import { TECHNOLOGY_FIGURES } from './figures/technology';
import { ECONOMICS_FIGURES } from './figures/economics';
import { AGRICULTURAL_SCIENCE_FIGURES } from './figures/agricultural-science';
import { HOME_ECONOMICS_S_AND_S_FIGURES } from './figures/home-economics-s-and-s';
import { COMPUTER_SCIENCE_FIGURES } from './figures/computer-science';
import { PHYSICS_AND_CHEMISTRY_FIGURES } from './figures/physics-and-chemistry';
import { JC_SCIENCE_FIGURES } from './figures/jc-science';
import { JC_GEOGRAPHY_FIGURES } from './figures/jc-geography';
import { JC_MATHEMATICS_FIGURES } from './figures/jc-mathematics';
import { JC_ENGINEERING_FIGURES } from './figures/jc-engineering';
import { JC_APPLIED_TECHNOLOGY_FIGURES } from './figures/jc-applied-technology';
import { JC_WOOD_TECHNOLOGY_FIGURES } from './figures/jc-wood-technology';
import { JC_HOME_ECONOMICS_FIGURES } from './figures/jc-home-economics';
import { JC_BUSINESS_STUDIES_FIGURES } from './figures/jc-business-studies';
import { LCA_ENGINEERING_FIGURES } from './figures/lca-engineering';
import { LCA_GRAPHICS_AND_CONSTRUCTION_STUDIES_FIGURES } from './figures/lca-graphics-and-construction-studies';
import { LCA_TECHNOLOGY_FIGURES } from './figures/lca-technology';
import { LCA_AGRICULTURE_HORTICULTURE_FIGURES } from './figures/lca-agriculture-horticulture';
import { PHYSICAL_EDUCATION_FIGURES } from './figures/physical-education';
import { AGRICULTURAL_ECONOMICS_FIGURES } from './figures/agricultural-economics';
import { POLITICS_AND_SOCIETY_FIGURES } from './figures/politics-and-society';
import { LCA_MATHEMATICAL_APPLICATIONS_FIGURES } from './figures/lca-mathematical-applications';
import { LCA_INFORMATION_AND_COMMUNICATION_TECH_FIGURES } from './figures/lca-information-and-communication-tech';

export const NATIVE_FIGURES: DiagramEntry[] = [
  ...BIOLOGY_FIGURES,
  ...GEOGRAPHY_FIGURES,
  ...PHYSICS_FIGURES,
  ...CHEMISTRY_FIGURES,
  ...BUSINESS_FIGURES,
  ...MATHEMATICS_FIGURES,
  ...APPLIED_MATHEMATICS_FIGURES,
  ...DESIGN_AND_COMMUNICATION_GRAPHICS_FIGURES,
  ...CONSTRUCTION_STUDIES_FIGURES,
  ...ENGINEERING_FIGURES,
  ...TECHNOLOGY_FIGURES,
  ...ECONOMICS_FIGURES,
  ...AGRICULTURAL_SCIENCE_FIGURES,
  ...HOME_ECONOMICS_S_AND_S_FIGURES,
  ...COMPUTER_SCIENCE_FIGURES,
  ...PHYSICS_AND_CHEMISTRY_FIGURES,
  ...JC_SCIENCE_FIGURES,
  ...JC_GEOGRAPHY_FIGURES,
  ...JC_MATHEMATICS_FIGURES,
  ...JC_ENGINEERING_FIGURES,
  ...JC_APPLIED_TECHNOLOGY_FIGURES,
  ...JC_WOOD_TECHNOLOGY_FIGURES,
  ...JC_HOME_ECONOMICS_FIGURES,
  ...JC_BUSINESS_STUDIES_FIGURES,
  ...LCA_ENGINEERING_FIGURES,
  ...LCA_GRAPHICS_AND_CONSTRUCTION_STUDIES_FIGURES,
  ...LCA_TECHNOLOGY_FIGURES,
  ...LCA_AGRICULTURE_HORTICULTURE_FIGURES,
  ...PHYSICAL_EDUCATION_FIGURES,
  ...AGRICULTURAL_ECONOMICS_FIGURES,
  ...POLITICS_AND_SOCIETY_FIGURES,
  ...LCA_MATHEMATICAL_APPLICATIONS_FIGURES,
  ...LCA_INFORMATION_AND_COMMUNICATION_TECH_FIGURES,
];
