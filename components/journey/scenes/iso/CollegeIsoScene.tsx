/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import Sprite, { IsoGround, GoldenOverlay } from '../../IsometricSprite';

const K = '/assets/kenney';

interface SceneProps { unlockedMilestones: number; }

/**
 * College-Learning — University Campus
 * Acceptance letter → full graduation ceremony.
 */
const CollegeIsoScene: React.FC<SceneProps> = ({ unlockedMilestones: m }) => (
  <div style={{ position: 'absolute', inset: 0 }}>
    {/* ── Campus grass ── */}
    <IsoGround color1="#6DB85A" color2="#4A9038" />

    {/* ── Main university building (always visible) ── */}
    <Sprite src={`${K}/buildings/building-type-a.png`} x={450} y={460} width={260} label="University" />

    {/* ── Campus paths ── */}
    <Sprite src={`${K}/nature/ground_pathStraight.png`} x={550} y={270} width={80} zIndex={8} />
    <Sprite src={`${K}/nature/ground_pathStraight.png`} x={550} y={340} width={80} zIndex={8} />
    <Sprite src={`${K}/nature/ground_pathStraight.png`} x={550} y={400} width={80} zIndex={8} />

    {/* ── Hedges along building ── */}
    <Sprite src={`${K}/nature/plant_bushLargeTriangle.png`} x={400} y={390} width={50} />
    <Sprite src={`${K}/nature/plant_bushLargeTriangle.png`} x={700} y={390} width={50} />

    {/* ── Base trees ── */}
    <Sprite src={`${K}/nature/tree_oak.png`}     x={220} y={430} width={120} />
    <Sprite src={`${K}/nature/tree_detailed.png`} x={880} y={420} width={100} />

    {/* ── Campus bench ── */}
    <Sprite src={`${K}/furniture/bench.png`} x={760} y={270} width={70} label="Campus Bench" />

    {/* ── Flowers ── */}
    <Sprite src={`${K}/nature/flower_redA.png`}    x={470} y={335} width={30} />
    <Sprite src={`${K}/nature/flower_yellowA.png`} x={500} y={330} width={30} />
    <Sprite src={`${K}/nature/flower_purpleA.png`} x={660} y={330} width={30} />
    <Sprite src={`${K}/nature/flower_redB.png`}    x={690} y={335} width={30} />

    {/* ── m>=1: Acceptance letter on bench ── */}
    <Sprite src={`${K}/furniture/books.png`} x={780} y={295} width={32} visible={m >= 1} delay={0} label="Acceptance Letter" />

    {/* ── m>=2: Campus gates ── */}
    <Sprite src={`${K}/nature/fence_gate.png`}   x={530} y={240} width={75} visible={m >= 2} delay={0} label="Campus Gates" />
    <Sprite src={`${K}/nature/fence_simple.png`} x={440} y={240} width={65} visible={m >= 2} delay={0.04} />
    <Sprite src={`${K}/nature/fence_simple.png`} x={630} y={240} width={65} visible={m >= 2} delay={0.06} />
    <Sprite src={`${K}/nature/fence_simple.png`} x={350} y={240} width={65} visible={m >= 2} delay={0.08} />
    <Sprite src={`${K}/nature/fence_simple.png`} x={720} y={240} width={65} visible={m >= 2} delay={0.1} />

    {/* ── m>=3: Dorm building ── */}
    <Sprite src={`${K}/buildings/building-type-b.png`} x={810} y={460} width={160} visible={m >= 3} delay={0} label="Dorm" />
    <Sprite src={`${K}/nature/plant_bushSmall.png`}    x={840} y={380} width={38} visible={m >= 3} delay={0.04} />
    <Sprite src={`${K}/nature/plant_bush.png`}         x={890} y={375} width={45} visible={m >= 3} delay={0.06} />

    {/* ── m>=4: Study area + books ── */}
    <Sprite src={`${K}/furniture/bench.png`}  x={280} y={260} width={65} visible={m >= 4} delay={0} label="Study Bench" />
    <Sprite src={`${K}/furniture/books.png`}  x={295} y={290} width={35} visible={m >= 4} delay={0.04} />
    <Sprite src={`${K}/furniture/books.png`}  x={325} y={288} width={30} visible={m >= 4} delay={0.06} />
    <Sprite src={`${K}/nature/tree_small.png`} x={230} y={310} width={70} visible={m >= 4} delay={0.08} />
    <Sprite src={`${K}/nature/tree_pineSmallA.png`} x={330} y={330} width={55} visible={m >= 4} delay={0.1} />

    {/* ── m>=5: Library building ── */}
    <Sprite src={`${K}/buildings/building-type-c.png`} x={190} y={470} width={170} visible={m >= 5} delay={0} label="Library" />
    <Sprite src={`${K}/nature/plant_bush.png`}         x={250} y={380} width={48} visible={m >= 5} delay={0.04} />

    {/* ── m>=6: Study group ── */}
    <Sprite src={`${K}/furniture/tableRound.png`} x={370} y={200} width={90} visible={m >= 6} delay={0} label="Study Table" />
    <Sprite src={`${K}/furniture/chair.png`}      x={345} y={180} width={42} visible={m >= 6} delay={0.03} />
    <Sprite src={`${K}/furniture/chair.png`}      x={420} y={180} width={42} visible={m >= 6} delay={0.05} flip />
    <Sprite src={`${K}/characters/character-d.png`} x={350} y={185} width={45} visible={m >= 6} delay={0.07} label="Study Partner" />
    <Sprite src={`${K}/characters/character-e.png`} x={415} y={185} width={45} visible={m >= 6} delay={0.09} />
    <Sprite src={`${K}/furniture/books.png`}      x={390} y={235} width={30} visible={m >= 6} delay={0.11} />

    {/* ── m>=7: Lecture hall ── */}
    <Sprite src={`${K}/buildings/building-type-d.png`}  x={660} y={470} width={165} visible={m >= 7} delay={0} label="Lecture Hall" />
    <Sprite src={`${K}/nature/tree_pineDefaultA.png`}   x={790} y={350} width={65} visible={m >= 7} delay={0.04} />

    {/* ── m>=8: Campus life ── */}
    <Sprite src={`${K}/characters/character-f.png`} x={560} y={200} width={45} visible={m >= 8} delay={0} label="Students" />
    <Sprite src={`${K}/characters/character-g.png`} x={620} y={195} width={45} visible={m >= 8} delay={0.03} />
    <Sprite src={`${K}/characters/character-h.png`} x={500} y={205} width={42} visible={m >= 8} delay={0.06} />
    <Sprite src={`${K}/nature/tree_oak.png`}        x={700} y={280} width={95} visible={m >= 8} delay={0.09} />
    <Sprite src={`${K}/nature/tree_pineRoundA.png`} x={190} y={350} width={65} visible={m >= 8} delay={0.11} />

    {/* ── m>=9: Research desk ── */}
    <Sprite src={`${K}/furniture/desk.png`}           x={180} y={230} width={115} visible={m >= 9} delay={0} label="Research Desk" />
    <Sprite src={`${K}/furniture/chairDesk.png`}      x={215} y={210} width={48} visible={m >= 9} delay={0.03} />
    <Sprite src={`${K}/furniture/laptop.png`}         x={200} y={275} width={50} visible={m >= 9} delay={0.05} />
    <Sprite src={`${K}/furniture/lampRoundTable.png`} x={260} y={285} width={24} visible={m >= 9} delay={0.07} />

    {/* ── m>=10: Thesis ── */}
    <Sprite src={`${K}/furniture/books.png`} x={195} y={278} width={35} visible={m >= 10} delay={0} label="Thesis" />
    <Sprite src={`${K}/nature/flower_yellowA.png`} x={520} y={350} width={28} visible={m >= 10} delay={0.04} />
    <Sprite src={`${K}/nature/flower_purpleA.png`} x={640} y={350} width={28} visible={m >= 10} delay={0.06} />

    {/* ── m>=11: Graduation ceremony ── */}
    <Sprite src={`${K}/characters/character-a.png`} x={545} y={380} width={55} visible={m >= 11} delay={0} label="Graduate" />
    <Sprite src={`${K}/characters/character-i.png`} x={460} y={275} width={42} visible={m >= 11} delay={0.03} />
    <Sprite src={`${K}/characters/character-j.png`} x={510} y={270} width={42} visible={m >= 11} delay={0.05} />
    <Sprite src={`${K}/characters/character-k.png`} x={600} y={272} width={42} visible={m >= 11} delay={0.07} />
    <Sprite src={`${K}/characters/character-l.png`} x={650} y={275} width={42} visible={m >= 11} delay={0.09} />
    <Sprite src={`${K}/characters/character-m.png`} x={480} y={245} width={40} visible={m >= 11} delay={0.11} />
    <Sprite src={`${K}/characters/character-n.png`} x={570} y={240} width={40} visible={m >= 11} delay={0.13} />
    <Sprite src={`${K}/nature/flower_redA.png`}     x={560} y={365} width={28} visible={m >= 11} delay={0.15} />

    {/* ── m>=12: Bright inspiring light ── */}
    <GoldenOverlay active={m >= 12} />
  </div>
);

export default memo(CollegeIsoScene);
