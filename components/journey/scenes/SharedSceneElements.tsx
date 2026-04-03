/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useRef, useMemo } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { useKenneyModel } from './models/useKenneyModel';
import { MODEL_CATALOG } from './models/modelCatalog';

/* ═══════════════════════════════════════════
   TOON GRADIENT TEXTURE — 3-band cell shading
   ═══════════════════════════════════════════ */

const toonGradientTexture = (() => {
  const data = new Uint8Array([60, 140, 255]); // shadow / mid / highlight
  const tex = new THREE.DataTexture(data, 3, 1, THREE.RedFormat);
  tex.minFilter = THREE.NearestFilter;
  tex.magFilter = THREE.NearestFilter;
  tex.needsUpdate = true;
  return tex;
})();

/* ═══════════════════════════════════════════
   COLOR PALETTE — Bold Crossy Road style
   ═══════════════════════════════════════════ */

export const COLORS = {
  wood: '#D4874E',
  woodDark: '#9B6B3D',
  woodLight: '#E8B878',
  white: '#FAFAF5',
  cream: '#F5ECD7',
  grass: '#58CC4E',
  grassDark: '#3DA835',
  stone: '#B8B8B0',
  stoneDark: '#8A8A82',
  concrete: '#C8C8C8',
  roof: '#E85D3A',
  roofDark: '#C04020',
  sky: '#4A90D9',
  metal: '#999999',
  metalDark: '#666666',
  fabric: {
    navy: '#3B82F6',
    red: '#EF4444',
    green: '#22C55E',
    cream: '#F5ECD7',
    purple: '#A855F7',
  },
  skin: '#FFBD80',
  hair: { dark: '#2D1B0E', brown: '#8B5E3C', blonde: '#FFD866' },
  paper: '#FEFCE8',
  gold: '#F59E0B',
  goldBright: '#FBBF24',
  screen: '#1E293B',
  glass: '#7DD3FC',
  curtainRed: '#DC2626',
  blackboard: '#1A3A2A',
  parquet: '#D4A76A',
};

/* Helper to create toon-shaded material */
const mat = (color: string) => (
  <meshToonMaterial color={color} gradientMap={toonGradientTexture} />
);

/* ═══════════════════════════════════════════
   SPRING-IN ANIMATION WRAPPER
   ═══════════════════════════════════════════ */

interface SpringInProps {
  children: React.ReactNode;
  delay?: number;
}

export const SpringIn: React.FC<SpringInProps> = ({ children, delay = 0 }) => {
  const ref = useRef<THREE.Group>(null);
  const state = useRef({ started: false, elapsed: 0, done: false });

  useFrame((_, dt) => {
    if (!ref.current || state.current.done) return;
    state.current.elapsed += dt;
    if (state.current.elapsed < delay) {
      ref.current.scale.setScalar(0.001);
      return;
    }
    if (!state.current.started) {
      state.current.started = true;
      state.current.elapsed = 0;
    }
    state.current.elapsed += dt;
    const t = Math.min(state.current.elapsed / 0.6, 1);
    // damped spring: overshoot then settle
    const s = 1 - Math.exp(-6 * t) * Math.cos(t * Math.PI * 2.5);
    const scale = t >= 1 ? 1 : Math.max(0.001, s);
    ref.current.scale.setScalar(scale);
    if (t >= 1) state.current.done = true;
  });

  return (
    <group ref={ref} scale={[0.001, 0.001, 0.001]}>
      {children}
    </group>
  );
};

/* ═══════════════════════════════════════════
   GROUND & STRUCTURE
   ═══════════════════════════════════════════ */

interface GroundProps {
  color?: string;
  size?: [number, number];
  position?: [number, number, number];
}

export const Ground: React.FC<GroundProps> = ({
  color = COLORS.cream,
  size = [12, 12],
  position = [0, -0.05, 0],
}) => (
  <mesh position={position} receiveShadow rotation={[-Math.PI / 2, 0, 0]}>
    <planeGeometry args={[size[0], size[1]]} />
    <meshToonMaterial color={color} gradientMap={toonGradientTexture} />
  </mesh>
);

interface RoomProps {
  width?: number;
  depth?: number;
  wallHeight?: number;
  floorColor?: string;
  wallColor?: string;
  accentWallColor?: string;
  position?: [number, number, number];
}

export const Room: React.FC<RoomProps> = ({
  width = 8,
  depth = 6,
  wallHeight = 3,
  floorColor = COLORS.parquet,
  wallColor = COLORS.white,
  accentWallColor,
  position = [0, 0, 0],
}) => (
  <group position={position}>
    {/* Floor */}
    <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
      <planeGeometry args={[width, depth]} />
      <meshToonMaterial color={floorColor} gradientMap={toonGradientTexture} />
    </mesh>
    {/* Back wall */}
    <mesh position={[0, wallHeight / 2, -depth / 2]} castShadow receiveShadow>
      <boxGeometry args={[width, wallHeight, 0.1]} />
      <meshToonMaterial color={accentWallColor || wallColor} gradientMap={toonGradientTexture} />
    </mesh>
    {/* Left wall */}
    <mesh position={[-width / 2, wallHeight / 2, 0]} castShadow receiveShadow>
      <boxGeometry args={[0.1, wallHeight, depth]} />
      <meshToonMaterial color={wallColor} gradientMap={toonGradientTexture} />
    </mesh>
  </group>
);

interface WallProps {
  width?: number;
  height?: number;
  depth?: number;
  color?: string;
  position?: [number, number, number];
}

export const Wall: React.FC<WallProps> = ({
  width = 4,
  height = 3,
  depth = 0.1,
  color = COLORS.white,
  position = [0, 0, 0],
}) => (
  <mesh position={[position[0], position[1] + height / 2, position[2]]} castShadow receiveShadow>
    <boxGeometry args={[width, height, depth]} />
    {mat(color)}
  </mesh>
);

/* ═══════════════════════════════════════════
   FURNITURE
   ═══════════════════════════════════════════ */

interface DeskProps {
  position?: [number, number, number];
  color?: string;
  width?: number;
}

export const Desk: React.FC<DeskProps> = ({
  position = [0, 0, 0],
  color = COLORS.wood,
  width = 1.4,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.desk.path, { colorOverride: color });
  const s = MODEL_CATALOG.desk.scale * (width / 1.4);
  return (
    <group position={position} scale={[s, MODEL_CATALOG.desk.scale, MODEL_CATALOG.desk.scale]}>
      <primitive object={scene} />
    </group>
  );
};

interface ChairProps {
  position?: [number, number, number];
  color?: string;
}

export const Chair: React.FC<ChairProps> = ({
  position = [0, 0, 0],
  color = COLORS.wood,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.chair.path, { colorOverride: color });
  const s = MODEL_CATALOG.chair.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface BookshelfProps {
  position?: [number, number, number];
  variant?: 'starter' | 'premium';
}

export const Bookshelf: React.FC<BookshelfProps> = ({
  position = [0, 0, 0],
  variant = 'starter',
}) => {
  const modelKey = variant === 'premium' ? 'bookshelfLarge' : 'bookshelf';
  const entry = MODEL_CATALOG[modelKey];
  const scene = useKenneyModel(entry.path);
  const s = entry.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface SofaProps {
  position?: [number, number, number];
  color?: string;
}

export const Sofa: React.FC<SofaProps> = ({
  position = [0, 0, 0],
  color = COLORS.fabric.navy,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.couch.path, { colorOverride: color });
  const s = MODEL_CATALOG.couch.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface TableProps {
  position?: [number, number, number];
  size?: [number, number];
  height?: number;
  color?: string;
}

export const Table: React.FC<TableProps> = ({
  position = [0, 0, 0],
  size = [0.8, 0.5],
  height = 0.4,
  color = COLORS.wood,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.tableCoffee.path, { colorOverride: color });
  const baseScale = MODEL_CATALOG.tableCoffee.scale;
  const sx = baseScale * (size[0] / 0.8);
  const sy = baseScale * (height / 0.4);
  const sz = baseScale * (size[1] / 0.5);
  return (
    <group position={position} scale={[sx, sy, sz]}>
      <primitive object={scene} />
    </group>
  );
};

interface TelevisionProps {
  position?: [number, number, number];
}

export const Television: React.FC<TelevisionProps> = ({
  position = [0, 0, 0],
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.tv.path);
  const s = MODEL_CATALOG.tv.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface KitchenCounterProps {
  position?: [number, number, number];
  variant?: 'starter' | 'premium';
}

export const KitchenCounter: React.FC<KitchenCounterProps> = ({
  position = [0, 0, 0],
  variant = 'starter',
}) => {
  const modelKey = variant === 'premium' ? 'kitchenCounterPremium' : 'kitchenCounter';
  const entry = MODEL_CATALOG[modelKey];
  const scene = useKenneyModel(entry.path);
  const s = entry.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface RugProps {
  position?: [number, number, number];
  color?: string;
  size?: [number, number];
}

export const Rug: React.FC<RugProps> = ({
  position = [0, 0, 0],
  color = '#C8956A',
  size = [2, 1.4],
}) => (
  <mesh position={[position[0], 0.01, position[2]]} receiveShadow rotation={[-Math.PI / 2, 0, 0]}>
    <planeGeometry args={[size[0], size[1]]} />
    <meshToonMaterial color={color} gradientMap={toonGradientTexture} />
  </mesh>
);

/* ═══════════════════════════════════════════
   DECOR
   ═══════════════════════════════════════════ */

interface PlantProps {
  position?: [number, number, number];
  size?: 'small' | 'large';
  seed?: number;
}

export const Plant: React.FC<PlantProps> = ({
  position = [0, 0, 0],
  size = 'small',
}) => {
  const modelKey = size === 'large' ? 'plantPotLarge' : 'plantPot';
  const entry = MODEL_CATALOG[modelKey];
  const scene = useKenneyModel(entry.path);
  const s = entry.scale;
  const ref = useRef<THREE.Group>(null);

  // Breathing / pulse animation
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime();
    const pulse = 1 + Math.sin(t * 2.5 + (position?.[0] ?? 0) * 3) * 0.04;
    ref.current.scale.setScalar(s * pulse);
  });

  return (
    <group position={position}>
      <group ref={ref} scale={[s, s, s]}>
        <primitive object={scene} />
      </group>
    </group>
  );
};

interface TreeProps {
  position?: [number, number, number];
  size?: 'small' | 'large';
  seed?: number;
  canopyColor?: string;
}

export const Tree: React.FC<TreeProps> = ({
  position = [0, 0, 0],
  size = 'large',
  seed = 0,
  canopyColor = '#3DA835',
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.treeOak.path, { colorOverride: canopyColor });
  const baseScale = MODEL_CATALOG.treeOak.scale;
  const s = baseScale * (size === 'large' ? 1.0 : 0.6);
  const ref = useRef<THREE.Group>(null);

  // Canopy sway animation — unique per tree via seed
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime();
    ref.current.rotation.z = Math.sin(t * 1.2 + seed * 2.7) * 0.04;
    ref.current.rotation.x = Math.sin(t * 0.9 + seed * 1.3) * 0.03;
  });

  return (
    <group position={position}>
      <group ref={ref} scale={[s, s, s]}>
        <primitive object={scene} />
      </group>
    </group>
  );
};

interface WallArtProps {
  position?: [number, number, number];
  width?: number;
  height?: number;
  frameColor?: string;
  imageColor?: string;
}

export const WallArt: React.FC<WallArtProps> = ({
  position = [0, 0, 0],
  width = 0.5,
  height = 0.4,
  frameColor = '#2D1B0E',
  imageColor = '#D4874E',
}) => (
  <group position={position}>
    <mesh castShadow>
      <boxGeometry args={[width + 0.04, height + 0.04, 0.03]} />
      {mat(frameColor)}
    </mesh>
    <mesh position={[0, 0, 0.02]}>
      <boxGeometry args={[width, height, 0.01]} />
      {mat(imageColor)}
    </mesh>
  </group>
);

interface MugProps {
  position?: [number, number, number];
  color?: string;
  steam?: boolean;
}

export const Mug: React.FC<MugProps> = ({
  position = [0, 0, 0],
  color = COLORS.white,
  steam = false,
}) => (
  <group position={position}>
    <mesh position={[0, 0.06, 0]} castShadow>
      <cylinderGeometry args={[0.04, 0.035, 0.12, 6]} />
      {mat(color)}
    </mesh>
    {/* Handle */}
    <mesh position={[0.05, 0.06, 0]} castShadow>
      <torusGeometry args={[0.025, 0.008, 4, 6, Math.PI]} />
      {mat(color)}
    </mesh>
    {steam && <SteamParticles position={[0, 0.14, 0]} />}
  </group>
);

const SteamParticles: React.FC<{ position: [number, number, number] }> = ({ position }) => {
  const ref = useRef<THREE.Group>(null);
  useFrame((_, dt) => {
    if (ref.current) {
      ref.current.children.forEach((c) => {
        c.position.y += dt * 0.15;
        if ((c as THREE.Mesh).material) { (c as any).material.opacity = Math.max(0, 0.4 - c.position.y * 1.5); }
        if (c.position.y > 0.3) c.position.y = 0;
      });
    }
  });
  return (
    <group position={position} ref={ref}>
      {[0, 0.1, 0.2].map((y, i) => (
        <mesh key={i} position={[(i - 1) * 0.01, y, 0]}>
          <sphereGeometry args={[0.012, 4, 4]} />
          <meshStandardMaterial color="#FFFFFF" transparent opacity={0.3} />
        </mesh>
      ))}
    </group>
  );
};

interface LampProps {
  position?: [number, number, number];
  on?: boolean;
  variant?: 'floor' | 'desk';
}

export const Lamp: React.FC<LampProps> = ({
  position = [0, 0, 0],
  on = true,
  variant = 'floor',
}) => {
  const modelKey = variant === 'floor' ? 'lampFloor' : 'lampDesk';
  const entry = MODEL_CATALOG[modelKey];
  const scene = useKenneyModel(entry.path);
  const s = entry.scale;
  const h = variant === 'floor' ? 1.5 : 0.5;
  return (
    <group position={position}>
      <group scale={[s, s, s]}>
        <primitive object={scene} />
      </group>
      {on && (
        <pointLight
          position={[0, h - 0.1, 0]}
          intensity={0.3}
          distance={2}
          color="#FFF5D0"
        />
      )}
    </group>
  );
};

interface ClockProps {
  position?: [number, number, number];
}

export const Clock: React.FC<ClockProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh castShadow>
      <cylinderGeometry args={[0.12, 0.12, 0.03, 8]} />
      {mat(COLORS.white)}
    </mesh>
    {/* Rim */}
    <mesh>
      <torusGeometry args={[0.12, 0.01, 4, 8]} />
      {mat('#333333')}
    </mesh>
  </group>
);

interface BookStackProps {
  position?: [number, number, number];
}

export const BookStack: React.FC<BookStackProps> = ({
  position = [0, 0, 0],
}) => {
  const colors = ['#DC2626', '#3B82F6', '#22C55E'];
  return (
    <group position={position}>
      {colors.map((c, i) => (
        <mesh key={i} position={[0, 0.025 + i * 0.05, 0]} castShadow>
          <boxGeometry args={[0.16, 0.04, 0.1]} />
          {mat(c)}
        </mesh>
      ))}
    </group>
  );
};

/* ═══════════════════════════════════════════
   PEOPLE — Crossy Road style with bob animation
   ═══════════════════════════════════════════ */

interface PersonProps {
  position?: [number, number, number];
  shirtColor?: string;
  pantsColor?: string;
  hairColor?: string;
  rotation?: number;
}

export const Person: React.FC<PersonProps> = ({
  position = [0, 0, 0],
  shirtColor = COLORS.fabric.navy,
  pantsColor = '#333344',
  hairColor = COLORS.hair.dark,
  rotation = 0,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.characterA.path, {
    colorOverride: shirtColor,
  });
  const s = MODEL_CATALOG.characterA.scale;
  const ref = useRef<THREE.Group>(null);

  // Bob up/down animation — unique per position
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime();
    const seed = (position?.[0] ?? 0) * 5 + (position?.[2] ?? 0) * 3;
    ref.current.position.y = Math.sin(t * 2.2 + seed) * 0.025;
  });

  return (
    <group position={position}>
      <group ref={ref} rotation={[0, rotation, 0]} scale={[s, s, s]}>
        <primitive object={scene} />
      </group>
    </group>
  );
};

/* ═══════════════════════════════════════════
   OUTDOOR
   ═══════════════════════════════════════════ */

interface HouseProps {
  position?: [number, number, number];
  wallColor?: string;
  roofColor?: string;
}

export const House: React.FC<HouseProps> = ({
  position = [0, 0, 0],
  wallColor = COLORS.cream,
  roofColor = COLORS.roof,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.house.path, { colorOverride: wallColor });
  const s = MODEL_CATALOG.house.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface FenceProps {
  position?: [number, number, number];
  length?: number;
  color?: string;
}

export const Fence: React.FC<FenceProps> = ({
  position = [0, 0, 0],
  length = 3,
  color = COLORS.white,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.fenceSection.path, { colorOverride: color });
  const s = MODEL_CATALOG.fenceSection.scale;
  // Tile fence sections to fill the requested length
  // Assume each fence section model is ~1 unit wide at scale=1
  const sectionWidth = 1.0 * s;
  const sections = Math.max(1, Math.round(length / sectionWidth));
  return (
    <group position={position}>
      {Array.from({ length: sections }).map((_, i) => (
        <group key={i} position={[i * sectionWidth, 0, 0]} scale={[s, s, s]}>
          <primitive object={scene.clone()} />
        </group>
      ))}
    </group>
  );
};

interface PathProps {
  position?: [number, number, number];
  width?: number;
  length?: number;
  color?: string;
}

export const Path: React.FC<PathProps> = ({
  position = [0, 0, 0],
  width = 0.6,
  length = 3,
  color = '#E8D8A8',
}) => (
  <mesh position={[position[0], 0.01, position[2]]} receiveShadow rotation={[-Math.PI / 2, 0, 0]}>
    <planeGeometry args={[width, length]} />
    <meshToonMaterial color={color} gradientMap={toonGradientTexture} />
  </mesh>
);

interface CarProps {
  position?: [number, number, number];
  color?: string;
}

export const Car: React.FC<CarProps> = ({
  position = [0, 0, 0],
  color = COLORS.fabric.navy,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.sedan.path, { colorOverride: color });
  const s = MODEL_CATALOG.sedan.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface MailboxProps {
  position?: [number, number, number];
}

export const Mailbox: React.FC<MailboxProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 0.4, 0]} castShadow>
      <cylinderGeometry args={[0.025, 0.025, 0.8, 6]} />
      {mat(COLORS.woodDark)}
    </mesh>
    <mesh position={[0, 0.85, 0]} castShadow>
      <boxGeometry args={[0.18, 0.14, 0.12]} />
      {mat(COLORS.fabric.red)}
    </mesh>
  </group>
);

interface BBQGrillProps {
  position?: [number, number, number];
}

export const BBQGrill: React.FC<BBQGrillProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    {/* Body */}
    <mesh position={[0, 0.5, 0]} castShadow>
      <cylinderGeometry args={[0.2, 0.2, 0.15, 8]} />
      {mat('#2A2A2A')}
    </mesh>
    {/* Legs */}
    {[-0.12, 0.12].map((lx, i) => (
      <mesh key={i} position={[lx, 0.21, 0]} castShadow>
        <cylinderGeometry args={[0.02, 0.02, 0.42, 6]} />
        {mat(COLORS.metal)}
      </mesh>
    ))}
    {/* Lid handle */}
    <mesh position={[0, 0.6, 0]} castShadow>
      <cylinderGeometry args={[0.04, 0.04, 0.02, 6]} />
      {mat(COLORS.metal)}
    </mesh>
  </group>
);

interface BicycleProps {
  position?: [number, number, number];
  color?: string;
}

export const Bicycle: React.FC<BicycleProps> = ({
  position = [0, 0, 0],
  color = COLORS.fabric.red,
}) => (
  <group position={position}>
    {/* Wheels */}
    {[-0.2, 0.2].map((wx, i) => (
      <mesh key={i} position={[wx, 0.12, 0]} rotation={[Math.PI / 2, 0, 0]} castShadow>
        <torusGeometry args={[0.1, 0.015, 4, 8]} />
        {mat('#2A2A2A')}
      </mesh>
    ))}
    {/* Frame */}
    <mesh position={[0, 0.18, 0]} castShadow rotation={[0, 0, 0.3]}>
      <boxGeometry args={[0.35, 0.02, 0.02]} />
      {mat(color)}
    </mesh>
    <mesh position={[0, 0.22, 0]} castShadow>
      <boxGeometry args={[0.1, 0.02, 0.02]} />
      {mat(color)}
    </mesh>
    {/* Seat */}
    <mesh position={[-0.05, 0.28, 0]} castShadow>
      <boxGeometry args={[0.06, 0.02, 0.04]} />
      {mat('#2A2A2A')}
    </mesh>
    {/* Handlebars */}
    <mesh position={[0.15, 0.28, 0]} castShadow>
      <boxGeometry args={[0.02, 0.06, 0.1]} />
      {mat(COLORS.metal)}
    </mesh>
  </group>
);

/* ═══════════════════════════════════════════
   SCENE-SPECIFIC
   ═══════════════════════════════════════════ */

interface BuildingProps {
  position?: [number, number, number];
  width?: number;
  height?: number;
  depth?: number;
  color?: string;
  windowColor?: string;
}

export const Building: React.FC<BuildingProps> = ({
  position = [0, 0, 0],
  width = 3,
  height = 2.5,
  depth = 2,
  color = COLORS.cream,
  windowColor = COLORS.glass,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.buildingOffice.path, { colorOverride: color });
  const baseScale = MODEL_CATALOG.buildingOffice.scale;
  const sx = baseScale * (width / 3);
  const sy = baseScale * (height / 2.5);
  const sz = baseScale * (depth / 2);
  return (
    <group position={position} scale={[sx, sy, sz]}>
      <primitive object={scene} />
    </group>
  );
};

interface UniversityBuildingProps {
  position?: [number, number, number];
}

export const UniversityBuilding: React.FC<UniversityBuildingProps> = ({
  position = [0, 0, 0],
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.buildingUniversity.path);
  const s = MODEL_CATALOG.buildingUniversity.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface TrainTrackProps {
  position?: [number, number, number];
  length?: number;
}

export const TrainTrack: React.FC<TrainTrackProps> = ({
  position = [0, 0, 0],
  length = 5,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.trackStraight.path);
  const s = MODEL_CATALOG.trackStraight.scale;
  // Tile track sections to fill the requested length
  const sectionWidth = 1.0 * s;
  const sections = Math.max(1, Math.round(length / sectionWidth));
  return (
    <group position={position}>
      {Array.from({ length: sections }).map((_, i) => (
        <group key={i} position={[i * sectionWidth, 0, 0]} scale={[s, s, s]}>
          <primitive object={scene.clone()} />
        </group>
      ))}
    </group>
  );
};

interface PlatformProps {
  position?: [number, number, number];
  width?: number;
  depth?: number;
  height?: number;
  color?: string;
}

export const Platform: React.FC<PlatformProps> = ({
  position = [0, 0, 0],
  width = 4,
  depth = 1,
  height = 0.2,
  color = COLORS.concrete,
}) => (
  <mesh position={[position[0], height / 2, position[2]]} castShadow receiveShadow>
    <boxGeometry args={[width, height, depth]} />
    {mat(color)}
  </mesh>
);

interface StageProps {
  position?: [number, number, number];
  width?: number;
  depth?: number;
}

export const Stage: React.FC<StageProps> = ({
  position = [0, 0, 0],
  width = 3,
  depth = 2,
}) => (
  <group position={position}>
    {/* Platform */}
    <mesh position={[0, 0.15, 0]} castShadow receiveShadow>
      <boxGeometry args={[width, 0.3, depth]} />
      {mat(COLORS.woodDark)}
    </mesh>
    {/* Front trim */}
    <mesh position={[0, 0.15, depth / 2 + 0.02]}>
      <boxGeometry args={[width, 0.3, 0.03]} />
      {mat(COLORS.wood)}
    </mesh>
  </group>
);

interface PodiumProps {
  position?: [number, number, number];
}

export const Podium: React.FC<PodiumProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 0.5, 0]} castShadow>
      <boxGeometry args={[0.4, 1.0, 0.3]} />
      {mat(COLORS.woodDark)}
    </mesh>
    {/* Top surface */}
    <mesh position={[0, 1.02, 0]} castShadow>
      <boxGeometry args={[0.44, 0.03, 0.34]} />
      {mat(COLORS.wood)}
    </mesh>
  </group>
);

interface TrophyProps {
  position?: [number, number, number];
}

export const Trophy: React.FC<TrophyProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    {/* Base */}
    <mesh position={[0, 0.04, 0]} castShadow>
      <boxGeometry args={[0.12, 0.08, 0.08]} />
      {mat('#2A2A2A')}
    </mesh>
    {/* Stem */}
    <mesh position={[0, 0.15, 0]} castShadow>
      <cylinderGeometry args={[0.015, 0.015, 0.14, 6]} />
      {mat(COLORS.goldBright)}
    </mesh>
    {/* Cup */}
    <mesh position={[0, 0.28, 0]} castShadow>
      <cylinderGeometry args={[0.06, 0.03, 0.12, 6]} />
      {mat(COLORS.goldBright)}
    </mesh>
  </group>
);

interface PegboardProps {
  position?: [number, number, number];
  width?: number;
  height?: number;
}

export const Pegboard: React.FC<PegboardProps> = ({
  position = [0, 0, 0],
  width = 1.2,
  height = 0.8,
}) => (
  <group position={position}>
    {/* Board */}
    <mesh castShadow>
      <boxGeometry args={[width, height, 0.04]} />
      {mat('#D4874E')}
    </mesh>
    {/* Tool shapes */}
    {[[-0.3, 0.15], [0, 0.1], [0.3, 0.15], [-0.15, -0.15], [0.15, -0.15]].map(([tx, ty], i) => (
      <mesh key={i} position={[tx, ty, 0.03]}>
        <boxGeometry args={[0.08, 0.18, 0.02]} />
        {mat(i % 2 === 0 ? COLORS.metal : COLORS.metalDark)}
      </mesh>
    ))}
  </group>
);

interface LaptopProps {
  position?: [number, number, number];
}

export const Laptop: React.FC<LaptopProps> = ({
  position = [0, 0, 0],
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.laptop.path);
  const s = MODEL_CATALOG.laptop.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface FruitBowlProps {
  position?: [number, number, number];
}

export const FruitBowl: React.FC<FruitBowlProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 0.04, 0]} castShadow>
      <cylinderGeometry args={[0.1, 0.07, 0.06, 6]} />
      {mat(COLORS.white)}
    </mesh>
    {/* Fruits */}
    <mesh position={[-0.03, 0.1, 0]} castShadow>
      <sphereGeometry args={[0.035, 5, 4]} />
      {mat('#EF4444')}
    </mesh>
    <mesh position={[0.03, 0.09, 0.02]} castShadow>
      <sphereGeometry args={[0.03, 5, 4]} />
      {mat('#F59E0B')}
    </mesh>
    <mesh position={[0, 0.1, -0.02]} castShadow>
      <sphereGeometry args={[0.03, 5, 4]} />
      {mat('#22C55E')}
    </mesh>
  </group>
);

interface PenHolderProps {
  position?: [number, number, number];
}

export const PenHolder: React.FC<PenHolderProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 0.04, 0]} castShadow>
      <cylinderGeometry args={[0.03, 0.025, 0.08, 6]} />
      {mat(COLORS.metal)}
    </mesh>
    {/* Pens */}
    <mesh position={[0.01, 0.1, 0]} castShadow rotation={[0, 0, 0.1]}>
      <cylinderGeometry args={[0.005, 0.005, 0.1, 4]} />
      {mat('#1E3A8A')}
    </mesh>
    <mesh position={[-0.01, 0.1, 0.01]} castShadow rotation={[0.1, 0, -0.1]}>
      <cylinderGeometry args={[0.005, 0.005, 0.1, 4]} />
      {mat(COLORS.fabric.red)}
    </mesh>
  </group>
);

interface CushionProps {
  position?: [number, number, number];
  color?: string;
}

export const Cushion: React.FC<CushionProps> = ({
  position = [0, 0, 0],
  color = COLORS.fabric.red,
}) => (
  <mesh position={position} castShadow>
    <boxGeometry args={[0.2, 0.08, 0.2]} />
    {mat(color)}
  </mesh>
);

interface WindowOpeningProps {
  position?: [number, number, number];
  width?: number;
  height?: number;
}

export const WindowOpening: React.FC<WindowOpeningProps> = ({
  position = [0, 0, 0],
  width = 0.5,
  height = 0.4,
}) => (
  <group position={position}>
    {/* Window pane */}
    <mesh>
      <boxGeometry args={[width, height, 0.02]} />
      <meshStandardMaterial color={COLORS.glass} transparent opacity={0.4} />
    </mesh>
    {/* Frame */}
    <mesh position={[0, 0, 0.01]}>
      <boxGeometry args={[width + 0.04, 0.03, 0.02]} />
      {mat(COLORS.white)}
    </mesh>
    <mesh position={[0, 0, 0.01]}>
      <boxGeometry args={[0.03, height + 0.04, 0.02]} />
      {mat(COLORS.white)}
    </mesh>
  </group>
);

interface WallSconceProps {
  position?: [number, number, number];
  on?: boolean;
}

export const WallSconce: React.FC<WallSconceProps> = ({
  position = [0, 0, 0],
  on = true,
}) => (
  <group position={position}>
    <mesh castShadow>
      <boxGeometry args={[0.08, 0.1, 0.06]} />
      {mat(COLORS.metal)}
    </mesh>
    {on && (
      <pointLight
        position={[0, 0, 0.08]}
        intensity={0.15}
        distance={1.5}
        color="#FFF5D0"
      />
    )}
  </group>
);

interface DiningTableProps {
  position?: [number, number, number];
  chairs?: number;
}

export const DiningTable: React.FC<DiningTableProps> = ({
  position = [0, 0, 0],
  chairs = 4,
}) => (
  <group position={position}>
    <Table position={[0, 0, 0]} size={[1.2, 0.8]} height={0.75} />
    {chairs >= 2 && (
      <>
        <Chair position={[-0.4, 0, 0.55]} />
        <Chair position={[0.4, 0, 0.55]} />
      </>
    )}
    {chairs >= 4 && (
      <>
        <Chair position={[-0.4, 0, -0.55]} />
        <Chair position={[0.4, 0, -0.55]} />
      </>
    )}
  </group>
);

interface CanopyProps {
  position?: [number, number, number];
  width?: number;
  depth?: number;
}

export const Canopy: React.FC<CanopyProps> = ({
  position = [0, 0, 0],
  width = 4,
  depth = 1.2,
}) => (
  <group position={position}>
    {/* Roof */}
    <mesh position={[0, 2.2, 0]} castShadow>
      <boxGeometry args={[width, 0.06, depth]} />
      {mat(COLORS.metal)}
    </mesh>
    {/* Support poles */}
    {[-width/2 + 0.1, width/2 - 0.1].map((px, i) => (
      <mesh key={i} position={[px, 1.1, 0]} castShadow>
        <cylinderGeometry args={[0.03, 0.03, 2.2, 6]} />
        {mat(COLORS.metalDark)}
      </mesh>
    ))}
  </group>
);

interface DepartureBoardProps {
  position?: [number, number, number];
  filled?: boolean;
}

export const DepartureBoard: React.FC<DepartureBoardProps> = ({
  position = [0, 0, 0],
  filled = false,
}) => (
  <group position={position}>
    {/* Board */}
    <mesh position={[0, 1.8, 0]} castShadow>
      <boxGeometry args={[0.8, 0.5, 0.06]} />
      {mat('#2A2A2A')}
    </mesh>
    {/* Screen area */}
    <mesh position={[0, 1.8, 0.035]}>
      <boxGeometry args={[0.7, 0.4, 0.01]} />
      {mat('#1A2030')}
    </mesh>
    {/* Text lines */}
    {[0.1, 0, -0.1].map((ty, i) => (
      <mesh key={i} position={[-0.1, 1.8 + ty, 0.04]}>
        <boxGeometry args={[filled ? 0.4 : 0.3 - i * 0.05, 0.03, 0.005]} />
        {mat(i === 0 ? '#FBBF24' : i === 1 ? '#7DD3FC' : '#4ADE80')}
      </mesh>
    ))}
    {/* Pole */}
    <mesh position={[0, 0.75, 0]} castShadow>
      <cylinderGeometry args={[0.025, 0.025, 1.5, 6]} />
      {mat(COLORS.metalDark)}
    </mesh>
  </group>
);

interface BackpackProps {
  position?: [number, number, number];
  color?: string;
}

export const Backpack: React.FC<BackpackProps> = ({
  position = [0, 0, 0],
  color = COLORS.fabric.navy,
}) => (
  <group position={position}>
    <mesh position={[0, 0.12, 0]} castShadow>
      <boxGeometry args={[0.16, 0.22, 0.1]} />
      {mat(color)}
    </mesh>
    {/* Pocket */}
    <mesh position={[0, 0.06, 0.055]}>
      <boxGeometry args={[0.12, 0.1, 0.02]} />
      {mat(color === COLORS.fabric.navy ? '#2563EB' : COLORS.metalDark)}
    </mesh>
  </group>
);

interface PassportProps {
  position?: [number, number, number];
}

export const Passport: React.FC<PassportProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 0.015, 0]} castShadow>
      <boxGeometry args={[0.08, 0.02, 0.1]} />
      {mat('#1E40AF')}
    </mesh>
    {/* Emblem */}
    <mesh position={[0, 0.026, 0]}>
      <cylinderGeometry args={[0.02, 0.02, 0.002, 6]} />
      {mat(COLORS.gold)}
    </mesh>
  </group>
);

interface SignalProps {
  position?: [number, number, number];
  color?: 'green' | 'red';
}

export const Signal: React.FC<SignalProps> = ({
  position = [0, 0, 0],
  color = 'green',
}) => (
  <group position={position}>
    <mesh position={[0, 0.6, 0]} castShadow>
      <cylinderGeometry args={[0.015, 0.015, 1.2, 6]} />
      {mat(COLORS.metalDark)}
    </mesh>
    <mesh position={[0, 1.25, 0]} castShadow>
      <sphereGeometry args={[0.05, 6, 5]} />
      <meshStandardMaterial
        color={color === 'green' ? '#22CC22' : '#CC2222'}
        emissive={color === 'green' ? '#22CC22' : '#CC2222'}
        emissiveIntensity={0.3}
      />
    </mesh>
  </group>
);

interface BenchProps {
  position?: [number, number, number];
}

export const Bench: React.FC<BenchProps> = ({
  position = [0, 0, 0],
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.bench.path);
  const s = MODEL_CATALOG.bench.scale;
  return (
    <group position={position} scale={[s, s, s]}>
      <primitive object={scene} />
    </group>
  );
};

interface PlaneShapeProps {
  position?: [number, number, number];
  scale?: number;
}

export const PlaneShape: React.FC<PlaneShapeProps> = ({
  position = [0, 0, 0],
  scale = 1,
}) => (
  <group position={position} scale={[scale, scale, scale]}>
    {/* Fuselage */}
    <mesh position={[0, 0, 0]} castShadow rotation={[0, 0, Math.PI / 2]}>
      <cylinderGeometry args={[0.08, 0.08, 0.8, 6]} />
      {mat(COLORS.white)}
    </mesh>
    {/* Wings */}
    <mesh position={[0, 0, 0]} castShadow>
      <boxGeometry args={[0.15, 0.02, 0.7]} />
      {mat(COLORS.white)}
    </mesh>
    {/* Tail */}
    <mesh position={[-0.35, 0.06, 0]} castShadow>
      <boxGeometry args={[0.1, 0.15, 0.02]} />
      {mat(COLORS.white)}
    </mesh>
    <mesh position={[-0.35, 0, 0]} castShadow>
      <boxGeometry args={[0.08, 0.02, 0.2]} />
      {mat(COLORS.white)}
    </mesh>
  </group>
);

interface OverheadBridgeProps {
  position?: [number, number, number];
  width?: number;
}

export const OverheadBridge: React.FC<OverheadBridgeProps> = ({
  position = [0, 0, 0],
  width = 4,
}) => (
  <group position={position}>
    {/* Bridge deck */}
    <mesh position={[0, 2.5, 0]} castShadow>
      <boxGeometry args={[width, 0.06, 0.6]} />
      {mat(COLORS.metal)}
    </mesh>
    {/* Support pillars */}
    {[-width/2 + 0.1, width/2 - 0.1].map((px, i) => (
      <mesh key={i} position={[px, 1.25, 0]} castShadow>
        <boxGeometry args={[0.08, 2.5, 0.08]} />
        {mat(COLORS.metalDark)}
      </mesh>
    ))}
    {/* Railings */}
    <mesh position={[0, 2.65, -0.28]}>
      <boxGeometry args={[width, 0.3, 0.02]} />
      {mat(COLORS.metal)}
    </mesh>
    <mesh position={[0, 2.65, 0.28]}>
      <boxGeometry args={[width, 0.3, 0.02]} />
      {mat(COLORS.metal)}
    </mesh>
  </group>
);

interface LampPostProps {
  position?: [number, number, number];
}

export const LampPost: React.FC<LampPostProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 1.0, 0]} castShadow>
      <cylinderGeometry args={[0.025, 0.03, 2.0, 6]} />
      {mat('#444444')}
    </mesh>
    <mesh position={[0, 2.05, 0]} castShadow>
      <boxGeometry args={[0.2, 0.1, 0.12]} />
      {mat('#444444')}
    </mesh>
    <pointLight
      position={[0, 1.95, 0]}
      intensity={0.2}
      distance={2}
      color="#FFF5D0"
    />
  </group>
);

/* ═══════════════════════════════════════════
   EFFECTS
   ═══════════════════════════════════════════ */

interface CelebrationBurstProps {
  position?: [number, number, number];
}

export const CelebrationBurst: React.FC<CelebrationBurstProps> = ({
  position = [0, 2, 0],
}) => {
  const ref = useRef<THREE.Group>(null);
  const particles = useMemo(() => {
    const colors = ['#EF4444', '#FBBF24', '#3B82F6', '#22C55E', '#EC4899', '#F59E0B'];
    return Array.from({ length: 30 }).map((_, i) => ({
      x: (Math.random() - 0.5) * 0.1,
      y: Math.random() * 0.1,
      z: (Math.random() - 0.5) * 0.1,
      vx: (Math.random() - 0.5) * 3,
      vy: Math.random() * 3 + 1,
      vz: (Math.random() - 0.5) * 3,
      color: colors[i % colors.length],
      size: 0.04 + Math.random() * 0.04,
    }));
  }, []);

  useFrame((_, dt) => {
    if (!ref.current) return;
    ref.current.children.forEach((child, i) => {
      const p = particles[i];
      child.position.x += p.vx * dt;
      child.position.y += p.vy * dt;
      child.position.z += p.vz * dt;
      p.vy -= 4 * dt; // gravity
      child.rotation.x += dt * 3;
      child.rotation.z += dt * 2;
      const m = (child as THREE.Mesh).material as THREE.MeshStandardMaterial;
      if (m) m.opacity = Math.max(0, m.opacity - dt * 0.5);
    });
  });

  return (
    <group position={position} ref={ref}>
      {particles.map((p, i) => (
        <mesh key={i} position={[p.x, p.y, p.z]}>
          <boxGeometry args={[p.size, p.size, p.size]} />
          <meshStandardMaterial color={p.color} transparent opacity={1} />
        </mesh>
      ))}
    </group>
  );
};

interface GoldenOverlayProps {
  active: boolean;
}

export const GoldenOverlay: React.FC<GoldenOverlayProps> = ({ active }) => {
  const lightRef = useRef<THREE.AmbientLight>(null);
  useFrame(() => {
    if (!lightRef.current) return;
    const target = active ? 0.4 : 0;
    lightRef.current.intensity += (target - lightRef.current.intensity) * 0.05;
  });

  return (
    <>
      <ambientLight ref={lightRef} color="#FFD080" intensity={0} />
      {active && <fog attach="fog" args={['#FFF0D0', 15, 30]} />}
    </>
  );
};

/* ═══════════════════════════════════════════
   EXTRA SCENE ELEMENTS
   ═══════════════════════════════════════════ */

interface GardenGnomeProps {
  position?: [number, number, number];
}

export const GardenGnome: React.FC<GardenGnomeProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    {/* Body */}
    <mesh position={[0, 0.1, 0]} castShadow>
      <cylinderGeometry args={[0.06, 0.07, 0.2, 6]} />
      {mat('#3B82F6')}
    </mesh>
    {/* Head */}
    <mesh position={[0, 0.25, 0]} castShadow>
      <sphereGeometry args={[0.05, 5, 4]} />
      {mat(COLORS.skin)}
    </mesh>
    {/* Hat */}
    <mesh position={[0, 0.35, 0]} castShadow>
      <coneGeometry args={[0.05, 0.12, 5]} />
      {mat('#EF4444')}
    </mesh>
  </group>
);

interface BirdBathProps {
  position?: [number, number, number];
}

export const BirdBath: React.FC<BirdBathProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    {/* Pedestal */}
    <mesh position={[0, 0.25, 0]} castShadow>
      <cylinderGeometry args={[0.03, 0.05, 0.5, 6]} />
      {mat('#A0A0A0')}
    </mesh>
    {/* Basin */}
    <mesh position={[0, 0.52, 0]} castShadow>
      <cylinderGeometry args={[0.12, 0.08, 0.06, 8]} />
      {mat('#B0B0B0')}
    </mesh>
    {/* Water */}
    <mesh position={[0, 0.56, 0]}>
      <cylinderGeometry args={[0.1, 0.1, 0.02, 8]} />
      <meshStandardMaterial color="#38BDF8" transparent opacity={0.5} />
    </mesh>
  </group>
);

interface FlowerBoxProps {
  position?: [number, number, number];
}

export const FlowerBox: React.FC<FlowerBoxProps> = ({
  position = [0, 0, 0],
}) => {
  const flowerColors = ['#EF4444', '#F59E0B', '#EC4899', '#A855F7'];
  return (
    <group position={position}>
      {/* Box */}
      <mesh position={[0, 0, 0]} castShadow>
        <boxGeometry args={[0.3, 0.06, 0.08]} />
        {mat('#D4733D')}
      </mesh>
      {/* Flowers */}
      {flowerColors.map((c, i) => (
        <mesh key={i} position={[(i - 1.5) * 0.06, 0.05, 0]}>
          <sphereGeometry args={[0.025, 4, 4]} />
          {mat(c)}
        </mesh>
      ))}
    </group>
  );
};

interface ToolboxProps {
  position?: [number, number, number];
}

export const Toolbox: React.FC<ToolboxProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 0.05, 0]} castShadow>
      <boxGeometry args={[0.2, 0.1, 0.12]} />
      {mat('#EF4444')}
    </mesh>
    <mesh position={[0, 0.11, 0]} castShadow>
      <boxGeometry args={[0.12, 0.02, 0.04]} />
      {mat(COLORS.metalDark)}
    </mesh>
  </group>
);

interface EquipmentCabinetProps {
  position?: [number, number, number];
}

export const EquipmentCabinet: React.FC<EquipmentCabinetProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 0.5, 0]} castShadow>
      <boxGeometry args={[0.5, 1.0, 0.35]} />
      {mat('#666666')}
    </mesh>
    {/* Doors */}
    <mesh position={[-0.08, 0.5, 0.18]}>
      <boxGeometry args={[0.2, 0.9, 0.01]} />
      {mat('#777777')}
    </mesh>
    <mesh position={[0.08, 0.5, 0.18]}>
      <boxGeometry args={[0.2, 0.9, 0.01]} />
      {mat('#777777')}
    </mesh>
    {/* Handles */}
    {[-0.02, 0.02].map((hx, i) => (
      <mesh key={i} position={[hx, 0.5, 0.2]}>
        <boxGeometry args={[0.01, 0.1, 0.01]} />
        {mat('#AAAAAA')}
      </mesh>
    ))}
  </group>
);

interface GoldenEnvelopeProps {
  position?: [number, number, number];
}

export const GoldenEnvelope: React.FC<GoldenEnvelopeProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 0.015, 0]} castShadow>
      <boxGeometry args={[0.14, 0.02, 0.1]} />
      {mat(COLORS.gold)}
    </mesh>
    {/* Seal */}
    <mesh position={[0, 0.026, 0]}>
      <cylinderGeometry args={[0.02, 0.02, 0.003, 6]} />
      {mat('#DC2626')}
    </mesh>
  </group>
);

interface CurtainProps {
  position?: [number, number, number];
  height?: number;
  side?: 'left' | 'right';
}

export const Curtain: React.FC<CurtainProps> = ({
  position = [0, 0, 0],
  height = 2.5,
  side = 'left',
}) => (
  <group position={position}>
    <mesh position={[0, height / 2, 0]} castShadow>
      <boxGeometry args={[0.15, height, 0.06]} />
      {mat(COLORS.curtainRed)}
    </mesh>
    <mesh position={[side === 'left' ? 0.06 : -0.06, height / 2, 0]}>
      <boxGeometry args={[0.04, height, 0.06]} />
      {mat('#991B1B')}
    </mesh>
  </group>
);

interface HedgeProps {
  position?: [number, number, number];
  width?: number;
}

export const Hedge: React.FC<HedgeProps> = ({
  position = [0, 0, 0],
  width = 0.6,
}) => {
  const scene = useKenneyModel(MODEL_CATALOG.hedge.path, { colorOverride: '#22C55E' });
  const baseScale = MODEL_CATALOG.hedge.scale;
  const sx = baseScale * (width / 0.6);
  return (
    <group position={[position[0], 0, position[2]]} scale={[sx, baseScale, baseScale]}>
      <primitive object={scene} />
    </group>
  );
};

interface StringLightsProps {
  position?: [number, number, number];
  length?: number;
  count?: number;
}

export const StringLights: React.FC<StringLightsProps> = ({
  position = [0, 0, 0],
  length = 3,
  count = 8,
}) => {
  const ref = useRef<THREE.Group>(null);

  // Twinkle animation — pulse emissive intensity
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime();
    ref.current.children.forEach((child, i) => {
      const m = (child as THREE.Mesh).material as THREE.MeshStandardMaterial;
      if (m && m.emissiveIntensity !== undefined) {
        m.emissiveIntensity = 0.2 + Math.sin(t * 3 + i * 1.2) * 0.15;
      }
    });
  });

  return (
    <group position={position} ref={ref}>
      {Array.from({ length: count }).map((_, i) => {
        const x = (i / (count - 1)) * length - length / 2;
        const y = Math.sin((i / (count - 1)) * Math.PI) * -0.08;
        return (
          <mesh key={i} position={[x, y, 0]}>
            <sphereGeometry args={[0.02, 4, 4]} />
            <meshStandardMaterial
              color="#FFF5D0"
              emissive="#FFF5D0"
              emissiveIntensity={0.3}
            />
          </mesh>
        );
      })}
    </group>
  );
};

interface ExamPaperProps {
  position?: [number, number, number];
}

export const ExamPaper: React.FC<ExamPaperProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh position={[0, 0.005, 0]} castShadow>
      <boxGeometry args={[0.12, 0.005, 0.16]} />
      {mat(COLORS.paper)}
    </mesh>
    {/* Lines */}
    {[-0.04, -0.02, 0, 0.02, 0.04].map((z, i) => (
      <mesh key={i} position={[-0.01, 0.009, z]}>
        <boxGeometry args={[0.08, 0.001, 0.005]} />
        {mat('#C0C0D0')}
      </mesh>
    ))}
  </group>
);

interface ResultsBoardProps {
  position?: [number, number, number];
  strips?: number;
}

export const ResultsBoard: React.FC<ResultsBoardProps> = ({
  position = [0, 0, 0],
  strips = 3,
}) => {
  const stripColors = ['#FBBF24', '#3B82F6', '#C0C0C0', '#CD7F32', '#22C55E', '#EF4444', '#A855F7', '#14B8A6'];
  return (
    <group position={position}>
      {/* Board frame */}
      <mesh castShadow>
        <boxGeometry args={[1.0, 0.7, 0.04]} />
        {mat(COLORS.woodDark)}
      </mesh>
      {/* Inner */}
      <mesh position={[0, 0, 0.025]}>
        <boxGeometry args={[0.9, 0.6, 0.01]} />
        {mat(COLORS.paper)}
      </mesh>
      {/* Title bar */}
      <mesh position={[0, 0.2, 0.03]}>
        <boxGeometry args={[0.5, 0.06, 0.005]} />
        {mat('#1E293B')}
      </mesh>
      {/* Result strips */}
      {Array.from({ length: Math.min(strips, 8) }).map((_, i) => (
        <mesh key={i} position={[(i % 2 === 0 ? -0.1 : 0.1), 0.1 - i * 0.06, 0.03]}>
          <boxGeometry args={[0.3 + Math.random() * 0.15, 0.035, 0.005]} />
          {mat(stripColors[i % stripColors.length])}
        </mesh>
      ))}
    </group>
  );
};

interface FluorescentLightProps {
  position?: [number, number, number];
}

export const FluorescentLight: React.FC<FluorescentLightProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh castShadow>
      <boxGeometry args={[0.5, 0.04, 0.08]} />
      {mat('#E0E0E0')}
    </mesh>
    <mesh position={[0, -0.03, 0]}>
      <boxGeometry args={[0.45, 0.02, 0.06]} />
      <meshStandardMaterial color="#F0F0FF" emissive="#F0F0FF" emissiveIntensity={0.1} />
    </mesh>
  </group>
);

interface GateProps {
  position?: [number, number, number];
}

export const Gate: React.FC<GateProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    {/* Posts */}
    {[-0.6, 0.6].map((px, i) => (
      <group key={i}>
        <mesh position={[px, 0.6, 0]} castShadow>
          <boxGeometry args={[0.12, 1.2, 0.12]} />
          {mat(COLORS.stoneDark)}
        </mesh>
        {/* Cap */}
        <mesh position={[px, 1.25, 0]} castShadow>
          <coneGeometry args={[0.08, 0.12, 4]} />
          {mat(COLORS.stoneDark)}
        </mesh>
      </group>
    ))}
    {/* Bars */}
    <mesh position={[0, 0.95, 0]}>
      <boxGeometry args={[1.1, 0.03, 0.03]} />
      {mat(COLORS.metalDark)}
    </mesh>
    {[-0.4, -0.2, 0, 0.2, 0.4].map((bx, i) => (
      <mesh key={i} position={[bx, 0.55, 0]}>
        <boxGeometry args={[0.02, 0.8, 0.02]} />
        {mat(COLORS.metalDark)}
      </mesh>
    ))}
    {[-0.4, -0.2, 0, 0.2, 0.4].map((bx, i) => (
      <mesh key={`f${i}`} position={[bx, 0.98, 0]} castShadow>
        <coneGeometry args={[0.02, 0.06, 4]} />
        {mat(COLORS.metalDark)}
      </mesh>
    ))}
  </group>
);

interface NoticeboardProps {
  position?: [number, number, number];
}

export const Noticeboard: React.FC<NoticeboardProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    <mesh castShadow>
      <boxGeometry args={[0.4, 0.3, 0.03]} />
      {mat(COLORS.wood)}
    </mesh>
    {/* Cork board */}
    <mesh position={[0, 0, 0.02]}>
      <boxGeometry args={[0.35, 0.25, 0.01]} />
      {mat('#D4874E')}
    </mesh>
    {/* Notes */}
    <mesh position={[-0.08, 0.04, 0.03]}>
      <boxGeometry args={[0.06, 0.06, 0.003]} />
      {mat('#FEFCE8')}
    </mesh>
    <mesh position={[0.06, -0.02, 0.03]}>
      <boxGeometry args={[0.05, 0.05, 0.003]} />
      {mat('#DCFCE7')}
    </mesh>
  </group>
);

/* Graduation cap - sits on a person's head */
interface GraduationCapProps {
  position?: [number, number, number];
}

export const GraduationCap: React.FC<GraduationCapProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    {/* Board */}
    <mesh position={[0, 0.02, 0]} castShadow>
      <boxGeometry args={[0.2, 0.02, 0.2]} />
      {mat('#1E1B4B')}
    </mesh>
    {/* Cap body */}
    <mesh position={[0, -0.02, 0]} castShadow>
      <cylinderGeometry args={[0.07, 0.08, 0.06, 6]} />
      {mat('#1E1B4B')}
    </mesh>
    {/* Tassel */}
    <mesh position={[0.1, 0.02, 0]} castShadow>
      <sphereGeometry args={[0.012, 4, 4]} />
      {mat(COLORS.gold)}
    </mesh>
  </group>
);

interface CheckInDeskProps {
  position?: [number, number, number];
}

export const CheckInDesk: React.FC<CheckInDeskProps> = ({
  position = [0, 0, 0],
}) => (
  <group position={position}>
    {/* Counter */}
    <mesh position={[0, 0.5, 0]} castShadow>
      <boxGeometry args={[0.5, 0.1, 0.3]} />
      {mat(COLORS.metalDark)}
    </mesh>
    <mesh position={[0, 0.25, 0]} castShadow>
      <boxGeometry args={[0.45, 0.5, 0.25]} />
      {mat(COLORS.metal)}
    </mesh>
    {/* Screen */}
    <mesh position={[0, 0.7, -0.05]} rotation={[0.2, 0, 0]}>
      <boxGeometry args={[0.2, 0.14, 0.01]} />
      {mat('#1A2030')}
    </mesh>
  </group>
);

interface ObservationDeckProps {
  position?: [number, number, number];
  width?: number;
}

export const ObservationDeck: React.FC<ObservationDeckProps> = ({
  position = [0, 0, 0],
  width = 4,
}) => (
  <group position={position}>
    {/* Deck floor */}
    <mesh position={[0, 0, 0]} castShadow receiveShadow>
      <boxGeometry args={[width, 0.06, 1]} />
      {mat(COLORS.concrete)}
    </mesh>
    {/* Railing */}
    <mesh position={[0, 0.3, 0.48]}>
      <boxGeometry args={[width, 0.02, 0.02]} />
      {mat(COLORS.metal)}
    </mesh>
    <mesh position={[0, 0.15, 0.48]}>
      <boxGeometry args={[width, 0.02, 0.02]} />
      {mat(COLORS.metal)}
    </mesh>
    {/* Railing posts */}
    {Array.from({ length: Math.floor(width / 0.5) + 1 }).map((_, i) => (
      <mesh key={i} position={[-width/2 + i * 0.5, 0.15, 0.48]}>
        <boxGeometry args={[0.02, 0.3, 0.02]} />
        {mat(COLORS.metalDark)}
      </mesh>
    ))}
  </group>
);

/* Balloon cluster for party scene — with float animation */
interface BalloonsProps {
  position?: [number, number, number];
}

export const Balloons: React.FC<BalloonsProps> = ({
  position = [0, 0, 0],
}) => {
  const colors = ['#EF4444', '#22C55E', '#3B82F6'];
  const ref = useRef<THREE.Group>(null);

  // Float + drift animation
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime();
    ref.current.position.y = Math.sin(t * 1.5) * 0.06;
    ref.current.rotation.z = Math.sin(t * 0.8) * 0.05;
  });

  return (
    <group position={position}>
      <group ref={ref}>
        {colors.map((c, i) => (
          <group key={i}>
            <mesh position={[(i - 1) * 0.08, 0.3 + i * 0.12, 0]} castShadow>
              <sphereGeometry args={[0.06, 5, 5]} />
              <meshStandardMaterial color={c} transparent opacity={0.8} />
            </mesh>
          </group>
        ))}
      </group>
    </group>
  );
};

/* Bunting for party scene — with wave sway animation */
interface BuntingProps {
  position?: [number, number, number];
  length?: number;
  count?: number;
}

export const Bunting: React.FC<BuntingProps> = ({
  position = [0, 0, 0],
  length = 2,
  count = 10,
}) => {
  const colors = ['#EF4444', '#FBBF24', '#3B82F6', '#22C55E'];
  const ref = useRef<THREE.Group>(null);

  // Wave sway animation — per-flag sine offset
  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime();
    ref.current.children.forEach((child, i) => {
      child.rotation.z = Math.PI + Math.sin(t * 2.5 + i * 0.5) * 0.1;
    });
  });

  return (
    <group position={position} ref={ref}>
      {Array.from({ length: count }).map((_, i) => {
        const x = (i / (count - 1)) * length - length / 2;
        const sag = Math.sin((i / (count - 1)) * Math.PI) * -0.06;
        return (
          <mesh key={i} position={[x, sag, 0]} rotation={[0, 0, Math.PI]}>
            <coneGeometry args={[0.03, 0.06, 3]} />
            {mat(colors[i % colors.length])}
          </mesh>
        );
      })}
    </group>
  );
};

/* Welcome mat */
interface WelcomeMatProps {
  position?: [number, number, number];
}

export const WelcomeMat: React.FC<WelcomeMatProps> = ({
  position = [0, 0, 0],
}) => (
  <mesh position={[position[0], 0.01, position[2]]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
    <planeGeometry args={[0.4, 0.25]} />
    <meshToonMaterial color="#D4874E" gradientMap={toonGradientTexture} />
  </mesh>
);

/* Letterbox / acceptance letter */
interface LetterProps {
  position?: [number, number, number];
  color?: string;
}

export const Letter: React.FC<LetterProps> = ({
  position = [0, 0, 0],
  color = COLORS.paper,
}) => (
  <mesh position={[position[0], position[1] + 0.005, position[2]]} castShadow>
    <boxGeometry args={[0.1, 0.005, 0.07]} />
    {mat(color)}
  </mesh>
);

/* Stars for award decor */
interface StarProps {
  position?: [number, number, number];
  size?: number;
  color?: string;
}

export const Star: React.FC<StarProps> = ({
  position = [0, 0, 0],
  size = 0.06,
  color = COLORS.goldBright,
}) => (
  <mesh position={position} castShadow>
    <coneGeometry args={[size, size * 1.5, 5]} />
    {mat(color)}
  </mesh>
);
