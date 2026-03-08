/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import {
  Ground, Room, Desk, Bookshelf, Plant, WallArt, Mug, Lamp,
  Clock, Person, Laptop, PenHolder, Pegboard, EquipmentCabinet,
  Toolbox, GoldenOverlay, Star, COLORS,
} from './SharedSceneElements';

interface SceneProps {
  unlockedMilestones: number;
  personalMilestones: Set<number>;
}

const CareerScene: React.FC<SceneProps> = ({ unlockedMilestones }) => {
  const m = unlockedMilestones;

  return (
    <group>
      {/* Ground plane */}
      <Ground color={COLORS.cream} size={[12, 10]} />

      {/* Workshop room — wide industrial space */}
      <Room
        width={10}
        depth={7}
        wallHeight={3.2}
        floorColor={COLORS.concrete}
        wallColor="#E8DCC8"
      />

      {/* Exposed ceiling beams */}
      <mesh position={[0, 3.1, 0]} castShadow>
        <boxGeometry args={[9, 0.08, 0.08]} />
        <meshStandardMaterial color={COLORS.woodDark} flatShading />
      </mesh>
      <mesh position={[-4.5, 1.6, 0]}>
        <boxGeometry args={[0.08, 3.2, 0.08]} />
        <meshStandardMaterial color={COLORS.woodDark} flatShading />
      </mesh>
      <mesh position={[4.5, 1.6, 0]}>
        <boxGeometry args={[0.08, 3.2, 0.08]} />
        <meshStandardMaterial color={COLORS.woodDark} flatShading />
      </mesh>

      {/* Overhead conduit */}
      <mesh position={[0, 3.15, -1]}>
        <boxGeometry args={[8, 0.03, 0.03]} />
        <meshStandardMaterial color={COLORS.metal} flatShading />
      </mesh>

      {/* m>=1: Primary workbench */}
      {m >= 1 && (
        <group>
          <Desk position={[-1.5, 0, -2]} width={1.6} />
          {/* Rubber mat on desk */}
          <mesh position={[-1.5, 0.77, -2]} castShadow>
            <boxGeometry args={[1.2, 0.01, 0.5]} />
            <meshStandardMaterial color="#2A2A2A" transparent opacity={0.4} flatShading />
          </mesh>
        </group>
      )}

      {/* m>=2: Pegboard above workbench */}
      {m >= 2 && (
        <Pegboard position={[-1.5, 2.0, -3.45]} width={1.4} height={0.8} />
      )}

      {/* m>=3: Blueprint + drawing tools */}
      {m >= 3 && (
        <group>
          {/* Blueprint paper */}
          <mesh position={[-1.8, 0.78, -2]} castShadow>
            <boxGeometry args={[0.3, 0.005, 0.2]} />
            <meshStandardMaterial color="#B0D4F1" flatShading />
          </mesh>
          {/* Ruler */}
          <mesh position={[-1.2, 0.78, -2.1]} castShadow>
            <boxGeometry args={[0.25, 0.005, 0.03]} />
            <meshStandardMaterial color={COLORS.gold} flatShading />
          </mesh>
          <PenHolder position={[-0.8, 0.76, -2.2]} />
        </group>
      )}

      {/* m>=4: Second work table */}
      {m >= 4 && (
        <group>
          <Desk position={[2, 0, 0]} width={1.4} />
          {/* Workpieces */}
          <mesh position={[1.8, 0.78, 0]} castShadow>
            <boxGeometry args={[0.15, 0.1, 0.1]} />
            <meshStandardMaterial color="#CD853F" flatShading />
          </mesh>
          <mesh position={[2.2, 0.8, 0]} castShadow>
            <sphereGeometry args={[0.06, 6, 5]} />
            <meshStandardMaterial color={COLORS.gold} transparent opacity={0.7} flatShading />
          </mesh>
        </group>
      )}

      {/* m>=5: Mentor + pendant light */}
      {m >= 5 && (
        <group>
          <Person position={[-3.5, 0, 0.5]} shirtColor="#6B5B4F" pantsColor="#333333" hairColor={COLORS.hair.dark} />
          <Lamp position={[-1.5, 0, -3]} variant="floor" on />
          {/* Clipboard in mentor's area */}
          <mesh position={[-3.2, 0.6, 0.3]} castShadow>
            <boxGeometry args={[0.08, 0.12, 0.02]} />
            <meshStandardMaterial color="#6B4226" flatShading />
          </mesh>
        </group>
      )}

      {/* m>=6: Equipment cabinet + floor lamp + toolbox */}
      {m >= 6 && (
        <group>
          <EquipmentCabinet position={[-4, 0, 1]} />
          <Lamp position={[-4, 0, 2.2]} variant="floor" on />
          <Toolbox position={[-3.5, 0, 1.5]} />
          <Lamp position={[2, 0, -3]} variant="floor" on />
        </group>
      )}

      {/* m>=7: Display pedestal + clock */}
      {m >= 7 && (
        <group>
          {/* Pedestal */}
          <mesh position={[3.5, 0.5, -1.5]} castShadow>
            <boxGeometry args={[0.2, 1.0, 0.2]} />
            <meshStandardMaterial color={COLORS.woodDark} flatShading />
          </mesh>
          {/* Gold masterwork piece */}
          <mesh position={[3.5, 1.1, -1.5]} castShadow>
            <coneGeometry args={[0.1, 0.2, 5]} />
            <meshStandardMaterial color={COLORS.goldBright} flatShading />
          </mesh>
          <Clock position={[4.9, 2.2, -1]} />
        </group>
      )}

      {/* m>=8: Team member + second pegboard */}
      {m >= 8 && (
        <group>
          <Person position={[2.5, 0, 1.5]} shirtColor={COLORS.fabric.navy} pantsColor="#3A3A50" hairColor={COLORS.hair.blonde} />
          <Pegboard position={[4, 2.0, -3.45]} width={0.8} height={0.5} />
        </group>
      )}

      {/* m>=9: Award plaques + desk lamp */}
      {m >= 9 && (
        <group>
          <WallArt position={[2, 2.2, -3.45]} width={0.3} height={0.3} frameColor="#B5883A" imageColor="#F5E6C8" />
          <Star position={[2, 2.2, -3.4]} size={0.04} />
          <WallArt position={[1.2, 2.2, -3.45]} width={0.22} height={0.22} frameColor="#8B6914" imageColor="#E8D8B8" />
          <Lamp position={[-1.8, 0.76, -1.8]} variant="desk" on />
        </group>
      )}

      {/* m>=10: Business sign + bookshelf */}
      {m >= 10 && (
        <group>
          {/* Business sign above beams */}
          <mesh position={[0, 2.8, -3.45]} castShadow>
            <boxGeometry args={[1.4, 0.25, 0.04]} />
            <meshStandardMaterial color="#2C1810" flatShading />
          </mesh>
          <mesh position={[0, 2.8, -3.42]}>
            <boxGeometry args={[1.2, 0.18, 0.02]} />
            <meshStandardMaterial color="#F5E6C8" flatShading />
          </mesh>
          <Bookshelf position={[4, 0, 0.5]} variant="premium" />
        </group>
      )}

      {/* m>=11: Full workspace expansion */}
      {m >= 11 && (
        <group>
          <Desk position={[0.5, 0, -2]} width={1.4} color={COLORS.woodDark} />
          <Laptop position={[0.5, 0.76, -2]} />
          <Mug position={[1.2, 0.76, -1.8]} color="#C8B080" />
          <Plant position={[4.2, 0, 2]} size="large" />
          <Plant position={[-1, 0.76, -2.2]} size="small" />
          <WallArt position={[-3.5, 2.2, -3.45]} width={0.3} height={0.22} frameColor="#333333" imageColor="#E0D8C8" />
        </group>
      )}

      {/* m>=12: Warm productive glow */}
      <GoldenOverlay active={m >= 12} />
    </group>
  );
};

export default memo(CareerScene);
