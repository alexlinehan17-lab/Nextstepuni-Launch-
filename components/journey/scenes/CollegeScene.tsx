/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import {
  Ground, UniversityBuilding, Tree, Desk, Chair,
  Laptop, Person, Plant, BookStack, Mug, Lamp, WallArt,
  Bench, Path, Gate, Hedge, Stage, GoldenOverlay, GraduationCap,
  PenHolder, LampPost, COLORS,
} from './SharedSceneElements';

interface SceneProps {
  unlockedMilestones: number;
  personalMilestones: Set<number>;
}

const CollegeScene: React.FC<SceneProps> = ({ unlockedMilestones }) => {
  const m = unlockedMilestones;

  return (
    <group>
      {/* Grass ground */}
      <Ground color={COLORS.grass} size={[14, 14]} />

      {/* Path from gate to building */}
      <Path position={[0, 0, 1.5]} width={0.6} length={6} />

      {/* Main university building */}
      <UniversityBuilding position={[0, 0, -2]} />

      {/* Hedges along building */}
      <Hedge position={[-2, 0, -0.5]} width={0.8} />
      <Hedge position={[2, 0, -0.5]} width={0.8} />

      {/* Base trees */}
      <Tree position={[-3, 0, 1]} size="large" seed={1} />
      <Tree position={[3.5, 0, 0.5]} size="large" seed={2} />

      {/* Flower beds */}
      {[[-1, 1], [-1, 1.5], [1, 1], [1, 1.5]].map(([x, z], i) => (
        <mesh key={i} position={[x, 0.03, z]} castShadow>
          <sphereGeometry args={[0.05, 4, 4]} />
          <meshStandardMaterial color={[COLORS.fabric.red, '#E8A030', COLORS.fabric.navy, COLORS.fabric.purple][i]} flatShading />
        </mesh>
      ))}

      {/* Bench */}
      <Bench position={[2.5, 0, 2]} />

      {/* Small plants at entrance */}
      <Plant position={[-0.5, 0, -0.3]} size="small" />
      <Plant position={[0.5, 0, -0.3]} size="small" />

      {/* Crest */}
      <WallArt position={[0, 2.3, -0.87]} width={0.2} height={0.15} frameColor="#B5883A" imageColor="#1A3A6B" />

      {/* m>=1: Acceptance letter on bench */}
      {m >= 1 && (
        <group>
          <mesh position={[2.5, 0.45, 2]} castShadow>
            <boxGeometry args={[0.1, 0.005, 0.07]} />
            <meshStandardMaterial color={COLORS.paper} flatShading />
          </mesh>
          {/* Envelope */}
          <mesh position={[2.3, 0.45, 2.05]} castShadow>
            <boxGeometry args={[0.08, 0.005, 0.06]} />
            <meshStandardMaterial color={COLORS.gold} flatShading />
          </mesh>
        </group>
      )}

      {/* m>=2: Campus gates */}
      {m >= 2 && (
        <Gate position={[0, 0, 4.5]} />
      )}

      {/* m>=3: Dorm building */}
      {m >= 3 && (
        <group>
          {/* Small dorm building */}
          <mesh position={[4, 0.6, -1]} castShadow>
            <boxGeometry args={[1.2, 1.2, 1.0]} />
            <meshStandardMaterial color="#D2B48C" flatShading />
          </mesh>
          {/* Dorm cornice */}
          <mesh position={[4, 1.22, -1]}>
            <boxGeometry args={[1.3, 0.06, 1.1]} />
            <meshStandardMaterial color="#8B7355" flatShading />
          </mesh>
          {/* Dorm door */}
          <mesh position={[4, 0.35, -0.49]}>
            <boxGeometry args={[0.2, 0.5, 0.02]} />
            <meshStandardMaterial color={COLORS.woodDark} flatShading />
          </mesh>
          {/* Dorm windows */}
          <mesh position={[3.6, 0.8, -0.49]}>
            <boxGeometry args={[0.18, 0.15, 0.02]} />
            <meshStandardMaterial color={COLORS.glass} transparent opacity={0.5} flatShading />
          </mesh>
          <mesh position={[4.4, 0.8, -0.49]}>
            <boxGeometry args={[0.18, 0.15, 0.02]} />
            <meshStandardMaterial color={COLORS.glass} transparent opacity={0.5} flatShading />
          </mesh>
          <Plant position={[3.3, 0, -0.5]} size="small" />
        </group>
      )}

      {/* m>=4: Study bench with books */}
      {m >= 4 && (
        <group>
          <Bench position={[-3, 0, 2]} />
          <BookStack position={[-3.1, 0.45, 2]} />
          <BookStack position={[-2.9, 0.45, 2.1]} />
          <Tree position={[-3.5, 0, 1]} size="small" seed={3} />
        </group>
      )}

      {/* m>=5: Library wing */}
      {m >= 5 && (
        <group>
          <mesh position={[-3.5, 0.6, -1.5]} castShadow>
            <boxGeometry args={[1.5, 1.2, 1.0]} />
            <meshStandardMaterial color="#C8BCA0" flatShading />
          </mesh>
          <mesh position={[-3.5, 1.22, -1.5]}>
            <boxGeometry args={[1.6, 0.06, 1.1]} />
            <meshStandardMaterial color="#8B7355" flatShading />
          </mesh>
          {/* Library windows */}
          <mesh position={[-3.5, 0.7, -0.99]}>
            <boxGeometry args={[0.5, 0.45, 0.02]} />
            <meshStandardMaterial color={COLORS.glass} transparent opacity={0.35} flatShading />
          </mesh>
          {/* Library sign */}
          <mesh position={[-3.5, 1.05, -0.99]}>
            <boxGeometry args={[0.3, 0.08, 0.02]} />
            <meshStandardMaterial color="#1A3A6B" flatShading />
          </mesh>
        </group>
      )}

      {/* m>=6: Study group */}
      {m >= 6 && (
        <group>
          <Desk position={[-1.5, 0, 2.5]} width={1.0} />
          <Chair position={[-2, 0, 3.2]} />
          <Chair position={[-1, 0, 3.2]} />
          <Person position={[-2, 0, 3]} shirtColor={COLORS.fabric.navy} hairColor={COLORS.hair.dark} />
          <Person position={[-1, 0, 3]} shirtColor={COLORS.fabric.red} hairColor={COLORS.hair.blonde} />
          <Mug position={[-1.6, 0.76, 2.5]} />
          <Mug position={[-1.2, 0.76, 2.6]} color={COLORS.fabric.navy} />
        </group>
      )}

      {/* m>=7: Lecture hall block */}
      {m >= 7 && (
        <group>
          <mesh position={[3.5, 0.7, 2]} castShadow>
            <boxGeometry args={[2, 1.4, 1.5]} />
            <meshStandardMaterial color="#C8BCA0" flatShading />
          </mesh>
          {/* Lecture hall rows (visible through front) */}
          {[0, 0.3, 0.6].map((dz, i) => (
            <mesh key={i} position={[3.5, 0.2 + i * 0.15, 1.2 + dz]}>
              <boxGeometry args={[1.6, 0.04, 0.15]} />
              <meshStandardMaterial color={COLORS.woodDark} flatShading />
            </mesh>
          ))}
          {/* Blackboard */}
          <mesh position={[3.5, 0.7, 2.74]}>
            <boxGeometry args={[1.2, 0.5, 0.04]} />
            <meshStandardMaterial color={COLORS.blackboard} flatShading />
          </mesh>
        </group>
      )}

      {/* m>=8: Campus life */}
      {m >= 8 && (
        <group>
          <Person position={[1.5, 0, 2.5]} shirtColor="#3A6B35" hairColor={COLORS.hair.dark} />
          <Person position={[1.8, 0, 3]} shirtColor="#8B6914" hairColor={COLORS.hair.blonde} />
          <Person position={[1.2, 0, 3.2]} shirtColor={COLORS.fabric.purple} hairColor={COLORS.hair.brown} />
          <Tree position={[3.5, 0, 3.5]} size="large" seed={4} />
          <LampPost position={[1, 0, 3.5]} />
        </group>
      )}

      {/* m>=9: Research desk */}
      {m >= 9 && (
        <group>
          <Desk position={[-3, 0, 3.5]} width={1.2} color={COLORS.woodDark} />
          <Chair position={[-3, 0, 4.2]} />
          <Laptop position={[-2.8, 0.76, 3.5]} />
          <Lamp position={[-2.3, 0.76, 3.4]} variant="desk" on />
          <Mug position={[-3.3, 0.76, 3.6]} color="#8B2500" />
          <PenHolder position={[-3.4, 0.76, 3.3]} />
        </group>
      )}

      {/* m>=10: Thesis book */}
      {m >= 10 && (
        <group>
          {/* Gold-bound thesis */}
          <mesh position={[-2.9, 0.78, 3.2]} castShadow>
            <boxGeometry args={[0.1, 0.06, 0.12]} />
            <meshStandardMaterial color={COLORS.paper} flatShading />
          </mesh>
          <mesh position={[-2.9, 0.82, 3.2]} castShadow>
            <boxGeometry args={[0.11, 0.02, 0.13]} />
            <meshStandardMaterial color="#1A1A4E" flatShading />
          </mesh>
          {/* Gold lettering */}
          <mesh position={[-2.9, 0.835, 3.2]}>
            <boxGeometry args={[0.06, 0.005, 0.04]} />
            <meshStandardMaterial color={COLORS.gold} flatShading />
          </mesh>
        </group>
      )}

      {/* m>=11: Graduation */}
      {m >= 11 && (
        <group>
          <Stage position={[0, 0, -0.5]} width={3} depth={1.5} />
          <Person position={[0, 0.3, -0.5]} shirtColor="#1A1A2E" hairColor={COLORS.hair.dark} />
          <GraduationCap position={[0, 1.05, -0.5]} />
          {/* Audience */}
          <Person position={[-1.5, 0, 0.8]} shirtColor={COLORS.fabric.navy} hairColor={COLORS.hair.brown} />
          <Person position={[1.5, 0, 0.8]} shirtColor={COLORS.fabric.green} hairColor={COLORS.hair.blonde} />
          {/* Flowers */}
          {[0.15, 0, -0.15].map((dx, i) => (
            <mesh key={i} position={[1.8 + dx, 0.35, -0.5]} castShadow>
              <sphereGeometry args={[0.025, 4, 4]} />
              <meshStandardMaterial color={[COLORS.fabric.red, '#E8A030', COLORS.fabric.purple][i]} flatShading />
            </mesh>
          ))}
        </group>
      )}

      {/* m>=12: Golden glow */}
      <GoldenOverlay active={m >= 12} />
    </group>
  );
};

export default memo(CollegeScene);
