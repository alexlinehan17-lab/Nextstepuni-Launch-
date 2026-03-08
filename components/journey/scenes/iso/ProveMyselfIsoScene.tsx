/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import Sprite, { IsoGround, GoldenOverlay } from '../../IsometricSprite';

const K = '/assets/kenney';

interface SceneProps { unlockedMilestones: number; }

/**
 * Prove-Myself — Exam Hall to Stage
 * Lone desk at back → standing ovation on stage.
 */
const ProveMyselfIsoScene: React.FC<SceneProps> = ({ unlockedMilestones: m }) => (
  <div style={{ position: 'absolute', inset: 0 }}>
    {/* ── Exam hall floor ── */}
    <IsoGround color1="#D4C4A0" color2="#C0AD8A" />

    {/* ── Hall walls ── */}
    <Sprite src={`${K}/furniture/wall.png`}       x={240} y={520} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wall.png`}       x={355} y={520} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wallWindow.png`} x={470} y={520} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wall.png`}       x={585} y={520} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wallWindow.png`} x={700} y={520} width={135} zIndex={12} />
    <Sprite src={`${K}/furniture/wall.png`}       x={815} y={520} width={135} zIndex={12} />

    {/* ── m>=1: Desk at back of hall ── */}
    <Sprite src={`${K}/furniture/desk.png`}      x={520} y={250} width={130} visible={m >= 1} delay={0} label="Your Desk" />
    <Sprite src={`${K}/furniture/chairDesk.png`} x={555} y={220} width={52}  visible={m >= 1} delay={0.04} />

    {/* ── m>=2: Notes + pen + lamp ── */}
    <Sprite src={`${K}/furniture/books.png`}          x={545} y={295} width={40} visible={m >= 2} delay={0} label="Study Notes" />
    <Sprite src={`${K}/furniture/laptop.png`}         x={525} y={295} width={48} visible={m >= 2} delay={0.04} />
    <Sprite src={`${K}/furniture/lampRoundTable.png`} x={600} y={305} width={24} visible={m >= 2} delay={0.06} />

    {/* ── m>=3: First result on board ── */}
    <Sprite src={`${K}/survival/signpost-single.png`} x={430} y={620} width={40} visible={m >= 3} delay={0} label="Results Board" />

    {/* ── m>=4: Desk moves forward + more results ── */}
    <Sprite src={`${K}/furniture/desk.png`}            x={520} y={330} width={130} visible={m >= 4} delay={0} label="Front Desk" />
    <Sprite src={`${K}/furniture/chairDesk.png`}       x={555} y={300} width={52}  visible={m >= 4} delay={0.04} />
    <Sprite src={`${K}/survival/signpost-single.png`}  x={480} y={615} width={40}  visible={m >= 4} delay={0.06} />
    <Sprite src={`${K}/survival/signpost-single.png`}  x={530} y={618} width={40}  visible={m >= 4} delay={0.08} />

    {/* ── m>=5: Wall of results ── */}
    <Sprite src={`${K}/survival/signpost-single.png`} x={580} y={616} width={40} visible={m >= 5} delay={0} />
    <Sprite src={`${K}/survival/signpost-single.png`} x={630} y={614} width={40} visible={m >= 5} delay={0.03} />
    <Sprite src={`${K}/survival/signpost-single.png`} x={680} y={617} width={40} visible={m >= 5} delay={0.06} />
    <Sprite src={`${K}/furniture/lampRoundFloor.png`} x={270} y={380} width={24} visible={m >= 5} delay={0.08} />
    <Sprite src={`${K}/furniture/lampRoundFloor.png`} x={900} y={380} width={24} visible={m >= 5} delay={0.1} />

    {/* ── m>=6: More desks + chairs (front row) ── */}
    <Sprite src={`${K}/furniture/desk.png`}      x={320} y={300} width={120} visible={m >= 6} delay={0} />
    <Sprite src={`${K}/furniture/chairDesk.png`} x={350} y={270} width={48}  visible={m >= 6} delay={0.03} />
    <Sprite src={`${K}/furniture/desk.png`}      x={720} y={300} width={120} visible={m >= 6} delay={0.04} />
    <Sprite src={`${K}/furniture/chairDesk.png`} x={750} y={270} width={48}  visible={m >= 6} delay={0.07} />
    <Sprite src={`${K}/furniture/desk.png`}      x={320} y={230} width={115} visible={m >= 6} delay={0.08} />
    <Sprite src={`${K}/furniture/chairDesk.png`} x={348} y={200} width={45}  visible={m >= 6} delay={0.11} />
    <Sprite src={`${K}/furniture/desk.png`}      x={720} y={230} width={115} visible={m >= 6} delay={0.1} />
    <Sprite src={`${K}/furniture/chairDesk.png`} x={748} y={200} width={45}  visible={m >= 6} delay={0.13} />

    {/* ── m>=7: Golden envelope ── */}
    <Sprite src={`${K}/furniture/books.png`} x={545} y={375} width={42} visible={m >= 7} delay={0} label="Results Envelope" />

    {/* ── m>=8: Standing — person appears ── */}
    <Sprite src={`${K}/characters/character-a.png`} x={555} y={315} width={55} visible={m >= 8} delay={0} label="You" />

    {/* ── m>=9: Walking to front ── */}
    <Sprite src={`${K}/characters/character-a.png`}    x={545} y={420} width={58} visible={m >= 9} delay={0} label="Walking Forward" />
    <Sprite src={`${K}/furniture/lampSquareFloor.png`} x={260} y={450} width={24} visible={m >= 9} delay={0.04} />
    <Sprite src={`${K}/furniture/lampSquareFloor.png`} x={910} y={450} width={24} visible={m >= 9} delay={0.06} />

    {/* ── m>=10: Stage + podium ── */}
    <Sprite src={`${K}/furniture/desk.png`}      x={470} y={460} width={150} visible={m >= 10} delay={0} label="Stage" />
    <Sprite src={`${K}/survival/chest.png`}      x={640} y={460} width={55}  visible={m >= 10} delay={0.04} label="Trophy" />
    <Sprite src={`${K}/furniture/bookcaseOpen.png`} x={430} y={475} width={55} visible={m >= 10} delay={0.06} label="Podium" />

    {/* ── m>=11: Audience fills the hall ── */}
    {/* Front row */}
    <Sprite src={`${K}/characters/character-b.png`} x={340} y={340} width={42} visible={m >= 11} delay={0} />
    <Sprite src={`${K}/characters/character-c.png`} x={395} y={335} width={42} visible={m >= 11} delay={0.02} />
    <Sprite src={`${K}/characters/character-d.png`} x={450} y={340} width={42} visible={m >= 11} delay={0.04} />
    <Sprite src={`${K}/characters/character-e.png`} x={660} y={338} width={42} visible={m >= 11} delay={0.06} />
    <Sprite src={`${K}/characters/character-f.png`} x={715} y={335} width={42} visible={m >= 11} delay={0.08} />
    <Sprite src={`${K}/characters/character-g.png`} x={770} y={340} width={42} visible={m >= 11} delay={0.1} />
    {/* Back row */}
    <Sprite src={`${K}/characters/character-h.png`} x={310} y={270} width={40} visible={m >= 11} delay={0.12} />
    <Sprite src={`${K}/characters/character-i.png`} x={370} y={265} width={40} visible={m >= 11} delay={0.14} />
    <Sprite src={`${K}/characters/character-j.png`} x={430} y={268} width={40} visible={m >= 11} delay={0.16} />
    <Sprite src={`${K}/characters/character-k.png`} x={680} y={270} width={40} visible={m >= 11} delay={0.18} />
    <Sprite src={`${K}/characters/character-l.png`} x={740} y={266} width={40} visible={m >= 11} delay={0.2} />
    <Sprite src={`${K}/characters/character-m.png`} x={800} y={268} width={40} visible={m >= 11} delay={0.22} />

    {/* ── m>=12: Standing ovation ── */}
    <GoldenOverlay active={m >= 12} />
  </div>
);

export default memo(ProveMyselfIsoScene);
