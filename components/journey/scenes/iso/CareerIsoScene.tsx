/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import Sprite, { IsoGround, GoldenOverlay } from '../../IsometricSprite';

const K = '/assets/kenney';

interface SceneProps { unlockedMilestones: number; }

/**
 * Career-Craft — Workshop / Studio
 * Empty bench → thriving creative workshop.
 */
const CareerIsoScene: React.FC<SceneProps> = ({ unlockedMilestones: m }) => (
  <div style={{ position: 'absolute', inset: 0 }}>
    {/* ── Concrete workshop floor ── */}
    <IsoGround color1="#C0B8A8" color2="#A09888" />

    {/* ── Workshop walls ── */}
    <Sprite src={`${K}/furniture/wall.png`}       x={260} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wallWindow.png`} x={375} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wall.png`}       x={490} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wall.png`}       x={605} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wallWindow.png`} x={720} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wall.png`}       x={835} y={480} width={135} zIndex={12} />

    {/* ── m>=1: Primary workbench ── */}
    <Sprite src={`${K}/survival/workbench.png`} x={350} y={360} width={110} visible={m >= 1} delay={0} label="Workbench" />

    {/* ── m>=2: Tools on wall ── */}
    <Sprite src={`${K}/survival/tool-hammer.png`}  x={370} y={590} width={38} visible={m >= 2} delay={0} label="Hammer" />
    <Sprite src={`${K}/survival/tool-axe.png`}     x={415} y={585} width={38} visible={m >= 2} delay={0.04} label="Axe" />
    <Sprite src={`${K}/survival/tool-pickaxe.png`} x={460} y={588} width={38} visible={m >= 2} delay={0.06} label="Pickaxe" />

    {/* ── m>=3: Drawing desk + blueprints ── */}
    <Sprite src={`${K}/furniture/desk.png`}    x={560} y={370} width={140} visible={m >= 3} delay={0} label="Drawing Desk" />
    <Sprite src={`${K}/furniture/books.png`}   x={600} y={415} width={50}  visible={m >= 3} delay={0.04} label="Blueprints" />
    <Sprite src={`${K}/furniture/laptop.png`}  x={565} y={418} width={55}  visible={m >= 3} delay={0.06} />
    <Sprite src={`${K}/furniture/chairDesk.png`} x={600} y={330} width={55} visible={m >= 3} delay={0.08} />

    {/* ── m>=4: Projects / materials ── */}
    <Sprite src={`${K}/survival/box.png`}             x={270} y={310} width={58} visible={m >= 4} delay={0} label="Supplies" />
    <Sprite src={`${K}/survival/box-open.png`}        x={320} y={305} width={58} visible={m >= 4} delay={0.04} />
    <Sprite src={`${K}/survival/resource-planks.png`} x={255} y={280} width={55} visible={m >= 4} delay={0.06} label="Materials" />
    <Sprite src={`${K}/survival/barrel.png`}          x={240} y={330} width={48} visible={m >= 4} delay={0.08} />
    <Sprite src={`${K}/survival/resource-wood.png`}   x={295} y={340} width={50} visible={m >= 4} delay={0.1} />

    {/* ── m>=5: Mentor figure ── */}
    <Sprite src={`${K}/characters/character-a.png`}    x={760} y={330} width={55} visible={m >= 5} delay={0} label="Mentor" />
    <Sprite src={`${K}/furniture/lampRoundFloor.png`}  x={740} y={360} width={26} visible={m >= 5} delay={0.04} />
    <Sprite src={`${K}/survival/signpost-single.png`}  x={800} y={380} width={35} visible={m >= 5} delay={0.06} label="Guidance" />

    {/* ── m>=6: Equipment expands ── */}
    <Sprite src={`${K}/survival/workbench-anvil.png`} x={810} y={370} width={100} visible={m >= 6} delay={0} label="Anvil Bench" />
    <Sprite src={`${K}/survival/chest.png`}           x={890} y={340} width={58}  visible={m >= 6} delay={0.04} label="Tool Chest" />
    <Sprite src={`${K}/survival/barrel-open.png`}     x={920} y={360} width={48}  visible={m >= 6} delay={0.06} />
    <Sprite src={`${K}/furniture/lampSquareFloor.png`} x={250} y={380} width={26} visible={m >= 6} delay={0.08} />
    <Sprite src={`${K}/survival/bucket.png`}          x={930} y={320} width={40}  visible={m >= 6} delay={0.1} />

    {/* ── m>=7: Finished project on display ── */}
    <Sprite src={`${K}/furniture/sideTable.png`}       x={660} y={320} width={65} visible={m >= 7} delay={0} label="Display Stand" />
    <Sprite src={`${K}/survival/bottle.png`}           x={675} y={370} width={28} visible={m >= 7} delay={0.04} label="Finished Piece" />
    <Sprite src={`${K}/furniture/lampRoundTable.png`}  x={700} y={370} width={26} visible={m >= 7} delay={0.06} />

    {/* ── m>=8: Team member ── */}
    <Sprite src={`${K}/characters/character-b.png`} x={470} y={280} width={55} visible={m >= 8} delay={0} label="Team Member" />
    <Sprite src={`${K}/furniture/stoolBar.png`}     x={500} y={260} width={38} visible={m >= 8} delay={0.04} />

    {/* ── m>=9: Awards on wall ── */}
    <Sprite src={`${K}/survival/signpost-single.png`} x={570} y={590} width={40} visible={m >= 9} delay={0} label="Award" />
    <Sprite src={`${K}/survival/signpost-single.png`} x={630} y={585} width={40} visible={m >= 9} delay={0.04} />
    <Sprite src={`${K}/furniture/lampSquareTable.png`} x={585} y={418} width={26} visible={m >= 9} delay={0.06} />

    {/* ── m>=10: Business sign + reference library ── */}
    <Sprite src={`${K}/survival/signpost.png`}           x={520} y={620} width={60} visible={m >= 10} delay={0} label="Business Sign" />
    <Sprite src={`${K}/furniture/bookcaseOpen.png`}      x={860} y={410} width={75} visible={m >= 10} delay={0.04} label="Reference Library" />
    <Sprite src={`${K}/furniture/bookcaseClosedWide.png`} x={920} y={405} width={85} visible={m >= 10} delay={0.06} />

    {/* ── m>=11: Full workspace ── */}
    <Sprite src={`${K}/furniture/desk.png`}           x={750} y={260} width={130} visible={m >= 11} delay={0} label="Second Workstation" />
    <Sprite src={`${K}/furniture/laptop.png`}         x={780} y={305} width={52}  visible={m >= 11} delay={0.03} />
    <Sprite src={`${K}/furniture/computerScreen.png`} x={830} y={310} width={42}  visible={m >= 11} delay={0.05} />
    <Sprite src={`${K}/furniture/chairDesk.png`}      x={780} y={240} width={52}  visible={m >= 11} delay={0.07} />
    <Sprite src={`${K}/furniture/pottedPlant.png`}    x={950} y={390} width={30}  visible={m >= 11} delay={0.09} />
    <Sprite src={`${K}/characters/character-c.png`}   x={310} y={240} width={50}  visible={m >= 11} delay={0.11} />

    {/* ── m>=12: Warm productive light ── */}
    <GoldenOverlay active={m >= 12} />
  </div>
);

export default memo(CareerIsoScene);
