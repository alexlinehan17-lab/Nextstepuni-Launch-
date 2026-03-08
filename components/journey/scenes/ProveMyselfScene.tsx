/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { memo } from 'react';
import {
  Ground, Room, Desk, Chair, Lamp, Mug, PenHolder, Clock,
  Person, Stage, Podium, Trophy, WallSconce, WallArt,
  ExamPaper, ResultsBoard, FluorescentLight, Curtain,
  GoldenEnvelope, CelebrationBurst, GoldenOverlay, Noticeboard,
  COLORS,
} from './SharedSceneElements';

interface SceneProps {
  unlockedMilestones: number;
  personalMilestones: Set<number>;
}

const ProveMyselfScene: React.FC<SceneProps> = ({ unlockedMilestones }) => {
  const m = unlockedMilestones;

  return (
    <group>
      {/* Ground plane */}
      <Ground color={COLORS.cream} size={[12, 10]} />

      {/* Exam hall — long room */}
      <Room
        width={10}
        depth={8}
        wallHeight={3.5}
        floorColor={COLORS.parquet}
        wallColor={COLORS.white}
      />

      {/* Parquet floor lines */}
      {Array.from({ length: 8 }).map((_, i) => (
        <mesh key={i} position={[-4 + i * 1.1, 0.005, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[0.01, 8]} />
          <meshStandardMaterial color="#9A7A48" transparent opacity={0.15} flatShading />
        </mesh>
      ))}

      {/* Fluorescent ceiling lights */}
      {[-2.5, -0.5, 1.5, 3.5].map((x, i) => (
        <FluorescentLight key={i} position={[x, 3.4, -1]} />
      ))}

      {/* Large clock on back wall */}
      <Clock position={[0, 2.8, -3.95]} />

      {/* EXAM HALL sign */}
      <mesh position={[-2, 2.8, -3.95]}>
        <boxGeometry args={[0.5, 0.12, 0.02]} />
        <meshStandardMaterial color="#2C3E50" flatShading />
      </mesh>

      {/* Exit sign */}
      <mesh position={[3.5, 2.8, -3.95]}>
        <boxGeometry args={[0.25, 0.1, 0.02]} />
        <meshStandardMaterial color="#22AA22" transparent opacity={0.7} flatShading />
      </mesh>

      {/* Windows on side walls */}
      {[-3, 3].map((z, i) => (
        <group key={i}>
          <mesh position={[-4.95, 2.0, z]}>
            <boxGeometry args={[0.02, 0.5, 0.35]} />
            <meshStandardMaterial color={COLORS.glass} transparent opacity={0.3} flatShading />
          </mesh>
        </group>
      ))}

      {/* Notice board */}
      <Noticeboard position={[4, 2.0, -3.95]} />

      {/* m>=1: Desk + desk lamp */}
      {m >= 1 && (
        <group>
          <Desk position={[0, 0, 1.5]} />
          <Lamp position={[0.5, 0.76, 1.4]} variant="desk" on />
        </group>
      )}

      {/* m>=2: Exam paper, pen, mug */}
      {m >= 2 && (
        <group>
          <ExamPaper position={[-0.15, 0.76, 1.5]} />
          {/* Pen */}
          <mesh position={[0.15, 0.77, 1.6]} castShadow rotation={[0, 0.3, 0]}>
            <boxGeometry args={[0.12, 0.008, 0.01]} />
            <meshStandardMaterial color="#1A1A4E" flatShading />
          </mesh>
          <Mug position={[0.45, 0.76, 1.3]} />
          <PenHolder position={[-0.4, 0.76, 1.3]} />
        </group>
      )}

      {/* m>=3: Results board */}
      {m >= 3 && (
        <ResultsBoard position={[0, 2.2, -3.93]} strips={2} />
      )}

      {/* m>=4: More result strips */}
      {m >= 4 && (
        <ResultsBoard position={[0, 2.2, -3.92]} strips={4} />
      )}

      {/* m>=5: Full wall of results + star */}
      {m >= 5 && (
        <group>
          <ResultsBoard position={[0, 2.2, -3.91]} strips={8} />
          {/* Gold star */}
          <mesh position={[0, 2.65, -3.9]} castShadow>
            <coneGeometry args={[0.06, 0.1, 5]} />
            <meshStandardMaterial color={COLORS.goldBright} flatShading />
          </mesh>
        </group>
      )}

      {/* m>=6: More exam desks + floor lamps */}
      {m >= 6 && (
        <group>
          {[-2.5, -1.2, 1.2, 2.5].map((x, i) => (
            <group key={i}>
              <Desk position={[x, 0, 0]} width={1.0} />
              <Chair position={[x, 0, 0.7]} />
            </group>
          ))}
          <Lamp position={[-4, 0, -1]} variant="floor" on />
          <Lamp position={[4, 0, -1]} variant="floor" on />
        </group>
      )}

      {/* m>=7: Golden envelope */}
      {m >= 7 && (
        <GoldenEnvelope position={[0.2, 0.76, 1.5]} />
      )}

      {/* m>=8: Person standing */}
      {m >= 8 && (
        <group>
          <Person position={[0.8, 0, 2.2]} shirtColor="#1A1A4E" pantsColor="#2A2A3E" hairColor={COLORS.hair.dark} />
          <Chair position={[0, 0, 2.2]} />
        </group>
      )}

      {/* m>=9: Person at front + wall sconces */}
      {m >= 9 && (
        <group>
          <Person position={[0, 0, -1.5]} shirtColor="#1A1A4E" pantsColor="#2A2A3E" hairColor={COLORS.hair.brown} />
          {[-3, -1.5, 0].map((z, i) => (
            <WallSconce key={`l${i}`} position={[-4.93, 2.0, z]} on />
          ))}
          {[-3, -1.5, 0].map((z, i) => (
            <WallSconce key={`r${i}`} position={[4.93, 2.0, z]} on />
          ))}
        </group>
      )}

      {/* m>=10: Stage + podium + trophy + curtains */}
      {m >= 10 && (
        <group>
          <Stage position={[0, 0, -2.5]} width={4} depth={2} />
          <Podium position={[0, 0.3, -2.5]} />
          <Trophy position={[1.5, 0.3, -2.5]} />
          {/* Curtains */}
          <Curtain position={[-4.3, 0, -3.2]} height={3.2} side="left" />
          <Curtain position={[4.3, 0, -3.2]} height={3.2} side="right" />
          {/* Curtain rod */}
          <mesh position={[0, 3.2, -3.5]}>
            <boxGeometry args={[9, 0.02, 0.02]} />
            <meshStandardMaterial color={COLORS.gold} flatShading />
          </mesh>
        </group>
      )}

      {/* m>=11: Audience */}
      {m >= 11 && (
        <group>
          {/* Front row */}
          {[
            [-2.5, 0.5], [-1.2, 0.3], [0, 0.6], [1.2, 0.4], [2.5, 0.5], [3.5, 0.3],
          ].map(([x, z], i) => (
            <Person
              key={`a1-${i}`}
              position={[x, 0, z]}
              shirtColor={[COLORS.fabric.navy, COLORS.fabric.red, COLORS.fabric.green, '#8B6914', COLORS.fabric.purple, COLORS.fabric.navy][i]}
              hairColor={[COLORS.hair.dark, COLORS.hair.brown, COLORS.hair.blonde, COLORS.hair.dark, COLORS.hair.brown, COLORS.hair.blonde][i]}
            />
          ))}
          {/* Back row */}
          {[
            [-2, 1.5], [-0.5, 1.7], [1, 1.3], [2.5, 1.8], [3.8, 1.4],
          ].map(([x, z], i) => (
            <Person
              key={`a2-${i}`}
              position={[x, 0, z]}
              shirtColor={['#5A4A85', '#C09050', '#3A8B55', '#6B4A14', '#3A6B5A'][i]}
              hairColor={[COLORS.hair.brown, COLORS.hair.dark, COLORS.hair.blonde, COLORS.hair.brown, COLORS.hair.dark][i]}
            />
          ))}
          {/* Ushers */}
          <Person position={[-4, 0, -1]} shirtColor="#2C3E50" pantsColor="#1A1A2E" hairColor={COLORS.hair.dark} />
          <Person position={[4, 0, -1]} shirtColor="#2C3E50" pantsColor="#1A1A2E" hairColor={COLORS.hair.brown} />
        </group>
      )}

      {/* m>=12: Celebration confetti */}
      {m >= 12 && <CelebrationBurst position={[0, 3, -1]} />}

      <GoldenOverlay active={m >= 12} />
    </group>
  );
};

export default memo(ProveMyselfScene);
