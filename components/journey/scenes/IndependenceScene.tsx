/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import {
  Ground, Room, Desk, Bookshelf, Sofa, Television, Table,
  KitchenCounter, Rug, Plant, WallArt, Mug, Lamp, Clock,
  BookStack, Person, Car, Cushion, Laptop, FruitBowl,
  PenHolder, WindowOpening, WallSconce, GoldenOverlay,
  COLORS,
} from './SharedSceneElements';

interface SceneProps {
  unlockedMilestones: number;
  personalMilestones: Set<number>;
}

const IndependenceScene: React.FC<SceneProps> = ({ unlockedMilestones }) => {
  const m = unlockedMilestones;

  return (
    <group>
      {/* Ground plane */}
      <Ground color={COLORS.cream} size={[12, 10]} />

      {/* Room shell — cross-section apartment */}
      <Room
        width={8}
        depth={6}
        wallHeight={3}
        floorColor={COLORS.parquet}
        wallColor={COLORS.white}
        accentWallColor="#E8DCC8"
      />

      {/* Windows on back wall */}
      <WindowOpening position={[-2, 2.0, -2.99]} width={0.6} height={0.5} />
      <WindowOpening position={[2, 2.0, -2.99]} width={0.6} height={0.5} />

      {/* m>=1: Desk */}
      {m >= 1 && (
        <Desk position={[-2.5, 0, -2]} />
      )}

      {/* m>=2: Desk accessories */}
      {m >= 2 && (
        <group>
          <Laptop position={[-2.5, 0.76, -2]} />
          <Mug position={[-1.8, 0.76, -1.8]} steam />
          <PenHolder position={[-3.0, 0.76, -2.1]} />
        </group>
      )}

      {/* m>=3: Bookshelf + photo frame */}
      {m >= 3 && (
        <group>
          <Bookshelf position={[-3.5, 0, -1]} variant={m >= 8 ? 'premium' : 'starter'} />
          <WallArt position={[-3.5, 2.0, -2.95]} width={0.25} height={0.2} frameColor="#5C3317" imageColor="#E8C8A0" />
        </group>
      )}

      {/* m>=4: Kitchen counter + fruit bowl */}
      {m >= 4 && (
        <group>
          <KitchenCounter position={[2.5, 0, -2]} variant="starter" />
          <FruitBowl position={[2.5, 0.94, -2]} />
        </group>
      )}

      {/* m>=5: Wall art + clock */}
      {m >= 5 && (
        <group>
          <WallArt position={[-0.5, 2.2, -2.95]} width={0.35} height={0.25} frameColor="#5C3317" imageColor="#C4956A" />
          <WallArt position={[0.5, 2.15, -2.95]} width={0.25} height={0.3} frameColor="#3A3A3A" imageColor="#6A8FA5" />
          <WallArt position={[1.5, 2.2, -2.95]} width={0.2} height={0.18} frameColor="#4A3820" imageColor="#A0C490" />
          <Clock position={[-3.94, 2.2, -1.5]} />
        </group>
      )}

      {/* m>=6: Plants + pendant lights */}
      {m >= 6 && (
        <group>
          <Plant position={[3.2, 0, -1.5]} size="small" />
          <Plant position={[-3.5, 0, 1.5]} size="large" />
          <Plant position={[-1.5, 0.76, -2.1]} size="small" />
          <Lamp position={[-1, 0, -2.5]} variant="floor" on={m >= 7} />
        </group>
      )}

      {/* m>=7: Living area — sofa, TV, coffee table, rug */}
      {m >= 7 && (
        <group>
          <Rug position={[1, 0, 1]} color="#B8A088" size={[2.5, 1.8]} />
          <Sofa position={[1, 0, 1.8]} />
          <Television position={[1, 0, -0.5]} />
          <Table position={[1, 0, 0.8]} size={[0.8, 0.5]} height={0.4} color={COLORS.wood} />
          <Lamp position={[-0.5, 0, 2]} variant="floor" on />
          <Lamp position={[2.8, 0, 2]} variant="floor" on />
          <Cushion position={[0.6, 0.44, 1.8]} color={COLORS.fabric.red} />
          <Cushion position={[1.4, 0.44, 1.75]} color={COLORS.fabric.navy} />
        </group>
      )}

      {/* m>=8: Car through window + desk lamp + book stack */}
      {m >= 8 && (
        <group>
          <Car position={[2.5, 0, -4.5]} color={m >= 10 ? '#2A2A2A' : COLORS.fabric.navy} />
          <Lamp position={[-3.0, 0.76, -1.9]} variant="desk" on />
          <BookStack position={[-3.5, 0.76, -2.2]} />
        </group>
      )}

      {/* m>=9: Kitchen upgrade + wall sconces */}
      {m >= 9 && (
        <group>
          <KitchenCounter position={[2.5, 0, -0.5]} variant="premium" />
          <Mug position={[2.5, 0.94, -0.5]} color="#F5F5F0" />
          <WallSconce position={[3.9, 2.0, -2]} on />
          <WallSconce position={[-3.94, 2.0, -2.5]} on />
          <Plant position={[3.2, 0, -0.3]} size="small" />
        </group>
      )}

      {/* m>=10: More wall art */}
      {m >= 10 && (
        <group>
          <WallArt position={[-3.94, 2.0, -0.5]} width={0.25} height={0.18} frameColor="#4A2810" imageColor="#7A9A5A" />
          <Plant position={[2.2, 0, 2]} size="small" />
        </group>
      )}

      {/* m>=11: Balcony extension with plant */}
      {m >= 11 && (
        <group>
          {/* Balcony platform extending through window */}
          <mesh position={[-2, 1.5, -3.5]} castShadow receiveShadow>
            <boxGeometry args={[1.2, 0.06, 0.6]} />
            <meshStandardMaterial color={COLORS.concrete} flatShading />
          </mesh>
          {/* Railing */}
          <mesh position={[-2, 1.7, -3.8]}>
            <boxGeometry args={[1.2, 0.04, 0.02]} />
            <meshStandardMaterial color={COLORS.metal} flatShading />
          </mesh>
          <Plant position={[-1.8, 1.53, -3.5]} size="small" />
        </group>
      )}

      {/* m>=12: Golden warm lighting overlay */}
      <GoldenOverlay active={m >= 12} />
    </group>
  );
};

export default memo(IndependenceScene);
