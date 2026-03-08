/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import Sprite, { IsoGround, GoldenOverlay } from '../../IsometricSprite';

const K = '/assets/kenney';

interface SceneProps { unlockedMilestones: number; }

/**
 * Options-Freedom — Train Station to Airport
 * Empty platform → observation deck watching planes take off.
 */
const OptionsIsoScene: React.FC<SceneProps> = ({ unlockedMilestones: m }) => (
  <div style={{ position: 'absolute', inset: 0 }}>
    {/* ── Station ground (concrete/gray) ── */}
    <IsoGround color1="#B8B0A0" color2="#9A9080" />

    {/* ── Platform structure (always visible) ── */}
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={320} y={310} width={130} zIndex={8} />
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={440} y={310} width={130} zIndex={8} />
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={560} y={310} width={130} zIndex={8} />
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={680} y={310} width={130} zIndex={8} />
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={800} y={310} width={130} zIndex={8} />

    {/* ── Platform bench ── */}
    <Sprite src={`${K}/furniture/bench.png`} x={560} y={335} width={70} label="Platform Bench" />
    <Sprite src={`${K}/furniture/bench.png`} x={400} y={335} width={70} />

    {/* ── m>=1: Departure board ── */}
    <Sprite src={`${K}/survival/signpost.png`} x={460} y={400} width={60} visible={m >= 1} delay={0} label="Departure Board" />

    {/* ── m>=2: Backpack on bench ── */}
    <Sprite src={`${K}/survival/bedroll.png`} x={590} y={355} width={48} visible={m >= 2} delay={0} label="Backpack" />
    <Sprite src={`${K}/furniture/books.png`}  x={610} y={358} width={30} visible={m >= 2} delay={0.04} />

    {/* ── m>=3: Second platform ── */}
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={320} y={190} width={130} visible={m >= 3} delay={0} zIndex={7} />
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={440} y={190} width={130} visible={m >= 3} delay={0.02} zIndex={7} />
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={560} y={190} width={130} visible={m >= 3} delay={0.04} zIndex={7} />
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={680} y={190} width={130} visible={m >= 3} delay={0.06} zIndex={7} />
    <Sprite src={`${K}/buildings/buildingTiles_010.png`} x={800} y={190} width={130} visible={m >= 3} delay={0.08} zIndex={7} />
    <Sprite src={`${K}/furniture/bench.png`} x={500} y={215} width={65} visible={m >= 3} delay={0.1} />

    {/* ── m>=4: Board fills with destinations ── */}
    <Sprite src={`${K}/survival/signpost.png`}        x={540} y={405} width={60} visible={m >= 4} delay={0} label="More Destinations" />
    <Sprite src={`${K}/survival/signpost-single.png`} x={510} y={415} width={32} visible={m >= 4} delay={0.04} />

    {/* ── m>=5: Passport ── */}
    <Sprite src={`${K}/furniture/books.png`} x={640} y={355} width={28} visible={m >= 5} delay={0} label="Passport" />

    {/* ── m>=6: Station grows — bridge + signals ── */}
    <Sprite src={`${K}/nature/bridge_stone.png`}       x={410} y={260} width={100} visible={m >= 6} delay={0} label="Bridge" />
    <Sprite src={`${K}/nature/bridge_stone.png`}       x={580} y={260} width={100} visible={m >= 6} delay={0.04} />
    <Sprite src={`${K}/survival/signpost-single.png`}  x={310} y={250} width={32} visible={m >= 6} delay={0.06} label="Signal" />
    <Sprite src={`${K}/survival/signpost-single.png`}  x={870} y={250} width={32} visible={m >= 6} delay={0.08} label="Signal" />

    {/* ── m>=7: People appear ── */}
    <Sprite src={`${K}/characters/character-a.png`} x={470} y={340} width={48} visible={m >= 7} delay={0} label="Traveller" />
    <Sprite src={`${K}/characters/character-b.png`} x={700} y={335} width={48} visible={m >= 7} delay={0.03} />
    <Sprite src={`${K}/characters/character-c.png`} x={530} y={345} width={45} visible={m >= 7} delay={0.06} />
    <Sprite src={`${K}/characters/character-d.png`} x={780} y={340} width={45} visible={m >= 7} delay={0.09} />
    <Sprite src={`${K}/nature/tree_small.png`}      x={240} y={330} width={60} visible={m >= 7} delay={0.12} />
    <Sprite src={`${K}/nature/tree_small.png`}      x={930} y={325} width={55} visible={m >= 7} delay={0.14} />

    {/* ── m>=8: Airport terminal building ── */}
    <Sprite src={`${K}/buildings/building-type-e.png`}     x={370} y={530} width={260} visible={m >= 8} delay={0} label="Airport Terminal" />
    <Sprite src={`${K}/buildings/building-skyscraper-a.png`} x={250} y={560} width={110} visible={m >= 8} delay={0.05} label="Control Tower" />

    {/* ── m>=9: Terminal interior — check-in desks ── */}
    <Sprite src={`${K}/furniture/desk.png`}           x={390} y={445} width={105} visible={m >= 9} delay={0} label="Check-in" />
    <Sprite src={`${K}/furniture/desk.png`}           x={520} y={445} width={105} visible={m >= 9} delay={0.03} />
    <Sprite src={`${K}/furniture/desk.png`}           x={650} y={445} width={105} visible={m >= 9} delay={0.06} />
    <Sprite src={`${K}/furniture/computerScreen.png`} x={420} y={490} width={38}  visible={m >= 9} delay={0.09} />
    <Sprite src={`${K}/furniture/computerScreen.png`} x={550} y={490} width={38}  visible={m >= 9} delay={0.11} />
    <Sprite src={`${K}/furniture/computerScreen.png`} x={680} y={490} width={38}  visible={m >= 9} delay={0.13} />
    <Sprite src={`${K}/furniture/benchCushion.png`}   x={450} y={415} width={70}  visible={m >= 9} delay={0.15} label="Waiting Area" />
    <Sprite src={`${K}/furniture/benchCushion.png`}   x={580} y={415} width={70}  visible={m >= 9} delay={0.17} />

    {/* ── m>=10: Boarding passes ── */}
    <Sprite src={`${K}/furniture/books.png`}        x={475} y={435} width={26} visible={m >= 10} delay={0} label="Boarding Passes" />
    <Sprite src={`${K}/characters/character-e.png`} x={570} y={420} width={45} visible={m >= 10} delay={0.04} label="Traveller" />
    <Sprite src={`${K}/furniture/books.png`}        x={585} y={440} width={22} visible={m >= 10} delay={0.06} />

    {/* ── m>=11: Observation deck + planes ── */}
    <Sprite src={`${K}/buildings/building-type-a.png`}  x={650} y={570} width={190} visible={m >= 11} delay={0} label="Observation Deck" />
    <Sprite src={`${K}/vehicles/delivery.png`}          x={860} y={180} width={95}  visible={m >= 11} delay={0.04} label="Aircraft" />
    <Sprite src={`${K}/vehicles/truck.png`}             x={220} y={170} width={80}  visible={m >= 11} delay={0.08} label="Aircraft" />
    <Sprite src={`${K}/characters/character-f.png`}     x={700} y={580} width={42}  visible={m >= 11} delay={0.1} />
    <Sprite src={`${K}/characters/character-g.png`}     x={760} y={575} width={42}  visible={m >= 11} delay={0.12} />
    <Sprite src={`${K}/characters/character-h.png`}     x={820} y={178} width={42}  visible={m >= 11} delay={0.14} />

    {/* ── m>=12: World is yours ── */}
    <GoldenOverlay active={m >= 12} />
  </div>
);

export default memo(OptionsIsoScene);
