/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import {
  Ground, Platform, TrainTrack, Canopy, DepartureBoard, Backpack,
  Passport, Signal, Person, Tree, Building, OverheadBridge,
  Bench, PlaneShape, CheckInDesk, ObservationDeck,
  GoldenOverlay, COLORS,
} from './SharedSceneElements';

interface SceneProps {
  unlockedMilestones: number;
  personalMilestones: Set<number>;
}

const OptionsScene: React.FC<SceneProps> = ({ unlockedMilestones }) => {
  const m = unlockedMilestones;

  return (
    <group>
      {/* Ground */}
      <Ground color={COLORS.concrete} size={[14, 14]} />

      {/* Base: Platform + track + canopy */}
      <Platform position={[0, 0, -1]} width={5} depth={1.2} height={0.2} />
      <TrainTrack position={[-2.5, 0, 0.5]} length={5} />
      <Canopy position={[0, 0, -1]} width={4} depth={1.2} />

      {/* Bench on platform */}
      <Bench position={[1, 0.2, -1]} />

      {/* m>=1: Departure board */}
      {m >= 1 && (
        <DepartureBoard position={[-1, 0.2, -1]} />
      )}

      {/* m>=2: Backpack on bench */}
      {m >= 2 && (
        <Backpack position={[1.2, 0.45, -1]} />
      )}

      {/* m>=3: Second platform + track */}
      {m >= 3 && (
        <group>
          <Platform position={[0, 0, 2]} width={5} depth={1.0} height={0.2} />
          {/* Safety line */}
          <mesh position={[0, 0.21, 1.5]}>
            <boxGeometry args={[5, 0.01, 0.04]} />
            <meshStandardMaterial color={COLORS.gold} transparent opacity={0.6} flatShading />
          </mesh>
          <TrainTrack position={[-2.5, 0, 3.2]} length={5} />
        </group>
      )}

      {/* m>=4: Board fills with destinations */}
      {m >= 4 && (
        <DepartureBoard position={[-1, 0.2, -1]} filled />
      )}

      {/* m>=5: Passport */}
      {m >= 5 && (
        <Passport position={[1.5, 0.45, -0.9]} />
      )}

      {/* m>=6: Third track + overhead bridge + signals */}
      {m >= 6 && (
        <group>
          <TrainTrack position={[-2.5, 0, 4.5]} length={5} />
          <OverheadBridge position={[0, 0, 1.5]} width={5} />
          <Signal position={[-3, 0, 0.5]} color="green" />
          <Signal position={[3, 0, 0.5]} color="red" />
        </group>
      )}

      {/* m>=7: People + trees */}
      {m >= 7 && (
        <group>
          <Person position={[-1.5, 0.2, -0.8]} shirtColor={COLORS.fabric.navy} hairColor={COLORS.hair.dark} />
          <Person position={[2, 0.2, -0.6]} shirtColor={COLORS.fabric.red} hairColor={COLORS.hair.blonde} />
          <Person position={[0, 0.2, -1.2]} shirtColor={COLORS.fabric.green} hairColor={COLORS.hair.brown} />
          <Person position={[2.5, 0.2, -1.1]} shirtColor="#8B6914" hairColor={COLORS.hair.dark} />
          <Tree position={[-3.5, 0, -0.5]} size="small" seed={1} />
          <Tree position={[3.5, 0, -0.5]} size="small" seed={2} />
        </group>
      )}

      {/* m>=8: Airport terminal building */}
      {m >= 8 && (
        <Building
          position={[0, 0, -3.5]}
          width={5}
          height={2.0}
          depth={1.5}
          color={COLORS.white}
          windowColor={COLORS.glass}
        />
      )}

      {/* m>=9: Terminal interior — check-in desks + screens + seating */}
      {m >= 9 && (
        <group>
          {[-1.5, -0.5, 0.5, 1.5].map((x, i) => (
            <CheckInDesk key={i} position={[x, 0, -2.7]} />
          ))}
          {/* Seating rows */}
          {[-1.5, -0.8, -0.1, 1, 1.7, 2.4].map((x, i) => (
            <mesh key={i} position={[x, 0.25, -2.3]}>
              <boxGeometry args={[0.15, 0.06, 0.12]} />
              <meshStandardMaterial color={COLORS.metal} flatShading />
            </mesh>
          ))}
          {/* Info screens */}
          {[-1.2, 1.2].map((x, i) => (
            <group key={i}>
              <mesh position={[x, 1.6, -3.2]}>
                <boxGeometry args={[0.35, 0.2, 0.02]} />
                <meshStandardMaterial color="#1A2030" flatShading />
              </mesh>
              {/* Screen text lines */}
              <mesh position={[x - 0.05, 1.63, -3.19]}>
                <boxGeometry args={[0.2, 0.02, 0.005]} />
                <meshStandardMaterial color="#FFB030" transparent opacity={0.6} flatShading />
              </mesh>
              <mesh position={[x - 0.05, 1.59, -3.19]}>
                <boxGeometry args={[0.15, 0.02, 0.005]} />
                <meshStandardMaterial color="#80C0FF" transparent opacity={0.5} flatShading />
              </mesh>
            </group>
          ))}
        </group>
      )}

      {/* m>=10: Boarding passes + person reading */}
      {m >= 10 && (
        <group>
          {/* Boarding passes */}
          <mesh position={[1.2, 0.28, -2.3]} castShadow>
            <boxGeometry args={[0.08, 0.005, 0.05]} />
            <meshStandardMaterial color={COLORS.paper} flatShading />
          </mesh>
          <mesh position={[1.25, 0.285, -2.28]} castShadow>
            <boxGeometry args={[0.08, 0.005, 0.05]} />
            <meshStandardMaterial color={COLORS.gold} flatShading />
          </mesh>
          <Person position={[1.8, 0, -2.5]} shirtColor={COLORS.fabric.purple} hairColor={COLORS.hair.brown} />
          {/* Reading material */}
          <mesh position={[1.75, 0.6, -2.35]} castShadow>
            <boxGeometry args={[0.06, 0.08, 0.01]} />
            <meshStandardMaterial color="#2E4057" flatShading />
          </mesh>
        </group>
      )}

      {/* m>=11: Observation deck + planes on tarmac */}
      {m >= 11 && (
        <group>
          <ObservationDeck position={[0, 2, -3.5]} width={5} />

          {/* Planes */}
          <PlaneShape position={[3, 0, 5.5]} scale={1.2} />
          <PlaneShape position={[-2, 0, 6]} scale={0.8} />

          {/* People on observation deck */}
          <Person position={[-1, 2.06, -3.2]} shirtColor="#E67E22" hairColor={COLORS.hair.dark} />
          <Person position={[1, 2.06, -3.2]} shirtColor="#2980B9" hairColor={COLORS.hair.blonde} />
        </group>
      )}

      {/* m>=12: Sky gradient (warm ambient) + golden glow */}
      <GoldenOverlay active={m >= 12} />
    </group>
  );
};

export default memo(OptionsScene);
