/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import Sprite, { IsoGround, GoldenOverlay } from '../../IsometricSprite';

const K = '/assets/kenney';

interface SceneProps { unlockedMilestones: number; }

/**
 * Family-Community — Family Home & Garden
 * Bare yard → vibrant family home with garden, people, and celebration.
 */
const FamilyIsoScene: React.FC<SceneProps> = ({ unlockedMilestones: m }) => (
  <div style={{ position: 'absolute', inset: 0 }}>
    {/* ── Green grass ground ── */}
    <IsoGround color1="#7DB86A" color2="#5A9A48" />

    {/* ── House (always visible) ── */}
    <Sprite src={`${K}/buildings/building-a.png`} x={520} y={440} width={220} label="Family Home" />

    {/* ── Garden path ── */}
    <Sprite src={`${K}/nature/ground_pathStraight.png`} x={590} y={280} width={80} zIndex={8} />
    <Sprite src={`${K}/nature/ground_pathStraight.png`} x={590} y={340} width={80} zIndex={8} />

    {/* ── Perimeter fence ── */}
    <Sprite src={`${K}/nature/fence_simple.png`}     x={230} y={340} width={70} />
    <Sprite src={`${K}/nature/fence_simple.png`}     x={300} y={340} width={70} />
    <Sprite src={`${K}/nature/fence_simple.png`}     x={370} y={340} width={70} />
    <Sprite src={`${K}/nature/fence_simple.png`}     x={790} y={340} width={70} />
    <Sprite src={`${K}/nature/fence_simple.png`}     x={860} y={340} width={70} />
    <Sprite src={`${K}/nature/fence_simple.png`}     x={930} y={340} width={70} />

    {/* ── Base trees (always) ── */}
    <Sprite src={`${K}/nature/tree_oak.png`}        x={200} y={420} width={120} />
    <Sprite src={`${K}/nature/tree_pineDefaultA.png`} x={920} y={440} width={90} />

    {/* ── m>=1: Welcome mat ── */}
    <Sprite src={`${K}/furniture/rugDoormat.png`} x={585} y={340} width={85} visible={m >= 1} delay={0} label="Welcome Mat" zIndex={9} />

    {/* ── m>=2: Family photo + porch light ── */}
    <Sprite src={`${K}/furniture/lampWall.png`}  x={555} y={560} width={22} visible={m >= 2} delay={0} />
    <Sprite src={`${K}/furniture/books.png`}     x={600} y={510} width={35} visible={m >= 2} delay={0.05} label="Family Photo" />

    {/* ── m>=3: Garden starts growing ── */}
    <Sprite src={`${K}/nature/tree_oak.png`}       x={300} y={450} width={110} visible={m >= 3} delay={0} />
    <Sprite src={`${K}/nature/tree_cone.png`}      x={850} y={420} width={95}  visible={m >= 3} delay={0.04} />
    <Sprite src={`${K}/nature/plant_bush.png`}     x={370} y={330} width={55}  visible={m >= 3} delay={0.06} />
    <Sprite src={`${K}/nature/plant_bushSmall.png`} x={800} y={335} width={40} visible={m >= 3} delay={0.08} />
    <Sprite src={`${K}/nature/flower_redA.png`}    x={420} y={290} width={35}  visible={m >= 3} delay={0.1} />
    <Sprite src={`${K}/nature/flower_yellowA.png`} x={460} y={285} width={35}  visible={m >= 3} delay={0.12} />
    <Sprite src={`${K}/nature/flower_purpleA.png`} x={780} y={290} width={35}  visible={m >= 3} delay={0.14} />
    <Sprite src={`${K}/nature/flower_redB.png`}    x={820} y={285} width={35}  visible={m >= 3} delay={0.16} />

    {/* ── m>=4: Outdoor dining table ── */}
    <Sprite src={`${K}/furniture/tableRound.png`} x={330} y={220} width={100} visible={m >= 4} delay={0} label="Dining Table" />
    <Sprite src={`${K}/furniture/chair.png`}      x={300} y={200} width={45}  visible={m >= 4} delay={0.04} />
    <Sprite src={`${K}/furniture/chair.png`}      x={385} y={200} width={45}  visible={m >= 4} delay={0.06} flip />
    <Sprite src={`${K}/furniture/chair.png`}      x={335} y={260} width={45}  visible={m >= 4} delay={0.08} />
    <Sprite src={`${K}/furniture/chair.png`}      x={350} y={170} width={45}  visible={m >= 4} delay={0.1} />

    {/* ── m>=5: Graduation cap + flower boxes ── */}
    <Sprite src={`${K}/nature/flower_yellowB.png`} x={510} y={520} width={30} visible={m >= 5} delay={0} />
    <Sprite src={`${K}/nature/flower_redB.png`}    x={720} y={520} width={30} visible={m >= 5} delay={0.04} />
    <Sprite src={`${K}/furniture/plantSmall3.png`} x={545} y={360} width={22} visible={m >= 5} delay={0.06} />
    <Sprite src={`${K}/nature/pot_large.png`}      x={750} y={350} width={40} visible={m >= 5} delay={0.08} />

    {/* ── m>=6: More garden ── */}
    <Sprite src={`${K}/nature/plant_bushLarge.png`}  x={220} y={380} width={65} visible={m >= 6} delay={0} />
    <Sprite src={`${K}/nature/tree_small.png`}       x={950} y={380} width={65} visible={m >= 6} delay={0.04} />
    <Sprite src={`${K}/nature/rock_smallA.png`}      x={430} y={240} width={28} visible={m >= 6} delay={0.06} />
    <Sprite src={`${K}/nature/grass_leafs.png`}      x={330} y={195} width={45} visible={m >= 6} delay={0.08} zIndex={15} />
    <Sprite src={`${K}/nature/grass_leafs.png`}      x={810} y={210} width={45} visible={m >= 6} delay={0.1} zIndex={15} />
    <Sprite src={`${K}/nature/stone_smallA.png`}     x={890} y={270} width={20} visible={m >= 6} delay={0.12} />

    {/* ── m>=7: Family in garden + BBQ ── */}
    <Sprite src={`${K}/characters/character-a.png`} x={710} y={210} width={55} visible={m >= 7} delay={0} label="Family" />
    <Sprite src={`${K}/characters/character-b.png`} x={770} y={205} width={55} visible={m >= 7} delay={0.04} />
    <Sprite src={`${K}/characters/character-c.png`} x={740} y={175} width={50} visible={m >= 7} delay={0.06} />
    <Sprite src={`${K}/survival/campfire-pit.png`}  x={830} y={200} width={70} visible={m >= 7} delay={0.08} label="BBQ" />
    <Sprite src={`${K}/furniture/bench.png`}        x={850} y={180} width={70} visible={m >= 7} delay={0.1} />

    {/* ── m>=8: New kitchen + car ── */}
    <Sprite src={`${K}/vehicles/hatchback-sports.png`} x={950} y={240} width={90} visible={m >= 8} delay={0} label="Family Car" />
    <Sprite src={`${K}/furniture/kitchenFridge.png`}   x={430} y={460} width={55} visible={m >= 8} delay={0.05} />
    <Sprite src={`${K}/furniture/kitchenStove.png`}    x={470} y={450} width={55} visible={m >= 8} delay={0.08} />

    {/* ── m>=9: Community board ── */}
    <Sprite src={`${K}/survival/signpost.png`}     x={210} y={290} width={55} visible={m >= 9} delay={0} label="Community Board" />
    <Sprite src={`${K}/nature/fence_gate.png`}     x={575} y={335} width={65} visible={m >= 9} delay={0.05} label="Garden Gate" />
    <Sprite src={`${K}/furniture/lampRoundFloor.png`} x={960} y={320} width={24} visible={m >= 9} delay={0.08} />
    <Sprite src={`${K}/nature/plant_bushDetailed.png`} x={250} y={260} width={50} visible={m >= 9} delay={0.1} />

    {/* ── m>=10: Garden features ── */}
    <Sprite src={`${K}/nature/flower_purpleB.png`} x={300} y={280} width={32} visible={m >= 10} delay={0} />
    <Sprite src={`${K}/nature/flower_yellowA.png`} x={340} y={272} width={32} visible={m >= 10} delay={0.03} />
    <Sprite src={`${K}/nature/mushroom_red.png`}   x={250} y={250} width={28} visible={m >= 10} delay={0.06} />
    <Sprite src={`${K}/nature/pot_large.png`}      x={500} y={310} width={40} visible={m >= 10} delay={0.08} label="Garden Pot" />
    <Sprite src={`${K}/nature/plant_flatTall.png`} x={870} y={310} width={40} visible={m >= 10} delay={0.1} />
    <Sprite src={`${K}/furniture/bench.png`}       x={920} y={290} width={70} visible={m >= 10} delay={0.12} label="Garden Bench" />
    <Sprite src={`${K}/nature/bridge_wood.png`}    x={440} y={230} width={80} visible={m >= 10} delay={0.14} label="Garden Bridge" />

    {/* ── m>=11: Family celebration ── */}
    <Sprite src={`${K}/characters/character-d.png`} x={340} y={170} width={48} visible={m >= 11} delay={0} />
    <Sprite src={`${K}/characters/character-e.png`} x={395} y={165} width={48} visible={m >= 11} delay={0.03} />
    <Sprite src={`${K}/characters/character-f.png`} x={620} y={180} width={48} visible={m >= 11} delay={0.06} />
    <Sprite src={`${K}/characters/character-g.png`} x={560} y={170} width={45} visible={m >= 11} delay={0.09} />
    <Sprite src={`${K}/characters/character-h.png`} x={850} y={165} width={45} visible={m >= 11} delay={0.12} />
    <Sprite src={`${K}/characters/character-i.png`} x={680} y={155} width={45} visible={m >= 11} delay={0.15} />
    <Sprite src={`${K}/nature/tree_oak_fall.png`}  x={170} y={500} width={120} visible={m >= 11} delay={0.18} label="Autumn Oak" />

    {/* ── m>=12: Warm golden light ── */}
    <GoldenOverlay active={m >= 12} />
  </div>
);

export default memo(FamilyIsoScene);
