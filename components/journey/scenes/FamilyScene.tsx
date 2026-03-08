/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import {
  Ground, House, Tree, Fence, Path, Mailbox, BBQGrill, Bicycle,
  Plant, WallArt, Mug, Lamp, Person, DiningTable, FruitBowl,
  WelcomeMat, FlowerBox, GardenGnome, BirdBath, StringLights,
  Balloons, Bunting, GoldenOverlay, SpringIn, COLORS,
} from './SharedSceneElements';

interface SceneProps {
  unlockedMilestones: number;
  personalMilestones: Set<number>;
}

const FamilyScene: React.FC<SceneProps> = ({ unlockedMilestones }) => {
  const m = unlockedMilestones;

  return (
    <group>
      {/* Grass ground */}
      <Ground color={COLORS.grass} size={[14, 12]} />

      {/* Garden path to house */}
      <Path position={[0, 0, 2.5]} width={0.6} length={4} />

      {/* House — centered */}
      <House position={[0, 0, 0]} />

      {/* Base fences */}
      <Fence position={[-4, 0, 3]} length={2.5} />
      <Fence position={[2.5, 0, 3]} length={2.5} />

      {/* m>=1: Welcome mat + mailbox */}
      {m >= 1 && (
        <SpringIn delay={0}>
          <WelcomeMat position={[0, 0, 1.2]} />
          <Mailbox position={[3, 0, 2]} />
        </SpringIn>
      )}

      {/* m>=2: Family photo + porch light */}
      {m >= 2 && (
        <SpringIn delay={0.05}>
          <WallArt position={[0.4, 1.4, 0.82]} width={0.2} height={0.15} frameColor="#8B6914" imageColor="#F5D7A0" />
          {/* Porch light */}
          <mesh position={[-0.6, 1.8, 0.82]}>
            <sphereGeometry args={[0.04, 5, 4]} />
            <meshStandardMaterial color="#FFF5D0" emissive="#FFF5D0" emissiveIntensity={0.2} />
          </mesh>
        </SpringIn>
      )}

      {/* m>=3: Trees + garden plants + flowers */}
      {m >= 3 && (
        <SpringIn delay={0.1}>
          <Tree position={[3, 0, 0.5]} size="large" seed={1} />
          <Tree position={[-3, 0, 1]} size="large" seed={2} />
          <Plant position={[2, 0, 1.5]} size="small" />
          <Plant position={[-2, 0, 1.8]} size="small" />
          {/* Flowers */}
          {[[2.5, 2], [2.8, 2.2], [2.6, 2.4]].map(([x, z], i) => (
            <mesh key={i} position={[x, 0.05, z]} castShadow>
              <sphereGeometry args={[0.04, 4, 4]} />
              <meshToonMaterial color={['#EF4444', '#F59E0B', '#A855F7'][i]} />
            </mesh>
          ))}
        </SpringIn>
      )}

      {/* m>=4: Outdoor dining */}
      {m >= 4 && (
        <SpringIn delay={0.15}>
          <DiningTable position={[-2.5, 0, 2.5]} chairs={4} />
          <FruitBowl position={[-2.5, 0.78, 2.5]} />
        </SpringIn>
      )}

      {/* m>=5: Window flower boxes + graduation cap */}
      {m >= 5 && (
        <SpringIn delay={0.2}>
          <FlowerBox position={[-0.6, 1.2, 0.86]} />
          <FlowerBox position={[0.6, 1.2, 0.86]} />
          {/* Graduation cap on wall inside */}
          <mesh position={[-0.2, 1.5, 0.82]} castShadow>
            <boxGeometry args={[0.12, 0.015, 0.12]} />
            <meshToonMaterial color="#1E1B4B" />
          </mesh>
        </SpringIn>
      )}

      {/* m>=6: More garden */}
      {m >= 6 && (
        <SpringIn delay={0.25}>
          <Plant position={[-3.5, 0, 2.5]} size="large" />
          <Tree position={[4.5, 0, 1]} size="small" seed={3} />
          {/* Garden border stones */}
          {[0, 1, 2, 3, 4].map((i) => (
            <mesh key={i} position={[1.5 + i * 0.25, 0.02, 2.5]} castShadow>
              <sphereGeometry args={[0.06, 4, 3]} />
              <meshStandardMaterial color={COLORS.stone} transparent opacity={0.6} />
            </mesh>
          ))}
        </SpringIn>
      )}

      {/* m>=7: Family + BBQ */}
      {m >= 7 && (
        <SpringIn delay={0.3}>
          <Person position={[3, 0, 2.5]} shirtColor={COLORS.fabric.navy} hairColor={COLORS.hair.brown} />
          <Person position={[3.5, 0, 2.2]} shirtColor={COLORS.fabric.red} hairColor={COLORS.hair.dark} />
          <Person position={[2.5, 0, 2.8]} shirtColor={COLORS.fabric.green} hairColor={COLORS.hair.blonde} />
          <BBQGrill position={[4, 0, 2.5]} />
        </SpringIn>
      )}

      {/* m>=8: Bicycles + mug */}
      {m >= 8 && (
        <SpringIn delay={0.35}>
          <Bicycle position={[-4, 0, 3.5]} />
          <Bicycle position={[-3.5, 0, 3.8]} />
          <Mug position={[-0.3, 0.01, 1.2]} color="#F5ECD7" steam />
        </SpringIn>
      )}

      {/* m>=9: String lights + more decor */}
      {m >= 9 && (
        <SpringIn delay={0.4}>
          <WallArt position={[0.6, 1.5, 0.82]} width={0.15} height={0.12} frameColor="#B8860B" imageColor="#7DD3FC" />
          <StringLights position={[0, 2.3, 0.9]} length={2.5} count={10} />
        </SpringIn>
      )}

      {/* m>=10: Garden features */}
      {m >= 10 && (
        <SpringIn delay={0.45}>
          <BirdBath position={[-2, 0, 1]} />
          <GardenGnome position={[2, 0, 3]} />
        </SpringIn>
      )}

      {/* m>=11: Party */}
      {m >= 11 && (
        <SpringIn delay={0.5}>
          <Person position={[-2, 0, 3.5]} shirtColor="#F97316" hairColor={COLORS.hair.dark} />
          <Person position={[-1.5, 0, 3.2]} shirtColor="#A855F7" hairColor={COLORS.hair.blonde} />
          <Person position={[-2.8, 0, 3.8]} shirtColor="#22C55E" hairColor={COLORS.hair.brown} />
          <Person position={[1, 0, 3.8]} shirtColor="#3B82F6" hairColor={COLORS.hair.dark} />
          <Bunting position={[0, 2.5, 0.85]} length={2.5} count={12} />
          <Balloons position={[-1.2, 1.5, 0.85]} />
          <Lamp position={[1.5, 0, 2.5]} variant="floor" on />
        </SpringIn>
      )}

      {/* m>=12: Golden glow */}
      <GoldenOverlay active={m >= 12} />
    </group>
  );
};

export default memo(FamilyScene);
