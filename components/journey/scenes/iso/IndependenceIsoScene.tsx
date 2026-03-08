/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import Sprite, { IsoGround, GoldenOverlay } from '../../IsometricSprite';

const K = '/assets/kenney';

interface SceneProps { unlockedMilestones: number; }

/**
 * Independence — Studio Apartment
 * Empty room → fully furnished personal space.
 */
const IndependenceIsoScene: React.FC<SceneProps> = ({ unlockedMilestones: m }) => (
  <div style={{ position: 'absolute', inset: 0 }}>
    {/* ── Warm parquet floor diamond ── */}
    <IsoGround color1="#D4C4A0" color2="#B8A580" />

    {/* ── Back wall (always visible) ── */}
    <Sprite src={`${K}/furniture/wall.png`}         x={280} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wallWindow.png`}    x={395} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wall.png`}          x={510} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wallWindow.png`}    x={625} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wallDoorway.png`}   x={740} y={480} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wallCorner.png`}    x={855} y={480} width={135} zIndex={12} />

    {/* ── m>=1: Desk appears ── */}
    <Sprite src={`${K}/furniture/desk.png`}      x={320} y={380} width={140} visible={m >= 1} delay={0} label="Your Desk" />
    <Sprite src={`${K}/furniture/chairDesk.png`} x={370} y={340} width={55}  visible={m >= 1} delay={0.05} />

    {/* ── m>=2: Laptop + accessories on desk ── */}
    <Sprite src={`${K}/furniture/laptop.png`}    x={345} y={430} width={60}  visible={m >= 2} delay={0} label="Laptop" />
    <Sprite src={`${K}/furniture/books.png`}     x={410} y={425} width={50}  visible={m >= 2} delay={0.05} />
    <Sprite src={`${K}/furniture/lampRoundTable.png`} x={300} y={435} width={28} visible={m >= 2} delay={0.08} />

    {/* ── m>=3: Bookshelf against wall ── */}
    <Sprite src={`${K}/furniture/bookcaseOpen.png`}     x={260} y={420} width={80}  visible={m >= 3} delay={0} label="Bookshelf" />
    <Sprite src={`${K}/furniture/bookcaseClosedWide.png`} x={245} y={410} width={95} visible={m >= 3} delay={0.05} />

    {/* ── m>=4: Kitchen corner ── */}
    <Sprite src={`${K}/furniture/kitchenStove.png`}   x={750} y={400} width={110} visible={m >= 4} delay={0} label="Stove" />
    <Sprite src={`${K}/furniture/kitchenSink.png`}    x={840} y={400} width={100} visible={m >= 4} delay={0.05} label="Sink" />
    <Sprite src={`${K}/furniture/kitchenCabinet.png`} x={790} y={440} width={90}  visible={m >= 4} delay={0.08} />

    {/* ── m>=5: Art & personality ── */}
    <Sprite src={`${K}/furniture/lampWall.png`}     x={430} y={620} width={28} visible={m >= 5} delay={0} />
    <Sprite src={`${K}/furniture/lampWall.png`}     x={660} y={620} width={28} visible={m >= 5} delay={0.03} />
    <Sprite src={`${K}/furniture/plantSmall1.png`}  x={430} y={585} width={26} visible={m >= 5} delay={0.06} label="Window Plant" />
    <Sprite src={`${K}/furniture/plantSmall2.png`}  x={670} y={585} width={26} visible={m >= 5} delay={0.09} />

    {/* ── m>=6: Plants ── */}
    <Sprite src={`${K}/furniture/pottedPlant.png`}  x={890} y={380} width={32} visible={m >= 6} delay={0} label="Potted Plant" />
    <Sprite src={`${K}/furniture/pottedPlant.png`}  x={260} y={340} width={30} visible={m >= 6} delay={0.05} />
    <Sprite src={`${K}/furniture/plantSmall3.png`}  x={580} y={400} width={24} visible={m >= 6} delay={0.08} />

    {/* ── m>=7: Cozy living area ── */}
    <Sprite src={`${K}/furniture/rugRound.png`}          x={480} y={200} width={220} visible={m >= 7} delay={0} zIndex={15} />
    <Sprite src={`${K}/furniture/loungeSofa.png`}        x={500} y={230} width={170} visible={m >= 7} delay={0.05} label="Couch" />
    <Sprite src={`${K}/furniture/cabinetTelevision.png`} x={530} y={380} width={130} visible={m >= 7} delay={0.08} />
    <Sprite src={`${K}/furniture/televisionModern.png`}  x={555} y={420} width={85}  visible={m >= 7} delay={0.1} label="TV" />
    <Sprite src={`${K}/furniture/tableCoffee.png`}       x={530} y={280} width={110} visible={m >= 7} delay={0.12} label="Coffee Table" />
    <Sprite src={`${K}/furniture/pillow.png`}            x={520} y={250} width={32}  visible={m >= 7} delay={0.14} />
    <Sprite src={`${K}/furniture/pillowBlue.png`}        x={620} y={248} width={32}  visible={m >= 7} delay={0.14} />

    {/* ── m>=8: Car outside window ── */}
    <Sprite src={`${K}/vehicles/sedan.png`}  x={400} y={680} width={95} visible={m >= 8} delay={0} label="Your Car" />

    {/* ── m>=9: Full kitchen upgrade ── */}
    <Sprite src={`${K}/furniture/kitchenFridge.png`}       x={870} y={420} width={85}  visible={m >= 9} delay={0} label="Fridge" />
    <Sprite src={`${K}/furniture/kitchenMicrowave.png`}    x={810} y={460} width={60}  visible={m >= 9} delay={0.04} />
    <Sprite src={`${K}/furniture/kitchenCabinetDrawer.png`} x={750} y={450} width={80} visible={m >= 9} delay={0.06} />
    <Sprite src={`${K}/furniture/toaster.png`}             x={770} y={445} width={38}  visible={m >= 9} delay={0.08} />
    <Sprite src={`${K}/furniture/kitchenBlender.png`}      x={720} y={440} width={30}  visible={m >= 9} delay={0.1} />
    <Sprite src={`${K}/furniture/kitchenCoffeeMachine.png`} x={690} y={445} width={35} visible={m >= 9} delay={0.12} />

    {/* ── m>=10: Decorated space ── */}
    <Sprite src={`${K}/furniture/rugRectangle.png`}  x={280} y={260} width={200} visible={m >= 10} delay={0} zIndex={14} />
    <Sprite src={`${K}/furniture/lampRoundFloor.png`} x={470} y={310} width={28}  visible={m >= 10} delay={0.04} label="Floor Lamp" />
    <Sprite src={`${K}/furniture/lampSquareFloor.png`} x={710} y={280} width={28} visible={m >= 10} delay={0.06} />
    <Sprite src={`${K}/furniture/sideTable.png`}     x={460} y={270} width={60}  visible={m >= 10} delay={0.08} />
    <Sprite src={`${K}/furniture/radio.png`}         x={470} y={305} width={38}  visible={m >= 10} delay={0.1} />
    <Sprite src={`${K}/furniture/speaker.png`}       x={700} y={350} width={28}  visible={m >= 10} delay={0.12} />
    <Sprite src={`${K}/furniture/speakerSmall.png`}  x={700} y={370} width={22}  visible={m >= 10} delay={0.12} />

    {/* ── m>=11: Balcony with view ── */}
    <Sprite src={`${K}/nature/plant_bush.png`}   x={375} y={660} width={65} visible={m >= 11} delay={0} label="Balcony Garden" />
    <Sprite src={`${K}/nature/pot_small.png`}    x={450} y={650} width={40} visible={m >= 11} delay={0.05} />
    <Sprite src={`${K}/nature/flower_redA.png`}  x={340} y={665} width={45} visible={m >= 11} delay={0.08} />
    <Sprite src={`${K}/furniture/benchCushionLow.png`} x={360} y={640} width={80} visible={m >= 11} delay={0.1} />
    <Sprite src={`${K}/furniture/coatRackStanding.png`} x={870} y={340} width={35} visible={m >= 11} delay={0.12} />

    {/* ── m>=12: Golden hour light ── */}
    <GoldenOverlay active={m >= 12} />
  </div>
);

export default memo(IndependenceIsoScene);
